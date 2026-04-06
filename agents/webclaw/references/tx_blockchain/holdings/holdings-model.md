# Holdings Model (Asset Epoch Data Model)

The Asset Epoch Data Model proto provides all the functionality required to interact with the holdings service. It supports tracking user asset holdings, balances, historical snapshots, and epoch-based accounting.

## Overview

The Holdings service is a gRPC-based system that handles:
- User asset holdings tracking
- Balance management across multiple assets
- Historical balance snapshots (epoch-based)
- Asset epoch data aggregation
- Holdings reconciliation
- Portfolio valuation
- Staking and locked balance tracking
- Cross-epoch balance comparisons

## Architecture
┌─────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Wallet, Portfolio Dashboard, Trading, Analytics) │
└───────────────────┬─────────────────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────────────────┐
│ Holdings Service (Asset Epoch Data Model) │
│ - Balance Management │
│ - Epoch Snapshots │
│ - Historical Tracking │
│ - Portfolio Aggregation │
│ - Reconciliation Engine │
└───────────────────┬─────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Storage Layer │
│ - Holdings Store (PostgreSQL) │
│ - Epoch Store (TimescaleDB) │
│ - Balance Cache (Redis) │
│ - Analytics Store (ClickHouse) │
└─────────────────────────────────────────────────────────┘

text

## Environment Variables

### Required Variables

| Variable | Description | Format | Example |
|----------|-------------|--------|---------|
| `HOLDINGS_STORE` | gRPC endpoint for holdings store service | `host:port` | `holdings-store:50066` |
| `HOLDINGS_STORE_TESTING` | Enable test mode with in-memory buffer | `TRUE` | `TRUE` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EPOCH_DURATION_HOURS` | Epoch duration in hours | `24` |
| `SNAPSHOT_RETENTION_DAYS` | Historical snapshot retention | `365` |
| `MAX_HOLDINGS_PER_USER` | Maximum distinct assets per user | `1000` |
| `RECONCILIATION_ENABLED` | Enable automatic reconciliation | `true` |
| `PRICE_CACHE_TTL` | Price cache TTL in seconds | `60` |

## Proto Definition

```protobuf
syntax = "proto3";

package holdings.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Holdings Service Definition
service HoldingsService {
    // Balance operations
    rpc GetBalance(GetBalanceRequest) returns (GetBalanceResponse);
    rpc GetBalances(GetBalancesRequest) returns (GetBalancesResponse);
    rpc UpdateBalance(UpdateBalanceRequest) returns (UpdateBalanceResponse);
    rpc TransferBalance(TransferBalanceRequest) returns (TransferBalanceResponse);
    
    // Epoch operations
    rpc GetEpochSnapshot(GetEpochSnapshotRequest) returns (GetEpochSnapshotResponse);
    rpc GetEpochSnapshots(GetEpochSnapshotsRequest) returns (GetEpochSnapshotsResponse);
    rpc GetCurrentEpoch(GetCurrentEpochRequest) returns (GetCurrentEpochResponse);
    rpc GetEpochHistory(GetEpochHistoryRequest) returns (GetEpochHistoryResponse);
    
    // Holdings management
    rpc GetHoldings(GetHoldingsRequest) returns (GetHoldingsResponse);
    rpc GetHoldingHistory(GetHoldingHistoryRequest) returns (GetHoldingHistoryResponse);
    rpc GetHoldingsSummary(GetHoldingsSummaryRequest) returns (GetHoldingsSummaryResponse);
    
    // Portfolio valuation
    rpc GetPortfolioValue(GetPortfolioValueRequest) returns (GetPortfolioValueResponse);
    rpc GetPortfolioHistory(GetPortfolioHistoryRequest) returns (GetPortfolioHistoryResponse);
    rpc GetAssetDistribution(GetAssetDistributionRequest) returns (GetAssetDistributionResponse);
    
    // Staking and locked balances
    rpc GetStakedBalance(GetStakedBalanceRequest) returns (GetStakedBalanceResponse);
    rpc GetLockedBalance(GetLockedBalanceRequest) returns (GetLockedBalanceResponse);
    rpc GetVestingBalance(GetVestingBalanceRequest) returns (GetVestingBalanceResponse);
    
    // Reconciliation
    rpc ReconcileHoldings(ReconcileHoldingsRequest) returns (ReconcileHoldingsResponse);
    rpc GetReconciliationStatus(GetReconciliationStatusRequest) returns (GetReconciliationStatusResponse);
    
    // Analytics
    rpc GetHoldingsAnalytics(GetHoldingsAnalyticsRequest) returns (GetHoldingsAnalyticsResponse);
    rpc GetTopHolders(GetTopHoldersRequest) returns (GetTopHoldersResponse);
}

