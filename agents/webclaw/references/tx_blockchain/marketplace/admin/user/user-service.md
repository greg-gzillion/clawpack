# Admin User Service

The Admin User Service provides API interfaces that enable organization administrators to manage retail users within a multi-tier system. It handles user profiles, wallet associations, social links, status management, and tenant isolation.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin User Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ GET /get │ GET /list │ PUT /update │ PUT /update/status│ │
│ │ (By ID) │ (With filter) │ (User info) │ (Status only) │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ User Store │ Account Store │ Role Store │ Feature Flag │ │
│ │ │ │ │ Store │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Systems │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Firebase Authentication (User identity) │ │
│ │ • Organization Service (Tenant isolation) │ │
│ │ • KYC Service (Verification status) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role-Based Access Control

All admin endpoints are protected by role-based access control and default to the `ORGANIZATION_ADMINISTRATOR` role. Permissions are managed dynamically by Organization administrators.

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/adminuser/get | ORGANIZATION_ADMINISTRATOR | Get user by ID or external ID |
| GET /api/adminuser/list | ORGANIZATION_ADMINISTRATOR | List users with filtering |
| PUT /api/adminuser/update | ORGANIZATION_ADMINISTRATOR | Update user information |
| PUT /api/adminuser/update/status | ORGANIZATION_ADMINISTRATOR | Update user status |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Organization ID in `OrganizationID` header (enforces tenant isolation)
- Network in `Network` header (mainnet, testnet, devnet)

## Data Models

### User Object

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| UserID | string | User email or unique identifier | Yes |
| FirstName | string | User's first name | No |
| LastName | string | User's last name | No |
| Address | string | Physical address | No |
| Avatar | string | URL to profile avatar image | No |
| Alias | string | Display name/nickname | No |
| Description | string | User bio or description | No |
| Status | int | User account status (see Status values) | Yes |
| Wallets | []Wallet | Associated blockchain wallets | No |
| Socials | []Social | Social media links | No |
| Language | Language | Preferred language | No |
| ExternalUserID | string | External reference ID (e.g., from KYC provider) | No |
| OrganizationID | string | Organization UUID (tenant) | Yes |
| Role | int | User role within organization | Yes |

### Wallet Object

| Field | Type | Description |
|-------|------|-------------|
| Address | string | Blockchain wallet address (e.g., XRP/Coreum address) |
| Alias | string | Friendly name for the wallet |
| Type | int | Wallet type (see Wallet Type values) |

### Social Object

| Field | Type | Description |
|-------|------|-------------|
| URL | string | Full URL to social media profile |
| Type | int | Social media platform type (see Social Type values) |

### Language Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Language | string | BCP 47 language code | "en-US", "es-ES", "fr-FR" |

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
| Reason | string | Reason for the change |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

### Filter Object (for GET /list)

