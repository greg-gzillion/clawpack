# Auth Service (Internal gRPC)

The Auth Service implements the `fs-auth-model` and uses the `fs-account-model` to provide authentication and authorization for other services. This is an **internal gRPC service** (no HTTP RESTful interface) used exclusively for service-to-service communication.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Internal Auth Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Service Characteristics │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • gRPC interface only (no HTTP REST) │ │
│ │ • Internal service (not exposed externally) │ │
│ │ • No persistent storage (stateless) │ │
│ │ • Token validation via Coreum blockchain │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Functions │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Token Signature Validation (via Coreum nodes) │ │
│ │ • Token Expiry Management (via GCloud Datastore) │ │
│ │ • Account Resolution (via fs-account-model) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Dependencies │ │
│ ├───────────────┬───────────────┬─────────────────────────────────────┤ │
│ │ Coreum Nodes │ Auth Smart │ GCloud Datastore │ │
│ │ (Multi-network│ Contracts │ (Token expiry tracking) │ │
│ │ support) │ │ │ │
│ └───────────────┴───────────────┴─────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Key Characteristics

### What Makes This Service Unique

| Characteristic | Description |
|----------------|-------------|
| **gRPC Only** | No HTTP RESTful interface - internal service only |
| **No Persistence** | Does not store data (stateless) - exception to naming convention |
| **Multi-Network** | Connected to multiple Coreum networks simultaneously |
| **Token Validation** | Validates signatures via Coreum blockchain nodes |
| **Expiry Management** | Uses GCloud Datastore to track expired tokens |

### Naming Note

This repository is a deviation from the standard naming convention:

- **Standard naming**: `com-fs-{name}-store` (for services with persistence)
- **This service**: `com-fs-auth-service` (internal, stateless, gRPC only)

This is effectively the only internal service, so it's the exception to the otherwise well-working naming convention.

## Core Functions

### Token Signature Validation

The Auth Service validates token signatures by accessing the correct Coreum node associated with the network.
┌─────────────────────────────────────────────────────────────────────────────┐
│ Token Signature Validation Flow │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ Service Request with Token │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ValidateToken(token, network) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 1. Determine Network │ │
│ │ • Extract network from request (mainnet/testnet/devnet) │ │
│ │ • Select appropriate Coreum node configuration │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 2. Query Auth Smart Contract │ │
│ │ • Call auth contract at AUTH_ADDRESSES[network] │ │
│ │ • Retrieve token data from blockchain │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 3. Validate Signature │ │
│ │ • Verify cryptographic signature │ │
│ │ • Check token integrity │ │
│ │ • Validate signer identity │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 4. Check Expiry │ │
│ │ • Query GCloud Datastore for revoked/expired tokens │ │
│ │ • Verify token not past EXPIRY days │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ 5. Resolve Account │ │
│ │ • Use fs-account-model to get account details │ │
│ │ • Return account ID and metadata │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

### Token Expiry Management

The Auth Service uses GCloud Datastore to track and remove tokens that are past the expiration date.
┌─────────────────────────────────────────────────────────────────────────────┐
│ Token Expiry Management │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Token Created │ │
│ │ • Record stored in GCloud Datastore │ │
│ │ • Creation timestamp recorded │ │
│ │ • EXPIRY days added to calculate expiration │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Periodic Cleanup (Background Job) │ │
│ │ • Scan for tokens with age > EXPIRY days │ │
│ │ • Remove expired token records │ │
│ │ • Log cleanup metrics │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Token Validation │ │
│ │ • Check if token exists in Datastore │ │
│ │ • If not found → token is expired/invalid │ │
│ │ • If found → check creation timestamp │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Dependencies

### Coreum Node Configuration

The Auth Service depends on access to the correct Coreum node associated with the network to validate token signatures.

#### NETWORKS Environment Variable

