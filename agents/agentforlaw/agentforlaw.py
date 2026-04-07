#!/usr/bin/env python3
"""
AGENTFORLAW - Open Court Access with WORKING Cross-Agent Search
"""

import sys
import sqlite3
import urllib.parse
import webbrowser
from pathlib import Path
from datetime import datetime

# ============================================
# PATHS
# ============================================
ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack")
WEBCLAW_REFS = Path(r"C:\Users\greg\dev\clawpack\agents\webclaw\references\agentforlaw")
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

SHARED_DB.parent.mkdir(exist_ok=True)

# ============================================
# WORKING CROSS-AGENT SEARCH
# ============================================

def cross_agent_search(query):
    """Search ALL agents' shared memory - DIRECT DATABASE QUERY"""
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    query_lower = query.lower()
    results = []
    
    # 1. Search Medical Knowledge
    try:
        c.execute("SELECT query, response FROM medical_knowledge WHERE LOWER(query) LIKE ? OR LOWER(response) LIKE ?", 
                  (f'%{query_lower}%', f'%{query_lower}%'))
        for row in c.fetchall():
            results.append(('🏥', 'MedicLaw', row[0], row[1][:400]))
    except: pass
    
    # 2. Search Translations
    try:
        c.execute("SELECT source_text, translated_text FROM translations WHERE LOWER(source_text) LIKE ? OR LOWER(translated_text) LIKE ?", 
                  (f'%{query_lower}%', f'%{query_lower}%'))
        for row in c.fetchall():
            results.append(('🌐', 'PolyClaw', f"{row[0]} → {row[1]}", ''))
    except: pass
    
    # 3. Search Math Knowledge (different column names)
    try:
        c.execute("SELECT * FROM math_knowledge LIMIT 1")
        cols = [description[0] for description in c.description]
        if 'question' in cols:
            c.execute("SELECT question, answer FROM math_knowledge WHERE LOWER(question) LIKE ?", (f'%{query_lower}%',))
            for row in c.fetchall():
                results.append(('📐', 'MathematicaClaw', row[0], row[1][:200]))
        elif 'query' in cols:
            c.execute("SELECT query, response FROM math_knowledge WHERE LOWER(query) LIKE ?", (f'%{query_lower}%',))
            for row in c.fetchall():
                results.append(('📐', 'MathematicaClaw', row[0], row[1][:200]))
    except: pass
    
    # 4. Search Court Knowledge
    try:
        c.execute("SELECT query, response FROM agentforlaw_knowledge WHERE LOWER(query) LIKE ? AND query NOT LIKE '/%'", (f'%{query_lower}%',))
        for row in c.fetchall():
            if not row[0].startswith('/'):
                results.append(('⚖️', 'AgentForLaw', row[0], row[1][:300]))
    except: pass
    
    # 5. Search Unified Knowledge
    try:
        c.execute("SELECT query, response FROM unified_knowledge WHERE LOWER(query) LIKE ?", (f'%{query_lower}%',))
        for row in c.fetchall():
            results.append(('🧠', 'Unified', row[0], row[1][:200]))
    except: pass
    
    conn.close()
    
    # Remove duplicates
    seen = set()
    unique = []
    for r in results:
        key = f"{r[0]}_{r[2]}"
        if key not in seen:
            seen.add(key)
            unique.append(r)
    
    return unique

# ============================================
# COURT DATA FUNCTIONS
# ============================================

def get_specific_county_info(state, county):
    county_path = WEBCLAW_REFS / "jurisdictions" / state.upper() / county
    if not county_path.exists():
        return f"County '{county}' not found in {state}."
    output = [f"# {county} County, {state}\n"]
    for court_file in sorted(county_path.glob("*.md")):
        court_name = court_file.stem.replace('_', ' ').title()
        content = court_file.read_text(encoding='utf-8')
        output.append(f"\n## {court_name}\n{content[:500]}")
    return "\n".join(output)

def get_court_info(jurisdiction):
    if '/' in jurisdiction:
        state, county = jurisdiction.split('/', 1)
        return get_specific_county_info(state.upper(), county.title())
    
    juris_path = WEBCLAW_REFS / "jurisdictions" / jurisdiction.upper()
    if not juris_path.exists():
        return None
    
    output = []
    state_dir = juris_path / "state"
    if state_dir.exists():
        for filename in ['supreme_court.md', 'court_of_appeals.md', 'state_resources.md']:
            file_path = state_dir / filename
            if file_path.exists():
                output.append(file_path.read_text(encoding='utf-8'))
    
    counties = [item.name for item in juris_path.iterdir() 
                if item.is_dir() and item.name not in ['state', 'federal']]
    
    if counties:
        output.append(f"\n## COUNTIES ({len(counties)})\n")
        output.append(f"Tip: Use /court {jurisdiction.upper()}/CountyName\n")
        output.append(f"**Counties:** {', '.join(sorted(counties)[:30])}")
        if len(counties) > 30:
            output.append(f"\n... and {len(counties) - 30} more")
    
    return "\n".join(output) if output else None

