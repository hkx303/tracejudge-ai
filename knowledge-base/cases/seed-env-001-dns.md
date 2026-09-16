# DNS 解析失败

verified: true
synthetic: true
case_id: CASE-E-001
classification: ENVIRONMENT

## English summary

Several unrelated tests failed with DNS and network-unreachable errors while product logs were healthy. Restoring test-network DNS configuration fixed the suite.

## 症状

登录步骤失败，日志出现 `DNS network unreachable`。

## 关键证据

- 多个无关用例同时失败。
- 工具、设备和服务均无业务异常。
- 更换 DNS 或网络出口后立即恢复。

## 最终根因与验证

测试网络 DNS 配置失效。恢复域名解析服务后所有用例通过。
