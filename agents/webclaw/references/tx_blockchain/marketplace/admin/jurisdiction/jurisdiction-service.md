# Admin Jurisdiction Service

The Admin Jurisdiction Service provides RESTful interfaces for managing legal and regulatory jurisdictions within the marketplace platform. Jurisdictions define the geographic and regulatory framework under which assets can be traded and users can operate.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin Jurisdiction Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ GET /get │ GET /list │ POST /create │ PUT /update │ │
│ │ │ │ │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Jurisdiction │ Account Store │ Asset Store │ Organization Store│ │
│ │ Store │ │ │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Systems │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • KYC Service (jurisdiction verification) │ │
│ │ • Asset Service (jurisdiction-based restrictions) │ │
│ │ • User Service (user jurisdiction assignments) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/jurisdiction/get | ORGANIZATION_ADMINISTRATOR | Get jurisdiction by ID |
| GET /api/jurisdiction/list | ORGANIZATION_ADMINISTRATOR | List all jurisdictions |
| POST /api/jurisdiction/create | ORGANIZATION_ADMINISTRATOR | Create new jurisdiction |
| PUT /api/jurisdiction/update | ORGANIZATION_ADMINISTRATOR | Update existing jurisdiction |
| PUT /api/jurisdiction/update/status | ORGANIZATION_ADMINISTRATOR | Update jurisdiction status |

**Note:** All admin endpoints are protected by role-based access control and default to the `ORGANIZATION_ADMINISTRATOR` role. Permissions are managed dynamically by Organization administrators on the fly.

## Data Models

### Jurisdiction Object

| Field | Type | Description | Immutable |
|-------|------|-------------|-----------|
| ID | string | Unique jurisdiction identifier (UUID) | ✅ Yes |
| OrganizationID | string | Organization UUID | ✅ Yes |
| Name | string | Display name of the jurisdiction | ❌ No |
| Description | string | Detailed description | ❌ No |
| ExternalID | string | External reference identifier | ✅ Yes |
| Status | int | Jurisdiction status (1, 2) | ❌ No (via /status endpoint) |
| Country | Country | Country information | ✅ Yes |
| Subdivision | Subdivision | Optional subdivision (state/province) | ✅ Yes |
| Regulators | []int | Array of regulatory body IDs | ❌ No |
| EffectiveFrom | timestamp | Date when jurisdiction becomes effective | ❌ No |
| EffectiveTo | timestamp | Date when jurisdiction expires | ❌ No |

### Country Object

| Field | Type | Description | Standard |
|-------|------|-------------|----------|
| Name | string | Full country name | - |
| Code | string | ISO 3166-1 alpha-3 country code | ISO 3166-1 |

### Subdivision Object

| Field | Type | Description | Standard |
|-------|------|-------------|----------|
| Name | string | Subdivision name (state/province) | - |
| Code | string | ISO 3166-2 subdivision code | ISO 3166-2 |

### Regulator Values

| Regulator ID | Regulator Name | Description |
|--------------|----------------|-------------|
| 1 | SEC | U.S. Securities and Exchange Commission |
| 2 | FINRA | Financial Industry Regulatory Authority |
| 3 | FCA | UK Financial Conduct Authority |
| 4 | ESMA | European Securities and Markets Authority |
| 5 | BaFin | German Federal Financial Supervisory Authority |
| 6 | AMF | French Financial Markets Authority |
| 7 | JFSA | Japan Financial Services Agency |
| 8 | ASIC | Australian Securities and Investments Commission |
| 9 | OSC | Ontario Securities Commission |
| 10 | CSA | Canadian Securities Administrators |

### Jurisdiction Status Values

| Status ID | Status Name | Description |
|-----------|-------------|-------------|
| 1 | INACTIVE | Jurisdiction is not currently active |
| 2 | ACTIVE | Jurisdiction is active and enforceable |

### Metadata Object

| Field | Type | Description |
|-------|------|-------------|
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |
| CreatedAt | timestamp | Creation timestamp |
| UpdatedAt | timestamp | Last update timestamp |

### Audit Object

| Field | Type | Description |
|-------|------|-------------|
| ChangedBy | string | User who made the change |
| ChangedAt | timestamp | When the change was made |
| Reason | string | Reason for the change |

## API Endpoints

### GET /api/jurisdiction/get

