# Admin Certificate Service

The Admin Certificate Service provides RESTful interfaces for managing digital certificates within organizations. These certificates are used for secure service-to-service authentication, such as Firebase service accounts, cloud storage access, and other external service integrations.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin Certificate Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├─────────────────────┬─────────────────────┬───────────────────────┤ │
│ │ GET /get │ GET /list │ POST /upsert │ │
│ │ (Retrieve by type) │ (List all) │ (Create/Update) │ │
│ └─────────────────────┴─────────────────────┴───────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Certificate │ Account Store │ Role Store │ Organization Store│ │
│ │ Store │ │ │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Services │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Firebase Authentication │ │
│ │ • Google Cloud Storage │ │
│ │ • External APIs with certificate auth │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/admincertificate/get | ORGANIZATION_ADMINISTRATOR | Retrieve certificate by type |
| GET /api/admincertificate/list | ORGANIZATION_ADMINISTRATOR | List all certificates |
| POST /api/admincertificate/upsert | ORGANIZATION_ADMINISTRATOR | Create or update certificate |

**Note:** All admin endpoints are protected by role-based access control and default to the `ORGANIZATION_ADMINISTRATOR` role. Permissions are managed dynamically by Organization administrators on the fly.

## Certificate Types

| Type ID | Certificate Type | Description | Typical Use |
|---------|------------------|-------------|-------------|
| 1 | SERVICE_ACCOUNT | Google/Firebase service account | Firebase auth, GCP services |
| 2 | API_KEY | External API authentication | Third-party service integration |
| 3 | JWT_SIGNING | JWT signing certificate | Token generation/validation |
| 4 | SSL_TLS | SSL/TLS certificates | HTTPS, secure communication |
| 5 | CUSTOM | Custom certificate type | Organization-specific needs |

## API Endpoints

### GET /api/admincertificate/get

