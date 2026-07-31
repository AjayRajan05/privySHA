"""Smoke tests for CLI entry points (no network required).

Run click commands in a subprocess so transformers/numpy reloads cannot
corrupt torch for the rest of the suite (Windows docstring / DLL pollution).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run_cli_snippet(snippet: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-c", snippet],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )


def test_quick_test_command():
    snippet = (
        "from click.testing import CliRunner\n"
        "from asha.cli.main import quick_test\n"
        "r = CliRunner().invoke(quick_test)\n"
        "print(r.output)\n"
        "raise SystemExit(0 if r.exit_code == 0 else 1)\n"
    )
    result = _run_cli_snippet(snippet)
    out = (result.stdout or "") + (result.stderr or "")
    assert result.returncode == 0, out
    assert "tests passed" in out.lower() or "PASS" in out


def test_quick_test_via_cli_group():
    snippet = (
        "from click.testing import CliRunner\n"
        "from asha.cli.main import cli\n"
        "r = CliRunner().invoke(cli, ['quick-test'])\n"
        "print(r.output)\n"
        "raise SystemExit(0 if r.exit_code == 0 else 1)\n"
    )
    result = _run_cli_snippet(snippet)
    assert result.returncode == 0, result.stdout + result.stderr


def test_examples_command_runs():
    snippet = (
        "from click.testing import CliRunner\n"
        "from asha.cli.main import examples\n"
        "r = CliRunner().invoke(examples, ['--count', '1'])\n"
        "print(r.output)\n"
        "raise SystemExit(0 if r.exit_code == 0 else 1)\n"
    )
    result = _run_cli_snippet(snippet)
    out = (result.stdout or "") + (result.stderr or "")
    assert result.returncode == 0, out
    assert "1." in out
