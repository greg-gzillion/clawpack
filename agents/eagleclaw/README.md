# 🦅 EagleClaw

**AI-powered development assistant for blockchain smart contracts**

[![Rust 1.70+](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)

## What is EagleClaw?

EagleClaw is an autonomous coding agent that helps developers write, review, and optimize smart contracts.

## ✨ Features

- Multi-language support - Rust, Go, TypeScript, Solidity
- Blockchain focused - CosmWasm, EVM, custom chains
- Local AI integration - Ollama or Groq API
- Full tool suite - File operations, search, shell, git
- Session management - Save and resume conversations
- Cost tracking - Monitor token usage and API costs

## 🚀 Quick Start

```bash
git clone https://github.com/greg-gzillion/eagleclaw.git
cd eagleclaw/rust
cargo build --release
./target/release/eagleclaw --help
```

## 🦅 Commands

| Command | Description |
|---------|-------------|
| ask <question> | Ask AI about your code |
| search <term> | Search codebase |
| git status/diff | Git integration |
| session new/list/load | Session management |
| cost | Show token/cost usage |
| permission <mode> | Set permission level |
| model <name> | Switch AI model |

## 🔧 Requirements

- Rust 1.70+
- Ollama (for local AI) or Groq API key

## 🤝 Related Projects

- **[rustypycraw](https://github.com/greg-gzillion/rustypycraw)** - Hybrid Rust+Python code crawler
- **[crustyclaw](https://github.com/greg-gzillion/crustyclaw)** - Pure Rust AI assistant
- **[claw-coder](https://github.com/greg-gzillion/claw-coder)** - Python AI assistant

## ⚠️ Disclaimer

This software is a **clean-room reimplementation** based on publicly observable behavior.

**No proprietary source code is included.**

This project is for **educational and research purposes**.
Not affiliated with Anthropic. Use at your own risk.

## 📝 Terms

Free to use, modify, and distribute. No warranty. No ownership claimed.
