k# CoreDEX API

The CoreDEX is a permissionless, fee-free exchange with an organic order book designed for Real-World Assets (RWAs). Build trading interfaces using the CoreDEX API with pre-built extensions for compliance and increased security.

## Overview

| Feature | Description |
|---------|-------------|
| **Quick Setup** | Get started in under 15 minutes with minimal technical overhead |
| **Custom Trading Logic** | Configure trading hours, compliance rules, and asset restrictions with built-in smart contract extensions |
| **Developer Ready API** | Use any language to interact with the API for trade history, order history, OHLC data |

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ CoreDEX Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │ TX Blockchain │────▶│ Data │────▶│ Store │ │
│ │ (Devnet/ │ │ Aggregator │ │ (MySQL) │ │
│ │ Testnet/ │ │ (Scanner) │ │ │ │
│ │ Mainnet) │ └─────────────────┘ └────────┬────────┘ │
│ └─────────────────┘ │ │ │
│ │ │ gRPC │
│ ▼ ▼ │
│ ┌─────────────────┐ ┌─────────────────┐ │
│ │ API Server │◀────│ Store │ │
│ │ (RESTful) │ │ (gRPC) │ │
│ └────────┬────────┘ └─────────────────┘ │
│ │ │
│ │ HTTP/REST │
│ ▼ │
│ ┌─────────────────┐ │
│ │ UI / Clients │ │
│ │ (Frontend) │ │
│ └─────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Core Components

| Component | Description | Scaling |
|-----------|-------------|---------|
| **Data Aggregator** | Blockchain scanner that processes blocks and generates OHLC data | Single instance (restarts where left off) |
| **API Server** | RESTful API providing trade history, orders, OHLC, tickers | Horizontally scalable |
| **Store** | gRPC-based data layer (MySQL implementation) | Replaceable for scaling |
| **UI** | Demo frontend at http://localhost:3000 | Optional |

## API Features

| Feature | Description |
|---------|-------------|
| **Trade History** | Complete historical trade data |
| **Order Tracking** | Real-time order status and history |
| **OHLC Data** | Open/High/Low/Close candlestick data |
| **Tickers** | Current market prices and volumes |
| **Order Entry** | Place and manage orders |
| **Order Execution** | Automated order matching |

## Quick Setup (Localhost)

### Prerequisites

