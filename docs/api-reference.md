# API Reference

Complete API documentation for PrivySHA, including all classes, methods, and configuration options.

---

## 🔧 Core Classes

### Agent

The main interface for interacting with PrivySHA.

#### Constructor

```python
from privysha import Agent

agent = Agent(
    model="gpt-4o-mini",
    privacy=False,
    optimization_level="balanced",
    fallback_providers=None,
    routing_strategy="balanced",
    debug_level="basic"
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | `"gpt-4o-mini"` | Model to use or `"auto"` for automatic selection |
| `privacy` | bool | `False` | Enable PII masking and injection protection |
| `optimization_level` | str | `"balanced"` | `"conservative"`, `"balanced"`, or `"aggressive"` |
| `fallback_providers` | list | `None` | List of fallback provider configurations |
| `routing_strategy` | str or callable | `"balanced"` | `"cost_optimized"`, `"performance_optimized"`, `"balanced"`, or custom function |
| `debug_level` | str | `"basic"` | `"basic"`, `"verbose"`, or `"none"` |
| `provider_config` | dict | `{}` | Provider-specific configuration |

#### Fallback Provider Configuration

```python
fallback_providers=[
    {
        "provider": "anthropic",
        "model": "claude-3-haiku",
        "config": {"temperature": 0.7}
    },
    {
        "provider": "openai", 
        "model": "gpt-3.5-turbo",
        "config": {"timeout": 30}
    }
]
```

#### Custom Routing Strategy

```python
def custom_routing(task_ir, context):
    if task_ir.intent == "analyze":
        return {"provider": "openai", "model": "gpt-4o"}
    else:
        return {"provider": "anthropic", "model": "claude-3-haiku"}

