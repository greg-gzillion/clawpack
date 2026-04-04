# 📋 AGENTFORLAW - Complete Command Matrix

## 🚀 Quick Reference (Most Used Commands)

| Command | Purpose | Example |
|---------|---------|---------|
| `--analyze` | AI legal analysis | `--analyze "What is consideration?"` |
| `--list-models` | Show available AI models | `--list-models` |
| `--statute` | Look up US Code | `--statute "15 USC 78a"` |
| `--case` | Search case law | `--case "Marbury v Madison"` |
| `--constitution` | Read Constitution | `--constitution --article 1` |
| `--draft-contract` | Draft a contract | `--draft-contract service` |
| `--draft-will` | Draft a will | `--draft-will` |
| `--remember` | Store in shared memory | `--remember key value` |
| `--recall` | Retrieve from memory | `--recall key` |

## 🤖 AI & MODEL COMMANDS

| Command | Description | Provider | Example |
|---------|-------------|----------|---------|
| `--analyze "question"` | Analyze legal question | Auto | `--analyze "What is tort law?"` |
| `--analyze --provider groq` | Use Groq (fastest) | Groq | `--analyze "Explain contract" --provider groq` |
| `--analyze --provider deepseek` | Use DeepSeek | DeepSeek | `--analyze "SEC v. Ripple" --provider deepseek` |
| `--list-models` | List all available models | All | `--list-models` |
| `--recommend "task"` | Get model recommendation | - | `--recommend legal_analysis` |

### Model Recommendation Tasks

| Task | Best Models |
|------|-------------|
| `contract_drafting` | deepseek/deepseek-coder, groq/llama-3.1-8b |
| `long_document` | groq/mixtral-8x7b, deepseek/deepseek-chat |

## 📜 CONSTITUTION COMMANDS

| Command | Description | Example |
|---------|-------------|---------|
| `--constitution --article N` | Read article | `--constitution --article 1` |
| `--constitution --article N --section M` | Read article section | `--constitution --article 1 --section 8` |
| `--constitution --amendment N` | Read amendment | `--constitution --amendment 1` |

### Key Amendments

| Amendment | Summary |
|-----------|---------|
| 1 | Free speech, religion, press, assembly |
| 2 | Right to bear arms |
| 4 | Search and seizure protection |
| 5 | Due process, self-incrimination |
| 6 | Speedy trial, right to counsel |
| 8 | Cruel and unusual punishment |
| 10 | Powers reserved to states |
| 13 | Abolition of slavery |
| 14 | Equal protection, due process |

## 📝 CONTRACT DRAFTING COMMANDS

| Contract Type | Command | Required Parameters |
|---------------|---------|---------------------|
| Service | `--draft-contract service` | `party_a`, `party_b`, `services`, `payment` |
| Sale | `--draft-contract sale` | `seller`, `buyer`, `goods`, `price` |
| Employment | `--draft-contract employment` | `employer`, `employee`, `position`, `salary` |
| Lease | `--draft-contract lease` | `landlord`, `tenant`, `premises`, `rent`, `term` |
| Partnership | `--draft-contract partnership` | `partner_a`, `partner_b`, `purpose`, `sharing` |
| Loan | `--draft-contract loan` | `lender`, `borrower`, `principal`, `interest` |

## 📄 WILLS, TRUSTS & ESTATE COMMANDS

| Document | Command | Parameters |
|----------|---------|------------|
| Last Will | `--draft-will` | `name`, `executor`, `beneficiary`, `governing_state` |
| Living Trust | `--draft-trust` | `name`, `trustee`, `beneficiaries`, `governing_state` |
| Power of Attorney | `--draft-estate power_of_attorney` | `principal`, `agent` |
| Healthcare Directive | `--draft-estate healthcare_directive` | `principal`, `agent` |
| Living Will | `--draft-estate living_will` | `declarant` |

## 📚 CLAUSE LIBRARY COMMANDS

| Command | Description |
|---------|-------------|
| `--list-clauses` | List all clauses |
| `--clause indemnification` | Get indemnification clause |
| `--clause confidentiality` | Get confidentiality clause |
| `--clause termination` | Get termination clause |
| `--clause governing_law` | Get governing law clause |
| `--clause arbitration` | Get arbitration clause |

## 📖 LEGAL DEFINITIONS COMMANDS

| Command | Description |
|---------|-------------|
| `--list-terms` | List all legal terms |
| `--define consideration` | Define consideration |
| `--define due_process` | Define due process |
| `--define tort` | Define tort |
| `--define contract` | Define contract |
| `--define negligence` | Define negligence |

## 🧠 SHARED MEMORY COMMANDS

| Command | Description | Example |
|---------|-------------|---------|
| `--remember KEY VALUE` | Store in shared memory | `--remember "case" "Marbury v Madison"` |
| `--recall KEY` | Retrieve from memory | `--recall "case"` |
| `--agents` | List other claw agents | `--agents` |

## ℹ️ INFORMATION COMMANDS

| Command | Description |
|---------|-------------|
| `--agencies` | List regulatory agencies (SEC, CFTC, FINRA) |
| `--agency NAME` | Get agency info |
| `--domains` | List law domains |

## 🔄 COMPLETE WORKFLOW EXAMPLES

### Example 1: Research → Draft → Store

```bash
# 1. Research statute
python agentforlaw.py --statute "15 USC 78a"

# 2. Analyze with AI
python agentforlaw.py --analyze "What does the Securities Exchange Act require?"

# 3. Draft compliance contract
python agentforlaw.py --draft-contract service --parties '{"party_a":"Company","party_b":"Client"}' --provisions '{"services":"compliance consulting"}'

# 4. Store for other agents
python agentforlaw.py --remember "sec_compliance" "SEC registration requirements"
```

## 📊 COMMAND SUMMARY

| Category | # Commands |
|----------|------------|
| AI & Models | 6 |
| Constitution | 3 |
| Statutes/Regulations | 2 |
| Case Law | 1 |
| Contract Drafting | 6 |
| Wills/Trusts/Estate | 5 |
| Clause Library | 6 |
| Legal Definitions | 6 |
| Shared Memory | 3 |
| Information | 3 |
| **TOTAL** | **41+** |

---

*For full documentation, see [README.md](README.md) and [ECOSYSTEM.md](ECOSYSTEM.md)*
