# Admin Asset Service

The Asset service provides RESTful interfaces for managing assets within organizations. All admin endpoints are protected by role-based access control and default to the `BROKER_ASSET_ADMINISTRATOR` role. Permissions are managed dynamically by Organization administrators on the fly.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin Asset Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ GET /list │ POST /create │ POST /create │ PUT /update │ │
│ │ │ │ /version │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Asset Store │ Account Store │ Role Store │ Organization Store│ │
│ │ Certificate │ Feature Flag │ File Store │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Blockchain Layer (Coreum) │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Registry │ ATG Broker │ Order Hub │ Asset Extension │ │
│ │ Contract │ Contract │ Contract │ Code │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/asset/list | BROKER_ASSET_ADMINISTRATOR | List assets |
| POST /api/asset/create | BROKER_ASSET_ADMINISTRATOR | Create new asset |
| POST /api/asset/create/version | BROKER_ASSET_ADMINISTRATOR | Create new version |
| PUT /api/asset/update | BROKER_ASSET_ADMINISTRATOR | Update asset |
| PUT /api/asset/update/status | BROKER_ASSET_ADMINISTRATOR | Update asset status |

## API Endpoints

### GET /api/asset/list

Returns a list of all assets in the organization with pagination support.

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| offset | int | Pagination offset | No (default: 0) |
| jurisdiction_ids | string | Comma-separated jurisdiction IDs | No |
| status | int | Asset status filter | No |
| asset_type | int | Asset type filter | No |
| exchange_ticker_symbol | string | Ticker symbol filter | No |
| exchange | string | Exchange filter | No |
| symbol | string | Asset symbol filter | No |
| version | string | Asset version filter | No |
| issuer | string | Issuer address filter | No |
| industry | int | Industry filter | No |

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| OrganizationID | Organization UUID | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Example Request

