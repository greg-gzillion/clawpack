# TX Blockchain Integration Notice

## 🎯 Project Context
This PhoenixPME project has been reorganized and prepared for deployment on the 
**TX blockchain**, which represents the merger of Coreum and Sologenic.

**Last Updated:** February 24, 2026  
**Days Until TX Testnet Launch:** 9

---

## 🔗 Blockchain Integration

| Aspect | Details |
|--------|---------|
| **Primary Chain** | TX (Coreum + Sologenic merger) |
| **Current Testnet** | Coreum testnet (v3.x - NOT compatible for contracts) |
| **TX Testnet** | Launches March 6, 2026 (v6.0 - fully compatible) |
| **TX Mainnet** | Q2 2026 (estimated) |
| **Smart Contracts** | CosmWasm (7 contracts, 16 tests passing) |
| **Contract Size** | 193KB optimized WASM |
| **Wallet Compatibility** | Keplr, Leap, MetaMask, Phantom (UniversalWalletV2) |

---

## 💰 Token Information

| Token | Purpose | Denom | Status |
|-------|---------|-------|--------|
| **TESTCORE** | Gas fees | `utestcore` | ✅ Available now |
| **TESTUSD** | Auction currency | `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6` | ✅ Denom ready |
| **PHNX** | Governance weight | Non-transferable | 📝 Post-launch |
| **TRUST** | Positive reputation | Non-transferable | 📝 Post-launch |
| **DONT TRUST** | Negative reputation | Non-transferable | 📝 Post-launch |

---

## 🚀 Migration Path

### Phase 1: Preparation (Current - Feb 24)
- ✅ Project reorganized (2026-02-21)
- ✅ Smart contracts ready (7 contracts, 16 tests)
- ✅ Multi-wallet integration complete
- ✅ TESTUSD token integration
- ✅ Frontend/backend live on Vercel/Render
- ✅ Documentation updated

### Phase 2: Mock Mode (Now - March 5)
- ✅ UI fully functional with mock data
- ✅ Price banner fetching live data
- ✅ Admin panel for manual updates
- ✅ Wallet connection testing
- ✅ Developer sandbox available

### Phase 3: TX Testnet Launch (March 6)
- 🔜 00:01 UTC - TX Testnet 6.0 launches
- 🔜 00:15 UTC - Deploy phoenix-escrow contract
- 🔜 00:30 UTC - Update frontend with contract address
- 🔜 01:00 UTC - First test auction
- 🔜 Community testing begins

### Phase 4: Mainnet (Q2 2026)
- 📝 Security audit
- 📝 Mainnet contract deployment
- 📝 Real TESTUSD trading
- 📝 DAO governance formation

---

## 📊 Current Status (as of Feb 24, 2026)

| Component | Status | URL |
|-----------|--------|-----|
| Frontend | ✅ Live | [phoenix-frontend-seven.vercel.app](https://phoenix-frontend-seven.vercel.app) |
| Backend | ✅ Live | [phoenix-api-756y.onrender.com](https://phoenix-api-756y.onrender.com) |
| Smart Contracts | ✅ Ready | 7 contracts, 16 tests |
| Multi-Wallet | ✅ Complete | Keplr, Leap, MetaMask, Phantom |
| TESTUSD Token | ✅ Ready | 6 decimals, denom configured |
| Admin Panel | ✅ Working | Password protected |
| Price Banner | ✅ Working | Live data from API |
| TX Testnet | ⏳ March 6 | 9 days remaining |

---

## 🔧 Wallet Setup for TX Testnet

### Supported Wallets
| Wallet | Chain | Installation |
|--------|-------|--------------|
| **Keplr** | Cosmos | [keplr.app](https://www.keplr.app) |
| **Leap** | Cosmos | [leapwallet.io](https://www.leapwallet.io) |
| **MetaMask** | EVM | [metamask.io](https://metamask.io) |
| **Phantom** | Solana | [phantom.app](https://phantom.app) |

### Getting TESTCORE (Gas Fees)
1. Visit [Coreum Faucet](https://faucet.testnet-1.coreum.dev)
2. Enter your address (starts with `testcore1...`)
3. Complete CAPTCHA
4. Receive 10-20 TESTCORE instantly

### Adding TESTUSD Manually
In Keplr, go to "Add Token" and enter:
- **Denom:** `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6`
- **Symbol:** TESTUSD
- **Decimals:** 6

---

## 📝 Documentation Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| Architecture Overview | ✅ Complete | 2026-02-24 |
| Security Patterns | ✅ Complete | 2026-02-24 |
| Oracle Design | ✅ Updated | 2026-02-24 |
| Quick Start Guide | ✅ Updated | 2026-02-24 |
| Setup Guide | ✅ Updated | 2026-02-24 |
| Current Focus | ✅ Updated | 2026-02-24 |
| Roadmap | ✅ Updated | 2026-02-24 |
| Legal Documents (14) | ✅ Complete | 2026-02-21 |

---

## 🎯 Key Features Ready for TX

### Smart Contracts
- ✅ Dual collateral (10% both parties)
- ✅ 1.1% fee to Community Reserve Fund
- ✅ Auction creation and bidding logic
- ✅ Escrow management
- ✅ TESTUSD token integration

### Frontend
- ✅ Multi-wallet support (UniversalWalletV2)
- ✅ Auction creation form (8 components)
- ✅ BidForm with collateral calculation
- ✅ Price banner with live data
- ✅ Admin panel for updates
- ✅ Developer sandbox

### Backend
- ✅ Express.js API
- ✅ PostgreSQL database
- ✅ Price management
- ✅ Admin authentication
- ✅ CORS configured

---

## 📞 Contact

| Purpose | Contact |
|---------|---------|
| TX Integration Inquiries | gjf20842@gmail.com |
| Technical Questions | [GitHub Issues](https://github.com/greg-gzillion/TX/issues) |
| Security | security@phoenixpme.com (private) |
| Community | [GitHub Discussions](https://github.com/greg-gzillion/TX/discussions) |

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| Live Frontend | [phoenix-frontend-seven.vercel.app](https://phoenix-frontend-seven.vercel.app) |
| Live Backend | [phoenix-api-756y.onrender.com](https://phoenix-api-756y.onrender.com) |
| GitHub Repo | [github.com/greg-gzillion/TX](https://github.com/greg-gzillion/TX) |
| Coreum Faucet | [faucet.testnet-1.coreum.dev](https://faucet.testnet-1.coreum.dev) |
| Coreum Docs | [docs.coreum.dev](https://docs.coreum.dev) |

---

*This project maintains full legal continuity from original PhoenixPME.*
*Last Updated: February 24, 2026*
*Next Milestone: March 6, 2026 - TX Testnet 6.0 Launch* 🚀