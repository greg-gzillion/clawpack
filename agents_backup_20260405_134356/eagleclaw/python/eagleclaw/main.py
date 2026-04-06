"""EagleClaw - AI-powered coding assistant (extended from rustypycraw)"""

import os
import sys
from .security import PermissionClassifier, PermissionLevel
from .memory import MemoryLoader
from .agents import SUBAGENTS
from .session import PersistentSession
from .harness import Harness

class EagleClaw:
    def __init__(self, root_path: str = "."):
        self.root_path = os.path.expanduser(root_path)
        self.security = PermissionClassifier()
        self.memory = MemoryLoader(root_path)
        self.session = PersistentSession()
        self.harness = Harness()
        self.subagents = SUBAGENTS
    
    def ask(self, question: str) -> str:
        """Ask AI with full context and security"""
        # Load context from memory
        context = self.memory.load_all_context(question)
        
        # Check if question is dangerous
        level, reason = self.security.classify(question)
        if level == PermissionLevel.BLOCK:
            return f"⚠️ Blocked: {reason}"
        
        # Use appropriate subagent
        if "security" in question.lower() or "audit" in question.lower():
            agent = self.subagents.get('auditor')
            return f"[Auditor] Analyzing: {question}"
        elif "optimize" in question.lower() or "gas" in question.lower():
            agent = self.subagents.get('optimizer')
            return f"[Optimizer] Optimizing: {question}"
        else:
            return f"[EagleClaw] Processing: {question}\nContext: {context[:200]}..."
    
    def stats(self) -> dict:
        """Return system statistics"""
        return {
            "name": "EagleClaw",
            "version": "0.1.0",
            "subagents": list(self.subagents.keys()),
            "permission_mode": "read-only",
            "memory_loaded": True
        }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="EagleClaw AI Assistant")
    parser.add_argument("--ask", "-a", help="Ask a question")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    args = parser.parse_args()
    
    eagle = EagleClaw()
    
    if args.ask:
        print(eagle.ask(args.ask))
    elif args.stats:
        print(eagle.stats())
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
