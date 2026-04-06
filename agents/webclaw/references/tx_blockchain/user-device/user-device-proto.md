# User Device and Session Management Service (User Device Proto)

The User Device proto provides all the functionality required to interact with user device data and session management. This service tracks Firebase tokens for push notifications and session tokens for white-labeling and payments.

## Overview

The User Device service is a gRPC-based system that handles:
- Firebase Cloud Messaging (FCM) tokens for push notifications
- Session tokens for white-labeling and payments
- Device registration and management
- Token lifecycle tracking
- Push notification delivery
- Session validation and management
- Cross-device synchronization

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Mobile App, Web App, Desktop App, Admin Dashboard) │
└───────────────────────────────────┬─────────────────────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ User Device & Session Service │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Device │ │ Firebase │ │ Session │ │ Token │ │
│ │ Management │ │ Token Mgmt │ │ Management │ │ Lifecycle │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Push │ │ White-label │ │ Payment │ │
│ │ Notification│ │ Session │ │ Session │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────────────┬─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Storage Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Device │ │ Token Store │ │ Session │ │ Analytics │ │
│ │ Store │ │ (PostgreSQL)│ │ Store (Redis│ │ Store │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ External Services │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Firebase │ │ Apple APNS │ │ Payment │ │
│ │ Cloud │ │ │ │ Gateway │ │
│ │ Messaging │ │ │ │ │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Data Models

### Firebase Tokens
The model provides the ability to track token usage using the metadata field. If a user replaces a token (automatic replacement may occur by apps), the device ID indicates which token to replace. Tokens have a limited lifespan; when they are older than a determined time, the token can be removed (the device may not connect or have the app any longer).

### Session Tokens
Session tokens are used for:
- White-labeling: Identifying which branded interface to serve
- Payments: Associating payment sessions with users
- Authentication: Maintaining user sessions across devices

## Environment Variables

### Required Variables

| Variable | Description | Format | Example |
|----------|-------------|--------|---------|
| `USER_SESSION_STORE` | gRPC endpoint for user session store service | `host:port` | `user-session-store:50078` |
| `USER_SESSION_STORE_TESTING` | Enable test mode with in-memory buffer | `TRUE` | `TRUE` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TOKEN_EXPIRY_DAYS` | Firebase token expiry in days | `30` |
| `SESSION_EXPIRY_MINUTES` | Session token expiry in minutes | `60` |
| `MAX_DEVICES_PER_USER` | Maximum devices per user | `10` |
| `MAX_SESSIONS_PER_USER` | Maximum active sessions per user | `5` |
| `FCM_API_KEY` | Firebase Cloud Messaging API key | (required for push) |
| `ENABLE_TOKEN_CLEANUP` | Enable automatic token cleanup | `true` |
| `CLEANUP_INTERVAL_HOURS` | Token cleanup interval in hours | `24` |

## Proto Definition

```protobuf
syntax = "proto3";

package userdevice.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/struct.proto";

// User Device & Session Service Definition
service UserDeviceService {
    // Device management
    rpc RegisterDevice(RegisterDeviceRequest) returns (RegisterDeviceResponse);
    rpc UnregisterDevice(UnregisterDeviceRequest) returns (UnregisterDeviceResponse);
    rpc GetDevices(GetDevicesRequest) returns (GetDevicesResponse);
    rpc UpdateDevice(UpdateDeviceRequest) returns (UpdateDeviceResponse);
    rpc GetDevice(GetDeviceRequest) returns (GetDeviceResponse);
    
    // Firebase token management
    rpc RegisterFirebaseToken(RegisterFirebaseTokenRequest) returns (RegisterFirebaseTokenResponse);
    rpc UpdateFirebaseToken(UpdateFirebaseTokenRequest) returns (UpdateFirebaseTokenResponse);
    rpc RemoveFirebaseToken(RemoveFirebaseTokenRequest) returns (RemoveFirebaseTokenResponse);
    rpc GetFirebaseTokens(GetFirebaseTokensRequest) returns (GetFirebaseTokensResponse);
    rpc GetUserFirebaseTokens(GetUserFirebaseTokensRequest) returns (GetUserFirebaseTokensResponse);
    
    // Session token management
    rpc CreateSession(CreateSessionRequest) returns (CreateSessionResponse);
    rpc GetSession(GetSessionRequest) returns (GetSessionResponse);
    rpc ValidateSession(ValidateSessionRequest) returns (ValidateSessionResponse);
    rpc RevokeSession(RevokeSessionRequest) returns (RevokeSessionResponse);
    rpc RevokeAllSessions(RevokeAllSessionsRequest) returns (RevokeAllSessionsResponse);
    rpc ExtendSession(ExtendSessionRequest) returns (ExtendSessionResponse);
    rpc ListUserSessions(ListUserSessionsRequest) returns (ListUserSessionsResponse);
    
    // Push notification delivery
    rpc SendPushNotification(SendPushNotificationRequest) returns (SendPushNotificationResponse);
    rpc SendBulkPushNotification(SendBulkPushNotificationRequest) returns (SendBulkPushNotificationResponse);
    rpc SendTopicNotification(SendTopicNotificationRequest) returns (SendTopicNotificationResponse);
    
    // White-label session management
    rpc CreateWhiteLabelSession(CreateWhiteLabelSessionRequest) returns (CreateWhiteLabelSessionResponse);
    rpc GetWhiteLabelSession(GetWhiteLabelSessionRequest) returns (GetWhiteLabelSessionResponse);
    rpc ValidateWhiteLabelSession(ValidateWhiteLabelSessionRequest) returns (ValidateWhiteLabelSessionResponse);
    
    // Payment session management
    rpc CreatePaymentSession(CreatePaymentSessionRequest) returns (CreatePaymentSessionResponse);
    rpc GetPaymentSession(GetPaymentSessionRequest) returns (GetPaymentSessionResponse);
    rpc UpdatePaymentSession(UpdatePaymentSessionRequest) returns (UpdatePaymentSessionResponse);
    rpc CompletePaymentSession(CompletePaymentSessionRequest) returns (CompletePaymentSessionResponse);
    
    // Token cleanup
    rpc CleanupExpiredTokens(CleanupExpiredTokensRequest) returns (CleanupExpiredTokensResponse);
    rpc GetTokenStats(GetTokenStatsRequest) returns (GetTokenStatsResponse);
    
    // Analytics and monitoring
    rpc GetDeviceAnalytics(GetDeviceAnalyticsRequest) returns (GetDeviceAnalyticsResponse);
    rpc GetSessionAnalytics(GetSessionAnalyticsRequest) returns (GetSessionAnalyticsResponse);
    rpc StreamDeviceEvents(StreamDeviceEventsRequest) returns (stream DeviceEvent);
}

// ==================== Core Messages ====================

// Device platform types
enum DevicePlatform {
    DEVICE_PLATFORM_UNSPECIFIED = 0;
    IOS = 1;
    ANDROID = 2;
    WEB = 3;
    DESKTOP = 4;
    OTHER = 5;
}

// Device status
enum DeviceStatus {
    DEVICE_STATUS_UNSPECIFIED = 0;
    ACTIVE = 1;
    INACTIVE = 2;
    SUSPENDED = 3;
    REMOVED = 4;
}

// Session types
enum SessionType {
    SESSION_TYPE_UNSPECIFIED = 0;
    AUTHENTICATION = 1;     // User authentication session
    WHITE_LABEL = 2;        // White-label branding session
    PAYMENT = 3;            // Payment processing session
    API_ACCESS = 4;         // API access token session
}

// Session status
enum SessionStatus {
    SESSION_STATUS_UNSPECIFIED = 0;
    ACTIVE = 1;
    EXPIRED = 2;
    REVOKED = 3;
    INVALID = 4;
}

// Push notification priority
enum NotificationPriority {
    NOTIFICATION_PRIORITY_UNSPECIFIED = 0;
    HIGH = 1;               // Immediate delivery
    NORMAL = 2;             // Standard delivery
    LOW = 3;                // Background delivery
}

// Device information
message Device {
    string device_id = 1;               // Unique device identifier
    string user_id = 2;                 // Associated user
    string organization_id = 3;         // Organization context
    
    // Device details
    string device_name = 4;              // User-provided name
    DevicePlatform platform = 5;         // iOS, Android, Web, etc.
    string os_version = 6;               // Operating system version
    string app_version = 7;              // Application version
    string model = 8;                    // Device model
    string manufacturer = 9;             // Device manufacturer
    
    // Network information
    string ip_address = 10;              // Last known IP
    string country_code = 11;            // Country from IP
    string timezone = 12;                // Device timezone
    
    // Status
    DeviceStatus status = 13;            // Active, inactive, etc.
    bool is_trusted = 14;                // Trusted device flag
    bool is_primary = 15;                // Primary device flag
    
    // Timestamps
    google.protobuf.Timestamp first_seen_at = 16;
    google.protobuf.Timestamp last_seen_at = 17;
    google.protobuf.Timestamp registered_at = 18;
    google.protobuf.Timestamp updated_at = 19;
    
    // Metadata
    map<string, string> metadata = 20;
    repeated string capabilities = 21;    // push, biometric, etc.
}

// Firebase token for push notifications
message FirebaseToken {
    string token_id = 1;                 // Internal token ID
    string device_id = 2;                // Associated device
    string user_id = 3;                  // Associated user
    string organization_id = 4;          // Organization context
    
    // Token details
    string fcm_token = 5;                // Firebase Cloud Messaging token
    string apns_token = 6;               // Apple Push Notification token (iOS)
    string push_provider = 7;            // fcm, apns, webpush
    
    // Token metadata
    bool is_active = 8;                  // Whether token is active
    int32 usage_count = 9;               // Number of times used
    google.protobuf.Timestamp last_used_at = 10;
    google.protobuf.Timestamp expires_at = 11;
    google.protobuf.Timestamp created_at = 12;
    google.protobuf.Timestamp updated_at = 13;
    
    // Token replacement tracking
    string replaces_token_id = 14;       // Token being replaced
    string replacement_reason = 15;      // Why token was replaced
    
    // Usage metadata
    map<string, string> metadata = 16;   // Custom metadata for tracking
}

// Session token (general purpose)
message SessionToken {
    string session_id = 1;               // Unique session ID
    string token = 2;                    // Session token (JWT or opaque)
    string user_id = 3;                  // Associated user
    string organization_id = 4;          // Organization context
    string device_id = 5;                // Associated device
    
    SessionType session_type = 6;        // Type of session
    SessionStatus status = 7;            // Current status
    
    // Token details
    string token_type = 8;               // bearer, jwt, opaque
    repeated string scopes = 9;          // Permission scopes
    map<string, string> claims = 10;     // Custom JWT claims
    
    // Timestamps
    google.protobuf.Timestamp issued_at = 11;
    google.protobuf.Timestamp expires_at = 12;
    google.protobuf.Timestamp last_used_at = 13;
    google.protobuf.Timestamp revoked_at = 14;
    
    // Security
    string ip_address = 15;              // IP at issuance
    string user_agent = 16;              // User agent at issuance
    string revocation_reason = 17;       // Why revoked
    
    // Metadata
    map<string, string> metadata = 18;
}

// White-label session (for branded interfaces)
message WhiteLabelSession {
    string session_id = 1;
    string token = 2;
    string user_id = 3;
    string organization_id = 4;
    string brand_id = 5;                 // White-label brand identifier
    string theme = 6;                    // UI theme (dark, light, brand)
    string logo_url = 7;                 // Brand logo URL
    string primary_color = 8;            // Brand primary color
    string secondary_color = 9;          // Brand secondary color
    
    SessionStatus status = 10;
    google.protobuf.Timestamp issued_at = 11;
    google.protobuf.Timestamp expires_at = 12;
    google.protobuf.Timestamp last_used_at = 13;
    
    map<string, string> brand_config = 14;  // Brand-specific configuration
    map<string, string> metadata = 15;
}

// Payment session (for payment processing)
message PaymentSession {
    string session_id = 1;
    string token = 2;
    string user_id = 3;
    string organization_id = 4;
    string payment_id = 5;               // Associated payment ID
    string payment_gateway = 6;          // Stripe, PayPal, etc.
    string payment_intent_id = 7;        // Gateway payment intent ID
    
    string amount = 8;                   // Payment amount
    string currency = 9;                 // Currency code
    string status = 10;                  // pending, processing, completed, failed
    
    // Payment details
    string payment_method = 11;          // card, bank, crypto
    string payment_method_id = 12;       // Tokenized payment method
    string customer_id = 13;             // Gateway customer ID
    
    // Return URLs
    string success_url = 14;             // Redirect on success
    string cancel_url = 15;              // Redirect on cancel
    string webhook_url = 16;             // Webhook for updates
    
    // Timestamps
    google.protobuf.Timestamp created_at = 17;
    google.protobuf.Timestamp expires_at = 18;
    google.protobuf.Timestamp completed_at = 19;
    
    map<string, string> metadata = 20;
}

// Push notification message
message PushNotification {
    string notification_id = 1;
    string user_id = 2;
    string device_id = 3;                // Optional - specific device
    string token_id = 4;                 // Optional - specific token
    
    // Notification content
    string title = 5;
    string body = 6;
    string image_url = 7;
    string icon = 8;
    string click_action = 9;             // Deep link or action
    
    // Data payload
    map<string, string> data = 10;
    google.protobuf.Struct custom_data = 11;
    
    // Delivery options
    NotificationPriority priority = 12;
    int32 ttl_seconds = 13;              // Time to live
    bool is_silent = 14;                 // Silent notification
    string collapse_key = 15;            // For collapsing notifications
    
    // Delivery status
    bool delivered = 16;
    string delivery_error = 17;
    google.protobuf.Timestamp sent_at = 18;
    google.protobuf.Timestamp delivered_at = 19;
}

// Device event for streaming
message DeviceEvent {
    string event_id = 1;
    string device_id = 2;
    string user_id = 3;
    string event_type = 4;               // register, unregister, token_update, session_start, etc.
    map<string, string> event_data = 5;
    google.protobuf.Timestamp event_time = 6;
}

// ==================== Request/Response Messages ====================

// Device management
message RegisterDeviceRequest {
    string user_id = 1;
    string organization_id = 2;
    string device_name = 3;
    DevicePlatform platform = 4;
    string os_version = 5;
    string app_version = 6;
    string model = 7;
    string manufacturer = 8;
    string ip_address = 9;
    map<string, string> metadata = 10;
    repeated string capabilities = 11;
}

message RegisterDeviceResponse {
    Device device = 1;
    bool registered = 2;
    string message = 3;
}

message UnregisterDeviceRequest {
    string user_id = 1;
    string organization_id = 2;
    string device_id = 3;
    string reason = 4;
}

message UnregisterDeviceResponse {
    bool unregistered = 1;
    string message = 2;
}

message GetDevicesRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_inactive = 3;
}

