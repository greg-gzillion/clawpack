"""Transfer language knowledge between agents"""
from language_learner_working import LanguageLearner

ll = LanguageLearner()

# Languages to transfer
languages = ["Rust", "Python", "TypeScript", "Solidity", "Go", "JavaScript", "C++"]

print("🎓 TRANSFERRING LANGUAGE KNOWLEDGE")
print("="*50)

for language in languages:
    expert = ll.get_expert_agent(language)
    if expert:
        print(f"\n📚 {language}: Expert is {expert}")
        
        # Transfer to all other agents
        agents = ["agentforlaw", "eagleclaw", "crustyclaw", "claw-coder", "claw-code"]
        for agent in agents:
            if agent != expert:
                result = ll.transfer_knowledge(expert, agent, language)
                if result.get('transferred'):
                    print(f"   ✅ {agent} learned {language} (level {result['new_level']})")
                else:
                    current = ll.get_proficiency(agent, language)
                    if current > 0:
                        print(f"   📖 {agent} already knows {language} (level {current})")

print("\n" + "="*50)
print("🎉 KNOWLEDGE TRANSFER COMPLETE!")

# Show final dashboard
ll.show_dashboard()
