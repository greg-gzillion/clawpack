# PhoenixPME Governance

**Last updated:** February 24, 2026  
**Current Phase:** Bootstrap (Pre-DAO)  
**Next Phase:** DAO Formation - Q3 2026 (estimated)

---

## Current Phase: Bootstrap (Pre-DAO)

During the initial bootstrap phase, governance is intentionally centralized to enable rapid development and iteration leading up to the TX Testnet launch on March 6, 2026.

### Decision Hierarchy
| Level | Role | Responsibility |
|-------|------|----------------|
| **1** | **Founder (Greg)** | Final authority on all matters |
| **2** | **Technical Advisors** | Architecture review and guidance |
| **3** | **Contributors (8)** | Code contributions and feedback |
| **4** | **Community** | Input via GitHub issues and discussions |

### Current Decision Process

All major decisions are documented in GitHub with:

| Component | Location |
|-----------|----------|
| **Problem statement** | GitHub Issue |
| **Options considered** | Issue comments |
| **Decision and rationale** | Issue resolution |
| **Implementation plan** | Pull Request |
| **Documentation** | Updated in `/docs` |

### Recent Decisions (Feb 2026)

| Decision | Date | Rationale |
|----------|------|-----------|
| Multi-wallet support (UniversalWalletV2) | Feb 23 | Broader user access |
| TESTUSD integration (vs CORE) | Feb 24 | Align with token strategy |
| Convert next.config.ts → next.config.js | Feb 24 | Next.js compatibility |
| Remove 30+ old files | Feb 22 | Project cleanup |
| Frontend reorganization | Feb 21 | Eliminate duplicates |

### Transparency
- ✅ All decisions documented in public GitHub issues
- ✅ Community input welcomed and considered
- ✅ Rationale for decisions clearly explained
- ✅ 8 contributors actively participating
- ✅ 24 daily visitors providing feedback

---

## Community Reserve Fund (CRF) Governance

### Current Status (Pre-DAO)
| Aspect | Detail |
|--------|--------|
| **Fee Collection** | 1.1% (hardcoded, not yet active) |
| **Fund Location** | Community Reserve Fund (smart contract) |
| **Withdrawal Rights** | ❌ **NO ONE** (not even founder) |
| **Governance** | ⏳ DAO pending (Q3 2026) |

### Future DAO Structure
- **PHNX Voting Weight:** 1 PHNX per 1 TESTUSD in fees generated
- **Non-transferable:** Cannot be bought or sold
- **Community Control:** 90% voting weight
- **Founder Voice:** 10% voting weight (permanent)

---

## Future Evolution: DAO Framework

This governance structure will evolve into the DAO framework described in [`docs/technical/DAO_OPERATIONS.md`](docs/technical/DAO_OPERATIONS.md) once the protocol reaches sufficient maturity and usage.

### Estimated Timeline
| Phase | Timeline | Status |
|-------|----------|--------|
| Bootstrap (Pre-DAO) | Feb - June 2026 | ✅ Current |
| Testnet Launch | March 6, 2026 | 🔜 9 days |
| First Trades | March 6+ | ⏳ |
| TRUST/DONT TRUST System | Q2 2026 | 📝 Planned |
| PHNX Governance | Q2 2026 | 📝 Planned |
| DAO Formation | Q3 2026 | 📝 Planned |
| First DAO Votes | Q3 2026 | 📝 Planned |

---

## Key Governance Principles

### Immutable Protocol Rules
```solidity
// Cannot be changed by any governance vote
1. 1.1% protocol fee → Community Reserve Fund
2. NO INDIVIDUAL can withdraw from CRF
3. PHNX, TRUST, DONT TRUST are non-transferable
4. Founder retains 10% voting weight (permanent)
Community-Guided Decisions
Feature prioritization

Treasury allocation

Oracle selection

Dispute resolution rules

Grant distribution

Protection Mechanisms
Time-locks: Critical changes delayed 48+ hours

Transparency: All proposals public

Quorum: Minimum participation required

Veto power: None - community decides

How to Participate Now
Current Contributors (8)
Role	How to Join
Code Contributions	Submit PRs
Bug Reports	Open GitHub Issues
Feature Suggestions	Start Discussion
Documentation	Improve docs
Community Building	Spread the word
Getting Started
Read CONTRIBUTING.md

Join GitHub Discussions

Pick an open issue

Submit your first PR

Testnet Participation (Starting March 6)
Get TESTCORE from faucet

Connect wallet (Keplr/Leap/MetaMask/Phantom)

Create test auctions

Place test bids

Provide feedback

📊 Governance Metrics
Metric	Current	Target (DAO)
Contributors	8	30+
Daily Visitors	24	100+
GitHub Issues	10+	Managed
PHNX Holders	0	500+
DAO Proposals	0	Monthly
🔗 Related Documents
Document	Link
DAO Operations	DAO_OPERATIONS.md
Vision	VISION.md
Current Focus	CURRENT-FOCUS.md
Roadmap	ROADMAP.md
Legal Documents	/docs/legal/
Contributing Guide	CONTRIBUTING.md
📝 Changelog
2026-02-24: Updated for TESTUSD, multi-wallet, added metrics

2026-02-21: Added recent decisions table

2026-02-14: Initial version (Bootstrap phase)

Last updated: February 24, 2026
*Next Milestone: March 6, 2026 - TX Testnet Launch* 🚀