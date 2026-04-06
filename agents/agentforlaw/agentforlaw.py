#!/usr/bin/env python3
"""
AGENTFORLAW - Statutes, Codes, and Regulations Information Agent
Full shared memory integration with cross-learning capabilities
"""

import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime

# Add paths for shared modules
CLAW_SHARED = Path(__file__).parent.parent / "claw_shared"
sys.path.insert(0, str(CLAW_SHARED))
sys.path.insert(0, str(Path(__file__).parent))

try:
    from memory import get_memory
    SHARED_MEMORY_AVAILABLE = True
except ImportError:
    SHARED_MEMORY_AVAILABLE = False

class AgentForLaw:
    """Statutes, codes, and regulations information agent"""
    
    def __init__(self):
        self.name = "agentforlaw"
        self.db_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.db_path.parent.mkdir(exist_ok=True)
        
        if SHARED_MEMORY_AVAILABLE:
            self.memory = get_memory(self.name)
        
        # Statutes and codes database
        self.statutes = {
            # Constitutional provisions
            "first amendment": "Protects speech, religion, press, assembly, and petition.",
            "fourth amendment": "Protects against unreasonable searches and seizures.",
            "fifth amendment": "Protects against self-incrimination and guarantees due process.",
            "miranda rights": "Right to remain silent and right to an attorney upon arrest.",
            
            # Contract provisions
            "contract requirements": "Offer, acceptance, consideration, mutual assent, capacity, and purpose.",
            "breach": "Failure to perform contractual obligations without excuse.",
            "consideration": "Something of value exchanged between parties.",
            
            # Criminal provisions
            "felony classification": "Serious offenses with 1+ year confinement.",
            "misdemeanor classification": "Less serious offenses with under 1 year confinement.",
            "probable cause": "Reasonable belief based on factual evidence.",
            
            # Family provisions
            "custody types": "Decision-making rights and physical living arrangements.",
            "dissolution": "Process ending a marriage with asset division and support.",
            "support": "Court-ordered financial assistance between former spouses.",
            
            # Business structures
            "corporation definition": "Entity separate from owners with liability protection.",
            "llc definition": "Hybrid structure with liability protection and tax flexibility.",
            "partnership definition": "Two or more persons sharing profits and liabilities.",
            
            # Employment provisions
            "at-will doctrine": "Either party can end employment anytime for any reason.",
            "wrongful termination": "Ending employment violating contract or anti-discrimination statutes.",
            
            # Property provisions
            "eminent domain": "Government taking private property for public use with compensation.",
            "easement definition": "Right to use another's property for specific purposes."
        }
        
        self.landmark_cases = {
            "marbury v madison": "Established judicial review (1803)",
            "brown v board": "Ended school segregation (1954)"
        }
        
        self.init_db()
        self.print_welcome()
    
    def init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS agentforlaw_knowledge
                     (id INTEGER PRIMARY KEY, query TEXT UNIQUE, 
                      response TEXT, category TEXT, timestamp TEXT, 
                      source_agent TEXT, usage_count INTEGER DEFAULT 1)''')
        conn.commit()
        conn.close()
    
    def save_to_shared_memory(self, query, response, category="statute"):
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO agentforlaw_knowledge 
                         (query, response, category, timestamp, source_agent, usage_count) 
                         VALUES (?,?,?,?,?,1)''',
                      (query.lower(), response, category, datetime.now().isoformat(), self.name))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def get_from_shared_memory(self, query):
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            c.execute('SELECT response, category, source_agent FROM agentforlaw_knowledge WHERE query = ?', (query.lower(),))
            row = c.fetchone()
            conn.close()
            if row:
                return {"response": row[0], "category": row[1], "source": row[2]}
            return None
        except:
            return None
    
    def search_knowledge(self, query):
        query_lower = query.lower()
        
        cached = self.get_from_shared_memory(query_lower)
        if cached:
            return cached["response"]
        
        for key, value in self.statutes.items():
            if key in query_lower or query_lower in key:
                self.save_to_shared_memory(query, value, "statute")
                return value
        
        for case, desc in self.landmark_cases.items():
            if case in query_lower:
                response = f"{case.title()}: {desc}"
                self.save_to_shared_memory(query, response, "case")
                return response
        
        return None
    
    def answer_question(self, question):
        answer = self.search_knowledge(question)
        
        if answer:
            return f"""
📚 INFORMATION:
{answer}

💡 Source: AgentForLaw knowledge base
🔗 Shared with all Clawpack agents
"""
        else:
            return f"""
❓ I don't have information about: "{question}"

📋 I can answer about:
  • Constitutional provisions
  • Contract requirements
  • Criminal classifications
  • Family proceedings
  • Business structures
  • Employment doctrines
  • Property rights
  • Landmark rulings

Try rephrasing or ask about a specific topic.
"""
    
    def print_welcome(self):
        print("\n" + "="*60)
        print("⚖️ AGENTFORLAW - Statutes & Codes")
        print("="*60)
        print(f"Shared memory: {'Yes' if SHARED_MEMORY_AVAILABLE else 'No'}")
        print("="*60)
        print("\nCOMMANDS:")
        print("  /ask [question]  - Ask about statutes, codes, or regulations")
        print("  /stats           - Show shared memory statistics")
        print("  /quit            - Exit")
        print("="*60)
    
    def show_stats(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM agentforlaw_knowledge')
        count = c.fetchone()[0]
        conn.close()
        print(f"\n📊 Shared knowledge entries: {count}")
        return ""
    
    def chat(self):
        self.print_welcome()
        
        while True:
            try:
                cmd = input("\n⚖️ AgentForLaw> ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/stats":
                    self.show_stats()
                elif cmd.startswith("/ask "):
                    question = cmd[5:]
                    print(self.answer_question(question))
                else:
                    print("Unknown command. Use /ask [question] or /quit")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = AgentForLaw()
    agent.chat()
