# Tokenomics: PHNX, TRUST & DONT TRUST

**Status:** Final Design - Ready for Implementation  
**Last Updated:** February 24, 2026  
**Related Docs:** [DAO_OPERATIONS.md](DAO_OPERATIONS.md), [GOVERNANCE.md](../GOVERNANCE.md)

---

## 🪙 The Three Tokens of PhoenixPME

| Token | Purpose | Transferable | Cash Value |
|-------|---------|--------------|------------|
| **PHNX** | Governance weight | ❌ NO | $0 |
| **TRUST** | Positive reputation | ❌ NO | $0 |
| **DONT TRUST** | Negative reputation | ❌ NO | $0 |

**Core Principle:** These are NOT securities, NOT investments, and NOT transferable. They are simply **records of participation, reputation, and governance weight.**

---

## PHNX – Governance Weight

### What It Is
Non-transferable voting weight in the Community Reserve Fund. 1 PHNX = 1 vote.

### How You Earn It
- **1 PHNX** per **1 TESTUSD** in fees you generate through trading
- Fees paid → PHNX voting weight accrued
- No上限 (uncapped)

### Why You Can't Sell It
Governance shouldn't be for sale. Your voice should be earned through participation, not purchased with capital.

### Distribution Model (Implemented)

| Allocation | Purpose | Vesting |
|------------|---------|---------|
| **90%** | Community (earned through trading) | Instant |
| **10%** | Founder (@greg-gzillion) | Permanent, non-transferable |

### What It Gives You
- Vote on Community Reserve Fund usage
- Propose and decide on grants, audits, marketing
- Shape the future of the protocol

### Legal Status
✅ NOT a security (Howey test passed):
- No investment of money (earned, not bought)
- No expectation of profits (no cash value)
- No transferability (can't sell)

---

## TRUST – Positive Reputation

### What It Is
Non-transferable reputation tokens minted for every successful transaction.

### How You Get It
- **1 TRUST** minted to your wallet for **each successful trade**
- Both buyer and seller receive TRUST upon completion

### Why You Can't Sell It
Reputation isn't merchandise. You can't buy a good name—you have to earn it.

### What It Signals
- "This person delivers. They've completed X successful trades."
- Visible to all users
- Permanent on-chain record

### KYC Binding
- Tethered to verified identity via TX blockchain's KYC/AML infrastructure
- One person, one reputation—no sock puppets
- Can't create new wallets to escape history

---

## DONT TRUST – Negative Reputation

### What It Is
Non-transferable reputation tokens minted for every failed transaction.

### How You Get It
- **1 DONT TRUST** minted for each failed obligation:
  - Seller fails to ship
  - Buyer fails to pay
  - Dispute resolved against you
  - Scam attempt detected

### Why You Can't Sell It
You wouldn't want to buy it. And neither would anyone else.

### What It Signals
- "Warning: This person has failed to complete X trades."
- Permanent warning to future traders
- Can't be erased

### Amendment (Rare)
Amendable only under extenuating circumstances through DAO vote (requires 2/3 majority).

---

## Net Reputation Score

Every wallet displays:
Wallet: testcore1...xyz
────────────────
TRUST: 47 ✅
DONT TRUST: 2 ❌
────────────────
NET TRUST: 45 ⭐
────────────────
Trades: 49
Member since: Feb 2026
PHNX voting power: 4.7%


This is **public, permanent, and earned.**

---

## Why Regulators Can't Touch This

| Argument | Reality |
|----------|---------|
| "PHNX is a security!" | It has no cash value and can't be sold. It's a voting ledger. |
| "TRUST is a security!" | It's feedback. You want to regulate feedback? |
| "DONT TRUST is a security!" | It's a warning. You want to regulate warnings? |
| "People could profit!" | How? You can't sell them. You can't transfer them. |
| "It's an investment!" | You can't invest in something you can't buy. |

### Howey Test Analysis

| Element | PHNX | TRUST | DONT TRUST |
|---------|------|-------|------------|
| Investment of money? | ❌ No - earned | ❌ No - earned | ❌ No - earned |
| Common enterprise? | ✅ Platform exists | ✅ Platform exists | ✅ Platform exists |
| Expectation of profits? | ❌ NO - no cash value | ❌ NO - no cash value | ❌ NO - no cash value |
| From efforts of others? | ❌ NO - you earn it | ❌ NO - you earn it | ❌ NO - you earn it |

**Verdict:** NOT SECURITIES

---

## Comparison to Earlier Drafts

| Aspect | Feb 14 Draft | Feb 24 Implementation |
|--------|--------------|----------------------|
| **Token Sale** | Planned (none) | ✅ NO SALE |
| **Transferability** | Discussed | ✅ NON-TRANSFERABLE |
| **Founder Allocation** | 10% (vested) | ✅ 10% voting weight |
| **Community** | 50%+ | ✅ 90% earned |
| **Treasury** | 30% DAO | ✅ CRF accumulates fees |
| **Reputation** | Not mentioned | ✅ TRUST/DONT TRUST |
| **KYC Binding** | Not mentioned | ✅ TX blockchain KYC |

---

## Community Reserve Fund (CRF)

- **Source:** 1.1% of all successful trades
- **Control:** PHNX voting weight holders (future DAO)
- **Withdrawal:** ❌ **NO ONE** can withdraw (not even founder)
- **Usage (to be voted):**
  - Development grants
  - Security audits
  - Bug bounties
  - Marketing
  - Community initiatives

---

## How to Earn PHNX

| Activity | PHNX Earned |
|----------|-------------|
| Generate 1 TESTUSD in fees | 1 PHNX |
| Successful trade (as buyer) | 0.9 PHNX |
| Successful trade (as seller) | 0.4 PHNX (proposed) |
| Developer contribution | Via DAO grant |

*Note: Seller PHNX allocation is under discussion to incentivize listings.*

---

## Implementation Status

| Feature | Status | Target |
|---------|--------|--------|
| PHNX in smart contracts | 📝 Planned | Q2 2026 |
| TRUST minting | 📝 Planned | Q2 2026 |
| DONT TRUST minting | 📝 Planned | Q2 2026 |
| KYC binding | 🔜 TX feature | Post-launch |
| DAO voting | 📝 Planned | Q3 2026 |

---

## 🔗 Related Documents

| Document | Link |
|----------|------|
| DAO Operations | [DAO_OPERATIONS.md](DAO_OPERATIONS.md) |
| Governance | [GOVERNANCE.md](../GOVERNANCE.md) |
| Vision | [VISION.md](../../VISION.md) |
| Legal | [/docs/legal/](../legal/) |

---

## 📝 Changelog

- **2026-02-24:** Complete rewrite with PHNX/TRUST/DONT TRUST design
- **2026-02-14:** Initial conceptual draft (older)

---

*Last Updated: February 24, 2026*
*Status: Final Design - Ready for Implementation* 🚀