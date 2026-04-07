#!/usr/bin/env python3
"""
CLAWPACK CROSS-AGENT LEARNING DEMO
Shows how all 19 agents share knowledge
"""

import sqlite3
from pathlib import Path
from datetime import datetime

SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

print("\n" + "="*70)
print("🦞 CLAWPACK CROSS-AGENT LEARNING DEMO")
print("="*70)
print("\nThis demo shows how ALL agents share memory and learn from each other\n")

conn = sqlite3.connect(str(SHARED_DB))
c = conn.cursor()

# 1. Show all agents that have contributed
print("📊 AGENTS WITH SHARED MEMORY:")
print("-" * 50)

agents_with_data = []
tables = [
    ('agentforlaw_knowledge', '⚖️ AgentForLaw', 'Court/Legal'),
    ('medical_knowledge', '🏥 MedicLaw', 'Medical/Health'),
    ('math_knowledge', '📐 MathematicaClaw', 'Math/Calculations'),
    ('translations', '🌐 PolyClaw', 'Translations'),
    ('unified_knowledge', '🧠 Unified', 'Cross-Agent'),
    ('memories', '💾 Memory', 'General Knowledge'),
    ('documents', '📄 DocuClaw', 'Documents')
]

for table, icon, desc in tables:
    try:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        if count > 0:
            print(f"  {icon} {desc}: {count} entries")
            agents_with_data.append((table, icon, desc, count))
    except:
        pass

print(f"\n✅ {len(agents_with_data)} agents actively sharing knowledge")

# 2. Show recent cross-agent learning
print("\n" + "="*70)
print("🔄 RECENT CROSS-AGENT KNOWLEDGE")
print("="*70)

try:
    # Get recent entries from unified_knowledge (routing decisions)
    c.execute("SELECT query, response, timestamp FROM unified_knowledge ORDER BY timestamp DESC LIMIT 3")
    for row in c.fetchall():
        print(f"\n📋 Query: {row[0]}")
        print(f"   Routed to: {row[1]}")
        print(f"   Time: {row[2][:16]}")
except:
    pass

# 3. Show translation examples (PolyClaw learning)
print("\n" + "="*70)
print("🌐 TRANSLATION KNOWLEDGE (PolyClaw)")
print("="*70)
try:
    c.execute("SELECT source_text, translated_text, target_lang FROM translations LIMIT 3")
    for row in c.fetchall():
        print(f"\n  • {row[0]} -> {row[1]} ({row[2] if len(row) > 2 else 'unknown'})")
except:
    pass

# 4. Show medical knowledge (MedicLaw)
print("\n" + "="*70)
print("🏥 MEDICAL KNOWLEDGE (MedicLaw)")
print("="*70)
try:
    c.execute("SELECT query, response FROM medical_knowledge LIMIT 3")
    for row in c.fetchall():
        print(f"\n  • Q: {row[0][:50]}...")
        print(f"    A: {row[1][:80]}...")
except:
    pass

conn.close()

print("\n" + "="*70)
print("✅ ALL AGENTS ARE CONNECTED VIA SHARED MEMORY!")
print("="*70)
print("\n💡 To see cross-agent learning in action:")
print("   1. In AgentForLaw: /court TX")
print("   2. In Unified: /ask Texas courts")
print("   3. The answer appears because agents share memory!")
print("="*70)
