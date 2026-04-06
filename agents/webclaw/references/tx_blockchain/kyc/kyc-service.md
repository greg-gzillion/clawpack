# KYC Service (be-kyc-service)

The KYC Service handles Know Your Customer (KYC) operations for Sologenic.com. This service manages KYC admin interface interactions and integrations with **Sumsub** for KYC verifications.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ KYC Service Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ REST API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ GET /kyc/get │ GET /kyc/count│ GET /kyc/list │ POST /kyc/status │ │
│ │ (Get record) │ (Count by │ (List │ (Update status) │ │
│ │ │ status) │ accounts) │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ KYC Admin Functions │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Mark as │ Send Ticket │ Reprocess │ Authorize Account │ │
│ │ NotProcessable│ to Devs │ Records │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Integrations │ │
│ ├─────────────────────────────┬───────────────────────────────────────┤ │
│ │ Sumsub KYC Provider │ Internal Services │ │
│ │ • Applicant verification │ • Organization Store │ │
│ │ • Document validation │ • Auth Service │ │
│ │ • Fraud detection │ • Account Store │ │
│ └─────────────────────────────┴───────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /kyc/get | KYC_ADMIN | Retrieve KYC record by external user ID |
| GET /kyc/count | KYC_ADMIN | Get count of KYC records by status |
| GET /kyc/list | KYC_ADMIN | List accounts with optional status filter |
| POST /kyc/status | KYC_ADMIN | Update KYC record status |

**Note:** All authenticated requests must include:
- `Authorization` header (Bearer token)
- `Network` header (mainnet, testnet, devnet)

## Data Models

### KYC Record Object

| Field | Type | Description |
|-------|------|-------------|
| AccountID | string | Internal account identifier |
| ExternalUserID | string | External user identifier |
| ParticipantID | string | Sumsub participant ID |
| KYCProvider | int | Provider type (1 = Sumsub) |
| Status | int | Current KYC status (see Status Codes) |
| AdminComment | string | Optional admin comment |
| FirstSeen | Timestamp | First time record was seen |
| UpdatedAt | Timestamp | Last update timestamp |
| ApprovedAt | []Timestamp | Approval timestamps (if approved multiple times) |
| Documents | []string | List of document references |
| Details | Details | KYC details (applicant info, review) |
| Network | string | Network environment |
| OrganizationID | string | Organization UUID |

### Status Codes

| Status Code | Status Name | Description |
|-------------|-------------|-------------|
| 1 | INIT | Initial state, KYC not started |
| 2 | APPROVED | KYC approved (auto or admin) |
| 3 | ADMIN_DENIED | Admin denied regardless of KYC status |
| 4 | PENDING | KYC verification in progress |
| 5 | RE_REQUESTED | KYC re-requested (reset process) |
| 6 | FAILED | KYC verification failed |
| 7 | NOT_PROCESSABLE_FOREVER | Cannot be processed |
| 8 | FIX_REQUIRED | Stuck record needs developer attention |

### KYC Provider Types

| Provider ID | Provider Name | Description |
|-------------|---------------|-------------|
| 1 | Sumsub | Primary KYC provider |

### Applicant Info Object

| Field | Type | Description |
|-------|------|-------------|
| FirstName | string | Applicant's first name |
| LastName | string | Applicant's last name |
| DOB | string | Date of birth |
| Country | string | Country of residence |
| Addresses | []Address | List of addresses |

### Address Object

| Field | Type | Description |
|-------|------|-------------|
| Country | string | Country |
| Town | string | Town/City |
| State | string | State/Province |
| PostCode | string | Postal code |
| Street | string | Street name |
| SubStreet | string | Sub-street (optional) |
| FlatNumber | string | Apartment/flat number |
| BuildingNumber | string | Building number |

### Review Object

| Field | Type | Description |
|-------|------|-------------|
| ReviewID | string | Sumsub review identifier |
| LevelName | string | Review level name |
| ReviewResult | ReviewResult | Detailed review result |

### ReviewResult Object

