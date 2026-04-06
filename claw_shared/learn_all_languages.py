"""Master all programming languages across agents"""
from language_learner import LanguageLearner

# Target languages to master
TARGET_LANGUAGES = ["Rust", "Python", "TypeScript", "Solidity", "Go", "JavaScript", "C++"]

ll = LanguageLearner()

print("🎯 INITIATING CROSS-AGENT LANGUAGE LEARNING")
print("="*50)

# For each language, assign the best teacher
for language in TARGET_LANGUAGES:
    expert = ll.get_expert_agent(language)
    if expert:
        print(f"\n📚 {language}: Expert is {expert}")
        
        # All other agents learn from the expert
        agents = ["rustypycraw", "eagleclaw", "agentforlaw", "crustyclaw", "claw-coder", "claw-code"]
        for agent in agents:
            if agent != expert:
                result = ll.transfer_language_knowledge(expert, agent, language)
                if result.get("transferred"):
                    print(f"   ✅ {agent} learned {language} (level {result['new_level']})")
                else:
                    current = ll.get_proficiency(agent, language)
                    if current < 5:
                        print(f"   ⏳ {agent} already learning {language} (level {current})")
    else:
        print(f"\n⚠️ No expert found for {language} - assigning learning path")

print("\n" + "="*50)
print("🎉 LANGUAGE LEARNING INITIATED ACROSS ALL AGENTS!")
