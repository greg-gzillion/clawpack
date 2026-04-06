# 🦞 The Claw Ecosystem - How All Agents Work Together

## Overview

Five specialized AI agents share memory and work together as a unified system.

## The Five Agents

| Agent | Purpose | Repository |
|-------|---------|------------|
| **agentforlaw** | Law study, contracts, wills, statutes, constitution | agentforlaw |
| **rustypycraw** | Code generation (8+ languages) | rustypycraw |
| **eagleclaw** | AI coding assistant | eagleclaw |
| **crustyclaw** | Bug detection, pinch mode | crustyclaw |
| **claw-coder** | Python AI with Groq | claw-coder |

## AI Model Providers

All agents support multiple AI backends.

### Supported Providers

| Provider | Type | Speed | Cost | Best For |
|----------|------|-------|------|----------|
| **Groq** | Cloud | 1-2 sec | Free | Fast legal analysis |
| **Ollama** | Local | 30-120 sec | Free | Privacy, offline |
| **Local Models** | Local | Varies | Free | Custom models |

### Available Models

**Groq (Cloud)**
- `llama-3.3-70b-versatile` - Best for legal reasoning
- `llama-3.1-8b-instant` - Fast, good for definitions

**Ollama (Local)**
- `codellama:7b` - Legal document analysis
- `deepseek-coder:6.7b` - Best for contracts
- `llama3.2:3b` - Fastest local option

### Setup

