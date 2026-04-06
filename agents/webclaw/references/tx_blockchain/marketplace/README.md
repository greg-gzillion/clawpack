# TX Marketplace API Documentation

Complete API documentation for the TX Blockchain Marketplace platform.

## Overview

The TX Marketplace provides a comprehensive set of REST APIs for asset trading, user management, KYC compliance, document handling, and more.

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ TX Marketplace Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Routes │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Admin API │ Account API │ Asset API │ Certificate API │ │
│ │ Comment API │ Document API │ Feature API │ File API │ │
│ │ Jurisdiction │ KYC API │ MiniCMS API │ Notification API │ │
│ │ Organization │ Smart Contract│ User API │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ AED Service │ Alert Service │ Asset Service │ Auth Service │ │
│ │ Comment Svc │ Document Svc │ Email Svc │ Feature Flag Svc │ │
│ │ File Service │ Holdings Svc │ KYC Service │ MiniCMS Service │ │
│ │ Notification │ Open Search │ Order Mgmt │ Record Service │ │
│ │ Update Svc │ User Service │ Wallet Svc │ Reference Service │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Data Models │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ AED Model │ Asset Model │ Auth Model │ Comment Model │ │
│ │ Document │ Holdings │ Order Model │ Record Model │ │
│ │ Reference │ Trade Model │ User Model │ Session Model │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## API Categories

### Admin API
Administrative endpoints for platform management.

### Account API
User account management and profile operations.

### Asset API
Asset listing, metadata, and trading pair management.

### Certificate API
Digital certificate issuance and verification.

### Comment API
User comments and feedback on assets.

### Document API
Document upload, storage, and retrieval.

### Feature Flag API
Feature toggles and configuration management.

### File API
File storage and management (images, PDFs, etc.).

### Jurisdiction Asset API
Jurisdiction-specific asset rules and restrictions.

### Jurisdiction API
Regional compliance and legal framework management.

### KYC Document API
Know-Your-Customer document submission and verification.

### MiniCMS API
Content management for marketplace pages.

### Notification API
User notifications, alerts, and messaging.

### Organization API
Corporate and institutional account management.

### Smart Contract Management API
Smart contract deployment and interaction.

### User API
User registration, profiles, and settings.

## Services

### Core Services

| Service | Description |
|---------|-------------|
| **AED Service** | Asset Exchange Data service |
| **Alert Service** | Price alerts and notifications |
| **Asset Service** | Asset management and metadata |
| **Auth Firebase Service** | Firebase authentication integration |
| **Auth Service** | Core authentication logic |
| **Comment Service** | Comment management |
| **Contact List Service** | User contact management |
| **Document Service** | Document processing |
| **Email Send Service** | Email delivery |
| **Email Template Service** | Email template management |
| **Feature Flag Service** | Feature toggle management |
| **File Service** | File storage and retrieval |
| **Holdings Service** | User asset holdings |
| **KYC Service** | Identity verification |
| **MiniCMS Service** | Content management |
| **Notification Service** | Push notifications |
| **Open Search Service** | Search functionality |
| **Order Management Service** | Trade order processing |
| **Record Service** | Transaction records |
| **Update Service** | Real-time updates |
| **User Service** | User management |
| **Wallet Service** | Wallet operations |
| **Reference Service** | Reference data |

## Data Models

### Core Models

| Model | Description |
|-------|-------------|
| **AED Model** | Asset Exchange Data structure |
| **Asset Model** | Asset metadata and properties |
| **Auth Firebase Model** | Firebase auth data |
| **Auth Model** | Authentication data |
| **Comment Model** | Comment structure |
| **Contact List Model** | Contact relationships |
| **Document Model** | Document metadata |
| **Holdings Model** | User asset holdings |
| **Order Model** | Trade order structure |
| **Record Model** | Transaction record |
| **Reference Model** | Reference data |
| **Trade Model** | Trade execution data |
| **Trade Profile Model** | User trading preferences |
| **User Model** | User account data |
| **User Session Model** | Session management |

## Quick Links

| Category | Documentation |
|----------|---------------|
| Admin API | [admin-api.md](./admin-api.md) |
| Account API | [account-api.md](./account-api.md) |
| Asset API | [asset-api.md](./asset-api.md) |
| User API | [user-api.md](./user-api.md) |
| KYC API | [kyc-api.md](./kyc-api.md) |
| Services | [services.md](./services.md) |
| Data Models | [data-models.md](./data-models.md) |

## Authentication

Most API endpoints require authentication using Firebase Auth or JWT tokens.

