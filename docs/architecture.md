# 架构

TraceJudge 采用浏览器、API、分析服务和本地持久化四层结构。

```text
Next.js Web → FastAPI API → Correlator → Parser / Rules / RAG / LLM
                                  ↓
                     SQLite、Chroma、知识库 Markdown
```

- `api`：校验 HTTP 输入、提供分析、读取、确认和知识库重建接口。
- `parsers`：将不同日志格式转换为统一 `Event`。v1 实现普通文本解析器。
- `correlator`：合并事件、按时间与链路标识排序，编排规则、RAG 和 LLM。
- `rules`：输出带证据的分类分数；不承担最终审查职责。
- `rag`：读取版本化 Markdown；有 OpenAI 密钥时使用 Chroma 与 OpenAI embedding，否则使用可解释的本地关键词回退。
- `llm`：仅在配置密钥时请求 OpenAI；服务故障时回退本地结论。
- `persistence`：SQLite 持久化脱敏后的分析和人工确认。

容器部署通过 `docker-compose.yml` 启动前端和后端。默认数据卷仅保留在部署机器。
