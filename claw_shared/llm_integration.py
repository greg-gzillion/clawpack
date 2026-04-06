# claw_shared/llm_integration.py
# Unified LLM that leverages your claw_shared learning systems

import os
import sys
import requests
from pathlib import Path

# Import your actual classes
from claw_shared.memory import ClawMemory
from claw_shared.cross_learner import CrossAgentLearner
from claw_shared.neural_memory import NeuralMemory

class UnifiedLLM:
    """Unified LLM that leverages claw_shared learning systems"""
    
    def __init__(self):
        self.memory = ClawMemory("UnifiedLLM")
        self.learner = CrossAgentLearner()
        self.neural = NeuralMemory()
        self.ollama_url = "http://localhost:11434/api/generate"
        self.cloud_key = os.environ.get("OPENROUTER_API_KEY")
        self.available_models = []
        self._check_ollama()
    
    def _check_ollama(self):
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                self.available_models = [m["name"] for m in response.json().get("models", [])]
                print(f"? Local Ollama: {len(self.available_models)} models available")
        except:
            print("?? Local Ollama not running")
    
    def generate_with_learning(self, prompt: str, task: str = "general") -> str:
        """Generate using LLM AND learn from the interaction"""
        
        # Check shared memory first
        cached = self._check_memory(prompt, task)
        if cached:
            print("?? [FROM SHARED MEMORY]")
            return cached
        
        # Try local Ollama
        result = self._try_local(prompt, task)
        if result:
            self._store_learning(prompt, result, task)
            return result
        
        # Fallback to cloud
        result = self._try_cloud(prompt)
        if result:
            self._store_learning(prompt, result, task)
            return result
        
        return "? No LLM available. Start Ollama or check API key."
    
    def _check_memory(self, prompt: str, task: str) -> str:
        try:
            # Query memory for similar knowledge
            self.memory.cursor.execute(
                "SELECT value FROM memories WHERE key LIKE ? ORDER BY timestamp DESC LIMIT 1",
                (f'%{prompt[:50]}%',)
            )
            row = self.memory.cursor.fetchone()
            return row[0] if row else None
        except:
            return None
    
    def _store_learning(self, prompt: str, result: str, task: str):
        try:
            # Store in memory
            self.memory.cursor.execute(
                "INSERT INTO memories (agent, key, value, timestamp, tags) VALUES (?, ?, ?, ?, ?)",
                ("UnifiedLLM", prompt[:200], result[:1000], 
                 datetime.now().isoformat(), task)
            )
            self.memory.conn.commit()
            print("?? [Stored in shared memory]")
        except:
            pass
    
    def _try_local(self, prompt: str, task: str) -> str:
        if not self.available_models:
            return ""
        
        # Select best model for task
        if "code" in task.lower():
            model = next((m for m in self.available_models if "coder" in m or "deepseek" in m), self.available_models[0])
        elif "translate" in task.lower():
            model = next((m for m in self.available_models if "llama" in m), self.available_models[0])
        else:
            model = self.available_models[0]
        
        try:
            print(f"??? [Local] Using {model}...")
            response = requests.post(
                self.ollama_url,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=120
            )
            if response.status_code == 200:
                return response.json().get("response", "")
        except Exception as e:
            print(f"Local error: {e}")
        return ""
    
    def _try_cloud(self, prompt: str) -> str:
        if not self.cloud_key:
            return ""
        try:
            print("?? [Cloud] Using OpenRouter...")
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.cloud_key}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Cloud error: {e}")
        return ""

# Global instance
llm = UnifiedLLM()
