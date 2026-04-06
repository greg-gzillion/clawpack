# Admin File Service

The File Service provides RESTful and gRPC interfaces for file upload, temporary storage, and permanent commit operations. It handles file management with automatic garbage collection for temporary files.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ File Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├─────────────────────┬─────────────────────────────────────────────┤ │
│ │ POST /upload │ GET /exist │ │
│ │ (Temporary upload) │ (Check existence) │ │
│ └─────────────────────┴─────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ gRPC Interface │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ Commit - Move temp file to permanent location │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Google Cloud Storage │ │
│ ├───────────────────────────────┬─────────────────────────────────────┤ │
│ │ Temporary Bucket │ Permanent Bucket │ │
│ │ • 30-day TTL │ • Configurable retention │ │
│ │ • Auto-cleanup │ • Public access configurable │ │
│ │ • Unique filenames │ • Organized by path │ │
│ └───────────────────────────────┴─────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## File Naming and Path Structure

### Temporary Files

Temporary filenames are made unique by the file service by pre-pending:
- Address of uploader (account ID)
- Network (mainnet, testnet, devnet)

Format: `{address}_{network}_{original_filename}_{timestamp}`

### Committed Files

Committed (final) files are uniquely managed by a naming schema from the requesting application. The `PathBuilder` from `com-fs-utils-lib/go/storage` package should be used.

## Garbage Collection

The cloud-based temp folder has automatic garbage collection:

| Property | Value |
|----------|-------|
| TTL (Time To Live) | 30 days after creation |
| Cleanup Method | Google Cloud Storage lifecycle rule |
| Expected processing time | Seconds to minutes |
| 99th percentile | 24 hours |
| 99.99th percentile | 5 days |

**Note:** If a user aborts a process where files are to be permanently kept, no cleanup is required as garbage is automatically managed.

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| POST /api/adminfile/upload | ORGANIZATION_ADMINISTRATOR | Upload temporary file |
| GET /api/adminfile/exist | ORGANIZATION_ADMINISTRATOR | Check file existence |
| Commit (gRPC) | ORGANIZATION_ADMINISTRATOR | Commit temp file to permanent storage |

**Note:** All authenticated requests must include `Network`, `OrganizationID`, and `Authorization` in the header.

## REST API Endpoints

### POST /api/adminfile/upload

Uploads a file to the temporary location in the storage. Returns a temporary filename in base64. This temp filename must be included in the commit request as `TempFilename` param and in the `filename` URL query for calling the download endpoint.

#### Important Notes

- Content-Type must be `multipart/form-data`
- Multiple attachments are **NOT** allowed (single file per request)
- Temporary files are automatically deleted after 30 days

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | multipart/form-data | Yes |
| Network | mainnet, testnet, devnet | Yes |
| OrganizationID | Organization UUID | Yes |
| Authorization | Bearer <firebase_token> | Yes |
| address | Uploader's account address | Yes |

#### Request Body (multipart/form-data)

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| file | file | File attachment to upload | Yes |

#### Response

