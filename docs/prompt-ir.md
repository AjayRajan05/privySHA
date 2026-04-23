# Prompt IR (Intermediate Representation)

Prompt IR is PrivySHA's killer feature - a structured representation that transforms unstructured prompts into optimized, machine-readable programs.

---

## 🔥 What is Prompt IR?

Prompt IR is a structured JSON representation of user intent, enabling:

- **Deterministic processing** - Same input → same structure
- **Systematic optimization** - Algorithmic improvements
- **Advanced routing** - Intelligent model selection
- **Full debugging** - Step-by-step visibility

---

## 🏗️ IR Structure

### Basic IR Schema

```json
{
  "intent": "analyze",
  "object": "dataset",
  "constraints": ["anomaly_detection"],
  "style": "concise",
  "privacy": {
    "masked": true,
    "level": "high"
  },
  "optimization": {
    "target_tokens": 50,
    "preserve_meaning": true
  },
  "metadata": {
    "domain": "data_analysis",
    "complexity": "medium",
    "estimated_tokens": 38
  }
}
```

### Core Fields Explained

#### `intent`
The user's primary goal:

```python
"Analyze data" → {"intent": "analyze"}
"Create summary" → {"intent": "generate"}
"Categorize items" → {"intent": "classify"}
"Extract information" → {"intent": "extract"}
"Transform format" → {"intent": "transform"}
"Check validity" → {"intent": "validate"}
```

#### `object`
What the intent acts upon:

```python
"Analyze customer data" → {"object": "customer_data"}
"Debug Python code" → {"object": "code"}
"Summarize article" → {"object": "text"}
"Format JSON output" → {"object": "data_structure"}
```

#### `constraints`
Specific requirements or limitations:

```python
"Analyze quickly" → {"constraints": ["speed"]}
"Be thorough" → {"constraints": ["completeness"]}
"Keep it simple" → {"constraints": ["simplicity"]}
"Use formal tone" → {"constraints": ["formality"]}
```

#### `style`
Desired output style:

```python
"Keep it brief" → {"style": "concise"}
"Explain like I'm 5" → {"style": "simple"}
"Be professional" → {"style": "formal"}
"Use bullet points" → {"style": "structured"}
```

---

## 🔄 IR Generation Process

### Stage 1: Raw Input Analysis

```python
# Input
"Please analyze the sales dataset and find any unusual patterns or anomalies. Be thorough but keep it brief."

# Tokenization & Entity Recognition
tokens = ["please", "analyze", "sales", "dataset", "find", "unusual", "patterns", "anomalies", "thorough", "brief"]
entities = ["sales_dataset", "patterns", "anomalies"]
```

### Stage 2: Intent Classification

```python
# Pattern matching against intent database
if "analyze" in tokens or "find" in tokens:
    intent = "analyze"
if "patterns" in entities or "anomalies" in entities:
    object = "dataset"
```

### Stage 3: Constraint Extraction

```python
# Constraint detection
if "thorough" in tokens:
    constraints.append("completeness")
if "brief" in tokens:
    constraints.append("conciseness")
```

### Stage 4: IR Construction

```python
ir = {
    "intent": "analyze",
    "object": "dataset",
    "constraints": ["completeness", "conciseness"],
    "style": "balanced",
    "privacy": {"masked": False},
    "optimization": {"target_tokens": 45}
}
```

---

## 🎯 Real-World Examples

### Data Analysis Request

**Input:**
```
"Hey can you look at the customer data and find any weird patterns? Also make sure to keep PII private and be quick about it."
```

**Generated IR:**
```json
{
  "intent": "analyze",
  "object": "customer_data",
  "constraints": ["speed", "privacy"],
  "style": "concise",
  "privacy": {
    "masked": true,
    "level": "high",
    "pii_types": ["email", "phone", "name"]
  },
  "optimization": {
    "target_tokens": 35,
    "preserve_meaning": true
  },
  "metadata": {
    "domain": "data_analysis",
    "complexity": "medium",
    "urgency": "high"
  }
}
```

### Content Generation Request

**Input:**
```
"Write a professional email to the team about the quarterly results. Make it formal but not too long."
```

**Generated IR:**
```json
{
  "intent": "generate",
  "object": "email",
  "constraints": ["formality", "brevity"],
  "style": "professional",
  "privacy": {
    "masked": false
  },
  "optimization": {
    "target_tokens": 150,
    "preserve_meaning": true
  },
  "metadata": {
    "domain": "business_communication",
    "complexity": "low",
    "audience": "internal_team"
  }
}
```

### Code Debugging Request

**Input:**
```
"This Python code isn't working, can you debug it? Focus on performance issues."
```

**Generated IR:**
```json
{
  "intent": "debug",
  "object": "code",
  "constraints": ["performance"],
  "style": "technical",
  "privacy": {
    "masked": false
  },
  "optimization": {
    "target_tokens": 200,
    "preserve_meaning": true
  },
  "metadata": {
    "domain": "programming",
    "complexity": "high",
    "language": "python"
  }
}
```

---

## ⚡ IR Optimization

### Token Reduction

