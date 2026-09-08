# 产品错误与网络断连同时出现

verified: true
synthetic: true
case_id: CASE-U-002
classification: UNKNOWN

## 症状

一次失败同时出现服务 500 和网络连接重置，但缺少明确的先后时间线。

## 关键证据

- 日志来自不同机器且时钟未同步。
- 无公共 traceId。
- 不同重试的现象不一致。

## 最终结论与后续动作

证据相互冲突，保持 `UNKNOWN`。先统一时钟并增加分布式 traceId 后再复现。