message GetDevicesResponse {
    repeated Device devices = 1;
    int32 total_count = 2;
    int32 active_count = 3;
}

message UpdateDeviceRequest {
    string user_id = 1;
    string organization_id = 2;
    string device_id = 3;
    optional string device_name = 4;
    optional string os_version = 5;
    optional string app_version = 6;
    optional bool is_trusted = 7;
    optional bool is_primary = 8;
    map<string, string> metadata = 9;
}

message UpdateDeviceResponse {
    Device device = 1;
    bool updated = 2;
}

message GetDeviceRequest {
    string device_id = 1;
    string user_id = 2;
    string organization_id = 3;
}

message GetDeviceResponse {
    Device device = 1;
    bool found = 2;
}

// Firebase token management
message RegisterFirebaseTokenRequest {
    string user_id = 1;
    string organization_id = 2;
    string device_id = 3;
    string fcm_token = 4;
    string apns_token = 5;               // Optional for iOS
    string push_provider = 6;            // fcm, apns, webpush
    string replaces_token_id = 7;        // Token being replaced (if any)
    map<string, string> metadata = 8;
}

message RegisterFirebaseTokenResponse {
    FirebaseToken token = 1;
    bool registered = 2;
    string message = 3;
}

message UpdateFirebaseTokenRequest {
    string user_id = 1;
    string organization_id = 2;
    string token_id = 3;
    optional string fcm_token = 4;
    optional string apns_token = 5;
    optional bool is_active = 6;
    map<string, string> metadata = 7;
}