```typescript
// Authentication header
headers: {
  'Authorization': 'Bearer <token>',
  'Content-Type': 'application/json'
}
Common Response Formats
Success Response
json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
Error Response
json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": {}
  }
}
Paginated Response
json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
Rate Limits
Endpoint Category	Rate Limit
Public endpoints	100 req/min
Authenticated	500 req/min
Admin endpoints	1000 req/min
KYC/Verification	50 req/min
Environment URLs
Environment	API Base URL
Devnet	https://api.devnet.tx.marketplace
Testnet	https://api.testnet.tx.marketplace
Mainnet	https://api.tx.marketplace
text

Now let me create individual API documentation files:

```bash
nano ~/dev/TXdocumentation/marketplace/asset-api.md
markdown
# Asset API

Asset management endpoints for listing, querying, and managing marketplace assets.

## Endpoints

### Get All Assets
GET /api/v1/assets

text

#### Query Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| page | int | Page number | 1 |
| limit | int | Items per page | 20 |
| sort | string | Sort field (name, price, volume) | name |
| order | string | asc or desc | asc |
| category | string | Filter by category | - |
| status | string | active, pending, inactive | active |
| search | string | Search by name/description | - |

#### Response

```json
{
  "success": true,
  "data": [
    {
      "id": "asset_123",
      "name": "Tokenized Real Estate",
      "symbol": "TRE",
      "description": "Commercial real estate token",
      "category": "real_estate",
      "issuer": "core1issuer...",
      "total_supply": "1000000",
      "circulating_supply": "500000",
      "price": {
        "amount": "100.00",
        "currency": "USD",
        "change_24h": 2.5
      },
      "volume_24h": "50000",
      "market_cap": "50000000",
      "status": "active",
      "metadata": {
        "logo_url": "https://...",
        "website": "https://...",
        "whitepaper": "https://..."
      },
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
Get Asset by ID
text
GET /api/v1/assets/{asset_id}
Response
json
{
  "success": true,
  "data": {
    "id": "asset_123",
    "name": "Tokenized Real Estate",
    "symbol": "TRE",
    "description": "Commercial real estate token",
    "category": "real_estate",
    "issuer": "core1issuer...",
    "total_supply": "1000000",
    "circulating_supply": "500000",
    "price": {
      "amount": "100.00",
      "currency": "USD",
      "change_24h": 2.5
    },
    "volume_24h": "50000",
    "market_cap": "50000000",
    "status": "active",
    "kyc_required": true,
    "accredited_only": true,
    "jurisdictions": ["US", "EU", "UK"],
    "documents": [
      {
        "type": "prospectus",
        "url": "https://...",
        "name": "Investment Prospectus"
      }
    ],
    "metadata": {
      "logo_url": "https://...",
      "website": "https://...",
      "whitepaper": "https://...",
      "social": {
        "twitter": "@asset",
        "linkedin": "company/asset"
      }
    },
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
Get Asset Price History
text
GET /api/v1/assets/{asset_id}/price-history
Query Parameters
Parameter	Type	Description	Default
interval	string	1m, 5m, 15m, 1h, 4h, 1d, 1w	1d
from	timestamp	Start time	7 days ago
to	timestamp	End time	now
limit	int	Max data points	100
Response
json
{
  "success": true,
  "data": {
    "asset_id": "asset_123",
    "symbol": "TRE",
    "interval": "1d",
    "history": [
      {
        "timestamp": "2024-01-01T00:00:00Z",
        "open": "98.50",
        "high": "101.00",
        "low": "98.00",
        "close": "100.00",
        "volume": "5000"
      }
    ]
  }
}
Get Asset Order Book
text
GET /api/v1/assets/{asset_id}/orderbook
Response
json
{
  "success": true,
  "data": {
    "asset_id": "asset_123",
    "bids": [
      {
        "price": "99.50",
        "quantity": "100",
        "total": "9950"
      }
    ],
    "asks": [
      {
        "price": "100.50",
        "quantity": "150",
        "total": "15075"
      }
    ],
    "spread": "1.00",
    "spread_percentage": "1.00"
  }
}
Get Asset Trades
text
GET /api/v1/assets/{asset_id}/trades
Query Parameters
Parameter	Type	Description
limit	int	Number of trades (default: 50)
from	timestamp	Start time
to	timestamp	End time
Response
json
{
  "success": true,
  "data": {
    "asset_id": "asset_123",
    "trades": [
      {
        "id": "trade_123",
        "price": "100.00",
        "quantity": "10",
        "total": "1000",
        "side": "buy",
        "timestamp": "2024-01-01T00:00:00Z",
        "buyer": "core1buyer...",
        "seller": "core1seller..."
      }
    ]
  }
}
Get Asset Statistics
text
GET /api/v1/assets/{asset_id}/statistics
Response
json
{
  "success": true,
  "data": {
    "asset_id": "asset_123",
    "statistics": {
      "price_change_1h": 0.5,
      "price_change_24h": 2.5,
      "price_change_7d": 10.2,
      "price_change_30d": 15.8,
      "volume_24h": "50000",
      "volume_7d": "350000",
      "volume_30d": "1500000",
      "high_24h": "101.00",
      "low_24h": "98.50",
      "ath": "150.00",
      "atl": "50.00"
    }
  }
}
Search Assets
text
GET /api/v1/assets/search
Query Parameters
Parameter	Type	Description
q	string	Search query
category	string	Filter by category
min_price	decimal	Minimum price
max_price	decimal	Maximum price
kyc_required	boolean	Filter by KYC requirement
Response
json
{
  "success": true,
  "data": {
    "query": "real estate",
    "total": 25,
    "results": [
      {
        "id": "asset_123",
        "name": "Tokenized Real Estate",
        "symbol": "TRE",
        "price": "100.00",
        "relevance_score": 0.95
      }
    ]
  }
}
Get Asset Categories
text
GET /api/v1/assets/categories
Response
json
{
  "success": true,
  "data": {
    "categories": [
      {
        "id": "real_estate",
        "name": "Real Estate",
        "count": 45,
        "icon": "🏢"
      },
      {
        "id": "commodities",
        "name": "Commodities",
        "count": 23,
        "icon": "📦"
      },
      {
        "id": "equities",
        "name": "Equities",
        "count": 67,
        "icon": "📈"
      }
    ]
  }
}
Admin: Create Asset
text
POST /api/v1/admin/assets
Request Body
json
{
  "name": "New Tokenized Asset",
  "symbol": "NTA",
  "description": "Description of the asset",
  "category": "real_estate",
  "issuer": "core1issuer...",
  "total_supply": "1000000",
  "kyc_required": true,
  "accredited_only": false,
  "jurisdictions": ["US", "EU"],
  "metadata": {
    "logo_url": "https://...",
    "website": "https://..."
  }
}
Response
json
{
  "success": true,
  "data": {
    "id": "asset_new_123",
    "name": "New Tokenized Asset",
    "symbol": "NTA",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
Admin: Update Asset
text
PUT /api/v1/admin/assets/{asset_id}
Request Body
json
{
  "name": "Updated Asset Name",
  "description": "Updated description",
  "status": "active",
  "metadata": {
    "website": "https://new-website.com"
  }
}
Admin: Delete Asset
text
DELETE /api/v1/admin/assets/{asset_id}
Asset Status Values
Status	Description
pending	Awaiting approval
active	Available for trading
suspended	Temporarily unavailable
delisted	Permanently removed
Asset Categories
Category	Description
real_estate	Tokenized real estate
commodities	Commodities (gold, oil, etc.)
equities	Stock tokens
bonds	Bond tokens
funds	Investment funds
art	Fine art tokens
collectibles	Digital collectibles
text

```bash
nano ~/dev/TXdocumentation/marketplace/user-api.md
markdown
# User API

