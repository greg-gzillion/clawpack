# Asset Epoch Data (AED) Model

The Asset Epoch Data model provides a complete proto-based service for managing asset epoch data across the platform. It offers both Go and TypeScript clients for seamless integration.

## Overview

AED (Asset Epoch Data) is a gRPC-based service that manages epoch-specific asset data, including pricing, metadata, and state changes over time. It provides versioned data storage and retrieval with support for different networks and organizations.

## Architecture
┌─────────────────────────────────────────────┐
│ AED Service Client │
│ (Go / TypeScript with auto-initialization) │
└─────────────────┬───────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────┐
│ AED Service │
│ (Proto-defined endpoints) │
└─────────────────┬───────────────────────────┘
│
▼
┌─────────────────────────────────────────────┐
│ AED Store (Backend) │
│ (Persistent or In-memory for testing) │
└─────────────────────────────────────────────┘

text

## Proto Definition

### Base Message Types

```protobuf
syntax = "proto3";

package aed.v1;

import "google/protobuf/timestamp.proto";

// Asset Epoch Data message
message AssetEpochData {
    string asset_id = 1;           // Unique asset identifier
    uint64 epoch = 2;               // Epoch number
    string network = 3;             // Network (mainnet, testnet, devnet)
    string organization_id = 4;     // Organization isolation
    AssetMetadata metadata = 5;     // Asset metadata
    AssetPrices prices = 6;         // Price data for epoch
    AssetState state = 7;           // State changes
    google.protobuf.Timestamp created_at = 8;
    google.protobuf.Timestamp updated_at = 9;
    string version = 10;            // Data schema version
}

// Asset metadata
message AssetMetadata {
    string name = 1;
    string symbol = 2;
    uint32 decimals = 3;
    string asset_type = 4;          // token, nft, lp_token, etc.
    string issuer = 5;              // Asset issuer address
    string uri = 6;                 // Metadata URI
    map<string, string> properties = 7;
}

// Price data for an epoch
message AssetPrices {
    double open = 1;
    double high = 2;
    double low = 3;
    double close = 4;
    double volume = 5;
    string quote_asset = 6;         // e.g., "WUSDC", "XRP"
    uint64 timestamp = 7;           // Unix timestamp
    map<string, double> additional_prices = 8; // Other pairs
}

// Asset state tracking
message AssetState {
    bool is_active = 1;
    bool is_frozen = 2;
    string status = 3;              // active, paused, delisted
    map<string, string> state_data = 4;
    repeated StateTransition transitions = 5;
}

message StateTransition {
    string from_state = 1;
    string to_state = 2;
    google.protobuf.Timestamp transition_time = 3;
    string reason = 4;
    string initiated_by = 5;
}

// Request/Response messages
message GetAssetEpochDataRequest {
    string asset_id = 1;
    uint64 epoch = 2;
    string network = 3;
    string organization_id = 4;
}

message GetAssetEpochDataResponse {
    AssetEpochData data = 1;
    bool found = 2;
}

message ListAssetEpochDataRequest {
    string asset_id = 1;
    string network = 2;
    string organization_id = 3;
    uint64 from_epoch = 4;
    uint64 to_epoch = 5;
    int32 limit = 6;
    int32 offset = 7;
}

message ListAssetEpochDataResponse {
    repeated AssetEpochData data = 1;
    int64 total_count = 2;
}

message CreateAssetEpochDataRequest {
    AssetEpochData data = 1;
}

message CreateAssetEpochDataResponse {
    AssetEpochData data = 1;
    bool created = 2;
}

message UpdateAssetEpochDataRequest {
    string asset_id = 1;
    uint64 epoch = 2;
    string network = 3;
    AssetPrices prices = 4;
    AssetState state = 5;
    AssetMetadata metadata = 6;
}

message UpdateAssetEpochDataResponse {
    AssetEpochData data = 1;
    bool updated = 2;
}

message DeleteAssetEpochDataRequest {
    string asset_id = 1;
    uint64 epoch = 2;
    string network = 3;
    string organization_id = 4;
}

message DeleteAssetEpochDataResponse {
    bool deleted = 1;
}

message BatchCreateRequest {
    repeated AssetEpochData data = 1;
    string organization_id = 2;
}

message BatchCreateResponse {
    int32 successful = 1;
    int32 failed = 2;
    repeated string errors = 3;
}

// Service definition
service AEDService {
    rpc GetAssetEpochData(GetAssetEpochDataRequest) returns (GetAssetEpochDataResponse);
    rpc ListAssetEpochData(ListAssetEpochDataRequest) returns (ListAssetEpochDataResponse);
    rpc CreateAssetEpochData(CreateAssetEpochDataRequest) returns (CreateAssetEpochDataResponse);
    rpc UpdateAssetEpochData(UpdateAssetEpochDataRequest) returns (UpdateAssetEpochDataResponse);
    rpc DeleteAssetEpochData(DeleteAssetEpochDataRequest) returns (DeleteAssetEpochDataResponse);
    rpc BatchCreate(BatchCreateRequest) returns (BatchCreateResponse);
    
    // Additional utility endpoints
    rpc GetLatestEpoch(GetLatestEpochRequest) returns (GetLatestEpochResponse);
    rpc GetEpochRange(GetEpochRangeRequest) returns (GetEpochRangeResponse);
}
Environment Configuration
Required Environment Variables
Variable	Description	Example
AED_STORE	Host:port of the AED store service	aed-store:50051
AED_STORE_TESTING	Enable test mode with in-memory buffer (value must be "TRUE")	TRUE
Behavior
If AED_STORE is set: Client connects to the specified AED store service

If AED_STORE_TESTING=TRUE is set: Client starts in test mode with in-memory buffer

If neither is set: Client panics with initialization error

Client Setup
Go Client
go
package main

import (
    "context"
    "log"
    "time"
    
    aed "github.com/sologenic/aed-model/client/go"
    pb "github.com/sologenic/aed-model/proto"
)

func main() {
    // Client auto-initializes from environment variables
    // Set AED_STORE=aed-store:50051 or AED_STORE_TESTING=TRUE
    client := aed.NewClient()
    
    ctx := context.Background()
    
    // Create asset epoch data
    assetData := &pb.AssetEpochData{
        AssetId: "XRP-12345",
        Epoch: 100,
        Network: "mainnet",
        OrganizationId: "org-123",
        Metadata: &pb.AssetMetadata{
            Name: "XRP Token",
            Symbol: "XRP",
            Decimals: 6,
            AssetType: "token",
            Issuer: "rXXX...",
        },
        Prices: &pb.AssetPrices{
            Open: 0.50,
            High: 0.52,
            Low: 0.49,
            Close: 0.51,
            Volume: 1000000,
            QuoteAsset: "WUSDC",
            Timestamp: uint64(time.Now().Unix()),
        },
        State: &pb.AssetState{
            IsActive: true,
            IsFrozen: false,
            Status: "active",
        },
    }
    
    // Create
    createResp, err := client.CreateAssetEpochData(ctx, &pb.CreateAssetEpochDataRequest{
        Data: assetData,
    })
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("Created asset data: %v", createResp.Data)
    
    // Get
    getResp, err := client.GetAssetEpochData(ctx, &pb.GetAssetEpochDataRequest{
        AssetId: "XRP-12345",
        Epoch: 100,
        Network: "mainnet",
        OrganizationId: "org-123",
    })
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("Retrieved asset data: %v", getResp.Data)
    
    // List with range
    listResp, err := client.ListAssetEpochData(ctx, &pb.ListAssetEpochDataRequest{
        AssetId: "XRP-12345",
        Network: "mainnet",
        OrganizationId: "org-123",
        FromEpoch: 90,
        ToEpoch: 110,
        Limit: 20,
        Offset: 0,
    })
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("Found %d epochs", listResp.TotalCount)
    
    // Update prices
    updateResp, err := client.UpdateAssetEpochData(ctx, &pb.UpdateAssetEpochDataRequest{
        AssetId: "XRP-12345",
        Epoch: 100,
        Network: "mainnet",
        Prices: &pb.AssetPrices{
            Close: 0.52,
            High: 0.53,
        },
    })
    if err != nil {
        log.Fatal(err)
    }
    log.Printf("Updated asset data: %v", updateResp.Data)
}
TypeScript Client
typescript
import { AEDClient } from '@sologenic/aed-model/client';
import { AssetEpochData, AssetMetadata, AssetPrices, AssetState } from '@sologenic/aed-model/proto';

// Client auto-initializes from environment variables
// Set AED_STORE=aed-store:50051 or AED_STORE_TESTING=TRUE
const client = new AEDClient();

async function example() {
    // Create asset epoch data
    const assetData: AssetEpochData = {
        assetId: "XRP-12345",
        epoch: 100,
        network: "mainnet",
        organizationId: "org-123",
        metadata: {
            name: "XRP Token",
            symbol: "XRP",
            decimals: 6,
            assetType: "token",
            issuer: "rXXX...",
            uri: "https://example.com/metadata",
            properties: {}
        },
        prices: {
            open: 0.50,
            high: 0.52,
            low: 0.49,
            close: 0.51,
            volume: 1000000,
            quoteAsset: "WUSDC",
            timestamp: Math.floor(Date.now() / 1000),
            additionalPrices: {}
        },
        state: {
            isActive: true,
            isFrozen: false,
            status: "active",
            stateData: {},
            transitions: []
        },
        createdAt: undefined,
        updatedAt: undefined,
        version: "1.0"
    };
    
    // Create
    const createResp = await client.createAssetEpochData({
        data: assetData
    });
    console.log("Created:", createResp.data);
    
    // Get
    const getResp = await client.getAssetEpochData({
        assetId: "XRP-12345",
        epoch: 100,
        network: "mainnet",
        organizationId: "org-123"
    });
    console.log("Retrieved:", getResp.data);
    
    // List
    const listResp = await client.listAssetEpochData({
        assetId: "XRP-12345",
        network: "mainnet",
        organizationId: "org-123",
        fromEpoch: 90,
        toEpoch: 110,
        limit: 20,
        offset: 0
    });
    console.log(`Found ${listResp.totalCount} epochs`);
    
    // Update
    const updateResp = await client.updateAssetEpochData({
        assetId: "XRP-12345",
        epoch: 100,
        network: "mainnet",
        prices: {
            close: 0.52,
            high: 0.53
        }
    });
    console.log("Updated:", updateResp.data);
    
    // Batch create
    const batchResp = await client.batchCreate({
        data: [assetData, /* more assets */],
        organizationId: "org-123"
    });
    console.log(`Batch result: ${batchResp.successful} successful, ${batchResp.failed} failed`);
}

// React hook example
import { useEffect, useState } from 'react';

function useAssetEpochData(assetId: string, epoch: number, network: string) {
    const [data, setData] = useState<AssetEpochData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);
    
    useEffect(() => {
        const client = new AEDClient();
        
        async function fetchData() {
            try {
                setLoading(true);
                const response = await client.getAssetEpochData({
                    assetId,
                    epoch,
                    network,
                    organizationId: process.env.REACT_APP_ORG_ID!
                });
                setData(response.data);
                setError(null);
            } catch (err) {
                setError(err as Error);
            } finally {
                setLoading(false);
            }
        }
        
        fetchData();
    }, [assetId, epoch, network]);
    
    return { data, loading, error };
}

// Component using the hook
function AssetPriceChart({ assetId, network }: { assetId: string; network: string }) {
    const [epochs, setEpochs] = useState<AssetEpochData[]>([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        const client = new AEDClient();
        
        async function loadEpochs() {
            const response = await client.listAssetEpochData({
                assetId,
                network,
                organizationId: process.env.REACT_APP_ORG_ID!,
                limit: 100,
                offset: 0
            });
            setEpochs(response.data);
            setLoading(false);
        }
        
        loadEpochs();
    }, [assetId, network]);
    
    if (loading) return <div>Loading chart...</div>;
    
    return (
        <div className="price-chart">
            {epochs.map(epoch => (
                <div key={epoch.epoch}>
                    Epoch {epoch.epoch}: ${epoch.prices?.close}
                </div>
            ))}
        </div>
    );
}
Building Proto Files
Build Script
Create bin/build.sh:

bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AED proto build...${NC}"

# Create build directory
mkdir -p build
mkdir -p client/go
mkdir -p client/typescript

# Generate Go files
echo -e "${YELLOW}Generating Go protobuf files...${NC}"
protoc \
    --go_out=client/go \
    --go_opt=paths=source_relative \
    --go-grpc_out=client/go \
    --go-grpc_opt=paths=source_relative \
    proto/aed.proto

# Generate TypeScript files
echo -e "${YELLOW}Generating TypeScript protobuf files...${NC}"
protoc \
    --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
    --ts_out=client/typescript \
    --proto_path=proto \
    proto/aed.proto

# Generate gRPC-web TypeScript
protoc \
    --plugin=protoc-gen-grpc-web=./node_modules/.bin/protoc-gen-grpc-web \
    --grpc-web_out=import_style=typescript,mode=grpcwebtext:client/typescript \
    --proto_path=proto \
    proto/aed.proto

# Add generated files to git
echo -e "${YELLOW}Adding generated files to git...${NC}"
git add client/go/*.go
git add client/typescript/*.ts
git add build/

echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}Generated files:${NC}"
echo "  - client/go/aed.pb.go"
echo "  - client/go/aed_grpc.pb.go"
echo "  - client/typescript/aed.ts"
Make the script executable:

bash
chmod +x bin/build.sh
Run Build
bash
./bin/build.sh
Docker Compose Example
yaml
version: '3.8'

services:
  aed-service:
    image: sologenic/aed-service:latest
    environment:
      - AED_STORE=aed-store:50051
      - LOG_LEVEL=info
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=aed
      - DB_USER=aed_user
      - DB_PASSWORD=${DB_PASSWORD}
    ports:
      - "50051:50051"
    networks:
      - internal
    depends_on:
      - aed-store
      - postgres

  aed-store:
    image: sologenic/aed-store:latest
    environment:
      - STORE_TYPE=postgres
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=aed
      - DB_USER=aed_user
      - DB_PASSWORD=${DB_PASSWORD}
      - CACHE_TTL=300
    networks:
      - internal
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=aed
      - POSTGRES_USER=aed_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal

  # Test mode example (no persistent storage)
  aed-service-test:
    image: sologenic/aed-service:latest
    environment:
      - AED_STORE_TESTING=TRUE
      - LOG_LEVEL=debug
    ports:
      - "50052:50051"
    networks:
      - test

networks:
  internal:
    driver: bridge
  test:
    driver: bridge

volumes:
  postgres_data:
Error Handling
Go Error Examples
go
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

func handleErrors(err error) {
    if err == nil {
        return
    }
    
    st, ok := status.FromError(err)
    if !ok {
        log.Printf("Non-gRPC error: %v", err)
        return
    }
    
    switch st.Code() {
    case codes.NotFound:
        log.Printf("Asset epoch data not found: %v", st.Message())
    case codes.InvalidArgument:
        log.Printf("Invalid argument: %v", st.Message())
    case codes.PermissionDenied:
        log.Printf("Permission denied: %v", st.Message())
    case codes.Internal:
        log.Printf("Internal server error: %v", st.Message())
    default:
        log.Printf("Unknown error: %v", st.Message())
    }
}
TypeScript Error Examples
typescript
import { status } from '@grpc/grpc-js';

try {
    await client.getAssetEpochData(request);
} catch (error) {
    if (error.code === status.NOT_FOUND) {
        console.error("Asset epoch data not found:", error.details);
    } else if (error.code === status.INVALID_ARGUMENT) {
        console.error("Invalid argument:", error.details);
    } else if (error.code === status.PERMISSION_DENIED) {
        console.error("Permission denied:", error.details);
    } else if (error.code === status.INTERNAL) {
        console.error("Internal error:", error.details);
    } else {
        console.error("Unknown error:", error);
    }
}
Testing
Unit Test Example (Go)
go
package aed_test

import (
    "context"
    "testing"
    
    aed "github.com/sologenic/aed-model/client/go"
    pb "github.com/sologenic/aed-model/proto"
    "github.com/stretchr/testify/assert"
)

func TestAssetEpochData(t *testing.T) {
    // Set AED_STORE_TESTING=TRUE for test mode
    client := aed.NewClient()
    ctx := context.Background()
    
    testData := &pb.AssetEpochData{
        AssetId: "test-asset",
        Epoch: 1,
        Network: "testnet",
        OrganizationId: "test-org",
        Metadata: &pb.AssetMetadata{
            Name: "Test Asset",
            Symbol: "TEST",
        },
    }
    
    // Create
    createResp, err := client.CreateAssetEpochData(ctx, &pb.CreateAssetEpochDataRequest{
        Data: testData,
    })
    assert.NoError(t, err)
    assert.True(t, createResp.Created)
    
    // Get
    getResp, err := client.GetAssetEpochData(ctx, &pb.GetAssetEpochDataRequest{
        AssetId: "test-asset",
        Epoch: 1,
        Network: "testnet",
        OrganizationId: "test-org",
    })
    assert.NoError(t, err)
    assert.True(t, getResp.Found)
    assert.Equal(t, "Test Asset", getResp.Data.Metadata.Name)
    
    // Delete
    deleteResp, err := client.DeleteAssetEpochData(ctx, &pb.DeleteAssetEpochDataRequest{
        AssetId: "test-asset",
        Epoch: 1,
        Network: "testnet",
        OrganizationId: "test-org",
    })
    assert.NoError(t, err)
    assert.True(t, deleteResp.Deleted)
}
Performance Considerations
Caching Strategy
go
type CachedAEDClient struct {
    client *aed.AEDClient
    cache  *cache.Cache
}

func (c *CachedAEDClient) GetAssetEpochData(ctx context.Context, req *pb.GetAssetEpochDataRequest) (*pb.GetAssetEpochDataResponse, error) {
    // Cache key
    key := fmt.Sprintf("aed:%s:%d:%s:%s", req.AssetId, req.Epoch, req.Network, req.OrganizationId)
    
    // Check cache
    if cached, found := c.cache.Get(key); found {
        return cached.(*pb.GetAssetEpochDataResponse), nil
    }
    
    // Fetch from service
    resp, err := c.client.GetAssetEpochData(ctx, req)
    if err != nil {
        return nil, err
    }
    
    // Cache for 30 seconds
    c.cache.Set(key, resp, 30*time.Second)
    
    return resp, nil
}
Batch Operations
For better performance with multiple assets:

go
func batchGetAssets(ctx context.Context, client *aed.AEDClient, assets []AssetKey) (map[string]*pb.AssetEpochData, error) {
    results := make(map[string]*pb.AssetEpochData)
    
    // Process in batches of 100
    batchSize := 100
    for i := 0; i < len(assets); i += batchSize {
        end := i + batchSize
        if end > len(assets) {
            end = len(assets)
        }
        
        batch := assets[i:end]
        
        // Use batch create for multiple gets (if supported)
        // Or use goroutines for parallel fetching
        var wg sync.WaitGroup
        var mu sync.Mutex
        
        for _, asset := range batch {
            wg.Add(1)
            go func(asset AssetKey) {
                defer wg.Done()
                
                resp, err := client.GetAssetEpochData(ctx, &pb.GetAssetEpochDataRequest{
                    AssetId: asset.ID,
                    Epoch: asset.Epoch,
                    Network: asset.Network,
                    OrganizationId: asset.OrgID,
                })
                
                if err == nil && resp.Found {
                    mu.Lock()
                    results[asset.ID] = resp.Data
                    mu.Unlock()
                }
            }(asset)
        }
        
        wg.Wait()
    }
    
    return results, nil
}
Troubleshooting
Issue	Possible Cause	Solution
Client panic on start	Neither AED_STORE nor AED_STORE_TESTING set	Set at least one environment variable
Connection refused	AED store not running	Verify AED_STORE host:port is correct
Test mode not working	AED_STORE_TESTING not set to "TRUE"	Set exact value "TRUE" (case-sensitive)
Proto generation fails	Missing protoc plugins	Install protoc-gen-go, protoc-gen-go-grpc, protoc-gen-ts
Data not found	Wrong network or organization ID	Verify organization isolation parameters
Version mismatch	Old proto files	Re-run build script to regenerate
Best Practices
Data Management
Use meaningful epoch numbers (e.g., block height, day number)

Always include organization_id for proper isolation

Version your data schema for backward compatibility

Implement data retention policies for old epochs

Client Usage
Always close gRPC connections when done

Implement retry logic with exponential backoff

Use context timeouts for all operations

Cache frequently accessed data

Testing
Use AED_STORE_TESTING=TRUE for unit tests

Test with both real and mock stores

Verify error handling paths

Test batch operations with large datasets

License
This documentation is part of the TX Marketplace platform.
