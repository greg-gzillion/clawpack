# PhoenixPME - Precious Metals Exchange Protocol

**Last Updated:** February 24, 2026  
**Current Phase:** Pre-TX Testnet Launch (9 days remaining)  
**Live Frontend:** [phoenix-frontend-seven.vercel.app](https://phoenix-frontend-seven.vercel.app)  
**Live Backend:** [phoenix-api-756y.onrender.com](https://phoenix-api-756y.onrender.com)  
**GitHub:** [github.com/greg-gzillion/TX](https://github.com/greg-gzillion/TX)

---

## 🏛️ Overview
A blockchain-based auction protocol for physical precious metals (gold, silver, platinum, palladium) with integrated **dual collateral** and **Community Reserve Fund**.

**Built on TX Blockchain** (Coreum + Sologenic merger)  
**Target Testnet Launch:** March 6, 2026

---

## ✅ Current Status (as of Feb 24, 2026)

| Component | Status | Details |
|-----------|--------|---------|
| **Frontend** | ✅ LIVE | [phoenix-frontend-seven.vercel.app](https://phoenix-frontend-seven.vercel.app) |
| **Backend** | ✅ LIVE | [phoenix-api-756y.onrender.com](https://phoenix-api-756y.onrender.com) |
| **Multi-Wallet** | ✅ SUPPORTED | Keplr, Leap, MetaMask, Phantom |
| **TESTUSD Token** | ✅ READY | 6 decimals, denom configured |
| **Smart Contracts** | ✅ READY | 7 contracts, 16 tests passing |
| **Price Banner** | ✅ WORKING | Live metal prices from API |
| **Admin Panel** | ✅ WORKING | Password-protected updates |
| **TX Testnet** | ⏳ March 6 | 9 days to launch |

---

## 🪙 TESTUSD Token - Live on Coreum Testnet

The foundation token for PhoenixPME auctions is operational on Coreum testnet (TX-compatible).

| Detail | Value |
|--------|-------|
| **Symbol** | TESTUSD |
| **Denom** | `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6` |
| **Decimals** | 6 |
| **Transaction** | [37EC84596A02687D8F77E7D92538F518CCE847D8B4A325732B911FD0B0D35E9A](https://explorer.testnet-1.coreum.dev/coreum/transaction/37EC84596A02687D8F77E7D92538F518CCE847D8B4A325732B911FD0B0D35E9A) |

📄 [TESTUSD Token Creation Docs](docs/TESTUSD_TOKEN_CREATION.md)

---

## 🔧 Core Components

### 1. Auction Platform
| Aspect | Detail |
|--------|--------|
| **Purpose** | Peer-to-peer trading of physical precious metals |
| **Fee** | **1.1%** per successful transaction (hardcoded) |
| **Destination** | Community Reserve Fund |
| **Collateral** | **10% both parties** (seller + buyer) |
| **Verification** | 48-hour buyer inspection period |

**Features:**
- ✅ Buy It Now & bidding functionality
- ✅ Reference market prices (updated manually via admin)
- ✅ Seller-set grading premiums (purity, certification)
- ✅ TX blockchain settlement (March 6+)

### 2. Token System (Non-Transferable)

| Token | Purpose | How You Get It |
|-------|---------|----------------|
| **PHNX** | Governance weight | 1 PHNX per 1 TESTUSD in fees generated |
| **TRUST** | Positive reputation | 1 per successful trade |
| **DONT TRUST** | Negative reputation | 1 per failed obligation |

**All tokens:**
- ❌ NON-TRANSFERABLE
- 💰 $0 CASH VALUE
- 🔗 KYC-bound via TX blockchain
- ⏳ Permanent on-chain record

### 3. Community Reserve Fund
| Aspect | Detail |
|--------|--------|
| **Source** | 1.1% of all successful trades |
| **Control** | Future DAO (PHNX holders) |
| **Withdrawal** | ❌ **NO INDIVIDUAL** can withdraw |
| **Founder** | 10% voting weight only (permanent) |
| **Address** | `testcore1m5adn3k68tk4zqmujpnstmp9r933jafzu44tnv` |

---

## 📊 Fee Structure (Immutable)

```solidity
// Cannot be changed by any governance vote
1. 1.1% protocol fee → Community Reserve Fund
2. NO INDIVIDUAL can withdraw from CRF
3. PHNX, TRUST, DONT TRUST are non-transferable
4. Founder retains 10% voting weight (permanent)

Wallet Support

Wallet	Chain	Status
Keplr	Cosmos	✅ Supported
Leap	Cosmos	✅ Supported
🚀 Technical Architecture
Layer	Technology	Port/URL
Frontend	Next.js 14, TypeScript, Tailwind	3000
Backend	Express.js, PostgreSQL, Prisma	3001
Blockchain	TX (Coreum + Sologenic)	Testnet March 6
Smart Contracts	CosmWasm (Rust)	7 contracts, 16 tests
Database	PostgreSQL on Render	Connected
📁 Repository Structure
text
/home/greg/dev/TX/
├── apps/
│   ├── frontend/          # Next.js app (Vercel)
│   │   ├── app/           # Pages & layouts
│   │   ├── components/     # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── lib/           # Contract client, API
│   │   └── public/        # Static assets
│   └── backend/           # Express API (Render)
│       ├── src/
│       │   ├── routes/    # API endpoints
│       │   ├── services/  # Business logic
│       │   └── lib/       # Utilities
│       └── prisma/        # Database schema
├── contracts/             # Smart contracts
│   └── phoenix-escrow/    # Main escrow contract
├── docs/                  # Documentation
│   ├── architecture/      # System design
│   ├── legal/             # 14 legal documents
│   └── setup/             # Setup guides
└── scripts/               # Automation scripts
    └── update-prices.sh   # Price update script
🚀 Quick Start
Use Live Version (No Installation)
Frontend: https://phoenix-frontend-seven.vercel.app

Sandbox: /sandbox

Admin: /admin (password protected)

Run Locally
bash
# Clone repo
git clone https://github.com/greg-gzillion/TX.git
cd TX

# Backend
cd apps/backend
npm install
npm run dev

# Frontend (new terminal)
cd apps/frontend
npm install
npm run dev
See QUICK_START.md for details.

📅 Roadmap
Phase	Timeline	Status
Foundation	Jan-Feb 2026	✅ Complete
TX Testnet Launch	March 6, 2026	🔜 9 days
Testnet Testing	March-April 2026	⏳ Planned
TRUST/DONT TRUST	Q2 2026	📝 Planned
PHNX Governance	Q2 2026	📝 Planned
Mainnet Launch	Q3 2026	📝 Planned
🤝 Contributing
We welcome contributors! See:

CONTRIBUTING.md

CURRENT-FOCUS.md

ROADMAP.md

Current priorities:

✅ Multi-wallet integration
✅ TESTUSD token support
✅ Build system stabilization
🔜 Contract deployment (March 6)
🔜 Testnet testing
⚖️ Legal & Compliance
Document	Purpose
Terms of Service	Platform usage agreement
Privacy Policy	Data handling
Risk Disclosure	Important risks
Contributor Agreement	Contribution terms
Key Legal Facts:
✅ Code is original work by Greg (@greg-gzillion)
✅ Licensed under GNU GPL v3.0
✅ "PhoenixPME" name in use (not registered trademark)
✅ No securities - tokens have no cash value

📞 Contact
Purpose	Contact
Technical Questions	gjf20842@gmail.com
GitHub Issues	github.com/greg-gzillion/TX/issues
Security	security@phoenixpme.com (private)
🦅 Keywords
TX Blockchain Coreum Sologenic CosmWasm Precious Metals Gold Silver Platinum Palladium RWA DEX Escrow P2P Marketplace Dual Collateral Community Reserve Fund TESTUSD

Last Updated: February 24, 2026
*Next Milestone: March 6, 2026 - TX Testnet Launch* 🚀

## Related Repositories

- **[TX](https://github.com/greg-gzillion/TX)** - PhoenixPME auction implementation
- **[Claw-Coder](https://github.com/greg-gzillion/claw-coder)** - AI agent for compliance validation
