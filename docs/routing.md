# Routing

PrivySHA's intelligent routing system automatically selects the best model for each request based on task complexity, cost constraints, and performance requirements.

---

## 🧠 Routing Overview

### Why Intelligent Routing?

**Traditional Approach:**
```
User → Single Model → Response
```
**Problems:**
- Over-provisioning for simple tasks
- Under-provisioning for complex tasks
- No cost optimization
- Single point of failure

**PrivySHA Routing:**
```
User → Task Analysis → Best Model → Response
```
**Benefits:**
- Optimal cost-performance balance
- Automatic fallbacks
- Load balancing
- Reliability

---

## 🎯 Routing Strategies

### Cost Optimized

```python
from privysha import Agent

agent = Agent(
    model="auto",
    routing_strategy="cost_optimized"
)
```

**Logic:**
- Simple tasks → Cheapest capable model
- Medium tasks → Balanced cost-performance
- Complex tasks → Justified expensive models

**Example Routing:**
```python
def cost_optimized_routing(task_analysis):
    complexity = task_analysis.complexity
    intent = task_analysis.intent
    
    if complexity == "low":
        return {"provider": "openai", "model": "gpt-3.5-turbo"}
    elif complexity == "medium":
        return {"provider": "openai", "model": "gpt-4o-mini"}
    elif complexity == "high":
        return {"provider": "openai", "model": "gpt-4o"}
    else:
        return {"provider": "anthropic", "model": "claude-3-opus"}
```

### Performance Optimized

```python
agent = Agent(
    model="auto",
    routing_strategy="performance_optimized"
)
```

**Logic:**
- Always use best available model
- Prioritize speed and quality
- Ignore cost constraints

**Example Routing:**
```python
def performance_optimized_routing(task_analysis):
    intent = task_analysis.intent
    
    if intent == "generate":
        return {"provider": "anthropic", "model": "claude-3-opus"}
    elif intent == "analyze":
        return {"provider": "openai", "model": "gpt-4o"}
    elif intent == "code":
        return {"provider": "anthropic", "model": "claude-3-sonnet"}
    else:
        return {"provider": "openai", "model": "gpt-4o"}
```

### Balanced (Default)

```python
agent = Agent(
    model="auto",
    routing_strategy="balanced"
)
```

**Logic:**
- Balance cost and performance
- Consider task requirements
- Optimize for overall value

**Example Routing:**
```python
def balanced_routing(task_analysis):
    complexity = task_analysis.complexity
    intent = task_analysis.intent
    time_sensitive = task_analysis.time_sensitive
    
    if time_sensitive:
        # Prioritize speed for urgent tasks
        return {"provider": "anthropic", "model": "claude-3-haiku"}
    elif complexity == "high" and intent == "analyze":
        return {"provider": "openai", "model": "gpt-4o"}
    elif complexity == "low":
        return {"provider": "openai", "model": "gpt-4o-mini"}
    else:
        return {"provider": "anthropic", "model": "claude-3-sonnet"}
```

---

## 🔧 Task Analysis

### Complexity Assessment

```python
# Task complexity factors
complexity_factors = {
    "semantic_depth": 0.3,      # How deep is the understanding needed?
    "creativity_required": 0.2,  # How creative must the response be?
    "domain_knowledge": 0.2,    # How specialized is the domain?
    "response_length": 0.1,       # How long will the response be?
    "reasoning_steps": 0.2        # How many reasoning steps?
}
```

### Complexity Scoring

```python
def calculate_complexity(task_ir):
    score = 0
    
    # Semantic depth
    if task_ir.intent in ["analyze", "synthesize"]:
        score += 0.3
    elif task_ir.intent in ["generate", "create"]:
        score += 0.2
    
    # Domain knowledge
    if task_ir.metadata.get("domain") in ["medical", "legal", "finance"]:
        score += 0.2
    elif task_ir.metadata.get("domain") in ["technical", "scientific"]:
        score += 0.1
    
    # Response requirements
    if "detailed" in task_ir.constraints:
        score += 0.1
    if "comprehensive" in task_ir.constraints:
        score += 0.1
    
    return min(score, 1.0)  # Cap at 1.0
```

### Intent-Based Routing

```python
INTENT_ROUTING_MAP = {
    "analyze": {
        "low": {"provider": "openai", "model": "gpt-4o-mini"},
        "medium": {"provider": "openai", "model": "gpt-4o"},
        "high": {"provider": "anthropic", "model": "claude-3-sonnet"}
    },
    "generate": {
        "low": {"provider": "anthropic", "model": "claude-3-haiku"},
        "medium": {"provider": "anthropic", "model": "claude-3-sonnet"},
        "high": {"provider": "anthropic", "model": "claude-3-opus"}
    },
    "code": {
        "low": {"provider": "openai", "model": "gpt-4o-mini"},
        "medium": {"provider": "openai", "model": "gpt-4o"},
        "high": {"provider": "anthropic", "model": "claude-3-sonnet"}
    },
    "classify": {
        "low": {"provider": "openai", "model": "gpt-3.5-turbo"},
        "medium": {"provider": "openai", "model": "gpt-4o-mini"},
        "high": {"provider": "anthropic", "model": "claude-3-haiku"}
    }
}
```

