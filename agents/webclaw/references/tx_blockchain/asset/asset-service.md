# Asset Service (Normal User)

The Asset Service provides RESTful interfaces for normal users to view and manage assets. This service handles asset discovery, jurisdiction-based access control, and user-specific asset lists (bookmarks/whitelists).

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Asset Service (Normal User) │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Asset Endpoints User Asset List Endpoints │ │
│ ├─────────────────────┐ ├─────────────────────────────┤ │
│ │ GET /asset/get │ │ GET /asset/user/get │ │
│ │ GET /asset/list │ │ GET /asset/user/list │ │
│ │ │ │ POST /asset/user/add │ │
│ │ │ │ PUT /user/update/status │ │
│ │ │ │ PUT /user/update/visible │ │
│ └─────────────────────┘ └─────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Asset Store │ Jurisdiction │ Account Store │ Organization │ │
│ │ │ Store │ │ Store │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Access Control │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • User Jurisdiction Database (determines allowed jurisdictions) │ │
│ │ • Asset Status (must be LISTED) │ │
│ │ • Jurisdiction Matching (asset jurisdiction ∩ user jurisdictions) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /asset/get | NORMAL_USER | Get asset by key (jurisdiction-filtered) |
| GET /asset/list | NORMAL_USER | List available assets (jurisdiction-filtered) |
| GET /asset/user/get | NORMAL_USER | Get user asset list entry |
| GET /asset/user/list | NORMAL_USER | List user's bookmarked assets |
| POST /asset/user/add | NORMAL_USER | Add asset to user's list |
| PUT /asset/user/update/status | NORMAL_USER | Update asset status in user's list |
| PUT /asset/user/update/visible | NORMAL_USER | Update asset visibility in user's list |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Network in `Network` header (mainnet, testnet, devnet)

## Data Models

### Asset Object

| Field | Type | Description |
|-------|------|-------------|
| ID | string | Unique asset identifier (format: `{symbol}-{org_id}-{version}`) |
| OrganizationID | string | Organization UUID that owns the asset |
| Status | int | Asset status (see Asset Status values) |
| JurisdictionIDs | []string | List of jurisdiction IDs where asset is approved |
| Network | string | Network identifier ("mainnet", "testnet", "devnet") |
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |
| Type | int | Asset type (see Asset Type values) |
| Symbol | string | Trading symbol (e.g., "btc-test") |
| Currency | string | Currency code (e.g., "BTC") |
| Version | string | Asset version identifier |
| Precision | int | Decimal precision for the asset |
| Name | string | Display name of the asset |
| ExchangeTickerSymbol | string | Ticker symbol on exchange |
| Exchange | string | Exchange identifier |
| Description | string | Asset description |

### UserAssetList Object

| Field | Type | Description |
|-------|------|-------------|
| AccountID | string | User account identifier |
| Wallet | string | Wallet address or identifier |
| AssetKey | string | Asset identifier (matches Asset.ID) |
| Status | int | Status in user's list (see User Asset Status) |
| Network | string | Network identifier |
| Visible | bool | Whether asset is visible in user's list |
| CreatedAt | Timestamp | When added to user's list |
| UpdatedAt | Timestamp | Last update timestamp |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset (optional) |

### Asset Status Values

| Status ID | Status Name | Description |
|-----------|-------------|-------------|
| 1 | DRAFT | Asset in draft, not yet submitted |
| 2 | PENDING_APPROVAL | Awaiting admin approval |
| 3 | LISTED | Active and available for trading |
| 4 | REJECTED | Approval rejected |
| 5 | SUSPENDED | Temporarily unavailable |
| 6 | DELISTED | Permanently removed |

### User Asset Status Values

| Status ID | Status Name | Description |
|-----------|-------------|-------------|
| 1 | WATCHLIST | Added to watchlist for monitoring |
| 2 | WHITELISTED | Approved for trading |
| 3 | WHITELISTING_REQUESTED | Request pending approval |
| 4 | BLACKLISTED | Blocked from viewing/trading |
| 5 | IGNORED | Hidden from user |

### Asset Type Values

| Type ID | Type Name | Description |
|---------|-----------|-------------|
| 1 | STOCK | Equity/stock asset |
| 2 | CRYPTO | Cryptocurrency |
| 3 | COMMODITY | Physical commodity |
| 4 | ETF | Exchange-traded fund |
| 5 | BOND | Debt security |
| 6 | DERIVATIVE | Options, futures, etc. |

## API Endpoints

### GET /asset/get

Returns an asset if the user is authorized to view it based on their jurisdiction.

