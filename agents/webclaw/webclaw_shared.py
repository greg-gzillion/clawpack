#!/usr/bin/env python3
"""
🌐 WEBCLAW SHARED - Web Research Agent with Cross-Learning
Integrates with claw_shared memory system and shares knowledge with all agents
"""

import sys
import os
from pathlib import Path

# Add parent directories for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "claw_shared"))

# Import shared memory system
from memory import get_memory
from cross_learner import CrossAgentLearner

import requests
import sqlite3
from datetime import datetime

class WebclawShared:
    def __init__(self):
        self.name = "webclaw"
        self.memory = get_memory(self.name)
        self.learner = CrossAgentLearner()
        self.shared_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.medical_base = Path(__file__).parent / "references/mediclaw/medical"
        
        # Register with the agent registry
        self.memory.register(
            capabilities="web_research, medical_references, source_lookup, cross_referencing",
            repo="https://github.com/YOUR_USERNAME/clawpack/tree/main/agents/webclaw"
        )
        
        self.init_database()
        print(f"✅ Webclaw Shared initialized - Connected to cross-learning system")
    
    def init_database(self):
        """Initialize shared memory database"""
        self.shared_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS web_research (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT UNIQUE,
                url TEXT,
                content_summary TEXT,
                source_agent TEXT,
                timestamp TEXT,
                category TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_medical_specialty(self, specialty):
        """Get reference information for a medical specialty"""
        ref_path = self.medical_base / specialty / f"{specialty}_references.md"
        if ref_path.exists():
            content = ref_path.read_text(encoding='utf-8')
            # Store in shared memory for other agents
            self.memory.remember(
                key=f"medical_ref_{specialty}",
                value=content[:500],  # Store preview
                tags=f"medical,reference,{specialty}"
            )
            return content
        return None
    
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
    
    def research(self, topic):
        """Research a topic and share findings with other agents"""
        # First check shared memory
        existing = self.memory.recall(topic)
        if existing:
            print(f"📚 Found in shared memory from {existing[0][0]}")
            return existing[0][2]
        
        # Do research
        prompt = f"""Research the following topic and provide a comprehensive summary: {topic}

Include key facts, reputable sources, and important information.
Base your research on authoritative sources."""
        
        try:
            import os
            api_key = os.environ.get("OPENROUTER_API_KEY", "")
            if not api_key:
                return "❌ No API key found. Set OPENROUTER_API_KEY environment variable."
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                # Save to shared memory for other agents
                self.memory.remember(key=topic, value=result, tags="research")
                # Transfer knowledge to other agents
                self.learner.transfer_knowledge(
                    from_agent=self.name,
                    to_agent="all",
                    knowledge_type="research",
                    content=result[:500]
                )
                return result
            return f"⚠️ API Error: {response.status_code}"
        except Exception as e:
            return f"⚠️ Error: {e}"
    
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
    
    def run(self):
        """Main interactive loop"""
        print("\n" + "="*70)
        print("🌐 WEBCLAW SHARED - Web Research Agent with Cross-Learning")
        print("="*70)
        print("\n⚠️ DISCLAIMER: For research purposes only.")
        print(f"💡 Connected to cross-learning system. Sharing knowledge with {len(self.memory.get_agents())} agents.")
        print("="*70)
        
        print("\n📚 COMMANDS:")
        print("  /research [topic]     - Research a topic")
        print("  /sources [specialty]  - Show reference sources")
        print("  /list-specialties     - List all medical specialties")
        print("  /search [keyword]     - Search references for keyword")
        print("  /agents               - List connected agents")
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
                
                if cmd == '/agents':
                    agents = self.memory.get_agents()
                    print(f"\n🤖 Connected Agents ({len(agents)}):")
                    print("=" * 40)
                    for agent in agents:
                        print(f"  • {agent[0]} - {agent[1][:50]}...")
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
    webclaw = WebclawShared()
    webclaw.run()