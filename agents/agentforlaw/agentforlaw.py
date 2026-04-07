#!/usr/bin/env python3
"""
AGENTFORLAW - Open Court Access Agent
Part of Clawpack Cross-Learning Ecosystem

ARCHITECTURE:
- ALL references come from Webclaw (central reference hub)
- ALL documents go to DocuClaw for creation
- ALL knowledge shared via shared memory
- NO hardcoded data - everything is referenced
"""

import sys
import os
import sqlite3
import re
import urllib.parse
import webbrowser
from pathlib import Path
from datetime import datetime

# ============================================
# CLAWPACK PATHS
# ============================================
AGENT_DIR = Path(__file__).parent
ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack")
WEBCLAW_REFS = ROOT_DIR / "agents" / "webclaw" / "references" / "agentforlaw"
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

# ============================================
# SHARED MEMORY - Cross-Learning
# ============================================
SHARED_DB.parent.mkdir(exist_ok=True)

def init_shared_memory():
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agentforlaw_knowledge
                 (id INTEGER PRIMARY KEY, query TEXT UNIQUE,
                  response TEXT, category TEXT, jurisdiction TEXT,
                  timestamp TEXT, source_agent TEXT, usage_count INTEGER DEFAULT 1)''')
    c.execute('''CREATE TABLE IF NOT EXISTS case_searches
                 (id INTEGER PRIMARY KEY, query TEXT, citation TEXT,
                  court TEXT, date TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_to_shared_memory(query, response, category="general", jurisdiction="federal"):
    try:
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO agentforlaw_knowledge 
                     (query, response, category, jurisdiction, timestamp, source_agent)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (query, response[:2000], category, jurisdiction, 
                   datetime.now().isoformat(), "agentforlaw"))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def get_court_info(jurisdiction):
    """Get court information from Webclaw jurisdictions folder"""
    juris_path = WEBCLAW_REFS / "jurisdictions" / jurisdiction.upper()
    
    if not juris_path.exists():
        return None
    
    output = []
    
    # Read state-level resources
    state_resources = juris_path / "state_resources.md"
    if state_resources.exists():
        output.append(state_resources.read_text(encoding='utf-8')[:1500])
    
    # List county/court directories
    for county_dir in sorted(juris_path.iterdir()):
        if county_dir.is_dir() and county_dir.name not in ['state', 'federal']:
            output.append(f"\n## {county_dir.name} County")
            for court_file in sorted(county_dir.glob("*.md")):
                court_name = court_file.stem.replace('_', ' ').title()
                content = court_file.read_text(encoding='utf-8')
                output.append(f"\n### {court_name}\n{content[:500]}")
    
    return "\n".join(output) if output else None

def main():
    init_shared_memory()
    
    print("=" * 70)
    print("⚖️ AGENTFORLAW - Open Court Access")
    print("=" * 70)
    print("🔓 FREE ACCESS TO:")
    print("  • All US court systems (via Webclaw references)")
    print("  • 50 State Courts + Federal Courts")
    print("  • Case law search (no paywalls)")
    print("  • Legal citations and forms")
    print("=" * 70)
    print("\n📚 COMMANDS:")
    print("  /court [state]  - Get court information (from Webclaw)")
    print("  /stats          - Show shared memory stats")
    print("  /help, /quit")
    print("=" * 70)
    print("💡 All references come from Webclaw - the central hub")
    print("🔗 All knowledge shared with other Clawpack agents")
    print("=" * 70)
    
    while True:
        try:
            cmd = input("\n⚖️ AgentForLaw> ").strip()
            
            if cmd == "/quit" or cmd == "/exit":
                print("Goodbye!")
                break
            elif cmd == "/help":
                print("\nCOMMANDS:")
                print("  /court [state]  - Get court info (TX, CA, NY, etc.)")
                print("  /stats          - Show shared memory stats")
                print("  /quit           - Exit")
            elif cmd == "/stats":
                conn = sqlite3.connect(str(SHARED_DB))
                c = conn.cursor()
                c.execute("SELECT COUNT(*) FROM agentforlaw_knowledge")
                count = c.fetchone()[0]
                conn.close()
                print(f"\n📊 Shared Memory Stats:")
                print(f"  Knowledge entries: {count}")
            elif cmd.startswith("/court "):
                state = cmd[7:].strip().upper()
                print(f"\n🏛️ Looking up court information for: {state}")
                print("-" * 50)
                info = get_court_info(state)
                if info:
                    print(info)
                    save_to_shared_memory(f"court_{state}", info[:500], "court_info", state)
                else:
                    print(f"❌ No court information found for: {state}")
                    print("Try: /court CA, /court NY, /court TX")
            else:
                print("Unknown command. Type /help for commands.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
