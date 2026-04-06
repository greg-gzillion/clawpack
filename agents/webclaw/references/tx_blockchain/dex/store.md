# CoreDEX Store

The store implementation uses MySQL to persist data. The store is a gRPC server, allowing any other database to be used as a backend. Tables in the store are independent of each other with no merge operations by design, making it easier to scale the store by backing it with multiple databases of the same or different architecture.

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ Store Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ gRPC Server (Port xxxxx) │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ State │ OrderData │ Trade │ OHLC │ │
│ │ Service │ Service │ Service │ Service │ │
│ ├───────────────┼───────────────┼───────────────┼─────────────────────┤ │
│ │ OrderData │ TradePairs │ Currency │ │ │
│ │ History │ Service │ Service │ │ │
│ │ Service │ │ │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ MySQL Database │ │
│ │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐ │ │
│ │ │ State │ │ Orders │ │ Trades │ │ OHLC │ │ Currencies │ │ │
│ │ └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## gRPC Services

The store contains multiple gRPC services, all exposed on the same port:

| Service | Purpose |
|---------|---------|
| **State** | Store and retrieve application state |
| **OrderData** | Store and retrieve active orders |
| **OrderDataHistory** | Store and retrieve order history |
| **Trade** | Store and retrieve trades (executed orders, whole or partial) |
| **TradePairs** | Store and retrieve trade pairs (active markets for dropdowns) |
| **OHLC** | Store and retrieve OHLC (Open/High/Low/Close) data |
| **Currency** | Retrieve denom/currency information |

## Design Principles

### Independent Tables

Tables are independent of each other with **no merge operations by design**. This provides:

- ✅ **Horizontal scalability** - Back with multiple databases
- ✅ **Heterogeneous backends** - Use different database architectures
- ✅ **Simplified scaling** - No complex joins across shards
- ✅ **Independent optimization** - Tune each table separately

### Server Sizing Challenge

Server sizing can be challenging since the overall application can produce high load, dependent on:
- Number of end users
- Trading activity on the blockchain

## Setting Up the Store

### Prerequisites

- MySQL database (5.7+ or 8.0+)
- Database user with read/write access
- Network connectivity between store and API server/data aggregator

### Database Setup