message UpdateFirebaseTokenResponse {
    FirebaseToken token = 1;
    bool updated = 2;
}

message RemoveFirebaseTokenRequest {
    string user_id = 1;
    string organization_id = 2;
    string token_id = 3;
    string reason = 4;
}

message RemoveFirebaseTokenResponse {
    bool removed = 1;
    string message = 2;
}

message GetFirebaseTokensRequest {
    string user_id = 1;
    string organization_id = 2;
    string device_id = 3;                // Optional - filter by device
    bool include_inactive = 4;
}

message GetFirebaseTokensResponse {
    repeated FirebaseToken tokens = 1;
    int32 total_count = 2;
    int32 active_count = 3;
}

message GetUserFirebaseTokensRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_inactive = 3;
}

message GetUserFirebaseTokensResponse {
    repeated FirebaseToken tokens = 1;
    int32 total_count = 2;
}

// Session token management
message CreateSessionRequest {
    string user_id = 1;
    string organization_id = 2;
    string device_id = 3;
    SessionType session_type = 4;
    string ip_address = 5;
    string user_agent = 6;
    repeated string scopes = 7;
    map<string, string> claims = 8;
    int32 expiry_minutes = 9;            // Optional custom expiry
    map<string, string> metadata = 10;
}

message CreateSessionResponse {
    SessionToken session = 1;
    bool created = 2;
    string token = 3;                    // The actual session token
    string message = 4;
}

