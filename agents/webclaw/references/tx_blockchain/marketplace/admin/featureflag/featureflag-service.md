# Admin Feature Flag Service

The Admin Feature Flag Service provides RESTful interfaces for managing feature flags across the marketplace platform. Feature flags enable dynamic feature toggling, gradual rollouts, A/B testing, and runtime configuration without redeploying services.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Admin Feature Flag Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├─────────────────────┬─────────────────────┬───────────────────────┤ │
│ │ GET /get │ GET /list │ PUT /update │ │
│ │ (Get by name) │ (List with filter) │ (Update flag) │ │
│ └─────────────────────┴─────────────────────┴───────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ Feature Flag │ Role Store │ Auth Service │ Organization Store│ │
│ │ Store │ │ │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Feature Flag Consumers │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • UI Components (feature visibility) │ │
│ │ • API Gateways (route enable/disable) │ │
│ │ • Backend Services (behavior toggles) │ │
│ │ • Mobile Apps (client-side flags) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/featureflag/get | ORGANIZATION_ADMINISTRATOR | Retrieve feature flag by name |
| GET /api/featureflag/list | ORGANIZATION_ADMINISTRATOR | List all feature flags with filter |
| PUT /api/featureflag/update | ORGANIZATION_ADMINISTRATOR | Update feature flag |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header
- Network in `Network` header (mainnet, testnet, devnet)

## Feature Flag Data Model

### FeatureFlag Object

| Field | Type | Description |
|-------|------|-------------|
| Name | string | Unique feature flag identifier |
| OrganizationID | string | Organization UUID (or empty for global flags) |
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |
| Enabled | boolean | Current enabled/disabled state |
| Description | string | Human-readable description of the feature |
| Attributes | map<string, string> | Additional configuration attributes |
| TargetUsers | []string | Specific users for gradual rollout |
| TargetPercentage | int | Percentage of users to enable for (0-100) |
| CreatedAt | timestamp | Creation timestamp |
| UpdatedAt | timestamp | Last update timestamp |
| UpdatedBy | string | User who last updated the flag |

### Filter Object (for GET /list)

