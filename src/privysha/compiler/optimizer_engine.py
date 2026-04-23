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

import re
from typing import Dict, List, Any, Tuple, Optional
from ..ir.prompt_ir import PromptIR, IntentType, EntityType, ConstraintType, PrivacyLevel


class PromptOptimizer:
    """
    Prompt Optimizer Engine - Optimizes prompts for token efficiency, 
    performance, and cost while maintaining functionality.
    
    This implements compiler-style optimizations including:
    - Token reduction
    - Semantic compression
    - Structural optimization
    - Cost-aware transformations
    """

    def __init__(self):
        """Initialize optimizer with strategies and rules."""
        self.optimization_strategies = self._init_strategies()
        self.compression_patterns = self._init_compression_patterns()
        self.cost_models = self._init_cost_models()
        self.performance_weights = self._init_performance_weights()

    def _init_strategies(self) -> Dict[str, Any]:
        """Initialize optimization strategies."""
        return {
            "token_reduction": {
                "remove_fillers": True,
                "compress_phrases": True,
                "use_abbreviations": True,
                "remove_redundancy": True,
                "simplify_structure": True
            },
            "semantic_preservation": {
                "maintain_intent": True,
                "preserve_constraints": True,
                "keep_context": True,
                "entity_integrity": True
            },
            "cost_optimization": {
                "prefer_cheaper_models": True,
                "reduce_context": True,
                "batch_operations": True
            },
            "performance_optimization": {
                "parallelizable_tasks": True,
                "cache_friendly": True,
                "fast_paths": True
            }
        }

    def _init_compression_patterns(self) -> Dict[str, str]:
        """Initialize text compression patterns."""
        return {
            # Conversational fillers
            r'\bplease\b': '',
            r'\bkindly\b': '',
            r'\bcould you\b': '',
            r'\bwould you\b': '',
            r'\bcan you\b': '',
            r'\bi need you to\b': '',
            r'\bi want you to\b': '',
            
            # Redundant phrases
            r'\bas much as possible\b': 'maximize',
            r'\bas quickly as possible\b': 'quickly',
            r'\bin a timely manner\b': 'quickly',
            r'\bthe best possible\b': 'optimal',
            r'\bmake sure that\b': 'ensure',
            r'\btake into account\b': 'consider',
            r'\bkeep in mind\b': 'remember',
            
            # Wordy phrases
            r'\bdue to the fact that\b': 'because',
            r'\bin order to\b': 'to',
            r'\bwith regard to\b': 'about',
            r'\bin the event that\b': 'if',
            r'\bon the basis of\b': 'based on',
            r'\bat the present time\b': 'now',
            r'\bfor the purpose of\b': 'to',
            
            # Technical abbreviations
            r'\bapplication programming interface\b': 'API',
            r'\buser interface\b': 'UI',
            r'\buser experience\b': 'UX',
            r'\bartificial intelligence\b': 'AI',
            r'\bmachine learning\b': 'ML',
            r'\bnatural language processing\b': 'NLP',
            r'\blarge language model\b': 'LLM',
            
            # Common contractions
            r'\bdo not\b': "don't",
            r'\bdoes not\b': "doesn't",
            r'\bdid not\b': "didn't",
            r'\bwill not\b': "won't",
            r'\bcannot\b': "can't",
            r'\bshall not\b': "shan't",
            r'\bshould not\b': "shouldn't",
            r'\bwould not\b': "wouldn't",
            r'\bcould not\b': "couldn't",
            r'\bmust not\b': "mustn't",
            r'\bhave not\b': "haven't",
            r'\bhas not\b': "hasn't",
            r'\bhad not\b': "hadn't",
            r'\bare not\b': "aren't",
            r'\bis not\b': "isn't",
            r'\bwas not\b': "wasn't",
            r'\bwere not\b': "weren't"
        }

    def _init_cost_models(self) -> Dict[str, Dict[str, float]]:
        """Initialize cost models for different providers."""
        return {
            "openai": {
                "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},  # per 1K tokens
                "gpt-4o": {"input": 0.005, "output": 0.015},
                "gpt-4-turbo": {"input": 0.01, "output": 0.03},
                "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
            },
            "anthropic": {
                "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
                "claude-3-sonnet": {"input": 0.003, "output": 0.015},
                "claude-3-opus": {"input": 0.015, "output": 0.075}
            },
            "grok": {
                "grok-beta": {"input": 0.0005, "output": 0.0015}
            }
        }

    def _init_performance_weights(self) -> Dict[str, float]:
        """Initialize performance optimization weights."""
        return {
            "token_efficiency": 0.4,
            "cost_reduction": 0.3,
            "speed_optimization": 0.2,
            "quality_preservation": 0.1
        }

    def optimize(self, prompt: str, ir: PromptIR, optimization_targets: List[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Optimize prompt based on IR and targets.
        
        Args:
            prompt: Original prompt
            ir: Prompt IR for context
            optimization_targets: List of optimization targets
            
        Returns:
            Tuple of (optimized_prompt, optimization_metrics)
        """
        if optimization_targets is None:
            optimization_targets = ir.optimization_targets or ["tokens", "accuracy"]
        
        # Start with original prompt
        optimized = prompt
        metrics = {
            "original_tokens": self._estimate_tokens(prompt),
            "optimizations_applied": [],
            "token_savings": 0,
            "cost_savings": 0.0,
            "quality_score": 1.0
        }
        
        # Apply optimization strategies based on targets
        if "tokens" in optimization_targets or "cost" in optimization_targets:
            optimized, token_metrics = self._optimize_for_tokens(optimized, ir)
            metrics.update(token_metrics)
        
        if "speed" in optimization_targets:
            optimized, speed_metrics = self._optimize_for_speed(optimized, ir)
            metrics.update(speed_metrics)
        
        if "accuracy" in optimization_targets:
            optimized, accuracy_metrics = self._optimize_for_accuracy(optimized, ir)
            metrics.update(accuracy_metrics)
        
        # Calculate final metrics
        metrics["optimized_tokens"] = self._estimate_tokens(optimized)
        metrics["token_reduction"] = metrics["original_tokens"] - metrics["optimized_tokens"]
        metrics["token_reduction_percentage"] = (metrics["token_reduction"] / metrics["original_tokens"] * 100) if metrics["original_tokens"] > 0 else 0
        
        return optimized, metrics

    def _optimize_for_tokens(self, prompt: str, ir: PromptIR) -> Tuple[str, Dict[str, Any]]:
        """Optimize prompt for token efficiency."""
        optimized = prompt
        optimizations_applied = []
        
        # Apply compression patterns
        for pattern, replacement in self.compression_patterns.items():
            if re.search(pattern, optimized, re.IGNORECASE):
                optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
                optimizations_applied.append(f"pattern_compression: {pattern}")
        
        # Remove redundant whitespace
        if re.search(r'\s+', optimized):
            optimized = re.sub(r'\s+', ' ', optimized)
            optimizations_applied.append("whitespace_normalization")
        
        # Remove conversational fillers
        filler_patterns = [
            r'\bhey\b', r'\bhi\b', r'\bhello\b', r'\bthanks\b', r'\bthank you\b',
            r'\bsorry\b', r'\bexcuse me\b', r'\bpardon\b'
        ]
        
        for filler in filler_patterns:
            if re.search(filler, optimized, re.IGNORECASE):
                optimized = re.sub(filler, '', optimized, flags=re.IGNORECASE)
                optimizations_applied.append(f"filler_removal: {filler}")
        
        # Compose multiple instructions into compact format
        if "• " in optimized:
            optimized = self._compress_bullets(optimized)
            optimizations_applied.append("bullet_compression")
        
        # Use functional notation for simple tasks
        optimized = self._apply_functional_notation(optimized, ir)
        if optimized != prompt:
            optimizations_applied.append("functional_notation")
        
        # Remove redundant adjectives and adverbs
        optimized = self._remove_redundant_modifiers(optimized)
        optimizations_applied.append("modifier_optimization")
        
        return optimized.strip(), {
            "optimizations_applied": optimizations_applied,
            "token_savings": self._estimate_tokens(prompt) - self._estimate_tokens(optimized)
        }

    def _optimize_for_speed(self, prompt: str, ir: PromptIR) -> Tuple[str, Dict[str, Any]]:
        """Optimize prompt for faster processing."""
        optimized = prompt
        optimizations_applied = []
        
        # Simplify complex instructions
        if len(prompt.split()) > 100:
            optimized = self._simplify_instructions(optimized)
            optimizations_applied.append("instruction_simplification")
        
        # Use direct commands instead of polite requests
        polite_patterns = [
            (r'\bplease\b', ''),
            (r'\bkindly\b', ''),
            (r'\bcould you\b', ''),
            (r'\bwould you\b', '')
        ]
        
        for pattern, replacement in polite_patterns:
            if re.search(pattern, optimized, re.IGNORECASE):
                optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
                optimizations_applied.append("politeness_removal")
        
        # Prioritize essential constraints
        if len(ir.constraints) > 3:
            essential_constraints = [ConstraintType.ACCURACY, ConstraintType.SECURITY, ConstraintType.PRIVACY]
            optimized = self._prioritize_constraints(optimized, essential_constraints)
            optimizations_applied.append("constraint_prioritization")
        
        return optimized.strip(), {
            "optimizations_applied": optimizations_applied,
            "speed_improvement": "estimated_20_30_percent"
        }

    def _optimize_for_accuracy(self, prompt: str, ir: PromptIR) -> Tuple[str, Dict[str, Any]]:
        """Optimize prompt for accuracy and quality."""
        optimized = prompt
        optimizations_applied = []
        
        # Add specificity to vague instructions
        vague_terms = {
            r'\bgood\b': 'high-quality',
            r'\bbetter\b': 'improved',
            r'\bbest\b': 'optimal',
            r'\bproper\b': 'appropriate',
            r'\bcorrect\b': 'accurate'
        }
        
        for vague, specific in vague_terms.items():
            if re.search(vague, optimized, re.IGNORECASE):
                optimized = re.sub(vague, specific, optimized, flags=re.IGNORECASE)
                optimizations_applied.append(f"specificity_enhancement: {vague}->{specific}")
        
        # Add quality constraints if missing
        if ConstraintType.ACCURACY not in ir.constraints and ir.intent in [IntentType.ANALYZE, IntentType.VALIDATE]:
            optimized += "\nEnsure high accuracy and precision in results."
            optimizations_applied.append("accuracy_constraint_added")
        
        # Add validation steps for critical tasks
        if ir.intent in [IntentType.VALIDATE, IntentType.DEBUG]:
            optimized += "\nProvide step-by-step reasoning and validation."
            optimizations_applied.append("validation_steps_added")
        
        return optimized.strip(), {
            "optimizations_applied": optimizations_applied,
            "quality_score": 1.1  # Estimated quality improvement
        }

    def _compress_bullets(self, text: str) -> str:
        """Compress bullet points into compact format."""
        bullets = re.findall(r'•\s*([^\n]+)', text)
        if len(bullets) > 2:
            # Convert to comma-separated list
            compressed = ", ".join(bullet.strip() for bullet in bullets)
            # Replace the entire bullet section
            text = re.sub(r'•\s*[^\n]+(\n•\s*[^\n]+)*', compressed, text, flags=re.MULTILINE)
        return text

    def _apply_functional_notation(self, text: str, ir: PromptIR) -> str:
        """Apply functional notation for simple tasks."""
        # Simple task patterns
        functional_mappings = {
            r'analyze\s+(\w+)\s+for\s+(\w+)': r'analyze(\1).for(\2)',
            r'generate\s+(\w+)\s+with\s+(\w+)': r'generate(\1).with(\2)',
            r'summarize\s+(\w+)\s+in\s+(\w+)\s+words': r'summarize(\1).length(\2)',
            r'extract\s+(\w+)\s+from\s+(\w+)': r'extract(\1).from(\2)',
            r'classify\s+(\w+)\s+as\s+(\w+)': r'classify(\1).as(\2)'
        }
        
        for pattern, replacement in functional_mappings.items():
            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text

    def _remove_redundant_modifiers(self, text: str) -> str:
        """Remove redundant adjectives and adverbs."""
        redundant_modifiers = [
            r'\bvery\b',
            r'\breally\b',
            r'\bquite\b',
            r'\bextremely\b',
            r'\bhighly\b',
            r'\bcompletely\b',
            r'\btotally\b',
            r'\babsolutely\b',
            r'\bsimply\b',
            r'\bbasically\b'
        ]
        
        for modifier in redundant_modifiers:
            text = re.sub(modifier, '', text, flags=re.IGNORECASE)
        
        return text

    def _simplify_instructions(self, text: str) -> str:
        """Simplify complex instructions."""
        # Break down long sentences
        sentences = re.split(r'[.!?]+', text)
        simplified_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence.split()) > 20:
                # Split long sentence
                if ',' in sentence:
                    parts = sentence.split(',', 1)
                    simplified_sentences.extend([parts[0].strip(), parts[1].strip()])
                else:
                    simplified_sentences.append(sentence)
            else:
                simplified_sentences.append(sentence)
        
        return '. '.join(filter(None, simplified_sentences))

    def _prioritize_constraints(self, text: str, essential_constraints: List[ConstraintType]) -> str:
        """Prioritize essential constraints in prompt."""
        # This is a simplified implementation
        # In practice, would parse and restructure the constraint section
        constraint_keywords = {
            ConstraintType.ACCURACY: ['accurate', 'precise', 'correct'],
            ConstraintType.SECURITY: ['secure', 'safe', 'protected'],
            ConstraintType.PRIVACY: ['private', 'confidential', 'masked']
        }
        
        essential_text_parts = []
        for constraint in essential_constraints:
            keywords = constraint_keywords.get(constraint, [])
            for keyword in keywords:
                if keyword in text.lower():
                    essential_text_parts.append(keyword)
        
        if essential_text_parts:
            # Add prioritized constraints at the beginning
            priority_text = f"Priority: {', '.join(essential_text_parts)}. "
            text = priority_text + text
        
        return text

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation)."""
        return int(len(text.split()) * 1.3)

    def calculate_cost_savings(self, original_tokens: int, optimized_tokens: int, 
                              provider: str, model: str) -> float:
        """Calculate cost savings from optimization."""
        if provider not in self.cost_models or model not in self.cost_models[provider]:
            return 0.0
        
        cost_per_1k = self.cost_models[provider][model]["input"]
        original_cost = (original_tokens / 1000) * cost_per_1k
        optimized_cost = (optimized_tokens / 1000) * cost_per_1k
        
        return original_cost - optimized_cost

    def get_optimization_recommendations(self, ir: PromptIR) -> List[str]:
        """Get optimization recommendations based on IR."""
        recommendations = []
        
        # Token optimization recommendations
        if ir.token_estimate and ir.token_estimate > 500:
            recommendations.append("Consider token optimization - prompt is quite long")
        
        # Cost optimization recommendations
        if ir.is_cost_sensitive():
            recommendations.append("Enable cost optimization strategies")
            if ir.intent in [IntentType.GENERATE, IntentType.CREATE]:
                recommendations.append("Consider using smaller model for generation tasks")
        
        # Speed optimization recommendations
        if ir.is_time_sensitive():
            recommendations.append("Enable speed optimization")
            recommendations.append("Prioritize essential constraints only")
        
        # Privacy recommendations
        if ir.requires_privacy_masking():
            recommendations.append("Ensure privacy masking is applied")
            recommendations.append("Consider using privacy-focused models")
        
        # Complexity-based recommendations
        complexity = ir.get_complexity_level()
        if complexity == "high":
            recommendations.append("Break down complex task into simpler sub-tasks")
            recommendations.append("Consider using comprehensive optimization")
        elif complexity == "low":
            recommendations.append("Minimal optimization should be sufficient")
        
        return recommendations

    def benchmark_optimization(self, prompt: str, ir: PromptIR) -> Dict[str, Any]:
        """Benchmark optimization performance."""
        results = {}
        
        # Test different optimization strategies
        strategies = ["tokens", "speed", "accuracy", "cost"]
        
        for strategy in strategies:
            optimized, metrics = self.optimize(prompt, ir, [strategy])
            results[strategy] = {
                "optimized_prompt": optimized,
                "metrics": metrics,
                "token_reduction": metrics["token_reduction_percentage"],
                "quality_impact": metrics.get("quality_score", 1.0)
            }
        
        # Find best overall strategy
        best_strategy = max(strategies, key=lambda s: results[s]["token_reduction"])
        results["best_strategy"] = best_strategy
        results["recommendations"] = self.get_optimization_recommendations(ir)
        
        return results
