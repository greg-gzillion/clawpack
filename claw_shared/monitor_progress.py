"""Monitor progress toward Level 5 mastery"""
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

def show_progress():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("🎯 PROGRESS TO LEVEL 5 MASTERY")
    print("="*80)
    
    # Get all languages
    cursor.execute("SELECT DISTINCT language FROM language_proficiency")
    languages = [row[0] for row in cursor.fetchall()]
    
    agents = ["agentforlaw", "claw-code", "claw-coder", "crustyclaw", "eagleclaw", "rustypycraw"]
    
    # Level distribution
    levels = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for agent in agents:
        for lang in languages:
            cursor.execute("SELECT proficiency_level FROM language_proficiency WHERE agent = ? AND language = ?", (agent, lang))
            level = cursor.fetchone()
            if level:
                levels[level[0]] = levels.get(level[0], 0) + 1
    
    print("\n📊 LEVEL DISTRIBUTION:")
    print(f"   Level 5 (Master): {'█' * (levels[5] // 2)} {levels[5]} proficiencies")
    print(f"   Level 4: {'█' * (levels[4] // 2)} {levels[4]} proficiencies")
    print(f"   Level 3: {'█' * (levels[3] // 2)} {levels[3]} proficiencies")
    print(f"   Level 2: {'█' * (levels[2] // 2)} {levels[2]} proficiencies")
    print(f"   Level 1: {'█' * (levels[1] // 2)} {levels[1]} proficiencies")
    
    # Find bottlenecks
    print("\n🔍 BOTTLENECKS (Languages below Level 3):")
    for lang in languages:
        low_agents = []
        for agent in agents:
            cursor.execute("SELECT proficiency_level FROM language_proficiency WHERE agent = ? AND language = ?", (agent, lang))
            level = cursor.fetchone()
            if level and level[0] < 3:
                low_agents.append(agent)
        if low_agents:
            print(f"   {lang}: {len(low_agents)} agents struggling - {', '.join(low_agents[:3])}")
    
    # Time to completion estimate
    total_needed = sum(5 - level[0] for agent in agents for lang in languages 
                       if (level := cursor.execute("SELECT proficiency_level FROM language_proficiency WHERE agent = ? AND language = ?", (agent, lang)).fetchone()))
    
    print(f"\n⏱️  Estimated learning cycles to Level 5: {total_needed // 10} cycles")
    
    conn.close()

if __name__ == "__main__":
    show_progress()
