# Smart Contract Deployment Service

The Smart Contract Deployment Service provides RESTful interfaces for deploying and managing CosmWasm smart contracts on the Coreum blockchain. It handles contract metadata, deployment, version management, and migration tracking.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Smart Contract Deployment Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────────────────────────┤ │
│ │ GET /get │ GET /list │ POST /deploy │ │
│ │ (By name) │ (All metadata)│ (Deploy or migrate) │ │
│ └───────────────┴───────────────┴───────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Smart Contract│ Account Store │ Role Store │ Feature Flag │ │
│ │ Store │ │ │ Store │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Blockchain Layer (Coreum) │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Contract Upload (Store Code) │ │
│ │ • Contract Instantiation │ │
│ │ • Contract Migration │ │
│ │ • Code ID Management │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Storage Layer │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Contract Metadata (JSON) │ │
│ │ • Deployment Records │ │
│ │ • Audit Logs │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/smartcontract/get | ORGANIZATION_ADMINISTRATOR | Retrieve smart contract by name |
| GET /api/smartcontract/list | ORGANIZATION_ADMINISTRATOR | List all contract metadata |
| POST /api/smartcontract/deploy | ORGANIZATION_ADMINISTRATOR | Deploy or migrate smart contract |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Network in `Network` header (mainnet, testnet, devnet)

## Data Models

### Contract Metadata Object

| Field | Type | Description |
|-------|------|-------------|
| contract_name | string | Unique name of the smart contract |
| version | string | Contract version hash (e.g., git commit hash) |
| description | string | Human-readable description |
| repository | string | Git repository URL |
| last_build | string | ISO 8601 timestamp of last build |
| release_notes | string | Markdown release notes |

### SmartContractDetails Object

| Field | Type | Description |
|-------|------|-------------|
| Name | string | Contract name (matches metadata) |
| Version | string | Contract version hash |
| Address | string | Blockchain address of deployed instance |
| OrganizationID | string | Organization UUID |
| ActiveCodeID | int64 | Currently active code ID on chain |

### Deployed Contract Response

| Field | Type | Description |
|-------|------|-------------|
| metadata | MetadataObject | Contract metadata from metadata file |
| deployed | DeployedInstance | Deployed contract instance details |
| on_chain_code_id | int64 | Current active code ID on chain (may be nil if not deployed) |
| latest_code_id | int64 | Latest available code ID (mismatch indicates new version available) |

### DeployedInstance Object

| Field | Type | Description |
|-------|------|-------------|
| SmartContract | SmartContractDetails | Contract details |
| MetaData | MetaData | Creation/update timestamps and network |
| Audit | Audit | Change tracking information |

### MetaData Object

| Field | Type | Description |
|-------|------|-------------|
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |

### Audit Object

| Field | Type | Description |
|-------|------|-------------|
| ChangedBy | string | User who made the change |
| ChangedAt | Timestamp | When the change was made |
| Reason | string | Reason for deployment/migration |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

### Network Values

| Network ID | Network Name | Description |
|------------|--------------|-------------|
| 1 | mainnet | Production network |
| 2 | testnet | Testing network |
| 3 | devnet | Development network |

## API Endpoints

### GET /api/smartcontract/get