| Field | Type | Description |
|-------|------|-------------|
| ReviewAnswer | int | 1=GREEN (approved), 2=RED (rejected) |
| RejectLabels | []string | Labels for rejection reasons |
| ReviewResultType | int | Type of review result |
| ClientComment | string | Client-facing comment |
| ModerationComment | string | Internal moderation comment |
| ButtonIDs | []string | Action button IDs |
| ReviewStatus | int | Review status code |

### Account List Object

| Field | Type | Description |
|-------|------|-------------|
| ID | string | Account ID |
| FirstName | string | User's first name |
| LastName | string | User's last name |
| Address | string | Account address |
| Wallets | []Wallet | Associated wallets |
| CreatedAt | Timestamp | Account creation time |
| UpdatedAt | Timestamp | Last update time |
| Socials | []Social | Social media links |
| Avatar | string | Avatar URL |
| Alias | string | User alias |
| Description | string | User description |
| Network | string | Network environment |
| Status | int | Account status |
| Roles | []int | User roles |
| ExternalUserID | string | External user ID |
| OrganizationID | string | Organization UUID |

### Wallet Object

| Field | Type | Description |
|-------|------|-------------|
| Address | string | Wallet address |
| Alias | string | Wallet alias |
| Type | int | Wallet type (1=XRP, 2=ETH, 3=BTC, etc.) |

### Social Object

| Field | Type | Description |
|-------|------|-------------|
| URL | string | Social media profile URL |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

## API Endpoints

### GET /kyc/get

Retrieves a KYC record by external user ID.

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| external_user_id | string | External user identifier | Yes |

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Authorization | Bearer token | Yes |
| Network | mainnet, testnet, devnet | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.sologenic.org/kyc/get?external_user_id=a9ab4580-7f8f-7889-2df6-d774ce8921a7" \
  -H "Content-Type: application/json" \
  -H "Authorization: eyJQcml2YXRlS2...someEncodedToken...OGY0ZSJ9" \
  -H "Network: testnet"
Example Response
json
{
  "AccountID": "0660ba9a-8423-9c53-eb0d-ae6ebb848544",
  "ExternalUserID": "a9ab4580-7f8f-7889-2df6-d774ce8921a7",
  "ParticipantID": "6675aa52-e05f-5b4f-a3ea-625858433d78",
  "KYCProvider": 1,
  "Status": 6,
  "AdminComment": "action required",
  "FirstSeen": {
    "seconds": 326,
    "nanos": 223
  },
  "UpdatedAt": {
    "seconds": 1720466106,
    "nanos": 46857000
  },
  "ApprovedAt": [
    {"seconds": 739, "nanos": 88},
    {"seconds": 825, "nanos": 296}
  ],
  "Documents": [
    "artificial intelligence",
    "Jamaican Dollar"
  ],
  "Details": {
    "SourceKey": "District Branding Handmade Wooden Car",
    "Email": "Hoyt.Borer@example.com",
    "Phone": "(890) 754-3139",
    "ApplicantInfo": {
      "FirstName": "Alanis",
      "LastName": "Hyatt",
      "DOB": "salmon Spring mobile",
      "Country": "Tokelau",
      "Addresses": [
        {
          "Country": "24/365",
          "Town": "azure Extended",
          "State": "Hawaii",
          "PostCode": "Liaison Kansas homogeneous",
          "Street": "Vandervort Crest",
          "SubStreet": "Accounts Cotton",
          "FlatNumber": "12267",
          "BuildingNumber": "459"
        }
      ]
    },
    "Review": {
      "ReviewID": "5f23aba3-045f-28b1-3742-0827ab07c379",
      "LevelName": "Fantastic Granite Tuna invoice",
      "ReviewResult": {
        "ReviewAnswer": 1,
        "RejectLabels": [
          "index Dynamic Berkshire",
          "red bypassing Unbranded Wooden Tuna"
        ],
        "ReviewResultType": 1,
        "ClientComment": "Turkey JBOD open-source",
        "ModerationComment": "Representative Investor Lake",
        "ButtonIDs": [
          "Usability driver",
          "sensor Industrial"
        ],
        "ReviewStatus": 3
      }
    }
  },
  "Network": "mainnet",
  "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca"
}
GET /kyc/count
Retrieves the count of KYC records categorized by their current status.

