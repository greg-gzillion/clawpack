#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AGENTFORLAW - Complete Legal Research System
With OpenRouter API, Legal Resources, and Cross-Agent Search
"""

import sys
import sqlite3
import urllib.parse
import urllib.request
import webbrowser
import os
import json
from pathlib import Path
from datetime import datetime

# ============================================
# PATHS
# ============================================
ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack")
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
LEGAL_REFS = ROOT_DIR / "agents" / "webclaw" / "references" / "agentforlaw"

# Load .env file
env_path = ROOT_DIR / ".env"
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

class AgentForLaw:
    def __init__(self):
        self.print_welcome()
    
    def print_welcome(self):
        print("\n" + "="*70)
        print("⚖️ AGENTFORLAW - COMPLETE LEGAL RESEARCH")
        print("="*70)
        print("\nCOMMANDS:")
        print("  /stats")
        print("  /llm [question]")
        print("  /search [query]")
        print("  /court [state]")
        print("  /browse [jurisdiction]")
        print("  /list")
        print("  /help, /quit")
        print("="*70)
    
    def run(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("\n⚖️ AgentForLaw> ").strip()
                if not cmd:
                    continue
                
                # Parse command and arguments
                parts = cmd.split(' ', 1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command == "/quit":
                    print("Goodbye!")
                    break
                elif command == "/help":
                    self.print_welcome()
                elif command == "/stats":
                    self.show_stats()
                elif command == "/list":
                    self.list_jurisdictions()
                elif command == "/llm":
                    self.handle_llm(args)
                elif command == "/search":
                    self.handle_search(args)
                elif command == "/court":
                    self.handle_court(args)
                elif command == "/browse":
                    self.browse_jurisdiction(args)
                else:
                    print(f"Unknown command: {command}")
                    print("Type /help for available commands")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_stats(self):
        print("\n" + "="*50)
        print("📊 SYSTEM STATISTICS")
        print("="*50)
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if api_key:
            print(f"✅ OpenRouter API: Configured")
        else:
            print("❌ OpenRouter API: Not configured")
        print(f"📁 Legal Resources: {LEGAL_REFS}")
        print(f"💾 Shared Memory: {SHARED_DB}")
        
        # Count available jurisdictions
        juris_path = LEGAL_REFS / "jurisdictions"
        if juris_path.exists():
            states = [d.name for d in juris_path.iterdir() if d.is_dir()]
            print(f"🗺️ Jurisdictions Available: {len(states)} states")
        print("="*50)
    
    def list_jurisdictions(self):
        """List all available jurisdictions"""
        print("\n" + "="*50)
        print("🗺️ AVAILABLE JURISDICTIONS")
        print("="*50)
        
        juris_path = LEGAL_REFS / "jurisdictions"
        if juris_path.exists():
            states = sorted([d.name for d in juris_path.iterdir() if d.is_dir()])
            print(f"\nFound {len(states)} states:\n")
            # Display in columns
            for i, state in enumerate(states, 1):
                print(f"  {state}", end="  ")
                if i % 8 == 0:
                    print()
            print(f"\n\n💡 Use /browse {states[0]} to explore a state")
        else:
            print("No jurisdictions found")
    
    def browse_jurisdiction(self, state):
        """Browse a specific jurisdiction's court files"""
        if not state:
            print("❌ Please provide a state code (e.g., TX, CA, NY)")
            return
        
        state = state.strip().upper()
        state_path = LEGAL_REFS / "jurisdictions" / state
        
        if not state_path.exists():
            print(f"❌ State '{state}' not found")
            print("\nAvailable states:")
            juris_path = LEGAL_REFS / "jurisdictions"
            if juris_path.exists():
                states = [d.name for d in juris_path.iterdir() if d.is_dir()][:20]
                print(f"  {', '.join(states)}...")
            return
        
        print(f"\n📁 Exploring {state} Court System")
        print("="*50)
        
        # Find all county directories
        counties = [d for d in state_path.iterdir() if d.is_dir()]
        
        if counties:
            print(f"\n🏛️ COUNTIES ({len(counties)} total):\n")
            for county in sorted(counties)[:30]:
                # Count court files in this county
                court_files = list(county.rglob("*.md"))
                print(f"  • {county.name}: {len(court_files)} court files")
            
            if len(counties) > 30:
                print(f"\n  ... and {len(counties) - 30} more counties")
            
            print(f"\n💡 To view a specific county: /browse {state}/DALLAS")
        else:
            # Look for direct court files
            court_files = list(state_path.rglob("*.md"))
            if court_files:
                print(f"\n📄 Court Documents ({len(court_files)} files):\n")
                for cf in court_files[:20]:
                    rel_path = cf.relative_to(state_path)
                    print(f"  • {rel_path}")
    
    def handle_llm(self, question):
        """Handle LLM queries using OpenRouter"""
        if not question:
            print("❌ Please provide a question")
            print("Example: /llm What is tort law?")
            return
        
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            print("\n❌ OPENROUTER_API_KEY not configured")
            return
        
        print(f"\n🤖 QUESTION: {question}")
        print("="*60)
        print("📡 Contacting OpenRouter API...")
        
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a legal expert assistant. Provide accurate, clear legal information."},
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
            req.add_header('HTTP-Referer', 'https://clawpack.local')
            req.add_header('X-Title', 'CLAWpack AgentForLaw')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                answer = result['choices'][0]['message']['content']
                print("\n" + "="*60)
                print("🤖 RESPONSE:")
                print("="*60)
                print(answer)
                print("="*60)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_search(self, query):
        """Search legal resources including jurisdictions"""
        if not query:
            print("❌ Please provide a search query")
            return
        
        print(f"\n🔍 SEARCHING: {query}")
        print("-"*50)
        
        results = []
        
        # Search in all legal resources
        if LEGAL_REFS.exists():
            for area in LEGAL_REFS.iterdir():
                if area.is_dir():
                    for md_file in area.rglob("*.md"):
                        try:
                            # Read first 10KB for performance
                            content = md_file.read_text(encoding='utf-8', errors='ignore')[:10000]
                            if query.lower() in content.lower():
                                rel_path = md_file.relative_to(LEGAL_REFS)
                                results.append(rel_path)
                                if len(results) >= 10:
                                    break
                        except:
                            pass
                if len(results) >= 10:
                    break
        
        if results:
            print(f"\n✅ Found {len(results)} results:\n")
            for r in results:
                # Highlight the area
                area = str(r).split('\\')[0] if '\\' in str(r) else "general"
                print(f"  📁 {area}")
                print(f"     📄 {r.name}")
                print()
        else:
            print("\n❌ No results found")
            print("\n💡 Tips:")
            print("   • Use /list to see available jurisdictions")
            print("   • Use /browse to explore specific states")
            print("   • Use /llm for AI-powered answers")
    
    def handle_court(self, location):
        """Get court information for a state or county"""
        if not location:
            print("❌ Please provide a state (e.g., TX) or state/county (e.g., TX/DALLAS)")
            return
        
        location = location.strip().upper()
        
        # Check if it's state/county format
        if '/' in location:
            state, county = location.split('/', 1)
            self.show_county_courts(state, county)
        else:
            self.show_state_courts(location)
    
    def show_state_courts(self, state):
        """Show courts for a state"""
        state_path = LEGAL_REFS / "jurisdictions" / state
        
        if not state_path.exists():
            print(f"\n❌ No data found for {state}")
            print("\n💡 Available states:")
            juris_path = LEGAL_REFS / "jurisdictions"
            if juris_path.exists():
                states = [d.name for d in juris_path.iterdir() if d.is_dir()][:15]
                print(f"   {', '.join(states)}")
            return
        
        print(f"\n🏛️ {state} COURT SYSTEM")
        print("="*50)
        
        # Look for state-level court files
        state_files = list(state_path.rglob("*.md"))
        
        if state_files:
            print("\n📄 State Court Documents:\n")
            for sf in state_files[:10]:
                if 'state' in str(sf).lower():
                    content = sf.read_text(encoding='utf-8', errors='ignore')[:500]
                    lines = content.split('\n')
                    title = lines[0].replace('#', '').strip() if lines else sf.stem
                    print(f"  • {title}")
        
        # Count counties
        counties = [d for d in state_path.iterdir() if d.is_dir()]
        if counties:
            print(f"\n🗺️ Counties with court data: {len(counties)}")
            print(f"\n💡 To view a specific county: /court {state}/DALLAS")
    
    def show_county_courts(self, state, county):
        """Show courts for a specific county"""
        county_path = LEGAL_REFS / "jurisdictions" / state / county
        
        if not county_path.exists():
            print(f"\n❌ No data found for {county} County, {state}")
            return
        
        print(f"\n🏛️ {county} COUNTY, {state}")
        print("="*50)
        
        court_files = list(county_path.glob("*.md"))
        
        if court_files:
            print(f"\n📄 Court Information ({len(court_files)} files):\n")
            for cf in court_files:
                content = cf.read_text(encoding='utf-8', errors='ignore')
                # Get title from first line
                lines = content.split('\n')
                title = lines[0].replace('#', '').strip() if lines else cf.stem
                print(f"\n{'='*40}")
                print(f"📋 {title}")
                print('='*40)
                # Show first 800 characters
                print(content[:800])
                if len(content) > 800:
                    print("\n... (truncated)")
        else:
            print("No court files found for this county")

if __name__ == "__main__":
    agent = AgentForLaw()
    agent.run()
