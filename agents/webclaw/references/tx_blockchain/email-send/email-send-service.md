# Email Send Service

The Email Send Service provides a gRPC endpoint for sending templated emails. Unlike most services in the platform, this service is designed for **internal use only** - it is called by other services rather than being exposed as an end-user or admin HTTP interface.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Email Send Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ gRPC Endpoint (Internal) │ │
│ │ │ │
│ │ Send(SendEmailRequest) returns (SendEmailResponse) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Email Processing Pipeline │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ 1. Fetch template from Email Template Service │ │
│ │ 2. Check for organization-specific custom templates │ │
│ │ 3. Apply translations (if needed) │ │
│ │ 4. Populate template data based on template type │ │
│ │ 5. Send email via SendGrid │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Services │ │
│ ├───────────────┬───────────────┬─────────────────────────────────────┤ │
│ │ Email Template│ Translation │ SendGrid │ │
│ │ Service │ Service │ (Email Delivery) │ │
│ └───────────────┴───────────────┴─────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Access Level | Description |
|----------|--------------|-------------|
| Send (gRPC) | Internal Services Only | Send templated emails |

**Note:** This service is for internal use only. It does not expose HTTP endpoints and should only be called by other backend services.

## Protocol Buffer Definition

### SendEmailRequest

```protobuf
message SendEmailRequest {
    string RecipientEmail = 1;                      // Email address of recipient
    string RecipientName = 2;                       // Full name of recipient
    emailtemplate.EmailTemplateType EmailTemplateType = 3;  // Type of template to use
    string OrganizationID = 4;                      // Organization UUID
    metadata.Network Network = 5;                   // Network (mainnet, testnet, devnet)
    optional language.Language Language = 6;        // Language for translation (optional)
}
SendEmailResponse
protobuf
message SendEmailResponse {
    bool Success = 1;                               // Whether email was sent
    string MessageId = 2;                          // SendGrid message ID
    string Error = 3;                              // Error message if any
}
EmailTemplateType Enum
Type	Description
KYC_VERIFICATION	KYC verification status notification
KYC_REJECTION	KYC rejection notification
KYC_APPROVAL	KYC approval notification
WELCOME_EMAIL	New user welcome email
PASSWORD_RESET	Password reset request
EMAIL_VERIFICATION	Email address verification
TRANSACTION_CONFIRMATION	Transaction confirmation
WITHDRAWAL_REQUEST	Withdrawal request notification
DEPOSIT_CONFIRMATION	Deposit confirmation
ACCOUNT_SUSPENDED	Account suspension notification
ACCOUNT_REACTIVATED	Account reactivation notification
SECURITY_ALERT	Security alert notification
NEW_DEVICE_LOGIN	New device login notification
Language Enum
Value	Language
LANG_NOT_USED	Use default (no translation)
ENGLISH	English
SPANISH	Spanish
FRENCH	French
GERMAN	German
ITALIAN	Italian
PORTUGUESE	Portuguese
DUTCH	Dutch
CHINESE_SIMPLIFIED	Simplified Chinese
CHINESE_TRADITIONAL	Traditional Chinese
JAPANESE	Japanese
KOREAN	Korean
RUSSIAN	Russian
ARABIC	Arabic
Network Enum
Value	Network
NETWORK_MAINNET	Production network
NETWORK_TESTNET	Testing network
NETWORK_DEVNET	Development network
Email Sending Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Email Sending Flow                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Service calls Send(SendEmailRequest)                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ SendEmailRequest {                                                   │   │
│  │   RecipientEmail: "user@example.com"                                 │   │
│  │   RecipientName: "John Doe"                                          │   │
│  │   EmailTemplateType: KYC_APPROVAL                                    │   │
│  │   OrganizationID: "org-123"                                          │   │
│  │   Network: NETWORK_MAINNET                                           │   │
│  │   Language: ENGLISH                                                  │   │
│  │ }                                                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Step 1: Fetch Template                                               │   │
│  │ • Call Email Template Service                                        │   │
│  │ • Get template by Type + OrganizationID + Network                    │   │
│  │ • Check for organization-specific custom template                    │   │
│  │ • Fall back to default template if no custom exists                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Step 2: Apply Translation (Conditional)                              │   │
│  │ • Check if translation is needed:                                    │   │
│  │   - Not a custom organization template                               │   │
│  │   - Valid language specified (not LANG_NOT_USED)                     │   │
│  │   - Language is not ENGLISH                                          │   │
│  │ • Call Translation Service if needed                                 │   │
│  │ • Replace template strings with translated content                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Step 3: Populate Template Data                                       │   │
│  │ • Get data structure from EmailTemplateDataRegistry                  │   │
│  │ • Populate with request-specific data                                │   │
│  │ • Example for KYC_APPROVAL:                                          │   │
│  │   - UserName: "John Doe"                                             │   │
│  │   - AccountID: "core1abc..."                                         │   │
│  │   - ApprovalDate: "2024-01-01"                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Step 4: Render Email                                                 │   │
│  │ • Replace placeholders with actual data                              │   │
│  │ • Generate HTML and plain text versions                              │   │
│  │ • Apply organization branding (if configured)                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Step 5: Send via SendGrid                                            │   │
│  │ • Build SendGrid API request                                         │   │
│  │ • Set from address (configured per organization)                     │   │
│  │ • Set recipient, subject, body                                       │   │
│  │ • Send email                                                         │   │
│  │ • Return MessageId on success                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Response: SendEmailResponse                                          │   │
│  │ {                                                                    │   │
│  │   Success: true,                                                     │   │
│  │   MessageId: "sendgrid_message_123456"                               │   │
│  │ }                                                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Template Data Registry
The EmailTemplateDataRegistry maps template types to their corresponding data structures. Each template type has a specific data structure defined in the registry.

KYC Email Templates
go
type KYCEmailData struct {
    UserName        string   // User's full name
    RejectionReason string   // Reason for KYC rejection (if applicable)
    ExternalUserID  string   // External user identifier
    AccountID       string   // Blockchain account ID
    ClientComment   string   // Comment from client
    AdminComment    string   // Comment from admin
}
Welcome Email Template
go
type WelcomeEmailData struct {
    UserName        string   // User's full name
    AccountID       string   // Blockchain account ID
    VerificationLink string  // Link to verify email
    DashboardURL    string   // URL to user dashboard
    SupportEmail    string   // Support contact email
}
Transaction Email Templates
go
type TransactionEmailData struct {
    UserName        string   // User's full name
    TransactionID   string   // Transaction identifier
    Amount          string   // Transaction amount
    Asset           string   // Asset type (e.g., "USD", "BTC")
    Status          string   // Transaction status
    Timestamp       string   // Transaction timestamp
    Fee             string   // Transaction fee
    FromAddress     string   // Sender address
    ToAddress       string   // Recipient address
    TxHash          string   // Blockchain transaction hash
}
Security Email Templates
go
type SecurityEmailData struct {
    UserName        string   // User's full name
    DeviceName      string   // Device name (for new device login)
    DeviceType      string   // Device type (mobile, desktop)
    Location        string   // Geographic location
    IPAddress       string   // IP address
    Timestamp       string   // Login timestamp
    ResetLink       string   // Password reset link (if applicable)
    SupportEmail    string   // Support contact email
}
Language Support
Translation Conditions
The service applies translation to email content only when ALL of the following conditions are met:

Condition	Description
✅ Not a custom organization template	Custom templates are assumed to already be in the correct language
✅ Valid language specified	Language is not LANG_NOT_USED
✅ Language is not ENGLISH	English is the default and doesn't need translation
Supported Languages
Language Code	Language	Translation Service Support
en	English	No translation needed (default)
es	Spanish	Yes
fr	French	Yes
de	German	Yes
it	Italian	Yes
pt	Portuguese	Yes
nl	Dutch	Yes
zh-CN	Simplified Chinese	Yes
zh-TW	Traditional Chinese	Yes
ja	Japanese	Yes
ko	Korean	Yes
ru	Russian	Yes
ar	Arabic	Yes
Translation Process
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Translation Process                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Original Template (English)                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Subject: Welcome to {{.PlatformName}}, {{.UserName}}!                │   │
│  │ Body: Thank you for joining {{.PlatformName}}.                       │   │
│  │        Your account ID: {{.AccountID}}                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Translation Service (NOTIFICATION_PARSER_LIB)                        │   │
│  │ • Detects language: en → es                                          │   │
│  │ • Translates template strings                                        │   │
│  │ • Preserves placeholders ({{.Variable}})                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Translated Template (Spanish)                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Subject: ¡Bienvenido a {{.PlatformName}}, {{.UserName}}!             │   │
│  │ Body: Gracias por unirte a {{.PlatformName}}.                        │   │
│  │        Tu ID de cuenta: {{.AccountID}}                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Data Population                                                     │   │
│  │ • Replace {{.UserName}} with actual user name                       │   │
│  │ • Replace {{.AccountID}} with actual account ID                     │   │
│  │ • Replace {{.PlatformName}} with organization name                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Adding New Template Types
To add support for new email template types, follow these steps:

Step 1: Define Template Type
Add the new template type to com-fs-email-template-model/domain/emailtemplatedmn.go:

go
const (
    // Existing types...
    EmailTemplateTypeNewFeature    EmailTemplateType = 15
    EmailTemplateTypeMaintenance   EmailTemplateType = 16
    EmailTemplateTypeSurvey        EmailTemplateType = 17
)
Step 2: Define Data Structure
Create the data structure for your template:

go
type NewFeatureEmailData struct {
    UserName        string   // User's full name
    FeatureName     string   // Name of the new feature
    FeatureDescription string // Description of the feature
    LearnMoreURL    string   // URL to learn more
    ReleaseDate     string   // Feature release date
}
Step 3: Register in EmailTemplateDataRegistry
go
func init() {
    // Register the new template type
    RegisterTemplateData(EmailTemplateTypeNewFeature, func() interface{} {
        return &NewFeatureEmailData{}
    })
}
Step 4: Create Template
Create the email template in the Email Template Service:

sql
INSERT INTO email_templates (
    template_type,
    organization_id,
    network,
    subject,
    body_html,
    body_text,
    created_at
) VALUES (
    15,  -- EmailTemplateTypeNewFeature
    NULL,  -- Default template (all organizations)
    1,  -- NETWORK_MAINNET
    'New Feature Alert: {{.FeatureName}}',
    '<html><body><h1>Hello {{.UserName}}!</h1><p>{{.FeatureDescription}}</p><a href="{{.LearnMoreURL}}">Learn More</a></body></html>',
    'Hello {{.UserName}}!\n\n{{.FeatureDescription}}\n\nLearn more: {{.LearnMoreURL}}',
    NOW()
);
Step 5: Test
go
// Test the new template
request := &SendEmailRequest{
    RecipientEmail:   "test@example.com",
    RecipientName:    "Test User",
    EmailTemplateType: EmailTemplateTypeNewFeature,
    OrganizationID:   "org-123",
    Network:          NETWORK_MAINNET,
    Language:         ENGLISH,
}

response, err := client.Send(context.Background(), request)
Integration Examples
Go gRPC Client
go
package main

import (
    "context"
    "log"
    "time"

    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    
    emailpb "github.com/sologenic/com-fs-email-send-service/proto"
    templatepb "github.com/sologenic/com-fs-email-template-model/proto"
)

type EmailSendClient struct {
    client emailpb.EmailSendServiceClient
    conn   *grpc.ClientConn
}

func NewEmailSendClient(endpoint string) (*EmailSendClient, error) {
    conn, err := grpc.Dial(
        endpoint,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
    )
    if err != nil {
        return nil, err
    }
    
    return &EmailSendClient{
        client: emailpb.NewEmailSendServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *EmailSendClient) Close() error {
    return c.conn.Close()
}

func (c *EmailSendClient) SendKYCApprovalEmail(
    ctx context.Context,
    recipientEmail, recipientName string,
    organizationID string,
    network templatepb.Network,
) error {
    request := &emailpb.SendEmailRequest{
        RecipientEmail:    recipientEmail,
        RecipientName:     recipientName,
        EmailTemplateType: templatepb.EmailTemplateType_KYC_APPROVAL,
        OrganizationID:    organizationID,
        Network:           network,
        Language:          templatepb.Language_ENGLISH,
    }
    
    response, err := c.client.Send(ctx, request)
    if err != nil {
        return err
    }
    
    if !response.Success {
        log.Printf("Email send failed: %s", response.Error)
        return nil
    }
    
    log.Printf("Email sent successfully! MessageID: %s", response.MessageId)
    return nil
}

func (c *EmailSendClient) SendWelcomeEmail(
    ctx context.Context,
    recipientEmail, recipientName, accountID string,
    organizationID string,
    network templatepb.Network,
    language templatepb.Language,
) error {
    request := &emailpb.SendEmailRequest{
        RecipientEmail:    recipientEmail,
        RecipientName:     recipientName,
        EmailTemplateType: templatepb.EmailTemplateType_WELCOME_EMAIL,
        OrganizationID:    organizationID,
        Network:           network,
        Language:          language,
    }
    
    // The actual template data is populated by the service
    // based on the EmailTemplateType and organization context
    
    response, err := c.client.Send(ctx, request)
    if err != nil {
        return err
    }
    
    if !response.Success {
        return fmt.Errorf("email send failed: %s", response.Error)
    }
    
    return nil
}

// Usage
func main() {
    client, err := NewEmailSendClient("localhost:50051")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    
    // Send KYC approval email
    err = client.SendKYCApprovalEmail(
        ctx,
        "user@example.com",
        "John Doe",
        "org-123",
        templatepb.Network_NETWORK_MAINNET,
    )
    if err != nil {
        log.Printf("Error sending email: %v", err)
    }
}
Node.js gRPC Client
javascript
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const PROTO_PATH = './proto/email-send-service.proto';

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const proto = grpc.loadPackageDefinition(packageDefinition);

class EmailSendClient {
  constructor(endpoint) {
    this.client = new proto.email.EmailSendService(
      endpoint,
      grpc.credentials.createInsecure()
    );
  }

  async sendEmail(request) {
    return new Promise((resolve, reject) => {
      this.client.Send(request, (error, response) => {
        if (error) {
          reject(error);
        } else {
          resolve(response);
        }
      });
    });
  }

  async sendKYCApprovalEmail(recipientEmail, recipientName, organizationID, network) {
    const request = {
      RecipientEmail: recipientEmail,
      RecipientName: recipientName,
      EmailTemplateType: 'KYC_APPROVAL',
      OrganizationID: organizationID,
      Network: network,
      Language: 'ENGLISH'
    };
    
    return this.sendEmail(request);
  }

  async sendWelcomeEmail(recipientEmail, recipientName, organizationID, network, language) {
    const request = {
      RecipientEmail: recipientEmail,
      RecipientName: recipientName,
      EmailTemplateType: 'WELCOME_EMAIL',
      OrganizationID: organizationID,
      Network: network,
      Language: language
    };
    
    return this.sendEmail(request);
  }

  async sendTransactionConfirmation(recipientEmail, recipientName, organizationID, network) {
    const request = {
      RecipientEmail: recipientEmail,
      RecipientName: recipientName,
      EmailTemplateType: 'TRANSACTION_CONFIRMATION',
      OrganizationID: organizationID,
      Network: network,
      Language: 'ENGLISH'
    };
    
    return this.sendEmail(request);
  }
}

// Usage
async function main() {
  const client = new EmailSendClient('localhost:50051');
  
  try {
    const response = await client.sendKYCApprovalEmail(
      'user@example.com',
      'John Doe',
      'org-123',
      'NETWORK_MAINNET'
    );
    
    console.log('Email sent:', response);
  } catch (error) {
    console.error('Error sending email:', error);
  }
}

main();
Python gRPC Client
python
import grpc
import email_send_service_pb2
import email_send_service_pb2_grpc

class EmailSendClient:
    def __init__(self, endpoint):
        self.channel = grpc.insecure_channel(endpoint)
        self.stub = email_send_service_pb2_grpc.EmailSendServiceStub(self.channel)
    
    def send_email(self, request):
        return self.stub.Send(request)
    
    def send_kyc_approval_email(self, recipient_email, recipient_name, organization_id, network):
        request = email_send_service_pb2.SendEmailRequest(
            RecipientEmail=recipient_email,
            RecipientName=recipient_name,
            EmailTemplateType='KYC_APPROVAL',
            OrganizationID=organization_id,
            Network=network,
            Language='ENGLISH'
        )
        return self.send_email(request)
    
    def send_welcome_email(self, recipient_email, recipient_name, organization_id, network, language):
        request = email_send_service_pb2.SendEmailRequest(
            RecipientEmail=recipient_email,
            RecipientName=recipient_name,
            EmailTemplateType='WELCOME_EMAIL',
            OrganizationID=organization_id,
            Network=network,
            Language=language
        )
        return self.send_email(request)
    
    def send_transaction_confirmation(self, recipient_email, recipient_name, organization_id, network):
        request = email_send_service_pb2.SendEmailRequest(
            RecipientEmail=recipient_email,
            RecipientName=recipient_name,
            EmailTemplateType='TRANSACTION_CONFIRMATION',
            OrganizationID=organization_id,
            Network=network,
            Language='ENGLISH'
        )
        return self.send_email(request)
    
    def close(self):
        self.channel.close()

# Usage
def main():
    client = EmailSendClient('localhost:50051')
    
    try:
        response = client.send_kyc_approval_email(
            'user@example.com',
            'John Doe',
            'org-123',
            'NETWORK_MAINNET'
        )
        
        print(f"Email sent: {response.Success}")
        print(f"Message ID: {response.MessageId}")
        
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    main()
Environment Configuration
Required Environment Variables
Environment Variable	Description	Source
GRPC_PORT	Port the gRPC server listens on	Configuration
SENDGRID_CONFIG	SendGrid API key for sending emails	SendGrid
EMAIL_TEMPLATE_STORE	Email template gRPC endpoint	com-fs-email-template-model
NOTIFICATION_PARSER_LIB	Translation gRPC endpoint	com-fs-notification-translation-model
GRPC_APPEND	Suffix to append to gRPC service names	Configuration
Example Environment Configuration
bash
# Required
GRPC_PORT=50051
SENDGRID_CONFIG='{"api_key": "SG.xxxxxxxxxxxxx"}'
EMAIL_TEMPLATE_STORE=localhost:50052
NOTIFICATION_PARSER_LIB=localhost:50053
GRPC_APPEND=dev

# Optional
LOG_LEVEL=debug
MAX_RETRIES=3
RETRY_DELAY_MS=1000
SEND_TIMEOUT_SECONDS=30
BATCH_SIZE=10
Docker Compose Example
yaml
version: '3.8'

services:
  email-send-service:
    image: sologenic/email-send-service:latest
    environment:
      - GRPC_PORT=50051
      - SENDGRID_CONFIG={"api_key":"${SENDGRID_API_KEY}"}
      - EMAIL_TEMPLATE_STORE=email-template-service:50052
      - NOTIFICATION_PARSER_LIB=translation-service:50053
      - GRPC_APPEND=prod
      - LOG_LEVEL=info
    ports:
      - "50051:50051"
    networks:
      - internal
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50051"]
      interval: 30s
      timeout: 10s
      retries: 3

  email-template-service:
    image: sologenic/email-template-service:latest
    environment:
      - GRPC_PORT=50052
      - DATABASE_URL=postgres://user:pass@postgres:5432/email_templates
    networks:
      - internal

  translation-service:
    image: sologenic/translation-service:latest
    environment:
      - GRPC_PORT=50053
      - TRANSLATION_API_KEY=${TRANSLATION_API_KEY}
    networks:
      - internal

networks:
  internal:
    driver: bridge
Kubernetes Deployment
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: email-send-service
  namespace: sologenic
spec:
  replicas: 3
  selector:
    matchLabels:
      app: email-send-service
  template:
    metadata:
      labels:
        app: email-send-service
    spec:
      containers:
      - name: email-send-service
        image: gcr.io/sologenic-platform/email-send-service:latest
        ports:
        - containerPort: 50051
          name: grpc
        env:
        - name: GRPC_PORT
          value: "50051"
        - name: SENDGRID_CONFIG
          valueFrom:
            secretKeyRef:
              name: sendgrid-secret
              key: config
        - name: EMAIL_TEMPLATE_STORE
          value: "email-template-service:50052"
        - name: NOTIFICATION_PARSER_LIB
          value: "translation-service:50053"
        - name: GRPC_APPEND
          value: "prod"
        - name: LOG_LEVEL
          value: "info"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          exec:
            command:
            - grpc_health_probe
            - -addr=:50051
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - grpc_health_probe
            - -addr=:50051
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: email-send-service
  namespace: sologenic
spec:
  selector:
    app: email-send-service
  ports:
  - port: 50051
    targetPort: 50051
    name: grpc
  type: ClusterIP
---
apiVersion: v1
kind: Secret
metadata:
  name: sendgrid-secret
  namespace: sologenic
type: Opaque
stringData:
  config: |
    {
      "api_key": "SG.xxxxxxxxxxxxxxxxxxxxx",
      "from_email": "noreply@sologenic.org",
      "from_name": "Sologenic Platform"
    }
Error Handling
Common Errors
Error	Cause	Solution
Invalid template type	Template type not registered	Register template type in registry
Template not found	No template for type/organization	Create default template
Translation failed	Translation service unavailable	Fall back to English
SendGrid error	Invalid API key or rate limit	Check SendGrid configuration
Invalid recipient	Malformed email address	Validate email before sending
Error Response Example
json
{
  "Success": false,
  "MessageId": "",
  "Error": "Template not found for type KYC_APPROVAL and organization org-123"
}
Best Practices
Performance
Aspect	Recommendation
Batch sending	Group emails when possible
Async sending	Use async/await or callbacks
Connection pooling	Reuse gRPC connections
Retry logic	Implement exponential backoff
Reliability
go
// Implement retry logic
func (c *EmailSendClient) SendWithRetry(
    ctx context.Context,
    request *SendEmailRequest,
    maxRetries int,
) (*SendEmailResponse, error) {
    var lastError error
    
    for i := 0; i < maxRetries; i++ {
        response, err := c.client.Send(ctx, request)
        if err == nil && response.Success {
            return response, nil
        }
        
        lastError = err
        if response != nil && response.Error != "" {
            lastError = fmt.Errorf(response.Error)
        }
        
        // Exponential backoff
        time.Sleep(time.Duration(math.Pow(2, float64(i))) * 100 * time.Millisecond)
    }
    
    return nil, fmt.Errorf("failed after %d retries: %w", maxRetries, lastError)
}
Security
Never log email content in production

Validate recipient email addresses

Use TLS for gRPC communication

Rotate SendGrid API keys regularly

Implement rate limiting per organization

Monitoring
go
// Add metrics collection
func (c *EmailSendClient) SendWithMetrics(
    ctx context.Context,
    request *SendEmailRequest,
) (*SendEmailResponse, error) {
    start := time.Now()
    
    response, err := c.client.Send(ctx, request)
    
    duration := time.Since(start)
    
    // Record metrics
    metrics.EmailSendDuration.Observe(duration.Seconds())
    metrics.EmailSendTotal.Inc()
    
    if err != nil || (response != nil && !response.Success) {
        metrics.EmailSendErrors.Inc()
    }
    
    return response, err
}
Related Services
Service	Description
Email Template Service	Template storage and management
Translation Service	Content translation
Notification Service	Notification orchestration
User Service	User email preferences
Organization Service	Organization email configuration
Troubleshooting
Debug Commands
bash
# Check if service is healthy
grpc_health_probe -addr=localhost:50051

# List available services
grpcurl -plaintext localhost:50051 list

# Describe the Send method
grpcurl -plaintext localhost:50051 describe email.EmailSendService.Send

# Test send email
grpcurl -plaintext -d '{
  "RecipientEmail": "test@example.com",
  "RecipientName": "Test User",
  "EmailTemplateType": "WELCOME_EMAIL",
  "OrganizationID": "org-123",
  "Network": "NETWORK_TESTNET",
  "Language": "ENGLISH"
}' localhost:50051 email.EmailSendService/Send
Log Analysis
bash
# View service logs
kubectl logs -f deployment/email-send-service -n sologenic

# Filter errors
kubectl logs deployment/email-send-service -n sologenic | grep ERROR

# Check SendGrid delivery
kubectl logs deployment/email-send-service -n sologenic | grep "MessageId"
License
This documentation is part of the TX Marketplace platform.
