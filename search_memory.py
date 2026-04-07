#!/usr/bin/env python3
"""
UNIFIED SHARED MEMORY QUERY - Search ALL agent knowledge
This allows agents to learn from each other across tables
"""

import sqlite3
from pathlib import Path
from datetime import datetime

SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

# Map of tables to their query/response columns
AGENT_TABLES = {
    'agentforlaw_knowledge': ('query', 'response'),
    'medical_knowledge': ('query', 'response'),
    'math_knowledge': ('query', 'response'),
    'translations': ('source_text', 'translated_text'),
    'unified_knowledge': ('query', 'response'),
    'memories': ('memory_text', 'memory_text'),  # fallback
    'documents': ('title', 'content')
}

def search_all_agents(query_text):
    """Search ALL agent tables for knowledge"""
    results = []
    
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    
    query_lower = query_text.lower()
    
    for table, (query_col, response_col) in AGENT_TABLES.items():
        try:
            # Check if table exists
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not c.fetchone():
                continue
            
            # Search in this table
            c.execute(f"SELECT {query_col}, {response_col} FROM {table} WHERE LOWER({query_col}) LIKE ? LIMIT 5", 
                      (f'%{query_lower}%',))
            
            for row in c.fetchall():
                results.append({
                    'agent': table.replace('_knowledge', '').replace('_', ' ').title(),
                    'query': row[0][:100],
                    'response': row[1][:500],
                    'table': table
                })
        except Exception as e:
            pass
    
    conn.close()
    return results

def show_all_knowledge():
    """Show all knowledge across all agents"""
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    
    print("\n" + "="*70)
    print("📚 ALL AGENT KNOWLEDGE (Shared Memory)")
    print("="*70)
    
    total = 0
    for table, (query_col, response_col) in AGENT_TABLES.items():
        try:
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not c.fetchone():
                continue
            
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            if count > 0:
                print(f"\n📁 {table}: {count} entries")
                total += count
                
                # Show sample
                c.execute(f"SELECT {query_col}, {response_col} FROM {table} LIMIT 3")
                for row in c.fetchall():
                    print(f"   • {row[0][:50]}...")
        except:
            pass
    
    print(f"\n📊 TOTAL: {total} knowledge entries across {len([t for t in AGENT_TABLES if t])} agents")
    print("="*70)
    conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        print(f"\n🔍 Searching ALL agents for: {query}")
        print("-"*50)
        
        results = search_all_agents(query)
        if results:
            for r in results:
                print(f"\n✅ Found in {r['agent']} ({r['table']}):")
                print(f"   Q: {r['query']}")
                print(f"   A: {r['response'][:200]}...")
        else:
            print(f"\n❌ No results found in any agent's memory")
            print("\n💡 Try a different query or run:")
            print("   python agents/agentforlaw/agentforlaw.py")
            print("   Then: /court TX")
    else:
        show_all_knowledge()
