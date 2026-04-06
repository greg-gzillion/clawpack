# Alert Service

The Alert Service provides RESTful interfaces for managing price alerts. Users can create, delete, and retrieve price alerts for specific assets. The service validates target prices against current market prices with configurable percentage limits.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Alert Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬─────────────────────────────────────┤ │
│ │ POST /add │ DELETE /delete│ GET /get │ │
│ │ (Create alert)│ (Remove alert)│ (Retrieve by asset key) │ │
│ └───────────────┴───────────────┴─────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Alert Store │ Organization │ User Store │ Role Store │ │
│ │ │ Store │ │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Systems │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Firebase Authentication (User identity) │ │
│ │ • Price Feed Service (Current market prices) │ │
│ │ • Asset Service (Asset metadata) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| POST /api/alert/add | ORGANIZATION_ADMINISTRATOR | Create new price alert |
| DELETE /api/alert/delete | ORGANIZATION_ADMINISTRATOR | Delete existing alert |
| GET /api/alert/get | ORGANIZATION_ADMINISTRATOR | Retrieve alert by asset key |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Organization ID in `OrganizationID` header (tenant isolation)
- Network in `Network` header (mainnet, testnet, devnet)

## Data Models

### Alert Object

| Field | Type | Description |
|-------|------|-------------|
| Account | string | User account identifier (owner of alert) |
| AssetKey | string | Unique identifier for the asset to monitor |
| OrganizationID | string | Organization UUID |
| TargetPrice | float64 | Price at which alert should trigger |
| Status | int | Alert status (see Alert Status values) |

### Audit Object

| Field | Type | Description |
|-------|------|-------------|
| ChangedBy | string | User who made the change |
| ChangedAt | Timestamp | When the change was made |

### MetaData Object

| Field | Type | Description |
|-------|------|-------------|
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |
| UpdatedByAccount | string | Account that last updated the alert |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

### Alert Status Values

| Status ID | Status Name | Description |
|-----------|-------------|-------------|
| 1 | ACTIVE | Alert is active and monitoring |
| 2 | TRIGGERED | Alert has been triggered |
| 3 | DISABLED | Alert is disabled (manually or expired) |
| 4 | DELETED | Alert has been deleted |

### Network Values

| Network ID | Network Name | Description |
|------------|--------------|-------------|
| 1 | mainnet | Production network |
| 2 | testnet | Testing network |
| 3 | devnet | Development network |

## API Endpoints

### POST /api/alert/add

Creates a new price alert for the specified asset. The service validates that the target price is within acceptable percentage limits of the current market price.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| OrganizationID | Organization UUID | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Request Body

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| AssetKey | string | Unique identifier for the asset to monitor | Yes |
| TargetPrice | float64 | Price at which alert should trigger | Yes |
| Status | int | Alert status (default: 1 = ACTIVE) | No |

#### Example Request

