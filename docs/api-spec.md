# API specification / API 说明

## English

The service listens on `http://localhost:8000` by default.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Returns health state and knowledge-document count |
| POST | `/api/analyses` | Multipart upload of `.log` / `.txt`; accepts a `sources` JSON array and optional `metadata` JSON object |
| GET | `/api/analyses/{analysis_id}` | Reads a saved analysis |
| POST | `/api/analyses/{analysis_id}/confirmation` | Saves `classification`, `actual_root_cause`, and `confirmed_by` as human confirmation |
| POST | `/api/knowledge/reindex` | Reindexes repository Markdown knowledge |

Every upload file needs one matching source value. Unsupported extensions and invalid JSON return HTTP 400; an unknown analysis ID returns HTTP 404.

## 中文

服务默认监听 `http://localhost:8000`。上传文件和 `sources` 必须一一对应；不支持的扩展名或非法 JSON 返回 HTTP 400，未知分析 ID 返回 HTTP 404。接口用途与英文表格一致。
