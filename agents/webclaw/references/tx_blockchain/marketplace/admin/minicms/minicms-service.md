# Admin MiniCMS Service

The Admin MiniCMS Service provides lightweight content management functionality, enabling clients to retrieve, create, and update active content blocks configured for specific pages and organizations. This service is designed for managing marketing banners, announcements, call-to-action blocks, and other dynamic content on marketplace pages.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin MiniCMS Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ GET /get │ GET /list │ POST /create │ PUT /update │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ MiniCMS Store │ Account Store │ Role Store │ Feature Flag │ │
│ │ │ │ │ Store │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Storage Layer │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Content Database (MiniCMS Store) │ │
│ │ • File Storage (Background images) │ │
│ │ • Organization Store (Multi-tenant isolation) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/adminminicms/get | ORGANIZATION_ADMINISTRATOR | Retrieve content by ID |
| GET /api/adminminicms/list | ORGANIZATION_ADMINISTRATOR | List content with pagination |
| POST /api/adminminicms/create | ORGANIZATION_ADMINISTRATOR | Create new content block |
| PUT /api/adminminicms/update | ORGANIZATION_ADMINISTRATOR | Update existing content |

**Note:** All endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Organization ID in `OrganizationID` header (enforces tenant isolation)
- Network in `Network` header (mainnet, testnet, devnet)

## Content Activation Logic

For user-facing endpoints (GET /get, GET /list for non-admin users), content is considered **active** only when ALL of the following criteria are met:

| Criteria | Condition |
|----------|-----------|
| Status | `Status = true` |
| ActiveFrom | Current UTC time is after `ActiveFrom` (if set) |
| ActiveUntil | Current UTC time is before `ActiveUntil` (if set) |

**Important:** Admin endpoints return ALL content regardless of activation status. This allows administrators to preview and manage inactive/draft content.

### Activation Timeline
┌─────────────────────────────────────────────────────────────────────────────┐
│ Content Activation Timeline │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INACTIVE (Draft) ACTIVE INACTIVE (Expired) │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Status=true │ │ Status=true │ │ Status=true │ │
│ │ Now before │ ──────▶ │ Now after │ ──────▶ │ Now after │ │
│ │ ActiveFrom │ │ ActiveFrom │ │ ActiveUntil │ │
│ │ │ │ Now before │ │ │ │
│ │ │ │ ActiveUntil │ │ │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
│ │
│ Admin View: All content visible regardless of activation state │
│ User View: Only content in ACTIVE state is visible │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Data Models

### Content Object

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| ContentID | string | Unique content identifier (UUID) | Yes (for update) |
| BackgroundImage | FileObject | Background image for the content block | No |
| Title | string | Title text | Yes |
| Content | string | Main content body text | Yes |
| CallToAction | string | URL or action reference | No |
| ActiveFrom | Timestamp | Start date/time for activation | No |
| ActiveUntil | Timestamp | End date/time for activation | No |
| Status | boolean | Active status (true=active, false=inactive) | Yes |
| Identifier | string | Logical grouping identifier (e.g., "markets_top_left_block") | Yes |
| Language | LanguageObject | Language specification | Yes |
| OrganizationID | string | Organization UUID (tenant isolation) | Yes |

### FileObject (BackgroundImage)

| Field | Type | Description |
|-------|------|-------------|
| Reference | string | Storage reference path |
| Extension | string | File extension (e.g., "jpg", "png") |
| Name | string | Original filename |

### LanguageObject

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| Language | string | Language code (BCP 47 format) | "en-US", "es-ES", "fr-FR" |

### Metadata Object

| Field | Type | Description |
|-------|------|-------------|
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |

### Audit Object

| Field | Type | Description |
|-------|------|-------------|
| ChangedAt | Timestamp | When the change was made |
| ChangedBy | string | User who made the change |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| Seconds | int64 | Unix timestamp in seconds |
| Nanos | int32 | Nanoseconds offset |

### Network Values

| Network ID | Network Name | Description |
|------------|--------------|-------------|
| 1 | mainnet | Production network |
| 2 | testnet | Testing network |
| 3 | devnet | Development network |

## API Endpoints

### GET /api/adminminicms/get

