\# 🔧 CLAWPACK - Complete Setup Guide



\## 📋 Table of Contents

1\. \[Prerequisites](#prerequisites)

2\. \[Quick Installation](#quick-installation)

3\. \[LLM Provider Setup](#llm-provider-setup)

4\. \[API Key Configuration](#api-key-configuration)

5\. \[Ollama Setup (Local LLM)](#ollama-setup-local-llm)

6\. \[Verification](#verification)

7\. \[Troubleshooting](#troubleshooting)



\---



\## Prerequisites



\### System Requirements

| Component | Minimum | Recommended |

|-----------|---------|-------------|

| \*\*CPU\*\* | 4 cores | 8+ cores |

| \*\*RAM\*\* | 8 GB | 16-32 GB |

| \*\*Storage\*\* | 20 GB | 100+ GB (for models) |

| \*\*Python\*\* | 3.10+ | 3.12 |

| \*\*OS\*\* | Windows/Linux/Mac | Any |



\### Required Software

```bash

\# Python 3.10+

python --version



\# Git

git --version



\# pip

pip --version

Quick Installation

Step 1: Clone Repository

bash

git clone https://github.com/greg-gzillion/clawpack.git

cd clawpack

Step 2: Install Python Dependencies

bash

pip install -r requirements.txt

Step 3: Choose Your LLM Provider

Option A: Cloud Only (No Local Setup)



Get free API key from OpenRouter



Skip Ollama installation



Option B: Local Only (No Internet Required)



Install Ollama (see below)



No API keys needed



Option C: Hybrid (Recommended)



Both cloud and local LLMs



Automatic fallback if internet fails



LLM Provider Setup

🟢 OpenRouter (Primary - Recommended)

Free tier available!



Sign up: https://openrouter.ai/



Get API key: Dashboard → API Keys



Add credits (optional, $5 gets you started)



Set environment variable:



bash

\# Windows

set OPENROUTER\_API\_KEY=sk-or-v1-your-key-here



\# Linux/Mac

export OPENROUTER\_API\_KEY="sk-or-v1-your-key-here"



\# Or use .env file (copy from .env.example)

cp .env.example .env

\# Edit .env and add your key

Available Models (200+):



deepseek/deepseek-chat (default, free)



openai/gpt-4o (paid)



anthropic/claude-3.5-sonnet (paid)



google/gemini-2.0-flash (free tier)



meta-llama/llama-3.3-70b-instruct (free)



🟡 Groq (Fastest Inference)

Free tier available!



Sign up: https://console.groq.com/



Get API key: API Keys → Create API Key



Set environment variable:



bash

export GROQ\_API\_KEY="gsk\_your-key-here"

Features:



Lightning fast (50-100ms responses)



30 requests/minute free



Best for: Real-time applications



🔵 DeepSeek (Code-Specialized)

Very affordable!



Sign up: https://platform.deepseek.com/



Get API key: API Keys



Set environment variable:



bash

export DEEPSEEK\_API\_KEY="your-key-here"

Features:



$0.14 per 1M tokens



Excellent for code generation



1M tokens free to start



🟣 OpenAI (Optional)

bash

export OPENAI\_API\_KEY="sk-your-key-here"

🔴 Anthropic Claude (Optional)

bash

export ANTHROPIC\_API\_KEY="sk-ant-your-key-here"

🟠 Cohere (Optional)

bash

export COHERE\_API\_KEY="your-key-here"

🟤 Together AI (Optional)

bash

export TOGETHER\_API\_KEY="your-key-here"

⚪ Mistral AI (Optional)

bash

export MISTRAL\_API\_KEY="your-key-here"

🔵 Google Gemini (Optional)

bash

export GOOGLE\_API\_KEY="your-key-here"

Ollama Setup (Local LLM)

Windows Installation

Download: https://ollama.com/download/windows



Run installer (OllamaSetup.exe)



Verify installation:



powershell

ollama --version

Linux Installation

bash

curl -fsSL https://ollama.com/install.sh | sh

Mac Installation

bash

curl -fsSL https://ollama.com/install.sh | sh

Start Ollama Service

bash

\# Ollama usually starts automatically

\# If not, run:

ollama serve



\# Verify it's running

curl http://localhost:11434/api/tags

Pull Required Models

bash

\# Minimal setup (2-5 GB)

ollama pull llama3.2:3b

ollama pull deepseek-coder:6.7b



\# Full setup (80+ GB - all 10 models)

ollama pull qwen3-vl:30b        # 19GB - Vision

ollama pull qwen3-coder:30b     # 18GB - Code

ollama pull gemma3:27b          # 17GB - General

ollama pull gemma3:12b          # 8GB - Balanced

ollama pull deepseek-r1:8b      # 5GB - Reasoning

ollama pull gemma3:4b           # 3GB - Fast

ollama pull codellama:7b        # 4GB - Code

ollama pull deepseek-coder:6.7b # 4GB - Code

ollama pull llama3.2:3b         # 2GB - Lightweight

ollama pull gemma3:1b           # 815MB - Ultra-fast

Recommended Models by Use Case

Use Case	Recommended Model	Size	Speed

Medical advice	gemma3:27b	17GB	Slow

Legal research	gemma3:27b	17GB	Slow

Code generation	qwen3-coder:30b	18GB	Slow

Fast responses	llama3.2:3b	2GB	Fast

Vision tasks	qwen3-vl:30b	19GB	Slow

Balanced use	gemma3:12b	8GB	Medium

Ultra-fast	gemma3:1b	815MB	Lightning

API Key Configuration

Method 1: Environment Variables (Recommended)

Windows (Command Prompt):



cmd

set OPENROUTER\_API\_KEY=sk-or-v1-your-key-here

set GROQ\_API\_KEY=gsk\_your-key-here

Windows (PowerShell):



powershell

$env:OPENROUTER\_API\_KEY="sk-or-v1-your-key-here"

$env:GROQ\_API\_KEY="gsk\_your-key-here"

Linux/Mac:



bash

export OPENROUTER\_API\_KEY="sk-or-v1-your-key-here"

export GROQ\_API\_KEY="gsk\_your-key-here"

Method 2: .env File (Persistent)

bash

\# Copy template

cp .env.example .env



\# Edit with your keys (using any text editor)

nano .env  # Linux/Mac

notepad .env  # Windows

.env file example:



ini

\# Required for cloud AI

OPENROUTER\_API\_KEY=sk-or-v1-your-actual-key-here

GROQ\_API\_KEY=gsk\_your-actual-key-here

DEEPSEEK\_API\_KEY=your-actual-key-here



\# Optional providers

OPENAI\_API\_KEY=sk-your-key-here

ANTHROPIC\_API\_KEY=sk-ant-your-key-here

COHERE\_API\_KEY=your-key-here

TOGETHER\_API\_KEY=your-key-here

MISTRAL\_API\_KEY=your-key-here

GOOGLE\_API\_KEY=your-key-here



\# Ollama (local - no key needed)

OLLAMA\_HOST=http://localhost:11434



\# System settings

LOG\_LEVEL=INFO

DEFAULT\_LLM=openrouter

Method 3: Direct in Code (Not Recommended for Production)

Edit agent files directly:



python

\# In unified\_shared.py

CLOUD\_API\_KEY = "sk-or-v1-your-key-here"  # Not recommended!

Verification

Test 1: Check Python Environment

bash

python --version

pip list | findstr requests  # Windows

pip list | grep requests     # Linux/Mac

Test 2: Test API Keys

bash

\# Test OpenRouter

python -c "

import os, requests

key = os.getenv('OPENROUTER\_API\_KEY')

if key:

&#x20;   r = requests.post('https://openrouter.ai/api/v1/auth/key',

&#x20;                     headers={'Authorization': f'Bearer {key}'})

&#x20;   print('✅ OpenRouter valid' if r.status\_code == 200 else '❌ Invalid')

else:

&#x20;   print('❌ OPENROUTER\_API\_KEY not set')

"



\# Test Groq

python -c "

import os, requests

key = os.getenv('GROQ\_API\_KEY')

if key:

&#x20;   r = requests.get('https://api.groq.com/openai/v1/models',

&#x20;                    headers={'Authorization': f'Bearer {key}'})

&#x20;   print('✅ Groq valid' if r.status\_code == 200 else '❌ Invalid')

else:

&#x20;   print('❌ GROQ\_API\_KEY not set')

"

Test 3: Test Ollama

bash

\# Check Ollama is running

curl http://localhost:11434/api/tags



\# Test a model

ollama run llama3.2:3b "Hello, are you working?"

Test 4: Test Clawpack Agent

bash

\# Run Unified Controller

python agents/unified/unified\_shared.py



\# Should see welcome message

\# Type: What is artificial intelligence?

\# Should get response

Test 5: Run Full Model Test

bash

\# Test all 10 Ollama models

python test\_all\_models.py

Troubleshooting

Common Issues and Solutions

Issue	Solution

"Module not found: requests"	Run pip install requests

"OPENROUTER\_API\_KEY not set"	Set environment variable or create .env file

"Ollama connection refused"	Run ollama serve in separate terminal

"Model not found"	Run ollama pull \[model-name]

"Port 11434 already in use"	Ollama is already running (that's fine!)

"API rate limit exceeded"	Wait or upgrade to paid tier

"Insufficient memory for model"	Use smaller model (gemma3:4b or llama3.2:3b)

"Database locked"	Close other agents, run knowledge persistence

Windows-Specific Issues

PowerShell execution policy:



powershell

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Long path errors:



powershell

\# Enable long paths

New-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

Linux/Mac-Specific Issues

Permission denied:



bash

chmod +x \*.sh

Ollama not in PATH:



bash

\# Add to \~/.bashrc or \~/.zshrc

export PATH=$PATH:/usr/local/bin

Quick Start Commands

Minimum Setup (5 minutes)

bash

\# 1. Clone

git clone https://github.com/greg-gzillion/clawpack.git

cd clawpack



\# 2. Install dependencies

pip install -r requirements.txt



\# 3. Set API key (get from https://openrouter.ai/keys)

export OPENROUTER\_API\_KEY="sk-or-v1-your-key-here"



\# 4. Run agent

python agents/unified/unified\_shared.py

Full Setup (30 minutes)

bash

\# 1. Clone and install

git clone https://github.com/greg-gzillion/clawpack.git

cd clawpack

pip install -r requirements.txt



\# 2. Set up all API keys

cp .env.example .env

nano .env  # Add your keys



\# 3. Install Ollama

curl -fsSL https://ollama.com/install.sh | sh



\# 4. Pull models

ollama pull llama3.2:3b

ollama pull deepseek-coder:6.7b



\# 5. Test everything

python test\_all\_models.py

python agents/unified/unified\_shared.py

Support

GitHub Issues: https://github.com/greg-gzillion/clawpack/issues



Documentation: /docs folder



Examples: See README.md





\### \*\*2. Update README.md with Setup Links\*\*



```powershell

\# Add setup section to README

$readmeUpdate = @"



\## 🚀 Quick Setup (5 minutes)



\### Minimal Setup

```bash

\# 1. Clone repository

git clone https://github.com/greg-gzillion/clawpack.git

cd clawpack



\# 2. Install dependencies

pip install -r requirements.txt



\# 3. Get free API key from https://openrouter.ai/keys

export OPENROUTER\_API\_KEY="sk-or-v1-your-key-here"



\# 4. Run any agent

python agents/unified/unified\_shared.py

Full Setup (30 minutes)

For complete setup with 10 local LLM models + 200+ cloud models:

👉 Full Setup Guide



📚 Documentation

Document	Description

SETUP.md	Complete installation \& configuration guide

API.md	API reference and programmatic usage

AGENTS.md	Detailed agent documentation

LLM\_README.md	LLM provider configuration

SECURITY.md	Security policies and practices

🎯 Quick Commands

bash

\# Run Unified Controller (general Q\&A)

python agents/unified/unified\_shared.py



\# Run Polyclaw (translation)

python agents/polyclaw/polyclaw\_shared.py



\# Run Mediclaw (medical info)

python agents/mediclaw/mediclaw\_shared.py



\# Run AgentForLaw (legal research)

python agents/agentforlaw/agentforlaw.py



\# Test all Ollama models

python test\_all\_models.py



\# Check system health

python agents/knowledge/knowledge\_persistence.py

"@



Append to README if not already present

$currentReadme = Get-Content "README.md" -Raw

if ($currentReadme -notmatch "Quick Setup") {

Add-Content -Path "README.md" -Value $readmeUpdate

Write-Host "✅ Updated README.md with setup section" -ForegroundColor Green

}



text



\### \*\*3. Create QUICKREF.md - Quick Reference Card\*\*



```powershell

$quickref = @"

\# 🚀 CLAWPACK Quick Reference Card



\## One-Line Setup

```bash

git clone https://github.com/greg-gzillion/clawpack.git \&\& cd clawpack \&\& pip install -r requirements.txt \&\& export OPENROUTER\_API\_KEY="sk-or-v1-your-key-here" \&\& python agents/unified/unified\_shared.py

Essential Commands

Installation

Command	Purpose

pip install -r requirements.txt	Install dependencies

cp .env.example .env	Create environment file

ollama pull llama3.2:3b	Download local model

Running Agents

Command	Agent

python agents/unified/unified\_shared.py	General Q\&A

python agents/polyclaw/polyclaw\_shared.py	Translation

python agents/mediclaw/mediclaw\_shared.py	Medical

python agents/agentforlaw/agentforlaw.py	Legal

python agents/webclaw/webclaw.py	Reference

API Keys (Get Free)

Provider	URL	Command

OpenRouter	https://openrouter.ai/keys	export OPENROUTER\_API\_KEY=...

Groq	https://console.groq.com/keys	export GROQ\_API\_KEY=...

DeepSeek	https://platform.deepseek.com/	export DEEPSEEK\_API\_KEY=...

Ollama Commands

Command	Purpose

ollama list	List installed models

ollama pull \[model]	Download model

ollama run \[model]	Test model

ollama serve	Start service

Verification

bash

\# Test API keys

python -c "import os; print('✅' if os.getenv('OPENROUTER\_API\_KEY') else '❌')"



\# Test Ollama

curl http://localhost:11434/api/tags



\# Test all models

python test\_all\_models.py

Troubleshooting

Problem	Fix

"Module not found"	pip install -r requirements.txt

"API key not set"	export OPENROUTER\_API\_KEY=...

"Ollama not running"	ollama serve

"Port in use"	Already running (ignore)

Need Help?

Full Setup: SETUP.md



API Docs: API.md



Issues: https://github.com/greg-gzillion/clawpack/issues

"@



$quickref | Out-File -FilePath "QUICKREF.md" -Encoding UTF8

Write-Host "✅ Created QUICKREF.md - Quick reference card" -ForegroundColor Green



text



\### \*\*4. Update Requirements.txt with All Dependencies\*\*



```powershell

$requirements = @"

\# Core dependencies

requests>=2.31.0

sqlite3



\# Optional: Cloud APIs

openai>=1.0.0

anthropic>=0.18.0

groq>=0.4.0

cohere>=4.37.0

together>=0.2.0



\# Local LLM

\# Ollama is installed separately



\# Utilities

python-dotenv>=1.0.0

colorama>=0.4.6



\# Web framework (for future API)

\# fastapi>=0.104.0

\# uvicorn>=0.24.0

"@



$requirements | Out-File -FilePath "requirements.txt" -Encoding UTF8

Write-Host "✅ Updated requirements.txt" -ForegroundColor Green

5\. Create INSTALL.sh for Linux/Mac

bash

$installScript = @'#!/bin/bash



\# Clawpack Installation Script

echo "🦞 Installing Clawpack..."



\# Check Python

if ! command -v python3 \&> /dev/null; then

&#x20;   echo "❌ Python 3 not found. Please install Python 3.10+"

&#x20;   exit 1

fi



\# Install dependencies

echo "📦 Installing Python packages..."

pip3 install -r requirements.txt



\# Check for Ollama

if ! command -v ollama \&> /dev/null; then

&#x20;   echo "⚠️ Ollama not found. Installing..."

&#x20;   curl -fsSL https://ollama.com/install.sh | sh

fi



\# Create .env if not exists

if \[ ! -f .env ]; then

&#x20;   cp .env.example .env

&#x20;   echo "✅ Created .env file. Edit it to add your API keys."

fi



echo ""

echo "🎉 Installation complete!"

echo ""

echo "Next steps:"

echo "1. Get API key: https://openrouter.ai/keys"

echo "2. Add to .env: OPENROUTER\_API\_KEY=your-key"

echo "3. Run: python agents/unified/unified\_shared.py"

'@



$installScript | Out-File -FilePath "install.sh" -Encoding UTF8

Write-Host "✅ Created install.sh" -ForegroundColor Green

6\. Create INSTALL.ps1 for Windows

powershell

$installPs1 = @'

\# Clawpack Installation Script for Windows

Write-Host "🦞 Installing Clawpack..." -ForegroundColor Cyan



\# Check Python

try {

&#x20;   $pythonVersion = python --version

&#x20;   Write-Host "✅ $pythonVersion" -ForegroundColor Green

} catch {

&#x20;   Write-Host "❌ Python not found. Please install Python 3.10+" -ForegroundColor Red

&#x20;   exit 1

}



\# Install dependencies

Write-Host "`n📦 Installing Python packages..." -ForegroundColor Yellow

pip install -r requirements.txt



\# Create .env if not exists

if (-not (Test-Path ".env")) {

&#x20;   Copy-Item ".env.example" ".env"

&#x20;   Write-Host "✅ Created .env file. Edit it to add your API keys." -ForegroundColor Green

}



Write-Host "`n🎉 Installation complete!" -ForegroundColor Green

Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow

Write-Host "1. Get API key: https://openrouter.ai/keys" -ForegroundColor White

Write-Host "2. Add to .env: OPENROUTER\_API\_KEY=your-key" -ForegroundColor White

Write-Host "3. Run: python agents/unified/unified\_shared.py" -ForegroundColor White

'@



$installPs1 | Out-File -FilePath "install.ps1" -Encoding UTF8

Write-Host "✅ Created install.ps1" -ForegroundColor Green

📚 FINAL DOCUMENTATION SUMMARY

File	Purpose	Audience

SETUP.md	Complete installation guide	All users

QUICKREF.md	One-page quick reference	Experienced users

README.md	Project overview + quick start	Everyone

API.md	Programmatic usage	Developers

AGENTS.md	Agent details	Users

LLM\_README.md	LLM configuration	Power users

install.sh	Auto-install script	Linux/Mac

install.ps1	Auto-install script	Windows

requirements.txt	Python dependencies	All

