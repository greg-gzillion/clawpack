"""
Security and permission classification for RustyPyCraw
Based on agentic-ai-prompt-research Patterns 11-13
"""

import re
from typing import Dict, Tuple
from enum import Enum

class PermissionLevel(Enum):
    AUTO_APPROVE = "auto_approve"
    REQUIRE_APPROVAL = "require_approval"
    BLOCK = "block"

class PermissionClassifier:
    """Multi-stage security classifier for tool execution"""

    SAFE_PATTERNS = [
        r"^read\s+",
        r"^search\s+",
        r"^grep\s+",
        r"^stats$",
        r"^list-models$",
        r"^ask\s+",
    ]

    DANGEROUS_PATTERNS = [
        r"rm\s+-rf",
        r"sudo\s+",
        r"chmod\s+777",
        r">\s*/dev/",
        r"format\s+",
        r"dd\s+if=",
    ]

    WRITE_PATTERNS = [
        r"write\s+",
        r"edit\s+",
        r"delete\s+",
        r"mv\s+",
        r"cp\s+",
    ]

    @classmethod
    def classify(cls, command: str) -> Tuple[PermissionLevel, str]:
        """Classify a command and return permission level with reason"""
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return (PermissionLevel.BLOCK, f"Dangerous pattern detected: {pattern}")
        for pattern in cls.WRITE_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return (PermissionLevel.REQUIRE_APPROVAL, f"Write operation detected: {pattern}")
        for pattern in cls.SAFE_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return (PermissionLevel.AUTO_APPROVE, "Safe operation")
        return (PermissionLevel.REQUIRE_APPROVAL, "Unknown operation type")

    @classmethod
    def explain_risk(cls, command: str, level: PermissionLevel) -> str:
        """Generate human-readable risk explanation"""
        explanations = {
            PermissionLevel.AUTO_APPROVE: f"✅ SAFE: '{command}' - No risk detected",
            PermissionLevel.REQUIRE_APPROVAL: f"⚠️  CAUTION: '{command}' - May modify system state",
            PermissionLevel.BLOCK: f"❌ BLOCKED: '{command}' - Potentially dangerous operation"
        }
        return explanations.get(level, f"Unknown: {command}")

    # C++ specific dangerous patterns
    CPP_DANGEROUS = [
        r'delete\s+\*',
        r'free\(',
        r'malloc\(',
        r'new\s+\w+',
        r'#define\s+',
    ]
    
    @classmethod
    def classify_cpp(cls, code_line: str) -> Tuple[PermissionLevel, str]:
        """Classify C++ code for memory safety issues"""
        for pattern in cls.CPP_DANGEROUS:
            if re.search(pattern, code_line):
                return (PermissionLevel.REQUIRE_APPROVAL, f"Memory operation: {pattern}")
        return (PermissionLevel.AUTO_APPROVE, "Safe C++ operation")
