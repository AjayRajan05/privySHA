"""Visual pipeline components."""

from __future__ import annotations

from typing import List, Sequence, Tuple

import streamlit as st


def horizontal_pipeline(steps: Sequence[Tuple[str, str, str]], *, scanning: bool = False) -> None:
    """steps: (icon, title, description)."""
    if scanning:
        st.markdown('<div class="asha-scan"><div></div></div>', unsafe_allow_html=True)
    parts: List[str] = ['<div class="asha-pipe">']
    for icon, title, desc in steps:
        parts.append(
            f"""
<div class="asha-pipe-step">
  <div class="ico">{icon}</div>
  <div class="ttl">{title}</div>
  <div class="desc">{desc}</div>
  <div class="ok">OK</div>
</div>
"""
        )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def stage_list(stages: Sequence[Tuple[str, str, str]]) -> None:
    """Collapsible-friendly stage rows: (title, status, body)."""
    for title, status, body in stages:
        with st.expander(f"{status}  {title}", expanded=False):
            st.code(body or "(empty)", language="text")
