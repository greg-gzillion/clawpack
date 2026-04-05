# 🦞 CLAWPACK - Cross-Learning AI Agent Ecosystem

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## 🌟 Overview

Clawpack is a **cross-learning AI agent ecosystem** where multiple specialized agents share knowledge, learn from each other, and maintain persistent memory. Built with Python and powered by DeepSeek AI, Clawpack creates a collaborative intelligence system that grows over time.

### 🎯 Key Features

- **🧠 Cross-Learning Agents** - Agents share knowledge via shared SQLite database
- **🌐 Multi-Language Translation** - 20+ languages with Polyclaw
- **🏥 Medical Information** - Evidence-based medical knowledge with Mediclaw
- **🔗 Blockchain Expertise** - TX blockchain and RWA tokenization knowledge
- **💾 Persistent Memory** - Never lose learned information
- **🔄 Smart Routing** - Auto-selects best agent for each query
- **📦 Backup System** - Automatic and manual backups
- **🚀 Zero API Redundancy** - Cached answers reused across agents

## 🤖 Agents

### Core Agents

| Agent | File | Purpose | Commands |
|-------|------|---------|----------|
| 🦞 **Unified Controller** | `unified_shared.py` | Smart router, general Q&A | Natural language |
| 🌐 **Polyclaw** | `polyclaw_shared.py` | Translation (20+ languages) | `/to`, `/learn`, `/stats` |
| 🏥 **Mediclaw** | `mediclaw_shared.py` | Medical information | `/ask`, `/homeo`, `/emergency` |
| 💾 **Knowledge Persistence** | `knowledge_persistence.py` | Backup & maintenance | Menu-driven |
| 🦞 **Eagleclaw** | `chat_with_agent.py` | Main AI assistant | Natural language |
| 🔧 **Claw-coder** | Integrated | Python AI assistant | Code generation |
| 🐛 **Crustyclaw** | Integrated | Bug detection | Code analysis |
| 🦀 **Rustypycraw** | Integrated | Code generation | Python/CLI |
| 💻 **Sysclaw** | Integrated | Local machine maintenance | System commands |

### Agent Capabilities Matrix

| Agent | Reads Shared Memory | Writes Shared Memory | API Calls | Cache |
|-------|--------------------|---------------------|-----------|-------|
| Unified Controller | ✅ | ✅ | ✅ (fallback) | ✅ |
| Polyclaw | ✅ | ✅ | ✅ (first time) | ✅ |
| Mediclaw | ✅ | ✅ | ✅ (first time) | ✅ |
| Eagleclaw | ✅ | ✅ | ✅ | ✅ |
| Knowledge Persistence | ✅ | ❌ | ❌ | N/A |

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.12 or higher
python --version

# Required packages
pip install requests
pip install sqlite3  # Built-in

# Optional: Local LLM with Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
ollama pull deepseek-coder:6.7b

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)

## 🌟 Overview

Clawpack is a **cross-learning AI agent ecosystem** where multiple specialized agents share knowledge, learn from each other, and maintain persistent memory. Built with Python and powered by DeepSeek AI, Clawpack creates a collaborative intelligence system that grows over time.

### 🎯 Key Features

- **🧠 Cross-Learning Agents** - Agents share knowledge via shared SQLite database
- **🌐 Multi-Language Translation** - 20+ languages with Polyclaw
- **🏥 Medical Information** - Evidence-based medical knowledge with Mediclaw
- **🔗 Blockchain Expertise** - TX blockchain and RWA tokenization knowledge
- **💾 Persistent Memory** - Never lose learned information
- **🔄 Smart Routing** - Auto-selects best agent for each query
- **📦 Backup System** - Automatic and manual backups
- **🚀 Zero API Redundancy** - Cached answers reused across agents

## 🤖 Agents

### 1. 🦞 Unified Controller (`unified_shared.py`)
**Smart router that coordinates all agents**

```bash
python unified_shared.py