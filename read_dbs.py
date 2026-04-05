import sqlite3
import os

# Shared memory DB
shared_db = os.path.expanduser(r'~/.claw_memory/shared_memory.db')
if os.path.exists(shared_db):
    print(f'✅ Found: {shared_db}')
    conn = sqlite3.connect(shared_db)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f'Tables: {[t[0] for t in tables]}')
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f'  {table_name}: {count} rows')
        
        # Show sample if small table
        if count > 0 and count <= 5:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            for row in cursor.fetchall():
                print(f'    Sample: {str(row)[:150]}')
    conn.close()
else:
    print(f'❌ shared_memory.db not found at {shared_db}')

# Medical cache DB
medical_db = os.path.expanduser(r'~/.claw_memory/medical_cache.db')
if os.path.exists(medical_db):
    print(f'\n✅ Found: {medical_db}')
    conn = sqlite3.connect(medical_db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f'Tables: {[t[0] for t in tables]}')
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f'  {table_name}: {count} rows')
    conn.close()
else:
    print(f'❌ medical_cache.db not found at {medical_db}')

# Check for TX knowledge
tx_db = os.path.expanduser(r'~/.claw_memory/tx_knowledge.db')
if os.path.exists(tx_db):
    print(f'\n✅ Found TX knowledge DB')
else:
    print(f'\n❌ tx_knowledge.db not found')
