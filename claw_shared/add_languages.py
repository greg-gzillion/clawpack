"""Add new programming languages to agent learning system"""
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

# Define new languages with their use cases
NEW_LANGUAGES = {
    "Java": {
        "difficulty": 4,
        "use_case": "Enterprise backend, Android, Big Data (Hadoop, Kafka)",
        "why_useful": "60% of Fortune 500 companies use Java"
    },
    "C#": {
        "difficulty": 4,
        "use_case": "Game dev (Unity), Windows apps, .NET enterprise",
        "why_useful": "Unity game engine, 50% of PC games use C#"
    },
    "Kotlin": {
        "difficulty": 3,
        "use_case": "Android development, multiplatform mobile",
        "why_useful": "Google's preferred Android language"
    },
    "Swift": {
        "difficulty": 3,
        "use_case": "iOS, macOS, watchOS, tvOS apps",
        "why_useful": "Apple ecosystem - 1.5B active devices"
    },
    "SQL": {
        "difficulty": 2,
        "use_case": "Databases, data analysis, backend",
        "why_useful": "EVERY app needs a database"
    },
    "HTML/CSS": {
        "difficulty": 1,
        "use_case": "Web structure, styling, UI/UX",
        "why_useful": "Foundation of the web"
    },
    "Zig": {
        "difficulty": 4,
        "use_case": "Systems programming, compilers, game engines",
        "why_useful": "Rust competitor, simpler, faster compile times"
    },
    "Carbon": {
        "difficulty": 4,
        "use_case": "Systems, C++ replacement",
        "why_useful": "Google's official C++ successor"
    },
    "Mojo": {
        "difficulty": 4,
        "use_case": "AI/ML, scientific computing",
        "why_useful": "68,000x faster than Python, full Python compatibility"
    },
    "Move": {
        "difficulty": 4,
        "use_case": "Blockchain (Sui, Aptos, Diem)",
        "why_useful": "Next-gen smart contract language"
    },
    "Cairo": {
        "difficulty": 4,
        "use_case": "ZK-rollups, StarkNet, validity proofs",
        "why_useful": "Critical for layer 2 scaling"
    },
    "Vyper": {
        "difficulty": 3,
        "use_case": "Ethereum smart contracts (Pythonic)",
        "why_useful": "More secure than Solidity"
    }
}

def add_languages():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("🌍 ADDING NEW PROGRAMMING LANGUAGES")
    print("="*60)
    
    agents = ["agentforlaw", "claw-code", "claw-coder", "crustyclaw", "eagleclaw", "rustypycraw"]
    
    for language, info in NEW_LANGUAGES.items():
        print(f"\n📚 Adding {language}:")
        print(f"   Use Case: {info['use_case']}")
        print(f"   Why Useful: {info['why_useful']}")
        
        for agent in agents:
            # Start at Level 1 for new languages
            cursor.execute("""
                INSERT OR REPLACE INTO language_proficiency 
                (agent, language, proficiency_level, last_practiced, examples_generated, success_rate, source)
                VALUES (?, ?, 1, ?, 0, 0.0, 'new_language')
            """, (agent, language, datetime.now().isoformat()))
        
        print(f"   ✅ Added to all {len(agents)} agents (Level 1)")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print(f"✅ Added {len(NEW_LANGUAGES)} new languages!")
    print(f"   Total languages: {7 + len(NEW_LANGUAGES)}")

if __name__ == "__main__":
    from datetime import datetime
    add_languages()
