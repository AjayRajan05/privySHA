# ASHA demos

All interactive demos live in the Streamlit showcase.

```bash
pip install -e ".[demo]"
streamlit run examples/showcase/streamlit_app.py
```

That app shows library usefulness with real workflows:

- Prompt/file security (`process`, `sanitize`)
- Agent tool governance (ANCHOR ALLOW/BLOCK)
- Optional live LLM wrap (`Agent`, `wrap_llm`)

**Complete guide** (every page, workflow, and API mapping):  
[showcase/README.md](showcase/README.md)

Copy-paste code snippets (no separate demo scripts): [docs/examples.md](../docs/examples.md).
