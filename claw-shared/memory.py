"""
Shared Memory Module for All Claw Agents
Location: ~/dev/claw-shared/memory.py
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

SHARED_MEMORY_DIR = Path.home() / ".claw_memory"
SHARED_MEMORY_DIR.mkdir(exist_ok=True)
DB_PATH = SHARED_MEMORY_DIR / "shared_memory.db"

class ClawMemory:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self._init_tables()
    
    def _init_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent TEXT,
            key TEXT,
            value TEXT,
            timestamp TEXT,
            tags TEXT
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS agent_registry (
            agent_id TEXT PRIMARY KEY,
            name TEXT,
            repo TEXT,
            capabilities TEXT,
            last_seen TEXT
        )''')
        self.conn.commit()
    
    def register(self, capabilities: str, repo: str = ""):
        self.cursor.execute(
            "INSERT OR REPLACE INTO agent_registry VALUES (?, ?, ?, ?, ?)",
            (self.agent_name, self.agent_name, repo, capabilities, datetime.now().isoformat())
        )
        self.conn.commit()
    
    def remember(self, key: str, value: str, tags: str = ""):
        self.cursor.execute(
            "INSERT INTO memories (agent, key, value, timestamp, tags) VALUES (?, ?, ?, ?, ?)",
            (self.agent_name, key, value, datetime.now().isoformat(), tags)
        )
        self.conn.commit()
        return True
    
    def recall(self, key: str) -> list:
        self.cursor.execute(
            "SELECT agent, key, value, tags FROM memories WHERE key LIKE ? ORDER BY timestamp DESC LIMIT 10",
            (f"%{key}%",)
        )
        return self.cursor.fetchall()
    
    def get_agents(self) -> list:
        self.cursor.execute("SELECT name, capabilities FROM agent_registry")
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()

# Singleton for each agent
_instances = {}

def get_memory(agent_name: str) -> ClawMemory:
    if agent_name not in _instances:
        _instances[agent_name] = ClawMemory(agent_name)
    return _instances[agent_name]
