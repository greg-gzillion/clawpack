"""Prioritize learning based on real-world usefulness"""
from language_learner_working import LanguageLearner
import random

ll = LanguageLearner()

# Priority levels for each language
PRIORITIES = {
    # Tier 1: Critical (Everyone must master)
    "Python": 5, "SQL": 5, "HTML/CSS": 5, "TypeScript": 5, "JavaScript": 5,
    
    # Tier 2: High Value (Enterprise ready)
    "Java": 5, "Go": 5, "Rust": 5, "Solidity": 5,
    
    # Tier 3: Platform Specific
    "Kotlin": 4, "Swift": 4, "C#": 4,
    
    # Tier 4: Emerging Tech
    "Mojo": 3, "Move": 3, "Cairo": 3, "Zig": 2, "Carbon": 2, "Vyper": 2,
    
    # Tier 5: Nice to have
    "C++": 2
}

agents = ["agentforlaw", "claw-code", "claw-coder", "crustyclaw", "eagleclaw", "rustypycraw"]

print("🎯 PRIORITY-BASED LEARNING")
print("="*60)

# Sort languages by priority
sorted_langs = sorted(PRIORITIES.keys(), key=lambda x: PRIORITIES.get(x, 0), reverse=True)

print("\n📚 Learning Order (Highest Priority First):")
for i, lang in enumerate(sorted_langs[:10], 1):
    print(f"   {i}. {lang} (Priority: {'⭐' * PRIORITIES.get(lang, 1)})")

# Learn in priority order
for language in sorted_langs:
    print(f"\n📚 FOCUSING ON: {language}")
    
    for agent in agents:
        current = ll.get_proficiency(agent, language)
        target = 5  # All agents to Level 5
        
        # Multiple learning sessions for this language
        for session in range(target - current):
            if current < target:
                result = ll.record_learning(agent, language, success=True)
                if result['improved']:
                    print(f"   ✅ {agent}: Level {current + 1}/5")
                    current = result['level']

print("\n" + "="*60)
print("🎉 PRIORITY LEARNING COMPLETE!")
ll.show_dashboard()