```bash
curl -X GET \
  "https://com-be-admin-asset-service.a.run.app/api/asset/list?\
jurisdiction_ids=8878d73b-edff-40a1-b6ce-43a4508aa96a,5bc32483-d6a6-3a8e-8a23-65c5e483b0f0&\
issuer=testcore1j974n26f48wgt4dpcxryrakrnkg433yznff29v&\
offset=0" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer: <token>"
Example Response
json
{
  "Assets": [
    {
      "AssetDetails": {
        "ID": "dgly_1_72c4c072-2fe4-4f72-ae9d-d9d52a05fd71_testcore1j974n26f48wgt4dpcxryrakrnkg433yznff29v",
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Status": 2,
        "Type": 9,
        "Denom": {
          "Currency": {
            "Symbol": "DGLY",
            "Version": "1"
          },
          "Subunit": "sudgly_1",
          "Description": "Digital Ally, Inc. Common Stock"
        },
        "SmartContractIssuerAddr": "testcore1j974n26f48wgt4dpcxryrakrnkg433yznff29v",
        "EquityDetails": {
          "ExchangeTickerSymbol": "DGLY",
          "Exchange": "NASDAQ",
          "MinTransactionAmount": 1,
          "TradingMarginPercentage": 0.1,
          "AssetMarginPercentage": 0.5
        },
        "FinancialProperties": {
          "Symbol": "DGLY",
          "Issuer": "testcore1j974n26f48wgt4dpcxryrakrnkg433yznff29v",
          "JurisdictionIDs": ["8878d73b-edff-40a1-b6ce-43a4508aa96a"],
          "Network": 2
        },
        "Description": {
          "Name": "Digital Ally, Inc. Common Stock"
        }
      },
      "MetaData": {
        "Network": 2,
        "UpdatedAt": {
          "seconds": 1759786658,
          "nanos": 453447000
        },
        "CreatedAt": {
          "seconds": 1759786658,
          "nanos": 453437000
        }
      },
      "Audit": {
        "ChangedBy": "API_TOKEN_72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "ChangedAt": {
          "seconds": 1759786658,
          "nanos": 453447000
        }
      }
    }
  ],
  "Offset": 20
}
POST /api/asset/create
Creates a new asset for the organization (version 1).

Request Body
Field	Type	Description	Required
AssetDetails.OrganizationID	string	Organization UUID	Yes
AssetDetails.JurisdictionIDs	[]string	Array of jurisdiction IDs	Yes
AssetDetails.Type	int	Asset type	Yes
AssetDetails.Name	string	Asset name	Yes
AssetDetails.ExchangeTickerSymbol	string	Exchange ticker symbol	Yes
AssetDetails.Exchange	int	Exchange identifier	Yes
AssetDetails.InternalDescription	string	Internal description	No
AssetDetails.MinTransactionAmount	int	Minimum transaction amount	Yes
AssetDetails.ExtraPercentage	float	Extra percentage fee	No
AssetDetails.Industry	int	Industry category	Yes
AssetDetails.Denom.Currency.Symbol	string	Currency symbol	Yes
AssetDetails.Denom.Currency.Version	string	Version (must be "1")	Yes
AssetDetails.Denom.Precision	int	Decimal precision	Yes
AssetDetails.Denom.Description	string	Denomination description	Yes
Audit.Reason	string	Audit reason	No
Example Request
bash
curl -X POST "https://com-be-admin-asset-service.a.run.app/api/asset/create" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "AssetDetails": {
      "OrganizationID": "215a551d-5691-91ce-f4a6-9284f40d1340",
      "JurisdictionIDs": [
        "8ac93283-d8a6-4a8e-8c01-67c5e106b0f0"
      ],
      "Type": 1,
      "Name": "Tesla",
      "ExchangeTickerSymbol": "TSLA",
      "Exchange": 1,
      "InternalDescription": "TSLA Token Version 2",
      "MinTransactionAmount": 1,
      "ExtraPercentage": 0.05,
      "Industry": 1,
      "Denom": {
        "Currency": {
          "Symbol": "TSLA",
          "Version": "2"
        },
        "Precision": 6,
        "Description": "Tesla TOKEN Version 2"
      }
    },
    "Audit": {
      "Reason": "new version"
    }
  }'
Example Response
json
{
  "Key": "aapl_1_215a551d-5691-91ce-f4a6-9284f40d1340"
}
POST /api/asset/create/version
Creates a new version of an existing asset. The previous version will be automatically marked as outdated (status: OUTDATED_ASSET_VERSION).

Important Notes
New version must be exactly 1 greater than the current active version

Only the following fields can be modified in the new version:

JurisdictionIDs

Name

InternalDescription

MinTransactionAmount

ExtraPercentage

Precision

Denom.Description

When creating version N, version N-1 will be automatically marked as OUTDATED_ASSET_VERSION

Previous version must exist and be in LISTED status

Example Request
bash
curl -X POST "https://com-be-admin-asset-service.a.run.app/api/asset/create/version" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "AssetDetails": {
      "OrganizationID": "215a551d-5691-91ce-f4a6-9284f40d1340",
      "JurisdictionIDs": [
        "8ac93283-d8a6-4a8e-8c01-67c5e106b0f0"
      ],
      "Type": 1,
      "Name": "Tesla",
      "ExchangeTickerSymbol": "TSLA",
      "Exchange": 1,
      "InternalDescription": "TSLA Token Version 3",
      "MinTransactionAmount": 1,
      "ExtraPercentage": 0.1,
      "Industry": 4,
      "Denom": {
        "Currency": {
          "Symbol": "TSLA",
          "Version": "3"
        },
        "Precision": 6,
        "Description": "Tesla TOKEN Version 3"
      }
    }
  }'
Example Response
json
{
  "Key": "tsla_3_215a551d-5691-91ce-f4a6-9284f40d1340"
}
PUT /api/asset/update
Updates an existing asset.

Important Notes
The following fields will NOT be updated:

CreatedAt

Network

OrganizationID

Type

Currency

Subunit

Precision

Description

Status can only be updated through the /api/asset/update/status endpoint.

Example Request
bash
curl -X PUT "https://com-be-admin-asset-service.a.run.app/api/asset/update" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "AssetDetails": {
      "ID": "aapl_1-215a551d-5691-91ce-f4a6-9284f40d1340",
      "OrganizationID": "215a551d-5691-91ce-f4a6-9284f40d1340",
      "JurisdictionIDs": [
        "8ac93283-d8a6-4a8e-8c01-67c5e106b0f0"
      ],
      "Status": 2,
      "Name": "APPLE",
      "ExchangeTickerSymbol": "AAPL",
      "Exchange": 1,
      "InternalDescription": "APPLE Token Version 1 updated",
      "MinTransactionAmount": 1,
      "ExtraPercentage": 0.2,
      "Industry": 3,
      "Denom": {
        "Currency": {
          "Symbol": "AAPL",
          "Version": "1"
        }
      }
    },
    "Audit": {
      "Reason": "Update Test"
    }
  }'
Example Response
json
{
  "Key": "aapl_1_215a551d-5691-91ce-f4a6-9284f40d1340"
}
PUT /api/asset/update/status
Updates the status of an asset.

Query Parameters
Parameter	Type	Description	Required
asset_key	string	Asset identifier key	Yes
status	int	New status value	Yes
reason	string	Reason for status change	No
Example Request
bash
curl -X PUT "https://com-be-admin-asset-service.a.run.app/api/asset/update/status?asset_key=aapl_1-215a551d-5691-91ce-f4a6-9284f40d1340&status=2&reason=Asset%20no%20longer%20supported" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer: <token>"
Example Response
json
{
  "Key": "aapl_1_215a551d-5691-91ce-f4a6-9284f40d1340"
}
Data Models
AssetDetails Object
Field	Type	Description
ID	string	Unique asset identifier
OrganizationID	string	Organization UUID
Status	int	Asset status (see Status Values)
Type	int	Asset type (see Type Values)
Denom	Denom	Denomination information
SmartContractIssuerAddr	string	Blockchain issuer address
EquityDetails	EquityDetails	Equity-specific details
FinancialProperties	FinancialProperties	Financial properties
Description	Description	Asset description
Denom Object
Field	Type	Description
Currency.Symbol	string	Currency symbol (e.g., "AAPL")
Currency.Version	string	Asset version
Subunit	string	Subunit denomination
Precision	int	Decimal precision
Description	string	Denomination description
EquityDetails Object
Field	Type	Description
ExchangeTickerSymbol	string	Ticker symbol on exchange
Exchange	string	Exchange name (e.g., "NASDAQ")
MinTransactionAmount	int	Minimum transaction amount
TradingMarginPercentage	float	Trading margin percentage
AssetMarginPercentage	float	Asset margin percentage
FinancialProperties Object
Field	Type	Description
Symbol	string	Asset symbol
Issuer	string	Issuer address
JurisdictionIDs	[]string	Array of jurisdiction UUIDs
Network	int	Network identifier
Status Values
Status ID	Status Name	Description
1	PENDING	Awaiting approval
2	LISTED	Active and available for trading
3	SUSPENDED	Temporarily unavailable
4	DELISTED	Permanently removed
5	OUTDATED_ASSET_VERSION	Old version (superseded)
Asset Type Values
Type ID	Type Name	Description
1	EQUITY	Stock tokens
2	COMMODITY	Commodity tokens
3	REAL_ESTATE	Real estate tokens
4	BOND	Bond tokens
5	FUND	Investment fund tokens
6	ETF	Exchange-traded fund tokens
7	DERIVATIVE	Derivative tokens
8	CRYPTO	Cryptocurrency
9	OTHER	Other asset types
Exchange Values
Exchange ID	Exchange Name
1	NASDAQ
2	NYSE
3	LSE
4	TSX
5	HKEX
6	EURONEXT
7	ASX
8	BSE
9	NSE
Industry Values
Industry ID	Industry Name
1	Technology
2	Financial Services
3	Healthcare
4	Consumer Goods
5	Energy
6	Real Estate
7	Industrials
8	Utilities
9	Telecommunications
Audit Object
Field	Type	Description
ChangedBy	string	User or system that made the change
ChangedAt	timestamp	Time of change
Reason	string	Reason for the change
Metadata Object
Field	Type	Description
Network	int	Network identifier
CreatedAt	timestamp	Creation timestamp
UpdatedAt	timestamp	Last update timestamp
Start Parameters
Service Endpoints
Environment Variable	Description	Required
HTTP_CONFIG	HTTP server configuration	Yes
AUTH_FIREBASE_SERVICE	Firebase authentication service endpoint	Yes
ACCOUNT_STORE	Admin account store endpoint	Yes
FEATURE_FLAG_STORE	Feature flag store endpoint	Yes
FILE_STORE	File store endpoint	Yes
ROLE_STORE	Role store endpoint	Yes
ORGANIZATION_STORE	Organization store endpoint	Yes
ASSET_STORE	Asset store endpoint	Yes
CERTIFICATE_STORE	Certificate store endpoint	Yes
Smart Contract Configuration
Environment Variable	Description
REGISTRY_CONTRACT_ADDRESS	Registry smart contract address on Coreum
ATG_BROKER_CONTRACT_ADDRESS	ATG Broker contract address on Coreum
ASSET_EXTENSION_CODE	Asset extension code for Coreum assets
ORDER_HUB_CONTRACT_ADDRESS	Order hub smart contract address on Coreum
Blockchain Configuration
Environment Variable	Description
NETWORKS	JSON object with WebSocket/gRPC configs for Coreum
SINGLE_NETWORK	JSON object for single network configuration
Application Configuration
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, error)	info
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
  "message": "Insufficient permissions for this operation. Required role: BROKER_ASSET_ADMINISTRATOR"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid request parameters",
  "details": "OrganizationID is required"
}
Conflict (409)
json
{
  "error": "Conflict",
  "message": "Asset version already exists",
  "details": "Version 2 of symbol TSLA already exists"
}
Version Management Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Asset Version Management                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Version 1 (LISTED)                                                         │
│       │                                                                     │
│       │ POST /api/asset/create/version                                      │
│       │ (version: "2")                                                      │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Version 1 → OUTDATED_ASSET_VERSION (auto-marked)                    │   │
│  │  Version 2 → LISTED (new active version)                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       │ POST /api/asset/create/version                                      │
│       │ (version: "3")                                                      │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Version 2 → OUTDATED_ASSET_VERSION (auto-marked)                    │   │
│  │  Version 3 → LISTED (new active version)                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Modifiable Fields by Version
Field	Version 1 Creation	Version N Creation (N>1)	Update (any version)
OrganizationID	✓	✗	✗
JurisdictionIDs	✓	✓	✓
Type	✓	✗	✗
Name	✓	✓	✓
ExchangeTickerSymbol	✓	✗	✓
Exchange	✓	✗	✓
InternalDescription	✓	✓	✓
MinTransactionAmount	✓	✓	✓
ExtraPercentage	✓	✓	✓
Industry	✓	✗	✓
Denom.Currency.Symbol	✓	✗	✗
Denom.Currency.Version	✓	✓	✗
Denom.Precision	✓	✓	✗
Denom.Subunit	✓	✗	✗
Denom.Description	✓	✓	✗
Status	✗	✗	✗ (use /update/status)
Network Values
Network	Value	Description
mainnet	1	Production network
testnet	2	Test network
devnet	3	Development network
Asset Key Format
The asset key follows this format:

text
{symbol}_{version}_{organization_id}_{issuer?}
Examples:

aapl_1_215a551d-5691-91ce-f4a6-9284f40d1340

tsla_3_215a551d-5691-91ce-f4a6-9284f40d1340

Related Services
Service	Description
Admin Account Service	User and role management
Organization Service	Organization management
KYC Service	Identity verification
File Service	File storage
Troubleshooting
Common Issues
Issue	Solution
Permission denied	Verify user has BROKER_ASSET_ADMINISTRATOR role
Network mismatch	Ensure Network header matches the asset's network
Version conflict	Check that new version is exactly +1 from current
Asset not found	Verify asset_key format and existence
Invalid jurisdiction	Ensure jurisdiction IDs are valid for the organization
Best Practices
Version Management: Always increment versions by exactly 1

Audit Trails: Provide meaningful reasons in audit objects

Status Updates: Use the dedicated status endpoint for status changes

Pagination: Always use offset for large result sets

Validation: Validate jurisdiction IDs before creating assets

License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the admin asset service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the admin asset service section:

markdown
## Admin Services

### Admin Account Service

The Admin Account Service manages users and their roles within a multi-tier system.

📖 **[Admin Account Service Documentation](./admin/account-service.md)**

### Admin Asset Service

The Admin Asset Service provides RESTful interfaces for managing assets within organizations.

📖 **[Admin Asset Service Documentation](./admin/asset/asset-service.md)**

**Key Features:**
- Asset listing with pagination and filters
- Create new assets (version 1)
- Create new asset versions (version 2+)
- Update existing assets
- Update asset status
- Role-based access control (BROKER_ASSET_ADMINISTRATOR)

**Asset Status Values:**
- PENDING (1) - Awaiting approval
- LISTED (2) - Active for trading
- SUSPENDED (3) - Temporarily unavailable
- DELISTED (4) - Permanently removed
- OUTDATED_ASSET_VERSION (5) - Old version

**Quick Examples:**
```bash
# List assets
GET /api/asset/list?offset=0&status=2

# Create asset
POST /api/asset/create

# Create new version
POST /api/asset/create/version

# Update asset status
PUT /api/asset/update/status?asset_key=...&status=2
Account Types:

Sologenic Administrator (Platform level)

Organization Administrator (Organization level)

KYC Administrator

Broker Asset Administrator

Normal User (End User)
