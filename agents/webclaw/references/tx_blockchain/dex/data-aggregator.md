# CoreDEX Data Aggregator

The Data Aggregator scans blocks near real-time as they are produced by the blockchain. The scan results are per transaction processed by different associated handlers.

## Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Data Aggregator Flow │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│ │ Blockchain │────▶│ Block │────▶│ Transaction│────▶│ Handlers │ │
│ │ (Blocks) │ │ Scanner │ │ Parser │ │ │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────┬─────┘ │
│ │ │
│ ▼ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│ │ Store │◀────│ OHLC │◀────│ Trade │◀────│ Order │ │
│ │ (gRPC) │ │ Generator │ │ Handler │ │ Handler │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Start Parameters

The data aggregator can be started with the following environment variables:

| Parameter | Description | Required |
|-----------|-------------|----------|
| `NETWORKS` | Network config JSON with node endpoints | ✅ Yes |
| `STATE_STORE` | Store connection (host:port) | ✅ Yes |
| `TRADE_STORE` | Store connection (host:port) | ✅ Yes |
| `OHLC_STORE` | Store connection (host:port) | ✅ Yes |
| `ORDER_STORE` | Store connection (host:port) | ✅ Yes |
| `CURRENCY_STORE` | Store connection (host:port) | ✅ Yes |
| `LOG_LEVEL` | Logging level (debug, info, warn, error) | Optional |

## NETWORKS Configuration

The `NETWORKS` env is a JSON that can hold one or more TX nodes, one per network. In most user-facing applications, users will only use mainnet, but for development and testing you can add devnet and testnet nodes.

### Configuration Format

