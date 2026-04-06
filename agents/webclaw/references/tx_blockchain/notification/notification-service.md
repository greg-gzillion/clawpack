# Notification Service

The Notification Service provides a RESTful interface for managing user notifications, including admin announcements, marketing messages, system maintenance alerts, and user-to-user communications.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Notification Service Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ REST API Endpoints (Authenticated) │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ GET /unread │ GET /topauth │ GET /list │ PUT /read │ │
│ │ (Has unread?) │ (Top alerts) │ (Paginated) │ (Mark read) │ │
│ │ │ │ │ │ │
│ │ │ │ │ PUT /readall │ │
│ │ │ │ │ (Mark all read) │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Message Processing Pipeline │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Producers create static messages with parameters │ │
│ │ • Messages stored unmodified in notification store │ │
│ │ • Consumers apply display rules (FE, Telegram, Firebase, Email) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Data Sources │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Notification │ User Store │ Role Store │ Organization Store │ │
│ │ Store │ │ │ │ │
│ │ Feature Flag │ Auth Firebase │ HTTP Config │ │ │
│ │ Store │ Service │ │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Design Philosophy

### Separation of Concerns

The notification system follows a **producer-consumer** pattern with minimal coupling:
┌─────────────────────────────────────────────────────────────────────────────┐
│ Producer-Consumer Flow │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ PRODUCER (e.g., Payment Service) │ │
│ │ • Creates static message with parameters │ │
│ │ • Includes point-in-time values │ │
│ │ • Sends to notification store │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ NOTIFICATION SERVICE │ │
│ │ • Retrieves messages from store │ │
│ │ • Serves them unmodified │ │
│ │ • NO post-processing or value fetching │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ CONSUMERS (FE, Telegram, Firebase, Email) │ │
│ │ • Apply display rules │ │
│ │ • Format based on destination │ │
│ │ • NO additional API calls for values │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

### Key Principles

1. **Static Messages**: Messages are fully static at creation time
2. **No Post-Processing**: Notification service doesn't modify messages
3. **Display Rules Only**: Consumers only format, never fetch additional data
4. **Pre-processing Preference**: All dynamic values resolved at creation
5. **Stable Interface**: Notification service doesn't change per message type

## Data Models

### Notification Object

| Field | Type | Description |
|-------|------|-------------|
| ID | string | Unique notification identifier |
| Key | string | Message key (same for multi-user notifications) |
| Type | NotificationType | Type enum (27+ types) |
| Subject | string | Notification subject (supports i18n placeholders) |
| Body | string | Notification body (supports i18n placeholders) |
| Parameters | []Parameter | Dynamic values for placeholders |
| CreatedAt | timestamp | Creation time (RFC3339) |
| Read | bool | Read status for current user |
| To | string | Recipient account ID |
| From | string | Sender account ID |
| Priority | Priority | Notification priority level |

### NotificationType Enum

| Type | Description | Category |
|------|-------------|----------|
| TRANSACTION_RECEIVED | Received payment | Transaction |
| TRANSACTION_SENT | Sent payment | Transaction |
| OFFER_CREATED | New offer created | Trading |
| OFFER_FILLED | Offer partially/completely filled | Trading |
| OFFER_CANCELLED | Offer cancelled | Trading |
| NFT_MINTED | NFT successfully minted | NFT |
| NFT_BOUGHT | NFT purchased | NFT |
| NFT_SOLD | NFT sold | NFT |
| NFT_BID_PLACED | Bid placed on NFT | NFT |
| NFT_BID_WON | Won NFT auction | NFT |
| NFT_BID_OUTBID | Outbid on NFT | NFT |
| COLLECTION_CREATED | New collection created | NFT |
| KYC_STATUS_CHANGED | KYC status updated | Account |
| ACCOUNT_VERIFIED | Account verification complete | Account |
| WALLET_CONNECTED | New wallet connected | Account |
| ADMIN_ANNOUNCEMENT | Admin broadcast | Admin |
| MARKETING_PROMOTION | Marketing message | Marketing |
| MAINTENANCE_ALERT | System maintenance | Maintenance |
| SECURITY_ALERT | Security notification | Security |
| PRICE_ALERT | Price threshold reached | Market |
| ORDER_FILLED | Order executed | Trading |
| DEPOSIT_CONFIRMED | Deposit confirmed | Transaction |
| WITHDRAWAL_COMPLETED | Withdrawal complete | Transaction |
| WITHDRAWAL_FAILED | Withdrawal failed | Transaction |
| LIMIT_ORDER_TRIGGERED | Limit order executed | Trading |
| STOP_LOSS_TRIGGERED | Stop loss activated | Trading |
| SYSTEM_UPDATE | Platform update | System |
| FEATURE_RELEASED | New feature available | System |

