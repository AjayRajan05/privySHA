"""Architecture explainer page."""

from __future__ import annotations

import streamlit as st

from components.cards import section_header
from components.pipeline import horizontal_pipeline


NODES = [
    ("User / App", "SDK entry via process, sanitize, optimize, wrap_llm, Agent, anchor"),
    ("ASHA SDK", "Typed results, policy modes, document coercion"),
    ("Security Engine", "PII · secrets · injection · jailbreak signals"),
    ("Prompt Optimizer", "Compile + token budget compression"),
    ("Policy Engine", "strict / balanced / lite / off"),
    ("Agent Runtime (ANCHOR)", "Mission contract · tool gates · approval"),
    ("Universal Model Adapter", "OpenAI · Claude · Gemini · Ollama · mock"),
]


def render() -> None:
    section_header(
        "Platform",
        "Architecture",
        "How ASHA sits in front of your models and agents.",
    )

    horizontal_pipeline(
        [
            ("U", "User", "App / agent"),
            ("S", "ASHA SDK", "Drop-in APIs"),
            ("E", "Security", "Detect + mask"),
            ("O", "Optimize", "Compress"),
            ("P", "Policy", "Mode engine"),
            ("A", "ANCHOR", "Tool governance"),
            ("M", "Adapters", "Any LLM"),
        ]
    )

    for title, body in NODES:
        with st.expander(title, expanded=False):
            st.markdown(f'<div class="asha-arch-node">{body}</div>', unsafe_allow_html=True)

    st.markdown("#### Security engine detail")
    s1, s2 = st.columns(2)
    with s1:
        st.markdown(
            """
<div class="asha-card">
  <h4>Detectors</h4>
  <p>PII Detector · Secret Detector · Prompt Injection · Jailbreak Detection</p>
</div>
""",
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            """
<div class="asha-card">
  <h4>Downstream</h4>
  <p>Prompt Optimizer → Policy Engine → Agent Runtime → Universal Model Adapter → GPT / Claude / Gemini / Ollama</p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.info("Lite path works offline. Hardened ML detectors are optional extras.")
