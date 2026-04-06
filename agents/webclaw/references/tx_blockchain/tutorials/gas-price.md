# Gas Price on TX Blockchain

## Overview

This document describes the rules for gas price calculation for projects using TX Blockchain. Understanding gas prices is crucial for building reliable applications.

## Fee Model

The TX Blockchain uses a dynamic fee model for minimum gas price calculation. If a transaction's gas price is lower than the current minimum gas price, the transaction will be rejected.

> ⚠️ **Important**: The minimum gas price is a dynamic value that can change after each block based on network load.

## How to Calculate Min Gas Price for Next Block

There are three methods to determine the appropriate gas price:

| Method | Accuracy | Complexity | Use Case |
|--------|----------|------------|----------|
| Recommended Gas Price Endpoint | High | Low | Production applications |
| Optimized Gas Price Calculation | Medium | Medium | Custom implementations |
| Non-optimized Initial Gas Price | Low | Very Low | Simple scripts, testing |

---

## Method 1: Use Recommended Gas Price Endpoint (Recommended)

The `RecommendedGasPrice` endpoint returns accurate gas price predictions for future blocks.

### Response Fields

| Field | Description |
|-------|-------------|
| `low` | Minimum gas price for basic transactions |
| `med` | Recommended gas price for most transactions |
| `high` | High gas price for urgent transactions |

### Usage

