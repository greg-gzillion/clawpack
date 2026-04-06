# Order Service (Order Proto)

The order.proto file defines the data structures for tracking the entire lifecycle of an order, from its creation in a smart contract to its execution by a broker and final settlement. It does not represent a single state of an order, but rather the entire process and its state at any given time.

## Overview

The Order service is a gRPC-based system that tracks:
- Order lifecycle from creation to settlement
- Smart contract order placement and execution
- Broker submission and execution status
- Partial fills and cumulative execution
- Order cancellation and expiration
- Settlement and reconciliation

## Order Lifecycle

The Order message encapsulates the state of an order at any point in time. The `InternalOrderState` enum within the Order message tracks the progress of the order through its lifecycle.

### Lifecycle Stages
┌─────────────────────────────────────────────────────────────────────────────┐
│ ORDER LIFECYCLE │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│ │ Smart │ │ Broker │ │ Smart │ │ Execution │ │
│ │ Contract │───▶│ Submission │───▶│ Contract │───▶│ │ │
│ │ Creation │ │ │ │ Placement │ │ │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ └─────┬──────┘ │
│ │ │
│ ┌──────────────────────────────────────┘ │
│ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│ │ Smart │ │ Order │ │ Complete │ │
│ │ Contract │───▶│ Complete │───▶│ (Final) │ │
│ │ Execution │ │ (Filled) │ │ │ │
│ └──────────────┘ └──────────────┘ └────────────┘ │
│ │
│ ┌──────────────┐ ┌──────────────┐ │
│ │ User │ │ Broker │ │
│ │ Cancellation│───▶│ Cancellation│───▶┌────────────┐ │
│ │ Request │ │ │ │ Cancelled │ │
│ └──────────────┘ └──────────────┘ └────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

### State Transitions

| From State | To State | Trigger |
|------------|----------|---------|
| CREATED | SUBMITTED_TO_BROKER | Order submitted to broker |
| SUBMITTED_TO_BROKER | PLACED_ON_CONTRACT | Order placed on smart contract |
| PLACED_ON_CONTRACT | EXECUTED_ON_CONTRACT | Execution received from broker |
| EXECUTED_ON_CONTRACT | COMPLETED | Order fully filled |
| Any active state | CANCELLED_BY_USER | User cancellation request |
| Any active state | CANCELLED_BY_BROKER | Broker cancellation |

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Trading UI, API, WebSocket, Analytics) │
└───────────────────────────────────┬─────────────────────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Order Service │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Order │ │ Lifecycle │ │ Execution │ │ Settlement │ │
│ │ Management │ │ Tracker │ │ Handler │ │ Engine │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────────────┬─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Storage Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Order Store │ │ Execution │ │ Redis │ │ TimescaleDB │ │
│ │ (PostgreSQL)│ │ Store │ │ (Cache) │ │ (Analytics) │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ External Systems │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Blockchain │ │ Broker │ │ Settlement │ │
│ │ Node │ │ API │ │ System │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Environment Variables

### Required Variables

| Variable | Description | Format | Example |
|----------|-------------|--------|---------|
| `ORDER_STORE` | gRPC endpoint for order store service | `host:port` | `order-store:50068` |
| `ORDER_STORE_TESTING` | Enable test mode with in-memory buffer | `TRUE` | `TRUE` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MAX_ORDERS_PER_USER` | Maximum active orders per user | `100` |
| `ORDER_EXPIRY_HOURS` | Default order expiry in hours | `168` (7 days) |
| `MAX_PARTIAL_FILLS` | Maximum partial fills per order | `1000` |
| `SETTLEMENT_BATCH_SIZE` | Orders per settlement batch | `100` |
| `CACHE_TTL_SECONDS` | Order cache TTL | `300` |

## Proto Definition

```protobuf
syntax = "proto3";

package order.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/any.proto";

// Order Service Definition
service OrderService {
    // Order management
    rpc CreateOrder(CreateOrderRequest) returns (CreateOrderResponse);
    rpc GetOrder(GetOrderRequest) returns (GetOrderResponse);
    rpc GetOrders(GetOrdersRequest) returns (GetOrdersResponse);
    rpc CancelOrder(CancelOrderRequest) returns (CancelOrderResponse);
    rpc ReplaceOrder(ReplaceOrderRequest) returns (ReplaceOrderResponse);
    
    // Order lifecycle updates
    rpc UpdateOrderState(UpdateOrderStateRequest) returns (UpdateOrderStateResponse);
    rpc RecordExecution(RecordExecutionRequest) returns (RecordExecutionResponse);
    rpc RecordPartialFill(RecordPartialFillRequest) returns (RecordPartialFillResponse);
    
    // Broker operations
    rpc SubmitToBroker(SubmitToBrokerRequest) returns (SubmitToBrokerResponse);
    rpc UpdateBrokerStatus(UpdateBrokerStatusRequest) returns (UpdateBrokerStatusResponse);
    
    // Smart contract operations
    rpc RecordContractPlacement(RecordContractPlacementRequest) returns (RecordContractPlacementResponse);
    rpc RecordContractExecution(RecordContractExecutionRequest) returns (RecordContractExecutionResponse);
    
    // Settlement
    rpc SettleOrder(SettleOrderRequest) returns (SettleOrderResponse);
    rpc GetSettlementStatus(GetSettlementStatusRequest) returns (GetSettlementStatusResponse);
    
    // Analytics
    rpc GetOrderHistory(GetOrderHistoryRequest) returns (GetOrderHistoryResponse);
    rpc GetOrderStats(GetOrderStatsRequest) returns (GetOrderStatsResponse);
    rpc StreamOrderUpdates(StreamOrderUpdatesRequest) returns (stream OrderUpdate);
}

