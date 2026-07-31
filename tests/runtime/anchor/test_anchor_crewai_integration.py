"""CrewAI golden-path integration (skips if asha[crewai] not installed)."""

from __future__ import annotations

from typing import Any, Optional

import pytest

pytest.importorskip("crewai")

from asha.runtime.anchor.adapters.crewai import anchor_crewai


class _MiniCrew:
    __module__ = "crewai.crew"

    def __init__(self) -> None:
        self.agents: list[Any] = []
        self.tasks: list[Any] = []
        self.tools: list[Any] = []

    def kickoff(self, inputs: Optional[dict] = None) -> str:
        return f"done:{inputs}"


def test_crewai_package_importable() -> None:
    import crewai

    assert crewai is not None


def test_anchor_crewai_wraps_when_package_present() -> None:
    wrapped = anchor_crewai(_MiniCrew(), interactive=False, risk_tolerance="LOW")
    assert wrapped is not None
    assert hasattr(wrapped, "kickoff") or hasattr(wrapped, "_inner")
