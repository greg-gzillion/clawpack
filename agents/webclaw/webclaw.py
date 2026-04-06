#!/usr/bin/env python3
"""
🌐 WEBCLAW - Web Research Agent with Cross-Learning
"""

import os
import requests
import sqlite3
from pathlib import Path
from datetime import datetime

# Load API key from environment variable
CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

class Webclaw:
    def __init__(self):
        self.name = "Webclaw"
        self.shared_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.medical_base = Path(__file__).parent / "references/mediclaw/medical"
        self.init_database()
    
    def init_database(self):
        """Initialize shared memory database"""
        self.shared_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS web_research (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT UNIQUE,
                content_summary TEXT,
                source_agent TEXT,
                timestamp TEXT,
                category TEXT
            )
        """)
        conn.commit()
        conn.close()
        print("✅ Webclaw database initialized")
    
    def get_medical_specialty(self, specialty):
        """Get reference information for a medical specialty"""
        ref_path = self.medical_base / specialty / f"{specialty}_references.md"
        if ref_path.exists():
            with open(ref_path, 'r', encoding='utf-8') as f:
                return f.read()
        return f"No reference found for: {specialty}"
    
    def list_medical_specialties(self):
        """List all available medical specialties"""
        if self.medical_base.exists():
            return [d.name for d in self.medical_base.iterdir() if d.is_dir()]
        return []
    
    def search_references(self, keyword):
        """Search across all medical references for a keyword"""
        results = []
        if self.medical_base.exists():
            for ref_file in self.medical_base.rglob("*_references.md"):
                content = ref_file.read_text(encoding='utf-8')
                if keyword.lower() in content.lower():
                    results.append(ref_file.stem.replace('_references', ''))
        return results
    
    def show_sources(self, specialty=None):
        """Show sources for a specialty or all specialties"""
        if specialty:
            content = self.get_medical_specialty(specialty)
            if content:
                print(content)
            else:
                print(f"No references found for {specialty}")
        else:
            print("\n📚 Available Medical Specialties:")
            print("=" * 40)
            for s in sorted(self.list_medical_specialties()):
                print(f"  • {s}")
            print("\n💡 Use /sources [specialty] for detailed references")
    
    def research(self, topic):
        """Research a topic using AI"""
        if not CLOUD_API_KEY:
            return "❌ No API key found. Set OPENROUTER_API_KEY environment variable."
        
        prompt = f"""Research the following topic and provide a comprehensive summary: {topic}

Include key facts, reputable sources, and important information.
Base your research on authoritative sources."""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"⚠️ API Error: {response.status_code}"
        except Exception as e:
            return f"⚠️ Error: {e}"
    
    def run(self):
        """Main interactive loop"""
        print("\n" + "="*70)
        print("🌐 WEBCLAW - Web Research Agent with Cross-Learning")
        print("="*70)
        print("\n⚠️ DISCLAIMER: For research purposes only.")
        print(f"💡 This agent has access to {len(self.list_medical_specialties())} medical specialty references including HRI, LMHI, etc.")
        print("="*70)
        
        print("\n📚 COMMANDS:")
        print("  /research [topic]     - Research a topic")
        print("  /sources [specialty]  - Show reference sources")
        print("  /list-specialties     - List all medical specialties")
        print("  /search [keyword]     - Search references for keyword")
        print("  /help                 - Show this menu")
        print("  /quit                 - Exit")
        
        print("\n📖 EXAMPLES:")
        print("  /research homeopathy")
        print("  /sources homeopathy")
        print("  /list-specialties")
        print("  /search HRI")
        print("="*70)
        
        while True:
            try:
                cmd = input("\n🌐 Webclaw> ").strip()
                
                if not cmd:
                    continue
                if cmd == '/quit':
                    print("👋 Goodbye!")
                    break
                if cmd == '/help':
                    continue
                
                if cmd == '/list-specialties':
                    specialties = self.list_medical_specialties()
                    print(f"\n📚 Medical Specialties ({len(specialties)}):")
                    print("=" * 40)
                    for s in sorted(specialties):
                        print(f"  • {s}")
                    continue
                
                if cmd.startswith('/sources '):
                    specialty = cmd[9:].strip()
                    self.show_sources(specialty)
                    continue
                
                if cmd.startswith('/search '):
                    keyword = cmd[8:].strip()
                    results = self.search_references(keyword)
                    if results:
                        print(f"\n🔍 Found '{keyword}' in: {', '.join(results)}")
                    else:
                        print(f"\n❌ No references found containing '{keyword}'")
                    continue
                
                if cmd.startswith('/research '):
                    topic = cmd[10:].strip()
                    print(f"\n🔍 RESEARCHING: {topic}\n")
                    result = self.research(topic)
                    print(result)
                    continue
                
                print("Unknown command. Type /help")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    if not CLOUD_API_KEY:
        print("❌ ERROR: OPENROUTER_API_KEY not found!")
        print("Please set it in your .env file or environment variables.")
    else:
        webclaw = Webclaw()
        webclaw.run()
