# Email Template Service

The Email Template Service provides RESTful interfaces for managing email templates used by the Email Send Service. It supports two levels of template management:

1. **System Templates** - Global templates managed by Sologenic admins
2. **Organization Templates** - Custom templates per organization managed by organization admins

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Email Template Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ System Template Management (Sologenic Admin Only) │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ GET /system/ │ GET /system/ │ POST /system/ │ DELETE /system/ │ │
│ │ get │ list │ upsert │ delete │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Organization Template Management (Organization Admin Only) │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ GET /get │ GET /list │ POST /upsert │ POST /reset │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Template Resolution │ │
│ │ │ │
│ │ Organization Template? ──Yes──► Return Organization Template │ │
│ │ │ │ │
│ │ No │ │
│ │ ▼ │ │
│ │ System Template ─────────────► Return System Template │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Email Template│ Account Store │ Role Store │ Organization │ │
│ │ Store │ │ │ Store │ │
│ │ Feature Flag │ Auth Firebase │ HTTP Config │ │ │
│ │ Store │ Service │ │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/emailtemplate/system/get | SOLOGENIC_ADMIN | Get system template by type |
| GET /api/emailtemplate/system/list | SOLOGENIC_ADMIN | List all system templates |
| POST /api/emailtemplate/system/upsert | SOLOGENIC_ADMIN | Create/update system template |
| DELETE /api/emailtemplate/system/delete | SOLOGENIC_ADMIN | Delete system template |
| GET /api/emailtemplate/get | ORGANIZATION_ADMINISTRATOR | Get organization template |
| GET /api/emailtemplate/list | ORGANIZATION_ADMINISTRATOR | List organization templates |
| POST /api/emailtemplate/upsert | ORGANIZATION_ADMINISTRATOR | Create/update organization template |
| POST /api/emailtemplate/reset | ORGANIZATION_ADMINISTRATOR | Reset to system template |

**Note:** 
- All admin endpoints are protected by role-based access control
- Permissions are managed dynamically by Organization administrators
- If organization-network specific template is not found, the system template is returned

## Data Models

### EmailTemplate Object

| Field | Type | Description |
|-------|------|-------------|
| Type | int | Email template type (see EmailTemplateType) |
| OrganizationID | string | Organization UUID (empty for system templates) |
| Network | int | Network (0=system default, 1=mainnet, 2=testnet, 3=devnet) |
| Name | string | Template display name |
| Subject | string | Email subject line (supports placeholders) |
| HTML | string | HTML email body (supports placeholders) |
| Description | string | Template description/purpose |
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |

### Audit Object

| Field | Type | Description |
|-------|------|-------------|
| ChangedBy | string | Email of user who made the change |
| ChangedAt | Timestamp | When the change was made |
| Reason | string | Reason for the change (optional) |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

### EmailTemplateType Values

| Type ID | Template Name | Description | Placeholders |
|---------|---------------|-------------|--------------|
| 1 | KYC_APPROVAL | KYC verification approved | {{.UserName}}, {{.AccountID}} |
| 2 | KYC_REJECTION | KYC verification rejected | {{.UserName}}, {{.RejectionReason}} |
| 3 | KYC_PENDING | KYC verification pending | {{.UserName}} |
| 4 | KYC_REVIEW | KYC needs additional review | {{.UserName}}, {{.ClientComment}} |
| 5 | WELCOME_EMAIL | New user welcome | {{.UserName}}, {{.AccountID}}, {{.VerificationLink}} |
| 6 | PASSWORD_RESET | Password reset request | {{.UserName}}, {{.ResetLink}} |
| 7 | EMAIL_VERIFICATION | Email address verification | {{.UserName}}, {{.VerificationLink}} |
| 8 | TRANSACTION_CONFIRMATION | Transaction confirmation | {{.UserName}}, {{.TransactionID}}, {{.Amount}}, {{.Asset}} |
| 9 | WITHDRAWAL_REQUEST | Withdrawal request notification | {{.UserName}}, {{.Amount}}, {{.Address}} |
| 10 | DEPOSIT_CONFIRMATION | Deposit confirmation | {{.UserName}}, {{.Amount}}, {{.Asset}}, {{.TxHash}} |
| 11 | ACCOUNT_SUSPENDED | Account suspension notification | {{.UserName}}, {{.Reason}} |
| 12 | ACCOUNT_REACTIVATED | Account reactivation notification | {{.UserName}} |
| 13 | SECURITY_ALERT | Security alert notification | {{.UserName}}, {{.AlertType}}, {{.IPAddress}} |
| 14 | NEW_DEVICE_LOGIN | New device login notification | {{.UserName}}, {{.DeviceName}}, {{.Location}} |
| 15 | ORGANIZATION_ONBOARDING | Organization welcome email | {{.OrganizationName}}, {{.AdminEmail}} |
| 16 | INVITATION_EMAIL | User invitation | {{.InviterName}}, {{.InviteLink}} |
| 17 | TWO_FACTOR_SETUP | 2FA setup instructions | {{.UserName}}, {{.SetupCode}} |
| 18 | TWO_FACTOR_DISABLED | 2FA disabled notification | {{.UserName}} |
| 19 | LIMIT_INCREASE_APPROVED | Limit increase approved | {{.UserName}}, {{.NewLimit}} |
| 20 | LIMIT_INCREASE_REJECTED | Limit increase rejected | {{.UserName}}, {{.Reason}} |

