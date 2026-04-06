# User Service

The User Service provides API interfaces that manage (normal) users within an organization, including user creation, updates, KYC processes, and organization management.

## Technical Requirements

⚠️ **This service must be ALWAYS on to process webhook data**

## API Endpoints Overview

### Unauthenticated Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/get/alias` | Retrieves user aliases for a filter |
| POST | `/api/user/create` | Creates a new user under an organization |
| POST | `/api/kyc/webhook` | KYC Provider webhook for events |

### Authenticated Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/get` | Retrieves user information |
| PUT | `/api/user/update` | Updates user information |
| PUT | `/api/user/disable` | Disables a user (self only) |
| PUT | `/api/user/addtoorg` | Adds user to an organization |
| POST | `/api/kyc/start` | Starts KYC process |

### Authentication Requirements

All authenticated endpoints require:
- Valid Firebase JWT token in `Authorization` header (format: `Bearer: eyJhb....`)
- User must have status `ACTIVE`
- `OrganizationID` header for tenant isolation
- `Network` header (mainnet, testnet, devnet)

## API Endpoints Details

### Unauthenticated Endpoints

#### GET /api/user/get/alias

Retrieves an array of user alias objects, each containing `ExternalUserID` and corresponding `Alias`.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filter | string | Yes | Base64-encoded JSON filter object |

**Example Request:**