// ==================== Core Order Messages ====================

// Internal order state enum - tracks progress through lifecycle
enum InternalOrderState {
    STATE_UNSPECIFIED = 0;
    
    // Initial states
    CREATED = 1;                    // Order created in system
    SUBMITTED_TO_BROKER = 2;        // Sent to broker for execution
    PLACED_ON_CONTRACT = 3;         // Placed on smart contract
    
    // Execution states
    EXECUTING = 4;                  // Being executed (partial fills)
    EXECUTED_ON_CONTRACT = 5;       // Execution recorded on contract
    PARTIALLY_FILLED = 6;           // Partially filled, awaiting more
    
    // Terminal states
    COMPLETED = 7;                  // Fully executed and settled
    CANCELLED_BY_USER = 8;          // Cancelled by user request
    CANCELLED_BY_BROKER = 9;        // Cancelled by broker
    EXPIRED = 10;                   // Order expired
    REJECTED = 11;                  // Rejected by broker or system
    FAILED = 12;                    // Failed during execution
    
    // Settlement states
    PENDING_SETTLEMENT = 13;        // Awaiting settlement
    SETTLED = 14;                   // Successfully settled
    SETTLEMENT_FAILED = 15;         // Settlement failed
}

// Order side (buy/sell)
enum OrderSide {
    SIDE_UNSPECIFIED = 0;
    BUY = 1;
    SELL = 2;
}

// Order type
enum OrderType {
    TYPE_UNSPECIFIED = 0;
    MARKET = 1;                     // Market order
    LIMIT = 2;                      // Limit order
    STOP_MARKET = 3;                // Stop market order
    STOP_LIMIT = 4;                 // Stop limit order
    TRAILING_STOP = 5;              // Trailing stop order
}

// Time in force
enum TimeInForce {
    TIF_UNSPECIFIED = 0;
    GTC = 1;                        // Good 'til cancelled
    IOC = 2;                        // Immediate or cancel
    FOK = 3;                        // Fill or kill
    DAY = 4;                        // Good for day only
}

// Order Instruction - snapshot of order from smart contract
message OrderInstruction {
    string instruction_id = 1;      // Unique instruction ID
    bytes transaction_hash = 2;     // Smart contract transaction hash
    uint64 sequence_number = 3;     // Sequence number on chain
    string asset_pair = 4;          // Trading pair (e.g., "TX/USD")
    OrderSide side = 5;              // Buy or sell
    OrderType order_type = 6;        // Type of order
    string price = 7;               // Limit price (string for precision)
    string original_quantity = 8;   // Original order quantity
    string remaining_quantity = 9;  // Remaining unfilled quantity
    TimeInForce time_in_force = 10;  // Time in force
    uint64 expiry_timestamp = 11;    // Expiry timestamp (Unix)
    bytes signer_public_key = 12;    // Signer's public key
    bytes signature = 13;            // Order signature
    google.protobuf.Timestamp created_at = 14;
    map<string, string> metadata = 15;
}

// Broker Order Details - order status at broker
message BrokerOrderDetails {
    string broker_order_id = 1;     // Broker's order ID
    string broker_name = 2;         // Name of broker
    string broker_status = 3;        // Broker-specific status
    string avg_execution_price = 4;  // Average fill price
    string executed_quantity = 5;    // Quantity executed by broker
    string remaining_quantity = 6;   // Quantity remaining
    repeated Execution executions = 7; // Individual executions
    google.protobuf.Timestamp submitted_at = 8;
    google.protobuf.Timestamp last_update = 9;
    map<string, string> broker_metadata = 10;
}

// Individual execution/fill
message Execution {
    string execution_id = 1;        // Unique execution ID
    string broker_execution_id = 2; // Broker's execution reference
    bytes transaction_hash = 3;      // Smart contract transaction
    string price = 4;               // Execution price
    string quantity = 5;            // Quantity filled
    string total_value = 6;          // Price * Quantity
    string fee = 7;                 // Execution fee
    string fee_asset = 8;           // Fee currency
    google.protobuf.Timestamp executed_at = 9;
    uint64 sequence_number = 10;     // On-chain sequence
    map<string, string> metadata = 11;
}

// Settlement details
message Settlement {
    string settlement_id = 1;       // Unique settlement ID
    string settlement_tx_hash = 2;  // Settlement transaction
    string settled_amount = 3;      // Amount settled
    string settlement_asset = 4;    // Asset used for settlement
    string status = 5;              // pending, completed, failed
    google.protobuf.Timestamp requested_at = 6;
    google.protobuf.Timestamp completed_at = 7;
    string failure_reason = 8;
}

