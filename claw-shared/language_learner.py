"""Cross-agent language learning system - COMPLETELY FIXED"""
import sqlite3
import json
import random
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

class LanguageLearner:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self._init_language_tables()
    
    def _init_language_tables(self):
        # Language proficiency tracking
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS language_proficiency (
                agent TEXT,
                language TEXT,
                proficiency_level INTEGER DEFAULT 1,
                last_practiced TEXT,
                examples_generated INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                source TEXT,
                UNIQUE(agent, language)
            )
        """)
        
        # Language learning tasks
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS language_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT,
                task_type TEXT,
                difficulty INTEGER DEFAULT 1,
                completed_by TEXT,
                completed_at TEXT,
                result TEXT
            )
        """)
        
        # Cross-agent teaching assignments
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS teaching_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_agent TEXT,
                student_agent TEXT,
                language TEXT,
                topic TEXT,
                assigned_at TEXT,
                completed BOOLEAN DEFAULT 0,
                student_improvement INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()
    
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
    
    def assign_teacher(self, student_agent, target_language):
        """Assign a teacher agent to help another learn"""
        teacher = self.get_expert_agent(target_language)
        if not teacher:
            return None
        
        self.cursor.execute("""
            INSERT INTO teaching_assignments (teacher_agent, student_agent, language, assigned_at)
            VALUES (?, ?, ?, ?)
        """, (teacher, student_agent, target_language, datetime.now().isoformat()))
        self.conn.commit()
        
        return {"teacher": teacher, "assignment_id": self.cursor.lastrowid}
    
    def record_learning(self, agent, language, success=True):
        """Record a learning event - FIXED VERSION"""
        # First check if record exists
        self.cursor.execute("""
            SELECT proficiency_level, examples_generated, success_rate 
            FROM language_proficiency 
            WHERE agent = ? AND language = ?
        """, (agent, language))
        existing = self.cursor.fetchone()
        
        if existing:
            current_level, examples, rate = existing
            new_level = min(5, current_level + 1)
            new_examples = examples + 1
            new_rate = (rate * examples + (1.0 if success else 0.0)) / new_examples
            
            self.cursor.execute("""
                UPDATE language_proficiency 
                SET proficiency_level = ?,
                    last_practiced = ?,
                    examples_generated = ?,
                    success_rate = ?
                WHERE agent = ? AND language = ?
            """, (new_level, datetime.now().isoformat(), new_examples, new_rate, agent, language))
        else:
            # Insert new record
            self.cursor.execute("""
                INSERT INTO language_proficiency (agent, language, proficiency_level, last_practiced, examples_generated, success_rate)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (agent, language, 1, datetime.now().isoformat(), 1, 1.0 if success else 0.0))
        
        self.conn.commit()
        
        # Get updated level
        self.cursor.execute("SELECT proficiency_level FROM language_proficiency WHERE agent = ? AND language = ?", (agent, language))
        row = self.cursor.fetchone()
        level = row[0] if row else 1
        
        return {"level": level, "success": success}
    
    def generate_learning_task(self, language, difficulty=1):
        """Generate a learning task for an agent"""
        tasks = {
            "Rust": [
                "Write a simple function in Rust",
                "Create a basic smart contract in Rust",
                "Implement error handling in Rust",
                "Build a REST API in Rust"
            ],
            "Python": [
                "Write a basic Python script",
                "Create a simple API endpoint",
                "Implement data processing in Python",
                "Build a web scraper in Python"
            ],
            "TypeScript": [
                "Write simple TypeScript types",
                "Create a basic React component",
                "Implement type-safe functions",
                "Build a full-stack TypeScript app"
            ],
            "Solidity": [
                "Write a simple smart contract",
                "Create a basic token contract",
                "Implement secure withdrawal pattern",
                "Build a DeFi protocol in Solidity"
            ],
            "Go": [
                "Write a simple Go routine",
                "Create a basic HTTP server",
                "Implement concurrent processing",
                "Build a microservice in Go"
            ],
            "JavaScript": [
                "Write basic JavaScript functions",
                "Create a simple web app",
                "Implement async operations",
                "Build a Node.js server"
            ],
            "C++": [
                "Write a simple C++ program",
                "Create a basic class structure",
                "Implement memory management",
                "Build a data structure in C++"
            ]
        }
        
        task_list = tasks.get(language, [f"Write code in {language}"])
        return random.choice(task_list)
    
    def start_learning_session(self, agent, language):
        """Start a guided learning session"""
        current_level = self.get_proficiency(agent, language)
        task = self.generate_learning_task(language, min(current_level + 1, 3))
        
        print(f"\n📚 Learning Session: {agent} learning {language}")
        print(f"   Current level: {current_level}/5")
        print(f"   Task: {task}")
        
        return {"task": task, "current_level": current_level}
    
    def get_proficiency(self, agent, language):
        """Get agent's proficiency in a language"""
        self.cursor.execute("""
            SELECT proficiency_level FROM language_proficiency 
            WHERE agent = ? AND language = ?
        """, (agent, language))
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    def get_learning_path(self, agent):
        """Get recommended learning path for an agent"""
        self.cursor.execute("""
            SELECT language, proficiency_level FROM language_proficiency 
            WHERE agent = ? 
            ORDER BY proficiency_level ASC
        """, (agent,))
        languages = self.cursor.fetchall()
        
        recommendations = []
        for lang, level in languages:
            if level < 5:
                recommendations.append({
                    "language": lang,
                    "current_level": level,
                    "next_task": self.generate_learning_task(lang, min(level + 1, 3))
                })
        
        return recommendations
    
    def transfer_language_knowledge(self, from_agent, to_agent, language):
        """Transfer language knowledge from expert to learner"""
        source_level = self.get_proficiency(from_agent, language)
        target_level = self.get_proficiency(to_agent, language)
        
        if source_level > target_level:
            # Transfer knowledge (immediate boost)
            new_level = min(source_level - 1, target_level + 2)
            self.cursor.execute("""
                UPDATE language_proficiency 
                SET proficiency_level = ?,
                    source = 'transferred_from_' || ?
                WHERE agent = ? AND language = ?
            """, (new_level, from_agent, to_agent, language))
            self.conn.commit()
            
            return {"transferred": True, "new_level": new_level}
        
        return {"transferred": False, "reason": "Source not more proficient"}
    
    def get_all_proficiencies(self):
        """Get all language proficiencies for dashboard"""
        self.cursor.execute("""
            SELECT agent, language, proficiency_level 
            FROM language_proficiency 
            ORDER BY agent, proficiency_level DESC
        """)
        return self.cursor.fetchall()
    
    def get_learning_summary(self):
        """Get summary of learning progress"""
        self.cursor.execute("""
            SELECT 
                COUNT(DISTINCT agent) as total_agents,
                COUNT(DISTINCT language) as total_languages,
                AVG(proficiency_level) as avg_proficiency
            FROM language_proficiency
        """)
        return self.cursor.fetchone()

# Initialize the system
if __name__ == "__main__":
    ll = LanguageLearner()
    print("✅ Language Learning System Initialized")
    
    # Show summary
    total_agents, total_langs, avg_prof = ll.get_learning_summary()
    print(f"\n📊 Learning Summary:")
    print(f"   Agents: {total_agents}")
    print(f"   Languages: {total_langs}")
    print(f"   Average Proficiency: {avg_prof:.2f}/5")
    
    # Show current proficiencies
    print("\n📊 Current Language Proficiency:")
    for agent, lang, level in ll.get_all_proficiencies():
        print(f"   {agent}: {lang} = {'⭐' * level}")
