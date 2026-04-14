# TESTUSD Token - Live on Coreum Testnet ✅

**Last Updated:** February 24, 2026  
**Status:** ✅ OPERATIONAL (Ready for TX Testnet)  
**Next Milestone:** March 6, 2026 - TX Testnet 6.0 Launch

---

## 🎉 Token Creation Success
**Date:** February 2026
**Transaction:** `37EC84596A02687D8F77E7D92538F518CCE847D8B4A325732B911FD0B0D35E9A`
**Explorer:** [View on Coreum Explorer](https://explorer.testnet-1.coreum.dev/coreum/transaction/37EC84596A02687D8F77E7D92538F518CCE847D8B4A325732B911FD0B0D35E9A)

---

## 📋 Token Details

| Attribute | Value |
|-----------|-------|
| **Symbol** | TESTUSD |
| **Denom** | `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6` |
| **Decimals** | 6 |
| **Initial Supply** | 1000 TESTUSD |
| **Issuer** | `testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6` |

---

## 💰 Current Distribution

| Wallet | Amount | Purpose |
|--------|--------|---------|
| **Issuer Wallet** | 900 TESTUSD | Admin, fees, distribution |
| **Test Wallet** | 100 TESTUSD | `testcore1u5mnmlezme6nw9d9xtk086p2az9jk96syrnn67` |

---

## 🔧 Wallet Configuration

### For Leap Wallet
| Field | Value |
|-------|-------|
| **Coin minimal denom** | `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6` |
| **Coin denom** | TESTUSD |
| **Coin decimals** | 6 |

### For Keplr Wallet
1. Open Keplr
2. Go to "Add Token"
3. Enter:
   - **Denom:** `utestusd-testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6`
   - **Symbol:** TESTUSD
   - **Decimals:** 6

---

## 🏗️ Integration Status

### Smart Contracts (✅ Ready)
| Component | Status | Details |
|-----------|--------|---------|
| TESTUSD denom in contracts | ✅ Complete | Added to phoenix-escrow.ts |
| 6 decimal handling | ✅ Complete | 1 TESTUSD = 1,000,000 uTESTUSD |
| Conversion utilities | ✅ Complete | `testusdToUtestusd`, `utestusdToTestusd` |
| Fee calculation | ✅ Complete | 1.1% in uTESTUSD |
| Collateral calculation | ✅ Complete | 10% in uTESTUSD |

### Frontend (✅ Complete)
| Component | Status | Details |
|-----------|--------|---------|
| Price banner | ✅ Working | Displays prices in TESTUSD |
| Auction creation | ✅ Complete | Uses testusdToUtestusd |
| BidForm | ✅ Complete | Shows totals in TESTUSD |
| AuctionCard | ✅ Complete | Displays bids in TESTUSD |
| Admin panel | ✅ Working | Updates prices in TESTUSD |

### Backend (✅ Complete)
| Component | Status | Details |
|-----------|--------|---------|
| Price API | ✅ Working | Returns prices in TESTUSD |
| Database | ✅ Ready | PriceHistory model updated |
| Admin routes | ✅ Working | Password protected updates |

---

## 📊 Token Utilities in PhoenixPME

| Use Case | Description |
|----------|-------------|
| **Auction Currency** | All bids and payments in TESTUSD |
| **Collateral** | 10% seller and buyer collateral in TESTUSD |
| **Fees** | 1.1% protocol fee in TESTUSD → Community Reserve Fund |
| **PHNX Earning** | 1 PHNX per 1 TESTUSD in fees generated |
| **Price Display** | Metal prices shown in TESTUSD |

---

## 🔄 Conversion Utilities

```typescript
// TESTUSD has 6 decimals (1 TESTUSD = 1,000,000 uTESTUSD)
const TESTUSD_DECIMALS = 6;
const TESTUSD_FACTOR = 1_000_000;

// Convert TESTUSD to uTESTUSD for smart contracts
const toUtestusd = (testusd: string): string => {
  const parts = testusd.split('.');
  const whole = parts[0];
  const fraction = parts[1]?.padEnd(6, '0').slice(0, 6) || '000000';
  return whole + fraction;
};

// Convert uTESTUSD to TESTUSD for display
const toTestusd = (utestusd: string): string => {
  const amount = BigInt(utestusd);
  const whole = amount / 1_000_000n;
  const fraction = amount % 1_000_000n;
  
  if (fraction === 0n) return whole.toString();
  
  const fractionStr = fraction.toString().padStart(6, '0').replace(/0+$/, '');
  return `${whole}.${fractionStr}`;
};
✅ Operational Status
Feature	Status	Notes
Token Creation	✅ Complete	Transaction confirmed
Transferability	✅ Working	Can send between wallets
Wallet Visibility	✅ Working	Visible in Keplr/Leap
Smart Contract Integration	✅ Ready	7 contracts ready
Frontend Integration	✅ Complete	UI uses TESTUSD
Price Updates	✅ Working	Admin panel updates
TX Testnet	⏳ March 6	9 days remaining
🚀 Next Steps
Pre-March 6
✅ Token creation complete

✅ Smart contract integration ready

✅ Frontend UI complete

✅ Admin panel working

✅ Documentation updated

March 6 Launch
🔜 Deploy contracts to TX Testnet 6.0

🔜 Enable faucet for TESTUSD

🔜 First test auctions

🔜 Community testing begins

Post-Launch
📝 Increase TESTUSD supply as needed

📝 Integrate with multi-oracle system

📝 PHNX governance weight accumulation

📝 TRUST/DONT TRUST reputation tokens

🔗 Related Documentation
Document	Link
Architecture Overview	ARCHITECTURE-OVERVIEW.md
Tokenomics	TOKENOMICS.md
Quick Start	QUICK_START.md
Smart Contracts	phoenix-escrow.ts
📝 Changelog
2026-02-24: Updated with integration status, conversion utilities, next steps

2026-02-21: Added TX testnet context, multi-wallet support

2026-02-??: Initial token creation documentation

Last Updated: February 24, 2026
Status: ✅ OPERATIONAL - Ready for TX Testnet 🚀