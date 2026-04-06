# PhoenixPME Test Wallets
**Last Updated:** February 24, 2026
**Network:** Coreum Testnet / TX Testnet (March 6)
**Chain ID:** coreum-testnet-1

---

## 🏦 Test Wallet Registry

### User Wallets (Coreum Testnet)

| Name | Address | TESTCORE | TESTUSD | Last Verified | Notes |
|------|---------|----------|---------|---------------|-------|
| **Robert** | `testcore1xa352f6gtgc4g7c9rrdgl4wn9vaw9r25v47jen` | ✓ 9.97 | ✓ 5,000,000 | Feb 24, 2026 | Full user |
| **Alice** | `testcore14qkw9fplr9xplfl5qwz8rr8f3uxhja8yuf0z6l` | ✓ 9.97 | ✓ 5,000,000 | Feb 24, 2026 | Full user |
| **Charlie** | `testcore1urvw6ta906qphvvrmcuwwxy3z2fqns56er2agu` | ✓ 9.97 | ✓ 5,000,000 | Feb 24, 2026 | Full user |
| **Mike** | `testcore1rr8knhdwc9uthxh3fazt3k4keuqtycctzcvd3c` | ✓ 9.97 | ✓ 5,000,000 | Feb 24, 2026 | Full user |

### System Wallets

| Name | Address | TESTCORE | TESTUSD | Purpose | Last Verified |
|------|---------|----------|---------|---------|---------------|
| **Treasury** | `testcore19krrq7dtfck53dla2us9lxlmmzxg7d9wa6qkdm` | ✓ 10.0 | ✓ 1,000,000 | Multi-sig, DAO treasury | Feb 24, 2026 |
| **Deployer** | `testcore1wvrwgqjqfu7t9qzz3h05384ltjtnzfqlrytkmj` | ✓ 10.0 | ✓ 1,000,000 | Contract deployment | Feb 24, 2026 |
| **CRF** | `testcore1m5adn3k68tk4zqmujpnstmp9r933jafzu44tnv` | ✓ 10.0 | ✓ Accumulating | Community Reserve Fund | Feb 24, 2026 |

---

## 💰 Updated Wallet Balances (as of Feb 24, 2026)

| Name | TESTCORE | TESTUSD | Role |
|------|----------|---------|------|
| **Robert** | 9.97 | 5,000,000 | Full user |
| **Alice** | 9.97 | 5,000,000 | Full user |
| **Charlie** | 9.97 | 5,000,000 | Full user |
| **Mike** | 9.97 | 5,000,000 | Full user |
| **Treasury** | 10.0 | 1,000,000 | System |
| **Deployer** | 10.0 | 1,000,000 | System |
| **CRF** | 10.0 | 0 (accumulating) | System |

---

## 🔧 TESTUSD Token Configuration

### Token Details
| Field | Value |
|-------|-------|
| **Denom** | `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6` |
| **Symbol** | `TESTUSD` |
| **Decimals** | `6` |
| **Transaction** | `37EC84596A02687D8F77E7D92538F518CCE847D8B4A325732B911FD0B0D35E9A` |

### Adding TESTUSD to Wallets

#### Option 1: Manual Addition (For All Wallets)
1. Open Keplr extension
2. Click on Coreum Testnet
3. Click "Manage Tokens" → "Add Token"
4. Enter:
   - **Denom:** `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6`
   - **Symbol:** `TESTUSD`
   - **Decimals:** `6`
5. Click "Add"

#### Option 2: Chain Configuration Update
In `UniversalWalletV2.tsx` and `WalletSelector.tsx`, ensure the chain config includes:

```typescript
currencies: [
  {
    coinDenom: 'TESTCORE',
    coinMinimalDenom: 'utestcore',
    coinDecimals: 6,
  },
  {
    coinDenom: 'TESTUSD',
    coinMinimalDenom: 'utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6',
    coinDecimals: 6,
  },
],
🦊 Multi-Wallet Support (UniversalWalletV2)
Our new UniversalWalletV2 component supports multiple wallet types for testing:

Wallet	Chain	Supported	Notes
Keplr	Cosmos	✅ Yes	Full support
Leap	Cosmos	✅ Yes	Full support
MetaMask	EVM	✅ Yes	Testnet support
Phantom	Solana	✅ Yes	Testnet support
Sandbox Testing
Visit /sandbox to test all wallet types with mock data.

⚠️ TESTUSD Visibility Solution
The Issue
✅ TESTCORE balance shows correctly

✅ TESTUSD token exists on-chain

⚠️ TESTUSD not auto-visible in Keplr

The Fix (Applied Feb 24, 2026)
✅ Added TESTUSD to chain configuration

✅ Updated UniversalWalletV2 with proper denom

✅ All system wallets now have TESTUSD

✅ Users can manually add or wait for auto-configuration

📊 Wallet Distribution Plan
Current Distribution
Wallet Type	TESTUSD Amount	Purpose
User Wallets (4)	5,000,000 each	Testing auctions/bids
Treasury	1,000,000	DAO simulation
Deployer	1,000,000	Contract deployment
CRF	0 (accumulating)	Fee collection
Planned Distribution (Post-March 6)
Faucet for testers

Automatic distribution to new wallets

Fee accumulation in CRF

PHNX governance weight tracking

🔜 Next Steps
Pre-March 6
✅ All wallets funded with TESTCORE

✅ TESTUSD added to system wallets

✅ Documentation updated

✅ Multi-wallet testing complete

March 6 Launch
🔜 Deploy contracts to TX Testnet

🔜 Enable faucet for TESTUSD

🔜 First test auctions with all wallets

🔜 Track fee accumulation in CRF

Post-Launch
📝 Add more test wallets as needed

📝 Track PHNX governance weight

📝 Monitor TRUST/DONT TRUST tokens

🔗 Related Documentation
Document	Link
TESTUSD Token	TESTUSD_TOKEN.md
Quick Start	QUICK_START.md
Architecture	ARCHITECTURE-OVERVIEW.md
Sandbox	/sandbox
📝 Changelog
2026-02-24: Updated all wallet balances, added Treasury/Deployer/CRF, multi-wallet support

2026-02-21: Added TX testnet context, TESTUSD visibility solution

2026-02-18: Initial test wallet documentation

Last Updated: February 24, 2026
*Next Milestone: March 6, 2026 - TX Testnet Launch* 🚀