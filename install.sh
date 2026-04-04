#!/bin/bash
# clawpack installer

# Version flag - MUST BE FIRST
if [[ "$1" == "--version" ]] || [[ "$1" == "-v" ]]; then
    echo "clawpack version $(cat VERSION 2>/dev/null || echo "0.0.1")"
    exit 0
fi

# Actual installation
echo "🦞 Installing Claw Ecosystem"
echo "============================"

mkdir -p ~/dev ~/.claw_memory

echo "📦 Installing agents..."
for agent in agents/*/; do
    cp -r "$agent" ~/dev/ 2>/dev/null
    echo "  → $(basename "$agent")"
done

echo "📦 Installing claw-shared..."
cp -r claw-shared ~/dev/

echo "🧠 Restoring database..."
cp .claw_memory/shared_memory.db ~/.claw_memory/

echo ""
echo "✅ Done! Version: $(cat VERSION 2>/dev/null || echo "0.0.1")"