User management endpoints for registration, profiles, and account settings.

## Endpoints

### Register User
POST /api/v1/users/register

text

#### Request Body

```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "country": "US",
  "accept_terms": true
}
Response
json
{
  "success": true,
  "data": {
    "user_id": "user_123",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "status": "pending_kyc",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
Login
text
POST /api/v1/users/login
Request Body
json
{
  "email": "user@example.com",
  "password": "secure_password"
}
Response
json
{
  "success": true,
  "data": {
    "access_token": "jwt_token_here",
    "refresh_token": "refresh_token_here",
    "expires_in": 3600,
    "user": {
      "id": "user_123",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user",
      "kyc_status": "pending",
      "email_verified": false
    }
  }
}
Refresh Token
text
POST /api/v1/users/refresh
Request Body
json
{
  "refresh_token": "refresh_token_here"
}
Response
json
{
  "success": true,
  "data": {
    "access_token": "new_jwt_token",
    "expires_in": 3600
  }
}
Logout
text
POST /api/v1/users/logout
Headers
text
Authorization: Bearer <access_token>
Get User Profile
text
GET /api/v1/users/profile
Headers
text
Authorization: Bearer <access_token>
Response
json
{
  "success": true,
  "data": {
    "id": "user_123",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "country": "US",
    "timezone": "America/New_York",
    "language": "en",
    "role": "user",
    "status": "active",
    "kyc_status": "verified",
    "email_verified": true,
    "phone_verified": false,
    "two_factor_enabled": false,
    "preferences": {
      "notifications": {
        "email": true,
        "push": true,
        "price_alerts": true
      },
      "theme": "dark",
      "currency_display": "USD"
    },
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-15T00:00:00Z"
  }
}
Update User Profile
text
PUT /api/v1/users/profile
Headers
text
Authorization: Bearer <access_token>
Request Body
json
{
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "country": "US",
  "timezone": "America/New_York",
  "language": "en",
  "preferences": {
    "theme": "light",
    "currency_display": "EUR",
    "notifications": {
      "email": true,
      "push": false
    }
  }
}
Change Password
text
POST /api/v1/users/change-password
Headers
text
Authorization: Bearer <access_token>
Request Body
json
{
  "current_password": "old_password",
  "new_password": "new_secure_password"
}
Request Password Reset
text
POST /api/v1/users/forgot-password
Request Body
json
{
  "email": "user@example.com"
}
Response
json
{
  "success": true,
  "message": "Password reset email sent"
}
Reset Password
text
POST /api/v1/users/reset-password
Request Body
json
{
  "token": "reset_token_from_email",
  "new_password": "new_secure_password"
}
Verify Email
text
POST /api/v1/users/verify-email
Request Body
json
{
  "token": "verification_token"
}
Resend Verification Email
text
POST /api/v1/users/resend-verification
Headers
text
Authorization: Bearer <access_token>
Enable 2FA
text
POST /api/v1/users/2fa/enable
Headers
text
Authorization: Bearer <access_token>
Response
json
{
  "success": true,
  "data": {
    "secret": "ABCDEFGHIJKLMNOP",
    "qr_code_url": "https://...",
    "backup_codes": ["code1", "code2", "code3"]
  }
}
Verify 2FA
text
POST /api/v1/users/2fa/verify
Headers
text
Authorization: Bearer <access_token>
Request Body
json
{
  "code": "123456"
}
Disable 2FA
text
POST /api/v1/users/2fa/disable
Headers
text
Authorization: Bearer <access_token>
Request Body
json
{
  "code": "123456"
}
Get User Holdings
text
GET /api/v1/users/holdings
Headers
text
Authorization: Bearer <access_token>
Response
json
{
  "success": true,
  "data": {
    "total_value_usd": "15000.00",
    "holdings": [
      {
        "asset_id": "asset_123",
        "symbol": "TRE",
        "name": "Tokenized Real Estate",
        "balance": "100",
        "available": "100",
        "locked": "0",
        "value_usd": "10000.00",
        "price": "100.00"
      }
    ]
  }
}
Get User Orders
text
GET /api/v1/users/orders
Headers
text
Authorization: Bearer <access_token>
Query Parameters
Parameter	Type	Description
status	string	open, filled, cancelled
asset_id	string	Filter by asset
limit	int	Max orders
offset	int	Pagination offset
Response
json
{
  "success": true,
  "data": {
    "orders": [
      {
        "id": "order_123",
        "asset_id": "asset_123",
        "type": "limit",
        "side": "buy",
        "price": "100.00",
        "quantity": "10",
        "filled_quantity": "5",
        "status": "partial",
        "created_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
Get User Transactions
text
GET /api/v1/users/transactions
Headers
text
Authorization: Bearer <access_token>
Query Parameters
Parameter	Type	Description
type	string	trade, deposit, withdrawal
from	timestamp	Start date
to	timestamp	End date
limit	int	Max transactions
Response
json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "id": "tx_123",
        "type": "trade",
        "asset_id": "asset_123",
        "amount": "10",
        "price": "100.00",
        "total": "1000.00",
        "fee": "1.00",
        "timestamp": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
Delete Account
text
DELETE /api/v1/users/account
Headers
text
Authorization: Bearer <access_token>
Request Body
json
{
  "password": "current_password",
  "confirmation": true
}
User Roles
Role	Description
user	Standard marketplace user
verified	KYC verified user
institutional	Institutional account
admin	Platform administrator
super_admin	Full system access
KYC Status Values
Status	Description
not_started	No KYC submitted
pending	KYC under review
verified	KYC approved
rejected	KYC rejected
expired	KYC expired (needs renewal)
text

Let me continue with more API documentation:

```bash
nano ~/dev/TXdocumentation/marketplace/kyc-api.md
markdown
# KYC Document API