Returns a jurisdiction by its ID.

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| id | string | Jurisdiction UUID | Yes |

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/jurisdiction/get?id=8878d73b-edff-40a1-b6ce-43a4508aa96a" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
{
  "Jurisdiction": {
    "ID": "8878d73b-edff-40a1-b6ce-43a4508aa96a",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Name": "United States",
    "Description": "Federal jurisdiction of the United States of America",
    "ExternalID": "US-001",
    "Status": 2,
    "Country": {
      "Name": "United States",
      "Code": "USA"
    },
    "Regulators": [1, 2],
    "EffectiveFrom": {
      "seconds": 1672531200
    },
    "EffectiveTo": {
      "seconds": 1767225599
    }
  },
  "MetaData": {
    "Network": 2,
    "UpdatedAt": {
      "seconds": 1740516877,
      "nanos": 216014000
    },
    "CreatedAt": {
      "seconds": 1740511148,
      "nanos": 85177000
    }
  },
  "Audit": {
    "ChangedBy": "sg.org.testnet@gmail.com",
    "ChangedAt": {
      "seconds": 1740516877,
      "nanos": 216015000
    },
    "Reason": "Jurisdiction no longer supported"
  }
}
Error Responses
Status Code	Description
200	Success - Jurisdiction found
400	Bad request - Missing ID parameter
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Jurisdiction does not exist
GET /api/jurisdiction/list
Returns a list of all jurisdictions with optional filtering.

Query Parameters
Parameter	Type	Description	Required
filter	string	Base64 encoded JSON filter string	No
Filter Object
json
{
  "OrganizationID": "string",
  "Status": "int",
  "CountryCode": "string",
  "Regulator": "int",
  "Offset": "int",
  "Limit": "int"
}
Field	Type	Description	Default
OrganizationID	string	Filter by organization	-
Status	int	Filter by status (1, 2)	-
CountryCode	string	Filter by ISO country code	-
Regulator	int	Filter by regulator ID	-
Offset	int	Pagination offset	0
Limit	int	Items per page	20
Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/jurisdiction/list" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
[
  {
    "Jurisdiction": {
      "ID": "08af6b9f-9a9e-4689-8adb-5b4fe70fcddd",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "Canada-British Columbia",
      "Description": "Provincial jurisdiction of British Columbia, Canada",
      "ExternalID": "CA-BC-001",
      "Status": 1,
      "Country": {
        "Name": "Canada",
        "Code": "CAN"
      },
      "Subdivision": {
        "Name": "British Columbia",
        "Code": "CA-BC"
      },
      "Regulators": [1, 2],
      "EffectiveFrom": {
        "seconds": 1672531200
      },
      "EffectiveTo": {
        "seconds": 1767225599
      }
    },
    "MetaData": {
      "Network": 2,
      "UpdatedAt": {
        "seconds": 1740518732,
        "nanos": 171974000
      },
      "CreatedAt": {
        "seconds": 1740518732,
        "nanos": 171972000
      }
    },
    "Audit": {
      "ChangedBy": "sg.org.testnet@gmail.com",
      "ChangedAt": {
        "seconds": 1740518732,
        "nanos": 171974000
      }
    }
  },
  {
    "Jurisdiction": {
      "ID": "8878d73b-edff-40a1-b6ce-43a4508aa96a",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "United States",
      "Description": "Federal jurisdiction of the United States of America",
      "ExternalID": "US-001",
      "Status": 2,
      "Country": {
        "Name": "United States",
        "Code": "USA"
      },
      "Regulators": [1, 2],
      "EffectiveFrom": {
        "seconds": 1672531200
      },
      "EffectiveTo": {
        "seconds": 1767225599
      }
    },
    "MetaData": {
      "Network": 2,
      "UpdatedAt": {
        "seconds": 1740518012,
        "nanos": 266394000
      },
      "CreatedAt": {
        "seconds": 1740511148,
        "nanos": 85177000
      }
    },
    "Audit": {
      "ChangedBy": "sg.org.testnet@gmail.com",
      "ChangedAt": {
        "seconds": 1740518012,
        "nanos": 266395000
      },
      "Reason": "Update test"
    }
  }
]
POST /api/jurisdiction/create
Creates a new jurisdiction.

Important Notes
The Country.Code must follow ISO 3166-1 alpha-3 standard (e.g., USA for United States, CAN for Canada)

