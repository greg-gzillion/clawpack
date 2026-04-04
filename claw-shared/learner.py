"""Simple learning system for claw agents"""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

class LearningSystem:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self._init_learning_tables()
    
    def _init_learning_tables(self):
        # Track how often each memory is used
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_usage (
                memory_id INTEGER,
                agent TEXT,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                usefulness_score REAL DEFAULT 0.5,
                FOREIGN KEY(memory_id) REFERENCES memories(id)
            )
        """)
        # Track agent performance
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_performance (
                agent TEXT PRIMARY KEY,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                last_active TEXT,
                avg_response_time REAL DEFAULT 0
            )
        """)
        self.conn.commit()
    
    def record_usage(self, memory_id, agent, success=False):
        """Record when an agent uses a memory"""
        now = datetime.now().isoformat()
        self.cursor.execute("""
            INSERT INTO memory_usage (memory_id, agent, access_count, last_accessed, usefulness_score)
            VALUES (?, ?, 1, ?, ?)
            ON CONFLICT DO UPDATE SET
                access_count = access_count + 1,
                last_accessed = ?,
                usefulness_score = usefulness_score + (0.1 if success else -0.05)
        """, (memory_id, agent, now, 0.5 if success else 0.45, now))
        self.conn.commit()
    
    def get_top_memories(self, limit=5):
        """Get most useful memories"""
        self.cursor.execute("""
            SELECT m.key, m.value, mu.usefulness_score, mu.access_count
            FROM memories m
            JOIN memory_usage mu ON m.id = mu.memory_id
            ORDER BY mu.usefulness_score DESC, mu.access_count DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()
    
    def record_outcome(self, agent, success):
        """Track agent success/failure"""
        now = datetime.now().isoformat()
        if success:
            self.cursor.execute("""
                INSERT INTO agent_performance (agent, success_count, last_active)
                VALUES (?, 1, ?)
                ON CONFLICT DO UPDATE SET
                    success_count = success_count + 1,
                    last_active = ?
            """, (agent, now, now))
        else:
            self.cursor.execute("""
                INSERT INTO agent_performance (agent, failure_count, last_active)
                VALUES (?, 1, ?)
                ON CONFLICT DO UPDATE SET
                    failure_count = failure_count + 1,
                    last_active = ?
            """, (agent, now, now))
        self.conn.commit()
        return self.get_agent_score(agent)
    
    def get_agent_score(self, agent):
        """Calculate agent reliability score"""
        self.cursor.execute("""
            SELECT success_count, failure_count FROM agent_performance WHERE agent = ?
        """, (agent,))
        row = self.cursor.fetchone()
        if not row:
            return 0.5
        total = row[0] + row[1]
        return row[0] / total if total > 0 else 0.5

# Example usage
if __name__ == "__main__":
    ls = LearningSystem()
    print("✅ Learning system initialized")