### Network Values

| Network ID | Network Name | Description |
|------------|--------------|-------------|
| 0 | SYSTEM_DEFAULT | Default system template (all networks) |
| 1 | MAINNET | Production network |
| 2 | TESTNET | Testing network |
| 3 | DEVNET | Development network |

## System Template Endpoints (Sologenic Admin Only)

### GET /api/emailtemplate/system/get

Retrieves a system email template by type. Requires Sologenic admin privileges.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Authorization | Bearer <firebase_token> | Yes |
| Network | mainnet, testnet, devnet | Yes |

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| type | int | Email template type ID | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/emailtemplate/system/get?type=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: mainnet"
Example Response
json
{
  "EmailTemplate": {
    "Type": 1,
    "OrganizationID": "",
    "Name": "System KYC Approval Template",
    "Subject": "Your KYC Verification is Approved",
    "HTML": "<!DOCTYPE html>\n<html>\n<head>\n    <meta charset=\"UTF-8\">\n    <title>User Verification Completed</title>\n    <style>...</style>\n</head>\n<body>\n    <div class=\"container\">\n        <div class=\"header\">\n            <h2>Sologenic KYC Verification</h2>\n        </div>\n        <div class=\"content\">\n            <h1>Hello, {{.UserName}}!</h1>\n            <p>Your KYC verification has been successfully completed. Thank you for choosing our service.</p>\n            <p>If you have any questions, feel free to contact us at support@sologenic.org.</p>\n        </div>\n        <div class=\"footer\">\n            <p>Best regards,<br/>The Sologenic Team</p>\n        </div>\n    </div>\n</body>\n</html>",
    "Description": "System template sent when a user's KYC is approved",
    "CreatedAt": {
      "seconds": 1740518732,
      "nanos": 171972000
    },
    "UpdatedAt": {
      "seconds": 1740518732,
      "nanos": 171974000
    },
    "Network": 0
  },
  "Audit": {
    "ChangedBy": "admin@sologenic.org",
    "ChangedAt": {
      "seconds": 1740518732,
      "nanos": 171974000
    },
    "Reason": "Initial template creation"
  }
}
GET /api/emailtemplate/system/list
Returns a list of all system email templates. Requires Sologenic admin privileges.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/emailtemplate/system/list" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: testnet"
Example Response
json
{
  "EmailTemplates": [
    {
      "EmailTemplate": {
        "Type": 1,
        "OrganizationID": "",
        "Name": "System KYC Approval Template",
        "Subject": "Your KYC Verification is Approved",
        "HTML": "<!DOCTYPE html>\n...",
        "Description": "System template sent when a user's KYC is approved",
        "CreatedAt": {
          "seconds": 1741636052,
          "nanos": 876859000
        },
        "UpdatedAt": {
          "seconds": 1741636052,
          "nanos": 876860000
        },
        "Network": 0
      },
      "Audit": {
        "ChangedBy": "sg.be.test@gmail.com",
        "ChangedAt": {
          "seconds": 1741636052,
          "nanos": 876860000
        },
        "Reason": ""
      }
    },
    {
      "EmailTemplate": {
        "Type": 15,
        "OrganizationID": "",
        "Name": "System Organization Onboarding Template",
        "Subject": "Welcome to Solotex - Your Organization is Ready",
        "HTML": "<!DOCTYPE html>\n..",
        "Description": "System welcome email for new organizations onboarded to Solotex",
        "CreatedAt": {
          "seconds": 1741634227,
          "nanos": 863946000
        },
        "UpdatedAt": {
          "seconds": 1741634227,
          "nanos": 863947000
        },
        "Network": 0
      },
      "Audit": {
        "ChangedBy": "sg.be.test@gmail.com",
        "ChangedAt": {
          "seconds": 1741634227,
          "nanos": 863947000
        },
        "Reason": ""
      }
    },
    {
      "EmailTemplate": {
        "Type": 2,
        "OrganizationID": "",
        "Name": "System KYC Rejection Template",
        "Subject": "Your KYC Verification Status",
        "HTML": "<!DOCTYPE html>\n...",
        "Description": "System template sent when a user's KYC is rejected",
        "CreatedAt": {
          "seconds": 1741636975,
          "nanos": 185997000
        },
        "UpdatedAt": {
          "seconds": 1741636975,
          "nanos": 185998000
        },
        "Network": 0
      },
      "Audit": {
        "ChangedBy": "sg.be.test@gmail.com",
        "ChangedAt": {
          "seconds": 1741636975,
          "nanos": 185998000
        },
        "Reason": ""
      }
    }
  ]
}
POST /api/emailtemplate/system/upsert
Creates a new system email template or updates an existing one. Requires Sologenic admin privileges.

