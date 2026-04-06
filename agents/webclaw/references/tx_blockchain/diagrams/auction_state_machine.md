# PhoenixPME Auction Escrow: State Machine Specification

**Document Status:** Living Document  
**Last Updated:** February 24, 2026  
**Owner:** Greg (@greg-gzillion)  
**Review Cycle:** Monthly  
**Current Phase:** Ready for TX Testnet 6.0 Launch (March 6, 2026)

## 1. Overview
The PhoenixPME Auction Escrow is a state machine that manages the lifecycle of a peer-to-peer physical precious metals trade. Its primary purpose is to **custody funds securely** and **enforce rules transparently** until both parties fulfill their obligations. Security is initiated by a seller bond (10% collateral) and matched by a buyer bond (10% collateral).

**Current Status:**
- ✅ Smart contract implemented (CosmWasm, Rust)
- ✅ 7 contracts with 16 tests passing
- ✅ 193KB optimized WASM
- ✅ Dual collateral (10% both parties)
- ✅ 1.1% fee to Community Reserve Fund
- ⏳ Testnet deployment: March 6, 2026
- ⏳ Multi-oracle delivery system: Post-launch

## 2. Definitions
- **Seller Bond (10% Collateral)**: Funds locked by the seller to guarantee performance (shipment of described item). Forfeited in whole or part for bad faith actions. Based on **reserve price**.
- **Buyer Bond (10% Collateral)**: Funds locked by the winning bidder to guarantee payment and good faith. Forfeited if buyer fails to complete payment.
- **Reserve Price**: The minimum sale price set by the seller. The auction only succeeds if a bid meets or exceeds this amount.
- **Winning Bid**: The highest valid bid at the close of the auction.
- **TESTUSD**: The protocol's test token (6 decimals, Coreum testnet)
- **Community Reserve Fund**: Accumulates 1.1% of all successful trades

## 3. Core States & Transitions (Implemented)

### State: `AWAITING_SELLER_BOND`
**Purpose:** The initial state. Ensures the seller has "skin in the game" before the auction is publicly listed, thwarting fake or non-committal listings.

**Parameters & Storage (Implemented):**
- `seller_bond_amount`: Calculated as 10% of `reserve_price` (in uTESTUSD)
- `seller_bond_deadline`: 24-hour timer (configurable)

**Valid Triggers & Next States:**
1.  `SELLER_DEPOSITS_BOND` → `LISTING_ACTIVE`
    - ✅ Implemented: Seller locks 10% collateral
    - Auction listing becomes visible to buyers
2.  `SELLER_CANCELS` → `CANCELLED`
    - ✅ Implemented: Seller can cancel before bond deadline
    - No penalty, as no bond was locked
3.  `BOND_DEADLINE_EXPIRED` → `CANCELLED`
    - ✅ Implemented: 24-hour deadline passes without deposit
    - Listing automatically invalidated

**On-Chain Logic (Implemented):**
- Contract verifies deposited asset (TESTUSD) matches `seller_bond_amount`
- Bonded funds held in escrow until auction concludes in `COMPLETE`, `CANCELLED`, or `DISPUTE_RESOLVED`

---

### State: `LISTING_ACTIVE`
**Purpose:** The auction is live and visible. Buyers can place bids or trigger a "Buy It Now" if the seller has set that option.

**Parameters & Storage (Implemented):**
- `reserve_price`: Minimum price to win (in uTESTUSD)
- `buy_it_now_price`: Optional instant-win price
- `auction_end_time`: Timestamp when bidding closes
- `current_highest_bid` & `current_winning_bidder`: Tracks leading bid

**Valid Triggers & Next States:**
1.  `BUYER_TRIGGERS_BUY_IT_NOW` → `AWAITING_PAYMENT`
    - ✅ Implemented: Buy It Now available if price set
    - Buyer must lock full payment + 10% buyer collateral
2.  `BUYER_PLACES_BID` → (Remains in `LISTING_ACTIVE`)
    - ✅ Implemented: Bid must exceed current highest bid
    - Previous bidder refunded, new bid + 10% collateral locked
3.  `AUCTION_TIMER_EXPIRES` → `BIDDING_CLOSED`
    - ✅ Implemented: Timer expires, bidding closes
    - If highest bid >= reserve, proceeds to settlement
4.  `SELLER_CANCELS` → `CANCELLED`
    - ✅ Implemented: Allowed only if no bids placed
    - Seller's bond returned

**On-Chain Logic (Implemented):**
- Manages locking/refunding of bid amounts with each new higher bid
- Bid amount includes 10% buyer collateral automatically
- TESTUSD amounts handled with 6 decimal precision

---

