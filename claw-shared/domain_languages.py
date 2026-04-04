"""Add domain-specific languages"""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

DOMAIN_LANGUAGES = {
    # Blockchain & Web3
    "Solidity": {"domain": "EVM Smart Contracts", "importance": 5},
    "Vyper": {"domain": "Secure EVM Contracts", "importance": 4},
    "Move": {"domain": "Move Blockchain (Sui/Aptos)", "importance": 4},
    "Cairo": {"domain": "STARK/ZK-rollups", "importance": 4},
    "Rust": {"domain": "Solana/Polkadot", "importance": 5},
    
    # Data Science & AI
    "Python": {"domain": "ML/AI/Data Science", "importance": 5},
    "R": {"domain": "Statistics/Data Analysis", "importance": 3},
    "Julia": {"domain": "Scientific Computing", "importance": 3},
    "Mojo": {"domain": "AI/ML Acceleration", "importance": 4},
    
    # Mobile Development
    "Kotlin": {"domain": "Android", "importance": 5},
    "Swift": {"domain": "iOS/macOS", "importance": 5},
    "Dart": {"domain": "Flutter Cross-platform", "importance": 3},
    
    # Backend & Cloud
    "Go": {"domain": "Microservices/Cloud", "importance": 5},
    "Java": {"domain": "Enterprise/Big Data", "importance": 5},
    "C#": {"domain": ".NET/Game Dev", "importance": 4},
    "Zig": {"domain": "Systems Programming", "importance": 3},
    
    # Frontend
    "TypeScript": {"domain": "Frontend/Full-stack", "importance": 5},
    "JavaScript": {"domain": "Web Development", "importance": 5},
    "HTML/CSS": {"domain": "Web Structure/Styling", "importance": 5},
    
    # Database
    "SQL": {"domain": "Databases", "importance": 5},
}

def analyze_coverage():
    """Analyze language coverage by domain"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    print("\n🌍 LANGUAGE DOMAIN COVERAGE")
    print("="*70)
    
    domains = {}
    for lang, info in DOMAIN_LANGUAGES.items():
        domain = info['domain']
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(lang)
    
    for domain, languages in sorted(domains.items()):
        print(f"\n📂 {domain}:")
        for lang in languages:
            # Check if agent knows it
            cursor.execute("SELECT proficiency_level FROM language_proficiency WHERE agent = 'rustypycraw' AND language = ?", (lang,))
            level = cursor.fetchone()
            status = f"✅ Level {level[0]}" if level else "❌ Not learned"
            print(f"   • {lang}: {status}")
    
    conn.close()

if __name__ == "__main__":
    analyze_coverage()