Query Parameters
Parameter	Type	Description	Required
status	string	KYC status (INIT, APPROVED, PENDING, FAILED, etc.)	Yes
Headers
Header	Description	Required
Authorization	Bearer token	Yes
Network	mainnet, testnet, devnet	Yes
Example Request
bash
curl -X GET \
  "https://api.sologenic.org/kyc/count?status=APPROVED" \
  -H "Content-Type: application/json" \
  -H "Authorization: eyJQcml2YXRlS2...someEncodedToken...OGY0ZSJ9" \
  -H "Network: testnet"
Example Response
json
{
  "Count": 1,
  "KYCStatus": 3
}
GET /kyc/list
Retrieves a list of accounts with optional status filtering.

Query Parameters
Parameter	Type	Description	Required
status	string	Filter by KYC status	No
Headers
Header	Description	Required
Authorization	Bearer token	Yes
Network	mainnet, testnet, devnet	Yes
Example Request
bash
curl -X GET \
  "https://api.sologenic.org/kyc/list?status=APPROVED" \
  -H "Content-Type: application/json" \
  -H "Authorization: eyJQcml2YXRlS2...someEncodedToken...OGY0ZSJ9" \
  -H "Network: testnet"
Example Response
json
{
  "Accounts": [
    {
      "ID": "2461396b-8244-d8e2-4a25-bdb8d5b66710",
      "FirstName": "Karlie",
      "LastName": "Hills",
      "Address": "ABC2",
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
        "seconds": 1720464107,
        "nanos": 757227000
      },
      "UpdatedAt": {
        "seconds": 694,
        "nanos": 721
      },
      "Socials": [
        {"URL": "https://drew.net"},
        {"URL": "https://ephraim.net"}
      ],
      "Avatar": "https://cloudflare-ipfs.com/ipfs/Qmd3W5DuhgHirLHGVixi6V76LhCkZUz6pnFt5AJBiyvHye/avatar/1005.jpg",
      "Alias": "ABC2",
      "Description": "invoice back up",
      "Network": "mainnet",
      "Status": 1,
      "Roles": [1],
      "ExternalUserID": "6b5118f7-1912-5d6e-6b7f-c6036a517af1",
      "OrganizationID": "34422ce6-7b51-4a15-accb-34959f39d8ca"
    }
  ]
}
POST /kyc/status
Updates the status of a KYC record with optional admin comment.

Request Body
Field	Type	Description	Required
externalUserID	string	External user identifier	Yes
kycStatus	string	New KYC status (see Status Values below)	Yes
adminComment	string	Optional admin comment	No
Status Values for Update
Status Value	Code	Description	Warnings
APPROVED	2	Admin approval bypassing KYC	Use with caution - overrides standard process
ADMIN_DENIED	3	Admin denial regardless of application	Internal only, doesn't affect Sumsub
RE_REQUESTED	5	Reset and restart KYC process	Fails if fraud patterns detected
NOT_PROCESSABLE_FOREVER	7	Mark as unprocessable	Records reason for failure
FIX_REQUIRED	8	Notify dev team of stuck record	Creates support ticket
Headers
Header	Description	Required
Authorization	Bearer token (KYC_ADMIN role)	Yes
Network	mainnet, testnet, devnet	Yes
Content-Type	application/json	Yes
Example Request
bash
curl -X POST \
  "https://api.sologenic.org/kyc/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: eyJQcml2YXRlS2...someEncodedToken...OGY0ZSJ9" \
  -H "Network: testnet" \
  -d '{
    "externalUserID": "e1aad668-3af1-a4b4-557e-05ae7ca21d72",
    "kycStatus": "RE_REQUESTED",
    "adminComment": "user's first name has changed, re-request KYC process"
  }'
