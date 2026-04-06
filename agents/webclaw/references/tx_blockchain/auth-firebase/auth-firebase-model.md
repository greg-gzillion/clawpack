# Firebase Auth Model (com-fs-auth-firebase-model)

The Firebase Auth Model provides a comprehensive authentication and notification system through Firebase, supporting token validation, user session management, and push notifications.

## Overview

The Firebase Auth Model is a gRPC-based service that handles two primary functions:
- **Authentication**: Token validation, user signout, session management
- **Notifications**: Push notification delivery to Firebase-enabled devices

## Architecture
┌─────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Web, Mobile, Backend Services) │
└───────────────────┬─────────────────┬───────────────────┘
│ │
│ gRPC │ gRPC
▼ ▼
┌──────────────────┐ ┌──────────────────┐
│ AUTH_FIREBASE │ │ FIREBASE_ │
│ _SERVICE │ │ NOTIFICATION │
│ │ │ _SERVICE │
│ Port: 50075 │ │ Port: 50076 │
└────────┬─────────┘ └────────┬─────────┘
│ │
▼ ▼
┌──────────────────────────────────────────┐
│ Firebase Platform │
│ - Authentication │
│ - Cloud Messaging (FCM) │
│ - User Management │
└──────────────────────────────────────────┘

text

## Environment Variables

### Required Variables

| Variable | Description | Format | Example |
|----------|-------------|--------|---------|
| `AUTH_FIREBASE_SERVICE` | gRPC endpoint for Firebase Authentication Service | `host:port` | `auth-service:50075` |
| `FIREBASE_NOTIFICATION_SERVICE` | gRPC endpoint for Firebase Notification Service | `host:port` | `notification-service:50076` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FIREBASE_PROJECT_ID` | Firebase project identifier | - |
| `FIREBASE_CLIENT_EMAIL` | Firebase service account email | - |
| `FIREBASE_PRIVATE_KEY` | Firebase service account private key | - |
| `TOKEN_CACHE_TTL` | Token validation cache TTL (seconds) | `300` |
| `MAX_CONCURRENT_REQUESTS` | Max concurrent gRPC requests | `100` |
| `LOG_LEVEL` | Logging level (debug, info, warn, error) | `info` |

## Proto Definition

### Authentication Proto

```protobuf
syntax = "proto3";

package auth.firebase.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Firebase Authentication Service
service FirebaseAuthService {
    // Validate Firebase token
    rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
    
    // Signout user from current session
    rpc Signout(SignoutRequest) returns (SignoutResponse);
    
    // Signout user by email (admin function)
    rpc SignoutUserByEmail(SignoutUserByEmailRequest) returns (SignoutResponse);
    
    // Get user information
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    
    // List all users (paginated)
    rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
    
    // Revoke all user sessions
    rpc RevokeAllSessions(RevokeAllSessionsRequest) returns (RevokeAllSessionsResponse);
    
    // Verify custom token
    rpc VerifyCustomToken(VerifyCustomTokenRequest) returns (VerifyCustomTokenResponse);
}

// Token validation request
message ValidateTokenRequest {
    string token = 1;                   // Firebase ID token
    bool check_revoked = 2;             // Check if token is revoked
    string organization_id = 3;         // Organization context
}

// Token validation response
message ValidateTokenResponse {
    bool valid = 1;                     // Token validity
    UserInfo user = 2;                  // User information if valid
    string error_message = 3;           // Error message if invalid
    TokenMetadata metadata = 4;         // Token metadata
}

// User information
message UserInfo {
    string uid = 1;                     // Firebase user ID
    string email = 2;                   // User email
    string name = 3;                    // Display name
    string phone_number = 4;            // Phone number
    string photo_url = 5;               // Profile photo URL
    bool email_verified = 6;            // Email verification status
    bool phone_verified = 7;            // Phone verification status
    map<string, string> custom_claims = 8; // Custom claims
    repeated string roles = 9;          // User roles
    google.protobuf.Timestamp created_at = 10;
    google.protobuf.Timestamp last_login = 11;
    string organization_id = 12;        // Associated organization
}

// Token metadata
message TokenMetadata {
    string issuer = 1;                  // Token issuer
    string audience = 2;                // Token audience
    google.protobuf.Timestamp issued_at = 3;
    google.protobuf.Timestamp expires_at = 4;
    string token_id = 5;                // Unique token identifier
}

// Signout request
message SignoutRequest {
    string token = 1;                   // Current session token
    bool global_signout = 2;            // Signout from all devices
}

// Signout response
message SignoutResponse {
    bool success = 1;
    string message = 2;
}

// Signout by email request
message SignoutUserByEmailRequest {
    string email = 1;                   // User email address
    string organization_id = 2;         // Organization context
    bool all_devices = 3;               // Signout from all devices
}

