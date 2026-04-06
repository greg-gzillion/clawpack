# Trade Service (Trade Proto)

The Trade proto provides all the functionality required to interact with the trade store. The Trade model was initially designed to represent an executed order. However, with the introduction of the ActivityType enum, the definition of a Trade has expanded to become more of a **Transaction**.

## Overview

The Trade service is a gRPC-based system that handles:
- Executed trades (buys and sells)
- Deposits and withdrawals
- Dividends and distributions
- Transfers between accounts
- Fee payments and rebates
- Staking rewards
- Airdrops and bonuses
- System adjustments

### Key Concept

Since wallets hold tokenized assets, we can treat inflow activities (e.g., deposits, dividends, received) as **"buys"** and outflow activities (e.g., withdrawals, sent) as **"sells"**. This unified approach allows for consistent accounting across all transaction types.

## Activity Types

```protobuf
enum ActivityType {
    ACTIVITY_TYPE_UNSPECIFIED = 0;
    
    // Trading activities
    TRADE_BUY = 1;              // Market/limit buy execution
    TRADE_SELL = 2;             // Market/limit sell execution
    
    // Transfer activities
    DEPOSIT = 3;                // Asset deposit
    WITHDRAWAL = 4;             // Asset withdrawal
    TRANSFER_SENT = 5;          // Transfer to another user
    TRANSFER_RECEIVED = 6;      // Transfer from another user
    
    // Earnings activities
    DIVIDEND = 7;               // Dividend payment
    STAKING_REWARD = 8;         // Staking reward
    INTEREST = 9;               // Interest earned
    REBATE = 10;                // Fee rebate
    
    // Fee activities
    FEE = 11;                   // Transaction fee
    GAS_FEE = 12;               // Blockchain gas fee
    
    // Corporate actions
    AIRDROP = 13;               // Airdrop received
    BONUS = 14;                 // Bonus credit
    ADJUSTMENT = 15;            // System adjustment
    
    // Settlement activities
    SETTLEMENT_IN = 16;         // Settlement inbound
    SETTLEMENT_OUT = 17;        // Settlement outbound
    
    // Lock/Unlock activities
    LOCK = 18;                  // Asset lock (vesting/staking)
    UNLOCK = 19;                // Asset unlock
}
Architecture
text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Client Applications                                                          │
│ (Trading UI, Reports, Analytics, Accounting, Tax, Portfolio)                 │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │ gRPC
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Trade Service                                                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│ │ Trade       │ │ Activity    │ │ Settlement  │ │ Report      │              │
│ │ Management  │ │ Tracker     │ │ Engine      │ │ Generator   │              │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘              │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Storage Layer                                                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐              │
│ │ Trade Store │ │ TimescaleDB │ │ Redis Cache │ │ ClickHouse  │              │
│ │ (PostgreSQL)│ │ (Historical)│ │             │ │ (Analytics) │              │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
Environment Variables
Required Variables
Variable	Description	Format	Example
TRADE_STORE	gRPC endpoint for trade store service	host:port	trade-store:50072
TRADE_STORE_TESTING	Enable test mode with in-memory buffer	TRUE	TRUE
Optional Variables
Variable	Description	Default
MAX_TRADES_PER_QUERY	Maximum trades per query	1000
TRADE_RETENTION_DAYS	Trade record retention in days	2555 (7 years)
REPORT_BATCH_SIZE	Trades per report batch	10000
CACHE_TTL_SECONDS	Trade cache TTL	300
ENABLE_REAL_TIME_STREAMING	Enable trade streaming	true
Proto Definition
protobuf
syntax = "proto3";

package trade.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/struct.proto";

// Trade Service Definition
service TradeService {
    // Trade CRUD operations
    rpc CreateTrade(CreateTradeRequest) returns (CreateTradeResponse);
    rpc GetTrade(GetTradeRequest) returns (GetTradeResponse);
    rpc GetTrades(GetTradesRequest) returns (GetTradesResponse);
    
    // Activity recording
    rpc RecordActivity(RecordActivityRequest) returns (RecordActivityResponse);
    rpc RecordDeposit(RecordDepositRequest) returns (RecordDepositResponse);
    rpc RecordWithdrawal(RecordWithdrawalRequest) returns (RecordWithdrawalResponse);
    rpc RecordTransfer(RecordTransferRequest) returns (RecordTransferResponse);
    rpc RecordDividend(RecordDividendRequest) returns (RecordDividendResponse);
    rpc RecordStakingReward(RecordStakingRewardRequest) returns (RecordStakingRewardResponse);
    rpc RecordFee(RecordFeeRequest) returns (RecordFeeResponse);
    
    // Trade execution
    rpc ExecuteTrade(ExecuteTradeRequest) returns (ExecuteTradeResponse);
    rpc BatchExecuteTrades(BatchExecuteTradesRequest) returns (BatchExecuteTradesResponse);
    
    // Reporting and analytics
    rpc GetTradeHistory(GetTradeHistoryRequest) returns (GetTradeHistoryResponse);
    rpc GetTradeSummary(GetTradeSummaryRequest) returns (GetTradeSummaryResponse);
    rpc GetVolumeReport(GetVolumeReportRequest) returns (GetVolumeReportResponse);
    rpc GetCapitalGainsReport(GetCapitalGainsReportRequest) returns (GetCapitalGainsReportResponse);
    
    // Streaming
    rpc StreamTrades(StreamTradesRequest) returns (stream Trade);
    rpc GetRealTimeStats(GetRealTimeStatsRequest) returns (stream TradeStats);
    
    // Reconciliation
    rpc ReconcileTrades(ReconcileTradesRequest) returns (ReconcileTradesResponse);
    rpc GetReconciliationStatus(GetReconciliationStatusRequest) returns (GetReconciliationStatusResponse);
}

// ==================== Core Trade Messages ====================

// Activity type enum - expanded to include all transaction types
enum ActivityType {
    ACTIVITY_TYPE_UNSPECIFIED = 0;
    
    // Trading activities
    TRADE_BUY = 1;              // Market/limit buy execution
    TRADE_SELL = 2;             // Market/limit sell execution
    
    // Transfer activities
    DEPOSIT = 3;                // Asset deposit
    WITHDRAWAL = 4;             // Asset withdrawal
    TRANSFER_SENT = 5;          // Transfer to another user
    TRANSFER_RECEIVED = 6;      // Transfer from another user
    
    // Earnings activities
    DIVIDEND = 7;               // Dividend payment
    STAKING_REWARD = 8;         // Staking reward
    INTEREST = 9;               // Interest earned
    REBATE = 10;                // Fee rebate
    
    // Fee activities
    FEE = 11;                   // Transaction fee
    GAS_FEE = 12;               // Blockchain gas fee
    
    // Corporate actions
    AIRDROP = 13;               // Airdrop received
    BONUS = 14;                 // Bonus credit
    ADJUSTMENT = 15;            // System adjustment
    
    // Settlement activities
    SETTLEMENT_IN = 16;         // Settlement inbound
    SETTLEMENT_OUT = 17;        // Settlement outbound
    
    // Lock/Unlock activities
    LOCK = 18;                  // Asset lock (vesting/staking)
    UNLOCK = 19;                // Asset unlock
}

// Trade status
enum TradeStatus {
    TRADE_STATUS_UNSPECIFIED = 0;
    PENDING = 1;                // Pending processing
    COMPLETED = 2;              // Successfully completed
    FAILED = 3;                 // Failed
    REVERSED = 4;               // Reversed/rolled back
    RECONCILED = 5;             // Reconciled with external system
}

// Main Trade message - represents any financial activity
message Trade {
    string trade_id = 1;                // Unique trade ID
    string transaction_hash = 2;        // Blockchain transaction hash
    string order_id = 3;                // Associated order ID (if any)
    
    // Participants
    string user_id = 4;                 // User who performed the activity
    string counterparty_id = 5;         // Other party (if applicable)
    string organization_id = 6;         // Organization context
    
    // Activity details
    ActivityType activity_type = 7;     // Type of activity
    TradeStatus status = 8;             // Current status
    
    // Asset details
    string asset_id = 9;                // Asset ID (e.g., "TX", "USD")
    string asset_symbol = 10;           // Asset symbol
    string amount = 11;                 // Amount (string for precision)
    string price = 12;                  // Price per unit (if applicable)
    string total_value = 13;            // Total value (amount * price)
    
    // Fee details
    string fee_amount = 14;             // Fee paid
    string fee_asset = 15;              // Fee currency
    string gas_fee = 16;                // Blockchain gas fee
    
    // Reference tracking
    string reference_id = 17;           // External reference ID
    string reference_type = 18;         // Type of reference (order, deposit, etc.)
    
    // Timestamps
    google.protobuf.Timestamp executed_at = 19;
    google.protobuf.Timestamp recorded_at = 20;
    google.protobuf.Timestamp settled_at = 21;
    
    // Additional data
    string memo = 22;                   // User-provided memo
    map<string, string> metadata = 23;  // Custom metadata
    repeated string tags = 24;          // Searchable tags
    
    // Cost basis for tax purposes
    string cost_basis = 25;             // Cost basis (for sells)
    string realized_gain = 26;          // Realized gain/loss
    
    // Blockchain confirmation
    int32 confirmations = 27;           // Number of confirmations
    string block_hash = 28;             // Block hash
    uint64 block_number = 29;           // Block number
}

// ==================== Request/Response Messages ====================

message CreateTradeRequest {
    string user_id = 1;
    string organization_id = 2;
    ActivityType activity_type = 3;
    string asset_id = 4;
    string asset_symbol = 5;
    string amount = 6;
    string price = 7;                   // Optional for non-trade activities
    string fee_amount = 8;
    string fee_asset = 9;
    string reference_id = 10;
    string reference_type = 11;
    string memo = 12;
    map<string, string> metadata = 13;
    repeated string tags = 14;
    string counterparty_id = 15;        // For transfers
    string order_id = 16;               // Associated order
}

message CreateTradeResponse {
    Trade trade = 1;
    bool created = 2;
    string message = 3;
}

message GetTradeRequest {
    string trade_id = 1;
    string transaction_hash = 2;        // Alternative lookup
    string user_id = 3;
    string organization_id = 4;
}

message GetTradeResponse {
    Trade trade = 1;
    bool found = 2;
}

message GetTradesRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_id = 3;                // Filter by asset
    ActivityType activity_type = 4;     // Filter by type
    TradeStatus status = 5;             // Filter by status
    google.protobuf.Timestamp from_date = 6;
    google.protobuf.Timestamp to_date = 7;
    int32 limit = 8;
    int32 offset = 9;
    string sort_by = 10;                // executed_at, amount, total_value
    string sort_order = 11;             // asc, desc
}

message GetTradesResponse {
    repeated Trade trades = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

// ==================== Activity Recording ====================

message RecordActivityRequest {
    string user_id = 1;
    string organization_id = 2;
    ActivityType activity_type = 3;
    string asset_id = 4;
    string amount = 5;
    string reference_id = 6;
    string memo = 7;
    map<string, string> metadata = 8;
}

message RecordActivityResponse {
    Trade trade = 1;
    bool recorded = 2;
    string message = 3;
}

message RecordDepositRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_id = 3;
    string amount = 4;
    string transaction_hash = 5;
    string source_address = 6;
    string memo = 7;
}

message RecordDepositResponse {
    Trade trade = 1;
    bool recorded = 2;
    string message = 3;
}

message RecordWithdrawalRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_id = 3;
    string amount = 4;
    string destination_address = 5;
    string fee_amount = 6;
    string memo = 7;
}

message RecordWithdrawalResponse {
    Trade trade = 1;
    bool recorded = 2;
    string message = 3;
}

message RecordTransferRequest {
    string from_user_id = 1;
    string to_user_id = 2;
    string organization_id = 3;
    string asset_id = 4;
    string amount = 5;
    string reference_id = 6;
    string memo = 7;
}

message RecordTransferResponse {
    Trade sent_trade = 1;
    Trade received_trade = 2;
    bool recorded = 3;
    string message = 4;
}

message RecordDividendRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_id = 3;
    string amount = 4;
    string dividend_type = 5;           // cash, stock
    string reference_id = 6;
}

message RecordDividendResponse {
    Trade trade = 1;
    bool recorded = 2;
}

message RecordStakingRewardRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_id = 3;
    string amount = 4;
    string validator = 5;
    uint64 epoch_number = 6;
}

message RecordStakingRewardResponse {
    Trade trade = 1;
    bool recorded = 2;
}

message RecordFeeRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_id = 3;
    string amount = 4;
    string fee_type = 5;                // trading, withdrawal, gas
    string reference_id = 6;
}

message RecordFeeResponse {
    Trade trade = 1;
    bool recorded = 2;
}

// ==================== Trade Execution ====================

message ExecuteTradeRequest {
    string order_id = 1;
    string user_id = 2;
    string organization_id = 3;
    string asset_pair = 4;
    string side = 5;                    // buy or sell
    string price = 6;
    string quantity = 7;
    string fee_amount = 8;
    string fee_asset = 9;
    string transaction_hash = 10;
}

message ExecuteTradeResponse {
    Trade trade = 1;
    bool executed = 2;
    string message = 3;
}

message BatchExecuteTradesRequest {
    repeated ExecuteTradeRequest trades = 1;
    string organization_id = 2;
}

message BatchExecuteTradesResponse {
    repeated Trade trades = 1;
    int32 successful_count = 2;
    int32 failed_count = 3;
    string message = 4;
}

// ==================== Reporting and Analytics ====================

message GetTradeHistoryRequest {
    string user_id = 1;
    string organization_id = 2;
    google.protobuf.Timestamp from_date = 3;
    google.protobuf.Timestamp to_date = 4;
    string interval = 5;                // day, week, month, quarter, year
    bool group_by_asset = 6;
    bool group_by_type = 7;
}

message GetTradeHistoryResponse {
    repeated TradeHistoryEntry history = 1;
    TradeSummary summary = 2;
}

message TradeHistoryEntry {
    google.protobuf.Timestamp period = 1;
    string total_volume = 2;
    int32 trade_count = 3;
    map<string, string> volume_by_asset = 4;
    map<string, int32> count_by_type = 5;
    string total_fees = 6;
}

message TradeSummary {
    string total_volume = 1;
    int32 total_trades = 2;
    string total_deposits = 3;
    string total_withdrawals = 4;
    string total_fees_paid = 5;
    string net_flow = 6;
    string best_price = 7;
    string worst_price = 8;
    string average_price = 9;
    int32 unique_assets = 10;
}

message GetTradeSummaryRequest {
    string user_id = 1;
    string organization_id = 2;
    google.protobuf.Timestamp from_date = 3;
    google.protobuf.Timestamp to_date = 4;
}

message GetTradeSummaryResponse {
    TradeSummary summary = 1;
    map<string, AssetTradeSummary> asset_summaries = 2;
}

message AssetTradeSummary {
    string asset_symbol = 1;
    string buy_volume = 2;
    string sell_volume = 3;
    string net_volume = 4;
    int32 buy_count = 5;
    int32 sell_count = 6;
    string average_buy_price = 7;
    string average_sell_price = 8;
    string total_fees = 9;
}

message GetVolumeReportRequest {
    string organization_id = 1;
    google.protobuf.Timestamp from_date = 2;
    google.protobuf.Timestamp to_date = 3;
    string group_by = 4;                // hour, day, week, month
    string asset_id = 5;                // Optional filter
}

message GetVolumeReportResponse {
    repeated VolumeEntry volumes = 1;
    string total_volume = 2;
    int32 total_transactions = 3;
}

message VolumeEntry {
    google.protobuf.Timestamp timestamp = 1;
    string volume = 2;
    int32 transaction_count = 3;
    string average_trade_size = 4;
}

message GetCapitalGainsReportRequest {
    string user_id = 1;
    string organization_id = 2;
    int32 tax_year = 3;
    string calculation_method = 4;      // fifo, lifo, specific
}

message GetCapitalGainsReportResponse {
    string report_id = 1;
    string download_url = 2;
    string total_short_term_gain = 3;
    string total_long_term_gain = 4;
    string total_realized_gain = 5;
    int32 total_trades = 6;
    repeated CapitalGainsEntry gains = 7;
}

message CapitalGainsEntry {
    string trade_id = 1;
    string asset_symbol = 2;
    string sell_date = 3;
    string sell_price = 4;
    string sell_amount = 5;
    string cost_basis = 6;
    string gain_loss = 7;
    string holding_period = 8;          // short_term, long_term
}

// ==================== Streaming ====================

message StreamTradesRequest {
    string user_id = 1;
    string organization_id = 2;
    repeated string asset_ids = 3;
    repeated ActivityType activity_types = 4;
}

message TradeStats {
    string total_volume_24h = 1;
    int32 total_trades_24h = 2;
    string average_trade_size = 3;
    string top_asset = 4;
    int32 active_users = 5;
    google.protobuf.Timestamp timestamp = 6;
}

message GetRealTimeStatsRequest {
    string organization_id = 1;
}

// ==================== Reconciliation ====================

message ReconcileTradesRequest {
    string organization_id = 1;
    google.protobuf.Timestamp from_date = 2;
    google.protobuf.Timestamp to_date = 3;
    string external_source = 4;         // blockchain, broker, exchange
    bool auto_correct = 5;
}

message ReconcileTradesResponse {
    string reconciliation_id = 1;
    int32 total_trades = 2;
    int32 matched_trades = 3;
    int32 mismatched_trades = 4;
    int32 missing_trades = 5;
    int32 corrections_made = 6;
    string message = 7;
}

message GetReconciliationStatusRequest {
    string reconciliation_id = 1;
    string organization_id = 2;
}

message GetReconciliationStatusResponse {
    string status = 1;                  // pending, in_progress, completed, failed
    int32 total_processed = 2;
    int32 total_to_process = 3;
    double completion_percentage = 4;
    google.protobuf.Timestamp started_at = 5;
    google.protobuf.Timestamp completed_at = 6;
}
Save the file:

Ctrl+O (WriteOut)

Enter (confirm)

Ctrl+X (exit)

2. Trade Build Script
bash
mkdir -p ~/dev/TXdocumentation/trade/bin
nano ~/dev/TXdocumentation/trade/bin/build.sh
bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting Trade proto build...${NC}"

# Check if proto file exists
if [ ! -f "trade.proto" ] && [ ! -f "proto/trade.proto" ]; then
    echo -e "${RED}Error: No trade.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "trade.proto" ]; then
    PROTO_FILE="trade.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/trade.proto"
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
        --doc_opt=markdown,trade-api.md \
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
echo "  - client/go/trade.pb.go"
echo "  - client/go/trade_grpc.pb.go"
if [ -f "client/typescript/trade.ts" ]; then
    echo "  - client/typescript/trade.ts"
fi
echo "  - build/trade-api.md"
Save and make executable:

Ctrl+O, Enter, Ctrl+X

Then run: chmod +x ~/dev/TXdocumentation/trade/bin/build.sh

3. Trade Go Client
bash
nano ~/dev/TXdocumentation/trade/client/go/trade_client.go
go
package trade

import (
    "context"
    "fmt"
    "log"
    "os"
    "strings"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/metadata"
    
    tradePb "github.com/sologenic/trade/client/go"
    "google.golang.org/protobuf/types/known/timestamppb"
)

type TradeClient struct {
    client tradePb.TradeServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new trade client
func NewTradeClient(addr string) (*TradeClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("TRADE_STORE_TESTING"); testingMode == "TRUE" {
            return &TradeClient{}, nil
        }
        return nil, fmt.Errorf("TRADE_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to trade service: %w", err)
    }
    
    return &TradeClient{
        client: tradePb.NewTradeServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *TradeClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *TradeClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *TradeClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Create a new trade
func (c *TradeClient) CreateTrade(ctx context.Context, req *tradePb.CreateTradeRequest) (*tradePb.Trade, error) {
    if c.client == nil {
        return mockTrade(req), nil
    }
    
    resp, err := c.client.CreateTrade(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create trade failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("trade creation failed: %s", resp.Message)
    }
    
    return resp.Trade, nil
}

// Get trade by ID
func (c *TradeClient) GetTrade(ctx context.Context, tradeID, userID, orgID string) (*tradePb.Trade, error) {
    if c.client == nil {
        return mockTradeByID(tradeID), nil
    }
    
    req := &tradePb.GetTradeRequest{
        TradeId:        tradeID,
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetTrade(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get trade failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Trade, nil
}

// Get user's trades
func (c *TradeClient) GetTrades(ctx context.Context, userID, orgID, assetID string, activityType tradePb.ActivityType, fromDate, toDate time.Time, limit, offset int32) ([]*tradePb.Trade, int32, error) {
    if c.client == nil {
        return []*tradePb.Trade{}, 0, nil
    }
    
    req := &tradePb.GetTradesRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetId:        assetID,
        ActivityType:   activityType,
        Limit:          limit,
        Offset:         offset,
        SortBy:         "executed_at",
        SortOrder:      "desc",
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestamppb.New(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestamppb.New(toDate)
    }
    
    resp, err := c.client.GetTrades(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("get trades failed: %w", err)
    }
    
    return resp.Trades, resp.TotalCount, nil
}

// Record a deposit
func (c *TradeClient) RecordDeposit(ctx context.Context, userID, orgID, assetID, amount, txHash, sourceAddress, memo string) (*tradePb.Trade, error) {
    if c.client == nil {
        return mockDepositTrade(), nil
    }
    
    req := &tradePb.RecordDepositRequest{
        UserId:           userID,
        OrganizationId:   orgID,
        AssetId:          assetID,
        Amount:           amount,
        TransactionHash:  txHash,
        SourceAddress:    sourceAddress,
        Memo:             memo,
    }
    
    resp, err := c.client.RecordDeposit(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("record deposit failed: %w", err)
    }
    
    if !resp.Recorded {
        return nil, fmt.Errorf("deposit recording failed: %s", resp.Message)
    }
    
    return resp.Trade, nil
}

// Record a withdrawal
func (c *TradeClient) RecordWithdrawal(ctx context.Context, userID, orgID, assetID, amount, destinationAddress, feeAmount, memo string) (*tradePb.Trade, error) {
    if c.client == nil {
        return mockWithdrawalTrade(), nil
    }
    
    req := &tradePb.RecordWithdrawalRequest{
        UserId:              userID,
        OrganizationId:      orgID,
        AssetId:             assetID,
        Amount:              amount,
        DestinationAddress:  destinationAddress,
        FeeAmount:           feeAmount,
        Memo:                memo,
    }
    
    resp, err := c.client.RecordWithdrawal(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("record withdrawal failed: %w", err)
    }
    
    if !resp.Recorded {
        return nil, fmt.Errorf("withdrawal recording failed: %s", resp.Message)
    }
    
    return resp.Trade, nil
}

// Record a transfer between users
func (c *TradeClient) RecordTransfer(ctx context.Context, fromUserID, toUserID, orgID, assetID, amount, referenceID, memo string) (*tradePb.Trade, *tradePb.Trade, error) {
    if c.client == nil {
        return mockTransferSent(), mockTransferReceived(), nil
    }
    
    req := &tradePb.RecordTransferRequest{
        FromUserId:     fromUserID,
        ToUserId:       toUserID,
        OrganizationId: orgID,
        AssetId:        assetID,
        Amount:         amount,
        ReferenceId:    referenceID,
        Memo:           memo,
    }
    
    resp, err := c.client.RecordTransfer(c.getContext(ctx), req)
    if err != nil {
        return nil, nil, fmt.Errorf("record transfer failed: %w", err)
    }
    
    if !resp.Recorded {
        return nil, nil, fmt.Errorf("transfer recording failed: %s", resp.Message)
    }
    
    return resp.SentTrade, resp.ReceivedTrade, nil
}

// Record a dividend payment
func (c *TradeClient) RecordDividend(ctx context.Context, userID, orgID, assetID, amount, dividendType, referenceID string) (*tradePb.Trade, error) {
    if c.client == nil {
        return mockDividendTrade(), nil
    }
    
    req := &tradePb.RecordDividendRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetId:        assetID,
        Amount:         amount,
        DividendType:   dividendType,
        ReferenceId:    referenceID,
    }
    
    resp, err := c.client.RecordDividend(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("record dividend failed: %w", err)
    }
    
    if !resp.Recorded {
        return nil, fmt.Errorf("dividend recording failed")
    }
    
    return resp.Trade, nil
}

// Record a staking reward
func (c *TradeClient) RecordStakingReward(ctx context.Context, userID, orgID, assetID, amount, validator string, epochNumber uint64) (*tradePb.Trade, error) {
    if c.client == nil {
        return mockStakingReward(), nil
    }
    
    req := &tradePb.RecordStakingRewardRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetId:        assetID,
        Amount:         amount,
      Validator:      validator,
        EpochNumber:    epochNumber,
    }
    
    resp, err := c.client.RecordStakingReward(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("record staking reward failed: %w", err)
    }
    
    if !resp.Recorded {
        return nil, fmt.Errorf("staking reward recording failed")
    }
    
    return resp.Trade, nil
}

// Execute a trade from an order
func (c *TradeClient) ExecuteTrade(ctx context.Context, orderID, userID, orgID, assetPair, side, price, quantity, feeAmount, feeAsset, txHash string) (*tradePb.Trade, error) {
    if c.client == nil {
        return mockExecutedTrade(), nil
    }
    
    req := &tradePb.ExecuteTradeRequest{
        OrderId:         orderID,
        UserId:          userID,
        OrganizationId:  orgID,
        AssetPair:       assetPair,
        Side:            side,
        Price:           price,
        Quantity:        quantity,
        FeeAmount:       feeAmount,
        FeeAsset:        feeAsset,
        TransactionHash: txHash,
    }
    
    resp, err := c.client.ExecuteTrade(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("execute trade failed: %w", err)
    }
    
    if !resp.Executed {
        return nil, fmt.Errorf("trade execution failed: %s", resp.Message)
    }
    
    return resp.Trade, nil
}

// Get trade summary
func (c *TradeClient) GetTradeSummary(ctx context.Context, userID, orgID string, fromDate, toDate time.Time) (*tradePb.TradeSummary, error) {
    if c.client == nil {
        return mockTradeSummary(), nil
    }
    
    req := &tradePb.GetTradeSummaryRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestamppb.New(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestamppb.New(toDate)
    }
    
    resp, err := c.client.GetTradeSummary(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get trade summary failed: %w", err)
    }
    
    return resp.Summary, nil
}

// Get volume report
func (c *TradeClient) GetVolumeReport(ctx context.Context, orgID string, fromDate, toDate time.Time, groupBy, assetID string) (*tradePb.GetVolumeReportResponse, error) {
    if c.client == nil {
        return &tradePb.GetVolumeReportResponse{}, nil
    }
    
    req := &tradePb.GetVolumeReportRequest{
        OrganizationId: orgID,
        GroupBy:        groupBy,
        AssetId:        assetID,
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestamppb.New(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestamppb.New(toDate)
    }
    
    resp, err := c.client.GetVolumeReport(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get volume report failed: %w", err)
    }
    
    return resp, nil
}

// Get capital gains report for tax purposes
func (c *TradeClient) GetCapitalGainsReport(ctx context.Context, userID, orgID string, taxYear int32, calculationMethod string) (*tradePb.GetCapitalGainsReportResponse, error) {
    if c.client == nil {
        return &tradePb.GetCapitalGainsReportResponse{
            ReportId: "test-report-id",
        }, nil
    }
    
    req := &tradePb.GetCapitalGainsReportRequest{
        UserId:             userID,
        OrganizationId:     orgID,
        TaxYear:            taxYear,
        CalculationMethod:  calculationMethod,
    }
    
    resp, err := c.client.GetCapitalGainsReport(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get capital gains report failed: %w", err)
    }
    
    return resp, nil
}

// Reconcile trades with external source
func (c *TradeClient) ReconcileTrades(ctx context.Context, orgID string, fromDate, toDate time.Time, externalSource string, autoCorrect bool) (*tradePb.ReconcileTradesResponse, error) {
    if c.client == nil {
        return &tradePb.ReconcileTradesResponse{
            ReconciliationId: "test-recon-id",
            TotalTrades:      100,
            MatchedTrades:    95,
            MismatchedTrades: 5,
        }, nil
    }
    
    req := &tradePb.ReconcileTradesRequest{
        OrganizationId:  orgID,
        ExternalSource:  externalSource,
        AutoCorrect:     autoCorrect,
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestamppb.New(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestamppb.New(toDate)
    }
    
    resp, err := c.client.ReconcileTrades(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("reconcile trades failed: %w", err)
    }
    
    return resp, nil
}

// Stream real-time trades
func (c *TradeClient) StreamTrades(ctx context.Context, userID, orgID string, assetIDs []string, activityTypes []tradePb.ActivityType) (<-chan *tradePb.Trade, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &tradePb.StreamTradesRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetIds:       assetIDs,
        ActivityTypes:  activityTypes,
    }
    
    stream, err := c.client.StreamTrades(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("failed to create stream: %w", err)
    }
    
    trades := make(chan *tradePb.Trade, 100)
    
    go func() {
        defer close(trades)
        for {
            trade, err := stream.Recv()
            if err != nil {
                log.Printf("Stream receive error: %v", err)
                return
            }
            trades <- trade
        }
    }()
    
    return trades, nil
}

// Mock functions for testing
func mockTrade(req *tradePb.CreateTradeRequest) *tradePb.Trade {
    return &tradePb.Trade{
        TradeId:        "mock-trade-id",
        UserId:         req.UserId,
        ActivityType:   req.ActivityType,
        AssetId:        req.AssetId,
        AssetSymbol:    req.AssetSymbol,
        Amount:         req.Amount,
        Price:          req.Price,
        Status:         tradePb.TradeStatus_COMPLETED,
        ExecutedAt:     timestamppb.Now(),
        RecordedAt:     timestamppb.Now(),
    }
}

func mockTradeByID(tradeID string) *tradePb.Trade {
    return &tradePb.Trade{
        TradeId: tradeID,
        Status:  tradePb.TradeStatus_COMPLETED,
    }
}

func mockDepositTrade() *tradePb.Trade {
    return &tradePb.Trade{
        TradeId:      "deposit-trade-id",
        ActivityType: tradePb.ActivityType_DEPOSIT,
        Status:       tradePb.TradeStatus_COMPLETED,
    }
}

func mockWithdrawalTrade() *tradePb.Trade {
    return &tradePb.Trade{
        TradeId:      "withdrawal-trade-id",
        ActivityType: tradePb.ActivityType_WITHDRAWAL,
        Status:       tradePb.TradeStatus_COMPLETED,
    }
}

func mockTransferSent() *tradePb.Trade {
    return &tradePb.Trade{
        TradeId:      "transfer-sent-id",
        ActivityType: tradePb.ActivityType_TRANSFER_SENT,
        Status:       tradePb.TradeStatus_COMPLETED,
    }
}

func mockTransferReceived() *tradePb.Trade {
    return &tradePb.Trade{
        TradeId:      "transfer-received-id",
        ActivityType: tradePb.ActivityType_TRANSFER_RECEIVED,
        Status:       tradePb.TradeStatus_COMPLETED,
    }
}

func mockDividendTrade() *tradePb.Trade {
    return &tradePb.Trade{
        TradeId:      "dividend-trade-id",
        ActivityType: tradePb.ActivityType_DIVIDEND,
        Status:       tradePb.TradeStatus_COMPLETED,
    }
}

func mockStakingReward() *tradePb.Trade {
    return &tradePb.Trade{
        TradeId:      "staking-reward-id",
        ActivityType: tradePb.ActivityType_STAKING_REWARD,
        Status:       tradePb.TradeStatus_COMPLETED,
    }
}

func mockExecutedTrade() *tradePb.Trade {
    return &tradePb.Trade{
        TradeId:      "executed-trade-id",
        ActivityType: tradePb.ActivityType_TRADE_BUY,
        Status:       tradePb.TradeStatus_COMPLETED,
    }
}

func mockTradeSummary() *tradePb.TradeSummary {
    return &tradePb.TradeSummary{
        TotalVolume:     "1000000.00",
        TotalTrades:     500,
        TotalDeposits:   "500000.00",
        TotalWithdrawals: "200000.00",
        TotalFeesPaid:   "5000.00",
        NetFlow:         "300000.00",
        UniqueAssets:    5,
    }
}

// Example usage
func main() {
    client, err := NewTradeClient("trade-store:50072")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    userID := "user-789"
    
    // Record a deposit
    deposit, err := client.RecordDeposit(ctx, userID, orgID, "TX", "1000.00", "0x123abc", "external-wallet-1", "Initial deposit")
    if err != nil {
        log.Printf("Failed to record deposit: %v", err)
    } else {
        log.Printf("Deposit recorded: %s - %s %s", deposit.TradeId, deposit.Amount, deposit.AssetSymbol)
    }
    
    // Execute a trade
    trade, err := client.ExecuteTrade(ctx, "order-456", userID, orgID, "TX/USD", "buy", "50.00", "100.0", "0.50", "TX", "0x456def")
    if err != nil {
        log.Printf("Failed to execute trade: %v", err)
    } else {
        log.Printf("Trade executed: %s - %s %s @ %s", trade.TradeId, trade.Amount, trade.AssetSymbol, trade.Price)
    }
    
    // Record a transfer
    sent, received, err := client.RecordTransfer(ctx, userID, "user-456", orgID, "TX", "50.00", "transfer-789", "Payment for services")
    if err != nil {
        log.Printf("Failed to record transfer: %v", err)
    } else {
        log.Printf("Transfer sent: %s, received: %s", sent.TradeId, received.TradeId)
    }
    
    // Get trade summary
    summary, err := client.GetTradeSummary(ctx, userID, orgID, time.Now().AddDate(-1, 0, 0), time.Now())
    if err != nil {
        log.Printf("Failed to get trade summary: %v", err)
    } else {
        log.Printf("Trade Summary:")
        log.Printf("  Total Volume: $%s", summary.TotalVolume)
        log.Printf("  Total Trades: %d", summary.TotalTrades)
        log.Printf("  Total Fees: $%s", summary.TotalFeesPaid)
        log.Printf("  Net Flow: $%s", summary.NetFlow)
    }
    
    // Get user's trades
    trades, total, err := client.GetTrades(ctx, userID, orgID, "TX", tradePb.ActivityType_ACTIVITY_TYPE_UNSPECIFIED, time.Now().AddDate(0, -1, 0), time.Now(), 20, 0)
    if err != nil {
        log.Printf("Failed to get trades: %v", err)
    } else {
        log.Printf("Found %d trades (total: %d)", len(trades), total)
        for _, t := range trades {
            log.Printf("  - %s: %s %s (%s)", t.TradeId, t.Amount, t.AssetSymbol, t.ActivityType)
        }
    }
    
    // Get capital gains report for tax season
    gainsReport, err := client.GetCapitalGainsReport(ctx, userID, orgID, 2024, "fifo")
    if err != nil {
        log.Printf("Failed to get capital gains report: %v", err)
    } else {
        log.Printf("Capital Gains Report: %s", gainsReport.DownloadUrl)
        log.Printf("  Short-term gain: $%s", gainsReport.TotalShortTermGain)
        log.Printf("  Long-term gain: $%s", gainsReport.TotalLongTermGain)
        log.Printf("  Total realized gain: $%s", gainsReport.TotalRealizedGain)
    }
}
Save the file:

Ctrl+O, Enter, Ctrl+X

4. Trade Docker Compose
bash
nano ~/dev/TXdocumentation/trade/docker-compose.yml
yaml
version: '3.8'

services:
  trade-service:
    image: sologenic/trade-service:latest
    environment:
      - TRADE_SERVICE_PORT=50072
      - TRADE_STORE=trade-store:50072
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=trades
      - POSTGRES_USER=trade_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - TIMESCALEDB_HOST=timescaledb
      - TIMESCALEDB_PORT=5432
      - TIMESCALEDB_DB=trade_history
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - CLICKHOUSE_HOST=clickhouse
      - CLICKHOUSE_PORT=9000
      - MAX_TRADES_PER_QUERY=1000
      - TRADE_RETENTION_DAYS=2555
      - REPORT_BATCH_SIZE=10000
      - CACHE_TTL_SECONDS=300
      - ENABLE_REAL_TIME_STREAMING=true
      - LOG_LEVEL=info
    ports:
      - "50072:50072"
    networks:
      - internal
    depends_on:
      - postgres
      - timescaledb
      - redis
      - clickhouse
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50072"]
      interval: 30s
      timeout: 10s
      retries: 3

  trade-store:
    image: sologenic/trade-store:latest
    environment:
      - TRADE_STORE_PORT=50073
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=trades
      - POSTGRES_USER=trade_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - TIMESCALEDB_HOST=timescaledb
      - TIMESCALEDB_PORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50073:50073"
    networks:
      - internal
    depends_on:
      - postgres
      - timescaledb
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=trades
      - POSTGRES_USER=trade_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U trade_user -d trades"]
      interval: 10s
      timeout: 5s
      retries: 5

  timescaledb:
    image: timescale/timescaledb:latest-pg15
    environment:
      - POSTGRES_DB=trade_history
      - POSTGRES_USER=trade_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - timescaledb_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U trade_user -d trade_history"]
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

  clickhouse:
    image: clickhouse/clickhouse-server:latest
    environment:
      - CLICKHOUSE_DB=trade_analytics
      - CLICKHOUSE_USER=analytics_user
      - CLICKHOUSE_PASSWORD=${CLICKHOUSE_PASSWORD}
    volumes:
      - clickhouse_data:/var/lib/clickhouse
    networks:
      - internal
    healthcheck:
      test: ["CMD", "clickhouse-client", "--query", "SELECT 1"]
      interval: 30s
      timeout: 10s
      retries: 5

networks:
  internal:
    driver: bridge

volumes:
  postgres_data:
  timescaledb_data:
  redis_data:
  clickhouse_data:
Save the file:

Ctrl+O, Enter, Ctrl+X

5. Trade Environment File
bash
nano ~/dev/TXdocumentation/trade/.env
bash
# Database Configuration
DB_PASSWORD=your_secure_password
CLICKHOUSE_PASSWORD=clickhouse_secure_password

# Service Configuration
TRADE_STORE=trade-store:50073
TRADE_STORE_TESTING=FALSE

# Business Rules
MAX_TRADES_PER_QUERY=1000
TRADE_RETENTION_DAYS=2555
REPORT_BATCH_SIZE=10000

# Cache Configuration
CACHE_TTL_SECONDS=300

# Streaming
ENABLE_REAL_TIME_STREAMING=true

# Logging
LOG_LEVEL=info
Save the file:

Ctrl+O, Enter, Ctrl+X

Now let me create the missing build scripts and Go clients for the other services:

6. Holdings Build Script
bash
nano ~/dev/TXdocumentation/holdings/bin/build.sh
bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting Holdings proto build...${NC}"

# Check if proto file exists
if [ ! -f "holdings.proto" ] && [ ! -f "proto/holdings.proto" ]; then
    echo -e "${RED}Error: No holdings.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "holdings.proto" ]; then
    PROTO_FILE="holdings.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/holdings.proto"
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
        --doc_opt=markdown,holdings-api.md \
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
echo "  - client/go/holdings.pb.go"
echo "  - client/go/holdings_grpc.pb.go"
if [ -f "client/typescript/holdings.ts" ]; then
    echo "  - client/typescript/holdings.ts"
fi
echo "  - build/holdings-api.md"
Save and make executable:

Ctrl+O, Enter, Ctrl+X

chmod +x ~/dev/TXdocumentation/holdings/bin/build.sh

7. Order Build Script
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
Save and make executable:

Ctrl+O, Enter, Ctrl+X

chmod +x ~/dev/TXdocumentation/order/bin/build.sh

8. Record Build Script
bash
mkdir -p ~/dev/TXdocumentation/record/bin
nano ~/dev/TXdocumentation/record/bin/build.sh
bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting Record proto build...${NC}"

# Check if proto file exists
if [ ! -f "record.proto" ] && [ ! -f "proto/record.proto" ]; then
    echo -e "${RED}Error: No record.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "record.proto" ]; then
    PROTO_FILE="record.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/record.proto"
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
        --doc_opt=markdown,record-api.md \
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
echo "  - client/go/record.pb.go"
echo "  - client/go/record_grpc.pb.go"
if [ -f "client/typescript/record.ts" ]; then
    echo "  - client/typescript/record.ts"
fi
echo "  - build/record-api.md"
