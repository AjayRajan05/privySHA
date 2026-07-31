"""Timeline / mission event visuals."""

from __future__ import annotations

from typing import Sequence, Tuple

import streamlit as st


def act_timeline(acts: Sequence[Tuple[str, str, str]]) -> None:
    """acts: (act_label, title, body_html_or_text)."""
    for label, title, body in acts:
        st.markdown(
            f"""
<div class="asha-card">
  <span class="asha-pill pill-accent">{label}</span>
  <h4 style="margin-top:0.65rem">{title}</h4>
  <p>{body}</p>
</div>
""",
            unsafe_allow_html=True,
        )


def event_timeline(events: Sequence[Tuple[str, str, str]]) -> None:
    """events: (status ALLOW|BLOCK|INFO, title, detail)."""
    for status, title, detail in events:
        css = {
            "ALLOW": "pill-allow",
            "BLOCK": "pill-block",
            "INFO": "pill-muted",
            "WARN": "pill-warn",
        }.get(status, "pill-muted")
        st.markdown(
            f"""
<div class="asha-card">
  <span class="asha-pill {css}">{status}</span>
  <strong style="margin-left:0.35rem">{title}</strong>
  <p style="margin-top:0.45rem">{detail}</p>
</div>
""",
            unsafe_allow_html=True,
        )
