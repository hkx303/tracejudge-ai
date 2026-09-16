# Verified case: page loading after tool timeout / 已验证案例：页面加载晚于工具超时

## English summary

The tool reported `Element not found` at 30 seconds, while the device recorded `login page rendered` at 35 seconds. Manual reproduction showed product behavior was normal; increasing the timeout to 60 seconds fixed the test tool.

verified: true

工具在 30 秒时报 `Element not found`，设备日志在第 35 秒记录 `login page rendered`。经手工复现，产品功能正常；将工具等待时间改为 60 秒后通过。

- 归因：`TEST_TOOL`
- 验证：延长超时并通过第二套工具交叉验证。
