# PhoenixPME Frontend Architecture
**Last Updated:** February 24, 2026
**Version:** 3.0 (Multi-Wallet & TESTUSD Integration)

## 📋 Recent Changes (Feb 18-24, 2026)

| Change | Description | Date |
|--------|-------------|------|
| **Multi-wallet support** | Added UniversalWalletV2 (Keplr, Leap, MetaMask, Phantom) | Feb 23 |
| **TESTUSD integration** | Migrated from CORE to TESTUSD throughout | Feb 24 |
| **Build system stabilized** | All TypeScript errors resolved | Feb 24 |
| **Phoenix SVG icon** | Custom branding with gradient text | Feb 23 |
| **Price banner** | Live data from API with fallback | Feb 23 |
| **Admin panel** | Password-protected price updates | Feb 23 |
| **Sandbox mode** | Developer testing environment | Feb 23 |
| **Project cleanup** | Removed 30+ old files | Feb 22 |
| **Frontend reorganization** | Clean structure, no duplicates | Feb 21 |

---

## 🏗️ Current Structure (as of Feb 24, 2026)
frontend/
├── app/ # Next.js App Router pages
│ ├── page.tsx # Homepage with Phoenix branding
│ ├── layout.tsx # Root layout
│ ├── globals.css # Global styles
│ ├── auctions/
│ │ ├── page.tsx # Auctions listing
│ │ ├── create/
│ │ │ └── page.tsx # Create auction form
│ │ └── [id]/
│ │ └── page.tsx # Auction detail (planned)
│ ├── admin/
│ │ └── page.tsx # Admin panel for prices
│ └── sandbox/
│ └── page.tsx # Developer sandbox with multi-wallet
│
├── components/ # Reusable components
│ ├── auctions/
│ │ ├── bid/
│ │ │ └── BidForm.tsx # Bid placement with collateral
│ │ └── list/
│ │ ├── AuctionCard.tsx # Individual auction display (TESTUSD)
│ │ ├── AuctionList.tsx # Auction grid
│ │ └── index.ts # Barrel exports
│ ├── features/
│ │ └── sandbox/
│ │ ├── WalletSelector.tsx # Simple wallet (Keplr/Leap)
│ │ ├── TestWalletsPanel.tsx # Test wallet selector
│ │ ├── AuctionPlayground.tsx # Test auction creation
│ │ ├── PriceFeed.tsx # Test price display
│ │ └── ContractTester.tsx # Contract interaction test
│ ├── layout/
│ │ └── NavBar.tsx # Navigation with wallet
│ ├── phoenix/
│ │ ├── PhoenixIcon.tsx # Custom SVG phoenix icon
│ │ └── Tools.tsx # Developer tools (Excel shortcuts)
│ ├── shared/
│ │ └── ui/
│ │ ├── Button.tsx # Reusable button
│ │ ├── FilterTabs.tsx # Metal filter tabs
│ │ ├── PriceBanner.tsx # Live price display
│ │ ├── Toast.tsx # Notification system
│ │ └── index.ts # Barrel exports
│ └── UniversalWalletV2.tsx # Multi-wallet component
│
├── hooks/
│ └── useWallet.ts # Wallet connection hook
│
├── lib/
│ ├── api.ts # API service
│ ├── contract/
│ │ └── phoenix-escrow.ts # Contract client with TESTUSD
│ └── contexts/
│ └── wallet-context.tsx # Wallet context provider
│
├── public/
│ ├── phoenix-icon.svg # Phoenix logo
│ ├── phoenix-logo.svg # Alternate logo
│ └── excel-shortcuts.png # Developer tools image
│
├── next.config.js # Next.js config (redirects)
├── tsconfig.json # TypeScript config (ES2020)
└── package.json # Dependencies

---

## 🎯 Component Reference (Updated Feb 24, 2026)

| Component | Location | Purpose | Status |
|-----------|----------|---------|--------|
| **Homepage** | `app/page.tsx` | Main landing with Phoenix branding | ✅ COMPLETE |
| **NavBar** | `components/layout/NavBar.tsx` | Top navigation | ✅ COMPLETE |
| **UniversalWalletV2** | `components/UniversalWalletV2.tsx` | Multi-wallet (Keplr, Leap, MetaMask, Phantom) | ✅ NEW |
| **WalletSelector** | `components/features/sandbox/WalletSelector.tsx` | Simple wallet (sandbox) | ✅ KEPT |
| **PriceBanner** | `components/shared/ui/PriceBanner.tsx` | Live price display | ✅ UPDATED |
| **AuctionCard** | `components/auctions/list/AuctionCard.tsx` | Individual auction (TESTUSD) | ✅ UPDATED |
| **AuctionList** | `components/auctions/list/AuctionList.tsx` | Auction grid | ✅ UPDATED |
| **BidForm** | `components/auctions/bid/BidForm.tsx` | Bid placement with collateral | ✅ UPDATED |
| **PhoenixIcon** | `components/phoenix/PhoenixIcon.tsx` | Custom SVG logo | ✅ NEW |
| **Tools** | `components/phoenix/Tools.tsx` | Developer tools (Excel) | ✅ NEW |
| **Admin Panel** | `app/admin/page.tsx` | Password-protected price updates | ✅ NEW |
| **Sandbox** | `app/sandbox/page.tsx` | Developer testing environment | ✅ NEW |
| **Button** | `components/shared/ui/Button.tsx` | Reusable button | ✅ KEPT |
| **FilterTabs** | `components/shared/ui/FilterTabs.tsx` | Metal filter tabs | ✅ KEPT |
| **Toast** | `components/shared/ui/Toast.tsx` | Notification system | ✅ KEPT |
| **API Service** | `lib/api.ts` | Backend calls | ✅ UPDATED |
| **PhoenixEscrowClient** | `lib/contract/phoenix-escrow.ts` | Contract client with TESTUSD | ✅ UPDATED |

