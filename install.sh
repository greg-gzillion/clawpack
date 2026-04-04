#!/bin/bash
echo "🦞 Installing Claw Ecosystem"

# Copy agents
for agent in agents/*/; do
    cp -r "$agent" ~/dev/
done

# Copy shared memory
cp -r claw-shared ~/dev/

# Copy database
mkdir -p ~/.claw_memory
cp .claw_memory/shared_memory.db ~/.claw_memory/

echo "✅ Done: 6 agents, 19 languages at Level 5"
