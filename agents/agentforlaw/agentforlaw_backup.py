#!/usr/bin/env python3
"""
AGENTFORLAW - Open Court Access Agent
"""

import sys
import os
import sqlite3
import urllib.parse
import webbrowser
from pathlib import Path
from datetime import datetime

# Paths
AGENT_DIR = Path(__file__).parent
ROOT_DIR = AGENT_DIR.parent.parent
WEBCLAW_REFS = ROOT_DIR / "agents" / "webclaw" / "references" / "agentforlaw"
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
SHARED_DB.parent.mkdir(exist_ok=True)

class AgentForLaw:
    def __init__(self):
        self.name = "agentforlaw"
        self.init_shared_memory()
        self.print_welcome()
    
    def init_shared_memory(self):
        try:
            conn = sqlite3.connect(str(SHARED_DB))
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS agentforlaw_knowledge
                         (id INTEGER PRIMARY KEY, query TEXT UNIQUE,
                          response TEXT, category TEXT, jurisdiction TEXT,
                          timestamp TEXT, source_agent TEXT)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Init error: {e}")
    
    def save_to_shared_memory(self, query, response, category="court_info", jurisdiction="federal"):
        try:
            conn = sqlite3.connect(str(SHARED_DB))
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO agentforlaw_knowledge
                         (query, response, category, jurisdiction, timestamp, source_agent)
                         VALUES (?,?,?,?,?,?)''',
                      (query.lower(), response[:500], category, jurisdiction,
                       datetime.now().isoformat(), self.name))
            conn.commit()
            conn.close()
            print(f"💾 Saved to shared memory: {query[:50]}...")
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    def print_welcome(self):
        print("\n" + "="*70)
        print("⚖️ AGENTFORLAW - Open Court Access")
        print("="*70)
        print("🔓 FREE ACCESS TO:")
        print("  • All US court systems (via Webclaw)")
        print("  • 50 State Courts + Federal Courts")
        print("  • Case law search (no paywalls)")
        print("="*70)
        print("\n📚 COMMANDS:")
        print("  /court [state]     - Get court info (TX, CA, NY)")
        print("  /search [case]     - Search case law (opens free databases)")
        print("  /stats             - Show shared memory stats")
        print("  /quit              - Exit")
        print("="*70)
    
    def get_court_info(self, jurisdiction):
        jurisdictions_path = WEBCLAW_REFS / "jurisdictions"
        if not jurisdictions_path.exists():
            return None
        
        # Try state code (TX, CA, etc.)
        juris_path = jurisdictions_path / jurisdiction.upper()
        if juris_path.exists():
            court_file = juris_path / "court_system.md"
            if court_file.exists():
                return court_file.read_text(encoding='utf-8')
        
        # Try full name match
        for state_dir in jurisdictions_path.iterdir():
            if state_dir.is_dir() and jurisdiction.lower() in state_dir.name.lower():
                court_file = state_dir / "court_system.md"
                if court_file.exists():
                    return court_file.read_text(encoding='utf-8')
        return None
    
    def handle_court(self, jurisdiction):
        print(f"\n🏛️ Looking up: {jurisdiction}")
        print("-" * 50)
        info = self.get_court_info(jurisdiction)
        if info:
            print(info[:1500])
            self.save_to_shared_memory(f"court_{jurisdiction}", info[:500], "court_info", jurisdiction)
        else:
            print(f"❌ No info found for: {jurisdiction}")
            print("Try: TX, CA, NY, FL, or use 2-letter state code")
    
    def handle_search(self, query):
        print(f"\n🔍 Searching: {query}")
        print("-" * 50)
        
        # Free search engines
        engines = {
            "courtlistener": f"https://www.courtlistener.com/?q={urllib.parse.quote(query)}",
            "google_scholar": f"https://scholar.google.com/scholar?q={urllib.parse.quote(query)}",
            "justia": f"https://law.justia.com/search?q={urllib.parse.quote(query)}"
        }
        
        print("🔓 Opening free databases:")
        for name, url in engines.items():
            print(f"  • {name}: {url}")
            webbrowser.open(url)
        
        self.save_to_shared_memory(query, f"Searched: {query}", "search", "general")
    
    def show_stats(self):
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        try:
            c.execute('SELECT COUNT(*) FROM agentforlaw_knowledge')
            count = c.fetchone()[0]
            print(f"\n📊 Shared memory entries from AgentForLaw: {count}")
        except:
            print("No entries yet")
        conn.close()
    
    def run(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("\n⚖️ AgentForLaw> ").strip()
                if not cmd:
                    continue
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/help":
                    self.print_welcome()
                elif cmd == "/stats":
                    self.show_stats()
                elif cmd.startswith("/court "):
                    self.handle_court(cmd[7:])
                elif cmd.startswith("/search "):
                    self.handle_search(cmd[8:])
                else:
                    print("Unknown command. Use /court, /search, /stats, /quit")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = AgentForLaw()
    agent.run()