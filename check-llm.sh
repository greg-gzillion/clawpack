#!/bin/bash
# LLM Health Check
echo "=== LLM Status ==="
if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama running"
    echo "Models: $(ollama list | tail -n +2 | wc -l)"
else
    echo "❌ Ollama not running"
    echo "Start with: ollama serve &"
fi