```json
{
  "Filename": "eyJBZGRyZXNzIjoickw1NHd6a25VWHhxaUM4VHpzNm16TGkzUUpUdFg1dVZLNiIsIk5ldHdvcmsiOiJtYWlubmV0IiwiVGVtcEZpbGVuYW1lIjoiYnV0dGVyZmx5XzMwMC5qcGciLCJFeHRlcm5hbEtleXMiOlt7IktleSI6ImNvbGxlY3Rpb25faWQiLCJWYWx1ZSI6InJFeXpwS3V2MXRnQVRFNkZadmdvYVh0Z3VYTU1qV3lxYlIifSx7IktleSI6Im5mdF91aWQiLCJWYWx1ZSI6IjQxMDQ0NmU1LWU1OWUtNDU3My1hN2QyLWIyYmY3NjIyNzc1YiJ9XX0="
}
The Filename is a base64 encoded string containing:

Address (uploader's address)

Network

TempFilename (temporary filename)

ExternalKeys (optional metadata)

Example Request
bash
curl --location 'https://api.admin.sologenic.org/api/adminfile/upload' \
  --header 'address: rL54wzknUXxqiC8Tzs6mzLi3QJTtX5uVK6' \
  --header 'Content-Type: multipart/form-data' \
  --header 'Authorization: Bearer <token>' \
  --header 'Network: mainnet' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --form 'file=@"/Users/username/Downloads/document.pdf"'
Error Responses
Status Code	Description
400	Bad request - Invalid form data or missing file
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
413	Payload too large - File exceeds size limit
500	Internal server error
GET /api/adminfile/exist
Checks if a file exists in the storage. Returns true if found by filename.

Query Parameters
Parameter	Type	Description	Required	Default
filename	string	Base64 encoded filename	Yes	-
committed	boolean	Check committed file (permanent location)	No	false
Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
address	Uploader's account address	Yes
Response
json
{
  "Exist": true
}
Example Request
bash
# Check temporary file (committed=false or omitted)
curl --location 'https://api.admin.sologenic.org/api/adminfile/exist?filename=bmZ0L3JFeXpwS3V2MXRnQVRFNkZadmdvYVh0Z3VYTU1qV3lxYlIvNDEwNDQ2ZTUtZTU5ZS00NTczLWE3ZDItYjJiZjc2MjI3NzVi' \
  --header 'address: rL54wzknUXxqiC8Tzs6mzLi3QJTtX5uVK6' \
  --header 'Authorization: Bearer <token>' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --header 'Network: mainnet'

# Check committed file
curl --location 'https://api.admin.sologenic.org/api/adminfile/exist?filename=bmZ0L3JFeXpwS3V2MXRnQVRFNkZadmdvYVh0Z3VYTU1qV3lxYlIvNDEwNDQ2ZTUtZTU5ZS00NTczLWE3ZDItYjJiZjc2MjI3NzVi&committed=true' \
  --header 'address: rL54wzknUXxqiC8Tzs6mzLi3QJTtX5uVK6' \
  --header 'Authorization: Bearer <token>' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --header 'Network: mainnet'
Error Responses
Status Code	Description
400	Bad request - Missing filename parameter
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
500	Internal server error
gRPC Service
Commit
Moves an uploaded temporary file to the permanent location in the cloud storage with the final name.

Behavior
If the temporary file is not found (TTL expired, already committed, or never existed), returns FileFound: false

Client is responsible for re-uploading the file and committing again

The AllowOverwrite flag controls whether to overwrite an existing file at the permanent location

Request Parameters
Parameter	Type	Description	Required
TempFileName	string	Temp filename from upload response (must be identical)	Yes
PermanentPath	string	Base64 string of permanent path including final filename	Yes
AllowOverwrite	boolean	Whether to overwrite if PermanentPath already exists	Yes
Network	string	"mainnet", "testnet", or "devnet"	Yes
PermanentPath Format
Decoded string format:

text
{app}/{first_level_dir}/{second_level_dir}/.../{final_filename}
Example:

text
nft/collection_id/nft_id/document.pdf
Response
Field	Type	Description
FileFound	boolean	Whether the temp filename was found in storage
PublicURL	string	Publicly accessible link (if storage configured for public access)
Network	string	"mainnet", "testnet", or "devnet"
Example gRPC Call (Conceptual)
protobuf
service FileService {
  rpc Commit(CommitRequest) returns (CommitResponse);
}

message CommitRequest {
  string TempFileName = 1;
  string PermanentPath = 2;  // base64 encoded
  bool AllowOverwrite = 3;
  string Network = 4;
}

message CommitResponse {
  bool FileFound = 1;
  string PublicURL = 2;
  string Network = 3;
}
File Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           File Lifecycle                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Upload                                                                │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Temporary Bucket                                                     │   │
│  │ • Unique filename (address_network_timestamp)                        │   │
│  │ • 30-day TTL                                                         │   │
│  │ • Auto-delete after 30 days                                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│       │                                                                     │
│       ├─────────────────────────────────────┐                              │
│       │                                     │                              │
│       │ Commit within 30 days               │ No commit (abandoned)        │
│       ▼                                     ▼                              │
│  ┌──────────────────────────────┐    ┌──────────────────────────────┐     │
│  │ Permanent Bucket             │    │ Auto-deleted after 30 days    │     │
│  │ • Organized by path          │    │ (No cleanup required)         │     │
│  │ • Configurable retention     │    └──────────────────────────────┘     │
│  │ • Public URL available       │                                          │
│  └──────────────────────────────┘                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
GCS Bucket Configuration
Temporary Bucket Setup
The temp bucket has a lifecycle rule that deletes files after 30 days.

Step-by-Step Configuration
Create bucket

Single region (no high availability required - lowest cost)

Standard class

Uniform access control

Set access

All data is public (but hashed filenames make guessing nearly impossible)

Similar security level to ledger secret keys

Protection

None - data loss is acceptable (user can re-upload)

No extra encryption required (data is public by design)

Public access

Uncheck "Enforce public access prevention on this bucket"

(Bucket is publicly accessible as a just-in-case measure)

Permissions

Click on bucket → Permissions → Grant access

Enter allUsers in New Principals field

Select Cloud Storage → Storage object viewer in Select a role field

Save → Confirm Allow public access

Lifecycle rule

Select Lifecycle → Add a rule

Select Delete object → Continue

Select Age → Enter 30 in Days

Click Continue → Create

Result: Rule stating: Delete object 30+ days since object was created

Request Body Size Configuration
The application uses nginx as an Ingress controller. Default request body size is 1MB.

Increase Request Body Size
Add the following configuration to the file-service deployment file (file-service.yaml.erb):

yaml
ingress:
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: 100m  # Sets request body size to 100MB
Start Parameters
Required Environment Variables
Environment Variable	Description
PROJECT_ID	Google Cloud project ID
CREDENTIALS_LOCATION	Google Cloud credentials location
HTTP_CONFIG	HTTP server configuration
AUTH_FIREBASE_SERVICE	Firebase authentication service endpoint
ROLE_STORE	Role store endpoint
Source References
Component	Source
HTTP_CONFIG	github.com/sologenic/com-be-http-lib/
ROLE_STORE	github.com/sologenic/com-fs-role-model/
AUTH_FIREBASE_SERVICE	github.com/sologenic/com-fs-auth-firebase-service/
PathBuilder	github.com/sologenic/com-fs-utils-lib/go/storage
Testing
Run Testing Frontend
To run the testing frontend, execute the following command in the app's root folder:

bash
./bin/test.sh
Then open localhost:3000 in the browser.

Note: The PermanentFileName input should be in plain text (e.g., test1/test11/test111), not base64 encoded. The testing FE encodes it automatically.

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
  "message": "Missing file attachment",
  "details": "No file found in multipart form data"
}
Payload Too Large (413)
json
{
  "error": "Payload Too Large",
  "message": "File exceeds maximum allowed size",
  "details": "Max size: 100MB"
}
Not Found (404) - Commit
json
{
  "FileFound": false,
  "PublicURL": "",
  "Network": "mainnet"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
File not found on commit	TTL expired (30 days)	Re-upload file and commit
Upload fails (413)	File too large	Increase proxy-body-size or reduce file size
Permission denied	Missing/invalid token	Verify Firebase token and role
File not found on exist check	Wrong committed flag	Set committed=true for permanent files
Temp file not unique	Naming collision	System pre-pends address & network for uniqueness
Debugging
Check file existence:

bash
# Check temp file
curl -X GET /api/adminfile/exist?filename=<base64_filename>

# Check committed file
curl -X GET /api/adminfile/exist?filename=<base64_filename>&committed=true
Verify upload response includes valid Filename:

json
{
  "Filename": "base64_encoded_string"
}
Best Practices
File Upload
Always commit within 30 days - Temporary files auto-delete after TTL

Store the temp filename - Required for commit and exist checks

Use PathBuilder - For consistent permanent path construction

Set AllowOverwrite carefully - Set to false when uncertain

Path Organization
Recommended path structure:

text
{app_name}/{entity_type}/{entity_id}/{document_type}/{version}/{filename}
Examples:

nft/collection_123/nft_456/image.png

kyc/user_789/id_document.pdf

asset/asset_123/prospectus_v2.pdf

Error Handling
Check FileFound after commit - If false, re-upload and retry

Handle TTL expiration - Implement retry logic for expired temp files

Validate file size - Check against configured limits before upload

Related Services
Service	Description
Admin Document Service	Document management with file storage
Admin Certificate Service	Certificate file storage
KYC Service	KYC document file uploads
Asset Service	Asset image and document files
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the file service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the file service section:

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

**Key Features:**
- Upload files to temporary storage (30-day TTL)
- Check file existence (temporary or committed)
- Commit temporary files to permanent storage (gRPC)
- Automatic garbage collection for temp files
- Public URL generation for committed files

**File Lifecycle:**
| Stage | Location | TTL | Access |
|-------|----------|-----|--------|
| Upload | Temporary bucket | 30 days | Temporary filename |
| Commit | Permanent bucket | Configurable | Public URL |

**Quick Examples:**
```bash
# Upload file
POST /api/adminfile/upload
Content-Type: multipart/form-data
file: @document.pdf

# Check existence
GET /api/adminfile/exist?filename=<base64_filename>

# Commit (gRPC)
Commit(TempFileName, PermanentPath, AllowOverwrite)
Account Types:

Sologenic Administrator (Platform level)

Organization Administrator (Organization level)

KYC Administrator

Broker Asset Administrator

Normal User (End User)
