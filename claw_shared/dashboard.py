#!/usr/bin/env python3
"""Learning dashboard for claw agents"""
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

def show_dashboard():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print("🦞 CLAW AGENT LEARNING DASHBOARD")
    print("="*50)
    
    # Agent activity
    cursor.execute("SELECT agent, COUNT(*) FROM memories GROUP BY agent ORDER BY COUNT(*) DESC")
    print("\n📊 AGENT ACTIVITY:")
    for agent, count in cursor.fetchall():
        print(f"   {agent}: {count} memories")
    
    # Patterns discovered
    cursor.execute("SELECT pattern_type, confidence, occurrences FROM neural_patterns ORDER BY confidence DESC")
    print("\n🧠 PATTERNS DISCOVERED:")
    for ptype, conf, occ in cursor.fetchall():
        print(f"   {ptype}: {conf:.0%} confidence ({occ} occurrences)")
    
    # Collaboration suggestions
    cursor.execute("SELECT source_agent, target_agent, confidence FROM agent_recommendations ORDER BY confidence DESC LIMIT 5")
    print("\n🤝 TOP COLLABORATIONS:")
    for src, tgt, conf in cursor.fetchall():
        print(f"   {src} → {tgt}: {conf:.0%} confidence")
    
    # Active learning cycle
    cursor.execute("SELECT COUNT(*) FROM memories WHERE timestamp > datetime('now', '-1 hour')")
    recent = cursor.fetchone()[0]
    print(f"\n⏱️  Recent activity (last hour): {recent} memories")
    
    conn.close()

if __name__ == "__main__":
    show_dashboard()
