# How to Contribute to PhoenixPME

**Last updated:** February 21, 2026

---

## 🎯 Project Focus
First, please read [`CURRENT-FOCUS.md`](CURRENT-FOCUS.md) to understand what we're building NOW vs what's parked for later. This will save everyone time.

---

## 📋 Finding Tasks
1. Check [`PROJECTS_NEW.md`](PROJECTS_NEW.md) for current priorities
2. Look for issues tagged `good-first-issue` or `help-wanted` on [GitHub Issues](https://github.com/greg-gzillion/TX/issues)
3. Review the architecture docs in [`/docs/architecture/`](/docs/architecture/) to understand the system
4. Check [`docs/TERMINOLOGY_GUIDE.md`](docs/TERMINOLOGY_GUIDE.md) for consistent language before contributing

---

## 🚀 Development Setup

### Prerequisites
- Node.js v20+
- PostgreSQL v14+ (optional, for local backend)
- Docker (optional, for local blockchain)
- Keplr wallet (for testnet interaction)

### ⚠️ Important Note About Testnet
**The current Coreum testnet (v3.x) is NOT compatible with our smart contracts (built for v5.0+).**

- **TX Testnet Launches:** March 6, 2026
- **Current Status:** Mock mode active for UI testing
- **Real contract calls:** Begin March 6

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/TX.git
cd TX

# Install dependencies
cd apps/frontend && npm install
cd ../backend && npm install
Mock Wallets (For Testing)
The project includes mock wallets for UI testing without a blockchain connection:

### Mock Wallets (For Testing)
The project includes mock wallets for UI testing without a blockchain connection:

| Wallet | Address | Balance | Role |
|--------|---------|---------|------|
| Robert | `testcore1xa352f6gtgc4g7c9rrdgl4wn9vaw9r25v47jen` | 5,000,000 | Can create auctions |
| Alice | `testcore14qkw9fplr9xplfl5qwz8rr8f3uxhja8yuf0z6l` | 1,000,000 | Can bid |
| Bob | `testcore1afmlm9ra7m555vurve6ek4754rnv7max2hl6en` | 2,000,000 | Can bid |
| Charlie | `testcore1urvw6ta906qphvvrmcuwwxy3z2fqns56er2agu` | 3,000,000 | Can bid |
| Treasury | `testcore1mocktreasuryaddress12345` | 13,000,000 | Admin (funds auctions) |
| Deployer | `testcore1mockdeployeraddress67890` | 5,000,000 | Contract deployment |
| **Community Reserve Fund** | `testcore1m5adn3k68tk4zqmujpnstmp9r933jafzu44tnv` | 0 (accumulates) | Receives 1.1% fees |

**Important Notes:**
- Any user can be a buyer OR seller depending on the auction (Robert can bid, Alice can create auctions)
- The Community Reserve Fund address is where 1.1% fees accumulate
- **No one can withdraw** from this address - funds are locked until DAO governance
- Balance grows with each successful auction


Start Development Servers
Terminal 1 - Backend
bash
cd apps/backend
cp .env.example .env  # Configure as needed
npm run dev
# Runs on http://localhost:3001
Terminal 2 - Frontend
bash
cd apps/frontend
cp .env.local.example .env.local  # Configure as needed
npm run dev
# Runs on http://localhost:3000
Verify Everything Works
✅ Frontend loads at http://localhost:3000

✅ Backend health check: http://localhost:3001/health

✅ Mock wallet selector appears in navbar

✅ No errors in browser console (F12)

📝 Pull Request Process
Branch Naming
feature/description for new features

fix/description for bug fixes

docs/description for documentation

test/description for test improvements

Before Submitting
✅ Test your changes locally

✅ Ensure all tests pass (npm test)

✅ Update documentation if needed

✅ Check terminology guide for consistent language

✅ Add your changes to PROJECTS_NEW.md if applicable

✅ Run npm run build to verify no build errors

PR Description Should Include
What problem does this solve? (Link to issue if applicable)

How did you test it? (Local testing, browser console, etc.)

Screenshots for UI changes

Related issue numbers (e.g., "Fixes #123")

Any breaking changes (and how to migrate)

💬 Communication
Channel	Purpose
GitHub Issues	Technical discussions, bug reports, feature requests
GitHub Discussions	Grant proposals, community feedback, long-form discussions
Email	gjf20842@gmail.com - For serious work, grants, or partnership inquiries
Do NOT: Open issues for general questions about blockchain or React (use Discussions first).

💰 The PhoenixPME Funding Model
This project aims to become self-sustaining through a 1.1% protocol fee governed by the community. All fees flow to the Community Reserve Fund (CRF) - a smart contract that no individual can access.

Key Facts About Funding
✅ 1.1% fee is hardcoded in smart contracts

✅ Funds go to Community Reserve Fund (no individual access)

✅ Founder (Greg) has 10% voting weight, NOT withdrawal rights

✅ Future use determined by DAO vote

✅ Contributors paid via transparent grants, not equity or tokens

Path for Technical Contributors
Step 1: Find an Open Task
Check active issues in GitHub Issues

Review ROADMAP.md and CURRENT-FOCUS.md

Comment on an issue to express interest and share initial thoughts

Step 2: Submit a Grant Proposal
For substantial work, submit a proposal to the community via GitHub Discussions. A good proposal includes:

Section	What to Include
Title & Summary	e.g., "Build BidForm Component v1.0"
Scope of Work	Reference relevant architecture docs
Deliverables	Concrete outputs (code, tests, docs)
Timeline	Estimated start and completion dates
Grant Request	Total amount + milestone breakdown
Your Background	Links to previous relevant work
Step 3: Community Review & Vote
Proposal posted to GitHub Discussions

Community feedback and refinement (minimum 7 days)

On-chain snapshot vote for funding approval

Step 4: Work & Get Paid
Grant amount locked in Community Reserve Fund

Work publicly in fork or branch

Submit proof of work at milestones

Multi-sig of community trustees releases funds

✅ Current Priority Tracks (as of Feb 21, 2026)
✅ Completed
Area	Status
Core auction contracts	✅ 7 + 16 tests passing
Frontend auction creation form	✅ Complete with 8 components
Wallet integration (Keplr/Leap)	✅ Working
Live deployment	✅ Vercel + Render
Frontend reorganization	✅ Clean structure, no duplicates
🔜 Immediate Needs
Priority	Task	Status
🔴 HIGH	BidForm component	⏳ IN PROGRESS
🔴 HIGH	Auction detail page	⏳ PLANNED
🔴 HIGH	Real contract integration	⏳ March 6+
🟡 MEDIUM	Shipping oracle development	📝 FUTURE
🟡 MEDIUM	Dispute resolution system	📝 FUTURE
Future Tracks (Post-MVP)
Oracle Development (shipping tracking verification)

Cross-Chain Infrastructure (settlement layer bridges)

Testing & Security (audits, bug bounties)

🚀 Getting Started Today
You don't need to wait for a grant to contribute:

Fork the repository and start experimenting

Submit a Pull Request for:

Documentation fixes

Design ideas

Small improvements

Test additions

Join the Discussion to help shape the protocol's future

Building trust through small, public contributions is the best path to larger, funded work.

🔒 Legal
By contributing, you agree to:

The terms in docs/legal/CONTRIBUTOR_AGREEMENT.md

License your work under GPL v3.0 (see LICENSE)

Maintain the project's dual-license structure for commercial use

Use consistent terminology from docs/TERMINOLOGY_GUIDE.md

❓ Questions?
Check existing issues first

Review documentation in /docs/

Open a GitHub issue with the question label

Email serious inquiries to gjf20842@gmail.com

📚 Related Documents
Document	Purpose
CURRENT-FOCUS.md	What we're building NOW
ROADMAP.md	Future plans
PROJECTS_NEW.md	Current priorities
TERMINOLOGY_GUIDE.md	Consistent language
CONTRIBUTOR_AGREEMENT.md	Legal terms
Thank you for helping build the future of physical metals trading on blockchain! 🏆

Last updated: February 21, 2026