// Main Order message - encapsulates complete order state
message Order {
    // Core identifiers
    string order_id = 1;            // Unique order ID (UUID)
    string client_order_id = 2;      // Client-provided ID
    string user_id = 3;              // User who placed order
    string organization_id = 4;      // Organization context
    
    // Order details
    string asset_pair = 5;           // Trading pair
    OrderSide side = 6;              // Buy or sell
    OrderType order_type = 7;        // Order type
    string price = 8;               // Limit price (if applicable)
    string stop_price = 9;          // Stop price (if applicable)
    string original_quantity = 10;   // Original order quantity
    string executed_quantity = 11;   // Total executed quantity
    string remaining_quantity = 12;  // Remaining quantity
    string average_price = 13;       // Average execution price
    TimeInForce time_in_force = 14;  // Time in force
    uint64 expiry_timestamp = 15;    // Expiry time (Unix)
    
    // State tracking
    InternalOrderState state = 16;   // Current lifecycle state
    string status_reason = 17;       // Reason for current state
    
    // Execution details
    repeated Execution executions = 18; // All executions/fills
    int32 partial_fill_count = 19;   // Number of partial fills
    string total_fees = 20;          // Total fees paid
    string total_value_executed = 21; // Total value of executions
    
    // Smart contract data
    OrderInstruction contract_instruction = 22;
    string contract_order_id = 23;   // Order ID on contract
    
    // Broker data
    BrokerOrderDetails broker_details = 24;
    
    // Settlement data
    Settlement settlement = 25;
    
    // Timestamps
    google.protobuf.Timestamp created_at = 26;
    google.protobuf.Timestamp submitted_at = 27;
    google.protobuf.Timestamp placed_on_contract_at = 28;
    google.protobuf.Timestamp first_execution_at = 29;
    google.protobuf.Timestamp last_execution_at = 30;
    google.protobuf.Timestamp completed_at = 31;
    google.protobuf.Timestamp cancelled_at = 32;
    google.protobuf.Timestamp updated_at = 33;
    
    // Additional data
    string trigger_price = 34;       // Trigger price for stop orders
    bool is_maker = 35;              // Whether order provided liquidity
    map<string, string> metadata = 36;
    repeated string tags = 37;       // User-defined tags
}

// ==================== Request/Response Messages ====================

message CreateOrderRequest {
    string client_order_id = 1;      // Client-provided ID (optional)
    string user_id = 2;
    string asset_pair = 3;
    OrderSide side = 4;
    OrderType order_type = 5;
    string price = 6;               // Required for limit orders
    string stop_price = 7;          // Required for stop orders
    string quantity = 8;
    TimeInForce time_in_force = 9;
    uint64 expiry_timestamp = 10;    // Optional expiry
    string organization_id = 11;
    map<string, string> metadata = 12;
    repeated string tags = 13;
}

message CreateOrderResponse {
    Order order = 1;
    bool created = 2;
    string message = 3;
}

message GetOrderRequest {
    string order_id = 1;
    string client_order_id = 2;      // Alternative lookup
    string user_id = 3;              // Required for authorization
    string organization_id = 4;
    bool include_executions = 5;     // Include full execution details
}

message GetOrderResponse {
    Order order = 1;
    bool found = 2;
}

message GetOrdersRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_pair = 3;           // Filter by pair
    OrderSide side = 4;              // Filter by side
    repeated InternalOrderState states = 5; // Filter by states
    google.protobuf.Timestamp from_date = 6;
    google.protobuf.Timestamp to_date = 7;
    int32 limit = 8;
    int32 offset = 9;
    string sort_by = 10;             // created_at, updated_at, executed_quantity
    string sort_order = 11;          // asc, desc
}

