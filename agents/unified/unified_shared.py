# unified_shared.py - Unified Controller with Cross-Learning
import requests
import sqlite3
from pathlib import Path
from datetime import datetime

CLOUD_API_KEY = "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"

class UnifiedShared:
    def __init__(self):
        self.shared_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Ensure all tables exist for cross-learning
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT,
                target_language TEXT,
                translated_text TEXT,
                source_agent TEXT,
                timestamp TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tx_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                content TEXT,
                source TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def smart_query(self, question):
        """Query across all shared knowledge"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Check medical knowledge first
        cursor.execute("SELECT response, source_agent FROM medical_knowledge WHERE query LIKE ?", (f"%{question}%",))
        medical = cursor.fetchone()
        
        if medical:
            conn.close()
            return f"📚 [FROM {medical[1]}]\n{medical[0]}"
        
        # Check TX knowledge
        cursor.execute("SELECT content FROM tx_knowledge WHERE topic LIKE ?", (f"%{question}%",))
        tx = cursor.fetchone()
        
        if tx:
            conn.close()
            return f"🔗 [FROM TX KNOWLEDGE BASE]\n{tx[0]}"
        
        conn.close()
        
        # If nothing found, query AI and save
        return self.query_ai_and_save(question)
    
    def query_ai_and_save(self, question):
        """Query AI and save to shared memory"""
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": question}]},
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                
                # Save to shared memory
                conn = sqlite3.connect(str(self.shared_path))
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO medical_knowledge (query, response, specialty, timestamp, source_agent)
                    VALUES (?, ?, ?, ?, ?)
                """, (question, result, "general", datetime.now().isoformat(), "Unified"))
                conn.commit()
                conn.close()
                
                return f"🤖 [NEW - SAVED TO SHARED MEMORY]\n{result}"
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def chat(self):
        print("\n" + "="*70)
        print("🦞 UNIFIED SHARED - Cross-Learning Controller")
        print("="*70)
        print("\n💡 This agent reads from AND writes to shared memory!")
        print("   Other agents (Mediclaw, Polyclaw) can learn from these answers.")
        print("="*70)
        
        while True:
            question = input("\n❓ Ask me anything: ").strip()
            if not question:
                continue
            if question.lower() == 'quit':
                break
            
            print("\n🤔 Searching shared memory...")
            result = self.smart_query(question)
            print(f"\n{result}\n")
            print("-"*50)

if __name__ == "__main__":
    unified = UnifiedShared()
    unified.chat()