```protobuf
message Filter {
    optional string Name = 1;
    optional string OrganizationID = 2;
    optional bool Enabled = 3;
    optional int32 Offset = 4;
    optional int32 Limit = 5;
    optional string Network = 6;
}
API Endpoints
GET /api/featureflag/get
Retrieves the FeatureFlag information for the given featureflag_name.

Query Parameters
Parameter	Type	Description	Required
featureflag_name	string	Unique name of the feature flag	Yes
Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/featureflag/get?featureflag_name=new_trading_ui" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet"
Example Response
json
{
  "FeatureFlag": {
    "Name": "new_trading_ui",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Network": 1,
    "Enabled": true,
    "Description": "Enable the new trading interface with advanced charting",
    "Attributes": {
      "theme": "dark",
      "chart_library": "tradingview",
      "refresh_rate": "1000"
    },
    "TargetUsers": [
      "user1@example.com",
      "user2@example.com"
    ],
    "TargetPercentage": 25,
    "CreatedAt": {
      "seconds": 1700000000,
      "nanos": 0
    },
    "UpdatedAt": {
      "seconds": 1700005000,
      "nanos": 123456000
    },
    "UpdatedBy": "admin@organization.org"
  },
  "MetaData": {
    "Version": 3,
    "LastModified": "2024-01-15T10:30:00Z"
  }
}
Error Responses
Status Code	Description
200	Success - Feature flag found
400	Bad request - Missing featureflag_name
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Feature flag does not exist
GET /api/featureflag/list
Retrieves all FeatureFlags information using the provided filter, with pagination.

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
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
# Filter for enabled flags with pagination
curl -X GET \
  "https://api.admin.sologenic.org/api/featureflag/list?filter=ewogICJFbmFibGVkIjogdHJ1ZSwKICAiTGltaXQiOiAyMCwKICAiT2Zmc2V0IjogMAp9" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet"
Example Response
json
{
  "FeatureFlags": [
    {
      "Name": "new_trading_ui",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Network": 1,
      "Enabled": true,
      "Description": "Enable the new trading interface",
      "Attributes": {},
      "TargetUsers": [],
      "TargetPercentage": 100,
      "CreatedAt": {
        "seconds": 1700000000,
        "nanos": 0
      },
      "UpdatedAt": {
        "seconds": 1700005000,
        "nanos": 0
      },
      "UpdatedBy": "admin@organization.org"
    },
    {
      "Name": "instant_settlement",
      "OrganizationID": "",
      "Network": 1,
      "Enabled": false,
      "Description": "Enable instant settlement for trades",
      "Attributes": {
        "max_amount": "10000",
        "supported_assets": "USD,EUR"
      },
      "TargetUsers": [],
      "TargetPercentage": 0,
      "CreatedAt": {
        "seconds": 1699900000,
        "nanos": 0
      },
      "UpdatedAt": {
        "seconds": 1699950000,
        "nanos": 0
      },
      "UpdatedBy": "system"
    },
    {
      "Name": "mobile_biometrics",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Network": 2,
      "Enabled": true,
      "Description": "Enable biometric authentication on mobile",
      "Attributes": {
        "min_ios_version": "15.0",
        "min_android_version": "12.0"
      },
      "TargetUsers": [
        "beta_tester_1@example.com",
        "beta_tester_2@example.com"
      ],
      "TargetPercentage": 10,
      "CreatedAt": {
        "seconds": 1699800000,
        "nanos": 0
      },
      "UpdatedAt": {
        "seconds": 1699850000,
        "nanos": 0
      },
      "UpdatedBy": "product_manager@organization.org"
    }
  ],
  "Offset": 20,
  "Total": 45
}
PUT /api/featureflag/update
Updates a FeatureFlag for the given FeatureFlagName.

Request Body
Field	Type	Description	Required
FeatureFlag.Name	string	Unique feature flag identifier	Yes
FeatureFlag.OrganizationID	string	Organization UUID (empty for global)	No
FeatureFlag.Network	int	Network identifier	Yes
FeatureFlag.Enabled	boolean	Enabled/disabled state	Yes
FeatureFlag.Description	string	Human-readable description	No
FeatureFlag.Attributes	map<string, string>	Additional configuration	No
FeatureFlag.TargetUsers	[]string	Specific user whitelist	No
FeatureFlag.TargetPercentage	int	Percentage rollout (0-100)	No
Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
Authorization	Bearer <firebase_token>	Yes
Example Request
bash
curl -X PUT "https://api.admin.sologenic.org/api/featureflag/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "Network: mainnet" \
  -d '{
    "FeatureFlag": {
      "Name": "new_trading_ui",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Network": 1,
      "Enabled": true,
      "Description": "Enable the new trading interface with advanced charting and real-time updates",
      "Attributes": {
        "theme": "dark",
        "chart_library": "tradingview",
        "refresh_rate": "500",
        "default_view": "advanced"
      },
      "TargetUsers": [
        "premium_user_1@example.com",
        "premium_user_2@example.com"
      ],
      "TargetPercentage": 50
    }
  }'
Success Response
text
200 OK
json
{
  "Success": true,
  "Message": "Feature flag updated successfully",
  "FeatureFlag": {
    "Name": "new_trading_ui",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Network": 1,
    "Enabled": true,
    "UpdatedAt": {
      "seconds": 1700010000,
      "nanos": 0
    },
    "UpdatedBy": "admin@organization.org"
  }
}
Error Responses
Status Code	Description
400	Bad request - Missing required fields or invalid values
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Feature flag does not exist
409	Conflict - Version mismatch or concurrent update
Feature Flag Use Cases
1. Feature Rollout
Gradually enable new features to reduce risk:

Phase	TargetPercentage	Description
Internal testing	0% (specific users)	Internal team only
Alpha	1-5%	Early adopters
Beta	10-25%	Broader testing
General availability	50-100%	All users
2. A/B Testing
Compare different implementations:

json
{
  "Name": "checkout_v2",
  "Enabled": true,
  "TargetPercentage": 50,
  "Attributes": {
    "variant": "B",
    "tracking_id": "ab_test_001"
  }
}
3. Regional Rollouts
Enable features based on jurisdiction:

json
{
  "Name": "derivatives_trading",
  "Enabled": true,
  "TargetUsers": ["user_1", "user_2"],
  "Attributes": {
    "jurisdictions": "US,UK,EU",
    "min_balance": "25000"
  }
}
4. Emergency Kill Switch
Quickly disable problematic features:

json
{
  "Name": "automated_trading",
  "Enabled": false,
  "Description": "TEMPORARILY DISABLED - Investigating performance issues"
}
Common Feature Flag Examples
UI Features
Flag Name	Description	Default
dashboard_v2	New dashboard layout	false
advanced_charts	TradingView integration	false
dark_mode	Dark theme support	true
mobile_app_redesign	New mobile UI	false
Trading Features
Flag Name	Description	Default
margin_trading	Leveraged trading	false
stop_loss_orders	Advanced order types	true
fractional_shares	Fractional asset trading	false
instant_settlement	Real-time settlement	false
Compliance Features
Flag Name	Description	Default
enhanced_kyc	Stricter verification	false
travel_rule	FATF compliance	false
transaction_monitoring	AML checks	true
sanctions_screening	OFAC compliance	true
Performance Features
Flag Name	Description	Default
websocket_realtime	Real-time updates	true
batch_processing	Bulk operations	false
redis_caching	Response caching	true
cdn_acceleration	Static asset CDN	true
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/
AUTH_SERVICE	Authentication service endpoint	github.com/sologenic/com-fs-auth-model/
ROLE_STORE	Role store service endpoint	github.com/sologenic/com-fs-role-model/
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model/
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-store/
Optional Environment Variables
Environment Variable	Description
GRPC_APPEND	Segment of the service URL that follows the service keyword (e.g., "dfjiao-ijgao.a.run.app")
LOG_LEVEL	Logging level (info, debug, warn, error)
Base64 Filter Encoding Examples
Example 1: Filter by Enabled Status
json
{
  "Enabled": true,
  "Limit": 20,
  "Offset": 0
}
Base64 encoded:

text
ewogICJFbmFibGVkIjogdHJ1ZSwKICAiTGltaXQiOiAyMCwKICAiT2Zmc2V0IjogMAp9
Example 2: Filter by Name Pattern
json
{
  "Name": "trading",
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Limit": 50
}
Base64 encoded:

text
ewogICJOYW1lIjogInRyYWRpbmciLAogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJMaW1pdCI6IDUwCn0=
Example 3: All Flags for Organization
json
{
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Limit": 100,
  "Offset": 0
}
Base64 encoded:

text
ewogICJPcmdhbml6YXRpb25JRCI6ICI3MmM0YzA3Mi0yZmU0LTRmNzItYWU5ZC1kOWQ1MmEwNWZkNzEiLAogICJMaW1pdCI6IDEwMCwKICAiT2Zmc2V0IjogMAp9
Feature Flag Evaluation Logic
When a client checks if a feature is enabled:

text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Feature Flag Evaluation Flow                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Client Request (User: user@example.com)                                   │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Check if flag exists                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│           │                                                                 │
│           ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Check if flag is globally enabled                                │   │
│  │    (Enabled = false → return false)                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│           │ (Enabled = true)                                              │
│           ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. Check TargetUsers whitelist                                      │   │
│  │    (User in list → return true)                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│           │ (User not in whitelist)                                      │
│           ▼                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. Check TargetPercentage                                           │   │
│  │    (hash(user_id) % 100 < percentage → return true)                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│           │                                                                 │
│           ▼                                                                 │
│  Return false (user not in rollout)                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Gradual Rollout Strategy
Recommended Rollout Plan
Stage	Duration	Target%	Success Criteria
Internal	1-2 days	Specific users	No critical bugs
Canary	2-3 days	1%	Error rate < 0.1%
Early adopter	3-5 days	5-10%	Positive feedback
General	5-7 days	25-50%	Metrics stable
Full	After approval	100%	All metrics green
Rollback Plan
bash
# Emergency rollback - disable immediately
curl -X PUT /api/featureflag/update \
  -d '{
    "FeatureFlag": {
      "Name": "problematic_feature",
      "Enabled": false,
      "Description": "EMERGENCY DISABLE - Investigating issue #12345"
    }
  }'
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
  "message": "Invalid request parameters",
  "details": "TargetPercentage must be between 0 and 100"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Feature flag not found",
  "details": "No feature flag found with name: non_existent_flag"
}
Conflict (409)
json
{
  "error": "Conflict",
  "message": "Feature flag was modified concurrently",
  "details": "Please refresh and try again"
}
Best Practices
Naming Conventions
Type	Pattern	Example
UI features	{component}_{feature}	dashboard_new_charts
Backend features	{service}_{capability}	trading_margin_enabled
Beta features	beta_{feature}	beta_social_trading
Experimental	experiment_{name}	experiment_recommendation_engine
Flag Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Feature Flag Lifecycle                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │ Created  │───▶│ Alpha    │───▶│ Beta     │───▶│ GA       │             │
│  │ (0%)     │    │ (1-5%)   │    │ (10-25%) │    │ (100%)   │             │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘             │
│                                                          │                  │
│                                                          ▼                  │
│                                                   ┌──────────┐             │
│                                                   │ Removed  │             │
│                                                   │ (Cleanup)│             │
│                                                   └──────────┘             │
│                                                                             │
│  Best Practice: Remove flags after feature is fully adopted                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Documentation Requirements
Each feature flag should have:

Description: Clear purpose and expected behavior

Owner: Team or person responsible

Rollout Plan: Gradual enablement strategy

Rollback Procedure: Steps to disable if issues arise

Removal Date: When to clean up the flag

Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Flag not working	Wrong network	Check Network header matches flag's network
Flag not found	Misspelled name	Verify exact flag name
Users not seeing feature	TargetPercentage too low	Increase rollout percentage
Permission denied	Insufficient role	Ensure user has ORGANIZATION_ADMINISTRATOR
Concurrent update conflict	Multiple admins	Refresh and retry update
Debugging
Check flag status:

bash
# Get specific flag
curl -X GET /api/featureflag/get?featureflag_name=my_feature \
  -H "Network: mainnet" \
  -H "Authorization: Bearer <token>"

# List all flags for organization
curl -X GET /api/featureflag/list?filter=<org_filter> \
  -H "Network: mainnet" \
  -H "Authorization: Bearer <token>"
Related Services
Service	Description
Admin Account Service	User and role management
Organization Service	Organization management
Admin Asset Service	Asset management
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the admin feature flag service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the admin feature flag service section:

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

**Key Features:**
- Retrieve feature flags by name
- List all feature flags with filtering
- Update feature flag configuration
- Gradual rollout with percentage-based targeting
- User-specific whitelisting
- A/B testing support
- Emergency kill switch capability

**Feature Flag Use Cases:**
| Use Case | Description |
|----------|-------------|
| Feature Rollout | Gradual enablement to reduce risk |
| A/B Testing | Compare different implementations |
| Regional Rollouts | Enable based on jurisdiction |
| Emergency Kill Switch | Quickly disable problematic features |

**Quick Examples:**
```bash
# Get feature flag
GET /api/featureflag/get?featureflag_name=new_trading_ui

# List flags
GET /api/featureflag/list?filter=<base64_filter>

# Update flag
PUT /api/featureflag/update
Account Types:

Sologenic Administrator (Platform level)

Organization Administrator (Organization level)

KYC Administrator

Broker Asset Administrator

Normal User (End User)

