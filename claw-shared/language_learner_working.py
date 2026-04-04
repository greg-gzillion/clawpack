"""Complete working language learning system"""
import sqlite3
import random
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

class LanguageLearner:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
    
    def initialize_agent_languages(self):
        """Initialize all agents with their current language knowledge"""
        agent_languages = {
            "rustypycraw": [
                ("Python", 5), ("Rust", 5), ("Solidity", 4), ("TypeScript", 4),
                ("Go", 3), ("JavaScript", 3), ("C++", 2)
            ],
            "eagleclaw": [
                ("Python", 4), ("Rust", 4), ("TypeScript", 3), ("Go", 2)
            ],
            "agentforlaw": [
                ("Python", 4), ("JavaScript", 2), ("TypeScript", 2)
            ],
            "crustyclaw": [
                ("Rust", 5), ("Python", 3)
            ],
            "claw-coder": [
                ("Python", 5), ("JavaScript", 3), ("TypeScript", 3)
            ],
            "claw-code": [
                ("TypeScript", 4), ("Python", 3), ("Rust", 3)
            ]
        }
        
        for agent, languages in agent_languages.items():
            for lang, level in languages:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO language_proficiency 
                    (agent, language, proficiency_level, last_practiced, examples_generated, success_rate, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (agent, lang, level, datetime.now().isoformat(), 0, 0.0, "initial"))
        
        self.conn.commit()
        print("✅ Agent languages initialized")
    
    def get_proficiency(self, agent, language):
        """Get agent's proficiency in a language"""
        self.cursor.execute("""
            SELECT proficiency_level FROM language_proficiency 
            WHERE agent = ? AND language = ?
        """, (agent, language))
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def record_learning(self, agent, language, success=True):
        """Record a learning event"""
        current_level = self.get_proficiency(agent, language)
        
        if current_level == 0:
            # New language
            self.cursor.execute("""
                INSERT INTO language_proficiency (agent, language, proficiency_level, last_practiced, examples_generated, success_rate)
                VALUES (?, ?, 1, ?, 1, ?)
            """, (agent, language, datetime.now().isoformat(), 1.0 if success else 0.0))
            new_level = 1
        else:
            # Update existing
            new_level = min(5, current_level + 1)
            self.cursor.execute("""
                UPDATE language_proficiency 
                SET proficiency_level = ?,
                    last_practiced = ?,
                    examples_generated = examples_generated + 1
                WHERE agent = ? AND language = ?
            """, (new_level, datetime.now().isoformat(), agent, language))
        
        self.conn.commit()
        return {"level": new_level, "improved": new_level > current_level}
    
    def get_expert_agent(self, language):
        """Find the most proficient agent for a language"""
        self.cursor.execute("""
            SELECT agent, proficiency_level FROM language_proficiency 
            WHERE language = ? 
            ORDER BY proficiency_level DESC 
            LIMIT 1
        """, (language,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def transfer_knowledge(self, from_agent, to_agent, language):
        """Transfer language knowledge from expert to learner"""
        source_level = self.get_proficiency(from_agent, language)
        target_level = self.get_proficiency(to_agent, language)
        
        if source_level > target_level:
            new_level = min(source_level, target_level + 2)
            self.cursor.execute("""
                INSERT OR REPLACE INTO language_proficiency 
                (agent, language, proficiency_level, last_practiced, source)
                VALUES (?, ?, ?, ?, ?)
            """, (to_agent, language, new_level, datetime.now().isoformat(), f"learned_from_{from_agent}"))
            self.conn.commit()
            return {"transferred": True, "new_level": new_level}
        return {"transferred": False}
    
    def generate_learning_task(self, language, level):
        """Generate a learning task based on current level"""
        tasks = {
            1: f"Learn basic syntax and variables in {language}",
            2: f"Write functions and control structures in {language}",
            3: f"Create a small project using advanced {language} features",
            4: f"Optimize and refactor {language} code for performance",
            5: f"Master {language} and teach others"
        }
        return tasks.get(min(level + 1, 5), f"Practice {language} programming")
    
    def start_learning_session(self, agent, language):
        """Start a guided learning session"""
        current = self.get_proficiency(agent, language)
        task = self.generate_learning_task(language, current)
        
        print(f"\n📚 Learning Session: {agent} learning {language}")
        print(f"   Current level: {current}/5")
        print(f"   Task: {task}")
        return {"task": task, "current_level": current}
    
    def get_statistics(self):
        """Get learning statistics"""
        self.cursor.execute("""
            SELECT 
                COUNT(DISTINCT agent) as agents,
                COUNT(DISTINCT language) as languages,
                AVG(proficiency_level) as avg_prof,
                SUM(CASE WHEN proficiency_level >= 4 THEN 1 ELSE 0 END) as advanced
            FROM language_proficiency
        """)
        return self.cursor.fetchone()
    
    def show_dashboard(self):
        """Display learning dashboard"""
        print("\n" + "="*80)
        print("🌍 LANGUAGE LEARNING DASHBOARD")
        print("="*80)
        
        # Get all data
        self.cursor.execute("SELECT agent, language, proficiency_level FROM language_proficiency ORDER BY agent, proficiency_level DESC")
        data = self.cursor.fetchall()
        
        # Group by agent
        agents = {}
        for agent, lang, level in data:
            if agent not in agents:
                agents[agent] = []
            agents[agent].append((lang, level))
        
        print("\n📚 LANGUAGE PROFICIENCY:")
        print("-"*80)
        for agent in sorted(agents.keys()):
            print(f"\n🦞 {agent.upper()}:")
            for lang, level in agents[agent]:
                print(f"   {lang}: {'⭐' * level} (Level {level}/5)")
        
        # Statistics
        stats = self.get_statistics()
        print("\n" + "="*80)
        print("📊 STATISTICS:")
        print(f"   Agents: {stats[0]}")
        print(f"   Languages: {stats[1]}")
        print(f"   Average Proficiency: {stats[2]:.2f}/5")
        print(f"   Advanced Skills (Level 4+): {stats[3]}")
        print("="*80)

# Initialize and run
if __name__ == "__main__":
    ll = LanguageLearner()
    ll.initialize_agent_languages()
    ll.show_dashboard()
