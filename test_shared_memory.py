import sqlite3
import os
from pathlib import Path

db = Path.home() / ".claw_memory" / "shared_memory.db"
print(f"\n📁 Shared Memory DB: {db}")
print(f"   Exists: {db.exists()}")
print(f"   Size: {db.stat().st_size if db.exists() else 0} bytes\n")

if db.exists():
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    
    print("📊 TABLES AND COUNTS:")
    print("-" * 40)
    
    tables = ['medical_knowledge', 'translations', 'math_knowledge', 'language_vocab', 'agentforlaw_knowledge']
    
    for table in tables:
        try:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            print(f"  {table}: {count} entries")
        except:
            print(f"  {table}: table not found")
    
    print("\n📚 SAMPLE ENTRIES:")
    print("-" * 40)
    
    # Show sample from each table that has data
    for table in ['medical_knowledge', 'translations', 'math_knowledge']:
        try:
            c.execute(f"SELECT query, source_agent FROM {table} LIMIT 2")
            rows = c.fetchall()
            for row in rows:
                print(f"  [{table}] {row[0][:40]}... (from: {row[1]})")
        except:
            pass
    
    conn.close()
