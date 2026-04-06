# PhoenixPME Architecture Overview
## Generated: February 24, 2026

## 🏗️ PROJECT STRUCTURE OVERVIEW
/home/greg/dev/TX/
├── apps/ → Application Services
├── contracts/ → Smart Contracts
├── docs/ → Documentation
├── scripts/ → Automation Scripts
└── tests/ → Test Suites

## 📦 MODULE 1: APPLICATIONS (`/apps`)

### **Purpose:** Core application services that power the PhoenixPME platform

#### 1.1 Backend (`/apps/backend`)
**Purpose:** Main API server handling business logic and database operations

backend/
├── src/ → Source code
│   ├── controllers/ → Request handlers
│   ├── routes/ → API endpoint definitions
│   │   ├── price.routes.ts → Metal price endpoints (updated with CORS)
│   │   ├── auction.routes.ts → Auction management
│   │   ├── admin.routes.ts → Admin panel for price updates
│   │   └── health.routes.ts → Health checks
│   ├── services/ → Business logic layer
│   │   └── priceOracle.ts → Price fetching & caching
│   ├── middleware/ → Auth, logging, error handling
│   ├── config/ → Environment configuration
│   └── lib/ → Utility functions
├── prisma/ → Database layer
│   ├── migrations/ → Database version control
│   └── schema.prisma → Database schema with PriceHistory model
└── dist/ → Compiled JavaScript

**Key Files:**
- `src/app.ts` - Express app with CORS configuration
- `src/routes/price.routes.ts` - Metal price API with manual updates
- `src/routes/admin.routes.ts` - Password-protected price updates
- `prisma/schema.prisma` - Database models

**Deployment:** Render (`https://phoenix-api-756y.onrender.com`)

#### 1.2 Frontend (`/apps/frontend`)
**Purpose:** Next.js web application for user interface

frontend/
├── app/ → Next.js pages (App Router)
│   ├── page.tsx → Homepage with live price banner
│   ├── layout.tsx → Root layout
│   ├── globals.css → Global styles
│   ├── auctions/
│   │   ├── page.tsx → Auction listing
│   │   ├── create/
│   │   │   └── page.tsx → Create auction form
│   │   └── [id]/
│   │       └── page.tsx → Auction detail (coming soon)
│   ├── admin/
│   │   └── page.tsx → Admin panel for price updates
│   └── sandbox/
│       └── page.tsx → Developer sandbox with multi-wallet
├── components/ → React components
│   ├── auctions/
│   │   ├── bid/
│   │   │   └── BidForm.tsx → Bid placement form
│   │   └── list/
│   │       ├── AuctionCard.tsx → Individual auction display (TESTUSD)
│   │       ├── AuctionList.tsx → Auction grid
│   │       └── index.ts → Barrel exports
│   ├── features/
│   │   └── sandbox/
│   │       ├── WalletSelector.tsx → Simple wallet (Keplr/Leap)
│   │       ├── TestWalletsPanel.tsx → Test wallet selector
│   │       ├── AuctionPlayground.tsx → Test auction creation
│   │       ├── PriceFeed.tsx → Test price display
│   │       └── ContractTester.tsx → Contract interaction test
│   ├── layout/
│   │   └── NavBar.tsx → Navigation
│   ├── phoenix/
│   │   ├── PhoenixIcon.tsx → Custom SVG phoenix icon
│   │   └── Tools.tsx → Developer tools (Excel shortcuts)
│   ├── shared/
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── FilterTabs.tsx
│   │       ├── PriceBanner.tsx → Live price display from API
│   │       └── index.ts → Barrel exports
│   └── UniversalWalletV2.tsx → Multi-chain wallet (Keplr, Leap, MetaMask, Phantom)
├── hooks/
│   └── useWallet.ts → Wallet connection hook
├── lib/
│   ├── contract/
│   │   └── phoenix-escrow.ts → Contract client with TESTUSD support
│   ├── contexts/
│   │   └── wallet-context.tsx → Wallet context provider
│   └── api.ts → API client for backend
└── public/
    ├── phoenix-icon.svg → Phoenix logo
    ├── phoenix-logo.svg → Alternate logo
    └── excel-shortcuts.png → Developer tools image

