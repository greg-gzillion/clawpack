"""MedicLaw V2 - Modular Medical AI Agent (Upgraded from V1)"""

import sys
from pathlib import Path

# Add V2 shared LLM
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "clawpack_v2" / "shared"))

# Import V1 modules for compatibility
from mediclaw_shared import *
from pharmaclaw import *

# Import V2 components
from core.engine import MedicalEngineV2
from cli.interface import CLI

class MedicLawV2:
    def __init__(self):
        self.engine = MedicalEngineV2()
        self.v1_shared = mediclaw_shared  # Your existing module
        self.pharmaclaw = pharmaclaw      # Your existing module
        self.cli = CLI(self)
    
    def run(self):
        print("\n" + "="*70)
        print("🩺 MEDICLAW V2 - Modular Medical AI Agent")
        print("   (Upgraded with Hybrid LLM + WebClaw References)")
        print("="*70)
        self.cli.start()
    
    # V2 methods using new LLM
    def diagnose_v2(self, symptoms: str, specialty: str = None):
        return self.engine.diagnose(symptoms, specialty)
    
    def treatment_v2(self, condition: str):
        return self.engine.get_treatment(condition)
    
    # Keep your V1 methods available
    def homeopathy(self, remedy: str):
        return self.v1_shared.get_homeopathy_info(remedy) if hasattr(self.v1_shared, 'get_homeopathy_info') else "Homeopathy info from V1"
    
    def integrative(self, condition: str):
        return self.engine.integrative_approach(condition)

if __name__ == "__main__":
    agent = MedicLawV2()
    agent.run()
