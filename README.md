# ASHA

**ASHA is the security layer that sits between your application and every LLM, protecting prompts before inference and governing agents after inference.**

> **Developer preview (v0.4.2).** Pre-1.0: APIs may change.
> Install with `pip install asha-ai`. For long-lived pilots, pin the version you tested (see [docs/status.md](docs/status.md)).

[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/pypi-0.4.2-orange)](https://pypi.org/project/asha-ai/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-mkdocs-material-blue)](https://ajayrajan05.github.io/ASHA/)
[![Discussions](https://img.shields.io/badge/GitHub-Discussions-black?logo=github)](https://github.com/AjayRajan05/ASHA/discussions)
[![Slack](https://img.shields.io/badge/Slack-Join-4A154B?logo=slack&logoColor=white)](https://join.slack.com/t/asha-community/shared_invite/zt-45h11ellh-yY~YG4BL8W~TvxsMXSgPzw)

## Quickstart

```bash
pip install asha-ai
```

PyPI distribution name is **`asha-ai`** (the name `asha` is taken by an unrelated project). Imports stay `from asha import ...`.

No API key and no model download required for the quickstart.

```python
from asha import process

result = process("Contact john@example.com for data analysis", mode="balanced")
print(result.output)   # PII masked, prompt compiled + optimized
print(result.security) # detection summary
print(result.metrics)  # token / stage metrics
```

## Why ASHA

- **Mission-scoped agent governance** — `anchor()` compiles an immutable mission contract and gates every tool call against it (`ALLOW` / `WARN` / `BLOCK` / `REVIEW`).
- **Layered prompt-injection and PII defense** — fail-closed calibrated detection with heuristic fallbacks on a lite install, not a single regex list.
- **Tool-execution sandbox (preview)** — in-process side-effect hooks by default (`isolation="auto"`); stronger child-process isolation with `isolation="hard"`. Container backends (`docker` / `bwrap`) are not implemented yet.
- **Install-time cost control** — base install includes text-document extractors for PII masking; pay only for heavier extras you need (`fast`, `hardened`, providers, `asha-ai[anchor]`).
- **One-line client wrapping** — `wrap_llm(openai.OpenAI())` preprocesses prompts and local file attachments without rewriting your app.

## Install tiers

| Install | What you get | Dependency cost |
|---------|--------------|-----------------|
| `pip install asha-ai` | **Recommended for everyone** — core APIs + lite/heuristic detectors + text PDF/DOCX extraction for PII masking | pydantic, tiktoken, requests, click, pypdf, python-docx |
| `pip install asha-ai[fast]` | Faster pattern matching | + `pyahocorasick` |
| `pip install asha-ai[hardened]` | Optional classical ML detectors (models auto-download on first use) | + torch / transformers / sklearn stack |
| `pip install asha-ai[anchor]` | All ANCHOR framework adapters (CrewAI, LangChain, LangGraph, LlamaIndex, MCP) | + framework packages |

Other common extras: `asha-ai[openai]`, `asha-ai[integrations]`, `asha-ai[ml]`, or per-framework `asha-ai[crewai]` / `asha-ai[langchain]` / `asha-ai[langgraph]` / `asha-ai[llamaindex]` / `asha-ai[mcp]`. Hardened weights are **not** required for the default lite path. Adapter matrix: [docs/anchor.md](docs/anchor.md).

## Mission governance (`anchor`)

```python
from asha.runtime.anchor import AnchorRuntime
from asha.exceptions import ASHAAnchorBlocked

runtime = AnchorRuntime(warn_policy="strict", interactive=False, risk_tolerance="LOW")
runtime.initialize_mission(
    "Analyze Q1 sales locally and write a report. Do not send data externally.",
    context={
        "available_tools": ["load_sales_data", "write_report", "send_email"],
        "local_only": True,
    },
)

# On-mission → allowed
assert runtime.evaluate_action_request(
    "tool_call",
    {
        "tool_name": "write_report",
        "arguments": str({"args": (), "kwargs": {"report_content": "Q1 summary"}}),
    },
)

# High-risk / off-policy → blocked
try:
    runtime.evaluate_action_request(
        "tool_call",
        {
            "tool_name": "send_email",
            "arguments": str({"args": (), "kwargs": {"to": "exfil@evil.com"}}),
        },
        raise_on_block=True,
    )
except ASHAAnchorBlocked as err:
    print(err)
    # ANCHOR blocked tool/action 'send_email': High-risk tool 'send_email'
    # requires human approval before execution.
```

One-line adoption for an existing agent (headless-safe):

```python
from asha import Agent, anchor

agent = anchor(
    Agent(provider="mock", model="mock", tools=["read_file", "email"]),
    interactive=False,
)
print(agent.run("Generate the monthly sales report"))
```

## Live demos

```bash
pip install -e ".[demo]"
streamlit run examples/showcase/streamlit_app.py
```

Interactive Streamlit app that runs the **real** ASHA APIs to show usefulness:

1. **Scrub** dirty prompts/files (`process` / `sanitize`) so PII, secrets, and injections do not reach the model  
2. **Leash** agents with ANCHOR (ALLOW local tools, BLOCK email/cloud exfil)  
3. **Drop in** via `wrap_llm` / `Agent` (mock offline; Gemini/Ollama optional)

Full page-by-page workflows: [examples/showcase/README.md](examples/showcase/README.md).

## Docs

Full documentation (tutorial, how-tos, reference, explanation): **[docs site](https://ajayrajan05.github.io/ASHA/)** · [docs/index.md](docs/index.md) · [Status](docs/status.md) · [Roadmap](docs/roadmap.md)

### Migration from PrivySHA

```bash
pip uninstall privysha -y
pip install asha-ai==0.4.2
```

```python
# before: from privysha import process
from asha import process
```

Env prefix is `ASHA_*`. Details: [docs/migration-v0.4.md](docs/migration-v0.4.md).

## Community & support

- **[GitHub Discussions](https://github.com/AjayRajan05/ASHA/discussions)** — questions, ideas, design talk (primary)
- **[Slack](https://join.slack.com/t/asha-community/shared_invite/zt-45h11ellh-yY~YG4BL8W~TvxsMXSgPzw)** — optional community chat
- **[GitHub Issues](https://github.com/AjayRajan05/ASHA/issues)** — bugs and feature requests
- **Support policy:** [SUPPORT.md](SUPPORT.md)

## License

Apache 2.0 — see [LICENSE](LICENSE).

- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md) · [docs/contributing.md](docs/contributing.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Security: [SECURITY.md](SECURITY.md)
- Roadmap: [docs/roadmap.md](docs/roadmap.md)
