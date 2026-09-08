from pathlib import Path

from app.rag.repository import RepositoryKnowledgeBase
from app.models import Classification, Source
from app.correlator.service import Analyzer

ROOT = Path(__file__).resolve().parents[2]


def run_sample(folder: str, mappings: list[tuple[str, Source]]):
    files = [(name, source, (ROOT / "sample-data" / folder / name).read_text()) for name, source in mappings]
    return Analyzer(RepositoryKnowledgeBase()).analyze(files)


def test_product_device_sample():
    result = run_sample("product-device", [("tool.log", Source.TEST_TOOL), ("service.log", Source.PRODUCT_SERVICE)])
    assert result.classification == Classification.PRODUCT_DEVICE
    assert result.evidence and result.recommended_actions


def test_test_tool_sample():
    result = run_sample("test-tool", [("tool.log", Source.TEST_TOOL), ("device.log", Source.DEVICE)])
    assert result.classification == Classification.TEST_TOOL
    assert any(hit.verified_case for hit in result.knowledge_hits)


def test_environment_sample():
    result = run_sample("environment", [("environment.log", Source.ENVIRONMENT)])
    assert result.classification == Classification.ENVIRONMENT


def test_unknown_sample():
    result = run_sample("unknown", [("unknown.log", Source.TEST_TOOL)])
    assert result.classification == Classification.UNKNOWN


def test_seed_cases_are_verified_and_cover_every_classification():
    cases = (ROOT / "knowledge-base" / "cases")
    seed_files = list(cases.glob("seed-*.md"))
    content = "\n".join(path.read_text() for path in seed_files)
    assert len(seed_files) == 14
    assert content.count("verified: true") == 14
    for classification in Classification:
        assert f"classification: {classification.value}" in content