Retrieves a single piece of content for the requested ContentID.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| OrganizationID | Organization UUID | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| content_id | string | Content ID to retrieve | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/adminminicms/get?content_id=1234-5678" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "Content": {
    "ContentID": "1234-5678",
    "BackgroundImage": {
      "Reference": "cms/images/marketing_banner",
      "Extension": "jpg",
      "Name": "banner"
    },
    "Title": "Welcome to Solotex",
    "Content": "Asset tokenization and trading platform",
    "CallToAction": "https://solotex.com",
    "ActiveFrom": {
      "Seconds": 1741900000
    },
    "ActiveUntil": {
      "Seconds": 1745500000
    },
    "Status": true,
    "Identifier": "markets_top_left_block",
    "Language": {
      "Language": "en-US"
    },
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
  },
  "MetaData": {
    "CreatedAt": {
      "Seconds": 1741890000
    },
    "UpdatedAt": {
      "Seconds": 1741980000
    },
    "Network": 2
  },
  "Audit": {
    "ChangedAt": {
      "Seconds": 1741983951
    }
  }
}
Error Responses
Status Code	Description
200	Success - Content found
400	Bad request - Missing content_id parameter
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Content does not exist
500	Internal server error
GET /api/adminminicms/list
Lists content with pagination support. Results can be filtered by identifier.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Default
identifier	string	Filter by identifier	(no filter)
limit	int	Maximum items per page	20
offset	int	Pagination offset	0
Example Request
bash
# List all content with default pagination
curl -X GET \
  "https://api.admin.sologenic.org/api/adminminicms/list" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"

# Filter by identifier with pagination
curl -X GET \
  "https://api.admin.sologenic.org/api/adminminicms/list?identifier=markets_top_left_block&offset=0&limit=10" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "Content": [
    {
      "ContentID": "1234-5678",
      "BackgroundImage": {
        "Reference": "cms/images/marketing_banner",
        "Extension": "jpg",
        "Name": "banner"
      },
      "Title": "Welcome to Solotex",
      "Content": "Asset tokenization and trading platform",
      "CallToAction": "https://solotex.com",
      "ActiveFrom": {
        "Seconds": 1741900000
      },
      "ActiveUntil": {
        "Seconds": 1745500000
      },
      "Status": true,
      "Identifier": "markets_top_left_block",
      "Language": {
        "Language": "en-US"
      },
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
    },
    {
      "ContentID": "5678-1234",
      "BackgroundImage": {
        "Reference": "cms/images/another_banner",
        "Extension": "jpg",
        "Name": "banner"
      },
      "Title": "Welcome to Solotex",
      "Content": "Asset tokenization and trading platform",
      "CallToAction": "https://solotex.com",
      "ActiveFrom": {
        "Seconds": 1741900000
      },
      "ActiveUntil": {
        "Seconds": 1745500000
      },
      "Status": true,
      "Identifier": "markets_bottom_left_block",
      "Language": {
        "Language": "en-US"
      },
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
    }
  ],
  "MetaData": {
    "CreatedAt": {
      "Seconds": 1741890000
    },
    "UpdatedAt": {
      "Seconds": 1741980000
    },
    "Network": 2
  },
  "Audit": {
    "ChangedAt": {
      "Seconds": 1741983951
    }
  },
  "Offset": 20,
  "Total": 45
}
Error Responses
Status Code	Description
200	Success - Returns array (may be empty)
400	Bad request - Invalid parameters
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
500	Internal server error
POST /api/adminminicms/create
Creates a new content block. The ContentID field must be empty as it will be generated on creation.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
Content.Title	string	Title text	Yes
Content.Content	string	Main content body	Yes
Content.Status	boolean	Active status	Yes
Content.Identifier	string	Logical grouping identifier	Yes
Content.Language.Language	string	Language code (BCP 47)	Yes
Content.OrganizationID	string	Organization UUID	Yes
Content.BackgroundImage	FileObject	Background image metadata	No
Content.CallToAction	string	URL or action reference	No
Content.ActiveFrom	Timestamp	Start date/time	No
Content.ActiveUntil	Timestamp	End date/time	No
Example Request
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/adminminicms/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet" \
  -d '{
    "Content": {
      "BackgroundImage": {
        "Reference": "cms/images/marketing_banner",
        "Extension": "jpg",
        "Name": "banner"
      },
      "Title": "Welcome to Solotex",
      "Content": "Asset tokenization and trading platform",
      "CallToAction": "https://solotex.com",
      "ActiveFrom": {
        "Seconds": 1741900000
      },
      "ActiveUntil": {
        "Seconds": 1745500000
      },
      "Status": true,
      "Identifier": "markets_top_left_block",
      "Language": {
        "Language": "en-US"
      },
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
    }
  }'
