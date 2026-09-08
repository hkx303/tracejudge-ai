# 测试账号权限过期

verified: true
synthetic: true
case_id: CASE-E-004
classification: ENVIRONMENT

## 症状

批量测试返回 `permission denied`，普通用户手工登录正常。

## 关键证据

- 自动化专用账号权限组到期。
- 相同脚本替换有效账号立即通过。
- 服务端审计日志无产品异常。

## 最终根因与验证

测试账号授权过期。续期权限组后恢复。
