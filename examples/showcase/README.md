# ASHA Streamlit showcase

> **ASHA is the security layer that sits between your application and every LLM, protecting prompts before inference and governing agents after inference.**

This is the **only runnable demo** for ASHA. It is a product-style Streamlit app that runs the **real library APIs** (`process`, `sanitize`, `Agent`, `ANCHOR`, `wrap_llm`, `PolicyConfig`) so visitors can see *why* ASHA exists and *how* it protects LLM apps?not just read docs.

```bash
# From repo root (preferred ? installs asha + UI deps)
pip install -e ".[demo]"

# Or install UI deps from this folder after `pip install -e .`
# pip install -r examples/showcase/requirements.txt

streamlit run examples/showcase/streamlit_app.py
```

Opens a local UI (default `http://localhost:8501`). No API key is required for the core demos. Optional Gemini / Ollama can be enabled later via `.env`.

---

## Who should use ASHA?

- AI application developers shipping chat or copilots
- Teams building **agentic** systems with tools
- Enterprise copilots and internal knowledge assistants
- **RAG** pipelines that pull sensitive documents into context
- Customer support platforms that ingest tickets and attachments
- Healthcare, finance, and legal AI that must not leak regulated data
- Anyone who currently calls OpenAI / Gemini / Claude / Ollama with raw prompts

If you send user text (or files) to a model today, this showcase is for you.

---

## 30-second demo

```text
1. Open Security Console
2. Click "Run security scan"
3. Watch PII / secrets disappear in the After panel
4. Open Rogue agent
5. Click "Evaluate mission"
6. Watch send_email get BLOCKED

Done. That's ASHA:
  - scrub what goes into the model
  - leash what the agent is allowed to do
```

Suggested follow-up: **End-to-end story** (one click) or **Playground** (paste your own prompt).

---

## Why not just call the LLM provider?

Providers generate text. They do **not** act as your application's security layer.

| Question | Typical provider API | ASHA |
|----------|----------------------|------|
| Does it remove PII before inference? | No | Yes (`process` / `sanitize`) |
| Does it stop prompt injection / jailbreaks in *your* ingress? | No (model-side filters vary; not your control plane) | Yes (detect + surface threats) |
| Does it prevent agent tool abuse (email / upload)? | No | Yes (ANCHOR mission gates) |
| Does it optimize tokens before you pay? | No | Yes (compile + budget) |
| Does it work offline on a lite install? | No | Yes (no key required for core path) |
| Does it wrap multiple providers the same way? | Partial / per-SDK | Yes (`wrap_llm` / `Agent`) |

**ASHA does not replace GPT, Claude, Gemini, or Ollama.**  
It sits **in front of** them so your app stays safe and cheaper regardless of which model you pick.

---

## Why ASHA instead of raw LLM usage?

| Capability | Raw LLM call | ASHA |
|------------|--------------|------|
| PII masking | No | Yes |
| Secret / API-key redaction | No | Yes |
| Prompt injection detection | No | Yes |
| Token optimization | No | Yes |
| Agent / tool governance | No | Yes (ANCHOR) |
| Offline processing (lite) | No | Yes |
| Multi-provider drop-in | Partial | Yes |
| Configurable policies (`strict` / `balanced` / `lite`) | No | Yes |

---

## How much code?

You do **not** rewrite your app. Minimal integration:

```python
from asha import process

safe = process(user_prompt, mode="balanced")
# send safe.output to OpenAI / Gemini / Claude / Ollama
```

```python
from asha import Agent

agent = Agent(model="mock", privacy=True)  # or gemini-1.5-flash, llama3.2, ...
response = agent.run(user_prompt)
```

```python
from asha.integrations import wrap_llm
# client = wrap_llm(openai.OpenAI(), mode="balanced")
# client.chat.completions.create(...)
```

```python
from asha.runtime.anchor import AnchorRuntime

runtime = AnchorRuntime(interactive=False, warn_policy="strict")
runtime.initialize_mission("Analyze data locally. Do not email anyone.", context={...})
runtime.evaluate_action_request("tool_call", {"tool_name": "send_email", ...})
```