Retrieves the specified smart contract, including metadata, deployment details, and version information.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| name | string | Smart contract name | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/smartcontract/get?name=hello-world-1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
{
  "metadata": {
    "contract_name": "hello-world-1",
    "version": "e5de9b77adc65cac1fddbb140b00fc90",
    "description": "A CosmWasm smart contract built using the Rust optimizer.",
    "repository": "https://github.com/sologenic/com-atg-sample-contract",
    "last_build": "2025-03-06T01:09:22.704943+00:00",
    "release_notes": "# Release Notes\n\n## Version e3b0c44298fc1c149afbf4c8996fb924\n- Initial release.\n\n## Version 606386b328d90ca02a33dbb4a12c0cef\n- Fixed some issues.\n- Added migration function.\n"
  },
  "deployed": {
    "SmartContract": {
      "Name": "hello-world-1",
      "Version": "e5de9b77adc65cac1fddbb140b00fc90",
      "Address": "testcore13dlcgqv2dqlnsnww35wxgprpfeqjewmda60g2pq89qh2u37gkeyq0ela4u",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "ActiveCodeID": 2188
    },
    "MetaData": {
      "Network": 2,
      "UpdatedAt": {
        "seconds": 1741292412,
        "nanos": 993577000
      },
      "CreatedAt": {
        "seconds": 1741292412,
        "nanos": 993576000
      }
    },
    "Audit": {
      "ChangedBy": "admin@organization.org",
      "ChangedAt": {
        "seconds": 1741292412,
        "nanos": 993577000
      },
      "Reason": "Initial deployment"
    }
  },
  "on_chain_code_id": 2188,
  "latest_code_id": 2189
}
Response Field Explanations
Field	Description
metadata	Contract metadata from the metadata file
deployed	Deployed instance details (null if not deployed)
on_chain_code_id	Current active code ID fetched from chain
latest_code_id	Latest available code ID from metadata
Important: ActiveCodeID from deployed will be the same as on_chain_code_id. However, it is more reliable to use on_chain_code_id as it is fetched directly from the chain.

Version Mismatch Indication
When on_chain_code_id != latest_code_id, a new version of the contract is available for migration.

Error Responses
Status Code	Description
200	Success - Contract found
400	Bad request - Missing name parameter
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Contract does not exist
500	Internal server error
GET /api/smartcontract/list
Retrieves a list of metadata files for all available smart contracts.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/smartcontract/list" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
[
  {
    "contract_name": "hello-world-1",
    "version": "e5de9b77adc65cac1fddbb140b00fc90",
    "description": "A CosmWasm smart contract built using the Rust optimizer.",
    "repository": "https://github.com/sologenic/com-atg-sample-contract",
    "last_build": "2025-03-05T23:34:49.153283+00:00",
    "release_notes": "# Release Notes\n\n## Version e3b0c44298fc1c149afbf4c8996fb924\n- Initial release.\n\n## Version 606386b328d90ca02a33dbb4a12c0cef\n- Fixed some issues.\n- Added migration function.\n"
  },
  {
    "contract_name": "hello-world-2",
    "version": "e5de9b77adc65cac1fddbb140b00fc90",
    "description": "A CosmWasm smart contract built using the Rust optimizer.",
    "repository": "https://github.com/sologenic/com-atg-sample-contract",
    "last_build": "2025-03-05T23:34:57.628786+00:00",
    "release_notes": "# Release Notes\n\n## Version e3b0c44298fc1c149afbf4c8996fb924\n- Initial release.\n\n## Version 606386b328d90ca02a33dbb4a12c0cef\n- Fixed some issues.\n- Added migration function.\n"
  },
  {
    "contract_name": "hello-world-3",
    "version": "e5de9b77adc65cac1fddbb140b00fc90",
    "description": "A CosmWasm smart contract built using the Rust optimizer.",
    "repository": "https://github.com/sologenic/com-atg-sample-contract",
    "last_build": "2025-03-05T23:35:14.377590+00:00",
    "release_notes": "# Release Notes\n\n## Version e3b0c44298fc1c149afbf4c8996fb924\n- Initial release.\n\n## Version 606386b328d90ca02a33dbb4a12c0cef\n- Fixed some issues.\n- Added migration function.\n"
  }
]
Error Responses
Status Code	Description
200	Success - Returns array (may be empty)
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
500	Internal server error
POST /api/smartcontract/deploy
Deploys a new smart contract or migrates an existing one to a new code version.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
SmartContract.Name	string	Name of the smart contract (matches metadata)	Yes
SmartContract.OrganizationID	string	Organization UUID	Yes
SmartContract.ActiveCodeID	int64	Code ID to deploy or migrate to	Yes
SmartContract.Address	string	Contract address (required for migration)	No (required for migration)
Audit.Reason	string	Reason for deployment/migration	No
Deployment vs Migration:

Operation	Address Field	Description
Initial Deployment	Omit	Deploys new contract instance
Migration	Include	Migrates existing contract to new code version
Example 1: Initial Deployment
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/smartcontract/deploy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -d '{
    "SmartContract": {
      "Name": "hello-world-1",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "ActiveCodeID": 2182
    },
    "Audit": {
      "Reason": "Initial deployment of hello-world contract"
    }
  }'
