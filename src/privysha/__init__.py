# Copyright 2026 Ajay Rajan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
PrivySHA - Prompt Compiler Infrastructure for LLM Systems

This package provides a unified interface for v2 functionality while maintaining
backward compatibility with v1 code.

Simple usage (backward compatible):
    from privysha import Agent
    
    agent = Agent(model="gpt-4o-mini")
    response = agent.run("Analyze this dataset")

Advanced usage (v2 features):
    from privysha import Agent, PromptIR, SecurityLayer, ModelRouter
    
    agent = Agent(
        model="gpt-4o-mini",
        fallback_providers=[{"provider": "anthropic", "model": "claude-3-haiku"}]
    )
"""

# Core v1-compatible components
from .agent import Agent
from .pipeline import Pipeline
from .adapters.factory import AdapterFactory

# Advanced v2 components for power users
from .ir.prompt_ir import PromptIR, IntentType, EntityType, ConstraintType, PrivacyLevel
from .ir.ir_builder import IRBuilder
from .compiler.prompt_compiler import PromptCompiler
from .compiler.optimizer_engine import PromptOptimizer
from .security.security_layer import SecurityLayer, SecurityResult, SecurityLevel, ThreatType
from .routing.model_router import ModelRouter, RoutingDecision, RoutingStrategy, ModelConfig, ModelCapability
from .debug.debugger import PrivySHADebugger, DebugTrace, PipelineStage, MetricsCollector

# Universal adapter system
from .adapters.universal_adapter import UniversalModelAdapter

__all__ = [
    # Core v1 API (backward compatible)
    "Agent",
    "Pipeline", 
    "AdapterFactory",
    
    # Advanced v2 components
    "PromptIR",
    "IntentType",
    "EntityType",
    "ConstraintType", 
    "PrivacyLevel",
    "IRBuilder",
    "PromptCompiler",
    "PromptOptimizer",
    "SecurityLayer",
    "SecurityResult",
    "SecurityLevel",
    "ThreatType",
    "ModelRouter",
    "RoutingDecision",
    "RoutingStrategy",
    "ModelConfig",
    "ModelCapability",
    "PrivySHADebugger",
    "DebugTrace",
    "PipelineStage",
    "MetricsCollector",
    "UniversalModelAdapter"
]