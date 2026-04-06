# Admin Comment Service

The Admin Comment Service provides generic functionality to attach comments to any source type from the notification model (`github.com/sologenic/com-fs-notification-model`). This provides consistency between what can be commented and source types used for rendering content. The source types represent the different functions of the system.

The Admin Comment Service facilitates the management of the support system (chat and ticket) in the admin dashboard, as well as admin delete actions of comments. For general usage, `com-be-comment-service` is to be used.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin Comment Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ GET /get │ GET /count │ POST /add │ PUT /status │ │
│ │ │ │ │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Comment Store │ Account Store │ Role Store │ File Store │ │
│ │ Feature Flag │ Organization │ Auth Firebase │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Trigger Channel (Kafka) │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Remove uploads │ │
│ │ • Log deleted images (MD5) │ │
│ │ • Log deleted messages (MD5) │ │
│ │ • Adjust user reputation scores │ │
│ │ • Process cascading deletes │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Source Types

Source types define what kind of object a comment is attached to. These are defined in the notification model.

| Source Type ID | Source Type | Description |
|----------------|-------------|-------------|
| 1 | COMMENT_ID | Reply to another comment |
| 2 | ASSET_ID | Comment on an asset |
| 3 | ORDER_ID | Comment on an order |
| 4 | NFT_ID | Comment on an NFT |
| 5 | TRANSACTION_ID | Comment on a transaction |
| 6 | USER_ID | Comment on a user profile |
| 7 | TICKET_ID | Support ticket comment |
| 8 | ORGANIZATION_ID | Comment on an organization |
| 9 | KYC_ID | Comment on KYC submission |

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/admincomment/get | ORGANIZATION_ADMINISTRATOR | List comments with filters |
| GET /api/admincomment/count | ORGANIZATION_ADMINISTRATOR | Count comments |
| POST /api/admincomment/add | ORGANIZATION_ADMINISTRATOR | Add a comment or reply |
| PUT /api/admincomment/status | ORGANIZATION_ADMINISTRATOR | Update comment status |
| DELETE /api/admincomment/delete | ORGANIZATION_ADMINISTRATOR | Delete a comment |

**Note:** All authenticated requests must include `Network`, `OrganizationID`, and `Authorization` headers.

## Comment Status Enum

| Status ID | Status Name | Description |
|-----------|-------------|-------------|
| 0 | NOT_USED_STATUS | Unused/default status |
| 1 | NORMAL | Normal visible comment |
| 2 | REVIEWED | Admin has reviewed the comment |
| 3 | REVIEW_REQUESTED | Comment flagged for review |
| 4 | ADMIN_DELETED | Admin deleted the comment |
| 5 | ADMIN_DELETED_CASCADE | Admin deleted with cascade |
| 6 | DELETED | Deleted by user or moderator |
| 7 | DELETED_CASCADE | Deleted with all children |
| 8 | READ | Read by admin (for support tickets) |

## Reason Enum (for ADMIN_DELETED)

| Reason ID | Reason | Description |
|-----------|--------|-------------|
| 1 | INAPPROPRIATE_CONTENT | Vulgar or offensive content |
| 2 | SPAM | Promotional or repetitive content |
| 3 | HARASSMENT | Targeted harassment |
| 4 | HATE_SPEECH | Discriminatory content |
| 5 | MISINFORMATION | False or misleading information |
| 6 | COPYRIGHT_VIOLATION | Unauthorized copyrighted material |
| 7 | OTHER | Other violation |

## API Endpoints

### GET /api/admincomment/get

Lists comments by various filter criteria. Oldest comments are first so that the oldest not-processed comments get highest priority.

#### Query Parameters

The endpoint accepts the following query parameter combinations (order is optional for all):

| Combination | Parameters |
|-------------|------------|
| 1 | source_type, order |
| 2 | source, order |
| 3 | source_type, source, order |
| 4 | account, order |
| 5 | comment_ids, order |
| 6 | status, order |
| 7 | reporter, order |
| 8 | source_type, source |

