"""Cross-agent learning and knowledge transfer"""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

class CrossAgentLearner:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self._init_cross_tables()
    
    def _init_cross_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_agent TEXT,
                to_agent TEXT,
                knowledge_type TEXT,
                knowledge_content TEXT,
                transfer_time TEXT,
                success BOOLEAN DEFAULT NULL,
                feedback TEXT
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_lessons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                lesson TEXT,
                lesson_type TEXT,
                timestamp TEXT,
                applied_count INTEGER DEFAULT 0,
                effectiveness REAL DEFAULT 0.5
            )
        """)
        self.conn.commit()
    
    def transfer_knowledge(self, from_agent, to_agent, knowledge_type, content):
        """Transfer knowledge from one agent to another"""
        self.cursor.execute("""
            INSERT INTO knowledge_transfers (from_agent, to_agent, knowledge_type, knowledge_content, transfer_time)
            VALUES (?, ?, ?, ?, ?)
        """, (from_agent, to_agent, knowledge_type, content, datetime.now().isoformat()))
        self.conn.commit()
        
        # Also store as lesson for receiving agent
        self.add_lesson(to_agent, content, knowledge_type)
        return self.cursor.lastrowid
    
    def add_lesson(self, agent, lesson, lesson_type):
        """Store a lesson learned by an agent"""
        self.cursor.execute("""
            INSERT INTO agent_lessons (agent, lesson, lesson_type, timestamp)
            VALUES (?, ?, ?, ?)
        """, (agent, lesson, lesson_type, datetime.now().isoformat()))
        self.conn.commit()
    
    def apply_lesson(self, lesson_id, success):
        """Mark a lesson as applied with success/failure"""
        effectiveness = 0.7 if success else 0.3
        self.cursor.execute("""
            UPDATE agent_lessons 
            SET applied_count = applied_count + 1,
                effectiveness = (effectiveness * applied_count + ?) / (applied_count + 1)
            WHERE id = ?
        """, (effectiveness, lesson_id))
        self.conn.commit()
    
    def get_best_practices(self, agent, limit=5):
        """Retrieve best practices learned by agent"""
        self.cursor.execute("""
            SELECT lesson, effectiveness, applied_count
            FROM agent_lessons 
            WHERE agent = ? AND effectiveness > 0.7
            ORDER BY effectiveness DESC, applied_count DESC
            LIMIT ?
        """, (agent, limit))
        return self.cursor.fetchall()
    
    def broadcast_lesson(self, lesson, from_agent, to_agents=None):
        """Broadcast a lesson to multiple agents"""
        if to_agents is None:
            self.cursor.execute("SELECT agent_id FROM agent_registry")
            to_agents = [row[0] for row in self.cursor.fetchall()]
        
        results = []
        for agent in to_agents:
            if agent != from_agent:
                transfer_id = self.transfer_knowledge(from_agent, agent, "broadcast_lesson", lesson)
                results.append(transfer_id)
        
        return results

print("✅ Cross-agent learning initialized")
