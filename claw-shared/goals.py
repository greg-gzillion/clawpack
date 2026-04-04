"""Set learning goals for agents"""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

def set_goal(agent, goal, target_metric):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_goals (
            agent TEXT,
            goal TEXT,
            target_metric REAL,
            current_value REAL DEFAULT 0,
            start_time TEXT,
            achieved BOOLEAN DEFAULT 0
        )
    """)
    
    cursor.execute("""
        INSERT INTO learning_goals (agent, goal, target_metric, start_time)
        VALUES (?, ?, ?, ?)
    """, (agent, goal, target_metric, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    print(f"✅ Goal set for {agent}: {goal} (target: {target_metric})")

# Set goals for your agents
set_goal("eagleclaw", "Improve code generation accuracy", 0.85)
set_goal("crustyclaw", "Detect 90% of common bugs", 0.90)
set_goal("agentforlaw", "Complete legal research in under 2 seconds", 2.0)

print("🎯 Learning goals established!")