message GetOrdersResponse {
    repeated Order orders = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

message CancelOrderRequest {
    string order_id = 1;
    string user_id = 2;
    string organization_id = 3;
    string reason = 4;               // Reason for cancellation
}

message CancelOrderResponse {
    bool success = 1;
    Order order = 2;
    string message = 3;
}

message ReplaceOrderRequest {
    string order_id = 1;
    string user_id = 2;
    string organization_id = 3;
    optional string new_price = 4;
    optional string new_quantity = 5;
    optional string new_stop_price = 6;
    optional uint64 new_expiry = 7;
    string reason = 8;
}

message ReplaceOrderResponse {
    bool success = 1;
    Order old_order = 2;
    Order new_order = 3;
    string message = 4;
}

// ==================== Lifecycle Update Messages ====================

message UpdateOrderStateRequest {
    string order_id = 1;
    InternalOrderState new_state = 2;
    string user_id = 3;
    string organization_id = 4;
    string reason = 5;
    map<string, string> metadata = 6;
}

message UpdateOrderStateResponse {
    bool success = 1;
    Order order = 2;
}

message RecordExecutionRequest {
    string order_id = 1;
    string price = 2;
    string quantity = 3;
    string fee = 4;
    string fee_asset = 5;
    string broker_execution_id = 6;
    bytes transaction_hash = 7;
    string user_id = 8;
    string organization_id = 9;
    map<string, string> metadata = 10;
}

message RecordExecutionResponse {
    bool success = 1;
    Execution execution = 2;
    Order order = 3;
    bool order_completed = 4;
}

message RecordPartialFillRequest {
    string order_id = 1;
    string price = 2;
    string quantity = 3;
    string remaining_quantity = 4;
    string user_id = 5;
    string organization_id = 6;
}

message RecordPartialFillResponse {
    bool success = 1;
    Order order = 2;
    int32 fill_sequence = 3;
}

// ==================== Broker Operations ====================

message SubmitToBrokerRequest {
    string order_id = 1;
    string broker_name = 2;
    string broker_order_id = 3;      // Pre-assigned or empty
    string user_id = 4;
    string organization_id = 5;
    map<string, string> broker_metadata = 6;
}

message SubmitToBrokerResponse {
    bool success = 1;
    Order order = 2;
    string broker_order_id = 3;
}

message UpdateBrokerStatusRequest {
    string order_id = 1;
    string broker_status = 2;
    string broker_order_id = 3;
    string avg_execution_price = 4;
    string executed_quantity = 5;
    string user_id = 6;
    string organization_id = 7;
}

message UpdateBrokerStatusResponse {
    bool success = 1;
    Order order = 2;
}

// ==================== Smart Contract Operations ====================

message RecordContractPlacementRequest {
    string order_id = 1;
    bytes transaction_hash = 2;
    uint64 sequence_number = 3;
    string contract_order_id = 4;
    string user_id = 5;
    string organization_id = 6;
}

message RecordContractPlacementResponse {
    bool success = 1;
    Order order = 2;
}

message RecordContractExecutionRequest {
    string order_id = 1;
    bytes transaction_hash = 2;
    string price = 3;
    string quantity = 4;
    uint64 sequence_number = 5;
    string user_id = 6;
    string organization_id = 7;
}

message RecordContractExecutionResponse {
    bool success = 1;
    Execution execution = 2;
    Order order = 3;
}

// ==================== Settlement Operations ====================

message SettleOrderRequest {
    string order_id = 1;
    string settlement_asset = 2;
    string user_id = 3;
    string organization_id = 4;
}

message SettleOrderResponse {
    bool success = 1;
    Settlement settlement = 2;
    Order order = 3;
}

message GetSettlementStatusRequest {
    string order_id = 1;
    string user_id = 2;
    string organization_id = 3;
}

message GetSettlementStatusResponse {
    Settlement settlement = 1;
    string status = 2;
}

// ==================== Analytics ====================

message GetOrderHistoryRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_pair = 3;
    google.protobuf.Timestamp from_date = 4;
    google.protobuf.Timestamp to_date = 5;
    string interval = 6;             // hour, day, week, month
    int32 limit = 7;
}

message GetOrderHistoryResponse {
    repeated OrderHistoryEntry history = 1;
    SummaryStats summary = 2;
}

message OrderHistoryEntry {
    google.protobuf.Timestamp timestamp = 1;
    int32 order_count = 2;
    string total_volume = 3;
    string average_price = 4;
    int32 completed_count = 5;
    int32 cancelled_count = 6;
}

message SummaryStats {
    int32 total_orders = 1;
    int32 completed_orders = 2;
    int32 cancelled_orders = 3;
    int32 partially_filled = 4;
    string total_volume = 5;
    string total_fees = 6;
    string average_fill_rate = 7;
    string best_price = 8;
    string worst_price = 9;
}

message GetOrderStatsRequest {
    string organization_id = 1;
    string asset_pair = 2;
    google.protobuf.Timestamp from_date = 3;
    google.protobuf.Timestamp to_date = 4;
}

message GetOrderStatsResponse {
    map<string, AssetStats> asset_stats = 1;
    OverallStats overall = 2;
}

message AssetStats {
    string asset_pair = 1;
    int32 total_orders = 2;
    string buy_volume = 3;
    string sell_volume = 4;
    string total_volume = 5;
    int32 open_orders = 6;
    int32 completed_orders = 7;
    int32 cancelled_orders = 8;
}

message OverallStats {
    int32 total_orders = 1;
    string total_volume = 2;
    string average_order_size = 3;
    double fill_rate = 4;
    int32 active_users = 5;
}

message StreamOrderUpdatesRequest {
    string user_id = 1;
    string organization_id = 2;
    repeated string asset_pairs = 3;
    repeated InternalOrderState states = 4;
}

message OrderUpdate {
    string order_id = 1;
    InternalOrderState previous_state = 2;
    InternalOrderState current_state = 3;
    Order order = 4;
    google.protobuf.Timestamp update_time = 5;
    string update_type = 6;          // creation, execution, cancellation, state_change
}
Building the Required Files
Create the build script:

bash
mkdir -p ~/dev/TXdocumentation/order/bin
nano ~/dev/TXdocumentation/order/bin/build.sh
bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting Order proto build...${NC}"

# Check if proto file exists
if [ ! -f "order.proto" ] && [ ! -f "proto/order.proto" ]; then
    echo -e "${RED}Error: No order.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "order.proto" ]; then
    PROTO_FILE="order.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/order.proto"
    PROTO_PATH="proto"
fi

echo -e "${BLUE}Using proto file: ${PROTO_FILE}${NC}"

# Check for required tools
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        exit 1
    fi
}

check_command protoc
check_command protoc-gen-go
check_command protoc-gen-go-grpc

# Create directories
echo -e "${YELLOW}Creating build directories...${NC}"
mkdir -p build
mkdir -p client/go
mkdir -p client/typescript

# Generate Go files
echo -e "${BLUE}Generating Go protobuf files...${NC}"
protoc \
    --go_out=client/go \
    --go_opt=paths=source_relative \
    --go-grpc_out=client/go \
    --go-grpc_opt=paths=source_relative \
    --proto_path=${PROTO_PATH} \
    ${PROTO_FILE}

