# ⚖️ AGENT FOR LAW

**An agent that studies, understands, and applies LAW 

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Law](https://img.shields.io/badge/domain-LAW-red.svg)]()
[![Courts](https://img.shields.io/badge/courts-Federal%20%26%20State-green.svg)]()
[![Memory](https://img.shields.io/badge/memory-Shared-purple.svg)]()

---

## 📜 WHAT IS AGENT FOR LAW?

**AgentForLaw is an agent OF law, not an agent FOR legal practice.**

| Concept | Meaning | AgentForLaw Role |
|---------|---------|------------------|
| **LAW** | Statutes, codes, regulations, constitutions, case law | ✅ STUDIES AND APPLIES |
| **LEGAL** | Practice, profession, lawyers, courts, advice | ❌ DOES NOT PRACTICE |

---

## 🔧 SETUP

### 1. Install Dependencies

```bash
cd agentforlaw
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
2. Get a Groq API Key
Go to Groq Console

Sign up for a free account

Navigate to API Keys

Click Create API Key

Copy the key (starts with gsk_)

3. Configure Environment
bash
# Create .env file with your API key
echo "GROQ_API_KEY=gsk_your_key_here" > .env

# Or set as environment variable
export GROQ_API_KEY="gsk_your_key_here"
4. Run the API Server
bash
python3 api.py
The API will run at http://localhost:8000

5. (Optional) Deploy Publicly with ngrok
bash
# Install ngrok
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com bookworm main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok -y

# Add your authtoken (get from https://dashboard.ngrok.com)
ngrok config add-authtoken YOUR_TOKEN_HERE

# Start tunnel (keep API running in another terminal)
ngrok http 8000
Your API will be publicly accessible at https://your-subdomain.ngrok-free.dev

6. Install CLI Wrapper (Optional)
bash
cat > ~/.local/bin/claw-law << 'EOF'
#!/bin/bash
API_URL="${CLAW_LAW_API:-http://localhost:8000}"
curl -s -X POST "$API_URL/analyze" -H "Content-Type: application/json" -d "{\"question\": \"$*\"}" | jq -r '.answer'
EOF
chmod +x ~/.local/bin/claw-law

# Use it anywhere
claw-law "What is the 4th Amendment?"
🔑 Environment Variables
Variable	Purpose	Default
GROQ_API_KEY	Groq API key (required)	None
CLAW_LAW_API	API URL for CLI wrapper	http://localhost:8000
🌐 Public Deployment Options
Option	Command	Use Case
ngrok	ngrok http 8000	Quick testing, temporary sharing
Cloudflare Tunnel	cloudflared tunnel --url localhost:8000	Free, stable
VPS (DigitalOcean, Linode)	Deploy with systemd	Permanent production
🧪 Testing Your Setup
bash
# Test local API
curl http://localhost:8000/

# Test analyze endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the 4th Amendment?"}'

# Test with ngrok (if deployed)
curl -X POST https://your-subdomain.ngrok-free.dev/analyze \
  -H "Content-Type: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -d '{"question": "What is the 1st Amendment?"}'
🐳 Docker Deployment (Alternative)
dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api.py"]
bash
docker build -t agentforlaw .
docker run -p 8000:8000 -e GROQ_API_KEY="gsk_xxx" agentforlaw
📋 Requirements File
Create requirements.txt:

bash
cat > requirements.txt << 'EOF'
fastapi==0.115.0
uvicorn==0.30.0
groq==0.9.0
python-dotenv==1.0.0
httpx==0.27.0
pydantic==2.9.0
EOF
Then install:

bash
pip install -r requirements.txt
text

Save (`Ctrl+O`, `Enter`, `Ctrl+X`).

---

## 📤 Commit and Push

```bash
cd /home/greg/dev/agentforlaw
git add README.md
git commit -m "Add comprehensive setup instructions

- Groq API key configuration
- Environment setup with .env
- ngrok deployment guide
- CLI wrapper installation
- Docker deployment option
- Requirements.txt instructions
- Testing commands"
git push origin main
✅ What's Now Documented
Section	What It Covers
Setup	Virtual env, dependencies, API key
Groq	How to get and configure API key
ngrok	Installation, authtoken, public deployment
CLI wrapper	claw-law command installation
Environment variables	GROQ_API_KEY, CLAW_LAW_API
Testing	Local and ngrok test commands
Docker	Alternative deployment method
Requirements	Full dependency list

```

## 📝 DRAFTING DOCUMENTS USING LAW

### Contracts (Contract Law & UCC)

```bash
python agentforlaw.py --draft-contract service --parties '{"party_a":"Acme","party_b":"Jane"}' --provisions '{"services":"consulting","payment":"$5k"}'
python agentforlaw.py --draft-contract sale --parties '{"seller":"Acme","buyer":"Jane"}' --provisions '{"goods":"widgets","price":"$1k"}'
python agentforlaw.py --draft-contract employment --parties '{"employer":"Acme","employee":"Jane"}' --provisions '{"position":"Engineer","salary":"$120k"}'
```

### Wills (Probate Law)

```bash
python agentforlaw.py --draft-will --parties '{"name":"John Smith"}' --provisions '{"executor":"Mary Smith","beneficiary":"my children"}'
```

### Trusts (Trust Law)

```bash
python agentforlaw.py --draft-trust --parties '{"name":"John Smith"}' --provisions '{"trustee":"First Bank","beneficiaries":"my children"}'
```

### Estate Documents (Agency & Health Law)

```bash
python agentforlaw.py --draft-estate power_of_attorney --parties '{"principal":"John"}' --provisions '{"agent":"Mary"}'
python agentforlaw.py --draft-estate healthcare_directive --parties '{"principal":"John"}' --provisions '{"agent":"Mary"}'
python agentforlaw.py --draft-estate living_will --parties '{"declarant":"John"}'
```

---

## 🔍 LAW RESEARCH

```bash
python agentforlaw.py --statute "15 USC 78a"
python agentforlaw.py --case "Marbury v Madison"
python agentforlaw.py --agencies
python agentforlaw.py --agency sec
python agentforlaw.py --domains
```

---

## 🧠 SHARED MEMORY

```bash
python agentforlaw.py --remember "howey_test" "investment of money, common enterprise, profits from others"
python agentforlaw.py --recall "howey"
python agentforlaw.py --agents
```

---

## 🔗 RELATED AGENTS

| Agent | Purpose |
|-------|---------|
| rustypycraw | Code generation (8+ languages) |
| eagleclaw | AI-powered coding assistant |
| crustyclaw | Bug detection, pinch mode |
| claw-coder | Python AI with Groq |

---
┌─────────────────────────────────────────────────────────────────┐
│                    SHARED MEMORY DATABASE                        │
│                 ~/.claw_memory/shared_memory.db                  │
│                                                                  │
│  Registered Agents: 6                                            │
│  Stored Memories: securities_law, test_key, another_key          │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ agentforlaw   │────►│ rustypycraw   │────►│ eagleclaw     │
│   Stores law  │     │  Generates    │     │  Answers      │
│   precedent   │     │  code from it │     │  questions    │
└───────────────┘     └───────────────┘     └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌───────────────┐     ┌───────────────┐
                    │ crustyclaw    │     │ claw-coder    │
                    │  Audits code  │     │  Executes     │
                    │  for bugs     │     │  Python tasks │
                    └───────────────┘     └───────────────┘
