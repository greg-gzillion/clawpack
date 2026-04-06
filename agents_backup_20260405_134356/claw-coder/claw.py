#!/usr/bin/env python3
import os
import subprocess
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def ask(prompt):
    if not client:
        return "Set GROQ_API_KEY for fast responses"
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )
    return completion.choices[0].message.content

def search_project(term):
    cmd = f"grep -rn '{term}' /home/greg/dev/TX --include='*.rs' --include='*.md' 2>/dev/null | head -30"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout if result.stdout else f"No results for: {term}"

print("\n🦞 CLAW - PhoenixPME Assistant")
print("Commands: ask | search | status | token | exit")

while True:
    try:
        cmd = input("\n🦞 ").strip()
        if not cmd:
            continue
        if cmd == "exit":
            break
        elif cmd == "status":
            print("\nFee: 1.1% | Collateral: 10% | Inspection: 48h")
        elif cmd == "token":
            print("\nTESTUSD on Coreum testnet")
        elif cmd.startswith("ask "):
            print(ask(cmd[4:]))
        elif cmd.startswith("search "):
            print(search_project(cmd[7:]))
        else:
            print("Commands: ask <question> | search <term> | status | token | exit")
    except KeyboardInterrupt:
        break

# Extended capabilities from rustypycraw
try:
    from .python.security import PermissionClassifier
    from .python.memory import MemoryLoader
    from .python.agents import SUBAGENTS
    from .python.session import PersistentSession
    from .python.harness import Harness
    EXTENDED_AVAILABLE = True
except ImportError:
    EXTENDED_AVAILABLE = False
    print("Extended capabilities not available")

if EXTENDED_AVAILABLE:
    class ExtendedCrawler:
        def __init__(self, root_path: str):
            self.root_path = root_path
            self.security = PermissionClassifier()
            self.memory = MemoryLoader(root_path)
            self.session = PersistentSession()
            self.harness = Harness()
            self.subagents = SUBAGENTS
        
        def ask_with_security(self, question: str) -> str:
            level, reason = self.security.classify(question)
            if level.name == "BLOCK":
                return f"🔒 Blocked: {reason}"
            context = self.memory.load_all_context(question)
            return f"Context loaded: {len(context)} chars\nQuestion: {question}"
    
    print("✅ Extended capabilities loaded for claw-coder")