Example Response
json
{
  "ContentID": "1234-5678"
}
Error Responses
Status Code	Description
200	Success - Content created
400	Bad request - Missing required fields or invalid data
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
409	Conflict - Content with same identifier and language already exists
500	Internal server error
PUT /api/adminminicms/update
Updates an existing content block. The ContentID field must be set to the ID of the content to be updated.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
Content.ContentID	string	ID of content to update	Yes
Content.Title	string	Updated title	No
Content.Content	string	Updated content body	No
Content.Status	boolean	Updated status	No
Content.Identifier	string	Updated identifier	No
Content.Language.Language	string	Updated language	No
Content.BackgroundImage	FileObject	Updated background image	No
Content.CallToAction	string	Updated URL/action	No
Content.ActiveFrom	Timestamp	Updated start date	No
Content.ActiveUntil	Timestamp	Updated end date	No
Audit.Reason	string	Reason for update	No
Example Request
bash
curl -X PUT \
  "https://api.admin.sologenic.org/api/adminminicms/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet" \
  -d '{
    "Content": {
      "ContentID": "1234-5678",
      "Title": "Welcome to Solotex - Updated",
      "Content": "Asset tokenization and trading platform - Now with NFT support",
      "CallToAction": "https://solotex.com/new",
      "Status": true,
      "Identifier": "markets_top_left_block",
      "Language": {
        "Language": "en-US"
      },
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
    },
    "Audit": {
      "Reason": "Updated marketing content for Q2 campaign"
    }
  }'
Example Response
json
{
  "ContentID": "1234-5678",
  "Success": true
}
Error Responses
Status Code	Description
200	Success - Content updated
400	Bad request - Missing ContentID or invalid data
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Content does not exist
409	Conflict - Version mismatch or concurrent update
500	Internal server error
Content Identifier Examples
Identifiers are used to logically group content blocks for specific page locations.

Page Area	Identifier Example	Description
Markets Page - Top Left	markets_top_left_block	Top left promotional block
Markets Page - Top Right	markets_top_right_block	Top right promotional block
Markets Page - Bottom Left	markets_bottom_left_block	Bottom left promotional block
Homepage - Hero Banner	homepage_hero_banner	Main hero banner
Homepage - Announcement	homepage_announcement_bar	Top announcement bar
Trading Page - Sidebar	trading_sidebar_promo	Sidebar promotion
Asset Page - Header	asset_page_header_banner	Asset page header
Footer - Links	footer_links_section	Footer links section
Multi-language Support
The service supports content in multiple languages using BCP 47 language codes.

Language Code Examples
Language Code	Language	Region
en-US	English	United States
en-GB	English	United Kingdom
es-ES	Spanish	Spain
es-MX	Spanish	Mexico
fr-FR	French	France
de-DE	German	Germany
ja-JP	Japanese	Japan
zh-CN	Chinese	China (Simplified)
zh-TW	Chinese	Taiwan (Traditional)
ko-KR	Korean	South Korea
Multi-language Content Example
For a single identifier, you might have multiple content entries:

json
// English version
{
  "Identifier": "markets_top_left_block",
  "Language": { "Language": "en-US" },
  "Title": "Welcome to Solotex",
  "Content": "Asset tokenization and trading platform"
}

// Spanish version
{
  "Identifier": "markets_top_left_block",
  "Language": { "Language": "es-ES" },
  "Title": "Bienvenido a Solotex",
  "Content": "Plataforma de tokenización e intercambio de activos"
}
Content Scheduling Examples
Immediate Activation (No end date)
json
{
  "Status": true,
  "ActiveFrom": null,
  "ActiveUntil": null
}
Scheduled Future Activation
json
{
  "Status": true,
  "ActiveFrom": { "Seconds": 1741900000 },  // March 13, 2025
  "ActiveUntil": { "Seconds": 1745500000 }   // April 24, 2025
}
Draft Content (Not yet active)
json
{
  "Status": false,  // Inactive regardless of dates
  "ActiveFrom": { "Seconds": 1741900000 },
  "ActiveUntil": { "Seconds": 1745500000 }
}
Expired Content (Admin can still view)
json
{
  "Status": true,
  "ActiveFrom": { "Seconds": 1700000000 },  // Past
  "ActiveUntil": { "Seconds": 1730000000 }  // Past (expired)
}
Tenant Isolation
The OrganizationID header is a mandatory parameter that enforces proper organizational data boundaries, ensuring each tenant can only access records within their designated scope.

