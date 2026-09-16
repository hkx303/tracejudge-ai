# 产品版本与设备协议不兼容

verified: true
synthetic: true
case_id: CASE-P-003
classification: PRODUCT_DEVICE

## English summary

Firmware 2.8.0 returned `UNSUPPORTED_PROTOCOL` for a v4 configuration while 2.9.0 worked. Upgrade firmware or downgrade the server protocol.

## 症状

仅固件 2.8.0 的设备在下发新配置时返回 `UNSUPPORTED_PROTOCOL`。

## 关键证据

- 同一工具、同一脚本在固件 2.9.0 正常通过。
- 设备协议日志返回明确错误码。
- 发布说明指出 2.8.0 不支持配置协议 v4。

## 最终根因与验证

产品版本兼容性缺陷。升级设备固件或将服务端协议降级到 v3 后通过。
