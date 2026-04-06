# Decentralized Exchange (DEX) - Overview

## Introduction
The DEX module is a native decentralized exchange built into the TX blockchain, enabling trading of any assets on the network including:
- Native $TX token
- Fungible tokens (issued via assetft)
- Non-fungible tokens (NFTs)

## Key Features
- **Native to blockchain** - No separate smart contracts needed
- **Low fees** - Deterministic gas costs
- **Fast execution** - ~6 second block times
- **Any trading pair** - Trade any asset against any other
- **Limit orders** - Set specific price points
- **Market orders** - Execute at current market price
- **Order book** - Central limit order book (CLOB)

## Architecture
┌─────────────────────────────────────┐
│ DEX Module │
├─────────────────────────────────────┤
│ Order Book Management │
│ • Limit Orders │
│ • Market Orders │
│ • Order Matching │
├─────────────────────────────────────┤
│ Price Discovery │
│ • Last traded price │
│ • Best bid/ask │
│ • Order book depth │
├─────────────────────────────────────┤
│ Settlement │
│ • Atomic execution │
│ • Balance updates │
└─────────────────────────────────────┘

text

## Order Types

### Limit Orders
Orders placed at a specific price. Only executed when market reaches that price.

**Example**:
```bash
# Buy BTC at 50,000 TESTUSD
txd tx dex place-order buy 1000000utestcore 50000000ubtc \
  --from wallet \
  --chain-id txchain-testnet-1 \
  -y
Market Orders
Orders executed immediately at current market price.

Example:

bash
# Buy BTC at market price
txd tx dex place-market-order buy 1000000utestcore \
  --from wallet \
  --chain-id txchain-testnet-1 \
  -y
Order Lifecycle
1. Order Placement
User submits order with price and quantity

Order added to order book

Collateral locked if applicable

2. Order Matching
System matches buy/sell orders

Matches based on price-time priority

Partial fills supported

3. Execution
Atomic swap between parties

Balances updated atomically

Events emitted

4. Settlement
Funds transferred

Remaining order stays in book

Full orders removed

Order Book Structure
text
SELL ORDERS (Asks)
Price       Quantity
100.00      10.5
99.50       5.2
99.00       8.1
----------------- Spread -----------------
BUY ORDERS (Bids)
Price       Quantity
98.50       7.3
98.00       12.4
97.50       3.8
Trading Pairs
Supported Pairs
Any fungible token can trade against any other

Denom format: BASE-QUOTE (e.g., utx-utestcore)

Both base and quote must be fungible tokens

Pair Activation
Tokens must have trading enabled by admin:

dex_block feature prevents trading

dex_whitelisted_denoms restricts trading pairs

dex_unified_ref_amount sets reference amount

Fees
Trading Fees
Maker fee: Paid by order creator (optional)

Taker fee: Paid by order taker

Fee rates determined by governance

Collected in quote token

Gas Costs
Order placement: ~10,000 gas (deterministic)

Order cancellation: ~5,000 gas

Order execution: included in trade

Queries
Get Order Book
bash
txd query dex order-book BASE QUOTE \
  --node https://rpc.testnet-1.coreum.dev:443
Get User Orders
bash
txd query dex orders-by-address address \
  --node https://rpc.testnet-1.coreum.dev:443
Get Order Details
bash
txd query dex order order-id \
  --node https://rpc.testnet-1.coreum.dev:443
Get Trades
bash
txd query dex trades BASE QUOTE \
  --node https://rpc.testnet-1.coreum.dev:443
Get Depth
bash
txd query dex depth BASE QUOTE \
  --node https://rpc.testnet-1.coreum.dev:443
Proto Definitions
For detailed structure, refer to:

dex.proto

tx.proto

query.proto

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

## 📄 Module 6: DEX Prices and Limits

```bash
nano ~/dev/TXdocumentation/modules/dex/prices-limits.md
Paste this content:

markdown
# DEX Prices and Limits

## Price Discovery

### Last Traded Price (LTP)
The most recent executed trade price for a trading pair.

### Best Bid/Ask
- **Best Bid**: Highest price anyone is willing to buy at
- **Best Ask**: Lowest price anyone is willing to sell at
- Spread = Best Ask - Best Bid

### Weighted Average Price
Price based on volume-weighted average of recent trades.

### Mid Price
Mid Price = (Best Bid + Best Ask) / 2

text

## Price Limits

### Minimum Price Increment
Smallest price change allowed for orders:
- **Tier 1** (< 1.0): 0.000001
- **Tier 2** (1.0 - 100.0): 0.00001
- **Tier 3** (100.0 - 10,000): 0.0001
- **Tier 4** (> 10,000): 0.001

### Maximum Price
- Maximum order price: 1,000,000,000 (1B)
- Prevents overflow errors

