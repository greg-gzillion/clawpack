"""Dashboard for language learning progress"""
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

def show_language_dashboard():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("\n" + "="*70)
    print("🌍 CROSS-AGENT LANGUAGE LEARNING DASHBOARD")
    print("="*70)
    
    # Language mastery by agent
    print("\n📚 LANGUAGE MASTERY MATRIX:")
    print("-"*80)
    
    # Get all agents and languages
    cursor.execute("SELECT DISTINCT agent FROM language_proficiency")
    agents = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT language FROM language_proficiency")
    languages = [row[0] for row in cursor.fetchall()]
    
    # Print header
    print(f"{'Agent':<15}", end="")
    for lang in sorted(languages):
        print(f"{lang:<12}", end="")
    print()
    print("-"*80)
    
    # Print each agent's proficiency
    for agent in sorted(agents):
        print(f"{agent:<15}", end="")
        for lang in sorted(languages):
            cursor.execute("""
                SELECT proficiency_level FROM language_proficiency 
                WHERE agent = ? AND language = ?
            """, (agent, lang))
            level = cursor.fetchone()
            if level and level[0] > 0:
                print(f"{'⭐' * level[0]:<12}", end="")
            else:
                print(f"{'⚪':<12}", end="")
        print()
    
    # Teaching assignments
    print("\n🎓 TEACHING ASSIGNMENTS:")
    cursor.execute("""
        SELECT teacher_agent, student_agent, language, completed 
        FROM teaching_assignments WHERE completed = 0
    """)
    assignments = cursor.fetchall()
    if assignments:
        for teacher, student, lang, completed in assignments:
            print(f"   {teacher} → {student}: {lang}")
    else:
        print("   No active teaching assignments")
    
    # Learning goals
    print("\n🎯 LEARNING GOALS:")
    cursor.execute("""
        SELECT agent, goal, target_metric, achieved 
        FROM learning_goals WHERE achieved = 0
    """)
    goals = cursor.fetchall()
    if goals:
        for agent, goal, target, achieved in goals:
            print(f"   {agent}: {goal} (target: {target})")
    else:
        print("   No active learning goals")
    
    conn.close()

if __name__ == "__main__":
    show_language_dashboard()
