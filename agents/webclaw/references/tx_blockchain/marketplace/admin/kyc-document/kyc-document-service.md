# KYC Admin Document Service

The KYC Admin Document Service provides RESTful interfaces for managing KYC (Know Your Customer) documents submitted by users during identity verification processes. This service integrates with identity verification providers like Persona to track and manage verification documents.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ KYC Admin Document Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├─────────────────────────┬───────────────────────────────────────────┤ │
│ │ GET /get │ GET /list │ │
│ │ (Get by ID) │ (List with filters) │ │
│ └─────────────────────────┴───────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ KYC Document │ Account Store │ Role Store │ Feature Flag │ │
│ │ Store │ │ │ Store │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Systems │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Persona (Identity Verification Provider) │ │
│ │ • File Storage (Document images/files) │ │
│ │ • KYC Service (Verification status) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/adminkycdoc/get | KYC_ADMINISTRATOR | Get document by ID |
| GET /api/adminkycdoc/list | KYC_ADMINISTRATOR | List documents with filters |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Organization ID in `OrganizationID` header
- Network in `Network` header (mainnet, testnet, devnet)

## Data Models

### KYCDocument Object

| Field | Type | Description |
|-------|------|-------------|
| DocumentID | string | Internal document UUID (not Persona ID) |
| PersonaDocumentID | string | Document ID from Persona verification service |
| InquiryID | string | Persona inquiry ID for the verification session |
| UserID | string | User email or identifier |
| FileName | string | Original filename of the document |
| FilePath | string | Storage path to the document file |
| Type | string | Document type (e.g., "passport", "drivers_license") |
| OrganizationID | string | Organization UUID |
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |
| CreatedAt | Timestamp | When the document was uploaded |
| ExpiresAt | Timestamp | When the document expires (if applicable) |

### Document Types

| Type | Description | Common Use |
|------|-------------|------------|
| passport | International passport | Primary ID verification |
| drivers_license | Driver's license | Secondary ID verification |
| national_id | National identity card | Country-specific ID |
| selfie | Selfie photograph | Liveness check |
| proof_of_address | Utility bill, bank statement | Address verification |
| tax_id | Tax identification number | Tax compliance |
| incorporation_certificate | Business registration | Corporate KYC |

### Network Values

| Network ID | Network Name | Description |
|------------|--------------|-------------|
| 1 | mainnet | Production network |
| 2 | testnet | Testing network |
| 3 | devnet | Development network |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | string | Unix timestamp in seconds |
| nanos | int | Nanoseconds offset |

## API Endpoints

### GET /api/adminkycdoc/get

Gets a KYC document by its internal ID. This ID is an internal system ID, not the Persona-assigned ID.

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| id | string | Internal document UUID | Yes |

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
  "https://api.admin.sologenic.org/api/adminkycdoc/get?id=f47ac10b-58cc-4372-a567-0e02b2c3d479" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "DocumentID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "PersonaDocumentID": "doc_abc123def456",
  "InquiryID": "inq_xyz789uvw012",
  "UserID": "someUser@gmail.com",
  "FileName": "passport_front",
  "FilePath": "/path/to/document/in/storage",
  "Type": "passport",
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Network": 1,
  "CreatedAt": {
    "seconds": "1717027800",
    "nanos": 0
  },
  "ExpiresAt": {
    "seconds": "1874793800",
    "nanos": 0
  }
}
Error Responses
Status Code	Description
200	Success - Document found
400	Bad request - Missing ID parameter
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions (requires KYC_ADMINISTRATOR)
404	Not found - Document does not exist
500	Internal server error
GET /api/adminkycdoc/list
Lists KYC documents belonging to a user using various filters.

Query Parameters
Parameter	Type	Description	Required
persona_id	string	Persona ID for the verification session	No
user_id	string	User email or identifier	No
inquiry_id	string	Persona inquiry ID	No
type	string	Document type filter	No
offset	int	Pagination offset	No (default: 0)
limit	int	Items per page	No (default: 20)
Note: At least one filter parameter should be provided.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
# List by user_id
curl -X GET \
  "https://api.admin.sologenic.org/api/adminkycdoc/list?user_id=someUser@gmail.com" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"

