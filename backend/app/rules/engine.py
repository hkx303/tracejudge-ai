from __future__ import annotations

from collections import defaultdict

from ..models import Classification, Evidence, Event, RuleHit

RULES = [
    ("tool_stack", Classification.TEST_TOOL, 0.7, ("traceback", "element not found", "xpath", "script error", "parser error", "selenium", "appium"), "A script, locator, or parser error occurred in the test tool. / 工具侧出现脚本、定位或解析异常。"),
    ("tool_timeout", Classification.TEST_TOOL, 0.45, ("timeout", "timed out", "等待超时"), "The tool log contains a timeout; verify it against device-side events. / 工具日志出现超时，需要结合设备侧事件复核。"),
    ("product_failure", Classification.PRODUCT_DEVICE, 0.75, ("http 500", "internal server error", "crash", "fatal exception", "业务错误", "firmware error"), "A clear failure signal appears in product, service, or device logs. / 产品、服务或设备日志出现明确失败信号。"),
    ("device_unavailable", Classification.PRODUCT_DEVICE, 0.65, ("device offline", "device reboot", "设备重启", "设备无响应"), "The device went offline, rebooted, or became unresponsive. / 设备出现离线、重启或无响应。"),
    ("environment", Classification.ENVIRONMENT, 0.75, ("dns", "connection refused", "network unreachable", "certificate verify", "permission denied", "依赖服务不可用"), "An environment, network, permission, or dependency failure was detected. / 环境、网络、权限或依赖服务异常。"),
]


def evaluate(events: list[Event]) -> tuple[dict[str, float], list[RuleHit]]:
    scores: defaultdict[Classification, float] = defaultdict(float)
    hits: list[RuleHit] = []
    for rule_id, classification, weight, phrases, explanation in RULES:
        matched = [e for e in events if any(phrase in e.message.lower() for phrase in phrases)]
        if not matched:
            continue
        evidence = [Evidence(file_name=e.file_name, line_number=e.line_number, source=e.source, detail=e.message, timestamp=e.timestamp) for e in matched[:3]]
        adjusted = weight + min(0.15, 0.05 * (len(matched) - 1))
        scores[classification] += adjusted
        hits.append(RuleHit(rule_id=rule_id, classification=classification, weight=adjusted, explanation=explanation, evidence=evidence))
    total = sum(scores.values())
    normalized = {kind.value: round(value / total, 3) if total else 0.0 for kind, value in scores.items()}
    for kind in Classification:
        normalized.setdefault(kind.value, 0.0)
    return normalized, hits


def rule_conclusion(scores: dict[str, float], hits: list[RuleHit]) -> tuple[Classification, float, str, list[str], list[str]]:
    ranked = sorted(((Classification(key), value) for key, value in scores.items()), key=lambda item: item[1], reverse=True)
    winner, score = ranked[0]
    if score < 0.5 or (len(ranked) > 1 and score - ranked[1][1] < 0.15):
        return Classification.UNKNOWN, 0.35, "The available logs support multiple explanations, so evidence is insufficient for reliable attribution. / 现有日志同时存在多种可能，证据不足以可靠归因。", ["Missing linked logs needed to exclude other categories. / 缺少可排除其他类别的链路日志。"], ["Collect device, tool, and service logs from 60 seconds before and after the failure. / 补充失败前后 60 秒的设备、工具和服务日志。"]
    actions = {
        Classification.TEST_TOOL: ["Confirm whether the command reached the device. / 确认指令是否真正下发到设备。", "Reproduce manually or with a second tool; inspect timeouts, scripts, and locators. / 使用手工操作或另一套工具复现，并检查超时、脚本与定位策略。"],
        Classification.PRODUCT_DEVICE: ["Reproduce manually with the same version and input. / 在相同版本和输入下手工复现。", "Collect device or service crash data, error codes, and version information. / 收集设备/服务崩溃信息、错误码和版本信息。"],
        Classification.ENVIRONMENT: ["Check network, DNS, permissions, and dependency health. / 检查网络、DNS、权限和依赖服务健康状态。", "Retry the same test in an isolated or alternative environment. / 在隔离或替代环境中重试同一用例。"],
    }
    return winner, min(0.92, round(0.55 + score * 0.4, 2)), f"Rule evidence primarily indicates {winner.value}. / 规则证据主要指向 {winner.value}。", [], actions[winner]
