# CoreDEX Update Service (WebSocket)

The Update Service provides a WebSocket that refreshes data based on actual changes. Using WebSocket reduces the number of database reads required to serve data to connected clients, thus lowering database load and related costs.

## Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Update Service Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Client │────▶│ WebSocket │────▶│ Database │ │
│ │ (Browser) │◀────│ (/ws) │◀────│ Polling │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │ │ │
│ │ Subscribe │ Every 10s │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Real-time │ │ Subscription│ │ OHLC/Trades │ │
│ │ Updates │ │ Management │ │ Order Book │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Key Features

| Feature | Description |
|---------|-------------|
| **Polling Interval** | Subscriptions poll database every 10 seconds |
| **Data Types** | OHLC, Trades, Tickers, Order Book, Wallet |
| **Connection Timeout** | 15 minutes of inactivity |
| **Response Format** | Echoes request + serialized JSON response |

## WebSocket Endpoint

| Network | WebSocket URL |
|---------|---------------|
| Mainnet | `wss://api.tx.org/ws` |
| Testnet | `wss://api.testnet.tx.org/ws` |
| Devnet | `wss://api.devnet.tx.org/ws` |

## Connection Management

### Initial Connection

Upon successful connection, the client receives:

```json
{
  "Action": "connected",
  "Message": "Connected to CoreDEX Update Service"
}
Connection Timeout
Connections are terminated after 15 minutes of inactivity to prevent background usage from overloading the application.

Important: The frontend application has a 10-minute background tab timeout, which is shorter than the 15-minute server timeout. The frontend will always be able to reconnect when switching tabs.

Reconnection Strategy
Background tabs may terminate WebSocket connections by going to sleep, which can lead to data loss. On tab reactivation:

Reload all data from scratch using REST API calls

Re-subscribe to all topics

Trade Subscription Consideration
For personal trades subscriptions, the timeout will occur when a tab is open for a long time without trading activity.

Recommendation: Open trade subscriptions only when the user performs an actual trade. In >99% of cases, the trade executes within the 15-minute window.

Message Protocol
Request Messages (Client → Server)
1. Subscribe to Topic
json
{
  "Action": "subscribe",
  "Subscription": {
    "Network": "mainnet",
    "Method": "ORDERBOOK",
    "ID": "denom1_denom2"
  }
}
2. Unsubscribe from Topic
json
{
  "Action": "unsubscribe",
  "Subscription": {
    "Network": "mainnet",
    "Method": "ORDERBOOK",
    "ID": "denom1_denom2"
  }
}
3. Close Connection
json
{
  "Action": "close"
}
Note: Using the close action is preferred so subscriptions can be cleaned up properly instead of garbage collected.

Response Messages (Server → Client)
Response messages echo the request structure so the caller can sync responses with requests.

json
{
  "Action": "response",
  "Subscription": {
    "Network": "mainnet",
    "Method": "ORDERBOOK",
    "ID": "core1abcdef",
    "Content": "{\"Buy\":[...],\"Sell\":[...]}"
  }
}
Field	Description
Action	Always "response" (or enum integer)
Subscription.Network	Network identifier
Subscription.Method	Topic type (enum integer)
Subscription.ID	Entity identifier (always present in responses)
Subscription.Content	Serialized JSON response (same format as REST API)
Subscription Methods (Topics)
Method Enum Values
Method	Integer	Description
OHLC	1	Candlestick data
TRADES	2	Trade history
TICKER	3	24hr ticker statistics
ORDERBOOK	4	Order book snapshot
WALLET	5	Wallet balances
ORDERBOOK_FOR_SYMBOL_AND_ACCOUNT	6	User-specific order book
TRADES_FOR_ACCOUNT	7	User trade history
TRADES_FOR_SYMBOL	8	Symbol trade history
TRADES_FOR_ACCOUNT_AND_SYMBOL	9	User + symbol trades
ID Format by Method
Method	ID Format	Example
OHLC	denom-issuer_denom2-issuer2_period	ucore-devcore1..._uusdc-..._1h
TICKER	denom-issuer_denom2-issuer2	ucore-devcore1..._uusdc-...
ORDERBOOK	denom-issuer_denom2-issuer2	ucore-devcore1..._uusdc-...
ORDERBOOK_FOR_SYMBOL_AND_ACCOUNT	account_denom-issuer_denom2-issuer2	devcore1..._ucore-..._uusdc-...
WALLET	account	devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs
TRADES_FOR_ACCOUNT	account	devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs
TRADES_FOR_SYMBOL	denom-issuer_denom2-issuer2	ucore-devcore1..._uusdc-...
TRADES_FOR_ACCOUNT_AND_SYMBOL	account_denom-issuer_denom2-issuer2	devcore1..._ucore-..._uusdc-...
Topic Details
1. OHLC Subscription
Most complex subscription due to period requirement. Other parameters (timestamps) are determined by the backend.

ID Format
text
denom-issuer_denom2-issuer2_period
Supported Periods
Period	Description
1m	1 minute
5m	5 minutes
15m	15 minutes
1h	1 hour
4h	4 hours
1d	1 day
1w	1 week
1M	1 month
Behavior
Produces data for the last complete interval

Flows over to next interval when reached

Contains last 10 minutes of data

Data needs to be merged into existing OHLC data

Replace previous records if present

Example Subscription
json
{
  "Action": "subscribe",
  "Subscription": {
    "Network": "mainnet",
    "Method": 1,
    "ID": "ucore-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs_uusdc-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs_1h"
  }
}
Example Response
json
{
  "Action": "response",
  "Subscription": {
    "Network": "mainnet",
    "Method": 1,
    "ID": "ucore-..._uusdc-..._1h",
    "Content": "[[1704067200,\"50000.00\",\"51000.00\",\"49000.00\",\"50500.00\",\"1250.5\"],[1704067260,\"50500.00\",\"50800.00\",\"50400.00\",\"50700.00\",\"800.3\"]]"
  }
}
2. Trades Subscription
Multiple filters available depending on required information.

Subscription Types
Method	ID Format	Use Case
TRADES_FOR_ACCOUNT	account	User's personal trade history
TRADES_FOR_SYMBOL	denom-issuer_denom2-issuer2	All trades for a trading pair
TRADES_FOR_ACCOUNT_AND_SYMBOL	account_denom-issuer_denom2-issuer2	User's trades for specific pair
Behavior
Trades are read from the last 10 minutes

Same format as REST API

Deduplication required - Receiver must deduplicate against existing data

Example Subscription (All Trades for Symbol)
json
{
  "Action": "subscribe",
  "Subscription": {
    "Network": "mainnet",
    "Method": 8,
    "ID": "ucore-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs_uusdc-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
  }
}
Example Response
json
{
  "Action": "response",
  "Subscription": {
    "Network": "mainnet",
    "Method": 8,
    "ID": "ucore-..._uusdc-...",
    "Content": "{\"Trades\":[{\"Account\":\"devcore1...\",\"Price\":50000,\"Quantity\":\"0.1\",\"Side\":1,\"Timestamp\":1704067200}]}"
  }
}
3. Ticker Subscription
24-hour statistics for a trading pair.

ID Format
text
denom-issuer_denom2-issuer2
Behavior
Same format as REST API /api/tickers endpoint

Updates every 10 seconds

Example Subscription
json
{
  "Action": "subscribe",
  "Subscription": {
    "Network": "mainnet",
    "Method": 3,
    "ID": "ucore-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs_uusdc-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
  }
}
Example Response
json
{
  "Action": "response",
  "Subscription": {
    "Network": "mainnet",
    "Method": 3,
    "ID": "ucore-..._uusdc-...",
    "Content": "{\"OpenTime\":1704063600,\"CloseTime\":1704150000,\"OpenPrice\":50000,\"HighPrice\":51000,\"LowPrice\":49000,\"LastPrice\":50500,\"Volume\":1250.5}"
  }
}
4. Order Book Subscription
Real-time order book updates.

Subscription Types
Method	ID Format	Use Case
ORDERBOOK	denom-issuer_denom2-issuer2	Market order book
ORDERBOOK_FOR_SYMBOL_AND_ACCOUNT	account_denom-issuer_denom2-issuer2	User-specific order book
Behavior
Complete replacement of previous order book

Represents current state of order book

First 50 bids and 50 asks around the spread

Same format as REST API /api/order/orderbook

Example Subscription
json
{
  "Action": "subscribe",
  "Subscription": {
    "Network": "mainnet",
    "Method": 4,
    "ID": "ucore-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs_uusdc-devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
  }
}
Example Response
json
{
  "Action": "response",
  "Subscription": {
    "Network": "mainnet",
    "Method": 4,
    "ID": "ucore-..._uusdc-...",
    "Content": "{\"Buy\":[{\"Price\":\"50000\",\"Amount\":\"2272\",\"Sequence\":41567,\"OrderID\":\"8b341e25-482e-487f-b9e2-9467d98c16ac\"}],\"Sell\":[{\"Price\":\"50100\",\"Amount\":\"2071\",\"Sequence\":41760,\"OrderID\":\"8b341e25-482e-487f-b9e2-9467d98c16ac\"}]}"
  }
}
5. Wallet Subscription
Real-time balance updates for a wallet address.

ID Format
text
account
Behavior
Returns all assets for the account

Same format as REST API /api/wallet/assets

Example Subscription
json
{
  "Action": "subscribe",
  "Subscription": {
    "Network": "mainnet",
    "Method": 5,
    "ID": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs"
  }
}
Example Response
json
{
  "Action": "response",
  "Subscription": {
    "Network": "mainnet",
    "Method": 5,
    "ID": "devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs",
    "Content": "[{\"Denom\":\"ucore\",\"Amount\":\"1000000000000\",\"SymbolAmount\":\"1000.0000\"},{\"Denom\":\"uusdc\",\"Amount\":\"5000000000\",\"SymbolAmount\":\"5000.0000\"}]"
  }
}
Complete JavaScript Client Example
javascript
class CoreDEXUpdateService {
  constructor(network = 'mainnet') {
    const endpoints = {
      mainnet: 'wss://api.tx.org/ws',
      testnet: 'wss://api.testnet.tx.org/ws',
      devnet: 'wss://api.devnet.tx.org/ws'
    };
    this.url = endpoints[network];
    this.ws = null;
    this.subscriptions = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      console.log('Connected to CoreDEX Update Service');
      this.reconnectAttempts = 0;
      this.resubscribeAll();
    };
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };
    
    this.ws.onclose = () => {
      console.log('Disconnected, reconnecting...');
      this.reconnect();
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
      setTimeout(() => this.connect(), delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  subscribe(method, id, callback) {
    const key = `${method}:${id}`;
    this.subscriptions.set(key, { method, id, callback });
    
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        Action: 'subscribe',
        Subscription: {
          Network: this.getNetworkId(),
          Method: method,
          ID: id
        }
      }));
    }
  }

  unsubscribe(method, id) {
    const key = `${method}:${id}`;
    this.subscriptions.delete(key);
    
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        Action: 'unsubscribe',
        Subscription: {
          Network: this.getNetworkId(),
          Method: method,
          ID: id
        }
      }));
    }
  }

  close() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ Action: 'close' }));
      this.ws.close();
    }
  }

  handleMessage(message) {
    if (message.Action === 'response') {
      const { Method, ID, Content } = message.Subscription;
      const key = `${Method}:${ID}`;
      const subscription = this.subscriptions.get(key);
      
      if (subscription && subscription.callback) {
        try {
          const parsedContent = JSON.parse(Content);
          subscription.callback(parsedContent, { method: Method, id: ID });
        } catch (e) {
          console.error('Failed to parse content:', e);
        }
      }
    }
  }

  resubscribeAll() {
    for (const [_, sub] of this.subscriptions) {
      this.ws.send(JSON.stringify({
        Action: 'subscribe',
        Subscription: {
          Network: this.getNetworkId(),
          Method: sub.method,
          ID: sub.id
        }
      }));
    }
  }

  getNetworkId() {
    // Convert network name to enum integer
    const networks = { mainnet: 1, testnet: 2, devnet: 3 };
    return networks[this.url.includes('mainnet') ? 'mainnet' : 
                      this.url.includes('testnet') ? 'testnet' : 'devnet'];
  }

  // Helper methods for common subscriptions
  subscribeOrderBook(baseDenom, baseIssuer, quoteDenom, quoteIssuer, callback) {
    const id = `${baseDenom}-${baseIssuer}_${quoteDenom}-${quoteIssuer}`;
    this.subscribe(4, id, callback);
  }

  subscribeTicker(baseDenom, baseIssuer, quoteDenom, quoteIssuer, callback) {
    const id = `${baseDenom}-${baseIssuer}_${quoteDenom}-${quoteIssuer}`;
    this.subscribe(3, id, callback);
  }

  subscribeWallet(address, callback) {
    this.subscribe(5, address, callback);
  }

  subscribeTradesForSymbol(baseDenom, baseIssuer, quoteDenom, quoteIssuer, callback) {
    const id = `${baseDenom}-${baseIssuer}_${quoteDenom}-${quoteIssuer}`;
    this.subscribe(8, id, callback);
  }

  subscribeTradesForAccount(address, callback) {
    this.subscribe(7, address, callback);
  }

  subscribeOHLC(baseDenom, baseIssuer, quoteDenom, quoteIssuer, period, callback) {
    const id = `${baseDenom}-${baseIssuer}_${quoteDenom}-${quoteIssuer}_${period}`;
    this.subscribe(1, id, callback);
  }
}

// Usage Example
const updateService = new CoreDEXUpdateService('mainnet');
updateService.connect();

// Subscribe to order book
updateService.subscribeOrderBook('ucore', 'devcore1...', 'uusdc', 'devcore1...', (orderBook) => {
  console.log('Order book updated:', orderBook);
  // Update UI with new order book (replace entire book)
});

// Subscribe to wallet
updateService.subscribeWallet('devcore1p0edzyzpazpt68vdrjy20c42lvwsjpvfzahygs', (balances) => {
  console.log('Wallet updated:', balances);
  // Update UI with new balances
});

// Subscribe to trades for a symbol
updateService.subscribeTradesForSymbol('ucore', 'devcore1...', 'uusdc', 'devcore1...', (trades) => {
  console.log('New trades:', trades);
  // Deduplicate and append to trade history
});

// Unsubscribe when done
// updateService.unsubscribe(4, 'ucore-..._uusdc-...');
React Hook Example
javascript
import { useState, useEffect, useCallback, useRef } from 'react';

function useCoreDEXSubscription(network = 'mainnet') {
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);
  const subscriptionsRef = useRef(new Map());

  const connect = useCallback(() => {
    const endpoints = {
      mainnet: 'wss://api.tx.org/ws',
      testnet: 'wss://api.testnet.tx.org/ws',
      devnet: 'wss://api.devnet.tx.org/ws'
    };
    
    wsRef.current = new WebSocket(endpoints[network]);
    
    wsRef.current.onopen = () => {
      setIsConnected(true);
      // Resubscribe to all
      for (const [key, sub] of subscriptionsRef.current) {
        wsRef.current.send(JSON.stringify({
          Action: 'subscribe',
          Subscription: {
            Network: { mainnet: 1, testnet: 2, devnet: 3 }[network],
            Method: sub.method,
            ID: sub.id
          }
        }));
      }
    };
    
    wsRef.current.onclose = () => {
      setIsConnected(false);
      // Reconnect after 5 seconds
      setTimeout(() => connect(), 5000);
    };
    
    wsRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.Action === 'response') {
        const { Method, ID, Content } = message.Subscription;
        const key = `${Method}:${ID}`;
        const sub = subscriptionsRef.current.get(key);
        if (sub && sub.callback) {
          sub.callback(JSON.parse(Content));
        }
      }
    };
  }, [network]);

  const subscribe = useCallback((method, id, callback) => {
    const key = `${method}:${id}`;
    subscriptionsRef.current.set(key, { method, id, callback });
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        Action: 'subscribe',
        Subscription: {
          Network: { mainnet: 1, testnet: 2, devnet: 3 }[network],
          Method: method,
          ID: id
        }
      }));
    }
    
    // Return unsubscribe function
    return () => {
      subscriptionsRef.current.delete(key);
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          Action: 'unsubscribe',
          Subscription: {
            Network: { mainnet: 1, testnet: 2, devnet: 3 }[network],
            Method: method,
            ID: id
          }
        }));
      }
    };
  }, [network]);

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) {
        wsRef.current.send(JSON.stringify({ Action: 'close' }));
        wsRef.current.close();
      }
    };
  }, [connect]);

  return { isConnected, subscribe };
}

// Usage in React component
function TradingView({ market }) {
  const [orderBook, setOrderBook] = useState({ bids: [], asks: [] });
  const [trades, setTrades] = useState([]);
  const { isConnected, subscribe } = useCoreDEXSubscription('mainnet');

  useEffect(() => {
    // Subscribe to order book
    const unsubscribeOrderBook = subscribe(4, market.symbol, (data) => {
      setOrderBook(data); // Replace entire order book
    });

    // Subscribe to trades
    const unsubscribeTrades = subscribe(8, market.symbol, (data) => {
      setTrades(prev => [...data.Trades, ...prev].slice(0, 100)); // Deduplicate
    });

    return () => {
      unsubscribeOrderBook();
      unsubscribeTrades();
    };
  }, [market.symbol, subscribe]);

  return (
    <div>
      <div>Connected: {isConnected ? '✅' : '❌'}</div>
      {/* Render order book and trades */}
    </div>
  );
}
Method Enum Reference (Integer Values)
For languages without enum support, use these integer values:

Method	Integer
OHLC	1
TRADES	2
TICKER	3
ORDERBOOK	4
WALLET	5
ORDERBOOK_FOR_SYMBOL_AND_ACCOUNT	6
TRADES_FOR_ACCOUNT	7
TRADES_FOR_SYMBOL	8
TRADES_FOR_ACCOUNT_AND_SYMBOL	9
Network Enum Reference
Network	Integer
mainnet	1
testnet	2
devnet	3
Best Practices
1. Connection Management
javascript
// ✅ Good: Handle reconnection with exponential backoff
let reconnectAttempts = 0;
const maxAttempts = 5;

function reconnect() {
  if (reconnectAttempts < maxAttempts) {
    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
    setTimeout(() => connect(), delay);
    reconnectAttempts++;
  }
}

// ❌ Bad: Immediate reconnect without backoff
ws.onclose = () => connect();
2. Data Deduplication
javascript
// Trades require deduplication
const tradeCache = new Set();

function handleTrades(newTrades) {
  const uniqueTrades = newTrades.filter(trade => {
    if (tradeCache.has(trade.TXID)) return false;
    tradeCache.add(trade.TXID);
    return true;
  });
  
  setTrades(prev => [...uniqueTrades, ...prev].slice(0, 100));
}
3. Order Book Replacement
javascript
// ✅ Good: Replace entire order book
subscribe(4, symbol, (data) => {
  setOrderBook(data); // Complete replacement
});

// ❌ Bad: Trying to merge (server sends full snapshot)
subscribe(4, symbol, (data) => {
  setOrderBook(prev => mergeOrderBooks(prev, data));
});
4. Tab Reactivation
javascript
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    // Tab became active again
    refreshAllData(); // REST API call
    reconnect(); // Re-establish WebSocket
  }
});
5. Trade Subscription Optimization
javascript
// ✅ Good: Subscribe only when user trades
function onUserPlacesOrder() {
  subscribe(7, userAddress, handleUserTrades);
}

// ❌ Bad: Always subscribed even when not trading
useEffect(() => {
  subscribe(7, userAddress, handleUserTrades);
}, []);
Troubleshooting
Issue	Cause	Solution
Connection drops after 15 minutes	Inactivity timeout	Implement reconnection logic
Missing trade data	Deduplication needed	Track received TXIDs
OHLC data gaps	Merge strategy incorrect	Replace, don't append
High memory usage	Too many subscriptions	Unsubscribe when components unmount
Reconnection loop	Immediate reconnect on close	Use exponential backoff
Resources
Resource	Link
API Server Documentation	./api-server.md
CoreDEX API Guide	./coredex-api.md
UI Documentation	./ui.md
WebSocket API Reference	MDN WebSocket API
text

Now update the DEX README to include the Update Service:

```bash
nano ~/dev/TXdocumentation/dex/README.md
Add this section:

markdown
### Update Service (WebSocket)

The Update Service provides real-time WebSocket streaming for market data, reducing database load compared to polling.

📖 **[Update Service Documentation](./update-service.md)**

**Key features:**
- Polls database every 10 seconds for changes
- 15-minute connection timeout (with reconnection strategy)
- Multiple subscription types (OHLC, trades, ticker, order book, wallet)
- Complete order book replacement (not incremental)
- Trade deduplication required

**Subscription Methods:**

| Method | ID Format | Use Case |
|--------|-----------|----------|
| OHLC (1) | `denom-issuer_denom2-issuer2_period` | Candlestick charts |
| Trades (2/7/8/9) | Various | Trade history |
| Ticker (3) | `denom-issuer_denom2-issuer2` | 24hr stats |
| Order Book (4/6) | `denom-issuer_denom2-issuer2` | Real-time orders |
| Wallet (5) | `account` | Balance updates |

**Message Flow:**
Client Server
│ │
│── subscribe ───────────▶│
│ │
│◀── response (every 10s)─│
│ │
│── unsubscribe ─────────▶│
│ │
│── close ───────────────▶│

text

**Quick Connect:**
```javascript
const ws = new WebSocket('wss://api.tx.org/ws');
ws.send(JSON.stringify({
  Action: 'subscribe',
  Subscription: {
    Network: 'mainnet',
    Method: 4,  // ORDERBOOK
    ID: 'ucore-issuer_uusdc-issuer'
  }
}));
