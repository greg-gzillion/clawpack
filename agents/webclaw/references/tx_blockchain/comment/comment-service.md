# Comment Service

The Comment Service provides generic functionality to attach comments to any source type defined in `github.com/sologenic/com-fs-notification-model`. This provides consistency between what can be commented and source types used for rendering content. Essentially, the source types represent the different functions of the system.

Beyond adding comments to a source type, the Comment Service also supports adding comments to other comments, enabling threaded discussions.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Comment Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Public Endpoints (Unauthenticated) │ │
│ ├─────────────────────────┬───────────────────────────────────────────┤ │
│ │ GET /get │ GET /count │ │
│ │ (List comments) │ (Count comments) │ │
│ └─────────────────────────┴───────────────────────────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Authenticated Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ GET /auth/get │ POST /auth/add│ DELETE /auth/ │ PUT /auth/close │ │
│ │ │ │ delete │ │ │
│ │ │ │ │ PUT /auth/new-reply │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Comment Store │ User Store │ Role Store │ File Store │ │
│ │ │ │ │ │ │
│ │ Organization │ Auth Firebase │ Feature Flag │ │ │
│ │ Store │ Service │ Store │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Asynchronous Processing │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Deletion Processing (cascade, rebase) │ │
│ │ • Reporting Processing │ │
│ │ • Reputation Updates │ │
│ │ • Notification Triggers │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Source Types

Source types define what kind of object a comment is attached to. These come from `com-fs-notification-model`.

| Source Type ID | Source Type Name | Description | Sensitive |
|----------------|------------------|-------------|-----------|
| 1 | COMMENT_ID | Reply to another comment | No |
| 2 | ASSET | Asset comment | No |
| 3 | NFT | NFT comment | No |
| 4 | SUPPORT_TICKET | Support ticket comment | **Yes** |
| 5 | ORDER | Order comment | **Yes** |
| 6 | TRANSACTION | Transaction comment | **Yes** |
| 7 | USER_PROFILE | User profile comment | No |
| 8 | ORGANIZATION | Organization comment | No |

**Important for Maintainers:** When adding new sensitive source types to the system, you MUST update the `sensitiveSourceTypes` variable in `comment.go` to include these types in the security check.

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/comment/get | None (Public) | List public comments |
| GET /api/comment/count | None (Public) | Count comments |
| GET /api/comment/auth/get | NORMAL_USER | List user's comments (including sensitive) |
| POST /api/comment/auth/add | NORMAL_USER | Add comment |
| DELETE /api/comment/auth/delete | NORMAL_USER | Delete own comment |
| PUT /api/comment/auth/close | NORMAL_USER | Close comment |
| PUT /api/comment/auth/new-reply | NORMAL_USER | Mark for admin attention |

**Note:** 
- Unauthenticated endpoints will be used for public comments visible to all users
- Sensitive source types (such as support tickets) are automatically blocked in unauthenticated endpoints
- Authenticated requests must include `Network`, `OrganizationID`, and `Authorization` headers
- Users can only access and modify their own comments
- Admin operations are handled through separate service (`com-be-admin-comment-service`)

## Data Models

### Comment Object

| Field | Type | Description |
|-------|------|-------------|
| CommentID | string | Unique comment identifier (UUID) |
| AccountID | string | User account ID who created the comment |
| MetaData | MetaData | Creation/update timestamps and network |
| Source | string | ID of the source object |
| SourceType | int | Type of source (see Source Types) |
| Content | string | Comment content (may contain media links) |
| Root | string | ID of the root object (for threaded comments) |
| RootType | int | Type of the root object |
| OrganizationID | string | Organization UUID |
| Tags | []string | Categorization tags |
| Files | []File | Attached files |
| Status | int | Comment status (see Status Values) |
| DeletionAccount | string | Account that deleted the comment |

### MetaData Object

| Field | Type | Description |
|-------|------|-------------|
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |

### File Object

| Field | Type | Description |
|-------|------|-------------|
| Reference | string | File reference ID (from file service) |
| Extension | string | MIME type or file extension |
| Name | string | Original file name |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

### Comment Status Values

| Status ID | Status Name | Description |
|-----------|-------------|-------------|
| 1 | ACTIVE | Normal active comment |
| 2 | REPORTED | Comment has been reported |
| 3 | REVIEWED | Comment has been reviewed (closed) |
| 4 | NEW_REPLY | Support ticket needs admin attention |
| 5 | DELETED | Soft-deleted comment |
| 6 | DELETED_CASCADE | Deleted with cascade (replies also deleted) |

### Order Values

