"""Global CSS for the ASHA product showcase."""

from __future__ import annotations

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {
    --ink: #0b1220;
    --ink-soft: #1e293b;
    --accent: #0d9488;
    --accent-deep: #0f766e;
    --accent-glow: rgba(13, 148, 136, 0.18);
    --danger: #dc2626;
    --danger-bg: #fef2f2;
    --success: #059669;
    --success-bg: #ecfdf5;
    --warn: #d97706;
    --warn-bg: #fffbeb;
    --panel: #ffffff;
    --panel-muted: #f1f5f9;
    --border: #e2e8f0;
    --muted: #64748b;
    --radius: 16px;
  }

  html, body, [class*="css"] {
    font-family: 'DM Sans', system-ui, sans-serif;
  }

  .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1180px !important;
  }

  #MainMenu, footer { visibility: hidden; }

  h1, h2, h3 { color: var(--ink) !important; letter-spacing: -0.03em; font-weight: 700; }

  .asha-hero {
    position: relative;
    overflow: hidden;
    background:
      radial-gradient(ellipse 80% 80% at 10% 10%, rgba(13,148,136,0.45), transparent 55%),
      radial-gradient(ellipse 60% 60% at 90% 20%, rgba(20,33,61,0.55), transparent 50%),
      linear-gradient(135deg, #0b1220 0%, #134e4a 55%, #0f766e 100%);
    color: #f8fafc;
    padding: 2.4rem 2.2rem 2.2rem;
    border-radius: 22px;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.25);
    animation: fadeUp 0.55s ease-out;
  }
  .asha-hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(120deg, transparent 40%, rgba(255,255,255,0.06) 50%, transparent 60%);
    pointer-events: none;
  }
  .asha-hero .brand {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: 0.6rem;
  }
  .asha-hero h1 {
    color: #fff !important;
    font-size: clamp(2rem, 4vw, 2.75rem);
    margin: 0 0 0.55rem 0;
    line-height: 1.1;
  }
  .asha-hero p {
    margin: 0;
    max-width: 36rem;
    font-size: 1.08rem;
    opacity: 0.92;
    line-height: 1.5;
  }

  .asha-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.35rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    animation: fadeUp 0.45s ease-out;
  }
  .asha-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
    border-color: #cbd5e1;
  }
  .asha-card h3, .asha-card h4 {
    margin: 0 0 0.4rem 0;
    font-size: 1.05rem;
  }
  .asha-card p { margin: 0; color: var(--muted); line-height: 1.5; font-size: 0.95rem; }

  .asha-kpi {
    background: linear-gradient(180deg, #fff 0%, #f8fafc 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.15rem 1.2rem;
    text-align: left;
    min-height: 110px;
    box-shadow: 0 1px 2px rgba(15,23,42,0.04);
    animation: fadeUp 0.5s ease-out;
  }
  .asha-kpi .label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  .asha-kpi .value {
    font-size: 1.85rem;
    font-weight: 700;
    color: var(--ink);
    margin-top: 0.35rem;
    letter-spacing: -0.03em;
  }
  .asha-kpi .hint { font-size: 0.8rem; color: var(--accent-deep); margin-top: 0.25rem; }

  .asha-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.02em;
  }
  .pill-allow { background: var(--success-bg); color: var(--success); }
  .pill-block { background: var(--danger-bg); color: var(--danger); }
  .pill-warn { background: var(--warn-bg); color: var(--warn); }
  .pill-muted { background: #e2e8f0; color: var(--muted); }
  .pill-accent { background: var(--accent-glow); color: var(--accent-deep); }

  .asha-chip {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    margin: 0.15rem 0.2rem 0.15rem 0;
    border-radius: 8px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
  }
  .chip-email { background: #dbeafe; color: #1d4ed8; }
  .chip-phone { background: #fce7f3; color: #be185d; }
  .chip-ssn { background: #ffedd5; color: #c2410c; }
  .chip-key { background: #ede9fe; color: #6d28d9; }
  .chip-card { background: #fee2e2; color: #b91c1c; }
  .chip-name { background: #d1fae5; color: #047857; }
  .chip-other { background: #e2e8f0; color: #475569; }

  .asha-compare-bad {
    background: linear-gradient(180deg, #fff5f5 0%, #fff 100%);
    border: 1px solid #fecaca;
    border-radius: var(--radius);
    padding: 1.25rem;
  }
  .asha-compare-good {
    background: linear-gradient(180deg, #ecfdf5 0%, #fff 100%);
    border: 1px solid #a7f3d0;
    border-radius: var(--radius);
    padding: 1.25rem;
  }
  .asha-compare-bad h3 { color: var(--danger) !important; }
  .asha-compare-good h3 { color: var(--success) !important; }
  .asha-li { margin: 0.4rem 0; font-size: 0.95rem; }

  .asha-pipe {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    align-items: stretch;
    margin: 0.75rem 0 1.25rem;
  }
  .asha-pipe-step {
    flex: 1 1 110px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.85rem 0.75rem;
    text-align: center;
    position: relative;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }
  .asha-pipe-step:hover {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }
  .asha-pipe-step .ico { font-size: 1.25rem; margin-bottom: 0.25rem; }
  .asha-pipe-step .ttl { font-size: 0.78rem; font-weight: 700; color: var(--ink); }
  .asha-pipe-step .desc { font-size: 0.7rem; color: var(--muted); margin-top: 0.2rem; }
  .asha-pipe-step .ok {
    margin-top: 0.4rem;
    color: var(--success);
    font-size: 0.72rem;
    font-weight: 700;
  }

  .asha-scan {
    height: 6px;
    border-radius: 999px;
    background: #e2e8f0;
    overflow: hidden;
    margin: 0.75rem 0 1rem;
  }
  .asha-scan > div {
    height: 100%;
    width: 40%;
    background: linear-gradient(90deg, var(--accent-deep), #2dd4bf);
    border-radius: 999px;
    animation: scan 1.4s ease-in-out infinite;
  }

  .asha-section-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent-deep);
    margin: 1.6rem 0 0.55rem;
  }

  .asha-arch-node {
    background: var(--panel-muted);
    border-left: 3px solid var(--accent);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.92rem;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes scan {
    0% { transform: translateX(-120%); }
    100% { transform: translateX(320%); }
  }

  div[data-testid="stMetricValue"] { font-size: 1.35rem; font-weight: 700; }
  div[data-testid="stSidebar"] { background: #0b1220; }
  div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  div[data-testid="stSidebar"] .stRadio label { font-weight: 500; }
</style>
""",
        unsafe_allow_html=True,
    )