---

## 🔄 Fallback System

### Primary-Fallback Chain

```python
agent = Agent(
    model="gpt-4o-mini",
    fallback_providers=[
        {"provider": "anthropic", "model": "claude-3-haiku"},
        {"provider": "openai", "model": "gpt-3.5-turbo"},
        {"provider": "local", "model": "llama-2-7b"}
    ]
)
```

### Fallback Triggers

```python
FALLBACK_TRIGGERS = {
    "rate_limit": {"action": "fallback", "delay": 60},
    "timeout": {"action": "fallback", "delay": 0},
    "api_error": {"action": "fallback", "delay": 5},
    "model_unavailable": {"action": "fallback", "delay": 0},
    "cost_threshold": {"action": "fallback", "delay": 0},
    "quality_threshold": {"action": "fallback", "delay": 0}
}
```

### Fallback Logic

```python
def execute_with_fallbacks(request, providers):
    for i, provider in enumerate(providers):
        try:
            response = call_provider(provider, request)
            
            # Quality check
            if validate_response_quality(response):
                return {
                    "response": response,
                    "provider_used": provider,
                    "fallback_index": i,
                    "success": True
                }
            elif i < len(providers) - 1:
                continue  # Try next provider
            else:
                return {"response": response, "quality_issue": True}
                
        except Exception as e:
            if i < len(providers) - 1:
                continue  # Try next provider
            else:
                raise e  # All providers failed
```

---

## 📊 Routing Analytics

### Performance Tracking

```python
# Get routing statistics
routing_stats = agent.get_routing_stats()
# {
#   "total_requests": 1000,
#   "routing_decisions": {
#     "gpt-4o-mini": 450,
#     "gpt-4o": 300,
#     "claude-3-haiku": 150,
#     "claude-3-sonnet": 100
#   },
#   "fallback_usage": {
#     "total_fallbacks": 45,
#     "fallback_rate": 0.045,
#     "most_common_fallback": "gpt-4o-mini → claude-3-haiku"
#   },
#   "cost_distribution": {
#     "openai": 0.75,
#     "anthropic": 0.23,
#     "local": 0.02
#   }
# }
```

### Cost Analysis

```python
# Routing cost analysis
cost_analysis = agent.get_routing_cost_analysis()
# {
#   "total_cost_usd": 12.45,
#   "cost_per_request": 0.01245,
#   "savings_from_routing": 3.21,
#   "savings_percentage": 20.5,
#   "model_efficiency": {
#     "gpt-4o-mini": {"cost_per_quality": 0.0001},
#     "gpt-4o": {"cost_per_quality": 0.0003},
#     "claude-3-haiku": {"cost_per_quality": 0.00015}
#   }
# }
```

### Quality Metrics

```python
# Quality by model
quality_metrics = agent.get_quality_by_model()
# {
#   "gpt-4o-mini": {
#     "avg_quality_score": 0.85,
#     "success_rate": 0.95,
#     "user_satisfaction": 0.82
#   },
#   "gpt-4o": {
#     "avg_quality_score": 0.92,
#     "success_rate": 0.98,
#     "user_satisfaction": 0.91
#   },
#   "claude-3-haiku": {
#     "avg_quality_score": 0.88,
#     "success_rate": 0.96,
#     "user_satisfaction": 0.86
#   }
# }
```

---

## 🎛️ Custom Routing

### Custom Routing Functions

```python
def custom_routing_function(task_ir, context):
    # Business-specific routing logic
    if task_ir.metadata.get("department") == "legal":
        return {"provider": "anthropic", "model": "claude-3-opus"}
    elif task_ir.metadata.get("department") == "engineering":
        return {"provider": "openai", "model": "gpt-4o"}
    elif task_ir.metadata.get("priority") == "urgent":
        return {"provider": "anthropic", "model": "claude-3-haiku"}
    elif task_ir.privacy.get("level") == "high":
        return {"provider": "local", "model": "llama-2-7b"}
    else:
        return {"provider": "openai", "model": "gpt-4o-mini"}

agent = Agent(
    model="auto",
    routing_strategy=custom_routing_function
)
```

### Rule-Based Routing

```python
routing_rules = [
    {
        "condition": "intent == 'analyze' and complexity > 0.7",
        "action": {"provider": "openai", "model": "gpt-4o"},
        "priority": 1
    },
    {
        "condition": "intent == 'generate' and time_sensitive == True",
        "action": {"provider": "anthropic", "model": "claude-3-haiku"},
        "priority": 2
    },
    {
        "condition": "privacy.level == 'high'",
        "action": {"provider": "local", "model": "llama-2-7b"},
        "priority": 0  # Highest priority
    }
]

agent = Agent(
    model="auto",
    routing_rules=routing_rules
)
```

