"""Thin adapters around ASHA APIs for the showcase UI (logic preserved)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from asha import Agent, process, sanitize
from asha.core.policy_config import PolicyConfig
from asha.exceptions import ASHAAnchorBlocked
from asha.runtime.anchor.runtime import AnchorRuntime

try:
    from asha.integrations import wrap_llm
except Exception:  # pragma: no cover
    wrap_llm = None  # type: ignore


def sec_dict(result: Any) -> Dict[str, Any]:
    sec = getattr(result, "security", None)
    if not sec:
        return {
            "safe": None,
            "threat_level": "-",
            "score": 0.0,
            "pii": [],
            "threats": [],
            "masked": {},
        }
    threats: List[str] = []
    for t in sec.threats or []:
        threats.append(str(getattr(t, "value", None) or getattr(t, "name", None) or t))
    return {
        "safe": sec.safe,
        "threat_level": sec.threat_level,
        "score": float(sec.security_score or 0.0),
        "pii": list(sec.pii_detected or []),
        "threats": threats,
        "masked": dict(sec.masked_entities or {}),
    }


def metrics_dict(result: Any) -> Dict[str, Any]:
    m = getattr(result, "metrics", None)
    if not m:
        return {}
    return {
        "tokens_saved": m.tokens_saved,
        "reduction_pct": m.token_reduction_pct,
        "time_ms": m.processing_time_ms,
    }


def run_process(text: Any, mode: str = "balanced") -> Any:
    return process(text, mode=mode)


def run_sanitize(text: Any, mode: str = "balanced") -> Any:
    return sanitize(text, policy=PolicyConfig(mode=mode))


def tool_args(**kwargs: object) -> str:
    return str({"args": (), "kwargs": kwargs})


def make_runtime(warn_policy: str = "strict") -> AnchorRuntime:
    return AnchorRuntime(
        warn_policy=warn_policy,
        interactive=False,
        risk_tolerance="LOW",
    )


def evaluate_tool(
    runtime: AnchorRuntime,
    tool: str,
    arguments: str,
    *,
    raise_on_block: bool = True,
) -> tuple[str, Optional[str]]:
    """Return (status, detail). status in ALLOW|BLOCK|DENY."""
    try:
        allowed = runtime.evaluate_action_request(
            "tool_call",
            {"tool_name": tool, "arguments": arguments},
            raise_on_block=raise_on_block,
        )
        return ("ALLOW" if allowed else "DENY", None)
    except ASHAAnchorBlocked as err:
        return ("BLOCK", str(err))


def pii_chip_class(label: str) -> str:
    key = label.lower()
    if "email" in key:
        return "chip-email"
    if "phone" in key:
        return "chip-phone"
    if "ssn" in key:
        return "chip-ssn"
    if "key" in key or "secret" in key or "api" in key:
        return "chip-key"
    if "credit" in key or "card" in key:
        return "chip-card"
    if "name" in key:
        return "chip-name"
    return "chip-other"


__all__ = [
    "Agent",
    "wrap_llm",
    "sec_dict",
    "metrics_dict",
    "run_process",
    "run_sanitize",
    "tool_args",
    "make_runtime",
    "evaluate_tool",
    "pii_chip_class",
    "ASHAAnchorBlocked",
]
