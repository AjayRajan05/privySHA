# API Reference

**ASHA v0.4.2** - canonical signatures and import paths.

---

## Import map

```python
# Root (only these)
from asha import process, sanitize, optimize, Agent, anchor

# ANCHOR (also available from root)
from asha.runtime.anchor import anchor_any
from asha.runtime.anchor.adapters import anchor_crewai, anchor_langchain

# Subpackages
from asha.integrations import wrap_llm, auto_patch
from asha.runtime import PromptProcessor, ExecutionProfile
from asha.types import ProcessResult, SanitizeResult, OptimizeResult, AgentResult
from asha.core.policy_config import PolicyConfig, PolicyMode
from asha.utils.dropin import process_async, optimize_async, sanitize_async
from asha.utils.unmask import unmask
from asha.runtime.local_advisor.advisor import recommend_local_model
from asha.runtime.adapters.factory import AdapterFactory
from asha.compat.legacy_results import to_legacy_pipeline_dict
```

---

## Result types

```python
result = process("prompt")  # ProcessResult

result.output
result.original
result.degraded
result.degraded_reason
result.security       # SecurityInfo | None
result.metrics        # MetricsInfo | None
result.trace          # dict | None (trace=True)
result.diff           # str | None (debug=True)
str(result)           # == result.output
result.to_dict()      # legacy dict shape
```

---

## process()

```python
from asha import process
from asha.core.policy_config import PolicyConfig

result = process(
    prompt: str,
    mode: str = "balanced",           # strict | balanced | lite | off
    *,
    policy: PolicyConfig | None = None,
    token_budget: int = 1200,
    trace: bool = False,
    debug: bool = False,
    max_retries: int = 0,
    timeout_seconds: float | None = None,
    verbose: bool = False,
    log_level: str = "INFO",
    log_output: str = "console",
    log_file: str | None = None,
    include_legacy_detail: bool = False,
) -> ProcessResult
```

| Mode | Behavior |
|------|----------|
| `strict` | Fail-closed - raises on total failure |
| `balanced` | Fail-open fallback (default) |
| `lite` | Minimal policy; fail-open |
| `off` | Passthrough |

`PolicyConfig` fields: `pii_mode`, `reversible`, `preserve_intent`, `security_level`, stage enable flags.

---

## sanitize()

```python
from asha import sanitize

result = sanitize(
    prompt: str,
    mode: str = "balanced",
    *,
    policy: PolicyConfig | None = None,
    trace: bool = False,
    debug: bool = False,
    max_retries: int = 0,
    timeout_seconds: float | None = None,
    verbose: bool = False,
) -> SanitizeResult
```

---

## optimize()

```python
from asha import optimize

result = optimize(
    prompt: str,
    *,
    token_budget: int = 1200,
    trace: bool = False,
    debug: bool = False,
    timeout_seconds: float | None = None,
) -> OptimizeResult
```

Token compression only - no security or compile stages.

---

## wrap_llm()

```python
from asha.integrations import wrap_llm

client = wrap_llm(
    client,
    mode: str = "balanced",
    token_budget: int = 1200,
    auto_select_local_model: bool = False,
    sample_prompts: list[str] | None = None,
)
```

- `mode="off"` - no preprocessing
- Processing errors: strict raises; balanced degrades
- Wrap infrastructure errors raise when `mode != "off"`

---

## auto_patch()

```python
from asha.integrations import auto_patch
from asha.integrations.auto_patch import (
    get_patch_status,
    disable_auto_patch,
    enable_auto_patch,
)

auto_patch(mode: str = "strict", enable: bool = True, verbose: bool = False)
```

Globally patches installed SDKs. **Prefer `wrap_llm()`** for production.

---

## Async

```python
from asha.utils.dropin import process_async, sanitize_async, optimize_async

result = await process_async("prompt", mode="balanced")
```

---

## unmask()

```python
from asha.utils.unmask import unmask

restored = unmask(llm_output, masking_map)
```

Requires `policy=PolicyConfig(reversible=True)` during `process()` / `sanitize()`.

---

## Agent

```python
from asha import Agent

agent = Agent(
    model: str = "gpt-4o-mini",
    privacy: bool = True,
    token_budget: int = 1200,
    provider: str | None = None,
    fallback_providers: list[dict] | None = None,
    routing_config: dict[str, str] | None = None,
    timeout: int = 10,
    retries: int = 3,
    api_key: str | None = None,
    local_model: str | None = None,
    sample_prompts: list[str] | None = None,
)

# Returns str by default
response = agent.run(prompt, trace=False, task_type="chat")

# Returns AgentResult when trace=True
result = agent.run(prompt, trace=True)
```

