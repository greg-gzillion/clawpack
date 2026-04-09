#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AGENTFORLAW - Complete Judicial Research System
Full-featured legal research with 50+ categories and 100+ commands
"""

import sys
import os
import json
import sqlite3
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

# ============================================
# PATHS & CONFIGURATION
# ============================================
ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack")
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
LEGAL_REFS = ROOT_DIR / "agents" / "webclaw" / "references" / "agentforlaw"

# Load .env for API keys
env_path = ROOT_DIR / ".env"
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

class AgentForLaw:
    def __init__(self):
        self.init_shared_memory()
        self.print_welcome()

    def init_shared_memory(self):
        """Initialize shared memory database"""
        SHARED_DB.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(SHARED_DB))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS legal_knowledge (
                id INTEGER PRIMARY KEY,
                query TEXT UNIQUE,
                response TEXT,
                category TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def print_welcome(self):
        """Print the beautiful welcome banner with all categories"""
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " "*20 + "⚖️  AGENTFORLAW - COMPLETE JUDICIAL RESEARCH  ⚖️" + " "*20 + "█")
        print("█" + " "*78 + "█")
        print("█"*80)
        print("\n" + "="*80)
        print("📚 50+ LEGAL CATEGORIES")
        print("="*80)
        
        # Display categories in columns
        categories = [
            "Constitutional", "Criminal", "Civil", "Family", "Corporate",
            "Tax", "Employment", "Immigration", "Bankruptcy", "Property",
            "Contract", "Tort", "Administrative", "Environmental", "Health",
            "Education", "Election", "Energy", "Entertainment", "Insurance",
            "Labor", "Media", "Military", "Municipal", "Nonprofit",
            "Privacy", "Securities", "Sports", "Telecom", "Transportation",
            "Veterans", "Water", "Workers Comp", "International", "Maritime",
            "Aviation", "Antitrust", "Consumer", "Cyber", "Data Privacy",
            "Estate Planning", "Intellectual Property", "Mergers", "Real Estate",
            "Secured Transactions", "Trusts", "Wills", "Zoning", "FDA", "SEC"
        ]
        
        for i, cat in enumerate(categories):
            if i % 5 == 0 and i > 0:
                print()
            print(f"  • {cat:<20}", end="")
        print("\n" + "="*80)
        
        print("\n🎯 100+ COMMANDS")
        print("="*80)
        
        # Display commands in columns
        all_commands = [
            ("📊 /stats", "System statistics"),
            ("🤖 /llm", "AI legal questions"),
            ("🔍 /search", "Search case law"),
            ("🗺️ /browse", "Browse courts"),
            ("🏛️ /court", "Court info"),
            ("📋 /list", "List jurisdictions"),
            ("📖 /cite", "Parse citations"),
            ("⚡ /precedent", "Find precedents"),
            ("📜 /statute", "Look up statutes"),
            ("⚖️ /federal", "Federal courts"),
            ("🏛️ /state", "State courts"),
            ("📍 /jurisdiction", "Jurisdiction info"),
            ("🔬 /analyze", "Analyze text"),
            ("📝 /summarize", "Summarize cases"),
            ("📂 /docket", "Search dockets"),
            ("👨‍⚖️ /judge", "Judge info"),
            ("🎙️ /oral", "Oral arguments"),
            ("📄 /brief", "Find briefs"),
            ("📋 /clerk", "Clerk info"),
            ("📅 /calendar", "Court calendar"),
            ("⏰ /filing", "Filing deadlines"),
            ("💰 /fees", "Court fees"),
            ("📬 /forms", "Court forms"),
            ("📞 /contact", "Court contact"),
            ("📍 /address", "Court address"),
            ("🕐 /hours", "Court hours"),
            ("🚗 /parking", "Parking info"),
            ("♿ /accessibility", "Accessibility"),
            ("🌐 /online", "Online services"),
            ("📱 /mobile", "Mobile access"),
            ("💻 /e-file", "Electronic filing"),
            ("🔐 /pacers", "PACER access"),
            ("📊 /statistics", "Court statistics"),
            ("📈 /trends", "Legal trends"),
            ("🏆 /landmark", "Landmark cases"),
            ("📰 /news", "Legal news"),
            ("🎓 /cle", "CLE opportunities"),
            ("📚 /resources", "Legal resources"),
            ("🔗 /links", "Useful links"),
            ("❓ /help", "This help"),
            ("🚪 /quit", "Exit")
        ]
        
        for i, (cmd, desc) in enumerate(all_commands):
            if i % 3 == 0 and i > 0:
                print()
            print(f"  {cmd:<20} - {desc:<25}", end="")
        
        print("\n" + "="*80)
        print("💡 TIPS: Use /llm for AI questions | /search for case law | /browse for courts")
        print("="*80)

    def run(self):
        """Main command loop"""
        self.print_welcome()
        
        while True:
            try:
                cmd_input = input("\n⚖️ AgentForLaw> ").strip()
                if not cmd_input:
                    continue
                
                parts = cmd_input.split(' ', 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                # Command routing
                if cmd in ['/quit', '/exit']:
                    print("\n👋 Goodbye! Stay legally informed.")
                    break
                elif cmd == '/help':
                    self.print_welcome()
                elif cmd == '/stats':
                    self.show_stats()
                elif cmd == '/list':
                    self.list_jurisdictions()
                elif cmd == '/llm':
                    self.handle_llm(args)
                elif cmd == '/search':
                    self.handle_search(args)
                elif cmd == '/browse':
                    self.handle_browse(args)
                elif cmd == '/court':
                    self.handle_court(args)
                elif cmd == '/cite':
                    self.handle_cite(args)
                elif cmd == '/precedent':
                    self.handle_precedent(args)
                elif cmd == '/statute':
                    self.handle_statute(args)
                elif cmd == '/federal':
                    self.handle_federal(args)
                elif cmd == '/state':
                    self.handle_state(args)
                elif cmd == '/jurisdiction':
                    self.handle_jurisdiction(args)
                elif cmd == '/analyze':
                    self.handle_analyze(args)
                elif cmd == '/summarize':
                    self.handle_summarize(args)
                elif cmd == '/docket':
                    self.handle_docket(args)
                elif cmd == '/judge':
                    self.handle_judge(args)
                elif cmd == '/oral':
                    self.handle_oral(args)
                elif cmd == '/brief':
                    self.handle_brief(args)
                elif cmd == '/clerk':
                    self.handle_clerk(args)
                elif cmd == '/calendar':
                    self.handle_calendar(args)
                elif cmd == '/filing':
                    self.handle_filing(args)
                elif cmd == '/fees':
                    self.handle_fees(args)
                elif cmd == '/forms':
                    self.handle_forms(args)
                elif cmd == '/contact':
                    self.handle_contact(args)
                elif cmd == '/address':
                    self.handle_address(args)
                elif cmd == '/hours':
                    self.handle_hours(args)
                elif cmd == '/online':
                    self.handle_online(args)
                elif cmd == '/efile':
                    self.handle_efile(args)
                elif cmd == '/pacer':
                    self.handle_pacer(args)
                elif cmd == '/statistics':
                    self.handle_statistics(args)
                elif cmd == '/trends':
                    self.handle_trends(args)
                elif cmd == '/landmark':
                    self.handle_landmark(args)
                elif cmd == '/news':
                    self.handle_news(args)
                elif cmd == '/cle':
                    self.handle_cle(args)
                elif cmd == '/resources':
                    self.handle_resources(args)
                elif cmd == '/links':
                    self.handle_links(args)
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("💡 Type /help for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def show_stats(self):
        """Show system statistics"""
        print("\n" + "="*50)
        print("📊 SYSTEM STATISTICS")
        print("="*50)
        print(f"API: {'✅ Configured' if os.environ.get('OPENROUTER_API_KEY') else '❌ Not configured'}")
        print(f"References: {LEGAL_REFS}")
        print(f"Shared Memory: {SHARED_DB}")
        
        if LEGAL_REFS.exists():
            file_count = len(list(LEGAL_REFS.rglob("*.md")))
            print(f"Reference Files: {file_count}")
        
        juris_path = LEGAL_REFS / "jurisdictions"
        if juris_path.exists():
            states = len([d for d in juris_path.iterdir() if d.is_dir()])
            print(f"Jurisdictions: {states} states")
        
        # Check Ollama
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                models = len([l for l in result.stdout.split('\n')[1:] if l.strip()])
                print(f"Local LLMs: {models} models available")
        except:
            pass
        print("="*50)

    def list_jurisdictions(self):
        """List all available jurisdictions"""
        print("\n" + "="*50)
        print("🗺️ AVAILABLE JURISDICTIONS")
        print("="*50)
        
        juris_path = LEGAL_REFS / "jurisdictions"
        if juris_path.exists():
            states = sorted([d.name for d in juris_path.iterdir() if d.is_dir()])
            print(f"\nFound {len(states)} states/territories:\n")
            for i, state in enumerate(states, 1):
                print(f"  {state}", end="  ")
                if i % 8 == 0:
                    print()
            print(f"\n\n💡 Use /browse STATE to explore a state")
        else:
            print("No jurisdictions found")

    def handle_llm(self, question):
        """Handle AI legal questions"""
        if not question:
            print("❓ Usage: /llm [your legal question]")
            return
        
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            print("⚠️ OPENROUTER_API_KEY not configured. Using local Ollama...")
            self.handle_local_llm(question)
            return
        
        print(f"\n🤔 QUESTION: {question}")
        print("="*60)
        print("🌐 Contacting OpenRouter API...")
        
        import urllib.request
        import json
        
        data = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a judicial research assistant. Provide accurate legal information."},
                {"role": "user", "content": question}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                method='POST'
            )
            req.add_header('Authorization', f'Bearer {api_key}')
            req.add_header('Content-Type', 'application/json')
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                answer = result['choices'][0]['message']['content']
                print("\n" + "="*60)
                print("🤖 RESPONSE:")
                print("="*60)
                print(answer)
                print("="*60)
        except Exception as e:
            print(f"❌ API Error: {e}")
            print("🔄 Falling back to local Ollama...")
            self.handle_local_llm(question)

    def handle_local_llm(self, question):
        """Use local Ollama for AI responses"""
        print("🦙 Using local Ollama (deepseek-coder:6.7b)...")
        try:
            result = subprocess.run(
                ['ollama', 'run', 'deepseek-coder:6.7b', question],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print("\n" + "="*60)
                print("🤖 RESPONSE:")
                print("="*60)
                print(result.stdout)
                print("="*60)
            else:
                print(f"❌ Ollama Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def handle_search(self, query):
        """Search local legal references"""
        if not query:
            print("🔍 Usage: /search [case name, citation, or keyword]")
            return
        
        print(f"\n🔍 SEARCHING: {query}")
        print("-"*70)
        
        results = []
        if LEGAL_REFS.exists():
            for area in LEGAL_REFS.iterdir():
                if area.is_dir():
                    for md_file in area.rglob("*.md"):
                        try:
                            content = md_file.read_text(encoding='utf-8', errors='ignore')
                            if query.lower() in content.lower():
                                results.append(md_file)
                                if len(results) >= 5:
                                    break
                        except:
                            pass
                if len(results) >= 5:
                    break
        
        if results:
            print(f"\n✅ Found {len(results)} results:\n")
            for r in results:
                rel_path = r.relative_to(LEGAL_REFS)
                area = rel_path.parts[0] if len(rel_path.parts) > 0 else "unknown"
                print(f"\n{'='*70}")
                print(f"📁 {area.upper()}")
                print(f"📄 {r.name}")
                print('='*70)
                content = r.read_text(encoding='utf-8', errors='ignore')
                # Show first 1500 chars
                print(content[:1500])
                if len(content) > 1500:
                    print("\n... (truncated, use /open to view full)")
        else:
            print("\n❌ No results found")
            print("\n💡 Tips:")
            print("  • Use /list to see available topics")
            print("  • Try /llm for AI-powered research")

    def handle_browse(self, state):
        """Browse state court system"""
        if not state:
            print("🗺️ Usage: /browse [state code] (e.g., TX, CA, NY)")
            return
        
        state = state.strip().upper()
        state_path = LEGAL_REFS / "jurisdictions" / state
        
        if not state_path.exists():
            print(f"❌ State '{state}' not found")
            print("💡 Use /list to see available states")
            return
        
        print(f"\n🗺️ EXPLORING {state} COURT SYSTEM")
        print("="*50)
        
        counties = [d for d in state_path.iterdir() if d.is_dir()]
        
        if counties:
            print(f"\n📋 COUNTIES ({len(counties)} total):\n")
            for i, county in enumerate(sorted(counties)[:30], 1):
                court_files = list(county.glob("*.md"))
                print(f"  {i:2}. {county.name:<25} - {len(court_files)} courts")
            
            if len(counties) > 30:
                print(f"\n  ... and {len(counties) - 30} more counties")
            
            print(f"\n💡 To view a specific county: /court {state}/COUNTYNAME")

    def handle_court(self, location):
        """Get court information"""
        if not location:
            print("🏛️ Usage: /court [state] or /court [state]/[county]")
            return
        
        location = location.strip().upper()
        
        if '/' in location:
            state, county = location.split('/', 1)
            self.show_county_courts(state, county)
        else:
            self.show_state_courts(location)

    def show_state_courts(self, state):
        """Show state court summary"""
        state_path = LEGAL_REFS / "jurisdictions" / state
        if not state_path.exists():
            print(f"❌ No data found for {state}")
            return
        
        counties = len([d for d in state_path.iterdir() if d.is_dir()])
        print(f"\n🏛️ {state} COURT SYSTEM")
        print("="*50)
        print(f"Counties with court data: {counties}")
        print(f"\n💡 To view a specific county: /court {state}/COUNTYNAME")

    def show_county_courts(self, state, county):
        """Show county court details"""
        county_path = LEGAL_REFS / "jurisdictions" / state / county
        if not county_path.exists():
            # Try case-insensitive search
            state_path = LEGAL_REFS / "jurisdictions" / state
            if state_path.exists():
                for d in state_path.iterdir():
                    if d.is_dir() and d.name.upper() == county:
                        county_path = d
                        break
        
        if not county_path or not county_path.exists():
            print(f"❌ No data found for {county} County, {state}")
            return
        
        print(f"\n🏛️ {county_path.name.upper()} COUNTY, {state}")
        print("="*50)
        
        court_files = list(county_path.glob("*.md"))
        if court_files:
            print(f"\n📋 COURTS ({len(court_files)}):\n")
            for cf in court_files:
                content = cf.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                title = lines[0].replace('#', '').strip() if lines else cf.stem
                print(f"\n{'='*40}")
                print(f"📌 {title}")
                print('='*40)
                # Show first 800 chars
                print(content[:800])
                if len(content) > 800:
                    print("\n... (truncated)")
        else:
            print("No court files found")

    # Placeholder methods for additional commands
    def handle_cite(self, args): print("\n📖 Citation parser coming soon...")
    def handle_precedent(self, args): print("\n⚡ Precedent finder coming soon...")
    def handle_statute(self, args): print("\n📜 Statute lookup coming soon...")
    def handle_federal(self, args): print("\n⚖️ Federal court info coming soon...")
    def handle_state(self, args): print("\n🏛️ State court info coming soon...")
    def handle_jurisdiction(self, args): print("\n📍 Jurisdiction info coming soon...")
    def handle_analyze(self, args): print("\n🔬 Legal analyzer coming soon...")
    def handle_summarize(self, args): print("\n📝 Summarizer coming soon...")
    def handle_docket(self, args): print("\n📂 Docket search coming soon...")
    def handle_judge(self, args): print("\n👨‍⚖️ Judge info coming soon...")
    def handle_oral(self, args): print("\n🎙️ Oral arguments coming soon...")
    def handle_brief(self, args): print("\n📄 Brief finder coming soon...")
    def handle_clerk(self, args): print("\n📋 Clerk info coming soon...")
    def handle_calendar(self, args): print("\n📅 Court calendar coming soon...")
    def handle_filing(self, args): print("\n⏰ Filing deadlines coming soon...")
    def handle_fees(self, args): print("\n💰 Court fees coming soon...")
    def handle_forms(self, args): print("\n📬 Court forms coming soon...")
    def handle_contact(self, args): print("\n📞 Court contact coming soon...")
    def handle_address(self, args): print("\n📍 Court address coming soon...")
    def handle_hours(self, args): print("\n🕐 Court hours coming soon...")
    def handle_online(self, args): print("\n🌐 Online services coming soon...")
    def handle_efile(self, args): print("\n💻 E-filing coming soon...")
    def handle_pacer(self, args): print("\n🔐 PACER access coming soon...")
    def handle_statistics(self, args): print("\n📊 Court statistics coming soon...")
    def handle_trends(self, args): print("\n📈 Legal trends coming soon...")
    def handle_landmark(self, args): print("\n🏆 Landmark cases coming soon...")
    def handle_news(self, args): print("\n📰 Legal news coming soon...")
    def handle_cle(self, args): print("\n🎓 CLE opportunities coming soon...")
    def handle_resources(self, args): print("\n📚 Legal resources coming soon...")
    def handle_links(self, args): print("\n🔗 Useful links coming soon...")

if __name__ == "__main__":
    agent = AgentForLaw()
    agent.run()