The Streamlit app exercises these same APIs live.

---

## What problem it showcases

Raw LLM usage is risky and expensive:

| Without ASHA | With ASHA (what the app proves) |
|--------------|----------------------------------|
| Emails, phones, SSNs, cards, API keys go to the model | PII / secrets are masked **before** inference |
| Jailbreak / injection text is trusted | Threats are detected and surfaced |
| Bloated prompts burn tokens | Prompts are optimized under a budget |
| Agents can email or upload off-mission | ANCHOR **ALLOW**s local tools and **BLOCK**s exfil |
| Apps must rewrite clients per provider | `wrap_llm` / `Agent` drop into existing stacks |

**Product line:** *Scrub what goes into the model. Leash what the agent is allowed to do.*

---

## Concrete use cases

| Vertical | What ASHA does in practice |
|----------|----------------------------|
| **Healthcare** | Remove PHI (names, MRNs, phones) before clinical copilots see notes |
| **Finance** | Mask account numbers, SSNs, cards; catch injection in research agents |
| **Legal** | Redact parties and secrets in contract / NDA review flows |
| **Customer support** | Scrub tickets and attachments; strip leaked API keys before helpdesk LLMs |
| **AI agents** | Mission-scope tools so agents cannot email or upload off-policy |
| **Enterprise copilots** | Govern HR/ops prompts that mix personal and internal data |
| **RAG** | Sanitize retrieved chunks before they enter the context window |

On the **Overview** page, industry cards load realistic prompts into the **Playground** with one click.

---

## How usefulness is shown (workflows)

Each page is a **workflow**, not a feature dump. Together they cover ASHA's two jobs:

1. **Prompt security** ? protect what enters the model  
2. **Agent governance** ? control what tools may run after the model decides  

### Master workflow (end-to-end)

```text
Dirty input (ticket / chat / file)
        |
        v
  process() / sanitize()     <- PII, secrets, injection, optimize
        |
        v
  Safe / optimized prompt
        |
        +---> wrap_llm / Agent  -> model reply (Live LLM page)
        |
        +---> ANCHOR mission    -> ALLOW / BLOCK tools (Rogue agent page)
```

The **End-to-end story** page walks this narrative in five acts. Other pages zoom into one stage.

---

## Pages (what is in the app)

### 1. Overview ? ?Why ASHA?? in 30 seconds

**Workflow:** storytelling + jump into live demos.

| Section | What it shows |
|---------|----------------|
| Hero | Product positioning |
| KPI cards | Protected prompts, threats, PII, token savings, latency, LLMs |
| Why ASHA | Problem ? Solution ? Result |
| Visual pipeline | Prompt ? PII ? secrets ? injection ? optimize ? policy ? router ? safe response |
| Without vs With | Side-by-side risk comparison |
| Use-case cards | Load industry prompts into Playground |
| Live impact | Example counters (PII removed, injections, token %, confidence) |

---

### 2. Playground ? full pipeline on any prompt

```text
Paste prompt -> mode (balanced / lite / strict)
  -> process()
  -> stages: raw -> PII -> threats -> metrics -> final prompt
  -> security gauge + token reduction
```

**APIs:** `process()`.

---

### 3. Security console ? before / after leak prevention

```text
Load ticket -> process() or sanitize()
  -> Before | After
  -> score gauge, threat badges, PII chips, threat chart
  -> optional injection gallery batch
```

**APIs:** `process()`, `sanitize()`, `PolicyConfig`.  
**Fixtures:** `fixtures/support_ticket.txt`, `fixtures/injection_prompts.txt` (synthetic PII).

---

### 4. Rogue agent ? ANCHOR mission control

```text
Mission ("work locally, do not email")
  -> tools registered
  -> AnchorRuntime.initialize_mission(...)
  -> evaluate_action_request per tool
  -> ALLOW local read/write ? BLOCK email / cloud upload
```

**Flow in UI:** Agent ? ANCHOR ? Decision ? ALLOW/BLOCK.  
**APIs:** `AnchorRuntime`, `ASHAAnchorBlocked` (`interactive=False`).