Important: For creating a new template, there are prerequisites. Refer to the README.md in com-fs-email-template-model for details on adding new template types.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
Request Body
Field	Type	Description	Required
EmailTemplate	EmailTemplate	Template object	Yes
Audit	Audit	Audit information	No
Example Request (Create)
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/emailtemplate/system/upsert" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: testnet" \
  -d '{
    "EmailTemplate": {
      "Type": 1,
      "Name": "System KYC Approval Template",
      "Subject": "Your KYC Verification is Approved",
      "Description": "System template sent when a user's KYC is approved",
      "HTML": "<!DOCTYPE html>\n<html>\n<head>\n    <meta charset=\"UTF-8\">\n    <title>User Verification Completed</title>\n    <style>\n        body {\n            font-family: Arial, sans-serif;\n            background-color: #f4f4f4;\n            margin: 0;\n            padding: 0;\n        }\n        .container {\n            width: 100%;\n            max-width: 600px;\n            margin: 0 auto;\n            background-color: #ffffff;\n            padding: 20px;\n            border-radius: 10px;\n            box-shadow: 0 0 10px rgba(0,0,0,0.1);\n        }\n        .header {\n            background-color: #007bff;\n            color: #ffffff;\n            padding: 10px;\n            border-radius: 10px 10px 0 0;\n            text-align: center;\n        }\n        .content {\n            padding: 20px;\n        }\n        .content h1 {\n            color: #333333;\n        }\n        .content p {\n            color: #555555;\n        }\n        .footer {\n            text-align: center;\n            color: #777777;\n            padding: 10px;\n            border-top: 1px solid #eeeeee;\n        }\n        .footer a {\n            color: #007bff;\n            text-decoration: none;\n        }\n        .button {\n            display: inline-block;\n            padding: 10px 20px;\n            margin-top: 20px;\n            background-color: #007bff;\n            color: #ffffff;\n            text-align: center;\n            border-radius: 5px;\n            text-decoration: none;\n            font-size: 16px;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"container\">\n        <div class=\"header\">\n            <h2>Sologenic KYC Verification</h2>\n        </div>\n        <div class=\"content\">\n            <h1>Hello, {{.UserName}}!</h1>\n            <p>Your KYC verification has been successfully completed. Thank you for choosing our service.</p>\n            <p>If you have any questions, feel free to contact us at <a href=\"mailto:support@sologenic.org\">support@sologenic.org</a>.</p>\n            <a href=\"https://sologenic.org\" class=\"button\">Visit Our Website</a>\n        </div>\n        <div class=\"footer\">\n            <p>Best regards,<br/>The Sologenic Team</p>\n            <p>&copy; 2024 Sologenic. All rights reserved.</p>\n        </div>\n    </div>\n</body>\n</html>"
    },
    "Audit": {
      "Reason": "Initial template creation"
    }
  }'
Example Response
json
{
  "Success": true,
  "Message": "Template upserted successfully"
}
DELETE /api/emailtemplate/system/delete
Deletes a system email template. Requires Sologenic admin privileges.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
Request Body
Field	Type	Description	Required
EmailTemplate	EmailTemplate	Template to delete (Type field required)	Yes
Example Request
bash
curl -X DELETE \
  "https://api.admin.sologenic.org/api/emailtemplate/system/delete" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: mainnet" \
  -d '{
    "EmailTemplate": {
      "Type": 1
    }
  }'
