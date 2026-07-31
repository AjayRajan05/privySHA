"""Shared helpers for ASHA showcase demos."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def configure_stdio() -> None:
    """Prefer UTF-8 on Windows so demo output does not crash the console."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def load_env() -> None:
    """Load repo-root .env if python-dotenv is available (never commit secrets)."""
    configure_stdio()
    env_path = ROOT / ".env"
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
    except ImportError:
        pass


def banner(title: str) -> None:
    line = "=" * 72
    print(f"\n{line}\n  {title}\n{line}")


def sub(title: str) -> None:
    print(f"\n--- {title} ---")


def gemini_api_key() -> Optional[str]:
    key = (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or "").strip()
    return key or None


def ollama_reachable(timeout: float = 1.5) -> bool:
    try:
        import urllib.request

        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=timeout):
            return True
    except Exception:
        return False


def pick_llm_backend() -> str:
    """Return gemini, ollama, or mock.

    Showcase defaults to **mock** so demos work without keys.
    Set ASHA_DEMO_BACKEND=gemini|ollama when you are ready for a live model.
    """
    forced = (os.getenv("ASHA_DEMO_BACKEND") or "mock").strip().lower()
    if forced not in {"gemini", "ollama", "mock"}:
        forced = "mock"
    if forced == "gemini" and not gemini_api_key():
        print(
            "ASHA_DEMO_BACKEND=gemini but GOOGLE_API_KEY/GEMINI_API_KEY is unset "
            "in .env - falling back to mock."
        )
        return "mock"
    if forced == "ollama" and not ollama_reachable():
        print(
            "ASHA_DEMO_BACKEND=ollama but localhost:11434 is unreachable "
            "- falling back to mock."
        )
        return "mock"
    return forced


def truncate(text: str, n: int = 220) -> str:
    text = (text or "").replace("\n", " ").strip()
    return text if len(text) <= n else text[: n - 3] + "..."
