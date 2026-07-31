"""KPI / metric card helpers."""

from __future__ import annotations

from typing import Iterable, Sequence, Tuple

import streamlit as st


def hero_metrics(items: Sequence[Tuple[str, str, str]]) -> None:
    """Render large KPI cards. items: (label, value, hint)."""
    cols = st.columns(len(items))
    for col, (label, value, hint) in zip(cols, items):
        with col:
            st.markdown(
                f"""
<div class="asha-kpi">
  <div class="label">{label}</div>
  <div class="value">{value}</div>
  <div class="hint">{hint}</div>
</div>
""",
                unsafe_allow_html=True,
            )


def kpi_row(items: Iterable[Tuple[str, str]]) -> None:
    items = list(items)
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        col.metric(label, value)
