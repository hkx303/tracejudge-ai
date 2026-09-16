# Evaluation guide / 评测规范

## English

The baseline regression set is in `sample-data/`; tests live in `backend/tests/test_analysis.py`.

| Scenario | Expected classification | Minimum assertion |
| --- | --- | --- |
| Service HTTP 500 | `PRODUCT_DEVICE` | At least one evidence item and one verification action |
| Locator timeout | `TEST_TOOL` | A verified case is retrievable |
| DNS or network unavailable | `ENVIRONMENT` | An environment rule matches |
| No clear error | `UNKNOWN` | The system does not force attribution |

When adding rules, parsers, or prompts, add a real-but-redacted regression sample and evaluate attribution accuracy, sensible `UNKNOWN` use, evidence coverage, knowledge-reference correctness, and verified-case recall after human confirmation.

## 中文

基础回归集位于 `sample-data/`，对应测试位于 `backend/tests/test_analysis.py`。

| 场景 | 期望分类 | 最低断言 |
| --- | --- | --- |
| 服务 HTTP 500 | `PRODUCT_DEVICE` | 至少一个证据和验证动作 |
| 元素定位超时 | `TEST_TOOL` | 可检索已验证案例 |
| DNS 或网络不可达 | `ENVIRONMENT` | 命中环境规则 |
| 无明确错误 | `UNKNOWN` | 不强行归因 |

每次新增规则、解析器或提示词时，须新增真实但已脱敏的回归样例，并检查分类准确率、`UNKNOWN` 的合理性、证据覆盖率、知识库引用正确性与人工确认后的案例召回。