// Get user request
message GetUserRequest {
    string uid = 1;                     // Firebase user ID
    string email = 2;                   // User email (alternative)
    string organization_id = 3;
}

// Get user response
message GetUserResponse {
    UserInfo user = 1;
    bool found = 2;
}

// List users request
message ListUsersRequest {
    int32 limit = 1;                    // Max users to return (max 1000)
    string page_token = 2;              // Pagination token
    string organization_id = 3;
    string role_filter = 4;             // Filter by role
}

// List users response
message ListUsersResponse {
    repeated UserInfo users = 1;
    string next_page_token = 2;
    int32 total_count = 3;
}

// Revoke all sessions request
message RevokeAllSessionsRequest {
    string uid = 1;                     // User ID
    string organization_id = 2;
    string reason = 3;                  // Reason for revocation
}

// Revoke all sessions response
message RevokeAllSessionsResponse {
    bool success = 1;
    int32 sessions_revoked = 2;
}

// Verify custom token request
message VerifyCustomTokenRequest {
    string custom_token = 1;            // Custom Firebase token
    string organization_id = 2;
}

// Verify custom token response
message VerifyCustomTokenResponse {
    bool valid = 1;
    UserInfo user = 2;
    string firebase_token = 3;          // New Firebase ID token
}
Notification Proto
protobuf
syntax = "proto3";

package notification.firebase.v1;

import "google/protobuf/struct.proto";

// Firebase Notification Service
service FirebaseNotificationService {
    // Send notification to a single device
    rpc Send(SendNotificationRequest) returns (SendNotificationResponse);
    
    // Send notification to multiple devices
    rpc SendMulticast(SendMulticastRequest) returns (SendMulticastResponse);
    
    // Send notification to a topic
    rpc SendToTopic(SendToTopicRequest) returns (SendToTopicResponse);
    
    // Subscribe device to topic
    rpc SubscribeToTopic(SubscribeTopicRequest) returns (SubscribeTopicResponse);
    
    // Unsubscribe device from topic
    rpc UnsubscribeFromTopic(UnsubscribeTopicRequest) returns (UnsubscribeTopicResponse);
    
    // Get device info
    rpc GetDeviceInfo(GetDeviceInfoRequest) returns (GetDeviceInfoResponse);
    
    // Register device token
    rpc RegisterDevice(RegisterDeviceRequest) returns (RegisterDeviceResponse);
    
    // Unregister device token
    rpc UnregisterDevice(UnregisterDeviceRequest) returns (UnregisterDeviceResponse);
}

// Notification message
message Notification {
    string title = 1;                   // Notification title
    string body = 2;                    // Notification body
    string image_url = 3;               // Image URL
    string sound = 4;                   // Sound to play
    string badge = 5;                   // Badge count
    string click_action = 6;            // Action on click
    string channel_id = 7;              // Android channel ID
    string priority = 8;                // high, normal
    int32 ttl_seconds = 9;              // Time to live in seconds
}

// Data payload (custom key-value pairs)
message DataPayload {
    map<string, string> data = 1;
}

// APNS specific configuration
message APNSConfig {
    string sound = 1;
    string badge = 2;
    string category = 3;
    bool content_available = 4;
    bool mutable_content = 5;
}

// Android specific configuration
message AndroidConfig {
    string channel_id = 1;
    string priority = 2;                // high, normal
    int32 ttl_seconds = 3;
    string collapse_key = 4;
}

// Send notification request
message SendNotificationRequest {
    string device_token = 1;            // FCM device token
    Notification notification = 2;      // Notification payload
    DataPayload data = 3;               // Custom data payload
    string organization_id = 4;         // Organization context
    APNSConfig apns_config = 5;         // iOS specific config
    AndroidConfig android_config = 6;   // Android specific config
}

// Send notification response
message SendNotificationResponse {
    bool success = 1;
    string message_id = 2;              // FCM message ID
    string error = 3;                   // Error message if failed
}

// Send multicast request
message SendMulticastRequest {
    repeated string device_tokens = 1;  // Max 500 tokens
    Notification notification = 2;
    DataPayload data = 3;
    string organization_id = 4;
    APNSConfig apns_config = 5;
    AndroidConfig android_config = 6;
}

// Send multicast response
message SendMulticastResponse {
    int32 success_count = 1;
    int32 failure_count = 2;
    repeated DeviceResult results = 3;
}

// Individual device result
message DeviceResult {
    string device_token = 1;
    bool success = 2;
    string message_id = 3;
    string error = 4;
}

