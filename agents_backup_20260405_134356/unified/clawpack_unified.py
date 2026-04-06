# clawpack_unified.py - Full Featured Unified Controller
import requests
import sqlite3
import os
from pathlib import Path

# ===== CONFIGURATION - EDIT THESE =====
# YOUR WORKING API KEY (copy this exactly)
CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY")
CLOUD_MODEL = "deepseek/deepseek-chat"
LOCAL_OLLAMA_URL = "http://127.0.0.1:11434"
# ======================================

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

class ClawpackUnified:
    def __init__(self):
        self.working_mode = "auto"
        
    def db_query(self, question):
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT topic, content, source FROM tx_knowledge WHERE topic LIKE ? OR content LIKE ? LIMIT 3", 
                      (f"%{question}%", f"%{question}%"))
        results = cursor.fetchall()
        conn.close()
        if results:
            answer = "📚 ACCURATE (from TX knowledge base):\n\n"
            for topic, content, source in results:
                answer += f"📖 {topic}:\n{content}\n🔗 {source}\n\n"
            return answer
        return None
    
    def local_query(self, question, model="gemma3:4b"):
        try:
            response = requests.post(f"{LOCAL_OLLAMA_URL}/api/generate",
                json={"model": model, "prompt": question, "stream": False, "temperature": 0.7}, timeout=120)
            if response.status_code == 200:
                return f"🖥️ LOCAL ({model}):\n{response.json()['response']}"
            return f"Local error: {response.status_code}"
        except Exception as e:
            return f"Local error: {str(e)}"
    
    def cloud_query(self, question):
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": CLOUD_MODEL, "messages": [{"role": "user", "content": question}]}, timeout=60)
            if response.status_code == 200:
                return f"☁️ CLOUD ({CLOUD_MODEL}):\n{response.json()['choices'][0]['message']['content']}"
            return f"Cloud error: {response.status_code} - {response.text[:200]}"
        except Exception as e:
            return f"Cloud error: {str(e)}"
    
    def smart_route(self, question):
        question_lower = question.lower()
        db_keywords = ["tx blockchain", "smart token", "rwa", "tokenization", "xrpl bridge", "ibc", "wasm", "compliance", "clawback", "asset types", "issuer features", "tx_platform"]
        coding_keywords = ["code", "python", "function", "script", "write", "implement", "class", "def", "import"]
        
        for keyword in db_keywords:
            if keyword in question_lower:
                db_answer = self.db_query(question)
                if db_answer:
                    return db_answer + "\n💡 Tip: This answer is from your local TX knowledge base (100% accurate)."
        
        for keyword in coding_keywords:
            if keyword in question_lower:
                return self.local_query(question, "deepseek-coder:6.7b")
        
        return self.cloud_query(question)
    
    def compare_modes(self, question):
        print("\n" + "="*70)
        print(f"🔍 COMPARING ANSWERS FOR: {question}")
        print("="*70)
        
        db_answer = self.db_query(question)
        if db_answer:
            print("\n📚 DATABASE (100% accurate):")
            print("-"*50)
            print(db_answer)
        else:
            print("\n📚 DATABASE: No exact match found")
        
        print("\n🖥️ LOCAL MODEL (gemma3:4b - fast):")
        print("-"*50)
        print(self.local_query(question, "gemma3:4b"))
        
        print("\n☁️ CLOUD MODEL (DeepSeek - powerful):")
        print("-"*50)
        print(self.cloud_query(question))
        
        print("\n" + "="*70)
        print("💡 RECOMMENDATION:")
        if db_answer:
            print("   Use DATABASE for factual TX questions (100% accurate)")
        print("   Use LOCAL for quick answers and coding")
        print("   Use CLOUD for complex reasoning and analysis")
        print("="*70)

def main():
    claw = ClawpackUnified()
    
    print("\n" + "="*70)
    print("🦞 CLAWPACK UNIFIED - Best of Both Worlds")
    print("="*70)
    print("\nMODES:")
    print("  auto    - Smart routing (recommended)")
    print("  local   - Force local model (fast, private)")
    print("  cloud   - Force cloud model (powerful)")
    print("  db      - Database only (100% accurate)")
    print("  compare - Compare all sources")
    print("  help    - Show this menu")
    print("  quit    - Exit")
    print("\n" + "="*70)
    
    while True:
        mode = input("\n🔧 Mode [auto/local/cloud/db/compare/help/quit]: ").strip().lower()
        
        if mode == 'quit':
            break
        elif mode == 'help':
            print("\nauto - Smart routing (DB for facts, local for coding, cloud for complex)")
            print("local - Use local gemma models (fast, private, no API key)")
            print("cloud - Use DeepSeek cloud (powerful, needs internet)")
            print("db - Query local TX knowledge base only")
            print("compare - See answer from all sources side-by-side")
            continue
        elif mode == 'compare':
            question = input("❓ Question: ").strip()
            if question:
                claw.compare_modes(question)
            continue
        elif mode not in ['auto', 'local', 'cloud', 'db']:
            print("Invalid mode. Use: auto, local, cloud, db, compare, help, quit")
            continue
        
        while True:
            question = input(f"\n❓ [{mode.upper()}] Your question (or 'back' to change mode): ").strip()
            
            if question.lower() == 'back':
                break
            if question.lower() == 'quit':
                return
            if not question:
                continue
            
            print("\n🤔 Processing...\n")
            
            if mode == 'auto':
                answer = claw.smart_route(question)
            elif mode == 'local':
                answer = claw.local_query(question)
            elif mode == 'cloud':
                answer = claw.cloud_query(question)
            elif mode == 'db':
                answer = claw.db_query(question)
                if not answer:
                    answer = "No exact match found in TX knowledge base. Try 'auto' mode for AI assistance."
            else:
                answer = "Invalid mode"
            
            print(answer)
            print("\n" + "-"*50)

if __name__ == "__main__":
    main()