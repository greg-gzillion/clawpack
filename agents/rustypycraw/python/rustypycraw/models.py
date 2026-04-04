"""
Multi-Model Provider for RustyPyCraw
Supports: Groq API, Ollama (multiple models)
"""

import os
import requests
import json
from typing import Optional, Dict, Any, List

class ModelProvider:
    """Unified interface for multiple LLM providers"""
    
    def __init__(self):
        self.providers = {}
        self._check_groq()
        self._check_ollama()
    
    def _check_groq(self):
        """Check if Groq API is available"""
        try:
            from groq import Groq
            api_key = os.environ.get("GROQ_API_KEY")
            if api_key:
                self.providers['groq'] = {
                    'type': 'cloud',
                    'speed': 'fast (1-2s)',
                    'cost': 'free',
                    'models': ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant'],
                    'client': Groq(api_key=api_key)
                }
                print("✅ Groq API available")
        except ImportError:
            pass
    
    def _check_ollama(self):
        """Check available Ollama models"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                self.providers['ollama'] = {
                    'type': 'local',
                    'speed': 'slow (30-120s)',
                    'cost': 'free',
                    'models': [m['name'] for m in models],
                    'model_details': {m['name']: m for m in models}
                }
                print(f"✅ Ollama available with {len(models)} models")
        except:
            pass
    
    def list_models(self) -> Dict:
        """List all available models"""
        all_models = {}
        for provider_name, provider in self.providers.items():
            for model in provider['models']:
                all_models[f"{provider_name}/{model}"] = {
                    'provider': provider_name,
                    'model': model,
                    'speed': provider['speed'],
                    'cost': provider['cost'],
                    'type': provider['type']
                }
        return all_models
    
    def ask(self, question: str, provider: str = None, model: str = None, context: str = "") -> str:
        """Ask a question using specified provider/model"""
        full_prompt = f"Context:\n{context}\n\nQuestion: {question}" if context else question
        
        # Auto-select best provider
        if not provider:
            if "code" in question.lower() or "rust" in question.lower():
                provider = "ollama"
                model = model or "codellama:7b"
            else:
                provider = "groq"
        
        if provider == "groq" and provider in self.providers:
            return self._ask_groq(full_prompt, model)
        elif provider == "ollama" and provider in self.providers:
            return self._ask_ollama(full_prompt, model)
        else:
            return f"Provider {provider} not available. Available: {list(self.providers.keys())}"
    
    def _ask_groq(self, prompt: str, model: str = None) -> str:
        """Query Groq API"""
        try:
            groq = self.providers['groq']['client']
            model = model or "llama-3.3-70b-versatile"
            response = groq.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq Error: {e}"
    
    def _ask_ollama(self, prompt: str, model: str = None) -> str:
        """Query local Ollama"""
        try:
            model = model or "codellama:7b"
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=120
            )
            if response.status_code == 200:
                return response.json()["response"]
            return f"Ollama Error: HTTP {response.status_code}"
        except Exception as e:
            return f"Ollama Error: {e}"
    
    def compare(self, question: str) -> Dict:
        """Compare responses from different models"""
        results = {}
        if 'groq' in self.providers:
            results['groq/llama-3.3-70b'] = self._ask_groq(question)
        if 'ollama' in self.providers:
            for model in self.providers['ollama']['models'][:2]:
                results[f'ollama/{model}'] = self._ask_ollama(question, model)
        return results

# Test the provider
if __name__ == "__main__":
    print("=" * 50)
    print("Model Provider Test")
    print("=" * 50)
    provider = ModelProvider()
    print("\nAvailable models:")
    for name, info in provider.list_models().items():
        print(f"  • {name} ({info['speed']})")

    def assemble_prompt(self, question: str, context: str = "", mode: str = "standard") -> str:
        """Assemble layered prompt like Claude Code system prompts"""
        layers = []
        
        # Layer 1: Identity (always)
        layers.append("You are RustyPyCraw, a hybrid code crawler for CosmWasm/PhoenixPME")
        
        # Layer 2: Security boundaries (always)
        layers.append("NEVER suggest modifying code without user approval")
        
        # Layer 3: Mode-specific instructions
        if mode == "code_review":
            layers.append("Focus: security vulnerabilities, gas optimization, CosmWasm patterns")
        elif mode == "debug":
            layers.append("Focus: error handling, unwrap() usage, clone() optimization")
        elif mode == "explain":
            layers.append("Focus: clarity, examples, references to VISION.md")
        elif mode == "audit":
            layers.append("Focus: access control, economic attacks, oracle manipulation")
        elif mode == "optimize":
            layers.append("Focus: gas usage, storage patterns, unnecessary allocations")
        
        # Layer 4: Context (dynamic)
        if context:
            layers.append(f"Context:\n{context}")
        
        # Layer 5: Question
        layers.append(f"Question: {question}")
        
        return "\n\n".join(layers)

    def ask_with_mode(self, question: str, mode: str = "auto", context: str = "") -> str:
        """Ask with specialized agent mode (auto-detects if mode='auto')"""
        
        # Auto-detect mode from question
        if mode == "auto":
            q_lower = question.lower()
            if any(w in q_lower for w in ['fix', 'bug', 'error', 'issue']):
                mode = "debug"
            elif any(w in q_lower for w in ['review', 'security', 'audit', 'vulnerab']):
                mode = "audit"
            elif any(w in q_lower for w in ['explain', 'what is', 'how does', 'describe']):
                mode = "explain"
            elif any(w in q_lower for w in ['optimize', 'gas', 'clone', 'performance']):
                mode = "optimize"
            elif any(w in q_lower for w in ['review', 'check']):
                mode = "code_review"
            else:
                mode = "standard"
        
        # Build the layered prompt
        prompt = self.assemble_prompt(question, context, mode)
        
        # Use the selected provider
        if 'groq' in self.providers:
            return self._ask_groq(prompt)
        elif 'ollama' in self.providers:
            return self._ask_ollama(prompt)
        else:
            return "No AI provider available"
# Add system prompt assembler

    def assemble_system_prompt(self, mode: str = "standard") -> str:
        """Assemble dynamic system prompt like Pattern 01"""
        layers = []
        layers.append("You are RustyPyCraw, a hybrid code crawler for CosmWasm/PhoenixPME")
        layers.append("")
        layers.append("## Security Boundaries")
        layers.append("- NEVER modify code without explicit user approval")
        layers.append("- Read operations are always safe")
        layers.append("- Report security vulnerabilities immediately")
        layers.append("")
        layers.append("## Mode Instructions")
        if mode == "code_review":
            layers.append("Focus: security vulnerabilities, gas optimization, CosmWasm patterns")
        elif mode == "audit":
            layers.append("Focus: access control, economic attacks, oracle manipulation")
        elif mode == "explain":
            layers.append("Focus: clarity, examples, references to VISION.md")
        else:
            layers.append("Focus: balanced, helpful responses")
        layers.append("")
        layers.append("## CosmWasm Specific")
        layers.append("- Entry points: instantiate, execute, query, migrate")
        layers.append("- Storage: Item, Map, Bucket, SnapshotMap")
        layers.append("- Reply pattern for submessage handling")
        return "\\n".join(layers)