message GetSessionRequest {
    string session_id = 1;
    string token = 2;                    // Alternative lookup by token
    string user_id = 3;
    string organization_id = 4;
}

message GetSessionResponse {
    SessionToken session = 1;
    bool found = 2;
    bool is_valid = 3;
}

message ValidateSessionRequest {
    string token = 1;
    string user_id = 2;                  // Optional - validate specific user
    string organization_id = 3;          // Optional - validate specific org
    repeated string required_scopes = 4; // Optional - check scopes
}

message ValidateSessionResponse {
    bool valid = 1;
    SessionToken session = 2;
    string error_message = 3;
    bool expired = 4;
    bool revoked = 5;
}

message RevokeSessionRequest {
    string session_id = 1;
    string user_id = 2;
    string organization_id = 3;
    string reason = 4;
}

message RevokeSessionResponse {
    bool revoked = 1;
    string message = 2;
}

message RevokeAllSessionsRequest {
    string user_id = 1;
    string organization_id = 2;
    string exclude_session_id = 3;       // Keep current session
    string reason = 4;
}

message RevokeAllSessionsResponse {
    int32 revoked_count = 1;
    string message = 2;
}

message ExtendSessionRequest {
    string session_id = 1;
    string user_id = 2;
    string organization_id = 3;
    int32 extend_minutes = 4;
}

