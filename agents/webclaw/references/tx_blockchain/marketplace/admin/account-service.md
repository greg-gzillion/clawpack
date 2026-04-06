# Admin Account Service

The Admin Account Service provides API interfaces that manage users and their roles within a multi-tier system. All organization-related operations are provided by the `com-be-admin-organization-service` separately.

## Account Types Hierarchy
┌─────────────────────────────────────────────────────────────────────────────┐
│ Account Type Hierarchy │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────┐ │
│ │ Sologenic Administrator │ │
│ │ (Platform Level) │ │
│ └─────────────┬───────────────┘ │
│ │ │
│ │ Creates │
│ ▼ │
│ ┌─────────────────────────────┐ │
│ │ Organization Administrator │ │
│ │ (Organization Level) │ │
│ └─────────────┬───────────────┘ │
│ │ │
│ ┌───────────────────┼───────────────────┐ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│ │ KYC │ │ Broker Asset │ │ Normal User │ │
│ │ Administrator │ │ Administrator │ │ (End User) │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Account Types

### Sologenic Administrator (SOLOGENIC_ADMINISTRATOR)

Sologenic Administrators provide initial setup such as the creation and management of organizations, and assign initial Organization Administrators.

**Permissions:**
- Creates new organizations
- Creates initial organization administrators
- Views list of organizations
- Creates new sologenic administrators
- Cannot access or modify org users, end users, or organization details

### Organization Administrator (ORGANIZATION_ADMINISTRATOR)

Organization Administrators have complete authority within their assigned organization.

