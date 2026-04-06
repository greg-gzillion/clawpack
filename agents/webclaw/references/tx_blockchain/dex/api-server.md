k# CoreDEX API Server

The API server provides a **RESTful API** for the CoreDEX. Its goal is to flatten the learning curve for the TX DEX (and Cosmos SDK), providing a simple, easy-to-use API for developers to build trading interfaces.

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Reduce blockchain knowledge** | Frontend developers don't need to understand Cosmos SDK internals |
| **Remove denomination math** | Human-readable values (0.25 instead of 25000 base units) |
| **Reduce frontend business rules** | Server validates all order rules, frontend focuses on UX/UI |
| **Abstract communication** | Single JavaScript package handles all backend communication |

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ CoreDEX API Server Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Client │────▶│ REST API │────▶│ Store │ │
│ │ (Browser) │◀────│ (:8080) │◀────│ (gRPC) │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │ │ │
│ │ WebSocket │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Real-time │ │ Data │ │ Data │ │
│ │ Updates │ │ Aggregator │────▶│ Store │ │
│ │ (/ws) │ │ (Scanner) │ │ (MySQL) │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Prerequisites

| Requirement | Description |
|-------------|-------------|
| **Store** | Must be running (gRPC server on port 50051) |
| **Data Aggregator** | Must be running to populate store with blockchain data |
| **Network Access** | Access to TX blockchain RPC/gRPC endpoints |

## Complete API Reference

### 1. GET /api/ohlc - OHLC Candlestick Data

Returns Open/High/Low/Close candlestick data for technical analysis.

#### Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `symbol` | ✅ Yes | Trading pair symbol (URL-safe encoded) | `dextestdenom9-..._dextestdenom1-...` |
| `period` | ✅ Yes | Timeframe: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `3h`, `6h`, `12h`, `1d`, `3d`, `1w` | `1h` |
| `from` | ✅ Yes | Start timestamp (Unix seconds) | `1611007200` |
| `to` | ✅ Yes | End timestamp (Unix seconds) | `1611070980` |

**Limitation:** Maximum 2000 points per request

| Period | Max Time Range |
|--------|----------------|
| 1m | ~1.3 days |
| 1h | ~83.3 days |
| 1d | ~5.5 years |

#### Response Format

