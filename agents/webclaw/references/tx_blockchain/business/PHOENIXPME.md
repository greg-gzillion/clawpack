# PhoenixPME Auction Platform - Roadmap

**Last Updated:** February 24, 2026  
**Next Milestone:** March 6, 2026 - TX Testnet 6.0 Launch (9 days)

## ✅ CURRENT STATUS (as of Feb 24, 2026)

| Priority | Items | Progress |
|----------|-------|----------|
| MVP Launch | 7 items | 5/7 complete (71%) |
| Testnet Phase | 4 items | 0/4 (0%) - starts March 6 |
| Enhanced Features | 4 items | 0/4 (0%) |
| ICEBOX | 3 items | Not started |

**Next milestone:** March 6, 2026 - TX testnet launch (9 days remaining)

---

## PRIORITY 1: MVP Launch - PREPARATION PHASE
**Status: ✅ 5/7 Complete**

### ✅ COMPLETED (Pre-Launch)

| Item | Status | Notes |
|------|--------|-------|
| TESTUSD token integration | ✅ Complete | 6 decimals, UI ready |
| Basic listing/bidding interface | ✅ Complete | Create auction form, BidForm |
| Wallet connection | ✅ Complete | UniversalWalletV2 (Keplr, Leap, MetaMask, Phantom) |
| Price management system | ✅ Complete | Admin panel + update scripts |
| Frontend/backend infrastructure | ✅ Complete | Vercel + Render, stable builds |

### 🚧 IN PROGRESS (Ready for March 6)

| Item | Status | Notes |
|------|--------|-------|
| Core escrow smart contract | ✅ Ready | 193KB, 7 contracts, 16 tests passing |
| Contract deployment | ⏳ March 6 | Waiting for TX Testnet 6.0 |
| 1.1% fee collection to CRF | ⏳ March 6 | Contract ready, needs testnet |

**What's left for MVP Launch:**
- Deploy contract to testnet (March 6)
- Connect frontend to live contract (March 6)
- Test end-to-end flow (March 6+)

---

## PRIORITY 2: Testnet Phase
**Target: March 6 - April 2026**

| Item | Status | Target |
|------|--------|--------|
| Contract deployment | ⏳ March 6 | Day 1 |
| First test auction | ⏳ March 6 | Day 1 |
| Bid placement testing | ⏳ March 6+ | Week 1 |
| Complete trade with dual collateral | ⏳ March 6+ | Week 1 |
| Community testing program | 📝 Planned | Week 2-3 |
| Bug fixes and iterations | 📝 Planned | Ongoing |
| Performance optimization | 📝 Planned | April |

---

## PRIORITY 3: Enhanced Features
**Target: Q2-Q3 2026**

| Item | Status | Target |
|------|--------|--------|
| TRUST/DONT TRUST reputation system | 📝 Planned | Q2 2026 |
| PHNX governance weight accumulation | 📝 Planned | Q2 2026 |
| Advanced auction types | 📝 Planned | Q2 2026 |
| Dispute resolution system | 📝 Planned | Q3 2026 |
| Multi-oracle delivery verification | 📝 Design | Q3 2026 |
| Shipping/tracking integration | 📝 Research | Q3 2026 |
| Community Reserve Fund DAO voting | 📝 Future | Q4 2026 |

---

## PRIORITY 4: ICEBOX (Future)
**Target: 2026+ (community-driven)**

- [ ] Real RLUSD integration (production stablecoin)
- [ ] PCGS/NGC partnership for graded coins
- [ ] Collectibles registry (NFT representation)
- [ ] Inventory management system for dealers
- [ ] Mobile apps
- [ ] Batch auctions
- [ ] Dealer API access

---

## 📊 PROGRESS TRACKING

| Date | Milestone | Status |
|------|-----------|--------|
| Feb 5, 2026 | Project started | ✅ Complete |
| Feb 18, 2026 | Frontend/backend live | ✅ Complete |
| Feb 21, 2026 | Frontend reorganization | ✅ Complete |
| Feb 23, 2026 | Multi-wallet integration | ✅ Complete |
| Feb 24, 2026 | TESTUSD integration | ✅ Complete |
| Feb 24, 2026 | Build system stabilized | ✅ Complete |
| **March 6, 2026** | **TX Testnet 6.0 launch** | 🔜 9 days |
| March 6-31, 2026 | Testnet testing phase | ⏳ Planned |
| April 2026 | MVP mainnet launch | 📝 Planned |
| Q2 2026 | Reputation system (TRUST/DONT TRUST) | 📝 Planned |
| Q3 2026 | PHNX governance activation | 📝 Planned |
| Q4 2026 | DAO voting for CRF | 📝 Future |

---

## 🚀 LAUNCH DAY TIMELINE (March 6, 2026)
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


---

## 📈 METRICS TARGETS

| Metric | Current | MVP Target | End of 2026 |
|--------|---------|------------|-------------|
| GitHub clones | 3,175 | 5,000 | 10,000+ |
| Unique cloners | 843 | 1,500 | 3,000+ |
| Testnet testers | 0 | 50 | 200+ |
| Mainnet users | 0 | 100 | 1,000+ |
| Monthly volume | 0 | $10K | $100K+ |
| Contributors | 8 | 15 | 30+ |

