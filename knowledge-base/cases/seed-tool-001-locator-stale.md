# 页面改版导致 XPath 定位失效

verified: true
synthetic: true
case_id: CASE-T-001
classification: TEST_TOOL

## 症状

工具报 `Element not found`，但设备截图显示登录按钮已经出现。

## 关键证据

- App 无崩溃、接口无错误。
- 页面 DOM 改版后原 XPath 路径不再存在。
- 手工点击和 accessibility id 定位均成功。

## 最终根因与验证

自动化脚本定位器过时。替换为稳定的 accessibility id 后连续运行通过。
