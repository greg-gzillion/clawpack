# Fee Model Module

## Overview
The `feemodel` module calculates the minimum gas price required by the chain based on network load. It uses an Exponential Moving Average (EMA) of gas consumption to dynamically adjust fees.

## Terms
- **Long Average Block Gas**: EMA of gas consumed using `LongEmaBlockLength`
- **Short Average Block Gas**: EMA of gas consumed using `ShortEmaBlockLength`
- **MaxGasPrice**: `InitialGasPrice × MaxGasPriceMultiplier`
- **EscalationStartBlockGas**: `MaxBlockGas × EscalationStartFraction`

## Fee Model Curve
Price
↑
│
│ ┌──────────┐
│ ╱ │
│ ╱ │
│ ╱ │
│ ╱ │
│ ╱ │
│ ┌─────────╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│ ╱ ╱ │
│╱ ╱ │
└──────────────────────────────────────────────→ Gas
0 LongEMA EscalationStart MaxBlockGas

text

## Four Regions

### 1. Green Region (0 to LongEMA)
- Gas price decreases exponentially
- From `InitialGasPrice` down to `InitialGasPrice × (1 - MaxDiscount)`
- Low demand = lower prices

### 2. Red Region (LongEMA to EscalationStart)
- Gas price stays at maximum discount
- `Price = InitialGasPrice × (1 - MaxDiscount)`
- Stable pricing during normal operation

### 3. Yellow Region (EscalationStart to MaxBlockGas)
- Gas price increases rapidly (power function)
- From max discount up to `MaxGasPrice`
- Higher demand = higher prices

### 4. Blue Region (> MaxBlockGas)
- Gas price flat at `MaxGasPrice`
- Maximum price to prevent network overload

## Parameters

| Parameter | Current Value | Description |
|-----------|---------------|-------------|
| `InitialGasPrice` | 0.0625 utx | Base price when no load |
| `MaxGasPriceMultiplier` | 1000 | Multiplier for max price |
| `MaxDiscount` | 0.5 | Maximum discount (50%) |
| `EscalationStartFraction` | 0.8 | Where escalation starts (80% of MaxBlockGas) |
| `MaxBlockGas` | 50,000,000 | Maximum block gas capacity |
| `ShortEmaBlockLength` | 50 | Blocks for short EMA |
| `LongEmaBlockLength` | 1000 | Blocks for long EMA |

## Calculations

### MaxGasPrice
MaxGasPrice = InitialGasPrice × MaxGasPriceMultiplier

text

**Example**:
0.0625 × 1000 = 62.5 utx

text

### EscalationStartBlockGas
EscalationStartBlockGas = MaxBlockGas × EscalationStartFraction

text

**Example**:
50,000,000 × 0.8 = 40,000,000 gas

text

### Maximum Discount Price
MaxDiscountPrice = InitialGasPrice × (1 - MaxDiscount)

text

**Example**:
0.0625 × 0.5 = 0.03125 utx

text

## EMA Calculations

### Short EMA
NewShortEMA = ((ShortEmaBlockLength - 1) × PreviousShortEMA + CurrentBlockGas) / ShortEmaBlockLength

text

### Long EMA
NewLongEMA = ((LongEmaBlockLength - 1) × PreviousLongEMA + CurrentBlockGas) / LongEmaBlockLength

text

## State Management

The module maintains these states:
- **MinGasPrice**: Current minimum gas price
- **ShortEMAGas**: Short-term EMA of gas usage
- **LongEMAGas**: Long-term EMA of gas usage

## Fee Model Behavior Examples

### Scenario 1: Low Traffic
- ShortEMA drops near 0
- MinGasPrice returns to `InitialGasPrice` (0.0625 utx)

### Scenario 2: Normal Traffic
- ShortEMA between LongEMA and EscalationStart
- MinGasPrice at max discount (0.03125 utx)

### Scenario 3: High Traffic
- ShortEMA exceeds EscalationStart
- MinGasPrice increases rapidly up to 62.5 utx

### Scenario 4: Congestion
- ShortEMA > MaxBlockGas
- MinGasPrice = MaxGasPrice (62.5 utx)

## Keeper Methods

```go
type Keeper interface {
    // Track gas for current block
    TrackedGas(ctx sdk.Context) int64
    TrackGas(ctx sdk.Context, gas int64)
    
    // Parameter management
    SetParams(ctx sdk.Context, params types.Params)
    GetParams(ctx sdk.Context) types.Params
    
    // EMA state
    GetShortEMAGas(ctx sdk.Context) int64
    SetShortEMAGas(ctx sdk.Context, emaGas int64)
    GetLongEMAGas(ctx sdk.Context) int64
    SetLongEMAGas(ctx sdk.Context, emaGas int64)
    
    // Gas price
    GetMinGasPrice(ctx sdk.Context) sdk.DecCoin
    SetMinGasPrice(ctx sdk.Context, minGasPrice sdk.DecCoin)
}
Query Examples
Get Current Min Gas Price
bash
txd query feemodel min-gas-price \
  --node https://rpc.testnet-1.coreum.dev:443
Get Parameters
bash
txd query feemodel params \
  --node https://rpc.testnet-1.coreum.dev:443
Proto Definitions
For detailed structure, refer to:

tx.proto

query.proto

params.proto

