# 🦞 CLAWPACK - Cross-Learning AI Agent Ecosystem

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black.svg)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## 🌟 Overview

Clawpack is a **cross-learning AI agent ecosystem** where multiple specialized agents share knowledge, learn from each other, and maintain persistent memory. Built with Python and powered by DeepSeek AI, Clawpack creates a collaborative intelligence system that grows over time.

### 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Cross-Learning Agents** | Agents share knowledge via shared SQLite database |
| 🌐 **Multi-Language Translation** | 20+ languages with Polyclaw |
| 🏥 **Medical Information** | Evidence-based medical knowledge with Mediclaw |
| 🔗 **Blockchain Expertise** | TX blockchain and RWA tokenization knowledge |
| 💾 **Persistent Memory** | Never lose learned information |
| 🔄 **Smart Routing** | Auto-selects best agent for each query |
| 📦 **Backup System** | Automatic and manual backups |
| 🚀 **Zero API Redundancy** | Cached answers reused across agents |

## 🤖 Agents

### Core Agents

| Agent | File | Purpose | Commands |
|-------|------|---------|----------|
| 🧠 **Unified Controller** | `agents/unified/unified_shared.py` | Smart router, general Q&A | Natural language |
| 🌐 **Polyclaw** | `agents/polyclaw/polyclaw_shared.py` | Translation (20+ languages) | `/to`, `/learn`, `/stats` |
| 🏥 **Mediclaw** | `agents/mediclaw/mediclaw_shared.py` | Medical information | `/ask`, `/homeo`, `/emergency` |
| 💾 **Knowledge Persistence** | `agents/knowledge/knowledge_persistence.py` | Backup & maintenance | Menu-driven |

### Additional Agents

| Agent | Directory | Purpose |
|-------|-----------|---------|
| 🦞 **Eagleclaw** | `agents/eagleclaw/` | Main AI assistant |
| 🔧 **Claw-coder** | `agents/claw-coder/` | Python AI assistant |
| 🐛 **Crustyclaw** | `agents/crustyclaw/` | Bug detection |
| 🦀 **Rustypycraw** | `agents/rustypycraw/` | Code generation |
| 💻 **Sysclaw** | `agents/sysclaw/` | System maintenance |
| ⚖️ **AgentForLaw** | `agents/agentforlaw/` | Legal assistance |
| 🔗 **TX-Agent** | `agents/tx-agent/` | TX blockchain |

### Agent Capabilities

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

# Optional: Local LLM with Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
ollama pull deepseek-coder:6.7b
Installation
bash
# Clone repository
git clone https://github.com/greg-gzillion/clawpack.git
cd clawpack

# Set up API key (get from https://openrouter.ai/keys)
export OPENROUTER_API_KEY="your-key-here"

# Run any agent
python agents/unified/unified_shared.py
📖 Usage Examples
1. Unified Controller - General Knowledge
bash
python agents/unified/unified_shared.py
text
❓ Ask me anything: What is the XRPL bridge?
🤖 [NEW - SAVED TO SHARED MEMORY]
The XRPL Bridge enables cross-chain transfers between XRP Ledger and other blockchains...
2. Polyclaw - Translation
bash
python agents/polyclaw/polyclaw_shared.py
text
🌐 Polyclaw> /to es "Smart Tokens on TX blockchain"
📝 TRANSLATION: "Tokens Inteligentes en la cadena de bloques TX"

🌐 Polyclaw> /stats
📊 SHARED LEARNING STATS:
  Total translations: 10
3. Mediclaw - Medical Information
bash
python agents/mediclaw/mediclaw_shared.py
text
🏥 Mediclaw> /ask What is diabetes?
📚 Diabetes is a chronic condition where blood sugar levels are too high...

🏥 Mediclaw> /homeo Arnica
🌿 Homeopathic remedy for trauma, bruising, and shock...

🏥 Mediclaw> /emergency chest pain
⚠️ URGENT: 'chest pain' - Call emergency services NOW!
4. Knowledge Persistence - Backup
bash
python agents/knowledge/knowledge_persistence.py
text
📊 KNOWLEDGE HEALTH:
  Medical entries: 7
  Translation entries: 10
  Latest backup: 2 days ago

📋 COMMANDS:
  1. Create backup
  2. Restore from backup
  3. Consolidate duplicates
  4. Export knowledge
