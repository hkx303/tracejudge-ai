# API 说明

服务默认监听 `http://localhost:8000`。

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/api/health` | 返回健康状态与知识文档数量 |
| POST | `/api/analyses` | multipart 上传 `.log` / `.txt`，同时传 `sources` JSON 数组和可选 `metadata` JSON 对象 |
| GET | `/api/analyses/{analysis_id}` | 读取已保存的分析结果 |
| POST | `/api/analyses/{analysis_id}/confirmation` | 传入 `classification`、`actual_root_cause`、`confirmed_by`，保存人工确认 |
| POST | `/api/knowledge/reindex` | 重新索引仓库内 Markdown 知识库 |

上传文件和 `sources` 必须一一对应；不支持的扩展名或非法 JSON 返回 HTTP 400，未知分析 ID 返回 HTTP 404。
