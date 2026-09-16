# Architecture / 架构

## English

TraceJudge has four layers: browser UI, API, analysis services, and local persistence.

```text
Next.js Web → FastAPI API → Correlator → Parser / Rules / RAG / LLM
                                  ↓
                     SQLite, Chroma, knowledge-base Markdown
```

- `api`: validates HTTP input and exposes analysis, read, confirmation, and reindex operations.
- `parsers`: converts log formats to a shared `Event`; v1 ships a general text parser.
- `correlator`: merges and orders events by time and correlation IDs, then orchestrates rules, RAG, and LLM work.
- `rules`: produces evidence-backed class scores; it never replaces final review.
- `rag`: reads versioned Markdown. With an OpenAI key it uses Chroma and OpenAI embeddings; otherwise it falls back to local keyword matching.
- `llm`: requests OpenAI only when configured; provider failures fall back safely to local conclusions.
- `persistence`: stores redacted analyses and human confirmations in SQLite.

`docker-compose.yml` runs the frontend and backend. Default data volumes remain on the deployment machine.

## 中文

TraceJudge 采用浏览器界面、API、分析服务和本地持久化四层结构。

- `api`：校验 HTTP 输入，提供分析、读取、确认和知识库重建接口。
- `parsers`：将不同日志格式转换为统一 `Event`；v1 内置普通文本解析器。
- `correlator`：按时间和链路标识合并、排序事件，并编排规则、RAG 和 LLM。
- `rules`：输出带证据的分类分数，不替代最终审查。
- `rag`：读取版本化 Markdown；配置 OpenAI 密钥时使用 Chroma 和 OpenAI embedding，否则回退到本地关键词匹配。
- `llm`：仅在已配置时请求 OpenAI；服务故障时安全回退到本地结论。
- `persistence`：将脱敏分析结果和人工确认存储到 SQLite。

`docker-compose.yml` 用于启动前后端，默认数据卷仅保留在部署机器。
