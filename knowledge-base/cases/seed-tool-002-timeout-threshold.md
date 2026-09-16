# 工具等待阈值过短

verified: true
synthetic: true
case_id: CASE-T-002
classification: TEST_TOOL

## English summary

The tool timed out at 30 seconds while the device rendered the login page at 35 seconds under the same session ID. Raising the wait to 60 seconds and listening for page readiness fixed it.

## 症状

测试工具在 30 秒记录 `timeout`，设备在第 35 秒记录 `login page rendered`。

## 关键证据

- `sessionId` 在工具和设备日志中一致。
- 页面最终成功加载，未发现产品错误码。
- 延长等待时间后用例通过。

## 最终根因与验证

工具同步策略和超时阈值不匹配。将阈值调整为 60 秒，并监听页面就绪事件后稳定通过。
