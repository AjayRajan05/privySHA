# PrivySHA Usage Guide

## Quick Start

### Installation

```bash
pip install privysha
```

### Basic Usage

```python
from privysha import Agent

# Create an agent with privacy protection
agent = Agent(
    model="mock",  # Use "gpt-4o-mini" for OpenAI, "llama3" for Ollama
    privacy=True,
    token_budget=1200
)

# Process a prompt
response = agent.run("Hey bro can you analyze this dataset for anomalies?")
print(response)
```

### Debug Mode

See the full pipeline transformation:

```python
result = agent.run("Your prompt here", trace=True)

print("RAW PROMPT:")
print(result["raw_prompt"])

print("SANITIZED:")
print(result["sanitized"])

print("OPTIMIZED:")
print(result["optimized"])

print("COMPILED PROMPT:")
print(result["compiled_prompt"])
```

## Model Providers

### OpenAI (Requires API Key)

```python
import os
from privysha import Agent

os.environ["OPENAI_API_KEY"] = "your-api-key"

agent = Agent(model="gpt-4o-mini")
response = agent.run("Analyze this data")
```

### Ollama (Requires Local Server)

```bash
# Install and start Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
ollama pull llama3
```

```python
from privysha import Agent

agent = Agent(model="llama3")
response = agent.run("Analyze this data")
```

### HuggingFace (Requires Transformers)

```python
from privysha import Agent

agent = Agent(model="microsoft/DialoGPT-medium")
response = agent.run("Analyze this data")
```

## Testing Your Setup

### Test with Mock Adapter

```python
from privysha import Agent

# Test without external services
agent = Agent(model="mock", privacy=True)
response = agent.run("Test prompt with email@example.com")
print(response)
```

### Test Pipeline Stages

```python
from privysha import Agent

agent = Agent(model="mock", privacy=True)
result = agent.run("Hey bro analyze my dataset john@example.com", trace=True)

# Check PII masking
assert "john@example.com" not in result["sanitized"]
assert "<EMAIL_HASH>" in result["sanitized"]

# Check sanitization
assert "bro" not in result["sanitized"]

# Check optimization
assert "@" in result["optimized"]  # Token optimization
```

## Production Deployment

### Environment Setup

```python
# production.py
from privysha import Agent
import os

# Configure environment
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Production agent
agent = Agent(
    model="gpt-4o-mini",
    privacy=True,  # Always enable in production
    token_budget=2000  # Adjust based on your needs
)

def process_prompt(user_input):
    """Process user input with privacy protection"""
    try:
        response = agent.run(user_input)
        return response
    except Exception as e:
        return f"Error processing prompt: {e}"
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

CMD ["python", "your_app.py"]
```

### Requirements.txt

```
privysha>=0.1.0
python-dotenv
fastapi  # if using web framework
```

## Security Considerations

1. **Always enable `privacy=True` in production**
2. **Never log raw prompts** - use trace mode carefully
3. **Validate user inputs** before processing
4. **Monitor token usage** with `token_budget`
5. **Use environment variables** for API keys

## Monitoring

```python
import time
from privysha import Agent

agent = Agent(model="gpt-4o-mini", privacy=True)

def monitored_process(prompt):
    start_time = time.time()
    
    result = agent.run(prompt, trace=True)
    
    processing_time = time.time() - start_time
    
    # Log metrics (without sensitive data)
    print(f"Processing time: {processing_time:.2f}s")
    print(f"Token optimization: {len(result['raw_prompt'])} -> {len(result['optimized'])}")
    
    return result["response"]
```

## Troubleshooting

### Common Issues

1. **Import Error**: `pip install -e .` in development
2. **Connection Refused**: Start Ollama server or check API keys
3. **Memory Issues**: Reduce `token_budget` or use smaller models
4. **PII Not Masked**: Ensure `privacy=True`

### Debug Mode

```python
# Enable full debugging
result = agent.run(prompt, trace=True)

# Print all stages
for stage, output in result.items():
    if stage != "response":
        print(f"{stage.upper()}:")
        print(f"  {output}")
        print()
```

## Examples

### Data Analysis Pipeline

```python
from privysha import Agent

agent = Agent(model="gpt-4o-mini", privacy=True)

def analyze_data(data_description):
    prompt = f"Analyze this dataset for patterns: {data_description}"
    return agent.run(prompt)

# Usage
result = analyze_data("Sales data from Q1 2024 with customer emails")
```

### Customer Support

```python
from privysha import Agent

agent = Agent(model="gpt-4o-mini", privacy=True)

def support_query(customer_message):
    # PII will be automatically masked
    return agent.run(customer_message)

# Usage
response = support_query("Help me with order #12345, email john@example.com")
```