Example 2: Contract Migration
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/smartcontract/deploy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -d '{
    "SmartContract": {
      "Name": "hello-world-1",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Address": "testcore13dlcgqv2dqlnsnww35wxgprpfeqjewmda60g2pq89qh2u37gkeyq0ela4u",
      "ActiveCodeID": 2189
    },
    "Audit": {
      "Reason": "Migrating to version with bug fixes"
    }
  }'
Example Response (Initial Deployment)
json
"testcore1ppsa8yzg6x53h67c9y04wsw5unk7xmgmgaz4e64nhrwk8gj9722quytmmh"
The response is the blockchain address of the newly deployed or migrated smart contract.

Error Responses
Status Code	Description
200	Success - Contract deployed/migrated
400	Bad request - Missing required fields or invalid parameters
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Contract metadata not found
409	Conflict - Contract already deployed or migration conflict
500	Internal server error
Smart Contract Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Smart Contract Lifecycle                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Contract Development                                              │   │
│  │    • Write CosmWasm contract in Rust                                 │   │
│  │    • Build and optimize wasm                                         │   │
│  │    • Upload to metadata storage                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Store Code on Chain                                               │   │
│  │    • Upload wasm to Coreum                                           │   │
│  │    • Receive Code ID                                                 │   │
│  │    • Code ID stored in metadata                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. Initial Deployment                                                │   │
│  │    • POST /deploy (no Address)                                       │   │
│  │    • Instantiate contract                                            │   │
│  │    • Contract address returned                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. Active State                                                      │   │
│  │    • Contract available for use                                      │   │
│  │    • on_chain_code_id = latest_code_id                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │                               │                       │
│                    ▼                               ▼                       │
│  ┌─────────────────────────────┐   ┌─────────────────────────────────────┐ │
│  │ 5a. Migration                │   │ 5b. New Version Available           │ │
│  │    • New code ID stored      │   │    • GET /get shows mismatch        │ │
│  │    • POST /deploy with       │   │    • on_chain_code_id !=            │ │
│  │      Address                 │   │      latest_code_id                 │ │
│  │    • Contract migrated       │   │    • Migration recommended          │ │
│  └─────────────────────────────┘   └─────────────────────────────────────┘ │
│                    │                               │                        │
│                    └───────────────┬───────────────┘                       │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 6. Contract Updated (New Version Active)                            │   │
│  │    • on_chain_code_id = new latest_code_id                           │   │
│  │    • Contract state preserved                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Version Management
Code ID Tracking
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Code ID Tracking                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Metadata Store                      Coreum Blockchain                     │
│  ┌─────────────────────┐            ┌─────────────────────┐               │
│  │ Contract: hello-v1  │            │ Code ID: 2188       │               │
│  │ latest_code_id: 2189│            │ (Stored code)       │               │
│  └─────────────────────┘            └─────────────────────┘               │
│           │                                  │                             │
│           │                                  │                             │
│           ▼                                  ▼                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ GET /get Response                                                    │   │
│  │                                                                      │   │
│  │ {                                                                    │   │
│  │   "on_chain_code_id": 2188,  ← Current active on chain              │   │
│  │   "latest_code_id": 2189      ← New version available               │   │
│  │ }                                                                    │   │
│  │                                                                      │   │
│  │ Mismatch indicates migration is available!                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Version Information Sources
Source	Field	Reliability	Description
Blockchain	on_chain_code_id	Most reliable	Fetched directly from chain
Deployed Record	ActiveCodeID	Reliable	Stored in deployment record
Metadata	latest_code_id	Reference	Latest available version
Contract Metadata Structure
Metadata files are stored in a Google Cloud Storage bucket and contain contract information.

