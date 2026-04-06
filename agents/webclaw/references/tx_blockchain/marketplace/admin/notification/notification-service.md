# Admin Notification Service

The Admin Notification Service provides RESTful interfaces for managing system notifications across the marketplace platform. Notifications can be sent system-wide, to specific organizations, or to individual users, with support for expiration dates and importance levels.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin Notification Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├─────────────────────────┬───────────────────────────────────────────┤ │
│ │ GET /list │ POST /create │ │
│ │ (Retrieve notifications)│ (Create new notification) │ │
│ └─────────────────────────┴───────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Notification │ Account Store │ Role Store │ Feature Flag │ │
│ │ Store │ │ │ Store │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Consumers (Display Rules Applied) │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Web Frontend (Admin dashboard) │ │
│ │ • Mobile Apps (Push notifications) │ │
│ │ • Email (Digest notifications) │ │
│ │ • Telegram (Bot notifications) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Design Philosophy

The notification system follows a principle where messages are manipulated at a minimal number of locations in the codebase:

| Component | Responsibility |
|-----------|---------------|
| **Producer** | Creates static message with point-in-time parameters, sends to store for persistence |
| **Notification Service** | Retrieves messages from store and serves them unmodified |
| **Consumer (FE, Telegram, Firebase)** | Applies display rules (links, images, formatting) |

This ensures:
- Producers don't need to know display logic
- Consumers don't need to fetch additional data from APIs
- Messages are consistent across all channels

## Role-Based Access Control

| Role | Notification Scope | Description |
|------|-------------------|-------------|
| Sologenic Administrator (Platform) | System-wide + All Organizations | Can retrieve all notifications (system-wide and all organization-specific) |
| Organization Administrator | Organization-specific | Can only retrieve notifications specific to their organization |

## Data Models

### Notification Object

| Field | Type | Description |
|-------|------|-------------|
| NotificationID | int64 | Unique notification identifier (timestamp-based) |
| Type | int | Notification type (see Type values below) |
| Message | MessageObject | Notification content (subject, body, format) |
| From | string | Sender email or identifier |
| Importance | int | Importance level (1=Normal, 2=High, 3=Critical) |
| Target | []int | Target audience roles |
| Key | string | Unique key for deduplication |
| ValidFrom | Timestamp | When notification becomes valid |
| ExpiresAt | Timestamp | When notification expires |
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |

### Message Object

| Field | Type | Description |
|-------|------|-------------|
| Format | int | Message format (1=Plain text, 2=HTML, 3=Markdown) |
| Subject | string | Notification subject/title |
| Body | string | Notification content body |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

### Notification Type Values

| Type ID | Type Name | Description |
|---------|-----------|-------------|
| 1 | Maintenance | System maintenance announcements |
| 2 | Admin | Administrative notifications |
| 3 | Marketing | Marketing and promotional messages |
| 4 | Security | Security alerts and updates |
| 5 | Compliance | Regulatory compliance notifications |
| 6 | System | General system notifications |

### Importance Levels

| Level | Importance | Description | UI Treatment |
|-------|------------|-------------|--------------|
| 1 | Normal | Standard notification | Default styling |
| 2 | High | Important notification | Highlighted/warning styling |
| 3 | Critical | Urgent action required | Red/alert styling, may require acknowledgment |

### Target Role Values

| Target ID | Role | Description |
|-----------|------|-------------|
| 1 | Sologenic Administrator | Platform-level administrators |
| 2 | Organization Administrator | Organization-level administrators |
| 3 | KYC Administrator | KYC verification administrators |
| 4 | Broker Asset Administrator | Asset management administrators |
| 5 | Normal User | Regular end users |

## API Endpoints

### GET /api/adminnotification/list

Retrieves notifications based on the caller's role. Returns a cursor for pagination to indicate if there is a next set of notifications.

#### Role-Based Response Scope

| Caller Role | Notifications Returned |
|-------------|----------------------|
| Sologenic Administrator | System-wide notifications + All organization-specific notifications |
| Organization Administrator | Organization-specific notifications only (their organization) |

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| OrganizationID | Organization UUID | Yes (for org admins) |
| Authorization | Bearer <firebase_token> | Yes |

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| id | int64 | Notification ID for pagination (cursor) | No |
| ts | int64 | Timestamp for pagination | No |

**Pagination Logic:**
- First call: No parameters (returns most recent notifications)
- Subsequent calls: Pass `id` and `ts` from the `More` field in previous response
- The `More` field contains the ID of the first notification in the next set

