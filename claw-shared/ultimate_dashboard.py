"""Ultimate language learning dashboard with all languages"""
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

def show_ultimate_dashboard():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("\n" + "="*90)
    print("🌍 ULTIMATE LANGUAGE MASTERY DASHBOARD")
    print("="*90)
    
    # Get all languages
    cursor.execute("SELECT DISTINCT language FROM language_proficiency ORDER BY language")
    languages = [row[0] for row in cursor.fetchall()]
    
    # Get all agents
    cursor.execute("SELECT DISTINCT agent FROM language_proficiency ORDER BY agent")
    agents = [row[0] for row in cursor.fetchall()]
    
    # Print header
    print(f"\n{'Agent':<15}", end="")
    for lang in languages:
        print(f"{lang:<12}", end="")
    print()
    print("-"*90)
    
    # Print each agent's proficiency
    for agent in agents:
        print(f"{agent:<15}", end="")
        for lang in languages:
            cursor.execute("SELECT proficiency_level FROM language_proficiency WHERE agent = ? AND language = ?", (agent, lang))
            level = cursor.fetchone()
            if level and level[0] > 0:
                print(f"{'⭐' * level[0]:<12}", end="")
            else:
                print(f"{'⚪':<12}", end="")
        print()
    
    # Statistics
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT language) as total_langs,
            AVG(proficiency_level) as avg_prof,
            SUM(CASE WHEN proficiency_level = 5 THEN 1 ELSE 0 END) as mastered
        FROM language_proficiency
    """)
    total_langs, avg_prof, mastered = cursor.fetchone()
    
    print("\n" + "="*90)
    print("📊 MASTERY STATISTICS:")
    print(f"   Total Languages: {total_langs}")
    print(f"   Average Proficiency: {avg_prof:.2f}/5")
    print(f"   Perfect Masteries: {mastered}")
    print("="*90)
    
    conn.close()

if __name__ == "__main__":
    show_ultimate_dashboard()