Know-Your-Customer document submission and verification endpoints.

## Endpoints

### Get KYC Status
GET /api/v1/kyc/status

text

#### Headers
Authorization: Bearer <access_token>

text

#### Response

```json
{
  "success": true,
  "data": {
    "status": "pending",
    "level": "tier_2",
    "submitted_at": "2024-01-01T00:00:00Z",
    "verified_at": null,
    "rejection_reason": null,
    "required_documents": [
      "government_id",
      "proof_of_address",
      "selfie"
    ]
  }
}
Submit KYC Documents
text
POST /api/v1/kyc/documents
Headers
text
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
Request Body (multipart/form-data)
Field	Type	Description
document_type	string	government_id, passport, driver_license, proof_of_address
file	file	Document image/PDF
document_number	string	Optional: ID document number
issuing_country	string	Country of issuance
expiry_date	date	Document expiry date
Response
json
{
  "success": true,
  "data": {
    "document_id": "doc_123",
    "status": "pending",
    "submitted_at": "2024-01-01T00:00:00Z"
  }
}
Get KYC Documents
text
GET /api/v1/kyc/documents
Headers
text
Authorization: Bearer <access_token>
Response
json
{
  "success": true,
  "data": {
    "documents": [
      {
        "id": "doc_123",
        "type": "government_id",
        "status": "verified",
        "submitted_at": "2024-01-01T00:00:00Z",
        "verified_at": "2024-01-02T00:00:00Z"
      },
      {
        "id": "doc_124",
        "type": "proof_of_address",
        "status": "pending",
        "submitted_at": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
Start Video Verification
text
POST /api/v1/kyc/video/start
Headers
text
Authorization: Bearer <access_token>
Response
json
{
  "success": true,
  "data": {
    "session_id": "video_session_123",
    "url": "https://video-verification.com/session/123",
    "expires_at": "2024-01-01T01:00:00Z"
  }
}
Complete Video Verification
text
POST /api/v1/kyc/video/complete
Headers
text
Authorization: Bearer <access_token>
Request Body
json
{
  "session_id": "video_session_123",
  "verification_code": "code_from_video_session"
}
Get KYC Limits
text
GET /api/v1/kyc/limits
Headers
text
Authorization: Bearer <access_token>
Response
json
{
  "success": true,
  "data": {
    "tier_1": {
      "name": "Basic",
      "deposit_limit_daily": "1000",
      "deposit_limit_monthly": "10000",
      "trading_limit_daily": "5000",
      "withdrawal_limit_daily": "1000",
      "requirements": ["email_verification"]
    },
    "tier_2": {
      "name": "Verified",
      "deposit_limit_daily": "10000",
      "deposit_limit_monthly": "100000",
      "trading_limit_daily": "50000",
      "withdrawal_limit_daily": "10000",
      "requirements": ["government_id", "proof_of_address"]
    },
    "tier_3": {
      "name": "Institutional",
      "deposit_limit_daily": "1000000",
      "deposit_limit_monthly": "unlimited",
      "trading_limit_daily": "unlimited",
      "withdrawal_limit_daily": "500000",
      "requirements": ["corporate_documents", "director_verification"]
    }
  }
}
Admin: Get User KYC
text
GET /api/v1/admin/kyc/users/{user_id}
Headers
text
Authorization: Bearer <admin_token>
Admin: Verify KYC Document
text
POST /api/v1/admin/kyc/documents/{document_id}/verify
Headers
text
Authorization: Bearer <admin_token>
Request Body
json
{
  "status": "approved",
  "notes": "Document verified successfully"
}
Admin: Reject KYC Document
text
POST /api/v1/admin/kyc/documents/{document_id}/reject
Headers
text
Authorization: Bearer <admin_token>
Request Body
json
{
  "reason": "Document is blurry",
  "instructions": "Please upload a clearer image"
}
Admin: Get Pending KYC
text
GET /api/v1/admin/kyc/pending
Headers
text
Authorization: Bearer <admin_token>
Query Parameters
Parameter	Type	Description
page	int	Page number
limit	int	Items per page
KYC Document Types
Type	Description	Accepted Formats
passport	International passport	JPG, PNG, PDF
government_id	National ID card	JPG, PNG, PDF
driver_license	Driver's license	JPG, PNG, PDF
proof_of_address	Utility bill, bank statement	JPG, PNG, PDF
selfie	Photo holding ID	JPG, PNG
corporate_documents	Business registration	PDF
proof_of_funds	Bank statement	PDF
KYC Tiers
Tier	Name	Description
0	Unverified	Basic access, limited functionality
1	Basic	Email verified, low limits
2	Verified	ID verified, higher limits
3	Enhanced	Additional verification, high limits
4	Institutional	Corporate accounts, unlimited
text

```bash
nano ~/dev/TXdocumentation/marketplace/services.md
markdown
# Marketplace Services