**Current Status (as of Feb 24, 2026):**
- ✅ Live price banner fetching from backend API
- ✅ Multi-wallet support (UniversalWalletV2)
- ✅ TESTUSD token integration throughout
- ✅ Admin panel for manual price updates
- ✅ Price update script (`/scripts/update-prices.sh`)
- ✅ Clean component organization (no duplicates)
- ✅ Successful production builds
- ✅ All TypeScript errors resolved
- ✅ Developer sandbox with wallet testing
- ✅ Custom Phoenix SVG icon with gradient
- ✅ Excel shortcuts reference for developers

**Deployment:** Vercel (`https://phoenix-frontend-seven.vercel.app`)

#### 1.3 Community Reserve Fund (formerly Insurance Module)
**Purpose:** 1.1% of platform fees accumulate in community-controlled treasury

**Key Changes (Feb 18-24, 2026):**
- ✅ Rebranded from "Insurance Pool" to "Community Reserve Fund"
- ✅ 100% of fees go to CRF (no individual access)
- ✅ 10% founder allocation (voting power only, not withdrawal)
- ✅ Funds locked until DAO governance active
- ✅ No insurance product - pure community treasury
- ✅ Address: `testcore1m5adn3k68tk4zqmujpnstmp9r933jafzu44tnv`

## 📦 MODULE 2: SMART CONTRACTS (`/contracts`)

### **Purpose:** CosmWasm smart contracts on TX blockchain

contracts/
├── phoenix-escrow/ → Main escrow contract with dual collateral
│   ├── src/
│   │   ├── contract.rs → Main contract logic
│   │   ├── msg.rs → Execute and query messages
│   │   ├── state.rs → State management
│   │   └── error.rs → Error handling
│   └── tests/
│       └── integration.rs → Integration tests
└── auction/ → Auction-specific contract (legacy)

**Status:** ✅ 7 contracts, 16 tests passing
**Target Chain:** TX (Coreum + Sologenic merger)
**Launch:** March 6, 2026

## 📦 MODULE 3: SCRIPTS (`/scripts`)

### **Purpose:** Automation and utility scripts

scripts/
├── update-prices.sh → Interactive price update script
├── update-prices-interactive.sh → User-friendly price updater
├── deploy-to-testnet.sh → Contract deployment (coming soon)
└── cleanup.sh → Project cleanup utility

**Key Features:**
- ✅ Password-protected admin updates
- ✅ Fetches current prices from API
- ✅ Interactive confirmation
- ✅ TESTUSD formatting (6 decimals)

## 📦 MODULE 4: DOCUMENTATION (`/docs`)

### **Purpose:** Project documentation and guides

docs/
├── setup/
│   ├── QUICK_START.md → Fast setup guide
│   └── SETUP_GUIDE.md → Detailed setup
├── legal/
│   ├── TERMS_OF_SERVICE.md
│   ├── PRIVACY_POLICY.md
│   ├── RISK_DISCLOSURE.md
│   └── CONTRIBUTOR_AGREEMENT.md
└── VISION.md → Project vision and philosophy

## 🔧 RECENT IMPROVEMENTS (Feb 24, 2026)

### ✅ Build System
- Fixed all TypeScript errors
- Updated `tsconfig.json` to ES2020 for BigInt support
- Converted `next.config.ts` to `next.config.js`
- Successful production builds

### ✅ Token Integration
- Migrated from CORE to TESTUSD throughout
- Updated contract client with TESTUSD denom
- Fixed conversion utilities
- Updated UI to display TESTUSD

### ✅ Wallet System
- Added `UniversalWalletV2` with multi-chain support
- Supports Keplr, Leap, MetaMask, Phantom
- Clean fallback for missing wallets
- Proper TypeScript types

### ✅ CORS Configuration
- Backend properly configured for both production and local
- Allowed origins: production domain and localhost
- Preflight requests handled correctly
- Price banner now working locally

## 🚀 DEPLOYMENT

| Service | URL | Status |
|---------|-----|--------|
| Frontend | https://phoenix-frontend-seven.vercel.app | ✅ Live |
| Backend API | https://phoenix-api-756y.onrender.com | ✅ Live |
| Database | PostgreSQL on Render | ✅ Connected |
| TESTUSD | Coreum testnet | ✅ Live |

## 🔑 ENVIRONMENT VARIABLES

### Backend (.env)
DATABASE_URL=postgresql://...
ADMIN_PASSWORD=[protected]
NODE_ENV=development
PORT=3001

### Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://phoenix-api-756y.onrender.com
NEXT_PUBLIC_CONTRACT_ADDRESS=[to be deployed March 6]


