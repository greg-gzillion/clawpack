#!/bin/bash
# Launch all learning components

echo "🦞 Starting Claw Agent Learning System"
echo "========================================"

# 1. Initialize databases
cd ~/dev/claw-shared

python3 -c "
from neural_memory import NeuralMemory
from predictor import PredictiveIntelligence
from cross_learner import CrossAgentLearner

nm = NeuralMemory()
pi = PredictiveIntelligence()
cl = CrossAgentLearner()

print('✅ All learning systems initialized')
"

# 2. Start autonomous learner in background
echo "Starting autonomous learner..."
python3 autonomous_learner.py &
LEARNER_PID=$!

echo "✅ Learning system running (PID: $LEARNER_PID)"
echo ""
echo "To stop: kill $LEARNER_PID"
echo "To monitor: sqlite3 ~/.claw_memory/shared_memory.db 'SELECT * FROM neural_patterns LIMIT 5;'"

# Save PID for later
echo $LEARNER_PID > ~/.claw_memory/learner.pid
