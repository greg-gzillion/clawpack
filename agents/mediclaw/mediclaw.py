"""MedicLaw - Professional Medical Research System"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import get_config
from core.llm.client import MedicalLLMClient

class MedicLaw:
    def __init__(self):
        self.config = get_config()
        self.llm = MedicalLLMClient(self.config)
    
    def research(self, query: str) -> str:
        """Conduct medical research"""
        result = self.llm.generate(query)
        return result.text
    
    def diagnose(self, symptoms: str) -> str:
        """Clinical diagnosis support"""
        prompt = f"""Provide differential diagnosis for: {symptoms}
        
        Format:
        PRIMARY: (most likely)
        SECONDARY: (less likely)
        RULE OUT: (must exclude)
        RED FLAGS: (emergency signs)
        TESTS: (recommended diagnostics)"""
        
        return self.llm.generate(prompt).text
    
    def treatment(self, condition: str) -> str:
        """Treatment recommendations"""
        prompt = f"""Treatment guidelines for: {condition}
        
        Include:
        - First-line therapy with evidence level
        - Alternative options
        - Medication dosing
        - Monitoring parameters
        - Follow-up schedule"""
        
        return self.llm.generate(prompt).text

def main():
    medic = MedicLaw()
    
    print("\n" + "="*70)
    print("🩺 MEDICLAW - Professional Medical Research System")
    print("="*70)
    
    # Try to show available providers
    try:
        available = medic.llm.client.get_available_providers()
        print(f"🔌 LLM Providers: {available}")
    except:
        print("🔌 LLM: Hybrid (API + Ollama)")
    
    print(f"📚 Config loaded")
    print("\nCommands:")
    print("  /research <query>     - Conduct medical research")
    print("  /diagnose <symptoms>  - Differential diagnosis")
    print("  /treatment <condition>- Treatment guidelines")
    print("  /config               - Show current configuration")
    print("  /quit                 - Exit")
    print("="*70)
    
    while True:
        try:
            cmd = input("\n🔬 mediclaw> ").strip()
            if not cmd:
                continue
            
            if cmd == "/quit":
                print("Goodbye!")
                break
            elif cmd == "/config":
                print(medic.config.to_dict())
            elif cmd.startswith("/research"):
                args = cmd.replace("/research", "").strip()
                if args:
                    print("\n🔬 Researching...")
                    result = medic.research(args)
                    print(f"\n{result}")
                else:
                    print("Usage: /research <query>")
            elif cmd.startswith("/diagnose"):
                args = cmd.replace("/diagnose", "").strip()
                if args:
                    print("\n🩺 Diagnosing...")
                    result = medic.diagnose(args)
                    print(f"\n{result}")
                else:
                    print("Usage: /diagnose <symptoms>")
            elif cmd.startswith("/treatment"):
                args = cmd.replace("/treatment", "").strip()
                if args:
                    print("\n💊 Finding treatments...")
                    result = medic.treatment(args)
                    print(f"\n{result}")
                else:
                    print("Usage: /treatment <condition>")
            else:
                print(f"Unknown: {cmd}. Type /research, /diagnose, or /treatment")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