Example Response
json
{
  "Success": true,
  "Message": "Template deleted successfully"
}
Organization Template Endpoints (Organization Admin Only)
GET /api/emailtemplate/get
Retrieves an organization-specific email template by type. If no organization template exists, returns the system template. Requires organization admin privileges.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Query Parameters
Parameter	Type	Description	Required
type	int	Email template type ID	Yes
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/emailtemplate/get?type=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet"
Example Response (Organization Template Exists)
json
{
  "EmailTemplate": {
    "Type": 1,
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Network": 2,
    "Name": "Custom KYC Approval Template",
    "Subject": "Your KYC Verification is Complete",
    "HTML": "<!DOCTYPE html>\n<html>\n<head>\n    <meta charset=\"UTF-8\">\n    <title>Your KYC is Approved</title>\n    <style>...</style>\n</head>\n<body>\n    <div class=\"container\">\n        <div class=\"header\">\n            <h2>KYC Verification Complete</h2>\n        </div>\n        <div class=\"content\">\n            <h1>Hello, {{.UserName}}!</h1>\n            <p>Your KYC verification has been approved. You may now access all platform features.</p>\n        </div>\n        <div class=\"footer\">\n            <p>Best regards,<br/>The Example Company Team</p>\n        </div>\n    </div>\n</body>\n</html>",
    "Description": "Organization-specific template sent when a user's KYC is approved",
    "CreatedAt": {
      "seconds": 1740519032,
      "nanos": 471972000
    },
    "UpdatedAt": {
      "seconds": 1740519032,
      "nanos": 471974000
    }
  },
  "Audit": {
    "ChangedBy": "org-admin@example.com",
    "ChangedAt": {
      "seconds": 1740519032,
      "nanos": 471974000
    }
  }
}
Example Response (No Organization Template - Returns System Template)
json
{
  "EmailTemplate": {
    "Type": 1,
    "OrganizationID": "",
    "Name": "System KYC Approval Template",
    "Subject": "Your KYC Verification is Approved",
    "HTML": "<!DOCTYPE html>\n...",
    "Description": "System template sent when a user's KYC is approved",
    "CreatedAt": {
      "seconds": 1740518732,
      "nanos": 171972000
    },
    "UpdatedAt": {
      "seconds": 1740518732,
      "nanos": 171974000
    },
    "Network": 0
  },
  "Audit": {
    "ChangedBy": "admin@sologenic.org",
    "ChangedAt": {
      "seconds": 1740518732,
      "nanos": 171974000
    }
  }
}
GET /api/emailtemplate/list
Retrieves all email templates for an organization (both custom and system fallbacks). Requires organization admin privileges.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Query Parameters
Parameter	Type	Description	Required
include_system	bool	Include system templates as fallbacks	No (default: true)
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/emailtemplate/list" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet"
Example Response
json
{
  "EmailTemplates": [
    {
      "EmailTemplate": {
        "Type": 1,
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Name": "Custom KYC Approval Template",
        "Subject": "Your KYC Verification is Complete",
        "HTML": "<!DOCTYPE html>\n...",
        "Description": "Organization-specific template sent when a user's KYC is approved",
        "CreatedAt": {
          "seconds": 1741641911,
          "nanos": 741847000
        },
        "UpdatedAt": {
          "seconds": 1741641911,
          "nanos": 741848000
        },
        "Network": 2
      },
      "Audit": {
        "ChangedBy": "org-admin@example.com",
        "ChangedAt": {
          "seconds": 1741641911,
          "nanos": 741849000
        },
        "Reason": "Custom branding update"
      }
    },
    {
      "EmailTemplate": {
        "Type": 15,
        "OrganizationID": "",
        "Name": "System Organization Onboarding Template",
        "Subject": "Welcome to Solotex - Your Organization is Ready",
        "HTML": "<!DOCTYPE html>\n...",
        "Description": "System welcome email for new organizations onboarded to Solotex",
        "CreatedAt": {
          "seconds": 1741634227,
          "nanos": 863946000
        },
        "UpdatedAt": {
          "seconds": 1741634227,
          "nanos": 863947000
        },
        "Network": 0
      },
      "Audit": {
        "ChangedBy": "admin@sologenic.org",
        "ChangedAt": {
          "seconds": 1741634227,
          "nanos": 863947000
        },
        "Reason": ""
      }
    },
    {
      "EmailTemplate": {
        "Type": 2,
        "OrganizationID": "",
        "Name": "System KYC Rejection Template",
        "Subject": "Your KYC Verification Status",
        "HTML": "<!DOCTYPE html>\n...",
        "Description": "System template sent when a user's KYC is rejected",
        "CreatedAt": {
          "seconds": 1741636975,
          "nanos": 185997000
        },
        "UpdatedAt": {
          "seconds": 1741636975,
          "nanos": 185998000
        },
        "Network": 0
      },
      "Audit": {
        "ChangedBy": "admin@sologenic.org",
        "ChangedAt": {
          "seconds": 1741636975,
          "nanos": 185998000
        },
        "Reason": ""
      }
    }
  ]
}
POST /api/emailtemplate/upsert
Creates or updates an organization-specific email template. Requires organization admin privileges.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Request Body
Field	Type	Description	Required
EmailTemplate	EmailTemplate	Template object (OrganizationID is auto-populated from header)	Yes
Audit	Audit	Audit information	No
Example Request
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/emailtemplate/upsert" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet" \
  -d '{
    "EmailTemplate": {
      "Type": 1,
      "Name": "Custom KYC Approval Template",
      "Subject": "Your KYC Verification is Complete",
      "Description": "Organization-specific template sent when a user's KYC is approved",
      "HTML": "<!DOCTYPE html>\n<html>\n<head>\n    <meta charset=\"UTF-8\">\n    <title>Your KYC is Approved</title>\n    <style>\n        body {\n            font-family: Arial, sans-serif;\n            background-color: #f5f5f5;\n            margin: 0;\n            padding: 0;\n        }\n        .container {\n            width: 100%;\n            max-width: 600px;\n            margin: 0 auto;\n            background-color: #ffffff;\n            padding: 20px;\n            border-radius: 10px;\n            box-shadow: 0 2px 10px rgba(0,0,0,0.1);\n        }\n        .header {\n            background-color: #28a745;\n            color: #ffffff;\n            padding: 10px;\n            border-radius: 10px 10px 0 0;\n            text-align: center;\n        }\n        .content {\n            padding: 20px;\n        }\n        .content h1 {\n            color: #333333;\n        }\n        .content p {\n            color: #555555;\n        }\n        .footer {\n            text-align: center;\n            color: #777777;\n            padding: 10px;\n            border-top: 1px solid #eeeeee;\n        }\n        .footer a {\n            color: #28a745;\n            text-decoration: none;\n        }\n        .button {\n            display: inline-block;\n            padding: 10px 20px;\n            margin-top: 20px;\n            background-color: #28a745;\n            color: #ffffff;\n            text-align: center;\n            border-radius: 5px;\n            text-decoration: none;\n            font-size: 16px;\n        }\n    </style>\n</head>\n<body>\n    <div class=\"container\">\n        <div class=\"header\">\n            <h2>KYC Verification Complete</h2>\n        </div>\n        <div class=\"content\">\n            <h1>Hello, {{.UserName}}!</h1>\n            <p>Your KYC verification has been approved. You may now access all platform features.</p>\n            <p>If you have any questions, feel free to contact our support team at <a href=\"mailto:support@example.com\">support@example.com</a>.</p>\n            <a href=\"https://example.com/dashboard\" class=\"button\">Go to Dashboard</a>\n        </div>\n        <div class=\"footer\">\n            <p>Best regards,<br/>The Example Company Team</p>\n            <p>&copy; 2024 Example Company. All rights reserved.</p>\n        </div>\n    </div>\n</body>\n</html>"
    },
    "Audit": {
      "Reason": "Custom branding for organization"
    }
  }'