```bash
# Go 1.23 or higher
go version

# MySQL
mysql --version
Database Setup
sql
CREATE DATABASE friendly_dex;
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON friendly_dex.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;
Clone and Start
bash
# Clone repository
git clone https://github.com/tokenize-x/coredex
cd coredex

# Start all components
./bin/start.sh
First Start - Block Sync
On first start, the process scans from block 1. To start from current block:

Stop the data-aggregator

Run SQL to set current height:

sql
UPDATE State SET Content = '{"Height":6618678}' WHERE StateType=1;
Restart data-aggregator

Verify Running Processes
bash
ps -ef | grep "go run"
Expected processes:

data-aggregator - Blockchain scanner

api-server - REST API server

store - gRPC store service

Access Services
Service	URL
UI	http://localhost:3000
API	http://localhost:8080
Swagger	http://localhost:8080/swagger
Docker Compose Setup
Start with Docker Compose
bash
# Edit block height in mysql-init/init-databases.sql first
./bin/start-docker-compose.sh
Stop Docker Compose Environment
bash
# This removes volumes (resets database)
./bin/stop-docker-compose.sh

# Or just shutdown without removing volumes
docker compose down
Kubernetes Deployment
Build Docker Images
bash
docker build -t coreumfoundation/api-server:latest -f Dockerfile.api-server .
docker build -t coreumfoundation/data-aggregator:latest -f Dockerfile.data-aggregator .
docker build -t coreumfoundation/store:latest -f Dockerfile.store .
docker build -t coreumfoundation/frontend:latest -f Dockerfile.frontend .
Sample Kubernetes Deployments
Sample deployment files are located in apps/kubernetes/

Resource Expectations (Single Instance)
Component	CPU	Memory
API Server	1 CPU	128MB
Store	1 CPU	128MB
Data Aggregator	1 CPU	128MB
UI	1 CPU	256MB
Expected throughput: 1000s of parallel requests with single instances

Market Simulator
For demonstration purposes, there is a market simulator in apps/market-simulator/.

bash
# Build market simulator
docker build -t coreumfoundation/market-simulator:latest -f Dockerfile.market-simulator .
⚠️ Warning: The checked-in mnemonics are for demonstration purposes only and should not be used in production.

API Endpoints
Trade History
text
GET /api/v1/trades
Parameter	Type	Description
market	string	Market ID (e.g., "BTC-USD")
limit	int	Number of records (default 100)
offset	int	Pagination offset
Order History
text
GET /api/v1/orders
Parameter	Type	Description
address	string	User's blockchain address
market	string	Market ID
status	string	Order status (open/filled/cancelled)
OHLC Data
text
GET /api/v1/ohlc
Parameter	Type	Description
market	string	Market ID
resolution	string	Timeframe (1m, 5m, 15m, 1h, 4h, 1d)
from	timestamp	Start time
to	timestamp	End time
Tickers
text
GET /api/v1/tickers
GET /api/v1/ticker/{market}
Order Entry
text
POST /api/v1/order
json
{
  "market": "BTC-USD",
  "side": "buy",
  "type": "limit",
  "price": "50000.00",
  "amount": "0.1",
  "address": "core1..."
}
Configuration
Environment Variables
Variable	Description	Default
CHAIN_ID	TX Blockchain network	txchain-devnet-1
RPC_URL	Node RPC endpoint	https://rpc.devnet.tx.dev:443
DB_HOST	MySQL host	localhost
DB_USER	MySQL user	testuser
DB_PASSWORD	MySQL password	password
DB_NAME	Database name	friendly_dex
API_PORT	API server port	8080
Troubleshooting
Block Height Not Updating
Error:

text
rpc error for block 1: error in json rpc client. RPC error -32603 - Internal error: 
height 1 is not available, lowest height is 36782260
Solution: Set height manually in database:

sql
INSERT INTO State (StateType, Content, MetaData) 
VALUES (1, '{"Height":36782260}', '{"Network": 3, "UpdatedAt": {"seconds": 1738799304, "nanos": 164479000}}');

-- Or update existing:
UPDATE State SET Content = '{"Height":36782260}' WHERE StateType=1;
MySQL Connection Issues
bash
# Verify MySQL is running
sudo systemctl status mysql

# Test connection
mysql -u testuser -p -h localhost
Port Already in Use
bash
# Check what's using port 8080
lsof -i :8080

# Kill process or change API_PORT
export API_PORT=8081
Production Considerations
Recommended Setup
Use local TX node instead of public node for better performance

Scale API Server horizontally behind load balancer

Use managed MySQL (AWS RDS, Google Cloud SQL) for production

Monitor data-aggregator - ensure it's running continuously

Set up backups for the MySQL database

Performance Tuning
Component	Tuning Options
API Server	Increase replicas, add caching layer
Store	Use connection pooling, read replicas
Data Aggregator	Adjust batch sizes, block processing interval
MySQL	Increase buffer pool, optimize indexes
Resources
CoreDEX GitHub Repository

TX Blockchain Documentation

API Swagger Documentation

DEX Module Documentation

text

---

Now create a DEX README:

```bash
nano ~/dev/TXdocumentation/dex/README.md
Paste this content:

markdown
# CoreDEX - TX Blockchain DEX

The CoreDEX is a permissionless, fee-free exchange built on TX Blockchain, designed specifically for Real-World Assets (RWAs).

## Overview

CoreDEX provides a RESTful API on top of TX Blockchain's integrated DEX, making it easier to build trading interfaces than using the blockchain directly.

## Documentation

| Document | Description |
|----------|-------------|
| [CoreDEX API Guide](./coredex-api.md) | Complete API documentation, setup, and deployment |

## Key Features

- ✅ **Fee-free trading** - No trading fees
- ✅ **Permissionless** - Anyone can trade
- ✅ **Organic order book** - True market discovery
- ✅ **RWA focused** - Built for real-world assets
- ✅ **Compliance ready** - Built-in extensions for regulations
- ✅ **Horizontally scalable** - Handle 1000s of parallel requests

## Quick Links

- [GitHub Repository](https://github.com/tokenize-x/coredex)
- [API Documentation](./coredex-api.md)
- [TX Blockchain Documentation](../README.md)

## Architecture Components
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ TX Chain │───▶│ Data │───▶│ Store │
│ (Source) │ │ Aggregator │ │ (MySQL) │
└─────────────┘ └─────────────┘ └──────┬──────┘
│
▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Clients │◀───│ API │◀───│ Store │
│ (UI/Apps) │ │ Server │ │ (gRPC) │
└─────────────┘ └─────────────┘ └─────────────┘

text

## Getting Started

1. **Prerequisites**: Go 1.23+, MySQL
2. **Clone**: `git clone https://github.com/tokenize-x/coredex`
3. **Setup DB**: Create database and user
4. **Run**: `./bin/start.sh`
5. **Access**: http://localhost:3000 (UI) or http://localhost:8080 (API)

For detailed instructions, see the [CoreDEX API Guide](./coredex-api.md).