Retrieves a certificate by its type for the authenticated organization.

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| type | int | Certificate type ID (1-5) | Yes |

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/admincertificate/get?type=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
{
  "Certificate": {
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Type": 1,
    "CredentialsJSON": "{\"type\":\"service_account\",\"project_id\":\"my-project-12345\",\"private_key_id\":\"abc123def456ghi789\",\"private_key\":\"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7...\\n-----END PRIVATE KEY-----\\n\",\"client_email\":\"my-service-account@my-project-12345.iam.gserviceaccount.com\",\"client_id\":\"123456789012345678901\",\"auth_uri\":\"https://accounts.google.com/o/oauth2/auth\",\"token_uri\":\"https://oauth2.googleapis.com/token\",\"auth_provider_x509_cert_url\":\"https://www.googleapis.com/oauth2/v1/certs\",\"client_x509_cert_url\":\"https://www.googleapis.com/robot/v1/metadata/x509/my-service-account%40my-project-12345.iam.gserviceaccount.com\"}",
    "Description": "Storage access for production environment"
  },
  "MetaData": {
    "UpdatedAt": {
      "seconds": 1748392726,
      "nanos": 950528000
    },
    "CreatedAt": {
      "seconds": 1748392214,
      "nanos": 950670000
    }
  },
  "Audit": {
    "ChangedBy": "sg.org.testnet@gmail.com",
    "ChangedAt": {
      "seconds": 1748392726,
      "nanos": 950552000
    }
  }
}
Error Responses
Status Code	Description
200	Success - Certificate found
400	Bad request - Invalid type parameter
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Certificate type not found for organization
GET /api/admincertificate/list
Retrieves a list of all certificates for the authenticated organization.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters (Optional)
Parameter	Type	Description
limit	int	Maximum number of certificates to return
offset	int	Pagination offset
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/admincertificate/list" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet"
Example Response
json
{
  "Certificates": [
    {
      "Certificate": {
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Type": 1,
        "CredentialsJSON": "{\"type\":\"service_account\",\"project_id\":\"my-project-12345\",\"private_key_id\":\"abc123def456ghi789\",\"private_key\":\"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7...\\n-----END PRIVATE KEY-----\\n\",\"client_email\":\"my-service-account@my-project-12345.iam.gserviceaccount.com\",\"client_id\":\"123456789012345678901\",\"auth_uri\":\"https://accounts.google.com/o/oauth2/auth\",\"token_uri\":\"https://oauth2.googleapis.com/token\",\"auth_provider_x509_cert_url\":\"https://www.googleapis.com/oauth2/v1/certs\",\"client_x509_cert_url\":\"https://www.googleapis.com/robot/v1/metadata/x509/my-service-account%40my-project-12345.iam.gserviceaccount.com\"}",
        "Description": "Storage access for production environment"
      },
      "MetaData": {
        "UpdatedAt": {
          "seconds": 1748392726,
          "nanos": 950528000
        },
        "CreatedAt": {
          "seconds": 1748392214,
          "nanos": 950670000
        }
      },
      "Audit": {
        "ChangedBy": "sg.org.testnet@gmail.com",
        "ChangedAt": {
          "seconds": 1748392726,
          "nanos": 950552000
        }
      }
    },
    {
      "Certificate": {
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Type": 2,
        "CredentialsJSON": "{\"type\":\"service_account\",\"project_id\":\"my-project-12345\",\"private_key_id\":\"abc123def456ghi789\",\"private_key\":\"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7...\\n-----END PRIVATE KEY-----\\n\",\"client_email\":\"my-service-account@my-project-12345.iam.gserviceaccount.com\",\"client_id\":\"123456789012345678901\",\"auth_uri\":\"https://accounts.google.com/o/oauth2/auth\",\"token_uri\":\"https://oauth2.googleapis.com/token\",\"auth_provider_x509_cert_url\":\"https://www.googleapis.com/oauth2/v1/certs\",\"client_x509_cert_url\":\"https://www.googleapis.com/robot/v1/metadata/x509/my-service-account%40my-project-12345.iam.gserviceaccount.com\"}",
        "Description": "Production service account"
      },
      "MetaData": {
        "UpdatedAt": {
          "seconds": 1748392971,
          "nanos": 381590000
        },
        "CreatedAt": {
          "seconds": 1748392782,
          "nanos": 740613000
        }
      },
      "Audit": {
        "ChangedBy": "sg.org.testnet@gmail.com",
        "ChangedAt": {
          "seconds": 1748392971,
          "nanos": 381591000
        }
      }
    }
  ]
}
POST /api/admincertificate/upsert
Creates a new certificate or updates an existing certificate by type for the authenticated organization.

Request Body
Field	Type	Description	Required
Certificate.OrganizationID	string	Organization UUID	Yes
Certificate.Type	int	Certificate type (1-5)	Yes
Certificate.CredentialsJSON	string	JSON string containing credentials	Yes
Certificate.Description	string	Human-readable description	No
Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/admincertificate/upsert" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: testnet" \
  -d '{
    "Certificate": {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Type": 2,
      "CredentialsJSON": "{\"type\":\"service_account\",\"project_id\":\"my-project-12345\",\"private_key_id\":\"abc123def456ghi789\",\"private_key\":\"-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7...\\n-----END PRIVATE KEY-----\\n\",\"client_email\":\"my-service-account@my-project-12345.iam.gserviceaccount.com\",\"client_id\":\"123456789012345678901\",\"auth_uri\":\"https://accounts.google.com/o/oauth2/auth\",\"token_uri\":\"https://oauth2.googleapis.com/token\",\"auth_provider_x509_cert_url\":\"https://www.googleapis.com/oauth2/v1/certs\",\"client_x509_cert_url\":\"https://www.googleapis.com/robot/v1/metadata/x509/my-service-account%40my-project-12345.iam.gserviceaccount.com\"}",
      "Description": "Storage access for production environment"
    }
  }'
