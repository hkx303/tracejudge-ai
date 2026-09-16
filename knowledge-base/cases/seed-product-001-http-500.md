# 登录接口 HTTP 500

verified: true
synthetic: true
case_id: CASE-P-001
classification: PRODUCT_DEVICE

## English summary

The login API returned HTTP 500 after the tool sent the request. Matching request IDs and a manual API reproduction confirmed database connection-pool exhaustion; fix the service configuration and retry.

## 症状

自动化点击登录后失败，工具记录 `requestId=req-101`，服务返回 `HTTP 500 Internal Server Error`。

## 关键证据

- 工具日志显示请求已成功发送。
- 服务日志中同一 `requestId` 出现 `INTERNAL_SERVER_ERROR`。
- 手工调用同一接口得到相同响应。

## 最终根因与验证

认证服务数据库连接池耗尽。重启服务并修复连接池配置后，手工和自动化登录均通过。
