# Pipeline Documentation

The PrivySHA pipeline is a multi-stage processing system that transforms raw prompts into optimized, secure, and efficient instructions for LLMs.

---

## 🏗️ Pipeline Overview

```
Raw Prompt
    ↓
Sanitization Stage
    ↓
PII Detection Stage
    ↓
IR Generation Stage
    ↓
Optimization Stage
    ↓
Compilation Stage
    ↓
Model Gateway
    ↓
Response Processing
    ↓
Final Output
```

Each stage has clear responsibilities, inputs/outputs, and can be customized or disabled.

---

## 🧼 Stage 1: Sanitization

**Purpose**: Clean and normalize raw input

### Input
```python
raw_prompt = "Hey bro, can you analyze   this data???!   \n\nThanks!"
```

### Processing
```python
# Text normalization
cleaned = normalize_text(raw_prompt)
# Remove excessive whitespace, normalize punctuation

# Content filtering
filtered = filter_content(cleaned)
# Remove harmful or inappropriate content

# Language detection
language = detect_language(filtered)
# Identify processing language
```

### Output
```python
sanitized_prompt = "Can you analyze this data?"
metadata = {
    "original_length": 42,
    "sanitized_length": 23,
    "language": "en",
    "content_filtered": False
}
```

### Customization
```python
from privysha.stages.sanitizer import SanitizerStage

sanitizer = SanitizerStage(
    normalize_whitespace=True,
    remove_excessive_punctuation=True,
    filter_content=True,
    detect_language=True,
    custom_filters=["slang", "informal_language"]
)
```

---

## 🔒 Stage 2: PII Detection

**Purpose**: Identify and protect sensitive information

### Input
```python
prompt = "Contact john@email.com or call 555-0123 about customer data"
```

### Processing
```python
# PII pattern matching
pii_detected = pii_detector.scan(prompt)
# Email, phone, SSN, credit card, etc.

# Context analysis
context = analyze_pii_context(prompt)
# Is PII being requested to be processed?

# Risk assessment
risk_level = assess_pii_risk(pii_detected, context)
# Low, medium, high risk
```

### Output
```python
masked_prompt = "Contact [EMAIL] or call [PHONE] about customer data"
pii_result = {
    "pii_detected": ["email", "phone"],
    "pii_masked": 2,
    "risk_level": "medium",
    "masking_applied": True
}
```

### PII Types Detected
- **Email**: `user@domain.com`
- **Phone**: `555-0123`, `(555) 123-4567`
- **SSN**: `123-45-6789`
- **Credit Card**: `4111-1111-1111-1111`
- **Address**: `123 Main St, City, State`
- **Name**: `John Doe`, `Jane Smith`
- **Custom**: Configurable patterns

### Customization
```python
from privysha.stages.sanitizer import PIIDetector

detector = PIIDetector(
    detect_email=True,
    detect_phone=True,
    detect_ssn=True,
    detect_custom_patterns=True,
    custom_patterns={
        "employee_id": r"EMP\d{6}",
        "project_code": r"PROJ-[A-Z]{3}-\d{4}"
    }
)
```

---

## 🧠 Stage 3: IR Generation

**Purpose**: Convert structured prompt to Intermediate Representation

### Input
```python
prompt = "Analyze customer data for patterns and anomalies"
```

### Processing
```python
# Tokenization
tokens = tokenize(prompt)
# ["analyze", "customer", "data", "patterns", "anomalies"]

# Entity recognition
entities = extract_entities(tokens)
# ["customer_data", "patterns", "anomalies"]

# Intent classification
intent = classify_intent(tokens, entities)
# "analyze"

# Constraint extraction
constraints = extract_constraints(tokens)
# ["pattern_detection", "anomaly_detection"]

# IR construction
ir = build_ir(intent, entities, constraints)
```

### Output
```json
{
  "intent": "analyze",
  "object": "customer_data",
  "constraints": ["pattern_detection", "anomaly_detection"],
  "style": "analytical",
  "metadata": {
    "confidence": 0.92,
    "domain": "data_analysis",
    "complexity": "medium"
  }
}
```

### Customization
```python
from privysha.ir.ir_builder import IRBuilder

builder = IRBuilder(
    custom_intents={"visualize": ["plot", "chart", "graph"]},
    custom_constraints=["gdpr_compliant", "real_time"],
    confidence_threshold=0.8
)
```

---

## ⚡ Stage 4: Optimization

**Purpose**: Reduce token usage and improve efficiency

