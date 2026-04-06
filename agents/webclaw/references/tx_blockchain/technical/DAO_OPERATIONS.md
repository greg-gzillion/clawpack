# PhoenixPME DAO Operations & Governance

**Last updated:** February 24, 2026
**Status:** Living Document - Pre-DAO Phase
**Current Phase:** ⚠️ Preparation & Launch (9 days until TX Testnet)

---

## Core Philosophy
PhoenixPME will be governed by its users through a Decentralized Autonomous Organization (DAO). The protocol's parameters—including the 1.1% fee—are transparently encoded in smart contracts. Future governance will allow the community to decide how accumulated funds are used.

**Current Status:** ⚠️ DAO NOT YET ACTIVE. Funds accumulate in Community Reserve Fund with **no withdrawal ability** until DAO forms (estimated Q3-Q4 2026).

---

## Phase 0: Preparation & Launch (Current - Feb 24, 2026)

**Objective:** Build, test, and prepare for testnet launch.

### Current Status:
| Area | Status | Details |
|------|--------|---------|
| Frontend | ✅ Live | [phoenix-frontend-seven.vercel.app](https://phoenix-frontend-seven.vercel.app) |
| Backend | ✅ Live | [phoenix-api-756y.onrender.com](https://phoenix-api-756y.onrender.com) |
| Smart Contracts | ✅ Ready | 7 contracts, 16 tests passing |
| Multi-Wallet | ✅ Complete | Keplr, Leap, MetaMask, Phantom |
| TESTUSD Token | ✅ Ready | 6 decimals, denom configured |
| Mock Mode | ✅ Active | UI testing ready |
| Legal Documentation | ✅ Complete | 14 documents |
| Community Reserve Fund | ⏳ Test mode | Accumulating after March 6 |
| TX Testnet Launch | ⏳ March 6 | 9 days remaining |

### Fee Status:
| Aspect | Detail |
|--------|--------|
| **Protocol Fee** | 1.1% hardcoded (not yet active) |
| **Destination** | Community Reserve Fund |
| **Withdrawal** | ❌ **NO ONE can withdraw** (not even founder) |
| **Current Balance** | 0 TESTUSD (test mode pending) |

### Governance (Pre-DAO):
- Informal, guided by founder (@greg-gzillion)
- Community input via GitHub Issues
- No on-chain voting yet
- 8 contributors already participating

### Exit Condition:
- ✅ Contracts ready
- ✅ Frontend/backend live
- ✅ Documentation complete
- 🔜 TX testnet deployment (March 6)
- 🔜 First real auction completed
- 🔜 Community Reserve Fund accumulates first fees

---

## Phase 1: Bootstrap & Foundation (Post-Launch - Q2 2026)

**Objective:** Launch a secure, functional MVP. Acquire the first 100 users and prove the protocol's value.

### Fee Structure (Hardcoded, Immutable):
| Aspect | Detail |
|--------|--------|
| **Protocol Fee** | **1.1%** (encoded in contract, cannot be changed) |
| **Destination** | Community Reserve Fund |
| **Founder Allocation** | **10% voting weight** (not withdrawal rights) |
| **Community** | **90% voting weight** (earned through participation) |
| **Withdrawal** | ❌ No individual can withdraw funds |

### PHNX Governance Weight Distribution:
- **Earned through:** 1 PHNX per 1 TESTUSD in fees generated
- **Non-transferable:** Cannot be bought, sold, or transferred
- **Voting weight:** 1 PHNX = 1 vote
- **Total supply:** Dynamic (earned, not minted)

### Treasury Allocation (To Be Voted):
| Allocation | Purpose |
|------------|---------|
| **50%** | Security (Smart contract audits, bug bounties) |
| **30%** | Protocol Maintenance (Oracle servers, infrastructure) |
| **20%** | Community Initiatives (Grants, education) |

### Governance Process:
1. **Discussion:** Proposals debated in GitHub Discussions
2. **Formal Proposal:** Submitted on-chain (requires 5% quorum)
3. **Voting Period:** 7 days
4. **Execution:** If passed, funds allocated as voted

### TRUST/DONT TRUST Reputation:
- **TRUST:** 1 token minted per successful trade
- **DONT TRUST:** 1 token minted per failed obligation
- **Non-transferable:** Permanent on-chain record
- **KYC-bound:** One identity, one reputation

### Goals:
- First 100 successful testnet trades
- Security audit completion
- TRUST/DONT TRUST system live
- Community governance framework established

### Exit Condition:
- Consistent monthly volume exceeds **$10,000**
- DAO vote to move to Phase 2

---

## Phase 2: Sustainable Operations (Q3-Q4 2026)

**Trigger:** Successful on-chain DAO vote after Phase 1 goals met.

### Fee Structure (Immutable):
| Aspect | Detail |
|--------|--------|
| **Protocol Fee** | **1.1%** (remains hardcoded) |
| **Destination** | Community Reserve Fund |
| **Founder Stake** | 10% voting weight (maintained) |
| **Community** | 90% voting weight |

### Treasury Allocation (Example Proposal):
| Allocation | Purpose |
|------------|---------|
| **40%** | Development Grants (building new features) |
| **30%** | Security & Operations |
| **20%** | Growth & Partnerships |
| **10%** | Community Treasury (emergency reserve) |

### Expanded Governance:
- Multi-oracle delivery system active
- Dispute resolution module operational
- Community-elected arbitrators
- Grant program for developers

### Goals:
- Self-sustaining ecosystem
- Builder grants from treasury
- Volume milestones: $100k/month
- Multiple asset support (gold, silver, platinum, palladium)

### Exit Condition:
- DAO vote to move to Phase 3
- Volume exceeds $1M/month

---

## Phase 3: Full Decentralization (2027+)

**Trigger:** DAO vote, proven track record, mature community.

### Governance Evolution:
- Community-elected council (optional)
- Parameter adjustments (within limits)
- Cross-chain expansion
- Mobile app ecosystem

### Treasury Maturity:
- Multiple revenue streams
- Investment in ecosystem projects
- Sustainable funding for core team
- Community dividends (if voted)

---

## How Value is Distributed (Immutable)

The smart contracts include two non-negotiable economic protections encoded at deployment:

```solidity
// Cannot be changed by any governance vote
1. 1.1% protocol fee → Community Reserve Fund
2. Founder retains 10% voting weight (not withdrawal rights)
3. NO INDIVIDUAL can withdraw from Community Reserve Fund
4. PHNX, TRUST, DONT TRUST tokens are non-transferable
Why These Are Immutable:
Legal protection: No securities risk

User trust: Cannot be changed to extract value

Fairness: Community controls treasury, not individuals

Permanence: Reputation follows forever

Current Contributors
Contributor	Role	Since
@greg-gzillion	Founder/Lead Dev	Feb 2026
@dependabot	Dependency Management	Feb 2026
6 others	Code contributions	Feb 2026
Join us! See CONTRIBUTING.md

📊 Key Metrics to Watch
Metric	Current	Phase 1 Target	Phase 2 Target
Daily Users	24	100	1,000
Monthly Volume	$0	$10,000	$100,000
Contributors	8	15	30
PHNX Holders	0	50	500
CRF Balance	0 TESTUSD	$1,000	$10,000
🔗 Related Documentation
Document	Link
Vision	VISION.md
Architecture	ARCHITECTURE-OVERVIEW.md
Security Patterns	SECURITY_PATTERNS.md
Current Focus	CURRENT-FOCUS.md
Roadmap	ROADMAP.md
Legal Documents	/docs/legal/
📝 Changelog
2026-02-24: Updated for TESTUSD, multi-wallet, added Phase details

2026-02-21: Initial version (Pre-DAO Phase)

Last Updated: February 24, 2026
*Next Milestone: March 6, 2026 - TX Testnet Launch* 🚀