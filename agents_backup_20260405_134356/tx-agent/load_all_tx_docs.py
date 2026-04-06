import sqlite3
import os
from pathlib import Path
from datetime import datetime

db_path = Path.home() / ".claw_memory" / "shared_memory.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Ensure tx_knowledge table exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tx_knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT UNIQUE,
        content TEXT,
        category TEXT,
        source TEXT,
        stored_at TEXT
    )
""")

# Load ALL markdown and text files from TXdocumentation
docs_dir = Path.home() / "dev/TXdocumentation"
loaded = 0
failed = 0

for md_file in docs_dir.rglob("*"):
    if md_file.suffix in ['.md', '.txt', '.rst'] and md_file.is_file():
        try:
            topic = str(md_file.relative_to(docs_dir)).replace('/', '_').replace('.md', '').replace('.txt', '')
            content = md_file.read_text(encoding='utf-8', errors='ignore')[:8000]  # 8k limit
            
            cursor.execute("""
                INSERT OR REPLACE INTO tx_knowledge (topic, content, category, source, stored_at)
                VALUES (?, ?, ?, ?, ?)
            """, (topic, content, "tx_documentation", str(md_file), datetime.now().isoformat()))
            loaded += 1
            print(f"✅ Loaded: {topic[:50]}")
        except Exception as e:
            failed += 1
            print(f"❌ Failed: {md_file.name} - {e}")

print(f"\n📚 Total loaded: {loaded}")
print(f"❌ Failed: {failed}")
conn.commit()
conn.close()
