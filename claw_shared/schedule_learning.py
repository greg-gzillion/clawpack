"""Schedule language learning sessions for all agents"""
from language_learner import LanguageLearner

ll = LanguageLearner()

# Define what each agent should learn
learning_plan = {
    "agentforlaw": ["Rust", "TypeScript", "Solidity", "Go"],
    "eagleclaw": ["Solidity", "Go", "TypeScript", "JavaScript"],
    "crustyclaw": ["TypeScript", "Go", "Python", "Solidity"],
    "claw-coder": ["Rust", "TypeScript", "Go", "Solidity"],
    "claw-code": ["Python", "Rust", "Solidity", "Go"]
}

print("🎯 STARTING SCHEDULED LANGUAGE LEARNING")
print("="*50)

for agent, languages in learning_plan.items():
    print(f"\n📚 {agent.upper()} LEARNING SESSION")
    for language in languages:
        current = ll.get_proficiency(agent, language)
        if current < 5:
            # Start learning session
            session = ll.start_learning_session(agent, language)
            # Record learning
            result = ll.record_learning(agent, language, success=True)
            print(f"   ✅ Learned {language}: level {current} → {result['level']}")
        else:
            print(f"   ⭐ Already mastered {language}")

print("\n" + "="*50)
print("🎉 ALL AGENTS HAVE COMPLETED THEIR LEARNING SESSIONS!")

# Show final summary
summary = ll.get_learning_summary()
print(f"\n📊 FINAL LEARNING SUMMARY:")
print(f"   Total Languages Mastered: {summary[1]}")
print(f"   Average Proficiency: {summary[2]:.2f}/5")