**Important:** An asset will only be returned if:
1. Asset status is `LISTED` (3)
2. At least one of the asset's `JurisdictionIDs` is permitted for the user
3. User's allowed jurisdictions are determined by the UserJurisdiction database

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| asset_key | string | Unique asset identifier | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.sologenic.org/asset/get?asset_key=BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
{
  "ID": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2",
  "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca",
  "Status": 3,
  "JurisdictionIDs": [
    "US",
    "EU",
    "UK"
  ],
  "Network": "testnet",
  "CreatedAt": {
    "seconds": 1724092846
  },
  "UpdatedAt": {
    "seconds": 1724268537
  },
  "Type": 2,
  "Symbol": "btc-test",
  "Currency": "BTC",
  "Version": "2",
  "Precision": 8,
  "Name": "Bitcoin Test Asset",
  "ExchangeTickerSymbol": "BTC",
  "Exchange": "sologenic",
  "Description": "BTC Test Asset for Trading"
}
Error Responses
Status Code	Description
200	Success - Asset found and authorized
400	Bad request - Missing asset_key
401	Unauthorized - Invalid or missing token
403	Forbidden - Asset not authorized for user's jurisdiction
404	Not found - Asset does not exist
500	Internal server error
GET /asset/list
Returns a list of all available (listed and allowed) assets that the user is authorized to view based on their jurisdiction.

Filtering Rules:

Only assets with status LISTED (3)

Assets whose JurisdictionIDs include at least one of user's permitted jurisdictions

User jurisdictions retrieved from UserJurisdiction database

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required
offset	int	Pagination offset	No (default: 0)
jurisdiction_ids	string	Comma-separated jurisdiction IDs	No
asset_type	int	Filter by asset type	No
exchange_ticker_symbol	string	Filter by ticker symbol	No
exchange	string	Filter by exchange	No
Example Request
bash
curl -X GET \
  "https://api.sologenic.org/asset/list?jurisdiction_ids=US,EU,UK&exchange_ticker_symbol=BTC&exchange=sologenic&offset=0&asset_type=2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
[
  {
    "ID": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2",
    "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca",
    "Status": 3,
    "JurisdictionIDs": ["US", "EU", "UK"],
    "Network": "testnet",
    "CreatedAt": {"seconds": 1724092846},
    "UpdatedAt": {"seconds": 1724268537},
    "Type": 2,
    "Symbol": "btc-test",
    "Currency": "BTC",
    "Version": "2",
    "Precision": 8,
    "Name": "Bitcoin Test Asset",
    "ExchangeTickerSymbol": "BTC",
    "Exchange": "sologenic",
    "Description": "BTC Test Asset for Trading"
  },
  {
    "ID": "ETH-34422ce6-7b51-4a15-accb-34959f39d8ca-1",
    "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca",
    "Status": 3,
    "JurisdictionIDs": ["US", "EU"],
    "Network": "testnet",
    "CreatedAt": {"seconds": 1724093000},
    "UpdatedAt": {"seconds": 1724268600},
    "Type": 2,
    "Symbol": "eth-test",
    "Currency": "ETH",
    "Version": "1",
    "Precision": 8,
    "Name": "Ethereum Test Asset",
    "ExchangeTickerSymbol": "ETH",
    "Exchange": "sologenic",
    "Description": "ETH Test Asset"
  }
]
Error Responses
Status Code	Description
200	Success - Returns array (may be empty)
400	Bad request - Invalid parameters
401	Unauthorized - Invalid or missing token
500	Internal server error
GET /asset/user/get
Returns a user asset list entry (bookmarked/whitelisted asset).

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required
user_asset_list_key	string	Unique key (format: {asset_key}-{account_id})	Yes
Example Request
bash
curl -X GET \
  "https://api.sologenic.org/asset/user/get?user_asset_list_key=BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2-ddb9e00a-147b-4fdd-b9bc-0a79b01202d2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
{
  "AccountID": "ddb9e00a-147b-4fdd-b9bc-0a79b01202d2",
  "Wallet": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
  "AssetKey": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2",
  "Status": 2,
  "Network": "testnet",
  "Visible": true,
  "CreatedAt": {
    "seconds": 1724199574
  },
  "UpdatedAt": {
    "seconds": 1724263252
  }
}
Error Responses
Status Code	Description
200	Success - Entry found
400	Bad request - Missing user_asset_list_key
401	Unauthorized - Invalid or missing token
404	Not found - Entry does not exist
500	Internal server error
GET /asset/user/list
Returns a list of assets that the user has specifically bookmarked and whitelisted for viewing and trading.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required
account_id	string	User account ID	Yes
offset	int	Pagination offset	No (default: 0)
wallet	string	Filter by wallet address	No
asset_key	string	Filter by specific asset	No
status	int/string	Filter by status (ID or name)	No
visible	bool	Filter by visibility	No
Example Request
bash
curl -X GET \
  "https://api.sologenic.org/asset/user/list?account_id=ddb9e00a-147b-4fdd-b9bc-0a79b01202d2&visible=true&status=WHITELISTED&wallet=rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1&offset=0" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