```bash
# Query recommended gas price
curl -s https://api.testnet.tx.dev/cosmos/tx/v1beta1/gas_prices | jq .

# Example response:
# {
#   "low": "0.0625",
#   "med": "0.0750",
#   "high": "0.1000"
# }
Implementation
Using med value:

Decent certainty that transaction will go through

Recommended for most applications

Using high value:

Almost 100% certainty

Recommended for urgent/time-sensitive transactions

Go Example
go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

type GasPrices struct {
    Low  string `json:"low"`
    Med  string `json:"med"`
    High string `json:"high"`
}

func GetRecommendedGasPrice(apiURL string) (*GasPrices, error) {
    resp, err := http.Get(apiURL + "/cosmos/tx/v1beta1/gas_prices")
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var gasPrices GasPrices
    if err := json.NewDecoder(resp.Body).Decode(&gasPrices); err != nil {
        return nil, err
    }
    
    return &gasPrices, nil
}

// Usage
func main() {
    apiURL := "https://api.testnet.tx.dev"
    gasPrices, _ := GetRecommendedGasPrice(apiURL)
    fmt.Printf("Recommended gas price: %s\n", gasPrices.Med)
}
TypeScript Example
typescript
interface GasPrices {
  low: string;
  med: string;
  high: string;
}

async function getRecommendedGasPrice(apiUrl: string): Promise<GasPrices> {
  const response = await fetch(`${apiUrl}/cosmos/tx/v1beta1/gas_prices`);
  return await response.json();
}

// Usage
const apiUrl = "https://api.testnet.tx.dev";
const gasPrices = await getRecommendedGasPrice(apiUrl);
console.log(`Recommended gas price: ${gasPrices.med}`);
Method 2: Optimized Gas Price Calculation
Use the MinGasPrice query to get the current minimum gas price, then apply a multiplier based on expected wait time.

Query Current Min Gas Price
bash
# Query current minimum gas price
txd query feemodel min-gas-price --node $TX_NODE

# Or via API
curl -s https://api.testnet.tx.dev/coreum/feemodel/v1/min_gas_price
Multiplier Table
Waiting Time	Multiplier	Description
1 second	1.1	Send immediately after query
30 seconds	1.3	Moderate delay
60 seconds	1.5	Significant delay
> 60 seconds	Initial Gas Price	Use initial gas price from params
Why Multipliers?
The minimum gas price changes over time based on network load. The chart below shows how it evolves:

text
Gas Price
    ↑
    │                    ╱
    │                  ╱
    │                ╱
    │              ╱
    │            ╱
    │          ╱
    │        ╱
    │      ╱
    │    ╱
    │  ╱
    │╱
    └──────────────────────────────────→ Time
    
    Query   1s    30s   60s
    Time
Implementation Examples
Go Implementation:

go
import (
    "fmt"
    "time"
    "github.com/cosmos/cosmos-sdk/types"
)

func CalculateGasPrice(minGasPrice sdk.DecCoin, waitTime time.Duration) sdk.DecCoin {
    multiplier := 1.1 // Default for < 1s
    
    if waitTime < 1*time.Second {
        multiplier = 1.1
    } else if waitTime < 30*time.Second {
        multiplier = 1.3
    } else if waitTime < 60*time.Second {
        multiplier = 1.5
    } else {
        // Use initial gas price from params
        return getInitialGasPrice()
    }
    
    amount := minGasPrice.Amount.Mul(sdk.NewDecWithPrec(int64(multiplier*100), 2))
    return sdk.NewDecCoin(minGasPrice.Denom, amount.TruncateInt())
}
TypeScript Implementation:

typescript
async function calculateGasPrice(
  minGasPrice: string, 
  waitTimeMs: number
): Promise<string> {
  let multiplier: number;
  
  if (waitTimeMs < 1000) {
    multiplier = 1.1;
  } else if (waitTimeMs < 30000) {
    multiplier = 1.3;
  } else if (waitTimeMs < 60000) {
    multiplier = 1.5;
  } else {
    // Get initial gas price from params
    return await getInitialGasPrice();
  }
  
  const price = parseFloat(minGasPrice) * multiplier;
  return price.toFixed(6);
}
Method 3: Use Non-optimized Initial Gas Price
The initial gas price is a parameter set in genesis that can be updated by governance.

Get Initial Gas Price
bash
# Query fee model parameters
txd query feemodel params --node $TX_NODE

# Or via API
curl -s https://api.testnet.tx.dev/coreum/feemodel/v1/params | jq .params.initial_gas_price

# Check on explorer
# https://explorer.testnet.tx.dev/params?module=feemodel
When to Use This Method
✅ Simple scripts and testing

✅ Tools that don't support additional queries

✅ Development environments

❌ Production applications (use Method 1 or 2)

⚠️ Important Caveats
Hardcoding is dangerous: If you hardcode gas price instead of querying and the value is increased by governance, transactions will start failing.

High network load: During peak times, the actual min gas price may exceed the initial gas price.

Always query when possible: Dynamic querying is always more reliable.

Best Practices
For Production Applications
typescript
async function getSafeGasPrice(): Promise<string> {
  // 1. Try recommended endpoint first
  try {
    const response = await fetch('https://api.testnet.tx.dev/cosmos/tx/v1beta1/gas_prices');
    const { high } = await response.json();
    return high;
  } catch (error) {
    // 2. Fallback to min gas price with multiplier
    try {
      const response = await fetch('https://api.testnet.tx.dev/coreum/feemodel/v1/min_gas_price');
      const { min_gas_price } = await response.json();
      const price = parseFloat(min_gas_price.amount) * 1.5;
      return price.toFixed(6);
    } catch (fallbackError) {
      // 3. Ultimate fallback to initial gas price
      return "0.0625";
    }
  }
}
Transaction Construction
bash
# Using dynamic gas price
GAS_PRICE=$(curl -s https://api.testnet.tx.dev/cosmos/tx/v1beta1/gas_prices | jq -r .med)

txd tx bank send $FROM $TO 1000000utestcore \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE \
  --gas-prices ${GAS_PRICE}utestcore \
  --gas auto --gas-adjustment 1.3 \
  -y
Gas Adjustment
Always use --gas auto --gas-adjustment 1.3 to ensure sufficient gas for execution:

bash
--gas auto --gas-adjustment 1.3
This adds a 30% buffer to the estimated gas, preventing out-of-gas errors.

Monitoring Gas Prices
Watch Gas Price Changes
bash
# Watch min gas price over time
watch -n 5 'txd query feemodel min-gas-price --node $TX_NODE'
Historical Analysis
bash
# Query gas price at specific block
BLOCK_HEIGHT=1000000
curl -s https://api.testnet.tx.dev/coreum/feemodel/v1/min_gas_price?height=$BLOCK_HEIGHT
Common Issues
Transaction Rejected Due to Low Gas Price
Error:

text
transaction gas price is less than the minimum gas price
Solutions:

Increase gas price using --gas-prices

Query current min gas price

Use recommended gas price endpoint

Gas Price Too High
Symptoms:

Paying more than necessary

Transactions still succeed but cost more

Solutions:

Use low or med values from recommended endpoint

Query current min gas price without multiplier

Monitor network load to choose optimal times

Quick Reference
Method	Command/Endpoint	When to Use
Recommended	/cosmos/tx/v1beta1/gas_prices	Production apps
Min Gas Price	/coreum/feemodel/v1/min_gas_price	Real-time needs
Initial Gas Price	/coreum/feemodel/v1/params	Fallback only
Next Steps
Transfer funds with CLI

Deploy first WASM contract

Create your first FT

Resources
Fee Model Documentation

Deterministic Gas

Network Variables

