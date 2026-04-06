"""Shared memory handling for Mathematicaclaw"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional

class SharedMemory:
    def __init__(self):
        self.shared_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.init_tables()
    
    def init_tables(self):
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS math_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT UNIQUE,
                result TEXT,
                operation_type TEXT,
                variables TEXT,
                timestamp TEXT,
                source_agent TEXT,
                usage_count INTEGER DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()
    
    def read(self, expression: str, operation: str) -> Optional[str]:
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT result FROM math_knowledge WHERE expression = ? AND operation_type = ?",
            (expression, operation)
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            print(f"📚 [FROM SHARED MEMORY]")
            return result[0]
        return None
    
    def write(self, expression: str, result: str, operation: str, variables: str = None, agent: str = "Mathematicaclaw"):
        conn = sqlite3.connect(str(self.shared_path))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO math_knowledge 
            (expression, result, operation_type, variables, timestamp, source_agent)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (expression, result, operation, variables, datetime.now().isoformat(), agent))
        conn.commit()
        conn.close()
        print("💡 [Saved to shared memory]")