#### Example Request (First Page)

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/adminnotification/list" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Request (Next Page)
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/adminnotification/list?id=1740697822969213000&ts=1740697822" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "Notification": [
    {
      "Type": 1,
      "Message": {
        "Format": 1,
        "Subject": "Maintenance Notification 2",
        "Body": "This is a maintenance notification. The service will be down on..."
      },
      "CreatedAt": {
        "seconds": 1740697822,
        "nanos": 775009000
      },
      "UpdatedAt": {
        "seconds": 1740697822,
        "nanos": 775009000
      },
      "NotificationID": 1740697822969213000,
      "From": "admin@organization.org",
      "Importance": 1,
      "Target": [2],
      "ExpiresAt": {
        "seconds": 1743205844,
        "nanos": 775010000
      },
      "ValidFrom": {
        "seconds": 1740697822,
        "nanos": 775011000
      },
      "Key": "Maintenance-1740697822775011000"
    },
    {
      "Type": 1,
      "Message": {
        "Format": 1,
        "Subject": "Maintenance Notification 1",
        "Body": "This is a maintenance notification. The service will be down on..."
      },
      "CreatedAt": {
        "seconds": 1740697819,
        "nanos": 147257000
      },
      "UpdatedAt": {
        "seconds": 1740697819,
        "nanos": 147258000
      },
      "NotificationID": 1740697819343267000,
      "From": "admin@organization.org",
      "Importance": 1,
      "Target": [2],
      "ExpiresAt": {
        "seconds": 1743205844,
        "nanos": 147258000
      },
      "ValidFrom": {
        "seconds": 1740697819,
        "nanos": 147259000
      },
      "Key": "Maintenance-1740697819147259000"
    }
  ],
  "More": {
    "ID": 1740697800000000000,
    "Timestamp": 1740697800
  }
}
Response Fields
Field	Description
Notification	Array of notification objects
More.ID	Notification ID for next page (omit if no more)
More.Timestamp	Timestamp for next page (omit if no more)
Error Responses
Status Code	Description
200	Success - Returns notifications (may be empty)
400	Bad request - Invalid pagination parameters
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
500	Internal server error
POST /api/adminnotification/create
Creates a new notification. Notifications can be recipient-specific (account or organization) or system-wide.

Creation Permissions
Creator Role	Can Create
Sologenic Administrator	System-wide notifications (all organizations)
Sologenic Administrator	Organization-specific for 'sologenic' organization (with IsOrgScoped=true)
Organization Administrator	Organization-specific notifications (their organization only)
Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes (for org-scoped)
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
Notification_type	string	Type name ("Maintenance", "Admin", "Marketing", "Security", "Compliance", "System")	Yes
Message.Subject	string	Notification subject/title	Yes
Message.Body	string	Notification content	Yes
Message.Format	int	Message format (1=Plain, 2=HTML, 3=Markdown)	No (default: 1)
Recipient_id	string	Specific user/account ID for recipient-specific notification	No
IsOrgScoped	boolean	If true, notification is scoped to organization	No
ExpiresAt	string	ISO 8601 expiration timestamp	No
ValidFrom	string	ISO 8601 valid-from timestamp	No
Importance	int	Importance level (1,2,3)	No (default: 1)
Target	[]int	Target role IDs	No
Example 1: System-Wide Maintenance Notification (Sologenic Admin)
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/adminnotification/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet" \
  -d '{
    "Notification_type": "Maintenance",
    "Message": {
      "Subject": "Scheduled Maintenance",
      "Body": "A system maintenance is scheduled for 2025-03-15 02:00 UTC. The system will be down for 1 hour.",
      "Format": 1
    },
    "Importance": 2,
    "ExpiresAt": "2025-03-16T23:59:59Z"
  }'
Example 2: Organization-Specific Notification (Sologenic Admin for Sologenic Org)
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/adminnotification/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet" \
  -d '{
    "Notification_type": "Admin",
    "Message": {
      "Subject": "Internal Update",
      "Body": "This message is only for Sologenic organization users."
    },
    "IsOrgScoped": true,
    "ExpiresAt": "2025-12-31T23:59:59Z"
  }'
Example 3: Organization-Specific Notification (Organization Admin)
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/adminnotification/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet" \
  -d '{
    "Notification_type": "Compliance",
    "Message": {
      "Subject": "New Regulatory Requirement",
      "Body": "Please review the updated compliance requirements for your organization."
    },
    "IsOrgScoped": true,
    "Importance": 2,
    "ExpiresAt": "2025-06-30T23:59:59Z"
  }'
