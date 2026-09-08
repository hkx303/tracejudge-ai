# 固件处理指令时崩溃

verified: true
synthetic: true
case_id: CASE-P-002
classification: PRODUCT_DEVICE

## 症状

设备执行拍照指令后离线，工具最终报等待响应超时。

## 关键证据

- 工具日志确认命令已通过协议层发送成功。
- 设备日志紧接着出现 `FATAL EXCEPTION camera-service` 和重启记录。
- 更换工具仍能稳定复现。

## 最终根因与验证

固件 3.2.1 的相机驱动空指针崩溃。升级至 3.2.2 后连续执行 100 次均未复现。