message ExtendSessionResponse {
    SessionToken session = 1;
    bool extended = 2;
    google.protobuf.Timestamp new_expiry = 3;
}

message ListUserSessionsRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_expired = 3;
    int32 limit = 4;
    int32 offset = 5;
}

message ListUserSessionsResponse {
    repeated SessionToken sessions = 1;
    int32 total_count = 2;
    int32 active_count = 3;
}

// Push notification delivery
message SendPushNotificationRequest {
    string user_id = 1;
    string organization_id = 2;
    string title = 3;
    string body = 4;
    string image_url = 5;
    string click_action = 6;
    map<string, string> data = 7;
    google.protobuf.Struct custom_data = 8;
    NotificationPriority priority = 9;
    int32 ttl_seconds = 10;
    bool is_silent = 11;
    string device_id = 12;               // Optional - specific device
    string token_id = 13;                // Optional - specific token
}

message SendPushNotificationResponse {
    string notification_id = 1;
    bool sent = 2;
    int32 delivery_count = 3;
    repeated string failed_tokens = 4;
    string message = 5;
}

message SendBulkPushNotificationRequest {
    repeated string user_ids = 1;
    string organization_id = 2;
    string title = 3;
    string body = 4;
    string image_url = 5;
    string click_action = 6;
    map<string, string> data = 7;
    NotificationPriority priority = 8;
    int32 ttl_seconds = 9;
}