# Check for TypeScript project
if [ -f "package.json" ] && [ -f "tsconfig.json" ]; then
    echo -e "${BLUE}TypeScript project detected. Generating TypeScript files...${NC}"
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing npm dependencies...${NC}"
        npm install
    fi
    
    if command -v protoc-gen-ts &> /dev/null; then
        protoc \
            --plugin=protoc-gen-ts=$(which protoc-gen-ts) \
            --ts_out=client/typescript \
            --proto_path=${PROTO_PATH} \
            ${PROTO_FILE}
    fi
    
    if command -v protoc-gen-grpc-web &> /dev/null; then
        protoc \
            --plugin=protoc-gen-grpc-web=$(which protoc-gen-grpc-web) \
            --grpc-web_out=import_style=typescript,mode=grpcwebtext:client/typescript \
            --proto_path=${PROTO_PATH} \
            ${PROTO_FILE}
    fi
    
    echo -e "${GREEN}TypeScript files generated successfully${NC}"
else
    echo -e "${YELLOW}Skipping TypeScript generation (package.json or tsconfig.json not found)${NC}"
fi

# Generate documentation
echo -e "${BLUE}Generating documentation...${NC}"
if command -v protoc-gen-doc &> /dev/null; then
    protoc \
        --doc_out=build \
        --doc_opt=markdown,order-api.md \
        --proto_path=${PROTO_PATH} \
        ${PROTO_FILE}
    echo -e "${GREEN}Documentation generated${NC}"
fi

