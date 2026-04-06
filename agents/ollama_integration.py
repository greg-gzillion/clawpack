# ollama_integration.py - Complete Ollama integration for Clawpack
import requests
import json
from typing import Optional, Dict, List

class OllamaManager:
    """Manager for Ollama local LLM with 10 models"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.models = self.list_models()
    
    def list_models(self) -> List[str]:
        """Get all available Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = [model['name'] for model in response.json()['models']]
                return models
        except Exception as e:
            print(f"Error listing models: {e}")
        return []
    
    def generate(self, prompt: str, model: str = "llama3.2:3b", 
                 system: Optional[str] = None, temperature: float = 0.7) -> str:
        """Generate text using specified Ollama model"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "temperature": temperature
        }
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            if response.status_code == 200:
                return response.json()['response']
        except Exception as e:
            print(f"Error generating: {e}")
        return ""
    
    def chat(self, messages: List[Dict], model: str = "llama3.2:3b") -> str:
        """Chat with Ollama model"""
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        try:
            response = requests.post(f"{self.base_url}/api/chat", json=payload)
            if response.status_code == 200:
                return response.json()['message']['content']
        except Exception as e:
            print(f"Error in chat: {e}")
        return ""
    
    def get_model_info(self, model: str) -> Dict:
        """Get detailed info about a model"""
        try:
            response = requests.post(f"{self.base_url}/api/show", json={"model": model})
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {}
    
    def recommend_model(self, task: str) -> str:
        """Recommend best model for specific task"""
        recommendations = {
            "code": ["qwen3-coder:30b", "deepseek-coder:6.7b", "codellama:7b"],
            "vision": ["qwen3-vl:30b"],
            "general": ["gemma3:27b", "gemma3:12b", "llama3.2:3b"],
            "reasoning": ["deepseek-r1:8b", "gemma3:27b"],
            "fast": ["gemma3:4b", "gemma3:1b", "llama3.2:3b"],
            "medical": ["gemma3:27b", "llama3.2:3b"],
            "legal": ["gemma3:27b", "deepseek-r1:8b"]
        }
        
        for key, models in recommendations.items():
            if key in task.lower():
                return models[0]
        return "llama3.2:3b"  # Default

# Model capabilities mapping
MODEL_CAPABILITIES = {
    "qwen3-vl:30b": {
        "size": "19GB",
        "best_for": ["vision", "multimodal", "general"],
        "speed": "slow",
        "quality": "excellent"
    },
    "qwen3-coder:30b": {
        "size": "18GB",
        "best_for": ["code", "programming", "debugging"],
        "speed": "slow",
        "quality": "excellent"
    },
    "gemma3:27b": {
        "size": "17GB",
        "best_for": ["general", "reasoning", "medical", "legal"],
        "speed": "slow",
        "quality": "excellent"
    },
    "gemma3:12b": {
        "size": "8.1GB",
        "best_for": ["general", "balanced"],
        "speed": "medium",
        "quality": "very good"
    },
    "deepseek-r1:8b": {
        "size": "5.2GB",
        "best_for": ["reasoning", "math", "logic"],
        "speed": "medium",
        "quality": "very good"
    },
    "gemma3:4b": {
        "size": "3.3GB",
        "best_for": ["fast", "general"],
        "speed": "fast",
        "quality": "good"
    },
    "codellama:7b": {
        "size": "3.8GB",
        "best_for": ["code", "programming"],
        "speed": "fast",
        "quality": "good"
    },
    "deepseek-coder:6.7b": {
        "size": "3.8GB",
        "best_for": ["code", "programming", "debugging"],
        "speed": "fast",
        "quality": "good"
    },
    "llama3.2:3b": {
        "size": "2.0GB",
        "best_for": ["general", "fast", "lightweight"],
        "speed": "very fast",
        "quality": "good"
    },
    "gemma3:1b": {
        "size": "815MB",
        "best_for": ["ultra-fast", "embedded"],
        "speed": "lightning",
        "quality": "fair"
    }
}

if __name__ == "__main__":
    ollama = OllamaManager()
    print(f"🦙 Connected to Ollama with {len(ollama.models)} models:")
    for model in ollama.models:
        print(f"  • {model}")