[
  {
    "AccountID": "ddb9e00a-147b-4fdd-b9bc-0a79b01202d2",
    "Wallet": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
    "AssetKey": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2",
    "Status": 2,
    "Network": "testnet",
    "Visible": true,
    "CreatedAt": {"seconds": 1724199574},
    "UpdatedAt": {"seconds": 1724263252}
  },
  {
    "AccountID": "ddb9e00a-147b-4fdd-b9bc-0a79b01202d2",
    "Wallet": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
    "AssetKey": "ETH-34422ce6-7b51-4a15-accb-34959f39d8ca-1",
    "Status": 1,
    "Network": "testnet",
    "Visible": true,
    "CreatedAt": {"seconds": 1724199700},
    "UpdatedAt": {"seconds": 1724199700}
  }
]
Error Responses
Status Code	Description
200	Success - Returns array (may be empty)
400	Bad request - Missing account_id
401	Unauthorized - Invalid or missing token
500	Internal server error
POST /asset/user/add
Adds an asset to the user's list (bookmark/whitelist).

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
AccountID	string	User account ID	Yes
Wallet	string	Wallet address	Yes
AssetKey	string	Asset identifier	Yes
Status	int	Status in user's list (default: 1)	No
Visible	bool	Whether visible (default: true)	No
Example Request
bash
curl -X POST \
  "https://api.sologenic.org/asset/user/add" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -d '{
    "AccountID": "ddb9e00a-147b-4fdd-b9bc-0a79b01202d2",
    "Wallet": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
    "AssetKey": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2",
    "Status": 1,
    "Visible": true
  }'
Example Response
json
{
  "Key": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2-ddb9e00a-147b-4fdd-b9bc-0a79b01202d2"
}
Error Responses
Status Code	Description
200	Success - Asset added to user's list
400	Bad request - Missing required fields
401	Unauthorized - Invalid or missing token
409	Conflict - Asset already in user's list
500	Internal server error
PUT /asset/user/update/status
Updates the status of an asset in the user's list.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required
user_asset_list_key	string	Unique key of the entry	Yes
status	int/string	New status (ID or name)	Yes
Example Request
bash
curl -X PUT \
  "https://api.sologenic.org/asset/user/update/status?user_asset_list_key=BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2-ddb9e00a-147b-4fdd-b9bc-0a79b01202d2&status=WHITELISTING_REQUESTED" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
{
  "Key": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2-ddb9e00a-147b-4fdd-b9bc-0a79b01202d2"
}
Error Responses
Status Code	Description
200	Success - Status updated
400	Bad request - Missing parameters or invalid status
401	Unauthorized - Invalid or missing token
404	Not found - Entry does not exist
500	Internal server error
PUT /asset/user/update/visible
Updates the visibility of an asset in the user's list.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required
user_asset_list_key	string	Unique key of the entry	Yes
visible	bool	Visibility setting (true/false)	Yes
Example Request
bash
curl -X PUT \
  "https://api.sologenic.org/asset/user/update/visible?user_asset_list_key=BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2-ddb9e00a-147b-4fdd-b9bc-0a79b01202d2&visible=false" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
{
  "Key": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2-ddb9e00a-147b-4fdd-b9bc-0a79b01202d2"
}
Error Responses
Status Code	Description
200	Success - Visibility updated
400	Bad request - Missing parameters
401	Unauthorized - Invalid or missing token
404	Not found - Entry does not exist
500	Internal server error
Jurisdiction-Based Access Control
The Asset Service implements strict jurisdiction-based access control to ensure users can only view assets approved for their region.