### Input
```json
{
  "intent": "analyze",
  "object": "comprehensive_customer_sales_dataset",
  "constraints": ["thorough_analysis", "detailed_examination"]
}
```

### Processing
```python
# Token estimation
original_tokens = estimate_tokens(ir)

# Constraint optimization
optimized_constraints = optimize_constraints(ir.constraints)
# Remove redundant constraints

# Object simplification
optimized_object = simplify_object(ir.object)
# "comprehensive_customer_sales_dataset" → "sales_data"

# Style optimization
optimized_style = optimize_style(ir.style)
# Choose most efficient style

# Target calculation
target_tokens = calculate_optimal_target(ir)
```

### Output
```json
{
  "intent": "analyze",
  "object": "sales_data",
  "constraints": ["thorough"],
  "style": "concise",
  "optimization_metrics": {
    "original_tokens": 120,
    "optimized_tokens": 38,
    "reduction_percentage": 68.3
  }
}
```

### Optimization Techniques
- **Constraint consolidation**: Merge similar constraints
- **Object simplification**: Remove redundant descriptors
- **Style optimization**: Choose most efficient style
- **Token estimation**: Accurate token counting
- **Semantic preservation**: Maintain meaning while reducing

### Customization
```python
from privysha.compiler.optimizer_engine import PromptOptimizer

optimizer = PromptOptimizer(
    optimization_level="aggressive",  # conservative, balanced, aggressive
    target_reduction=0.6,  # Target 60% reduction
    preserve_semantics=True,
    custom_optimizers=["domain_specific"]
)
```

---

## 🔧 Stage 5: Compilation

**Purpose**: Convert optimized IR to final prompt

### Input
```json
{
  "intent": "analyze",
  "object": "sales_data",
  "constraints": ["thorough"],
  "style": "concise"
}
```

### Processing
```python
# Template selection
template = select_template(ir.intent, ir.style)

# Variable substitution
prompt = substitute_variables(template, ir)

# Format optimization
final_prompt = optimize_format(prompt)

# Validation
validated_prompt = validate_prompt(final_prompt)
```

### Output
```python
final_prompt = "Analyze sales data thoroughly"
compilation_metadata = {
    "template_used": "analyze_concise",
    "variables_substituted": ["object", "constraint"],
    "final_tokens": 8
}
```

### Template Examples
```python
# Analysis templates
ANALYSIS_TEMPLATES = {
    "concise": "Analyze {object} {constraint}",
    "detailed": "Please provide a comprehensive analysis of {object}, focusing on {constraint}",
    "technical": "Perform technical analysis of {object} with emphasis on {constraint}"
}

# Generation templates
GENERATION_TEMPLATES = {
    "formal": "Generate a formal {object} that {constraint}",
    "casual": "Create a {object} that {constraint}",
    "technical": "Produce a technical {object} incorporating {constraint}"
}
```

### Customization
```python
from privysha.compiler.prompt_compiler import PromptCompiler

compiler = PromptCompiler(
    custom_templates={
        "analyze_visual": "Create visualization of {object} showing {constraint}",
        "generate_report": "Generate {object} report with {constraint}"
    }
)
```

---

## 🌐 Stage 6: Model Gateway

**Purpose**: Route to appropriate LLM provider

### Input
```python
prompt = "Analyze sales data thoroughly"
ir = {...}  # From previous stages
```

### Processing
```python
# Model selection
model = select_model(ir.intent, ir.complexity)

# Provider routing
provider = route_to_provider(model)

# API call preparation
api_params = prepare_api_call(prompt, model, provider)

# Execution with fallbacks
response = execute_with_fallbacks(api_params, provider)
```

### Output
```python
response = "The sales data shows..."
gateway_metadata = {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "fallback_used": False,
    "response_time_ms": 1234,
    "tokens_used": 45
}
```

### Routing Logic
```python
def select_model(intent, complexity):
    if intent == "analyze" and complexity == "low":
        return "gpt-3.5-turbo"
    elif intent == "analyze" and complexity == "high":
        return "gpt-4"
    elif intent == "generate":
        return "claude-3-haiku"
    else:
        return "gpt-4o-mini"
```

### Customization
```python
from privysha.routing.model_router import ModelRouter

router = ModelRouter(
    routing_strategy="cost_optimized",  # cost_optimized, performance_optimized, balanced
    fallback_providers=[
        {"provider": "anthropic", "model": "claude-3-haiku"},
        {"provider": "local", "model": "llama-2-7b"}
    ]
)
```

