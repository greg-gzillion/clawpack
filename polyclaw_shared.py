import os
# polyclaw_shared.py - Polyclaw with Cross-Learning Translation
import requests
import sqlite3
from pathlib import Path
from datetime import datetime

CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

class PolyclawShared:
    def __init__(self):
        self.name = "Polyclaw Shared"
        # Shared memory (for cross-agent learning)
        self.shared_path = Path.home() / ".claw_memory" / "shared_memory.db"
        
        # Translation cache (for speed)
        self.cache_path = Path.home() / ".claw_memory" / "translation_cache.db"
        
        self.init_databases()
        
        # Supported languages
        self.languages = {
            "en": "English", "es": "Spanish", "fr": "French", "de": "German",
            "it": "Italian", "pt": "Portuguese", "ru": "Russian", "zh": "Chinese",
            "ja": "Japanese", "ko": "Korean", "ar": "Arabic", "hi": "Hindi",
            "tr": "Turkish", "nl": "Dutch", "pl": "Polish", "sv": "Swedish",
            "vi": "Vietnamese", "th": "Thai", "id": "Indonesian", "ms": "Malay"
        }
    
    def init_databases(self):
        # Initialize shared memory for translations
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Create translations table in shared memory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT,
                target_language TEXT,
                translated_text TEXT,
                source_language TEXT,
                timestamp TEXT,
                source_agent TEXT,
                usage_count INTEGER DEFAULT 1
            )
        """)
        
        # Create multilingual knowledge table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS multilingual_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                language TEXT,
                content TEXT,
                source_agent TEXT,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Initialize private translation cache
        conn = sqlite3.connect(str(self.cache_path))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS translation_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT UNIQUE,
                target_lang TEXT,
                translated_text TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()
        
        print("âœ… Polyclaw connected to shared learning system!")
    
    def check_shared_translation(self, text, target_lang):
        """Check if another agent has already translated this"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT translated_text, source_agent 
            FROM translations 
            WHERE source_text = ? AND target_language = ?
            ORDER BY usage_count DESC LIMIT 1
        """, (text, target_lang))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"ðŸ’¡ [Found translation from {result[1]}]")
            return result[0]
        return None
    
    def save_translation(self, source, target_lang, translated, source_lang="auto"):
        """Save translation to shared memory for other agents"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO translations 
            (source_text, target_language, translated_text, source_language, timestamp, source_agent, usage_count)
            VALUES (?, ?, ?, ?, ?, ?, 
                COALESCE((SELECT usage_count + 1 FROM translations WHERE source_text = ? AND target_language = ?), 1))
        """, (source, target_lang, translated, source_lang, datetime.now().isoformat(), "Polyclaw", source, target_lang))
        
        conn.commit()
        conn.close()
        print("ðŸ’¡ [Polyclaw shared this translation with other agents]")
    
    def translate(self, text, target_lang, source_lang="auto"):
        """Translate text - checks shared memory first"""
        
        # First check if another agent already translated this
        cached = self.check_shared_translation(text, target_lang)
        if cached:
            return cached
        
        # If not found, call AI
        target_name = self.languages.get(target_lang, target_lang)
        
        prompt = f"""Translate the following text to {target_name}. 
Only output the translation, nothing else.

TEXT: {text}

TRANSLATION:"""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content'].strip()
                # Save to shared memory
                self.save_translation(text, target_lang, result, source_lang)
                return result
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def learn_from_medical(self, medical_term):
        """Learn medical terms from Mediclaw and translate them"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Get medical knowledge from shared memory
        cursor.execute("""
            SELECT query, response FROM medical_knowledge 
            WHERE query LIKE ? 
            LIMIT 5
        """, (f"%{medical_term}%",))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            print(f"\nðŸ“š Learning from Mediclaw about: {medical_term}")
            for query, response in results:
                print(f"  ðŸ“– Found: {query[:50]}...")
                # Auto-translate key terms to multiple languages
                for lang in ["es", "fr", "de", "zh", "ja"]:
                    if len(query) < 100:
                        trans = self.translate(query[:50], lang)
                        print(f"    â†’ {self.languages.get(lang, lang)}: {trans[:60]}...")
            return True
        return False
    
    def get_shared_stats(self):
        """Show what Polyclaw has learned from other agents"""
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        # Count translations in shared memory
        cursor.execute("SELECT COUNT(*) FROM translations")
        trans_count = cursor.fetchone()[0]
        
        # Count by source agent
        cursor.execute("""
            SELECT source_agent, COUNT(*) 
            FROM translations 
            GROUP BY source_agent
        """)
        agents = cursor.fetchall()
        
        conn.close()
        
        print("\nðŸ“Š SHARED LEARNING STATS:")
        print(f"  Total translations in shared memory: {trans_count}")
        for agent, count in agents:
            print(f"    {agent}: {count} translations")
    
    def chat(self):
        print("\n" + "="*70)
        print("ðŸ¦ž POLYCLAW SHARED - Cross-Learning Translation Agent")
        print("="*70)
        print("\nâš ï¸ This agent learns from and teaches other Clawpack agents!")
        print("="*70)
        
        print("\nðŸŒ AVAILABLE LANGUAGES:")
        langs = list(self.languages.items())
        for i in range(0, len(langs), 5):
            row = langs[i:i+5]
            print("  " + "  ".join([f"{code}: {name[:7]}" for code, name in row]))
        
        print("\nðŸ“š COMMANDS:")
        print("  /to [lang] [text]     - Translate text (learns from others)")
        print("  /learn [term]         - Learn medical terms from Mediclaw")
        print("  /stats                - Show shared learning statistics")
        print("  /languages            - List all languages")
        print("  /quit                 - Exit")
        
        print("\nðŸ“– EXAMPLES:")
        print("  /to es What are Smart Tokens on TX blockchain?")
        print("  /learn diabetes")
        print("  /stats")
        print("="*70)
        
        while True:
            cmd = input("\nðŸŒ Polyclaw> ").strip()
            
            if not cmd:
                continue
            if cmd == '/quit':
                break
            if cmd == '/languages':
                print("\nðŸŒ SUPPORTED LANGUAGES:")
                for code, name in self.languages.items():
                    print(f"  {code}: {name}")
                continue
            if cmd == '/stats':
                self.get_shared_stats()
                continue
            
            if cmd.startswith('/to '):
                parts = cmd[4:].split(' ', 1)
                if len(parts) < 2:
                    print("Usage: /to [language] [text]")
                    continue
                
                target_lang = parts[0].lower()
                text = parts[1]
                
                if target_lang not in self.languages:
                    print(f"Unknown language. Use /languages to see all.")
                    continue
                
                print(f"\nðŸ¦ž Translating to {self.languages[target_lang]}...")
                print("ðŸ” Checking if another agent has translated this...")
                
                result = self.translate(text, target_lang)
                print(f"\nðŸ“ TRANSLATION:\n{result}\n")
                print("-"*50)
            
            elif cmd.startswith('/learn '):
                term = cmd[7:]
                print(f"\nðŸ” Learning about: {term}")
                self.learn_from_medical(term)
                print()
            
            else:
                print("Unknown command. Use /to, /learn, /stats, or /languages")

if __name__ == "__main__":
    poly = PolyclawShared()
    poly.chat()