Detailed documentation for all marketplace services.

## Service Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ Service Layer │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ User Service │ Auth Service │ Asset Service │ Order Management │ │
│ │ Wallet Svc │ KYC Service │ Holdings Svc │ Record Service │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Support Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Email Svc │ Notification │ File Service │ Document Service │ │
│ │ MiniCMS Svc │ Feature Flag │ Alert Svc │ Comment Service │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Data Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Open Search │ Reference Svc │ Update Svc │ AED Service │ │
│ │ Contact List │ │ │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Core Services

### User Service

Manages user accounts, profiles, and authentication.

#### Methods

| Method | Description |
|--------|-------------|
| `createUser()` | Create new user account |
| `getUser()` | Retrieve user by ID |
| `updateUser()` | Update user profile |
| `deleteUser()` | Soft delete user account |
| `verifyEmail()` | Verify user email |
| `changePassword()` | Change user password |
| `resetPassword()` | Initiate password reset |
| `enable2FA()` | Enable 2-factor authentication |
| `disable2FA()` | Disable 2FA |
| `getUserByEmail()` | Lookup user by email |

#### Events

| Event | Description |
|-------|-------------|
| `user.created` | User account created |
| `user.updated` | Profile updated |
| `user.email_verified` | Email verification completed |
| `user.password_changed` | Password changed |
| `user.deleted` | Account deleted |

