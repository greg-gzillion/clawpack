"""Autonomous learning agent that runs continuously"""
import time
import sqlite3
from pathlib import Path
from datetime import datetime
import subprocess

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

class AutonomousLearner:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self.running = True
        self.learning_cycle = 0
    
    def analyze_memory_patterns(self):
        """Find patterns in stored memories"""
        self.cursor.execute("""
            SELECT agent, key, length(value) as value_len, timestamp
            FROM memories 
            WHERE timestamp > datetime('now', '-1 hour')
            ORDER BY timestamp DESC
        """)
        recent = self.cursor.fetchall()
        
        if len(recent) > 10:
            # Detect burst of activity
            agents = [r[0] for r in recent]
            from collections import Counter
            active_agent = Counter(agents).most_common(1)[0][0]
            
            # Suggest collaboration
            return f"High activity detected from {active_agent}. Other agents may want to assist."
        return None
    
    def generate_insights(self):
        """Generate insights from agent interactions"""
        insights = []
        
        # Most active agent
        self.cursor.execute("""
            SELECT agent, COUNT(*) as activity
            FROM memories
            GROUP BY agent
            ORDER BY activity DESC
            LIMIT 1
        """)
        most_active = self.cursor.fetchone()
        if most_active:
            insights.append(f"Most active agent: {most_active[0]} ({most_active[1]} memories)")
        
        # Most common memory type
        self.cursor.execute("""
            SELECT SUBSTR(key, 1, 10) as prefix, COUNT(*) as count
            FROM memories
            GROUP BY prefix
            ORDER BY count DESC
            LIMIT 1
        """)
        common = self.cursor.fetchone()
        if common:
            insights.append(f"Most common memory topic: {common[0]}... ({common[1]} occurrences)")
        
        return insights
    
    def auto_collaborate(self):
        """Automatically suggest agent collaborations"""
        self.cursor.execute("""
            SELECT name, capabilities FROM agent_registry
        """)
        agents = self.cursor.fetchall()
        
        suggestions = []
        for i, agent1 in enumerate(agents):
            for agent2 in agents[i+1:]:
                # Check if capabilities complement each other
                if "law" in agent1[1].lower() and "code" in agent2[1].lower():
                    suggestions.append(f"Consider collaboration: {agent1[0]} (law) + {agent2[0]} (code)")
                elif "code" in agent1[1].lower() and "bug" in agent2[1].lower():
                    suggestions.append(f"Consider collaboration: {agent1[0]} (code) + {agent2[0]} (audit)")
        
        return suggestions[:3]
    
    def learn_cycle(self):
        """One complete learning cycle"""
        self.learning_cycle += 1
        print(f"\n🔄 Learning Cycle #{self.learning_cycle}")
        
        # 1. Analyze patterns
        pattern = self.analyze_memory_patterns()
        if pattern:
            print(f"📊 Pattern detected: {pattern}")
        
        # 2. Generate insights
        insights = self.generate_insights()
        for insight in insights:
            print(f"💡 Insight: {insight}")
        
        # 3. Suggest collaborations
        suggestions = self.auto_collaborate()
        for suggestion in suggestions:
            print(f"🤝 Collaboration suggestion: {suggestion}")
        
        # 4. Record this learning cycle
        self.cursor.execute("""
            INSERT INTO memories (agent, key, value, timestamp, tags)
            VALUES (?, ?, ?, ?, ?)
        """, ("autonomous_learner", f"learning_cycle_{self.learning_cycle}", 
              f"Completed cycle with {len(insights)} insights", 
              datetime.now().isoformat(), "learning"))
        self.conn.commit()
    
    def run(self, interval_seconds=300):
        """Run the autonomous learner continuously"""
        print("🧠 Autonomous Learning Agent Started")
        print(f"   Learning interval: {interval_seconds} seconds")
        
        while self.running:
            try:
                self.learn_cycle()
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                print("\n🛑 Autonomous learning stopped")
                break
            except Exception as e:
                print(f"❌ Error in learning cycle: {e}")
                time.sleep(60)

if __name__ == "__main__":
    learner = AutonomousLearner()
    learner.run(interval_seconds=60)  # Learn every minute
