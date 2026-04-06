import os
# mediclaw_shared.py - Mediclaw with Shared Learning
import requests
import sqlite3
from pathlib import Path
from datetime import datetime

CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY")

class MediclawShared:
    def __init__(self):
        # Shared memory (for cross-agent learning)
        self.shared_path = Path.home() / ".claw_memory" / "shared_memory.db"
        
        # Private cache (for speed)
        self.cache_path = Path.home() / ".claw_memory" / "medical_cache.db"
        
        self.init_databases()
        
        # Emergency keywords
        self.emergency_keywords = {
            "cardiac": ["chest pain", "heart attack", "cardiac arrest"],
            "stroke": ["stroke", "facial droop", "arm weakness", "slurred speech"],
            "respiratory": ["choking", "difficulty breathing", "anaphylaxis"]
        }
    
    def init_databases(self):
        # Initialize shared memory (for cross-agent learning)
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Create medical_knowledge table in shared memory if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT UNIQUE,
                response TEXT,
                specialty TEXT,
                timestamp TEXT,
                                source_agent TEXT
            )
        """)
        
        # Also ensure tx_knowledge exists (for blockchain medical info)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tx_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                content TEXT,
                source TEXT,
                category TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Initialize private cache
        conn = sqlite3.connect(str(self.cache_path))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT UNIQUE,
                response TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def check_shared_memory(self, query):
        """Check if answer exists in shared memory first"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Check medical_knowledge table
        cursor.execute("SELECT response FROM medical_knowledge WHERE query LIKE ?", (f"%{query}%",))
        result = cursor.fetchone()
        
        if result:
            conn.close()
            return f"📚 [LEARNED FROM OTHER AGENTS]\n{result[0]}"
        
        # Check tx_knowledge for blockchain medical info
        cursor.execute("SELECT content FROM tx_knowledge WHERE topic LIKE ?", (f"%{query}%",))
        result = cursor.fetchone()
        
        conn.close()
        if result:
            return f"🔗 [FROM TX BLOCKCHAIN KNOWLEDGE]\n{result[0]}"
        
        return None
    
    def save_to_shared_memory(self, query, response, specialty):
        """Share knowledge with other agents"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO medical_knowledge (query, response, specialty, timestamp, source_agent)
            VALUES (?, ?, ?, ?, ?)
        """, (query, response, specialty, datetime.now().isoformat(), "Mediclaw"))
        conn.commit()
        conn.close()
        print("💡 [Mediclaw shared this knowledge with other agents]")
    
    def query_ai(self, topic, specialty="general"):
        """Query AI and cache results"""
        # First check shared memory
        cached = self.check_shared_memory(topic)
        if cached:
            return cached
        
        # If not found, query AI
        prompt = f"Provide helpful medical information about: {topic} in the context of {specialty}. Include disclaimer."
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                # Save to shared memory for other agents
                self.save_to_shared_memory(topic, result, specialty)
                return result
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def emergency_check(self, symptoms):
        symptoms_lower = symptoms.lower()
        for category, keywords in self.emergency_keywords.items():
            for keyword in keywords:
                if keyword in symptoms_lower:
                    return True, keyword, category
        return False, None, None

def main():
    m = MediclawShared()
    
    print("\n" + "="*70)
    print("🦞 MEDICLAW SHARED - Cross-Learning Medical Agent")
    print("="*70)
    print("\n⚠️ DISCLAIMER: For medical education only.")
    print("💡 This agent shares knowledge with other Clawpack agents!")
    print("="*70)
    
    print("\n📚 COMMANDS:")
    print("  /ask [question]       - Medical question (reads from shared memory)")
    print("  /emergency [symptoms] - Emergency checker")
    print("  /quit                 - Exit")
    
    while True:
        cmd = input("\n🏥 Mediclaw> ").strip()
        
        if not cmd:
            continue
        if cmd == '/quit':
            break
        
        if cmd.startswith('/ask '):
            question = cmd[5:]
            print(f"\n🔍 Checking shared memory for: {question}\n")
            result = m.query_ai(question)
            print(result)
            print()
        
        elif cmd.startswith('/emergency '):
            symptoms = cmd[11:]
            is_emerg, keyword, category = m.emergency_check(symptoms)
            if is_emerg:
                print(f"\n⚠️ URGENT: '{keyword}' - Call emergency services NOW!")
            else:
                print("\n✅ No emergency signs detected.")
            print()
        
        else:
            print("Unknown command. Use /ask or /emergency")

if __name__ == "__main__":
    main()