---

### 5. Document scrubber ? files and attachments

```text
Sample | upload (.txt/.md/.pdf/.docx) | paste
  -> sanitize() + process()
  -> Original vs secure + PII chips
```

**APIs:** path/bytes inputs to `sanitize` / `process`.

---

### 6. Live LLM ? drop-in before the model

```text
Raw prompt -> process() preview
  -> mock Agent (default)
  -> or wrap_llm(Gemini) / Agent(Ollama) if configured
  -> reply + latency / threat / length metrics
```

**APIs:** `process()`, `Agent`, optional `wrap_llm`.

Optional:

```bash
copy .env.example .env
# GOOGLE_API_KEY=...
# ASHA_DEMO_BACKEND=gemini
# or ASHA_DEMO_BACKEND=ollama
```

Default backend is **mock** (always works offline).

---

### 7. End-to-end story ? both jobs in one run

1. Incoming dirty ticket  
2. ASHA security scan (`process`)  
3. Prompt optimization  
4. ANCHOR: ALLOW local write, BLOCK `send_email`  
5. Secure outcome  

---

### 8. Architecture ? where ASHA sits

```text
User / App -> ASHA SDK -> Security Engine -> Optimizer -> Policy
          -> ANCHOR -> Universal adapters
          -> OpenAI / Claude / Gemini / Ollama
```

ASHA is a **layer**, not a model.

---

### 9. Benchmarks ? capability snapshot

Illustrative cards/charts (lite vs hardened, offline-first, token examples). Validate on your workload before production claims. Preview: v0.4.2.

---

## APIs exercised by page

| Page | Primary ASHA surface |
|------|----------------------|
| Overview | Narrative ? live pages |
| Playground | `process` |
| Security console | `process`, `sanitize`, `PolicyConfig` |
| Rogue agent | `AnchorRuntime` |
| Document scrubber | `sanitize` / `process` on files |
| Live LLM | `process`, `Agent`, optional `wrap_llm` |
| End-to-end story | `process` + `AnchorRuntime` |
| Architecture / Benchmarks | Product education |

UI pages call `ui_backend.py`; they do **not** reimplement detectors.

---

## Enterprise-ready checklist

What enterprise readers typically look for (preview build?pin `asha==0.4.2` for pilots):

- Offline-first lite path (no API key / no model download required)
- Local processing of prompts and documents
- Multi-provider support (OpenAI, Anthropic, Gemini, Ollama, mock)
- Prompt optimization / token budget control
- Mission-aware agents (ANCHOR)
- Configurable security policies (`strict` / `balanced` / `lite` / `off`)
- Drop-in integration (`process`, `wrap_llm`, `Agent`)
- Headless CI-friendly ANCHOR (`interactive=False`)
- Apache 2.0 license

---

## Project layout

```text
examples/showcase/
  streamlit_app.py      # entry + sidebar navigation
  ui_backend.py         # wrappers over real asha.* APIs
  _common.py            # .env load, Gemini/Ollama probes
  components/           # styles, cards, metrics, pipeline, charts
  views/                # one module per page
  data/use_cases.py     # industry prompts
  fixtures/             # synthetic ticket + injection lines
```

---

## Suggested demo path

1. **Overview** ? Why ASHA + Without/With (30s)  
2. **Security console** ? Run scan on the sample ticket  
3. **Rogue agent** ? Evaluate mission (BLOCK on `send_email`)  
4. **End-to-end story** ? Play story  
5. **Playground** ? your own prompt  
6. **Live LLM** ? mock now; Gemini when `.env` is set  

That path answers: *Why ASHA? What changes? How do agents stay on mission? How little code do I need?*

---

## Requirements

- Python 3.10+
- ASHA from this repo (v0.4.2 developer preview)
- UI packages: see [`requirements.txt`](requirements.txt) or `pip install -e ".[demo]"`

Never paste keys into chat or commit them. Use repo-root `.env` (gitignored). See [../../.env.example](../../.env.example).
