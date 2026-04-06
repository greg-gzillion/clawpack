# PhoenixPME - Quick Start Guide

**Last Updated:** February 24, 2026  
**Project Status:** ✅ **LIVE!** Deployed on Render & Vercel  
**Next Milestone:** TX Testnet 6.0 Launch - March 6, 2026 (9 days)

## 🚧 Important Timeline Information

**The current Coreum testnet (v3.x) is NOT compatible with our smart contracts (built for v5.0+).**

### 📅 March 6, 2026 - TX TESTNET LAUNCHES
**This is when REAL TESTING BEGINS, NOT mainnet launch.**

On March 6:
- ✅ TX unified testnet (v6.0) goes live
- ✅ Smart contracts CAN be deployed
- ✅ Real testing of auctions/bids starts
- ⏳ Mainnet is still weeks/months away

### What This Means For You:
- **Now:** Use the live UI with mock data (testnet mode)
- **March 6+:** Help test real contracts on testnet
- **Future:** Mainnet launch after successful testing

**We're not launching March 6 - we're STARTING REAL TESTING March 6.**

---

## 🌐 Option 1: Use the Live Cloud Version (Easiest)

No installation needed! Visit:

| Service | URL |
|---------|-----|
| **Frontend App** | [https://phoenix-frontend-seven.vercel.app](https://phoenix-frontend-seven.vercel.app) |
| **Backend API** | [https://phoenix-api-756y.onrender.com](https://phoenix-api-756y.onrender.com) |
| **Live Prices** | [https://phoenix-api-756y.onrender.com/api/prices](https://phoenix-api-756y.onrender.com/api/prices) |
| **Health Check** | [https://phoenix-api-756y.onrender.com/health](https://phoenix-api-756y.onrender.com/health) |
| **Admin Panel** | [https://phoenix-frontend-seven.vercel.app/admin](password protected) |
| **Developer Sandbox** | [https://phoenix-frontend-seven.vercel.app/sandbox](https://phoenix-frontend-seven.vercel.app/sandbox) |

⚠️ Free tier spins down after inactivity. First request may take 30-50 seconds.

---

## 🔧 Wallet Setup

### ✅ Multi-Wallet Support Now Available!

We now support **4 different wallets** through our UniversalWalletV2:

| Wallet | Chain | Icon | Status |
|--------|-------|------|--------|
| **Keplr** | Cosmos | 🪐 | ✅ Working |
| **Leap** | Cosmos | 🐆 | ✅ Working |
| **MetaMask** | EVM | 🦊 | ✅ Working |
| **Phantom** | Solana | 👻 | ✅ Working |

### Step 1: Install Your Preferred Wallet

| Wallet | Installation | Best For |
|--------|--------------|----------|
| **Keplr** | [keplr.app](https://www.keplr.app) | Cosmos users |
| **Leap** | [leapwallet.io](https://www.leapwallet.io) | Cosmos users |
| **MetaMask** | [metamask.io](https://metamask.io) | EVM users |
| **Phantom** | [phantom.app](https://phantom.app) | Solana users |

### Step 2: Add Coreum Testnet to Your Wallet

#### For Keplr & Leap:
```json
{
  "chainId": "coreum-testnet-1",
  "chainName": "Coreum Testnet",
  "rpc": "https://full-node.testnet-1.coreum.dev:26657",
  "rest": "https://rest-full-node.testnet-1.coreum.dev",
  "bip44": { "coinType": 990 },
  "bech32Config": {
    "bech32PrefixAccAddr": "testcore",
    "bech32PrefixAccPub": "testcorepub"
  },
  "currencies": [{
    "coinDenom": "TESTCORE",
    "coinMinimalDenom": "utestcore",
    "coinDecimals": 6
  }],
  "feeCurrencies": [{
    "coinDenom": "TESTCORE",
    "coinMinimalDenom": "utestcore",
    "coinDecimals": 6
  }],
  "stakeCurrency": {
    "coinDenom": "TESTCORE",
    "coinMinimalDenom": "utestcore",
    "coinDecimals": 6
  },
  "gasPriceStep": { "low": 0.01, "average": 0.025, "high": 0.03 }
}
For MetaMask:
Open MetaMask

Click network dropdown → "Add Network"

Enter:

Network Name: Coreum Testnet

New RPC URL: https://full-node.testnet-1.coreum.dev:26657

Chain ID: 990

Currency Symbol: TESTCORE

Block Explorer URL: https://explorer.testnet-1.coreum.dev

For Phantom:
Phantom doesn't natively support Coreum yet. Use the sandbox mode for testing until March 6.

💰 Getting Test Tokens
⚠️ IMPORTANT: Token Order Matters
text
1. First, get TESTCORE (required for gas fees)
2. ONLY THEN can your address receive TESTUSD
3. Your address must be activated with TESTCORE first
Step 1: Get TESTCORE (Gas Fees)
Official Coreum Faucet:

Visit: https://faucet.testnet-1.coreum.dev

Enter your address (starts with testcore1...)

Complete CAPTCHA

Click "Request Funds"

You'll receive 10-20 TESTCORE instantly

Verify TESTCORE:

bash
curl https://rest-full-node.testnet-1.coreum.dev/cosmos/bank/v1beta1/balances/[YOUR-ADDRESS]
Step 2: Activate Your Address
✅ Your address is now ACTIVE and can receive other tokens.

Step 3: Get TESTUSD (For Auctions)
Manual Addition (Until March 6):

In Keplr, go to "Add Token" and enter:

Denom: utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6

Symbol: TESTUSD

Decimals: 6

After March 6:

bash
# Use PhoenixPME faucet (when available)
curl -X POST https://phoenix-api-756y.onrender.com/api/faucet \
  -H "Content-Type: application/json" \
  -d '{"address":"your-testcore-address"}'
✅ Verify Everything Works
Visit PhoenixPME

Click "Connect Wallet" (or go to Sandbox for multi-wallet testing)

Your address should appear

You should see TESTCORE balance

Price banner should show live metal prices

TESTUSD will appear after March 6

📊 Current Status (as of Feb 24, 2026)
Aspect	Status	Notes
Live Frontend	✅ Working	8 pages, responsive
Live Backend	✅ Working	API operational
Metal Prices	✅ Live	Updated manually via admin
Wallet Connection	✅ Multi-wallet	Keplr, Leap, MetaMask, Phantom
Admin Panel	✅ Working	Password protected
Sandbox Mode	✅ Working	Test wallets, auctions
Smart Contracts	✅ Ready	7 contracts, 16 tests
TESTUSD Token	✅ Ready	6 decimals, denom configured
TX Testnet	⏳ March 6	Launch in 9 days
📚 Official Coreum Documentation
Resource	Link	Purpose
Coreum Docs	docs.coreum.dev	Official documentation
Testnet Faucet	faucet.testnet-1.coreum.dev	Get TESTCORE
Coreum Discord	discord.gg/coreum	Community support
Explorer	explorer.testnet-1.coreum.dev	View transactions
Coreum Protocol Rules (From Official Docs)
Coin Type: 990 (Coreum's registered BIP44 coin type)

Bech32 Prefix: testcore (testnet), core (mainnet)

Minimum Gas: 0.01 utestcore

Token Denom Format: Minimal denom = base token name (e.g., utestcore)

❓ Troubleshooting
Problem	Solution
"No TESTCORE"	Use faucet - address must be funded first
"Address not active"	Fund with TESTCORE first
"Transaction fails"	Not enough TESTCORE for gas
TESTUSD not visible	Add manually using denom above
"Chain not found"	Double-check chain ID: coreum-testnet-1
Wallet not connecting	Try different wallet (MetaMask/Phantom in sandbox)
Price banner not showing	Check CORS, refresh page
🚀 Quick Commands Reference
Action	Command/URL
Live Frontend	https://phoenix-frontend-seven.vercel.app
Live API	https://phoenix-api-756y.onrender.com
Live Prices	https://phoenix-api-756y.onrender.com/api/prices
Coreum Faucet	https://faucet.testnet-1.coreum.dev
TESTUSD Denom	utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6
Check Balance	curl https://rest-full-node.testnet-1.coreum.dev/cosmos/bank/v1beta1/balances/[ADDRESS]
📋 Local Development Setup (For Developers)
If you want to run the platform locally:

Prerequisites
Node.js v20+

PostgreSQL v14+

Git

Quick Start (3 Terminals)
Terminal 1: Start Database

bash
sudo systemctl start postgresql
Terminal 2: Start Backend

bash
cd ~/dev/TX/apps/backend
npm install
npm run dev
Terminal 3: Start Frontend

bash
cd ~/dev/TX/apps/frontend
npm install
npm run dev
For more detailed technical setup, see SETUP_GUIDE.md

🔗 Quick Links
Resource	URL
GitHub Repo	https://github.com/greg-gzillion/TX
Architecture Docs	/docs/architecture/
Legal Documents	/docs/legal/
Current Focus	CURRENT-FOCUS.md
Roadmap	ROADMAP.md
Last Updated: February 24, 2026
*Next Milestone: March 6, 2026 - TX Testnet Launch (9 days)* 🚀