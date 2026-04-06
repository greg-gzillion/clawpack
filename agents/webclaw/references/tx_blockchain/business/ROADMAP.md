# PhoenixPME: Phoenix Precious Metals Exchange Roadmap
**Formerly:** coreum-pme  
**Current Status:** Pre-Testnet Launch  
**Last Updated:** February 24, 2026  
**Next Milestone:** TX Testnet 6.0 Launch - March 6, 2026 (9 days)

## Phase 0: Foundation (COMPLETED)
- ✅ Organization setup
- ✅ Repository creation (`greg-gzillion/TX`)
- ✅ Manifesto creation ([VISION.md](../VISION.md))
- ✅ Core documentation (14 legal docs)
- ✅ Project rebrand from "coreum-pme" to "PhoenixPME"
- ✅ GitHub organization established
- ✅ Development environment configured

## Phase 1: Specification & Design (95% COMPLETE)
- ✅ Complete technical specification ([ARCHITECTURE-OVERVIEW.md](./architecture/ARCHITECTURE-OVERVIEW.md))
- ✅ UI/UX wireframes (implemented in code)
- ✅ Smart contract architecture ([phoenix-escrow](../../contracts/phoenix-escrow/))
- ✅ Multi-wallet design (UniversalWalletV2)
- ✅ Dual collateral mechanism specified
- ✅ TESTUSD token integration design
- ✅ Community building (767 cloners, 8 contributors)
- ⏳ Multi-oracle delivery specification (in design)
- ⏳ DAO governance framework (planned)

## Phase 2: Development (95% COMPLETE)

### Smart Contracts (✅ COMPLETE)
- ✅ Auction escrow contract (CosmWasm)
- ✅ Dual collateral implementation
- ✅ 1.1% fee mechanism
- ✅ TESTUSD token support
- ✅ 7 contracts with 16 passing tests
- ✅ 193KB optimized WASM

### Frontend (✅ COMPLETE)
- ✅ Next.js application with App Router
- ✅ Multi-wallet support (Keplr, Leap, MetaMask, Phantom)
- ✅ Auction creation form (8 components)
- ✅ Auction listing and detail pages
- ✅ BidForm with collateral calculation
- ✅ Admin panel for price updates
- ✅ Developer sandbox
- ✅ TESTUSD integration throughout
- ✅ Phoenix branding with custom SVG

### Backend (✅ COMPLETE)
- ✅ Express.js API
- ✅ PostgreSQL database with Prisma
- ✅ Price management endpoints
- ✅ Admin authentication
- ✅ CORS configuration
- ✅ Deployed on Render

### Integration (⏳ IN PROGRESS)
- ✅ Frontend-backend connected
- ✅ TESTUSD token integration complete
- ⏳ Testnet deployment (March 6, 2026)
- ⏳ XRPL integration (post-MVP)
- ⏳ Multi-oracle system (post-launch)

## Phase 3: Launch & Growth

### Testnet Launch (March 6, 2026) 🔜
- ⏳ Deploy contracts to TX Testnet 6.0
- ⏳ First test auctions and bids
- ⏳ Community testing program
- ⏳ Bug fixes and iterations
- ⏳ Performance optimization

### Mainnet Launch (Q2 2026) 📝
- Security audit
- Mainnet contract deployment
- First real trades
- Volume milestones tracking

### Ecosystem Growth (Q3-Q4 2026) 📝
- TRUST/DONT TRUST reputation system
- PHNX governance weight accumulation
- First vault partnerships
- Tokenomics implementation (fee distribution)
- DAO formation and governance
- Multi-oracle delivery verification
- Cross-chain bridge (XRPL)

## 📊 Progress Summary

| Phase | Progress | Status |
|-------|----------|--------|
| Phase 0: Foundation | 100% | ✅ Complete |
| Phase 1: Specification | 95% | ✅ Near Complete |
| Phase 2: Development | 95% | ✅ Near Complete |
| Phase 3: Launch | 10% | ⏳ March 6 |
| **Overall** | **75%** | 🔜 Launch in 9 days |

## 📈 Key Metrics

| Metric | Current | Target |
|--------|---------|--------|
| GitHub clones | 3,175 | 5,000 (MVP) |
| Unique cloners | 843 | 1,500 (MVP) |
| Contributors | 8 | 15 (MVP) |
| Daily visitors | 24 | 100 (post-launch) |
| Smart contract tests | 16 passing | 20+ |
| Pages generated | 8 | 12 |
| Testnet launch | ⏳ 9 days | March 6 |

## 🚀 Launch Timeline

### Pre-Launch (Feb 24 - March 5)
- ✅ Code cleanup and stabilization
- ✅ Document updates
- ✅ Dependency updates (safe patches)
- ⏳ Prepare deployment scripts
- ⏳ Draft launch announcements
- ⏳ Prepare testnet tokens

### Launch Day (March 6)

00:01 UTC - TX Testnet 6.0 launches
00:15 UTC - Deploy phoenix-escrow contract
00:30 UTC - Update frontend with contract address
00:45 UTC - Redeploy frontend to Vercel
01:00 UTC - Create first test auction
01:30 UTC - Place first test bid
02:00 UTC - Complete first trade
03:00 UTC - Verify 1.1% fee to CRF
04:00 UTC - Announce to community
08:00 UTC - Open to testers


## 🔧 Tech Stack

| Layer | Technology | Status |
|-------|------------|--------|
| Blockchain | TX (Coreum + Sologenic) | ⏳ Testnet March 6 |
| Smart Contracts | CosmWasm (Rust) | ✅ Complete |
| Frontend | Next.js 14, TypeScript | ✅ Complete |
| Backend | Express, PostgreSQL | ✅ Complete |
| Wallet | UniversalWalletV2 | ✅ Complete |
| Token | TESTUSD | ✅ Ready |
| Hosting | Vercel + Render | ✅ Live |

## 🤝 How to Contribute

We're actively seeking:

**Coreum/CosmWasm developers**
- Skills: Rust, CosmWasm, Coreum testnet experience
- Tasks: Multi-oracle system, contract optimizations
- Status: 8 contributors already, more welcome

**Testnet testers**
- Skills: Keplr/Leap wallet, interest in metals
- Tasks: Test auctions on March 6, provide feedback
- Status: ⏳ Sign up now (email gjf20842@gmail.com)

**Community moderators**
- Skills: Knowledge of precious metals markets
- Tasks: Help grow and manage community
- Status: Ongoing

## 📝 Related Documents

- [VISION.md](../VISION.md) - Project philosophy
- [CURRENT-FOCUS.md](./CURRENT-FOCUS.md) - What we're building now
- [ROADMAP.md](./ROADMAP.md) - Full roadmap
- [ARCHITECTURE-OVERVIEW.md](./architecture/ARCHITECTURE-OVERVIEW.md) - System design
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| Live Frontend | https://phoenix-frontend-seven.vercel.app |
| Live Backend | https://phoenix-api-756y.onrender.com |
| GitHub Repo | https://github.com/greg-gzillion/TX |
| Admin Panel | /admin (password protected) |
| Sandbox | /sandbox |

---

*Original project: coreum-pme → Rebranded to PhoenixPME*
*Last Updated: February 24, 2026*
*Next Milestone: March 6, 2026 - TX Testnet Launch* 🚀