### State: `BIDDING_CLOSED`
**Purpose:** The bidding period is over. The contract determines the outcome.

**Parameters & Storage (Implemented):**
- `current_highest_bid`: Winning bid amount (in uTESTUSD)
- `current_winning_bidder`: Address of winner
- `reserve_price`: For final validation

**Valid Triggers & Next States:**
1.  `RESERVE_MET` → `AWAITING_WINNER_PAYMENT`
    - ✅ Implemented: `current_highest_bid` >= `reserve_price`
    - Winner bound to lock payment, all other bids refunded
2.  `RESERVE_NOT_MET` → `CANCELLED_NO_WINNER`
    - ✅ Implemented: `current_highest_bid` < `reserve_price`
    - Seller's bond returned, all bids refunded

**On-Chain Logic (Implemented):**
- Validation and routing state
- Bulk refund operations for losing bidders

---

### State: `AWAITING_WINNER_PAYMENT`
**Purpose:** The winning bidder must lock the full payment amount (in TESTUSD) with the escrow contract.

**Parameters & Storage (Implemented):**
- `payment_amount`: Equal to `current_highest_bid` (in uTESTUSD)
- `payment_deadline`: 48-hour timer for winner to act
- `buyer_collateral`: 10% of bid amount (already locked)

**Mechanics (Implemented):**
1.  Winner's 10% buyer collateral already locked during bidding
2.  Winner must send remaining 90% (payment_amount - collateral)
3.  Contract automatically tracks total required

**Valid Triggers & Next States:**
1.  `WINNER_LOCKS_FULL_PAYMENT` → `AWAITING_SHIPMENT`
    - ✅ Implemented: Contract verifies total funds = `payment_amount + buyer_collateral`
    - Seller notified to proceed with shipment
2.  `PAYMENT_DEADLINE_EXPIRED` → `CANCELLED_WINNER_DEFAULT`
    - ✅ Implemented: 48-hour deadline passes
    - Seller's bond returned, buyer forfeits 10% collateral to seller

**Note:** Cross-chain flow (XRPL) is planned for Phase 2. MVP uses TESTUSD on Coreum testnet.

---

### State: `AWAITING_SHIPMENT` (🔄 Planned for Post-Launch)
**Purpose:** The buyer's payment is locked. The seller must now ship the physical item.

**Parameters & Storage (Planned):**
- `shipment_deadline`: 5 business days
- `allowed_carrier`: Initially USPS only
- `allowed_destination_region`: US-Lower48

**Valid Triggers & Next States (Planned):**
1.  `SELLER_SUBMITS_SHIPMENT_PROOF` → `IN_TRANSIT`
    - Shipping oracle validates USPS tracking
2.  `SHIPMENT_DEADLINE_EXPIRED` → `DISPUTE_SELLER_DEFAULT`
    - Buyer refunded, seller's bond forfeited to buyer

**Current Status:** Design phase. MVP will use manual verification (admin) until multi-oracle system is implemented.

---

### State: `IN_TRANSIT` (🔄 Planned for Post-Launch)
**Purpose:** The item is en route. Waiting for delivery confirmation.

**Parameters & Storage (Planned):**
- `tracking_number`: Verified USPS tracking ID
- `delivery_confirmation_deadline`: Estimated delivery + 7 days
- `last_verified_scan`: Updated by shipping oracle

**Valid Triggers & Next States (Planned):**
1.  `CARRIER_CONFIRMS_DELIVERY` → `AWAITING_BUYER_CONFIRMATION`
    - Oracle reports "Delivered" from USPS
2.  `DELIVERY_TIMEOUT_EXPIRED` → `DISPUTE_IN_TRANSIT`
    - Lost/stalled package, dispute raised

**Current Status:** Design phase.

---

### State: `AWAITING_BUYER_CONFIRMATION` (🔄 Planned for Post-Launch)
**Purpose:** The item is marked as delivered. Buyer has 72 hours to inspect and confirm or raise a dispute.

**Parameters & Storage (Planned):**
- `delivery_timestamp`: When oracle reported "Delivered"
- `buyer_challenge_deadline`: 72 hours after delivery
- `seller_payout_address`: Where funds will be sent

**Valid Triggers & Next States (Planned):**
1.  `BUYER_CONFIRMS_SATISFACTION` → `COMPLETE`
    - Funds released to seller, seller's bond returned
2.  `BUYER_RAISES_DISCREPANCY` → `DISPUTE_MATERIAL_DISCREPANCY`
    - Buyer submits evidence + dispute fee
3.  `BUYER_CHALLENGE_DEADLINE_EXPIRES` → `COMPLETE`
    - Silent acceptance, funds released to seller

**Current Status:** Design phase.

