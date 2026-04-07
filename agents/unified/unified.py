#!/usr/bin/env python3
"""
UNIFIED CLAWPACK CONTROLLER - The Brain That Connects All Agents
All 19 agents share memory, learn from each other, and work together
"""

import sys
import sqlite3
import subprocess
import threading
import queue
from pathlib import Path
from datetime import datetime

# ============================================
# PATHS
# ============================================
AGENT_DIR = Path(__file__).parent
ROOT_DIR = AGENT_DIR.parent.parent
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

# ============================================
# ALL 19 AGENTS REGISTERED
# ============================================
AGENTS = {
    "agentforlaw": {"port": 8001, "capabilities": ["court", "law", "legal", "citation"]},
    "dataclaw": {"port": 8002, "capabilities": ["data", "database", "query"]},
    "docuclaw": {"port": 8003, "capabilities": ["document", "pdf", "contract"]},
    "webclaw": {"port": 8004, "capabilities": ["web", "reference", "search"]},
    "langclaw": {"port": 8005, "capabilities": ["language", "translate"]},
    "mediclaw": {"port": 8006, "capabilities": ["medical", "health", "diagnosis"]},
    "polyclaw": {"port": 8007, "capabilities": ["language", "translate"]},
    "mathematicaclaw": {"port": 8008, "capabilities": ["math", "calculate"]},
    "tx_agent": {"port": 8009, "capabilities": ["texas", "blockchain"]},
    "eagleclaw": {"port": 8010, "capabilities": ["scrape", "crawl"]},
    "sysclaw": {"port": 8011, "capabilities": ["system", "monitor"]},
    "knowledge": {"port": 8012, "capabilities": ["learn", "memory"]},
    "claw_code": {"port": 8013, "capabilities": ["code", "programming"]},
    "claw_coder": {"port": 8014, "capabilities": ["code", "generate"]},
    "crustyclaw": {"port": 8015, "capabilities": ["scrape", "data"]},
    "rustypycraw": {"port": 8016, "capabilities": ["crawl", "extract"]},
    "unified": {"port": 8017, "capabilities": ["orchestrate", "route"]},
    "masterclaw": {"port": 8018, "capabilities": ["master", "control"]},
    "ollama": {"port": 11434, "capabilities": ["llm", "ai", "generate"]}
}

