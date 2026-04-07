import sqlite3
from pathlib import Path

db = Path.home() / ".claw_memory" / "shared_memory.db"
print(f"DB Path: {db}")
print(f"Exists: {db.exists()}")

if db.exists():
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    
    # Get all tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print(f"\n📊 TABLES FOUND: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
        
        # Count rows in each table
        try:
            c.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = c.fetchone()[0]
            print(f"    Rows: {count}")
        except:
            pass
    
    # Check for cross_agent_knowledge specifically
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cross_agent_knowledge'")
    if c.fetchone():
        c.execute("SELECT query, agent_source, timestamp FROM cross_agent_knowledge ORDER BY timestamp DESC LIMIT 5")
        print("\n📚 RECENT KNOWLEDGE:")
        for row in c.fetchall():
            print(f"  - {row[0][:50]}... (from {row[1]})")
    else:
        print("\n❌ No cross_agent_knowledge table yet - agents not sharing!")
    
    conn.close()
else:
    print("\n❌ Shared memory database doesn't exist!")
    print("   Agents need to create it by saving knowledge first.")
