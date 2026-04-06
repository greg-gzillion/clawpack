# DEX Technical Specification: Price Ticks, Quantity Steps, and Precision

## Problem Statement

In our system, all balances are stored and operated as integers. This means during order matching and execution, all calculations must use integer values. This approach is not unique to our system—centralized exchanges (CEXes) and traditional finance exchanges also use integers as the underlying type for calculations to ensure precise execution and avoid rounding errors.

### The Integer Constraint Challenge

If we relied solely on integer requirements, order creation would only need to follow two simple rules:

1. `base_quantity` must be an integer
2. `quote_quantity = price × base_quantity` must also be an integer

However, this introduces a significant problem: **the granularity of price and base amount become dependent on each other**.

| base_quantity | min price | quote_quantity |
|---------------|-----------|----------------|
| 1 | 1 | 1 |
| 10 | 0.1 | 1 |
| 100 | 0.01 | 1 |
| 1,000 | 0.001 | 1 |
| 10,000 | 0.0001 | 1 |
| 100,000 | 0.00001 | 1 |
| 1,000,000 | 0.000001 | 1 |

**Key Insight**: A larger `base_quantity` allows specifying a more precise price, while a higher price enables a more precise `base_quantity`. This means price precision can increase infinitely simply by increasing `base_quantity`, leading to inconsistencies and execution issues.

### Real-World Example

Consider these two orders (assuming only integer amounts for simplicity):

- **Order 1**: Sell 1,000,000 BTC at price 90,000.111111 USDT per BTC
- **Order 2**: Buy 0.1 BTC at price 91,000 USDT per BTC

For Order 2 to be valid, the buyer must pay: `0.1 BTC × 90,000.111111 = 9,000.0111111 USDT`

Since balances are stored as integers, this fractional amount cannot be accurately represented. The mismatch between price granularity and integer representation makes it impossible to execute certain trades consistently.

## Solution: Price Tick, Quantity Step, and Quote Quantity Step

To resolve these issues, we introduce three parameters:

| Parameter | Description |
|-----------|-------------|
| `price_tick_size` | Ensures prices have a fixed minimum increment |
| `quantity_step` | Enforces minimum step size for base asset quantities |
| `quote_quantity_step` | Provides consistent step size for quote amounts (derived from the other two) |

Only two parameters are required to determine the third.

## Price Tick

A **tick** is the minimum price movement an asset price can make, either upward or downward. Tick size is set by the exchange and is primarily based on the asset's price (though also depends on asset type and market conditions).

### Unified Ref Amount

To define an asset's price on-chain, we introduce `unified_ref_amount`—the quantity of the token's subunit that corresponds to 1 USD.

**Example**: 
- BTC issued with satoshi subunit (1 BTC = 100,000,000 satoshis)
- Market price: $90,000
- `unified_ref_amount` = 0.0000111 BTC (or 1,110 satoshis)
- Since: `1 BTC / 90,000 = 0.0000111 BTC` (approximates 1 USD in satoshi terms)

### How unified_ref_amount is Defined

| Token Type | Definition Method |
|------------|-------------------|
| TX Native Assets | Set or updated by token admin |
| IBC Tokens / Admin-less | Set or updated through chain governance |
| Default | `10^6` if not explicitly set |

### Price Tick Formula

For assets AAA and BBB, price_tick for the AAA/BBB market is:
price_tick(AAA/BBB) = 10^(price_tick_exponent + ceil(log10(unified_ref_amount(BBB)/unified_ref_amount(AAA))))

text

Where:
- `price_tick_exponent` = coefficient controlling price precision (current value: -6, changeable via governance)
- `ceil(log10(...))` ensures price step size accounts for both asset magnitudes

## Quantity Step (Base Quantity Step)

`quantity_step` defines the smallest allowable step for the base asset inside a market, preventing:
- Rounding issues
- Partial order cancellations during execution
- Excessively small trade sizes

### Quantity Step Formula
quantity_step(AAA) = max(1, 10^(quantity_step_exponent + ceil(log10(unified_ref_amount(AAA)))))

text

Where:
- `quantity_step_exponent` = coefficient controlling granularity (current value: -2, changeable via governance)
- `ceil(log10(...))` ensures step size aligns with asset magnitude

### Quote Quantity Step

Derived from price_tick and quantity_step:
quote_quantity_step = price_tick × quantity_step

text

## Interactive Spreadsheet

