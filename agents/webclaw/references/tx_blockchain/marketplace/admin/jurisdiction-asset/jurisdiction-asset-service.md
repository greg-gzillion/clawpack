# Admin Jurisdiction and Asset Management Service

The Admin Jurisdiction and Asset Management Service provides the necessary technical interfaces with the blockchain to manage whitelists on smart tokens and asset whitelists in the broker smart contract. The service also handles KYC (Know Your Customer) related changes, ensuring that users' jurisdictional data is up to date and correctly managed within the system.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin Jurisdiction and Asset Management Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Functions │ │
│ ├─────────────────────┬─────────────────────┬───────────────────────┤ │
│ │ User Jurisdiction │ Whitelist │ Asset Management │ │
│ │ Management │ Management │ │ │
│ └─────────────────────┴─────────────────────┴───────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Service Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Account Store │ Jurisdiction │ Asset Store │ HTTP Config │ │
│ │ │ Store │ │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Blockchain Layer (Coreum) │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Smart Token Whitelists │ │
│ │ • Broker Smart Contract Asset Whitelists │ │
│ │ • Jurisdiction Validation │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Core Functions

### 1. User Jurisdiction Management

Monitors KYC changes and updates UserJurisdiction records accordingly, including the addition or invalidation (NOT_ALLOWED) of jurisdictions.

**Workflow:**
┌─────────────────────────────────────────────────────────────────────────────┐
│ User Jurisdiction Management Flow │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ KYC Change Detected │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Validate User's Jurisdiction Information │ │
│ │ • Country of residence │ │
│ │ • Citizenship │ │
│ │ • Regulatory classifications │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ├─────────────────────┬─────────────────────┐ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ ADD │ │ UPDATE │ │ INVALIDATE │ │
│ │ Jurisdiction │ │ Jurisdiction │ │ (NOT_ALLOWED)│ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │ │ │
│ └─────────────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Update UserJurisdiction Record in Store │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

### 2. Whitelist Management

Adds wallets to the whitelist, enabling direct trading of assets without interacting with the broker smart contract, thereby improving system efficiency.

**Benefits:**
- Reduced gas costs (bypass broker contract)
- Faster transaction execution
- Improved system throughput
- Direct peer-to-peer trading capability

**Whitelist Workflow:**
┌─────────────────────────────────────────────────────────────────────────────┐
│ Whitelist Management Flow │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ User Completes KYC │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Validate User Jurisdiction for Target Asset │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ (Valid) │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Add Wallet to Smart Token Whitelist │ │
│ │ • Token contract whitelist │ │
│ │ • Direct trading enabled │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Add Wallet to Broker Contract Asset Whitelist (if needed) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ User Can Trade Asset Directly │ │
│ │ • No broker contract interaction │ │
│ │ • Lower fees │ │
│ │ • Faster settlement │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

### 3. Asset Management

Interacts with the broker smart contract to create or update assets as needed when handling whitelist requests.

**Asset Operations:**
- Create new asset whitelists in broker contract
- Update existing asset configurations
- Sync asset status with blockchain
- Manage asset jurisdiction requirements

## Data Models

### UserJurisdiction Record

| Field | Type | Description |
|-------|------|-------------|
| UserID | string | Unique user identifier |
| JurisdictionID | string | Jurisdiction identifier (e.g., country code) |
| Status | enum | ALLOWED, NOT_ALLOWED, PENDING |
| ValidFrom | timestamp | When jurisdiction became valid |
| ValidTo | timestamp | When jurisdiction expires (if applicable) |
| KYCReference | string | Reference to KYC verification |
| UpdatedAt | timestamp | Last update timestamp |

### Whitelist Entry

| Field | Type | Description |
|-------|------|-------------|
| WalletAddress | string | Blockchain wallet address |
| AssetID | string | Asset identifier |
| JurisdictionID | string | Jurisdiction granting access |
| AddedAt | timestamp | When added to whitelist |
| ExpiresAt | timestamp | Expiration (if applicable) |
| Status | enum | ACTIVE, REVOKED, EXPIRED |

### Jurisdiction Status Values

| Status | Description |
|--------|-------------|
| ALLOWED | User is permitted to trade assets in this jurisdiction |
| NOT_ALLOWED | User is not permitted to trade in this jurisdiction |
| PENDING | Awaiting verification or approval |
| EXPIRED | Previous authorization has expired |
| RESTRICTED | Partial restrictions apply |

## Service Interactions

### Integration Points
┌─────────────────────────────────────────────────────────────────────────────┐
│ Service Integration │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────┐ │
│ │ KYC Service │ │
│ │ (User verification) │ │
│ └───────────┬─────────────┘ │
│ │ │
│ │ KYC Changes │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Jurisdiction & Asset Management Service │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │ │ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Account │ │ Jurisdiction │ │ Asset │ │
│ │ Store │ │ Store │ │ Store │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │ │ │
│ └────────────────────┼────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────┐ │
│ │ Coreum Blockchain │ │
│ │ • Smart Tokens │ │
│ │ • Broker Contract │ │
│ └─────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Start Parameters