| Order ID | Order Name | Description |
|----------|------------|-------------|
| 1 | NEWEST_FIRST | Sort by creation date descending |
| 2 | OLDEST_FIRST | Sort by creation date ascending |
| 3 | MOST_REPLIES | Sort by reply count descending |

### Network Values

| Network ID | Network Name | Description |
|------------|--------------|-------------|
| 1 | mainnet | Production network |
| 2 | testnet | Testing network |
| 3 | devnet | Development network |

## Public Endpoints (Unauthenticated)

### GET /api/comment/get

Lists comments based on query parameters. This endpoint is for public comments visible to all users. Sensitive source types are automatically blocked.

#### Query Parameters

The endpoint accepts the following query parameter combinations (4 variants only):

| Variant | Parameters | Description |
|---------|------------|-------------|
| 1 | source_type, order | All comments for a source type |
| 2 | source_type, source, order | Comments for specific source |
| 3 | account_id, order | Comments by specific account |
| 4 | comment_ids | Specific comments by IDs |

**Important:** Other combinations are not allowed and may lead to unexpected results. The backend checks are not strict - the first matching parameter determines the query.

**Order is optional** (default: NEWEST_FIRST)

#### Example Requests

```bash
# Get comments for source type
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -X GET "https://api.sologenic.org/api/comment/get?source_type=2&source=1234ABCD&order=1"

# Get all comments for source type
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -X GET "https://api.sologenic.org/api/comment/get?source_type=2&order=1"

# Get comments by account
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -X GET "https://api.sologenic.org/api/comment/get?account_id=user@example.com&order=1"

# Get specific comments (base64 encoded IDs)
# comment_ids = base64([12345, 123456, 1234567])
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -X GET "https://api.sologenic.org/api/comment/get?comment_ids=WzEyMzQ1LDEyMzQ1NiwxMjM0NTY3XQo="
Success Response
json
{
  "Offset": 1,
  "CommentResult": [
    {
      "Comments": [
        {
          "CommentID": "62e3f1fc-fc12-45c6-982b-4455934a02ef",
          "Account": "rhozSjrMoVBV8PuQAdyLro2FEF2uVBPfzw",
          "Network": 1,
          "Source": "1",
          "SourceType": 2,
          "CreatedAt": {
            "seconds": 1686172948,
            "nanos": 555295000
          },
          "UpdatedAt": {
            "seconds": 1686172948,
            "nanos": 555298000
          },
          "Content": "This is a comment",
          "Status": 1
        },
        {
          "CommentID": "72e3f1fc-fc12-45c6-982b-4455934a02ef",
          "Account": "rhozSjrMoVBV8PuQAdyLro2FEF2uVBPfzw",
          "Network": 1,
          "Source": "1",
          "SourceType": 2,
          "CreatedAt": {
            "seconds": 1686173092,
            "nanos": 411150000
          },
          "UpdatedAt": {
            "seconds": 1686173092,
            "nanos": 411151000
          },
          "Content": "This is another comment",
          "Status": 1
        }
      ]
    }
  ]
}
Note: Comments marked for deletion or reported are still visible in results. Deletion and reporting are processed asynchronously. Once complete, comments are removed from the result set.

Error Responses
Status Code	Error Code	Description
500	ACCOUNT PARAM INVALID	Invalid account parameter
500	NETWORK PARAM INVALID	Invalid network parameter
500	COMMENT_IDS PARAM INVALID	Invalid comment_ids format
500	SOURCE_TYPE PARAM INVALID	Invalid source_type parameter
500	ORDER PARAM INVALID	Invalid order parameter
500	INVALID COMBINATION OF PARAMS	Unsupported parameter combination
GET /api/comment/count
Counts comments based on query parameters.

Query Parameter Combinations
Variant	Parameters	Description
1	source_type, source	Count comments for specific source
2	source_type	Count comments for source type
3	account_id	Count comments by account
4	comment_ids	Count sub-comments (max 20 IDs, base64 encoded)
Example Requests
bash
# Count comments for source
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -X GET "https://api.sologenic.org/api/comment/count?source_type=2&source=12345"

# Count comments by account
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -X GET "https://api.sologenic.org/api/comment/count?account_id=user@example.com"

# Count sub-comments (base64 encoded comment IDs array)
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -X GET "https://api.sologenic.org/api/comment/count?comment_ids=WzEyMzQ1LDEyMzQ1Nl0="
Success Response
json
{
  "Counts": [{}]
}
The actual count is returned in the response structure.

Error Responses
Status Code	Error Code	Description
500	NETWORK PARAM INVALID	Invalid network parameter
500	SOURCE_TYPE PARAM INVALID	Invalid source_type parameter
Authenticated Endpoints
GET /api/comment/auth/get
Lists comments for authenticated users. Supports the same four query patterns as the public endpoint, but authenticated users can access their own sensitive content (like support tickets).

Headers
Header	Description	Required
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Same as public GET endpoint.

Example Request
bash
curl -H "Network: testnet" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -X GET "https://api.sologenic.org/api/comment/auth/get?source_type=4&order=1"
Success Response
json
{
  "Offset": 1,
  "CommentResult": [
    {
      "Comments": [
        {
          "CommentID": "62e3f1fc-fc12-45c6-982b-4455934a02ef",
          "AccountID": "user@example.com",
          "MetaData": {
            "Network": 2,
            "UpdatedAt": {
              "seconds": 1742502788,
              "nanos": 274733605
            },
            "CreatedAt": {
              "seconds": 1742502788,
              "nanos": 250151933
            }
          },
          "Source": "04f51a34-fbe8-4d02-97f7-8a4be2d4c4dc",
          "SourceType": 4,
          "Content": "Test support ticket comment",
          "Root": "04f51a34-fbe8-4d02-97f7-8a4be2d4c4dc",
          "RootType": 4,
          "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
          "Tags": ["Account issue"],
          "Files": [
            {
              "Reference": "7a39bf30-3b1c-4538-94ed-f76210b7c973",
              "Extension": "image/png",
              "Name": "Screenshot.png"
            }
          ],
          "Status": 1
        }
      ]
    }
  ]
}
Error Responses
Same as public GET endpoint plus authentication errors (401).

POST /api/comment/auth/add
Adds a new comment to a source type or as a reply to another comment.

Headers
Header	Description	Required
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Content-Type	application/json	Yes
Request Body (Root Comment)
Field	Type	Description	Required
SourceType	int	Type of source (from Source Types)	Yes
Source	string	ID of the source object	Yes
Content	string	Comment content	Yes
Tags	[]string	Categorization tags	No
Files	[]File	Attached files	No
Example Request (Root Comment)
bash
curl -H "Network: testnet" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "SourceType": 4,
    "Source": "12345",
    "Content": "This is a support ticket comment",
    "Tags": ["payment", "urgent"],
    "Files": [
      {
        "Reference": "a5dd1be5-b93a-46fc-98e0-0c20f64955f1",
        "Extension": "image/png",
        "Name": "Screenshot.png"
      }
    ]
  }' \
  -X POST "https://api.sologenic.org/api/comment/auth/add"
Request Body (Reply to Comment)
For replying to an existing comment, additional fields are required:

Field	Type	Description	Required
SourceType	int	Must be 1 (COMMENT_ID)	Yes
Source	string	ID of the parent comment	Yes
RootType	int	Type of the root object	Yes
Root	string	ID of the root object	Yes
Content	string	Comment content	Yes
Note: The backend adds RootType and Root to ensure the comment is added to the correct object and prevent cross-commenting hacks.

Example Request (Reply to Comment)
bash
# Adding a reply to comment ID 1234567890, which is a comment on NFT ID 12345
curl -H "Network: testnet" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "SourceType": 1,
    "Source": "1234567890",
    "RootType": 3,
    "Root": "12345",
    "Content": "This is a reply to the comment"
  }' \
  -X POST "https://api.sologenic.org/api/comment/auth/add"
Success Response
text
200 OK
Error Responses
Status Code	Error Code	Description
401	UNAUTHORIZED	Invalid or missing token
500	ACCOUNT PARAM INVALID	Invalid account parameter
500	NETWORK PARAM INVALID	Invalid network parameter
500	SOURCE TYPE INVALID	Invalid source type
500	COMMENT INVALID	Empty comment or source
json
{
  "errors": [
    {
      "name": "account.invalid"
    }
  ]
}
DELETE /api/comment/auth/delete
Deletes a comment. Only the owner of the comment can delete it. The system verifies ownership by checking that the account ID matches.

Deletion Behavior
The service only sets the state of the comment to DELETED or DELETED_CASCADE. Asynchronous processes handle:

Removing the comment from the database

Updating counts

Adjusting reputation

Sending notifications

Cascading Delete Rules
Scenario	Behavior
User owns comment, has replies	Can choose to delete replies or keep them (rebase)
User owns root object	Cascading delete executed for all comments
User does not own root object	Cascading delete ignored
User does not own comment or root	Delete ignored
Request Body
Field	Type	Description	Required
CommentID	string	UUID of comment to delete	Yes
KeepReplies	bool	If true, replies are rebased to parent	No (default: false)
Rebase Behavior:

KeepReplies: true - Replies are moved up one level (attached to parent of deleted comment)

KeepReplies: false - All replies are also deleted (cascade)

Example Request
bash
curl -H "Network: testnet" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "CommentID": "62e3f1fc-fc12-45c6-982b-4455934a02ef",
    "KeepReplies": true
  }' \
  -X DELETE "https://api.sologenic.org/api/comment/auth/delete"
Success Response
text
200 OK
Note: Success is returned in virtually all scenarios (including invalid CommentID) to prevent enumeration attacks.

Error Responses
Status Code	Error Code	Description
401	UNAUTHORIZED	Invalid or missing token
500	ACCOUNT PARAM INVALID	Invalid account parameter
500	NETWORK PARAM INVALID	Invalid network parameter
500	COMBINATION OF PARAMETERS INVALID	Invalid request parameters
500	DELETE IN PROGRESS	Deletion already in progress
PUT /api/comment/auth/close
Closes a comment. Hardcodes the status to REVIEWED (3). A user cannot reopen a comment once it is closed.

Request Body
Field	Type	Description	Required
CommentID	string	UUID of comment to close	Yes
Example Request
bash
curl -H "Network: testnet" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{"CommentID": "62e3f1fc-fc12-45c6-982b-4455934a02ef"}' \
  -X PUT "https://api.sologenic.org/api/comment/auth/close"
Success Response
text
200 OK
PUT /api/comment/auth/new-reply
Sets the status of a comment to NEW_REPLY (4) to signal that a support ticket needs further admin attention after receiving a reply. Used in the support ticket system.

Request Body
Field	Type	Description	Required
CommentID	string	UUID of comment to mark	Yes
Example Request
bash
curl -H "Network: testnet" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{"CommentID": "62e3f1fc-fc12-45c6-982b-4455934a02ef"}' \
  -X PUT "https://api.sologenic.org/api/comment/auth/new-reply"
Success Response
text
200 OK
Threaded Discussion Structure
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Threaded Discussion Structure                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Root Object (NFT ID: 12345)                                                │
│  SourceType: 3 (NFT), Source: "12345"                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Comment A (Root)                                                     │   │
│  │ • SourceType: 3, Source: "12345"                                     │   │
│  │ • RootType: 3, Root: "12345"                                         │   │
│  │ • Status: ACTIVE                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Reply to Comment A                                                   │   │
│  │ • SourceType: 1 (COMMENT_ID)                                         │   │
│  │ • Source: "comment-a-uuid"                                           │   │
│  │ • RootType: 3, Root: "12345"                                         │   │
│  │ • Status: ACTIVE                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Reply to Reply                                                       │   │
│  │ • SourceType: 1 (COMMENT_ID)                                         │   │
│  │ • Source: "reply-1-uuid"                                             │   │
│  │ • RootType: 3, Root: "12345"                                         │   │
│  │ • Status: ACTIVE                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Count all comments on NFT 12345: Query WHERE RootType=3 AND Root="12345"  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Pagination
All list-style endpoints (multiple results) support pagination with an offset returned in the response.

Pagination Response Format
json
{
  "Offset": 1,
  "CommentResult": [...]
}
Offset present - More data available, use this offset in next request

Offset absent - No more data to retrieve

Using Offset
bash
# First page
GET /api/comment/get?source_type=2&offset=0

# Second page (using offset from response)
GET /api/comment/get?source_type=2&offset=1
Empty Database Note
Important: GET/COUNT does not work against an empty database due to lack of any model for the database to reference. Add at least 1 comment into the system using wget/curl to avoid this empty database error (easier than catching it everywhere for a 10-second situation only at launch).

bash
# Add initial comment to bootstrap the system
curl -X POST "https://api.sologenic.org/api/comment/auth/add" \
  -H "Authorization: Bearer: ..." \
  -H "Network: testnet" \
  -H "OrganizationID: ..." \
  -d '{
    "SourceType": 2,
    "Source": "bootstrap",
    "Content": "Initial comment for database initialization"
  }'
Asynchronous Processing
Deletion Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Asynchronous Deletion Flow                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Request: DELETE /api/comment/auth/delete                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ • Validate ownership                                                 │   │
│  │ • Set status to DELETED or DELETED_CASCADE                           │   │
│  │ • Return 200 OK immediately                                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Trigger Topic Event                                                  │   │
│  │ • Comment deletion event published                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Asynchronous Processing                                              │   │
│  │ • Remove comment from database                                       │   │
│  │ • Update comment counts for affected objects                         │   │
│  │ • Adjust user reputation (if applicable)                             │   │
│  │ • Send notifications to relevant parties                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Content Guidelines
Content Format
The Content field is agnostic of language and can contain various content types:

Content Type	Format Example
Plain text	"This is a comment"
Markdown	"Bold text and italic"
Image links	"/uploads/image-123.png"
Video links	"/uploads/video-456.mp4"
Important: Media files must be uploaded separately via com-be-file-service, with the resulting links included in the Content field (excluding domain to prevent external linking).

File Attachments
Files are attached using the Files array:

json
{
  "Files": [
    {
      "Reference": "file-reference-uuid",
      "Extension": "image/png",
      "Name": "screenshot.png"
    }
  ]
}
The actual file content is managed by the File Service.

Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/http/
COMMENT_STORE	Comment service endpoint	github.com/sologenic/com-fs-comment-model
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
USER_STORE	User management service	github.com/sologenic/com-fs-user-model
ROLE_STORE	Role management service	github.com/sologenic/com-fs-role-model
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-model
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model
FILE_STORE	File service endpoint	github.com/sologenic/com-fs-file-model
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
PAGE_SIZE	Default page size for list endpoints	20
MAX_PAGE_SIZE	Maximum page size allowed	100
Example Environment Configuration
bash
# Required
COMMENT_STORE=localhost:50052
AUTH_FIREBASE_SERVICE=localhost:50070
USER_STORE=localhost:50049
ROLE_STORE=localhost:50066
ORGANIZATION_STORE=localhost:50060
FEATURE_FLAG_STORE=localhost:50055
FILE_STORE=localhost:50054

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
Error Responses
Unauthorized (401)
json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
Forbidden (403) - Sensitive Source Type
json
{
  "error": "Forbidden",
  "message": "Access to sensitive source type requires authentication",
  "source_type": 4,
  "details": "Support tickets require authentication"
}
Bad Request (400) - Empty Comment
json
{
  "errors": [
    {
      "name": "comment.invalid",
      "message": "Comment content cannot be empty"
    }
  ]
}
Bad Request (400) - Invalid Source Type
json
{
  "errors": [
    {
      "name": "sourceType.invalid",
      "message": "Invalid source type",
      "allowed_values": [1, 2, 3, 4, 5, 6, 7, 8]
    }
  ]
}
Too Many Requests (429)
json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Please wait before making more requests.",
  "retry_after": 60
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Empty results	Empty database	Add initial comment to bootstrap
Sensitive content visible	Missing sensitiveSourceTypes update	Update comment.go with new source types
Delete not working	User doesn't own comment	Verify ownership or use admin service
Missing file attachments	File not uploaded to file service	Upload file before creating comment
Comment count mismatch	Async processing delay	Wait for async processing to complete
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check comment existence:

bash
curl -X GET "/api/comment/get?comment_ids=$(echo -n '["comment-uuid"]' | base64)" \
  -H "Network: testnet"
Test comment creation:

bash
curl -X POST "/api/comment/auth/add" \
  -H "Authorization: Bearer: <token>" \
  -H "Network: testnet" \
  -H "OrganizationID: <org-id>" \
  -d '{"SourceType": 2, "Source": "test", "Content": "Test comment"}'
Best Practices
Comment Creation
Validate Content: Ensure content is not empty and properly formatted

Upload Files First: Always upload files to file service before creating comment

Use Tags: Add relevant tags for categorization (especially for support tickets)

Thread Properly: Use RootType and Root when replying to comments

Moderation
Async Deletion: Don't expect immediate removal from result sets

Cascade Carefully: Use KeepReplies=true to preserve discussion context

Respect Ownership: Only owners can delete their comments

Sensitive Types: Always authenticate for sensitive source types

Performance
Scenario	Recommendation
Large comment threads	Use pagination (offset)
Many replies	Use comment_ids for specific queries
Real-time updates	Subscribe to notification triggers
Bulk operations	Use admin comment service
Security
Validate Source Types: Never trust client-supplied source types blindly

Update Sensitive List: Add new sensitive types to sensitiveSourceTypes

Ownership Checks: Always verify comment ownership before modifications

Rate Limiting: Implement rate limiting on add/delete endpoints

Related Services
Service	Description
Admin Comment Service	Admin operations (moderation, bulk actions)
File Service	File attachment management
Notification Service	Comment notifications
User Service	User reputation and profiles
Organization Service	Tenant isolation
License
This documentation is part of the TX Marketplace platform.