Metadata File Location
text
gs://{project_id}/smart-contracts/{contract_name}/metadata.json
Complete Metadata Example
json
{
  "contract_name": "compliance-manager",
  "version": "a1b2c3d4e5f67890abcdef1234567890",
  "description": "Manages compliance rules and jurisdiction restrictions for asset trading",
  "repository": "https://github.com/sologenic/compliance-manager",
  "last_build": "2025-03-15T10:30:00.000000+00:00",
  "release_notes": "# Release Notes\n\n## Version 2.0.0\n- Added support for new jurisdiction types\n- Improved gas efficiency\n- Fixed migration bug\n\n## Version 1.0.0\n- Initial release\n- Basic compliance rules",
  "code_ids": {
    "mainnet": 12345,
    "testnet": 2189,
    "devnet": 1001
  },
  "wasm_path": "gs://bucket/contracts/compliance-manager.wasm"
}
Deployment Examples
Example 1: Deploy Compliance Manager Contract
bash
# First, check if contract exists and get latest code ID
curl -X GET "https://api.admin.sologenic.org/api/smartcontract/get?name=compliance-manager" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"

# Response shows latest_code_id: 2189

# Deploy the contract
curl -X POST "https://api.admin.sologenic.org/api/smartcontract/deploy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -d '{
    "SmartContract": {
      "Name": "compliance-manager",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "ActiveCodeID": 2189
    },
    "Audit": {
      "Reason": "Deploying compliance manager for production use"
    }
  }'
Example 2: Migrate Contract to New Version
bash
# Check current status - notice mismatch
curl -X GET "https://api.admin.sologenic.org/api/smartcontract/get?name=compliance-manager" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"

# Response shows:
# "on_chain_code_id": 2188
# "latest_code_id": 2189  ← New version available!

# Migrate to new version
curl -X POST "https://api.admin.sologenic.org/api/smartcontract/deploy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -d '{
    "SmartContract": {
      "Name": "compliance-manager",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Address": "testcore13dlcgqv2dqlnsnww35wxgprpfeqjewmda60g2pq89qh2u37gkeyq0ela4u",
      "ActiveCodeID": 2189
    },
    "Audit": {
      "Reason": "Upgrading to version with new jurisdiction support"
    }
  }'
