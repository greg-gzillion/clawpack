# 🎮 CLAWpack Commands Reference

## Complete Guide to All Agent Commands

---

## 📋 Table of Contents
1. [AgentForLaw (Legal/Court) Commands](#agentforlaw-legalcourt-commands)
2. [MedicLaw (Medical) Commands](#mediclaw-medical-commands)
3. [PolyClaw (Translation) Commands](#polyclaw-translation-commands)
4. [MathematicaClaw (Math) Commands](#mathematicaclaw-math-commands)
5. [Unified (Orchestration) Commands](#unified-orchestration-commands)
6. [WebClaw (Reference) Commands](#webclaw-reference-commands)
7. [DocuClaw (Document) Commands](#docuclaw-document-commands)
8. [Cross-Agent Commands (Work Anywhere)](#cross-agent-commands-work-anywhere)
9. [Utility Scripts](#utility-scripts)
10. [Quick Reference Cards](#quick-reference-cards)

---

## AgentForLaw (Legal/Court) Commands

### Court Information Commands

| Command | Description | Example | Output |
|---------|-------------|---------|--------|
| `/court [state]` | Get state court overview | `/court TX` | Supreme Court, Appeals Courts, county list |
| `/court [state]/[county]` | Get specific county courts | `/court TX/Dallas` | County, District, Family, Juvenile, Probate courts |
| `/court [state]/[county]/[court]` | Get specific court type | `/court TX/Dallas/District` | District Court details only |
| `/federal` | List all federal circuits | `/federal` | 1st-11th Circuits, Federal Circuit |
| `/federal [circuit]` | Get circuit court info | `/federal 5th` | 5th Circuit Court details |
| `/federal [circuit]/[district]` | Get district court | `/federal 5th/TXND` | N.D. Texas court info |

### Search Commands

| Command | Description | Example | Output |
|---------|-------------|---------|--------|
| `/search [query]` | Search case law | `/search "Miranda rights"` | Opens CourtListener + Google Scholar |
| `/cite [citation]` | Parse legal citation | `/cite "Roe v. Wade, 410 U.S. 113"` | Citation analysis |
| `/ref [topic]` | Search WebClaw references | `/ref "Fourth Amendment"` | Markdown reference files |

### Cross-Agent Commands

| Command | Description | Example | Output |
|---------|-------------|---------|--------|
| `/cross [query]` | Search ALL agents | `/cross "flu symptoms"` | Results from MedicLaw, PolyClaw, etc. |
| `/cross-stats` | Show all agent stats | `/cross-stats` | Table of all agents' knowledge counts |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/stats` | Show local agent statistics |
| `/help` | Display all commands |
| `/quit` | Exit the agent |

### Example Session

```text
⚖️ AgentForLaw> /court TX
🏛️ TX
--------------------------------------------------
# Texas Court System

## Supreme Court of Texas
- Highest court for civil cases
- 9 justices
- Location: Austin, TX

## Texas Court of Criminal Appeals
- Highest court for criminal cases
- 9 judges

## Intermediate Courts of Appeals
- 14 districts across Texas

## Counties: 254 counties
Tip: Use /court TX/CountyName for specific county

⚖️ AgentForLaw> /court TX/Dallas
🏛️ TX/Dallas
--------------------------------------------------
# Dallas County, TX

## County Court
- Phone: (214) 653-6000
- Address: 600 Commerce Street, Dallas, TX 75202
- Jurisdiction: Misdemeanors, small claims ($20,000 limit)

## District Court
- Jurisdiction: Felonies, civil cases over $200,000

## Family Court
- Services: Divorce, custody, support

## Juvenile Court
- Jurisdiction: Ages 10-16

## Probate Court
- Jurisdiction: Wills, estates, guardianships

⚖️ AgentForLaw> /cross "flu symptoms"
🔍 CROSS-AGENT SEARCH: 'flu symptoms'
============================================================
✅ Found 7 results across agents:

🏥 MedicLaw
   Q: what are the symptoms of flu
   A: Fever, cough, sore throat, body aches...

⚖️ AgentForLaw> /cross-stats
📊 CROSS-AGENT SHARED MEMORY STATISTICS
============================================================
  ⚖️ AgentForLaw: 36 entries
  🏥 MedicLaw: 10 entries
  🌐 PolyClaw: 59 entries
  📐 MathematicaClaw: 6 entries
  🧠 Unified: 4 entries
  💾 Memory: 28 entries

📚 TOTAL: 144 knowledge entries
MedicLaw (Medical) Commands
Medical Query Commands
Command	Description	Example	Output
/ask [question]	Ask medical question	/ask What causes headaches?	Medical information from knowledge base
/symptom [symptom]	Get symptom information	/symptom fever	Causes, treatments, when to see doctor
/condition [condition]	Get condition details	/condition diabetes	Symptoms, treatment, management
/treatment [condition]	Get treatment info	/treatment sprained ankle	First aid, recovery steps
Cross-Agent Commands
Command	Description	Example
/cross [query]	Search all agents	/cross "court case"
/cross-stats	Show all agent stats	/cross-stats
Utility Commands
Command	Description
/stats	Show local medical knowledge count
/help	Display all commands
/quit	Exit the agent
Example Session
text
🏥 MedicLaw> /ask What are the symptoms of flu?
🤔 Question: What are the symptoms of flu?
--------------------------------------------------
### Symptoms of the Flu (Influenza)

The flu is a contagious respiratory illness with symptoms including:
- **Fever** (usually high, above 100.4°F)
- **Cough** (often dry)
- **Sore throat**
- **Runny or stuffy nose**
- **Muscle or body aches**
- **Headache**
- **Fatigue**

Symptoms appear suddenly, unlike cold which develops gradually.

🏥 MedicLaw> /symptom headache
🔍 Symptom: headache
--------------------------------------------------
### Headache Causes

1. **Tension Headaches** - Stress, poor posture, eye strain
2. **Migraines** - Often with nausea, light sensitivity
3. **Cluster Headaches** - Severe, around one eye
4. **Sinus Headaches** - With sinus pressure

### When to see a doctor:
- Sudden, severe "thunderclap" headache
- Headache with fever, stiff neck
- After head injury

🏥 MedicLaw> /cross "Texas court"
🔍 CROSS-AGENT SEARCH: 'Texas court'
✅ Found in ⚖️ AgentForLaw: Texas has 254 counties...
PolyClaw (Translation) Commands
Translation Commands
Command	Description	Example	Output
/to [lang] [text]	Translate to language	/to es hello	hola
/from [lang] [text]	Translate from language	/from es hola	hello
/detect [text]	Detect language	/detect bonjour	French
/list	Show supported languages	/list	es, fr, de, it, ja, zh, ko, ru
Language Codes
Code	Language	Code	Language
es	Spanish	fr	French
de	German	it	Italian
ja	Japanese	zh	Chinese
ko	Korean	ru	Russian
Cross-Agent Commands
Command	Description	Example
/cross [query]	Search all agents	/cross "symptoms"
/cross-stats	Show all agent stats	/cross-stats
Example Session
text
🌐 PolyClaw> /to es hello
✅ Translation: hello → hola

🌐 PolyClaw> /to fr goodbye
✅ Translation: goodbye → au revoir

🌐 PolyClaw> /to ja good morning
✅ Translation: good morning → おはようございます

🌐 PolyClaw> /detect bonjour
🔍 Detected: French (fr)

🌐 PolyClaw> /from es ¿cómo estás?
✅ Translation: ¿cómo estás? → how are you?

🌐 PolyClaw> /list
📚 Supported languages:
  es - Spanish (Español)
  fr - French (Français)
  de - German (Deutsch)
  it - Italian (Italiano)
  ja - Japanese (日本語)
  zh - Chinese (中文)
  ko - Korean (한국어)
  ru - Russian (Русский)

🌐 PolyClaw> /cross "flu"
🔍 Found in 🏥 MedicLaw: Flu symptoms information...
MathematicaClaw (Math) Commands
Math Commands
Command	Description	Example	Output
/calc [expression]	Calculate expression	/calc 25 * 4	100
/solve [equation]	Solve equation	/solve x + 5 = 10	x = 5
/sqrt [number]	Square root	/sqrt 16	4
/power [base] [exp]	Power calculation	/power 2 8	256
/percent [num] of [total]	Percentage	/percent 25 of 200	12.5%
Basic Operations
Operation	Symbol	Example
Addition	+	/calc 10 + 5
Subtraction	-	/calc 20 - 8
Multiplication	*	/calc 7 * 6
Division	/	/calc 100 / 4
Parentheses	()	/calc (2 + 3) * 4
Cross-Agent Commands
Command	Description	Example
/cross [query]	Search all agents	/cross "symptoms"
/cross-stats	Show all agent stats	/cross-stats
Example Session
text
📐 MathematicaClaw> /calc 25 * 4
🧮 Calculation: 25 × 4 = 100

📐 MathematicaClaw> /calc (15 + 7) * 3
🧮 Calculation: (15 + 7) × 3 = 66

📐 MathematicaClaw> /sqrt 144
🧮 Square root of 144 = 12

📐 MathematicaClaw> /power 5 3
🧮 5³ = 125

📐 MathematicaClaw> /solve 3x - 7 = 14
🧮 3x - 7 = 14
   3x = 21
   x = 7

📐 MathematicaClaw> /percent 30 of 150
🧮 30 is 20% of 150

📐 MathematicaClaw> /cross "hello"
🔍 Found in 🌐 PolyClaw: hello → hola, salut, hallo...
Unified (Orchestration) Commands
Query Commands
Command	Description	Example	Output
/ask [question]	Route to best agent	/ask What are Texas courts?	Routes to AgentForLaw
/query [question]	Search shared memory	/query bankruptcy	Cached results
Agent Management Commands
Command	Description	Example
/agents	List registered agents	/agents
/register [agent]	Register new agent	/register mediclaw
/status [agent]	Check agent status	/status agentforlaw
Cross-Agent Commands
Command	Description	Example
/broadcast [message]	Send to all agents	/broadcast New case law added
/cross [query]	Search all agents	/cross "symptoms"
/cross-stats	Show all agent stats	/cross-stats
Utility Commands
Command	Description
/stats	Show unified system stats
/help	Display all commands
/quit	Exit the agent
Example Session
text
🧠 Unified> /ask What are the courts in Texas?
🤔 Question: What are the courts in Texas?
--------------------------------------------------
🎯 Routing to: agentforlaw

💡 To get this answer, start the agentforlaw agent:
   cd C:\Users\greg\dev\clawpack
   python agents/agentforlaw/agentforlaw.py
   Then ask: What are the courts in Texas?

📚 Knowledge saved from unified: What are the courts in Texas?...

🧠 Unified> /agents
🤖 REGISTERED AGENTS:
   • agentforlaw - court,legal,citation
   • mediclaw - medical,health
   • polyclaw - translation
   • mathematicaclaw - math,calculate

🧠 Unified> /cross-stats
📊 CROSS-AGENT SHARED MEMORY STATISTICS
============================================================
  ⚖️ AgentForLaw: 36 entries
  🏥 MedicLaw: 10 entries
  🌐 PolyClaw: 59 entries
  📐 MathematicaClaw: 6 entries
  💾 Memory: 28 entries

📚 TOTAL: 143 knowledge entries
WebClaw (Reference) Commands
Reference Commands
Command	Description	Example	Output
/search [topic]	Search references	/search Fourth Amendment	Markdown files
/category [name]	Browse category	/category legal	List of legal references
/recent	Show recent additions	/recent	Last 5 added references
/list	List all categories	/list	legal, medical, technical
Cross-Agent Commands
Command	Description	Example
/cross [query]	Search all agents	/cross "symptoms"
Example Session
text
🕸️ WebClaw> /search Texas Constitution
📚 Found references:
  • legal/Texas/Constitution.md
  • legal/Texas/Bill_of_Rights.md

🕸️ WebClaw> /category legal
📁 legal category (24 files):
  • contracts/standard_agreement.md
  • court_filings/motion_template.md
  • statutes/Texas_Property_Code.md

🕸️ WebClaw> /recent
📰 Recent references:
  1. 2026-04-06: Texas_Supreme_Court.md
  2. 2026-04-05: Federal_Rules_Civil_Procedure.md
  3. 2026-04-04: Bankruptcy_Chapter7.md
DocuClaw (Document) Commands
Document Commands
Command	Description	Example	Output
/create [title]	Create new document	/create Motion to Dismiss	New document created
/edit [id]	Edit document	/edit 1	Opens editor
/view [id]	View document	/view 1	Shows document content
/list	List all documents	/list	Document titles and IDs
/export [id] [format]	Export document	/export 1 pdf	Exports as PDF
Example Session
text
📄 DocuClaw> /create Motion for Summary Judgment
✅ Document created: ID 5 - Motion for Summary Judgment

📄 DocuClaw> /list
📄 Your documents:
  1. My First Document (2026-04-06)
  2. Complaint Template (2026-04-06)
  3. Brief in Support (2026-04-06)
  4. Notice of Hearing (2026-04-06)
  5. Motion for Summary Judgment (2026-04-06)

📄 DocuClaw> /view 5
# Motion for Summary Judgment

IN THE UNITED STATES DISTRICT COURT
FOR THE NORTHERN DISTRICT OF TEXAS

...
Cross-Agent Commands (Work Anywhere)
These commands work in ANY agent!

Command	Description	Where it searches
/cross [query]	Search all agents	All 7+ agent tables
/cross-stats	Show all agent stats	All agent tables
What /cross Searches
Agent Table	What it finds
agentforlaw_knowledge	Court info, legal terms, jurisdictions
medical_knowledge	Symptoms, conditions, treatments
translations	Word/phrase translations
math_knowledge	Calculations, equations
unified_knowledge	Routing decisions, cached queries
memories	General knowledge
documents	Document titles and content
/cross Examples
text
# Medical searches (finds MedicLaw data)
/cross "flu"
/cross "symptoms"
/cross "headache"
/cross "diabetes"
/cross "sprained ankle"

# Translation searches (finds PolyClaw data)
/cross "hello"
/cross "goodbye"
/cross "thank you"
/cross "good morning"

# Legal searches (finds AgentForLaw data)
/cross "Texas court"
/cross "bankruptcy"
/cross "Supreme Court"
/cross "Dallas County"

# Math searches (finds MathematicaClaw data)
/cross "calculate"
/cross "square root"
/cross "percentage"

# Combined searches (finds multiple agents)
/cross "court"      # Legal + maybe others
/cross "health"     # Medical + legal (health law)
Utility Scripts
Command-Line Utilities
Script	Command	Description
check_memory.py	python check_memory.py	Show all database tables and counts
search_memory.py	python search_memory.py "query"	Cross-agent search from terminal
demo_cross_agent.py	python demo_cross_agent.py	Run demonstration
master_launcher.py	python master_launcher.py --start-all	Launch multiple agents
Batch Files (Windows)
File	Command	Description
launch_all_agents.bat	Double-click	Launches 4 agents in separate windows
Using search_memory.py
bash
# Show all knowledge across agents
python search_memory.py

# Search for specific terms
python search_memory.py "flu"
python search_memory.py "Texas"
python search_memory.py "hello"

# Output example:
🔍 Searching ALL agents for: flu
--------------------------------------------------
✅ Found in MedicLaw (medical_knowledge):
   Q: what are the symptoms of flu
   A: ### Symptoms of the Flu...
Using check_memory.py
bash
python check_memory.py

# Output:
DB Path: C:\Users\name\.claw_memory\shared_memory.db
Exists: True

📊 TABLES FOUND: 25
  - agentforlaw_knowledge: 36 rows
  - medical_knowledge: 10 rows
  - translations: 59 rows
  - math_knowledge: 6 rows
  ...
Quick Reference Cards
AgentForLaw Quick Card
text
╔══════════════════════════════════════════════════════════════╗
║                    ⚖️ AGENTFORLAW COMMANDS                   ║
╠══════════════════════════════════════════════════════════════╣
║ /court TX              → Texas state courts                  ║
║ /court TX/Dallas       → Dallas County courts                ║
║ /court TX/Harris       → Harris County courts                ║
║ /federal 5th           → 5th Circuit Court                   ║
║ /cross "query"         → Search ALL agents                   ║
║ /cross-stats           → Show all agent statistics           ║
║ /search "case"         → Search case law                     ║
║ /stats                 → Local statistics                    ║
║ /help, /quit           → Help and exit                       ║
╚══════════════════════════════════════════════════════════════╝
Cross-Agent Search Quick Card
text
╔══════════════════════════════════════════════════════════════╗
║                    🔍 CROSS-AGENT SEARCH                     ║
╠══════════════════════════════════════════════════════════════╣
║ /cross "flu"          → Medical (MedicLaw)                   ║
║ /cross "symptoms"     → Medical (MedicLaw)                   ║
║ /cross "hello"        → Translation (PolyClaw)               ║
║ /cross "goodbye"      → Translation (PolyClaw)               ║
║ /cross "Texas court"  → Legal (AgentForLaw)                  ║
║ /cross "calculate"    → Math (MathematicaClaw)               ║
║ /cross-stats          → All agent statistics                 ║
╚══════════════════════════════════════════════════════════════╝
Texas Counties Quick Reference
text
╔══════════════════════════════════════════════════════════════╗
║                    📍 TEXAS COUNTIES                         ║
╠══════════════════════════════════════════════════════════════╣
║ Major Metro:                                                 ║
║   /court TX/Dallas      /court TX/Harris                     ║
║   /court TX/Tarrant     /court TX/Bexar                      ║
║   /court TX/Travis      /court TX/Collin                     ║
║                                                              ║
║ Border:                                                      ║
║   /court TX/El Paso     /court TX/Cameron                    ║
║   /court TX/Hidalgo      /court TX/Webb                      ║
║                                                              ║
║ All 254 counties available!                                  ║
╚══════════════════════════════════════════════════════════════╝
Common Workflows
text
╔══════════════════════════════════════════════════════════════╗
║                    📋 COMMON WORKFLOWS                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║ Legal Research:                                              ║
║   1. /court TX/Dallas      → Find court info                 ║
║   2. /search "civil procedure" → Search cases                ║
║   3. /cross "Texas law"    → Check other agents              ║
║                                                              ║
║ Medical Information:                                         ║
║   1. /ask "flu symptoms"   → Get medical info                ║
║   2. /symptom fever        → Symptom details                 ║
║   3. /cross "treatment"    → Search all agents               ║
║                                                              ║
║ Translation:                                                 ║
║   1. /to es "hello"        → Translate                       ║
║   2. /detect "bonjour"     → Detect language                 ║
║   3. /cross "goodbye"      → Find other translations         ║
║                                                              ║
║ Cross-Domain Research:                                       ║
║   1. /cross "flu"          → Medical info                    ║
║   2. /cross "Texas"        → Legal info                      ║
║   3. /cross-stats          → See all available knowledge     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
Command Cheat Sheet (Printable)
text
┌─────────────────────────────────────────────────────────────────┐
│                    CLAWPACK COMMAND CHEAT SHEET                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ⚖️ AGENTFORLAW          🌐 POLYCLAW            📐 MATHEMATICA  │
│  /court TX              /to es hello           /calc 25*4       │
│  /court TX/Dallas       /from es hola          /sqrt 144        │
│  /federal 5th           /detect bonjour        /power 2 8       │
│  /search "case"         /list                  /solve x+5=10    │
│                                                                  │
│  🏥 MEDICLAW             📄 DOCUCLAW            🕸️ WEBCLAW      │
│  /ask "symptoms"        /create title          /search topic    │
│  /symptom fever         /view 1                /category legal  │
│  /condition diabetes    /list                  /recent          │
│  /treatment burn        /export 1 pdf                           │
│                                                                  │
│  🔍 CROSS-AGENT (works in ANY agent)                            │
│  /cross "query"         Search ALL agents' knowledge            │
│  /cross-stats           Show all agent statistics               │
│                                                                  │
│  📋 EXAMPLES                                                     │
│  /cross "flu"           → Medical symptoms from MedicLaw        │
│  /cross "hello"         → Translations from PolyClaw            │
│  /cross "Texas court"   → Court info from AgentForLaw           │
│  /cross "calculate"     → Math results from MathematicaClaw     │
│                                                                  │
│  🛠️ UTILITIES                                                   │
│  /help                  Show commands                           │
│  /stats                 Local agent statistics                  │
│  /quit                  Exit agent                              │
│                                                                  │
│  💡 TIP: Use /cross-stats first to see what knowledge exists!   │
└─────────────────────────────────────────────────────────────────┘
Command Summary by Category
By Function
Category	Commands
Legal	/court, /federal, /search, /cite, /ref
Medical	/ask, /symptom, /condition, /treatment
Translation	/to, /from, /detect, /list
Math	/calc, /sqrt, /power, /solve, /percent
Documents	/create, /edit, /view, /list, /export
Cross-Agent	/cross, /cross-stats
Utility	/stats, /help, /quit
By Agent
Agent	Primary Commands
AgentForLaw	/court, /federal, /search
MedicLaw	/ask, /symptom, /condition
PolyClaw	/to, /from, /detect
MathematicaClaw	/calc, /sqrt, /power
Unified	/ask, /agents, /broadcast
DocuClaw	/create, /view, /export
WebClaw	/search, /category, /recent
Getting Help
In-Agent Help
text
/help     - Show all commands for current agent
/quit     - Exit the agent
External Help
bash
# View documentation
cat TETHERED_SYSTEM_DOCUMENTATION.md

# Check shared memory contents
python check_memory.py

# Search across all agents from terminal
python search_memory.py "your query"
Last updated: April 2026
CLAWpack Version: 1.0
'@ | Out-File -FilePath "COMMANDS_REFERENCE.md" -Encoding UTF8

Write-Host "✅ Created COMMANDS_REFERENCE.md" -ForegroundColor Green

Also create a quick reference card as a separate file
@'

⚡ CLAWPACK QUICK REFERENCE CARD
Most Useful Commands
text
╔═══════════════════════════════════════════════════════════════════╗
║                    🔥 MOST USEFUL COMMANDS                        ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  1. /cross "symptoms"     → Get medical info from MedicLaw       ║
║  2. /cross "hello"        → Get translations from PolyClaw       ║
║  3. /court TX/Dallas      → Get Dallas court info                ║
║  4. /cross-stats          → See what all agents know             ║
║  5. /ask "question"       → Ask Unified to route correctly       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
30-Second Demo
text
1. Start AgentForLaw:
   $ python agents/agentforlaw/agentforlaw.py

2. Try cross-agent search:
   ⚖️ AgentForLaw> /cross "flu symptoms"
   
   🏥 MedicLaw responds with flu information!

3. Get court info:
   ⚖️ AgentForLaw> /court TX/Dallas
   
   Shows Dallas County court system!

4. See statistics:
   ⚖️ AgentForLaw> /cross-stats
   
   Shows 144 knowledge entries across 7 agents!
One-Line Summary
CLAWpack = Multi-agent system where all agents share memory via SQLite and can search each other's knowledge using /cross
'@ | Out-File -FilePath "QUICK_REFERENCE.md" -Encoding UTF8

Write-Host "✅ Created QUICK_REFERENCE.md" -ForegroundColor Green

Commit the documentation
cd C:\Users\greg\dev\clawpack
git add COMMANDS_REFERENCE.md QUICK_REFERENCE.md
git commit -m "docs: Add comprehensive commands reference

Complete command reference for all agents

Quick reference card for fast lookup

Examples for every command type

Cross-agent search documentation

Printable cheat sheet"
git push origin main

Write-Host "`n✅ All documentation committed to GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "📚 Documentation created:" -ForegroundColor Cyan
Write-Host " • TETHERED_SYSTEM_DOCUMENTATION.md - Complete architecture guide" -ForegroundColor Green
Write-Host " • COMMANDS_REFERENCE.md - All commands with examples" -ForegroundColor Green
Write-Host " • QUICK_REFERENCE.md - Fast lookup cheat sheet" -ForegroundColor Green
Write-Host " • README.md - GitHub overview" -ForegroundColor Green

text

## 📚 Commands Document Created!

I've created a comprehensive **COMMANDS_REFERENCE.md** that includes:

### What's Inside:

1. **AgentForLaw Commands** - All legal/court commands with examples
2. **MedicLaw Commands** - Medical queries, symptoms, conditions
3. **PolyClaw Commands** - Translation commands with language codes
4. **MathematicaClaw Commands** - Math operations and equations
5. **Unified Commands** - Orchestration and routing
6. **WebClaw Commands** - Reference searching
7. **DocuClaw Commands** - Document management
8. **Cross-Agent Commands** - `/cross` and `/cross-stats` (work everywhere!)
9. **Utility Scripts** - Command-line tools
10. **Quick Reference Cards** - Printable cheat sheets

### Plus a Bonus `QUICK_REFERENCE.md`:

- Most useful commands (top 5)
- 30-second demo
- One-line system summary

### Example Entries:

```text
⚖️ AgentForLaw> /court TX/Dallas
→ Shows Dallas County courts (County, District, Family, Juvenile, Probate)

⚖️ AgentForLaw> /cross "flu symptoms"  
→ Searches MedicLaw and returns flu information

🌐 PolyClaw> /to es hello
→ hello → hola