class UnifiedController:
    """The Brain - Routes queries to the right agent and shares memory"""
    
    def __init__(self):
        self.name = "unified"
        self.init_shared_memory()
        self.message_queue = queue.Queue()
        self.running_agents = {}
        
    def init_shared_memory(self):
        """Initialize shared memory for ALL agents"""
        SHARED_DB.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        # Master knowledge table for ALL agents
        c.execute('''CREATE TABLE IF NOT EXISTS unified_knowledge
                     (id INTEGER PRIMARY KEY, query TEXT UNIQUE,
                      response TEXT, agent_source TEXT, category TEXT,
                      timestamp TEXT, confidence REAL, 
                      usage_count INTEGER DEFAULT 1)''')
        
        # Agent registry
        c.execute('''CREATE TABLE IF NOT EXISTS agent_registry
                     (agent_name TEXT PRIMARY KEY, status TEXT,
                      last_seen TEXT, capabilities TEXT,
                      pid INTEGER)''')
        
        # Cross-agent messages
        c.execute('''CREATE TABLE IF NOT EXISTS agent_messages
                     (id INTEGER PRIMARY KEY, from_agent TEXT,
                      to_agent TEXT, message TEXT, timestamp TEXT,
                      status TEXT DEFAULT 'pending')''')
        
        # Learning from all agents
        c.execute('''CREATE TABLE IF NOT EXISTS cross_agent_learnings
                     (id INTEGER PRIMARY KEY, source_agent TEXT,
                      target_agent TEXT, knowledge_id INTEGER,
                      transfer_date TEXT, success_rate REAL)''')
        
        conn.commit()
        conn.close()
        print("✅ Unified shared memory initialized for ALL 19 agents")
    
    def register_agent(self, agent_name, capabilities, pid=None):
        """Register an agent in the unified system"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO agent_registry 
                     (agent_name, status, last_seen, capabilities, pid)
                     VALUES (?, 'active', ?, ?, ?)''',
                  (agent_name, datetime.now().isoformat(), 
                   ','.join(capabilities), pid))
        conn.commit()
        conn.close()
        print(f"✅ Registered: {agent_name}")
    
    def route_to_agent(self, query):
        """Route query to the most appropriate agent"""
        query_lower = query.lower()
        
        # Legal/court queries
        if any(word in query_lower for word in ['court', 'law', 'legal', 'attorney', 
                                                  'judge', 'supreme', 'federal', 'case',
                                                  'texas', 'california', 'citation']):
            return "agentforlaw"
        
        # Medical/health queries
        if any(word in query_lower for word in ['medical', 'health', 'doctor', 'patient',
                                                  'diagnosis', 'symptom', 'disease']):
            return "mediclaw"
        
        # Math/calculation queries
        if any(word in query_lower for word in ['calculate', 'math', 'equation', 'solve',
                                                  'sum', 'average', 'statistic']):
            return "mathematicaclaw"
        
        # Translation queries
        if any(word in query_lower for word in ['translate', 'spanish', 'french', 'german']):
            return "polyclaw"
        
        # Document queries
        if any(word in query_lower for word in ['document', 'pdf', 'contract', 'motion',
                                                  'brief', 'complaint']):
            return "docuclaw"
        
        # Data queries
        if any(word in query_lower for word in ['data', 'database', 'query', 'sql']):
            return "dataclaw"
        
        # Default to agentforlaw
        return "agentforlaw"
    
    def search_shared_memory(self, query):
        """Search ALL shared memory across agents"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        try:
            c.execute('''SELECT query, response, agent_source, timestamp 
                         FROM unified_knowledge 
                         WHERE query LIKE ? 
                         ORDER BY confidence DESC, usage_count DESC 
                         LIMIT 1''', (f'%{query}%',))
            row = c.fetchone()
            if row:
                return {"found": True, "query": row[0], "response": row[1], 
                        "source": row[2], "timestamp": row[3]}
        except:
            pass
        finally:
            conn.close()
        
        return {"found": False}
    
    def save_to_shared_memory(self, query, response, agent_source, confidence=0.8):
        """Save knowledge so ALL agents can learn"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        try:
            c.execute('''INSERT OR REPLACE INTO unified_knowledge 
                         (query, response, agent_source, timestamp, confidence, usage_count)
                         VALUES (?, ?, ?, ?, ?, 
                                 COALESCE((SELECT usage_count + 1 FROM unified_knowledge WHERE query = ?), 1))''',
                      (query.lower(), response[:1000], agent_source, 
                       datetime.now().isoformat(), confidence, query.lower()))
            conn.commit()
            print(f"📚 Knowledge saved from {agent_source}: {query[:50]}...")
        except Exception as e:
            print(f"Error saving: {e}")
        finally:
            conn.close()
    
    def broadcast_to_agents(self, message, source_agent):
        """Broadcast a message to all registered agents"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        # Get all active agents except source
        c.execute('SELECT agent_name FROM agent_registry WHERE status = "active" AND agent_name != ?', (source_agent,))
        agents = c.fetchall()
        
        for (agent_name,) in agents:
            c.execute('''INSERT INTO agent_messages (from_agent, to_agent, message, timestamp)
                         VALUES (?, ?, ?, ?)''',
                      (source_agent, agent_name, message, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        print(f"📡 Broadcast from {source_agent} to {len(agents)} agents")
    
    def show_stats(self):
        """Show unified system statistics"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        print("\n" + "="*70)
        print("📊 UNIFIED CLAWPACK SYSTEM STATISTICS")
        print("="*70)
        
        # Knowledge count
        c.execute('SELECT COUNT(*) FROM unified_knowledge')
        count = c.fetchone()[0]
        print(f"\n📚 Total knowledge entries: {count}")
        
        # Knowledge by agent
        c.execute('''SELECT agent_source, COUNT(*) FROM unified_knowledge 
                     GROUP BY agent_source ORDER BY COUNT(*) DESC''')
        print("\n📖 Knowledge by agent:")
        for row in c.fetchall():
            print(f"   • {row[0]}: {row[1]} entries")
        
        # Active agents
        c.execute('SELECT agent_name, last_seen FROM agent_registry WHERE status = "active"')
        agents = c.fetchall()
        print(f"\n🤖 Active agents: {len(agents)}")
        for agent in agents:
            print(f"   • {agent[0]}")
        
        # Pending messages
        c.execute('SELECT COUNT(*) FROM agent_messages WHERE status = "pending"')
        pending = c.fetchone()[0]
        print(f"\n💬 Pending cross-agent messages: {pending}")
        
        conn.close()
    
    def run_interactive(self):
        """Run the unified controller interactively"""
        print("\n" + "="*70)
        print("🤖 UNIFIED CLAWPACK CONTROLLER - The Brain")
        print("="*70)
        print("ALL 19 AGENTS SHARE MEMORY AND LEARN TOGETHER")
        print("="*70)
        print("\nCOMMANDS:")
        print("  /ask [question]     - Ask any question (routes to best agent)")
        print("  /stats              - Show unified system statistics")
        print("  /agents             - List all registered agents")
        print("  /broadcast [msg]    - Broadcast to all agents")
        print("  /help, /quit")
        print("="*70)
        
        while True:
            try:
                cmd = input("\n🧠 Unified> ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye! All agents remember what we learned.")
                    break
                elif cmd == "/help":
                    continue
                elif cmd == "/stats":
                    self.show_stats()
                elif cmd == "/agents":
                    conn = sqlite3.connect(str(SHARED_DB))
                    c = conn.cursor()
                    c.execute('SELECT agent_name, capabilities, last_seen FROM agent_registry')
                    print("\n🤖 REGISTERED AGENTS:")
                    for row in c.fetchall():
                        print(f"   • {row[0]} - {row[1][:50]}...")
                    conn.close()
                elif cmd.startswith("/ask "):
                    question = cmd[5:]
                    self.handle_question(question)
                elif cmd.startswith("/broadcast "):
                    msg = cmd[10:]
                    self.broadcast_to_agents(msg, "unified")
                    print(f"✅ Broadcast sent: {msg}")
                else:
                    self.handle_question(cmd)
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def handle_question(self, question):
        """Handle a question by routing to the appropriate agent"""
        print(f"\n🤔 Question: {question}")
        print("-" * 50)
        
        # First, check shared memory
        cached = self.search_shared_memory(question)
        if cached["found"]:
            print(f"✅ Found in shared memory (learned from {cached['source']}):")
            print(f"\n{cached['response'][:500]}")
            return
        
        # Route to appropriate agent
        target_agent = self.route_to_agent(question)
        print(f"🎯 Routing to: {target_agent}")
        print(f"\n💡 To get this answer, start the {target_agent} agent:")
        print(f"\n   cd C:\\Users\\greg\\dev\\clawpack")
        print(f"   python agents/{target_agent}/{target_agent}.py")
        print(f"\n   Then ask: {question}")
        print(f"\n   Once answered, the knowledge will be saved to shared memory!")
        
        # Register that this question was asked
        self.save_to_shared_memory(question, f"Question routed to {target_agent}", "unified", 0.5)

if __name__ == "__main__":
    controller = UnifiedController()
    controller.run_interactive()
