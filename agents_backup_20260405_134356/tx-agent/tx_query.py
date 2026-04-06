#!/usr/bin/env python3
"""Query TX knowledge from any agent"""

import sqlite3
from pathlib import Path

def query_tx(topic=None):
    db_path = Path.home() / ".claw_memory" / "shared_memory.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    if topic:
        cursor.execute("""
            SELECT topic, content, source FROM tx_knowledge 
            WHERE topic LIKE ? OR content LIKE ?
            LIMIT 5
        """, (f"%{topic}%", f"%{topic}%"))
    else:
        cursor.execute("SELECT topic, content, source FROM tx_knowledge LIMIT 10")
    
    results = cursor.fetchall()
    conn.close()
    
    for topic, content, source in results:
        print(f"\n📖 {topic}")
        print(f"   {content[:300]}...")
        print(f"   Source: {source}")
    
    return results

if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    query_tx(topic)
