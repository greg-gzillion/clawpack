#!/usr/bin/env python3
"""
AGENTFORLAW - Open Court Access Agent
Part of Clawpack Cross-Learning Ecosystem
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
ROOT_DIR = AGENT_DIR.parent.parent
WEBCLAW_REFS = ROOT_DIR / "agents" / "webclaw" / "references" / "agentforlaw"
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
SHARED_DB.parent.mkdir(exist_ok=True)

# ============================================
# STATE NAME MAPPING
# ============================================
STATE_NAME_MAP = {
    'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR',
    'california': 'CA', 'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE',
    'florida': 'FL', 'georgia': 'GA', 'hawaii': 'HI', 'idaho': 'ID',
    'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA', 'kansas': 'KS',
    'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
    'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS',
    'missouri': 'MO', 'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV',
    'new hampshire': 'NH', 'new jersey': 'NJ', 'new mexico': 'NM', 'new york': 'NY',
    'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH', 'oklahoma': 'OK',
    'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
    'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT',
    'vermont': 'VT', 'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV',
    'wisconsin': 'WI', 'wyoming': 'WY'
}

def normalize_jurisdiction(jurisdiction):
    """Convert state name to 2-letter code"""
    jur_lower = jurisdiction.lower().strip()
    if len(jurisdiction) == 2 and jurisdiction.isalpha():
        return jurisdiction.upper()
    return STATE_NAME_MAP.get(jur_lower, jurisdiction.upper())

# ============================================
# SHARED MEMORY FUNCTIONS
# ============================================
def init_shared_memory():
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agentforlaw_knowledge
                 (id INTEGER PRIMARY KEY, query TEXT UNIQUE,
                  response TEXT, category TEXT, jurisdiction TEXT,
                  timestamp TEXT, source_agent TEXT, usage_count INTEGER DEFAULT 1)''')
    conn.commit()
    conn.close()

def save_to_shared_memory(query, response, category="general", jurisdiction="federal"):
    try:
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO agentforlaw_knowledge
                     (query, response, category, jurisdiction, timestamp, source_agent, usage_count)
                     VALUES (?,?,?,?,?,?,1)''',
                  (query.lower(), response[:500], category, jurisdiction,
                   datetime.now().isoformat(), "agentforlaw"))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

# ============================================
# WEBCLAW QUERY FUNCTIONS
# ============================================
def get_court_info(jurisdiction):
    """Get court information from Webclaw jurisdictions folder"""
    jurisdictions_path = WEBCLAW_REFS / "jurisdictions"
    
    if not jurisdictions_path.exists():
        return None
    
    normalized = normalize_jurisdiction(jurisdiction)
    juris_path = jurisdictions_path / normalized
    
    if juris_path.exists():
        court_file = juris_path / "court_system.md"
        if court_file.exists():
            return court_file.read_text(encoding='utf-8')
    
    # Try partial match by name
    for state_dir in jurisdictions_path.iterdir():
        if state_dir.is_dir() and jurisdiction.lower() in state_dir.name.lower():
            court_file = state_dir / "court_system.md"
            if court_file.exists():
                return court_file.read_text(encoding='utf-8')
    
    return None

def get_federal_court_info(circuit=None):
    """Get federal court information from Webclaw"""
    federal_path = WEBCLAW_REFS / "jurisdictions" / "federal"
    
    if not federal_path.exists():
        return None
    
    if circuit:
        for district_dir in federal_path.iterdir():
            if district_dir.is_dir() and circuit.lower() in district_dir.name.lower():
                court_file = district_dir / "district_court.md"
                if court_file.exists():
                    return court_file.read_text(encoding='utf-8')
    
    return None

def query_webclaw_reference(topic):
    """Search Webclaw reference files"""
    if not WEBCLAW_REFS.exists():
        return None
    
    topic_lower = topic.lower()
    results = []
    
    for category_dir in WEBCLAW_REFS.iterdir():
        if category_dir.is_dir():
            for md_file in category_dir.glob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    if topic_lower in content.lower():
                        results.append({
                            "category": category_dir.name,
                            "file": md_file.name,
                            "content": content[:500]
                        })
                except:
                    pass
    
    return results[:3]

# ============================================
# SEARCH FUNCTIONS
# ============================================
FREE_SEARCH_ENGINES = {
    "courtlistener": "https://www.courtlistener.com/?q={query}",
    "google_scholar": "https://scholar.google.com/scholar?as_sdt=4,60&q={query}",
    "justia": "https://law.justia.com/search?q={query}",
    "findlaw": "https://caselaw.findlaw.com/search?q={query}",
    "openjurist": "https://openjurist.org/search?q={query}",
    "recap": "https://www.courtlistener.com/recap/?q={query}",
}

def search_case_law(query):
    encoded = urllib.parse.quote(query)
    results = {}
    for name, url_template in FREE_SEARCH_ENGINES.items():
        results[name] = url_template.format(query=encoded)
    return results

# ============================================
# MAIN AGENT CLASS
# ============================================
class AgentForLaw:
    def __init__(self):
        init_shared_memory()
        self.print_welcome()
    
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
        print("  /court [state]     - Get court info (CA, Texas, New York)")
        print("  /federal [circuit] - Get federal court info (9th, 2nd)")
        print("  /search [case]     - Search case law (opens free databases)")
        print("  /ref [topic]       - Search Webclaw references")
        print("  /stats             - Show shared memory stats")
        print("  /quit              - Exit")
        print("="*70)
        print(f"📁 Webclaw: {WEBCLAW_REFS}")
        print("="*70)
    
    def handle_court(self, jurisdiction):
        print(f"\n🏛️ Looking up: {jurisdiction}")
        print("-" * 50)
        info = get_court_info(jurisdiction)
        if info:
            print(info[:1500])
            save_to_shared_memory(f"court_{jurisdiction}", info[:300], "court_info", jurisdiction)
        else:
            print(f"❌ No info found for: {jurisdiction}")
            print("Try: CA, Texas, New York, FL, NY, TX")
    
    def handle_federal(self, circuit):
        print(f"\n🏛️ Federal Circuit: {circuit}")
        print("-" * 50)
        info = get_federal_court_info(circuit)
        if info:
            print(info[:1500])
        else:
            print(f"❌ No info found for circuit: {circuit}")
            print("Try: 9th, 2nd, 11th, 5th")
    
    def handle_search(self, query):
        print(f"\n🔍 Searching: {query}")
        print("-" * 50)
        searches = search_case_law(query)
        print("🔓 Opening free databases:")
        for name, url in searches.items():
            print(f"  • {name}: {url}")
            webbrowser.open(url)
        save_to_shared_memory(query, f"Searched: {query}", "search")
        print("\n💡 Saved to shared memory - all agents can learn from this")
    
    def handle_ref(self, topic):
        print(f"\n📚 Searching Webclaw: {topic}")
        print("-" * 50)
        results = query_webclaw_reference(topic)
        if results:
            for r in results:
                print(f"\n📁 {r['category']}/{r['file']}")
                print(f"   {r['content'][:200]}...")
        else:
            print(f"No references found for: {topic}")
    
    def show_stats(self):
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        try:
            c.execute('SELECT COUNT(*) FROM agentforlaw_knowledge')
            count = c.fetchone()[0]
            print(f"\n📊 Shared memory entries: {count}")
            if count > 0:
                print("\n📚 Recent:")
                c.execute('SELECT query, category FROM agentforlaw_knowledge ORDER BY id DESC LIMIT 5')
                for row in c.fetchall():
                    print(f"  • {row[0][:40]}... ({row[1]})")
        except:
            print("No knowledge yet")
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
                elif cmd.startswith("/court_rules "):`n                    self.handle_court_rules(cmd[13:])`n                elif cmd.startswith("/court "):
                    self.handle_court(cmd[7:])
                elif cmd.startswith("/federal "):
                    self.handle_federal(cmd[9:])
                elif cmd.startswith("/search "):
                    self.handle_search(cmd[8:])
                elif cmd.startswith("/ref "):
                    self.handle_ref(cmd[5:])
                else:
                    self.handle_search(cmd)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = AgentForLaw()
    agent.run()