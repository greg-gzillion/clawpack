"""MedicLaw Professional Configuration"""

from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class LLMConfig:
    """LLM configuration"""
    router_type: str = "priority"
    task_type: str = "medical_research"
    max_tokens: int = 4000
    temperature: float = 0.3
    timeout: int = 60

@dataclass
class ClinicalConfig:
    """Clinical decision support settings"""
    evidence_levels: List[str] = field(default_factory=lambda: [
        "meta_analysis", "rct", "cohort", "case_control", "case_series", "expert_opinion"
    ])
    guideline_sources: List[str] = field(default_factory=lambda: [
        "nih", "who", "fda", "ema", "nice", "acc", "aha", "asco", "idsa"
    ])
    include_off_label: bool = True
    include_alternative: bool = True
    include_investigational: bool = False

@dataclass
class ResearchConfig:
    """Research interface settings"""
    citation_format: str = "ama"
    include_doi: bool = True
    include_pmid: bool = True
    max_references: int = 20
    require_evidence_grade: bool = True
    show_statistical_data: bool = True
    show_population_data: bool = True

@dataclass
class ExportConfig:
    """Export configuration"""
    formats: List[str] = field(default_factory=lambda: ["json", "csv", "html", "pdf", "markdown"])
    include_timestamp: bool = True
    include_session_data: bool = True
    output_dir: Path = Path.home() / ".mediclaw" / "exports"

class MedicLawConfig:
    """Main configuration aggregator"""
    
    def __init__(self):
        self.llm = LLMConfig()
        self.clinical = ClinicalConfig()
        self.research = ResearchConfig()
        self.export = ExportConfig()
        
        # Correct paths
        # Current file: clawpack/agents/mediclaw/config/settings.py
        # Target: clawpack_v2/
        self.base_dir = Path(__file__).parent.parent.parent.parent
        self.clawpack_v2 = self.base_dir / "clawpack_v2"
        self.webclaw_refs = self.clawpack_v2 / "agents" / "webclaw" / "references" / "mediclaw"
        self.pharma_refs = self.clawpack_v2 / "agents" / "webclaw" / "references" / "pharmacology"
        
        # Create export directory
        self.export.output_dir.mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> Dict:
        return {
            "llm": self.llm.__dict__,
            "clinical": self.clinical.__dict__,
            "research": self.research.__dict__,
            "export": self.export.__dict__,
            "paths": {
                "webclaw_refs": str(self.webclaw_refs),
                "pharma_refs": str(self.pharma_refs)
            }
        }

_config = None

def get_config() -> MedicLawConfig:
    global _config
    if _config is None:
        _config = MedicLawConfig()
    return _config
