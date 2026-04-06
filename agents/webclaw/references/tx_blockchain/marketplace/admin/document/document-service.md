# Admin Document Service

The Admin Document Service provides document lifecycle management with version control and status management for organizational compliance. It handles legal documents, terms of service, privacy policies, margin agreements, and other compliance-related documents that require version tracking and signature collection.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin Document Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ GET /list │ POST /create │ PUT /update │ PUT /publish │ │
│ │ │ /draft │ /draft │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Document Store│ Account Store │ Role Store │ File Store │ │
│ │ Feature Flag │ Organization │ Auth Firebase │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Storage Layer │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Temporary file storage (drafts) │ │
│ │ • Permanent file storage (published) │ │
│ │ • Document metadata database │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Document Statuses

Documents have three states in the system:

| Status ID | Status Name | Description | Editable | Can Publish | Can Sign |
|-----------|-------------|-------------|----------|-------------|----------|
| 1 | UNPUBLISHED | Draft document that can be modified freely | ✅ Yes | ✅ Yes | ❌ No |
| 2 | ACTIVE | Published document, current and effective | ❌ No | ❌ No | ✅ Yes |
| 3 | OUTDATED | Archived document for historical reference | ❌ No | ❌ No | ❌ No |

### Status Transitions
┌─────────────────────────────────────────────────────────────────────────────┐
│ Document Status Transitions │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────────┐ │
│ ┌───▶│ UNPUBLISHED │◀───┐ │
│ │ │ (Draft) │ │ │
│ │ └────────┬─────────┘ │ │
│ │ │ │ │
│ │ │ publish │ update draft │
│ │ ▼ │ │
│ │ ┌──────────────────┐ │ │
│ │ │ ACTIVE │ │ │
│ │ │ (Published) │ │ │
│ │ └────────┬─────────┘ │ │
│ │ │ │ │
│ │ │ mark outdated │
│ │ │ (irreversible) │
│ │ ▼ │ │
│ │ ┌──────────────────┐ │ │
│ └───▶│ OUTDATED │───┘ │
│ │ (Archived) │ │
│ └──────────────────┘ │
│ │
│ Note: Outdated documents cannot be reactivated │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Document Management Workflow

### 1. Create Draft Documents
- Upload PDF files and create document records
- Set version, description, and signature requirement flag
- Files are stored temporarily until published

### 2. Edit & Update
- Draft documents can be edited for metadata only
- Modify description or signature requirement flag
- **Immutable fields**: Name, Version, and File cannot be changed once created
- To change a file, create a new version
- Active and Outdated documents cannot be edited

### 3. Publish Workflow
- Publish draft documents to make them active
- Each document name can have a maximum of 1 active version
- Publishing a new version automatically marks any existing active version with the same name as outdated

### 4. Status Management
- Documents transition through statuses (UNPUBLISHED → ACTIVE → OUTDATED)
- Once published, documents cannot be modified

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/admindoc/list | ORGANIZATION_ADMINISTRATOR | List documents with filter |
| POST /api/admindoc/create/draft | ORGANIZATION_ADMINISTRATOR | Create draft document |
| PUT /api/admindoc/update/draft | ORGANIZATION_ADMINISTRATOR | Update draft document |
| PUT /api/admindoc/publish | ORGANIZATION_ADMINISTRATOR | Publish document |
| PUT /api/admindoc/outdated | ORGANIZATION_ADMINISTRATOR | Mark document as outdated |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Organization ID in `OrganizationID` header
- Network in `Network` header (mainnet, testnet, devnet)

## Data Models

### Document Object

| Field | Type | Description | Immutable After Creation |
|-------|------|-------------|-------------------------|
| OrganizationID | string | Organization UUID | ✅ Yes |
| Name | string | Document name identifier | ✅ Yes |
| Version | string | Document version (e.g., "1.0.0", "v2") | ✅ Yes |
| Description | string | Human-readable description | ❌ No (drafts only) |
| File | FileObject | File metadata and reference | ✅ Yes |
| SignatureRequired | boolean | Whether user signature is required | ❌ No (drafts only) |
| Status | int | Document status (1, 2, 3) | System-managed |

### File Object