```protobuf
message Filter {
    repeated string UserIDs = 1;      // Filter by specific user IDs
    optional Order Order = 2;          // Sort order
    optional int32 Offset = 3;         // Pagination offset (default: 0)
    optional int32 Limit = 4;          // Items per page (default: 20)
    optional metadata.Network Network = 5;
    string OrganizationID = 6;         // Required - tenant isolation
}
Order Object
Field	Type	Description
Field	string	Field to sort by (e.g., "CreatedAt", "UserID")
Direction	string	"ASC" or "DESC"
User Status Values
Status ID	Status Name	Description
1	ACTIVE	User account is active and can access platform
2	SUSPENDED	User account is suspended (temporarily blocked)
3	DISABLED	User account is permanently disabled
4	PENDING_VERIFICATION	Awaiting email/phone verification
5	PENDING_KYC	Awaiting KYC verification
Wallet Types
Type ID	Type Name	Description
1	PRIMARY	Primary/default wallet for transactions
2	SECONDARY	Secondary wallet for specific use cases
3	TRADING	Wallet designated for trading activities
4	COLD_STORAGE	Cold storage wallet (not for trading)
5	CUSTODIAL	Custodial wallet managed by platform
Social Media Types
Type ID	Platform	Description
1	FACEBOOK	Facebook profile
2	GITHUB	GitHub profile
3	INSTAGRAM	Instagram profile
4	REDDIT	Reddit profile
5	TWITTER	Twitter/X profile
6	TELEGRAM	Telegram username
7	DISCORD	Discord username
8	MEDIUM	Medium blog
9	LINKEDIN	LinkedIn profile
10	YOUTUBE	YouTube channel
User Role Values
Role ID	Role Name	Description
1	NORMAL_USER	Standard retail user
2	PREMIUM_USER	Premium tier user
3	INSTITUTIONAL_USER	Institutional/corporate user
4	BROKER_USER	Broker-affiliated user
Network Values
Network ID	Network Name	Description
1	mainnet	Production network
2	testnet	Testing network
3	devnet	Development network
API Endpoints
GET /api/adminuser/get
Retrieves User information for the given user_id or external_id.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required (one of)
user_id	string	User email or identifier	Yes (with external_id)
external_id	string	External reference ID	Yes (with user_id)
Example Request
bash
# Get by user_id
curl -X GET \
  "https://api.admin.sologenic.org/api/adminuser/get?user_id=john.doe@example.com" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"

# Get by external_id
curl -X GET \
  "https://api.admin.sologenic.org/api/adminuser/get?external_id=cbf6a315-3438-4ea0-a27b-3f0041ade118" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
Example Response
json
{
  "User": {
    "UserID": "john.doe@example.com",
    "FirstName": "John",
    "LastName": "Doe",
    "Address": "123 Main Street, Apt 4B, Cityville, ST 12345",
    "Avatar": "https://example.com/avatars/johndoe.png",
    "Alias": "JD",
    "Description": "Blockchain enthusiast and investor",
    "Status": 2,
    "Wallets": [
      {
        "Address": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
        "Alias": "Primary Wallet",
        "Type": 3
      },
      {
        "Address": "rBKPS4oLSaV2KVVuHH8EpQqMGgGefGFRs9",
        "Alias": "Savings",
        "Type": 1
      }
    ],
    "Socials": [
      {
        "URL": "https://twitter.com/johndoe",
        "Type": 5
      },
      {
        "URL": "https://github.com/johndoe",
        "Type": 2
      },
      {
        "URL": "https://linkedin.com/in/johndoe",
        "Type": 9
      }
    ],
    "Language": {
      "Language": "en-US"
    },
    "ExternalUserID": "cbf6a315-3438-4ea0-a27b-3f0041ade118",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Role": 1
  },
  "MetaData": {
    "Network": 2,
    "UpdatedAt": {
      "seconds": 1741992596,
      "nanos": 71607000
    },
    "CreatedAt": {
      "seconds": 1741984486,
      "nanos": 16812090
    }
  },
  "Audit": {
    "ChangedBy": "admin@organization.org",
    "ChangedAt": {
      "seconds": 1741992245,
      "nanos": 360512000
    }
  }
}
Error Responses
Status Code	Description
200	Success - User found
400	Bad request - Missing user_id or external_id
401	Unauthorized - Invalid or missing token
403	Forbidden - User not in organization scope
404	Not found - User does not exist
500	Internal server error
GET /api/adminuser/list
Retrieves all User information based on the given Filter, with pagination.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Default
filter	string	Base64 encoded Filter object	Required
limit	int	Items per page	20
offset	int	Pagination offset	0
Note: OrganizationID is a mandatory parameter that enforces proper organizational data boundaries, ensuring each tenant can only access records within their designated scope.

Filter Examples
Basic Filter (No UserIDs)
json
{
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Limit": 20,
  "Offset": 0
}
Filter by Specific User IDs
json
{
  "UserIDs": ["user1@example.com", "user2@example.com"],
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Limit": 50
}
Filter with Sorting
json
{
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Order": {
    "Field": "CreatedAt",
    "Direction": "DESC"
  },
  "Limit": 20,
  "Offset": 0
}
Example Request
bash
# Base64 encoded filter: {"OrganizationID":"72c4c072-2fe4-4f72-ae9d-d9d52a05fd71","Limit":20,"Offset":0}
curl -X GET \
  "https://api.admin.sologenic.org/api/adminuser/list?filter=eyJPcmdhbml6YXRpb25JRCI6IjcyYzRjMDcyLTJmZTQtNGY3Mi1hZTlkLWQ5ZDUyYTA1ZmQ3MSIsIkxpbWl0IjoyMCwiT2Zmc2V0IjowfQ==" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
Example Response
json
{
  "Users": [
    {
      "User": {
        "UserID": "john.doe@example.com",
        "FirstName": "John",
        "LastName": "Doe",
        "Address": "123 Main Street, Apt 4B, Cityville, ST 12345",
        "Avatar": "https://example.com/avatars/johndoe.png",
        "Alias": "JD",
        "Description": "Blockchain enthusiast and investor",
        "Status": 1,
        "Wallets": [
          {
            "Address": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
            "Alias": "Primary Wallet",
            "Type": 3
          }
        ],
        "Socials": [
          {
            "URL": "https://twitter.com/johndoe",
            "Type": 5
          }
        ],
        "Language": {
          "Language": "en-US"
        },
        "ExternalUserID": "cbf6a315-3438-4ea0-a27b-3f0041ade118",
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Role": 1
      },
      "MetaData": {
        "Network": 2,
        "UpdatedAt": {
          "seconds": 1741984486,
          "nanos": 16812450
        },
        "CreatedAt": {
          "seconds": 1741984486,
          "nanos": 16812090
        }
      },
      "Audit": {
        "ChangedAt": {
          "seconds": 1741984486,
          "nanos": 16812560
        }
      }
    }
  ],
  "Offset": 20,
  "Total": 45
}
Error Responses
Status Code	Description
200	Success - Returns array (may be empty)
400	Bad request - Invalid filter format
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
500	Internal server error
PUT /api/adminuser/update
Updates user information for a specified User.

Important: Status cannot be updated using this endpoint. Use /api/adminuser/update/status for status changes.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
User.UserID	string	User identifier	Yes
User.FirstName	string	Updated first name	No
User.LastName	string	Updated last name	No
User.Address	string	Updated address	No
User.Avatar	string	Updated avatar URL	No
User.Alias	string	Updated display name	No
User.Description	string	Updated bio	No
User.Wallets	[]Wallet	Updated wallet list	No
User.Socials	[]Social	Updated social links	No
User.Language	Language	Updated language preference	No
User.Role	int	Updated role	No
MetaData.Network	int	Network identifier	Yes
Example Request
bash
curl -X PUT \
  "https://api.admin.sologenic.org/api/adminuser/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "User": {
      "UserID": "john.doe@example.com",
      "FirstName": "John",
      "LastName": "Doe",
      "Address": "456 New Address, Suite 100, Metropolis, ST 67890",
      "Avatar": "https://example.com/avatars/johndoe_new.png",
      "Alias": "JohnnyD",
      "Description": "Senior blockchain architect and DeFi expert",
      "Wallets": [
        {
          "Address": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
          "Alias": "Primary Wallet",
          "Type": 3
        },
        {
          "Address": "rBKPS4oLSaV2KVVuHH8EpQqMGgGefGFRs9",
          "Alias": "Trading Wallet",
          "Type": 3
        }
      ],
      "Socials": [
        {
          "URL": "https://twitter.com/johndoe",
          "Type": 5
        },
        {
          "URL": "https://github.com/johndoe",
          "Type": 2
        },
        {
          "URL": "https://linkedin.com/in/johndoe",
          "Type": 9
        },
        {
          "URL": "https://medium.com/@johndoe",
          "Type": 8
        }
      ],
      "Language": {
        "Language": "en-US"
      },
      "Role": 2
    },
    "MetaData": {
      "Network": 2
    }
  }'
Example Response
json
{
  "UserID": "john.doe@example.com",
  "Network": 2
}
Error Responses
Status Code	Description
200	Success - User updated
400	Bad request - Missing required fields or attempting to update status
401	Unauthorized - Invalid or missing token
403	Forbidden - Cannot modify user outside organization
404	Not found - User does not exist
409	Conflict - Concurrent update conflict
500	Internal server error
PUT /api/adminuser/update/status
Updates the status for a User. Use this endpoint for all status changes (activate, suspend, disable, etc.).

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
UserID	string	User identifier	Yes
OrganizationID	string	Organization UUID	Yes
Status	int	New status value (1-5)	Yes
Network	int	Network identifier	Yes
Reason	string	Reason for status change	No
Example Request
bash
# Suspend a user
curl -X PUT \
  "https://api.admin.sologenic.org/api/adminuser/update/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "UserID": "john.doe@example.com",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Status": 2,
    "Network": 2,
    "Reason": "Violation of terms of service"
  }'

# Activate a user
curl -X PUT \
  "https://api.admin.sologenic.org/api/adminuser/update/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "UserID": "john.doe@example.com",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Status": 1,
    "Network": 2
  }'
Example Response
json
{
  "Success": true,
  "UserID": "john.doe@example.com",
  "PreviousStatus": 1,
  "CurrentStatus": 2,
  "Network": 2
}
Error Responses
Status Code	Description
200	Success - Status updated
400	Bad request - Invalid status value
401	Unauthorized - Invalid or missing token
403	Forbidden - Cannot modify user outside organization
404	Not found - User does not exist
500	Internal server error
Tenant Isolation
The OrganizationID header is a mandatory parameter that enforces proper organizational data boundaries, ensuring each tenant can only access records within their designated scope.

text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Tenant Isolation                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Organization A (ID: org-a-123)    Organization B (ID: org-b-456)          │
│  ┌─────────────────────────┐       ┌─────────────────────────┐            │
│  │ User A1                  │       │ User B1                  │            │
│  │ User A2                  │       │ User B2                  │            │
│  │ User A3                  │       │ User B3                  │            │
│  └─────────────────────────┘       └─────────────────────────┘            │
│                                                                             │
│  Admin from Org A can only see/modify Org A users                          │
│  Admin from Org B can only see/modify Org B users                          │
│                                                                             │
│  Platform administrators (Sologenic Admin) can see all users               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Base64 Filter Examples
Example 1: Basic Pagination
json
{
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Limit": 20,
  "Offset": 0
}
Base64 encoded:

text
ewogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJMaW1pdCI6IDIwLAogICJPZmZzZXQiOiAwCn0=
Example 2: Filter Specific Users
json
{
  "UserIDs": ["user1@example.com", "user2@example.com", "user3@example.com"],
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Limit": 50
}
Base64 encoded:

text
ewogICJVc2VySURzIjogWyJ1c2VyMUBleGFtcGxlLmNvbSIsICJ1c2VyMkBleGFtcGxlLmNvbSIsICJ1c2VyM0BleGFtcGxlLmNvbSJdLAogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJMaW1pdCI6IDUwCn0=
Example 3: Sorted by Creation Date
json
{
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Order": {
    "Field": "CreatedAt",
    "Direction": "DESC"
  },
  "Limit": 100,
  "Offset": 0
}
Base64 encoded:

text
ewogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJPcmRlciI6IHsKICAgICJGaWVsZCI6ICJDcmVhdGVkQXQiLAogICAgIkRpcmVjdGlvbiI6ICJERVNDIgogIH0sCiAgIkxpbWl0IjogMTAwLAogICJPZmZzZXQiOiAwCn0=
User Status Workflow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         User Status Workflow                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. User Registration                                                 │   │
│  │    Status: PENDING_VERIFICATION (4)                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Email/Phone Verified                                             │   │
│  │    Status: PENDING_KYC (5)                                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │                               │                       │
│                    ▼                               ▼                       │
│  ┌─────────────────────────────┐   ┌─────────────────────────────────────┐ │
│  │ 3a. KYC Approved             │   │ 3b. KYC Rejected                    │ │
│  │     Status: ACTIVE (1)       │   │     Status: DISABLED (3)            │ │
│  └─────────────────────────────┘   └─────────────────────────────────────┘ │
│                    │                               │                       │
│                    ▼                               │                       │
│  ┌─────────────────────────────┐                   │                       │
│  │ 4. Violation Detected       │                   │                       │
│  │    Status: SUSPENDED (2)    │                   │                       │
│  └─────────────────────────────┘                   │                       │
│                    │                               │                       │
│                    ├───────────────────────────────┘                       │
│                    │                                                       │
│                    ▼                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 5. Permanent Action                                                  │   │
│  │    Status: DISABLED (3)                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
USER_STORE	User service endpoint	github.com/sologenic/com-fs-user-model/
ACCOUNT_STORE	Admin account service endpoint	github.com/sologenic/com-fs-admin-account-model/
ROLE_STORE	Admin role service endpoint	github.com/sologenic/com-fs-admin-role-model/
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-admin-organization-model/
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
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
Forbidden - Organization Mismatch (403)
json
{
  "error": "Forbidden",
  "message": "User does not belong to your organization",
  "details": "Cannot access user from different organization"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid status value",
  "details": "Status must be between 1 and 5",
  "allowed_values": [1, 2, 3, 4, 5]
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "User not found",
  "details": "No user found with ID: john.doe@example.com"
}
Conflict (409)
json
{
  "error": "Conflict",
  "message": "Concurrent update detected",
  "details": "User was modified by another admin. Please refresh and try again."
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Cannot find user	Wrong UserID format	Use email address or external_id
Cannot update user	Missing required fields	Ensure UserID and OrganizationID are provided
Status update fails	Invalid status value	Use valid status (1-5)
List returns empty	Wrong OrganizationID	Verify organization UUID
Permission denied	Insufficient role	User must have ORGANIZATION_ADMINISTRATOR
Wallet address invalid	Wrong blockchain format	Use valid XRP/Coreum address format
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check user existence:

bash
# Get user by email
curl -X GET "/api/adminuser/get?user_id=user@example.com" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet"
List all users in organization:

bash
# Base64 filter: {"OrganizationID":"<org-id>","Limit":100}
FILTER=$(echo -n "{\"OrganizationID\":\"<org-id>\",\"Limit\":100}" | base64)
curl -X GET "/api/adminuser/list?filter=$FILTER" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet"
Best Practices
User Management
Use ExternalUserID: Store external references (e.g., from KYC provider) in ExternalUserID

Keep Wallets Updated: Maintain accurate wallet addresses for each user

Regular Audits: Monitor user status changes and update reasons

Data Privacy: Only store necessary user information

Status Management
Document Status Changes: Always provide a Reason when changing status

Suspension Before Disable: Use SUSPENDED for temporary issues, DISABLED for permanent

KYC Integration: Link KYC status to user status

Notify Users: Inform users of status changes through notification service

Security
Tenant Isolation: Always include OrganizationID header

Audit Trail: All changes are logged with ChangedBy and ChangedAt

Role Validation: Ensure users have appropriate roles

Sensitive Data: Avoid storing sensitive information in Description or Address fields

Related Services
Service	Description
Admin Account Service	Admin user and role management
Admin KYC Service	KYC verification status
Organization Service	Tenant organization management
Admin Notification Service	User notifications
File Service	Avatar image storage
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the Admin User Service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the Admin User Service section under Admin Services:

markdown
### Admin User Service

The Admin User Service provides API interfaces that enable organization administrators to manage retail users within a multi-tier system.

📖 **[Admin User Service Documentation](./admin/user/user-service.md)**

**Key Features:**
- Get user by ID or external ID
- List users with pagination and filtering
- Update user profile information
- Update user status (activate, suspend, disable)
- Multi-wallet support per user
- Social media profile links
- Language preferences
- Tenant isolation via OrganizationID

**User Statuses:**
| Status | Description |
|--------|-------------|
| ACTIVE (1) | Account active
| SUSPENDED (2) | Temporarily blocked |
| DISABLED (3) | Permanently disabled |
| PENDING_VERIFICATION (4) | Awaiting email/phone verification |
| PENDING_KYC (5) | Awaiting KYC verification |

**User Fields:**
| Field | Description |
|-------|-------------|
| UserID | User email or identifier |
| FirstName/LastName | User's full name |
| Address | Physical address |
| Avatar | Profile picture URL |
| Alias | Display name |
| Wallets | Associated blockchain wallets |
| Socials | Social media profiles |
| Language | Preferred language (BCP 47) |
| Role | User role within organization |

**Quick Examples:**
```bash
# Get user by email
GET /api/adminuser/get?user_id=user@example.com

# List users with pagination
GET /api/adminuser/list?filter=<base64_filter>

# Update user profile
PUT /api/adminuser/update

# Update user status
PUT /api/adminuser/update/status
{
  "UserID": "user@example.com",
  "Status": 2,
  "Reason": "Violation of terms"
}