```json
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
Network Configuration Options
Field	Description
Network	Network identifier (devnet, testnet, mainnet)
GRPCHost	gRPC endpoint for blockchain queries
RPCHost	RPC endpoint for blockchain queries
⚠️ Production Note: Using public nodes is not recommended for production. Run your own private nodes for better performance and reliability.

Handlers
The data aggregator processes blockchain data through specialized handlers:

1. Order Handler
Processes order-related transactions:

Order creation

Order cancellation

Order matching

Order status updates

2. Trade Handler
Processes trade transactions:

Trade execution

Trade settlement

Trade history recording

3. OHLC Generator
Generates candlestick data:

Open/High/Low/Close prices

Multiple timeframes (1m, 5m, 15m, 1h, 4h, 1d, 1w)

Volume data

Starting the Data Aggregator
Environment Variables Setup
bash
# Network configuration (single network)
export NETWORKS='{"Node":[{"Network":"devnet","GRPCHost":"grpc.devnet.tx.dev:443","RPCHost":"https://rpc.devnet.tx.dev:443"}]}'

# Multiple networks
export NETWORKS='{
    "Node": [
        {"Network":"devnet","GRPCHost":"grpc.devnet.tx.dev:443","RPCHost":"https://rpc.devnet.tx.dev:443"},
        {"Network":"testnet","GRPCHost":"grpc.testnet.tx.dev:443","RPCHost":"https://rpc.testnet.tx.dev:443"}
    ]
}'

# Store connections
export STATE_STORE="localhost:50051"
export TRADE_STORE="localhost:50051"
export OHLC_STORE="localhost:50051"
export ORDER_STORE="localhost:50051"
export CURRENCY_STORE="localhost:50051"

# Log level (optional)
export LOG_LEVEL="info"

# Start the aggregator
go run cmd/data-aggregator/main.go
Docker Start
bash
docker run -d \
  -e NETWORKS='{"Node":[{"Network":"mainnet","GRPCHost":"grpc.tx.org:443","RPCHost":"https://rpc.tx.org:443"}]}' \
  -e STATE_STORE="store:50051" \
  -e TRADE_STORE="store:50051" \
  -e OHLC_STORE="store:50051" \
  -e ORDER_STORE="store:50051" \
  -e CURRENCY_STORE="store:50051" \
  -e LOG_LEVEL="info" \
  coreumfoundation/data-aggregator:latest
Block Scanning Process
1. Initial Scan
On first start, the aggregator scans from block 1. This can take significant time depending on the blockchain height.

sql
-- Check current scan height
SELECT * FROM State WHERE StateType=1;
2. Real-time Scanning
After catching up, the aggregator scans blocks near real-time as they are produced.

3. State Management
The aggregator maintains state to resume scanning after restarts:

sql
-- State table structure
CREATE TABLE State (
    StateType INT PRIMARY KEY,
    Content JSON,
    MetaData JSON
);

-- Example state record
INSERT INTO State (StateType, Content, MetaData) 
VALUES (1, '{"Height":6618678}', '{"Network": 3, "UpdatedAt": {"seconds": 1738799304, "nanos": 164479000}}');
Currency Scanning
On application start, the data aggregator scans all currencies to ensure they are present in the database. This happens while other goroutines are already running.

Important Note
Depending on the scan speed, it may appear as if the application is hanging. The log will show:

text
BlockHeight as logged is not increasing, channel capacity left is 0
This is not a problem. The application will continue processing once currencies have been scanned.

Testnet Currency Count
Testnet has over 4,000 currencies to process on start, which may cause a noticeable delay.

Performance Monitoring
Key Metrics
Metric	Description
block_height	Current block being processed
channel_capacity	Processing channel buffer
txs_per_second	Transaction throughput
handler_latency	Handler processing time
Monitoring Commands
bash
# Check block progress
curl http://localhost:8080/metrics | grep block_height

# Check channel status
grep "channel capacity" /var/log/data-aggregator.log

# Monitor processing lag
grep "BlockHeight" /var/log/data-aggregator.log | tail -20
Configuration File Example
yaml
# config.yaml
networks:
  - network: "mainnet"
    grpc_host: "grpc.tx.org:443"
    rpc_host: "https://rpc.tx.org:443"
  - network: "testnet"
    grpc_host: "grpc.testnet.tx.dev:443"
    rpc_host: "https://rpc.testnet.tx.dev:443"

store:
  state: "localhost:50051"
  trade: "localhost:50051"
  ohlc: "localhost:50051"
  order: "localhost:50051"
  currency: "localhost:50051"

logging:
  level: "info"
  format: "json"

scanning:
  batch_size: 100
  parallel_workers: 4
  retry_attempts: 3
Troubleshooting
Issue: Block height not increasing
Symptoms:

Log shows same block height repeatedly

Channel capacity shows 0

Possible causes:

Currency scan in progress (especially on testnet)

Network connectivity issues

Store connection problems

Solutions:

bash
# Check currency scan status
grep "currency scan" /var/log/data-aggregator.log

# Verify network connectivity
nc -zv grpc.testnet.tx.dev 443

# Check store connection
grpcurl -plaintext localhost:50051 list
Issue: RPC Error - Height not available
Error:

text
rpc error for block 1: RPC error -32603 - Internal error: 
height 1 is not available, lowest height is 36782260
Solution: Set the state height to the available lowest height:

sql
UPDATE State SET Content = '{"Height":36782260}' WHERE StateType=1;
Issue: High Memory Usage
Solutions:

Reduce batch size

Limit parallel workers

Increase channel buffer or reduce scan frequency

bash
export SCAN_BATCH_SIZE=50
export PARALLEL_WORKERS=2
Production Recommendations
Setting	Recommendation
Network	Run private nodes, not public
Instance Count	Single instance (stateful)
Resources	1 CPU, 128MB memory minimum
Storage	Persistent volume for state
Monitoring	Set up alerts for block lag
Backup	Regular State table backups
Logging Examples
Normal Operation
json
{"level":"info","time":"2025-05-20T15:35:10Z","message":"Starting block scan","height":6618678}
{"level":"info","time":"2025-05-20T15:35:11Z","message":"Processing block","height":6618679,"txs":25}
{"level":"info","time":"2025-05-20T15:35:12Z","message":"Block processed","height":6618679,"duration":"1.2s"}
Currency Scan in Progress
json
{"level":"info","time":"2025-05-20T15:35:10Z","message":"Scanning currencies","total":4234}
{"level":"warn","time":"2025-05-20T15:35:15Z","message":"BlockHeight not increasing","channel_capacity":0}
Error Condition
json
{"level":"error","time":"2025-05-20T15:35:10Z","message":"RPC error","error":"height 1 is not available","lowest_height":36782260}
Resources
CoreDEX API Guide

DEX Overview

TX Blockchain RPC Documentation

text

---

Now update the DEX README to include the Data Aggregator:

```bash
nano ~/dev/TXdocumentation/dex/README.md
Add this section:

markdown
## Components

### Data Aggregator

The Data Aggregator scans blocks in near real-time and processes transactions through specialized handlers.

📖 **[Data Aggregator Documentation](./data-aggregator.md)**

Key features:
- Real-time block scanning
- Multi-network support (devnet, testnet, mainnet)
- Handlers for orders, trades, and OHLC data
- Resumable state management
- Currency scanning on startup

