# 依赖服务不可用

verified: true
synthetic: true
case_id: CASE-E-003
classification: ENVIRONMENT

## 症状

支付相关用例都报 `connection refused`，其他产品流程正常。

## 关键证据

- 被测服务的业务日志只记录下游连接失败。
- 监控显示沙箱支付服务未启动。
- 启动依赖后无需修改产品或脚本即可通过。

## 最终根因与验证

测试环境依赖服务未启动。恢复服务后批量回归通过。