def get_federal_court_info(circuit=None):
    federal_path = WEBCLAW_REFS / "jurisdictions" / "federal"
    if not federal_path.exists():
        return None
    for district_dir in federal_path.iterdir():
        if district_dir.is_dir() and circuit and circuit.lower() in district_dir.name.lower():
            court_file = district_dir / "district_court.md"
            if court_file.exists():
                return court_file.read_text(encoding='utf-8')
    return None

# ============================================
# MAIN AGENT CLASS
# ============================================

class AgentForLaw:
    def __init__(self):
        self.print_welcome()
    
    def print_welcome(self):
        print("\n" + "="*70)
        print("⚖️ AGENTFORLAW - Open Court Access")
        print("="*70)
        print("\nCOMMANDS:")
        print("  /court [state]        - Get state court information")
        print("  /court [state]/[cty]  - Get specific county court")
        print("  /federal [circuit]    - Get federal court information")
        print("  /cross [query]        - Search ALL agents (MedicLaw, PolyClaw, etc)")
        print("  /cross-stats          - Show cross-agent statistics")
        print("  /stats                - Show local stats")
        print("  /help, /quit")
        print("="*70)
    
    def handle_cross(self, query):
        print(f"\n🔍 CROSS-AGENT SEARCH: '{query}'")
        print("="*60)
        
        results = cross_agent_search(query)
        
        if results:
            print(f"\n✅ Found {len(results)} results across agents:\n")
            for icon, agent, q, a in results:
                print(f"{icon} {agent}")
                print(f"   Q: {q}")
                if a:
                    print(f"   A: {a}")
                print()
        else:
            print("\n❌ No results found.")
            print("\n💡 Try: /cross symptoms, /cross hello, /cross flu")
    
    def handle_cross_stats(self):
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        print("\n" + "="*60)
        print("📊 CROSS-AGENT SHARED MEMORY STATISTICS")
        print("="*60)
        
        tables = [
            ('agentforlaw_knowledge', '⚖️ AgentForLaw'),
            ('medical_knowledge', '🏥 MedicLaw'),
            ('math_knowledge', '📐 MathematicaClaw'),
            ('translations', '🌐 PolyClaw'),
            ('unified_knowledge', '🧠 Unified'),
            ('memories', '💾 Memory'),
            ('documents', '📄 DocuClaw')
        ]
        
        total = 0
        for table, name in tables:
            try:
                c.execute(f"SELECT COUNT(*) FROM {table}")
                count = c.fetchone()[0]
                if count > 0:
                    print(f"  {name}: {count} entries")
                    total += count
            except:
                pass
        
        print(f"\n📚 TOTAL: {total} knowledge entries shared across agents")
        print("="*60)
        conn.close()
    
    def handle_court(self, jurisdiction):
        print(f"\n🏛️ {jurisdiction}")
        print("-" * 50)
        info = get_court_info(jurisdiction)
        if info:
            print(info[:2000])
        else:
            print(f"❌ No court information found for: {jurisdiction}")
    
    def handle_federal(self, circuit):
        print(f"\n🏛️ Federal Circuit: {circuit}")
        print("-" * 50)
        info = get_federal_court_info(circuit)
        if info:
            print(info)
        else:
            print(f"❌ No federal court found for: {circuit}")
    
    def show_stats(self):
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        try:
            c.execute('SELECT COUNT(*) FROM agentforlaw_knowledge')
            count = c.fetchone()[0]
            print(f"\n📊 AgentForLaw entries: {count}")
        except:
            print("No local data")
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
                elif cmd == "/cross-stats":
                    self.handle_cross_stats()
                elif cmd.startswith("/cross "):
                    self.handle_cross(cmd[7:])
                elif cmd.startswith("/court "):
                    self.handle_court(cmd[7:])
                elif cmd.startswith("/federal "):
                    self.handle_federal(cmd[9:])
                else:
                    print("Unknown command. Type /help")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = AgentForLaw()
    agent.run()