```sql
-- Create database
CREATE DATABASE coredex_store;
USE coredex_store;

-- User will be created automatically by the store on first connection
-- Tables, indexes, and foreign keys are created automatically on first use
Note: All tables, indexes, and foreign keys will be created by the store itself on first use of each entity.

Manual Table Creation (Optional)
If you prefer to create tables manually:

sql
-- State table
CREATE TABLE State (
    StateType INT PRIMARY KEY,
    Content JSON NOT NULL,
    MetaData JSON
);

-- Orders table
CREATE TABLE Orders (
    OrderId VARCHAR(255) PRIMARY KEY,
    Market VARCHAR(100) NOT NULL,
    Side VARCHAR(10) NOT NULL,
    Type VARCHAR(20) NOT NULL,
    Price DECIMAL(40,20) NOT NULL,
    Amount DECIMAL(40,20) NOT NULL,
    Filled DECIMAL(40,20) DEFAULT 0,
    Status VARCHAR(20) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    CreatedAt BIGINT NOT NULL,
    UpdatedAt BIGINT NOT NULL,
    INDEX idx_market (Market),
    INDEX idx_address (Address),
    INDEX idx_status (Status)
);

-- Trades table
CREATE TABLE Trades (
    TradeId VARCHAR(255) PRIMARY KEY,
    OrderId VARCHAR(255) NOT NULL,
    Market VARCHAR(100) NOT NULL,
    Price DECIMAL(40,20) NOT NULL,
    Amount DECIMAL(40,20) NOT NULL,
    Side VARCHAR(10) NOT NULL,
    Address VARCHAR(255) NOT NULL,
    Timestamp BIGINT NOT NULL,
    INDEX idx_order (OrderId),
    INDEX idx_market_timestamp (Market, Timestamp)
);

-- OHLC table
CREATE TABLE OHLC (
    Market VARCHAR(100) NOT NULL,
    Resolution VARCHAR(10) NOT NULL,
    Timestamp BIGINT NOT NULL,
    Open DECIMAL(40,20) NOT NULL,
    High DECIMAL(40,20) NOT NULL,
    Low DECIMAL(40,20) NOT NULL,
    Close DECIMAL(40,20) NOT NULL,
    Volume DECIMAL(40,20) NOT NULL,
    PRIMARY KEY (Market, Resolution, Timestamp)
);

-- TradePairs table
CREATE TABLE TradePairs (
    Market VARCHAR(100) PRIMARY KEY,
    BaseCurrency VARCHAR(50) NOT NULL,
    QuoteCurrency VARCHAR(50) NOT NULL,
    Active BOOLEAN DEFAULT TRUE,
    INDEX idx_active (Active)
);

-- Currencies table
CREATE TABLE Currencies (
    Denom VARCHAR(100) PRIMARY KEY,
    Symbol VARCHAR(50),
    Name VARCHAR(100),
    Decimals INT DEFAULT 6,
    INDEX idx_symbol (Symbol)
);
Start Parameters
Parameter	Description	Required
MYSQL_CONFIG	MySQL connection configuration	✅ Yes
LOG_LEVEL	Log level (debug, info, warn, error)	Optional
GRPC_PORT	Port for gRPC server (format: :port)	✅ Yes
MYSQL_CONFIG Format
The MYSQL_CONFIG follows the mysqlstore connection description format.

Examples:

bash
# Simple format
export MYSQL_CONFIG="user:password@tcp(localhost:3306)/coredex_store"

# With parameters
export MYSQL_CONFIG="user:password@tcp(localhost:3306)/coredex_store?charset=utf8mb4&parseTime=True&loc=Local"

# With socket
export MYSQL_CONFIG="user:password@unix(/var/run/mysqld/mysqld.sock)/coredex_store"
Starting the Store
Command Line
bash
# Set environment variables
export MYSQL_CONFIG="testuser:password@tcp(localhost:3306)/friendly_dex"
export GRPC_PORT=":50051"
export LOG_LEVEL="info"

# Start the store
go run cmd/store/main.go
Docker
bash
docker run -d \
  -e MYSQL_CONFIG="testuser:password@tcp(mysql:3306)/friendly_dex" \
  -e GRPC_PORT=":50051" \
  -e LOG_LEVEL="info" \
  -p 50051:50051 \
  coreumfoundation/store:latest
Docker Compose
yaml
# docker-compose.yml snippet
services:
  store:
    image: coreumfoundation/store:latest
    environment:
      MYSQL_CONFIG: "testuser:password@tcp(mysql:3306)/friendly_dex"
      GRPC_PORT: ":50051"
      LOG_LEVEL: "info"
    ports:
      - "50051:50051"
    depends_on:
      - mysql
  
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: friendly_dex
      MYSQL_USER: testuser
      MYSQL_PASSWORD: password
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
gRPC Service Definitions
State Service
protobuf
service StateService {
    rpc GetState(GetStateRequest) returns (GetStateResponse);
    rpc SetState(SetStateRequest) returns (SetStateResponse);
}

message GetStateRequest {
    int32 state_type = 1;
}

message GetStateResponse {
    string content = 1;
    string metadata = 2;
}
Order Service
protobuf
service OrderDataService {
    rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
    rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
    rpc UpdateOrder(UpdateOrderRequest) returns (UpdateOrderResponse);
    rpc CancelOrder(CancelOrderRequest) returns (CancelOrderResponse);
    rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
}
Trade Service
protobuf
service TradeService {
    rpc RecordTrade(RecordTradeRequest) returns (RecordTradeResponse);
    rpc GetTrades(GetTradesRequest) returns (GetTradesResponse);
    rpc GetTradeHistory(GetTradeHistoryRequest) returns (GetTradeHistoryResponse);
}
OHLC Service
protobuf
service OHLService {
    rpc GetOHLC(GetOHLCRequest) returns (GetOHLCResponse);
    rpc StreamOHLC(StreamOHLCRequest) returns (stream OHLCData);
}

message GetOHLCRequest {
    string market = 1;
    string resolution = 2;
    int64 from = 3;
    int64 to = 4;
}
Scaling Strategies
Horizontal Scaling
Since tables are independent, you can scale by:

Service-based sharding - Different services to different database instances

text
State → DB1
Orders → DB2
Trades → DB3
OHLC → DB4
Market-based sharding - Different markets to different databases

text
BTC-USD → DB1
ETH-USD → DB2
Other markets → DB3
Time-based sharding - Historical data to different databases

text
Recent data (last 30 days) → Fast storage
Historical data → Archive storage
Read Replicas
yaml
# Multiple store instances for read scaling
store-read-1:
  image: coreumfoundation/store:latest
  environment:
    MYSQL_CONFIG: "reader@tcp(mysql-replica1:3306)/friendly_dex"
    
store-read-2:
  image: coreumfoundation/store:latest
  environment:
    MYSQL_CONFIG: "reader@tcp(mysql-replica2:3306)/friendly_dex"
Performance Optimization
Connection Pooling
bash
# MYSQL_CONFIG with connection pool settings
export MYSQL_CONFIG="user:password@tcp(localhost:3306)/db?max_connections=100&max_idle_connections=10&connection_max_lifetime=3600"
Index Recommendations
Table	Recommended Indexes
Orders	(market, status), (address), (created_at)
Trades	(market, timestamp), (order_id)
OHLC	(market, resolution, timestamp) - Primary key
TradePairs	(active)
Query Optimization
sql
-- Optimized order history query
SELECT * FROM Orders 
WHERE address = ? 
  AND status IN ('filled', 'cancelled')
  AND created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY created_at DESC
LIMIT 100;
Monitoring
Health Check
bash
# gRPC health check
grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check

# Store metrics (if enabled)
curl http://localhost:9090/metrics | grep store_
Key Metrics to Monitor
Metric	Description	Alert Threshold
store_query_latency	Query execution time	> 100ms
store_connection_pool_size	Active connections	> 80% of max
store_error_rate	Error rate	> 1%
store_disk_usage	Disk utilization	> 80%
Troubleshooting
Connection Issues
bash
# Test MySQL connection
mysql -u testuser -p -h localhost -e "SELECT 1"

# Check gRPC connectivity
grpcurl -plaintext localhost:50051 list
Table Creation Failures
bash
# Check MySQL privileges
mysql -u testuser -p -e "SHOW GRANTS"

# Verify database exists
mysql -u testuser -p -e "SHOW DATABASES"
Performance Issues
sql
-- Check slow queries
SHOW PROCESSLIST;

-- Analyze table
ANALYZE TABLE Orders;

-- Check index usage
EXPLAIN SELECT * FROM Orders WHERE market = 'BTC-USD';
Configuration Examples
Development Environment
bash
export MYSQL_CONFIG="testuser:password@tcp(localhost:3306)/friendly_dex"
export GRPC_PORT=":50051"
export LOG_LEVEL="debug"
Production Environment
bash
export MYSQL_CONFIG="produser:securepass@tcp(mysql-prod.internal:3306)/friendly_dex?charset=utf8mb4&parseTime=True&max_connections=200"
export GRPC_PORT=":50051"
export LOG_LEVEL="warn"
Kubernetes ConfigMap
yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: store-config
data:
  MYSQL_CONFIG: "storeuser:${MYSQL_PASSWORD}@tcp(mysql-service:3306)/friendly_dex"
  GRPC_PORT: ":50051"
  LOG_LEVEL: "info"
Resources
Data Aggregator Documentation

CoreDEX API Guide

gRPC Documentation

MySQL Documentation

text

---

Now update the DEX README to include the Store:

```bash
nano ~/dev/TXdocumentation/dex/README.md
Add this section:

markdown
### Store

The Store is a gRPC-based persistence layer using MySQL with independent tables for horizontal scaling.

📖 **[Store Documentation](./store.md)**

Key features:
- gRPC server with multiple services (State, Order, Trade, OHLC)
- Independent tables with no merge operations
- Automatic table creation on first use
- Horizontally scalable design
- Connection pooling support
