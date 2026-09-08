# 重试后未清理会话状态

verified: true
synthetic: true
case_id: CASE-T-004
classification: TEST_TOOL

## 症状

首次失败重试后持续报 `session already exists`，新设备上首次执行正常。

## 关键证据

- 设备服务端没有重复会话。
- 工具日志显示重试前未执行 cleanup。
- 禁用工具重试或手动清理会话后通过。

## 最终根因与验证

工具重试钩子未释放本地会话状态。修复 cleanup 后重试流程恢复正常。
