"""Card layouts."""

from __future__ import annotations

import streamlit as st


def section_header(eyebrow: str, title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="asha-section-label">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)


def why_card(title: str, body: str, tone: str = "accent") -> None:
    pill = {
        "accent": "pill-accent",
        "warn": "pill-warn",
        "allow": "pill-allow",
    }.get(tone, "pill-accent")
    st.markdown(
        f"""
<div class="asha-card">
  <span class="asha-pill {pill}">{title}</span>
  <p style="margin-top:0.75rem">{body}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def impact_card(title: str, value: str, detail: str) -> None:
    st.markdown(
        f"""
<div class="asha-card">
  <h4>{title}</h4>
  <div style="font-size:1.8rem;font-weight:700;color:#0b1220;letter-spacing:-0.03em">{value}</div>
  <p>{detail}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def use_case_card(title: str, blurb: str) -> None:
    st.markdown(
        f"""
<div class="asha-card">
  <h4>{title}</h4>
  <p>{blurb}</p>
</div>
""",
        unsafe_allow_html=True,
    )