**Note:** Other combinations are not allowed and can lead to unexpected results.

| Parameter | Type | Description |
|-----------|------|-------------|
| source_type | int | Source type ID (see Source Types) |
| source | string | ID of the source object |
| account | string | Account ID of the commenter |
| comment_ids | string | Base64 encoded array of comment IDs |
| status | int | Comment status filter |
| reporter | string | Account ID of the reporter |
| order | int | Sort order (1=ASC, 2=DESC) |
| offset | int | Pagination offset |

#### Query Priority Logic

If multiple parameters are provided, the query runs in this priority order:

1. If `source` is found → source query runs
2. Else if `account` is found → account query runs
3. Else if `comment_ids` is found → comment_ids query runs
4. Else → default query

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| OrganizationID | Organization UUID | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Example Requests

```bash
# List comments by account with descending order
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer <token>" \
  -X GET "https://api.admin.sologenic.org/api/admincomment/get?account=rhozSjrMoVBV8PuQAdyLro2FEF2uVBPfzw&order=2"

# List comments by base64 encoded comment IDs
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer <token>" \
  -X GET "https://api.admin.sologenic.org/api/admincomment/get?comment_ids=WzEyMzQ1LDEyMzQ1NiwxMjM0NTY3XQo="
Example Response
json
{
  "Offset": 1,
  "CommentResult": [
    {
      "Comments": [
        {
          "CommentID": "uuid-string-1234",
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
          "Status": 6,
          "DeletionAccount": "rhozSjrMoVBV8PuQAdyLro2FEF2uVBPfzw"
        },
        {
          "CommentID": "uuid-string-5678",
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
Note: Comments marked for deletion (or reported) are still visible in results. Deletion and reporting are processed asynchronously. Once completed, comments are or can be removed from the result set.

Error Responses
Error Code	Description
500 ACCOUNT PARAM INVALID	Invalid account parameter
500 NETWORK PARAM INVALID	Invalid network parameter
500 COMMENT_IDS PARAM INVALID	Invalid comment_ids format
500 SOURCE_TYPE PARAM INVALID	Invalid source_type
500 ORDER PARAM INVALID	Invalid order value
500 INVALID COMBINATION OF PARAMS	Unsupported parameter combination
GET /api/admincomment/count
Counts the number of comments based on filter criteria. Used primarily on single object pages to display total comment counts.

Query Parameters
Parameter	Type	Description	Required (at least one)
source_type	int	Source type ID	Yes (with source)
source	string	ID of the source object	Yes (with source_type)
account	string	Account ID of the commenter	No
comment_ids	string	Base64 encoded array of comment IDs	No
Example Requests
bash
# Count comments for a specific source
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer <token>" \
  -X GET "https://api.admin.sologenic.org/api/admincomment/count?source_type=4&source=12345"

# Count comments by account
curl -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Authorization: Bearer <token>" \
  -X GET "https://api.admin.sologenic.org/api/admincomment/count?account=rhozSjrMoVBV8PuQAdyLro2FEF2uVBPfzw"
Example Response
json
{
  "Counts": [42]
}
Error Responses
Error Code	Description
500 NETWORK PARAM INVALID	Invalid network parameter
500 SOURCE_TYPE PARAM INVALID	Invalid source_type parameter
POST /api/admincomment/add
Adds a new comment or a reply to an existing comment.

Request Body (Top-Level Comment)
Field	Type	Description	Required
SourceType	int	Source type ID (from notification model)	Yes
Source	string	ID of the source object	Yes
Content	string	Comment content with embedded image/video links (domain excluded)	Yes
Tags	[]string	Tags for categorization (e.g., ["Payment issue"])	No
Example Request (Top-Level Comment)
bash
curl -H "Network: mainnet" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "SourceType": 4,
    "Source": "12345",
    "Content": "This is a comment",
    "Tags": ["tag1", "tag2"]
  }' \
  -X POST "https://api.admin.sologenic.org/api/admincomment/add"
Request Body (Reply to Comment)
When adding a reply to an existing comment:

Field	Type	Description	Required
SourceType	int	Must be 1 (COMMENT_ID)	Yes
Source	string	ID of the comment being replied to	Yes
Content	string	Reply content	Yes
The backend automatically adds:

RootType: The type of the root object (e.g., COMMENT_ID, NFT_ID)

Root: The ID of the root object

Example Request (Reply to Comment)
bash
# Adding a reply to comment ID 1234567890 (which is a comment on an NFT with ID 12345)
curl -H "Network: mainnet" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "SourceType": 1,
    "Source": "1234567890",
    "Content": "This is a reply to the comment"
  }' \
  -X POST "https://api.admin.sologenic.org/api/admincomment/add"
Success Response
text
200 OK
Error Responses
Error Code	Description
401 UNAUTHORIZED	Invalid or missing token
500 ACCOUNT PARAM INVALID	Invalid account
500 NETWORK PARAM INVALID	Invalid network
500 SOURCE TYPE INVALID	Invalid source type
500 COMMENT INVALID	Empty comment and/or empty source
json
{
  "errors": [
    {
      "name": "account.invalid"
    }
  ]
}
PUT /api/admincomment/status
Updates the status of a comment (read/unread, reviewed, admin deleted, etc.).

Request Body
Field	Type	Description	Required
CommentID	string	UUID of the comment	Yes
Status	int	Status enum value	Yes
Reason	int	Reason enum value (required for ADMIN_DELETED)	Conditional
Status Update Behavior
Status	Behavior
REVIEWED	Admin marks comment as reviewed. User's reporting score is adjusted.
ADMIN_DELETED	Admin deletes comment. Triggers async removal of uploads and logging.
ADMIN_DELETED_CASCADE	Admin deletes comment and all replies.
READ	Mark comment as read (for support tickets).
Example Request
bash
curl -H "Network: mainnet" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "CommentID": "uuid-string-1234",
    "Status": 4,
    "Reason": 1
  }' \
  -X PUT "https://api.admin.sologenic.org/api/admincomment/status"
Success Response
text
200 OK
Error Responses
Error Code	Description
401 UNAUTHORIZED	Invalid or missing token
500 ACCOUNT PARAM INVALID	Invalid account
500 NETWORK PARAM INVALID	Invalid network
500 COMMENT_ID PARAM INVALID	Invalid comment ID
500 STATUS PARAM INVALID	Invalid status value
500 REASON PARAM INVALID	Invalid reason (required for ADMIN_DELETED)
DELETE /api/admincomment/delete
Deletes a comment. Only the owner of a comment can delete it. The system verifies ownership by checking that the accountID matches the account ID associated with the comment.

Deletion Behavior
The service only sets the state of the comment to DELETED or DELETED_CASCADE. The trigger channel processes the comment and removes it from the database if the rules are met:

Rule	Behavior
Cascading delete	Executed only if ownership rules are met (account requesting delete is the owner of the root object)
Cascading delete	Ignored if account requesting delete is not the owner of the root object
Delete	Ignored if account requesting delete is not the owner of the comment or owner of the root object
Note: FE should only allow accounts with certain ownership of either the comment or the root object (NFT, etc.) to submit deletions.

Request Body
Field	Type	Description	Required
CommentID	string	UUID of the comment	Yes
KeepReplies	boolean	If true, replies are rebased to parent; if false, all replies are deleted	No (default: false)
Reply Handling
KeepReplies	Behavior
true	Replies are rebased (attached to the parent of the deleted comment or to the source if the deleted comment was a reply on the source)
false	All replies are marked as DELETED_CASCADE and processed as normal DELETION events
File Cleanup
If files are attached to the comment, the files are removed immediately from the bucket.

Example Request
bash
curl -H "Network: mainnet" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "CommentID": "uuid-string-1234",
    "KeepReplies": false
  }' \
  -X DELETE "https://api.admin.sologenic.org/api/admincomment/delete"
Success Response
text
200 OK
Note: Success response is given in virtually all scenarios (even if commentID is invalid). The system doesn't return errors for duplicate deletions or stale references.

Error Responses
Error Code	Description
401 UNAUTHORIZED	Invalid or missing token
500 ACCOUNT PARAM INVALID	Invalid account
500 NETWORK PARAM INVALID	Invalid network
500 COMBINATION OF PARAMETERS INVALID	Invalid parameters
500 DELETE IN PROGRESS	Delete operation already in progress
Pagination
All list-style endpoints (multiple results) have pagination options returned as a standard object in the response:

json
{
  "Offset": 20
}
The absence of the offset object means there is no more data to be retrieved.

To paginate, pass the offset parameter:

text
GET /api/admincomment/get?offset={offset}
User Reputation System
Reporting Score
When a message is marked as REVIEWED, the reporting account gets an adjusted score to prevent spamming the admin with reviews of items within normal community standards.

Score Value	Meaning
Positive	User reports comments that are deleted by admin
Zero	No reports by the user in the last period or never
Negative	User reports more comments that are NOT deleted by admin (incorrect reports)
Score Reset
A background process resets the user score from negative to 0 after a certain period of time.

Consequences
Having a certain negative score can lead to:

Banning the user from creating more reports

Banning the user completely from interactions with social aspects of the system

Trigger Channel Events
The system uses a Kafka trigger topic to delegate report processing consequences to a sub-process.

ADMIN_DELETED Trigger Process
On ADMIN_DELETED status:

Remove any uploads associated with the message

Record deleted images in separate image log as MD5 of the image, reason, and poster address

Record deleted message in separate message log as MD5 of the message, reason, and poster address

DELETED/DELETED_CASCADE Trigger Process
Secondary processes executed through the trigger topic:

Update counts for all users who liked the comment

Adjust account-based reputation (both positive and negative)

Process cascading deletes

Special Considerations
Testnet vs Mainnet
⚠️ Important: In production, both testnet and mainnet are available, and the admin is required to review both. No method for limiting the use of testnet is currently implemented or planned.

Since testnet does not have limitations with regards to availability of funds, testnet can be abused to spam the system and destroy the user experience. Additional consideration should be made to prevent this.

Empty Database
GET and COUNT do not work against an empty database due to lack of any model for the database to reference. One comment must be added into the system using curl to avoid this empty database error.

Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
COMMENT_STORE_ENDPOINT	Comment store endpoint	github.com/sologenic/com-fs-comment-model
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
ACCOUNT_STORE	Account store endpoint	github.com/sologenic/com-fs-account-model
ROLE_STORE	Role store endpoint	github.com/sologenic/com-fs-role-model
FILE_STORE	File store endpoint	github.com/sologenic/com-fs-file-model
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-store
Optional Environment Variables
Environment Variable	Description
FEATURE_FLAG_STORE	Feature flag service endpoint (if feature flags present)
LOG_LEVEL	Logging level (info, debug, warn, error)
Comment Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Comment Lifecycle                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐                                                              │
│  │ Created  │                                                              │
│  │ NORMAL   │                                                              │
│  └────┬─────┘                                                              │
│       │                                                                     │
│       ├──────────────────────┬──────────────────────┐                      │
│       │                      │                      │                      │
│       ▼                      ▼                      ▼                      │
│  ┌──────────┐           ┌──────────┐           ┌──────────┐               │
│  │ READ     │           │ REVIEW   │           │ REPORTED │               │
│  │ (Admin   │           │ REQUESTED│           │ (User    │               │
│  │ viewed)  │           │          │           │ flagged) │               │
│  └────┬─────┘           └────┬─────┘           └────┬─────┘               │
│       │                      │                      │                      │
│       │                      ▼                      │                      │
│       │                 ┌──────────┐                │                      │
│       │                 │ REVIEWED │                │                      │
│       │                 │ (Admin   │                │                      │
│       │                 │ approved)│                │                      │
│       │                 └──────────┘                │                      │
│       │                                             │                      │
│       └─────────────────────┬──────────────────────┘                      │
│                             │                                              │
│                             ▼                                              │
│                      ┌──────────────┐                                     │
│                      │ ADMIN_DELETED│                                     │
│                      │ or DELETED   │                                     │
│                      └──────────────┘                                     │
│                             │                                              │
│                             ▼                                              │
│                      ┌──────────────┐                                     │
│                      │ Async Cleanup│                                     │
│                      │ • Remove     │                                     │
│                      │   uploads    │                                     │
│                      │ • Log MD5    │                                     │
│                      │ • Adjust     │                                     │
│                      │   reputation │                                     │
│                      └──────────────┘                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Future Improvements
The collected MD5 hashes in the logs of removed images and messages can be used to create an algorithm/model to automatically remove messages and images similar to those removed by the admin.

Spam Prevention
User Reporting Score
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      User Reporting Score System                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Reports Comment                                                       │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Admin Reviews Comment                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│           │                                                                 │
│           ├─────────────────────┬─────────────────────┐                   │
│           │                     │                     │                   │
│           ▼                     ▼                     ▼                   │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐          │
│  │ Comment        │    │ Comment        │    │ No Action      │          │
│  │ Deleted        │    │ Approved       │    │ Taken          │          │
│  └────────┬───────┘    └────────┬───────┘    └────────┬───────┘          │
│           │                     │                     │                   │
│           ▼                     ▼                     ▼                   │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐          │
│  │ +1 Score       │    │ -1 Score       │    │ 0 Score        │          │
│  │ (Good report)  │    │ (Bad report)   │    │ (Neutral)      │          │
│  └────────────────┘    └────────────────┘    └────────────────┘          │
│                                                                             │
│  Score < Threshold ──────────────────────────────────────────────► Ban     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Related Services
Service	Description
Admin Account Service	User and role management
File Service	File upload and storage
Notification Service	Notification model definitions
Organization Service	Organization management
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Empty database error	No comments exist	Add one comment using curl
Comments not appearing	Status filter active	Check status parameter
Cannot delete comment	Not the owner	Verify account ID matches comment owner
Spam reports	User with negative score	Review user's reporting history
Testnet spam	No testnet limitations	Implement additional monitoring
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check Kafka trigger topic for async processing status.

Best Practices
Comment Moderation: Regularly review REVIEW_REQUESTED comments

Spam Prevention: Monitor user reporting scores

Testnet Monitoring: Pay special attention to testnet activity

Cascading Deletes: Use KeepReplies=false for spam/abuse removal

Audit Trail: All status changes are logged with user information

License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the admin comment service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the admin comment service section:

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

The Admin Comment Service provides generic functionality to attach comments to any source type, facilitating support system management (chat and ticket) and admin delete actions.

📖 **[Admin Comment Service Documentation](./admin/comment/comment-service.md)**

**Key Features:**
- List comments with multiple filter combinations
- Count comments for specific sources
- Add comments and replies
- Update comment status (read, reviewed, deleted)
- Delete comments with cascading options
- User reputation system to prevent spam
- Asynchronous processing via Kafka trigger channel

**Comment Status Values:**
| Status | Description |
|--------|-------------|
| NORMAL (1) | Normal visible comment |
| REVIEWED (2) | Admin has reviewed |
| REVIEW_REQUESTED (3) | Flagged for review |
| ADMIN_DELETED (4) | Admin deleted |
| DELETED (6) | User/moderator deleted |
| READ (8) | Read by admin |

**Quick Examples:**
```bash
# List comments by account
GET /api/admincomment/get?account=user123&order=2

# Add a comment
POST /api/admincomment/add
{"SourceType":4,"Source":"12345","Content":"Comment text"}

# Delete a comment
DELETE /api/admincomment/delete
{"CommentID":"uuid","KeepReplies":false}
Account Types:

Sologenic Administrator (Platform level)

Organization Administrator (Organization level)

KYC Administrator

Broker Asset Administrator

Normal User (End User)