---

### State: `COMPLETE`
**Purpose:** The auction has concluded successfully. All obligations are met.

**On-Chain Logic (Implemented):**
- ✅ Seller receives full payment
- ✅ Seller's bond (10%) returned
- ✅ Buyer's bond (10%) returned
- ✅ 1.1% fee transferred to Community Reserve Fund
- ✅ Auction archived
- 📝 TRUST tokens minted (planned for Phase 2)

**Valid Triggers & Next States:**
- Terminal state

---

## 4. System Dependencies & Oracles (Planned)

| Dependency | Status | Target |
|------------|--------|--------|
| Shipping Oracle (USPS) | 📝 Design | Q3 2026 |
| Multi-Oracle Consensus | 📝 Design | Q3 2026 |
| Dispute Resolution Module | 📝 Design | Q3 2026 |
| Cross-Chain Bridge (XRPL) | 📝 Research | Q4 2026 |

**Current MVP Approach:**
- Manual verification via admin panel
- Price updates via admin scripts
- Disputes handled manually (admin)

---

## 5. Version 1.0 Scope (Current)

### ✅ Implemented (Pre-Launch)
- Dual collateral (10% both parties)
- 1.1% fee to Community Reserve Fund
- TESTUSD token integration
- Auction creation and bidding flow
- BidForm with collateral calculation
- Admin panel for manual price updates

### ⏳ Launch Day (March 6, 2026)
- Contract deployment to TX Testnet 6.0
- First test auctions
- End-to-end testing

### 📝 Post-Launch (Q2-Q3 2026)
- Shipping oracle integration
- Multi-oracle consensus
- Dispute resolution system
- TRUST/DONT TRUST reputation tokens
- PHNX governance weight

---

## 6. State Machine Diagram (Implemented)
            ┌─────────────────┐
            │AWAITING_SELLER_ │
            │     BOND        │
            └────────┬────────┘
                     │ SELLER_DEPOSITS_BOND
                     ▼
            ┌─────────────────┐
            │  LISTING_ACTIVE │
            └────────┬────────┘
                     │ AUCTION_TIMER_EXPIRES
                     ▼
            ┌─────────────────┐
            │ BIDDING_CLOSED  │
            └────────┬────────┘
      ┌──────────────┼──────────────┐
 RESERVE_MET    RESERVE_NOT_MET    │
      ▼              ▼              │
┌─────────────────┐┌─────────────────┐ │
│AWAITING_WINNER_ ││ CANCELLED_NO_ │ │
│ PAYMENT ││ WINNER │ │
└────────┬────────┘└─────────────────┘ │
│ WINNER_LOCKS_PAYMENT │
▼ │
┌─────────────────┐ │
│ AWAITING_SHIPMENT│(Planned) │
└────────┬────────┘ │
│ (Oracle) │
▼ │
┌─────────────────┐ │
│ COMPLETE │◀─────────────────────┘
└─────────────────┘

## 7. Current Implementation Details

### Smart Contract
- **Language:** Rust (CosmWasm)
- **Size:** 193KB optimized WASM
- **Tests:** 16 integration tests passing
- **Contracts:** 7 total

### Key Features Implemented
- ✅ Dual collateral calculation
- ✅ Bid placement with automatic collateral
- ✅ Fee calculation (1.1%)
- ✅ TESTUSD handling (6 decimals)
- ✅ Auction state management
- ✅ Escrow logic

### Frontend Integration
- ✅ PhoenixEscrowClient for contract interaction
- ✅ TESTUSD conversion utilities
- ✅ BidForm with collateral display
- ✅ Auction creation with price validation

---

## 8. Known Gaps & Next Steps

| Gap | Mitigation | Target |
|-----|------------|--------|
| Shipping verification | Manual admin (MVP) | March 6 |
| Dispute resolution | Manual admin (MVP) | March 6 |
| Multi-oracle system | Design phase | Q3 2026 |
| Cross-chain payments | Research phase | Q4 2026 |
| TRUST/DONT TRUST tokens | Planned | Q2 2026 |

---

## 9. Related Documentation

- [ARCHITECTURE-OVERVIEW.md](./architecture/ARCHITECTURE-OVERVIEW.md)
- [SECURITY_PATTERNS.md](./architecture/SECURITY_PATTERNS.md)
- [ORACLE_DESIGN.md](./architecture/ORACLE_DESIGN.md)
- [CURRENT-FOCUS.md](./CURRENT-FOCUS.md)
- [ROADMAP.md](./ROADMAP.md)

---

*Document Version: 2.0 | Last Updated: February 24, 2026*
*Next Milestone: TX Testnet 6.0 Launch - March 6, 2026* 🚀