📁 Repository Structure
text
clawpack/
├── agents/
│   ├── mediclaw/          # 🏥 Medical information agent
│   ├── polyclaw/          # 🌐 Translation agent
│   ├── unified/           # 🧠 Smart controller
│   ├── knowledge/         # 💾 Backup & persistence
│   ├── eagleclaw/         # 🦞 Main AI assistant
│   ├── claw-coder/        # 🔧 Python AI assistant
│   ├── crustyclaw/        # 🐛 Bug detection
│   ├── rustypycraw/       # 🦀 Code generation
│   ├── sysclaw/           # 💻 System maintenance
│   ├── agentforlaw/       # ⚖️ Legal assistance
│   └── tx-agent/          # 🔗 TX blockchain
├── docs/                  # 📚 Documentation
├── config/                # ⚙️ Configuration files
└── claw-shared/           # 🔄 Shared utilities
💾 Knowledge Base
All agents share a central SQLite database at ~/.claw_memory/shared_memory.db

Database Schema
sql
-- Medical knowledge from all agents
CREATE TABLE medical_knowledge (
    id INTEGER PRIMARY KEY,
    query TEXT UNIQUE,
    response TEXT,
    specialty TEXT,
    timestamp TEXT,
    source_agent TEXT,
    usage_count INTEGER DEFAULT 1
);

-- Translations cached from Polyclaw
CREATE TABLE translations (
    id INTEGER PRIMARY KEY,
    source_text TEXT,
    target_language TEXT,
    translated_text TEXT,
    source_agent TEXT,
    timestamp TEXT
);

-- TX Blockchain facts
CREATE TABLE tx_knowledge (
    id INTEGER PRIMARY KEY,
    topic TEXT UNIQUE,
    content TEXT,
    source TEXT
);
🔧 Configuration
API Key Setup
Get your free API key from OpenRouter

python
# In each agent file
CLOUD_API_KEY = "sk-or-v1-your-key-here"
Environment Variable (Optional)
bash
# Linux/Mac
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"

# Windows
set OPENROUTER_API_KEY=sk-or-v1-your-key-here
📊 Monitoring & Analytics
Quick Health Check
bash
python -c "
import sqlite3, os
db = os.path.expanduser('~/.claw_memory/shared_memory.db')
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM medical_knowledge')
print(f'Medical: {c.fetchone()[0]}')
c.execute('SELECT COUNT(*) FROM translations')
print(f'Translations: {c.fetchone()[0]}')
conn.close()
"
View All Knowledge
bash
# View all medical knowledge
python -c "
import sqlite3, os
db = os.path.expanduser('~/.claw_memory/shared_memory.db')
c = sqlite3.connect(db).cursor()
c.execute('SELECT query FROM medical_knowledge')
for row in c.fetchall():
    print(f'• {row[0]}')
"
🛠️ Troubleshooting
Issue	Solution
API Key Error	Check CLOUD_API_KEY in agent files
Database Locked	Close other agents, run knowledge persistence to repair
Translations not saving	Check write permissions to ~/.claw_memory/
Agent not learning	Verify shared memory path exists
🤝 Contributing
Contributions welcome! Please:

Fork the repository

Create a feature branch

Submit a pull request

Development Guidelines
Follow PEP 8

Use type hints

Document new functions

Maintain cross-learning compatibility

📄 License
MIT License - See LICENSE file for details

🙏 Acknowledgments
OpenRouter for AI API access

DeepSeek for language model

Ollama for local LLM support

📞 Support
Issues: GitHub Issues

Documentation: /docs folder

Examples: See usage examples above

🎯 Roadmap
Completed ✅
Cross-learning agent architecture

Shared SQLite memory

Translation agent (20+ languages)

Medical information agent

Backup and restore system

Knowledge persistence

In Progress 🚧
Web interface

REST API

Real-time collaboration

Planned 📅
Cloud backup (Google Drive, S3)

Knowledge version control (git)

More specialized agents

Docker deployment


## 📚 Citation

If you use LawClaw in your research, please cite it as:

### APA
> Frank, G. (2026). *Clawpack - Comprehensive Legal Reference System* (Version 3.0.0) [Computer software]. https://doi.org/10.5281/zenodo.19599131

### BibTeX
```bibtex
@software{frank_clawpack_2026,
  author       = {Greg Frank},
  title        = {Clawpack - Comprehensive Law Reference System},
  version      = {3.0.0},
  year         = {2026},
  doi          = {10.5281/zenodo.19599131},
  url          = {https://github.com/greg-gzillion/clawpack},
  abstract     = {Comprehensive legal reference system with 50+ practice areas and 8,000+ verified URLs}
}

