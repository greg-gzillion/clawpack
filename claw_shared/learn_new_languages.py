"""Learning schedule for new languages"""
from language_learner_working import LanguageLearner
import random

ll = LanguageLearner()

NEW_LANGUAGES = ["Java", "C#", "Kotlin", "Swift", "SQL", "HTML/CSS", "Zig", "Carbon", "Mojo", "Move", "Cairo", "Vyper"]

print("🎯 LEARNING NEW LANGUAGES")
print("="*60)

# Set learning difficulty priority
priority = {
    "SQL": 5, "HTML/CSS": 5,  # Essential - everyone needs
    "Java": 4, "C#": 4, "Kotlin": 4, "Swift": 4,  # High demand
    "Mojo": 3, "Move": 3, "Cairo": 3,  # Emerging blockchain/AI
    "Zig": 2, "Carbon": 2, "Vyper": 2  # Niche but powerful
}

agents = ["agentforlaw", "claw-code", "claw-coder", "crustyclaw", "eagleclaw", "rustypycraw"]

for language in sorted(NEW_LANGUAGES, key=lambda x: priority.get(x, 0), reverse=True):
    print(f"\n📚 Learning {language} (Priority: {'⭐' * priority.get(language, 1)})")
    
    # Assign a teacher (rustypycraw or claw-coder as base)
    teacher = "rustypycraw"
    
    for agent in agents:
        if agent != teacher:
            # Transfer knowledge from teacher
            current = ll.get_proficiency(agent, language)
            if current < 3:
                # Learning session
                session = ll.start_learning_session(agent, language)
                result = ll.record_learning(agent, language, success=True)
                print(f"   ✅ {agent}: Level {current} → {result['level']}")
            else:
                print(f"   📖 {agent}: Already Level {current}")

print("\n" + "="*60)
print("🎉 NEW LANGUAGES INITIATED!")