### Required Environment Variables

| Environment Variable | Description | Source |
|---------------------|-------------|--------|
| ACCOUNT_STORE | The account store service endpoint | github.com/sologenic/com-fs-admin-account-model |
| JURISDICTION_STORE | The jurisdiction store service endpoint | github.com/sologenic/com-fs-jurisdiction-model |
| ASSET_STORE | The asset store service endpoint | github.com/sologenic/com-be-asset-store |
| PROJECT_ID | The project ID of the Google Cloud project | - |
| CREDENTIALS_LOCATION | The location of the Google Cloud credentials file with access credentials for the datastore | - |
| HTTP_CONFIG | The HTTP configuration for the service | github.com/sologenic/com-be-http-lib |

### Optional Environment Variables

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| LOG_LEVEL | Logging level (info, debug, warn, error) | info |
| BLOCKCHAIN_TIMEOUT | Timeout for blockchain transactions | 30s |
| WHITELIST_BATCH_SIZE | Number of whitelist entries per batch | 100 |

## Blockchain Integration

### Smart Token Whitelist

The service interacts with smart token contracts to manage whitelists:

| Operation | Description | Gas Impact |
|-----------|-------------|------------|
| AddToWhitelist | Add wallet to token whitelist | Medium |
| RemoveFromWhitelist | Remove wallet from token whitelist | Medium |
| CheckWhitelistStatus | Verify if wallet is whitelisted | Low |

### Broker Smart Contract Asset Whitelist

Manages asset-level whitelists in the broker contract:

| Operation | Description | Gas Impact |
|-----------|-------------|------------|
| AddAssetWhitelist | Add asset to broker whitelist | High |
| UpdateAssetWhitelist | Update asset configuration | Medium |
| RemoveAssetWhitelist | Remove asset from whitelist | Medium |

## KYC Integration

### Monitored KYC Events

| Event | Trigger | Action |
|-------|---------|--------|
| KYC_COMPLETED | User finishes KYC verification | Add jurisdictions, update whitelists |
| KYC_UPDATED | User updates KYC information | Re-validate jurisdictions |
| KYC_EXPIRED | KYC verification expires | Invalidate jurisdictions (NOT_ALLOWED) |
| KYC_REJECTED | KYC verification fails | Set jurisdictions to NOT_ALLOWED |
| JURISDICTION_CHANGE | User changes residence | Update jurisdiction records |

### Jurisdiction Validation Rules
┌─────────────────────────────────────────────────────────────────────────────┐
│ Jurisdiction Validation Rules │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ Asset Jurisdiction Requirements │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Asset A: Requires US jurisdiction only │ │
│ │ Asset B: Requires EU jurisdiction only │ │
│ │ Asset C: Requires US OR EU jurisdiction │ │
│ │ Asset D: No jurisdiction restrictions (global) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
│ User Jurisdiction Mapping │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ User X: Country = US → ALLOWED for Asset A, C │ │
│ │ User Y: Country = UK → NOT_ALLOWED for Asset A (requires US) │ │
│ │ User Z: Country = Germany → ALLOWED for Asset B, C │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Whitelist Management Strategies

### Direct Trading Whitelist

For high-volume or trusted users, direct whitelist enables:

- **No broker contract fees** - Reduced transaction costs
- **Faster settlement** - Direct token transfers
- **Higher limits** - Less restrictive trading parameters

### Broker Contract Whitelist

Standard whitelist through broker contract provides:

- **Compliance enforcement** - Jurisdiction checks
- **Trading limits** - Configurable restrictions
- **Audit trail** - Complete transaction history

### Hybrid Approach

The service can use both strategies based on:

| Factor | Direct Whitelist | Broker Whitelist |
|--------|-----------------|------------------|
| User Trust Level | High | Standard |
| Trading Volume | High | Any |
| Jurisdiction | Fully verified | Verified |
| Asset Type | Standard | Restricted |

## Error Handling

### Common Error Scenarios

| Error | Description | Resolution |
|-------|-------------|------------|
| JURISDICTION_NOT_ALLOWED | User jurisdiction not permitted for asset | Update KYC or choose different asset |
| WHITELIST_ALREADY_EXISTS | Wallet already on whitelist | No action needed |
| WHITELIST_FULL | Whitelist capacity reached | Contact administrator |
| CONTRACT_ERROR | Blockchain contract interaction failed | Retry with exponential backoff |
| KYC_MISSING | User has no valid KYC | Complete KYC verification |

### Retry Logic
┌─────────────────────────────────────────────────────────────────────────────┐
│ Retry Logic for Blockchain Ops │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ Attempt 1 ──────────────────────────────────────────────────────────────┐ │
│ │ │ │
│ ▼ (fail) │ │
│ Wait 1s │ │
│ │ │ │
│ ▼ │ │
│ Attempt 2 ──────────────────────────────────────────────────────────────┤ │
│ │ │ │
│ ▼ (fail) │ │
│ Wait 2s │ │
│ │ │ │
│ ▼ │ │
│ Attempt 3 ──────────────────────────────────────────────────────────────┤ │
│ │ │ │
│ ▼ (fail) │ │
│ Wait 4s │ │
│ │ │ │
│ ▼ │ │
│ Attempt 4 ──────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ (fail) │
│ Return Error to Client │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Performance Considerations