// ==================== Balance Messages ====================

message Balance {
    string user_id = 1;                 // User identifier
    string asset_id = 2;                // Asset identifier
    string asset_symbol = 3;            // Asset symbol (e.g., TX, ETH)
    string available_balance = 4;       // Available for trading (string for big numbers)
    string locked_balance = 5;          // Locked in orders/contracts
    string staked_balance = 6;          // Staked balance
    string vesting_balance = 7;         // Vesting balance
    string total_balance = 8;           // Total = available + locked + staked + vesting
    string reserved_balance = 9;        // Reserved for fees
    string pending_deposit = 10;        // Pending deposit amount
    string pending_withdrawal = 11;     // Pending withdrawal amount
    
    int32 decimals = 12;                // Asset decimals
    string value_usd = 13;              // Current USD value
    
    google.protobuf.Timestamp last_updated = 14;
    google.protobuf.Timestamp created_at = 15;
    string organization_id = 16;
    map<string, string> metadata = 17;
}

message GetBalanceRequest {
    string user_id = 1;
    string asset_id = 2;
    string asset_symbol = 3;            // Alternative lookup
    string organization_id = 4;
    bool include_history = 5;           // Include recent history
}

message GetBalanceResponse {
    Balance balance = 1;
    bool found = 2;
    repeated BalanceHistory recent_history = 3; // If include_history true
}

message GetBalancesRequest {
    string user_id = 1;
    repeated string asset_ids = 2;      // Specific assets (empty = all)
    string organization_id = 3;
    bool include_zero_balances = 4;
    int32 limit = 5;
    int32 offset = 6;
    string sort_by = 7;                 // value_usd, asset_symbol, total_balance
    string sort_order = 8;              // asc, desc
}

message GetBalancesResponse {
    repeated Balance balances = 1;
    int32 total_count = 2;
    bool has_more = 3;
    string total_value_usd = 4;         // Total portfolio value
}

message UpdateBalanceRequest {
    string user_id = 1;
    string asset_id = 2;
    string amount = 3;                  // Amount to add/subtract
    string operation = 4;               // credit, debit, lock, unlock, stake, unstake
    string reference_id = 5;            // Transaction reference
    string reference_type = 6;          // trade, deposit, withdrawal, fee, reward
    string organization_id = 7;
    string reason = 8;                  // Reason for update
    map<string, string> metadata = 9;
}

message UpdateBalanceResponse {
    Balance balance = 1;
    bool success = 2;
    string transaction_id = 3;
    string message = 4;
}

message TransferBalanceRequest {
    string from_user_id = 1;
    string to_user_id = 2;
    string asset_id = 3;
    string amount = 4;
    string reference_id = 5;
    string reference_type = 6;
    string organization_id = 7;
    string memo = 8;
    map<string, string> metadata = 9;
}

message TransferBalanceResponse {
    bool success = 1;
    string transfer_id = 2;
    Balance from_balance = 3;
    Balance to_balance = 4;
    string message = 5;
}

// ==================== Epoch Messages ====================

message Epoch {
    int64 epoch_number = 1;             // Sequential epoch number
    google.protobuf.Timestamp start_time = 2;
    google.protobuf.Timestamp end_time = 3;
    bool is_closed = 4;                 // Whether epoch is finalized
    google.protobuf.Timestamp closed_at = 5;
    int32 snapshot_count = 6;           // Number of snapshots in this epoch
    string total_value_usd = 7;         // Total value across all users
    map<string, string> metrics = 8;    // Epoch metrics
}

message EpochSnapshot {
    string user_id = 1;
    string asset_id = 2;
    string asset_symbol = 3;
    string balance = 4;
    string value_usd = 5;
    int64 epoch_number = 6;
    google.protobuf.Timestamp snapshot_time = 7;
    bool is_final = 8;                  // Final snapshot for epoch
}