```json
[
  [
    1611069600,              // timestamp (Unix seconds)
    "5.54016620498615",      // open price
    "5.54016620498615",      // high price
    "5.54016620498615",      // low price
    "5.54016620498615",      // close price
    "1.9855"                 // volume
  ],
  [
    1611069660,
    "5.54016620498615",
    "5.54016620498615",
    "5.54016620498615",
    "5.54016620498615",
    "0"
  ]
]
Example Request
bash
curl "https://coredex.test.tx.org/api/ohlc?\
symbol=dextestdenom9-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs_\
dextestdenom1-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs&\
period=1m&from=1611007200&to=1611070980" \
  --header "Network: devnet"
2. GET /api/trades - Trade History
Returns historical trade data with filtering options.

Parameters
Parameter	Required	Description	Example
symbol	✅ Yes	Trading pair symbol (URL-safe encoded)	denom1_denom2
from	❌ No	Start timestamp (default: last 50 trades)	1611007200
to	❌ No	End timestamp	1611070980
account	❌ No	Filter by account address	devcore1...
side	❌ No	1 = Buy, 2 = Sell	1
Response Format
json
{
  "Trades": [
    {
      "Account": "devcore1fpdgztw4aepgy8vezs9hx27yqua4fpewygdspc",
      "OrderID": "8b341e25-482e-487f-b9e2-9467d98c16ac",
      "Sequence": 27388,
      "Amount": {
        "Value": 2080,
        "Exp": -6
      },
      "Price": 35.015385,
      "Denom1": {
        "Currency": "dextestdenom8",
        "Issuer": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
        "Precision": 6,
        "Denom": "dextestdenom8-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
      },
      "Denom2": {
        "Currency": "dextestdenom3",
        "Issuer": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
        "Precision": 6,
        "Denom": "dextestdenom3-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
      },
      "Side": 1,
      "BlockTime": {
        "seconds": 1736358800,
        "nanos": 634506142
      },
      "TXID": "29E2362BE19BE53B5A38CFAAB4B777484F5956972C656A4378D7620A6E8F4A36",
      "BlockHeight": 6714462,
      "HumanReadablePrice": "35.015385",
      "SymbolAmount": "0.002080",
      "Status": 3
    }
  ]
}
Important Note
When retrieving exchange history, only retrieve one side of trades. Retrieving both sides returns duplicates (party and counterparty), which confuses end users.

Example Request
bash
curl -H "Network: devnet" \
  -X "GET" "https://coredex.test.tx.org/api/trades?\
symbol=dextestdenom9-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs_\
dextestdenom1-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs&\
from=1611007200&to=1611070980"
3. GET /api/tickers - Latest Prices
Returns the latest price for one or more trading pairs.

Parameters
Parameter	Required	Description
symbols	✅ Yes	Base64-encoded JSON array of symbols (max 20)
Warning: Symbol strings are very long. Limit queries to 5-10 symbols to avoid URL overflow.

Encoding Example
bash
# Original symbols array
echo '["USD-..._BTC-...", "XRPL/USD..."]' | base64

# Result
WyJVU0QrckQ5VzdVTHZlYXZ6OHFCR00xUjVqTWdLMlFLc0VEUFFWaS9YUlAiLCAiWFJQL1VTRCtyRDlXN1VMdmVhdno4cUJHTTFSNWpNZ0syUUtzRURQUVZpIl0=
Response Format
json
{
  "Tickers": {
    "dextestdenom9-..._dextestdenom1-...": {
      "OpenTime": 1723084712,
      "CloseTime": 1723171112,
      "OpenPrice": 0.17726004,
      "HighPrice": 3135.5825912454534,
      "LowPrice": 0.1730303609235772,
      "LastPrice": 0.1783099502981715,
      "FirstPrice": 0.1730303609235772,
      "Volume": 170639.98819271981,
      "InvertedVolume": 30319.373563999994
    }
  },
  "USDTickers": {
    "dextestdenom9-..._dextestdenom1-...": {
      "OpenTime": 1723084712,
      "CloseTime": 1723171112,
      "OpenPrice": 1.24082028,
      "HighPrice": 21949.078138718174,
      "LowPrice": 1.2112125264650404,
      "LastPrice": 1.2481696520872005,
      "FirstPrice": 1.2112125264650404,
      "Volume": 24377.141170388546,
      "InvertedVolume": 212235.61494799994
    }
  }
}
Example Request
bash
curl -H "Network: devnet" \
  -X "GET" "https://coredex.test.tx.org/api/tickers?symbols=WyJVU0QrckQ5VzdVTHZlYXZ6OHFCR00xUjVqTWdLMlFLc0VEUFFWaS9YUlAiLCAiWFJQL1VTRCtyRDlXN1VMdmVhdno4cUJHTTFSNWpNZ0syUUtzRURQUVZpIl0="
4. GET /api/currencies - Available Currencies
Returns all available currencies/tokens on the DEX.

Response Format
json
{
  "Currencies": [
    {
      "Denom": {
        "Currency": "ATOM",
        "Issuer": "cosmoshub-4",
        "Precision": 6,
        "IsIBC": false,
        "Denom": "uatom",
        "Name": "Cosmos",
        "Description": "Cosmos Hub native token",
        "Icon": "https://cosmos.network/logo.png"
      },
      "SendCommission": {
        "Value": 1,
        "Exp": -2
      },
      "BurnRate": {
        "Value": 1,
        "Exp": -3
      },
      "InitialAmount": {
        "Value": 1000000,
        "Exp": 0
      },
      "Chain": "cosmoshub-4",
      "OriginChain": "cosmoshub-4",
      "ChainSupply": "100000000",
      "Description": "Cosmos Hub native token",
      "SkipDisplay": false,
      "MetaData": {
        "Network": 1,
        "UpdatedAt": "2023-10-01T12:00:00Z",
        "CreatedAt": "2020-01-01T00:00:00Z"
      }
    }
  ],
  "Offset": 0
}
Example Request
bash
curl -H "Network: devnet" \
  -X "GET" "https://coredex.test.tx.org/api/currencies"
5. GET /api/market - Market Configuration
Returns market data for a specific trading pair, including tick size and quantity step.

Parameters
Parameter	Required	Description
symbol	✅ Yes	Trading pair symbol (URL-safe encoded)
Response Format
json
{
  "Denom1": {
    "Currency": "alb",
    "Issuer": "devcore19p7572k4pj00szx36ehpnhs8z2gqls8ky3ne43",
    "Precision": 6,
    "Denom": "alb-devcore19p7572k4pj00szx36ehpnhs8z2gqls8ky3ne43"
  },
  "Denom2": {
    "Currency": "nor",
    "Issuer": "devcore19p7572k4pj00szx36ehpnhs8z2gqls8ky3ne43",
    "Precision": 6,
    "Denom": "nor-devcore19p7572k4pj00szx36ehpnhs8z2gqls8ky3ne43"
  },
  "PriceTick": {
    "Value": 1,
    "Exp": -6
  },
  "QuantityStep": 10000
}
Field	Description
PriceTick	Minimum price increment (e.g., 1e-6 = 0.000001)
QuantityStep	Minimum quantity increment (in base units)
Example Request
bash
curl -H "Network: devnet" \
  -X "GET" "https://coredex.test.tx.org/api/market?symbol=alb-devcore19p7572k4pj00szx36ehpnhs8z2gqls8ky3ne43_nor-devcore19p7572k4pj00szx36ehpnhs8z2gqls8ky3ne43"
6. POST /api/order/create - Create Order (Unsigned)
Creates an unsigned transaction for placing an order. Returns a to-be-signed transaction. Order is not persisted until submitted.

Request Body
json
{
  "Sender": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
  "Type": 1,
  "OrderID": "optional-user-defined-id",
  "BaseDenom": "dextestdenom5-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
  "QuoteDenom": "dextestdenom9-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
  "Price": "0.25",
  "Quantity": "1000",
  "Side": 1,
  "GoodTil": {
    "GoodTilBlockHeight": 1000,
    "GoodTilBlockTime": "2025-12-30T12:00:00Z"
  },
  "TimeInForce": 1
}
Field Reference
Field	Type	Description
Sender	string	Wallet address
Type	int	1 = Limit, 2 = Market
OrderID	string	Optional user-defined ID
BaseDenom	string	Base currency denom (what you're buying/selling)
QuoteDenom	string	Quote currency denom (pricing currency)
Price	string	Human-readable price (e.g., "0.25")
Quantity	string	Human-readable quantity (e.g., "1000")
Side	int	1 = Buy, 2 = Sell
GoodTil	object	Expiry condition (block height or time)
TimeInForce	int	1 = GTC, 2 = IOC, 3 = FOK
Order Type Matrix
Parameter	Limit Order	Market Order
price	Required (e.g., "0.25")	Omit or empty string
timeInForce	GTC (1), IOC (2), FOK (3)	IOC (2) only
goodTil	Optional (time or height)	Not allowed
baseDenom	Required	Required
quoteDenom	Required	Required
quantity	Required	Required
side	Buy (1) or Sell (2)	Buy (1) or Sell (2)
type	1	2
Response Format
json
{
  "Sequence": 126378,
  "OrderData": {
    "sender": "devcore1878pk82zlndhldglx26r606qcd886562mad59y",
    "type": 1,
    "baseDenom": "dextestdenom5-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "quoteDenom": "dextestdenom9-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "price": "25e-2",
    "quantity": "1000000000",
    "side": 1,
    "goodTil": {
      "goodTilBlockTime": "2025-12-30T12:00:00Z"
    },
    "timeInForce": 1,
    "base_denom": "dextestdenom5-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "quote_denom": "dextestdenom9-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "time_in_force": 1,
    "good_til": {
      "good_til_block_time": "2025-12-30T12:00:00Z"
    }
  }
}
Note: Fields are duplicated for compatibility with both JavaScript and Go protobuf marshallers.

Example Request
bash
curl -H "Network: devnet" \
  -X "POST" "https://coredex.test.tx.org/api/order/create" \
  -H "Content-Type: application/json" \
  -d '{
    "Sender": "devcore1878pk82zlndhldglx26r606qcd886562mad59y",
    "Type": 1,
    "BaseDenom": "dextestdenom5-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "QuoteDenom": "dextestdenom9-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "Price": "0.25",
    "Quantity": "1000",
    "Side": 1,
    "GoodTil": {
      "GoodTilBlockTime": "2025-12-30T12:00:00Z"
    },
    "TimeInForce": 1
  }'
7. POST /api/order/cancel - Cancel Order
Creates a transaction to cancel an existing order.

Request Body
json
{
  "Sender": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
  "OrderID": "8b341e25-482e-487f-b9e2-9467d98c16ac"
}
Response Format
json
{
  "Sequence": 126378,
  "OrderCancel": {
    "sender": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "id": "8b341e25-482e-487f-b9e2-9467d98c16ac"
  }
}
Example Request
bash
curl -H "Network: devnet" \
  -X "POST" "https://coredex.test.tx.org/api/order/cancel" \
  -H "Content-Type: application/json" \
  -d '{
    "Sender": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "OrderID": "8b341e25-482e-487f-b9e2-9467d98c16ac"
  }'
8. POST /api/order/submit - Submit Signed Order
Submits a signed transaction to the blockchain.

Request Body
json
{
  "TX": "CqcCCqQCChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEoMCCvwBCvkBChwvY29yZXVtLmRleC52MS5Nc2dQbGFjZU9yZGVyEtgBCi5kZXZjb3JlMXAwZWR6eXpwYXpwdDY4dmRyankyMGM0Mmx2d3NqcHZmemFoeWdzEAEaBnN0cmluZyI8ZGV4dGVzdGRlbm9tNS1kZXZjb3JlMXAwZWR6eXpwYXpwdDY4dmRyankyMGM0Mmx2d3NqcHZmemFoeWdzKjxkZXh0ZXN0ZGVub205LWRldmNvcmUxcDBlZHp5enBhenB0Njh2ZHJqeTIwYzQybHZ3c2pwdmZ6YWh5Z3MyBTI1ZS0yOgoxMDAwMDAwMDAwQAFKCwjoBxIGCMCv9MYGEgISABJSCk4KRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEDWIusTf5MdJVCJlqRR1MVNO5So6We2b5v42yCQl+k3D0SBAoCCAESABpAa+STFz77MqaUIU2bbS5uKtXeOyGW/m2qLcf96WEAJPJCSnO/3em/QZtGKnF1eg4ylCawYOH/8gpDLrxI1ybsiw=="
}
Response Format
json
{
  "TXHash": "0x1234567890"
}
Example Request
bash
curl -H "Network: devnet" \
  -X "POST" "https://coredex.test.tx.org/api/order/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "TX": "CqcCCqQCChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEoMCCvwBCvkBChwvY29yZXVtLmRleC52MS5Nc2dQbGFjZU9yZGVyEtgBCi5kZXZjb3JlMXAwZWR6eXpwYXpwdDY4dmRyankyMGM0Mmx2d3NqcHZmemFoeWdzEAEaBnN0cmluZyI8ZGV4dGVzdGRlbm9tNS1kZXZjb3JlMXAwZWR6eXpwYXpwdDY4dmRyankyMGM0Mmx2d3NqcHZmemFoeWdzKjxkZXh0ZXN0ZGVub205LWRldmNvcmUxcDBlZHp5enBhenB0Njh2ZHJqeTIwYzQybHZ3c2pwdmZ6YWh5Z3MyBTI1ZS0yOgoxMDAwMDAwMDAwQAFKCwjoBxIGCMCv9MYGEgISABJSCk4KRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEDWIusTf5MdJVCJlqRR1MVNO5So6We2b5v42yCQl+k3D0SBAoCCAESABpAa+STFz77MqaUIU2bbS5uKtXeOyGW/m2qLcf96WEAJPJCSnO/3em/QZtGKnF1eg4ylCawYOH/8gpDLrxI1ybsiw=="
  }'
9. GET /api/order/orderbook - Order Book
Returns the order book for a trading pair.

Parameters
Parameter	Required	Description
symbol	✅ Yes	Trading pair symbol (format: denom1_denom2)
account	❌ No	Filter orders by account address
Response Format
json
{
  "Buy": [
    {
      "Price": "3140",
      "HumanReadablePrice": "3140",
      "Amount": "2272",
      "SymbolAmount": "0.002272",
      "Sequence": 41567,
      "OrderID": "8b341e25-482e-487f-b9e2-9467d98c16ac",
      "RemainingAmount": "2272",
      "RemainingSymbolAmount": "0.002272"
    }
  ],
  "Sell": [
    {
      "Price": "3360",
      "HumanReadablePrice": "3360",
      "Amount": "2071",
      "SymbolAmount": "0.002071",
      "Sequence": 41760,
      "OrderID": "8b341e25-482e-487f-b9e2-9467d98c16ac",
      "RemainingAmount": "2071",
      "RemainingSymbolAmount": "0.002071"
    }
  ]
}
Field	Description
Price	Price in base units
HumanReadablePrice	Human-readable price
Amount	Quantity in base units
SymbolAmount	Human-readable quantity
RemainingAmount	Remaining quantity in base units
RemainingSymbolAmount	Remaining human-readable quantity
Progress Indicator: (SymbolAmount - RemainingSymbolAmount) / SymbolAmount shows order fill percentage.

Example Request
bash
curl -H "Network: devnet" \
  -X "GET" "https://coredex.test.tx.org/api/order/orderbook?\
symbol=dextestdenom9-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs_\
dextestdenom1-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
10. GET /api/wallet/assets - Wallet Assets
Returns all assets (balances) for a specific wallet address.

Parameters
Parameter	Required	Description
address	✅ Yes	Wallet address
Response Format
json
[
  {
    "Denom": "dextestdenom0-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "Amount": "1000000000000",
    "SymbolAmount": "1000.0000"
  },
  {
    "Denom": "dextestdenom1-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "Amount": "1000000000000",
    "SymbolAmount": "1000.0000"
  }
]
Field	Description
Denom	Currency denomination (full denom string)
Amount	Balance in base units (smallest denomination)
SymbolAmount	Human-readable balance
Example Request
bash
curl -H "Network: devnet" \
  -X "GET" "https://coredex.test.tx.org/api/wallet/assets?address=devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
11. WebSocket Real-Time Updates (/api/ws)
The WebSocket service provides real-time streaming of market data.

Connection
javascript
const ws = new WebSocket('wss://coredex.test.tx.org/api/ws');

ws.onopen = () => {
  console.log('Connected to CoreDEX WebSocket');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
Subscription Message Format
json
{
  "method": "subscribe",
  "channel": "orderbook",
  "symbol": "BTC-USD",
  "id": "client-session-id"
}
Available Channels
Channel	Description	Data Format
orderbook	Real-time order book updates	Full order book snapshot + incremental updates
trades	Live trade execution feed	Individual trade objects
ticker	24hr ticker updates	Price, volume, change statistics
wallet	User balance updates	Balance changes for specific address
orders	User order status updates	Order creation, fill, cancellation events
Subscription Examples
Subscribe to Order Book
json
{
  "method": "subscribe",
  "channel": "orderbook",
  "symbol": "dextestdenom9-..._dextestdenom1-..."
}
Subscribe to Trades
json
{
  "method": "subscribe",
  "channel": "trades",
  "symbol": "BTC-USD"
}
Subscribe to Wallet Updates
json
{
  "method": "subscribe",
  "channel": "wallet",
  "address": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
}
Subscribe to User Orders
json
{
  "method": "subscribe",
  "channel": "orders",
  "address": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
}
Unsubscribe
json
{
  "method": "unsubscribe",
  "channel": "orderbook",
  "symbol": "BTC-USD"
}
WebSocket Message Types
Order Book Snapshot
json
{
  "type": "snapshot",
  "channel": "orderbook",
  "symbol": "BTC-USD",
  "data": {
    "bids": [
      ["50000.00", "0.5"],
      ["49900.00", "1.0"]
    ],
    "asks": [
      ["50100.00", "0.3"],
      ["50200.00", "0.8"]
    ]
  }
}
Order Book Update
json
{
  "type": "update",
  "channel": "orderbook",
  "symbol": "BTC-USD",
  "data": {
    "bids": [
      ["50000.00", "0.6"]  // Price, new quantity (0 = remove)
    ],
    "asks": []
  }
}
Trade Message
json
{
  "type": "trade",
  "channel": "trades",
  "symbol": "BTC-USD",
  "data": {
    "id": "trade-12345",
    "price": "50000.00",
    "quantity": "0.1",
    "side": "buy",
    "timestamp": 1704067200
  }
}
Ticker Update
json
{
  "type": "ticker",
  "channel": "ticker",
  "symbol": "BTC-USD",
  "data": {
    "last": "50000.00",
    "high": "51000.00",
    "low": "49000.00",
    "volume": "1250.5",
    "change": "2.5",
    "changePercent": "0.05"
  }
}
Wallet Update
json
{
  "type": "wallet",
  "channel": "wallet",
  "address": "devcore1...",
  "data": {
    "balances": [
      {
        "denom": "ucore",
        "amount": "1000000000",
        "symbolAmount": "1000.00"
      }
    ]
  }
}
Order Update
json
{
  "type": "order",
  "channel": "orders",
  "address": "devcore1...",
  "data": {
    "orderId": "8b341e25-482e-487f-b9e2-9467d98c16ac",
    "status": "filled",
    "filledQuantity": "1000",
    "remainingQuantity": "0",
    "avgPrice": "50000.00"
  }
}
JavaScript Client Example
javascript
class CoreDEXWebSocket {
  constructor(url) {
    this.ws = null;
    this.url = url;
    this.subscriptions = new Map();
  }

  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      console.log('Connected');
      this.resubscribeAll();
    };
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };
    
    this.ws.onclose = () => {
      console.log('Disconnected, reconnecting in 5s...');
      setTimeout(() => this.connect(), 5000);
    };
  }

  subscribe(channel, params, callback) {
    const key = `${channel}:${JSON.stringify(params)}`;
    this.subscriptions.set(key, { channel, params, callback });
    
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        method: 'subscribe',
        channel,
        ...params
      }));
    }
  }

  unsubscribe(channel, params) {
    const key = `${channel}:${JSON.stringify(params)}`;
    this.subscriptions.delete(key);
    
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        method: 'unsubscribe',
        channel,
        ...params
      }));
    }
  }

  handleMessage(message) {
    // Route to appropriate handler
    const { channel, type, symbol, data } = message;
    
    for (const [key, sub] of this.subscriptions) {
      if (sub.channel === channel) {
        sub.callback(message);
      }
    }
  }

  resubscribeAll() {
    for (const [_, sub] of this.subscriptions) {
      this.ws.send(JSON.stringify({
        method: 'subscribe',
        channel: sub.channel,
        ...sub.params
      }));
    }
  }
}

// Usage
const dexWS = new CoreDEXWebSocket('wss://coredex.test.tx.org/api/ws');
dexWS.connect();

// Subscribe to BTC-USD order book
dexWS.subscribe('orderbook', { symbol: 'BTC-USD' }, (data) => {
  console.log('Order book update:', data);
});

// Subscribe to wallet updates
dexWS.subscribe('wallet', { address: 'devcore1...' }, (data) => {
  console.log('Balance update:', data);
});
Application Start Parameters
Environment Variables
Variable	Required	Description
NETWORKS	✅ Yes	Network configuration JSON
STATE_STORE	✅ Yes	State store gRPC endpoint (e.g., localhost:50051)
TRADE_STORE	✅ Yes	Trade store gRPC endpoint
OHLC_STORE	✅ Yes	OHLC store gRPC endpoint
ORDER_STORE	✅ Yes	Order store gRPC endpoint
CURRENCY_STORE	✅ Yes	Currency store gRPC endpoint
LOG_LEVEL	❌ No	debug, info, warn, error (default: info)
HTTP_CONFIG	❌ No	HTTP server configuration JSON
BASE_COIN	❌ No	Native coin configuration JSON
BASE_USDC	❌ No	USDC reference configuration JSON
NETWORKS Configuration
json
{
  "Node": [
    {
      "Network": "devnet",
      "GRPCHost": "grpc.devnet.tx.dev:443",
      "RPCHost": "https://rpc.devnet.tx.dev:443"
    },
    {
      "Network": "testnet",
      "GRPCHost": "grpc.testnet.tx.dev:443",
      "RPCHost": "https://rpc.testnet.tx.dev:443"
    },
    {
      "Network": "mainnet",
      "GRPCHost": "grpc.tx.org:443",
      "RPCHost": "https://rpc.tx.org:443"
    }
  ]
}
Production Note: Use private nodes, not public endpoints.

HTTP_CONFIG Configuration
json
{
  "HTTP": {
    "port": ":8080",
    "cors": {
      "allowedOrigins": ["http://localhost:3000", "https://yourdex.com"]
    },
    "timeouts": {
      "read": "10s",
      "write": "10s",
      "idle": "10s",
      "shutdown": "10s"
    }
  }
}
BASE_COIN Configuration
json
{
  "BaseCoin": [
    {
      "Network": "devnet",
      "Coin": "udevcore"
    },
    {
      "Network": "testnet",
      "Coin": "utestcore"
    },
    {
      "Network": "mainnet",
      "Coin": "ucore"
    }
  ]
}
BASE_USDC Configuration
Used by the path-finding algorithm (non-weighted Dijkstra) to resolve USD values.

json
{
  "BaseUSDC": [
    {
      "Network": "devnet",
      "Coin": "uusdc-E1E3674A0E4E1EF9C69646F9AF8D9497173821826074622D831BAB73CCB99A2D"
    },
    {
      "Network": "mainnet",
      "Coin": "ibc/8E2F4F1B6F5C9A7D3E8B2C4D6F1A9E7B5C3D8F2A6E4B9C7D1F5A3E8B2C6D4F"
    }
  ]
}
Note: Devnet/testnet may not have IBC USDC. Users may not see USD values on those networks.

Starting the API Server
Command Line
bash
export NETWORKS='{"Node":[{"Network":"devnet","GRPCHost":"grpc.devnet.tx.dev:443","RPCHost":"https://rpc.devnet.tx.dev:443"}]}'
export STATE_STORE="localhost:50051"
export TRADE_STORE="localhost:50051"
export OHLC_STORE="localhost:50051"
export ORDER_STORE="localhost:50051"
export CURRENCY_STORE="localhost:50051"
export LOG_LEVEL="info"
export HTTP_CONFIG='{"HTTP":{"port":":8080","cors":{"allowedOrigins":["http://localhost:3000"]}}}'

go run cmd/api-server/main.go
Docker
bash
docker run -d \
  -e NETWORKS='{"Node":[{"Network":"mainnet","GRPCHost":"grpc.tx.org:443","RPCHost":"https://rpc.tx.org:443"}]}' \
  -e STATE_STORE="store:50051" \
  -e TRADE_STORE="store:50051" \
  -e OHLC_STORE="store:50051" \
  -e ORDER_STORE="store:50051" \
  -e CURRENCY_STORE="store:50051" \
  -e LOG_LEVEL="info" \
  -e HTTP_CONFIG='{"HTTP":{"port":":8080","cors":{"allowedOrigins":["*"]}}}' \
  -p 8080:8080 \
  coreumfoundation/api-server:latest
Error Handling
HTTP Status Codes
Status	Description
200	Success
400	Bad Request (invalid parameters)
401	Unauthorized
404	Not Found
429	Too Many Requests
500	Internal Server Error
Error Response Format
json
{
  "error": true,
  "code": 400,
  "message": "Invalid symbol format",
  "details": "Symbol must be URL-safe encoded"
}
Common Errors
Error	Cause	Solution
invalid symbol	Symbol not URL-safe encoded	Use encodeURIComponent()
period not supported	Invalid timeframe	Use allowed periods: 1m, 5m, 1h, etc.
insufficient balance	Not enough funds	Check wallet/assets endpoint
order validation failed	Price/quantity below tick size	Check /market endpoint for limits
store connection failed	Store not running	Start store service first
Rate Limiting
Default rate limits:

Endpoint	Limit
GET /api/ohlc	100 requests/minute
GET /api/trades	100 requests/minute
GET /api/tickers	200 requests/minute
POST /api/order/*	50 requests/minute
WebSocket	10 connections/IP
Complete Workflow Example
1. Get Market Information
bash
# Get available currencies
curl -H "Network: devnet" \
  "https://coredex.test.tx.org/api/currencies"

# Get market config for trading pair
curl -H "Network: devnet" \
  "https://coredex.test.tx.org/api/market?symbol=BASE_QUOTE"
2. Check Wallet Balance
bash
curl -H "Network: devnet" \
  "https://coredex.test.tx.org/api/wallet/assets?address=devcore1..."
3. Get Order Book
bash
curl -H "Network: devnet" \
  "https://coredex.test.tx.org/api/order/orderbook?symbol=BASE_QUOTE"
4. Create Unsigned Order
bash
curl -X POST "https://coredex.test.tx.org/api/order/create" \
  -H "Content-Type: application/json" \
  -H "Network: devnet" \
  -d '{
    "Sender": "devcore1...",
    "Type": 1,
    "BaseDenom": "BASE",
    "QuoteDenom": "QUOTE",
    "Price": "100.00",
    "Quantity": "1.5",
    "Side": 1,
    "TimeInForce": 1
  }'
5. Sign Transaction (Client-side)
javascript
// Using Keplr wallet
const signer = await window.keplr.getOfflineSigner("txchain-devnet-1");
const signedTx = await signer.sign(client, orderData);
6. Submit Signed Order
bash
curl -X POST "https://coredex.test.tx.org/api/order/submit" \
  -H "Content-Type: application/json" \
  -H "Network: devnet" \
  -d '{"TX": "base64-encoded-signed-tx"}'
7. Monitor via WebSocket
javascript
const ws = new WebSocket('wss://coredex.test.tx.org/api/ws');
ws.onopen = () => {
  ws.send(JSON.stringify({
    method: 'subscribe',
    channel: 'orders',
    address: 'devcore1...'
  }));
};
Resources
Resource	Link
Store Documentation	./store.md
Data Aggregator	./data-aggregator.md
UI Documentation	./ui.md
CoreDEX GitHub	https://github.com/tokenize-x/coredex
TX Blockchain	https://tx.org
text

Now update the DEX README to link to this comprehensive API server documentation:

```bash
nano ~/dev/TXdocumentation/dex/README.md
Update the API Server section:

markdown
### API Server

The API Server provides a **complete RESTful API** for the CoreDEX with WebSocket real-time updates.

📖 **[API Server Documentation](./api-server.md)** - Complete API reference

**Key features:**
- 11 REST endpoints (OHLC, trades, order book, orders, wallet)
- WebSocket real-time streaming (orderbook, trades, ticker, wallet, orders)
- Human-readable numeric values (no denomination math)
- Built-in business rule validation
- Order creation → signing → submission flow

**Quick API Reference:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/ohlc` | GET | OHLC candlestick data |
| `/api/trades` | GET | Trade history |
| `/api/tickers` | GET | Latest prices (base64 symbols) |
| `/api/currencies` | GET | Available currencies |
| `/api/market` | GET | Market config (tick size, step) |
| `/api/order/orderbook` | GET | Order book (50 bids/asks) |
| `/api/wallet/assets` | GET | Wallet balances |
| `/api/order/create` | POST | Create unsigned order |
| `/api/order/submit` | POST | Submit signed order |
| `/api/order/cancel` | POST | Cancel order |
| `/api/ws` | WebSocket | Real-time updates |

**WebSocket Channels:**
- `orderbook` - Real-time order book updates
- `trades` - Live trade feed
- `ticker` - 24hr ticker updates
- `wallet` - Balance changes
- `orders` - Order status updates
