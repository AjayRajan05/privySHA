"""Without vs With ASHA comparison."""

from __future__ import annotations

import streamlit as st


def without_vs_with() -> None:
    left, right = st.columns(2)
    with left:
        st.markdown(
            """
<div class="asha-compare-bad">
  <h3>Without ASHA</h3>
  <div class="asha-li">Raw prompt sent to the model</div>
  <div class="asha-li">Email leaked</div>
  <div class="asha-li">API key leaked</div>
  <div class="asha-li">Credit card leaked</div>
  <div class="asha-li">Prompt injection succeeds</div>
  <div class="asha-li">High token usage</div>
  <div class="asha-li">Unsafe / ungoverned output</div>
  <div style="margin-top:0.8rem"><span class="asha-pill pill-block">HIGH RISK</span></div>
</div>
""",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            """
<div class="asha-compare-good">
  <h3>With ASHA</h3>
  <div class="asha-li">PII masked before inference</div>
  <div class="asha-li">Secrets removed / tokenized</div>
  <div class="asha-li">Injection detected &amp; contained</div>
  <div class="asha-li">Prompt optimized</div>
  <div class="asha-li">Lower token cost</div>
  <div class="asha-li">Safe prompt + governed tools</div>
  <div class="asha-li">Mission-aware agent decisions</div>
  <div style="margin-top:0.8rem"><span class="asha-pill pill-allow">PROTECTED</span>
  <span class="asha-pill pill-accent">LOWER COST</span></div>
</div>
""",
            unsafe_allow_html=True,
        )
