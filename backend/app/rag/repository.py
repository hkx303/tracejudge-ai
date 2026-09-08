from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from ..models import KnowledgeHit

ROOT = Path(__file__).resolve().parents[3]
KB_ROOT = ROOT / "knowledge-base"


@dataclass
class Document:
    document_id: str
    path: str
    title: str
    text: str
    verified_case: bool


class RepositoryKnowledgeBase:
    """Markdown RAG source with a safe dependency-free fallback."""
    def __init__(self) -> None:
        self.documents: list[Document] = []
        self.collection = None
        # Chroma uses OpenAI embeddings only with an explicit key. Otherwise this
        # tool stays entirely local and falls back to lexical matching.
        if os.getenv("OPENAI_API_KEY"):
            try:
                import chromadb
                from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
                client = chromadb.PersistentClient(path=str(ROOT / "backend" / "chroma"))
                self.collection = client.get_or_create_collection(
                    "tracejudge_knowledge",
                    embedding_function=OpenAIEmbeddingFunction(api_key=os.environ["OPENAI_API_KEY"], model_name="text-embedding-3-small"),
                )
            except Exception:
                self.collection = None
        self.reindex()

    def reindex(self) -> int:
        self.documents = []
        for path in KB_ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            title = next((line.removeprefix("# ").strip() for line in text.splitlines() if line.startswith("# ")), path.stem)
            relative = str(path.relative_to(ROOT))
            self.documents.append(Document(relative, relative, title, text, "verified: true" in text.lower()))
        if self.collection:
            self.collection.upsert(
                ids=[doc.document_id for doc in self.documents],
                documents=[doc.text for doc in self.documents],
                metadatas=[{"path": doc.path, "title": doc.title, "verified_case": str(doc.verified_case)} for doc in self.documents],
            )
        return len(self.documents)

    def search(self, query: str, limit: int = 4) -> list[KnowledgeHit]:
        if self.collection and query.strip():
            try:
                results = self.collection.query(query_texts=[query], n_results=min(limit, len(self.documents)), include=["documents", "metadatas", "distances"])
                return [KnowledgeHit(document_id=doc_id, path=meta["path"], title=meta["title"], excerpt=document[:500].strip(), score=round(1 / (1 + distance), 3), verified_case=meta["verified_case"] == "True") for doc_id, document, meta, distance in zip(results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0])]
            except Exception:
                pass
        terms = {word for word in re.findall(r"[\w-]{3,}", query.lower()) if word not in {"error", "warning", "info"}}
        scored: list[tuple[float, Document]] = []
        for doc in self.documents:
            lowered = doc.text.lower()
            matched = sum(1 for term in terms if term in lowered)
            if matched:
                boost = 0.25 if doc.verified_case else 0.0
                scored.append(((matched / max(len(terms), 1)) + boost, doc))
        return [KnowledgeHit(document_id=doc.document_id, path=doc.path, title=doc.title, excerpt=doc.text[:500].strip(), score=round(score, 3), verified_case=doc.verified_case) for score, doc in sorted(scored, reverse=True, key=lambda item: item[0])[:limit]]
