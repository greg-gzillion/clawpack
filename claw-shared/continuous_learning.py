"""Continuous learning to reach Level 5 in all languages"""
from language_learner_working import LanguageLearner
import time
import random

ll = LanguageLearner()

agents = ["agentforlaw", "eagleclaw", "crustyclaw", "claw-coder", "claw-code", "rustypycraw"]
languages = ["Rust", "Python", "TypeScript", "Solidity", "Go", "JavaScript", "C++"]

print("🦞 STARTING CONTINUOUS LEARNING TO LEVEL 5")
print("="*50)

cycle = 0
while cycle < 20:  # Run 20 cycles
    cycle += 1
    print(f"\n🔄 Learning Cycle #{cycle}")
    
    for agent in agents:
        for language in languages:
            current = ll.get_proficiency(agent, language)
            if current < 5 and random.random() < 0.4:  # 40% chance to improve
                result = ll.record_learning(agent, language, success=True)
                if result['improved']:
                    print(f"   ✅ {agent} improved {language} to level {result['level']}")
    
    # Show progress every 5 cycles
    if cycle % 5 == 0:
        stats = ll.get_statistics()
        print(f"\n📊 Progress: Avg Level {stats[2]:.2f}/5")
    
    time.sleep(2)

print("\n" + "="*50)
print("🎉 CONTINUOUS LEARNING COMPLETE!")
ll.show_dashboard()
