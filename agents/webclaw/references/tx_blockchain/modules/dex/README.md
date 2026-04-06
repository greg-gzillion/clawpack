# TX DEX - Complete Specification

## Overview
The TX DEX allows any TX user to create orders for trading any token pair. The order book is bidirectional and permissionless, allowing for flexible and open trading.

## Order Book

### Order Attributes
Users can place orders with the following attributes:

| Attribute | Description |
|-----------|-------------|
| `order_id` | Unique order identifier |
| `base_denom` | When buying, you buy base_denom; when selling, you sell base_denom |
| `quote_denom` | When buying, you sell quote_denom; when selling, you buy quote_denom |
| `price` | Value of one unit of base_denom expressed in quote_denom |
| `quantity` | Amount of base_denom being traded |
| `side` | `sell` = sell base_denom, `buy` = buy base_denom |
| `time_in_force` | GTC, IOC, or FOK |
| `good_til` | Block height or time expiration |

## Order Types

### Time In Force

| Type | Description |
|------|-------------|
| **GTC (Good Til Canceled)** | Order remains active until fully executed or manually canceled |
| **IOC (Immediate Or Cancel)** | Executed immediately; unfilled portion canceled |
| **FOK (Fill or Kill)** | Must fill entirely immediately or canceled fully |

### Good Til Settings

| Setting | Description |
|---------|-------------|
| `good_til_block_height` | Cancel when specific block height reached |
| `good_til_block_time` | Cancel when specific timestamp reached |

## Order Placement and Matching

Once an order is placed, the DEX attempts to match it with:
- Opposite orders in the same order book (e.g., AAA/BBB)
- Orders in the corresponding inverse order book (e.g., BBB/AAA)

The system ensures execution at the best available price, depending on order type and settings.

## 2-Way Matching

TX DEX uses a **2-way matching system** that:
1. Matches orders within its own order book (same base/quote denominations)
2. Simultaneously checks the opposite order book (inverse pair)
3. Finds the best possible execution price
4. Optimizes the trading experience
┌─────────────────────────────────────────────────────────┐
│ 2-Way Matching System │
├─────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────┐ ┌─────────────────────┐ │
│ │ AAA/BBB Order Book │ │ BBB/AAA Order Book │ │
│ │ • Buy Orders │ │ • Buy Orders │ │
│ │ • Sell Orders │ │ • Sell Orders │ │
│ └──────────┬──────────┘ └──────────┬──────────┘ │
│ │ │ │
│ └──────────────────┬──────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────┐ │
│ │ Best Price Resolution │ │
│ │ Compare both order books │ │
│ │ Execute at optimal rate │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

text

## Price and Amount Limits

### Price Type
Price uses `{number}e{exponent}` format:
- **Min exponent**: -100
- **Max exponent**: 100
- **Max digits in number**: 19
- **Zero price**: Prohibited

**Examples**:
- `45000000000000` → `45e12`
- `0.000123` → `123e-6`
- `70001` → `70001`

**Limits**:
- Min value: `1e-100`
- Max value: `9999999999999999999e100`

### Normalization
Price must match regex: `^(([1-9])|([1-9]\d*[1-9]))(e-?[1-9]\d*)?$`

**Invalid Examples**:
- `10` → must be `1e1`
- `01` → must be `1`
- `1e01` → must be `1e1`
- `1e+1` → must be `1e1`

## Order Matching with Rounding Resolution

### The Rounding Problem
When matching orders from opposite order books:

| Order | Base | Quote | Side | Remaining Quantity | Price |
|-------|------|-------|------|-------------------|-------|
| 1 | AAA | BBB | sell | 500,000,000 | 0.375 |
| 2 | BBB | AAA | sell | 10,000,000 | 2.6 |

The inverse taker price of order2 (1/2.6 ≈ 0.3846) > price of order1 (0.375), so orders match. Order2 should execute at price of order1 (taker gets better price).

### Max Execution Quantity Formula

Given:
- `Qa` = quantity of token AAA to trade (integer)
- `P` = execution price (decimal)
- `P = pn / pd` where `pn` is price numerator, `pd` is price denominator
- `pn/pd` is irreducible fraction

To make `Qb' = Qa' × P` an integer:
- `Qa'` must be a multiple of `pd`

**Formula**:
max_execution_quantity = floor(remaining_quantity / price_denominator) × price_denominator
opposite_execution_quantity = floor(remaining_quantity / price_denominator) × price_numerator

text