Example Response (Success)
json
{
  "Success": true,
  "Message": "Certificate upserted successfully",
  "Certificate": {
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Type": 2,
    "Description": "Storage access for production environment"
  }
}
Error Responses
Status Code	Description
200	Success - Certificate created or updated
400	Bad request - Invalid JSON or missing required fields
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
409	Conflict - Certificate type already exists for organization (update instead)
Data Models
Certificate Object
Field	Type	Description
OrganizationID	string	Unique identifier for the organization
Type	int	Certificate type (1-5)
CredentialsJSON	string	JSON string containing credential data
Description	string	Human-readable description of the certificate's purpose
MetaData Object
Field	Type	Description
CreatedAt	timestamp	Creation timestamp (seconds + nanos)
UpdatedAt	timestamp	Last update timestamp (seconds + nanos)
Audit Object
Field	Type	Description
ChangedBy	string	Email or identifier of user who made the change
ChangedAt	timestamp	Timestamp of the change
CredentialsJSON Formats
Type 1: Google Service Account
json
{
  "type": "service_account",
  "project_id": "my-project-12345",
  "private_key_id": "abc123def456ghi789",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7...\n-----END PRIVATE KEY-----\n",
  "client_email": "my-service-account@my-project-12345.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-service-account%40my-project-12345.iam.gserviceaccount.com"
}
Type 2: API Key
json
{
  "api_key": "abc123def456ghi789jkl",
  "api_secret": "secret_value",
  "endpoint": "https://api.external-service.com",
  "expires_at": "2025-12-31T23:59:59Z"
}
Type 3: JWT Signing Certificate
json
{
  "algorithm": "RS256",
  "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...\n-----END PUBLIC KEY-----\n",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASC...\n-----END PRIVATE KEY-----\n",
  "key_id": "key_12345",
  "issuer": "tx-marketplace"
}
Type 4: SSL/TLS Certificate
json
{
  "certificate": "-----BEGIN CERTIFICATE-----\nMIIDXTCCAkWgAwIBAgIJAKlM...\n-----END CERTIFICATE-----\n",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASC...\n-----END PRIVATE KEY-----\n",
  "ca_bundle": "-----BEGIN CERTIFICATE-----\nMIIDXTCCAkWgAwIBAgIJAKlM...\n-----END CERTIFICATE-----\n",
  "expires_at": "2025-12-31T23:59:59Z"
}
Type 5: Custom Certificate
json
{
  "certificate_data": {},
  "format": "custom",
  "version": "1.0",
  "metadata": {}
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_FIREBASE_SERVICE	Firebase authentication service endpoint	-
ACCOUNT_STORE	Admin account store endpoint	github.com/sologenic/com-be-admin-account-store/
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/fs-feature-flag-model/
ROLE_STORE	Role store endpoint	github.com/sologenic/com-be-admin-role-store/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-store/
CERTIFICATE_STORE	Certificate store endpoint	github.com/sologenic/com-be-admin-certificate-store/
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
Certificate Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Certificate Lifecycle                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐                                                              │
│  │ Created  │                                                              │
│  └────┬─────┘                                                              │
│       │                                                                     │
│       │ POST /upsert (first time)                                          │
│       ▼                                                                     │
│  ┌──────────┐                                                              │
│  │ Active   │◄──────────────────────────────────────────────────────┐     │
│  └────┬─────┘                                                       │     │
│       │                                                             │     │
│       │ POST /upsert (same type)                                    │     │
│       ▼                                                             │     │
│  ┌──────────┐                                                      │     │
│  │ Updated  │──────────────────────────────────────────────────────┘     │
│  └────┬─────┘                                                             │
│       │                                                                     │
│       │ Certificate rotation / expiry                                      │
│       ▼                                                                     │
│  ┌──────────┐                                                              │
│  │ Expired  │                                                              │
│  │/Revoked  │                                                              │
│  └──────────┘                                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Security Considerations
Best Practices
Secure Storage: Certificates are stored encrypted at rest

Access Control: Only ORGANIZATION_ADMINISTRATORS can manage certificates

Audit Trail: All certificate operations are logged with user information

Regular Rotation: Implement certificate rotation policies

Least Privilege: Use service accounts with minimal required permissions

Security Headers
All endpoints require:

Valid Firebase authentication token

Network header matching the certificate's intended environment

OrganizationID implicitly derived from authentication context

Error Handling
Common Error Codes
Error Code	Description	Resolution
CERT_001	Certificate type not found	Verify type parameter (1-5)
CERT_002	Invalid credentials JSON format	Validate JSON structure
CERT_003	Organization mismatch	Ensure OrganizationID matches auth context
CERT_004	Permission denied	Verify user has ORGANIZATION_ADMINISTRATOR role
CERT_005	Certificate already exists	Use upsert for update, not create
CERT_006	Network mismatch	Verify Network header matches certificate network
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Certificate not found	Wrong type parameter	Verify certificate type exists for organization
Permission denied	Insufficient role	Ensure user has ORGANIZATION_ADMINISTRATOR role
Invalid credentials	Malformed JSON	Validate CredentialsJSON format
Network error	Wrong network	Check Network header (mainnet/testnet/devnet)
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check audit logs for certificate operations:

json
{
  "Audit": {
    "ChangedBy": "user@example.com",
    "ChangedAt": "2024-01-01T00:00:00Z"
  }
}
Related Services
Service	Description
Admin Account Service	User and role management
Admin Asset Service	Asset management
Organization Service	Organization management
Feature Flag Service	Feature toggles
Example Use Cases
1. Firebase Service Account Setup
bash
# Create certificate for Firebase authentication
curl -X POST /api/admincertificate/upsert \
  -d '{
    "Certificate": {
      "OrganizationID": "org-123",
      "Type": 1,
      "CredentialsJSON": "{...firebase service account json...}",
      "Description": "Firebase auth for production"
    }
  }'