Access Control Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Jurisdiction Access Control Flow                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Request: GET /asset/get?asset_key=...                                 │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Authenticate User                                                 │   │
│  │    • Validate Firebase token                                         │   │
│  │    • Extract Account ID                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Retrieve User's Jurisdictions                                     │   │
│  │    • Query UserJurisdiction database                                 │   │
│  │    • Get allowed jurisdiction IDs for user                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. Fetch Asset from Asset Store                                      │   │
│  │    • Get asset by asset_key                                          │   │
│  │    • Check asset status (must be LISTED)                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. Jurisdiction Matching                                             │   │
│  │    • Compare asset.JurisdictionIDs ∩ user jurisdictions             │   │
│  │    • Must have at least one match                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │                               │                       │
│                    ▼                               ▼                       │
│           ┌──────────────┐                ┌──────────────┐                │
│           │ Match Found  │                │ No Match     │                │
│           │ Return Asset │                │ 403 Forbidden│                │
│           └──────────────┘                └──────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Jurisdiction ID Examples
Jurisdiction ID	Region
US	United States
EU	European Union
UK	United Kingdom
CA	Canada
AU	Australia
JP	Japan
SG	Singapore
CH	Switzerland
User Asset List Key Format
The user_asset_list_key uniquely identifies a user's relationship with an asset.

Format
text
{asset_key}-{account_id}
Components
Component	Description	Example
asset_key	Asset identifier	BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2
account_id	User account ID (UUID)	ddb9e00a-147b-4fdd-b9bc-0a79b01202d2
Example
text
BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2-ddb9e00a-147b-4fdd-b9bc-0a79b01202d2
Asset Key Format
The asset_key uniquely identifies an asset version.

Format
text
{symbol}-{organization_id}-{version}
Components
Component	Description	Example
symbol	Asset symbol	BTC
organization_id	Organization UUID	34422ce6-7b51-4a15-accb-34959f39d8ca
version	Version number	2
Example
text
BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2
User Asset Status Workflow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    User Asset Status Workflow                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Asset Added to User List                                          │   │
│  │    Status: WATCHLIST (1)                                             │   │
│  │    • User bookmarks asset for monitoring                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. User Requests Whitelisting                                        │   │
│  │    Status: WHITELISTING_REQUESTED (3)                                │   │
│  │    • User submits request to trade asset                             │   │
│  │    • Admin review required                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │                               │                       │
│                    ▼                               ▼                       │
│  ┌─────────────────────────────┐   ┌─────────────────────────────────────┐ │
│  │ 3a. Admin Approves           │   │ 3b. Admin Rejects                   │ │
│  │     Status: WHITELISTED (2)  │   │     Status: BLACKLISTED (4)         │ │
│  │     • User can trade asset   │   │     • User cannot trade             │ │
│  └─────────────────────────────┘   └─────────────────────────────────────┘ │
│                    │                               │                       │
│                    ▼                               │                       │
│  ┌─────────────────────────────┐                   │                       │
│  │ 4. User Hides Asset          │                   │                       │
│  │    Status: IGNORED (5)       │                   │                       │
│  │    • Visible: false          │                   │                       │
│  │    • Can be unhidden later   │                   │                       │
│  └─────────────────────────────┘                   │                       │
│                                                    │                       │
│                    └───────────────────────────────┘                       │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 5. User Removes Asset (Delete)                                       │   │
│  │    • Entry removed from user_asset_list                              │   │
│  │    • User can re-add later                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Error Responses
Unauthorized (401)
json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
Forbidden (403) - Jurisdiction Mismatch
json
{
  "error": "Forbidden",
  "message": "Asset not authorized for user's jurisdiction",
  "details": "Asset jurisdictions: [US, EU]. User jurisdictions: [UK, JP]",
  "asset_key": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2"
}
Forbidden (403) - Asset Not Listed
json
{
  "error": "Forbidden",
  "message": "Asset is not available for trading",
  "details": "Asset status: PENDING_APPROVAL (2)",
  "asset_key": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Missing required parameter: asset_key"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Asset not found",
  "asset_key": "INVALID-ASSET-KEY"
}
Conflict (409) - Duplicate User Asset
json
{
  "error": "Conflict",
  "message": "Asset already in user's list",
  "user_asset_list_key": "BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2-ddb9e00a-147b-4fdd-b9bc-0a79b01202d2"
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
ADMIN_ACCOUNT_STORE	Admin account store endpoint	github.com/sologenic/com-be-admin-account-store/
ACCOUNT_STORE	Account store endpoint	github.com/sologenic/com-be-account-store/
ASSET_STORE	Asset store endpoint	github.com/sologenic/com-be-asset-store/
JURISDICTION_STORE	Jurisdiction store endpoint	github.com/sologenic/com-be-jurisdiction-store/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-model
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
PAGE_SIZE	Default page size for list endpoints	20
MAX_PAGE_SIZE	Maximum page size allowed	100
Example Environment Configuration
bash
# Required
ASSET_STORE=localhost:50055
JURISDICTION_STORE=localhost:50056
ACCOUNT_STORE=localhost:50057
ADMIN_ACCOUNT_STORE=localhost:50058
ORGANIZATION_STORE=localhost:50059
AUTH_FIREBASE_SERVICE=localhost:50070

# Optional
LOG_LEVEL=debug
PAGE_SIZE=50
MAX_PAGE_SIZE=200

# HTTP Configuration
HTTP_CONFIG='{
  "port": ":8080",
  "cors": {
    "allowedOrigins": ["http://localhost:3000", "https://app.sologenic.org"]
  },
  "timeouts": {
    "read": "10s",
    "write": "10s",
    "idle": "10s",
    "shutdown": "10s"
  }
}'
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Asset not visible	Jurisdiction mismatch	Check user's allowed jurisdictions
Asset not found	Wrong asset_key format	Verify format: {symbol}-{org_id}-{version}
Can't add to list	Asset already exists	Check if already in user's list
Status update fails	Invalid status value	Use valid status ID (1-5) or name
Empty asset list	No listed assets in user's jurisdiction	Check jurisdiction configuration
403 Forbidden	Asset status not LISTED	Asset must be approved and listed
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check user's jurisdictions:

bash
# This would typically be retrieved from UserJurisdiction database
# Contact system administrator for jurisdiction configuration
Verify asset exists and status:

bash
curl -X GET "/asset/get?asset_key=BTC-34422ce6-7b51-4a15-accb-34959f39d8ca-2" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
List user's assets:

bash
curl -X GET "/asset/user/list?account_id=<account-id>&visible=true" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Best Practices
Asset Discovery
Use Filters: Always use jurisdiction_ids filter for better performance

Paginate Results: Use offset parameter for large result sets

Cache Asset Data: Cache frequently accessed assets client-side

Handle 403 Gracefully: Show user-friendly message for jurisdiction-restricted assets

User Asset Lists
Batch Add Operations: Add multiple assets in separate requests with proper error handling

Update Status Appropriately: Use WHITELISTING_REQUESTED only when user intends to trade

Respect Visibility: Honor user's visibility preferences in UI

Sync Periodically: Periodically refresh user's asset list to reflect status changes

Performance Optimization
| Scenario | Recommendation
Initial asset list load	Use jurisdiction_ids filter with asset_type
Search functionality	Implement server-side search with filters
Real-time price updates	Subscribe to AED service for price data
Large user asset lists	Implement client-side pagination
Security
Validate Jurisdictions: Never bypass jurisdiction checks on client side

Use HTTPS: Always use HTTPS in production

Token Management: Implement token refresh mechanism

Audit Trail: Log important actions (whitelist requests, status changes)

Related Services
Service	Description
AED Service	Price data for assets
Jurisdiction Service	Jurisdiction management
Admin Asset Service	Asset administration (create, update, delist)
Organization Service	Organization management
Admin Account Service	User and role management
License
This documentation is part of the TX Marketplace platform.

text

Now let's verify the Asset Service documentation was created and update the marketplace README:

```bash
ls -la ~/dev/TXdocumentation/asset/
bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the Asset Service section to the marketplace README:

markdown
### Asset Service (Normal User)

The Asset Service provides RESTful interfaces for normal users to view and manage assets, with jurisdiction-based access control.

📖 **[Asset Service Documentation](../asset/asset-service.md)**

**Key Features:**
- View assets by key with jurisdiction filtering
- List available assets based on user's jurisdiction
- Bookmark assets to user's personal list
- Request whitelisting for trading
- Update asset visibility in user's list
- Track asset status (watchlist, whitelisted, blacklisted)

**Asset Access Rules:**
| Rule | Description |
|------|-------------|
| Status | Asset must be LISTED (3) |
| Jurisdiction | Asset jurisdiction must match user's allowed jurisdictions |
| User Auth | Valid Firebase authentication required |

**User Asset Statuses:**
| Status | Description |
|--------|-------------|
| WATCHLIST (1) | Monitored but not tradable |
| WHITELISTED (2) | Approved for trading |
| WHITELISTING_REQUESTED (3) | Pending admin approval |
| BLACKLISTED (4) | Blocked from trading |
| IGNORED (5) | Hidden from user |

**Quick Examples:**
```bash
# Get asset by key
GET /asset/get?asset_key=BTC-org-1

# List available assets
GET /asset/list?jurisdiction_ids=US,EU&asset_type=2

# Add asset to user's list
POST /asset/user/add
{
  "AccountID": "user-123",
  "Wallet": "rWALLET...",
  "AssetKey": "BTC-org-1"
}

# Update asset visibility
PUT /asset/user/update/visible?user_asset_list_key=key&visible=false
Asset Key Format: {symbol}-{organization_id}-{version}

User Asset List Key Format: {asset_key}-{account_id}
