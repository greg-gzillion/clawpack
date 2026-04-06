# Asset List Service (Asset Store)

The Asset List proto provides all the functionality required to interact with the asset store service. It enables management of asset metadata, pricing, margins, and network-specific configurations.

## Overview

The Asset List service is a comprehensive asset management system that stores and retrieves asset information across different networks and organizations. It supports asset discovery, margin calculations, price feeds, and network-specific configurations.

## Architecture
┌─────────────────────────────────────────────┐
│ Asset List Client │
│ (Go / TypeScript / gRPC) │
└─────────────────┬───────────────────────────┘
│ gRPC/HTTP
▼
┌─────────────────────────────────────────────┐
│ Asset Store Service │
│ - Asset Registry │
│ - Price Feeds │
│ - Margin Configuration │
│ - Network Mapping │
└─────────────────┬───────────────────────────┘
│
▼
┌─────────────────────────────────────────────┐
│ Storage Layer │
│ (PostgreSQL / Redis Cache) │
└─────────────────────────────────────────────┘

text

## Proto Definition

### Base Message Types

```protobuf
syntax = "proto3";

package asset.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Asset information
message Asset {
    string asset_id = 1;                // Unique asset identifier
    string symbol = 2;                  // Trading symbol (e.g., XRP, BTC)
    string name = 3;                    // Full asset name
    string issuer = 4;                  // Asset issuer address
    uint32 decimals = 5;                // Decimal places
    string asset_type = 6;              // native, token, nft, lp_token
    string network = 7;                 // mainnet, testnet, devnet
    string organization_id = 8;         // Organization isolation
    AssetStatus status = 9;             // Asset status
    AssetMargin margin = 10;            // Margin configuration
    AssetPrice price = 11;              // Current price
    map<string, string> metadata = 12;  // Additional metadata
    google.protobuf.Timestamp created_at = 13;
    google.protobuf.Timestamp updated_at = 14;
    string version = 15;
}

// Asset status
enum AssetStatus {
    STATUS_UNSPECIFIED = 0;
    STATUS_ACTIVE = 1;
    STATUS_SUSPENDED = 2;
    STATUS_DELISTED = 3;
    STATUS_PENDING = 4;
}

// Margin configuration for asset
message AssetMargin {
    double margin_percentage = 1;       // 0.75 = 75% margin requirement
    double liquidation_threshold = 2;   // Liquidation at 0.85 (85%)
    double maintenance_margin = 3;      // Maintenance requirement
    double initial_margin = 4;          // Initial margin requirement
    bool is_collateral = 5;             // Can be used as collateral
    double collateral_weight = 6;       // Weight for collateral calculation
    string margin_type = 7;             // fixed, percentage, dynamic
    map<string, double> tiered_margins = 8; // Volume-based tiers
}

// Asset price information
message AssetPrice {
    string asset_id = 1;
    string quote_asset = 2;             // e.g., WUSDC, XRP
    double price = 3;                   // Current price
    double change_24h = 4;              // 24-hour change percentage
    double volume_24h = 5;              // 24-hour volume
    double high_24h = 6;                // 24-hour high
    double low_24h = 7;                 // 24-hour low
    uint64 timestamp = 8;               // Unix timestamp
    string price_source = 9;            // oracle, dex, aggregated
    double confidence = 10;             // Price confidence score (0-1)
}

// Asset pair for trading
message AssetPair {
    string pair_id = 1;
    string base_asset = 2;
    string quote_asset = 3;
    double min_trade_size = 4;
    double max_trade_size = 5;
    double tick_size = 6;
    int32 price_precision = 7;
    int32 quantity_precision = 8;
    bool is_active = 9;
    AssetMargin pair_margin = 10;
}

// Request/Response messages
message GetAssetRequest {
    string asset_id = 1;
    string network = 2;
    string organization_id = 3;
}

message GetAssetResponse {
    Asset asset = 1;
    bool found = 2;
}

message ListAssetsRequest {
    string network = 1;
    string organization_id = 2;
    string asset_type = 3;
    AssetStatus status = 4;
    bool only_collateral = 5;
    int32 limit = 6;
    int32 offset = 7;
    string search = 8;                  // Search by symbol or name
    repeated string asset_ids = 9;      // Specific assets to fetch
}

message ListAssetsResponse {
    repeated Asset assets = 1;
    int64 total_count = 2;
}

message GetAssetPriceRequest {
    string asset_id = 1;
    string quote_asset = 2;
    string network = 3;
}

message GetAssetPriceResponse {
    AssetPrice price = 1;
    bool found = 2;
}

message GetMultiplePricesRequest {
    repeated string asset_ids = 1;
    string quote_asset = 2;
    string network = 3;
}

message GetMultiplePricesResponse {
    map<string, AssetPrice> prices = 1;
}

message CreateAssetRequest {
    Asset asset = 1;
}

message CreateAssetResponse {
    Asset asset = 1;
    bool created = 2;
}

message UpdateAssetRequest {
    string asset_id = 1;
    string network = 2;
    optional AssetMargin margin = 3;
    optional AssetStatus status = 4;
    optional map<string, string> metadata = 5;
}

message UpdateAssetResponse {
    Asset asset = 1;
    bool updated = 2;
}

message UpdateAssetPriceRequest {
    string asset_id = 1;
    string quote_asset = 2;
    double price = 3;
    string price_source = 4;
    uint64 timestamp = 5;
}

message UpdateAssetPriceResponse {
    AssetPrice price = 1;
    bool updated = 2;
}

message GetAssetMarginRequest {
    string asset_id = 1;
    string network = 2;
    optional double volume_30d = 3;     // For tiered margins
}

message GetAssetMarginResponse {
    AssetMargin margin = 1;
    double effective_margin = 2;        // After tier adjustments
}

message BatchGetAssetsRequest {
    repeated string asset_ids = 1;
    string network = 2;
    string organization_id = 3;
}

message BatchGetAssetsResponse {
    map<string, Asset> assets = 1;
}

// Service definition
service AssetService {
    // Asset management
    rpc GetAsset(GetAssetRequest) returns (GetAssetResponse);
    rpc ListAssets(ListAssetsRequest) returns (ListAssetsResponse);
    rpc CreateAsset(CreateAssetRequest) returns (CreateAssetResponse);
    rpc UpdateAsset(UpdateAssetRequest) returns (UpdateAssetResponse);
    rpc BatchGetAssets(BatchGetAssetsRequest) returns (BatchGetAssetsResponse);
    
    // Price management
    rpc GetAssetPrice(GetAssetPriceRequest) returns (GetAssetPriceResponse);
    rpc GetMultiplePrices(GetMultiplePricesRequest) returns (GetMultiplePricesResponse);
    rpc UpdateAssetPrice(UpdateAssetPriceRequest) returns (UpdateAssetPriceResponse);
    
    // Margin calculations
    rpc GetAssetMargin(GetAssetMarginRequest) returns (GetAssetMarginResponse);
    rpc CalculateCollateralValue(CalculateCollateralRequest) returns (CalculateCollateralResponse);
    
    // Asset pairs
    rpc GetAssetPair(GetAssetPairRequest) returns (GetAssetPairResponse);
    rpc ListAssetPairs(ListAssetPairsRequest) returns (ListAssetPairsResponse);
}

message CalculateCollateralRequest {
    map<string, double> asset_balances = 1;  // asset_id -> balance
    string network = 2;
    string quote_asset = 3;                   // Target quote asset
}

message CalculateCollateralResponse {
    double total_collateral_value = 1;        // In quote_asset
    repeated AssetCollateralBreakdown breakdown = 2;
}

message AssetCollateralBreakdown {
    string asset_id = 1;
    double balance = 2;
    double price = 3;
    double margin_rate = 4;
    double collateral_value = 5;
    double weight = 6;
}

message GetAssetPairRequest {
    string pair_id = 1;
    string network = 2;
}

message GetAssetPairResponse {
    AssetPair pair = 1;
    bool found = 2;
}

message ListAssetPairsRequest {
    string network = 1;
    bool only_active = 2;
    string base_asset = 3;
    string quote_asset = 4;
    int32 limit = 5;
    int32 offset = 6;
}

message ListAssetPairsResponse {
    repeated AssetPair pairs = 1;
    int64 total_count = 2;
}
Building the Protos
Build Script
Create bin/build.sh:

bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Asset List proto build...${NC}"

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
mkdir -p proto

# Generate Go files
echo -e "${BLUE}Generating Go protobuf files...${NC}"
protoc \
    --go_out=client/go \
    --go_opt=paths=source_relative \
    --go-grpc_out=client/go \
    --go-grpc_opt=paths=source_relative \
    --proto_path=proto \
    proto/asset.proto

# Generate TypeScript files (if Node.js available)
if command -v npm &> /dev/null; then
    echo -e "${BLUE}Generating TypeScript protobuf files...${NC}"
    
    # Install required packages if not present
    if [ ! -f "node_modules/.bin/protoc-gen-ts" ]; then
        echo -e "${YELLOW}Installing protoc-gen-ts...${NC}"
        npm install -g protoc-gen-ts
    fi
    
    if [ ! -f "node_modules/.bin/protoc-gen-grpc-web" ]; then
        echo -e "${YELLOW}Installing protoc-gen-grpc-web...${NC}"
        npm install -g protoc-gen-grpc-web
    fi
    
    protoc \
        --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
        --ts_out=client/typescript \
        --proto_path=proto \
        proto/asset.proto
    
    protoc \
        --plugin=protoc-gen-grpc-web=./node_modules/.bin/protoc-gen-grpc-web \
        --grpc-web_out=import_style=typescript,mode=grpcwebtext:client/typescript \
        --proto_path=proto \
        proto/asset.proto
else
    echo -e "${YELLOW}Skipping TypeScript generation (npm not available)${NC}"
fi

# Generate documentation
echo -e "${BLUE}Generating documentation...${NC}"
if command -v protoc-gen-doc &> /dev/null; then
    protoc \
        --doc_out=build \
        --doc_opt=markdown,asset-api.md \
        --proto_path=proto \
        proto/asset.proto
else
    echo -e "${YELLOW}Skipping documentation generation (protoc-gen-doc not installed)${NC}"
fi

# Add generated files to git
echo -e "${YELLOW}Adding generated files to git...${NC}"
git add client/go/*.go 2>/dev/null || true
git add client/typescript/*.ts 2>/dev/null || true
git add build/ 2>/dev/null || true

echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}Generated files:${NC}"
echo "  - client/go/asset.pb.go"
echo "  - client/go/asset_grpc.pb.go"
echo "  - client/typescript/asset.ts"
echo "  - build/asset-api.md"

# Show file sizes
echo -e "\n${BLUE}File sizes:${NC}"
ls -lh client/go/*.pb.go 2>/dev/null || echo "Go files not found"
ls -lh client/typescript/*.ts 2>/dev/null || echo "TypeScript files not found"
Make the script executable:

bash
chmod +x bin/build.sh
Run Build
bash
./bin/build.sh
Client Implementation
Go Client
go
package main

import (
    "context"
    "log"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    
    pb "github.com/sologenic/asset-list/client/go"
)

type AssetClient struct {
    client pb.AssetServiceClient
    conn   *grpc.ClientConn
}

func NewAssetClient(addr string) (*AssetClient, error) {
    conn, err := grpc.Dial(addr, 
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
    )
    if err != nil {
        return nil, err
    }
    
    return &AssetClient{
        client: pb.NewAssetServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *AssetClient) Close() error {
    return c.conn.Close()
}

// Get asset information
func (c *AssetClient) GetAsset(ctx context.Context, assetID, network, orgID string) (*pb.Asset, error) {
    resp, err := c.client.GetAsset(ctx, &pb.GetAssetRequest{
        AssetId:        assetID,
        Network:        network,
        OrganizationId: orgID,
    })
    if err != nil {
        return nil, err
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Asset, nil
}

// List assets with filters
func (c *AssetClient) ListAssets(ctx context.Context, network, orgID string, onlyCollateral bool) ([]*pb.Asset, error) {
    var allAssets []*pb.Asset
    offset := int32(0)
    limit := int32(100)
    
    for {
        resp, err := c.client.ListAssets(ctx, &pb.ListAssetsRequest{
            Network:        network,
            OrganizationId: orgID,
            OnlyCollateral: onlyCollateral,
            Limit:          limit,
            Offset:         offset,
        })
        if err != nil {
            return nil, err
        }
        
        allAssets = append(allAssets, resp.Assets...)
        
        if int64(offset+limit) >= resp.TotalCount {
            break
        }
        offset += limit
    }
    
    return allAssets, nil
}

// Get asset price
func (c *AssetClient) GetAssetPrice(ctx context.Context, assetID, quoteAsset, network string) (*pb.AssetPrice, error) {
    resp, err := c.client.GetAssetPrice(ctx, &pb.GetAssetPriceRequest{
        AssetId:    assetID,
        QuoteAsset: quoteAsset,
        Network:    network,
    })
    if err != nil {
        return nil, err
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Price, nil
}

// Get multiple prices
func (c *AssetClient) GetMultiplePrices(ctx context.Context, assetIDs []string, quoteAsset, network string) (map[string]*pb.AssetPrice, error) {
    resp, err := c.client.GetMultiplePrices(ctx, &pb.GetMultiplePricesRequest{
        AssetIds:   assetIDs,
        QuoteAsset: quoteAsset,
        Network:    network,
    })
    if err != nil {
        return nil, err
    }
    
    return resp.Prices, nil
}

// Calculate collateral value
func (c *AssetClient) CalculateCollateralValue(ctx context.Context, balances map[string]float64, network, quoteAsset string) (float64, error) {
    resp, err := c.client.CalculateCollateralValue(ctx, &pb.CalculateCollateralRequest{
        AssetBalances: balances,
        Network:       network,
        QuoteAsset:    quoteAsset,
    })
    if err != nil {
        return 0, err
    }
    
    return resp.TotalCollateralValue, nil
}

// Get asset margin with tiering
func (c *AssetClient) GetAssetMargin(ctx context.Context, assetID, network string, volume30d *float64) (float64, error) {
    req := &pb.GetAssetMarginRequest{
        AssetId: assetID,
        Network: network,
    }
    
    if volume30d != nil {
        req.Volume30d = volume30d
    }
    
    resp, err := c.client.GetAssetMargin(ctx, req)
    if err != nil {
        return 0, err
    }
    
    return resp.EffectiveMargin, nil
}

// Example usage
func main() {
    client, err := NewAssetClient("asset-store:50055")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    
    // Get XRP asset info
    xrp, err := client.GetAsset(ctx, "XRP", "mainnet", "org-123")
    if err != nil {
        log.Printf("Error getting XRP: %v", err)
    } else if xrp != nil {
        log.Printf("XRP Symbol: %s, Name: %s", xrp.Symbol, xrp.Name)
        log.Printf("Margin: %.2f%%", xrp.Margin.MarginPercentage*100)
    }
    
    // Get current price
    price, err := client.GetAssetPrice(ctx, "XRP", "WUSDC", "mainnet")
    if err != nil {
        log.Printf("Error getting price: %v", err)
    } else if price != nil {
        log.Printf("XRP Price: %.4f WUSDC", price.Price)
        log.Printf("24h Change: %.2f%%", price.Change24H)
    }
    
    // Calculate collateral value
    balances := map[string]float64{
        "XRP":  1000.0,
        "BTC":  0.5,
        "WUSDC": 5000.0,
    }
    
    collateral, err := client.CalculateCollateralValue(ctx, balances, "mainnet", "WUSDC")
    if err != nil {
        log.Printf("Error calculating collateral: %v", err)
    } else {
        log.Printf("Total collateral value: %.2f WUSDC", collateral)
    }
}
TypeScript Client
typescript
import { AssetServiceClient } from './client/typescript/asset_grpc_web_pb';
import {
    GetAssetRequest,
    ListAssetsRequest,
    GetAssetPriceRequest,
    GetMultiplePricesRequest,
    CalculateCollateralRequest,
    Asset,
    AssetPrice
} from './client/typescript/asset_pb';

class AssetListClient {
    private client: AssetServiceClient;
    
    constructor(serviceUrl: string) {
        this.client = new AssetServiceClient(serviceUrl);
    }
    
    // Get asset information
    async getAsset(assetId: string, network: string, organizationId: string): Promise<Asset | null> {
        return new Promise((resolve, reject) => {
            const request = new GetAssetRequest();
            request.setAssetId(assetId);
            request.setNetwork(network);
            request.setOrganizationId(organizationId);
            
            this.client.getAsset(request, (err, response) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                resolve(response.getFound() ? response.getAsset() : null);
            });
        });
    }
    
    // List assets
    async listAssets(
        network: string, 
        organizationId: string, 
        options?: { onlyCollateral?: boolean; limit?: number; offset?: number }
    ): Promise<{ assets: Asset[]; totalCount: number }> {
        return new Promise((resolve, reject) => {
            const request = new ListAssetsRequest();
            request.setNetwork(network);
            request.setOrganizationId(organizationId);
            
            if (options?.onlyCollateral) {
                request.setOnlyCollateral(options.onlyCollateral);
            }
            if (options?.limit) {
                request.setLimit(options.limit);
            }
            if (options?.offset) {
                request.setOffset(options.offset);
            }
            
            this.client.listAssets(request, (err, response) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                resolve({
                    assets: response.getAssetsList(),
                    totalCount: response.getTotalCount()
                });
            });
        });
    }
    
    // Get asset price
    async getAssetPrice(assetId: string, quoteAsset: string, network: string): Promise<AssetPrice | null> {
        return new Promise((resolve, reject) => {
            const request = new GetAssetPriceRequest();
            request.setAssetId(assetId);
            request.setQuoteAsset(quoteAsset);
            request.setNetwork(network);
            
            this.client.getAssetPrice(request, (err, response) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                resolve(response.getFound() ? response.getPrice() : null);
            });
        });
    }
    
    // Get multiple prices
    async getMultiplePrices(assetIds: string[], quoteAsset: string, network: string): Promise<Map<string, AssetPrice>> {
        return new Promise((resolve, reject) => {
            const request = new GetMultiplePricesRequest();
            request.setAssetIdsList(assetIds);
            request.setQuoteAsset(quoteAsset);
            request.setNetwork(network);
            
            this.client.getMultiplePrices(request, (err, response) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                const pricesMap = response.getPricesMap();
                resolve(pricesMap);
            });
        });
    }
    
    // Calculate collateral value
    async calculateCollateralValue(
        balances: Map<string, number>, 
        network: string, 
        quoteAsset: string
    ): Promise<{ totalValue: number; breakdown: any[] }> {
        return new Promise((resolve, reject) => {
            const request = new CalculateCollateralRequest();
            request.setAssetBalancesMap(balances);
            request.setNetwork(network);
            request.setQuoteAsset(quoteAsset);
            
            this.client.calculateCollateralValue(request, (err, response) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                resolve({
                    totalValue: response.getTotalCollateralValue(),
                    breakdown: response.getBreakdownList()
                });
            });
        });
    }
}

// React hook for asset prices
import { useEffect, useState } from 'react';

function useAssetPrices(assetIds: string[], quoteAsset: string = 'WUSDC') {
    const [prices, setPrices] = useState<Map<string, AssetPrice>>(new Map());
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    
    useEffect(() => {
        const client = new AssetListClient(process.env.REACT_APP_ASSET_STORE_URL!);
        
        async function fetchPrices() {
            try {
                setLoading(true);
                const priceMap = await client.getMultiplePrices(
                    assetIds, 
                    quoteAsset, 
                    process.env.REACT_APP_NETWORK!
                );
                setPrices(priceMap);
                setError(null);
            } catch (err) {
                setError(err as Error);
            } finally {
                setLoading(false);
            }
        }
        
        if (assetIds.length > 0) {
            fetchPrices();
        }
        
        // Refresh every 30 seconds
        const interval = setInterval(fetchPrices, 30000);
        return () => clearInterval(interval);
    }, [assetIds.join(','), quoteAsset]);
    
    return { prices, loading, error };
}

// Component example
function AssetPriceTicker({ assetIds }: { assetIds: string[] }) {
    const { prices, loading, error } = useAssetPrices(assetIds);
    
    if (loading) return <div>Loading prices...</div>;
    if (error) return <div>Error: {error.message}</div>;
    
    return (
        <div className="price-ticker">
            {Array.from(prices.entries()).map(([assetId, price]) => (
                <div key={assetId} className="price-item">
                    <span className="symbol">{assetId}</span>
                    <span className="price">${price.getPrice()}</span>
                    <span className={`change ${price.getChange24H() >= 0 ? 'positive' : 'negative'}`}>
                        {price.getChange24H()}%
                    </span>
                </div>
            ))}
        </div>
    );
}

export { AssetListClient, useAssetPrices, AssetPriceTicker };
Environment Configuration
Required Environment Variables
Variable	Description	Example
ASSET_STORE_ENDPOINT	Asset store gRPC endpoint	asset-store:50055
ASSET_STORE_DB_HOST	Database host	postgres.example.com
ASSET_STORE_DB_NAME	Database name	asset_store
ASSET_STORE_DB_USER	Database user	asset_user
ASSET_STORE_DB_PASSWORD	Database password	${DB_PASSWORD}
Optional Environment Variables
Variable	Description	Default
ASSET_STORE_CACHE_TTL	Cache TTL in seconds	30
ASSET_STORE_PRICE_UPDATE_INTERVAL	Price update interval	10
ASSET_STORE_MAX_BATCH_SIZE	Maximum batch size	100
LOG_LEVEL	Logging level	info
Docker Compose Example
yaml
version: '3.8'

services:
  asset-store:
    image: sologenic/asset-store:latest
    environment:
      - ASSET_STORE_ENDPOINT=:50055
      - ASSET_STORE_DB_HOST=postgres
      - ASSET_STORE_DB_NAME=asset_store
      - ASSET_STORE_DB_USER=asset_user
      - ASSET_STORE_DB_PASSWORD=${DB_PASSWORD}
      - ASSET_STORE_CACHE_TTL=30
      - ASSET_STORE_PRICE_UPDATE_INTERVAL=10
      - LOG_LEVEL=info
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50055:50055"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50055"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=asset_store
      - POSTGRES_USER=asset_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U asset_user -d asset_store"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - internal
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Price feed oracle (example)
  price-oracle:
    image: sologenic/price-oracle:latest
    environment:
      - ASSET_STORE_ENDPOINT=asset-store:50055
      - ORACLE_SOURCES=coingecko,binance,kraken
      - UPDATE_INTERVAL=10
    networks:
      - internal
    depends_on:
      - asset-store

networks:
  internal:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
Database Initialization Script (init.sql)
sql
-- Create asset store tables
CREATE TABLE IF NOT EXISTS assets (
    asset_id VARCHAR(100) PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    issuer VARCHAR(100),
    decimals INT DEFAULT 0,
    asset_type VARCHAR(50),
    network VARCHAR(20) NOT NULL,
    organization_id VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    margin_percentage DECIMAL(10,4),
    liquidation_threshold DECIMAL(10,4),
    maintenance_margin DECIMAL(10,4),
    initial_margin DECIMAL(10,4),
    is_collateral BOOLEAN DEFAULT false,
    collateral_weight DECIMAL(10,4),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version VARCHAR(20),
    UNIQUE(asset_id, network, organization_id)
);

CREATE TABLE IF NOT EXISTS asset_prices (
    id SERIAL PRIMARY KEY,
    asset_id VARCHAR(100) NOT NULL,
    quote_asset VARCHAR(20) NOT NULL,
    price DECIMAL(30,15) NOT NULL,
    change_24h DECIMAL(10,4),
    volume_24h DECIMAL(30,2),
    high_24h DECIMAL(30,15),
    low_24h DECIMAL(30,15),
    price_source VARCHAR(50),
    confidence DECIMAL(3,2),
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(asset_id, quote_asset, timestamp),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

CREATE TABLE IF NOT EXISTS asset_pairs (
    pair_id VARCHAR(100) PRIMARY KEY,
    base_asset VARCHAR(100) NOT NULL,
    quote_asset VARCHAR(100) NOT NULL,
    min_trade_size DECIMAL(30,15),
    max_trade_size DECIMAL(30,15),
    tick_size DECIMAL(30,15),
    price_precision INT,
    quantity_precision INT,
    is_active BOOLEAN DEFAULT true,
    margin_percentage DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (base_asset) REFERENCES assets(asset_id),
    FOREIGN KEY (quote_asset) REFERENCES assets(asset_id)
);

CREATE INDEX idx_assets_network ON assets(network);
CREATE INDEX idx_assets_organization ON assets(organization_id);
CREATE INDEX idx_assets_symbol ON assets(symbol);
CREATE INDEX idx_assets_status ON assets(status);
CREATE INDEX idx_asset_prices_asset ON asset_prices(asset_id);
CREATE INDEX idx_asset_prices_timestamp ON asset_prices(timestamp);
CREATE INDEX idx_asset_pairs_base ON asset_pairs(base_asset);
CREATE INDEX idx_asset_pairs_quote ON asset_pairs(quote_asset);

-- Insert default assets
INSERT INTO assets (asset_id, symbol, name, asset_type, network, organization_id, is_collateral, collateral_weight, margin_percentage)
VALUES 
    ('XRP', 'XRP', 'XRP', 'native', 'mainnet', 'default', true, 1.0, 0.75),
    ('WUSDC', 'WUSDC', 'Wrapped USDC', 'token', 'mainnet', 'default', true, 1.0, 1.0),
    ('BTC', 'BTC', 'Bitcoin', 'token', 'mainnet', 'default', true, 0.85, 0.65)
ON CONFLICT (asset_id, network, organization_id) DO NOTHING;

-- Create update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_assets_updated_at 
    BEFORE UPDATE ON assets 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
Error Handling
Common Error Codes
Code	Description	Handling
404	Asset not found	Return null, don't throw
400	Invalid request parameters	Validate inputs before calling
409	Asset already exists	Check existence before create
429	Rate limit exceeded	Implement exponential backoff
503	Service unavailable	Circuit breaker pattern
Go Error Handler
go
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

type AssetErrorHandler struct {
    retryCount int
    backoff    time.Duration
}

func (h *AssetErrorHandler) HandleGetAssetError(err error) error {
    if err == nil {
        return nil
    }
    
    st, ok := status.FromError(err)
    if !ok {
        return fmt.Errorf("non-gRPC error: %w", err)
    }
    
    switch st.Code() {
    case codes.NotFound:
        return nil // Asset not found is not an error
    case codes.InvalidArgument:
        return fmt.Errorf("invalid request: %s", st.Message())
    case codes.PermissionDenied:
        return fmt.Errorf("permission denied: %s", st.Message())
    case codes.Unavailable:
        return h.handleUnavailable(err)
    default:
        return fmt.Errorf("unexpected error: %s", st.Message())
    }
}

func (h *AssetErrorHandler) handleUnavailable(err error) error {
    if h.retryCount < 3 {
        h.retryCount++
        time.Sleep(h.backoff)
        h.backoff *= 2
        return err // Retry
    }
    return fmt.Errorf("service unavailable after retries: %w", err)
}
Testing
Unit Test Example (Go)
go
package asset_test

import (
    "context"
    "testing"
    
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
    
    pb "github.com/sologenic/asset-list/client/go"
)

type MockAssetClient struct {
    mock.Mock
}

func (m *MockAssetClient) GetAsset(ctx context.Context, req *pb.GetAssetRequest) (*pb.GetAssetResponse, error) {
    args := m.Called(ctx, req)
    return args.Get(0).(*pb.GetAssetResponse), args.Error(1)
}

func TestGetAsset(t *testing.T) {
    mockClient := new(MockAssetClient)
    
    expectedAsset := &pb.Asset{
        AssetId: "XRP",
        Symbol:  "XRP",
        Name:    "XRP",
    }
    
    mockClient.On("GetAsset", mock.Anything, mock.Anything).Return(&pb.GetAssetResponse{
        Asset: expectedAsset,
        Found: true,
    }, nil)
    
    ctx := context.Background()
    resp, err := mockClient.GetAsset(ctx, &pb.GetAssetRequest{
 AssetId: "XRP",
        Network: "mainnet",
    })
    
    assert.NoError(t, err)
    assert.True(t, resp.Found)
    assert.Equal(t, "XRP", resp.Asset.Symbol)
    
    mockClient.AssertExpectations(t)
}

func TestCalculateCollateralValue(t *testing.T) {
    client := &AssetClient{}
    
    balances := map[string]float64{
        "XRP":   1000,
        "WUSDC": 5000,
    }
    
    value, err := client.CalculateCollateralValue(context.Background(), balances, "mainnet", "WUSDC")
    
    assert.NoError(t, err)
    assert.Greater(t, value, 0.0)
    assert.Less(t, value, 100000.0)
}
Performance Optimization
Cached Asset Client
go
type CachedAssetClient struct {
    client    *AssetClient
    cache     *redis.Client
    cacheTTL  time.Duration
}

func (c *CachedAssetClient) GetAsset(ctx context.Context, assetID, network, orgID string) (*pb.Asset, error) {
    // Try cache first
    cacheKey := fmt.Sprintf("asset:%s:%s:%s", assetID, network, orgID)
    cached, err := c.cache.Get(ctx, cacheKey).Bytes()
    if err == nil {
        var asset pb.Asset
        if err := proto.Unmarshal(cached, &asset); err == nil {
            return &asset, nil
        }
    }
    
    // Fetch from service
    asset, err := c.client.GetAsset(ctx, assetID, network, orgID)
    if err != nil {
        return nil, err
    }
    
    // Cache for TTL
    if asset != nil {
        data, _ := proto.Marshal(asset)
        c.cache.Set(ctx, cacheKey, data, c.cacheTTL)
    }
    
    return asset, nil
}

// Batch price fetching
func (c *CachedAssetClient) GetMultiplePricesBatch(ctx context.Context, assetIDs []string, quoteAsset, network string) (map[string]*pb.AssetPrice, error) {
    results := make(map[string]*pb.AssetPrice)
    uncached := make([]string, 0)
    
    // Check cache
    for _, assetID := range assetIDs {
        cacheKey := fmt.Sprintf("price:%s:%s:%s", assetID, quoteAsset, network)
        cached, err := c.cache.Get(ctx, cacheKey).Bytes()
        if err == nil {
            var price pb.AssetPrice
            if err := proto.Unmarshal(cached, &price); err == nil {
                results[assetID] = &price
                continue
            }
        }
        uncached = append(uncached, assetID)
    }
    
    // Fetch uncached from service
    if len(uncached) > 0 {
        prices, err := c.client.GetMultiplePrices(ctx, uncached, quoteAsset, network)
        if err != nil {
            return results, err
        }
        
        for assetID, price := range prices {
            results[assetID] = price
            data, _ := proto.Marshal(price)
            cacheKey := fmt.Sprintf("price:%s:%s:%s", assetID, quoteAsset, network)
            c.cache.Set(ctx, cacheKey, data, 30*time.Second)
        }
    }
    
    return results, nil
}
Best Practices
Asset Management
Always use organization_id for multi-tenant isolation

Implement asset versioning for schema changes

Regularly update price feeds with confidence scores

Use tiered margins for high-volume traders

Performance
Cache asset data with appropriate TTL (30 seconds recommended)

Batch requests when possible (max 100 assets per batch)

Implement pagination for list endpoints

Use connection pooling for database

Security
Validate all asset IDs before processing

Implement rate limiting by organization

Use TLS for gRPC in production

Sanitize metadata inputs

Data Integrity
Maintain referential integrity for asset pairs

Log all margin calculation changes

Implement soft deletes for asset delisting

Regular reconciliation of price feeds

Troubleshooting
Issue	Possible Cause	Solution
Asset not found	Wrong network or org ID	Verify parameters match asset configuration
Incorrect margin	Volume tier not applied	Pass 30-day volume parameter
Stale prices	Cache not invalidating	Reduce cache TTL or implement push updates
High latency	Missing database indexes	Create indexes on frequently queried fields
Rate limiting	Too many requests	Implement batch requests and caching
Connection refused	Service not running	Verify service health and port availability
License
This documentation is part of the TX Marketplace platform.
