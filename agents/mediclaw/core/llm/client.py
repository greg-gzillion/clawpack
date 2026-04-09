"""Professional LLM Client for Medical Research"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

# Correct path to clawpack_v2
# Current: clawpack/agents/mediclaw/core/llm/client.py
# Target: clawpack_v2/shared/llm/
CLAWPACK_V2 = Path(__file__).parent.parent.parent.parent.parent / "clawpack_v2"
sys.path.insert(0, str(CLAWPACK_V2))

from shared.llm import get_llm as get_hybrid_llm

@dataclass
class MedicalLLMResponse:
    text: str
    provider: str
    response_time: float
    tokens: Optional[int] = None
    confidence: Optional[float] = None
    evidence_links: List[str] = field(default_factory=list)

class MedicalLLMClient:
    def __init__(self, config):
        self.config = config
        self.client = get_hybrid_llm(router_type=config.llm.router_type)
    
    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> MedicalLLMResponse:
        if system_prompt is None:
            system_prompt = """You are a medical research assistant. Provide accurate, evidence-based information.
            Cite sources when possible. Distinguish between established fact and emerging research."""
        
        result = self.client.generate(prompt, task=self.config.llm.task_type, system=system_prompt)
        
        return MedicalLLMResponse(
            text=result.text,
            provider=result.provider_name,
            response_time=result.response_time,
            confidence=self._estimate_confidence(result.text)
        )
    
    def _estimate_confidence(self, text: str) -> float:
        confidence = 0.5
        if any(word in text.lower() for word in ["meta-analysis", "rct", "guideline"]):
            confidence += 0.3
        if any(word in text.lower() for word in ["suggests", "may", "might"]):
            confidence -= 0.2
        return min(max(confidence, 0.1), 0.95)