Example Response
json
{
  "UpdatedAt": {
    "seconds": 1720469737,
    "nanos": 116377000
  }
}
Admin Workflow
KYC Admin Overview Dashboard
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        KYC Admin Dashboard Workflow                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Overview Page                                                    │   │
│  │    • Display count of "stuck" records (status = FIX_REQUIRED)       │   │
│  │    • Show total pending, approved, failed counts                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. User List View (GET /kyc/list)                                   │   │
│  │    • Filter by status (stuck, pending, approved, failed)            │   │
│  │    • Order by updated datetime DESC                                 │   │
│  │    • Mark records as "Not Processable"                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. Record Actions                                                   │   │
│  │    • Mark as NOT_PROCESSABLE_FOREVER (POST /kyc/mark/{id})          │   │
│  │    • Send ticket to developers (POST /kyc/notif/{id})               │   │
│  │    • Reprocess single record (POST /kyc/reprocess/{id})             │   │
│  │    • Reprocess all stuck records (POST /kyc/reprocess/all)          │   │
│  │    • Authorize account (POST /kyc/authorize/{id})                   │   │
│  │    • Notify user of completion (POST /kyc/notify/{id})              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Pending Admin Endpoints (Not Yet Implemented)
The following endpoints are planned for future implementation:

Endpoint	Method	Description
/kyc/mark/{id}	POST	Mark record as NOT_PROCESSABLE_FOREVER
/kyc/notif/{id}	POST	Send ticket to developers for stuck record
/kyc/reprocess/{ids}	POST	Reprocess stuck records (single or bulk)
/kyc/create	POST	Create account on behalf of user
/kyc/authorize/{id}	POST	Authorize a user account
/kyc/notify/{id}	POST	Send notification when KYC is complete
/user/{query}	GET	View user details with search/filter
Integration Examples
Node.js KYC Admin Client
javascript
class KYCServiceClient {
  constructor(baseUrl, token, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.token = token;
    this.network = network;
  }

  async getKYCRecord(externalUserId) {
    const response = await fetch(
      `${this.baseUrl}/kyc/get?external_user_id=${encodeURIComponent(externalUserId)}`,
      {
        headers: this._getHeaders()
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch KYC record: ${response.statusText}`);
    }

    return response.json();
  }

  async getKYCCount(status) {
    const response = await fetch(
      `${this.baseUrl}/kyc/count?status=${status}`,
      {
        headers: this._getHeaders()
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch KYC count: ${response.statusText}`);
    }

    return response.json();
  }

  async listAccounts(status = null) {
    const url = status 
      ? `${this.baseUrl}/kyc/list?status=${status}`
      : `${this.baseUrl}/kyc/list`;
    
    const response = await fetch(url, {
      headers: this._getHeaders()
    });

    if (!response.ok) {
      throw new Error(`Failed to list accounts: ${response.statusText}`);
    }

    return response.json();
  }

