# Technical FAQ

**Last Updated:** February 24, 2026  
**Current Status:** Pre-TX Testnet Launch (9 days remaining)

---

## General Questions

### Q: What is PhoenixPME?
A: A peer-to-peer precious metals exchange built on the TX blockchain (Coreum + Sologenic merger). Users can trade gold, silver, platinum, and palladium with 1.1% fees, dual collateral (10% both parties), and permanent on-chain reputation.

### Q: Is it live yet?
A: ✅ Frontend and backend are live at [phoenix-frontend-seven.vercel.app](https://phoenix-frontend-seven.vercel.app). Smart contracts will deploy to TX Testnet 6.0 on **March 6, 2026** (9 days).

### Q: What's the current status?
A: 
- ✅ Frontend/backend: Live (Vercel + Render)
- ✅ Multi-wallet: Supported (Keplr, Leap, MetaMask, Phantom)
- ✅ TESTUSD token: Ready (6 decimals)
- ✅ Smart contracts: Ready (7 contracts, 16 tests)
- ⏳ TX Testnet: March 6, 2026
- ⏳ Real auctions: March 6+

---

## Development & Contribution

### Q: How do I contribute code?
A: 
1. Fork the repo: [github.com/greg-gzillion/TX](https://github.com/greg-gzillion/TX)
2. Pick an issue from [PROJECTS_NEW.md](../../PROJECTS_NEW.md) or open a new one
3. Create a branch, make your changes
4. Submit a Pull Request
5. Get reviewed within 48 hours

### Q: What's the tech stack?
A: 
| Layer | Technology |
|-------|------------|
| **Blockchain** | TX (Coreum + Sologenic merger) |
| **Smart Contracts** | CosmWasm (Rust) |
| **Frontend** | Next.js 14, TypeScript, Tailwind CSS |
| **Backend** | Express.js, PostgreSQL, Prisma |
| **Wallet** | UniversalWalletV2 (Keplr, Leap, MetaMask, Phantom) |
| **Token** | TESTUSD (6 decimals) |
| **Hosting** | Vercel (frontend), Render (backend) |

### Q: How do developers get paid?
A: Through grants from the Community Reserve Fund after DAO formation (estimated Q3 2026). See [CONTRIBUTOR_GUIDE.md](../../CONTRIBUTOR_GUIDE.md) for details.

### Q: What if I'm not good at explaining things verbally?
A: Perfect! We value **code and written documentation** over verbal communication. GitHub Issues and PRs are our primary communication channels.

### Q: Can I ask technical questions?
A: Yes! Open a GitHub Issue with the `technical` label. We aim to respond within 24-48 hours.

### Q: Is there real-time chat?
A: No. We use **GitHub Issues** for all discussions to maintain permanent, searchable documentation. This ensures decisions and answers are never lost in ephemeral chat.

### Q: How quickly will you respond to PRs?
A: All technical contributions are reviewed within **48 hours**. Smaller PRs often get reviewed sooner.

### Q: How are technical decisions made?
A: Through GitHub Issues discussions:
1. **Problem identified** in issue
2. **Options discussed** in comments
3. **Consensus emerges** from community
4. **Decision documented** in issue
5. **Implementation** via PR
6. **Documentation updated** in `/docs`

---

## Smart Contracts

### Q: What smart contracts are implemented?
A: 7 contracts with 16 passing tests:
- Phoenix Escrow (main auction logic)
- Dual collateral management
- 1.1% fee distribution
- TESTUSD token integration
- Auction creation and bidding
- Dispute resolution (planned)
- TRUST/DONT TRUST reputation (planned)

### Q: When will contracts be deployed?
A: **March 6, 2026** - TX Testnet 6.0 launch. Contracts are ready and waiting.

### Q: What blockchain are you using?
A: **TX blockchain** - the merger of Coreum and Sologenic. Optimized for Real World Assets (RWA) like precious metals.

### Q: Are contracts audited?
A: Internal tests (16 passing) are complete. External audit planned for Q2 2026 before mainnet.

---

## Wallet & Tokens

### Q: What wallets are supported?
A: **UniversalWalletV2** supports:
- 🪐 **Keplr** (Cosmos)
- 🐆 **Leap** (Cosmos)
- 🦊 **MetaMask** (EVM)
- 👻 **Phantom** (Solana)

### Q: What tokens do I need?
A: 
| Token | Purpose | How to Get |
|-------|---------|------------|
| **TESTCORE** | Gas fees | [Coreum Faucet](https://faucet.testnet-1.coreum.dev) |
| **TESTUSD** | Auctions | Add manually (denom below) |

TESTUSD Denom: `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6`

### Q: How do I add TESTUSD to Keplr?
A: 
1. Open Keplr
2. Go to "Add Token"
3. Enter:
   - **Denom:** `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6`
   - **Symbol:** TESTUSD
   - **Decimals:** 6

### Q: What about PHNX, TRUST, DONT TRUST tokens?
A: These are **non-transferable** and have **no cash value**:
- **PHNX:** Governance weight (earned from fees)
- **TRUST:** Positive reputation (earned from successful trades)
- **DONT TRUST:** Negative reputation (earned from failures)

---

## Testing & Development

### Q: How do I run the project locally?
A: Follow the [Setup Guide](../setup/SETUP_GUIDE.md). Quick start:
```bash
# Terminal 1: Database
sudo systemctl start postgresql

# Terminal 2: Backend
cd apps/backend && npm run dev

# Terminal 3: Frontend
cd apps/frontend && npm run dev