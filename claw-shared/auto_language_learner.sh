#!/bin/bash
# Automatically learn languages across agents

echo "🦞 Starting Cross-Agent Language Learning Loop"
echo "=============================================="

while true; do
    echo ""
    echo "📚 Learning cycle at $(date)"
    
    # Have each agent learn from the expert in each language
    python3 -c "
from language_learner import LanguageLearner
import random

ll = LanguageLearner()
languages = ['Rust', 'Python', 'TypeScript', 'Solidity', 'Go']

for agent in ['agentforlaw', 'claw-coder', 'crustyclaw', 'eagleclaw']:
    for lang in languages:
        # 30% chance to learn each cycle
        if random.random() < 0.3:
            result = ll.record_learning(agent, lang, success=random.random() > 0.2)
            if result['level']:
                print(f'✅ {agent} practiced {lang} (level {result[\"level\"]}/5)')
"
    
    echo "Waiting 5 minutes before next learning cycle..."
    sleep 300
done