### Auth Service

Handles authentication and authorization.

#### Methods

| Method | Description |
|--------|-------------|
| `login()` | Authenticate user |
| `logout()` | Invalidate session |
| `refreshToken()` | Refresh access token |
| `validateToken()` | Verify JWT token |
| `checkPermission()` | Verify user permissions |
| `getUserRoles()` | Get user roles and permissions |

#### Auth Firebase Service

Firebase authentication integration.

| Method | Description |
|--------|-------------|
| `verifyFirebaseToken()` | Verify Firebase ID token |
| `syncFirebaseUser()` | Sync Firebase user with local DB |
| `createFirebaseUser()` | Create user in Firebase |
| `deleteFirebaseUser()` | Remove user from Firebase |

### Asset Service

Manages marketplace assets and metadata.

#### Methods

| Method | Description |
|--------|-------------|
| `createAsset()` | Register new asset |
| `getAsset()` | Get asset by ID |
| `listAssets()` | List all assets with filters |
| `updateAsset()` | Update asset metadata |
| `deleteAsset()` | Remove asset (admin only) |
| `getAssetPrice()` | Get current asset price |
| `getPriceHistory()` | Get historical price data |
| `getOrderBook()` | Get current order book |
| `searchAssets()` | Search assets by criteria |

### Order Management Service

Processes trade orders and manages order book.

#### Methods

| Method | Description |
|--------|-------------|
| `createOrder()` | Create new trade order |
| `cancelOrder()` | Cancel existing order |
| `getOrder()` | Get order details |
| `listOrders()` | List user orders |
| `matchOrders()` | Match buy/sell orders |
| `executeOrder()` | Execute matched order |
| `getOrderBook()` | Get current order book |

#### Order States
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Pending │───▶│ Open │───▶│ Partial │───▶│ Filled │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
│ │ │ │
│ ▼ │ │
│ ┌──────────┐ │ │
└─────────▶│ Cancelled│◀────────┘ │
└──────────┘ │
│ │
▼ │
┌──────────┐ │
│ Expired │◀────────────────────────┘
└──────────┘

text

### Holdings Service

Tracks user asset holdings and balances.

#### Methods

| Method | Description |
|--------|-------------|
| `getHoldings()` | Get user asset holdings |
| `updateHoldings()` | Update holdings after trade |
| `lockHoldings()` | Lock holdings for pending order |
| `unlockHoldings()` | Release locked holdings |
| `getBalance()` | Get balance for specific asset |
| `getTotalValue()` | Calculate total portfolio value |

### Wallet Service

Manages user wallets and blockchain interactions.

#### Methods

| Method | Description |
|--------|-------------|
| `createWallet()` | Generate new blockchain wallet |
| `getWallet()` | Get wallet details |
| `getBalance()` | Get wallet balance |
| `deposit()` | Process deposit |
| `withdraw()` | Process withdrawal |
| `signTransaction()` | Sign blockchain transaction |
| `broadcastTransaction()` | Broadcast to blockchain |

### KYC Service

Manages identity verification.

#### Methods

| Method | Description |
|--------|-------------|
| `submitDocuments()` | Submit KYC documents |
| `verifyDocuments()` | Verify submitted documents |
| `getStatus()` | Get KYC verification status |
| `getLimits()` | Get tier-based limits |
| `startVideoCall()` | Initiate video verification |
| `completeVideoCall()` | Complete video verification |
| `updateTier()` | Upgrade user tier |

## Support Services

### Email Service

Handles email delivery and templates.

#### Methods

| Method | Description |
|--------|-------------|
| `sendEmail()` | Send email |
| `sendTemplateEmail()` | Send templated email |
| `verifyEmail()` | Send verification email |
| `sendPasswordReset()` | Send password reset email |
| `sendWelcomeEmail()` | Send welcome email |

#### Email Templates

| Template | Purpose |
|----------|---------|
| `welcome` | New user welcome |
| `verify_email` | Email verification |
| `reset_password` | Password reset |
| `kyc_status` | KYC status update |
| `order_confirmation` | Order confirmation |
| `trade_execution` | Trade executed |
| `withdrawal_confirmation` | Withdrawal processed |

