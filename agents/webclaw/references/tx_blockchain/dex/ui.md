# CoreDEX UI

This is the front-end UI for the CoreDEX demo application.

> **Note:** This webapp is not fully responsive and is developed for a desktop screen of 1440px - 1024px. Some screen sizes may not look the best as of now.

## Overview

The CoreDEX UI provides a complete trading interface including:
- Order book visualization
- Trade history
- OHLC charts
- Order entry forms
- Wallet balance display
- Real-time WebSocket updates

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ CoreDEX UI Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ React Application │ │
│ │ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────────┐ │ │
│ │ │ Order │ │ Trade │ │ Chart │ │ Wallet Balance │ │ │
│ │ │ Book │ │ History │ │ (OHLC) │ │ │ │ │
│ │ └───────────┘ └───────────┘ └───────────┘ └───────────────────┘ │ │
│ │ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────────┐ │ │
│ │ │ Order │ │ Open │ │ Market │ │ Trading View │ │ │
│ │ │ Entry │ │ Orders │ │ Selector │ │ Chart │ │ │
│ │ └───────────┘ └───────────┘ └───────────┘ └───────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ┌───────────────┼───────────────┐ │
│ ▼ ▼ ▼ │
│ ┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐ │
│ │ WebSocket │ │ REST API │ │ Local State │ │
│ │ (services/ │ │ (services/ │ │ (Zustand) │ │
│ │ websocket.ts) │ │ api.ts) │ │ │ │
│ └─────────────────────┘ └─────────────────┘ └─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Running the UI

### Quick Start