**Permissions:**
- Manages all aspects within their organization
- Creates new accounts (organization's employee) and assigns roles
- Updates organization details
- Assigns and updates user roles within the organization
- Manages rolepaths
- Manages users within their organization (retrieving, updating, disabling accounts)

### KYC Administrator (KYC_ADMINISTRATOR)

KYC Administrators are responsible for managing KYC processes within their organization.

**Permissions:**
- Manages KYC processes within their organization
- KYC processes are handled in a separate KYC service

### Broker Asset Administrator (BROKER_ASSET_ADMINISTRATOR)

Broker Asset Administrators are responsible for managing assets within their organization.

**Permissions:**
- Manages assets within their organization
- Creates and manages assets
- Asset management is handled in a separate asset service

### Normal User (NORMAL_USER)

Fully managed by Organization Administrators, with no direct access to the admin service.

**Characteristics:**
- Operates under organization management
- KYC managed by KYC Administrator in separate KYC service
- No direct API access to admin service

## Business Logic

### Sologenic Administrators
- Managing the entire platform's structure
- Creating new organizations
- Assigning initial Organization Administrators
- Onboarding new entities
- Ensuring administrative hierarchy is properly established

### Organization Administrators
- Responsible for internal management of their organizations
- Updating organizational details (names, addresses)
- Managing other types of admins
- Creating new users (organization's employees)
- Modifying existing users
- Assigning or updating user roles
- Managing end users (retrieving, updating, disabling accounts)

## Primary Sologenic Administrator Creation (Optional)

The application can be configured with a primary Sologenic Administrator account at startup. When configured, this account will be created automatically (if it doesn't exist) and granted Sologenic admin privileges.

### Configuration

Set the `SOLOGENIC_ADMINISTRATOR` environment variable with a JSON string containing:

| Field | Type | Description |
|-------|------|-------------|
| accountID | string | Email address of the primary administrator |
| network | string | "mainnet", "testnet", or "devnet" |

### Example Configuration

```bash
SOLOGENIC_ADMINISTRATOR='{"accountID":"sg.primary.admin@gmail.com","network":"mainnet"}'
Creating Additional Sologenic Administrators
Once at least one Sologenic Administrator exists in the system, they can create additional Sologenic Administrator accounts through the /api/account/create-sologenic-admin endpoint.

Characteristics:

Created on the same network as specified in the request

Have the SOLOGENIC_ADMINISTRATOR role

Only existing Sologenic Administrators can create new Sologenic Administrator accounts

Can only create them on networks they have access to

API Endpoints Overview
Sologenic Administrator Interfaces
Method	Endpoint	Description
POST	/api/account/create-org-admin	Creates new organization admin for newly registered organization
POST	/api/account/create-sologenic-admin	Creates a new Sologenic Administrator
PUT	/api/account/update-sologenic-admin	Updates a Sologenic Administrator account
PUT	/api/account/update-sologenic-admin/roles	Updates roles of a Sologenic Administrator
PUT	/api/account/update-sologenic-admin/status	Updates status of a Sologenic Administrator
Organization Administrator Interfaces
Method	Endpoint	Description
GET	/api/account/get?account_id=...	Retrieves account information
GET	/api/account/accounts?filter=...	Retrieves all accounts with filter
PUT	/api/account/update	Updates account information
PUT	/api/account/update/roles	Updates roles of an account
PUT	/api/account/update/status	Modifies account status
POST	/api/account/create	Creates new account under organization
GET	/api/account/rolepaths	Retrieves rolepath information
PUT	/api/account/rolepaths	Updates rolepath for organization
Authentication
All authenticated endpoints require a valid Firebase token in the Authorization header.

Header Format
text
Authorization: Bearer: eyJhbGciOiJSUzI1NiIsImtpZCI6...
Network: mainnet
Requirements:

Token must be obtained from Firebase Authentication service

Token must be prepended with Bearer:

Network header must specify the target network (mainnet, testnet, devnet)

Authorization Check Routes
Each authenticated route has a corresponding authorization check route for UI rendering decisions.

Pattern
Route Type	Format	Example
Main Route	{basepath}/{path}	/api/account/get
Auth Check	{basepath}/isauth/{path}	/api/account/isauth/get
Auth Check Response
json
{
  "Authorized": true,
  "Roles": [3, 7]
}
Field	Description
Authorized	Boolean indicating if user has permission
Roles	Array of role IDs the user possesses
API Endpoints Details
POST /api/account/create-org-admin
Role Required: Sologenic Administrator Only

Creates a new organization admin for the newly registered organization and assigns the organization admin roles.

Notes:

AccountID and ExternalUserID are generated automatically

New organization admins are created with the same network as the sologenic admin who creates them

Request
bash
curl -X POST "https://api.admin.sologenic.org/api/account/create-org-admin" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "FirstName": "Billy",
    "LastName": "Bob",
    "Address": "SomeAddress",
    "Avatar": "someAvatar",
    "Alias": "BillyBob",
    "Description": "1st admin for new org",
    "Status": 1,
    "OrganizationID": "783174ea-d891-4c0c-9c69-c733850ea391"
  }'
Response
json
{
  "AccountID": "billy@abc.org",
  "Network": 1
}
POST /api/account/create-sologenic-admin
Role Required: Sologenic Administrator Only

Creates a new Sologenic Administrator account.

Notes:

Account will be created (or updated) and role escalated to SOLOGENIC_ADMINISTRATOR

New Sologenic admins are created with the same network as the creating admin

Request
bash
curl -X POST "https://api.admin.sologenic.org/api/account/create-sologenic-admin" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "AccountID": "sologenic.admin@sologenic.org",
    "FirstName": "Martin",
    "LastName": "Kim",
    "Description": "Sologenic admin"
  }'
Response
json
{
  "AccountID": "sologenic.admin@sologenic.org",
  "Network": 1
}
PUT /api/account/update-sologenic-admin
Role Required: Sologenic Administrator Only

Updates a Sologenic Administrator account.

Notes:

Role and Status are not updated using this endpoint

Use /api/account/update-sologenic-admin/status for status updates

Roles for Sologenic Administrators are managed separately through the primary admin system

Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/account/update-sologenic-admin" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "AccountID": "sologenic.admin@sologenic.org",
    "FirstName": "Martin",
    "LastName": "Kim",
    "Address": "UpdatedAddress",
    "Avatar": "updatedAvatar",
    "Alias": "UpdatedAlias",
    "Description": "Updated Sologenic admin description",
    "Network": 1
  }'
Response
json
{
  "AccountID": "sologenic.admin@sologenic.org",
  "Network": 1
}
PUT /api/account/update-sologenic-admin/roles
Role Required: Sologenic Administrator Only

Updates the roles for an Account.

Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/account/update-sologenic-admin/roles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: <token>" \
  -H "Network: testnet" \
  -d '{
    "AccountID": "billy@abc.org",
    "Roles": [4, 6],
    "Network": 2
  }'
PUT /api/account/update-sologenic-admin/status
Role Required: Sologenic Administrator Only

Updates the status of a Sologenic Administrator account.

Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/account/update-sologenic-admin/status" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "AccountID": "sologenic.admin@sologenic.org",
    "Status": 1,
    "Network": 1
  }'
Response
json
{
  "AccountID": "sologenic.admin@sologenic.org",
  "Network": 1
}
GET /api/account/get
Role Required: Organization Administrator Only

Retrieves the Account information for the given account_id.

Query Parameters
Parameter	Type	Required	Description
account_id	string	Yes	The account ID to retrieve
Request
bash
curl -X GET "https://api.admin.sologenic.org/api/account/get?account_id=derrick@sologenic.org" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: <token>" \
  -H "Network: testnet"
Response
json
{
  "AccountID": "derrick@sologenic.org",
  "FirstName": "Derrick",
  "LastName": "Quigley",
  "Address": "ABC3",
  "Wallets": [
    {
      "Address": "Awesome Tasty invoice1",
      "Alias": "Fresh back up1",
      "Type": 2
    },
    {
      "Address": "maroon Handmade Wooden Keyboard Borders1",
      "Alias": "bus program Versatile1",
      "Type": 3
    }
  ],
  "CreatedAt": {
    "seconds": 1720469429,
    "nanos": 503021000
  },
  "UpdatedAt": {
    "seconds": 694,
    "nanos": 721
  },
  "Socials": [
    {
      "URL": "http://lurline.name"
    },
    {
      "URL": "https://maryam.biz"
    }
  ],
  "Avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/493.jpg",
  "Alias": "ABC3",
  "Description": "invoice back up",
  "Network": 2,
  "Status": 1,
  "Roles": [1],
  "ExternalUserID": "976e4b26-9a82-3353-c598-fff0c7ff2f32",
  "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca"
}
GET /api/account/accounts
Role Required: Sologenic Administrator and Organization Administrator Only

Retrieves all Account information based on the given AccountFilter, with pagination.

Query Parameters
Parameter	Type	Required	Description
filter	string	Yes	Base64 encoded AccountFilter
AccountFilter Object
protobuf
message AccountFilter {
    optional Role Role = 1;
    repeated string AccountIDs = 2;
    optional Order Order = 3;
    optional int32 Offset = 4;
    optional int32 Limit = 5;
    string Network = 6;
}
Defaults:

Limit: 20

Offset: 0

Request
bash
curl -X GET "https://api.admin.sologenic.org/api/account/accounts?filter=eyJSb2xlcyI6WzFdLCJBY2NvdW50SURzIjpbImYyNmY4NjJjLTBjNzAtYzYxYi0yNmFmLTczZDhlM2ZlZDg3ZiIsImY0YmVjMGZiLWZjMGItNTE4OS1jYzNkLWVlZGQwZDE0ZTNiOCIsIjk3MGIxYTY5LTA5NGEtOGZlZi04Y2FmLTI4MzMxYjJmNTU0MCJdLCJPcmRlciI6e30sIk9mZnNldCI6MSwiTGltaXQiOjIwfQ==" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: <token>" \
  -H "network: testnet"
Response
json
{
  "Accounts": [
    {
      "AccountID": "cecilia@abc.org",
      "FirstName": "Cecilia",
      "LastName": "Mueller",
      "Address": "HBTestAddress",
      "Wallets": [
        {
          "Address": "Future disintermediate",
          "Alias": "cross-media Jordanian Dinar Internal",
          "Type": 1
        }
      ],
      "CreatedAt": {
        "seconds": 1720564151,
        "nanos": 172969000
      },
      "Network": 2,
      "Status": 1,
      "Roles": [1, 2],
      "ExternalUserID": "2802f6b7-52ec-354a-5da7-33c0995ca972",
      "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca"
    }
  ],
  "Offset": 0
}
POST /api/account/create
Role Required: Organization Administrator Only

Creates a new account in the given organization.

Notes:

AccountID and ExternalUserID are generated automatically

Account is created with NORMAL_USER role by default

Request
bash
curl -X POST "https://api.admin.sologenic.org/api/account/create" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "AccountID": "billy.bob@abc.org",
    "FirstName": "Billy",
    "LastName": "Bob",
    "Address": "SomeAddress",
    "Avatar": "someAvatar",
    "Alias": "BillyBob",
    "Description": "some description",
    "Status": 1,
    "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca"
  }'
Response
json
{
  "AccountID": "billy.bob@abc.org",
  "Network": 2
}
PUT /api/account/update
Role Required: Organization Administrator Only

Updates the account information for a specified account within the organization.

Notes:

Role and Status are not updated using this endpoint

Use /api/account/update/roles and /api/account/update/status for those operations

Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/account/update" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "AccountID": "billy.bob@abc.org",
    "FirstName": "Billy",
    "LastName": "Bob",
    "Address": "SomeAddress",
    "Avatar": "someAvatar",
    "Alias": "BillyBob",
    "Description": "some description",
    "Network": 1,
    "ExternalUserID": "022a60d0-c78e-4eb5-92be-e417a466acee",
    "OrganizationID": "215a551d-5691-91ce-f4a6-9284f40d1340"
  }'
Response
json
{
  "AccountID": "billy.bob@abc.org",
  "Network": 1
}
PUT /api/account/update/roles
Role Required: Organization Administrator Only

Updates the roles for an Account.

Note: Including the SOLOGENIC_ADMINISTRATOR role will result in an error.

Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/account/update/roles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: <token>" \
  -H "Network: testnet" \
  -d '{
    "AccountID": "billy@abc.org",
    "Roles": [1, 2],
    "Network": 1
  }'
PUT /api/account/update/status
Role Required: Organization Administrator Only

Updates the status for an Account.

Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/account/update/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: <token>" \
  -H "Network: testnet" \
  -d '{
    "AccountID": "billy@abc.org",
    "Status": 1,
    "Network": 1
  }'
GET /api/account/rolepaths
Role Required: Organization Administrator Only

Retrieves all Rolepath information for the current organization and network.

Request
bash
curl -X GET "https://api.admin.sologenic.org/api/account/rolepaths" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "Authorization: Bearer: <token>"
Response
json
{
  "RolePaths": {
    "RolePaths": [
      {
        "Path": "create",
        "BasePath": "account",
        "Method": 1,
        "OrganizationID": "215a551d-5691-91ce-f4a6-9284f40d1340",
        "Role": [4, 7],
        "CreatedAt": {
          "seconds": 1732910539,
          "nanos": 358492000
        },
        "UpdatedAt": {
          "seconds": 1732910539,
          "nanos": 358493000
        },
        "Network": 1
      }
    ]
  }
}
PUT /api/account/rolepaths
Role Required: Organization Administrator Only

Updates the rolepath for an organization and network.

Note: Organization Administrators can create or update roles within their privilege level but cannot create or update role paths that require higher privileges than their own.

Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/account/rolepaths" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer: <token>" \
  -d '{
    "Path": "create",
    "BasePath": "account",
    "Method": 1,
    "Role": [3, 4, 7],
    "Description": "Update role testing"
  }'
Role Definitions
Role ID	Role Name	Description
1	NORMAL_USER	Standard end user
2	KYC_ADMINISTRATOR	Manages KYC processes
3	BROKER_ASSET_ADMINISTRATOR	Manages assets
4	ORGANIZATION_ADMINISTRATOR	Manages organization
5	SOLOGENIC_ADMINISTRATOR	Platform-level admin
Account Status Values
Status ID	Status Name	Description
0	INACTIVE	Account is disabled
1	ACTIVE	Account is active
2	SUSPENDED	Account is temporarily suspended
3	PENDING_VERIFICATION	Awaiting verification
Application Start Parameters
Environment Variables
Variable	Description	Required
HTTP_CONFIG	HTTP server configuration	Yes
AUTH_FIREBASE_SERVICE	Firebase authentication service endpoint	Yes
ACCOUNT_STORE	Account service endpoint	Yes
FEATURE_FLAG_STORE	Feature flag service endpoint	Yes
ORGANIZATION_STORE	Organization service endpoint	Yes
ROLE_STORE	Role service endpoint	Yes
SOLOGENIC_ADMINISTRATOR	Primary admin configuration (optional)	No
SOLOGENIC_ADMINISTRATOR Configuration
When set with a JSON object containing accountID and network, that account is injected into the database as a Sologenic Administrator, bypassing all security checks. This is used to initially set up the application.

bash
SOLOGENIC_ADMINISTRATOR='{"accountID":"admin@sologenic.org","network":"mainnet"}'
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
  "message": "Insufficient permissions for this operation"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid request parameters",
  "details": "AccountID is required"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Account not found"
}
Sequence Diagram
text
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│   Client   │     │   Admin    │     │  Account   │     │    Org     │
│            │     │   Service  │     │   Store    │     │  Service   │
└─────┬──────┘     └─────┬──────┘     └─────┬──────┘     └─────┬──────┘
      │                  │                  │                  │
      │ POST /create-org-admin              │                  │
      │─────────────────▶│                  │                  │
      │                  │                  │                  │
      │                  │ Verify Role      │                  │
      │                  │ (Sologenic)      │                  │
      │                  │                  │                  │
      │                  │ Create Account   │                  │
      │                  │─────────────────▶│                  │
      │                  │                  │                  │
      │                  │ Create Org Admin │                  │
      │                  │─────────────────────────────────────▶│
      │                  │                  │                  │
      │                  │ Return Response  │                  │
      │◀─────────────────│                  │                  │
      │                  │                  │                  │
Network Values
Network	Value	Description
devnet	3	Development network
testnet	2	Test network
mainnet	1	Production network
Best Practices
Security
Always use HTTPS in production environments

Store tokens securely - never expose in client-side code

Implement proper CORS policies

Use short-lived tokens with refresh mechanisms

Validate network headers match expected environment

Performance
Use pagination for large account lists

Cache rolepath data when appropriate

Implement rate limiting on sensitive endpoints

Use batch operations when possible

Error Handling
Implement retry logic for transient failures

Log all authorization failures for audit

Provide meaningful error messages without exposing internals

Troubleshooting
Common Issues
Issue	Solution
Token validation fails	Verify Firebase token is valid and not expired
Network mismatch	Ensure Network header matches the environment
Insufficient permissions	Verify user has required role for the operation
Account not found	Check account_id exists in the specified network
Role assignment error	Cannot assign SOLOGENIC_ADMINISTRATOR via org admin
Resources
Resource	Link
Organization Service	organization-service.md
KYC Service	kyc-service.md
Asset Service	asset-service.md
Firebase Auth	https://firebase.google.com/docs/auth
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the admin account service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add this section:

markdown
## Admin Services

### Admin Account Service

The Admin Account Service manages users and their roles within a multi-tier system.

📖 **[Admin Account Service Documentation](./admin/account-service.md)**

**Account Types:**
- Sologenic Administrator (Platform level)
- Organization Administrator (Organization level)
- KYC Administrator
- Broker Asset Administrator
- Normal User (End User)

**Key Features:**
- Multi-tier role-based access control
- Organization onboarding and management
- User creation and role assignment
- Rolepath management
- Firebase authentication integration
- Authorization check routes for UI

**Quick Example:**
```bash
# Create organization admin (Sologenic only)
POST /api/account/create-org-admin

# Create user (Organization admin)
POST /api/account/create

# Update user roles
PUT /api/account/update/roles
