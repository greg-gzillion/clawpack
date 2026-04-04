# 🤖 Complete LLM Setup for Claw Ecosystem

## Your Current LLM Models

| Model | Size | Purpose |
|-------|------|---------|
| llama3.2:3b | 2.0 GB | Main chat for eagleclaw |
| deepseek-coder:6.7b | 3.8 GB | Code generation |
| codellama:7b | 3.8 GB | Alternative coding |
| agentforlaw-law:latest | 3.8 GB | Legal model |

## Environment Setup

```bash
export ANTHROPIC_BASE_URL='http://127.0.0.1:11434'
export ANTHROPIC_API_KEY='ollama'
export OLLAMA_HOST='http://127.0.0.1:11434'
```

## Start Ollama

```bash
ollama serve &
ollama list  # Verify models
```