message SendBulkPushNotificationResponse {
    string batch_id = 1;
    int32 total_recipients = 2;
    int32 successful_deliveries = 3;
    int32 failed_deliveries = 4;
    string message = 5;
}

message SendTopicNotificationRequest {
    string topic = 1;
    string organization_id = 2;
    string title = 3;
    string body = 4;
    string image_url = 5;
    string click_action = 6;
    map<string, string> data = 7;
    NotificationPriority priority = 8;
    int32 ttl_seconds = 9;
}

message SendTopicNotificationResponse {
    string message_id = 1;
    bool sent = 2;
    string message = 3;
}

// White-label session management
message CreateWhiteLabelSessionRequest {
    string user_id = 1;
    string organization_id = 2;
    string brand_id = 3;
    string theme = 4;
    string ip_address = 5;
    string user_agent = 6;
    int32 expiry_minutes = 7;
    map<string, string> metadata = 8;
}

message CreateWhiteLabelSessionResponse {
    WhiteLabelSession session = 1;
    bool created = 2;
    string token = 3;
    string message = 4;
}

message GetWhiteLabelSessionRequest {
    string session_id = 1;
    string token = 2;
    string user_id = 3;
    string organization_id = 4;
}

message GetWhiteLabelSessionResponse {
    WhiteLabelSession session = 1;
    bool found = 2;
    bool is_valid = 3;
}

message ValidateWhiteLabelSessionRequest {
    string token = 1;
    string brand_id = 2;                 // Optional - validate specific brand
}

message ValidateWhiteLabelSessionResponse {
    bool valid = 1;
    WhiteLabelSession session = 2;
    string brand_config_json = 3;        // Brand configuration
    string error_message = 4;
}

// Payment session management
message CreatePaymentSessionRequest {
    string user_id = 1;
    string organization_id = 2;
    string payment_id = 3;
    string amount = 4;
    string currency = 5;
    string payment_gateway = 6;
    string success_url = 7;
    string cancel_url = 8;
    string webhook_url = 9;
    string payment_method = 10;
    int32 expiry_minutes = 11;
    map<string, string> metadata = 12;
}

message CreatePaymentSessionResponse {
    PaymentSession session = 1;
    bool created = 2;
    string token = 3;
    string checkout_url = 4;             // URL for payment gateway
    string message = 5;
}

message GetPaymentSessionRequest {
    string session_id = 1;
    string token = 2;
    string user_id = 3;
    string organization_id = 4;
}