### ML-Based Routing

```python
# Train routing model
routing_model = train_routing_model(
    historical_data=usage_data,
    features=["intent", "complexity", "domain", "time_sensitive"],
    target="best_provider"
)

agent = Agent(
    model="auto",
    routing_strategy="ml_based",
    routing_model=routing_model
)
```

---

## 🚀 Advanced Routing Features

### Load Balancing

```python
agent = Agent(
    model="gpt-4o-mini",
    load_balancing="weighted_round_robin",
    provider_instances=[
        {"provider": "openai", "weight": 3, "api_key": "key1"},
        {"provider": "openai", "weight": 2, "api_key": "key2"},
        {"provider": "anthropic", "weight": 1, "api_key": "key3"}
    ]
)
```

### Geographic Routing

```python
def geographic_routing(task_ir, user_location):
    # Route to nearest data center
    if user_location.region == "europe":
        return {"provider": "anthropic", "model": "claude-3-haiku"}
    elif user_location.region == "asia":
        return {"provider": "openai", "model": "gpt-4o-mini"}
    else:
        return {"provider": "openai", "model": "gpt-4o"}

agent = Agent(
    model="auto",
    routing_strategy=geographic_routing,
    detect_location=True
)
```

### Time-Based Routing

```python
def time_based_routing(task_ir, current_time):
    # Route based on time and availability
    if current_time.hour < 6:  # Off-peak
        return {"provider": "openai", "model": "gpt-3.5-turbo"}
    elif current_time.hour < 18:  # Business hours
        return {"provider": "openai", "model": "gpt-4o-mini"}
    else:  # Peak hours
        return {"provider": "anthropic", "model": "claude-3-haiku"}

agent = Agent(
    model="auto",
    routing_strategy=time_based_routing
)
```

---

## 🔍 Routing Debugging

### Routing Trace

```python
result = agent.run("Analyze complex data", trace=True)

# Routing decision trace
print(result["routing_trace"])
# {
#   "task_analysis": {
#     "intent": "analyze",
#     "complexity": 0.8,
#     "domain": "data_analysis",
#     "time_sensitive": False
#   },
#   "routing_decision": {
#     "strategy": "balanced",
#     "selected_model": "gpt-4o",
#     "reasoning": "High complexity analysis task",
#     "alternatives_considered": ["gpt-4o-mini", "claude-3-sonnet"]
#   },
#   "fallback_info": {
#     "fallbacks_available": True,
#     "fallback_chain": ["claude-3-haiku", "gpt-3.5-turbo"],
#     "fallback_used": False
#   }
# }
```

### A/B Testing

```python
# Test routing strategies
ab_test = agent.test_routing_strategy(
    strategy_a="cost_optimized",
    strategy_b="balanced",
    test_duration_hours=24,
    success_metric="user_satisfaction"
)

# Results
# {
#   "strategy_a": {"satisfaction": 0.82, "cost": 0.08},
#   "strategy_b": {"satisfaction": 0.87, "cost": 0.12},
#   "winner": "strategy_b",
#   "confidence": 0.94
# }
```

---

## 🎯 Best Practices

### Production Routing

```python
agent = Agent(
    model="auto",
    routing_strategy="balanced",
    fallback_providers=[
        {"provider": "anthropic", "model": "claude-3-haiku"},
        {"provider": "openai", "model": "gpt-3.5-turbo"}
    ],
    routing_config={
        "enable_load_balancing": True,
        "enable_geographic_routing": True,
        "cache_routing_decisions": True,
        "monitor_routing_performance": True
    }
)
```

### Cost Control

```python
agent = Agent(
    model="auto",
    routing_strategy="cost_optimized",
    cost_limits={
        "per_request_limit": 0.01,
        "daily_limit": 10.0,
        "monthly_limit": 200.0
    },
    budget_alerts={
        "threshold": 0.8,
        "notification": "email"
    }
)
```

### Performance Monitoring

```python
agent = Agent(
    model="auto",
    routing_strategy="balanced",
    monitoring={
        "track_routing_decisions": True,
        "track_fallback_usage": True,
        "track_cost_efficiency": True,
        "track_quality_metrics": True,
        "alert_on_degradation": True
    }
)
```

---

## 🎯 Next Steps

Now that you understand routing:

1. **[Learn Debugging](debugging.md)** - Full pipeline tracing
2. **[Explore Examples](examples.md)** - Routing in action
3. **[Check API Reference](api-reference.md)** - Full routing API
4. **[See FAQ](faq.md)** - Common routing questions

---

*Ready to debug your LLM pipeline? Check out the [Debugging documentation](debugging.md)!*
