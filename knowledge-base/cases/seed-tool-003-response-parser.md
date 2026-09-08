# 工具响应解析器不兼容

verified: true
synthetic: true
case_id: CASE-T-003
classification: TEST_TOOL

## 症状

服务返回 200，但工具报 `JSON parser error`。

## 关键证据

- 抓包显示响应体为合法 JSON。
- 产品服务日志确认请求成功完成。
- 工具旧版本无法处理新字段的空值。

## 最终根因与验证

测试工具解析器兼容性缺陷。升级工具适配器后相同响应可正确处理。