message GetEpochSnapshotRequest {
    string user_id = 1;
    int64 epoch_number = 2;
    string asset_id = 3;                // Optional, specific asset
    string organization_id = 4;
}

message GetEpochSnapshotResponse {
    repeated EpochSnapshot snapshots = 1;
    Epoch epoch = 2;
    bool found = 3;
}

message GetEpochSnapshotsRequest {
    string user_id = 1;
    int64 from_epoch = 2;
    int64 to_epoch = 3;
    string organization_id = 4;
    int32 limit = 5;
    int32 offset = 6;
}

message GetEpochSnapshotsResponse {
    repeated EpochSnapshot snapshots = 1;
    int32 total_count = 2;
}

message GetCurrentEpochRequest {
    string organization_id = 1;
}

message GetCurrentEpochResponse {
    Epoch epoch = 1;
    int64 time_remaining_seconds = 2;
    int32 snapshot_count = 3;
}

message GetEpochHistoryRequest {
    int64 from_epoch = 1;
    int64 to_epoch = 2;
    string organization_id = 3;
    int32 limit = 4;
    int32 offset = 5;
}

message GetEpochHistoryResponse {
    repeated Epoch epochs = 1;
    int32 total_count = 2;
}

// ==================== Holdings Management ====================

message Holding {
    string user_id = 1;
    string asset_id = 2;
    string asset_symbol = 3;
    string asset_name = 4;
    string logo_url = 5;
    
    // Current balances
    string total_balance = 6;
    string available_balance = 7;
    string locked_balance = 8;
    string staked_balance = 9;
    
    // Value
    string price_usd = 10;
    string value_usd = 11;
    string value_change_24h = 12;       // Percentage change
    string value_change_7d = 13;
    
    // Performance
    string cost_basis = 14;              // Average purchase price
    string realized_pnl = 15;            // Realized profit/loss
    string unrealized_pnl = 16;          // Unrealized profit/loss
    
    // Holdings metrics
    double allocation_percentage = 17;   // Percentage of portfolio
    int32 rank = 18;                    // Rank in portfolio
    
    google.protobuf.Timestamp first_acquired = 19;
    google.protobuf.Timestamp last_updated = 20;
}

message GetHoldingsRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_zero_holdings = 3;
    bool include_performance = 4;
    int32 limit = 5;
    int32 offset = 6;
    string sort_by = 7;                 // value_usd, allocation, symbol
    string sort_order = 8;
}

message GetHoldingsResponse {
    repeated Holding holdings = 1;
    int32 total_count = 2;
    string total_value_usd = 3;
    string total_change_24h = 4;
}

message HoldingHistory {
    string user_id = 1;
    string asset_id = 2;
    string balance = 3;
    string value_usd = 4;
    google.protobuf.Timestamp timestamp = 5;
    string event_type = 6;              // snapshot, trade, deposit, withdrawal
    string reference_id = 7;
}

message GetHoldingHistoryRequest {
    string user_id = 1;
    string asset_id = 2;
    string organization_id = 3;
    google.protobuf.Timestamp from_date = 4;
    google.protobuf.Timestamp to_date = 5;
    string interval = 6;                // hour, day, week, month
    int32 limit = 7;
}

message GetHoldingHistoryResponse {
    repeated HoldingHistory history = 1;
    int32 total_count = 2;
}

message GetHoldingsSummaryRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetHoldingsSummaryResponse {
    string total_value_usd = 1;
    int32 unique_assets = 2;
    int32 total_assets_count = 3;
    string best_performing_asset = 4;
    string worst_performing_asset = 5;
    string total_realized_pnl = 6;
    string total_unrealized_pnl = 7;
    map<string, string> asset_allocation = 8; // asset_symbol -> percentage
}

// ==================== Portfolio Valuation ====================

message PortfolioValue {
    string user_id = 1;
    string total_value_usd = 2;
    string change_24h = 3;
    string change_7d = 4;
    string change_30d = 5;
    string change_all_time = 6;
    google.protobuf.Timestamp timestamp = 7;
}

message GetPortfolioValueRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_history = 3;
}

message GetPortfolioValueResponse {
    PortfolioValue current = 1;
    repeated PortfolioValueHistory history = 2; // If include_history true
}