Example Response
json
{
  "Success": true,
  "Message": "Organization template upserted successfully"
}
POST /api/emailtemplate/reset
Resets an organization-specific email template to the system template (removes the custom template). Requires organization admin privileges.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Request Body
Field	Type	Description	Required
Type	int	Email template type ID to reset	Yes
Example Request
bash
curl -X POST \
  "https://api.admin.sologenic.org/api/emailtemplate/reset" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet" \
  -d '{
    "Type": 1
  }'
Example Response
json
{
  "Success": true,
  "Message": "Template reset to system default successfully"
}
Template Resolution Logic
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Template Resolution Flow                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Request: GET /api/emailtemplate/get?type=X                                 │
│  Headers: OrganizationID, Network                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ Does Organization + Network + Type template exist?          │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                          │                                          │   │
│  │            ┌─────────────┴─────────────┐                           │   │
│  │            │ Yes                       │ No                        │   │
│  │            ▼                           ▼                           │   │
│  │  ┌─────────────────┐         ┌─────────────────────────────────┐  │   │
│  │  │ Return          │         │ Does System + Type template     │  │   │
│  │  │ Organization    │         │ exist?                          │  │   │
│  │  │ Template        │         └─────────────────────────────────┘  │   │
│  │  └─────────────────┘                          │                    │   │
│  │                                      ┌─────────┴─────────┐         │   │
│  │                                      │ Yes               │ No      │   │
│  │                                      ▼                   ▼         │   │
│  │                              ┌─────────────┐    ┌─────────────┐    │   │
│  │                              │ Return      │    │ Return      │    │   │
│  │                              │ System      │    │ 404 Not     │    │   │
│  │                              │ Template    │    │ Found       │    │   │
│  │                              └─────────────┘    └─────────────┘    │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Template Placeholders
Available Placeholders by Template Type
Template Type	Placeholders
KYC_APPROVAL (1)	{{.UserName}}, {{.AccountID}}
KYC_REJECTION (2)	{{.UserName}}, {{.RejectionReason}}
KYC_PENDING (3)	{{.UserName}}
KYC_REVIEW (4)	{{.UserName}}, {{.ClientComment}}
WELCOME_EMAIL (5)	{{.UserName}}, {{.AccountID}}, {{.
PASSWORD_RESET (6)	{{.UserName}}, {{.ResetLink}}
EMAIL_VERIFICATION (7)	{{.UserName}}, {{.VerificationLink}}
TRANSACTION_CONFIRMATION (8)	{{.UserName}}, {{.TransactionID}}, {{.Amount}}, {{.Asset}}, {{.TxHash}}
WITHDRAWAL_REQUEST (9)	{{.UserName}}, {{.Amount}}, {{.Asset}}, {{.Address}}
DEPOSIT_CONFIRMATION (10)	{{.UserName}}, {{.Amount}}, {{.Asset}}, {{.TxHash}}
ACCOUNT_SUSPENDED (11)	{{.UserName}}, {{.Reason}}
ACCOUNT_REACTIVATED (12)	{{.UserName}}
SECURITY_ALERT (13)	{{.UserName}}, {{.AlertType}}, {{.IPAddress}}, {{.Timestamp}}
NEW_DEVICE_LOGIN (14)	{{.UserName}}, {{.DeviceName}}, {{.Location}}, {{.IPAddress}}
ORGANIZATION_ONBOARDING (15)	{{.OrganizationName}}, {{.AdminEmail}}, {{.DashboardURL}}
INVITATION_EMAIL (16)	{{.InviterName}}, {{.InviteLink}}, {{.OrganizationName}}
TWO_FACTOR_SETUP (17)	{{.UserName}}, {{.SetupCode}}
TWO_FACTOR_DISABLED (18)	{{.UserName}}
LIMIT_INCREASE_APPROVED (19)	{{.UserName}}, {{.NewLimit}}
LIMIT_INCREASE_REJECTED (20)	{{.UserName}}, {{.Reason}}
HTML Template Guidelines
Best Practices for HTML Templates
html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{.Subject}}</title>
    <style>
        /* Responsive styles */
        @media only screen and (max-width: 600px) {
            .container {
                width: 100% !important;
            }
            .button {
                display: block !important;
                width: 100% !important;
            }
        }
        
        /* Email client compatibility */
        .ExternalClass, .ReadMsgBody {
            width: 100%;
            background-color: #f4f4f4;
        }
        
        /* Consistent rendering */
        body, table, td, p, a {
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }
        
        table, td {
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }
        
        img {
            -ms-interpolation-mode: bicubic;
        }
    </style>
</head>
<body style="margin:0; padding:0; background-color:#f4f4f4; font-family:Arial, sans-serif;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f4f4f4;">
        <tr>
            <td align="center" style="padding:20px;">
                <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" class="container" style="background-color:#ffffff; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="background-color:#007bff; border-radius:10px 10px 0 0; padding:20px;">
                            <h2 style="color:#ffffff; margin:0;">{{.OrganizationName}}</h2>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding:30px;">
                            <h1 style="color:#333333; margin-top:0;">Hello, {{.UserName}}!</h1>
                            {{.Content}}
                            <p style="color:#555555; line-height:1.6;">
                                If you have any questions, feel free to contact us at 
                                <a href="mailto:{{.SupportEmail}}" style="color:#007bff; text-decoration:none;">{{.SupportEmail}}</a>
                            </p>
                            <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:20px;">
                                <tr>
                                    <td align="center" style="background-color:#007bff; border-radius:5px;">
                                        <a href="{{.ActionURL}}" class="button" style="display:inline-block; padding:12px 24px; color:#ffffff; text-decoration:none; font-size:16px;">{{.ActionText}}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="border-top:1px solid #eeeeee; padding:20px; color:#777777; font-size:12px;">
                            <p style="margin:0;">&copy; {{.CurrentYear}} {{.OrganizationName}}. All rights reserved.</p>
                            <p style="margin:10px 0 0;">
                                <a href="{{.UnsubscribeURL}}" style="color:#777777; text-decoration:none;">Unsubscribe</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
Integration Examples
Node.js Admin Client
javascript
class EmailTemplateService {
  constructor(baseUrl, token, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.token = token;
    this.network = network;
  }

  async getSystemTemplate(type) {
    const response = await fetch(
      `${this.baseUrl}/api/emailtemplate/system/get?type=${type}`,
      {
        headers: this._getSystemHeaders()
      }
    );
    return response.json();
  }

  async listSystemTemplates() {
    const response = await fetch(
      `${this.baseUrl}/api/emailtemplate/system/list`,
      {
        headers: this._getSystemHeaders()
      }
    );
    return response.json();
  }

  async upsertSystemTemplate(emailTemplate, reason) {
    const response = await fetch(
      `${this.baseUrl}/api/emailtemplate/system/upsert`,
      {
        method: 'POST',
        headers: this._getSystemHeaders(true),
        body: JSON.stringify({
          EmailTemplate: emailTemplate,
          Audit: { Reason: reason }
        })
      }
    );
    return response.json();
  }

  async deleteSystemTemplate(type) {
    const response = await fetch(
      `${this.baseUrl}/api/emailtemplate/system/delete`,
      {
        method: 'DELETE',
        headers: this._getSystemHeaders(true),
        body: JSON.stringify({
          EmailTemplate: { Type: type }
        })
      }
    );
    return response.json();
  }

  async getOrganizationTemplate(orgId, type) {
    const response = await fetch(
      `${this.baseUrl}/api/emailtemplate/get?type=${type}`,
      {
        headers: this._getOrgHeaders(orgId)
      }
    );
    return response.json();
  }

  async listOrganizationTemplates(orgId, includeSystem = true) {
    const response = await fetch(
      `${this.baseUrl}/api/emailtemplate/list?include_system=${includeSystem}`,
      {
        headers: this._getOrgHeaders(orgId)
      }
    );
    return response.json();
  }

  async upsertOrganizationTemplate(orgId, emailTemplate, reason) {
    const response = await fetch(
      `${this.baseUrl}/api/emailtemplate/upsert`,
      {
        method: 'POST',
        headers: this._getOrgHeaders(orgId, true),
        body: JSON.stringify({
          EmailTemplate: emailTemplate,
          Audit: { Reason: reason }
        })
      }
    );
    return response.json();
  }

  async resetOrganizationTemplate(orgId, type) {
    const response = await fetch(
      `${this.baseUrl}/api/emailtemplate/reset`,
      {
        method: 'POST',
        headers: this._getOrgHeaders(orgId, true),
        body: JSON.stringify({ Type: type })
      }
    );
    return response.json();
  }

  _getSystemHeaders(hasBody = false) {
    const headers = {
      'Authorization': `Bearer: ${this.token}`,
      'Network': this.network
    };
    if (hasBody) {
      headers['Content-Type'] = 'application/json';
    }
    return headers;
  }

  _getOrgHeaders(orgId, hasBody = false) {
    const headers = {
      'Authorization': `Bearer: ${this.token}`,
      'OrganizationID': orgId,
      'Network': this.network
    };
    if (hasBody) {
      headers['Content-Type'] = 'application/json';
    }
    return headers;
  }
}

// Usage
const emailTemplateService = new EmailTemplateService(
  'https://api.admin.sologenic.org',
  'firebase-token',
  'mainnet'
);

// Create organization custom template
await emailTemplateService.upsertOrganizationTemplate(
  'org-123',
  {
    Type: 1,
    Name: 'Custom KYC Approval',
    Subject: 'Welcome to Our Platform!',
    Description: 'Custom welcome email for our organization',
    HTML: '<!DOCTYPE html>...'
  },
  'Organization branding update'
);
Go Admin Client
go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type EmailTemplateService struct {
    BaseURL   string
    Token     string
    Network   string
    HTTPClient *http.Client
}

func NewEmailTemplateService(baseURL, token, network string) *EmailTemplateService {
    return &EmailTemplateService{
        BaseURL:   baseURL,
        Token:     token,
        Network:   network,
        HTTPClient: &http.Client{},
    }
}

type EmailTemplate struct {
    Type           int    `json:"Type"`
    OrganizationID string `json:"OrganizationID,omitempty"`
    Network        int    `json:"Network,omitempty"`
    Name           string `json:"Name"`
    Subject        string `json:"Subject"`
    HTML           string `json:"HTML"`
    Description    string `json:"Description"`
}

type Audit struct {
    ChangedBy string `json:"ChangedBy,omitempty"`
    Reason    string `json:"Reason,omitempty"`
}

type UpsertRequest struct {
    EmailTemplate EmailTemplate `json:"EmailTemplate"`
    Audit         Audit         `json:"Audit,omitempty"`
}

func (s *EmailTemplateService) GetSystemTemplate(templateType int) (*EmailTemplate, error) {
    url := fmt.Sprintf("%s/api/emailtemplate/system/get?type=%d", s.BaseURL, templateType)
    
    req, err := http.NewRequest("GET", url, nil)
    if err != nil {
        return nil, err
    }
    
    req.Header.Set("Authorization", fmt.Sprintf("Bearer: %s", s.Token))
    req.Header.Set("Network", s.Network)
    
    resp, err := s.HTTPClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var result struct {
        EmailTemplate EmailTemplate `json:"EmailTemplate"`
    }
    
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, err
    }
    
    return &result.EmailTemplate, nil
}

