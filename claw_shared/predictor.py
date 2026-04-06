"""Predictive intelligence for claw agents"""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

class PredictiveIntelligence:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self._init_predictive_tables()
    
    def _init_predictive_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent TEXT,
                action_type TEXT,
                context TEXT,
                frequency INTEGER DEFAULT 1,
                last_performed TEXT,
                predicted_next TEXT
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_agent TEXT,
                target_agent TEXT,
                recommendation TEXT,
                confidence REAL DEFAULT 0.5,
                times_successful INTEGER DEFAULT 0,
                last_recommended TEXT
            )
        """)
        self.conn.commit()
    
    def record_action(self, agent, action, context=""):
        """Record agent action for pattern learning"""
        self.cursor.execute("""
            INSERT INTO usage_patterns (agent, action_type, context, last_performed)
            VALUES (?, ?, ?, ?)
            ON CONFLICT DO UPDATE SET
                frequency = frequency + 1,
                last_performed = ?
        """, (agent, action, context, datetime.now().isoformat(), datetime.now().isoformat()))
        self.conn.commit()
        
        # Predict next action
        return self.predict_next_action(agent)
    
    def predict_next_action(self, agent):
        """Predict what agent will do next"""
        self.cursor.execute("""
            SELECT action_type, frequency FROM usage_patterns 
            WHERE agent = ? 
            ORDER BY frequency DESC LIMIT 3
        """, (agent,))
        predictions = self.cursor.fetchall()
        return [p[0] for p in predictions] if predictions else []
    
    def recommend_agent_collaboration(self, task_type):
        """Recommend which agents should collaborate"""
        # Map task types to agent expertise
        expertise_map = {
            "legal": ["agentforlaw"],
            "coding": ["rustypycraw", "eagleclaw", "claw-coder"],
            "debugging": ["crustyclaw"],
            "law_research": ["agentforlaw"],
            "code_generation": ["rustypycraw"],
            "security_audit": ["crustyclaw"]
        }
        
        return expertise_map.get(task_type, [])
    
    def suggest_improvement(self, agent):
        """Suggest improvements based on past behavior"""
        self.cursor.execute("""
            SELECT action_type, frequency, last_performed
            FROM usage_patterns 
            WHERE agent = ? AND last_performed > datetime('now', '-7 days')
            ORDER BY frequency DESC
        """, (agent,))
        recent_actions = self.cursor.fetchall()
        
        if not recent_actions:
            return "No recent activity to analyze"
        
        most_common = recent_actions[0]
        return f"Agent {agent} performs '{most_common[0]}' most often ({most_common[1]} times). Consider optimizing this action."

print("✅ Predictive intelligence initialized")