  async updateKYCStatus(externalUserID, kycStatus, adminComment = '') {
    const response = await fetch(
      `${this.baseUrl}/kyc/status`,
      {
        method: 'POST',
        headers: {
          ...this._getHeaders(),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          externalUserID,
          kycStatus,
          adminComment
        })
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to update KYC status: ${response.statusText}`);
    }

    return response.json();
  }

  async getStuckRecordsCount() {
    return this.getKYCCount('FIX_REQUIRED');
  }

  async getPendingRecords() {
    return this.listAccounts('PENDING');
  }

  async approveKYC(externalUserID, comment = 'Admin approved') {
    return this.updateKYCStatus(externalUserID, 'APPROVED', comment);
  }

  async denyKYC(externalUserID, comment = 'Admin denied') {
    return this.updateKYCStatus(externalUserID, 'ADMIN_DENIED', comment);
  }

  async reRequestKYC(externalUserID, comment = 'Re-requested by admin') {
    return this.updateKYCStatus(externalUserID, 'RE_REQUESTED', comment);
  }

  async markNotProcessable(externalUserID, comment = 'Cannot process this record') {
    return this.updateKYCStatus(externalUserID, 'NOT_PROCESSABLE_FOREVER', comment);
  }

  async markFixRequired(externalUserID, comment = 'Stuck record needs developer attention') {
    return this.updateKYCStatus(externalUserID, 'FIX_REQUIRED', comment);
  }

  _getHeaders() {
    return {
      'Authorization': this.token,
      'Network': this.network
    };
  }
}

// Usage example
async function adminDashboard() {
  const client = new KYCServiceClient(
    'https://api.sologenic.org',
    'eyJQcml2YXRlS2...someEncodedToken...OGY0ZSJ9',
    'mainnet'
  );

  // Get dashboard statistics
  const pendingCount = await client.getKYCCount('PENDING');
  const approvedCount = await client.getKYCCount('APPROVED');
  const failedCount = await client.getKYCCount('FAILED');
  const stuckCount = await client.getKYCCount('FIX_REQUIRED');

  console.log('KYC Dashboard:');
  console.log(`  Pending: ${pendingCount.Count}`);
  console.log(`  Approved: ${approvedCount.Count}`);
  console.log(`  Failed: ${failedCount.Count}`);
  console.log(`  Stuck (Fix Required): ${stuckCount.Count}`);

  // Get pending accounts for review
  const pendingAccounts = await client.getPendingRecords();
  console.log(`\nPending Accounts: ${pendingAccounts.Accounts.length}`);

  // Process a stuck record
  if (stuckCount.Count > 0) {
    const stuckAccounts = await client.listAccounts('FIX_REQUIRED');
    const firstStuck = stuckAccounts.Accounts[0];
    
    await client.reRequestKYC(
      firstStuck.ExternalUserID,
      'Re-requesting due to stuck status'
    );
    console.log(`\nRe-requested KYC for user: ${firstStuck.ExternalUserID}`);
  }
}
React KYC Admin Dashboard
jsx
import React, { useState, useEffect } from 'react';

function KYCDashboard() {
  const [stats, setStats] = useState({
    pending: 0,
    approved: 0,
    failed: 0,
    stuck: 0
  });
  const [accounts, setAccounts] = useState([]);
  const [selectedStatus, setSelectedStatus] = useState('PENDING');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, [selectedStatus]);

  const loadDashboard = async () => {
    setLoading(true);
    try {
      // Load statistics
      const [pending, approved, failed, stuck] = await Promise.all([
        fetchKYCCount('PENDING'),
        fetchKYCCount('APPROVED'),
        fetchKYCCount('FAILED'),
        fetchKYCCount('FIX_REQUIRED')
      ]);

      setStats({
        pending: pending.Count,
        approved: approved.Count,
        failed: failed.Count,
        stuck: stuck.Count
      });

      // Load accounts for selected status
      const accountsData = await listAccounts(selectedStatus);
      setAccounts(accountsData.Accounts || []);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchKYCCount = async (status) => {
    const response = await fetch(`/kyc/count?status=${status}`, {
      headers: getHeaders()
    });
    return response.json();
  };

  const listAccounts = async (status) => {
    const response = await fetch(`/kyc/list?status=${status}`, {
      headers: getHeaders()
    });
    return response.json();
  };

  const updateKYCStatus = async (externalUserID, kycStatus, adminComment) => {
    const response = await fetch('/kyc/status', {
      method: 'POST',
      headers: {
        ...getHeaders(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        externalUserID,
        kycStatus,
        adminComment
      })
    });

    if (!response.ok) {
      throw new Error('Failed to update status');
    }

    return response.json();
  };

  const getHeaders = () => ({
    'Authorization': localStorage.getItem('token'),
    'Network': 'mainnet'
  });

  const getStatusBadgeClass = (status) => {
    const classes = {
      'INIT': 'badge-secondary',
      'PENDING': 'badge-warning',
      'APPROVED': 'badge-success',
      'FAILED': 'badge-danger',
      'ADMIN_DENIED': 'badge-danger',
      'FIX_REQUIRED': 'badge-danger',
      'NOT_PROCESSABLE_FOREVER': 'badge-dark'
    };
    return classes[status] || 'badge-info';
  };

  const handleApprove = async (account) => {
    if (window.confirm(`Approve KYC for ${account.FirstName} ${account.LastName}?`)) {
      await updateKYCStatus(account.ExternalUserID, 'APPROVED', 'Admin approved');
      await loadDashboard();
    }
  };

  const handleDeny = async (account) => {
    const reason = prompt('Enter denial reason:');
    if (reason) {
      await updateKYCStatus(account.ExternalUserID, 'ADMIN_DENIED', reason);
      await loadDashboard();
    }
  };

  const handleReRequest = async (account) => {
    if (window.confirm(`Re-request KYC for ${account.FirstName} ${account.LastName}?`)) {
      await updateKYCStatus(account.ExternalUserID, 'RE_REQUESTED', 'Re-requested by admin');
      await loadDashboard();
    }
  };

  const handleMarkFixRequired = async (account) => {
    await updateKYCStatus(account.ExternalUserID, 'FIX_REQUIRED', 'Marked for developer fix');
    await loadDashboard();
  };

  return (
    <div className="kyc-dashboard">
      <h1>KYC Admin Dashboard</h1>

      {/* Statistics Cards */}
      <div className="stats-grid">
        <div className="stat-card pending">
          <h3>Pending</h3>
          <p className="stat-number">{stats.pending}</p>
        </div>
        <div className="stat-card approved">
          <h3>Approved</h3>
          <p className="stat-number">{stats.approved}</p>
        </div>
        <div className="stat-card failed">
          <h3>Failed</h3>
          <p className="stat-number">{stats.failed}</p>
        </div>
        <div className="stat-card stuck">
          <h3>Stuck (Fix Required)</h3>
          <p className="stat-number">{stats.stuck}</p>
        </div>
      </div>

      {/* Status Filter */}
      <div className="filter-bar">
        <label>Filter by Status: </label>
        <select 
          value={selectedStatus} 
          onChange={(e) => setSelectedStatus(e.target.value)}
        >
          <option value="PENDING">Pending</option>
          <option value="APPROVED">Approved</option>
          <option value="FAILED">Failed</option>
          <option value="FIX_REQUIRED">Stuck (Fix Required)</option>
          <option value="ADMIN_DENIED">Denied</option>
          <option value="NOT_PROCESSABLE_FOREVER">Not Processable</option>
        </select>
        <button onClick={loadDashboard} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {/* Accounts Table */}
      <div className="accounts-table">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {accounts.map((account) => (
              <tr key={account.ID}>
                <td>{account.FirstName} {account.LastName}</td>
                <td>{account.Email || 'N/A'}</td>
                <td>
                  <span className={`badge ${getStatusBadgeClass(account.Status)}`}>
                    {account.Status}
                  </span>
                </td>
                <td>{new Date(account.CreatedAt.seconds * 1000).toLocaleDateString()}</td>
                <td className="actions">
                  {account.Status === 'PENDING' && (
                    <>
                      <button onClick={() => handleApprove(account)} className="btn-success">
                        Approve
                      </button>
                      <button onClick={() => handleDeny(account)} className="btn-danger">
                        Deny
                      </button>
                    </>
                  )}
                  {(account.Status === 'FAILED' || account.Status === 'FIX_REQUIRED') && (
                    <>
                      <button onClick={() => handleReRequest(account)} className="btn-warning">
                        Re-request
                      </button>
                      <button onClick={() => handleMarkFixRequired(account)} className="btn-info">
                        Mark Fix Required
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default KYCDashboard;
Python KYC Admin Client
python
import requests
from typing import Optional, Dict, List
from datetime import datetime

class KYCServiceClient:
    def __init__(self, base_url: str, token: str, network: str = 'mainnet'):
        self.base_url = base_url
        self.token = token
        self.network = network
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': self.token,
            'Network': self.network
        }
    
    def get_kyc_record(self, external_user_id: str) -> Dict:
        """Get KYC record by external user ID"""
        response = requests.get(
            f'{self.base_url}/kyc/get',
            params={'external_user_id': external_user_id},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_kyc_count(self, status: str) -> Dict:
        """Get count of KYC records by status"""
        response = requests.get(
            f'{self.base_url}/kyc/count',
            params={'status': status},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def list_accounts(self, status: Optional[str] = None) -> Dict:
        """List accounts with optional status filter"""
        params = {'status': status} if status else {}
        response = requests.get(
            f'{self.base_url}/kyc/list',
            params=params,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def update_kyc_status(self, external_user_id: str, kyc_status: str, admin_comment: str = '') -> Dict:
        """Update KYC record status"""
        response = requests.post(
            f'{self.base_url}/kyc/status',
            headers={
                **self._get_headers(),
                'Content-Type': 'application/json'
            },
            json={
                'externalUserID': external_user_id,
                'kycStatus': kyc_status,
                'adminComment': admin_comment
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_dashboard_stats(self) -> Dict:
        """Get comprehensive dashboard statistics"""
        statuses = ['PENDING', 'APPROVED', 'FAILED', 'FIX_REQUIRED', 'ADMIN_DENIED']
        stats = {}
        
        for status in statuses:
            result = self.get_kyc_count(status)
            stats[status.lower()] = result.get('Count', 0)
        
        return stats
    
    def get_stuck_records(self) -> List[Dict]:
        """Get all stuck records requiring developer attention"""
        result = self.list_accounts('FIX_REQUIRED')
        return result.get('Accounts', [])
    
    def bulk_reprocess_stuck(self) -> List[Dict]:
        """Reprocess all stuck records (requires endpoint implementation)"""
        # This would call POST /kyc/reprocess/all
        pass

# Usage example
def generate_kyc_report():
    client = KYCServiceClient(
        base_url='https://api.sologenic.org',
        token='eyJQcml2YXRlS2...someEncodedToken...OGY0ZSJ9',
        network='mainnet'
    )
    
    # Get dashboard statistics
    stats = client.get_dashboard_stats()
    
    print("KYC Service Report")
    print("=" * 50)
    print(f"Pending: {stats['pending']}")
    print(f"Approved: {stats['approved']}")
    print(f"Failed: {stats['failed']}")
    print(f"Stuck (Fix Required): {stats['fix_required']}")
    print(f"Admin Denied: {stats['admin_denied']}")
    
    # Get detailed stuck records
    stuck_records = client.get_stuck_records()
    if stuck_records:
        print(f"\nStuck Records Details ({len(stuck_records)}):")
        for record in stuck_records:
            print(f"  - {record['FirstName']} {record['LastName']} (ID: {record['ExternalUserID']})")
            print(f"    Created: {datetime.fromtimestamp(record['CreatedAt']['seconds'])}")
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
ORGANIZATION_STORE	Organization service endpoint	com-fs-organization-model
AUTH_SERVICE	Auth gRPCservice endpoint	-
ACCOUNT_STORE	Account gRPC service endpoint	-
OPEN_SEARCH_STORE	Open search gRPC service endpoint	-
HTTP_CONFIG	HTTP server configuration	com-be-http-lib
Example Environment Configuration
bash
# Required
ORGANIZATION_STORE=organization-service:50060
AUTH_SERVICE=auth-service:50070
ACCOUNT_STORE=account-store:50061
OPEN_SEARCH_STORE=open-search:50062

# Optional
LOG_LEVEL=info
KYC_PROVIDER=sumsub
SUMSUB_API_KEY=your_sumsub_api_key
SUMSUB_SECRET_KEY=your_sumsub_secret

# HTTP Configuration
HTTP_CONFIG='{
  "port": ":8080",
  "cors": {
    "allowedOrigins": ["http://localhost:3000", "https://admin.sologenic.org"]
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
  kyc-service:
    image: sologenic/be-kyc-service:latest
    environment:
      - ORGANIZATION_STORE=organization-service:50060
      - AUTH_SERVICE=auth-service:50070
      - ACCOUNT_STORE=account-store:50061
      - OPEN_SEARCH_STORE=open-search:50062
      - LOG_LEVEL=info
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
    networks:
      - internal

  organization-service:
    image: sologenic/organization-service:latest
    networks:
      - internal

  auth-service:
    image: sologenic/auth-service:latest
    networks:
      - internal

networks:
  internal:
    driver: bridge
Sumsub Integration
Sumsub Webhook Events
The KYC service listens for Sumsub webhook events to update KYC status automatically:

Event Type	Description	Action
applicantCreated	New applicant created	Create KYC record (INIT)
applicantPending	Verification started	Update status to PENDING
applicantApproved	Verification passed	Update status to APPROVED
applicantDeclined	Verification failed	Update status to FAILED
applicantReset	Applicant reset	Update status to INIT
applicantDeleted	Applicant deleted	Archive record
Fraud Detection Labels
The service checks for fraud patterns before allowing RE_REQUESTED status:

Label	Description
FORGERY	Document forgery detected
SELFIE_MISMATCH	Selfie doesn't match document
BLACKLIST	Applicant on blacklist
BLOCKLIST	Applicant on blocklist
INCONSISTENT_PROFILE	Profile information inconsistent
FRAUDULENT_PATTERNS	Fraudulent behavior detected
Error Responses
Not Found (404)
json
{
  "error": "Not Found",
  "message": "KYC record not found for external_user_id: a9ab4580-7f8f-7889-2df6-d774ce8921a7"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid status value",
  "valid_values": ["APPROVED", "ADMIN_DENIED", "RE_REQUESTED", "NOT_PROCESSABLE_FOREVER", "FIX_REQUIRED"]
}
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
  "message": "KYC_ADMIN role required for this operation"
}
Conflict (409) - Fraud Detected
json
{
  "error": "Conflict",
  "message": "Cannot re-request KYC for applicant with fraud patterns",
  "fraud_labels": ["FORGERY", "BLACKLIST"],
  "action_required": "Manual review required"
}
Internal Server Error (500)
json
{
  "error": "Internal Server Error",
  "message": "Failed to update KYC status in Sumsub",
  "request_id": "req_12345"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Record not found	Wrong external_user_id	Verify user exists in system
Status update fails	Invalid status transition	Check allowed status transitions
Fraud pattern error	Applicant flagged	Manual review required
Sumsub sync issue	Network connectivity	Check Sumsub API connectivity
Stuck records	Provider dashboard issue	Use FIX_REQUIRED to notify devs
RE_REQUESTED fails	Fraud labels present	Review before attempting
Debugging Commands
bash
# Test get endpoint
curl -X GET "https://api.sologenic.org/kyc/get?external_user_id=$USER_ID" \
  -H "Authorization: $TOKEN" \
  -H "Network: mainnet" \
  -v

# Test count endpoint
curl -X GET "https://api.sologenic.org/kyc/count?status=PENDING" \
  -H "Authorization: $TOKEN" \
  -H "Network: mainnet" \
  -v

# Test list endpoint
curl -X GET "https://api.sologenic.org/kyc/list?status=FIX_REQUIRED" \
  -H "Authorization: $TOKEN" \
  -H "Network: mainnet" \
  -v | jq '.Accounts[] | {id: .ID, name: .FirstName + " " + .LastName, status: .Status}'

# Test status update
curl -X POST "https://api.sologenic.org/kyc/status" \
  -H "Authorization: $TOKEN" \
  -H "Network: mainnet" \
  -H "Content-Type: application/json" \
  -d '{
    "externalUserID": "'$USER_ID'",
    "kycStatus": "RE_REQUESTED",
    "adminComment": "Test reprocessing"
  }' \
  -v
Best Practices
Security
Practice	Recommendation
Authentication	Always require valid bearer tokens
Authorization	Enforce KYC_ADMIN role for all endpoints
Audit logging	Log all status changes with admin comments
Rate limiting	Implement per-admin rate limits
Operations
Practice	Recommendation
Status transitions	Only allow valid status changes
Fraud checking	Always check fraud labels before RE_REQUESTED
Manual review	Require human review for fraud cases
Error handling	Provide clear error messages for failures
Data Management
Practice	Recommendation
PII handling	Encrypt sensitive applicant data
Retention	Follow compliance requirements for data retention
Backups	Regular backup of KYC records
Reconciliation	Regular sync with Sumsub
Related Services
Service	Description
Organization Service	Tenant isolation and organization management
Auth Service	Authentication and token validation
Account Service	Account creation and management
Notification Service	User notifications for KYC completion
License
This documentation is part of the TX Marketplace platform.