message PortfolioValueHistory {
    string total_value_usd = 1;
    google.protobuf.Timestamp timestamp = 2;
    string day_change = 3;
}

message GetPortfolioHistoryRequest {
    string user_id = 1;
    string organization_id = 2;
    google.protobuf.Timestamp from_date = 3;
    google.protobuf.Timestamp to_date = 4;
    string interval = 5;                // hour, day, week, month
    bool include_breakdown = 6;         // Include asset breakdown
}

message GetPortfolioHistoryResponse {
    repeated PortfolioValueHistory values = 1;
    map<string, repeated AssetPortfolioHistory> breakdown = 2; // If include_breakdown
}

message AssetPortfolioHistory {
    string asset_symbol = 1;
    string value_usd = 2;
    google.protobuf.Timestamp timestamp = 3;
}

message GetAssetDistributionRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetAssetDistributionResponse {
    repeated AssetDistribution distributions = 1;
    map<string, double> allocation_percentages = 2;
}

message AssetDistribution {
    string asset_symbol = 1;
    string value_usd = 2;
    double percentage = 3;
    string balance = 4;
}

// ==================== Staking and Locked Balances ====================

message StakedBalance {
    string user_id = 1;
    string asset_id = 2;
    string staked_amount = 3;
    string reward_amount = 4;
    string total_amount = 5;
    string validator = 6;
    google.protobuf.Timestamp staked_at = 7;
    google.protobuf.Timestamp unstake_available_at = 8;
    string apy = 9;
    string status = 10;                 // staking, unstaking, completed
}

message GetStakedBalanceRequest {
    string user_id = 1;
    string asset_id = 2;                // Optional
    string organization_id = 3;
}

message GetStakedBalanceResponse {
    repeated StakedBalance staked_balances = 1;
    string total_staked_usd = 2;
}

message LockedBalance {
    string user_id = 1;
    string asset_id = 2;
    string locked_amount = 3;
    string lock_reason = 4;             // order, vesting, governance
    string reference_id = 5;
    google.protobuf.Timestamp locked_until = 6;
    google.protobuf.Timestamp locked_at = 7;
    bool is_releasable = 8;
}

message GetLockedBalanceRequest {
    string user_id = 1;
    string asset_id = 2;                // Optional
    string organization_id = 3;
    bool include_expired = 4;
}

message GetLockedBalanceResponse {
    repeated LockedBalance locked_balances = 1;
    string total_locked_usd = 2;
}

message VestingBalance {
    string user_id = 1;
    string asset_id = 2;
    string total_vesting_amount = 3;
    string vested_amount = 4;
    string unvested_amount = 5;
    google.protobuf.Timestamp start_time = 6;
    google.protobuf.Timestamp end_time = 7;
    string cliff_duration = 8;
    string vesting_schedule = 9;        // linear, monthly, quarterly
}

message GetVestingBalanceRequest {
    string user_id = 1;
    string asset_id = 2;                // Optional
    string organization_id = 3;
}

message GetVestingBalanceResponse {
    repeated VestingBalance vesting_balances = 1;
    string total_vesting_usd = 2;
}

// ==================== Reconciliation ====================

message ReconciliationRequest {
    string user_id = 1;
    string organization_id = 2;
    repeated string asset_ids = 3;      // Assets to reconcile
    google.protobuf.Timestamp as_of_date = 4;
}

message ReconciliationResult {
    string asset_id = 1;
    string expected_balance = 2;
    string actual_balance = 3;
    string difference = 4;
    bool matches = 5;
    repeated string discrepancies = 6;
}

message ReconcileHoldingsRequest {
    string user_id = 1;
    string organization_id = 2;
    repeated string asset_ids = 3;
    bool auto_correct = 4;              // Automatically fix discrepancies
}

message ReconcileHoldingsResponse {
    string reconciliation_id = 1;
    repeated ReconciliationResult results = 2;
    bool all_matched = 3;
    int32 corrections_made = 4;
    string message = 5;
}

message GetReconciliationStatusRequest {
    string reconciliation_id = 1;
    string organization_id = 2;
}

message GetReconciliationStatusResponse {
    string status = 1;                  // pending, in_progress, completed, failed
    int32 total_assets = 2;
    int32 completed_assets = 3;
    int32 discrepancies_found = 4;
    google.protobuf.Timestamp started_at = 5;
    google.protobuf.Timestamp completed_at = 6;
}