message GetPaymentSessionResponse {
    PaymentSession session = 1;
    bool found = 2;
    bool is_valid = 3;
}

message UpdatePaymentSessionRequest {
    string session_id = 1;
    string user_id = 2;
    string organization_id = 3;
    optional string status = 4;
    optional string payment_intent_id = 5;
    map<string, string> metadata = 6;
}

message UpdatePaymentSessionResponse {
    PaymentSession session = 1;
    bool updated = 2;
}

message CompletePaymentSessionRequest {
    string session_id = 1;
    string user_id = 2;
    string organization_id = 3;
    string payment_intent_id = 4;
    string transaction_id = 5;
    bool success = 6;
    string failure_reason = 7;
}

message CompletePaymentSessionResponse {
    PaymentSession session = 1;
    bool completed = 2;
    string message = 3;
}

// Token cleanup
message CleanupExpiredTokensRequest {
    string organization_id = 1;          // Optional - specific org
    int32 older_than_days = 2;           // Tokens older than N days
    bool dry_run = 3;                    // Preview without deleting
}

message CleanupExpiredTokensResponse {
    int32 tokens_removed = 1;
    int32 tokens_marked_inactive = 2;
    int32 devices_affected = 3;
    repeated string removed_token_ids = 4;
    string message = 5;
}

message GetTokenStatsRequest {
    string organization_id = 1;
    google.protobuf.Timestamp from_date = 2;
    google.protobuf.Timestamp to_date = 3;
}

message GetTokenStatsResponse {
    int32 total_tokens = 1;
    int32 active_tokens = 2;
    int32 expired_tokens = 3;
    int32 tokens_by_platform = 4;
    double average_token_age_days = 5;
    int32 tokens_created_last_24h = 6;
    int32 tokens_created_last_7d = 7;
    int32 tokens_created_last_30d = 8;
    map<string, int32> platform_breakdown = 9;
    map<string, int32> usage_breakdown = 10;
}

// Analytics and monitoring
message GetDeviceAnalyticsRequest {
    string organization_id = 1;
    google.protobuf.Timestamp from_date = 2;
    google.protobuf.Timestamp to_date = 3;
    string group_by = 4;                 // day, week, month, platform
}

message GetDeviceAnalyticsResponse {
    int32 total_devices = 1;
    int32 active_devices = 2;
    int32 new_devices = 3;
    repeated DeviceAnalyticsEntry history = 4;
    map<string, int32> platform_breakdown = 5;
    map<string, int32> os_version_breakdown = 6;
    map<string, int32> app_version_breakdown = 7;
}

message DeviceAnalyticsEntry {
    google.protobuf.Timestamp period = 1;
    int32 total_devices = 2;
    int32 active_devices = 3;
    int32 new_devices = 4;
    int32 devices_removed = 5;
}

message GetSessionAnalyticsRequest {
    string organization_id = 1;
    google.protobuf.Timestamp from_date = 2;
    google.protobuf.Timestamp to_date = 3;
    SessionType session_type = 4;
    string group_by = 5;
}

message GetSessionAnalyticsResponse {
    int32 total_sessions = 1;
    int32 active_sessions = 2;
    int32 expired_sessions = 3;
    int32 revoked_sessions = 4;
    double average_session_duration_minutes = 5;
    repeated SessionAnalyticsEntry history = 6;
}

message SessionAnalyticsEntry {
    google.protobuf.Timestamp period = 1;
    int32 sessions_created = 2;
    int32 sessions_active = 3;
    int32 sessions_expired = 4;
    int32 sessions_revoked = 5;
}

message StreamDeviceEventsRequest {
    string user_id = 1;
    string organization_id = 2;
    string device_id = 3;                // Optional - specific device
    repeated string event_types = 4;     // Filter by event type
}

// ==================== Database Schema Reference ====================