### Priority Levels

| Priority | Value | Description | Use Case |
|----------|-------|-------------|----------|
| HIGH | 1 | Critical, immediate attention | Security alerts, failed transactions |
| MEDIUM | 2 | Important but not urgent | KYC updates, order fills |
| LOW | 3 | Informational | Marketing, announcements |
| BULK | 4 | Batch notifications | System updates, newsletters |

### Parameter Object

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| Label | string | Parameter identifier (from enum) | Yes |
| Value | string | Display value (parsed) | Yes |
| DataType | DataType | Type for formatting | Yes |
| SourceType | string | Type of ID in Source | No (if Source present) |
| Source | string | Root address for logic/navigation | No |
| FromTo | FromTo | Direction indicator | No |

### DataType Enum

| DataType | Description | Formatting Rules |
|----------|-------------|------------------|
| string | Text value | Display as-is |
| number | Numeric value | Format with appropriate decimals |
| url | Web link | Render as clickable link |
| image | Image reference | Render as image |

### FromTo Enum

| Value | Description | Use Case |
|-------|-------------|----------|
| FROM | Source/origin | Left side in UI (sender) |
| TO | Destination | Right side in UI (recipient) |
| CONTENT | Content item | Center or main content |

**Note:** FromTo always accompanied by Source and SourceType. Used for rendering URLs or navigation identifiers.

### More Object (Pagination)

| Field | Type | Description |
|-------|------|-------------|
| ID | string | ID of first notification in next set |
| TS | string | Nano timestamp for next set |

## API Endpoints

### GET /api/notification/unread

Returns whether the user has unread notifications.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Authorization | Bearer token | Yes |
| OrganizationID | Organization UUID | Yes |
| Network | mainnet, testnet, devnet | Yes |

#### Example Request

