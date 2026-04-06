# Organization Service

The Organization Service provides RESTful interfaces for managing organizations within the marketplace platform. Organizations represent tenant entities that have their own users, assets, jurisdictions, and configurations. The service supports both organization-level administration and platform-level (Sologenic) administration.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Organization Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ GET /get │ PUT /update │ GET /list │ POST /create │ │
│ │ (Own org) │ (Own org) │ (All orgs) │ (New org) │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Organization │ Account Store │ Role Store │ Feature Flag │ │
│ │ Store │ │ │ Store │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Systems │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Coreum Blockchain (Compliance Manager Contract) │ │
│ │ • Authentication Service (Firebase) │ │
│ │ • Admin Account Service │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role-Based Access Control

| Role | Permissions | Endpoints |
|------|-------------|-----------|
| **Organization Administrator** | View and update their own organization | GET /get, PUT /update |
| **Sologenic Administrator** | View all organizations, create new organizations | GET /list, POST /create |

## Data Models

### Organization Object

| Field | Type | Description | Immutable |
|-------|------|-------------|-----------|
| OrganizationID | string | Unique organization identifier (UUID) | ✅ Yes (auto-generated) |
| Name | string | Organization display name | ❌ No |
| Description | string | Organization description | ❌ No |
| Logo | string | URL to organization logo | ❌ No |
| URL | string | Organization website URL | ❌ No |
| AdminEmail | string | Administrator email (create only) | ✅ Yes (set on create) |
| CreatedAt | Timestamp | Creation timestamp | ✅ Yes |
| UpdatedAt | Timestamp | Last update timestamp | Auto-updated |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset (optional) |

## API Endpoints

### GET /api/organization/get

Retrieves the Organization information for the organization to which the caller belongs.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/organization/get" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet"
Example Response
json
{
  "OrganizationID": "96b5e611-4bc7-4967-b5f9-7aee68aea158",
  "Name": "atg-org2",
  "Description": "atg test org2",
  "Logo": "https://example.com/logo.png",
  "URL": "https://example.com",
  "CreatedAt": {
    "seconds": 1722367552
  },
  "UpdatedAt": {
    "seconds": 1722369970
  }
}
Error Responses
Status Code	Description
200	Success - Organization found
401	Unauthorized - Invalid or missing token
403	Forbidden - User not associated with any organization
404	Not found - Organization does not exist
500	Internal server error
PUT /api/organization/update
Updates the Organization information for the organization to which the caller belongs.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
OrganizationID	string	Organization UUID (must match caller's org)	Yes
Name	string	Updated organization name	No
Description	string	Updated description	No
Logo	string	Updated logo URL	No
URL	string	Updated website URL	No
Example Request
bash
curl -X PUT \
  "https://api.admin.sologenic.org/api/organization/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet" \
  -d '{
    "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca",
    "Name": "com-atg",
    "Description": "atg test org",
    "Logo": "https://example.com/new-logo.png",
    "URL": "https://example.com"
  }'
Example Response
json
{
  "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca"
}
Error Responses
Status Code	Description
200	Success - Organization updated
400	Bad request - Invalid OrganizationID or missing fields
401	Unauthorized - Invalid or missing token
403	Forbidden - Cannot update organization you don't belong to
404	Not found - Organization does not exist
500	Internal server error
GET /api/organization/list
Retrieves a list of all organizations. This endpoint is only available to Sologenic administrators.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Default
offset	int	Pagination offset	0
limit	int	Maximum items per page	20
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/organization/list?offset=0&limit=10" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet"
Example Response
json
{
  "Organizations": [
    {
      "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca",
      "Name": "com-atg-org 1",
      "Description": "atg-test org1",
      "Logo": "https://example1.com/logo.png",
      "URL": "https://example1.com",
      "CreatedAt": {
        "seconds": 1722035004
      },
      "UpdatedAt": {
        "seconds": 1722622853
      }
    },
    {
      "OrganizationID": "783174ea-d891-4c0c-9c69-c733850ea391",
      "Name": "New ORG 2",
      "Description": "Test Register",
      "Logo": "https://example2.com/logo.png",
      "URL": "https://example2.com",
      "CreatedAt": {
        "seconds": 1722635122
      },
      "UpdatedAt": {
        "seconds": 1722635122
      }
    }
  ],
  "Offset": 0
}
Error Responses
Status Code	Description
200	Success - Returns array (may be empty)
401	Unauthorized - Invalid or missing token
403	Forbidden - Requires Sologenic Administrator role
500	Internal server error
POST /api/organization/create
Creates a new organization. This endpoint is only available to Sologenic administrators. The OrganizationID is generated automatically.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
Name	string	Organization display name	Yes
Description	string	Organization description	No
Logo	string	Organization logo URL	No
URL	string	Organization website URL	No
AdminEmail	string	Administrator email address	Yes
Example Request
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/organization/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet" \
  -d '{
    "Name": "New ORG 2",
    "Description": "Test Create",
    "Logo": "https://example.com/logo.png",
    "URL": "https://example.com",
    "AdminEmail": "admin@example.com"
  }'
