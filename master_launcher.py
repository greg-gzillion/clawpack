#!/usr/bin/env python3
"""
CLAWPACK MASTER LAUNCHER - Starts ALL Agents with Shared Memory
All agents run in background and share knowledge
"""

import subprocess
import sys
import time
import sqlite3
import threading
import os
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack")
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

# Agents that can run in background
AGENTS_TO_START = [
    "agentforlaw",
    "webclaw", 
    "docuclaw",
    "mediclaw",
    "polyclaw",
    "mathematicaclaw"
]

class MasterLauncher:
    def __init__(self):
        self.processes = {}
        self.init_master_memory()
        
    def init_master_memory(self):
        """Initialize master shared memory tables"""
        SHARED_DB.parent.mkdir(exist_ok=True)
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        # Master table for all cross-agent knowledge
        c.execute('''CREATE TABLE IF NOT EXISTS master_knowledge
                     (id INTEGER PRIMARY KEY, query TEXT UNIQUE,
                      response TEXT, agent_source TEXT, 
                      timestamp TEXT, category TEXT,
                      confidence REAL DEFAULT 0.8)''')
        
        # Active agents table
        c.execute('''CREATE TABLE IF NOT EXISTS active_agents
                     (agent_name TEXT PRIMARY KEY, 
                      pid INTEGER, status TEXT,
                      last_heartbeat TEXT,
                      port INTEGER)''')
        
        # Message bus for inter-agent communication
        c.execute('''CREATE TABLE IF NOT EXISTS message_bus
                     (id INTEGER PRIMARY KEY, 
                      from_agent TEXT, to_agent TEXT,
                      message TEXT, timestamp TEXT,
                      delivered INTEGER DEFAULT 0)''')
        
        conn.commit()
        conn.close()
        print("✅ Master shared memory initialized")
    
    def start_agent(self, agent_name):
        """Start an agent in background"""
        agent_path = ROOT_DIR / "agents" / agent_name
        
        # Check for main file
        main_file = agent_path / f"{agent_name}.py"
        shared_file = agent_path / f"{agent_name}_shared.py"
        
        if main_file.exists():
            cmd = [sys.executable, str(main_file)]
        elif shared_file.exists():
            cmd = [sys.executable, str(shared_file)]
        else:
            print(f"❌ Cannot start {agent_name}: no main file")
            return None
        
        try:
            # Start process
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(agent_path)
            )
            
            # Register in database
            conn = sqlite3.connect(str(SHARED_DB))
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO active_agents 
                         (agent_name, pid, status, last_heartbeat, port)
                         VALUES (?, ?, 'running', ?, 0)''',
                      (agent_name, proc.pid, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            print(f"✅ Started {agent_name} (PID: {proc.pid})")
            return proc
            
        except Exception as e:
            print(f"❌ Failed to start {agent_name}: {e}")
            return None
    
    def start_all(self):
        """Start all configured agents"""
        print("\n" + "="*70)
        print("🚀 CLAWPACK MASTER LAUNCHER")
        print("="*70)
        print(f"Starting {len(AGENTS_TO_START)} agents...\n")
        
        for agent in AGENTS_TO_START:
            proc = self.start_agent(agent)
            if proc:
                self.processes[agent] = proc
            time.sleep(2)  # Stagger startup
        
        print(f"\n✅ Started {len(self.processes)}/{len(AGENTS_TO_START)} agents")
        self.show_status()
    
    def show_status(self):
        """Show status of all agents"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        print("\n" + "="*70)
        print("📊 AGENT STATUS")
        print("="*70)
        
        c.execute('SELECT agent_name, pid, status, last_heartbeat FROM active_agents')
        for row in c.fetchall():
            print(f"  • {row[0]}: {row[2]} (PID: {row[1]})")
        
        conn.close()
    
    def broadcast_message(self, from_agent, message):
        """Broadcast a message to all agents"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        c.execute('SELECT agent_name FROM active_agents WHERE agent_name != ?', (from_agent,))
        agents = c.fetchall()
        
        for (agent_name,) in agents:
            c.execute('''INSERT INTO message_bus (from_agent, to_agent, message, timestamp)
                         VALUES (?, ?, ?, ?)''',
                      (from_agent, agent_name, message, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        print(f"📡 Broadcast from {from_agent} to {len(agents)} agents")
    
    def run_interactive(self):
        """Run interactive command center"""
        print("\n" + "="*70)
        print("🎮 CLAWPACK COMMAND CENTER")
        print("="*70)
        print("\nCOMMANDS:")
        print("  /status           - Show agent status")
        print("  /broadcast [msg]  - Send message to all agents")
        print("  /query [question] - Query shared memory")
        print("  /stats            - Show shared memory stats")
        print("  /stop             - Stop all agents")
        print("  /help, /quit")
        print("="*70)
        
        while True:
            try:
                cmd = input("\n🎮 Master> ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    self.stop_all()
                    break
                elif cmd == "/status":
                    self.show_status()
                elif cmd == "/stats":
                    self.show_stats()
                elif cmd.startswith("/broadcast "):
                    self.broadcast_message("master", cmd[10:])
                elif cmd.startswith("/query "):
                    self.query_memory(cmd[7:])
                elif cmd == "/stop":
                    self.stop_all()
                    break
                elif cmd == "/help":
                    continue
                else:
                    # Treat as query to shared memory
                    self.query_memory(cmd)
                    
            except KeyboardInterrupt:
                print("\nStopping...")
                self.stop_all()
                break
    
    def show_stats(self):
        """Show shared memory statistics"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        print("\n" + "="*70)
        print("📊 SHARED MEMORY STATISTICS")
        print("="*70)
        
        c.execute('SELECT COUNT(*) FROM master_knowledge')
        count = c.fetchone()[0]
        print(f"\n📚 Total knowledge entries: {count}")
        
        c.execute('''SELECT agent_source, COUNT(*) FROM master_knowledge 
                     GROUP BY agent_source''')
        print("\n📖 Knowledge by agent:")
        for row in c.fetchall():
            print(f"   • {row[0]}: {row[1]} entries")
        
        c.execute('SELECT COUNT(*) FROM message_bus WHERE delivered = 0')
        pending = c.fetchone()[0]
        print(f"\n💬 Pending messages: {pending}")
        
        conn.close()
    
    def query_memory(self, question):
        """Query shared memory for answers"""
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        c.execute('''SELECT response, agent_source, timestamp, confidence 
                     FROM master_knowledge 
                     WHERE query LIKE ? 
                     ORDER BY confidence DESC 
                     LIMIT 1''', (f'%{question}%',))
        
        row = c.fetchone()
        if row:
            print(f"\n✅ Found in shared memory (from {row[1]}, confidence: {row[3]}):")
            print("-" * 50)
            print(row[0][:500])
        else:
            print(f"\n❌ No answer found in shared memory for: {question}")
            print("\n💡 Try starting agentforlaw and searching there first:")
            print("   python agents/agentforlaw/agentforlaw.py")
            print(f"   Then: /search {question}")
        
        conn.close()
    
    def stop_all(self):
        """Stop all running agents"""
        print("\n🛑 Stopping all agents...")
        for agent_name, proc in self.processes.items():
            try:
                proc.terminate()
                print(f"  • Stopped {agent_name}")
            except:
                pass
        
        # Clear active agents from database
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('DELETE FROM active_agents')
        conn.commit()
        conn.close()
        
        print("\n✅ All agents stopped")
        sys.exit(0)

if __name__ == "__main__":
    launcher = MasterLauncher()
    
    # Parse command line
    if len(sys.argv) > 1 and sys.argv[1] == "--start-all":
        launcher.start_all()
        launcher.run_interactive()
    else:
        print("\nUsage: python master_launcher.py --start-all")
        print("\nOr run interactive mode:")
        launcher.run_interactive()