```python
# Original IR (estimated 120 tokens)
{
  "intent": "analyze",
  "object": "comprehensive_customer_sales_dataset",
  "constraints": ["thorough_analysis", "detailed_examination", "complete_review"],
  "style": "formal_professional_business_communication"
}

# Optimized IR (estimated 38 tokens)
{
  "intent": "analyze",
  "object": "sales_data",
  "constraints": ["completeness"],
  "style": "professional"
}
```

### Constraint Consolidation

```python
# Before: Conflicting constraints
constraints = ["thorough", "quick", "detailed", "brief"]

# After: Resolved constraints
constraints = ["balanced"]  # Automatically resolved
```

### Intent Disambiguation

```python
# Ambiguous input
"Look at this data"

# Context-aware IR
{
  "intent": "analyze",
  "object": "data",
  "confidence": 0.7,
  "fallback_intent": "examine"
}
```

---

## 🔧 IR Customization

### Adding Custom Intents

```python
from privysha.ir.ir_builder import IRBuilder

builder = IRBuilder()
builder.add_intent_pattern("visualize", ["plot", "chart", "graph", "visualize"])

# Now recognizes visualization requests
ir = builder.generate("Create a chart of the sales data")
```

### Custom Constraints

```python
# Add domain-specific constraints
builder.add_constraint_pattern("gdpr_compliant", ["gdpr", "privacy", "compliant"])
builder.add_constraint_pattern("real_time", ["live", "real-time", "streaming"])
```

### Style Templates

```python
# Define custom styles
builder.add_style_template("legal", {
    "formality": "high",
    "precision": "high",
    "structure": "structured"
})
```

---

## 🔍 IR Debugging

### Trace IR Generation

```python
result = agent.run("Analyze data", trace=True)

# IR generation trace
print(result["ir_trace"])
# {
#   "stage": "ir_generation",
#   "input": "Analyze data",
#   "tokens": ["analyze", "data"],
#   "entities": ["data"],
#   "intent_confidence": 0.95,
#   "object_confidence": 0.88,
#   "ir": {...}
# }
```

### IR Validation

```python
from privysha.ir.prompt_ir import PromptIR

ir = PromptIR({
    "intent": "analyze",
    "object": "data"
})

# Validate IR structure
if ir.is_valid():
    print("IR is valid")
else:
    print("IR errors:", ir.get_errors())
```

### Manual IR Creation

```python
from privysha.ir.prompt_ir import PromptIR

# Create IR manually for testing
ir = PromptIR({
    "intent": "analyze",
    "object": "dataset",
    "constraints": ["speed"],
    "style": "concise"
})

# Use directly with compiler
from privysha.compiler.prompt_compiler import PromptCompiler
compiler = PromptCompiler()
final_prompt = compiler.compile(ir)
```

---

## 🎯 Advanced IR Features

### Contextual IR

```python
# Maintains conversation context
conversation = [
    {"role": "user", "content": "Analyze sales data"},
    {"role": "assistant", "content": "Sales increased 15%"},
    {"role": "user", "content": "What about last year?"}
]

# IR understands context
ir = builder.generate("What about last year?", context=conversation)
# {"intent": "compare", "object": "yearly_sales", "timeframe": "last_year"}
```

### Multi-Intent IR

```python
# Complex requests with multiple intents
"Analyze the data and create a summary report"

# Generates compound IR
{
  "primary_intent": "analyze",
  "secondary_intent": "generate",
  "object": "data",
  "output_format": "summary_report"
}
```

### Conditional IR

```python
# IR with conditional logic
{
  "intent": "analyze",
  "object": "data",
  "conditions": {
    "if_data_size_large": {"constraints": ["sampling"]},
    "if_pii_detected": {"privacy": {"level": "high"}}
  }
}
```

---

## 📊 IR Analytics

### Intent Distribution

```python
# Track which intents are most common
analytics = agent.get_intent_analytics()
# {
#   "analyze": 45,
#   "generate": 32,
#   "classify": 18,
#   "extract": 5
# }
```

### Optimization Impact

```python
# Measure IR optimization effectiveness
metrics = agent.get_optimization_metrics()
# {
#   "average_token_reduction": 68.3,
#   "processing_time_ms": 234,
#   "ir_accuracy": 0.94
# }
```

---

## 🚀 Why Prompt IR Matters

### For Developers

- **Predictable** - Same input → same IR structure
- **Testable** - Each component can be unit tested
- **Extensible** - Add custom intents and constraints
- **Debuggable** - Full visibility into generation process

### For Businesses

- **Consistent** - Standardized prompt processing
- **Optimizable** - Systematic improvements
- **Measurable** - Quantifiable optimization metrics
- **Secure** - Built-in privacy controls

### For Users

- **Better Results** - Structured understanding of intent
- **Faster** - Optimized prompts → quicker responses
- **Private** - Automatic PII protection
- **Reliable** - Consistent behavior

---

## 🎯 Next Steps

Now that you understand Prompt IR:

1. **[See Pipeline Integration](pipeline.md)** - How IR fits in processing
2. **[Learn Optimization](optimization.md)** - How IR enables optimization
3. **[Check Examples](examples.md)** - IR in real applications
4. **[API Reference](api-reference.md)** - Full IR API documentation

---

*Ready to see how IR powers the entire pipeline? Check out the [Pipeline documentation](pipeline.md)!*
