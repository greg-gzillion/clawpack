"""
AgentForLaw - Model Connectivity Layer
Utilizes all available LLM models while staying specialized in law
"""

import os
import json
import requests
from typing import Dict, List, Optional

class ModelRegistry:
    """Registry of all available LLM models on your system"""
    
    @staticmethod
    def discover_models() -> Dict:
        """Discover all available models from all providers"""
        models = {
            "groq": [],
            "deepseek": [],
            "local": []
        }
        
        # 1. Groq (cloud, fastest)
        groq_key = os.environ.get("GROQ_API_KEY")
        if groq_key:
            models["groq"] = [
                {"name": "llama-3.3-70b-versatile", "speed": "fast", "best_for": "legal reasoning"},
                {"name": "llama-3.1-8b-instant", "speed": "fastest", "best_for": "quick definitions"},
                {"name": "mixtral-8x7b-32768", "speed": "fast", "best_for": "long context"}
            ]
        
        # 2. Ollama (local, private)
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                for m in response.json().get("models", []):
                        "name": m["name"],
                        "speed": "slow" if "70b" in m["name"] else "medium",
                        "best_for": "privacy" if "codellama" in m["name"] else "general"
                    })
        except:
            pass
        
        # 3. DeepSeek (cloud, cheap)
        deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        if deepseek_key:
            models["deepseek"] = [
                {"name": "deepseek-chat", "speed": "fast", "best_for": "legal analysis"},
                {"name": "deepseek-coder", "speed": "fast", "best_for": "contract drafting"}
            ]
        
        # 4. Local models (custom endpoints)
        for port in [8000, 8080, 5000]:
            try:
                response = requests.get(f"http://localhost:{port}/v1/models", timeout=1)
                if response.status_code == 200:
                    models["local"].append({
                        "name": f"localhost:{port}",
                        "speed": "varies",
                        "best_for": "custom"
                    })
            except:
                pass
        
        return models
    
    @staticmethod
    def get_best_model(task: str) -> Dict:
        """Recommend best model for a specific legal task"""
        models = ModelRegistry.discover_models()
        
        recommendations = {
            "contract_drafting": ["deepseek/deepseek-coder", "groq/llama-3.1-8b-instant"],
            "long_document": ["groq/mixtral-8x7b-32768", "deepseek/deepseek-chat"]
        }
        
        recommended = recommendations.get(task, recommendations["legal_analysis"])
        return {"task": task, "recommended_models": recommended}