// Send to topic request
message SendToTopicRequest {
    string topic = 1;                   // Topic name (e.g., "news", "alerts")
    Notification notification = 2;
    DataPayload data = 3;
    string organization_id = 4;
    APNSConfig apns_config = 5;
    AndroidConfig android_config = 6;
}

// Send to topic response
message SendToTopicResponse {
    bool success = 1;
    string message_id = 2;
    int32 estimated_delivery_count = 3;
}

// Subscribe to topic request
message SubscribeTopicRequest {
    string device_token = 1;
    string topic = 2;
    string organization_id = 3;
}

// Subscribe to topic response
message SubscribeTopicResponse {
    bool success = 1;
    string message = 2;
}

// Unsubscribe from topic request
message UnsubscribeTopicRequest {
    string device_token = 1;
    string topic = 2;
    string organization_id = 3;
}

// Unsubscribe from topic response
message UnsubscribeTopicResponse {
    bool success = 1;
    string message = 2;
}

// Get device info request
message GetDeviceInfoRequest {
    string device_token = 1;
    string organization_id = 2;
}

// Device information
message DeviceInfo {
    string device_token = 1;
    string platform = 2;                // ios, android, web
    string app_version = 3;
    string device_model = 4;
    string os_version = 5;
    google.protobuf.Timestamp registered_at = 6;
    google.protobuf.Timestamp last_active = 7;
    repeated string topics = 8;
    bool active = 9;
}

// Get device info response
message GetDeviceInfoResponse {
    DeviceInfo device = 1;
    bool found = 2;
}

// Register device request
message RegisterDeviceRequest {
    string device_token = 1;
    string platform = 2;
    string app_version = 3;
    string device_model = 4;
    string os_version = 5;
    string user_id = 6;
    string organization_id = 7;
}

// Register device response
message RegisterDeviceResponse {
    bool success = 1;
    string message = 2;
}

// Unregister device request
message UnregisterDeviceRequest {
    string device_token = 1;
    string organization_id = 2;
}

// Unregister device response
message UnregisterDeviceResponse {
    bool success = 1;
    string message = 2;
}
Client Implementation
Go Client
go
package main

import (
    "context"
    "fmt"
    "log"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    
    authpb "github.com/sologenic/auth-firebase-model/proto/auth"
    notifpb "github.com/sologenic/auth-firebase-model/proto/notification"
)

type FirebaseAuthClient struct {
    client authpb.FirebaseAuthServiceClient
    conn   *grpc.ClientConn
}

type FirebaseNotificationClient struct {
    client notifpb.FirebaseNotificationServiceClient
    conn   *grpc.ClientConn
}