For practical experimentation with different values: [Price Tick Calculator Spreadsheet](https://docs.google.com/spreadsheets/d/example)

## Important Notes

| Note | Description |
|------|-------------|
| **No retroactive changes** | Changes to unified_ref_amount, price_tick_exponent, or quantity_step_exponent do NOT affect existing orders |
| **Hard boundaries** | price_tick and quantity_step represent backend boundaries; applications may use less granular values for better UX |
| **Multiples handling** | quantity_step may be >1; frontends should handle this properly (e.g., kPEPE/USDT instead of PEPE/USDT where kPEPE = 1000 PEPE) |

## Market Analysis: Comparison with Other Exchanges

### Binance Market Configuration

| Market | Price Tick Size | Base Quantity Step | Quote Quantity Step |
|--------|-----------------|-------------------|---------------------|
| BTC/USDT | 0.01 | 0.00001 = 10^-5 | 10^-7 |
| ETH/USDT | 0.01 | 0.0001 = 10^-4 | 10^-6 |
| ATOM/USDT | 0.001 | 0.01 = 10^-2 | 10^-5 |
| TRX/USDT | 0.0001 | 0.1 = 10^-1 | 10^-5 |
| PEOPLE/USDT | 0.00001 | 0.1 = 10^-1 | 10^-6 |
| YFI/USDT | 1 | 0.00001 = 10^-5 | 10^-5 |
| SOL/USDT | 0.01 | 0.001 = 10^-3 | 10^-5 |
| TON/USDT | 0.001 | 0.01 = 10^-2 | 10^-5 |
| PEPE/USDT | 0.00000001 = 10^-8 | 1 | 10^-8 |

### Price vs. Base Quantity Step Correlation

| Avg Price Range | Base Quantity Step | Markets |
|-----------------|-------------------|---------|
| < $0.10 | 1 | PEPE |
| $0.10 - $1.00 | 0.1 | TRX, PEOPLE |
| $1 - $10 | 0.01 | TON |
| $10 - $100 | 0.01 | ATOM |
| $100 - $1,000 | 0.001 | SOL |
| $1,000 - $10,000 | 0.0001 | ETH |
| $10,000 - $100,000 | 0.00001 | BTC, YFI |

**Observation**: Quantity_step is inversely proportional to asset price.

### Cross-Exchange Comparison

| Exchange | Market | Price Tick Size | Base Quantity Step | Quote Quantity Step |
|----------|--------|-----------------|-------------------|---------------------|
| **Binance** | BTC/USDT | 0.01 | 10^-5 | 10^-7 |
| | ETH/USDT | 0.01 | 10^-4 | 10^-6 |
| | TON/USDT | 0.001 | 10^-2 | 10^-5 |
| | PEPE/USDT | 10^-8 | 1 | 10^-8 |
| **OKX** | BTC/USDT | 0.1 | 10^-8 | 10^-9 |
| | ETH/USDT | 0.01 | 10^-6 | 10^-8 |
| | TON/USDT | 0.001 | 10^-4 | 10^-7 |
| | PEPE/USDT | 10^-9 | 1 | 10^-9 |
| **ByBit** | BTC/USDT | 0.01 | 10^-6 | 10^-8 |
| | ETH/USDT | 0.01 | 10^-5 | 10^-7 |
| | TON/USDT | 0.001 | 10^-2 | 10^-5 |
| | PEPE/USDT | 10^-8 | 1 | 10^-8 |
| **HyperLiquid** | BTC/USDT | 0.1 | 10^-5 | 10^-6 |
| | ETH/USDT | 0.01 | 10^-4 | 10^-6 |
| | TON/USDT | 0.00001 | 10^-1 | 10^-6 |
| | kPEPE/USDT | 0.000001 | 1 | 10^-6 |

### Key Observations

| Observation | Details |
|-------------|---------|
| No universal standard | Price Tick and Base Quantity vary across exchanges |
| Base Quantity Step | Typically $0.01 to $1, except rare cases |
| Quote Quantity Step | Generally 10^-9 to 10^-6, depending on market demand |
| HyperLiquid consistency | Min Total always 10^-6, similar to our approach |

## Mathematical Derivation

### Target Ranges

Based on exchange data:

| Parameter | Target Range |
|-----------|--------------|
| Base Quantity Step | $0.01 ≤ base_quantity_step ≤ $0.10 |
| Quote Quantity Step | $10^-8 ≤ quote_quantity_step ≤ $10^-7 |

### Quantity Step Derivation

Since `unified_ref_amount` ≈ $1, we multiply by a value between 0.01 and 0.1 to achieve the target range, ensuring ticks are powers of 10.

**Formula**:
base_quantity_step(AAA) = max(1, 10^quantity_step_exponent × round_up_pow10(unified_ref_amount(AAA)))

text

With `round_up_pow10(x) = 10^ceil(log10(x))`

To achieve $0.01 to $0.10 range:
- Set `10^quantity_step_exponent = 0.01`
- Therefore `quantity_step_exponent = -2`

**Final Formula**:
quantity_step = max(1, 10^(quantity_step_exponent + ceil(log10(unified_ref_amount))))

text

### Price Tick Derivation

From `quote_quantity = base_quantity × price`, we derive:
quote_tick = base_tick × price_tick
price_tick = quote_tick / base_tick

text

Substituting definitions:
price_tick = 10^quantity_step_exponent × round_up_pow10(unified_ref_amount(BBB)) /
(10^quote_quantity_exponent × round_up_pow10(unified_ref_amount(AAA)))

text

Simplifying with `price_tick_exponent = quantity_step_exponent - quote_quantity_exponent`:

**Final Formula**:
price_tick = 10^(price_tick_exponent + ceil(log10(unified_ref_amount(BBB)/unified_ref_amount(AAA))))

text

### Example Calculations

| Base | Quote | ura_base | ura_quote | quantity_step | price_tick |
|------|-------|----------|-----------|---------------|------------|
| BTC | USDT | 0.000011 | 1.0 | 10^(-2+ceil(log10(0.000011)))=10^-6 | 10^(-6+ceil(log10(1/0.000011)))=10^-1=0.1 |
| ETH | USDT | 0.000333 | 1.0 | 10^(-2+ceil(log10(0.000333)))=10^-5 | 10^(-6+ceil(log10(1/0.000333)))=10^-2=0.01 |
| TRX | USDT | 4.5 | 1.0 | 10^(-2+ceil(log10(4.5)))=10^-1 | 10^(-6+ceil(log10(1/4.5)))=0.000001 |
| PEPE | USDT | 80000 | 1.0 | 10^(-2+ceil(log10(80000)))=10^3 | 10^-6×round_up_pow10(1.0/80000)=10^-10 |

### Non-USDT Pair Example: ETH/BTC

| Exchange | Price Tick Size | Base Quantity Step | Quote Quantity Step |
|----------|-----------------|-------------------|---------------------|
| Binance | 10^-5 | 10^-3 | 10^-8 |
| OKX | 10^-5 | 10^-6 | 10^-11 |
| ByBit | 10^-6 | 10^-5 | 10^-11 |
| **TX DEX** | **10^-7** | **10^-5** | **10^-12** |

Our proposed values align with or extend beyond ranges observed on other exchanges.

## Implementation

### Core Functions

```go
// Compute price tick for a market
func ComputePriceTick(uraBase, uraQuote sdk.Dec, priceTickExponent int64) sdk.Dec {
    ratio := uraQuote.Quo(uraBase)
    log10 := decimal.Log10(ratio)
    ceilLog10 := decimal.Ceil(log10)
    exponent := priceTickExponent + ceilLog10.Int64()
    return decimal.New(1, exponent)
}

// Compute quantity step for an asset
func ComputeQuantityStep(ura sdk.Dec, quantityStepExponent int64) sdk.Int {
    log10 := decimal.Log10(ura)
    ceilLog10 := decimal.Ceil(log10)
    exponent := quantityStepExponent + ceilLog10.Int64()
    step := decimal.New(1, exponent)
    return step.BigInt()
}
Parameters
Parameter	Current Value	Description
price_tick_exponent	-6	Controls price precision per market
quantity_step_exponent	-2	Controls base quantity granularity
Commands
bash
# Query unified ref amount for a token
txd query assetft token utoken --node <rpc>

# Update unified ref amount (admin)
txd tx assetft update-unified-ref-amount utoken 0.000011 \
  --from admin \
  --chain-id txchain-testnet-1 \
  -y

# Query DEX parameters
txd query dex params --node <rpc>

# Query market configuration
txd query dex market utoken ubtc --node <rpc>
Proto Definitions
For detailed structure, refer to:

dex.proto

params.proto

assetft.proto