Example 3: Deploy with Custom Instantiation Message
bash
# For contracts that require instantiation parameters
curl -X POST "https://api.admin.sologenic.org/api/smartcontract/deploy" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -d '{
    "SmartContract": {
      "Name": "token-factory",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "ActiveCodeID": 2190,
      "InstantiateMsg": {
        "owner": "core1...",
        "token_symbol": "TST",
        "decimals": 6
      }
    },
    "Audit": {
      "Reason": "Deploying token factory for asset creation"
    }
  }'
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-model/
ACCOUNT_STORE	Account service endpoint	github.com/sologenic/com-fs-admin-account-model/
ROLE_STORE	Role service endpoint	github.com/sologenic/com-fs-admin-role-model/
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-admin-feature-flag-model/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-admin-organization-model/
SMART_CONTRACT_STORE	Smart contract service endpoint	github.com/sologenic/com-fs-admin-smart-contract-model/
NETWORKS	Networks configuration for Coreum clients	-
PROJECT_ID	Google Cloud project ID for storage bucket	-
CREDENTIALS_LOCATION	Certificate with GCloud storage read rights	-
Optional Environment Variables
Environment Variable	Description
GRPC_APPEND	Segment of the service URL that follows the service keyword (e.g., "dfjiao-ijgao.a.run.app")
LOG_LEVEL	Logging level (info, debug, warn, error)
NETWORKS Configuration Example
json
{
  "mainnet": {
    "rpc_endpoint": "https://mainnet.coreum.com:26657",
    "grpc_endpoint": "https://mainnet.coreum.com:9090",
    "chain_id": "coreum-mainnet-1"
  },
  "testnet": {
    "rpc_endpoint": "https://testnet.coreum.com:26657",
    "grpc_endpoint": "https://testnet.coreum.com:9090",
    "chain_id": "coreum-testnet-1"
  },
  "devnet": {
    "rpc_endpoint": "https://devnet.coreum.com:26657",
    "grpc_endpoint": "https://devnet.coreum.com:9090",
    "chain_id": "coreum-devnet-1"
  }
}
Error Responses
Unauthorized (401)
json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
Forbidden (403)
json
{
  "error": "Forbidden",
  "message": "Insufficient permissions. Required role: ORGANIZATION_ADMINISTRATOR"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Missing required field: Name",
  "details": "Smart contract name is required"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Smart contract not found",
  "details": "No metadata found for contract name: hello-world-1"
}
Conflict (409) - Already Deployed
json
{
  "error": "Conflict",
  "message": "Contract already deployed",
  "details": "Contract hello-world-1 is already deployed at address testcore1...",
  "suggestion": "Use migration with Address field to update"
}
Conflict (409) - Migration Missing Address
json
{
  "error": "Conflict",
  "message": "Address required for migration",
  "details": "Contract is already deployed. Provide Address field to migrate to new code version."
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Deployment fails	Invalid Code ID	Verify code ID exists on chain
Migration fails	Wrong address format	Use address from GET response
Version mismatch	New version available	Migrate contract to latest code ID
Contract not found	Name mismatch	Check exact contract name in list
Permission denied	Insufficient role	Ensure user has ORGANIZATION_ADMINISTRATOR
Chain timeout	Network congestion	Retry with exponential backoff
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check contract status:

bash
# List all available contracts
curl -X GET /api/smartcontract/list \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"

# Get specific contract details
curl -X GET "/api/smartcontract/get?name=hello-world-1" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Verify version mismatch:

bash
# Check if migration is needed
response=$(curl -s -X GET "/api/smartcontract/get?name=hello-world-1" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet")

on_chain=$(echo $response | jq '.on_chain_code_id')
latest=$(echo $response | jq '.latest_code_id')

if [ "$on_chain" != "$latest" ]; then
  echo "Migration needed: $on_chain -> $latest"
fi
Best Practices
Deployment
Test on Testnet First: Always deploy and test on testnet before mainnet

Verify Code ID: Ensure the Code ID exists on the target network

Use Descriptive Names: Contract names should be unique and descriptive

Document Releases: Maintain detailed release notes in metadata

Migration
Check Version Status: Always check for version mismatches before migrating

Test Migration on Testnet: Verify migration works correctly on testnet first

Preserve State: Migration preserves contract state; ensure compatibility

Provide Reason: Always include migration reason in audit log

Version Management
Semantic Versioning: Use semantic versioning for contract versions

Track Code IDs: Maintain code ID mappings per network

Update Metadata: Keep metadata in sync with deployed versions

Monitor Mismatches: Regularly check for version mismatches

Security
Audit Contracts: Have smart contracts audited before deployment

Limited Permissions: Restrict deployment to authorized administrators

Migration Validation: Verify migration doesn't break existing functionality

Emergency Rollback: Have a plan for emergency migrations if issues arise

Related Services
Service	Description
Admin Account Service	User and role management
Organization Service	Organization management
Coreum Blockchain	Underlying blockchain platform
Admin Asset Service	Asset management using smart contracts
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the Smart Contract Service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the Smart Contract Deployment Service section under Admin Services:

markdown
### Admin Smart Contract Service

The Smart Contract Deployment Service provides RESTful interfaces for deploying and managing CosmWasm smart contracts on the Coreum blockchain.

📖 **[Admin Smart Contract Service Documentation](./admin/smartcontract/smartcontract-service.md)**

**Key Features:**
- Retrieve smart contract metadata and deployment status
- List all available smart contracts
- Deploy new contract instances
- Migrate existing contracts to new versions
- Version mismatch detection
- Code ID tracking

**Contract Information:**
| Field | Description |
|-------|-------------|
| metadata | Contract metadata (name, version, description, repo) |
| deployed | Deployed instance details (address, code ID) |
| on_chain_code_id | Current active code ID from chain |
| latest_code_id | Latest available code ID |

**Version Mismatch Indication:**
- When `on_chain_code_id != latest_code_id`, a new version is available
- Migrate contract using POST /deploy with Address field

**Quick Examples:**
```bash
# Get contract details
GET /api/smartcontract/get?name=hello-world-1

# List all contracts
GET /api/smartcontract/list

# Deploy new contract
POST /api/smartcontract/deploy
{
  "SmartContract": {
    "Name": "hello-world-1",
    "OrganizationID": "uuid",
    "ActiveCodeID": 2182
  }
}

# Migrate to new version
POST /api/smartcontract/deploy
{
  "SmartContract": {
    "Name": "hello-world-1",
    "OrganizationID": "uuid",
    "Address": "core1...",
    "ActiveCodeID": 2189
  }
}
Required Role: ORGANIZATION_ADMINISTRATOR
