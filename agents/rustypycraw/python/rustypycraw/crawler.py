"""
RustyPyCraw - Hybrid code crawler with Rust speed and Python AI
"""

import os
import json
from typing import List, Dict, Any
from datetime import datetime
from .shared_memory import SharedMemory

# Try to import Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Try Rust core
try:
    from rustypycrawcore import Crawler as RustCrawler
    RUST_AVAILABLE = True
except ImportError:
    print("⚠️ Rust core not built. Run: cd rustypycraw-core && maturin develop")
    RUST_AVAILABLE = False

class RustyPyCraw:
    """Hybrid code crawler with Rust speed and Python AI"""
    
    def __init__(self, root_path: str, use_ollama: bool = False):
        self.root_path = os.path.expanduser(root_path)
        self.rust = RustCrawler(self.root_path) if RUST_AVAILABLE else None
        self.use_ollama = use_ollama
        self.ollama_url = "http://localhost:11434/api/generate"
        
        # Initialize AI
        self.ai = None
        if not use_ollama and GROQ_AVAILABLE:
            self.ai = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            self.ai_type = "Groq"
        elif use_ollama:
            self.ai_type = "Ollama"
        else:
            self.ai_type = None
        
        self._session_history = []
        
        # Initialize shared memory and register agent
        self.shared_memory = SharedMemory()
        self.shared_memory.register_agent(
            agent_id="rustypycraw",
            name="RustyPyCraw",
            repo="https://github.com/greg-gzillion/rustypycraw",
            capabilities="hybrid code crawler, multi-model AI, Rust+Python, parallel search, pinch mode"
        )
    
    def search(self, pattern: str, file_types: List[str] = None) -> List[str]:
        """Fast parallel search for files containing pattern"""
        if self.rust:
            results = self.rust.fast_search(pattern)
            if file_types:
                filtered = []
                for r in results:
                    for ft in file_types:
                        if r.endswith(ft):
                            filtered.append(r)
                            break
                return filtered
            return results
        return []
    
    def ask(self, question: str) -> str:
        """Ask AI with context from shared memory"""
        # Search shared memories first
        memories = self.shared_memory.recall(question)
        if memories:
            context = "\n".join([f"[{m[0]}] {m[1]}: {m[2][:200]}" for m in memories[:3]])
            enhanced_question = f"Context from other agents:\n{context}\n\n{question}"
        else:
            enhanced_question = question
        
        if not self.ai:
            return "ERROR: No AI backend available. Set GROQ_API_KEY or use_ollama=True"
        
        try:
            if self.ai_type == "Groq":
                completion = self.ai.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": enhanced_question}],
                    max_tokens=500
                )
                answer = completion.choices[0].message.content
            else:
                import requests
                response = requests.post(
                    self.ollama_url,
                    json={"model": "codellama:7b", "prompt": enhanced_question, "stream": False},
                    timeout=120
                )
                answer = response.json()["response"] if response.status_code == 200 else "Error"
            
            # Log conversation
            self.shared_memory.log_conversation("rustypycraw", question, answer)
            
            return answer
        except Exception as e:
            return f"Error: {e}"
    
    def stats(self) -> Dict:
        """Get codebase statistics"""
        if not self.rust:
            return {"error": "Rust core not available"}
        
        by_lang = self.rust.count_by_language()
        total_lines = self.rust.total_lines()
        
        languages = {}
        for k, v in by_lang.items():
            languages[k] = v
        
        return {
            'root_path': self.root_path,
            'total_lines': total_lines,
            'languages': languages,
            'rust_available': RUST_AVAILABLE,
            'ai_type': self.ai_type,
            'ai_available': self.ai is not None or self.use_ollama
        }
    
    def summary(self) -> str:
        """Generate a summary"""
        stats = self.stats()
        return f"""
RustyPyCraw Summary
===================
Path: {stats.get('root_path', 'Unknown')}
Total lines: {stats.get('total_lines', 0):,}
AI backend: {stats.get('ai_type', 'None')}
Rust core: {'✅' if stats.get('rust_available') else '❌'}
"""
    
    def search_rust_only(self, pattern: str) -> List[str]:
        """Search only Rust files"""
        return self.search(pattern, ['.rs'])
    
    def grep(self, pattern: str, context: int = 2) -> List[Dict]:
        """Search with context lines"""
        if self.rust:
            results = self.rust.search_with_context(pattern, context)
            return [{
                'file': r.file,
                'line': r.line,
                'content': r.content,
                'before': r.context_before,
                'after': r.context_after
            } for r in results]
        return []
    
    def pinch(self) -> List[Dict]:
        """Find unnecessary .clone() calls"""
        if self.rust:
            bugs = self.rust.pinch_clones()
            return [{
                'file': b.file,
                'line': b.line,
                'column': b.column,
                'message': b.message,
                'severity': b.severity,
                'suggestion': b.suggestion
            } for b in bugs]
        return []