### Example Result
With price = 0.375 = 3/8:
- `pd` = 8
- `max_execution_quantity` = floor(10,000,000 / 8) × 8 = 9,999,750
- Remainder = 250
- Opposite execution quantity = floor(10,000,000 / 8) × 3 = 3,749,906

**Implementation**: `func computeMaxExecutionQuantity` in x/dex

## Balance Locking/Freezing/Whitelisting/Clawback

When a user places an order:
1. Lock coins in assetft (similar to freezing)
2. Reserve expected receiving amount if whitelisting enabled
3. Enforce all assetft rules at placement

⚠️ **Important**: If assetft rules change after order placement, orders still execute with amounts in order book. Token admins should cancel user orders before updating rules.

## Order Reserve

- **Purpose**: Security deposit to prevent spam and malicious activities
- **Amount**: 10 CORE (default, configurable by governance)
- **Release**: Returned when order is executed or canceled

## Max Orders Limit

- **Limit**: Maximum active orders per denom
- **Default**: 100
- **Controlled by**: DEX governance

## Events

The DEX module emits events during matching:

| Event | Description |
|-------|-------------|
| `EventOrderPlaced` | Order is placed |
| `EventOrderReduced` | Order is reduced during matching |
| `EventOrderClosed` | Order is closed (matching, manual, or good_til) |
| `EventOrderCreated` | Order is saved to order book |

## Asset FT Integration

### Unified Ref Amount
- Used for price tick and precision
- Updateable by governance or token admin

### Order Cancellation
Users can cancel their orders. Token admins or governance can also cancel user orders if `dex_order_cancellation` feature is enabled.

### Block DEX
If `block_dex` feature is enabled at token issuance:
- DEX completely blocked for that denom
- Orders with that denom not accepted

### Global Freeze
If `global_freeze` is enabled for base_denom or quote_denom:
- Cannot place orders with those denoms

### Denoms to Trade With
Asset FT tokens can be restricted to trade only with specific denoms:
- Set by token admin
- Denom can only be exchanged with specified currencies/assets

## Extension Integration

The DEX integrates with asset FT extension capability, allowing extension contracts to define custom functions invoked before order execution.

### Extension Place Order Message
```rust
pub enum SudoMsg {
    ExtensionTransfer {
        recipient: String,
        sender: String,
        transfer_amount: Uint128,
        commission_amount: Uint128,
        burn_amount: Uint128,
        context: TransferContext,
    },
    ExtensionPlaceOrder {
        order: DEXOrder,
        spent: Coin,
        received: Coin,
    },
}
DEXOrder Structure
rust
#[cw_serde]
pub struct DEXOrder {
    pub creator: String,
    #[serde(rename = "type")]
    pub order_type: String,
    pub id: String,
    pub base_denom: String,
    pub quote_denom: String,
    pub price: Option<String>,
    pub quantity: Uint128,
    pub side: String,
}
Extension Workflow
Order placement attempted

Asset FT features validated first

If extension enabled, smart contract called with ExtensionPlaceOrder

Contract can implement custom validation or business logic

If no contract function implemented, order placement fails

Example Extension Implementation
rust
#[entry_point]
pub fn sudo(deps: DepsMut, env: Env, msg: SudoMsg) -> CoreumResult<ContractError> {
    match msg {
        SudoMsg::ExtensionTransfer {
            recipient,
            sender,
            transfer_amount,
            commission_amount,
            burn_amount,
            context,
        } => sudo_extension_transfer(
            deps, env, recipient, sender, 
            transfer_amount, commission_amount, 
            burn_amount, context,
        ),
        SudoMsg::ExtensionPlaceOrder {
            order,
            spent,
            received,
        } => sudo_extension_place_order(
            deps, env, order, spent, received,
        ),
    }
}
Commands
Place Limit Order
bash
txd tx dex place-order buy 1000000utestcore 50000000ubtc \
  --price=0.5 \
  --from wallet \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  -y
Place Market Order
bash
txd tx dex place-market-order buy 1000000utestcore \
  --from wallet \
  --max-slippage=0.05 \
  -y
Cancel Order
bash
txd tx dex cancel-order order-id \
  --from wallet \
  -y
Query Order Book
bash
txd query dex order-book utestcore ubtc \
  --node https://rpc.testnet-1.coreum.dev:443
Query Orders
bash
txd query dex orders-by-address wallet-address \
  --node https://rpc.testnet-1.coreum.dev:443
Query Depth
bash
txd query dex depth utestcore ubtc --depth 10 \
  --node https://rpc.testnet-1.coreum.dev:443
Proto Definitions
For detailed structure, refer to:

dex.proto

tx.proto

query.proto

events.proto