# List by inquiry_id with pagination
curl -X GET \
  "https://api.admin.sologenic.org/api/adminkycdoc/list?inquiry_id=inq_xyz789uvw012&offset=0&limit=10" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"

# List by type and user
curl -X GET \
  "https://api.admin.sologenic.org/api/adminkycdoc/list?user_id=someUser@gmail.com&type=passport" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"

# List by persona_id
curl -X GET \
  "https://api.admin.sologenic.org/api/adminkycdoc/list?persona_id=per_abc123def456" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "KYCDocuments": [
    {
      "DocumentID": "b2c3d4e5-f6g7-8901-bcde-f23456789012",
      "PersonaDocumentID": "doc_def456ghi789",
      "InquiryID": "inq_xyz789uvw012",
      "UserID": "someUser@gmail.com",
      "FileName": "passport_front",
      "FilePath": "/path/to/document/in/storage",
      "Type": "passport",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Network": 1,
      "CreatedAt": {
        "seconds": "1717027800",
        "nanos": 0
      },
      "ExpiresAt": {
        "seconds": "1874793800",
        "nanos": 0
      }
    },
    {
      "DocumentID": "c3d4e5f6-g7h8-9012-cdef-345678901234",
      "PersonaDocumentID": "doc_ghi789jkl012",
      "InquiryID": "inq_xyz789uvw012",
      "UserID": "someUser@gmail.com",
      "FileName": "passport_back",
      "FilePath": "/path/to/document/in/storage",
      "Type": "passport",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Network": 1,
      "CreatedAt": {
        "seconds": "1717027820",
        "nanos": 0
      },
      "ExpiresAt": {
        "seconds": "1874793820",
        "nanos": 0
      }
    },
    {
      "DocumentID": "d4e5f6g7-h8i9-0123-def4-456789012345",
      "PersonaDocumentID": "doc_jkl012mno345",
      "InquiryID": "inq_xyz789uvw012",
      "UserID": "someUser@gmail.com",
      "FileName": "selfie_verification",
      "FilePath": "/path/to/document/in/storage",
      "Type": "selfie",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Network": 1,
      "CreatedAt": {
        "seconds": "1717027840",
        "nanos": 0
      },
      "ExpiresAt": {
        "seconds": "1874793840",
        "nanos": 0
      }
    }
  ],
  "Offset": 0
}
Error Responses
Status Code	Description
200	Success - Returns array (may be empty)
400	Bad request - Invalid filter parameters
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions (requires KYC_ADMINISTRATOR)
500	Internal server error
KYC Document Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        KYC Document Lifecycle                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐                                                          │
│  │ User Uploads │                                                          │
│  │ Document     │                                                          │
│  └──────┬───────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│  │ Persona      │────▶│ Document     │────▶│ Document     │               │
│  │ Verification │     │ Stored in    │     │ Record       │               │
│  │              │     │ Cloud Storage│     │ Created      │               │
│  └──────────────┘     └──────────────┘     └──────┬───────┘               │
│                                                    │                        │
│                                                    ▼                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Document Accessible via KYC Admin API                               │   │
│  │ • GET /get - Retrieve by ID                                         │   │
│  │ • GET /list - List by user/inquiry/persona                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                    │                        │
│                                                    ▼                        │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│  │ Document     │     │ Document      │     │ Document     │               │
│  │ Expires      │────▶│ Archived      │────▶│ Deleted      │               │
│  │ (ExpiresAt)  │     │               │     │              │               │
│  └──────────────┘     └──────────────┘     └──────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Persona Integration
The service integrates with Persona (identity verification provider) for document collection and verification.

Persona ID Mapping
Persona Field	System Field	Description
Persona Inquiry ID	InquiryID	Links documents to a verification session
Persona Document ID	PersonaDocumentID	Original document ID from Persona
Persona Account ID	-	Links to user's Persona account
Common Persona Document Types
Persona Type	System Type	Description
govt_id_national	national_id	Government-issued national ID
govt_id_passport	passport	Passport document
govt_id_drivers_license	drivers_license	Driver's license
selfie	selfie	Liveness selfie
proof_of_address	proof_of_address	Address verification
Filter Examples
Filter by User ID
Retrieve all documents for a specific user:

text
GET /api/adminkycdoc/list?user_id=john.doe@example.com
Filter by Inquiry ID
Retrieve all documents from a specific verification session:

text
GET /api/adminkycdoc/list?inquiry_id=inq_xyz789uvw012
Filter by Persona ID
Retrieve documents for a specific Persona account:

text
GET /api/adminkycdoc/list?persona_id=per_abc123def456
Filter by Document Type
Retrieve only passport documents for a user:

text
GET /api/adminkycdoc/list?user_id=john.doe@example.com&type=passport
Pagination Example
Retrieve documents with pagination:

text
GET /api/adminkycdoc/list?user_id=john.doe@example.com&offset=0&limit=10
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/http/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
KYC_DOCUMENT_STORE	KYC document store endpoint	github.com/sologenic/com-fs-admin-kyc-document-model
ACCOUNT_STORE	Admin account store endpoint	github.com/sologenic/com-fs-admin-account-model
ROLE_STORE	Role store endpoint	github.com/sologenic/com-fs-role-model
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-be-admin-certificate-store/
CERTIFICATE_STORE	Certificate store endpoint	github.com/sologenic/com-be-http-lib/http/
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
  "message": "Insufficient permissions for this operation. Required role: KYC_ADMINISTRATOR"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid filter parameters",
  "details": "At least one filter parameter (persona_id, user_id, inquiry_id, type) must be provided"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Document not found",
  "details": "No document found with ID: f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Document not found	Wrong ID type	Use internal DocumentID, not PersonaDocumentID
Empty list returned	No documents match filters	Verify user_id, inquiry_id, or persona_id
Permission denied	Insufficient role	Ensure user has KYC_ADMINISTRATOR role
Invalid token	Token expired or malformed	Refresh Firebase token
Missing filter parameters	No filters provided	Provide at least one filter parameter
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check document existence:

bash
# List documents for a user
curl -X GET /api/adminkycdoc/list?user_id=user@example.com \
  -H "Network: mainnet" \
  -H "Authorization: Bearer <token>"

# Get specific document
curl -X GET /api/adminkycdoc/get?id=<document_id> \
  -H "Network: mainnet" \
  -H "Authorization: Bearer <token>"
Best Practices
Document Retrieval
Use Appropriate Filters: Always use the most specific filter available (inquiry_id > user_id > persona_id)

Pagination: Always use offset/limit for large result sets

Cache When Possible: Document metadata rarely changes; implement caching for frequent access

Security
Role-Based Access: Ensure only KYC_ADMINISTRATORs can access sensitive documents

Audit Logging: Log all document access for compliance purposes

Data Minimization: Only request document access when necessary

Compliance
Document Expiration: Monitor ExpiresAt timestamps for document renewal

Retention Policy: Implement document retention based on regulatory requirements

Data Privacy: Ensure document access complies with GDPR, CCPA, etc.

Related Services
Service	Description
KYC Service	User verification status management
Admin Account Service	User and role management
File Service	Document file storage and retrieval
Persona	Identity verification provider
Admin Jurisdiction Service	Jurisdiction-based KYC requirements
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the KYC Document Service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the KYC Document Service section under Admin Services:

markdown
### Admin KYC Document Service

The KYC Admin Document Service provides RESTful interfaces for managing KYC (Know Your Customer) documents submitted by users during identity verification processes.

📖 **[Admin KYC Document Service Documentation](./admin/kyc-document/kyc-document-service.md)**

**Key Features:**
- Get document by internal ID
- List documents with filters (user_id, inquiry_id, persona_id, type)
- Integration with Persona identity verification
- Document metadata tracking (filename, type, timestamps)
- Expiration date management

**Document Types:**
| Type | Description |
|------|-------------|
| passport | International passport |
| drivers_license | Driver's license |
| national_id | National identity card |
| selfie | Liveness selfie |
| proof_of_address | Address verification |
| tax_id | Tax identification number |

**Quick Examples:**
```bash
# Get document by ID
GET /api/adminkycdoc/get?id=<document_id>

# List user documents
GET /api/adminkycdoc/list?user_id=user@example.com

# List by inquiry
GET /api/adminkycdoc/list?inquiry_id=inq_xyz789uvw012
Required Role: KYC_ADMINISTRATOR