---

## 🔗 Live URLs (as of Feb 24, 2026)

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | [https://phoenix-frontend-seven.vercel.app](https://phoenix-frontend-seven.vercel.app) | ✅ LIVE |
| **Backend API** | [https://phoenix-api-756y.onrender.com](https://phoenix-api-756y.onrender.com) | ✅ LIVE |
| **Prices** | [https://phoenix-api-756y.onrender.com/api/prices](https://phoenix-api-756y.onrender.com/api/prices) | ✅ LIVE |
| **Health Check** | [https://phoenix-api-756y.onrender.com/health](https://phoenix-api-756y.onrender.com/health) | ✅ WORKING |
| **Admin Panel** | [https://phoenix-frontend-seven.vercel.app/admin](https://phoenix-frontend-seven.vercel.app/admin) | ✅ PASSWORD |
| **Sandbox** | [https://phoenix-frontend-seven.vercel.app/sandbox](https://phoenix-frontend-seven.vercel.app/sandbox) | ✅ LIVE |
| **Auctions** | [https://phoenix-frontend-seven.vercel.app/auctions](https://phoenix-frontend-seven.vercel.app/auctions) | ✅ LIVE |

---

## 🧹 Clean Folders Status

| Folder | Status | Contains |
|--------|--------|----------|
| `/components/shared/ui` | ✅ CLEAN | Button, FilterTabs, PriceBanner, Toast |
| `/components/layout` | ✅ CLEAN | NavBar |
| `/components/auctions` | ✅ CLEAN | bid/, list/ |
| `/components/features/sandbox` | ✅ CLEAN | Test wallets, playground |
| `/components/phoenix` | ✅ CLEAN | PhoenixIcon, Tools |
| `/lib/contract` | ✅ CLEAN | phoenix-escrow.ts |
| `/lib/contexts` | ✅ CLEAN | wallet-context.tsx |
| `/hooks` | ✅ CLEAN | useWallet.ts |
| `/app` | ✅ CLEAN | Pages only (no stray files) |

---

## 🚀 Build Status (as of Feb 24, 2026)
Route (app) Size First Load JS
┌ ○ / 5.38 kB 104 kB
├ ○ /_not-found 873 B 88.2 kB
├ ○ /admin 2.08 kB 89.4 kB
├ ○ /auctions 3.8 kB 99.8 kB
├ ƒ /auctions/[id] 6.43 kB 105 kB
├ ○ /auctions/create 8.79 kB 96.1 kB
└ ○ /sandbox 11.4 kB 98.7 kB

---

## 📝 Key Features Implemented

| Feature | Status | Details |
|---------|--------|---------|
| Multi-wallet support | ✅ COMPLETE | Keplr, Leap, MetaMask, Phantom |
| TESTUSD integration | ✅ COMPLETE | 6 decimal handling throughout |
| Live price banner | ✅ WORKING | Fetches from backend API |
| Admin panel | ✅ WORKING | Password-protected updates |
| Price update script | ✅ WORKING | Interactive bash script |
| Auction creation | ✅ COMPLETE | 8 components integrated |
| BidForm | ✅ COMPLETE | With collateral calculation |
| Sandbox mode | ✅ COMPLETE | Developer testing |
| Phoenix branding | ✅ COMPLETE | Custom SVG with gradient |
| Build system | ✅ STABLE | All TypeScript errors resolved |

---

## 🔄 Next Steps (Pre-March 6)

- ✅ Build system stabilized
- ✅ Multi-wallet complete
- ✅ TESTUSD integration done
- ✅ Documentation updated
- 🔜 Contract deployment (March 6)
- 🔜 First test auctions (March 6+)

---

## 🔗 Related Documentation

| Document | Link |
|----------|------|
| Architecture Overview | [ARCHITECTURE-OVERVIEW.md](../architecture/ARCHITECTURE-OVERVIEW.md) |
| Quick Start | [QUICK_START.md](../setup/QUICK_START.md) |
| Setup Guide | [SETUP_GUIDE.md](../setup/SETUP_GUIDE.md) |
| Current Focus | [CURRENT-FOCUS.md](../CURRENT-FOCUS.md) |
| Roadmap | [ROADMAP.md](../ROADMAP.md) |

---

## 📝 Changelog

- **2026-02-24:** Added multi-wallet, TESTUSD, Phoenix icon, admin panel, sandbox
- **2026-02-21:** Added TX testnet context, price banner, cleanup status
- **2026-02-18:** Initial post-reorganization documentation

---

*Documentation maintained by @greg-gzillion*
*Last Updated: February 24, 2026*
*Next Milestone: March 6, 2026 - TX Testnet Launch* 🚀