## 📊 TESTNET LAUNCH COUNTDOWN
**March 6, 2026** - 9 days remaining

## 🎯 NEXT MILESTONES
1. TX Testnet 6.0 launch (March 6)
2. Contract deployment
3. First test auctions
4. Community testing phase

# PhoenixPME Architecture Overview
## Generated: February 21, 2026

## 🏗️ PROJECT STRUCTURE OVERVIEW
/home/greg/dev/TX/
├── apps/ → Application Services
├── contracts/ → Smart Contracts
├── docs/ → Documentation
├── scripts/ → Automation Scripts
└── tests/ → Test Suites

## 📦 MODULE 1: APPLICATIONS (`/apps`)

### **Purpose:** Core application services that power the PhoenixPME platform

#### 1.1 Backend (`/apps/backend`)
**Purpose:** Main API server handling business logic and database operations

backend/
├── src/ → Source code
│   ├── controllers/ → Request handlers
│   ├── routes/ → API endpoint definitions
│   │   ├── price.routes.ts → Metal price endpoints (updated with logging)
│   │   ├── auction.routes.ts → Auction management
│   │   └── debug.routes.ts → Debug endpoints
│   ├── services/ → Business logic layer
│   │   └── priceOracle.ts → Price fetching & caching
│   ├── models/ → Data models
│   ├── middleware/ → Auth, logging, error handling
│   ├── validators/ → Input validation
│   ├── config/ → Environment configuration
│   └── lib/ → Utility functions
├── prisma/ → Database layer
│   ├── migrations/ → Database version control
│   └── schema.prisma → Database schema
└── dist/ → Compiled JavaScript

**Key Files:**
- `server.ts` - Entry point (port 3001)
- `prisma/schema.prisma` - Database models
- `src/routes/price.routes.ts` - Metal price API

#### 1.2 Frontend (`/apps/frontend`)
**Purpose:** Next.js web application for user interface

frontend/
├── app/ → Next.js pages
│   ├── page.tsx → Homepage with static reference prices
│   ├── auctions/
│   │   ├── page.tsx → Auction listing
│   │   ├── create/
│   │   │   └── page.tsx → Create auction form
│   │   └── [id]/
│   │       └── page.tsx → Auction detail (coming soon)
│   └── dashboard/
│       └── page.tsx → User dashboard
├── components/ → React components
│   ├── auctions/
│   │   ├── create/
│   │   │   └── index.tsx → Create auction form
│   │   └── list/
│   │       ├── AuctionCard.tsx → Individual auction display
│   │       └── AuctionList.tsx → Auction grid
│   ├── wallet/
│   │   └── WalletSelector.tsx → Keplr/Leap wallet connection
│   ├── layout/
│   │   └── NavBar.tsx → Navigation with wallet selector
│   └── shared/
│       ├── ui/
│       │   ├── Button.tsx
│       │   ├── FilterTabs.tsx
│       │   └── PriceBanner.tsx → Static reference prices
│       └── forms/inputs/
│           ├── MetalSelector.tsx
│           ├── WeightInput.tsx
│           ├── PuritySelector.tsx
│           ├── CertificationInput.tsx
│           ├── SerialNumberInput.tsx
│           ├── ImageUploader.tsx
│           ├── FormTypeSelector.tsx
│           └── PriceCalculator.tsx
├── hooks/
│   └── useWallet.ts → Mock wallet hook for testing
├── lib/
│   └── contract/
│       └── phoenix-escrow.ts → Contract client
└── types/
    └── auction.ts → TypeScript definitions

**Current Status (as of Feb 21, 2026):**
- ✅ Clean component organization (no duplicates)
- ✅ Consistent import patterns (default vs named)
- ✅ Wallet connection (Keplr/Leap)
- ✅ Static reference price banner (manual updates)
- ✅ Create auction form with all metal inputs
- ✅ Auction listing page
- ✅ Dashboard with user stats
- ✅ All test pages removed
- ✅ Vercel builds successful

#### 1.3 Community Reserve Fund (formerly Insurance Module)
**Purpose:** 1.1% of platform fees accumulate in community-controlled treasury

**Key Changes (Feb 18, 2026):**
- ✅ Rebranded from "Insurance Pool" to "Community Reserve Fund"
- ✅ 100% of fees go to CRF (no individual access)
- ✅ 10% founder allocation (voting power, not withdrawal)
- ✅ Funds locked until DAO governance active
- ✅ No insurance product - pure community treasury

**Structure:**