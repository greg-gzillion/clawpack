# 🦞 CrustyClaw

**Pure Rust AI Assistant - Fast, Memory-Safe, and Self-Contained**

[![Rust 1.70+](https://img.shields.io/badge/rust-1.70+-orange.svg)](https://www.rust-lang.org/)

## ✨ Features

- **⚡ Blazing Fast** - Pure Rust implementation for maximum performance
- **🦞 Pinch Mode** - Automatically detect unnecessary `.clone()` calls
- **🤖 Local AI** - Built-in Ollama integration (codellama:7b)
- **🔍 Code Search** - Fast pattern matching across your codebase
- **📊 Code Analysis** - Security audit and bug detection
- **🎯 CosmWasm Optimized** - Specialized for smart contract development

## 🚀 Quick Start

```bash
cargo build --release
./target/release/crustyclaw shell
./target/release/crustyclaw ask "What is the collateral mechanism?"
./target/release/crustyclaw pinch ~/dev/TX
```

## 🦞 Commands

| Command | Description |
|---------|-------------|
| `ask <question>` | Ask AI about your code |
| `pinch <path>` | Analyze code for bugs and optimizations |
| `audit <path>` | Security audit of codebase |
| `shell` | Interactive lobster-themed shell |
| `status` | Show system status |
| `prices` | Show metal prices (PhoenixPME) |
| `claw` | Display the lobster |
| `molt` | Self-upgrade |

## 🔧 Requirements

- Rust 1.70+
- Ollama (for AI features)

## 🤝 Related Projects

- **[rustypycraw](https://github.com/greg-gzillion/rustypycraw)** - Hybrid Rust+Python code crawler
- **[claw-coder](https://github.com/greg-gzillion/claw-coder)** - Python AI assistant
- **[eagleclaw](https://github.com/greg-gzillion/eagleclaw)** - Full claw-code port

## ⚠️ Disclaimer

This software is a **clean-room reimplementation** based on publicly observable behavior.
**No proprietary source code is included.**

This project is for **educational and research purposes**. Not affiliated with Anthropic.

## 📝 Terms

Free to use, modify, and distribute. No warranty. No ownership claimed.

## License

Free to use. No ownership claimed.