**Groq (Recommended for Speed)**
```bash
export GROQ_API_KEY="your-api-key-here"
python agentforlaw.py --analyze "What is consideration?" --groq
Ollama (For Privacy)

bash
Which Agents Use AI
Agent	AI Features	Provider Support
agentforlaw	Legal analysis	Groq, Ollama
rustypycraw	Code generation	Groq, Ollama
eagleclaw	General assistance	Groq, Ollama
crustyclaw	Bug explanations	Groq, Ollama
claw-coder	Python AI tasks	Groq only
No API Key? No Problem
Without AI, AgentForLaw still works for:

Statute lookup (--statute)

Constitution access (--constitution)

Document drafting (--draft-contract, --draft-will)

Clause library (--clause)

Definitions (--define)

Shared memory (--remember, --recall)

Only --analyze requires an AI provider.

Shared Memory System
All agents share memory via ~/.claw_memory/shared_memory.db

Shared Memory Commands (All Agents)
Command	Purpose
--remember KEY VALUE	Store in shared memory
--recall KEY	Retrieve from shared memory
--agents	List all registered agents
Installation
Clone All Agents
bash
mkdir -p ~/claw-ecosystem
cd ~/claw-ecosystem

git clone https://github.com/greg-gzillion/agentforlaw.git
git clone https://github.com/greg-gzillion/rustypycraw.git
git clone https://github.com/greg-gzillion/eagleclaw.git
git clone https://github.com/greg-gzillion/crustyclaw.git
git clone https://github.com/greg-gzillion/claw-coder.git
How Agents Work Together
Example 1: Law Research → Code Generation
bash
# Step 1: AgentForLaw researches law
cd agentforlaw
python agentforlaw.py --remember "securities_rule" "SEC v. Ripple - XRP not a security"

# Step 2: RustyPyCraw reads law and generates code
cd ../rustypycraw
./rustypycraw --recall "securities_rule"
./rustypycraw --polyglot rust "SEC compliant token"
Example 2: Contract Drafting for Families
bash
# Draft a will
cd agentforlaw
python agentforlaw.py --draft-will --parties '{"name":"John Smith"}' --provisions '{"executor":"Mary Smith","beneficiary":"my children"}'

# Draft a living will
python agentforlaw.py --draft-estate living_will --parties '{"declarant":"John Smith"}'

# Draft healthcare directive
python agentforlaw.py --draft-estate healthcare_directive --parties '{"principal":"John Smith"}' --provisions '{"agent":"Mary Smith"}'

# Draft power of attorney
python agentforlaw.py --draft-estate power_of_attorney --parties '{"principal":"John Smith"}' --provisions '{"agent":"Mary Smith"}'

# Draft a lease agreement
python agentforlaw.py --draft-contract lease --parties '{"landlord":"John Smith","tenant":"Jane Doe"}' --provisions '{"premises":"123 Main St","rent":"$2,000/mo","term":"12 months"}'
Example 3: Legal Question → AI Answer
bash
# Store legal principle
cd agentforlaw
python agentforlaw.py --remember "due_process" "5th and 14th Amendments guarantee due process"

# AI analysis using Groq
python agentforlaw.py --analyze "What is due process in contract law?" --groq

# AI analysis using local Ollama
AgentForLaw Commands (Law Agent)
Command	Purpose
--statute "15 USC 78a"	Look up US Code
--cfr "17 CFR 240.10b-5"	Look up regulation
--case "Marbury v Madison"	Search case law
--constitution --article 1 --section 8	Read Constitution
--constitution --amendment 1	Read Amendment
--draft-contract service	Draft service contract
--draft-contract lease	Draft lease agreement
--draft-contract employment	Draft employment contract
--draft-will	Draft last will
--draft-trust	Draft living trust
--draft-estate power_of_attorney	Draft POA
--draft-estate healthcare_directive	Draft healthcare directive
--draft-estate living_will	Draft living will
--clause indemnification	Get contract clause
--define consideration	Define legal term
--analyze "question" --groq	AI legal analysis
--agencies	List agencies
--domains	List law domains
--remember KEY VALUE	Store in shared memory
--recall KEY	Retrieve from memory
--agents	See other agents
RustyPyCraw Commands (Code Agent)
Command	Purpose
--polyglot rust ContractName	Generate Rust code
--polyglot typescript Component	Generate TypeScript
--polyglot solidity Contract	Generate Solidity
--pinch ~/project	Find unnecessary clones
--search pattern	Search codebase
--stats	Code statistics
--recall KEY	Read from shared memory
Quick Start - One Command Test
bash
# 1. Set up AI (optional)
export GROQ_API_KEY="your-key"

# 2. Test shared memory across agents
cd agentforlaw
python agentforlaw.py --remember "test" "Ecosystem working"
python agentforlaw.py --recall "test"
python agentforlaw.py --agents

# 3. Draft a document
python agentforlaw.py --draft-will --parties '{"name":"Test"}' --provisions '{"executor":"Executor","beneficiary":"Family"}'

# 4. Test AI analysis (if Groq configured)
python agentforlaw.py --analyze "What is contract consideration?" --groq
Testing AI Setup
bash
# List available models
python agentforlaw.py --list-models

# Should show:
# groq/llama-3.3-70b-versatile
# groq/llama-3.1-8b-instant
Troubleshooting
Shared Memory Not Working
bash
# Check if database exists
ls ~/.claw_memory/

# Manually create directory
mkdir -p ~/.claw_memory
Agent Not Seeing Other Agents
bash
# Register agent manually
python agentforlaw.py --agents
# Should show registered agents
AI Not Working
bash
# Check Groq API key
echo $GROQ_API_KEY

# Test Ollama

# List available models
python agentforlaw.py --list-models
Directory Structure After Installation
text
~/claw-ecosystem/
├── agentforlaw/          # Law agent
├── rustypycraw/          # Code generation agent
├── eagleclaw/            # AI assistant agent
├── crustyclaw/           # Bug detection agent
└── claw-coder/           # Python AI agent

~/.claw_memory/
└── shared_memory.db      # Shared database (auto-created)
Use Cases Summary
For Families
Draft living wills with --draft-estate living_will

Create healthcare directives with --draft-estate healthcare_directive

Establish powers of attorney with --draft-estate power_of_attorney

Draft last wills with --draft-will

Create living trusts with --draft-trust

For Landlords & Tenants
Draft lease agreements with --draft-contract lease

Create rental terms and conditions

For Small Business Owners
Draft service contracts with --draft-contract service

Create employment agreements with --draft-contract employment

Generate partnership agreements with --draft-contract partnership

For Developers
Generate smart contracts with rustypycraw

Research securities law with agentforlaw

Audit code with crustyclaw

Support
GitHub Issues: https://github.com/greg-gzillion/agentforlaw/issues

Discord: https://discord.gg/claw-ecosystem

License
See DISCLAIMER file - Clean-room implementation, no ownership claimed.