---

## 🔄 HOW WE PRIORITIZE

1. **Must work** for peer-to-peer metal trading
2. **Must be secure** (dual collateral)
3. **Must be simple** (no feature creep)
4. **Community feedback** guides future priorities

---

## 📝 RECENT COMPLETIONS (Feb 21-24)

| Date | Achievement |
|------|-------------|
| Feb 24 | Multi-wallet support (UniversalWalletV2) |
| Feb 24 | TESTUSD integration complete |
| Feb 24 | All TypeScript errors resolved |
| Feb 24 | Build successful (8 pages) |
| Feb 23 | Phoenix SVG icon with gradient |
| Feb 23 | Price banner fetching live data |
| Feb 23 | CORS issues resolved |
| Feb 22 | Project cleanup (30+ old files removed) |

---

## ⚠️ KNOWN RISKS & MITIGATIONS

| Risk | Impact | Mitigation |
|------|--------|------------|
| TX blockchain adoption | High | Portable contracts, could migrate |
| Testnet delays | Medium | Buffer built into timeline |
| Security vulnerabilities | High | 16 tests passing, audit planned |
| User adoption | Medium | Building community pre-launch |
| Competition | Low | First mover on TX, dual collateral unique |

---

## 🔗 QUICK LINKS

| Resource | URL |
|----------|-----|
| Live Frontend | https://phoenix-frontend-seven.vercel.app |
| Live Backend | https://phoenix-api-756y.onrender.com |
| GitHub Repo | https://github.com/greg-gzillion/TX |
| Admin Panel | /admin (password protected) |
| Sandbox | /sandbox |
| Current Focus | [CURRENT-FOCUS.md](./CURRENT-FOCUS.md) |
| Architecture | [ARCHITECTURE-OVERVIEW.md](./architecture/ARCHITECTURE-OVERVIEW.md) |

---

## 🦅 PHOENIXPME VISION

A peer-to-peer precious metals exchange where:
- 1.1% fees go to Community Reserve Fund
- Both parties post 10% collateral
- 48-hour buyer verification
- Permanent on-chain reputation (TRUST/DONT TRUST)
- Users govern the platform via PHNX voting weight

**Built on TX Blockchain (Coreum + Sologenic merger)**


---

## 📈 METRICS TARGETS

| Metric | Current | MVP Target | End of 2026 |
|--------|---------|------------|-------------|
| GitHub clones | 3,175 | 5,000 | 10,000+ |
| Unique cloners | 843 | 1,500 | 3,000+ |
| Testnet testers | 0 | 50 | 200+ |
| Mainnet users | 0 | 100 | 1,000+ |
| Monthly volume | 0 | $10K | $100K+ |
| Contributors | 8 | 15 | 30+ |

---

## 🔄 HOW WE PRIORITIZE

1. **Must work** for peer-to-peer metal trading
2. **Must be secure** (dual collateral)
3. **Must be simple** (no feature creep)
4. **Community feedback** guides future priorities

---

## 📝 RECENT COMPLETIONS (Feb 21-24)

| Date | Achievement |
|------|-------------|
| Feb 24 | Multi-wallet support (UniversalWalletV2) |
| Feb 24 | TESTUSD integration complete |
| Feb 24 | All TypeScript errors resolved |
| Feb 24 | Build successful (8 pages) |
| Feb 23 | Phoenix SVG icon with gradient |
| Feb 23 | Price banner fetching live data |
| Feb 23 | CORS issues resolved |
| Feb 22 | Project cleanup (30+ old files removed) |

---

## ⚠️ KNOWN RISKS & MITIGATIONS

| Risk | Impact | Mitigation |
|------|--------|------------|
| TX blockchain adoption | High | Portable contracts, could migrate |
| Testnet delays | Medium | Buffer built into timeline |
| Security vulnerabilities | High | 16 tests passing, audit planned |
| User adoption | Medium | Building community pre-launch |
| Competition | Low | First mover on TX, dual collateral unique |

---

## 🔗 QUICK LINKS

| Resource | URL |
|----------|-----|
| Live Frontend | https://phoenix-frontend-seven.vercel.app |
| Live Backend | https://phoenix-api-756y.onrender.com |
| GitHub Repo | https://github.com/greg-gzillion/TX |
| Admin Panel | /admin (password protected) |
| Sandbox | /sandbox |
| Current Focus | [CURRENT-FOCUS.md](./CURRENT-FOCUS.md) |
| Architecture | [ARCHITECTURE-OVERVIEW.md](./architecture/ARCHITECTURE-OVERVIEW.md) |

---

## 🦅 PHOENIXPME VISION

A peer-to-peer precious metals exchange where:
- 1.1% fees go to Community Reserve Fund
- Both parties post 10% collateral
- 48-hour buyer verification
- Permanent on-chain reputation (TRUST/DONT TRUST)
- Users govern the platform via PHNX voting weight

**Built on TX Blockchain (Coreum + Sologenic merger)**


*Last Updated: February 24, 2026*
*Next Update: March 6, 2026 (Launch Day!)*