### Batch Processing

For large whitelist operations, batch processing is recommended:

| Batch Size | Gas Cost | Time Estimate |
|------------|----------|---------------|
| 10 | Low | ~5 seconds |
| 50 | Medium | ~20 seconds |
| 100 | High | ~40 seconds |
| 500+ | Very High | May timeout |

### Caching Strategy

| Data Type | Cache TTL | Invalidation Trigger |
|-----------|-----------|---------------------|
| User Jurisdiction | 5 minutes | KYC update |
| Whitelist Status | 1 minute | Whitelist change |
| Asset Jurisdictions | 10 minutes | Asset update |
| KYC Status | 2 minutes | KYC event |

## Security Considerations

### Access Control

| Operation | Required Role |
|-----------|---------------|
| Add to Whitelist | BROKER_ASSET_ADMINISTRATOR |
| Remove from Whitelist | BROKER_ASSET_ADMINISTRATOR |
| Update Jurisdictions | KYC_ADMINISTRATOR |
| View Whitelist | ORGANIZATION_ADMINISTRATOR |

### Audit Logging

All whitelist and jurisdiction changes are logged:

```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "operation": "ADD_TO_WHITELIST",
  "operator": "admin@organization.org",
  "wallet_address": "core1...",
  "asset_id": "asset_123",
  "jurisdiction_id": "US",
  "tx_hash": "0x..."
}
Troubleshooting
Common Issues and Solutions
Issue	Likely Cause	Solution
Whitelist add fails	User not KYC verified	Complete KYC process
Jurisdiction not allowed	Asset restrictions	Check asset jurisdiction requirements
Transaction timeout	Network congestion	Increase timeout or retry
Wallet already whitelisted	Duplicate request	Verify whitelist status first
Contract out of gas	High gas price	Adjust gas price or wait
Monitoring Metrics
Metric	Description	Alert Threshold
Whitelist add latency	Time to add to whitelist	> 30 seconds
Jurisdiction update failures	Failed updates	> 1%
Blockchain errors	Contract interaction errors	> 5%
KYC sync lag	Delay in processing KYC changes	> 1 minute
Related Services
Service	Description
Admin Account Service	User account management
KYC Service	Identity verification
Admin Asset Service	Asset management
Coreum Blockchain	Blockchain platform
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the jurisdiction and asset management service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the jurisdiction and asset management service section:

markdown
## Admin Services

### Admin Account Service

The Admin Account Service manages users and their roles within a multi-tier system.

📖 **[Admin Account Service Documentation](./admin/account-service.md)**

### Admin Asset Service

The Admin Asset Service provides RESTful interfaces for managing assets within organizations.

📖 **[Admin Asset Service Documentation](./admin/asset/asset-service.md)**

### Admin Certificate Service

The Admin Certificate Service provides RESTful interfaces for managing digital certificates within organizations.

📖 **[Admin Certificate Service Documentation](./admin/certificate/certificate-service.md)**

### Admin Comment Service

The Admin Comment Service provides generic functionality to attach comments to any source type.

📖 **[Admin Comment Service Documentation](./admin/comment/comment-service.md)**

### Admin Document Service

The Admin Document Service provides document lifecycle management with version control and status management for organizational compliance.

📖 **[Admin Document Service Documentation](./admin/document/document-service.md)**

### Admin Feature Flag Service

The Admin Feature Flag Service provides RESTful interfaces for managing feature flags across the marketplace platform.

📖 **[Admin Feature Flag Service Documentation](./admin/featureflag/featureflag-service.md)**

### Admin File Service

The File Service provides RESTful and gRPC interfaces for file upload, temporary storage, and permanent commit operations.

📖 **[Admin File Service Documentation](./admin/file/file-service.md)**

### Admin Jurisdiction and Asset Management Service

The Admin Jurisdiction and Asset Management Service provides blockchain interfaces to manage whitelists on smart tokens and asset whitelists in the broker smart contract.

📖 **[Admin Jurisdiction and Asset Management Service Documentation](./admin/jurisdiction-asset/jurisdiction-asset-service.md)**

**Core Functions:**
| Function | Description |
|----------|-------------|
| User Jurisdiction Management | Monitor KYC changes, update jurisdiction records |
| Whitelist Management | Add wallets to enable direct trading |
| Asset Management | Interact with broker contract for asset operations |

**Key Features:**
- Automatic jurisdiction updates based on KYC changes
- Direct trading whitelist (bypass broker contract)
- Lower gas costs and faster settlement
- Asset whitelist management in broker contract
- Jurisdiction validation for asset access

**Whitelist Benefits:**
- Reduced transaction costs
- Faster execution
- Higher throughput
- Direct peer-to-peer trading

**Account Types:**
- Sologenic Administrator (Platform level)
- Organization Administrator (Organization level)
- KYC Administrator
- Broker Asset Administrator
- Normal User (End User)