---

## 📝 Stage 7: Response Processing

**Purpose**: Process and format LLM response

### Input
```python
raw_response = "The sales data shows three main patterns..."
metadata = {...}
```

### Processing
```python
# Response validation
validated = validate_response(raw_response)

# Format optimization
formatted = format_response(validated, ir.style)

# Metadata extraction
response_metadata = extract_metadata(raw_response)

# Final assembly
final_result = assemble_result(formatted, response_metadata, metadata)
```

### Output
```python
final_result = {
    "response": "The sales data shows three main patterns...",
    "metadata": {
        "response_tokens": 67,
        "processing_time_ms": 1567,
        "model_used": "gpt-4o-mini"
    }
}
```

---

## 🔧 Pipeline Customization

### Custom Stages
```python
from privysha.pipeline import Pipeline

# Create custom stage
class CustomPreprocessor:
    def process(self, prompt, metadata):
        # Custom preprocessing logic
        return processed_prompt, new_metadata

# Add to pipeline
pipeline = Pipeline()
pipeline.add_stage("custom_preprocessor", CustomPreprocessor(), position=1)
```

### Stage Configuration
```python
pipeline = Pipeline(
    enable_sanitization=True,
    enable_pii_detection=True,
    enable_ir_generation=True,
    enable_optimization=True,
    enable_compilation=True,
    custom_config={
        "sanitization": {"normalize_whitespace": True},
        "pii_detection": {"detect_email": True},
        "optimization": {"level": "balanced"}
    }
)
```

### Stage Bypassing
```python
# Skip optimization for simple prompts
pipeline = Pipeline()
pipeline.configure({
    "enable_optimization": lambda ir: ir.complexity < 3
})
```

---

## 🔍 Pipeline Debugging

### Full Trace Mode
```python
result = agent.run("Analyze data", trace=True)

# Complete pipeline trace
trace = result["pipeline_trace"]
for stage in trace:
    print(f"{stage['name']}: {stage['input']} → {stage['output']}")
```

### Stage Metrics
```python
# Per-stage performance
metrics = pipeline.get_stage_metrics()
# {
#   "sanitization": {"time_ms": 12, "success_rate": 1.0},
#   "pii_detection": {"time_ms": 45, "pii_found": 2},
#   "ir_generation": {"time_ms": 23, "confidence": 0.92},
#   "optimization": {"time_ms": 34, "reduction": 0.68}
# }
```

### Error Handling
```python
# Stage-specific error handling
pipeline = Pipeline()
pipeline.add_error_handler("pii_detection", PIIErrorHandler())
pipeline.add_error_handler("model_gateway", RetryHandler(max_retries=3))
```

---

## 📊 Pipeline Performance

### Typical Processing Times
```python
{
    "sanitization": 12,      # ms
    "pii_detection": 45,      # ms
    "ir_generation": 23,      # ms
    "optimization": 34,        # ms
    "compilation": 8,          # ms
    "model_gateway": 1234,     # ms (API call)
    "response_processing": 15,  # ms
    "total": 1371             # ms
}
```

### Memory Usage
```python
{
    "peak_memory_mb": 45,
    "stage_memory": {
        "sanitization": 2,
        "pii_detection": 8,
        "ir_generation": 12,
        "optimization": 15,
        "compilation": 3
    }
}
```

---

## 🚀 Pipeline Best Practices

### Performance Optimization
```python
# Enable caching for repeated patterns
pipeline = Pipeline(enable_cache=True)

# Use batch processing for multiple prompts
results = pipeline.process_batch([
    "Analyze data A",
    "Analyze data B", 
    "Analyze data C"
])
```

### Error Recovery
```python
# Configure robust error handling
pipeline = Pipeline(
    error_recovery_mode="graceful",  # strict, graceful
    fallback_on_error=True,
    error_notification=True
)
```

### Monitoring
```python
# Enable detailed logging
pipeline = Pipeline(
    log_level="debug",
    metrics_collection=True,
    performance_tracking=True
)
```

---

## 🎯 Next Steps

Now that you understand the pipeline:

1. **[Learn Model Gateway](model-gateway.md)** - Multi-provider support
2. **[Explore Security](security.md)** - PII and injection protection
3. **[Check Optimization](optimization.md)** - Token reduction techniques
4. **[See Examples](examples.md)** - Pipeline in action

---

*Ready to see how the pipeline connects to different LLM providers? Check out the [Model Gateway documentation](model-gateway.md)!*
