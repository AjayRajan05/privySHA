# Roadmap

Forward-looking plan from **v0.4.2** (July 2026). Dates are estimates.

---

## Shipped in v0.4.2

- Package rename: `privysha` → `asha` (PyPI, imports, CLI)
- **ANCHOR** mission-aware agent governance (`anchor()`, guards, sandbox, human approval)
- Framework adapters: CrewAI, LangChain, AutoGen, LlamaIndex, MCP, LangGraph, generic
- ANCHOR extras (`asha-ai[anchor]`, per-framework installs) + golden-path CI
- CI/publish workflows updated for `asha` package layout
- Integration test job with optional framework deps in CI

## Productization (Phase 4 — done)

- Published [support policy](support.md) / repo `SUPPORT.md`
- Community intake: GitHub Issues templates + Discussions as primary channel
- Docs freeze pass for 0.4.2 preview claims (status, ANCHOR matrix, install tiers)
- Post-release setup done for Discussions, Slack invite, and `asha-models-0.4.2` asset

## Current focus — finish 0.4.2

Version stays **0.4.2**. No rush to 1.0. Keep the developer-preview story honest and ship remaining surface polish. A future 1.0 is documented for later — see [production-readiness.md](production-readiness.md) — not an active milestone.

## Shipped in v0.4.1

- Frozen root API (`process`, `sanitize`, `optimize`, `Agent`)
- `PromptProcessor` as sole orchestrator (security → compile → optimize)
- Typed `ProcessResult` / `SanitizeResult` / `OptimizeResult`
- Unified `mode=` safety semantics
- `runtime/resolve.py` - no compat on hot path
- Architecture boundary tests in CI
- Dead legacy code removed (`Pipeline`, `ModelRouter`, `debug/` package, etc.)
- `wrap_llm` / `auto_patch` in `asha.integrations`

---

## v0.5.x (target: H2 2026)

- API freeze - deprecation warnings only, no breaking removals
- Container sandbox backends (`docker`, `bwrap`)
- Prompt caching for repeated patterns
- Expanded international PII formats
- PyPI classifier → Beta

---

## v1.0.0 (deferred — only after 0.4.x is solid)

Not scheduled. Stay on **0.4.2** until the maintainer is ready to acknowledge a stable API. Checklist for that eventual day: [production-readiness.md](production-readiness.md).

**Not committed for 1.0:** managed cloud service, multi-tenant SaaS, paid SLA.

---

## Preview features (may change anytime)

| Feature | Module |
|---------|--------|
| ANCHOR framework adapters (non-CrewAI) | `runtime/anchor/adapters/` |
| AshaFit local advisor | `runtime/local_advisor/` |
| Hybrid ML PII | `core/hybrid_pii.py` + `pii_pipeline/` |
| `auto_patch()` | `integrations/auto_patch.py` |
| Framework middleware | `integrations/fastapi`, `langchain`, etc. |

---

## Long-term ideas

- Cost-aware multi-model routing
- Prometheus metrics export expansion
- Prompt caching engine
- Native function-calling in `asha.Agent` tool loop

See [status.md](status.md) for current limitations. Preview/experimental APIs: [experimental-features.md](experimental-features.md).
