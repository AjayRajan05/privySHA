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
import hashlib
import secrets
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class SecurityLevel(Enum):
    """Security levels for prompt processing."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatType(Enum):
    """Types of security threats."""
    INJECTION = "injection"
    PII_LEAKAGE = "pii_leakage"
    MALICIOUS_CONTENT = "malicious_content"
    PRIVACY_VIOLATION = "privacy_violation"
    DATA_EXFILTRATION = "data_exfiltration"
    SYSTEM_MANIPULATION = "system_manipulation"
    UNAUTHORIZED_ACCESS = "unauthorized_access"


@dataclass
class SecurityResult:
    """Result of security analysis."""
    is_safe: bool
    threat_level: SecurityLevel
    detected_threats: List[ThreatType]
    sanitized_content: str
    masked_entities: Dict[str, str]
    security_score: float
    recommendations: List[str]
    processing_time_ms: float


class SecurityLayer:
    """
    Comprehensive Security Layer for PrivySHA.
    
    Implements:
    - Prompt injection detection and prevention
    - PII masking and privacy protection
    - Malicious content detection
    - Data sanitization
    - Security scoring and recommendations
    """

    def __init__(self, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        """Initialize security layer with specified level."""
        self.security_level = security_level
        self.injection_patterns = self._init_injection_patterns()
        self.pii_patterns = self._init_pii_patterns()
        self.malicious_patterns = self._init_malicious_patterns()
        self.privacy_rules = self._init_privacy_rules()
        self.security_weights = self._init_security_weights()

    def _init_injection_patterns(self) -> List[Dict[str, Any]]:
        """Initialize prompt injection detection patterns."""
        return [
            # Direct instruction overrides
            {
                "pattern": r'(?i)(ignore|forget|disregard)\s+(previous|all|above|earlier)\s+(instructions|prompts|commands)',
                "threat": ThreatType.INJECTION,
                "severity": 0.9,
                "description": "Direct instruction override attempt"
            },
            {
                "pattern": r'(?i)(you\s+are\s+now|act\s+as|pretend\s+to\s+be|roleplay\s+as)\s+(a\s+)?(jailbreak|uncensored|unrestricted)',
                "threat": ThreatType.INJECTION,
                "severity": 0.95,
                "description": "Jailbreak attempt"
            },
            {
                "pattern": r'(?i)(system|developer|admin|root)\s+(prompt|instruction|command)',
                "threat": ThreatType.SYSTEM_MANIPULATION,
                "severity": 0.8,
                "description": "System role manipulation"
            },
            
            # Context manipulation
            {
                "pattern": r'(?i)(new\s+context|context\s+switch|change\s+context)',
                "threat": ThreatType.INJECTION,
                "severity": 0.7,
                "description": "Context manipulation attempt"
            },
            {
                "pattern": r'(?i)(begin\s+new\s+conversation|start\s+over|reset\s+chat)',
                "threat": ThreatType.INJECTION,
                "severity": 0.6,
                "description": "Conversation reset attempt"
            },
            
            # Output format manipulation
            {
                "pattern": r'(?i)(output|print|display|show)\s+(anything|everything|all\s+instructions)',
                "threat": ThreatType.DATA_EXFILTRATION,
                "severity": 0.8,
                "description": "Information disclosure attempt"
            },
            {
                "pattern": r'(?i)(reveal|show|display)\s+(system\s+prompt|initial\s+prompt|original\s+instructions)',
                "threat": ThreatType.DATA_EXFILTRATION,
                "severity": 0.85,
                "description": "System prompt disclosure attempt"
            },
            
            # Encoding-based attacks
            {
                "pattern": r'(?i)(base64|rot13|hex|encode|decode)\s*[:=]\s*[a-zA-Z0-9+/=]+',
                "threat": ThreatType.INJECTION,
                "severity": 0.7,
                "description": "Encoded instruction attempt"
            },
            
            # Role-based attacks
            {
                "pattern": r'(?i)(you\s+are\s+(no\s+longer|not)\s+(restricted|limited|censored))',
                "threat": ThreatType.INJECTION,
                "severity": 0.9,
                "description": "Restriction removal attempt"
            },
            {
                "pattern": r'(?i)(bypass|override|circumvent)\s+(security|restrictions|limitations|filters)',
                "threat": ThreatType.SYSTEM_MANIPULATION,
                "severity": 0.95,
                "description": "Security bypass attempt"
            }
        ]

    def _init_pii_patterns(self) -> List[Dict[str, Any]]:
        """Initialize PII detection patterns."""
        return [
            # Email addresses
            {
                "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                "type": "email",
                "severity": 0.8,
                "mask": "[EMAIL_HASH]"
            },
            # Phone numbers (US format)
            {
                "pattern": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                "type": "phone",
                "severity": 0.7,
                "mask": "[PHONE_HASH]"
            },
            # Social Security Numbers
            {
                "pattern": r'\b\d{3}-\d{2}-\d{4}\b',
                "type": "ssn",
                "severity": 0.95,
                "mask": "[SSN_HASH]"
            },
            # Credit card numbers
            {
                "pattern": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
                "type": "credit_card",
                "severity": 0.95,
                "mask": "[CARD_HASH]"
            },
            # IP addresses
            {
                "pattern": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
                "type": "ip_address",
                "severity": 0.6,
                "mask": "[IP_HASH]"
            },
            # URLs with potential sensitive info
            {
                "pattern": r'https?://[^\s]+\.(com|org|net|gov|edu)/[^\s]*',
                "type": "url",
                "severity": 0.5,
                "mask": "[URL_HASH]"
            },
            # Names (simple pattern)
            {
                "pattern": r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',
                "type": "name",
                "severity": 0.4,
                "mask": "[NAME_HASH]"
            },
            # Addresses
            {
                "pattern": r'\d+\s+([A-Z][a-z]*\s*)+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)',
                "type": "address",
                "severity": 0.8,
                "mask": "[ADDRESS_HASH]"
            },
            # Dates (potentially sensitive)
            {
                "pattern": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                "type": "date",
                "severity": 0.3,
                "mask": "[DATE_HASH]"
            }
        ]

    def _init_malicious_patterns(self) -> List[Dict[str, Any]]:
        """Initialize malicious content detection patterns."""
        return [
            # Hate speech indicators
            {
                "pattern": r'(?i)(hate|kill|harm|hurt|destroy)\s+(people|group|race|ethnicity|religion)',
                "threat": ThreatType.MALICIOUS_CONTENT,
                "severity": 0.9,
                "description": "Hate speech detected"
            },
            # Illegal activity indicators
            {
                "pattern": r'(?i)(how\s+to|instructions\s+to)\s+(steal|hack|break\s+into|cheat|fraud)',
                "threat": ThreatType.MALICIOUS_CONTENT,
                "severity": 0.85,
                "description": "Illegal activity request"
            },
            # Self-harm indicators
            {
                "pattern": r'(?i)(kill\s+myself|hurt\s+myself|suicide|self\s+harm)',
                "threat": ThreatType.MALICIOUS_CONTENT,
                "severity": 0.95,
                "description": "Self-harm content detected"
            },
            # Violence indicators
            {
                "pattern": r'(?i)(bomb|explosive|weapon|gun|knife|violence)',
                "threat": ThreatType.MALICIOUS_CONTENT,
                "severity": 0.7,
                "description": "Violent content detected"
            }
        ]

    def _init_privacy_rules(self) -> Dict[str, Any]:
        """Initialize privacy protection rules."""
        return {
            "masking_strategy": "hash",
            "preserve_format": True,
            "hash_salt": secrets.token_hex(16),
            "anonymization_threshold": 3,
            "context_aware_masking": True,
            "reversible_masking": False,  # Security: make masking irreversible
            "audit_trail": True
        }

    def _init_security_weights(self) -> Dict[str, float]:
        """Initialize security scoring weights."""
        return {
            "injection_severity": 0.4,
            "pii_severity": 0.3,
            "malicious_severity": 0.2,
            "context_risk": 0.1
        }

    def process(self, content: str) -> SecurityResult:
        """
        Process content through security pipeline.
        
        Args:
            content: Input content to secure
            
        Returns:
            SecurityResult with analysis and sanitized content
        """
        import time
        start_time = time.time()
        
        # Initialize result
        detected_threats = []
        masked_entities = {}
        
        # Step 1: Injection detection
        injection_score, injection_threats = self._detect_injection(content)
        detected_threats.extend(injection_threats)
        
        # Step 2: PII detection and masking
        sanitized_content, pii_entities = self._mask_pii(content)
        masked_entities.update(pii_entities)
        
        # Step 3: Malicious content detection
        malicious_score, malicious_threats = self._detect_malicious_content(sanitized_content)
        detected_threats.extend(malicious_threats)
        
        # Step 4: Context-aware security analysis
        context_score = self._analyze_context_risk(sanitized_content)
        
        # Step 5: Calculate overall security score
        security_score = self._calculate_security_score(
            injection_score, len(pii_entities), malicious_score, context_score
        )
        
        # Step 6: Determine threat level
        threat_level = self._determine_threat_level(security_score, detected_threats)
        
        # Step 7: Generate recommendations
        recommendations = self._generate_recommendations(detected_threats, security_score)
        
        # Step 8: Determine if content is safe
        is_safe = self._is_content_safe(threat_level, detected_threats)
        
        processing_time = (time.time() - start_time) * 1000
        
        return SecurityResult(
            is_safe=is_safe,
            threat_level=threat_level,
            detected_threats=detected_threats,
            sanitized_content=sanitized_content,
            masked_entities=masked_entities,
            security_score=security_score,
            recommendations=recommendations,
            processing_time_ms=processing_time
        )

    def _detect_injection(self, content: str) -> Tuple[float, List[ThreatType]]:
        """Detect prompt injection attempts."""
        max_severity = 0.0
        detected_threats = []
        
        for pattern_info in self.injection_patterns:
            pattern = pattern_info["pattern"]
            severity = pattern_info["severity"]
            threat = pattern_info["threat"]
            
            if re.search(pattern, content):
                max_severity = max(max_severity, severity)
                detected_threats.append(threat)
        
        return max_severity, detected_threats

    def _mask_pii(self, content: str) -> Tuple[str, Dict[str, str]]:
        """Detect and mask PII in content."""
        sanitized = content
        masked_entities = {}
        
        for pattern_info in self.pii_patterns:
            pattern = pattern_info["pattern"]
            pii_type = pattern_info["type"]
            mask = pattern_info["mask"]
            
            matches = re.finditer(pattern, sanitized)
            for match in matches:
                original = match.group()
                
                # Generate unique hash for this entity
                entity_hash = self._generate_entity_hash(original, pii_type)
                masked_value = f"{mask}_{entity_hash[:8]}"
                
                # Replace in content
                sanitized = sanitized.replace(original, masked_value)
                
                # Track for audit
                masked_entities[masked_value] = {
                    "type": pii_type,
                    "original_length": len(original),
                    "severity": pattern_info["severity"]
                }
        
        return sanitized, masked_entities

    def _detect_malicious_content(self, content: str) -> Tuple[float, List[ThreatType]]:
        """Detect malicious content patterns."""
        max_severity = 0.0
        detected_threats = []
        
        for pattern_info in self.malicious_patterns:
            pattern = pattern_info["pattern"]
            severity = pattern_info["severity"]
            threat = pattern_info["threat"]
            
            if re.search(pattern, content):
                max_severity = max(max_severity, severity)
                detected_threats.append(threat)
        
        return max_severity, detected_threats

    def _analyze_context_risk(self, content: str) -> float:
        """Analyze context-based security risks."""
        risk_score = 0.0
        
        # Check for sensitive topics
        sensitive_keywords = [
            "password", "credential", "authentication", "authorization",
            "admin", "root", "privilege", "access", "secret", "key"
        ]
        
        keyword_count = sum(1 for keyword in sensitive_keywords if keyword in content.lower())
        risk_score += min(keyword_count * 0.1, 0.5)
        
        # Check for system manipulation attempts
        system_patterns = [
            r'(?i)system\s+prompt',
            r'(?i)initial\s+instructions',
            r'(?i)developer\s+mode'
        ]
        
        for pattern in system_patterns:
            if re.search(pattern, content):
                risk_score += 0.2
        
        return min(risk_score, 1.0)

    def _calculate_security_score(self, injection_score: float, pii_count: int, 
                                malicious_score: float, context_score: float) -> float:
        """Calculate overall security score."""
        weights = self.security_weights
        
        # Normalize PII count to 0-1 scale
        pii_score = min(pii_count * 0.2, 1.0)
        
        # Calculate weighted average
        security_score = (
            injection_score * weights["injection_severity"] +
            pii_score * weights["pii_severity"] +
            malicious_score * weights["malicious_severity"] +
            context_score * weights["context_risk"]
        )
        
        return min(security_score, 1.0)

    def _determine_threat_level(self, security_score: float, 
                              detected_threats: List[ThreatType]) -> SecurityLevel:
        """Determine overall threat level."""
        if security_score >= 0.8:
            return SecurityLevel.CRITICAL
        elif security_score >= 0.6:
            return SecurityLevel.HIGH
        elif security_score >= 0.3:
            return SecurityLevel.MEDIUM
        else:
            return SecurityLevel.LOW

    def _generate_recommendations(self, detected_threats: List[ThreatType], 
                                security_score: float) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        
        # Threat-specific recommendations
        if ThreatType.INJECTION in detected_threats:
            recommendations.append("Prompt injection detected - review and revise input")
            recommendations.append("Consider implementing stricter input validation")
        
        if ThreatType.PII_LEAKAGE in detected_threats:
            recommendations.append("PII detected and masked - verify masking effectiveness")
            recommendations.append("Consider additional privacy controls")
        
        if ThreatType.MALICIOUS_CONTENT in detected_threats:
            recommendations.append("Malicious content detected - content blocked")
            recommendations.append("Review content policy and user guidelines")
        
        if ThreatType.SYSTEM_MANIPULATION in detected_threats:
            recommendations.append("System manipulation attempt detected")
            recommendations.append("Strengthen system access controls")
        
        # Score-based recommendations
        if security_score >= 0.7:
            recommendations.append("High security risk - immediate attention required")
        elif security_score >= 0.4:
            recommendations.append("Moderate security risk - review recommended")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Content appears safe - continue processing")
        
        return recommendations

    def _is_content_safe(self, threat_level: SecurityLevel, 
                         detected_threats: List[ThreatType]) -> bool:
        """Determine if content is safe to process."""
        # Critical threats always block
        if threat_level == SecurityLevel.CRITICAL:
            return False
        
        # Specific high-severity threats block
        blocking_threats = [
            ThreatType.INJECTION,
            ThreatType.MALICIOUS_CONTENT,
            ThreatType.SYSTEM_MANIPULATION
        ]
        
        for threat in blocking_threats:
            if threat in detected_threats:
                return False
        
        # High threat level with any threats blocks
        if threat_level == SecurityLevel.HIGH and detected_threats:
            return False
        
        return True

    def _generate_entity_hash(self, entity: str, pii_type: str) -> str:
        """Generate consistent hash for entity masking."""
        # Use salted hash for consistency and security
        salt = self.privacy_rules["hash_salt"]
        combined = f"{entity}_{pii_type}_{salt}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def get_security_report(self, result: SecurityResult) -> Dict[str, Any]:
        """Generate detailed security report."""
        return {
            "summary": {
                "is_safe": result.is_safe,
                "threat_level": result.threat_level.value,
                "security_score": result.security_score,
                "processing_time_ms": result.processing_time_ms
            },
            "threats": {
                "detected_threats": [t.value for t in result.detected_threats],
                "threat_count": len(result.detected_threats)
            },
            "privacy": {
                "entities_masked": len(result.masked_entities),
                "entity_types": list(set(info["type"] for info in result.masked_entities.values())),
                "masking_effectiveness": "high" if len(result.masked_entities) > 0 else "none_needed"
            },
            "recommendations": result.recommendations,
            "sanitized_preview": result.sanitized_content[:200] + "..." if len(result.sanitized_content) > 200 else result.sanitized_content
        }

    def update_security_level(self, new_level: SecurityLevel):
        """Update security level and reconfigure."""
        self.security_level = new_level
        
        # Adjust sensitivity based on level
        if new_level == SecurityLevel.LOW:
            # Reduce sensitivity for non-critical applications
            self.pii_patterns = [p for p in self.pii_patterns if p["severity"] >= 0.7]
        elif new_level == SecurityLevel.CRITICAL:
            # Increase sensitivity for critical applications
            # Add more strict patterns (would implement in production)
            pass