2. External API Integration
bash
# Store API key for external service
curl -X POST /api/admincertificate/upsert \
  -d '{
    "Certificate": {
      "OrganizationID": "org-123",
      "Type": 2,
      "CredentialsJSON": "{\"api_key\":\"key123\",\"api_secret\":\"secret456\"}",
      "Description": "Market data API credentials"
    }
  }'
3. Certificate Rotation
bash
# Update existing certificate (same type)
curl -X POST /api/admincertificate/upsert \
  -d '{
    "Certificate": {
      "OrganizationID": "org-123",
      "Type": 1,
      "CredentialsJSON": "{...new service account json...}",
      "Description": "Firebase auth - rotated Dec 2024"
    }
  }'
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the admin certificate service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the admin certificate service section:

markdown
## Admin Services

### Admin Account Service

The Admin Account Service manages users and their roles within a multi-tier system.

📖 **[Admin Account Service Documentation](./admin/account-service.md)**

### Admin Asset Service

The Admin Asset Service provides RESTful interfaces for managing assets within organizations.

📖 **[Admin Asset Service Documentation](./admin/asset/asset-service.md)**

### Admin Certificate Service

The Admin Certificate Service provides RESTful interfaces for managing digital certificates within organizations. These certificates are used for secure service-to-service authentication.

📖 **[Admin Certificate Service Documentation](./admin/certificate/certificate-service.md)**

**Certificate Types:**
| Type | Name | Use Case |
|------|------|----------|
| 1 | SERVICE_ACCOUNT | Google/Firebase service accounts |
| 2 | API_KEY | External API authentication |
| 3 | JWT_SIGNING | Token generation/validation |
| 4 | SSL_TLS | HTTPS, secure communication |
| 5 | CUSTOM | Organization-specific needs |

**Key Features:**
- Retrieve certificate by type
- List all organization certificates
- Create or update certificates (upsert)
- Role-based access control (ORGANIZATION_ADMINISTRATOR)
- Audit logging for all certificate operations

**Quick Examples:**
```bash
# Get certificate by type
GET /api/admincertificate/get?type=1

# List all certificates
GET /api/admincertificate/list

# Create or update certificate
POST /api/admincertificate/upsert
Account Types:

Sologenic Administrator (Platform level)

Organization Administrator (Organization level)

KYC Administrator

Broker Asset Administrator

Normal User (End User)