```bash
curl --request POST \
  --url https://api.admin.sologenic.org/api/alert/add \
  --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIs...' \
  --header 'Content-Type: application/json' \
  --header 'Network: testnet' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --data '{
    "AssetKey": "BTCUSDC",
    "TargetPrice": 150.50,
    "Status": 1
  }'
Example Response
Success (201 Created)

json
{
  "message": "alert created successfully"
}
Error (400 Bad Request) - Price Validation Failed

json
{
  "error": "price validation failed: target price 200.00 is 25.50% away from current price 150.00 (max allowed: 10.50%)"
}
Error (400 Bad Request) - Missing Fields

json
{
  "error": "missing or invalid required fields"
}
Error (401 Unauthorized)

json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
Error (403 Forbidden)

json
{
  "error": "Forbidden",
  "message": "Insufficient permissions for this operation. Required role: ORGANIZATION_ADMINISTRATOR"
}
Error (404 Not Found)

json
{
  "error": "Asset not found",
  "message": "No asset found with key: BTCUSDC"
}
DELETE /api/alert/delete
Removes an existing alert. Only the owner of the alert (authenticated user) can delete it.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
AssetKey	string	Unique identifier of the alert to delete	Yes
Example Request
bash
curl --request DELETE \
  --url https://api.admin.sologenic.org/api/alert/delete \
  --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIs...' \
  --header 'Content-Type: application/json' \
  --header 'Network: testnet' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --data '{
    "AssetKey": "BTCUSDC"
  }'
Example Response
Success (200 OK)

json
{
  "message": "alert deleted successfully"
}
Error (404 Not Found)

json
{
  "error": "alert not found"
}
Error (403 Forbidden) - Not Owner

json
{
  "error": "Forbidden",
  "message": "Cannot delete alert owned by another user"
}
GET /api/alert/get
Retrieves a specific alert by its asset key. Only the owner of the alert can retrieve it.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required
asset_key	string	Unique identifier of the alert to retrieve	Yes
Example Request
bash
curl --request GET \
  --url 'https://api.admin.sologenic.org/api/alert/get?asset_key=BTCUSDC' \
  --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIs...' \
  --header 'Network: testnet' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71'
Example Response
Success (200 OK)

json
{
  "Alert": {
    "Account": "O7ksna16ZhYlSh6TPTeCJLbNQq73",
    "AssetKey": "BTCUSDC",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "TargetPrice": 150.5,
    "Status": 1
  },
  "Audit": {
    "ChangedAt": {
      "seconds": 1749580302,
      "nanos": 123456000
    },
    "ChangedBy": "O7ksna16ZhYlSh6TPTeCJLbNQq73"
  },
  "MetaData": {
    "Network": 2,
    "CreatedAt": {
      "seconds": 1749580302,
      "nanos": 123456000
    },
    "UpdatedAt": {
      "seconds": 1749580302,
      "nanos": 123456000
    },
    "UpdatedByAccount": "O7ksna16ZhYlSh6TPTeCJLbNQq73"
  }
}
Error (404 Not Found)

json
{
  "error": "alert not found"
}
Error (400 Bad Request)

json
{
  "error": "missing asset_key parameter"
}
Alert Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Alert Lifecycle                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Alert Created                                                     │   │
│  │    Status: ACTIVE (1)                                                │   │
│  │    • User sets AssetKey and TargetPrice                              │   │
│  │    • Service validates price deviation ≤ max allowed                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Monitoring                                                        │   │
│  │    Status: ACTIVE (1)                                                │   │
│  │    • Service continuously monitors market price                      │   │
│  │    • Compares current price against target                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │                               │                       │
│                    ▼                               ▼                       │
│  ┌─────────────────────────────┐   ┌─────────────────────────────────────┐ │
│  │ 3a. Price Target Reached     │   │ 3b. User Deletes Alert              │ │
│  │     Status: TRIGGERED (2)    │   │     Status: DELETED (4)             │ │
│  │     • Notification sent      │   │     • Alert removed from monitoring │ │
│  │     • Alert may auto-disable │   │     • User can recreate later       │ │
│  └─────────────────────────────┘   └─────────────────────────────────────┘ │
│                    │                               │                       │
│                    ▼                               │                       │
│  ┌─────────────────────────────┐                   │                       │
│  │ 4. Alert Disabled (Optional)│                   │                       │
│  │    Status: DISABLED (3)      │                   │                       │
│  │    • Manual disable          │                   │                       │
│  │    • Auto-disable after      │                   │                       │
│  │      trigger                 │                   │                       │
│  └─────────────────────────────┘                   │                       │
│                                                    │                       │
│                    └───────────────────────────────┘                       │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 5. End State                                                         │   │
│  │    • Alert no longer active                                          │   │
│  │    • Record kept for audit purposes                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Price Validation
The Alert Service validates that target prices are within acceptable percentage limits of current market prices to prevent:

Accidental misconfiguration (e.g., decimal point errors)

Market manipulation attempts

Unreasonable alert targets

Validation Rules
Validation	Description	Default Limit
Max Deviation	Target price cannot exceed current price by more than X%	10.5%
Min Deviation	Target price cannot be below current price by more than X%	10.5%
Zero Price	Target price must be > 0	N/A
Validation Examples
Current Price	Target Price	Deviation	Allowed	Result
$100.00	$105.00	5.0%	Yes	✅ Pass
$100.00	$110.50	10.5%	Yes	✅ Pass (boundary)
$100.00	$111.00	11.0%	No	❌ Fail
$100.00	$90.00	10.0%	Yes	✅ Pass
$100.00	$89.00	11.0%	No	❌ Fail
$100.00	$0.00	N/A	No	❌ Fail
Multiple Alerts per Asset
Users can create multiple alerts for the same asset with different target prices.

Example: Multiple BTC Alerts
bash
# Alert 1: BTC reaches $50,000
curl -X POST /api/alert/add \
  -H "Authorization: Bearer <token>" \
  -d '{"AssetKey": "BTCUSDC", "TargetPrice": 50000, "Status": 1}'

# Alert 2: BTC reaches $55,000
curl -X POST /api/alert/add \
  -H "Authorization: Bearer <token>" \
  -d '{"AssetKey": "BTCUSDC", "TargetPrice": 55000, "Status": 1}'

# Alert 3: BTC drops to $45,000
curl -X POST /api/alert/add \
  -H "Authorization: Bearer <token>" \
  -d '{"AssetKey": "BTCUSDC", "TargetPrice": 45000, "Status": 1}'
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
  "message": "Insufficient permissions for this operation. Required role: ORGANIZATION_ADMINISTRATOR"
}
Forbidden - Not Owner (403)
json
{
  "error": "Forbidden",
  "message": "Cannot delete alert owned by another user"
}
Bad Request (400) - Missing Asset Key
json
{
  "error": "missing asset_key parameter"
}
Bad Request (400) - Invalid Target Price
json
{
  "error": "invalid target price",
  "message": "Target price must be greater than 0"
}
Bad Request (400) - Price Deviation Exceeds Limit
json
{
  "error": "price validation failed",
  "message": "target price 200.00 is 25.50% away from current price 150.00 (max allowed: 10.50%)",
  "current_price": 150.00,
  "target_price": 200.00,
  "deviation_percent": 25.50,
  "max_allowed_percent": 10.50
}
Not Found (404)
json
{
  "error": "alert not found"
}
Not Found (404) - Asset Not Found
json
{
  "error": "Asset not found",
  "message": "No asset found with key: INVALID_ASSET_KEY"
}
Conflict (409) - Alert Already Exists
json
{
  "error": "Conflict",
  "message": "Alert already exists for asset key: BTCUSDC",
  "existing_alert": {
    "target_price": 150.50,
    "status": 1
  }
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/http/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-model
ALERT_STORE	Alert store service endpoint	github.com/sologenic/com-fs-alert-model
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-model
ROLE_STORE	Role management service endpoint	github.com/sologenic/com-fs-role-model
USER_STORE	User management service endpoint	github.com/sologenic/com-fs-user-model
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
MAX_PRICE_DEVIATION_PERCENT	Maximum allowed price deviation for alerts	10.5
Example Environment Configuration
bash
# Required
ALERT_STORE=localhost:50053
AUTH_FIREBASE_SERVICE=localhost:50070
ROLE_STORE=localhost:50066
USER_STORE=localhost:50049
ORGANIZATION_STORE=localhost:50060
FEATURE_FLAG_STORE=localhost:50055

# Optional
LOG_LEVEL=debug
MAX_PRICE_DEVIATION_PERCENT=15.0

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
Alert creation fails with price deviation error	Target price too far from current price	Adjust target price within allowed deviation (default 10.5%)
Cannot delete alert	Not the owner of the alert	Only the user who created the alert can delete it
Alert not found	Wrong asset_key or alert doesn't exist	Verify asset_key matches exactly
Duplicate alert	Alert already exists for asset	Use existing alert or delete it first
Permission denied	Missing ORGANIZATION_ADMINISTRATOR role	Contact organization administrator
Alert never triggers	Status not ACTIVE or price not reached	Check alert status and current market price
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check alert existence:

bash
# Try to retrieve the alert
curl -X GET "/api/alert/get?asset_key=BTCUSDC" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet"
Verify current market price:

bash
# Get current price from AED service
curl -X GET "/api/aed/tickers?symbols=<base64_symbols>" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet"
Best Practices
Alert Creation
Use Reasonable Targets: Set target prices within 10% of current price

Monitor Active Alerts: Regularly review and clean up stale alerts

Avoid Duplicates: Check for existing alerts before creating new ones

Use Descriptive Asset Keys: Ensure asset keys are consistent across services

Alert Management
Clean Up Triggered Alerts: Delete or disable alerts after they trigger

Set Appropriate Status: Use DISABLED status for temporarily inactive alerts

Audit Trail: Review audit logs for unauthorized changes

Test on Testnet: Validate alert behavior on testnet before mainnet

Performance Optimization
Scenario	Recommendation
Many alerts per user	Implement client-side pagination
High-frequency price updates	Use webhooks instead of polling
Alert history	Archive old alerts to separate storage
Bulk operations	Use batch endpoints if available
Related Services
Service	Description
AED Service	Current market prices for validation
Admin Asset Service	Asset metadata and keys
Organization Service	Tenant organization management
Admin Account Service	User and role management
Admin Notification Service	Alert trigger notifications
License
This documentation is part of the TX Marketplace platform.
