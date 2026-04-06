# PhoenixPME TX Architecture
## Date: 2026-02-24

# Architecture Documentation
## Location: `/docs/architecture/`

This folder contains system architecture documents for the PhoenixPME platform.

## 📋 PURPOSE OF THIS FOLDER

The `architecture/` directory houses all documentation related to:
- **System design** - High-level architecture decisions
- **Component relationships** - How modules interact
- **Data flow diagrams** - Information movement
- **Technical specifications** - Implementation details
- **Architecture Decision Records (ADRs)** - Key technical choices

---

## 📚 DOCUMENTS IN THIS FOLDER

| Document | Purpose | Last Updated |
|----------|---------|--------------|
| `ARCHITECTURE-OVERVIEW.md` | Complete system architecture breakdown | 2026-02-24 |
| `BRIDGE_SECURITY.md` | Cross-chain bridge security architecture | 2026-02-15 |
| `ORACLE_DESIGN.md` | Delivery verification oracle system | 2026-02-24 |
| `SECURITY_PATTERNS.md` | Smart contract security best practices | 2026-02-18 |
| `README.md` | This file - folder guide | 2026-02-24 |

---

## 🏗️ WHAT BELONGS HERE

### ✅ **Do place these in this folder:**
- System architecture diagrams
- Component interaction models
- Database schema designs
- API architecture decisions
- Security architecture
- Deployment architecture
- Scalability plans
- Technology stack decisions
- Architecture Decision Records (ADRs)

### ❌ **Do NOT place these here:**
- User guides → `/docs/guides/`
- Setup instructions → `/docs/setup/`
- Business documents → `/docs/business/`
- Legal agreements → `/docs/legal/`
- Development guides → `/docs/development/`
- Test files → `/docs/test-files/`

---

## 📊 ARCHITECTURE LAYERS
┌─────────────────────────────────────┐
│ Presentation Layer │
│ (Frontend - Next.js) │
│ - React Components │
│ - Wallet Integration │
│ - Multi-wallet (Universal) │
├─────────────────────────────────────┤
│ Application Layer │
│ (Backend - Express) │
│ - REST API │
│ - Admin Panel │
│ - Price Management │
├─────────────────────────────────────┤
│ Service Layer │
│ (Community Reserve Fund) │
│ - 1.1% Fee Collection │
│ - DAO Governance (future) │
├─────────────────────────────────────┤
│ Data Layer │
│ (PostgreSQL, Prisma) │
│ - Price History │
│ - User Data │
│ - Auction Metadata │
├─────────────────────────────────────┤
│ Blockchain Layer │
│ (TX Blockchain - Coreum + Sologenic)│
│ - Smart Contracts (CosmWasm) │
│ - TESTUSD Token │
│ - Dual Collateral Escrow │
│ - TRUST/DONT TRUST Reputation │
└─────────────────────────────────────┘

---

## 🔗 KEY ARCHITECTURE DECISIONS

| Decision | Status | Documented In |
|----------|--------|---------------|
| Monorepo Structure | ✅ Implemented | `ARCHITECTURE-OVERVIEW.md` |
| Multi-wallet Support | ✅ Implemented (UniversalWalletV2) | `ARCHITECTURE-OVERVIEW.md` |
| Modular Backend (MVC) | ✅ Implemented | `ARCHITECTURE-OVERVIEW.md` |
| Smart Contract Isolation | ✅ Implemented | `ARCHITECTURE-OVERVIEW.md` |
| TESTUSD Token Integration | ✅ Implemented | `ARCHITECTURE-OVERVIEW.md` |
| Dual Collateral Mechanism | ✅ Implemented | `ARCHITECTURE-OVERVIEW.md` |
| TRUST/DONT TRUST System | 📝 Planned | `ARCHITECTURE-OVERVIEW.md` |
| Multi-Oracle Design | 📝 Planned | `ORACLE_DESIGN.md` |
| Bridge Security | 📝 Planned | `BRIDGE_SECURITY.md` |
| DAO Governance | 📝 Future | `ECONOMIC_MODEL.md` |

---

## 🔧 CURRENT TECHNICAL STACK (as of Feb 24, 2026)

### Frontend
- **Framework:** Next.js 14.2.35 (App Router)
- **Language:** TypeScript 5.4.5
- **Styling:** Tailwind CSS
- **Wallet Integration:** UniversalWalletV2 (Keplr, Leap, MetaMask, Phantom)
- **Icons:** Lucide React + Custom SVG
- **Deployment:** Vercel