```bash
# Filter for specific external user IDs
FILTER=$(echo -n '{
  "ExternalUserIDs": [
    "f8bf69ad-ef98-42d6-9cd3-beea4d28542a",
    "1783880d-e667-4c88-b565-a6a8dfdf3925"
  ],
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Network": 2
}' | base64 -w 0)

curl -X GET "https://api.sologenic.org/api/user/get/alias?filter=${FILTER}" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet"
Example Response:

json
[
  {
    "ExternalID": "00234946-010d-4c6e-abf1-dee6836c4e20",
    "Alias": "test"
  },
  {
    "ExternalID": "441e9c6e-f1b2-407d-a557-af89bcbc46a2",
    "Alias": "Verna"
  },
  {
    "ExternalID": "79f56dbc-d1d1-4448-9138-723f23ddae27",
    "Alias": "Joannie"
  },
  {
    "ExternalID": "e0c1672e-8a2d-4201-ac54-3043f847c19b",
    "Alias": "Justine"
  },
  {
    "ExternalID": "e605dbf1-db61-441e-8bff-df66d209a492",
    "Alias": "Sidney"
  }
]
POST /api/user/create
Creates a new user. UserID and ExternalUserID are generated automatically.

Headers:

Header	Required	Description
Network	Yes	mainnet, testnet, devnet
OrganizationID	Yes	Organization UUID
Content-Type	Yes	application/json
Request Body:

Field	Type	Required	Description
UserID	string	Yes	User email or identifier
FirstName	string	No	User's first name
LastName	string	No	User's last name
Address	string	No	Physical address
Avatar	string	No	Avatar URL
Alias	string	No	Display alias
Description	string	No	User description
Status	int	Yes	User status (1=active)
Wallets	[]Wallet	No	Associated wallets
Socials	[]Social	No	Social media links
Language	Language	No	Language preference
OrganizationID	string	Yes	Organization UUID
Employment	Employment	No	Employment information
Example Request:

bash
curl -X POST "https://api.sologenic.org/api/user/create" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "UserID": "randy.lahey@gmail.com",
    "FirstName": "Randy",
    "LastName": "Lahey",
    "Address": "123 Sunnyvale Trailer Park",
    "Avatar": "https://example.com/avatars/randy.png",
    "Alias": "Bobandy",
    "Description": "Assistant trailer park supervisor",
    "Status": 1,
    "Wallets": [
      {
        "Address": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
        "Alias": "Primary",
        "Type": 3
      }
    ],
    "Socials": [
      {
        "URL": "https://twitter.com/randy",
        "Type": 5
      }
    ],
    "Language": {
      "Language": "en-US"
    },
    "OrganizationID": "215a551d-9284-4f72-ae9d-9284f40d1340",
    "Employment": {
      "Employer": "Sunnyvale Trailer Park",
      "Position": "Assistant Supervisor"
    }
  }'
Example Response:

json
{
  "UserID": "randy.lahey@gmail.com",
  "Network": 1
}
POST /api/kyc/webhook
Allows KYC Provider to post events regarding inquiries and KYC processes of users.

Note: Service must be always on for goroutines to process data reliably.

Example Request:

bash
curl -X POST "https://api.sologenic.org/api/kyc/webhook" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -d '{
    "event": "kyc.completed",
    "userId": "user@example.com",
    "status": "approved",
    "timestamp": "2024-01-15T10:30:00Z"
  }'
Authenticated Endpoints
GET /api/user/get
Retrieves user information for the authenticated user.

Headers:

Header	Required	Description
Authorization	Yes	Bearer: Firebase JWT token
Network	Yes	mainnet, testnet, devnet
OrganizationID	Yes	Organization UUID
Example Request:

bash
curl -X GET "https://api.sologenic.org/api/user/get" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: mainnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
Example Response:

json
{
  "User": {
    "UserID": "test@gmail.com",
    "FirstName": "John",
    "LastName": "Doe",
    "Address": "123 Main Street, Apt 4B, Cityville, ST 12345",
    "Avatar": "https://example.com/avatars/johndoe.png",
    "Alias": "JD",
    "Description": "Blockchain enthusiast and investor",
    "Status": 1,
    "Wallets": [
      {
        "Address": "rU6K7V3Po4snVhBBaU29sesqs2qTQJWDw1",
        "Alias": "Primary Wallet",
        "Type": 3
      },
      {
        "Address": "rBKPS4oLSaV2KVVuHH8EpQqMGgGefGFRs9",
        "Alias": "Savings",
        "Type": 1
      }
    ],
    "Socials": [
      {
        "URL": "https://twitter.com/johndoe",
        "Type": 5
      },
      {
        "URL": "https://github.com/johndoe",
        "Type": 2
      },
      {
        "URL": "https://linkedin.com/in/johndoe",
        "Type": 9
      }
    ],
    "Language": {
      "Language": "en-US"
    },
    "ExternalUserID": "3492068a-c20f-4f66-8bfa-7f751057109b",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
  },
  "MetaData": {
    "Network": 2,
    "UpdatedAt": {
      "seconds": 1741983951,
      "nanos": 82486205
    },
    "CreatedAt": {
      "seconds": 1741983951,
      "nanos": 82485825
    }
  },
  "Audit": {
    "ChangedAt": {
      "seconds": 1741983951,
      "nanos": 82486435
    }
  }
}
PUT /api/user/update
Updates user information. Accepts full or partial user object.

Update Constraints - Immutable Fields:

Field	Reason
OrganizationID	Organization scope cannot be altered
ExternalUserID	System-assigned identifier
MetaData.CreatedAt	Original creation timestamp
MetaData.Network	Network cannot be altered
User.Role	Always enforced as NORMAL_USER
OrganizationIDs	Array cannot be altered
Special Field Handling:

Field	Behavior
Wallets	New wallets are added; existing wallets not removed or updated
Status	Cannot be updated via this endpoint (use /api/user/status endpoints)
Example Request:

bash
curl -X PUT "https://api.sologenic.org/api/user/update" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -d '{
    "User": {
      "FirstName": "Randy",
      "LastName": "Lahey",
      "Address": "SomeOtherAddress",
      "Avatar": "SomeOtherAvatar",
      "Alias": "Bobandy",
      "Description": "Some other description.",
      "Wallets": [
        {
          "Address": "new_wallet_address",
          "Alias": "New Wallet",
          "Type": 1
        }
      ]
    }
  }'
Example Response:

json
{
  "UserID": "randy.lahey@gmail.com",
  "Network": 1
}
PUT /api/user/disable
Allows a user to disable their own account.

⚠️ Important:

Self-disabling only (cannot disable other users)

Only admin can re-enable a disabled account

User must be ACTIVE to perform this action

Example Request:

bash
curl -X PUT "https://api.sologenic.org/api/user/disable" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: mainnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
Example Response:

json
{
  "success": true,
  "message": "User account disabled successfully"
}
POST /api/kyc/start
Allows user to start the KYC process with the Organization's KYC Provider.

Example Request:

bash
curl -X POST "https://api.sologenic.org/api/kyc/start" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response:

json
{
  "kyc_url": "https://kyc-provider.com/start?token=abc123",
  "inquiry_id": "inq_123456789",
  "status": "pending"
}
PUT /api/user/addtoorg
Adds a user to an organization (or an organization to a user).

Important Notes:

This function only works from TX to other organizations

OrganizationID in header must be the default TX organization ID, not the target organization

The organization ID in request body is the one being added

Example Request:

bash
curl -X PUT "https://api.sologenic.org/api/user/addtoorg" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: mainnet" \
  -H "OrganizationID: sologenic" \
  -d '{
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
  }'
Example Response (Success):

json
{
  "success": true,
  "message": "Organization added to user account"
}
Error Responses:

json
// 400 Bad Request - Invalid organization ID in header
{
  "error": "Invalid organization ID"
}

// 404 Not Found - Organization not found
{
  "error": "Organization not found"
}
Data Models
User Object
Field	Type	Description	Immutable
UserID	string	User email/identifier	No
FirstName	string	First name	No
LastName	string	Last name	No
Address	string	Physical address	No
Avatar	string	Avatar URL	No
Alias	string	Display alias	No
Description	string	User description	No
Status	int	1=active, 2=disabled, 3=suspended	No
Wallets	[]Wallet	Associated wallets	Add-only
Socials	[]Social	Social media links	No
Language	Language	Language preference	No
ExternalUserID	string	System identifier	Yes
OrganizationID	string	Organization UUID	Yes
Employment	Employment	Employment info	No
Wallet Object
Field	Type	Description
Address	string	Blockchain wallet address
Alias	string	Wallet alias/name
Type	int	Wallet type (1=hot, 2=cold, 3=exchange)
Social Object
Field	Type	Description
URL	string	Social media profile URL
Type	int	Social platform type
Social Types
Type	Value	Platform
1	Discord	
2	GitHub	GitHub
3	Reddit	Reddit
4	Telegram	Telegram
5	X (Twitter)	
6	Facebook	Facebook
7	Instagram	Instagram
8	LinkedIn	LinkedIn
9	LinkedIn Business	
Language Object
Field	Type	Description
Language	string	Language code (e.g., "en-US")
Employment Object
Field	Type	Description
Employer	string	Employer name
Position	string	Job position/title
Environment Variables
Variable	Description	Required
AUTH_FIREBASE_SERVICE	Firebase authentication endpoint	Yes
USER_STORE	User store endpoint	Yes
ORGANIZATION_STORE	Organization store endpoint	Yes
KYC_DOCUMENT_STORE	KYC document store endpoint	Yes
TRADE_PROFILE_STORE	Trade profile store endpoint	Yes
CERTIFICATE_STORE	Certificate store endpoint	Yes
HTTP_CONFIG	HTTP server configuration	Yes
CREDENTIALS_LOCATION	GCloud credentials file path	Yes
PROJECT_ID	GCloud project ID	Yes
REDIRECT_URL	KYC redirect URI	Yes
PARENT_ORGANIZATION_ID	TX organization ID for cloning	Yes
FEATURE_FLAG_STORE	Feature flag endpoint	No
ROLE_STORE	Role store endpoint	No
Example Configuration
bash
# Required
AUTH_FIREBASE_SERVICE=auth-service:50075
USER_STORE=user-store:50049
ORGANIZATION_STORE=organization-store:50062
KYC_DOCUMENT_STORE=kyc-document-store:50059
TRADE_PROFILE_STORE=trade-profile-store:50060
CERTIFICATE_STORE=certificate-store:50070
HTTP_CONFIG='{"port":":8080","cors":{"allowedOrigins":["*"]}}'
CREDENTIALS_LOCATION=/app/credentials.json
PROJECT_ID=my-gcp-project
REDIRECT_URL=https://app.sologenic.org/kyc/callback
PARENT_ORGANIZATION_ID=sologenic

# Optional
FEATURE_FLAG_STORE=feature-flag-store:50055
ROLE_STORE=role-store:50066
LOG_LEVEL=info
Integration Examples
JavaScript/React Client
javascript
class UserServiceClient {
  constructor(baseUrl, token = null, organizationId = null, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.token = token;
    this.organizationId = organizationId;
    this.network = network;
  }

  setAuth(token, organizationId) {
    this.token = token;
    this.organizationId = organizationId;
  }

  // Unauthenticated endpoints
  async getUserAliases(externalUserIds, orgId, network = 2) {
    const filter = {
      ExternalUserIDs: externalUserIds,
      OrganizationID: orgId,
      Network: network
    };
    const filterBase64 = btoa(JSON.stringify(filter));
    
    const response = await fetch(
      `${this.baseUrl}/api/user/get/alias?filter=${filterBase64}`,
      {
        headers: {
          'Content-Type': 'application/json',
          'OrganizationID': this.organizationId || orgId,
          'Network': this.network
        }
      }
    );
    return response.json();
  }

  async createUser(userData) {
    const response = await fetch(`${this.baseUrl}/api/user/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Network': this.network,
        'OrganizationID': this.organizationId
      },
      body: JSON.stringify(userData)
    });
    return response.json();
  }

  // Authenticated endpoints
  async getUser() {
    const response = await fetch(`${this.baseUrl}/api/user/get`, {
      headers: this._getAuthHeaders()
    });
    return response.json();
  }

  async updateUser(userData) {
    const response = await fetch(`${this.baseUrl}/api/user/update`, {
      method: 'PUT',
      headers: this._getAuthHeaders(),
      body: JSON.stringify({ User: userData })
    });
    return response.json();
  }

  async disableUser() {
    const response = await fetch(`${this.baseUrl}/api/user/disable`, {
      method: 'PUT',
      headers: this._getAuthHeaders()
    });
    return response.json();
  }

  async startKYC() {
    const response = await fetch(`${this.baseUrl}/api/kyc/start`, {
      method: 'POST',
      headers: this._getAuthHeaders()
    });
    return response.json();
  }

  async addToOrganization(orgId) {
    const response = await fetch(`${this.baseUrl}/api/user/addtoorg`, {
      method: 'PUT',
      headers: this._getAuthHeaders(),
      body: JSON.stringify({ OrganizationID: orgId })
    });
    return response.json();
  }

  _getAuthHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer: ${this.token}`,
      'OrganizationID': this.organizationId,
      'Network': this.network
    };
  }
}

// React Component Example
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [kycStatus, setKycStatus] = useState(null);
  const [editing, setEditing] = useState(false);

  const client = new UserServiceClient(
    'https://api.sologenic.org',
    localStorage.getItem('token'),
    localStorage.getItem('orgId'),
    'mainnet'
  );

  useEffect(() => {
    loadUserProfile();
  }, []);

  async function loadUserProfile() {
    try {
      const response = await client.getUser();
      setUser(response.User);
    } catch (error) {
      console.error('Failed to load user:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpdateUser(updatedData) {
    try {
      await client.updateUser(updatedData);
      await loadUserProfile();
      setEditing(false);
    } catch (error) {
      console.error('Failed to update user:', error);
    }
  }

  async function handleStartKYC() {
    try {
      const response = await client.startKYC();
      setKycStatus(response);
      // Redirect to KYC provider
      window.location.href = response.kyc_url;
    } catch (error) {
      console.error('Failed to start KYC:', error);
    }
  }

  async function handleDisableAccount() {
    if (confirm('Are you sure you want to disable your account? This action can only be reversed by an admin.')) {
      try {
        await client.disableUser();
        // Redirect to login or show message
        window.location.href = '/login?disabled=true';
      } catch (error) {
        console.error('Failed to disable account:', error);
      }
    }
  }

  if (loading) return <div>Loading...</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div className="user-profile">
      <div className="profile-header">
        <img src={user.Avatar} alt={user.Alias} className="avatar" />
        <h2>{user.Alias || `${user.FirstName} ${user.LastName}`}</h2>
        <p>{user.Email || user.UserID}</p>
      </div>

      <div className="profile-details">
        <h3>Personal Information</h3>
        <div className="info-row">
          <label>First Name:</label>
          <span>{user.FirstName}</span>
        </div>
        <div className="info-row">
          <label>Last Name:</label>
          <span>{user.LastName}</span>
        </div>
        <div className="info-row">
          <label>Address:</label>
          <span>{user.Address}</span>
        </div>
        <div className="info-row">
          <label>Description:</label>
          <span>{user.Description}</span>
        </div>
      </div>

      <div className="wallets-section">
        <h3>Wallets</h3>
        {user.Wallets?.map((wallet, idx) => (
          <div key={idx} className="wallet-card">
            <strong>{wallet.Alias}</strong>
            <code>{wallet.Address}</code>
          </div>
        ))}
        <button onClick={() => setEditing(true)}>Add Wallet</button>
      </div>

      <div className="kyc-section">
        <h3>Verification Status</h3>
        {kycStatus?.status === 'pending' ? (
          <div>KYC in progress...</div>
        ) : user.KYCStatus === 'verified' ? (
          <div className="verified">✓ Verified</div>
        ) : (
          <button onClick={handleStartKYC}>Start KYC Verification</button>
        )}
      </div>

      <div className="danger-zone">
        <h3>Danger Zone</h3>
        <button onClick={handleDisableAccount} className="danger-button">
          Disable Account
        </button>
      </div>
    </div>
  );
}

export { UserServiceClient, UserProfile };
Python Client
python
import requests
import base64
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import IntEnum

class UserStatus(IntEnum):
    ACTIVE = 1
    DISABLED = 2
    SUSPENDED = 3

class WalletType(IntEnum):
    HOT = 1
    COLD = 2
    EXCHANGE = 3

class SocialType(IntEnum):
    DISCORD = 1
    GITHUB = 2
    REDDIT = 3
    TELEGRAM = 4
    TWITTER = 5
    FACEBOOK = 6
    INSTAGRAM = 7
    LINKEDIN = 8
    LINKEDIN_BUSINESS = 9

@dataclass
class Wallet:
    address: str
    alias: str
    type: WalletType

@dataclass
class Social:
    url: str
    type: SocialType

@dataclass
class Language:
    language: str

@dataclass
class Employment:
    employer: str
    position: str

@dataclass
class User:
    user_id: str
    status: UserStatus
    organization_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    avatar: Optional[str] = None
    alias: Optional[str] = None
    description: Optional[str] = None
    wallets: Optional[List[Wallet]] = None
    socials: Optional[List[Social]] = None
    language: Optional[Language] = None
    employment: Optional[Employment] = None

class UserServiceClient:
    def __init__(self, base_url: str, token: Optional[str] = None, 
                 organization_id: Optional[str] = None, network: str = 'mainnet'):
        self.base_url = base_url
        self.token = token
        self.organization_id = organization_id
        self.network = network
    
    def set_auth(self, token: str, organization_id: str):
        """Set authentication credentials"""
        self.token = token
        self.organization_id = organization_id
    
    # Unauthenticated endpoints
    def get_user_aliases(self, external_user_ids: List[str], org_id: str, network: int = 2) -> List[Dict]:
        """Get aliases for external user IDs"""
        filter_obj = {
            "ExternalUserIDs": external_user_ids,
            "OrganizationID": org_id,
            "Network": network
        }
        filter_base64 = base64.b64encode(json.dumps(filter_obj).encode()).decode()
        
        response = requests.get(
            f"{self.base_url}/api/user/get/alias",
            params={'filter': filter_base64},
            headers={
                'Content-Type': 'application/json',
                'OrganizationID': org_id,
                'Network': 'testnet' if network == 2 else 'mainnet'
            }
        )
        response.raise_for_status()
        return response.json()
    
    def create_user(self, user: User) -> Dict[str, Any]:
        """Create a new user"""
        user_dict = {
            "UserID": user.user_id,
            "FirstName": user.first_name,
            "LastName": user.last_name,
            "Address": user.address,
            "Avatar": user.avatar,
            "Alias": user.alias,
            "Description": user.description,
            "Status": int(user.status),
            "OrganizationID": user.organization_id
        }
        
        if user.wallets:
            user_dict["Wallets"] = [
                {"Address": w.address, "Alias": w.alias, "Type": int(w.type)}
                for w in user.wallets
            ]
        
        if user.socials:
            user_dict["Socials"] = [
                {"URL": s.url, "Type": int(s.type)}
                for s in user.socials
            ]
        
        if user.language:
            user_dict["Language"] = {"Language": user.language.language}
        
        if user.employment:
            user_dict["Employment"] = {
                "Employer": user.employment.employer,
                "Position": user.employment.position
            }
        
        response = requests.post(
            f"{self.base_url}/api/user/create",
            headers={
                'Content-Type': 'application/json',
                'Network': self.network,
                'OrganizationID': self.organization_id
            },
            json=user_dict
        )
        response.raise_for_status()
        return response.json()
    
    # Authenticated endpoints
    def get_user(self) -> Dict[str, Any]:
        """Get current user information"""
        response = requests.get(
            f"{self.base_url}/api/user/get",
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def update_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user information"""
        response = requests.put(
            f"{self.base_url}/api/user/update",
            headers=self._get_auth_headers(),
            json={"User": user_data}
        )
        response.raise_for_status()
        return response.json()
    
    def disable_user(self) -> Dict[str, Any]:
        """Disable current user account"""
        response = requests.put(
            f"{self.base_url}/api/user/disable",
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def start_kyc(self) -> Dict[str, Any]:
        """Start KYC process"""
        response = requests.post(
            f"{self.base_url}/api/kyc/start",
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def add_to_organization(self, org_id: str) -> Dict[str, Any]:
        """Add user to an organization"""
        response = requests.put(
            f"{self.base_url}/api/user/addtoorg",
            headers=self._get_auth_headers(),
            json={"OrganizationID": org_id}
        )
        response.raise_for_status()
        return response.json()
    
    def _get_auth_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer: {self.token}',
            'OrganizationID': self.organization_id,
            'Network': self.network
        }

# Usage Example
def main():
    client = UserServiceClient(
        base_url='https://api.sologenic.org',
        network='mainnet'
    )
    
    # Create a new user (unauthenticated)
    new_user = User(
        user_id='newuser@example.com',
        first_name='John',
        last_name='Doe',
        alias='johndoe',
        description='New user',
        status=UserStatus.ACTIVE,
        organization_id='72c4c072-2fe4-4f72-ae9d-d9d52a05fd71'
    )
    
    result = client.create_user(new_user)
    print(f"User created: {result}")
    
    # Set auth token after user creation/login
    client.set_auth('firebase-jwt-token', '72c4c072-2fe4-4f72-ae9d-d9d52a05fd71')
    
    # Get user profile
    user_profile = client.get_user()
    print(f"User profile: {user_profile['User']['Alias']}")
    
    # Update user
    updates = {
        "FirstName": "Jonathan",
        "Description": "Updated description"
    }
    updated = client.update_user(updates)
    print(f"User updated: {updated}")
    
    # Start KYC
    kyc_result = client.start_kyc()
    print(f"KYC URL: {kyc_result.get('kyc_url')}")

# Run example
# main()
Go Client
go
package main

import (
    "bytes"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"
)

type UserStatus int

const (
    UserStatusActive    UserStatus = 1
    UserStatusDisabled  UserStatus = 2
    UserStatusSuspended UserStatus = 3
)

type WalletType int

const (
    WalletTypeHot      WalletType = 1
    WalletTypeCold     WalletType = 2
    WalletTypeExchange WalletType = 3
)

type SocialType int

const (
    SocialDiscord         SocialType = 1
    SocialGitHub          SocialType = 2
    SocialReddit          SocialType = 3
    SocialTelegram        SocialType = 4
    SocialTwitter         SocialType = 5
    SocialFacebook        SocialType = 6
    SocialInstagram       SocialType = 7
    SocialLinkedIn        SocialType = 8
    SocialLinkedInBusiness SocialType = 9
)

type Wallet struct {
    Address string     `json:"Address"`
    Alias   string     `json:"Alias"`
    Type    WalletType `json:"Type"`
}

type Social struct {
    URL  string     `json:"URL"`
    Type SocialType `json:"Type"`
}

type Language struct {
    Language string `json:"Language"`
}

type Employment struct {
    Employer string `json:"Employer"`
    Position string `json:"Position"`
}

type User struct {
    UserID         string      `json:"UserID"`
    FirstName      string      `json:"FirstName,omitempty"`
    LastName       string      `json:"LastName,omitempty"`
    Address        string      `json:"Address,omitempty"`
    Avatar         string      `json:"Avatar,omitempty"`
    Alias          string      `json:"Alias,omitempty"`
    Description    string      `json:"Description,omitempty"`
    Status         UserStatus  `json:"Status"`
    Wallets        []Wallet    `json:"Wallets,omitempty"`
    Socials        []Social    `json:"Socials,omitempty"`
    Language       *Language   `json:"Language,omitempty"`
    ExternalUserID string      `json:"ExternalUserID,omitempty"`
    OrganizationID string      `json:"OrganizationID"`
    Employment     *Employment `json:"Employment,omitempty"`
}

type UserResponse struct {
    User     User     `json:"User"`
    MetaData Metadata `json:"MetaData"`
    Audit    Audit    `json:"Audit"`
}

type Metadata struct {
    Network   int       `json:"Network"`
    CreatedAt Timestamp `json:"CreatedAt"`
    UpdatedAt Timestamp `json:"UpdatedAt"`
}

type Audit struct {
    ChangedAt Timestamp `json:"ChangedAt"`
}

type Timestamp struct {
    Seconds int64 `json:"seconds"`
    Nanos   int32 `json:"nanos"`
}

type UserServiceClient struct {
    baseURL        string
    token          string
    organizationID string
    network        string
    httpClient     *http.Client
}

func NewUserServiceClient(baseURL, network string) *UserServiceClient {
    return &UserServiceClient
  baseURL:    baseURL,
        network:    network,
        httpClient: &http.Client{Timeout: 30 * time.Second},
    }
}

func (c *UserServiceClient) SetAuth(token, organizationID string) {
    c.token = token
    c.organizationID = organizationID
}

// Unauthenticated endpoints
func (c *UserServiceClient) GetUserAliases(externalUserIDs []string, orgID string, network int) ([]map[string]string, error) {
    filterObj := map[string]interface{}{
        "ExternalUserIDs": externalUserIDs,
        "OrganizationID":  orgID,
        "Network":         network,
    }
    
    filterJSON, err := json.Marshal(filterObj)
    if err != nil {
        return nil, err
    }
    
    filterBase64 := base64.URLEncoding.EncodeToString(filterJSON)
    
    req, err := http.NewRequest("GET", fmt.Sprintf("%s/api/user/get/alias?filter=%s", c.baseURL, filterBase64), nil)
    if err != nil {
        return nil, err
    }
    
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("OrganizationID", orgID)
    req.Header.Set("Network", c.network)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result []map[string]string
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return result, nil
}

func (c *UserServiceClient) CreateUser(user *User) (map[string]interface{}, error) {
    userMap := map[string]interface{}{
        "UserID":         user.UserID,
        "FirstName":      user.FirstName,
        "LastName":       user.LastName,
        "Address":        user.Address,
        "Avatar":         user.Avatar,
        "Alias":          user.Alias,
        "Description":    user.Description,
        "Status":         int(user.Status),
        "OrganizationID": user.OrganizationID,
    }
    
    if len(user.Wallets) > 0 {
        wallets := make([]map[string]interface{}, len(user.Wallets))
        for i, w := range user.Wallets {
            wallets[i] = map[string]interface{}{
                "Address": w.Address,
                "Alias":   w.Alias,
                "Type":    int(w.Type),
            }
        }
        userMap["Wallets"] = wallets
    }
    
    jsonData, err := json.Marshal(userMap)
    if err != nil {
        return nil, err
    }
    
    req, err := http.NewRequest("POST", fmt.Sprintf("%s/api/user/create", c.baseURL), bytes.NewBuffer(jsonData))
    if err != nil {
        return nil, err
    }
    
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Network", c.network)
    req.Header.Set("OrganizationID", c.organizationID)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return result, nil
}

// Authenticated endpoints
func (c *UserServiceClient) GetUser() (*UserResponse, error) {
    req, err := http.NewRequest("GET", fmt.Sprintf("%s/api/user/get", c.baseURL), nil)
    if err != nil {
        return nil, err
    }
    
    c.setAuthHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result UserResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return &result, nil
}

func (c *UserServiceClient) UpdateUser(updates map[string]interface{}) (map[string]interface{}, error) {
    reqBody := map[string]interface{}{"User": updates}
    jsonData, err := json.Marshal(reqBody)
    if err != nil {
        return nil, err
    }
    
    req, err := http.NewRequest("PUT", fmt.Sprintf("%s/api/user/update", c.baseURL), bytes.NewBuffer(jsonData))
    if err != nil {
        return nil, err
    }
    
    c.setAuthHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return result, nil
}

func (c *UserServiceClient) DisableUser() error {
    req, err := http.NewRequest("PUT", fmt.Sprintf("%s/api/user/disable", c.baseURL), nil)
    if err != nil {
        return err
    }
    
    c.setAuthHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("failed to disable user: %d", resp.StatusCode)
    }
    
    return nil
}

func (c *UserServiceClient) StartKYC() (map[string]interface{}, error) {
    req, err := http.NewRequest("POST", fmt.Sprintf("%s/api/kyc/start", c.baseURL), nil)
    if err != nil {
        return nil, err
    }
    
    c.setAuthHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return result, nil
}

func (c *UserServiceClient) AddToOrganization(orgID string) error {
    reqBody := map[string]string{"OrganizationID": orgID}
    jsonData, err := json.Marshal(reqBody)
    if err != nil {
        return err
    }
    
    req, err := http.NewRequest("PUT", fmt.Sprintf("%s/api/user/addtoorg", c.baseURL), bytes.NewBuffer(jsonData))
    if err != nil {
        return err
    }
    
    c.setAuthHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("failed to add organization: %d", resp.StatusCode)
    }
    
    return nil
}

func (c *UserServiceClient) setAuthHeaders(req *http.Request) {
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer: "+c.token)
    req.Header.Set("OrganizationID", c.organizationID)
    req.Header.Set("Network", c.network)
}

// Usage Example
func main() {
    client := NewUserServiceClient("https://api.sologenic.org", "mainnet")
    
    // Create user (unauthenticated)
    newUser := &User{
        UserID:         "newuser@example.com",
        FirstName:      "John",
        LastName:       "Doe",
        Alias:          "johndoe",
        Status:         UserStatusActive,
        OrganizationID: "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    }
    
    result, err := client.CreateUser(newUser)
    if err != nil {
        panic(err)
    }
    fmt.Printf("User created: %v\n", result)
    
    // Set auth and get profile
    client.SetAuth("firebase-jwt-token", "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71")
    
    user, err := client.GetUser()
    if err != nil {
        panic(err)
    }
    fmt.Printf("User: %s %s\n", user.User.FirstName, user.User.LastName)
    
    // Update user
    updates := map[string]interface{}{
        "Description": "Updated description",
        "Alias":       "newalias",
    }
    
    updated, err := client.UpdateUser(updates)
    if err != nil {
        panic(err)
    }
    fmt.Printf("Updated: %v\n", updated)
}
Docker Compose Example
yaml
version: '3.8'

services:
  user-service:
    image: sologenic/user-service:latest
    environment:
      - AUTH_FIREBASE_SERVICE=auth-service:50075
      - USER_STORE=user-store:50049
      - ORGANIZATION_STORE=organization-store:50062
      - KYC_DOCUMENT_STORE=kyc-document-store:50059
      - TRADE_PROFILE_STORE=trade-profile-store:50060
      - CERTIFICATE_STORE=certificate-store:50070
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
      - CREDENTIALS_LOCATION=/app/credentials.json
      - PROJECT_ID=my-gcp-project
      - REDIRECT_URL=https://app.sologenic.org/kyc/callback
      - PARENT_ORGANIZATION_ID=sologenic
      - LOG_LEVEL=info
    ports:
      - "8080:8080"
    volumes:
      - ./credentials.json:/app/credentials.json
    networks:
      - internal

  user-store:
    image: sologenic/user-store:latest
    environment:
      - DATABASE_HOST=postgres:5432
      - DATABASE_NAME=users
    networks:
      - internal

  kyc-document-store:
    image: sologenic/kyc-document-store:latest
    environment:
      - STORAGE_BUCKET=kyc-documents
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Responses
Status	Code	Description
400	Bad Request	Invalid request format or missing required fields
401	Unauthorized	Missing or invalid authentication token
403	Forbidden	User not active or insufficient permissions
404	Not Found	User or organization not found
409	Conflict	User already exists
500	Internal Error	Server-side error
Example Error Response
json
{
  "error": "Invalid organization ID",
  "code": 400,
  "details": "The organization ID provided does not match any valid organization"
}
Troubleshooting
Issue	Possible Cause	Solution
User creation fails	Missing required fields	Ensure Status and OrganizationID are provided
Cannot update user	Immutable field attempted	Check immutable fields list
KYC start fails	User not active	Verify user status is ACTIVE
Add to org fails	Wrong org ID in header	Use TX organization ID in header
Webhook not received	Service not running	Ensure service is always on
Best Practices
Security
Always validate Firebase tokens

Use OrganizationID for tenant isolation

Never expose immutable fields in update requests

Implement rate limiting on user creation

Data Management
Store minimal PII (Personally Identifiable Information)

Encrypt sensitive user data

Regular backup of user data

Implement data retention policies

KYC Integration
Handle webhook idempotency

Implement retry logic for failed webhooks

Store KYC document references securely

Redirect users properly after KYC completion

Related Services
Service	Description
Auth Firebase Service	Token validation
User Store	User data persistence
Organization Store	Tenant management
KYC Document Store	KYC document storage
Trade Profile Store	Trading preferences
Certificate Store	User certificates
Role Store	Permission management
Feature Flag Store	Feature toggles
License
This documentation is part of the TX Marketplace platform.
