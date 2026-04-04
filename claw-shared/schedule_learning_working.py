"""Schedule language learning sessions for all agents"""
from language_learner_working import LanguageLearner

ll = LanguageLearner()

# What each agent should learn
learning_plan = {
    "agentforlaw": ["Rust", "TypeScript", "Solidity", "Go"],
    "eagleclaw": ["Solidity", "Go", "TypeScript", "JavaScript", "C++"],
    "crustyclaw": ["TypeScript", "Go", "Python", "Solidity", "JavaScript"],
    "claw-coder": ["Rust", "TypeScript", "Go", "Solidity", "C++"],
    "claw-code": ["Python", "Rust", "Solidity", "Go", "JavaScript"]
}

print("🎯 STARTING LANGUAGE LEARNING")
print("="*50)

for agent, languages in learning_plan.items():
    print(f"\n📚 {agent.upper()} LEARNING SESSION")
    for language in languages:
        current = ll.get_proficiency(agent, language)
        if current < 5:
            session = ll.start_learning_session(agent, language)
            result = ll.record_learning(agent, language, success=True)
            if result['improved']:
                print(f"   ✅ Learned {language}: level {current} → {result['level']}")
            else:
                print(f"   📖 Practiced {language}: still level {current}")
        else:
            print(f"   ⭐ Already mastered {language}")

print("\n" + "="*50)
print("🎉 LEARNING SESSIONS COMPLETE!")

# Show final dashboard
ll.show_dashboard()