```json
{
  "NETWORKS": {
    "GRPC": [
      {
        "Network": "devnet",
        "Host": "full-node.devnet-1.coreum.dev:9090"
      },
      {
        "Network": "testnet",
        "Host": "full-node.testnet-1.coreum.dev:9090"
      },
      {
        "Network": "mainnet",
        "Host": "full-node.mainnet-1.coreum.dev:9090"
      }
    ]
  }
}
Multi-Network Support
The Auth Service can connect to multiple Coreum networks simultaneously:

Network	Description	Typical Usage
devnet	Development network	Local development and testing
testnet	Test network	Integration testing
mainnet	Production network	Live production traffic
Auth Smart Contract Addresses
The Auth Service requires the Auth smart contract address (AUTH_ADDRESSES) to retrieve data from the blockchain.

AUTH_ADDRESSES Environment Variable
json
{
  "AuthAddresses": [
    {
      "Network": "devnet",
      "Address": "core1devnet1234567890abcdef"
    },
    {
      "Network": "testnet",
      "Address": "core1testnet1234567890abcdef"
    },
    {
      "Network": "mainnet",
      "Address": "core1mainnet1234567890abcdef"
    }
  ]
}
Smart Contract Interaction Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Smart Contract Interaction Flow                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Auth Service                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ ValidateToken(token, "mainnet")                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Lookup AuthAddress for "mainnet"                                     │   │
│  │ Address = "core1mainnet1234567890abcdef"                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Query Coreum Node (mainnet)                                          │   │
│  │ • Contract address: core1mainnet1234567890abcdef                     │   │
│  │ • Query: get_token_info(token_id)                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Receive Token Data                                                   │   │
│  │ • Signature                                                          │   │
│  │ • Creator account                                                    │   │
│  │ • Creation timestamp                                                 │   │
│  │ • Token metadata                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
gRPC Interface
The Auth Service provides a gRPC interface for internal service-to-service communication.

Proto Definition (Conceptual)
protobuf
syntax = "proto3";

package auth;

service AuthService {
    // Validate a token and return account information
    rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
    
    // Invalidate a token (logout)
    rpc RevokeToken(RevokeTokenRequest) returns (RevokeTokenResponse);
    
    // Check if a token is valid
    rpc CheckToken(CheckTokenRequest) returns (CheckTokenResponse);
}

message ValidateTokenRequest {
    string token = 1;           // The token to validate
    string network = 2;         // Network: mainnet, testnet, devnet
    string organization_id = 3; // Organization ID for tenant isolation
}

message ValidateTokenResponse {
    string account_id = 1;      // Resolved account ID
    string email = 2;           // User email (if available)
    int64 created_at = 3;       // Token creation timestamp
    int64 expires_at = 4;       // Token expiration timestamp
    map<string, string> metadata = 5; // Additional metadata
}

message RevokeTokenRequest {
    string token = 1;
    string network = 2;
}

message RevokeTokenResponse {
    bool success = 1;
    string message = 2;
}

message CheckTokenRequest {
    string token = 1;
    string network = 2;
}

message CheckTokenResponse {
    bool valid = 1;
    string account_id = 2;
    int64 expires_at = 3;
}
Client Usage (fs-auth-model)
The fs-auth-model contains client code for direct usage of the Auth Service by other services.

Go Client Example
go
package main

import (
    "context"
    "log"
    "time"
    
    "github.com/sologenic/com-fs-auth-model/client"
    "google.golang.org/grpc"
)

func main() {
    // Connect to Auth Service
    conn, err := grpc.Dial("auth-service:50051", grpc.WithInsecure())
    if err != nil {
        log.Fatalf("Failed to connect: %v", err)
    }
    defer conn.Close()
    
    // Create auth client
    authClient := client.NewAuthClient(conn)
    
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    // Validate token
    resp, err := authClient.ValidateToken(ctx, &client.ValidateTokenRequest{
        Token:          "eyJhbGciOiJSUzI1NiIs...",
        Network:        "mainnet",
        OrganizationID: "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    })
    if err != nil {
        log.Fatalf("Validation failed: %v", err)
    }
    
    log.Printf("Token valid for account: %s", resp.AccountID)
    log.Printf("Expires at: %d", resp.ExpiresAt)
}
Service Integration Pattern
go
// Typical service integration with Auth Service
type MyService struct {
    authClient AuthServiceClient
    userStore  UserStore
}

func (s *MyService) AuthenticatedHandler(ctx context.Context, token string, network string) (*User, error) {
    // Validate token with Auth Service
    authResp, err := s.authClient.ValidateToken(ctx, &ValidateTokenRequest{
        Token:   token,
        Network: network,
    })
    if err != nil {
        return nil, fmt.Errorf("authentication failed: %w", err)
    }
    
    // Use resolved account ID for business logic
    user, err := s.userStore.GetByAccountID(authResp.AccountID)
    if err != nil {
        return nil, fmt.Errorf("user not found: %w", err)
    }
    
    return user, nil
}
Environment Configuration
Required Environment Variables
Environment Variable	Description	Format
NETWORKS	Coreum node configurations for each network	JSON object with GRPC array
AUTH_ADDRESSES	Auth smart contract addresses per network	JSON object with AuthAddresses array
EXPIRY	Token expiry time in days since creation	Integer (days)
GOOGLE_CLOUD_PROJECT	GCloud project ID for Datastore	String
Complete Configuration Example
json
{
  "NETWORKS": {
    "GRPC": [
      {
        "Network": "devnet",
        "Host": "full-node.devnet-1.coreum.dev:9090"
      },
      {
        "Network": "testnet",
        "Host": "full-node.testnet-1.coreum.dev:9090"
      },
      {
        "Network": "mainnet",
        "Host": "full-node.mainnet-1.coreum.dev:9090"
      }
    ]
  },
  "AUTH_ADDRESSES": {
    "AuthAddresses": [
      {
        "Network": "devnet",
        "Address": "core1devnetauthcontract123456"
      },
      {
        "Network": "testnet",
        "Address": "core1testnetauthcontract123456"
      },
      {
        "Network": "mainnet",
        "Address": "core1mainnetauthcontract123456"
      }
    ]
  },
  "EXPIRY": 7,
  "GOOGLE_CLOUD_PROJECT": "sologenic-platform"
}
Shell Environment Setup
bash
# Coreum node configurations
export NETWORKS='{"GRPC":[{"Network":"devnet","Host":"full-node.devnet-1.coreum.dev:9090"},{"Network":"testnet","Host":"full-node.testnet-1.coreum.dev:9090"},{"Network":"mainnet","Host":"full-node.mainnet-1.coreum.dev:9090"}]}'

# Auth contract addresses
export AUTH_ADDRESSES='{"AuthAddresses":[{"Network":"devnet","Address":"core1devnet123..."},{"Network":"testnet","Address":"core1testnet123..."},{"Network":"mainnet","Address":"core1mainnet123..."}]}'

# Token expiry (days)
export EXPIRY=7

# GCloud project
export GOOGLE_CLOUD_PROJECT=sologenic-platform

# Optional: Log level
export LOG_LEVEL=debug
Docker Compose Example
yaml
version: '3.8'

services:
  auth-service:
    image: sologenic/auth-service:latest
    environment:
      - NETWORKS={"GRPC":[{"Network":"devnet","Host":"coreum-devnet:9090"}]}
      - AUTH_ADDRESSES={"AuthAddresses":[{"Network":"devnet","Address":"core1devnet123..."}]}
      - EXPIRY=7
      - GOOGLE_CLOUD_PROJECT=sologenic-platform
      - LOG_LEVEL=info
    ports:
      - "50051:50051"
    networks:
      - internal

  my-service:
    image: sologenic/my-service:latest
    environment:
      - AUTH_SERVICE_ENDPOINT=auth-service:50051
    depends_on:
      - auth-service
    networks:
      - internal

networks:
  internal:
    driver: bridge
Token Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Token Lifecycle                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Token Creation (External)                                         │   │
│  │    • User authenticates via wallet                                   │   │
│  │    • Token signed with private key                                   │   │
│  │    • Token recorded on blockchain (Auth contract)                    │   │
│  │    • Record stored in GCloud Datastore with creation timestamp       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Token Usage                                                        │   │
│  │    • Service calls ValidateToken                                      │   │
│  │    • Auth Service verifies signature via Coreum node                  │   │
│  │    • Auth Service checks expiry via Datastore                         │   │
│  │    • Returns account info if valid                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. Token Expiry (Automatic)                                          │   │
│  │    • EXPIRY days after creation                                      │   │
│  │    • Background job removes expired tokens from Datastore            │   │
│  │    • Token remains on blockchain but is considered expired           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. Token Revocation (Manual)                                         │   │
│  │    • User explicitly logs out                                        │   │
│  │    • Admin force revokes token                                       │   │
│  │    • Token removed from Datastore immediately                        │   │
│  │    • Subsequent validation fails                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
GCloud Datastore Schema
Token Entity Structure
json
{
  "kind": "AuthToken",
  "properties": {
    "token_id": {
      "type": "string",
      "value": "unique_token_identifier"
    },
    "account_id": {
      "type": "string",
      "value": "core1account..."
    },
    "network": {
      "type": "string",
      "value": "mainnet"
    },
    "created_at": {
      "type": "timestamp",
      "value": "2024-01-01T00:00:00Z"
    },
    "expires_at": {
      "type": "timestamp",
      "value": "2024-01-08T00:00:00Z"
    },
    "revoked": {
      "type": "boolean",
      "value": false
    }
  }
}
Datastore Indexes
yaml
# index.yaml
indexes:
  - kind: AuthToken
    properties:
      - name: expires_at
        direction: asc
      - name: revoked
        direction: asc
  
  - kind: AuthToken
    properties:
      - name: account_id
        direction: asc
      - name: network
        direction: asc
Deployment
Kubernetes Deployment
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: sologenic
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
    spec:
      containers:
      - name: auth-service
        image: gcr.io/sologenic-platform/auth-service:latest
        ports:
        - containerPort: 50051
          name: grpc
        env:
        - name: NETWORKS
          valueFrom:
            configMapKeyRef:
              name: auth-config
              key: networks
        - name: AUTH_ADDRESSES
          valueFrom:
            configMapKeyRef:
              name: auth-config
              key: auth_addresses
        - name: EXPIRY
          value: "7"
        - name: GOOGLE_CLOUD_PROJECT
          value: "sologenic-platform"
        - name: LOG_LEVEL
          value: "info"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          grpc:
            port: 50051
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          grpc:
            port: 50051
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: auth-service
  namespace: sologenic
spec:
  selector:
    app: auth-service
  ports:
  - port: 50051
    targetPort: 50051
    name: grpc
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: auth-config
  namespace: sologenic
data:
  networks: |
    {
      "GRPC": [
        {"Network": "devnet", "Host": "full-node.devnet-1.coreum.dev:9090"},
        {"Network": "testnet", "Host": "full-node.testnet-1.coreum.dev:9090"},
        {"Network": "mainnet", "Host": "full-node.mainnet-1.coreum.dev:9090"}
      ]
    }
  auth_addresses: |
    {
      "AuthAddresses": [
        {"Network": "devnet", "Address": "core1devnet123..."},
        {"Network": "testnet", "Address": "core1testnet123..."},
        {"Network": "mainnet", "Address": "core1mainnet123..."}
      ]
    }
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Token validation fails	Wrong Coreum node	Verify NETWORKS configuration
Auth contract query fails	Invalid contract address	Check AUTH_ADDRESSES for correct network
Expired token still valid	Datastore cleanup not running	Check GCloud Datastore indexes and background job
Cannot connect to Coreum	Network connectivity	Verify Coreum node is accessible
Account resolution fails	fs-account-model not configured	Check ACCOUNT_STORE environment variable
Debugging Commands
bash
# Check gRPC server health
grpcurl -plaintext localhost:50051 health.Health/Check

# Test token validation
grpcurl -plaintext -d '{
  "token": "eyJhbGciOiJSUzI1NiIs...",
  "network": "testnet"
}' localhost:50051 auth.AuthService/ValidateToken

# Check Datastore tokens (gcloud CLI)
gcloud datastore query --kind=AuthToken --project=sologenic-platform

# Monitor auth service logs
kubectl logs -f deployment/auth-service -n sologenic
Best Practices
Security
Network Isolation: Run Auth Service on internal network only

Token Expiry: Keep EXPIRY low (7 days or less)

Regular Cleanup: Ensure Datastore cleanup job runs frequently

Audit Logging: Log all token validation failures

Rate Limiting: Implement rate limiting on validation endpoints

Performance
Aspect	Recommendation
Connection Pooling	Maintain persistent gRPC connections
Caching	Cache validation results for short period (seconds)
Datastore Queries	Use appropriate indexes for expiry queries
Coreum Nodes	Use dedicated nodes for auth service
Reliability
Multi-Network Redundancy: Configure fallback nodes per network

Health Checks: Implement gRPC health checking

Circuit Breakers: Handle Coreum node failures gracefully

Retry Logic: Implement exponential backoff for node queries

Related Services
Service	Relationship
fs-auth-model	Client library for Auth Service
fs-account-model	Account resolution dependency
Coreum Blockchain	Token signature validation
GCloud Datastore	Token expiry tracking
License
This documentation is part of the TX Marketplace platform.