| Field | Type | Description |
|-------|------|-------------|
| Reference | string | Storage reference (temporary or permanent) |
| Extension | string | File extension (e.g., "pdf") |
| Name | string | Original filename |
| MD5SUM | string | MD5 hash for integrity verification |

### Filter Object (for GET /list)

```protobuf
message Filter {
    string OrganizationID = 1;
    optional string Name = 2;
    optional bool SignatureRequired = 3;
    optional DocumentStatus Status = 4;
    optional int32 Offset = 5;
    optional int32 Limit = 6;
}
MetaData Object
Field	Type	Description
CreatedAt	timestamp	Creation timestamp
UpdatedAt	timestamp	Last update timestamp
Audit Object
Field	Type	Description
ChangedBy	string	Email or identifier of user who made the change
ChangedAt	timestamp	Timestamp of the change
API Endpoints
GET /api/admindoc/list
Retrieves all documents based on the provided filter, with pagination.

Query Parameters
Parameter	Type	Description	Required
filter	string	Base64 encoded Filter object	Yes
Filter Defaults
Field	Default
Limit	20
Offset	0
Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
# Filter with OrganizationID and Limit
curl -X GET \
  "https://api.admin.sologenic.org/api/admindoc/list?filter=ewogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJMaW1pdCI6IDEwMAp9" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet"
Example Response
json
{
  "Documents": [
    {
      "Document": {
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Name": "Regulatory",
        "Version": "v2",
        "Description": "Draft",
        "File": {
          "Reference": "eyJBZGRyZXNzIjoic2cub3JnLnRlc3RuZXRAZ21haWwuY29tIiwiTmV0d29yayI6MiwiVGVtcEZpbGVuYW1lIjoiUmVndWxhdG9yeSBUZXN0XzIucGRmIiwiVGltZXN0YW1wIjoxNzQ4OTg3MjE0Njg3ODIwMDAwfQ==.pdf",
          "Extension": "pdf",
          "Name": "Regulatory Test_2.pdf",
          "MD5SUM": "b1a2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
        },
        "SignatureRequired": true,
        "Status": 1
      },
      "MetaData": {
        "UpdatedAt": {
          "seconds": 1748987215,
          "nanos": 802662000
        },
        "CreatedAt": {
          "seconds": 1748987215,
          "nanos": 802661000
        }
      },
      "Audit": {
        "ChangedBy": "sg.org.testnet@gmail.com",
        "ChangedAt": {
          "seconds": 1748987215,
          "nanos": 802663000
        }
      }
    },
    {
      "Document": {
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Name": "Regulatory",
        "Version": "v1",
        "Description": "Test",
        "File": {
          "Reference": "testnet/document/72c4c072-2fe4-4f72-ae9d-d9d52a05fd71/Regulatory_v1",
          "Extension": "pdf",
          "Name": "Regulatory",
          "MD5SUM": "c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8"
        },
        "SignatureRequired": true,
        "Status": 2
      },
      "MetaData": {
        "UpdatedAt": {
          "seconds": 1748987082,
          "nanos": 626485000
        },
        "CreatedAt": {
          "seconds": 1748987069,
          "nanos": 212503000
        }
      },
      "Audit": {
        "ChangedBy": "sg.org.testnet@gmail.com",
        "ChangedAt": {
          "seconds": 1748987082,
          "nanos": 626486000
        }
      }
    },
    {
      "Document": {
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Name": "Privacy",
        "Version": "1.1",
        "Description": "Test",
        "File": {
          "Reference": "testnet/document/72c4c072-2fe4-4f72-ae9d-d9d52a05fd71/Privacy_1.1",
          "Extension": "pdf",
          "Name": "Privacy",
          "MD5SUM": "e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1"
        },
        "SignatureRequired": true,
        "Status": 3
      },
      "MetaData": {
        "UpdatedAt": {
          "seconds": 1748986761,
          "nanos": 51447000
        },
        "CreatedAt": {
          "seconds": 1748986665,
          "nanos": 860168000
        }
      },
      "Audit": {
        "ChangedBy": "sg.org.testnet@gmail.com",
        "ChangedAt": {
          "seconds": 1748986761,
          "nanos": 51448000
        }
      }
    }
  ]
}
POST /api/admindoc/create/draft
Creates a new draft document.

Important Notes
If a document with the same Name and Version combination already exists, the request will be rejected

Files are stored in temporary storage until published

Draft documents are not visible to end users

Request Body
Field	Type	Description	Required
Document.OrganizationID	string	Organization UUID	Yes
Document.Name	string	Document name identifier	Yes
Document.Version	string	Document version (e.g., "1.0.0")	Yes
Document.Description	string	Human-readable description	No
Document.File.Reference	string	Temporary file reference (base64 encoded)	Yes
Document.File.Extension	string	File extension (e.g., "pdf")	Yes
Document.File.Name	string	Original filename	Yes
Document.File.MD5SUM	string	MD5 hash for integrity	Yes
Document.SignatureRequired	boolean	Whether signature is required	Yes
Example Request
bash
curl -X POST "https://api.admin.sologenic.org/api/admindoc/create/draft" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "Document": {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "Margin Agreement",
      "Version": "1.0.0",
      "Description": "Margin Agreement for testing purposes",
      "File": {
        "Reference": "eyJBZGRyZXNzIjoiaGVhdmVuOTFAaG90bWFpbC5jb20iLCJOZXR3b3JrIjoyLCJUZW1wRmlsZW5hbWUiOiJhYWEuanBnIiwiVGltZXN0YW1wIjoxNzQzNTU0NDQwMDU2NjYzNjM4fQ==.pdf",
        "Extension": "pdf",
        "Name": "Margin Agreement",
        "MD5SUM": "3a43056cb0bae9fed74dffaf9b3f7d73"
      },
      "SignatureRequired": true
    }
  }'
Success Response
text
200 OK
Error Responses
Status Code	Description
400	Document with same Name and Version already exists
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
500	Internal server error
PUT /api/admindoc/update/draft
Updates an existing draft document. Only UNPUBLISHED documents (drafts) can be updated.

Important Notes
Immutable fields: Name, Version, and File cannot be changed once created

Modifiable fields: Only Description and SignatureRequired can be updated

To change a file, create a new version of the document

Active and Outdated documents cannot be edited

Request Body
Field	Type	Description	Required
Document.OrganizationID	string	Organization UUID	Yes
Document.Name	string	Document name (immutable, for identification)	Yes
Document.Version	string	Document version (immutable, for identification)	Yes
Document.Description	string	Updated description	No
Document.File.MD5SUM	string	MD5 hash (for verification)	Yes
Document.SignatureRequired	boolean	Updated signature requirement	Yes
Document.Status	int	Must be 1 (UNPUBLISHED)	Yes
Example Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/admindoc/update/draft" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "Document": {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "Privacy Policy",
      "Version": "2.0.0",
      "Description": "Updated privacy policy with GDPR compliance",
      "File": {
        "MD5SUM": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
      },
      "SignatureRequired": false,
      "Status": 1
    }
  }'
Success Response
text
200 OK
Error Responses
Status Code	Description
400	Document is not in UNPUBLISHED status
400	Attempting to modify immutable field (Name, Version, File)
401	Unauthorized
403	Forbidden
404	Document not found
PUT /api/admindoc/publish
Publishes a draft document, making it active. Only UNPUBLISHED documents (drafts) can be published.

Important Notes
Publishing automatically outdates any existing active document with the same name

The file reference is updated to permanent storage during publishing

Only one active document per name is allowed at any time

Once published, SignatureRequired becomes immutable

Request Body
Field	Type	Description	Required
Document.OrganizationID	string	Organization UUID	Yes
Document.Name	string	Document name	Yes
Document.Version	string	Document version	Yes
Document.File.Reference	string	File reference (temporary → permanent)	Yes
Document.File.Extension	string	File extension	Yes
Document.File.Name	string	Original filename	Yes
Document.File.MD5SUM	string	MD5 hash	Yes
Document.SignatureRequired	boolean	Signature requirement (becomes immutable)	Yes
Document.Status	int	Must be 1 (UNPUBLISHED)	Yes
Example Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/admindoc/publish" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "Document": {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "Terms of Service",
      "Version": "3.1.0",
      "File": {
        "Reference": "eyJBZGRyZXNzIjoiaGVhdmVuOTFAaG90bWFpbC5jb20iLCJOZXR3b3JrIjoyLCJUZW1wRmlsZW5hbWUiOiJhYWEuanBnIiwiVGltZXN0YW1wIjoxNzQzNTU0NDQwMDU2NjYzNjM4fQ==.pdf",
        "Extension": "pdf",
        "Name": "Terms of Service Final",
        "MD5SUM": "z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4"
      },
      "SignatureRequired": false,
      "Status": 1
    }
  }'
Success Response
text
200 OK
Error Responses
Status Code	Description
400	Document is not in UNPUBLISHED status
400	Active document with same name already exists (auto-handled by outdating)
401	Unauthorized
403	Forbidden
404	Document not found
PUT /api/admindoc/outdated
Manually marks an active document as outdated. Only ACTIVE documents can be marked as outdated.

Important Notes
This action is irreversible - outdated documents cannot be reactivated

Outdated documents are preserved for historical reference

Outdated documents are not considered current for compliance purposes

Request Body
Field	Type	Description	Required
Document.OrganizationID	string	Organization UUID	Yes
Document.Name	string	Document name	Yes
Document.Version	string	Document version	Yes
Document.File.Reference	string	Permanent file reference	Yes
Document.File.Extension	string	File extension	Yes
Document.File.Name	string	Original filename	Yes
Document.File.MD5SUM	string	MD5 hash	Yes
Document.SignatureRequired	boolean	Signature requirement	Yes
Document.Status	int	Must be 2 (ACTIVE)	Yes
Example Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/admindoc/outdated" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "Document": {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "Terms of Service",
      "Version": "3.1.0",
      "File": {
        "Reference": "testnet/document/72c4c072-2fe4-4f72-ae9d-d9d52a05fd71/Terms_of_Service_3.1.0",
        "Extension": "pdf",
        "Name": "Terms of Service Final",
        "MD5SUM": "z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4"
      },
      "SignatureRequired": false,
      "Status": 2
    }
  }'
Success Response
text
200 OK
Error Responses
Status Code	Description
400	Document is not in ACTIVE status
401	Unauthorized
403	Forbidden
404	Document not found
Data Integrity Protection
The system automatically resolves data integrity violations. If multiple active documents are detected for the same name (which should not occur under normal operation), all conflicting active documents are automatically set to OUTDATED status to maintain system consistency.

Integrity Rules
Rule	Description	Enforcement
Unique active per name	Maximum 1 active document per document name	Automatic on publish
Version uniqueness	Name + Version combination must be unique	Reject on create
Immutable after publish	Name, Version, File, SignatureRequired cannot change	Reject on update
No reactivation	Outdated documents cannot become active	Reject on publish
Draft-only edits	Only UNPUBLISHED documents can be modified	Reject on update
Document Versioning Workflow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Document Versioning Example                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Terms of Service Document Evolution:                                       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Version 1.0 (OUTDATED)                                              │   │
│  │ • Created: Jan 2024                                                 │   │
│  │ • Published: Jan 2024                                               │   │
│  │ • Status: OUTDATED (after v2.0 published)                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Version 2.0 (OUTDATED)                                              │   │
│  │ • Created: June 2024                                                │   │
│  │ • Published: June 2024                                              │   │
│  │ • Status: OUTDATED (after v3.0 published)                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Version 3.0 (ACTIVE)                                                │   │
│  │ • Created: Dec 2024                                                 │   │
│  │ • Published: Dec 2024                                               │   │
│  │ • Status: ACTIVE                                                    │   │
│  │ • SignatureRequired: true                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  When Version 4.0 is published:                                            │
│  • Version 3.0 automatically becomes OUTDATED                              │
│  • Version 4.0 becomes ACTIVE                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Document Name Examples
Document Name	Description	Typical Use
Terms of Service	Legal terms for platform usage	User acceptance
Privacy Policy	Data handling and privacy practices	Compliance (GDPR/CCPA)
Margin Agreement	Borrowing/lending terms	Trading accounts
KYC Consent	Identity verification consent	User onboarding
Risk Disclosure	Investment risk acknowledgment	Trading accounts
Electronic Consent	E-signature agreement	All signatures
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
DOCUMENT_STORE	Document store endpoint	github.com/sologenic/com-fs-document-model
ACCOUNT_STORE	Admin account store endpoint	github.com/sologenic/com-fs-admin-account-model
ROLE_STORE	Role store endpoint	github.com/sologenic/com-fs-role-model
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model
FILE_STORE	File store endpoint	github.com/sologenic/com-fs-file-model
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-store
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
Base64 Filter Encoding Examples
Example 1: Basic Filter
json
{
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Limit": 100
}
Base64 encoded:

text
ewogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJMaW1pdCI6IDEwMAp9
Example 2: Filter with Status
json
{
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Status": 2,
  "Limit": 50,
  "Offset": 0
}
Base64 encoded:

text
ewogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJTdGF0dXMiOiAyLAogICJMaW1pdCI6IDUwLAogICJPZmZzZXQiOiAwCn0=
Example 3: Filter by Name
json
{
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Name": "Terms of Service",
  "SignatureRequired": true
}
Base64 encoded:

text
ewogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJOYW1lIjogIlRlcm1zIG9mIFNlcnZpY2UiLAogICJTaWduYXR1cmVSZXF1aXJlZCI6IHRydWUKfQ==
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
  "message": "Document with same Name and Version already exists",
  "details": "Name: Terms of Service, Version: 1.0.0"
}
Conflict (409)
json
{
  "error": "Conflict",
  "message": "Document cannot be modified",
  "details": "Document is not in UNPUBLISHED status"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Document not found",
  "details": "No document found with Name: Terms of Service, Version: 1.0.0"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Cannot update document	Document is not in UNPUBLISHED status	Only drafts can be updated
Cannot change file	File is immutable after creation	Create a new version instead
Publish fails	No changes detected or invalid status	Ensure document is in UNPUBLISHED status
Duplicate document	Name + Version combination exists	Use a different version number
Signature requirement stuck	Document is already published	Create new version with desired setting
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check document status before operations:

bash
# List documents to check status
GET /api/admindoc/list?filter=<base64_filter>
Best Practices
Version Management
Semantic Versioning: Use semantic versioning (MAJOR.MINOR.PATCH) for clarity

Increment Appropriately:

MAJOR: Incompatible/breaking changes

MINOR: Backward-compatible additions

PATCH: Bug fixes

Document Changes: Keep descriptions updated with change summaries

Publishing Workflow
Draft Creation: Create draft with all required fields

Review: Review document content and metadata

Test: Test in testnet environment first

Publish: Publish during low-traffic periods

Notify: Inform users of new document versions

Compliance
Retention: Keep outdated documents for audit purposes

Signatures: Set SignatureRequired=true for legal documents

Audit Trail: Monitor audit logs for document changes

Version History: Maintain clear version history for compliance

Related Services
Service	Description
Admin Account Service	User and role management
Admin Certificate Service	Certificate management
File Service	File storage
Organization Service	Organization management
KYC Service	Identity verification documents
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the admin document service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the admin document service section:

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

**Document Statuses:**
| Status | Description |
|--------|-------------|
| UNPUBLISHED (1) | Draft - editable, not yet published |
| ACTIVE (2) | Published - current, may require signatures |
| OUTDATED (3) | Archived - historical reference only |

**Key Features:**
- Create draft documents with temporary file storage
- Update draft metadata (description, signature requirement)
- Publish documents with automatic version outdating
- Mark active documents as outdated
- Filter documents by name, status, signature requirement
- Automatic data integrity protection
- One active version per document name

**Immutable Fields (after creation):**
- Name
- Version
- File
- SignatureRequired (after publish)

**Quick Examples:**
```bash
# List documents
GET /api/admindoc/list?filter=<base64_filter>

# Create draft
POST /api/admindoc/create/draft

# Update draft
PUT /api/admindoc/update/draft

# Publish document
PUT /api/admindoc/publish

# Mark as outdated
PUT /api/admindoc/outdated
Account Types:

Sologenic Administrator (Platform level)

Organization Administrator (Organization level)

KYC Administrator

Broker Asset Administrator

Normal User (End User)

