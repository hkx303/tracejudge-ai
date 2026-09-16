# Data model / 数据模型

## English

### Event

An event contains `event_id`, `file_name`, `source`, `line_number`, raw text, an optional timestamp, level, error code, and correlation IDs: `trace_id`, `request_id`, `session_id`, and `device_id`. Valid sources are `test_tool`, `device`, `product_service`, and `environment`.

### AnalysisResult

An analysis has a stable UUID, optional metadata, classification, confidence, summary, AI status, timeline events, evidence, rule hits, category scores, knowledge hits, counter-evidence, recommended actions, and version-audit fields.

### Confirmation and data handling

A confirmation stores an analysis ID, human-selected classification, actual root cause, and confirmer. Saving it also writes `knowledge-base/cases/<analysis-id>.md` with `verified: true`. SQLite redacts Bearer tokens, explicit tokens, emails, and mainland-China phone numbers; no secret is stored in any model.

## 中文

统一事件包含 `event_id`、`file_name`、`source`、`line_number`、原始文本、可选时间戳、日志等级、错误码和链路标识：`trace_id`、`request_id`、`session_id`、`device_id`。来源只能是 `test_tool`、`device`、`product_service` 或 `environment`。

分析结果包含稳定 UUID、可选元信息、分类、置信度、摘要、AI 状态、时间线事件、日志证据、规则命中、类别分数、知识命中、反证、验证动作和版本审计字段。

确认记录包含分析 ID、人工确认分类、实际根因、确认人。保存时同步生成 `knowledge-base/cases/<analysis-id>.md` 并标记 `verified: true`。SQLite 会脱敏 Bearer Token、显式 Token、邮箱和中国大陆手机号；密钥不进入任何数据模型。