text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Tenant Isolation                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Organization A (ID: org-a-123)    Organization B (ID: org-b-456)          │
│  ┌─────────────────────────┐       ┌─────────────────────────┐            │
│  │ Content Block 1          │       │ Content Block A         │            │
│  │ Content Block 2          │       │ Content Block B         │            │
│  │ Content Block 3          │       │ Content Block C         │            │
│  └─────────────────────────┘       └─────────────────────────┘            │
│                                                                             │
│  Admin from Org A can only see Org A content                               │
│  Admin from Org B can only see Org B content                               │
│                                                                             │
│  Platform administrators can see all content (cross-tenant)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
MINICMS_STORE	MiniCMS service endpoint	github.com/sologenic/com-be-minicms-store/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
ACCOUNT_STORE	Admin account service endpoint	github.com/sologenic/com-be-admin-account-store/
ROLE_STORE	Admin role service endpoint	github.com/sologenic/com-be-role-store/
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-be-feature-flag-store/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-store/
FILE_STORE	File store endpoint	github.com/sologenic/com-fs-file-model
CERTIFICATE_STORE	Certificate store endpoint (multi-tenant support)	-
CREDENTIALS_LOCATION	Service account credentials file (JSON)	-
PROJECT_ID	Google Cloud project ID	-
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
  "message": "Missing required field: Title",
  "details": "Content.Title is required"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Content not found",
  "details": "No content found with ID: 1234-5678"
}
Conflict (409)
json
{
  "error": "Conflict",
  "message": "Content already exists",
  "details": "Content with Identifier 'markets_top_left_block' and Language 'en-US' already exists"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Content not visible to users	Status=false or outside ActiveFrom/Until	Check activation criteria
Wrong content returned	Incorrect language code	Verify BCP 47 language format
Organization isolation violation	Wrong OrganizationID header	Use correct OrganizationID
Content not found	Wrong ContentID	Verify ContentID exists
Duplicate content error	Same Identifier + Language pair	Use unique combination or update existing
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check content activation status:

bash
# Get content (admin sees all)
curl -X GET /api/adminminicms/get?content_id=1234-5678 \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: mainnet"
List all content for an organization:

bash
curl -X GET /api/adminminicms/list \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: mainnet"
Best Practices
Content Management
Use Descriptive Identifiers: Name identifiers clearly (e.g., homepage_hero_banner not block1)

Schedule Content in Advance: Set ActiveFrom and ActiveUntil for time-sensitive campaigns

Preview Before Activation: Use admin endpoints to preview content before it goes live

Version Control: Keep audit reasons for significant changes

Multi-language
Always Provide Default Language: Ensure content exists in at least one language

Use BCP 47 Codes: Follow standard language codes for consistency

Fallback Strategy: Implement language fallback in UI (e.g., en-US → en → default)

Performance
Paginate Large Lists: Use limit and offset for efficient data retrieval

Cache Active Content: Implement caching for frequently accessed content

Optimize Images: Compress background images before uploading

Related Services
Service	Description
Admin Account Service	User and role management
Admin File Service	Background image storage
Organization Service	Multi-tenant organization management
Feature Flag Service	Feature toggles for content visibility
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the MiniCMS Service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the Admin MiniCMS Service section under Admin Services:

markdown
### Admin MiniCMS Service

The Admin MiniCMS Service provides lightweight content management functionality for managing marketing banners, announcements, and dynamic content blocks across marketplace pages.

📖 **[Admin MiniCMS Service Documentation](./admin/minicms/minicms-service.md)**

**Key Features:**
- Create, update, and retrieve content blocks
- Time-based content scheduling (ActiveFrom/ActiveUntil)
- Multi-language support (BCP 47 language codes)
- Tenant isolation via OrganizationID
- Status-based activation logic
- Pagination support for content lists

**Content Activation Criteria (User-Facing):**
| Criteria | Requirement |
|----------|-------------|
| Status | Must be `true` |
| ActiveFrom | Current time after ActiveFrom (if set) |
| ActiveUntil | Current time before ActiveUntil (if set) |

**Content Fields:**
| Field | Description |
|-------|-------------|
| Title | Content title/heading |
| Content | Main content body |
| BackgroundImage | Optional background image |
| CallToAction | URL or action reference |
| Identifier | Logical grouping (e.g., "markets_top_left_block") |
| Language | BCP 47 language code |

**Quick Examples:**
```bash
# Get content by ID
GET /api/adminminicms/get?content_id=<uuid>

# List content with pagination
GET /api/adminminicms/list?offset=0&limit=20

# Create content block
POST /api/adminminicms/create

# Update content block
PUT /api/adminminicms/update
Required Role: ORGANIZATION_ADMINISTRATOR
