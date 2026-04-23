# Welcome to PrivySHA Documentation

**The First Prompt Compiler Infrastructure for LLM Systems**

PrivySHA transforms raw prompts into optimized, structured, secure, and cost-efficient instructions before they ever reach an LLM.

---

## 🚀 Quick Start

**New to PrivySHA?** Start here:

- **[Getting Started](getting-started.md)** - Installation and first example
- **[Core Concepts](core-concepts.md)** - Understanding the mental model
- **[Architecture](architecture.md)** - System overview

---

## 🧱 Core Documentation

### Fundamentals
- **[Getting Started](getting-started.md)** - Installation, setup, first prompt
- **[Core Concepts](core-concepts.md)** - Prompt IR, Pipeline, Compiler concepts
- **[Architecture](architecture.md)** - System design and components

### Key Features
- **[Prompt IR](prompt-ir.md)** - 🔥 Structured prompt representation
- **[Pipeline](pipeline.md)** - Raw → Sanitized → IR → Optimized flow
- **[Model Gateway](model-gateway.md)** - Multi-provider abstraction
- **[Security](security.md)** - PII masking and injection protection
- **[Optimization](optimization.md)** - Token reduction and cost savings
- **[Routing](routing.md)** - Intelligent model selection
- **[Debugging](debugging.md)** - Full pipeline tracing

### Reference
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Examples](examples.md)** - Real-world use cases
- **[FAQ](faq.md)** - Common questions

### Project
- **[Contributing](contributing.md)** - How to contribute
- **[Roadmap](roadmap.md)** - Future vision and plans

---

## 🎯 Why PrivySHA?

### Traditional LLM Usage
```
User → Prompt → LLM → Response
```

**Problems:**
- ❌ Unstructured prompts
- ❌ High token cost
- ❌ No privacy guarantees
- ❌ No control over model selection
- ❌ No debugging visibility

### With PrivySHA
```
User → Sanitization → Prompt IR → Optimization → Best Model → Response
```

**Benefits:**
- ✅ Structured, reproducible prompts
- ✅ 68% average token reduction
- ✅ Built-in privacy protection
- ✅ Intelligent model routing
- ✅ Full debugging traces

---

## 📊 Key Metrics

| Feature | Traditional | PrivySHA | Improvement |
|---------|------------|-----------|------------|
| **Token Usage** | 120 tokens | 38 tokens | **68% reduction** |
| **Privacy** | None | Built-in PII masking | **Full protection** |
| **Debugging** | Limited | Full pipeline traces | **Complete visibility** |
| **Model Selection** | Manual | Intelligent routing | **Automatic optimization** |

---

## 🛠️ Installation

```bash
pip install privysha
```

### Quick Example

```python
from privysha import Agent

agent = Agent(model="gpt-4o-mini", privacy=True)

response = agent.run(
    "Hey bro can you analyze this dataset for anomalies?"
)

print(response)
```

---

## 🧠 Philosophy

PrivySHA treats prompts as:

> **Programs, not strings**

This enables:
- **Reproducibility** - Same input → same output
- **Optimization** - Systematic improvements
- **Composability** - Building blocks for complex systems
- **Debugging** - Step-by-step visibility

---

## 🏗️ What Makes PrivySHA Different?

| Feature | PrivySHA | LangChain | Guardrails |
|---------|----------|-----------|------------|
| **Prompt Compiler** | ✅ | ❌ | ❌ |
| **Prompt IR** | ✅ | ❌ | ❌ |
| **Cost Optimization** | ✅ | ❌ | ❌ |
| **Multi-model routing** | ✅ | ⚠️ | ❌ |
| **Security + Transformation** | ✅ | ⚠️ | ✅ |
| **Observability** | ✅ | ⚠️ | ⚠️ |

---

## 🚀 Next Steps

1. **[Install PrivySHA](getting-started.md#installation)**
2. **[Set up API keys](getting-started.md#setup-api-keys)**
3. **[Run your first prompt](getting-started.md#your-first-prompt)**
4. **[Explore advanced features](core-concepts.md)**

---

## 🤝 Community

- **GitHub**: [AjayRajan05/privySHA](https://github.com/AjayRajan05/privySHA)
- **Issues**: [Report bugs](https://github.com/AjayRajan05/privySHA/issues)
- **Contributing**: [How to contribute](contributing.md)

---

*Ready to transform your LLM prompts? Let's get started!*