The Subdivision.Code must follow ISO 3166-2 standard (e.g., US-TX for Texas, CA-BC for British Columbia)

If Subdivision is omitted, the jurisdiction is considered country-wide

Request Body
Field	Type	Description	Required
Jurisdiction.OrganizationID	string	Organization UUID	Yes
Jurisdiction.Name	string	Display name	Yes
Jurisdiction.Description	string	Detailed description	No
Jurisdiction.ExternalID	string	External reference ID	No
Jurisdiction.Status	int	Initial status (1=INACTIVE, 2=ACTIVE)	Yes
Jurisdiction.Country.Name	string	Full country name	Yes
Jurisdiction.Country.Code	string	ISO 3166-1 alpha-3 country code	Yes
Jurisdiction.Subdivision.Name	string	Subdivision name	No
Jurisdiction.Subdivision.Code	string	ISO 3166-2 subdivision code	No
Jurisdiction.Regulators	[]int	Array of regulator IDs	No
Jurisdiction.EffectiveFrom	string	ISO 8601 timestamp	No
Jurisdiction.EffectiveTo	string	ISO 8601 timestamp	No
Example Request
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/jurisdiction/create" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "Jurisdiction": {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "Canada-British Columbia",
      "Description": "Provincial jurisdiction of British Columbia, Canada",
      "ExternalID": "CA-BC-001",
      "Status": 1,
      "Country": {
        "Name": "Canada",
        "Code": "CAN"
      },
      "Subdivision": {
        "Name": "British Columbia",
        "Code": "CA-BC"
      },
      "Regulators": [1, 2],
      "EffectiveFrom": "2023-01-01T00:00:00Z",
      "EffectiveTo": "2025-12-31T23:59:59Z"
    }
  }'
Example Response
json
{
  "ID": "08af6b9f-9a9e-4689-8adb-5b4fe70fcddd"
}
Error Responses
Status Code	Description
400	Bad request - Invalid ISO code or missing required fields
401	Unauthorized
403	Forbidden
409	Conflict - Jurisdiction already exists
500	Internal server error
PUT /api/jurisdiction/update
Updates an existing jurisdiction.

Important Notes
The following fields are immutable and will not be updated:

CreatedAt

Network

ID

OrganizationID

ExternalID

Country

Subdivision

Status can only be updated through the /api/jurisdiction/update/status endpoint.

Request Body
Field	Type	Description	Required
Jurisdiction.ID	string	Jurisdiction UUID	Yes
Jurisdiction.OrganizationID	string	Organization UUID	Yes
Jurisdiction.Name	string	Updated name	No
Jurisdiction.Description	string	Updated description	No
Jurisdiction.Regulators	[]int	Updated regulator IDs	No
Jurisdiction.EffectiveFrom	string	Updated effective from date	No
Jurisdiction.EffectiveTo	string	Updated effective to date	No
Audit.Reason	string	Reason for update	No
Example Request
bash
curl -X PUT \
  "https://api.admin.sologenic.org/api/jurisdiction/update" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "Jurisdiction": {
      "ID": "8878d73b-edff-40a1-b6ce-43a4508aa96a",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "United States",
      "Description": "Federal jurisdiction of the United States of America",
      "ExternalID": "US-001",
      "Country": {
        "Name": "United States",
        "Code": "USA"
      },
      "Regulators": [1, 2],
      "EffectiveFrom": "2023-01-01T00:00:00Z",
      "EffectiveTo": "2025-12-31T23:59:59Z"
    },
    "Audit": {
      "Reason": "Update test"
    }
  }'
Example Response
json
{
  "ID": "8878d73b-edff-40a1-b6ce-43a4508aa96a"
}
Error Responses
Status Code	Description
400	Bad request - Attempting to modify immutable field
401	Unauthorized
403	Forbidden
404	Not found - Jurisdiction does not exist
409	Conflict - Cannot update active jurisdiction
PUT /api/jurisdiction/update/status
Updates the status of an existing jurisdiction.

Query Parameters
Parameter	Type	Description	Required
id	string	Jurisdiction UUID	Yes
status	int	New status (1=INACTIVE, 2=ACTIVE)	Yes
reason	string	Reason for status change	No
Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
curl -X PUT \
  'https://api.admin.sologenic.org/api/jurisdiction/update/status?id=8878d73b-edff-40a1-b6ce-43a4508aa96a&status=2&reason=Jurisdiction%20no%20longer%20supported' \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer <token>"