## Order Quantity Limits

### Minimum Quantity
Minimum order size:
- **Small tokens**: 1 unit
- **Large denominations**: Based on decimals
- For 6 decimal tokens: 1 unit = 0.000001

### Maximum Quantity
- Maximum per order: 1,000,000,000 (1B) units
- Can be split across multiple orders

### Batch Limits
- Maximum orders per block: Unlimited
- Maximum per user: 1,000 active orders

## Price Protection

### Slippage Protection
Market orders include slippage limits:
```bash
# Buy up to 5% slippage
txd tx dex place-market-order buy 1000000utestcore \
  --max-slippage 0.05 \
  --from wallet \
  -y
Price Bands
Orders outside these ranges are rejected:

Upper band: +50% from mid price

Lower band: -50% from mid price

Configurable by governance

Anti-Spam Measures
Minimum order size: 100 ucore (or equivalent)

Order cancellation fee after 1,000 blocks

Prevents order book spam

Order Book Depth
Depth Calculation
Depth = Cumulative quantity at each price level

Liquidity Score
Measure of market depth:

text
Liquidity Score = Σ(Quantity × Price) across first 10 levels
Depth Examples
Buy Side Depth:

Price	Quantity	Cumulative
98.50	100	100
98.00	150	250
97.50	200	450
Sell Side Depth:

Price	Quantity	Cumulative
99.50	80	80
100.00	120	200
100.50	150	350
Order Matching
Price-Time Priority
Price priority: Best price matches first

Time priority: Older orders match before newer

Matching Algorithm
For market buy: Match against lowest asks

For market sell: Match against highest bids

Partial fills allowed

Remaining order stays in book

Cross Rate Calculation
When trading non-native pairs:

text
Cross Rate = Price(Asset1/Asset2) × Price(Asset2/Asset3)
Fee Calculation
Maker Fee
Paid by order creator

Typically lower than taker fee

Incentivizes liquidity provision

Taker Fee
Paid by order taker

Removed from order execution

Fee Formula
text
Fee = TradeAmount × FeeRate
FeeRate = BaseFee + (VolumeFactor × VolumeDiscount)
Example
text
Trade: 1,000 TESTUSD at 0.1% fee
Fee = 1,000 × 0.001 = 1 TESTUSD
Volume Discounts
Volume (30d)	Discount
< 10,000	0%
10,000 - 100,000	10%
100,000 - 1,000,000	20%
> 1,000,000	30%
Settlement
Atomic Execution
Orders matched and settled in same block:

Both parties' balances updated

Fees collected

Events emitted

Partial Fills
When quantity doesn't fully match:

Remaining quantity stays in order book

New order ID generated

Original order updated

Order Cancellation
Users can cancel open orders:

No fee if within 1,000 blocks

Fee applies after 1,000 blocks

Funds returned immediately

Market Making
Incentives
Maker rebates (negative fees)

Volume-based rewards

Liquidity mining programs

Requirements
Minimum order size: 1,000 units

Maximum spread: 2%

Order duration: At least 1 hour

Monitoring
Price deviation from market

Order book depth

Spread width

Queries
Get Depth
bash
txd query dex depth BASE QUOTE --depth 10 \
  --node https://rpc.testnet-1.coreum.dev:443
Get Trades
bash
txd query dex trades BASE QUOTE --limit 100 \
  --node https://rpc.testnet-1.coreum.dev:443
Get Order Book
bash
txd query dex order-book BASE QUOTE \
  --node https://rpc.testnet-1.coreum.dev:443
Get Price
bash
txd query dex price BASE QUOTE \
  --node https://rpc.testnet-1.coreum.dev:443
Proto Definitions
For detailed structure, refer to the proto definitions in the tx codebase.

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

## 📄 Module 7: Governance

```bash
nano ~/dev/TXdocumentation/modules/governance/README.md
Paste this content:

markdown
# Governance Module

## Overview
TX Blockchain uses on-chain governance for protocol changes, parameter updates, and community decisions. Any token holder can participate by staking $TX.

## Proposal Types

### 1. Text Proposal
Simple text-based proposals for signaling or community discussion.

### 2. Parameter Change Proposal
Update module parameters without code changes.

### 3. Software Upgrade Proposal
Schedule network upgrades and hard forks.

### 4. Community Pool Spend Proposal
Spend from community pool for projects or grants.

### 5. Cancel Software Upgrade
Cancel a scheduled upgrade.

### 6. DEX Parameter Change
Specific parameters for DEX module.

### 7. Fee Model Parameter Change
Update fee model parameters.