class LegalAnalyzer:
    """Specialized legal analysis using any available model"""
    
    @staticmethod
    def analyze(question: str, model: str = None, provider: str = None) -> str:
        """
        Analyze legal question using best available model
        
        Args:
            question: Legal question to analyze
            model: Specific model name (e.g., "llama-3.3-70b-versatile")
        """
        
        # Auto-select best model if not specified
        if not model and not provider:
            # Try Groq first (fastest)
            if os.environ.get("GROQ_API_KEY"):
                provider = "groq"
                model = "llama-3.3-70b-versatile"
            # Then Ollama (local)
                model = "codellama:7b"
            # Then DeepSeek
            elif os.environ.get("DEEPSEEK_API_KEY"):
                provider = "deepseek"
                model = "deepseek-chat"
            else:
                return "No AI models available. Set GROQ_API_KEY, DEEPSEEK_API_KEY, or install Ollama."
        
        # Route to appropriate provider
        if provider == "groq":
            return LegalAnalyzer._groq_analyze(question, model)
        elif provider == "deepseek":
            return LegalAnalyzer._deepseek_analyze(question, model)
        else:
            return f"Unknown provider: {provider}"
    
    @staticmethod
    def _groq_analyze(question: str, model: str) -> str:
        """Use Groq for fast legal analysis"""
        try:
            from groq import Groq
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are AgentForLaw, an expert in US law. Provide accurate, concise legal analysis based on statutes, regulations, and case law."},
                    {"role": "user", "content": question}
                ],
                max_tokens=800,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq error: {e}"
    
    @staticmethod
        """Use Ollama for private, local legal analysis"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": f"You are AgentForLaw, a legal expert. Answer: {question}",
                    "stream": False,
                    "options": {"num_predict": 800, "temperature": 0.3}
                },
                timeout=90
            )
            if response.status_code == 200:
                return response.json().get("response", "No response")
            return f"Ollama error: HTTP {response.status_code}"
        except Exception as e:
            return f"Ollama error: {e}"
    
    @staticmethod
    def _deepseek_analyze(question: str, model: str) -> str:
        """Use DeepSeek for cost-effective legal analysis"""
        try:
            headers = {
                "Authorization": f"Bearer {os.environ.get('DEEPSEEK_API_KEY')}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are AgentForLaw, a legal expert."},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 800,
                "temperature": 0.3
            }
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return f"DeepSeek error: {response.status_code}"
        except Exception as e:
            return f"DeepSeek error: {e}"
    
    @staticmethod
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

class ContractAnalyzer:
    """Specialized contract analysis using LLMs"""
    
    @staticmethod
    def analyze_contract(contract_text: str, model: str = None) -> Dict:
        """Analyze a contract for risks, missing clauses, and improvements"""
        
        prompt = f"""
        Analyze this contract and identify:
        1. Missing standard clauses
        2. Potential risks
        3. Ambiguous language
        4. Suggestions for improvement
        
        Contract:
        {contract_text[:2000]}
        """
        
        analysis = LegalAnalyzer.analyze(prompt, model)
        
        return {
            "contract_length": len(contract_text),
            "analysis": analysis,
            "risk_level": "medium" if "risk" in analysis.lower() else "low"
        }

class CaseLawAnalyzer:
    """Analyze case law using LLMs"""
    
    @staticmethod
    def summarize_case(case_name: str, case_text: str = None, model: str = None) -> str:
        """Summarize a legal case"""
        
        if case_text:
            prompt = f"Summarize this case including facts, issue, holding, and reasoning:\n\n{case_text[:2000]}"
        else:
            prompt = f"Summarize the key holdings of {case_name} and explain its legal significance."
        
        return LegalAnalyzer.analyze(prompt, model)

# Add to main CLI
def add_model_commands(parser):
    """Add model-related commands to argument parser"""
    parser.add_argument("--list-models", action="store_true", help="List all available LLM models")
    parser.add_argument("--analyze", help="Analyze legal question using best available model")
    parser.add_argument("--model", help="Specify model (e.g., 'groq/llama-3.3-70b-versatile')")
    parser.add_argument("--recommend", help="Get model recommendation for a task (legal_analysis, contract_drafting, etc.)")

# Integration function
def handle_model_commands(args):
    """Handle model-related commands"""
    
    if args.list_models:
        models = ModelRegistry.discover_models()
        print("\n🤖 AVAILABLE LLM MODELS")
        print("=" * 50)
        
        for provider, provider_models in models.items():
            if provider_models:
                print(f"\n📡 {provider.upper()}:")
                for m in provider_models:
                    print(f"   • {m['name']} ({m['speed']}) - {m['best_for']}")
        
        if not any(models.values()):
            print("\n❌ No models found. Options:")
            print("   1. Set GROQ_API_KEY environment variable")
            print("   3. Set DEEPSEEK_API_KEY environment variable")
        return True
    
    elif args.recommend:
        result = ModelRegistry.get_best_model(args.recommend)
        print(f"\n🎯 RECOMMENDATION FOR: {result['task']}")
        print("=" * 40)
        for model in result['recommended_models']:
            print(f"   • {model}")
        return True
    
    elif args.analyze:
        print(f"\n🤖 AgentForLaw analyzing: {args.analyze[:100]}...")
        print(f"   Using provider: {args.provider}")
        if args.model:
            print(f"   Model: {args.model}")
        print("\n" + "=" * 50)
        
        result = LegalAnalyzer.analyze(args.analyze, args.model, args.provider)
        print(f"\n📜 ANALYSIS:\n{result}\n")
        return True
    
    return False

# Example usage
if __name__ == "__main__":
    # Test model discovery
    print("Discovering models...")
    models = ModelRegistry.discover_models()
    print(json.dumps(models, indent=2))
    
    # Test recommendation
    print("\n" + "="*50)
    rec = ModelRegistry.get_best_model("legal_analysis")
    print(json.dumps(rec, indent=2))