// ==================== Analytics ====================

message GetHoldingsAnalyticsRequest {
    string organization_id = 1;
    google.protobuf.Timestamp from_date = 2;
    google.protobuf.Timestamp to_date = 3;
    string group_by = 4;                // day, week, month, asset
}

message GetHoldingsAnalyticsResponse {
    TotalVolume total_volume = 1;
    repeated AssetVolume top_assets = 2;
    UserActivity user_activity = 3;
    map<string, string> metrics = 4;
}

message TotalVolume {
    string deposit_volume = 1;
    string withdrawal_volume = 2;
    string trading_volume = 3;
    string total_volume = 4;
}

message AssetVolume {
    string asset_symbol = 1;
    string volume = 2;
    double percentage = 3;
}

message UserActivity {
    int32 active_users = 1;
    int32 new_users = 2;
    int32 users_with_holdings = 3;
    double avg_holding_value = 4;
}

message GetTopHoldersRequest {
    string asset_id = 1;
    string asset_symbol = 2;
    string organization_id = 3;
    int32 limit = 4;                    // Max 100
}

message GetTopHoldersResponse {
    repeated TopHolder holders = 1;
    string total_supply_percentage = 2;
}

message TopHolder {
    string user_id = 1;
    string balance = 2;
    string percentage_of_supply = 3;
    string value_usd = 4;
    int32 rank = 5;
}
Building the Required Files
Create the build script:

bash
mkdir -p ~/dev/TXdocumentation/holdings/bin
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
Make it executable:

bash
chmod +x ~/dev/TXdocumentation/holdings/bin/build.sh
Client Implementation
Go Client
Create the Go client:

bash
nano ~/dev/TXdocumentation/holdings/client/go/holdings_client.go
go
package holdings

import (
    "context"
    "fmt"
    "log"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/metadata"
    
    holdingspb "github.com/sologenic/holdings/client/go"
)