func (s *EmailTemplateService) UpsertSystemTemplate(template EmailTemplate, reason string) error {
    request := UpsertRequest{
        EmailTemplate: template,
        Audit: Audit{Reason: reason},
    }
    
    body, err := json.Marshal(request)
    if err != nil {
        return err
    }
    
    url := fmt.Sprintf("%s/api/emailtemplate/system/upsert", s.BaseURL)
    
    req, err := http.NewRequest("POST", url, bytes.NewBuffer(body))
    if err != nil {
        return err
    }
    
    req.Header.Set("Authorization", fmt.Sprintf("Bearer: %s", s.Token))
    req.Header.Set("Network", s.Network)
    req.Header.Set("Content-Type", "application/json")
    
    resp, err := s.HTTPClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        body, _ := io.ReadAll(resp.Body)
        return fmt.Errorf("failed to upsert template: %s", body)
    }
    
    return nil
}

func (s *EmailTemplateService) GetOrganizationTemplate(orgID string, templateType int) (*EmailTemplate, error) {
    url := fmt.Sprintf("%s/api/emailtemplate/get?type=%d", s.BaseURL, templateType)
    
    req, err := http.NewRequest("GET", url, nil)
    if err != nil {
        return nil, err
    }
    
    req.Header.Set("Authorization", fmt.Sprintf("Bearer: %s", s.Token))
    req.Header.Set("OrganizationID", orgID)
    req.Header.Set("Network", s.Network)
    
    resp, err := s.HTTPClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var result struct {
        EmailTemplate EmailTemplate `json:"EmailTemplate"`
    }
    
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, err
    }
    
    return &result.EmailTemplate, nil
}

