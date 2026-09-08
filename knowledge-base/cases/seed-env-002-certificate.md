# 测试证书过期

verified: true
synthetic: true
case_id: CASE-E-002
classification: ENVIRONMENT

## 症状

所有 HTTPS 调用报 `certificate verify failed`。

## 关键证据

- 服务端健康检查正常。
- 同一产品版本在证书更新后的环境通过。
- 系统时间正确，错误指向中间证书过期。

## 最终根因与验证

测试环境网关证书链过期。更新证书后所有接口恢复。