### Notification Service

Manages user notifications.

#### Methods

| Method | Description |
|--------|-------------|
| `sendNotification()` | Send notification |
| `markAsRead()` | Mark notification as read |
| `getNotifications()` | Get user notifications |
| `deleteNotification()` | Delete notification |
| `setPreferences()` | Update notification preferences |

#### Notification Types

| Type | Channel | Description |
|------|---------|-------------|
| price_alert | push, email | Price threshold alerts |
| order_update | push, email | Order status changes |
| trade_executed | push, email | Trade confirmation |
| kyc_update | email | KYC verification status |
| security_alert | push, email | Suspicious activity |

### File Service

Manages file uploads and storage.

#### Methods

| Method | Description |
|--------|-------------|
| `uploadFile()` | Upload file |
| `getFile()` | Download file |
| `deleteFile()` | Delete file |
| `getFileInfo()` | Get file metadata |
| `validateFile()` | Validate file type/size |

#### Supported File Types

| Type | Extensions | Max Size |
|------|------------|----------|
| Image | JPG, PNG, GIF | 10 MB |
| Document | PDF, DOC, DOCX | 25 MB |
| Spreadsheet | XLS, XLSX | 10 MB |
| Video | MP4, MOV | 100 MB |

### Document Service

Manages document storage and retrieval.

#### Methods

| Method | Description |
|--------|-------------|
| `storeDocument()` | Store document |
| `retrieveDocument()` | Get document |
| `updateDocument()` | Update document |
| `deleteDocument()` | Delete document |
| `verifyDocument()` | Verify document authenticity |

### Feature Flag Service

Manages feature toggles.

#### Methods

| Method | Description |
|--------|-------------|
| `isEnabled()` | Check if feature is enabled |
| `getFlags()` | Get all feature flags |
| `setFlag()` | Set feature flag (admin) |
| `getUserFlags()` | Get flags for user |

### Alert Service

Manages price alerts and notifications.

#### Methods

| Method | Description |
|--------|-------------|
| `createAlert()` | Create new price alert |
| `deleteAlert()` | Delete alert |
| `getAlerts()` | Get user alerts |
| `triggerAlert()` | Check and trigger alerts |
| `updateAlert()` | Update alert settings |

### Comment Service

Manages user comments on assets.

#### Methods

| Method | Description |
|--------|-------------|
| `createComment()` | Post comment |
| `getComments()` | Get asset comments |
| `updateComment()` | Edit comment |
| `deleteComment()` | Delete comment |
| `reportComment()` | Report inappropriate comment |
| `moderateComment()` | Admin comment moderation |

### MiniCMS Service

Manages content pages.

#### Methods

| Method | Description |
|--------|-------------|
| `getPage()` | Get content page |
| `listPages()` | List all pages |
| `createPage()` | Create new page |
| `updatePage()` | Update page |
| `deletePage()` | Delete page |
| `getMenu()` | Get navigation menu |

### Open Search Service

Provides search functionality.

#### Methods

| Method | Description |
|--------|-------------|
| `search()` | Perform search |
| `indexDocument()` | Index document |
| `updateDocument()` | Update index |
| `deleteDocument()` | Remove from index |
| `getSuggestions()` | Get search suggestions |

### Record Service

Manages transaction records.

#### Methods

| Method | Description |
|--------|-------------|
| `createRecord()` | Create transaction record |
| `getRecord()` | Get record by ID |
| `listRecords()` | List user records |
| `exportRecords()` | Export records to CSV/PDF |
| `verifyRecord()` | Verify record authenticity |

### Update Service

Provides real-time updates via WebSocket.

#### Methods

| Method | Description |
|--------|-------------|
| `subscribe()` | Subscribe to updates |
| `unsubscribe()` | Unsubscribe |
| `broadcast()` | Broadcast update |
| `getStatus()` | Get connection status |

#### Update Channels

| Channel | Description |
|---------|-------------|
| `trades` | Real-time trade updates |
| `orders` | Order status updates |
| `prices` | Price ticker updates |
| `balances` | Balance updates |
| `notifications` | User notifications |

### Reference Service

Manages reference data.

#### Methods

| Method | Description |
|--------|-------------|
| `getCountries()` | Get country list |
| `getCurrencies()` | Get currency list |
| `getAssetCategories()` | Get asset categories |
| `getDocumentTypes()` | Get KYC document types |
| `getJurisdictions()` | Get jurisdiction list |

### Contact List Service

Manages user contact lists.

#### Methods

| Method | Description |
|--------|-------------|
| `addContact()` | Add to contact list |
| `removeContact()` | Remove from contacts |
| `getContacts()` | Get contact list |
| `blockContact()` | Block user |
| `unblockContact()` | Unblock user |