// Create new auth client
func NewFirebaseAuthClient(addr string) (*FirebaseAuthClient, error) {
    conn, err := grpc.Dial(addr, 
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to auth service: %w", err)
    }
    
    return &FirebaseAuthClient{
        client: authpb.NewFirebaseAuthServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *FirebaseAuthClient) Close() error {
    return c.conn.Close()
}

// Validate Firebase token
func (c *FirebaseAuthClient) ValidateToken(ctx context.Context, token, orgID string) (*authpb.ValidateTokenResponse, error) {
    req := &authpb.ValidateTokenRequest{
        Token:          token,
        CheckRevoked:   true,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.ValidateToken(ctx, req)
    if err != nil {
        return nil, fmt.Errorf("token validation failed: %w", err)
    }
    
    return resp, nil
}

// Signout current session
func (c *FirebaseAuthClient) Signout(ctx context.Context, token string, globalSignout bool) error {
    req := &authpb.SignoutRequest{
        Token:         token,
        GlobalSignout: globalSignout,
    }
    
    resp, err := c.client.Signout(ctx, req)
    if err != nil {
        return fmt.Errorf("signout failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("signout failed: %s", resp.Message)
    }
    
    return nil
}

// Signout user by email (admin)
func (c *FirebaseAuthClient) SignoutUserByEmail(ctx context.Context, email, orgID string, allDevices bool) error {
    req := &authpb.SignoutUserByEmailRequest{
        Email:          email,
        OrganizationId: orgID,
        AllDevices:     allDevices,
    }
    
    resp, err := c.client.SignoutUserByEmail(ctx, req)
    if err != nil {
        return fmt.Errorf("signout by email failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("signout failed: %s", resp.Message)
    }
    
    return nil
}

// Get user information
func (c *FirebaseAuthClient) GetUser(ctx context.Context, uid, email, orgID string) (*authpb.UserInfo, error) {
    req := &authpb.GetUserRequest{
        OrganizationId: orgID,
    }
    
    if uid != "" {
        req.Uid = uid
    } else if email != "" {
        req.Email = email
    } else {
        return nil, fmt.Errorf("either uid or email must be provided")
    }
    
    resp, err := c.client.GetUser(ctx, req)
    if err != nil {
        return nil, fmt.Errorf("get user failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.User, nil
}

// Revoke all user sessions
func (c *FirebaseAuthClient) RevokeAllSessions(ctx context.Context, uid, orgID, reason string) (int32, error) {
    req := &authpb.RevokeAllSessionsRequest{
        Uid:            uid,
        OrganizationId: orgID,
        Reason:         reason,
    }
    
    resp, err := c.client.RevokeAllSessions(ctx, req)
    if err != nil {
        return 0, fmt.Errorf("revoke sessions failed: %w", err)
    }
    
    return resp.SessionsRevoked, nil
}

// Create notification client
func NewFirebaseNotificationClient(addr string) (*FirebaseNotificationClient, error) {
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to notification service: %w", err)
    }
    
    return &FirebaseNotificationClient{
        client: notifpb.NewFirebaseNotificationServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *FirebaseNotificationClient) Close() error {
    return c.conn.Close()
}

// Send notification to single device
func (c *FirebaseNotificationClient) Send(ctx context.Context, deviceToken string, title, body string, data map[string]string, orgID string) error {
    req := &notifpb.SendNotificationRequest{
        DeviceToken: deviceToken,
        Notification: &notifpb.Notification{
            Title: title,
            Body:  body,
        },
        Data: &notifpb.DataPayload{
            Data: data,
        },
        OrganizationId: orgID,
    }
    
    resp, err := c.client.Send(ctx, req)
    if err != nil {
        return fmt.Errorf("send notification failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("notification failed: %s", resp.Error)
    }
    
    log.Printf("Notification sent successfully. Message ID: %s", resp.MessageId)
    return nil
}

// Send notification to multiple devices
func (c *FirebaseNotificationClient) SendMulticast(ctx context.Context, deviceTokens []string, title, body string, data map[string]string, orgID string) (*notifpb.SendMulticastResponse, error) {
    if len(deviceTokens) > 500 {
        return nil, fmt.Errorf("maximum 500 device tokens allowed, got %d", len(deviceTokens))
    }
    
    req := &notifpb.SendMulticastRequest{
        DeviceTokens: deviceTokens,
        Notification: &notifpb.Notification{
            Title: title,
            Body:  body,
        },
        Data: &notifpb.DataPayload{
            Data: data,
        },
        OrganizationId: orgID,
    }
    
    resp, err := c.client.SendMulticast(ctx, req)
    if err != nil {
        return nil, fmt.Errorf("multicast notification failed: %w", err)
    }
    
    return resp, nil
}

// Send notification to a topic
func (c *FirebaseNotificationClient) SendToTopic(ctx context.Context, topic, title, body string, data map[string]string, orgID string) error {
    req := &notifpb.SendToTopicRequest{
        Topic: topic,
        Notification: &notifpb.Notification{
            Title: title,
            Body:  body,
        },
        Data: &notifpb.DataPayload{
            Data: data,
        },
        OrganizationId: orgID,
    }
    
    resp, err := c.client.SendToTopic(ctx, req)
    if err != nil {
        return fmt.Errorf("send to topic failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("topic notification failed")
    }
    
    return nil
}

// Subscribe device to topic
func (c *FirebaseNotificationClient) SubscribeToTopic(ctx context.Context, deviceToken, topic, orgID string) error {
    req := &notifpb.SubscribeTopicRequest{
        DeviceToken:    deviceToken,
        Topic:          topic,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.SubscribeToTopic(ctx, req)
    if err != nil {
        return fmt.Errorf("subscribe to topic failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("subscription failed: %s", resp.Message)
    }
    
    return nil
}

// Unsubscribe device from topic
func (c *FirebaseNotificationClient) UnsubscribeFromTopic(ctx context.Context, deviceToken, topic, orgID string) error {
    req := &notifpb.UnsubscribeTopicRequest{
        DeviceToken:    deviceToken,
        Topic:          topic,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.UnsubscribeFromTopic(ctx, req)
    if err != nil {
        return fmt.Errorf("unsubscribe from topic failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("unsubscription failed: %s", resp.Message)
    }
    
    return nil
}

// Register device token
func (c *FirebaseNotificationClient) RegisterDevice(ctx context.Context, deviceToken, platform, appVersion, deviceModel, osVersion, userID, orgID string) error {
    req := &notifpb.RegisterDeviceRequest{
        DeviceToken:    deviceToken,
        Platform:       platform,
        AppVersion:     appVersion,
        DeviceModel:    deviceModel,
        OsVersion:      osVersion,
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.RegisterDevice(ctx, req)
    if err != nil {
        return fmt.Errorf("register device failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("registration failed: %s", resp.Message)
    }
    
    return nil
}

// Example usage
func main() {
    // Initialize auth client
    authClient, err := NewFirebaseAuthClient("auth-service:50075")
    if err != nil {
        log.Fatal(err)
    }
    defer authClient.Close()
    
    // Initialize notification client
    notifClient, err := NewFirebaseNotificationClient("notification-service:50076")
    if err != nil {
        log.Fatal(err)
    }
    defer notifClient.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    
    // Validate user token
    firebaseToken := "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
    validation, err := authClient.ValidateToken(ctx, firebaseToken, orgID)
    if err != nil {
        log.Printf("Token validation error: %v", err)
    } else if validation.Valid {
        log.Printf("User %s (%s) authenticated", 
            validation.User.Name, 
            validation.User.Email)
        
        // Send welcome notification
        err = notifClient.Send(ctx, "device_token_123", 
            "Welcome!", 
            fmt.Sprintf("Welcome %s to our platform!", validation.User.Name),
            map[string]string{
                "user_id": validation.User.Uid,
                "type":    "welcome",
            },
            orgID)
        if err != nil {
            log.Printf("Failed to send welcome notification: %v", err)
        }
    } else {
        log.Printf("Invalid token: %s", validation.ErrorMessage)
    }
    
    // Send notification to topic
    err = notifClient.SendToTopic(ctx, "announcements",
        "New Feature Available",
        "Check out our latest features!",
        map[string]string{
            "feature": "new_trading_view",
            "version": "2.0",
        },
        orgID)
    if err != nil {
        log.Printf("Failed to send topic notification: %v", err)
    }
}
TypeScript Client
typescript
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import * as path from 'path';

// Load proto definitions
const PROTO_PATH = path.join(__dirname, '../proto');

interface UserInfo {
    uid: string;
    email: string;
    name: string;
    phoneNumber?: string;
    photoUrl?: string;
    emailVerified: boolean;
    customClaims: Record<string, string>;
    roles: string[];
    organizationId: string;
}

interface Notification {
    title: string;
    body: string;
    imageUrl?: string;
    sound?: string;
    clickAction?: string;
    priority?: 'high' | 'normal';
}

class FirebaseAuthClient {
    private client: any;
    
    constructor(serviceUrl: string) {
        const packageDefinition = protoLoader.loadSync(
            `${PROTO_PATH}/auth.proto`,
            {
                keepCase: true,
                longs: String,
                enums: String,
                defaults: true,
                oneofs: true
            }
        );
        const proto = grpc.loadPackageDefinition(packageDefinition);
        this.client = new proto.auth.firebase.v1.FirebaseAuthService(
            serviceUrl,
            grpc.credentials.createInsecure()
        );
    }
    
    async validateToken(token: string, organizationId: string): Promise<{ valid: boolean; user?: UserInfo; error?: string }> {
        return new Promise((resolve, reject) => {
            this.client.ValidateToken(
                { token, check_revoked: true, organization_id: organizationId },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        valid: response.valid,
                        user: response.user,
                        error: response.error_message
                    });
                }
            );
        });
    }
    
    async signout(token: string, globalSignout: boolean = false): Promise<void> {
        return new Promise((resolve, reject) => {
            this.client.Signout(
                { token, global_signout: globalSignout },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.success) {
                        reject(new Error(response.message));
                        return;
                    }
                    
                    resolve();
                }
            );
        });
    }
    
    async signoutUserByEmail(email: string, organizationId: string, allDevices: boolean = false): Promise<void> {
        return new Promise((resolve, reject) => {
            this.client.SignoutUserByEmail(
                { email, organization_id: organizationId, all_devices: allDevices },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.success) {
                        reject(new Error(response.message));
                        return;
                    }
                    
                    resolve();
                }
            );
        });
    }
    
    async getUser(uid: string, organizationId: string): Promise<UserInfo | null> {
        return new Promise((resolve, reject) => {
            this.client.GetUser(
                { uid, organization_id: organizationId },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve(response.found ? response.user : null);
                }
            );
        });
    }
    
    async revokeAllSessions(uid: string, organizationId: string, reason: string): Promise<number> {
        return new Promise((resolve, reject) => {
            this.client.RevokeAllSessions(
                { uid, organization_id: organizationId, reason },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve(response.sessions_revoked);
                }
            );
        });
    }
}

class FirebaseNotificationClient {
    private client: any;
    
    constructor(serviceUrl: string) {
        const packageDefinition = protoLoader.loadSync(
            `${PROTO_PATH}/notification.proto`,
            {
                keepCase: true,
                longs: String,
                enums: String,
                defaults: true,
                oneofs: true
            }
        );
        const proto = grpc.loadPackageDefinition(packageDefinition);
        this.client = new proto.notification.firebase.v1.FirebaseNotificationService(
            serviceUrl,
            grpc.credentials.createInsecure()
        );
    }
    
    async sendNotification(
        deviceToken: string,
        notification: Notification,
        data: Record<string, string>,
        organizationId: string
    ): Promise<string> {
        return new Promise((resolve, reject) => {
            this.client.Send(
                {
                    device_token: deviceToken,
                    notification,
                    data: { data },
                    organization_id: organizationId
                },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.success) {
                        reject(new Error(response.error));
                        return;
                    }
                    
                    resolve(response.message_id);
                }
            );
        });
    }
    
    async sendMulticast(
        deviceTokens: string[],
        notification: Notification,
        data: Record<string, string>,
        organizationId: string
    ): Promise<{ successCount: number; failureCount: number; results: any[] }> {
        if (deviceTokens.length > 500) {
            throw new Error(`Maximum 500 device tokens allowed, got ${deviceTokens.length}`);
        }
        
        return new Promise((resolve, reject) => {
            this.client.SendMulticast(
                {
                    device_tokens: deviceTokens,
                    notification,
                    data: { data },
                    organization_id: organizationId
                },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        successCount: response.success_count,
                        failureCount: response.failure_count,
                        results: response.results
                    });
                }
            );
        });
    }
    
    async sendToTopic(
        topic: string,
        notification: Notification,
        data: Record<string, string>,
        organizationId: string
    ): Promise<string> {
        return new Promise((resolve, reject) => {
            this.client.SendToTopic(
                {
                    topic,
                    notification,
                    data: { data },
                    organization_id: organizationId
                },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.success) {
                        reject(new Error('Failed to send to topic'));
                        return;
                    }
                    
                    resolve(response.message_id);
                }
            );
        });
    }
    
    async subscribeToTopic(deviceToken: string, topic: string, organizationId: string): Promise<void> {
        return new Promise((resolve, reject) => {
            this.client.SubscribeToTopic(
                { device_token: deviceToken, topic, organization_id: organizationId },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.success) {
                        reject(new Error(response.message));
                        return;
                    }
                    
                    resolve();
                }
            );
        });
    }
    
    async registerDevice(
        deviceToken: string,
        platform: string,
        appVersion: string,
        userId: string,
        organizationId: string
    ): Promise<void> {
        return new Promise((resolve, reject) => {
            this.client.RegisterDevice(
                {
                    device_token: deviceToken,
                    platform,
                    app_version: appVersion,
                    user_id: userId,
                    organization_id: organizationId
                },
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.success) {
                        reject(new Error(response.message));
                        return;
                    }
                    
                    resolve();
                }
            );
        });
    }
}