### Backend
- **Framework:** Express.js
- **Language:** TypeScript
- **Database:** PostgreSQL with Prisma ORM
- **API:** REST
- **Authentication:** Wallet-based (JWT planned)
- **Deployment:** Render

### Blockchain
- **Network:** TX (Coreum + Sologenic merger)
- **Smart Contracts:** CosmWasm (Rust)
- **Token:** TESTUSD (6 decimals)
- **Contract Status:** 7 contracts, 16 tests passing
- **Launch Date:** March 6, 2026 (Testnet 6.0)

### Key Services
- **Price Management:** Admin panel + manual update scripts
- **File Storage:** Local (public folder), IPFS planned
- **Email:** SMTP (planned)
- **Monitoring:** Vercel Analytics, Render Logs

---

## 📁 REPOSITORY STRUCTURE
/home/greg/dev/TX/
├── apps/
│ ├── frontend/ # Next.js application
│ │ ├── app/ # Pages & layouts
│ │ ├── components/ # React components
│ │ │ ├── auctions/ # Auction-related components
│ │ │ ├── features/ # Feature-specific components
│ │ │ ├── layout/ # Layout components
│ │ │ ├── phoenix/ # Brand components
│ │ │ ├── shared/ # Reusable UI components
│ │ │ └── UniversalWalletV2.tsx # Multi-wallet
│ │ ├── hooks/ # Custom React hooks
│ │ ├── lib/ # Utilities & clients
│ │ │ └── contract/ # Smart contract client
│ │ ├── public/ # Static assets
│ │ └── package.json # Dependencies
│ └── backend/ # Express API
│ ├── src/
│ │ ├── routes/ # API endpoints
│ │ ├── services/ # Business logic
│ │ ├── middleware/ # Express middleware
│ │ └── lib/ # Utilities
│ ├── prisma/ # Database schema
│ └── package.json # Dependencies
├── contracts/ # Smart contracts
│ └── phoenix-escrow/ # Main escrow contract
├── docs/ # Documentation
│ ├── architecture/ # System architecture
│ ├── legal/ # Legal documents (14 files)
│ └── setup/ # Setup guides
├── scripts/ # Automation scripts
│ ├── update-prices.sh # Price update script
│ └── cleanup.sh # Project cleanup
└── tests/ # Test suites

---

## 🔄 DATA FLOW

### Auction Creation Flow
ser Input → Form Validation → Convert to uTESTUSD →
Smart Contract Call → Transaction Broadcast →
Indexer Event → Database Record → UI Update

### Bid Placement Flow
User Input → Balance Check → Convert to uTESTUSD →
Smart Contract Call → Escrow Lock →
Event Emission → UI Update → Real-time Bid Display

### Price Update Flow (Admin)
Admin Script → Password Auth → Price Input →
Backend API → Database Update →
Frontend Polling → Price Banner Update

---

## 🔒 SECURITY ARCHITECTURE

### Smart Contract Security
- **Dual Collateral:** Both parties post 10% collateral
- **Escrow:** Funds locked until delivery confirmation
- **Non-transferable Tokens:** PHNX, TRUST, DONT TRUST have no cash value
- **KYC Binding:** One identity, one reputation

### API Security
- **CORS:** Configured for specific origins
- **Rate Limiting:** Planned
- **Admin Auth:** Password-protected endpoints
- **Input Validation:** All endpoints validated

### Frontend Security
- **Wallet Signatures:** All transactions require wallet approval
- **Environment Variables:** Sensitive data in .env.local
- **Content Security Policy:** Planned

---

## 🚀 DEPLOYMENT ARCHITECTURE

### Production URLs
| Service | URL | Status |
|---------|-----|--------|
| Frontend | https://phoenix-frontend-seven.vercel.app | ✅ Live |
| Backend API | https://phoenix-api-756y.onrender.com | ✅ Live |
| Health Check | https://phoenix-api-756y.onrender.com/health | ✅ Working |
| Admin Panel | https://phoenix-frontend-seven.vercel.app/admin | ✅ Working |
| Sandbox | https://phoenix-frontend-seven.vercel.app/sandbox | ✅ Working |

### Deployment Process
1. **Push to GitHub** (`main` branch)
2. **Vercel** auto-deploys frontend
3. **Render** auto-deploys backend
4. **Database** migrations run automatically
5. **Health checks** verify deployment

---

## 🧪 TESTNET LAUNCH ARCHITECTURE (March 6, 2026)

### Pre-Launch (Current)
- ✅ Frontend built and tested
- ✅ Backend deployed and configured
- ✅ Database schema finalized
- ✅ Smart contracts compiled and tested
- ✅ Price update scripts ready

### Testnet (March 6, 2026)