Example 4: Recipient-Specific Notification
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/adminnotification/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet" \
  -d '{
    "Notification_type": "Marketing",
    "Recipient_id": "c12e34f5-6789-0abc-def1-234567890abc",
    "Message": {
      "Subject": "Exclusive Offer",
      "Body": "Dear user, we have a special offer for you. Please check your account for more details."
    },
    "Importance": 1,
    "ExpiresAt": "2025-04-30T23:59:59Z"
  }'
Example 5: Targeted by Role
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/adminnotification/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet" \
  -d '{
    "Notification_type": "Admin",
    "Message": {
      "Subject": "Admin Training Session",
      "Body": "Mandatory training for all organization administrators on April 1st."
    },
    "Target": [2],
    "Importance": 2,
    "ExpiresAt": "2025-04-05T23:59:59Z"
  }'
Example Response
json
{
  "Success": true,
  "NotificationID": 1740697822969213000,
  "Message": "Notification created successfully"
}
Error Responses
Status Code	Description
200	Success - Notification created
400	Bad request - Missing required fields or invalid data
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions for requested scope
500	Internal server error
Notification Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Notification Lifecycle                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐                                                          │
│  │ Notification │                                                          │
│  │ Created      │                                                          │
│  └──────┬───────┘                                                          │
│         │                                                                   │
│         │ ValidFrom reached (if set)                                       │
│         ▼                                                                   │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
│  │ Active       │────▶│ Displayed    │────▶│ Read/        │               │
│  │ (Valid)      │     │ to Users     │     │ Acknowledged │               │
│  └──────┬───────┘     └──────────────┘     └──────────────┘               │
│         │                                                                   │
│         │ ExpiresAt reached                                                 │
│         ▼                                                                   │
│  ┌──────────────┐                                                          │
│  │ Expired      │                                                          │
│  │ (Not shown)  │                                                          │
│  └──────────────┘                                                          │
│                                                                             │
│  Notifications are filtered by:                                            │
│  • ValidFrom (must be in the past)                                         │
│  • ExpiresAt (must be in the future)                                       │
│  • Target roles (must match user's roles)                                  │
│  • Organization scope (must match user's organization)                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Notification Targeting Matrix
Scope	Target	Who Receives
System-wide	None (or all roles)	All users across all organizations
Organization-scoped	None	All users in the specified organization
Role-targeted	[2]	All users with Organization Administrator role
Recipient-specific	Recipient_id	Single specific user
Targeting Examples
json
// System-wide to all administrators
{
  "Target": [1, 2],
  "IsOrgScoped": false
}

// Organization-scoped to all users in that org
{
  "IsOrgScoped": true,
  "Target": []
}

// Specific user only
{
  "Recipient_id": "user-uuid-1234"
}

// All KYC administrators across all organizations
{
  "Target": [3],
  "IsOrgScoped": false
}
Message Format Examples
Plain Text (Format: 1)
json
{
  "Format": 1,
  "Subject": "System Update",
  "Body": "The system will be updated on Friday at 10 PM UTC."
}
HTML (Format: 2)
json
{
  "Format": 2,
  "Subject": "New Feature Available",
  "Body": "<h3>Advanced Trading Charts</h3><p>We're excited to announce <strong>new charting features</strong> including:</p><ul><li>Candlestick patterns</li><li>Technical indicators</li><li>Drawing tools</li></ul><a href='https://solotex.com/charts'>Try it now</a>"
}
Markdown (Format: 3)
json
{
  "Format": 3,
  "Subject": "API Documentation Update",
  "Body": "## API v2.0 Released\n\nNew endpoints available:\n- `GET /api/v2/orders`\n- `POST /api/v2/webhooks`\n\nSee [docs](https://docs.solotex.com/api/v2) for details."
}
Notification Deduplication (Key Field)
The Key field is automatically generated to prevent duplicate notifications. Format: {Type}-{Timestamp}

Example keys:

Maintenance-1740697822775011000

Admin-1740697819147259000

Security-1740697800123456000

Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-model/
NOTIFICATION_STORE	Notification service endpoint	github.com/sologenic/com-fs-notification-model/
ACCOUNT_STORE	Account service endpoint	github.com/sologenic/com-fs-admin-account-model/
ROLE_STORE	Role service endpoint	github.com/sologenic/com-fs-admin-role-model/
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-admin-feature-flag-model/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-admin-organization-model/
SOLOGENIC_ORGANIZATION_ID	Organization ID of Sologenic Unified User	Required for platform identification
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
  "message": "Insufficient permissions to create system-wide notification. Required role: SOLOGENIC_ADMINISTRATOR"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Missing required field: Message.Subject",
  "details": "Notification subject is required"
}
Bad Request - Invalid Date Format
json
{
  "error": "Bad Request",
  "message": "Invalid date format",
  "details": "ExpiresAt must be in ISO 8601 format (e.g., 2025-12-31T23:59:59Z)"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Notifications not appearing	ExpiresAt in the past or ValidFrom in the future	Check expiration and validity dates
Wrong users receiving notifications	Target roles incorrect	Verify target role IDs
Organization admin sees no notifications	Wrong OrganizationID header	Ensure correct OrganizationID
Cannot create system-wide notification	Insufficient permissions	Requires Sologenic Administrator role
Duplicate notifications	Same Key generated	System handles deduplication automatically
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check notification retrieval:

bash
# Get first page
curl -X GET /api/adminnotification/list \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: mainnet"

# Get next page using More cursor
curl -X GET "/api/adminnotification/list?id=<more_id>&ts=<more_ts>" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: mainnet"
Best Practices
Notification Creation
Set Appropriate Expiration: Always set ExpiresAt for time-sensitive notifications

Use Importance Levels:

Level 1: General announcements

Level 2: Important updates requiring attention

Level 3: Critical issues requiring immediate action

Target Appropriately: Use the most specific targeting possible (Recipient_id > Target > IsOrgScoped)

Clear Subjects: Make notification subjects descriptive and actionable

Content Guidelines
Notification Type	Recommended Frequency	Example Use Case
Maintenance	As needed	Scheduled downtime
Admin	Weekly/Daily	Internal updates
Marketing	Weekly	Promotions, features
Security	Immediate	Breach alerts, suspicious activity
Compliance	As needed	Regulatory changes
System	As needed	Performance updates
Pagination
Store the Cursor: Save More.ID and More.Timestamp for pagination

Infinite Scroll: Use cursor for infinite scroll implementations

Refresh Strategy: Reset pagination when refreshing notification list

Consumer Display Rules
Different consumers apply their own display rules to the same notification data:

Consumer	Display Rules Applied
Web Frontend	HTML formatting, links, read/unread status
Mobile App	Push notification formatting, deep links
Email	HTML email template, branding
Telegram	Markdown formatting, inline buttons
The notification service itself does not modify the message content.

Related Services
Service	Description
Admin Account Service	User and role management
Organization Service	Organization management
Feature Flag Service	Feature toggles for notification channels
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the Notification Service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the Admin Notification Service section under Admin Services:

markdown
### Admin Notification Service

The Admin Notification Service provides RESTful interfaces for managing system notifications across the marketplace platform.

📖 **[Admin Notification Service Documentation](./admin/notification/notification-service.md)**

**Key Features:**
- Create system-wide, organization-scoped, or recipient-specific notifications
- Role-based access control (Sologenic Admin vs Organization Admin)
- Time-based validity (ValidFrom, ExpiresAt)
- Importance levels (Normal, High, Critical)
- Target by user role
- Pagination with cursor-based navigation
- Multiple message formats (Plain text, HTML, Markdown)

**Notification Types:**
| Type | Description |
|------|-------------|
| Maintenance | System maintenance announcements |
| Admin | Administrative notifications |
| Marketing | Promotional messages |
| Security | Security alerts |
| Compliance | Regulatory notifications |
| System | General system updates |

**Importance Levels:**
| Level | Name | UI Treatment |
|-------|------|--------------|
| 1 | Normal | Default styling |
| 2 | High | Highlighted/warning |
| 3 | Critical | Alert/action required |

**Quick Examples:**
```bash
# List notifications (paginated)
GET /api/adminnotification/list

# Create system-wide notification
POST /api/adminnotification/create
{
  "Notification_type": "Maintenance",
  "Message": {
    "Subject": "Scheduled Maintenance",
    "Body": "System down for 1 hour..."
  },
  "ExpiresAt": "2025-12-31T23:59:59Z"
}

# Create organization-scoped notification
POST /api/adminnotification/create
{
  "Notification_type": "Admin",
  "Message": {...},
  "IsOrgScoped": true
}
Role Scopes:

Role	Can View	Can Create
Sologenic Administrator	All notifications	System-wide + Org-scoped
Organization Administrator	Org-specific only	Org-scoped only
