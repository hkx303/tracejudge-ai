# Product and device error codes / 产品与设备错误码

## English

When product-service logs show `HTTP 500`, `INTERNAL_SERVER_ERROR`, or device logs show `FATAL EXCEPTION`, first inspect product version, server exceptions, and device crash information. If the test tool successfully sent a request and received one of these signals, do not attribute the issue to the tool merely because it reports the final failure.

## 中文

当产品服务日志出现 `HTTP 500`、`INTERNAL_SERVER_ERROR` 或设备出现 `FATAL EXCEPTION` 时，应优先检查产品版本、服务端异常和设备崩溃信息。测试工具已成功下发请求且收到这类响应时，不应仅因最终工具报错而归因为工具问题。
