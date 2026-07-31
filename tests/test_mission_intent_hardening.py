"""Mission domain + IR intent hardening tests (step 7)."""

from __future__ import annotations

import importlib
import sys

from asha.core._ir.ir_builder import IRBuilder
from asha.core._ir.prompt_ir import IntentType
from asha.runtime.anchor.mission import MissionCompiler
from asha.runtime.anchor.mission_session import MissionSession, merge_mission_with_baseline


def test_analytics_prompt_maps_to_analytics_domain() -> None:
    compiler = MissionCompiler()
    mission = compiler.compile(
        "Analyze the campus marketplace transaction data and find trends.",
        context={"available_tools": ["load_trend_data", "write_trend_report"]},
    )
    assert mission.low_confidence is False
    assert any(
        d in mission.allowed_domains
        for d in ("analytics", "analytics_reporting", "spreadsheets")
    )
    forbidden_lower = {a.lower() for a in mission.forbidden_actions}
    assert "payments" in forbidden_lower or "make_payment" in forbidden_lower
    assert "email" in forbidden_lower or "send_email" in forbidden_lower


def test_nonsense_prompt_is_low_confidence_restrictive() -> None:
    compiler = MissionCompiler()
    mission = compiler.compile(
        "xyzzy plugh qwerty nonsense",
        context={"available_tools": ["send_email", "write_trend_report"]},
    )
    assert mission.low_confidence is True
    assert mission.local_only is True
    assert mission.forbid_network_exfiltration is True
    assert "send" not in mission.allowed_actions
    assert "write" not in mission.allowed_actions
    forbidden_lower = {a.lower() for a in mission.forbidden_actions}
    assert "email" in forbidden_lower or "send_email" in forbidden_lower
    assert "payments" in forbidden_lower or "make_payment" in forbidden_lower


def test_refresh_phase_does_not_widen_when_baseline_low_confidence() -> None:
    session = MissionSession(MissionCompiler())
    baseline = session.initialize(
        "xyzzy plugh qwerty nonsense",
        context={"available_tools": ["read_file"]},
    )
    assert baseline.low_confidence is True
    assert "send" not in baseline.allowed_actions

    merged = session.refresh_phase(
        "Send email to partners@external.com with the summary.",
        context={"available_tools": ["send_email", "read_file"]},
    )
    assert merged.low_confidence is True
    assert "send" not in merged.allowed_actions
    assert merged.local_only is True
    assert merged.forbid_network_exfiltration is True


def test_merge_preserves_baseline_actions_when_low_confidence() -> None:
    compiler = MissionCompiler()
    baseline = compiler.compile("xyzzy plugh", context={})
    phase = compiler.compile(
        "Email partners@external.com using send_email.",
        context={"available_tools": ["send_email"]},
    )
    merged = merge_mission_with_baseline(baseline, phase)
    assert merged.low_confidence is True
    assert "send" not in merged.allowed_actions


def test_ir_builder_abstains_on_ambiguous_greeting() -> None:
    builder = IRBuilder()
    ir = builder.parse("hello")
    assert ir.intent == IntentType.ABSTAIN


def test_ir_builder_abstains_on_emptyish_prompt() -> None:
    builder = IRBuilder()
    ir = builder.parse("   ")
    assert ir.intent == IntentType.ABSTAIN


def test_domain_classifier_lazy_sklearn_import() -> None:
    sklearn_mods = {
        k: v for k, v in sys.modules.items() if k == "sklearn" or k.startswith("sklearn.")
    }
    for key in list(sklearn_mods):
        del sys.modules[key]

    if "asha.runtime.anchor.domain_classifier" in sys.modules:
        del sys.modules["asha.runtime.anchor.domain_classifier"]

    import asha.runtime.anchor.domain_classifier as dc

    assert not any(k.startswith("sklearn") for k in sys.modules)
    # predict() may lazy-load sklearn via joblib; import-time laziness is what we verify.
    assert "sklearn" not in dc.__dict__

    sys.modules.update(sklearn_mods)
    importlib.reload(dc)