`privacy=True` → internal `mode="strict"`. `privacy=False` → `mode="off"`.

---

## PromptProcessor

```python
from asha.runtime import PromptProcessor, ExecutionProfile

processor = PromptProcessor()
result = processor.run("prompt", mode="balanced", profile=ExecutionProfile(...))
```

---

## recommend_local_model() (experimental)

```python
from asha.runtime.local_advisor.advisor import recommend_local_model

report = recommend_local_model(
    prompts: list[str] | None = None,
    prompts_file: str | None = None,
    mode: str = "balanced",
    top: int = 5,
    gpu: str | None = None,
    vram_gb: float | None = None,
    cpu_only: bool = False,
    refresh_catalog: bool = False,
    preferred_quant: str | None = None,
    probe: bool = False,
)
```

!!! warning "Experimental — API may change"
    See [experimental-features.md](experimental-features.md).

---

## AdapterFactory (experimental)

```python
from asha.runtime.adapters.factory import AdapterFactory

adapter = AdapterFactory.create(provider="openai", model="gpt-4o-mini")
adapter = AdapterFactory.create(provider="mock")
adapter = AdapterFactory.create_smart_routing({"chat": "gpt-4o-mini"})
```

Providers: `openai`, `anthropic`, `gemini`, `ollama`, `huggingface`, `grok`, `mock`.

Smart routing and factory helpers may change — see [experimental-features.md](experimental-features.md).

---

## Legacy dict

```python
from asha.compat.legacy_results import to_legacy_pipeline_dict

legacy = to_legacy_pipeline_dict(
    process("prompt", include_legacy_detail=True)
)
```

---

## CLI

| Command | Description |
|---------|-------------|
| `asha "prompt"` | Demo process |
| `asha quick-test` | Built-in tests |
| `asha examples` | Sample transformations |
| `asha benchmark` | Benchmark harness |
| `asha recommend` | AshaFit advisor |

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GOOGLE_API_KEY` / `GEMINI_API_KEY` / `GROK_API_KEY` | Provider adapters / live demos |
| `ASHA_PROVIDER` / `ASHA_MODEL` | `Agent.from_env()` / adapter factory |
| `ASHA_TOKEN_BUDGET` / `ASHA_TIMEOUT` / `ASHA_RETRIES` | Agent / adapter defaults |
| `ASHA_PRIVACY` | `Agent.from_env()` privacy flag (`true`/`false`) |
| `ASHA_MODELS_DIR` | Use a local models tree (skip default cache layout) |
| `ASHA_MODELS_URL` | Override hardened-models download URL |
| `ASHA_MODELS_ZIP` | Local zip fallback for the models bundle |
| `ASHA_MODELS_CACHE` | Override cache directory (`~/.cache/asha/models` default) |
| `ASHA_DISABLE_MODEL_DOWNLOAD` | `1` — never fetch models (CI / air-gap) |
| `ASHA_DISABLE_ML` | Disable ML/NER paths where checked |
| `ASHA_THRESHOLDS_PATH` | Override packaged detector thresholds YAML |
| `ASHA_INJECTION_MODE` | Injection detector mode override |
| `ASHA_ENABLE_HF_SAFETY` | Opt-in Hugging Face safety path |
| `ASHA_OPTIMIZER_EMBEDDING` | Optimizer embedding mode hint |
| `ASHA_ANCHOR_INTERACTIVE` | ANCHOR interactive approval (`0`/`1`) |
| `ASHA_ANCHOR_WARN_POLICY` | ANCHOR warn policy (`strict` / `permissive` / …) |
| `ASHA_ANCHOR_TELEMETRY` / `ASHA_ANCHOR_TELEMETRY_PATH` | Opt-in ANCHOR telemetry |
| `ASHA_CACHE_DIR` | Local advisor catalog cache |

`mode` is **not** read from env — set per call. See also [`.env.example`](https://github.com/AjayRajan05/ASHA/blob/main/.env.example).

---

## Errors

| Exception | When |
|-----------|------|
| `ASHAProcessingError` | `mode="strict"` total failure |
| `TypeError` | Unknown kwargs on `process()` / `sanitize()` |
| `AttributeError` | Removed root exports (`wrap_llm`, `Pipeline`, etc.) |

See [migration-v0.4.md](migration-v0.4.md) and [deprecations.md](deprecations.md).
