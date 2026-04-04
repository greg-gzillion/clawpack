"""
Shared memory system across all agents (rustypycraw, eagleclaw, crustyclaw, claw-coder)
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path

SHARED_MEMORY_DIR = Path.home() / ".claw_memory"
SHARED_MEMORY_DIR.mkdir(exist_ok=True)

DB_PATH = SHARED_MEMORY_DIR / "shared_memory.db"

class SharedMemory:
    """Cross-agent shared memory system"""
    
    def __init__(self):
        self._init_db()
    
    def _init_db(self):
        """Initialize shared database"""
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                key TEXT,
                value TEXT,
                timestamp TEXT,
                tags TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_registry (
                agent_id TEXT PRIMARY KEY,
                name TEXT,
                repo TEXT,
                capabilities TEXT,
                last_seen TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                question TEXT,
                answer TEXT,
                timestamp TEXT,
                session_id TEXT
            )
        ''')
        
        self.conn.commit()
    
    def remember(self, agent: str, key: str, value: str, tags: str = ""):
        """Store a memory accessible by all agents"""
        self.cursor.execute(
            "INSERT INTO memories (agent, key, value, timestamp, tags) VALUES (?, ?, ?, ?, ?)",
            (agent, key, value, datetime.now().isoformat(), tags)
        )
        self.conn.commit()
    
    def recall(self, key: str) -> list:
        """Retrieve memories by key (any agent)"""
        self.cursor.execute(
            "SELECT agent, key, value, tags FROM memories WHERE key LIKE ? ORDER BY timestamp DESC LIMIT 10",
            (f"%{key}%",)
        )
        return self.cursor.fetchall()
    
    def register_agent(self, agent_id: str, name: str, repo: str, capabilities: str):
        """Register an agent in the shared registry"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO agent_registry VALUES (?, ?, ?, ?, ?)",
            (agent_id, name, repo, capabilities, datetime.now().isoformat())
        )
        self.conn.commit()
    
    def get_all_agents(self) -> list:
        """Get all registered agents"""
        self.cursor.execute("SELECT name, repo, capabilities FROM agent_registry")
        return self.cursor.fetchall()
    
    def log_conversation(self, agent: str, question: str, answer: str, session_id: str = ""):
        """Log conversation for cross-agent learning"""
        self.cursor.execute(
            "INSERT INTO conversations (agent, question, answer, timestamp, session_id) VALUES (?, ?, ?, ?, ?)",
            (agent, question, answer[:500], datetime.now().isoformat(), session_id)
        )
        self.conn.commit()
    
    def search_conversations(self, query: str) -> list:
        """Search past conversations across all agents"""
        self.cursor.execute(
            "SELECT agent, question, answer FROM conversations WHERE question LIKE ? OR answer LIKE ? ORDER BY timestamp DESC LIMIT 10",
            (f"%{query}%", f"%{query}%")
        )
        return self.cursor.fetchall()
    
    def get_stats(self) -> dict:
        """Get shared memory statistics"""
        self.cursor.execute("SELECT COUNT(*) FROM memories")
        memories_count = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM conversations")
        conversations_count = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM agent_registry")
        agents_count = self.cursor.fetchone()[0]
        
        return {
            "memories": memories_count,
            "conversations": conversations_count,
            "agents": agents_count
        }
    
    def close(self):
        """Close database connection"""
        self.conn.close()

    def auto_extract_memories(self, agent: str, question: str, answer: str):
        """Automatically extract and store key information from conversations"""
        import re
        
        # Look for percentage patterns (e.g., "10% collateral")
        percent_pattern = r'(\d+(?:\.\d+)?)%\s+(\w+)'
        matches = re.findall(percent_pattern, answer)
        for percent, subject in matches:
            self.remember(agent, f"{subject}_percentage", f"{percent}%")
        
        # Look for fee patterns
        fee_pattern = r'fee\s+is\s+(\d+(?:\.\d+)?)%'
        matches = re.findall(fee_pattern, answer, re.IGNORECASE)
        for fee in matches:
            self.remember(agent, "fee_percentage", f"{fee}%")
        
        # Look for time periods (inspection hours)
        time_pattern = r'(\d+)\s+hours?\s+inspection'
        matches = re.findall(time_pattern, answer, re.IGNORECASE)
        for hours in matches:
            self.remember(agent, "inspection_hours", hours)

    def find_agent_for_task(self, task: str) -> list:
        """Find which agent is best suited for a task"""
        self.cursor.execute(
            "SELECT name, capabilities FROM agent_registry WHERE capabilities LIKE ?",
            (f"%{task}%",)
        )
        return self.cursor.fetchall()
    
    def route_question(self, question: str) -> str:
        """Route question to the most appropriate agent"""
        agents = self.find_agent_for_task(question)
        if agents:
            return f"Recommended agent: {agents[0][0]} - {agents[0][1][:100]}"
        return "No specific agent recommendation"

    def cleanup_old_memories(self, days: int = 30):
        """Remove memories older than specified days"""
        import datetime
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
        self.cursor.execute("DELETE FROM memories WHERE timestamp < ?", (cutoff,))
        self.conn.commit()
        return self.cursor.rowcount
    
    def get_memory_age(self, key: str) -> str:
        """Get age of a specific memory"""
        self.cursor.execute(
            "SELECT timestamp FROM memories WHERE key = ? ORDER BY timestamp DESC LIMIT 1",
            (key,)
        )
        result = self.cursor.fetchone()
        if result:
            return f"Memory age: {result[0]}"
        return "Memory not found"

    def summarize_conversations(self, agent: str = None, limit: int = 100):
        """Get summary of recent conversations"""
        if agent:
            self.cursor.execute(
                "SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM conversations WHERE agent = ?",
                (agent,)
            )
        else:
            self.cursor.execute("SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM conversations")
        
        result = self.cursor.fetchone()
        return {
            "total_conversations": result[0],
            "first_conversation": result[1],
            "last_conversation": result[2]
        }