agent = Agent(routing_strategy=custom_routing)
```

#### Methods

##### run()

```python
result = agent.run(
    prompt="Analyze data",
    trace=False,
    context=None
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | str | Required | The input prompt to process |
| `trace` | bool | `False` | Enable full pipeline tracing |
| `context` | list | `None` | Conversation context for multi-turn conversations |

**Returns:**

```python
{
    "response": "The data shows...",
    "metadata": {
        "model_used": "gpt-4o-mini",
        "provider": "openai",
        "tokens_used": 45,
        "processing_time_ms": 1234
    },
    "optimization_metrics": {
        "original_tokens": 120,
        "optimized_tokens": 38,
        "reduction_percentage": 68.3
    },
    "security_result": {
        "pii_detected": [],
        "pii_masked": 0,
        "injection_attempts": 0
    }
}
```

##### print_debug_trace()

```python
agent.print_debug_trace()
```

Prints the most recent debug trace to console.

##### get_stats()

```python
stats = agent.get_stats()
```

Returns performance and usage statistics.

---

## 🧠 Prompt IR Classes

### PromptIR

Structured representation of user intent.

#### Constructor

```python
from privysha.ir.prompt_ir import PromptIR

ir = PromptIR({
    "intent": "analyze",
    "object": "data",
    "constraints": ["thorough"],
    "style": "analytical"
})
```

#### Properties

| Property | Type | Description |
|-----------|------|-------------|
| `intent` | str | Primary user intent |
| `object` | str | Object the intent acts upon |
| `constraints` | list | List of constraints |
| `style` | str | Desired output style |
| `privacy` | dict | Privacy configuration |
| `metadata` | dict | Additional metadata |

#### Methods

##### is_valid()

```python
valid = ir.is_valid()
```

Returns `True` if IR structure is valid.

##### to_dict()

```python
data = ir.to_dict()
```

Returns IR as dictionary.

##### from_prompt()

```python
ir = PromptIR.from_prompt("Analyze data thoroughly")
```

Creates IR from natural language prompt.

---

### IRBuilder

Builds PromptIR from text.

#### Constructor

```python
from privysha.ir.ir_builder import IRBuilder

builder = IRBuilder(
    confidence_threshold=0.8,
    custom_intents={},
    custom_constraints=[]
)
```

#### Methods

##### generate()

```python
ir = builder.generate(
    prompt="Analyze data",
    context=None
)
```

##### add_intent_pattern()

```python
builder.add_intent_pattern(
    name="visualize",
    patterns=["plot", "chart", "graph", "visualize"]
)
```

##### add_constraint_pattern()

```python
builder.add_constraint_pattern(
    name="gdpr_compliant",
    patterns=["gdpr", "privacy", "compliant"]
)
```

---

## 🔒 Security Classes

### SecurityLayer

Handles PII detection and injection protection.

#### Constructor

```python
from privysha.security.security_layer import SecurityLayer

security = SecurityLayer(
    security_level="medium",
    custom_pii_patterns={},
    custom_injection_rules=[]
)
```

#### Security Levels

| Level | Description | Features |
|-------|-------------|----------|
| `"low"` | Basic protection | Basic PII masking |
| `"medium"` | Standard protection | PII + basic injection |
| `"high"` | Enhanced protection | Comprehensive security |
| `"strict"` | Maximum protection | All security features |

#### Methods

##### scan()

```python
result = security.scan(text="Contact john@email.com")
```

**Returns:**

```python
{
    "pii_detected": ["email"],
    "pii_masked": 1,
    "masked_text": "Contact [EMAIL]",
    "injection_attempts": 0,
    "risk_level": "medium"
}
```

##### add_pii_pattern()

```python
security.add_pii_pattern(
    name="employee_id",
    pattern=r"EMP\d{6}",
    replacement="[EMPLOYEE_ID]"
)
```

##### add_injection_rule()

```python
security.add_injection_rule(
    name="custom_attack",
    pattern=r"(ignore|forget).+(above|previous)",
    action="block"
)
```

---

## ⚡ Optimization Classes

### PromptOptimizer

Optimizes prompts for token reduction.

#### Constructor

```python
from privysha.compiler.optimizer_engine import PromptOptimizer

optimizer = PromptOptimizer(
    level="balanced",
    preserve_semantics=True,
    target_reduction=0.5
)
```

#### Methods

##### optimize()

```python
result = optimizer.optimize(ir)
```

**Returns:**

```python
{
    "optimized_ir": {...},
    "original_tokens": 120,
    "optimized_tokens": 38,
    "reduction_percentage": 68.3,
    "optimizations_applied": [
        "constraint_consolidation",
        "object_simplification"
    ]
}
```

##### add_optimization_rule()

```python
optimizer.add_optimization_rule(
    name="custom_compression",
    pattern=r"(very|quite|rather)\s+(\w+)",
    replacement=r"\2",
    confidence=0.8
)
```

---

## 🌐 Gateway Classes

### ModelRouter

Routes requests to appropriate models.

#### Constructor

```python
from privysha.routing.model_router import ModelRouter

router = ModelRouter(
    strategy="balanced",
    fallback_providers=[],
    cost_limits={}
)
```

#### Routing Strategies

| Strategy | Description |
|----------|-------------|
| `"cost_optimized"` | Minimize cost |
| `"performance_optimized"` | Maximize performance |
| `"balanced"` | Balance cost and performance |
| `custom_function` | Custom routing logic |

#### Methods

##### route()

```python
selection = router.route(
    task_ir=ir,
    context={}
)
```

**Returns:**

```python
{
    "provider": "openai",
    "model": "gpt-4o-mini",
    "reasoning": "Balanced choice for analysis task",
    "confidence": 0.92
}
```

##### add_routing_rule()

```python
router.add_routing_rule(
    condition="intent == 'analyze' and complexity > 0.7",
    action={"provider": "openai", "model": "gpt-4o"},
    priority=1
)
```

---

## 🔧 Adapters

### BaseAdapter

Base class for all model adapters.

#### Methods

##### generate()

```python
response = adapter.generate(prompt="Analyze data")
```

##### validate_config()

```python
valid = adapter.validate_config()
```

### OpenAIAdapter

OpenAI model adapter.

#### Constructor

```python
from privysha.adapters.openai_adapter import OpenAIAdapter

adapter = OpenAIAdapter(
    model="gpt-4o-mini",
    api_key="your_key",
    base_url=None,
    timeout=30
)
```

### AnthropicAdapter

Anthropic Claude adapter.

#### Constructor

```python
from privysha.adapters.claude_adapter import AnthropicAdapter

adapter = AnthropicAdapter(
    model="claude-3-haiku",
    api_key="your_key",
    timeout=30
)
```

### HuggingFaceAdapter

Local HuggingFace model adapter.

#### Constructor

```python
from privysha.adapters.hf_adapter import HuggingFaceAdapter

adapter = HuggingFaceAdapter(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    device="auto",
    torch_dtype="float16"
)
```

---

## 🏗️ Pipeline Classes

### Pipeline

Main processing pipeline.

#### Constructor

```python
from privysha.pipeline import Pipeline

pipeline = Pipeline(
    enable_sanitization=True,
    enable_pii_detection=True,
    enable_ir_generation=True,
    enable_optimization=True,
    enable_compilation=True
)
```

#### Methods

##### process()

```python
result = pipeline.process(
    prompt="Analyze data",
    config={}
)
```

##### add_stage()

```python
pipeline.add_stage(
    name="custom_stage",
    stage_instance=CustomStage(),
    position=3
)
```

##### configure()

```python
pipeline.configure({
    "optimization_level": "aggressive",
    "security_level": "high"
})
```

---

## 🔍 Debugging Classes

### PrivySHADebugger

Debugging and tracing utilities.

#### Constructor

```python
from privysha.debug.debugger import PrivySHADebugger

debugger = PrivySHADebugger(
    enabled=True,
    log_level="debug",
    output_file="debug.log"
)
```

#### Methods

##### trace()

```python
trace_data = debugger.trace(
    stage="optimization",
    input_data={},
    output_data={},
    metadata={}
)
```

##### generate_report()

```python
report = debugger.generate_report(
    format="html",
    include_charts=True
)
```

---

## 📊 Utility Functions

### Metrics

```python
from privysha.utils.metrics import calculate_metrics

metrics = calculate_metrics(
    original_prompt="Analyze comprehensive data",
    optimized_prompt="Analyze data",
    response_time_ms=1234,
    tokens_used=45
)
```

### Validation

```python
from privysha.utils.validation import validate_prompt

validation = validate_prompt(
    prompt="Analyze data",
    checks=["length", "content", "security"]
)
```

### Configuration

```python
from privysha.utils.config import load_config

config = load_config(
    file_path="config.yaml",
    environment="production"
)
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | None |
| `ANTHROPIC_API_KEY` | Anthropic API key | None |
| `GROK_API_KEY` | xAI API key | None |
| `PRIVYSHA_LOG_LEVEL` | Logging level | `"INFO"` |
| `PRIVYSHA_CACHE_DIR` | Cache directory | `"./cache"` |
| `PRIVYSHA_CONFIG_FILE` | Config file path | `"./config.yaml"` |

### Configuration File

```yaml
# config.yaml
privysha:
  model: "gpt-4o-mini"
  privacy: true
  optimization_level: "balanced"
  
  security:
    level: "medium"
    pii_detection: true
    injection_protection: true
    
  routing:
    strategy: "balanced"
    fallback_providers:
      - provider: "anthropic"
        model: "claude-3-haiku"
        
  optimization:
    target_reduction: 0.5
    preserve_semantics: true
    
  debugging:
    enabled: false
    log_level: "INFO"
```

---

## 🚨 Error Handling

### Exception Classes

```python
from privysha.exceptions import (
    PrivySHAError,
    ConfigurationError,
    ModelError,
    SecurityError,
    OptimizationError
)

try:
    result = agent.run("Analyze data")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except ModelError as e:
    print(f"Model error: {e}")
except SecurityError as e:
    print(f"Security error: {e}")
except PrivySHAError as e:
    print(f"General error: {e}")
```

### Error Types

| Error | Description |
|--------|-------------|
| `ConfigurationError` | Invalid configuration |
| `ModelError` | Model-related errors |
| `SecurityError` | Security-related errors |
| `OptimizationError` | Optimization failures |
| `ValidationError` | Input validation errors |
| `RoutingError` | Routing failures |

---

## 🎯 Examples

### Basic Usage

```python
from privysha import Agent

# Simple agent
agent = Agent(model="gpt-4o-mini")
response = agent.run("Analyze data")
print(response)
```

### Advanced Usage

```python
from privysha import Agent

# Advanced configuration
agent = Agent(
    model="auto",
    privacy=True,
    optimization_level="aggressive",
    fallback_providers=[
        {"provider": "anthropic", "model": "claude-3-haiku"}
    ],
    routing_strategy="cost_optimized"
)

# Run with tracing
result = agent.run("Analyze comprehensive data", trace=True)

# Access detailed results
print("Response:", result["response"])
print("Optimization:", result["optimization_metrics"])
print("Security:", result["security_result"])

# Print debug trace
agent.print_debug_trace()
```

### Custom Components

```python
from privysha import Agent
from privysha.ir.ir_builder import IRBuilder
from privysha.security.security_layer import SecurityLayer

# Custom IR builder
builder = IRBuilder()
builder.add_intent_pattern("visualize", ["plot", "chart"])

# Custom security
security = SecurityLevel("high")
security.add_pii_pattern("custom_id", r"ID\d{6}")

# Agent with custom components
agent = Agent(
    model="gpt-4o-mini",
    ir_builder=builder,
    security_layer=security
)
```

---

## 🎯 Next Steps

Now that you have the complete API reference:

1. **[See Examples](examples.md)** - Real-world usage
2. **[Check FAQ](faq.md)** - Common questions
3. **[Learn Contributing](contributing.md)** - How to contribute
4. **[Review Roadmap](roadmap.md)** - Future features

---

*Ready to see real-world examples? Check out the [Examples documentation](examples.md)!*