/*
-- Devices table
CREATE TABLE devices (
    device_id UUID PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    organization_id VARCHAR(100),
    device_name VARCHAR(255),
    platform VARCHAR(20) NOT NULL,
    os_version VARCHAR(50),
    app_version VARCHAR(50),
    model VARCHAR(100),
    manufacturer VARCHAR(100),
    ip_address INET,
    country_code VARCHAR(2),
    timezone VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    is_trusted BOOLEAN DEFAULT false,
    is_primary BOOLEAN DEFAULT false,
    first_seen_at TIMESTAMP,
    last_seen_at TIMESTAMP,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    capabilities TEXT[],
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_last_seen (last_seen_at)
);

-- Firebase tokens table
CREATE TABLE firebase_tokens (
    token_id UUID PRIMARY KEY,
    device_id UUID REFERENCES devices(device_id),
    user_id VARCHAR(100) NOT NULL,
    organization_id VARCHAR(100),
    fcm_token TEXT UNIQUE NOT NULL,
    apns_token TEXT,
    push_provider VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    usage_count INT DEFAULT 0,
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    replaces_token_id UUID,
    replacement_reason VARCHAR(255),
    metadata JSONB,
    INDEX idx_user_id (user_id),
    INDEX idx_fcm_token (fcm_token),
    INDEX idx_expires_at (expires_at),
    INDEX idx_is_active (is_active)
);

-- Session tokens table
CREATE TABLE session_tokens (
    session_id UUID PRIMARY KEY,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    organization_id VARCHAR(100),
    device_id UUID REFERENCES devices(device_id),
    session_type VARCHAR(30) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    token_type VARCHAR(20),
    scopes TEXT[],
    claims JSONB,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    revoked_at TIMESTAMP,
    ip_address INET,
    user_agent TEXT,
    revocation_reason VARCHAR(255),
    metadata JSONB,
    INDEX idx_user_id (user_id),
    INDEX idx_token_hash (token_hash),
    INDEX idx_expires_at (expires_at),
    INDEX idx_status (status)
);

-- White-label sessions table
CREATE TABLE white_label_sessions (
    session_id UUID PRIMARY KEY,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(100),
    organization_id VARCHAR(100),
    brand_id VARCHAR(100) NOT NULL,
    theme VARCHAR(50),
    logo_url TEXT,
    primary_color VARCHAR(7),
    secondary_color VARCHAR(7),
    status VARCHAR(20) DEFAULT 'active',
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    brand_config JSONB,
    metadata JSONB,
    INDEX idx_token_hash (token_hash),
    INDEX idx_brand_id (brand_id),
    INDEX idx_expires_at (expires_at)
);

-- Payment sessions table
CREATE TABLE payment_sessions (
    session_id UUID PRIMARY KEY,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    organization_id VARCHAR(100),
    payment_id VARCHAR(100),
    payment_gateway VARCHAR(50),
    payment_intent_id VARCHAR(255),
    amount DECIMAL(20,8),
    currency VARCHAR(3),
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(50),
    payment_method_id VARCHAR(255),
    customer_id VARCHAR(255),
    success_url TEXT,
    cancel_url TEXT,
    webhook_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    completed_at TIMESTAMP,
    metadata JSONB,
    INDEX idx_user_id (user_id),
    INDEX idx_token_hash (token_hash),
    INDEX idx_status (status),
    INDEX idx_expires_at
    INDEX idx_expires_at (expires_at)
    );

    -- Push notifications table
    CREATE TABLE push_notifications (
    notification_id UUID PRIMARY KEY,
    user_id VARCHAR(100),
    device_id UUID,
    token_id UUID,
    title VARCHAR(255),
    body TEXT,
    image_url TEXT,
    click_action TEXT,
    priority VARCHAR(20),
    ttl_seconds INT,
    is_silent BOOLEAN DEFAULT false,
    delivered BOOLEAN DEFAULT false,
    delivery_error TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP,
    data JSONB,
    INDEX idx_user_id (user_id),
    INDEX idx_sent_at (sent_at)
);
*/
