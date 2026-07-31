"""Plotly charts for scores and benchmarks."""

from __future__ import annotations

from typing import Dict, List

import streamlit as st

try:
    import plotly.graph_objects as go
except Exception:  # pragma: no cover
    go = None  # type: ignore


def gauge_score(score: float, title: str = "Security score") -> None:
    """Circular-ish gauge. score 0..1 or 0..100."""
    if score <= 1:
        score = score * 100
    score = max(0.0, min(100.0, float(score)))
    if go is None:
        st.metric(title, f"{score:.0f}/100")
        return
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "", "font": {"size": 36}},
            title={"text": title, "font": {"size": 14}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#0d9488"},
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 70], "color": "#ffedd5"},
                    {"range": [70, 100], "color": "#d1fae5"},
                ],
                "threshold": {
                    "line": {"color": "#0f766e", "width": 3},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(height=240, margin=dict(l=20, r=20, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


def threat_bar(counts: Dict[str, int]) -> None:
    if go is None or not counts:
        st.write(counts)
        return
    labels = list(counts.keys())
    values = list(counts.values())
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=["#0d9488" if v == 0 else "#dc2626" if "injection" in k.lower() else "#d97706" for k, v in counts.items()],
        )
    )
    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Count",
    )
    st.plotly_chart(fig, use_container_width=True)


def token_savings_chart(labels: List[str], values: List[float]) -> None:
    if go is None:
        st.write(dict(zip(labels, values)))
        return
    fig = go.Figure(
        go.Bar(x=labels, y=values, marker_color="#0d9488", text=[f"{v:.0f}%" for v in values], textposition="outside")
    )
    fig.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Token reduction %",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