type HoldingsClient struct {
    client holdingspb.HoldingsServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new holdings client
func NewHoldingsClient(addr string) (*HoldingsClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("HOLDINGS_STORE_TESTING"); testingMode == "TRUE" {
            // Use in-memory test client
            return &HoldingsClient{}, nil
        }
        return nil, fmt.Errorf("HOLDINGS_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to holdings service: %w", err)
    }
    
    return &HoldingsClient{
        client: holdingspb.NewHoldingsServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *HoldingsClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *HoldingsClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *HoldingsClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Get balance for a specific asset
func (c *HoldingsClient) GetBalance(ctx context.Context, userID, assetID, orgID string) (*holdingspb.Balance, error) {
    if c.client == nil {
        return mockBalance(userID, assetID), nil
    }
    
    req := &holdingspb.GetBalanceRequest{
        UserId:         userID,
        AssetId:        assetID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetBalance(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get balance failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Balance, nil
}

// Get all balances for a user
func (c *HoldingsClient) GetBalances(ctx context.Context, userID, orgID string, includeZero bool, limit, offset int32) ([]*holdingspb.Balance, int32, string, error) {
    if c.client == nil {
        return []*holdingspb.Balance{}, 0, "0", nil
    }
    
    req := &holdingspb.GetBalancesRequest{
        UserId:              userID,
        OrganizationId:      orgID,
        IncludeZeroBalances: includeZero,
        Limit:               limit,
        Offset:              offset,
        SortBy:              "value_usd",
        SortOrder:           "desc",
    }
    
    resp, err := c.client.GetBalances(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, "", fmt.Errorf("get balances failed: %w", err)
    }
    
    return resp.Balances, resp.TotalCount, resp.TotalValueUsd, nil
}

// Update balance (credit/debit)
func (c *HoldingsClient) UpdateBalance(ctx context.Context, userID, assetID, amount, operation, referenceID, referenceType, orgID, reason string) (*holdingspb.Balance, error) {
    if c.client == nil {
        return mockBalance(userID, assetID), nil
    }
    
    req := &holdingspb.UpdateBalanceRequest{
        UserId:         userID,
        AssetId:        assetID,
        Amount:         amount,
        Operation:      operation,
        ReferenceId:    referenceID,
        ReferenceType:  referenceType,
        OrganizationId: orgID,
        Reason:         reason,
    }
    
    resp, err := c.client.UpdateBalance(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update balance failed: %w", err)
    }
    
    if !resp.Success {
        return nil, fmt.Errorf("update failed: %s", resp.Message)
    }
    
    return resp.Balance, nil
}

// Transfer balance between users
func (c *HoldingsClient) TransferBalance(ctx context.Context, fromUserID, toUserID, assetID, amount, referenceID, referenceType, orgID, memo string) (*holdingspb.TransferBalanceResponse, error) {
    if c.client == nil {
        return &holdingspb.TransferBalanceResponse{
            Success: true,
            TransferId: "test-transfer-id",
        }, nil
    }
    
    req := &holdingspb.TransferBalanceRequest{
        FromUserId:    fromUserID,
        ToUserId:      toUserID,
        AssetId:       assetID,
        Amount:        amount,
        ReferenceId:   referenceID,
        ReferenceType: referenceType,
        OrganizationId: orgID,
        Memo:          memo,
    }
    
    resp, err := c.client.TransferBalance(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("transfer balance failed: %w", err)
    }
    
    return resp, nil
}

// Get holdings (portfolio view)
func (c *HoldingsClient) GetHoldings(ctx context.Context, userID, orgID string, includePerformance bool, limit, offset int32) ([]*holdingspb.Holding, int32, string, error) {
    if c.client == nil {
        return []*holdingspb.Holding{}, 0, "0", nil
    }
    
    req := &holdingspb.GetHoldingsRequest{
        UserId:             userID,
        OrganizationId:     orgID,
        IncludePerformance: includePerformance,
        IncludeZeroHoldings: false,
        Limit:              limit,
        Offset:             offset,
        SortBy:             "value_usd",
        SortOrder:          "desc",
    }
    
    resp, err := c.client.GetHoldings(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, "", fmt.Errorf("get holdings failed: %w", err)
    }
    
    return resp.Holdings, resp.TotalCount, resp.TotalValueUsd, nil
}

// Get epoch snapshot
func (c *HoldingsClient) GetEpochSnapshot(ctx context.Context, userID string, epochNumber int64, orgID string) ([]*holdingspb.EpochSnapshot, error) {
    if c.client == nil {
        return []*holdingspb.EpochSnapshot{}, nil
    }
    
    req := &holdingspb.GetEpochSnapshotRequest{
        UserId:         userID,
        EpochNumber:    epochNumber,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetEpochSnapshot(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get epoch snapshot failed: %w", err)
    }
    
    return resp.Snapshots, nil
}

// Get current epoch
func (c *HoldingsClient) GetCurrentEpoch(ctx context.Context, orgID string) (*holdingspb.Epoch, error) {
    if c.client == nil {
        return mockEpoch(), nil
    }
    
    req := &holdingspb.GetCurrentEpochRequest{
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetCurrentEpoch(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get current epoch failed: %w", err)
    }
    
    return resp.Epoch, nil
}

// Get portfolio value
func (c *HoldingsClient) GetPortfolioValue(ctx context.Context, userID, orgID string, includeHistory bool) (*holdingspb.GetPortfolioValueResponse, error) {
    if c.client == nil {
        return &holdingspb.GetPortfolioValueResponse{
            Current: &holdingspb.PortfolioValue{
                TotalValueUsd: "10000.00",
                Change24H:     "+5.2",
            },
        }, nil
    }
    
    req := &holdingspb.GetPortfolioValueRequest{
        UserId:         userID,
        OrganizationId: orgID,
        IncludeHistory: includeHistory,
    }
    
    resp, err := c.client.GetPortfolioValue(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get portfolio value failed: %w", err)
    }
    
    return resp, nil
}

// Get staked balance
func (c *HoldingsClient) GetStakedBalance(ctx context.Context, userID, assetID, orgID string) ([]*holdingspb.StakedBalance, error) {
    if c.client == nil {
        return []*holdingspb.StakedBalance{}, nil
    }
    
    req := &holdingspb.GetStakedBalanceRequest{
        UserId:         userID,
        AssetId:        assetID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetStakedBalance(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get staked balance failed: %w", err)
    }
    
    return resp.StakedBalances, nil
}

// Get locked balance
func (c *HoldingsClient) GetLockedBalance(ctx context.Context, userID, assetID, orgID string) ([]*holdingspb.LockedBalance, error) {
    if c.client == nil {
        return []*holdingspb.LockedBalance{}, nil
    }
    
    req := &holdingspb.GetLockedBalanceRequest{
        UserId:         userID,
        AssetId:        assetID,
        OrganizationId: orgID,
        IncludeExpired: false,
    }
    
    resp, err := c.client.GetLockedBalance(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get locked balance failed: %w", err)
    }
    
    return resp.LockedBalances, nil
}

// Reconcile holdings
func (c *HoldingsClient) ReconcileHoldings(ctx context.Context, userID, orgID string, assetIDs []string, autoCorrect bool) (*holdingspb.ReconcileHoldingsResponse, error) {
    if c.client == nil {
        return &holdingspb.ReconcileHoldingsResponse{
            ReconciliationId: "test-recon-id",
            AllMatched:       true,
        }, nil
    }
    
    req := &holdingspb.ReconcileHoldingsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetIds:       assetIDs,
        AutoCorrect:    autoCorrect,
    }
    
    resp, err := c.client.ReconcileHoldings(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("reconcile holdings failed: %w", err)
    }
    
    return resp, nil
}

// Mock functions for testing
func mockBalance(userID, assetID string) *holdingspb.Balance {
    return &holdingspb.Balance{
        UserId:          userID,
        AssetId:         assetID,
        AssetSymbol:     "TX",
        AvailableBalance: "1000.00",
        TotalBalance:    "1000.00",
        ValueUsd:        "1000.00",
        LastUpdated:     timestampNow(),
    }
}

func mockEpoch() *holdingspb.Epoch {
    return &holdingspb.Epoch{
        EpochNumber: 1,
        StartTime:   timestampNow(),
        IsClosed:    false,
    }
}

func timestampNow() *google_protobuf.Timestamp {
    return &google_protobuf.Timestamp{
        Seconds: time.Now().Unix(),
        Nanos:   int32(time.Now().Nanosecond()),
    }
}

// Example usage
func main() {
    client, err := NewHoldingsClient("holdings-store:50066")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    userID := "user-789"
    
    // Get user's current epoch
    epoch, err := client.GetCurrentEpoch(ctx, orgID)
    if err != nil {
        log.Printf("Failed to get current epoch: %v", err)
    } else {
        log.Printf("Current epoch: %d", epoch.EpochNumber)
    }
    
    // Update balance (credit)
    balance, err := client.UpdateBalance(ctx, userID, "asset-tx", "500.00", "credit", 
        "ref-123", "deposit", orgID, "Initial deposit")
    if err != nil {
        log.Printf("Failed to update balance: %v", err)
    } else {
        log.Printf("New balance: %s", balance.AvailableBalance)
    }
    
    // Get all holdings
    holdings, total, totalValue, err := client.GetHoldings(ctx, userID, orgID, true, 20, 0)
    if err != nil {
        log.Printf("Failed to get holdings: %v", err)
    } else {
        log.Printf("Total portfolio value: $%s", totalValue)
        log.Printf("Found %d holdings (total: %d)", len(holdings), total)
        
        for _, holding := range holdings {
            log.Printf("- %s: %s ($%s) - %s", 
                holding.AssetSymbol, 
                holding.TotalBalance, 
                holding.ValueUsd,
                holding.AllocationPercentage)
        }
    }
    
    // Get portfolio value with history
    portfolio, err := client.GetPortfolioValue(ctx, userID, orgID, true)
    if err != nil {
        log.Printf("Failed to get portfolio value: %v", err)
    } else {
        log.Printf("Current value: $%s (24h change: %s%%)", 
            portfolio.Current.TotalValueUsd, 
            portfolio.Current.Change24H)
    }
    
    // Transfer balance
    transfer, err := client.TransferBalance(ctx, userID, "user-456", "asset-tx", 
        "100.00", "transfer-123", "internal", orgID, "Payment for services")
    if err != nil {
        log.Printf("Failed to transfer: %v", err)
    } else if transfer.Success {
        log.Printf("Transfer successful: %s", transfer.TransferId)
    }
}
Docker Compose Example
bash
nano ~/dev/TXdocumentation/holdings/docker-compose.yml
yaml
version: '3.8'

services:
  holdings-service:
    image: sologenic/holdings-service:latest
    environment:
      - HOLDINGS_SERVICE_PORT=50066
      - HOLDINGS_STORE=holdings-store:50066
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=holdings
      - POSTGRES_USER=holdings_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - TIMESCALEDB_HOST=timescaledb
      - TIMESCALEDB_PORT=5432
      - TIMESCALEDB_DB=holdings_historical
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - CLICKHOUSE_HOST=clickhouse
      - CLICKHOUSE_PORT=9000
      - EPOCH_DURATION_HOURS=24
      - SNAPSHOT_RETENTION_DAYS=365
      - RECONCILIATION_ENABLED=true
      - PRICE_CACHE_TTL=60
      - LOG_LEVEL=info
    ports:
      - "50066:50066"
    networks:
      - internal
    depends_on:
      - postgres
      - timescaledb
      - redis
      - clickhouse
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50066"]
      interval: 30s
      timeout: 10s
      retries: 3

  holdings-store:
    image: sologenic/holdings-store:latest
    environment:
      - HOLDINGS_STORE_PORT=50067
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=holdings
      - POSTGRES_USER=holdings_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - TIMESCALEDB_HOST=timescaledb
      - TIMESCALEDB_PORT=5432
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50067:50067"
    networks:
      - internal
    depends_on:
      - postgres
      - timescaledb
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=holdings
      - POSTGRES_USER=holdings_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U holdings_user -d holdings"]
      interval: 10s
      timeout: 5s
      retries: 5

  timescaledb:
    image: timescale/timescaledb:latest-pg15
    environment:
      - POSTGRES_DB=holdings_historical
      - POSTGRES_USER=holdings_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - timescaledb_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U holdings_user -d holdings_historical"]
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
      - CLICKHOUSE_DB=holdings_analytics
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
Environment Setup (.env file)
bash
nano ~/dev/TXdocumentation/holdings/.env
bash
# Database Configuration
DB_PASSWORD=your_secure_password
CLICKHOUSE_PASSWORD=clickhouse_secure_password

# Service Configuration
HOLDINGS_STORE=holdings-store:50067
HOLDINGS_STORE_TESTING=FALSE

# Epoch Configuration
EPOCH_DURATION_HOURS=24
SNAPSHOT_RETENTION_DAYS=365

# Business Rules
MAX_HOLDINGS_PER_USER=1000
RECONCILIATION_ENABLED=true
PRICE_CACHE_TTL=60

# Logging
LOG_LEVEL=info
Testing Mode
The client automatically detects test mode when HOLDINGS_STORE_TESTING=TRUE is set:

bash
# Run in test mode
export HOLDINGS_STORE_TESTING=TRUE
go test ./...
Database Schema (Reference)
sql
-- Current holdings table
CREATE TABLE current_holdings (
    user_id VARCHAR(100),
    asset_id VARCHAR(100),
    available_balance DECIMAL(40,18),
    locked_balance DECIMAL(40,18),
    staked_balance DECIMAL(40,18),
    total_balance DECIMAL(40,18),
    last_updated TIMESTAMP,
    PRIMARY KEY (user_id, asset_id)
);

-- Epoch snapshots (TimescaleDB hypertable)
CREATE TABLE epoch_snapshots (
    user_id VARCHAR(100),
    asset_id VARCHAR(100),
    epoch_number BIGINT,
    balance DECIMAL(40,18),
    value_usd DECIMAL(40,18),
    snapshot_time TIMESTAMPTZ,
    is_final BOOLEAN
);

SELECT create_hypertable('epoch_snapshots', 'snapshot_time');
Error Handling
go
// Example error handling
resp, err := client.UpdateBalance(ctx, req)
if err != nil {
    if strings.Contains(err.Error(), "INSUFFICIENT_BALANCE") {
        // Handle insufficient funds
    } else if strings.Contains(err.Error(), "ASSET_NOT_FOUND") {
        // Handle unknown asset
    } else if strings.Contains(err.Error(), "EPOCH_CLOSED") {
        // Handle epoch closure
    }
    log.Printf("Error: %v", err)
}
License
This documentation is part of the TX Marketplace platform.
