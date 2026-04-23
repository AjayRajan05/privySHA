# Getting Started with PrivySHA

Welcome to PrivySHA! This guide will get you up and running in minutes.

---

## 🚀 Installation

### Basic Installation

```bash
pip install privysha
```

### With Optional Dependencies

```bash
# For HuggingFace models
pip install privysha[hf]

# For development
pip install privysha[dev]

# For all features
pip install privysha[hf,dev]
```

### Verify Installation

```python
from privysha import Agent

# Should work without errors
print("PrivySHA installed successfully!")
```

---

## 🔑 Setup API Keys

PrivySHA supports multiple LLM providers. Set up the ones you need:

### OpenAI

```bash
export OPENAI_API_KEY=your_openai_key_here
```

### Anthropic Claude

```bash
export ANTHROPIC_API_KEY=your_anthropic_key_here
```

### xAI Grok

```bash
export GROK_API_KEY=your_grok_key_here
```

### Using .env File (Recommended)

Create a `.env` file in your project:

```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GROK_API_KEY=your_grok_key_here
```

Then load it:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🎯 Your First Prompt

### Basic Usage

```python
from privysha import Agent

# Create agent with default settings
agent = Agent(model="gpt-4o-mini")

# Run a simple prompt
response = agent.run("Analyze this dataset for anomalies")
print(response)
```

### With Privacy Protection

```python
from privysha import Agent

# Enable privacy features
agent = Agent(
    model="gpt-4o-mini",
    privacy=True  # Enables PII masking and injection protection
)

response = agent.run(
    "Analyze user data: john@email.com, phone: 555-0123"
)

print(response)
# PII will be automatically masked
```

### With Tracing (Debug Mode)

```python
from privysha import Agent

agent = Agent(model="gpt-4o-mini")

# Run with full trace
result = agent.run(
    "Analyze this dataset",
    trace=True  # Enables debugging information
)

print("Response:", result["response"])
print("Optimization:", result["optimization_metrics"])
print("Security:", result["security_result"])

# Print full debug trace
agent.print_debug_trace()
```

---

## 🏗️ Basic vs Advanced Usage

### Basic (v1 Compatible)

Simple, backward-compatible API:

```python
from privysha import Agent

agent = Agent(model="gpt-4o-mini")
response = agent.run("Your prompt here")
```

### Advanced (v2 Features)

Full control with fallbacks and routing:

```python
from privysha import Agent

agent = Agent(
    model="gpt-4o-mini",
    privacy=True,
    fallback_providers=[
        {"provider": "anthropic", "model": "claude-3-haiku"},
        {"provider": "grok", "model": "grok-beta"}
    ],
    optimization_level="aggressive"
)

result = agent.run("Complex prompt", trace=True)
```

---

## 📊 Understanding the Output

### Simple Response

```python
response = agent.run("Simple prompt")
print(response)
# Just the text response
```

### Advanced Result

```python
result = agent.run("Complex prompt", trace=True)

print("Response:", result["response"])
print("Tokens used:", result["token_usage"])
print("Optimization:", result["optimization_metrics"])
print("Security:", result["security_result"])
print("Model used:", result["model_info"])
```

### Example Output

```python
{
    "response": "The dataset shows 3 anomalies...",
    "token_usage": {
        "input_tokens": 38,
        "output_tokens": 45,
        "total_tokens": 83
    },
    "optimization_metrics": {
        "original_tokens": 120,
        "optimized_tokens": 38,
        "reduction_percentage": 68.3
    },
    "security_result": {
        "pii_detected": 2,
        "pii_masked": 2,
        "injection_attempts": 0
    },
    "model_info": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "fallback_used": False
    }
}
```

---

## 🛠️ Common Configurations

### Data Analysis

```python
from privysha import Agent

analyst = Agent(
    model="gpt-4o-mini",
    privacy=True,
    optimization_level="balanced"
)

result = analyst.run(
    "Analyze the sales data and identify trends",
    trace=True
)
```

### Chatbot

```python
from privysha import Agent

chatbot = Agent(
    model="gpt-4o-mini",
    privacy=True,
    fallback_providers=[
        {"provider": "anthropic", "model": "claude-3-haiku"}
    ]
)

response = chatbot.run("User message about their data")
```

### Content Moderation

```python
from privysha import Agent

moderator = Agent(
    model="gpt-4o-mini",
    privacy=True,
    security_level="high"
)

result = moderator.run(
    "Check this content for policy violations",
    trace=True
)
```

---

## 🔍 Troubleshooting

### Common Issues

#### API Key Not Found
```
Error: OPENAI_API_KEY not found
```
**Solution**: Set environment variables or use .env file

#### Model Not Available
```
Error: Model 'gpt-4' not found
```
**Solution**: Check available models for each provider

#### Import Error
```
Error: No module named 'privysha'
```
**Solution**: `pip install privysha`

### Debug Mode

Always use `trace=True` for debugging:

```python
result = agent.run("prompt", trace=True)
agent.print_debug_trace()
```

This shows the full pipeline:
```
RAW → SANITIZED → IR → OPTIMIZED → COMPILED → RESPONSE
```

---

## 🎯 Next Steps

Now that you're set up:

1. **[Learn Core Concepts](core-concepts.md)** - Understand Prompt IR and Pipeline
2. **[Explore Pipeline](pipeline.md)** - Deep dive into processing stages
3. **[Check Examples](examples.md)** - Real-world use cases
4. **[API Reference](api-reference.md)** - Complete documentation

---

## 💡 Pro Tips

- **Always use `trace=True` during development**
- **Enable `privacy=True` for user data**
- **Set up fallback providers for production**
- **Monitor optimization metrics for cost savings**
- **Use debug traces for troubleshooting**

---

*Ready to dive deeper? Check out [Core Concepts](core-concepts.md) next!*
