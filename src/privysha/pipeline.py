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

from typing import Dict, List, Any, Optional, Union
import time
from .ir.ir_builder import IRBuilder
from .security.security_layer import SecurityLayer, SecurityLevel
from .routing.model_router import ModelRouter, RoutingStrategy
from .compiler.prompt_compiler import PromptCompiler
from .compiler.optimizer_engine import PromptOptimizer
from .debug.debugger import PrivySHADebugger
from .adapters.universal_adapter import UniversalModelAdapter


class Pipeline:
    """
    Complete PrivySHA v2 Pipeline with all advanced features.
    
    This class provides v1 compatibility while including all v2 functionality
    directly. No separate enhanced files needed.
    
    Processing Flow:
    1. Raw Prompt → IR Generation
    2. IR → Security Processing
    3. Security Result → Model Routing
    4. Routing Decision → Prompt Compilation
    5. Compiled Prompt → Optimization
    6. Optimized Prompt → Model Generation
    7. Full Debug Trace Collection
    """

    def __init__(self, privacy: bool = True, token_budget: int = 1200,
                 security_level: SecurityLevel = SecurityLevel.MEDIUM,
                 routing_strategy: RoutingStrategy = RoutingStrategy.HYBRID,
                 debug_enabled: bool = False,
                 optimization_targets: List[str] = None):
        """
        Initialize pipeline with v2 capabilities.
        
        Args:
            privacy: Enable privacy features
            token_budget: Token budget for optimization
            security_level: Security processing level
            routing_strategy: Model routing strategy
            debug_enabled: Enable debug tracing
            optimization_targets: List of optimization targets
        """
        # Store original parameters for compatibility
        self.privacy = privacy
        self.token_budget = token_budget
        
        # Map privacy to security level if not explicitly provided
        if security_level == SecurityLevel.MEDIUM and privacy:
            security_level = SecurityLevel.HIGH
        
        self.security_level = security_level
        self.routing_strategy = routing_strategy
        self.debug_enabled = debug_enabled
        self.optimization_targets = optimization_targets or ["tokens", "accuracy"]
        
        # Initialize components
        self.ir_builder = IRBuilder()
        self.security_layer = SecurityLayer(security_level)
        self.model_router = ModelRouter(default_strategy=routing_strategy)
        self.prompt_compiler = PromptCompiler()
        self.prompt_optimizer = PromptOptimizer()
        self.debugger = PrivySHADebugger(enabled=debug_enabled, trace_level="detailed")

    def process(self, content: str, adapter: UniversalModelAdapter = None,
                constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process content through complete v2 pipeline.
        
        Args:
            content: Input content
            adapter: Universal model adapter (optional)
            constraints: Additional constraints
            
        Returns:
            Complete processing result with all metrics and traces
        """
        # Start debug trace
        session_id = self.debugger.start_trace(content)
        
        try:
            # Stage 1: IR Generation
            start_time = time.time()
            ir = self.ir_builder.parse(content)
            ir_time = (time.time() - start_time) * 1000
            self.debugger.add_stage("ir_generation", content, ir.to_dict().__str__(), True, None, 
                                   {"execution_time_ms": ir_time, "complexity": ir.get_complexity_level()})
            self.debugger.set_ir_representation(ir)
            
            # Stage 2: Security Processing
            start_time = time.time()
            security_result = self.security_layer.process(content)
            security_time = (time.time() - start_time) * 1000
            self.debugger.add_stage("security_processing", content, security_result.sanitized_content, 
                                   security_result.is_safe, None if security_result.is_safe else "Security threats detected",
                                   {"execution_time_ms": security_time, "threats": len(security_result.detected_threats)})
            self.debugger.set_security_result(security_result)
            
            # Check if content is safe
            if not security_result.is_safe:
                final_trace = self.debugger.finalize_trace()
                return {
                    "success": False,
                    "error": "Content blocked by security layer",
                    "security_result": security_result,
                    "debug_trace": final_trace,
                    "session_id": session_id
                }
            
            # Stage 3: Model Routing
            start_time = time.time()
            routing_decision = self.model_router.route(ir, constraints=constraints or {})
            routing_time = (time.time() - start_time) * 1000
            self.debugger.add_stage("model_routing", ir.to_dict().__str__(), routing_decision.selected_model.name,
                                   True, None, {"execution_time_ms": routing_time, "confidence": routing_decision.confidence_score})
            self.debugger.set_routing_decision(routing_decision)
            
            # Stage 4: Prompt Compilation
            start_time = time.time()
            compiled_prompt = self.prompt_compiler.compile(ir, optimization_level="standard")
            compilation_time = (time.time() - start_time) * 1000
            self.debugger.add_stage("prompt_compilation", ir.to_dict().__str__(), compiled_prompt,
                                   True, None, {"execution_time_ms": compilation_time, "tokens": len(compiled_prompt.split())})
            
            # Stage 5: Prompt Optimization
            start_time = time.time()
            optimized_prompt, optimization_metrics = self.prompt_optimizer.optimize(compiled_prompt, ir, self.optimization_targets)
            optimization_time = (time.time() - start_time) * 1000
            self.debugger.add_stage("prompt_optimization", compiled_prompt, optimized_prompt,
                                   True, None, {"execution_time_ms": optimization_time, "token_reduction": optimization_metrics["token_reduction_percentage"]})
            
            # Stage 6: Model Generation (if adapter provided)
            response = None
            if adapter:
                start_time = time.time()
                try:
                    response = adapter.generate(optimized_prompt)
                    generation_time = (time.time() - start_time) * 1000
                    self.debugger.add_stage("model_generation", optimized_prompt, response,
                                           True, None, {"execution_time_ms": generation_time, "model": adapter.provider})
                    self.debugger.set_final_response(response)
                except Exception as e:
                    generation_time = (time.time() - start_time) * 1000
                    self.debugger.add_stage("model_generation", optimized_prompt, str(e),
                                           False, str(e), {"execution_time_ms": generation_time, "model": adapter.provider})
                    final_trace = self.debugger.finalize_trace()
                    return {
                        "success": False,
                        "error": f"Model generation failed: {str(e)}",
                        "debug_trace": final_trace,
                        "session_id": session_id
                    }
            
            # Finalize trace
            final_trace = self.debugger.finalize_trace()
            
            # Compile comprehensive result
            result = {
                "success": True,
                "session_id": session_id,
                "ir": ir.to_dict(),
                "security_result": security_result,
                "routing_decision": {
                    "selected_model": routing_decision.selected_model.name,
                    "provider": routing_decision.selected_model.provider,
                    "confidence": routing_decision.confidence_score,
                    "reasoning": routing_decision.reasoning,
                    "estimated_cost": routing_decision.estimated_cost
                },
                "prompts": {
                    "original": content,
                    "sanitized": security_result.sanitized_content,
                    "compiled": compiled_prompt,
                    "optimized": optimized_prompt
                },
                "optimization_metrics": optimization_metrics,
                "response": response,
                "debug_trace": final_trace,
                "performance_metrics": {
                    "ir_generation_ms": ir_time,
                    "security_processing_ms": security_time,
                    "routing_ms": routing_time,
                    "compilation_ms": compilation_time,
                    "optimization_ms": optimization_time,
                    "total_pipeline_ms": final_trace.total_execution_time_ms
                }
            }
            
            return result
            
        except Exception as e:
            # Add error stage and finalize
            self.debugger.add_stage("pipeline_error", content, str(e), False, str(e))
            final_trace = self.debugger.finalize_trace()
            
            return {
                "success": False,
                "error": f"Pipeline error: {str(e)}",
                "debug_trace": final_trace,
                "session_id": session_id
            }

    # Backward compatibility methods
    def set_debug_mode(self, enabled: bool):
        """Enable/disable debug mode."""
        self.debug_enabled = enabled
        self.debugger.enabled = enabled

    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics."""
        stats = {
            "total_sessions": len(self.debugger.trace_history),
            "successful_sessions": len([t for t in self.debugger.trace_history if len(t.errors) == 0]),
            "failed_sessions": len([t for t in self.debugger.trace_history if len(t.errors) > 0]),
            "avg_execution_time": 0.0,
            "routing_statistics": self.model_router.get_routing_statistics(),
            "debugger_metrics": self.debugger.metrics_collector.get_metrics()
        }
        
        if self.debugger.trace_history:
            stats["avg_execution_time"] = sum(t.total_execution_time_ms for t in self.debugger.trace_history) / len(self.debugger.trace_history)
        
        return stats

    def get_debug_trace(self, session_id: str = None) -> Optional[Dict[str, Any]]:
        """Get debug trace for session."""
        if session_id:
            # Find trace by session ID
            for trace in self.debugger.trace_history:
                if trace.session_id == session_id:
                    return self.debugger.get_detailed_trace(trace)
            return None
        else:
            # Get most recent trace
            if self.debugger.trace_history:
                return self.debugger.get_detailed_trace(self.debugger.trace_history[-1])
            return None

    def print_debug_trace(self, session_id: str = None, format_type: str = "readable") -> str:
        """Print debug trace in specified format."""
        if session_id:
            # Find trace by session ID
            for trace in self.debugger.trace_history:
                if trace.session_id == session_id:
                    return self.debugger.print_debug_trace(trace, format_type)
            return "Session not found"
        else:
            # Get most recent trace
            if self.debugger.trace_history:
                return self.debugger.print_debug_trace(self.debugger.trace_history[-1], format_type)
            return "No traces available"

    def update_configuration(self, 
                            security_level: SecurityLevel = None,
                            routing_strategy: RoutingStrategy = None,
                            debug_enabled: bool = None,
                            optimization_targets: List[str] = None):
        """Update pipeline configuration."""
        if security_level:
            self.security_level = security_level
            self.security_layer.update_security_level(security_level)
        
        if routing_strategy:
            self.routing_strategy = routing_strategy
            self.model_router.default_strategy = routing_strategy
        
        if debug_enabled is not None:
            self.debug_enabled = debug_enabled
            self.debugger.enabled = debug_enabled
        
        if optimization_targets:
            self.optimization_targets = optimization_targets