// Usage
func main() {
    client := NewEmailTemplateService(
        "https://api.admin.sologenic.org",
        "firebase-token",
        "mainnet",
    )
    
    // Get system template
    template, err := client.GetSystemTemplate(1)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    
    fmt.Printf("Template: %s\n", template.Name)
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	com-be-http-lib
EMAIL_TEMPLATE_STORE	Email template store endpoint	com-be-email-template-store
AUTH_FIREBASE_SERVICE	Firebase authentication service	com-fs-auth-firebase-service
ACCOUNT_STORE	Account store endpoint	com-be-admin-account-store
ROLE_STORE	Role store endpoint	com-be-admin-role-store
ORGANIZATION_STORE	Organization service endpoint	com-fs-organization-model
FEATURE_FLAG_STORE	Feature flag service endpoint	fs-feature-flag-model
Example Environment Configuration
bash
# Required
EMAIL_TEMPLATE_STORE=localhost:50063
AUTH_FIREBASE_SERVICE=localhost:50070
ACCOUNT_STORE=localhost:50048
ROLE_STORE=localhost:50066
ORGANIZATION_STORE=localhost:50060
FEATURE_FLAG_STORE=localhost:50055

# Optional
LOG_LEVEL=debug
PAGE_SIZE=50
MAX_PAGE_SIZE=200

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
  email-template-service:
    image: sologenic/email-template-service:latest
    environment:
      - EMAIL_TEMPLATE_STORE=email-template-store:50063
      - AUTH_FIREBASE_SERVICE=auth-service:50070
      - ACCOUNT_STORE=account-store:50048
      - ROLE_STORE=role-store:50066
      - ORGANIZATION_STORE=organization-service:50060
      - FEATURE_FLAG_STORE=feature-flag-service:50055
      - LOG_LEVEL=info
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
    networks:
      - internal

  email-template-store:
    image: sologenic/email-template-store:latest
    environment:
      - DATABASE_URL=postgres://user:pass@postgres:5432/email_templates
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
  "message": "Insufficient permissions. Required role: SOLOGENIC_ADMIN"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Template not found for type: 999"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid template type",
  "details": "Template type must be between 1 and 20"
}
Conflict (409)
json
{
  "error": "Conflict",
  "message": "Template already exists. Use PUT to update."
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Template not found	Wrong type ID	Verify type ID is valid (1-20)
Permission denied	Missing role	Ensure user has SOLOGENIC_ADMIN or ORGANIZATION_ADMINISTRATOR role
HTML not rendering	Malformed HTML	Validate HTML syntax
Placeholders not replaced	Wrong placeholder syntax	Use {{.PlaceholderName}} format
Organization template not returned	Template not created	Check if organization template exists
Debugging
bash
# Enable debug logging
LOG_LEVEL=debug

# Test system template retrieval
curl -X GET "https://api.admin.sologenic.org/api/emailtemplate/system/get?type=1" \
  -H "Authorization: Bearer: <token>" \
  -H "Network: mainnet" \
  -v

# Test organization template upsert
curl -X POST "https://api.admin.sologenic.org/api/emailtemplate/upsert" \
  -H "Authorization: Bearer: <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet" \
  -H "Content-Type: application/json" \
  -d '{"EmailTemplate":{"Type":1,"Name":"Test","Subject":"Test","HTML":"<p>Test</p>"}}' \
  -v
Best Practices
Template Management
Aspect	Recommendation
Version control	Store templates in version control
Testing	Test templates with placeholder data
Fallbacks	Always have system templates as fallbacks
Audit	Always provide reason for changes
HTML Design
Aspect	Recommendation
Responsive	Use responsive design for mobile
Compatibility	Test in major email clients
Accessibility	Include alt text for images
Spam filters	Avoid spam trigger words
Performance
Aspect	Recommendation
Caching	Cache templates in memory
CDN	Serve images from CDN
Size	Keep HTML under 100KB
Related Services
Service	Description
Email Send Service	Uses templates to send emails
Email Template Store	Storage backend for templates
Organization Service	Organization management
Role Service	Permission management
License
This documentation is part of the TX Marketplace platform.