## Proposal Lifecycle
┌──────────────┐
│ Submit │ → Any account can submit
├──────────────┤
│ Deposit │ → 14 days to reach min deposit
├──────────────┤
│ Voting │ → 14 days for validator voting
├──────────────┤
│ Tally │ → Count votes, calculate result
├──────────────┤
│ Execute │ → If passed, changes applied
└──────────────┘

text

## Deposit Period
- **Duration**: 14 days (configurable)
- **Minimum deposit**: 100,000 utx (configurable)
- **Anyone can deposit**: To help proposals reach threshold
- **Refund**: Deposits returned if proposal passes
- **Burn**: Deposits burned if proposal fails

## Voting Period
- **Duration**: 14 days (configurable)
- **Voting power**: Based on staked tokens
- **Delegation**: Delegators can vote or delegate
- **Weighted votes**: Supported via MsgVoteWeighted

## Vote Options

| Option | Value | Description |
|--------|-------|-------------|
| Yes | 1 | Approve proposal |
| No | 2 | Reject proposal |
| Abstain | 3 | Abstain from voting |
| NoWithVeto | 4 | Veto with additional penalty |

## Voting Power Calculation
Voting Power = Staked Tokens × Delegator Weight

text

## Tally Requirements

### Quorum
- Minimum participation: **33.4%** of total voting power
- If quorum not met: Proposal fails

### Threshold
- **Yes** votes > 50% of non-abstain votes
- **NoWithVeto** votes < 33.4% of non-abstain votes
- Abstain votes do not count

### Example
Total Voting Power: 1,000,000
Turnout: 400,000 (40%)

Yes: 250,000 (62.5%)

No: 100,000 (25%)

Veto: 50,000 (12.5%)

Abstain: 0

Result: PASS (Yes > 50%, Veto < 33.4%)

text

## Submitting Proposals

### Text Proposal
```bash
txd tx gov submit-proposal text \
  --title "Community Fund Distribution" \
  --description "Proposal to allocate 100,000 UTX to community projects" \
  --deposit 100000utx \
  --from wallet \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:443 \
  -y
Parameter Change
bash
txd tx gov submit-proposal param-change \
  --title "Update MinDistributionGap" \
  --description "Increase minimum distribution gap to 1 hour" \
  --deposit 100000utx \
  --param "pse:MinDistributionGapSeconds=3600" \
  --from wallet \
  -y
Software Upgrade
bash
txd tx gov submit-proposal software-upgrade v1.0.0 \
  --title "Upgrade to v1.0.0" \
  --description "Mainnet upgrade" \
  --deposit 100000utx \
  --upgrade-height 1000000 \
  --from wallet \
  -y
Voting
Vote on Proposal
bash
txd tx gov vote PROPOSAL_ID yes \
  --from wallet \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:443 \
  -y
Weighted Vote
bash
txd tx gov vote PROPOSAL_ID \
  --options "0.8yes,0.2no" \
  --from wallet \
  -y
Queries
List Proposals
bash
txd query gov proposals \
  --node https://rpc.testnet-1.coreum.dev:443
Get Proposal
bash
txd query gov proposal PROPOSAL_ID \
  --node https://rpc.testnet-1.coreum.dev:443
Get Votes
bash
txd query gov votes PROPOSAL_ID \
  --node https://rpc.testnet-1.coreum.dev:443
Get Tally
bash
txd query gov tally PROPOSAL_ID \
  --node https://rpc.testnet-1.coreum.dev:443
Get Parameters
bash
txd query gov params \
  --node https://rpc.testnet-1.coreum.dev:443
Get Deposit
bash
txd query gov deposits PROPOSAL_ID \
  --node https://rpc.testnet-1.coreum.dev:443
Parameters
Parameter	Current	Description
min_deposit	100,000 utx	Minimum deposit
max_deposit_period	14 days	Deposit period duration
voting_period	14 days	Voting period duration
quorum	0.334	Minimum participation (33.4%)
threshold	0.5	Yes vote threshold (50%)
veto_threshold	0.334	Veto threshold (33.4%)
Community Reserve Fund
Source
1.1% fee from all PhoenixPME trades

Community-controlled treasury

Management
Controlled by future DAO

No individual can withdraw

Founder has 10% permanent voting weight

Address
Testnet: testcore1m5adn3k68tk4zqmujpnstmp9r933jafzu44tnv

Mainnet: To be announced

PHNX Governance Token
Overview
Non-transferable - Cannot be traded

Soulbound - Bound to user

Earned: 1 PHNX per 1 TESTUSD in fees generated

Voting Weight
1 PHNX = 1 vote in DAO

Weighted by lifetime fee contribution

No expiration

Distribution
Minted automatically when fees generated

Stored as soulbound NFT

Tracked by contract

Proto Definitions
For detailed structure, refer to:

gov.proto

tx.proto

query.proto