Example Response
json
{
  "OrganizationID": "783174ea-d891-4c0c-9c69-c733850ea391"
}
Error Responses
Status Code	Description
200	Success - Organization created
400	Bad request - Missing required fields (Name, AdminEmail)
401	Unauthorized - Invalid or missing token
403	Forbidden - Requires Sologenic Administrator role
409	Conflict - Organization name already exists
500	Internal server error
Organization Hierarchy
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Organization Hierarchy                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Sologenic (Platform)                              │   │
│  │  • Platform-level administration                                     │   │
│  │  • System-wide configuration                                         │   │
│  │  • Sologenic Administrator role                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    ┌───────────────┼───────────────┐                       │
│                    │               │               │                       │
│                    ▼               ▼               ▼                       │
│  ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐   │
│  │ Organization A      │ │ Organization B      │ │ Organization C      │   │
│  │ • Org Admin         │ │ • Org Admin         │ │ • Org Admin         │   │
│  │ • Own assets        │ │ • Own assets        │ │ • Own assets        │   │
│  │ • Own jurisdictions │ │ • Own jurisdictions │ │ • Own jurisdictions │   │
│  │ • Own users         │ │ • Own users         │ │ • Own users         │   │
│  └─────────────────────┘ └─────────────────────┘ └─────────────────────┘   │
│                                                                             │
│  Each organization is isolated - users, assets, and jurisdictions are      │
│  scoped to their owning organization.                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Tenant Isolation
The Organization Service is the foundation for multi-tenancy across all marketplace services:

Service	Isolation Mechanism
Admin Asset Service	OrganizationID header filters assets
Admin Jurisdiction Service	OrganizationID header filters jurisdictions
Admin Comment Service	OrganizationID header isolates comments
Admin Document Service	OrganizationID header filters documents
Admin Certificate Service	OrganizationID header isolates certificates
Admin Feature Flag Service	OrganizationID scopes feature flags
Admin Notification Service	OrganizationID scopes notifications
Admin MiniCMS Service	OrganizationID isolates content blocks
Organization Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Organization Lifecycle                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐                                                          │
│  │ Organization │                                                          │
│  │ Created      │                                                          │
│  │ (POST /create)                                                          │
│  └──────┬───────┘                                                          │
│         │                                                                   │
│         │ AdminEmail user assigned Organization Administrator role         │
│         ▼                                                                   │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│  │ Active       │────▶│ Configure    │────▶│ Operational  │               │
│  │ (Created)    │     │ Assets/      │     │ (Active)     │               │
│  │              │     │ Jurisdictions│     │              │               │
│  └──────────────┘     └──────────────┘     └──────┬───────┘               │
│                                                    │                        │
│                                                    │ (Future: Soft Delete) │
│                                                    ▼                        │
│                                          ┌──────────────┐                  │
│                                          │ Archived     │                  │
│                                          │ (Inactive)   │                  │
│                                          └──────────────┘                  │
│                                                                             │
│  Note: Organizations are not typically deleted; they may be archived.      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-model/
ACCOUNT_STORE	Account service endpoint	github.com/sologenic/com-fs-admin-account-model/
ROLE_STORE	Role service endpoint	github.com/sologenic/com-fs-admin-role-model/
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-admin-feature-flag-model/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-admin-organization-model/
Optional Environment Variables
Environment Variable	Description
GRPC_APPEND	Segment of the service URL that follows the service keyword (e.g., "dfjiao-ijgao.a.run.app")
SOLOGENIC_ADMINISTRATOR	JSON string containing accountID and network for bootstrap admin (e.g., {"accountID":"admin@example.com","network":"testnet"}). This account is injected as a Sologenic organizational administrator, bypassing all security checks.
COMPLIANCE_MANAGER_CODE_ID	Contract code ID of the compliance manager contract in the Coreum network
LOG_LEVEL	Logging level (info, debug, warn, error)
Bootstrap Administrator Configuration
The SOLOGENIC_ADMINISTRATOR environment variable allows bootstrapping the first platform administrator:

json
{
  "accountID": "admin@example.com",
  "network": "testnet"
}
When set, this account is injected into the database as a Sologenic organizational administrator, bypassing all security checks. This is used for initial platform setup.

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
  "message": "Insufficient permissions. Required role: SOLOGENIC_ADMINISTRATOR"
}
Forbidden - Organization Mismatch (403)
json
{
  "error": "Forbidden",
  "message": "Cannot update organization",
  "details": "User does not belong to the specified organization"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Missing required field: Name",
  "details": "Organization name is required"
}
Conflict (409)
json
{
  "error": "Conflict",
  "message": "Organization already exists",
  "details": "An organization with name 'New ORG 2' already exists"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Organization not found",
  "details": "No organization found with ID: 34422ce6-7b51-4a15-accb-34959f39d8ca"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Cannot update organization	OrganizationID doesn't match caller's org	Use GET /get first to verify your OrganizationID
List returns empty	Not a Sologenic Administrator	Verify user has platform admin role
Create fails with 403	Insufficient permissions	Only Sologenic Administrators can create organizations
User not associated with org	User account not assigned to organization	Assign user to organization via Account Service
AdminEmail user not created	Account creation failed	Verify Firebase user exists before creating organization
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check current user's organization:

bash
# Get own organization
curl -X GET /api/organization/get \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet"
List all organizations (Sologenic Admin only):

bash
curl -X GET "/api/organization/list?offset=0&limit=100" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet"
Best Practices
Organization Creation
Use Unique Names: Organization names should be unique and descriptive

Set AdminEmail Correctly: The AdminEmail user must exist in Firebase before creation

Provide Complete Information: Include Logo and URL for brand consistency

Use HTTPS URLs: Always use HTTPS for Logo and URL fields

Organization Management
Regular Updates: Keep organization information current

Logo Optimization: Use appropriately sized logos (recommended: 200x200px)

Descriptive Names: Use clear, identifiable organization names

Audit Trail: Monitor UpdatedAt timestamps for unauthorized changes

Multi-Tenant Configuration
When creating a new organization, ensure the following services are configured:

Service	Configuration Needed
Admin Account Service	Assign Organization Administrator role to AdminEmail
Admin Asset Service	Configure organization-specific assets
Admin Jurisdiction Service	Define applicable jurisdictions
Admin Certificate Service	Set up organization certificates
Admin Feature Flag Service	Configure organization feature flags
Related Services
Service	Description
Admin Account Service	User management and role assignment
Admin Asset Service	Organization asset management
Admin Jurisdiction Service	Organization jurisdiction configuration
Admin Certificate Service	Organization certificate management
Admin Feature Flag Service	Organization feature flags
Admin Notification Service	Organization notifications
Admin MiniCMS Service	Organization content blocks
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the Organization Service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the Organization Service section under Admin Services:

markdown
### Admin Organization Service

The Organization Service provides RESTful interfaces for managing organizations (tenants) within the marketplace platform.

📖 **[Admin Organization Service Documentation](./admin/organization/organization-service.md)**

**Key Features:**
- View own organization details
- Update organization information
- List all organizations (Sologenic Admin only)
- Create new organizations (Sologenic Admin only)
- Multi-tenant isolation foundation
- Bootstrap administrator injection

**Organization Fields:**
| Field | Description |
|-------|-------------|
| OrganizationID | Unique UUID (auto-generated) |
| Name | Organization display name |
| Description | Organization description |
| Logo | URL to organization logo |
| URL | Organization website |
| AdminEmail | Administrator email (create only) |

**Role-Based Access:**
| Role | Permissions |
|------|-------------|
| Organization Administrator | View/update own organization |
| Sologenic Administrator | List all, create organizations |

**Quick Examples:**
```bash
# Get own organization
GET /api/organization/get

# Update organization
PUT /api/organization/update
{
  "OrganizationID": "uuid",
  "Name": "Updated Name",
  "Description": "New description"
}

# List all organizations (Sologenic Admin)
GET /api/organization/list?offset=0&limit=20

# Create organization (Sologenic Admin)
POST /api/organization/create
{
  "Name": "New Organization",
  "AdminEmail": "admin@example.com"
}
Bootstrap Admin:

json
SOLOGENIC_ADMINISTRATOR={"accountID":"admin@example.com","network":"testnet"}
text

Now verify the structure:

```bash
ls -la ~/dev/TXdocumentation/marketplace/admin/
ls -la ~/dev/TXdocumentation/marketplace/admin/organization/