### AED Service (Asset Exchange Data)

Provides market data and analytics.

#### Methods

| Method | Description |
|--------|-------------|
| `getMarketData()` | Get market data |
| `getOHLC()` | Get OHLC data |
| `getVolume()` | Get trading volume |
| `getMarketCap()` | Get market cap |
| `getLiquidity()` | Get liquidity metrics |

## Service Communication

### REST APIs

Services expose REST endpoints for external communication.

### gRPC

Internal service-to-service communication uses gRPC for performance.

### Message Queue

Async operations use message queues (RabbitMQ/Kafka).

### WebSocket

Real-time updates delivered via WebSocket connections.

## Service Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DB_HOST` | Database host |
| `DB_PORT` | Database port |
| `REDIS_URL` | Redis connection URL |
| `KAFKA_BROKERS` | Kafka broker addresses |
| `JWT_SECRET` | JWT signing secret |
| `FIREBASE_CONFIG` | Firebase service account |

### Health Checks

Each service exposes health endpoints:

| Endpoint | Description |
|----------|-------------|
| `/health` | Basic health status |
| `/health/ready` | Readiness probe |
| `/health/live` | Liveness probe |
| `/metrics` | Prometheus metrics |

## Service Dependencies
┌─────────────┐
│ API │
│ Gateway │
└──────┬──────┘
│
┌────────────┼────────────┐
│ │ │
▼ ▼ ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Auth │ │ User │ │ Asset │
└──────────┘ └──────────┘ └──────────┘
│ │ │
└────────────┼────────────┘
│
┌──────▼──────┐
│ Order │
│ Mgmt │
└──────┬──────┘
│
┌────────────┼────────────┐
│ │ │
▼ ▼ ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Holdings │ │ Wallet │ │ Record │
└──────────┘ └──────────┘ └──────────┘

text

Now create the final index update:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Update with the complete table of contents:

markdown
# TX Marketplace API Documentation

Complete API documentation for the TX Blockchain Marketplace platform.

## Documentation Index

### API Endpoints

| API | Description | Documentation |
|-----|-------------|---------------|
| Admin API | Administrative operations | [admin-api.md](./admin-api.md) |
| Account API | User account management | [account-api.md](./account-api.md) |
| **Asset API** | Asset management and trading | [asset-api.md](./asset-api.md) |
| Certificate API | Digital certificates | [certificate-api.md](./certificate-api.md) |
| Comment API | User comments | [comment-api.md](./comment-api.md) |
| Document API | Document management | [document-api.md](./document-api.md) |
| Feature Flag API | Feature toggles | [feature-flag-api.md](./feature-flag-api.md) |
| File API | File upload/storage | [file-api.md](./file-api.md) |
| Jurisdiction Asset API | Regional compliance | [jurisdiction-asset-api.md](./jurisdiction-asset-api.md) |
| Jurisdiction API | Legal frameworks | [jurisdiction-api.md](./jurisdiction-api.md) |
| **KYC Document API** | Identity verification | [kyc-api.md](./kyc-api.md) |
| MiniCMS API | Content management | [minicms-api.md](./minicms-api.md) |
| Notification API | User notifications | [notification-api.md](./notification-api.md) |
| Organization API | Institutional accounts | [organization-api.md](./organization-api.md) |
| Smart Contract API | Contract management | [smart-contract-api.md](./smart-contract-api.md) |
| **User API** | User profiles and auth | [user-api.md](./user-api.md) |

### Services

| Service | Description | Documentation |
|---------|-------------|---------------|
| **Services Overview** | All services | [services.md](./services.md) |

### Data Models

| Model | Description | Documentation |
|-------|-------------|---------------|
| **Data Models** | All data models | [data-models.md](./data-models.md) |

## Quick Reference

### Authentication

```bash
# Login
curl -X POST https://api.tx.marketplace/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Use token
curl -X GET https://api.tx.marketplace/v1/users/profile \
  -H "Authorization: Bearer <token>"
Common Endpoints
bash
# List assets
GET /api/v1/assets

# Get asset details
GET /api/v1/assets/{asset_id}

# Get user holdings
GET /api/v1/users/holdings

# Get KYC status
GET /api/v1/kyc/status

# Submit KYC documents
POST /api/v1/kyc/documents
Environment URLs
Environment	API Base URL	Dashboard URL
Devnet	https://api.devnet.tx.marketplace	https://devnet.tx.marketplace
Testnet	https://api.testnet.tx.marketplace	https://testnet.tx.marketplace
Mainnet	https://api.tx.marketplace	https://tx.marketplace
Support
API Status: status.tx.marketplace

Documentation: docs.tx.marketplace

Support Email: support@tx.marketplace

Developer Discord: discord.gg/tx-marketplace