```bash
curl -X GET "https://api.sologenic.org/api/notification/unread" \
  -H "Network: mainnet" \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..."
Example Response
json
{
  "unread": true
}
GET /api/notification/topauth
Retrieves all unread admin/marketing/maintenance notifications for the current user.

Headers
Header	Description	Required
Authorization	Bearer token	Yes
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Query Parameters
Parameter	Type	Description	Required
type	string	Comma-separated types: admin, marketing, maintenance	No (returns all if omitted)
Example Request
bash
curl -X GET "https://api.sologenic.org/api/notification/topauth?type=admin,marketing" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..."
Example Response
json
{
  "Notifications": [
    {
      "ID": "notif_12345",
      "Key": "admin_announcement_001",
      "Type": "ADMIN_ANNOUNCEMENT",
      "Subject": "System Update Scheduled",
      "Body": "Maintenance will occur on Sunday at 2 AM UTC",
      "CreatedAt": "2024-01-15T10:30:00.000Z",
      "Read": false,
      "To": "user_account_id",
      "From": "admin@solotex.com",
      "Priority": "MEDIUM",
      "Parameters": [
        {
          "Label": "maintenance_date",
          "Value": "Sunday, 2 AM UTC",
          "DataType": "string"
        }
      ]
    },
    {
      "ID": "notif_12346",
      "Key": "marketing_promo_spring",
      "Type": "MARKETING_PROMOTION",
      "Subject": "Spring Trading Competition",
      "Body": "Win prizes by trading this month!",
      "CreatedAt": "2024-01-14T15:20:00.000Z",
      "Read": false,
      "To": "user_account_id",
      "From": "marketing@solotex.com",
      "Priority": "LOW",
      "Parameters": []
    }
  ]
}
GET /api/notification/list
Retrieves paginated notifications for the current user.

Headers
Header	Description	Required
Authorization	Bearer token	Yes
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Query Parameters
Parameter	Type	Description	Required
id	string	Notification ID for pagination	No (first page if omitted)
ts	string	Nano timestamp for pagination	No (first page if omitted)
Pagination Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Notification Pagination Flow                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Page 1 Request: GET /list                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Response:                                                            │   │
│  │ • Notifications: [msg1, msg2, msg3, ..., msg20]                      │   │
│  │ • More: { ID: "msg21", TS: "1234567890" }                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Page 2 Request: GET /list?id=msg21&ts=1234567890                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Response:                                                            │   │
│  │ • Notifications: [msg21, msg22, msg23, ..., msg40]                   │   │
│  │ • More: { ID: "msg41", TS: "1234567891" }                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Page 3 Request: GET /list?id=msg41&ts=1234567891                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Response:                                                            │   │
│  │ • Notifications: [msg41, msg42, ...]                                 │   │
│  │ • More: null (no more notifications)                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Example Request (First Page)
bash
curl -X GET "https://api.sologenic.org/api/notification/list" \
  -H "Network: mainnet" \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..."
Example Request (Subsequent Page)
bash
curl -X GET "https://api.sologenic.org/api/notification/list?id=notif_12345&ts=1705315200000000000" \
  -H "Network: mainnet" \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..."
Example Response
json
{
  "Notifications": [
    {
      "ID": "notif_12340",
      "Key": "txn_received_001",
      "Type": "TRANSACTION_RECEIVED",
      "Subject": "Payment Received",
      "Body": "You received {{amount}} {{currency}} from {{sender}}",
      "CreatedAt": "2024-01-15T09:15:00.000Z",
      "Read": true,
      "To": "rUserAddress",
      "From": "rSenderAddress",
      "Priority": "MEDIUM",
      "Parameters": [
        {
          "Label": "amount",
          "Value": "100.50",
          "DataType": "number",
          "FromTo": "CONTENT"
        },
        {
          "Label": "currency",
          "Value": "XRP",
          "DataType": "string"
        },
        {
          "Label": "sender",
          "Value": "John Doe",
          "DataType": "string",
          "SourceType": "ACCOUNT_ID",
          "Source": "rSenderAddress",
          "FromTo": "FROM"
        }
      ]
    }
  ],
  "More": {
    "ID": "notif_12341",
    "TS": "1705315300000000000"
  }
}
PUT /api/notification/read
Marks notifications with specific keys as read.

Important Notes
Admin/marketing/maintenance notifications have 1 key for all users

Backend tracks read status per user for shared notifications

Maximum 100 keys per request

Response is pre-emptive 200 OK (async processing)

Headers
Header	Description	Required
Authorization	Bearer token	Yes
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Content-Type	application/json	Yes
Request Body
Field	Type	Description	Required
Key	[]string	Array of notification keys	Yes
Example Request
bash
curl -X PUT "https://api.sologenic.org/api/notification/read" \
  -H "Network: mainnet" \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{"Key": ["admin_announcement_001", "marketing_promo_spring", "txn_received_001"]}'
Example Response
json
{
  "status": "accepted",
  "message": "Mark read request received, processing asynchronously"
}
PUT /api/notification/readall
Marks all notifications as read for the current user.

Important Notes
Processing may take significant time

Response is pre-emptive 200 OK (async processing)

FE should disable read all button after click to prevent duplicate requests

FE should optimistically mark messages as read locally

Headers
Header	Description	Required
Authorization	Bearer token	Yes
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Example Request
bash
curl -X PUT "https://api.sologenic.org/api/notification/readall" \
  -H "Network: mainnet" \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..."
Example Response
json
{
  "status": "accepted",
  "message": "Mark all read request received, processing asynchronously"
}
Internationalization (i18n)
i18n String Format
text
NOTIFICATION_TYPE_subject: "Subject text with {{placeholder}}"
NOTIFICATION_TYPE_body: "Body text with {{placeholder}}"
i18n Example
English (en-US):

json
{
  "TRANSACTION_RECEIVED_subject": "Payment Received",
  "TRANSACTION_RECEIVED_body": "You received {{amount}} {{currency}} from {{sender}}",
  "NFT_BOUGHT_subject": "NFT Purchase Confirmed",
  "NFT_BOUGHT_body": "You bought {{nft_name}} for {{price}} {{currency}}"
}
Dutch (nl-NL):

json
{
  "TRANSACTION_RECEIVED_subject": "Betaling Ontvangen",
  "TRANSACTION_RECEIVED_body": "Je hebt {{amount}} {{currency}} ontvangen van {{sender}}",
  "NFT_BOUGHT_subject": "NFT Aankoop Bevestigd",
  "NFT_BOUGHT_body": "Je hebt {{nft_name}} gekocht voor {{price}} {{currency}}"
}
Japanese (ja-JP):

json
{
  "TRANSACTION_RECEIVED_subject": "支払いを受け取りました",
  "TRANSACTION_RECEIVED_body": "{{sender}}から{{amount}}{{currency}}を受け取りました",
  "NFT_BOUGHT_subject": "NFT購入確認",
  "NFT_BOUGHT_body": "{{nft_name}}を{{price}}{{currency}}で購入しました"
}
i18n Rules
Subject: Uses {{Type}}_subject key if subject field absent

Body: Optional, used for person-to-person or marketing messages

Placeholders: Use {{PARAMETER}} format matching Parameter.Label

Fallback: English as base language if translation missing

Grammar: Translations can reorder placeholders (e.g., Dutch vs English)

No Layout: i18n files contain no HTML/formatting - reusable across formats

Parameter Resolution Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      i18n Parameter Resolution Flow                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Original Message:                                                          │
│  Subject: "TRANSACTION_RECEIVED_subject" (i18n key)                         │
│  Parameters: [                                                              │
│    {Label: "amount", Value: "100.50", DataType: "number"},                  │
│    {Label: "currency", Value: "XRP", DataType: "string"},                   │
│    {Label: "sender", Value: "John Doe", DataType: "string"}                 │
│  ]                                                                          │
│                                    │                                        │
│                                    ▼                                        │
│  Step 1: Load i18n string for language                                      │
│  English: "You received {{amount}} {{currency}} from {{sender}}"           │
│  Dutch:   "Je hebt {{currency}} {{amount}} ontvangen van {{sender}}"       │
│                                    │                                        │
│                                    ▼                                        │
│  Step 2: Replace placeholders with parameter values                         │
│  English: "You received 100.50 XRP from John Doe"                          │
│  Dutch:   "Je hebt XRP 100.50 ontvangen van John Doe"                      │
│                                    │                                        │
│                                    ▼                                        │
│  Step 3: Apply DataType formatting                                          │
│  • number: Format with appropriate decimals (100.50 → $100.50)             │
│  • url: Make clickable                                                      │
│  • image: Render as image tag                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Integration Examples
React Notification Center
jsx
import React, { useState, useEffect, useCallback } from 'react';

class NotificationClient {
  constructor(baseUrl, token, orgId, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.token = token;
    this.orgId = orgId;
    this.network = network;
  }

  async getUnread() {
    const response = await fetch(`${this.baseUrl}/api/notification/unread`, {
      headers: this._getHeaders()
    });
    return response.json();
  }

  async getTopAuth(types = null) {
    let url = `${this.baseUrl}/api/notification/topauth`;
    if (types) {
      url += `?type=${types.join(',')}`;
    }
    const response = await fetch(url, {
      headers: this._getHeaders()
    });
    return response.json();
  }

  async listNotifications(id = null, ts = null) {
    let url = `${this.baseUrl}/api/notification/list`;
    if (id && ts) {
      url += `?id=${id}&ts=${ts}`;
    }
    const response = await fetch(url, {
      headers: this._getHeaders()
    });
    return response.json();
  }

  async markRead(keys) {
    const response = await fetch(`${this.baseUrl}/api/notification/read`, {
      method: 'PUT',
      headers: {
        ...this._getHeaders(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ Key: keys })
    });
    return response.json();
  }

  async markAllRead() {
    const response = await fetch(`${this.baseUrl}/api/notification/readall`, {
      method: 'PUT',
      headers: this._getHeaders()
    });
    return response.json();
  }

  _getHeaders() {
    return {
      'Authorization': `Bearer: ${this.token}`,
      'OrganizationID': this.orgId,
      'Network': this.network
    };
  }
}

function NotificationCenter({ token, orgId }) {
  const [notifications, setNotifications] = useState([]);
  const [more, setMore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  const [topAlerts, setTopAlerts] = useState([]);
  
  const client = new NotificationClient(
    'https://api.sologenic.org',
    token,
    orgId,
    'mainnet'
  );

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [unreadData, alertsData, notificationsData] = await Promise.all([
        client.getUnread(),
        client.getTopAuth(['admin', 'maintenance']),
        client.listNotifications()
      ]);
      
      setHasUnread(unreadData.unread);
      setTopAlerts(alertsData.Notifications || []);
      setNotifications(notificationsData.Notifications || []);
      setMore(notificationsData.More);
    } catch (error) {
      console.error('Failed to load notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMore = async () => {
    if (!more) return;
    
    setLoading(true);
    try {
      const data = await client.listNotifications(more.ID, more.TS);
      setNotifications(prev => [...prev, ...(data.Notifications || [])]);
      setMore(data.More);
    } catch (error) {
      console.error('Failed to load more notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (keys) => {
    // Optimistic update
    setNotifications(prev =>
      prev.map(notif =>
        keys.includes(notif.Key) ? { ...notif, Read: true } : notif
      )
    );
    
    try {
      await client.markRead(keys);
      // Check if still has unread
      const unreadData = await client.getUnread();
      setHasUnread(unreadData.unread);
    } catch (error) {
      console.error('Failed to mark as read:', error);
      // Revert on error
      loadInitialData();
    }
  };

  const markAllAsRead = async () => {
    // Optimistic update
    setNotifications(prev =>
      prev.map(notif => ({ ...notif, Read: true }))
    );
    setHasUnread(false);
    
    try {
      await client.markAllRead();
    } catch (error) {
      console.error('Failed to mark all as read:', error);
      loadInitialData();
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    return date.toLocaleDateString();
  };

  const getPriorityColor = (priority) => {
    const colors = {
      HIGH: 'priority-high',
      MEDIUM: 'priority-medium',
      LOW: 'priority-low',
      BULK: 'priority-bulk'
    };
    return colors[priority] || 'priority-medium';
  };

  const getTypeIcon = (type) => {
    const icons = {
      TRANSACTION_RECEIVED: '💰',
      TRANSACTION_SENT: '💸',
      NFT_BOUGHT: '🖼️',
      NFT_SOLD: '🎨',
      ADMIN_ANNOUNCEMENT: '📢',
      MAINTENANCE_ALERT: '🔧',
      SECURITY_ALERT: '🔒',
      PRICE_ALERT: '📈'
    };
    return icons[type] || '📬';
  };

  const renderParameter = (param) => {
    switch (param.DataType) {
      case 'number':
        return <span className="param-number">{param.Value}</span>;
      case 'url':
        return <a href={param.Value} target="_blank" rel="noopener noreferrer">{param.Value}</a>;
      case 'image':
        return <img src={param.Value} alt={param.Label} className="param-image" />;
      default:
        return <span className="param-string">{param.Value}</span>;
    }
  };

  return (
    <div className="notification-center">
      {/* Top Alerts Bar */}
      {topAlerts.length > 0 && (
        <div className="top-alerts">
          {topAlerts.map(alert => (
            <div key={alert.ID} className={`alert ${getPriorityColor(alert.Priority)}`}>
              <span className="alert-icon">{getTypeIcon(alert.Type)}</span>
              <div className="alert-content">
                <strong>{alert.Subject}</strong>
                <p>{alert.Body}</p>
              </div>
              <button onClick={() => markAsRead([alert.Key])}>Dismiss</button>
            </div>
          ))}
        </div>
      )}
      
      {/* Notification Header */}
      <div className="notification-header">
        <h2>Notifications</h2>
        {hasUnread && (
          <button onClick={markAllAsRead} className="mark-all-read">
            Mark all as read
          </button>
        )}
      </div>
      
      {/* Notification List */}
      <div className="notification-list">
        {notifications.length === 0 && !loading && (
          <div className="empty-state">No notifications</div>
        )}
        
        {notifications.map(notification => (
          <div
            key={notification.ID}
            className={`notification-item ${!notification.Read ? 'unread' : ''}`}
            onClick={() => !notification.Read && markAsRead([notification.Key])}
          >
            <div className="notification-icon">
              {getTypeIcon(notification.Type)}
            </div>
            <div className="notification-content">
              <div className="notification-header-row">
                <span className="notification-subject">{notification.Subject}</span>
                <span className="notification-time">
                  {formatTimestamp(notification.CreatedAt)}
                </span>
              </div>
              {notification.Body && (
                <div className="notification-body">
                  {notification.Body}
                </div>
              )}
              {notification.Parameters.length > 0 && (
                <div className="notification-parameters">
                  {notification.Parameters.map(param => (
                    <span key={param.Label} className="parameter">
                      {param.Label}: {renderParameter(param)}
                    </span>
                  ))}
                </div>
              )}
            </div>
            {!notification.Read && <div className="unread-dot" />}
          </div>
        ))}
        
        {loading && <div className="loading">Loading...</div>}
        
        {more && !loading && (
          <button onClick={loadMore} className="load-more">
            Load more
          </button>
        )}
      </div>
    </div>
  );
}

export default NotificationCenter;
Node.js Producer Example
javascript
// Notification Producer Service
class NotificationProducer {
  constructor(notificationStoreClient) {
    this.store = notificationStoreClient;
  }

  async produceTransactionReceived(userId, transaction) {
    const notification = {
      Key: `txn_${transaction.hash}`,
      Type: 'TRANSACTION_RECEIVED',
      To: userId,
      From: transaction.sender,
      Priority: 'MEDIUM',
      CreatedAt: new Date().toISOString(),
      Parameters: [
        {
          Label: 'amount',
          Value: transaction.amount.toString(),
          DataType: 'number',
          FromTo: 'CONTENT'
        },
        {
          Label: 'currency',
          Value: transaction.currency,
          DataType: 'string'
        },
        {
          Label: 'sender',
          Value: transaction.senderName || transaction.sender,
          DataType: 'string',
          SourceType: 'ACCOUNT_ID',
          Source: transaction.sender,
          FromTo: 'FROM'
        }
      ]
    };
    
    await this.store.saveNotification(notification);
    return notification;
  }

  async produceNFTBought(userId, nftData, purchaseData) {
    const notification = {
      Key: `nft_bought_${purchaseData.txHash}`,
      Type: 'NFT_BOUGHT',
      To: userId,
      From: 'marketplace',
      Priority: 'MEDIUM',
      CreatedAt: new Date().toISOString(),
      Parameters: [
        {
          Label: 'nft_name',
          Value: nftData.name,
          DataType: 'string',
          SourceType: 'NFT_ID',
          Source: nftData.id,
          FromTo: 'CONTENT'
        },
        {
          Label: 'price',
          Value: purchaseData.price.toString(),
          DataType: 'number'
        },
        {
          Label: 'currency',
          Value: purchaseData.currency,
          DataType: 'string'
        },
        {
          Label: 'seller',
          Value: purchaseData.sellerName || purchaseData.seller,
          DataType: 'string',
          SourceType: 'ACCOUNT_ID',
          Source: purchaseData.seller,
          FromTo: 'FROM'
        }
      ]
    };
    
    await this.store.saveNotification(notification);
    return notification;
  }

  async producePriceAlert(userId, asset, price, threshold) {
    const notification = {
      Key: `price_alert_${asset}_${Date.now()}`,
      Type: 'PRICE_ALERT',
      To: userId,
      From: 'price_oracle',
      Priority: 'HIGH',
      CreatedAt: new Date().toISOString(),
      Parameters: [
        {
          Label: 'asset',
          Value: asset,
          DataType: 'string'
        },
        {
          Label: 'current_price',
          Value: price.toString(),
          DataType: 'number'
        },
        {
          Label: 'threshold',
          Value: threshold.toString(),
          DataType: 'number'
        },
        {
          Label: 'direction',
          Value: price >= threshold ? 'above' : 'below',
          DataType: 'string'
        }
      ]
    };
    
    await this.store.saveNotification(notification);
    return notification;
  }

  async produceAdminAnnouncement(userIds, subject, body, parameters = []) {
    const notification = {
      Key: `admin_${Date.now()}`,
      Type: 'ADMIN_ANNOUNCEMENT',
      To: userIds, // Can be array for bulk
      From: 'admin',
      Priority: 'MEDIUM',
      CreatedAt: new Date().toISOString(),
      Subject: subject,
      Body: body,
      Parameters: parameters
    };
    
    await this.store.saveBulkNotification(notification);
    return notification;
  }
}

// Usage
const producer = new NotificationProducer(notificationStoreClient);

// Transaction received
await producer.produceTransactionReceived('user123', {
  hash: 'txn_abc123',
  amount: 250.75,
  currency: 'XRP',
  sender
 sender: 'rSenderAddress',
  senderName: 'John Doe'
});

// NFT purchase
await producer.produceNFTBought('user123', 
  { id: 'nft_456', name: 'CryptoPunk #1234' },
  { price: 5000, currency: 'USD', seller: 'rSellerAddress', txHash: '0xabc...' }
);
Python Consumer Display Rules
python
# Display rules for different consumers
class NotificationDisplayRules:
    def __init__(self, i18n_manager):
        self.i18n = i18n_manager
    
    def format_for_web(self, notification, language='en-US'):
        """Format notification for web UI"""
        subject = self._get_localized_text(
            notification.get('Type'), 
            'subject', 
            notification.get('Subject'),
            language
        )
        
        body = self._get_localized_text(
            notification.get('Type'),
            'body',
            notification.get('Body'),
            language
        )
        
        # Replace placeholders
        subject = self._replace_placeholders(subject, notification.get('Parameters', []))
        body = self._replace_placeholders(body, notification.get('Parameters', []))
        
        # Apply web-specific formatting
        body = self._apply_web_formatting(body, notification.get('Parameters', []))
        
        return {
            'id': notification.get('ID'),
            'subject': subject,
            'body': body,
            'read': notification.get('Read', False),
            'priority': notification.get('Priority'),
            'timestamp': notification.get('CreatedAt'),
            'html': self._generate_html(subject, body, notification)
        }
    
    def format_for_telegram(self, notification, language='en-US'):
        """Format notification for Telegram"""
        subject = self._get_localized_text(
            notification.get('Type'),
            'subject',
            notification.get('Subject'),
            language
        )
        
        body = self._get_localized_text(
            notification.get('Type'),
            'body',
            notification.get('Body'),
            language
        )
        
        # Replace placeholders
        subject = self._replace_placeholders(subject, notification.get('Parameters', []))
        body = self._replace_placeholders(body, notification.get('Parameters', []))
        
        # Telegram markdown formatting
        message = f"*{subject}*\n\n{body}"
        
        return message
    
    def format_for_email(self, notification, language='en-US'):
        """Format notification for email"""
        subject = self._get_localized_text(
            notification.get('Type'),
            'subject',
            notification.get('Subject'),
            language
        )
        
        body = self._get_localized_text(
            notification.get('Type'),
            'body',
            notification.get('Body'),
            language
        )
        
        # Replace placeholders
        subject = self._replace_placeholders(subject, notification.get('Parameters', []))
        body = self._replace_placeholders(body, notification.get('Parameters', []))
        
        # HTML email template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><style>body {{ font-family: Arial, sans-serif; }}</style></head>
        <body>
            <h2>{subject}</h2>
            <p>{body}</p>
            <hr>
            <small>Sologenic Notification</small>
        </body>
        </html>
        """
        
        return {'subject': subject, 'html': html}
    
    def _get_localized_text(self, notif_type, field, fallback, language):
        key = f"{notif_type}_{field}"
        text = self.i18n.get(key, language)
        return text if text else fallback
    
    def _replace_placeholders(self, text, parameters):
        if not text:
            return text
        
        param_map = {p['Label']: p['Value'] for p in parameters}
        
        for label, value in param_map.items():
            text = text.replace(f'{{{{{label}}}}}', value)
        
        return text
    
    def _apply_web_formatting(self, text, parameters):
        # Convert URLs to links
        for param in parameters:
            if param.get('DataType') == 'url':
                text = text.replace(
                    param['Value'],
                    f'<a href="{param["Value"]}" target="_blank">{param["Value"]}</a>'
                )
            elif param.get('DataType') == 'image':
                text = text.replace(
                    param['Value'],
                    f'<img src="{param["Value"]}" alt="{param["Label"]}" style="max-width: 100%;">'
                )
        
        return text
    
    def _generate_html(self, subject, body, notification):
        priority_class = {
            'HIGH': 'priority-high',
            'MEDIUM': 'priority-medium',
            'LOW': 'priority-low'
        }.get(notification.get('Priority'), 'priority-medium')
        
        return f"""
        <div class="notification {priority_class}">
            <div class="notification-header">
                <strong>{subject}</strong>
                <small>{notification.get('CreatedAt')}</small>
            </div>
            <div class="notification-body">{body}</div>
            {'' if notification.get('Read') else '<div class="unread-badge">New</div>'}
        </div>
        """
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	com-be-http-lib
AUTH_FIREBASE_SERVICE	Firebase authentication	com-fs-auth-firebase-service
USER_STORE	User service endpoint	com-fs-user-model
ROLE_STORE	Role service endpoint	com-fs-role-model
ORGANIZATION_STORE	Organization service endpoint	com-fs-organization-model
NOTIFICATION_STORE	Notification store endpoint	com-fs-notification-model
Optional Environment Variables
Environment Variable	Description	Source
FEATURE_FLAG_STORE	Feature flag service	com-fs-feature-flag-model
Example Environment Configuration
bash
# Required
NOTIFICATION_STORE=notification-store:50059
USER_STORE=user-service:50049
ROLE_STORE=role-store:50066
ORGANIZATION_STORE=organization-service:50060
AUTH_FIREBASE_SERVICE=auth-service:50070

# Optional
FEATURE_FLAG_STORE=feature-flag-store:50055
LOG_LEVEL=info
BATCH_SIZE=100
MAX_KEYS_PER_READ=100

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
Docker Compose Example
yaml
version: '3.8'

services:
  notification-service:
    image: sologenic/notification-service:latest
    environment:
      - NOTIFICATION_STORE=notification-store:50059
      - USER_STORE=user-service:50049
      - ROLE_STORE=role-store:50066
      - ORGANIZATION_STORE=organization-service:50060
      - AUTH_FIREBASE_SERVICE=auth-service:50070
      - LOG_LEVEL=info
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
    networks:
      - internal

  notification-store:
    image: sologenic/notification-store:latest
    environment:
      - DATABASE_URL=postgres://user:pass@postgres:5432/notifications
    networks:
      - internal

  user-service:
    image: sologenic/user-service:latest
    networks:
      - internal

networks:
  internal:
    driver: bridge
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
  "message": "Access denied for this resource"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid type parameter",
  "valid_values": ["admin", "marketing", "maintenance"]
}
Bad Request (400) - Too Many Keys
json
{
  "error": "Bad Request",
  "message": "Too many keys in request",
  "max_keys": 100,
  "received": 150
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Notification not found"
}
Internal Server Error (500)
json
{
  "error": "Internal Server Error",
  "message": "Failed to retrieve notifications",
  "request_id": "req_12345"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Notifications not showing	Wrong OrganizationID	Verify organization header
Mark read slow	Too many keys	Limit to 100 keys per request
Duplicate read requests	FE not optimistic	Implement optimistic updates
Missing translations	i18n key missing	Add translation for notification type
Pagination not working	Invalid More params	Use exact values from previous response
Top auth empty	Wrong type filter	Use admin, marketing, maintenance only
Debugging Commands
bash
# Check unread status
curl -X GET "https://api.sologenic.org/api/notification/unread" \
  -H "Authorization: Bearer: $TOKEN" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v

# Get top auth notifications
curl -X GET "https://api.sologenic.org/api/notification/topauth?type=admin,maintenance" \
  -H "Authorization: Bearer: $TOKEN" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v | jq '.Notifications[] | {type: .Type, subject: .Subject}'

# List notifications with pagination
curl -X GET "https://api.sologenic.org/api/notification/list" \
  -H "Authorization: Bearer: $TOKEN" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v | jq '{count: .Notifications | length, has_more: .More != null}'

# Mark notification as read
curl -X PUT "https://api.sologenic.org/api/notification/read" \
  -H "Authorization: Bearer: $TOKEN" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -d '{"Key": ["notification_key_1", "notification_key_2"]}' \
  -v
Best Practices
Producer Guidelines
Practice	Recommendation
Static messages	Include all dynamic values at creation time
Parameter labels	Use consistent enum values across services
Source field	Always populate Source for navigable items
FromTo usage	Max 2 parameters with FromTo (1 From, 1 To)
DataType accuracy	Set correct DataType for proper formatting
Consumer Guidelines
Practice	Recommendation
Optimistic updates	Mark read locally before API response
Rate limiting	Don't poll too frequently (use WebSockets for real-time)
Pagination	Always handle More object for complete history
Error handling	Revert optimistic updates on failure
Accessibility	Ensure proper ARIA labels for notification elements
Performance Guidelines
Practice	Recommendation
Batch mark read	Combine multiple keys in single request
Limit initial load	Start with 20-50 notifications
Virtual scrolling	Use for large notification lists
Caching	Cache unread status with short TTL
WebSocket	Use for real-time notifications instead of polling
Related Services
Service	Description
Notification Store	Persistence layer for notifications
User Store	User preferences and settings
Role Store	Permission management for admin notifications
Organization Store	Tenant isolation
Auth Firebase Service	Authentication and user identification
Feature Flag Store	Notification feature toggles
License
This documentation is part of the TX Marketplace platform.
