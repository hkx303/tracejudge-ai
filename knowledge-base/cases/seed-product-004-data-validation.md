# 服务端业务参数校验错误

verified: true
synthetic: true
case_id: CASE-P-004
classification: PRODUCT_DEVICE

## 症状

订单提交流程返回 `BUSINESS_VALIDATION_FAILED`，页面显示提交失败。

## 关键证据

- 测试工具发出的 JSON 参数与 API 文档一致。
- 服务端日志显示金额字段的精度校验失败。
- 使用相同参数的 curl 请求也失败。

## 最终根因与验证

服务端金额精度规则与公开接口契约不一致。修复服务规则后接口回归通过。
