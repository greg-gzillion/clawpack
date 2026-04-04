"""Accelerate all agents to Level 5 in all languages"""
from language_learner_working import LanguageLearner
import random
import time

ll = LanguageLearner()

# All languages currently in the system
ALL_LANGUAGES = [
    "C++", "Go", "JavaScript", "Python", "Rust", "Solidity", "TypeScript",  # Core 7
    "Java", "C#", "Kotlin", "Swift", "SQL", "HTML/CSS", "Zig", "Carbon",    # New 8
    "Mojo", "Move", "Cairo", "Vyper"                                         # Emerging 4
]

agents = ["agentforlaw", "claw-code", "claw-coder", "crustyclaw", "eagleclaw", "rustypycraw"]

print("🚀 ACCELERATED LEARNING TO LEVEL 5")
print("="*60)

# Identify weak areas
print("\n📊 IDENTIFYING WEAK AREAS:")
for agent in agents:
    weak_languages = []
    for lang in ALL_LANGUAGES:
        level = ll.get_proficiency(agent, lang)
        if level < 5:
            weak_languages.append((lang, level))
    
    if weak_languages:
        print(f"\n🦞 {agent}: Need to improve {len(weak_languages)} languages")
        for lang, level in weak_languages[:5]:  # Show first 5
            print(f"   • {lang}: Level {level}/5")

# Intensive learning sessions
print("\n" + "="*60)
print("🎯 STARTING INTENSIVE LEARNING")

cycles = 0
while cycles < 50:  # Run 50 learning cycles
    cycles += 1
    improvements = 0
    
    for agent in agents:
        for language in ALL_LANGUAGES:
            current = ll.get_proficiency(agent, language)
            if current < 5:
                # Higher chance to learn for lower levels
                chance = 0.5 if current < 3 else 0.3
                if random.random() < chance:
                    result = ll.record_learning(agent, language, success=True)
                    if result['improved']:
                        improvements += 1
                        print(f"✅ {agent} improved {language} to level {result['level']}")
    
    if cycles % 10 == 0:
        stats = ll.get_statistics()
        print(f"\n📊 Cycle {cycles}: Avg Level {stats[2]:.2f}/5, Improvements: {improvements}")
    
    if improvements == 0:
        print(f"\n🎉 No more improvements needed after {cycles} cycles!")
        break
    
    time.sleep(0.5)  # Small delay to see progress

print("\n" + "="*60)
print("🎉 ACCELERATED LEARNING COMPLETE!")
ll.show_dashboard()