// React hook for authentication
import { useEffect, useState } from 'react';

function useFirebaseAuth(organizationId: string) {
    const [user, setUser] = useState<UserInfo | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    useEffect(() => {
        const authClient = new FirebaseAuthClient(process.env.REACT_APP_AUTH_SERVICE_URL!);
        
        const token = localStorage.getItem('firebase_token');
        if (!token) {
            setLoading(false);
            return;
        }
        
        authClient.validateToken(token, organizationId)
            .then(result => {
                if (result.valid && result.user) {
                    setUser(result.user);
                } else {
                    localStorage.removeItem('firebase_token');
                }
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, [organizationId]);
    
    const signout = async () => {
        const authClient = new FirebaseAuthClient(process.env.REACT_APP_AUTH_SERVICE_URL!);
        const token = localStorage.getItem('firebase_token');
        if (token) {
            await authClient.signout(token, false);
            localStorage.removeItem('firebase_token');
            setUser(null);
        }
    };
    
    return { user, loading, error, signout };
}

// React hook for notifications
function usePushNotifications(userId: string, organizationId: string) {
    const [deviceToken, setDeviceToken] = useState<string | null>(null);
    
    useEffect(() => {
        // Initialize Firebase Cloud Messaging
        const initializeFCM = async () => {
            try {
                // Request permission
                const permission = await Notification.requestPermission();
                if (permission !== 'granted') {
                    console.log('Notification permission denied');
                    return;
                }
                
                // Get FCM token (implementation depends on your FCM setup)
                // const token = await getToken({ vapidKey: 'YOUR_VAPID_KEY' });
                const token = 'fcm_device_token_example';
                
                setDeviceToken(token);
                
                // Register device with backend
                const notifClient = new FirebaseNotificationClient(
                    process.env.REACT_APP_NOTIFICATION_SERVICE_URL!
                );
                await notifClient.registerDevice(
                    token,
                    'web',
                    process.env.REACT_APP_VERSION!,
                    userId,
                    organizationId
                );
            } catch (error) {
                console.error('FCM initialization failed:', error);
            }
        };
        
        initializeFCM();
    }, [userId, organizationId]);
    
    const subscribeToTopic = async (topic: string) => {
        if (!deviceToken) return;
        
        const notifClient = new FirebaseNotificationClient(
            process.env.REACT_APP_NOTIFICATION_SERVICE_URL!
        );
        await notifClient.subscribeToTopic(deviceToken, topic, organizationId);
    };
    
    return { deviceToken, subscribeToTopic };
}

export { 
    FirebaseAuthClient, 
    FirebaseNotificationClient, 
    useFirebaseAuth, 
    usePushNotifications 
};
Docker Compose Example
yaml
version: '3.8'

services:
  # Firebase Authentication Service
  auth-firebase-service:
    image: sologenic/auth-firebase-service:latest
    environment:
      - AUTH_FIREBASE_SERVICE=:50075
      - FIREBASE_PROJECT_ID=${FIREBASE_PROJECT_ID}
      - FIREBASE_CLIENT_EMAIL=${FIREBASE_CLIENT_EMAIL}
      - FIREBASE_PRIVATE_KEY=${FIREBASE_PRIVATE_KEY}
      - TOKEN_CACHE_TTL=300
      - LOG_LEVEL=info
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50075:50075"
    networks:
      - internal
    depends_on:
      - redis
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50075"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Firebase Notification Service
  firebase-notification-service:
    image: sologenic/firebase-notification-service:latest
    environment:
      - FIREBASE_NOTIFICATION_SERVICE=:50076
      - FIREBASE_PROJECT_ID=${FIREBASE_PROJECT_ID}
      - FIREBASE_CLIENT_EMAIL=${FIREBASE_CLIENT_EMAIL}
      - FIREBASE_PRIVATE_KEY=${FIREBASE_PRIVATE_KEY}
      - MAX_CONCURRENT_REQUESTS=100
      - LOG_LEVEL=info
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50076:50076"
    networks:
      - internal
    depends_on:
      -redis
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50076"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Redis for token caching and session management
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - internal
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Optional: Admin UI for managing users
  firebase-admin-ui:
    image: sologenic/firebase-admin-ui:latest
    environment:
      - AUTH_SERVICE_ENDPOINT=auth-firebase-service:50075
      - PORT=8080
    ports:
      - "8080:8080"
    networks:
      - internal
    depends_on:
      - auth-firebase-service

networks:
  internal:
    driver: bridge

volumes:
  redis_data:
Environment Setup (.env file)
bash
# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=firebase-adminsdk@your-project.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYourPrivateKeyHere\n-----END PRIVATE KEY-----\n"

# Service Endpoints
AUTH_FIREBASE_SERVICE=auth-firebase-service:50075
FIREBASE_NOTIFICATION_SERVICE=firebase-notification-service:50076

# Service Configuration
TOKEN_CACHE_TTL=300
MAX_CONCURRENT_REQUESTS=100
LOG_LEVEL=info

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
Firebase Service Account Setup
Create Service Account
Go to Firebase Console

Select your project

Go to Project Settings > Service Accounts

Click "Generate New Private Key"

Save the JSON file

Service Account JSON Structure
json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk@your-project.iam.gserviceaccount.com",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
Convert to Environment Variables
bash
# Extract values from JSON
FIREBASE_PROJECT_ID=$(jq -r '.project_id' service-account.json)
FIREBASE_CLIENT_EMAIL=$(jq -r '.client_email' service-account.json)
FIREBASE_PRIVATE_KEY=$(jq -r '.private_key' service-account.json | sed 's/"/\\"/g')
Error Handling
Common Error Codes
Code	Description	Handling
UNAUTHENTICATED	Invalid or expired token	Refresh token or redirect to login
PERMISSION_DENIED	Insufficient permissions	Check user roles and claims
NOT_FOUND	User or device not found	Verify identifiers
INVALID_ARGUMENT	Malformed request	Validate input parameters
RESOURCE_EXHAUSTED	Rate limit exceeded	Implement exponential backoff
UNAVAILABLE	Service temporarily unavailable	Retry with backoff
Token Validation Middleware
go
// Go middleware for token validation
func AuthMiddleware(authClient *FirebaseAuthClient, orgID string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            // Extract token from Authorization header
            authHeader := r.Header.Get("Authorization")
            if authHeader == "" {
                http.Error(w, "Missing authorization header", http.StatusUnauthorized)
                return
            }
            
            // Extract Bearer token
            parts := strings.Split(authHeader, " ")
            if len(parts) != 2 || parts[0] != "Bearer" {
                http.Error(w, "Invalid authorization format", http.StatusUnauthorized)
                return
            }
            
            token := parts[1]
            
            // Validate token
            ctx := context.Background()
            validation, err := authClient.ValidateToken(ctx, token, orgID)
            if err != nil {
                http.Error(w, "Token validation failed", http.StatusUnauthorized)
                return
            }
            
            if !validation.Valid {
                http.Error(w, validation.ErrorMessage, http.StatusUnauthorized)
                return
            }
            
            // Add user info to context
            ctx = context.WithValue(r.Context(), "user", validation.User)
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}
TypeScript Auth Guard
typescript
// Express middleware for token validation
import { Request, Response, NextFunction } from 'express';

async function authGuard(req: Request, res: Response, next: NextFunction) {
    const authHeader = req.headers.authorization;
    
    if (!authHeader) {
        res.status(401).json({ error: 'Missing authorization header' });
        return;
    }
    
    const parts = authHeader.split(' ');
    if (parts.length !== 2 || parts[0] !== 'Bearer') {
        res.status(401).json({ error: 'Invalid authorization format' });
        return;
    }
    
    const token = parts[1];
    
    try {
        const authClient = new FirebaseAuthClient(process.env.AUTH_SERVICE_URL!);
        const validation = await authClient.validateToken(
            token,
            req.headers['x-organization-id'] as string
        );
        
        if (!validation.valid) {
            res.status(401).json({ error: validation.error });
            return;
        }
        
        (req as any).user = validation.user;
        next();
    } catch (error) {
        res.status(500).json({ error: 'Authentication service error' });
    }
}
Notification Templates
yaml
# notification-templates.yaml
templates:
  welcome:
    title: "Welcome to {{.Platform}}!"
    body: "Hello {{.UserName}}, welcome to our platform. Get started today!"
    data:
      type: "welcome"
      screen: "onboarding"
  
  transaction:
    title: "Transaction {{.Status}}"
    body: "Your transaction of {{.Amount}} {{.Asset}} has been {{.Status}}"
    data:
      type: "transaction"
      transaction_id: "{{.TransactionID}}"
  
  price_alert:
    title: "Price Alert: {{.Asset}}"
    body: "{{.Asset}} has reached {{.Price}} {{.QuoteAsset}}"
    data:
      type: "price_alert"
      asset_id: "{{.AssetID}}"
  
  order_filled:
    title: "Order Filled"
    body: "Your {{.Side}} order for {{.Quantity}} {{.Asset}} has been filled at {{.Price}}"
    data:
      type: "order"
      order_id: "{{.OrderID}}"
Best Practices
Security
Always validate tokens on every request

Implement token revocation on signout

Use short-lived tokens (max 1 hour)

Store Firebase private keys securely (use secrets manager)

Implement rate limiting on auth endpoints

Use organization_id for multi-tenant isolation

Performance
Cache validated tokens with short TTL (5 minutes)

Batch notification sends when possible (max 500 tokens)

Use connection pooling for gRPC clients

Implement retry logic with exponential backoff

Monitor token validation latency

Reliability
Implement circuit breakers for Firebase API calls

Use dead letter queues for failed notifications

Monitor Firebase quota usage

Implement graceful degradation for notification failures

Log all authentication events for audit

Client Best Practices
Refresh tokens before expiration

Handle token refresh failures gracefully

Implement silent authentication where possible

Store tokens securely (HTTP-only cookies for web)

Clear tokens on signout

Troubleshooting
Issue	Possible Cause	Solution
Token validation fails	Expired token	Refresh token client-side
Invalid token signature	Wrong Firebase project	Verify Firebase project configuration
User not found	User deleted or wrong UID	Check user exists in Firebase Console
Notification not delivered	Invalid device token	Re-register device token
Rate limit exceeded	Too many requests	Implement exponential backoff
Service unavailable	Firebase outage	Implement fallback authentication
Session not revoked	Token not invalidated	Use global_signout for all devices
Monitoring & Metrics
Key Metrics to Monitor
go
// Prometheus metrics example
var (
    tokenValidationTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "firebase_token_validations_total",
            Help: "Total number of token validations",
        },
        []string{"result"}, // valid, invalid, error
    )
    
    notificationSentTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "firebase_notifications_sent_total",
            Help: "Total number of notifications sent",
        },
        []string{"status"}, // success, failure
    )
    
    tokenValidationDuration = prometheus.NewHistogram(
        prometheus.HistogramOpts{
            Name: "firebase_token_validation_duration_seconds",
            Help: "Token validation duration in seconds",
            Buckets: []float64{0.1, 0.5, 1, 2, 5},
        },
    )
)
License
This documentation is part of the TX Marketplace platform.
