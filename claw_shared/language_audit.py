"""Audit language capabilities of each agent"""
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

# Define language proficiency levels
LANGUAGE_LEVELS = {
    1: "Basic syntax",
    2: "Functions & patterns",
    3: "Advanced features",
    4: "Expert optimization",
    5: "Mastery"
}

# Map agents to their current languages (from our earlier scan)
AGENT_LANGUAGES = {
    "rustypycraw": {
        "Rust": 5, "Python": 5, "TypeScript": 4, "Solidity": 4,
        "Go": 3, "JavaScript": 3, "C++": 2
    },
    "eagleclaw": {
        "Rust": 4, "Python": 4, "TypeScript": 3, "Go": 2
    },
    "agentforlaw": {
        "Python": 4, "JavaScript": 2, "TypeScript": 2
    },
    "crustyclaw": {
        "Rust": 5, "Python": 3
    },
    "claw-coder": {
        "Python": 5, "JavaScript": 3, "TypeScript": 3
    },
    "claw-code": {
        "TypeScript": 4, "Python": 3, "Rust": 3
    }
}

def audit_languages():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # Create language learning table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS language_proficiency (
            agent TEXT,
            language TEXT,
            proficiency_level INTEGER DEFAULT 1,
            last_practiced TEXT,
            source TEXT,
            UNIQUE(agent, language)
        )
    """)
    
    # Populate with known languages
    for agent, languages in AGENT_LANGUAGES.items():
        for lang, level in languages.items():
            cursor.execute("""
                INSERT OR REPLACE INTO language_proficiency (agent, language, proficiency_level, source)
                VALUES (?, ?, ?, ?)
            """, (agent, lang, level, "initial_audit"))
    
    conn.commit()
    
    # Show current state
    print("\n" + "="*60)
    print("📊 CURRENT LANGUAGE PROFICIENCY BY AGENT")
    print("="*60)
    
    for agent in AGENT_LANGUAGES.keys():
        print(f"\n🦞 {agent.upper()}:")
        cursor.execute("SELECT language, proficiency_level FROM language_proficiency WHERE agent = ? ORDER BY proficiency_level DESC", (agent,))
        for lang, level in cursor.fetchall():
            print(f"   {lang}: {'⭐' * level} ({LANGUAGE_LEVELS.get(level, 'Learning')})")
    
    conn.close()

if __name__ == "__main__":
    audit_languages()