```bash
# Navigate to frontend directory
cd /apps/frontend/

# Make start script executable (first time only)
chmod +x ./bin/start.sh

# Start the UI
./bin/start.sh
Access the UI
Once running, access the UI at: http://localhost:3000

Start Parameters
The UI is configured using environment variables:

Variable	Description	Required
VITE_ENV_BASE_API	API server URL used in services/api.ts	✅ Yes
VITE_ENV_WS	WebSocket URL used in services/websocket.ts	✅ Yes
VITE_ENV_MODE	Development flag for env import method	Optional
VITE_ENV_DEFAULT_MARKET_CONFIGS	Object storing pair ID for market per network	Optional
Environment Configuration Example
env
# .env file
VITE_ENV_BASE_API=http://localhost:8080
VITE_ENV_WS=ws://localhost:8080/ws
VITE_ENV_MODE=development
VITE_ENV_DEFAULT_MARKET_CONFIGS={"devnet":"123","testnet":"456","mainnet":"789"}
Environment Import Pattern
In this project, envs are imported in /config/envs.ts:

typescript
// config/envs.ts
interface CoreumEnv {
  VITE_ENV_BASE_API: string;
  VITE_ENV_WS: string;
}

const env: CoreumEnv =
  import.meta.env.VITE_ENV_MODE === "development"
    ? {
        VITE_ENV_BASE_API: import.meta.env.VITE_ENV_BASE_API,
        VITE_ENV_WS: import.meta.env.VITE_ENV_WS,
      }
    : (window as any).TX?.env;

export const BASE_API_URL = env.VITE_ENV_BASE_API;
export const WS_URL = env.VITE_ENV_WS;
Note: If using a different framework or build tool, adjust how envs are named and imported.

Utility Files
The project contains two utility files intended for your own DEX implementation:

File	Purpose
services/websocket.ts	WebSocket connection management
services/api.ts	Backend API calls
WebSocket Service
The WebSocket manager handles real-time data updates including:

Order book updates

Trade execution notifications

Balance changes

Order status updates

WebSocket Manager Features
Automatic reconnection

Subscription management

Data handling with configurable update strategies

State management

Using the WebSocket Manager
typescript
import { useEffect, useMemo } from 'react';
import {
  Method,
  NetworkToEnum,
  UpdateStrategy,
  wsManager,
} from "@/services/websocket";

const TradingComponent: React.FC = () => {
  // Create subscription configuration
  const walletSubscription = useMemo(
    () => ({
      Network: NetworkToEnum(network),
      Method: Method.WALLET,
      ID: `${wallet ? wallet.address : ""}`,
    }),
    [market.pair_symbol, wallet]
  );

  // Custom handler for wallet updates
  const handleWalletUpdate = (message: WalletBalances) => {
    if (message.length > 0) {
      setWalletBalances(message);
    }
  };

  useEffect(() => {
    // Connect and subscribe
    wsManager.connected().then(() => {
      wsManager.subscribe(
        walletSubscription,
        handleWalletUpdate,
        UpdateStrategy.REPLACE
      );
    });
    
    // Cleanup on unmount
    return () => {
      wsManager.unsubscribe(walletSubscription, setWalletBalances);
    };
  }, [walletSubscription]);

  return (
    <div>
      {/* Component UI */}
    </div>
  );
};

export default TradingComponent;
WebSocket Subscription Methods
Method	Description
Method.ORDER_BOOK	Subscribe to order book updates
Method.TRADES	Subscribe to trade history
Method.WALLET	Subscribe to wallet balance updates
Method.ORDERS	Subscribe to user orders
Update Strategies
Strategy	Description
UpdateStrategy.REPLACE	Replace existing data entirely
UpdateStrategy.MERGE	Merge new data with existing
UpdateStrategy.APPEND	Append new data to existing
Custom Handler Function
You can pass a custom handler function or just a setter:

typescript
// Custom handler example
const handleCustomUpdate = (data: OrderBook) => {
  // Custom logic
  const processedData = processOrderBook(data);
  updateState(processedData);
};

// Simple setter example
wsManager.subscribe(subscription, setOrderBook, UpdateStrategy.REPLACE);
API Service
The services/api.ts file handles all backend API calls:

typescript
// Example API calls
import { api } from '@/services/api';

// Get order book
const orderBook = await api.getOrderBook(market);

// Place order
const result = await api.placeOrder({
  market: "BTC-USD",
  side: "buy",
  type: "limit",
  price: "50000",
  amount: "0.1"
});

// Get trade history
const trades = await api.getTradeHistory(market, limit, offset);

// Get OHLC data
const ohlc = await api.getOHLC(market, resolution, from, to);
Helper Utilities
Refer to /utils/index.ts for helper functions:

Volume Weighted Average Price
getAvgPriceFromOBbyVolume calculates a volume-weighted price based on the current order book:

typescript
import { getAvgPriceFromOBbyVolume } from '@/utils';

// Calculate average price for a given volume
const volume = 1000; // Amount to buy/sell
const avgPrice = getAvgPriceFromOBbyVolume(orderBook, volume, side);
Project Structure
text
apps/frontend/
├── src/
│   ├── components/       # React components
│   │   ├── OrderBook/
│   │   ├── TradeHistory/
│   │   ├── Chart/
│   │   ├── OrderEntry/
│   │   └── Wallet/
│   ├── services/
│   │   ├── api.ts        # REST API calls
│   │   ├── websocket.ts  # WebSocket manager
│   │   └── keplr.ts      # Keplr wallet integration
│   ├── stores/           # Zustand state stores
│   ├── config/
│   │   └── envs.ts       # Environment configuration
│   ├── utils/
│   │   └── index.ts      # Helper functions
│   └── App.tsx           # Main application
├── bin/
│   └── start.sh          # Start script
├── public/
├── index.html
├── package.json
├── vite.config.ts
└── tsconfig.json
State Management (Zustand)
The app uses Zustand for state management:

typescript
// Example store
import { create } from 'zustand';

interface TradingStore {
  orderBook: OrderBook;
  trades: Trade[];
  userOrders: Order[];
  setOrderBook: (orderBook: OrderBook) => void;
  addTrade: (trade: Trade) => void;
  updateOrder: (order: Order) => void;
}

const useTradingStore = create<TradingStore>((set) => ({
  orderBook: { bids: [], asks: [] },
  trades: [],
  userOrders: [],
  setOrderBook: (orderBook) => set({ orderBook }),
  addTrade: (trade) => set((state) => ({ 
    trades: [trade, ...state.trades].slice(0, 100) 
  })),
  updateOrder: (order) => set((state) => ({
    userOrders: state.userOrders.map(o => 
      o.id === order.id ? order : o
    )
  })),
}));
Customization for Your DEX
Step 1: Configure Environment
bash
# Create .env file
echo "VITE_ENV_BASE_API=https://your-api.com" > .env
echo "VITE_ENV_WS=wss://your-api.com/ws" >> .env
echo "VITE_ENV_MODE=production" >> .env
Step 2: Port WebSocket Manager
Copy services/websocket.ts to your project.

Step 3: Port API Service
Copy services/api.ts to your project and adjust endpoints.

Step 4: Customize Components
Modify React components to match your brand and requirements.

Troubleshooting
WebSocket Connection Issues
typescript
// Check connection status
wsManager.connected().then(isConnected => {
  console.log('WebSocket connected:', isConnected);
});

// Monitor connection events
wsManager.on('connect', () => console.log('Connected'));
wsManager.on('disconnect', () => console.log('Disconnected'));
wsManager.on('error', (error) => console.error('WS Error:', error));
API Call Failures
typescript
// Add error handling
try {
  const data = await api.getOrderBook(market);
} catch (error) {
  console.error('API Error:', error);
  // Fallback to cached data or retry logic
}
Environment Variables Not Loading
bash
# Verify env variables are set
echo $VITE_ENV_BASE_API
echo $VITE_ENV_WS

# Restart dev server after env changes
./bin/start.sh
Production Build
bash
# Build for production
npm run build

# Serve production build
npm run preview
Performance Optimization
Area	Recommendation
WebSocket	Batch updates, throttle high-frequency messages
API	Implement caching, pagination
Rendering	Use memo, useCallback for expensive components
State	Keep Zustand stores focused and shallow
Resources
CoreDEX API Guide

Data Aggregator Documentation

Store Documentation

React Documentation

Zustand Documentation

Vite Documentation

text

---

Now update the DEX README to include the UI:

```bash
nano ~/dev/TXdocumentation/dex/README.md
Add this section:

markdown
### UI (Frontend)

The CoreDEX UI is a React-based trading interface with real-time WebSocket updates.

📖 **[UI Documentation](./ui.md)**

Key features:
- Real-time order book visualization
- Trade history and OHLC charts
- Order entry and management
- WebSocket manager for live updates
- Reusable API service layer
- Zustand state management
