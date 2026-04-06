
## 📦 Installation

```bash
git clone https://github.com/greg-gzillion/rustypycraw.git
cd rustypycraw
python3 -m venv .venv
source .venv/bin/activate
pip install -e . maturin requests groq
cd rustypycraw-core
maturin develop --release
cd ..
```

## 🚀 Quick Start

```bash
./rustypycraw --list-models
./rustypycraw ~/dev/TX --stats
./rustypycraw ~/dev/TX --search "collateral"
./rustypycraw ~/dev/TX --pinch
./rustypycraw --groq --ask 'What is PHNX?'
```

## 🤖 Supported Models

| Model | Provider | Speed | Best For |
|-------|----------|-------|----------|
| llama-3.3-70b | Groq | 1-2 sec | General Q&A |
| deepseek-coder:6.7b | Ollama | 30-60 sec | Code generation |
| codellama:7b | Ollama | 30-60 sec | Rust debugging |
| llama3.2:3b | Ollama | 15-30 sec | Fast local |

## 📚 Documentation References

```bash
# List all languages with references
./rustypycraw --list-langs

# Show references for specific language
./rustypycraw --docs rust
./rustypycraw --docs cosmwasm
./rustypycraw --docs cpp
./rustypycraw --docs typescript
```

## ⚠️ Disclaimer

This software is a **clean-room reimplementation** based on:
- Publicly observable behavior of Claude Code
- Independent research and community analysis
- Documentation and behavioral observation

**No proprietary source code from Anthropic is included.**

This project is for **educational and research purposes**. 
The author does not claim ownership of any underlying ideas, patterns, or functionality.

Not affiliated with Anthropic. Use at your own risk.

## Terms

Free to use, modify, and distribute. No warranty. No ownership claimed.