Example Response
json
{
  "ID": "8878d73b-edff-40a1-b6ce-43a4508aa96a"
}
Error Responses
Status Code	Description
400	Bad request - Invalid status value
401	Unauthorized
403	Forbidden
404	Not found - Jurisdiction does not exist
ISO Standards Reference
ISO 3166-1 alpha-3 Country Codes (Examples)
Country	Alpha-2	Alpha-3	Numeric
United States	US	USA	840
Canada	CA	CAN	124
United Kingdom	GB	GBR	826
Germany	DE	DEU	276
France	FR	FRA	250
Japan	JP	JPN	392
Australia	AU	AUS	036
Singapore	SG	SGP	702
Switzerland	CH	CHE	756
China	CN	CHN	156
ISO 3166-2 Subdivision Codes (Examples)
Country	Subdivision	Code
United States	Texas	US-TX
United States	California	US-CA
United States	New York	US-NY
Canada	British Columbia	CA-BC
Canada	Ontario	CA-ON
Canada	Quebec	CA-QC
United Kingdom	England	GB-ENG
United Kingdom	Scotland	GB-SCT
Germany	Bavaria	DE-BY
Germany	Berlin	DE-BE
Jurisdiction Hierarchy
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Jurisdiction Hierarchy                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Global/Supranational                             │   │
│  │  • European Union (EU)                                              │   │
│  │  • International (Global)                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Federal/National                              │   │
│  │  • United States (USA)                                              │   │
│  │  • Canada (CAN)                                                     │   │
│  │  • Germany (DEU)                                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    State/Provincial (Subdivision)                    │   │
│  │  • Texas (US-TX)                                                    │   │
│  │  • British Columbia (CA-BC)                                         │   │
│  │  • Bavaria (DE-BY)                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         Local/Municipal                              │   │
│  │  • City-specific regulations (optional extension)                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Base64 Filter Examples
Example 1: Filter by Status
json
{
  "Status": 2,
  "Limit": 50,
  "Offset": 0
}
Base64 encoded:

text
eyJTdGF0dXMiOjIsIkxpbWl0Ijo1MCwiT2Zmc2V0IjowfQ==
Example 2: Filter by Country Code
json
{
  "CountryCode": "USA",
  "Status": 2,
  "Limit": 20
}
Base64 encoded:

text
eyJDb3VudHJ5Q29kZSI6IlVTQSIsIlN0YXR1cyI6MiwiTGltaXQiOjIwfQ==
Example 3: Filter by Regulator
json
{
  "Regulator": 1,
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Limit": 100
}
Base64 encoded:

text
eyJSZWd1bGF0b3IiOjEsIk9yZ2FuaXphdGlvbklEIjoiNzJjNGMwNzItMmZlNC00ZjcyLWFlOWQtZDlkNTJhMDVmZDcxIiwiTGltaXQiOjEwMH0=
Jurisdiction Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Jurisdiction Lifecycle                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐                                                              │
│  │ Created  │                                                              │
│  │ (Draft)  │                                                              │
│  └────┬─────┘                                                              │
│       │                                                                     │
│       │ POST /create                                                        │
│       │ Status: INACTIVE (1)                                               │
│       ▼                                                                     │
│  ┌──────────┐                                                              │
│  │ INACTIVE │◄──────────────────────────────────────────────────────┐     │
│  └────┬─────┘                                                       │     │
│       │                                                             │     │
│       │ PUT /update/status (status=2)                               │     │
│       ▼                                                             │     │
│  ┌──────────┐                                                      │     │
│  │ ACTIVE   │──────────────────────────────────────────────────────┘     │
│  └────┬─────┘                                                            │
│       │                                                                   │
│       │ PUT /update/status (status=1)                                     │
│       │ or EffectiveTo reached                                           │
│       ▼                                                                   │
│  ┌──────────┐                                                            │
│  │ EXPIRED  │                                                            │
│  │ (Archived)│                                                           │
│  └──────────┘                                                            │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
Jurisdiction Examples
Country-Wide Jurisdiction
json
{
  "Name": "United States",
  "Country": {
    "Name": "United States",
    "Code": "USA"
  },
  "Subdivision": null,
  "Regulators": [1, 2]
}
Subdivision Jurisdiction
json
{
  "Name": "Canada-British Columbia",
  "Country": {
    "Name": "Canada",
    "Code": "CAN"
  },
  "Subdivision": {
    "Name": "British Columbia",
    "Code": "CA-BC"
  },
  "Regulators": [9, 10]
}
Multi-Regulator Jurisdiction
json
{
  "Name": "European Union",
  "Country": {
    "Name": "European Union",
    "Code": "EUU"
  },
  "Regulators": [3, 4]
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service/
ACCOUNT_STORE	Account store endpoint	github.com/sologenic/com-be-admin-account-store/
ASSET_STORE	Asset store endpoint	github.com/sologenic/com-be-asset-store/
JURISDICTION_STORE	Jurisdiction store endpoint	github.com/sologenic/com-be-jurisdiction-store/
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/fs-feature-flag-model/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-store/
ROLE_STORE	Role service endpoint	github.com/sologenic/com-fs-admin-role-model/
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
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid ISO country code",
  "details": "Country code 'XX' does not conform to ISO 3166-1 alpha-3 standard"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Jurisdiction not found",
  "details": "No jurisdiction found with ID: 8878d73b-edff-40a1-b6ce-43a4508aa96a"
}
Conflict (409)
json
{
  "error": "Conflict",
  "message": "Jurisdiction already exists",
  "details": "A jurisdiction with Country Code 'USA' and Subdivision Code 'US-TX' already exists"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Invalid country code	Wrong ISO standard	Use ISO 3166-1 alpha-3 (3 letters)
Invalid subdivision code	Wrong format	Use ISO 3166-2 (e.g., US-TX)
Cannot update jurisdiction	Field is immutable	Check immutable fields list
Status change rejected	Invalid transition	Use /update/status endpoint only
Duplicate jurisdiction	Already exists	Check for existing jurisdiction first
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check jurisdiction existence:

bash
# List all jurisdictions
curl -X GET /api/jurisdiction/list \
  -H "Network: testnet" \
  -H "Authorization: Bearer <token>"
Best Practices
Jurisdiction Creation
Use Standard Codes: Always use ISO 3166-1 alpha-3 for countries

Include Subdivisions: For state/province level regulations, include subdivision

Set Effective Dates: Define when jurisdiction becomes active/expires

Document Regulators: Specify which regulatory bodies apply

Jurisdiction Management
Status Transitions: Only use /update/status for status changes

Audit Trail: Always provide reasons for updates and status changes

Immutable Fields: Plan ahead for fields that cannot be changed

Effective Periods: Set reasonable effective from/to dates

Compliance
KYC Integration: Ensure jurisdiction aligns with KYC verification

Asset Restrictions: Map jurisdictions to asset availability

Regulatory Updates: Keep regulator assignments current

Expiration Management: Monitor and update expiring jurisdictions

Related Services
Service	Description
Admin Account Service	User and role management
Admin Asset Service	Asset management with jurisdiction restrictions
KYC Service	User jurisdiction verification
Jurisdiction Asset Management Service	Whitelist management
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the jurisdiction service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the jurisdiction service section:

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

### Admin Jurisdiction Service

The Admin Jurisdiction Service provides RESTful interfaces for managing legal and regulatory jurisdictions within the marketplace platform.

📖 **[Admin Jurisdiction Service Documentation](./admin/jurisdiction/jurisdiction-service.md)**

**Key Features:**
- Create, update, and list jurisdictions
- Status management (ACTIVE/INACTIVE)
- ISO 3166-1 alpha-3 country codes
- ISO 3166-2 subdivision codes (states/provinces)
- Regulator assignment
- Effective date ranges

**Jurisdiction Statuses:**
| Status | Description |
|--------|-------------|
| INACTIVE (1) | Not currently active |
| ACTIVE (2) | Active and enforceable |

**Immutable Fields:**
- ID, OrganizationID, ExternalID
- Country, Subdivision
- CreatedAt, Network

**Quick Examples:**
```bash
# Get jurisdiction
GET /api/jurisdiction/get?id=<uuid>

# List jurisdictions
GET /api/jurisdiction/list

# Create jurisdiction
POST /api/jurisdiction/create

# Update status
PUT /api/jurisdiction/update/status?id=<uuid>&status=2
Account Types:

Sologenic Administrator (Platform level)

Organization Administrator (Organization level)

KYC Administrator

Broker Asset Administrator

Normal User (End User)

