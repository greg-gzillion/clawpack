# Project Health Summary
## Generated: February 14, 2026

## ✅ WORKING:
- Directory structure organized (clean root, proper docs folders)
- All source code preserved and consolidated
- Wallet integration: Keplr + Leap working with 7 roles
- Auction creation form with all 8 components
- TESTUSD token created on Coreum testnet
- Insurance pool features (FeeDisplay, InsurancePoolBalance)
- Mock wallet system (7 wallets in tests/fixtures/wallets/)
- All documentation updated and consistent

## 🚧 IN PROGRESS:
- Auction contract tests for main auction contract
- Frontend-backend API integration
- Auction listing page
- Bid placement UI

## 📅 COUNTDOWN:
- **Days until TX mainnet:** 20 (March 6, 2026)
- **MVP completion:** 80%

## Run in SEPARATE terminals:

### Terminal 1 - Backend:

```bash

cd apps/backend && npm install && npm run dev
# Runs on http://localhost:3001

cd apps/frontend && npm install && npm run dev
# Runs on http://localhost:3000

cd apps/insurance-module && npm install && npm start
# Runs on port 3200-3204

🔑 Key Wallet Roles:
Role	Type	Purpose
Treasury	Mock	Admin (13M)
Deployer	Mock	Deployment (5M)
Insurance	Mock	Pool (0)
Seller	REAL	List items 📦
Alice	REAL	Bid 💰
Bob	REAL	Bid 💰
Charlie	REAL	Bid 💰
📊 Test Pages:
http://localhost:3000/test-wallet - Test wallet connections

http://localhost:3000/test-all/metal - Test MetalSelector

http://localhost:3000/auctions/create - Create auction form

http://localhost:3000/auctions/1 - Auction detail page

📚 Documentation Locations:
Architecture: /docs/architecture/

Business: /docs/business/

Development: /docs/development/

Legal: /docs/legal/

Ideas (future): /docs/ideas/

🎯 Current Focus:
See CURRENT-FOCUS.md for MVP scope.
See ROADMAP.md for release timeline.

Last updated: February 14, 2026


