# 案例库规范

此目录包含可供 RAG 检索的历史故障案例。当前 `seed-*` 文件均为**合成案例**，仅用于本地演示、检索与回归测试；它们不是生产事故记录。

每个可作为高可信召回依据的案例必须包含：

```text
verified: true
synthetic: true | false
case_id: CASE-XXXX
classification: PRODUCT_DEVICE | TEST_TOOL | ENVIRONMENT | UNKNOWN
```

同时记录症状、关键证据、排除过程、最终根因和验证方式。新增真实案例前必须完成脱敏，并由负责人确认后才可设置 `verified: true`。
