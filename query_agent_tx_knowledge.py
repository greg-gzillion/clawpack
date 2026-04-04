#!/usr/bin/env python3
"""Query any agent's TX knowledge"""

import sqlite3
from pathlib import Path

def query_agent(agent_name, topic=None):
    db_path = Path.home() / ".claw_memory" / "shared_memory.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    if topic:
        cursor.execute("""
            SELECT at.agent, at.proficiency, tk.topic, tk.content, tk.source
            FROM agent_training at
            JOIN tx_knowledge tk ON at.topic = tk.topic
            WHERE at.agent = ? AND (tk.topic LIKE ? OR tk.content LIKE ?)
        """, (agent_name, f"%{topic}%", f"%{topic}%"))
    else:
        cursor.execute("""
            SELECT at.agent, at.proficiency, tk.topic, tk.content, tk.source
            FROM agent_training at
            JOIN tx_knowledge tk ON at.topic = tk.topic
            WHERE at.agent = ?
            LIMIT 10
        """, (agent_name,))
    
    results = cursor.fetchall()
    conn.close()
    
    if results:
        print(f"\n🦞 {agent_name.upper()} TX Knowledge:")
        print("=" * 50)
        for agent, prof, topic, content, source in results:
            print(f"\n📖 {topic} (Level {prof}/5)")
            print(f"   {content[:200]}...")
            print(f"   Source: {source}")
    else:
        print(f"No TX knowledge found for {agent_name}")
    
    return results

if __name__ == "__main__":
    import sys
    agent = sys.argv[1] if len(sys.argv) > 1 else "eagleclaw"
    topic = sys.argv[2] if len(sys.argv) > 2 else None
    query_agent(agent, topic)
