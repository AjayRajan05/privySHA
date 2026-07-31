# Debugging

How to inspect what ASHA did to a prompt using traces and diffs.

---

## Trace a process() call

```python
from asha import process

result = process(
    "Analyze data with john@example.com",
    trace=True,
    debug=True,
)

print(result.output)
print(result.trace)
print(result.diff)
```

`trace=True` records stage names, timing, and intermediate outputs. `debug=True` adds `result.diff` (unified diff) and optional debug metadata.

```python
result = process("prompt", debug=True)
if result.degraded:
    print(result.degraded_reason)
print(result.diff)
```

---

## Agent tracing

```python
from asha import Agent

agent = Agent(model="mock")
result = agent.run("prompt with john@x.com", trace=True)
print(result.output)
print(result.response)
print(result.adapter_info)
```

Without `trace=True`, `agent.run()` returns a string only.

---

## CLI

```bash
asha "prompt with john@x.com" --debug --mode balanced
```

---

## Removed APIs

`ASHADebugger`, `DebugTracer`, and the old `debug/` package were removed in v0.4.1. Use `trace=True` / `debug=True` on `process()` instead.

---

## Related

- [Architecture](architecture.md)
- [API reference](api-reference.md)
- [Troubleshooting](troubleshooting.md)