# Add generated files to git
echo -e "${YELLOW}Adding generated files to git...${NC}"
git add client/go/*.pb.go 2>/dev/null || true
git add client/typescript/*.ts 2>/dev/null || true
git add build/ 2>/dev/null || true

echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}Generated files:${NC}"
echo "  - client/go/order.pb.go"
echo "  - client/go/order_grpc.pb.go"
if [ -f "client/typescript/order.ts" ]; then
    echo "  - client/typescript/order.ts"
fi
echo "  - build/order-api.md"
Make it executable:

bash
chmod +x ~/dev/TXdocumentation/order/bin/build.sh
Client Implementation
Go Client
Create the Go client:

bash
nano ~/dev/TXdocumentation/order/client/go/order_client.go
go
package order

import (
    "context"
    "fmt"
    "log"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/metadata"
    
    orderpb "github.com/sologenic/order/client/go"
)

type OrderClient struct {
    client orderpb.OrderServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new order client
func NewOrderClient(addr string) (*OrderClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("ORDER_STORE_TESTING"); testingMode == "TRUE" {
            return &OrderClient{}, nil
        }
        return nil, fmt.Errorf("ORDER_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to order service: %w", err)
    }
    
    return &OrderClient{
        client: orderpb.NewOrderServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *OrderClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *OrderClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *OrderClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Create a new order
func (c *OrderClient) CreateOrder(ctx context.Context, req *orderpb.CreateOrderRequest) (*orderpb.Order, error) {
    if c.client == nil {
        return mockOrder(req), nil
    }
    
    resp, err := c.client.CreateOrder(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create order failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("order creation failed: %s", resp.Message)
    }
    
    return resp.Order, nil
}

// Get order by ID
func (c *OrderClient) GetOrder(ctx context.Context, orderID, userID, orgID string, includeExecutions bool) (*orderpb.Order, error) {
    if c.client == nil {
        return mockOrderByID(orderID), nil
    }
    
    req := &orderpb.GetOrderRequest{
        OrderId:          orderID,
        UserId:           userID,
        OrganizationId:   orgID,
        IncludeExecutions: includeExecutions,
    }
    
    resp, err := c.client.GetOrder(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get order failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Order, nil
}

// Get user's orders
func (c *OrderClient) GetOrders(ctx context.Context, userID, orgID, assetPair string, states []orderpb.InternalOrderState, limit, offset int32) ([]*orderpb.Order, int32, error) {
    if c.client == nil {
        return []*orderpb.Order{}, 0, nil
    }
    
    req := &orderpb.GetOrdersRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetPair:      assetPair,
        States:         states,
        Limit:          limit,
        Offset:         offset,
        SortBy:         "created_at",
        SortOrder:      "desc",
    }
    
    resp, err := c.client.GetOrders(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("get orders failed: %w", err)
    }
    
    return resp.Orders, resp.TotalCount, nil
}

// Cancel an order
func (c *OrderClient) CancelOrder(ctx context.Context, orderID, userID, orgID, reason string) (*orderpb.Order, error) {
    if c.client == nil {
        return mockCancelledOrder(orderID), nil
    }
    
    req := &orderpb.CancelOrderRequest{
        OrderId:        orderID,
        UserId:         userID,
        OrganizationId: orgID,
        Reason:         reason,
    }
    
    resp, err := c.client.CancelOrder(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("cancel order failed: %w", err)
    }
    
    if !resp.Success {
        return nil, fmt.Errorf("cancellation failed: %s", resp.Message)
    }
    
    return resp.Order, nil
}

// Replace an order (amend price/quantity)
func (c *OrderClient) ReplaceOrder(ctx context.Context, orderID, userID, orgID string, newPrice, newQuantity *string) (*orderpb.Order, *orderpb.Order, error) {
    if c.client == nil {
        return nil, nil, nil
    }
    
    req := &orderpb.ReplaceOrderRequest{
        OrderId:        orderID,
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    if newPrice != nil {
        req.NewPrice = &orderpb.ReplaceOrderRequest_NewPrice{NewPrice: *newPrice}
    }
    if newQuantity != nil {
        req.NewQuantity = &orderpb.ReplaceOrderRequest_NewQuantity{NewQuantity: *newQuantity}
    }
    
    resp, err := c.client.ReplaceOrder(c.getContext(ctx), req)
    if err != nil {
        return nil, nil, fmt.Errorf("replace order failed: %w", err)
    }
    
    if !resp.Success {
        return nil, nil, fmt.Errorf("replacement failed: %s", resp.Message)
    }
    
    return resp.OldOrder, resp.NewOrder, nil
}

// Record execution (broker -> system)
func (c *OrderClient) RecordExecution(ctx context.Context, orderID, price, quantity, fee, feeAsset, brokerExecID, userID, orgID string) (*orderpb.Execution, *orderpb.Order, error) {
    if c.client == nil {
        return nil, nil, nil
    }
    
    req := &orderpb.RecordExecutionRequest{
        OrderId:           orderID,
        Price:             price,
        Quantity:          quantity,
        Fee:               fee,
        FeeAsset:          feeAsset,
        BrokerExecutionId: brokerExecID,
        UserId:            userID,
        OrganizationId:    orgID,
    }
    
    resp, err := c.client.RecordExecution(c.getContext(ctx), req)
    if err != nil {
        return nil, nil, fmt.Errorf("record execution failed: %w", err)
    }
    
    if !resp.Success {
        return nil, nil, fmt.Errorf("execution recording failed")
    }
    
    return resp.Execution, resp.Order, nil
}

// Submit order to broker
func (c *OrderClient) SubmitToBroker(ctx context.Context, orderID, brokerName, userID, orgID string) (string, error) {
    if c.client == nil {
        return "test-broker-id", nil
    }
    
    req := &orderpb.SubmitToBrokerRequest{
        OrderId:        orderID,
        BrokerName:     brokerName,
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.SubmitToBroker(c.getContext(ctx), req)
    if err != nil {
        return "", fmt.Errorf("submit to broker failed: %w", err)
    }
    
    if !resp.Success {
        return "", fmt.Errorf("broker submission failed")
    }
    
    return resp.BrokerOrderId, nil
}

// Record contract placement
func (c *OrderClient) RecordContractPlacement(ctx context.Context, orderID string, txHash []byte, sequenceNum uint64, contractOrderID, userID, orgID string) error {
    if c.client == nil {
        return nil
    }
    
    req := &orderpb.RecordContractPlacementRequest{
        OrderId:         orderID,
        TransactionHash: txHash,
        SequenceNumber:  sequenceNum,
        ContractOrderId: contractOrderID,
        UserId:          userID,
        OrganizationId:  orgID,
    }
    
    resp, err := c.client.RecordContractPlacement(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("record contract placement failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("contract placement recording failed")
    }
    
    return nil
}

// Settle order
func (c *OrderClient) SettleOrder(ctx context.Context, orderID, settlementAsset, userID, orgID string) (*orderpb.Settlement, error) {
    if c.client == nil {
        return &orderpb.Settlement{
            SettlementId: "test-settlement-id",
            Status:       "completed",
        }, nil
    }
    
    req := &orderpb.SettleOrderRequest{
        OrderId:         orderID,
        SettlementAsset: settlementAsset,
        UserId:          userID,
        OrganizationId:  orgID,
    }
    
    resp, err := c.client.SettleOrder(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("settle order failed: %w", err)
    }
    
    if !resp.Success {
        return nil, fmt.Errorf("settlement failed")
    }
    
    return resp.Settlement, nil
}

// Stream order updates (WebSocket/gRPC stream)
func (c *OrderClient) StreamOrderUpdates(ctx context.Context, userID, orgID string, assetPairs []string) (<-chan *orderpb.OrderUpdate, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &orderpb.StreamOrderUpdatesRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetPairs:     assetPairs,
    }
    
    stream, err := c.client.StreamOrderUpdates(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("failed to create stream: %w", err)
    }
    
    updates := make(chan *orderpb.OrderUpdate, 100)
    
    go func() {
        defer close(updates)
        for {
            update, err := stream.Recv()
            if err != nil {
                log.Printf("Stream receive error: %v", err)
                return
            }
            updates <- update
        }
    }()
    
    return updates, nil
}

// Get order history for analytics
func (c *OrderClient) GetOrderHistory(ctx context.Context, userID, orgID, assetPair string, fromDate, toDate time.Time, interval string) (*orderpb.GetOrderHistoryResponse, error) {
    if c.client == nil {
        return &orderpb.GetOrderHistoryResponse{}, nil
    }
    
    req := &orderpb.GetOrderHistoryRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetPair:      assetPair,
        FromDate:       timestampFromTime(fromDate),
        ToDate:         timestampFromTime(toDate),
        Interval:       interval,
        Limit:          100,
    }
    
    resp, err := c.client.GetOrderHistory(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get order history failed: %w", err)
    }
    
    return resp, nil
}

// Mock functions for testing
func mockOrder(req *orderpb.CreateOrderRequest) *orderpb.Order {
    return &orderpb.Order{
        OrderId:          "mock-order-id",
        ClientOrderId:    req.ClientOrderId,
        UserId:           req.UserId,
        AssetPair:        req.AssetPair,
        Side:             req.Side,
        OrderType:        req.OrderType,
        Price:            req.Price,
        OriginalQuantity: req.Quantity,
        RemainingQuantity: req.Quantity,
        State:            orderpb.InternalOrderState_CREATED,
        CreatedAt:        timestampNow(),
    }
}

func mockOrderByID(orderID string) *orderpb.Order {
    return &orderpb.Order{
        OrderId: orderID,
        State:   orderpb.InternalOrderState_CREATED,
    }
}

func mockCancelledOrder(orderID string) *orderpb.Order {
    return &orderpb.Order{
        OrderId:      orderID,
        State:        orderpb.InternalOrderState_CANCELLED_BY_USER,
        CancelledAt:  timestampNow(),
    }
}

func timestampNow() *google_protobuf.Timestamp {
    return &google_protobuf.Timestamp{
        Seconds: time.Now().Unix(),
        Nanos:   int32(time.Now().Nanosecond()),
    }
}

func timestampFromTime(t time.Time) *google_protobuf.Timestamp {
    return &google_protobuf.Timestamp{
        Seconds: t.Unix(),
        Nanos:   int32(t.Nanosecond()),
    }
}

// Example usage
func main() {
    client, err := NewOrderClient("order-store:50068")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    userID := "user-789"
    
    // Create a limit buy order
    createReq := &orderpb.CreateOrderRequest{
        ClientOrderId:    "client-order-001",
        UserId:           userID,
        AssetPair:        "TX/USD",
        Side:             orderpb.OrderSide_BUY,
        OrderType:        orderpb.OrderType_LIMIT,
        Price:            "50.00",
        Quantity:         "100.0",
        TimeInForce:      orderpb.TimeInForce_GTC,
        OrganizationId:   orgID,
        Metadata: map[string]string{
            "strategy": "grid_trading",
        },
    }
    
    order, err := client.CreateOrder(ctx, createReq)
    if err != nil {
        log.Printf("Failed to create order: %v", err)
    } else {
        log.Printf("Order created: %s (state: %v)", order.OrderId, order.State)
        
        // Submit to broker
        brokerOrderID, err := client.SubmitToBroker(ctx, order.OrderId, "sologenic-broker", userID, orgID)
        if err != nil {
            log.Printf("Failed to submit to broker: %v", err)
        } else {
            log.Printf("Submitted to broker: %s", brokerOrderID)
        }
    }
    
    // Record execution (partial fill)
    if order != nil {
        exec, updatedOrder, err := client.RecordExecution(ctx, order.OrderId, "50.00", "25.0", "0.125", "TX", "broker-exec-001", userID, orgID)
        if err != nil {
            log.Printf("Failed to record execution: %v", err)
        } else {
            log.Printf("Execution recorded: %s - %s @ %s", exec.ExecutionId, exec.Quantity, exec.Price)
            log.Printf("Order remaining: %s (state: %v)", updatedOrder.RemainingQuantity, updatedOrder.State)
        }
        
        // Settle order when complete
        if updatedOrder.State == orderpb.InternalOrderState_COMPLETED {
            settlement, err := client.SettleOrder(ctx, order.OrderId, "TX", userID, orgID)
            if err != nil {
                log.Printf("Failed to settle: %v", err)
            } else {
                log.Printf("Settlement: %s - %s", settlement.SettlementId, settlement.Status)
            }
        }
    }
    
    // Get user's active orders
    activeStates := []orderpb.InternalOrderState{
        orderpb.InternalOrderState_CREATED,
        orderpb.InternalOrderState_SUBMITTED_TO_BROKER,
        orderpb.InternalOrderState_PLACED_ON_CONTRACT,
        orderpb.InternalOrderState_EXECUTING,
        orderpb.InternalOrderState_PARTIALLY_FILLED,
    }
    
    orders, total, err := client.GetOrders(ctx, userID, orgID, "TX/USD", activeStates, 20, 0)
    if err != nil {
        log.Printf("Failed to get orders: %v", err)
    } else {
        log.Printf("Found %d active orders (total: %d)", len(orders), total)
        
        for _, o := range orders {
            log.Printf("- Order %s: %s %s %s @ %s (remaining: %s)", 
                o.OrderId, o.Side, o.AssetPair, o.OriginalQuantity, o.Price, o.RemainingQuantity)
        }
    }
}
Docker Compose Example
bash
nano ~/dev/TXdocumentation/order/docker-compose.yml
yaml
version: '3.8'

services:
  order-service:
    image: sologenic/order-service:latest
    environment:
      - ORDER_SERVICE_PORT=50068
      - ORDER_STORE=order-store:50068
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=orders
      - POSTGRES_USER=order_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - TIMESCALEDB_HOST=timescaledb
      - TIMESCALEDB_PORT=5432
      - TIMESCALEDB_DB=order_history
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - NATS_URL=nats://nats:4222
      - MAX_ORDERS_PER_USER=100
      - ORDER_EXPIRY_HOURS=168
      - SETTLEMENT_BATCH_SIZE=100
      - LOG_LEVEL=info
    ports:
      - "50068:50068"
    networks:
      - internal
    depends_on:
      - postgres
      - timescaledb
      - redis
      - nats
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50068"]
      interval: 30s
      timeout: 10s
      retries: 3

  order-store:
    image: sologenic/order-store:latest
    environment:
      - ORDER_STORE_PORT=50069
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=orders
      - POSTGRES_USER=order_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50069:50069"
    networks:
      - internal
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=orders
      - POSTGRES_USER=order_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U order_user -d orders"]
      interval: 10s
      timeout: 5s
      retries: 5

  timescaledb:
    image: timescale/timescaledb:latest-pg15
    environment:
      - POSTGRES_DB=order_history
      - POSTGRES_USER=order_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - timescaledb_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U order_user -d order_history"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - internal
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  nats:
    image: nats:2.10-alpine
    command: -js
    ports:
      - "4222:4222"
    networks:
      - internal
    healthcheck:
      test: ["CMD", "nats-server", "--help"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  internal:
    driver: bridge

volumes:
  postgres_data:
  timescaledb_data:
  redis_data:
Environment Setup (.env file)
bash
nano ~/dev/TXdocumentation/order/.env
bash
# Database Configuration
DB_PASSWORD=your_secure_password

# Service Configuration
ORDER_STORE=order-store:50069
ORDER_STORE_TESTING=FALSE

# Business Rules
MAX_ORDERS_PER_USER=100
ORDER_EXPIRY_HOURS=168
MAX_PARTIAL_FILLS=1000
SETTLEMENT_BATCH_SIZE=100

# Cache Configuration
CACHE_TTL_SECONDS=300

# Logging
LOG_LEVEL=info
Database Schema (Reference)
sql
-- Orders table
CREATE TABLE orders (
    order_id UUID PRIMARY KEY,
    client_order_id VARCHAR(100),
    user_id VARCHAR(100) NOT NULL,
    organization_id VARCHAR(100),
    asset_pair VARCHAR(50) NOT NULL,
    side VARCHAR(10) NOT NULL,
    order_type VARCHAR(20) NOT NULL,
    price DECIMAL(40,18),
    original_quantity DECIMAL(40,18) NOT NULL,
    executed_quantity DECIMAL(40,18) DEFAULT 0,
    remaining_quantity DECIMAL(40,18) NOT NULL,
    average_price DECIMAL(40,18),
    time_in_force VARCHAR(10),
    state VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    INDEX idx_user_state (user_id, state),
    INDEX idx_asset_pair (asset_pair)
);

-- Executions table
CREATE TABLE executions (
    execution_id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(order_id),
    price DECIMAL(40,18) NOT NULL,
    quantity DECIMAL(40,18) NOT NULL,
    fee DECIMAL(40,18),
    fee_asset VARCHAR(20),
    executed_at TIMESTAMP NOT NULL,
    transaction_hash BYTEA,
    INDEX idx_order (order_id)
);

-- Order history hypertable (TimescaleDB)
CREATE TABLE order_history (
    order_id UUID,
    user_id VARCHAR(100),
    asset_pair VARCHAR(50),
    state VARCHAR(30),
    price DECIMAL(40,18),
    quantity DECIMAL(40,18),
    recorded_at TIMESTAMPTZ NOT NULL
);

SELECT create_hypertable('order_history', 'recorded_at');
State Transition Validation
go
// Valid state transitions
var validTransitions = map[InternalOrderState][]InternalOrderState{
    CREATED:                    {SUBMITTED_TO_BROKER, CANCELLED_BY_USER, EXPIRED},
    SUBMITTED_TO_BROKER:        {PLACED_ON_CONTRACT, CANCELLED_BY_USER, CANCELLED_BY_BROKER, REJECTED},
    PLACED_ON_CONTRACT:         {EXECUTING, CANCELLED_BY_USER, CANCELLED_BY_BROKER, EXPIRED},
    EXECUTING:                  {EXECUTED_ON_CONTRACT, PARTIALLY_FILLED, CANCELLED_BY_USER, CANCELLED_BY_BROKER},
    PARTIALLY_FILLED:           {EXECUTING, EXECUTED_ON_CONTRACT, CANCELLED_BY_USER, CANCELLED_BY_BROKER},
    EXECUTED_ON_CONTRACT:       {COMPLETED, PENDING_SETTLEMENT, PARTIALLY_FILLED},
    PENDING_SETTLEMENT:         {SETTLED, SETTLEMENT_FAILED},
    // Terminal states (no outgoing transitions)
    COMPLETED:                  {},
    SETTLED:                    {},
    CANCELLED_BY_USER:          {},
    CANCELLED_BY_BROKER:        {},
    EXPIRED:                    {},
    REJECTED:                   {},
    FAILED:                     {},
    SETTLEMENT_FAILED:          {},
}
Error Handling
go
// Example error handling
order, err := client.CreateOrder(ctx, req)
if err != nil {
    if strings.Contains(err.Error(), "INSUFFICIENT_BALANCE") {
        // Handle insufficient funds
    } else if strings.Contains(err.Error(), "INVALID_PRICE") {
        // Handle invalid price
    } else if strings.Contains(err.Error(), "MAX_ORDERS_EXCEEDED") {
        // Handle order limit
    }
    log.Printf("Error: %v", err)
}
License
This documentation is part of the TX Marketplace platform.
