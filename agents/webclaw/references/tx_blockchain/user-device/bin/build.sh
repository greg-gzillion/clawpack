#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting User Device proto build...${NC}"

# Check if proto file exists
if [ ! -f "user-device.proto" ] && [ ! -f "proto/user-device.proto" ]; then
    echo -e "${RED}Error: No user-device.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "user-device.proto" ]; then
    PROTO_FILE="user-device.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/user-device.proto"
    PROTO_PATH="proto"
fi

echo -e "${BLUE}Using proto file: ${PROTO_FILE}${NC}"

# Check for required tools
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        exit 1
    fi
}

check_command protoc
check_command protoc-gen-go
check_command protoc-gen-go-grpc

# Create directories
echo -e "${YELLOW}Creating build directories...${NC}"
mkdir -p build
mkdir -p client/go
mkdir -p client/typescript

# Generate Go files
echo -e "${BLUE}Generating Go protobuf files...${NC}"
protoc \
    --go_out=client/go \
    --go_opt=paths=source_relative \
    --go-grpc_out=client/go \
    --go-grpc_opt=paths=source_relative \
    --proto_path=${PROTO_PATH} \
    ${PROTO_FILE}

# Check for TypeScript project
if [ -f "package.json" ] && [ -f "tsconfig.json" ]; then
    echo -e "${BLUE}TypeScript project detected. Generating TypeScript files...${NC}"
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing npm dependencies...${NC}"
        npm install
    fi
    
    if command -v protoc-gen-ts &> /dev/null; then
        protoc \
            --plugin=protoc-gen-ts=$(which protoc-gen-ts) \
            --ts_out=client/typescript \
            --proto_path=${PROTO_PATH} \
            ${PROTO_FILE}
    fi
    
    if command -v protoc-gen-grpc-web &> /dev/null; then
        protoc \
            --plugin=protoc-gen-grpc-web=$(which protoc-gen-grpc-web) \
            --grpc-web_out=import_style=typescript,mode=grpcwebtext:client/typescript \
            --proto_path=${PROTO_PATH} \
            ${PROTO_FILE}
    fi
    
    echo -e "${GREEN}TypeScript files generated successfully${NC}"
else
    echo -e "${YELLOW}Skipping TypeScript generation (package.json or tsconfig.json not found)${NC}"
fi

# Generate documentation
echo -e "${BLUE}Generating documentation...${NC}"
if command -v protoc-gen-doc &> /dev/null; then
    protoc \
        --doc_out=build \
        --doc_opt=markdown,user-device-api.md \
        --proto_path=${PROTO_PATH} \
        ${PROTO_FILE}
    echo -e "${GREEN}Documentation generated${NC}"
fi

# Add generated files to git
echo -e "${YELLOW}Adding generated files to git...${NC}"
git add client/go/*.pb.go 2>/dev/null || true
git add client/typescript/*.ts 2>/dev/null || true
git add build/ 2>/dev/null || true

echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}Generated files:${NC}"
echo "  - client/go/user_device.pb.go"
echo "  - client/go/user_device_grpc.pb.go"
if [ -f "client/typescript/user_device.ts" ]; then
    echo "  - client/typescript/user_device.ts"
fi
echo "  - build/user-device-api.md"
Save and make executable:

Ctrl+O, Enter, Ctrl+X

chmod +x ~/dev/TXdocumentation/user-device/bin/build.sh

3. User Device Go Client
bash
mkdir -p ~/dev/TXdocumentation/user-device/client/go
nano ~/dev/TXdocumentation/user-device/client/go/user_device_client.go
go
package userdevice

import (
    "context"
    "fmt"
    "log"
    "os"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/metadata"
    
    userdevicepb "github.com/sologenic/user-device/client/go"
    "google.golang.org/protobuf/types/known/timestamppb"
)

type UserDeviceClient struct {
    client userdevicepb.UserDeviceServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new user device client
func NewUserDeviceClient(addr string) (*UserDeviceClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("USER_SESSION_STORE_TESTING"); testingMode == "TRUE" {
            return &UserDeviceClient{}, nil
        }
        return nil, fmt.Errorf("USER_SESSION_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to user device service: %w", err)
    }
    
    return &UserDeviceClient{
        client: userdevicepb.NewUserDeviceServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *UserDeviceClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *UserDeviceClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *UserDeviceClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// ==================== Device Management ====================

// Register a new device
func (c *UserDeviceClient) RegisterDevice(ctx context.Context, userID, orgID, deviceName, osVersion, appVersion, model, manufacturer, ipAddress string, platform userdevicepb.DevicePlatform, metadata map[string]string, capabilities []string) (*userdevicepb.Device, error) {
    if c.client == nil {
        return mockDevice(userID, deviceName, platform), nil
    }
    
    req := &userdevicepb.RegisterDeviceRequest{
        UserId:         userID,
        OrganizationId: orgID,
        DeviceName:     deviceName,
        Platform:       platform,
        OsVersion:      osVersion,
        AppVersion:     appVersion,
        Model:          model,
        Manufacturer:   manufacturer,
        IpAddress:      ipAddress,
        Metadata:       metadata,
        Capabilities:   capabilities,
    }
    
    resp, err := c.client.RegisterDevice(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("register device failed: %w", err)
    }
    
    if !resp.Registered {
        return nil, fmt.Errorf("device registration failed: %s", resp.Message)
    }
    
    return resp.Device, nil
}

// Unregister a device
func (c *UserDeviceClient) UnregisterDevice(ctx context.Context, userID, orgID, deviceID, reason string) error {
    if c.client == nil {
        return nil
    }
    
    req := &userdevicepb.UnregisterDeviceRequest{
        UserId:         userID,
        OrganizationId: orgID,
        DeviceId:       deviceID,
        Reason:         reason,
    }
    
    resp, err := c.client.UnregisterDevice(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("unregister device failed: %w", err)
    }
    
    if !resp.Unregistered {
        return fmt.Errorf("device unregistration failed: %s", resp.Message)
    }
    
    return nil
}

// Get all devices for a user
func (c *UserDeviceClient) GetDevices(ctx context.Context, userID, orgID string, includeInactive bool) ([]*userdevicepb.Device, int32, int32, error) {
    if c.client == nil {
        return []*userdevicepb.Device{mockDevice(userID, "Test Device", userdevicepb.DevicePlatform_IOS)}, 1, 1, nil
    }
    
    req := &userdevicepb.GetDevicesRequest{
        UserId:          userID,
        OrganizationId:  orgID,
        IncludeInactive: includeInactive,
    }
    
    resp, err := c.client.GetDevices(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, 0, fmt.Errorf("get devices failed: %w", err)
    }
    
    return resp.Devices, resp.TotalCount, resp.ActiveCount, nil
}

// Update device information
func (c *UserDeviceClient) UpdateDevice(ctx context.Context, userID, orgID, deviceID string, deviceName, osVersion, appVersion *string, isTrusted, isPrimary *bool, metadata map[string]string) (*userdevicepb.Device, error) {
    if c.client == nil {
        return mockDevice(userID, *deviceName, userdevicepb.DevicePlatform_ANDROID), nil
    }
    
    req := &userdevicepb.UpdateDeviceRequest{
        UserId:         userID,
        OrganizationId: orgID,
        DeviceId:       deviceID,
        Metadata:       metadata,
    }
    
    if deviceName != nil {
        req.DeviceName = &userdevicepb.UpdateDeviceRequest_DeviceName{DeviceName: *deviceName}
    }
    if osVersion != nil {
        req.OsVersion = &userdevicepb.UpdateDeviceRequest_OsVersion{OsVersion: *osVersion}
    }
    if appVersion != nil {
        req.AppVersion = &userdevicepb.UpdateDeviceRequest_AppVersion{AppVersion: *appVersion}
    }
    if isTrusted != nil {
        req.IsTrusted = &userdevicepb.UpdateDeviceRequest_IsTrusted{IsTrusted: *isTrusted}
    }
    if isPrimary != nil {
        req.IsPrimary = &userdevicepb.UpdateDeviceRequest_IsPrimary{IsPrimary: *isPrimary}
    }
    
    resp, err := c.client.UpdateDevice(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update device failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("device update failed")
    }
    
    return resp.Device, nil
}

// ==================== Firebase Token Management ====================

// Register a Firebase token for push notifications
func (c *UserDeviceClient) RegisterFirebaseToken(ctx context.Context, userID, orgID, deviceID, fcmToken, apnsToken, pushProvider, replacesTokenID string, metadata map[string]string) (*userdevicepb.FirebaseToken, error) {
    if c.client == nil {
        return mockFirebaseToken(userID, deviceID, fcmToken), nil
    }
    
    req := &userdevicepb.RegisterFirebaseTokenRequest{
        UserId:          userID,
        OrganizationId:  orgID,
        DeviceId:        deviceID,
        FcmToken:        fcmToken,
        ApnsToken:       apnsToken,
        PushProvider:    pushProvider,
        ReplacesTokenId: replacesTokenID,
        Metadata:        metadata,
    }
    
    resp, err := c.client.RegisterFirebaseToken(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("register firebase token failed: %w", err)
    }
    
    if !resp.Registered {
        return nil, fmt.Errorf("firebase token registration failed: %s", resp.Message)
    }
    
    return resp.Token, nil
}

// Update a Firebase token
func (c *UserDeviceClient) UpdateFirebaseToken(ctx context.Context, userID, orgID, tokenID string, fcmToken, apnsToken *string, isActive *bool, metadata map[string]string) (*userdevicepb.FirebaseToken, error) {
    if c.client == nil {
        return mockFirebaseToken(userID, "device-id", *fcmToken), nil
    }
    
    req := &userdevicepb.UpdateFirebaseTokenRequest{
        UserId:         userID,
        OrganizationId: orgID,
        TokenId:        tokenID,
        Metadata:       metadata,
    }
    
    if fcmToken != nil {
        req.FcmToken = &userdevicepb.UpdateFirebaseTokenRequest_FcmToken{FcmToken: *fcmToken}
    }
    if apnsToken != nil {
        req.ApnsToken = &userdevicepb.UpdateFirebaseTokenRequest_ApnsToken{ApnsToken: *apnsToken}
    }
    if isActive != nil {
        req.IsActive = &userdevicepb.UpdateFirebaseTokenRequest_IsActive{IsActive: *isActive}
    }
    
    resp, err := c.client.UpdateFirebaseToken(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update firebase token failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("firebase token update failed")
    }
    
    return resp.Token, nil
}

// Remove a Firebase token
func (c *UserDeviceClient) RemoveFirebaseToken(ctx context.Context, userID, orgID, tokenID, reason string) error {
    if c.client == nil {
        return nil
    }
    
    req := &userdevicepb.RemoveFirebaseTokenRequest{
        UserId:         userID,
        OrganizationId: orgID,
        TokenId:        tokenID,
        Reason:         reason,
    }
    
    resp, err := c.client.RemoveFirebaseToken(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("remove firebase token failed: %w", err)
    }
    
    if !resp.Removed {
        return fmt.Errorf("firebase token removal failed: %s", resp.Message)
    }
    
    return nil
}

// Get Firebase tokens for a user
func (c *UserDeviceClient) GetUserFirebaseTokens(ctx context.Context, userID, orgID string, includeInactive bool) ([]*userdevicepb.FirebaseToken, error) {
    if c.client == nil {
        return []*userdevicepb.FirebaseToken{mockFirebaseToken(userID, "device-id", "fcm-token")}, nil
    }
    
    req := &userdevicepb.GetUserFirebaseTokensRequest{
        UserId:          userID,
        OrganizationId:  orgID,
        IncludeInactive: includeInactive,
    }
    
    resp, err := c.client.GetUserFirebaseTokens(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get user firebase tokens failed: %w", err)
    }
    
    return resp.Tokens, nil
}

// ==================== Session Token Management ====================

// Create a new session
func (c *UserDeviceClient) CreateSession(ctx context.Context, userID, orgID, deviceID, ipAddress, userAgent string, sessionType userdevicepb.SessionType, scopes []string, claims map[string]string, expiryMinutes int32, metadata map[string]string) (*userdevicepb.SessionToken, string, error) {
    if c.client == nil {
        return mockSessionToken(userID, sessionType), "mock-session-token", nil
    }
    
    req := &userdevicepb.CreateSessionRequest{
        UserId:         userID,
        OrganizationId: orgID,
        DeviceId:       deviceID,
        SessionType:    sessionType,
        IpAddress:      ipAddress,
        UserAgent:      userAgent,
        Scopes:         scopes,
        Claims:         claims,
        ExpiryMinutes:  expiryMinutes,
        Metadata:       metadata,
    }
    
    resp, err := c.client.CreateSession(c.getContext(ctx), req)
    if err != nil {
        return nil, "", fmt.Errorf("create session failed: %w", err)
    }
    
    if !resp.Created {
        return nil, "", fmt.Errorf("session creation failed: %s", resp.Message)
    }
    
    return resp.Session, resp.Token, nil
}

// Validate a session token
func (c *UserDeviceClient) ValidateSession(ctx context.Context, token, userID, orgID string, requiredScopes []string) (bool, *userdevicepb.SessionToken, error) {
    if c.client == nil {
        return true, mockSessionToken(userID, userdevicepb.SessionType_AUTHENTICATION), nil
    }
    
    req := &userdevicepb.ValidateSessionRequest{
        Token:          token,
        UserId:         userID,
        OrganizationId: orgID,
        RequiredScopes: requiredScopes,
    }
    
    resp, err := c.client.ValidateSession(c.getContext(ctx), req)
    if err != nil {
        return false, nil, fmt.Errorf("validate session failed: %w", err)
    }
    
    return resp.Valid, resp.Session, nil
}

// Revoke a session
func (c *UserDeviceClient) RevokeSession(ctx context.Context, sessionID, userID, orgID, reason string) error {
    if c.client == nil {
        return nil
    }
    
    req := &userdevicepb.RevokeSessionRequest{
        SessionId:      sessionID,
        UserId:         userID,
        OrganizationId: orgID,
        Reason:         reason,
    }
    
    resp, err := c.client.RevokeSession(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("revoke session failed: %w", err)
    }
    
    if !resp.Revoked {
        return fmt.Errorf("session revocation failed: %s", resp.Message)
    }
    
    return nil
}

// Revoke all sessions for a user
func (c *UserDeviceClient) RevokeAllSessions(ctx context.Context, userID, orgID, excludeSessionID, reason string) (int32, error) {
    if c.client == nil {
        return 5, nil
    }
    
    req := &userdevicepb.RevokeAllSessionsRequest{
        UserId:          userID,
        OrganizationId:  orgID,
        ExcludeSessionId: excludeSessionID,
        Reason:          reason,
    }
    
    resp, err := c.client.RevokeAllSessions(c.getContext(ctx), req)
    if err != nil {
        return 0, fmt.Errorf("revoke all sessions failed: %w", err)
    }
    
    return resp.RevokedCount, nil
}

// Extend a session
func (c *UserDeviceClient) ExtendSession(ctx context.Context, sessionID, userID, orgID string, extendMinutes int32) (*userdevicepb.SessionToken, error) {
    if c.client == nil {
        return mockSessionToken(userID, userdevicepb.SessionType_AUTHENTICATION), nil
    }
    
    req := &userdevicepb.ExtendSessionRequest{
        SessionId:      sessionID,
        UserId:         userID,
        OrganizationId: orgID,
        ExtendMinutes:  extendMinutes,
    }
    
    resp, err := c.client.ExtendSession(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("extend session failed: %w", err)
    }
    
    if !resp.Extended {
        return nil, fmt.Errorf("session extension failed")
    }
    
    return resp.Session, nil
}

// List user sessions
func (c *UserDeviceClient) ListUserSessions(ctx context.Context, userID, orgID string, includeExpired bool, limit, offset int32) ([]*userdevicepb.SessionToken, int32, int32, error) {
    if c.client == nil {
        return []*userdevicepb.SessionToken{mockSessionToken(userID, userdevicepb.SessionType_AUTHENTICATION)}, 1, 1, nil
    }
    
    req := &userdevicepb.ListUserSessionsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        IncludeExpired: includeExpired,
        Limit:          limit,
        Offset:         offset,
    }
    
    resp, err := c.client.ListUserSessions(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, 0, fmt.Errorf("list user sessions failed: %w", err)
    }
    
    return resp.Sessions, resp.TotalCount, resp.ActiveCount, nil
}

// ==================== Push Notification Delivery ====================

// Send a push notification to a user
func (c *UserDeviceClient) SendPushNotification(ctx context.Context, userID, orgID, title, body, imageURL, clickAction string, data map[string]string, priority userdevicepb.NotificationPriority, ttlSeconds int32, isSilent bool, deviceID, tokenID string) (*userdevicepb.SendPushNotificationResponse, error) {
    if c.client == nil {
        return &userdevicepb.SendPushNotificationResponse{
            NotificationId: "mock-notification-id",
            Sent:           true,
            DeliveryCount:  1,
        }, nil
    }
    
    req := &userdevicepb.SendPushNotificationRequest{
        UserId:        userID,
        OrganizationId: orgID,
        Title:         title,
        Body:          body,
        ImageUrl:      imageURL,
        ClickAction:   clickAction,
        Data:          data,
        Priority:      priority,
        TtlSeconds:    ttlSeconds,
        IsSilent:      isSilent,
        DeviceId:      deviceID,
        TokenId:       tokenID,
    }
    
    resp, err := c.client.SendPushNotification(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("send push notification failed: %w", err)
    }
    
    return resp, nil
}

// Send bulk push notifications to multiple users
func (c *UserDeviceClient) SendBulkPushNotification(ctx context.Context, userIDs []string, orgID, title, body, imageURL, clickAction string, data map[string]string, priority userdevicepb.NotificationPriority, ttlSeconds int32) (*userdevicepb.SendBulkPushNotificationResponse, error) {
    if c.client == nil {
        return &userdevicepb.SendBulkPushNotificationResponse{
            BatchId:              "mock-batch-id",
            TotalRecipients:      int32(len(userIDs)),
            SuccessfulDeliveries: int32(len(userIDs)),
            FailedDeliveries:     0,
        }, nil
    }
    
    req := &userdevicepb.SendBulkPushNotificationRequest{
        UserIds:       userIDs,
        OrganizationId: orgID,
        Title:         title,
        Body:          body,
        ImageUrl:      imageURL,
        ClickAction:   clickAction,
        Data:          data,
        Priority:      priority,
        TtlSeconds:    ttlSeconds,
    }
    
    resp, err := c.client.SendBulkPushNotification(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("send bulk push notification failed: %w", err)
    }
    
    return resp, nil
}

// ==================== White-Label Session Management ====================

// Create a white-label session
func (c *UserDeviceClient) CreateWhiteLabelSession(ctx context.Context, userID, orgID, brandID, theme, ipAddress, userAgent string, expiryMinutes int32, metadata map[string]string) (*userdevicepb.WhiteLabelSession, string, error) {
    if c.client == nil {
        return mockWhiteLabelSession(brandID), "mock-wl-token", nil
    }
    
    req := &userdevicepb.CreateWhiteLabelSessionRequest{
        UserId:         userID,
        OrganizationId: orgID,
        BrandId:        brandID,
        Theme:          theme,
        IpAddress:      ipAddress,
        UserAgent:      userAgent,
        ExpiryMinutes:  expiryMinutes,
        Metadata:       metadata,
    }
    
    resp, err := c.client.CreateWhiteLabelSession(c.getContext(ctx), req)
    if err != nil {
        return nil, "", fmt.Errorf("create white-label session failed: %w", err)
    }
    
    if !resp.Created {
        return nil, "", fmt.Errorf("white-label session creation failed: %s", resp.Message)
    }
    
    return resp.Session, resp.Token, nil
}

// Validate a white-label session
func (c *UserDeviceClient) ValidateWhiteLabelSession(ctx context.Context, token, brandID string) (bool, *userdevicepb.WhiteLabelSession, string, error) {
    if c.client == nil {
        return true, mockWhiteLabelSession(brandID), `{"theme":"dark"}`, nil
    }
    
    req := &userdevicepb.ValidateWhiteLabelSessionRequest{
        Token:   token,
        BrandId: brandID,
    }
    
    resp, err := c.client.ValidateWhiteLabelSession(c.getContext(ctx), req)
    if err != nil {
        return false, nil, "", fmt.Errorf("validate white-label session failed: %w", err)
    }
    
    return resp.Valid, resp.Session, resp.BrandConfigJson, nil
}

// ==================== Payment Session Management ====================

// Create a payment session
func (c *UserDeviceClient) CreatePaymentSession(ctx context.Context, userID, orgID, paymentID, amount, currency, paymentGateway, successURL, cancelURL, webhookURL, paymentMethod string, expiryMinutes int32, metadata map[string]string) (*userdevicepb.PaymentSession, string, string, error) {
    if c.client == nil {
        return mockPaymentSession(paymentID, amount, currency), "mock-payment-token", "https://checkout.example.com", nil
    }
    
    req := &userdevicepb.CreatePaymentSessionRequest{
        UserId:         userID,
        OrganizationId: orgID,
        PaymentId:      paymentID,
        Amount:         amount,
        Currency:       currency,
        PaymentGateway: paymentGateway,
        SuccessUrl:     successURL,
        CancelUrl:      cancelURL,
        WebhookUrl:     webhookURL,
        PaymentMethod:  paymentMethod,
        ExpiryMinutes:  expiryMinutes,
        Metadata:       metadata,
    }
    
    resp, err := c.client.CreatePaymentSession(c.getContext(ctx), req)
    if err != nil {
        return nil, "", "", fmt.Errorf("create payment session failed: %w", err)
    }
    
    if !resp.Created {
        return nil, "", "", fmt.Errorf("payment session creation failed: %s", resp.Message)
    }
    
    return resp.Session, resp.Token, resp.CheckoutUrl, nil
}

// Get payment session
func (c *UserDeviceClient) GetPaymentSession(ctx context.Context, sessionID, token, userID, orgID string) (*userdevicepb.PaymentSession, bool, error) {
    if c.client == nil {
        return mockPaymentSession("payment-123", "100.00", "USD"), true, nil
    }
    
    req := &userdevicepb.GetPaymentSessionRequest{
        SessionId:      sessionID,
        Token:          token,
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetPaymentSession(c.getContext(ctx), req)
    if err != nil {
        return nil, false, fmt.Errorf("get payment session failed: %w", err)
    }
    
    return resp.Session, resp.Found, nil
}

// Update payment session
func (c *UserDeviceClient) UpdatePaymentSession(ctx context.Context, sessionID, userID, orgID string, status, paymentIntentID *string, metadata map[string]string) (*userdevicepb.PaymentSession, error) {
    if c.client == nil {
        return mockPaymentSession("payment-123", "100.00", "USD"), nil
    }
    
    req := &userdevicepb.UpdatePaymentSessionRequest{
        SessionId:      sessionID,
        UserId:         userID,
        OrganizationId: orgID,
        Metadata:       metadata,
    }
    
    if status != nil {
        req.Status = &userdevicepb.UpdatePaymentSessionRequest_Status{Status: *status}
    }
    if paymentIntentID != nil {
        req.PaymentIntentId = &userdevicepb.UpdatePaymentSessionRequest_PaymentIntentId{PaymentIntentId: *paymentIntentID}
    }
    
    resp, err := c.client.UpdatePaymentSession(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update payment session failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("payment session update failed")
    }
    
    return resp.Session, nil
}

// Complete payment session
func (c *UserDeviceClient) CompletePaymentSession(ctx context.Context, sessionID, userID, orgID, paymentIntentID, transactionID string, success bool, failureReason string) (*userdevicepb.PaymentSession, error) {
    if c.client == nil {
        return mockPaymentSessionCompleted("payment-123"), nil
    }
    
    req := &userdevicepb.CompletePaymentSessionRequest{
        SessionId:       sessionID,
        UserId:          userID,
        OrganizationId:  orgID,
        PaymentIntentId: paymentIntentID,
        TransactionId:   transactionID,
        Success:         success,
        FailureReason:   failureReason,
    }
    
    resp, err := c.client.CompletePaymentSession(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("complete payment session failed: %w", err)
    }
    
    if !resp.Completed {
        return nil, fmt.Errorf("payment session completion failed: %s", resp.Message)
    }
    
    return resp.Session, nil
}

// ==================== Token Cleanup ====================

// Cleanup expired tokens
func (c *UserDeviceClient) CleanupExpiredTokens(ctx context.Context, orgID string, olderThanDays int32, dryRun bool) (*userdevicepb.CleanupExpiredTokensResponse, error) {
    if c.client == nil {
        return &userdevicepb.CleanupExpiredTokensResponse{
            TokensRemoved:        10,
            TokensMarkedInactive: 5,
            DevicesAffected:      8,
        }, nil
    }
    
    req := &userdevicepb.CleanupExpiredTokensRequest{
        OrganizationId: orgID,
        OlderThanDays:  olderThanDays,
        DryRun:         dryRun,
    }
    
    resp, err := c.client.CleanupExpiredTokens(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("cleanup expired tokens failed: %w", err)
    }
    
    return resp, nil
}

// Get token statistics
func (c *UserDeviceClient) GetTokenStats(ctx context.Context, orgID string, fromDate, toDate time.Time) (*userdevicepb.GetTokenStatsResponse, error) {
    if c.client == nil {
        return &userdevicepb.GetTokenStatsResponse{
            TotalTokens:              100,
            ActiveTokens:             75,
            ExpiredTokens:            25,
            TokensCreatedLast24h:     5,
            TokensCreatedLast7d:      20,
            TokensCreatedLast30d:     50,
            AverageTokenAgeDays:      15.5,
        }, nil
    }
    
    req := &userdevicepb.GetTokenStatsRequest{
        OrganizationId: orgID,
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestamppb.New(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestamppb.New(toDate)
    }
    
    resp, err := c.client.GetTokenStats(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get token stats failed: %w", err)
    }
    
    return resp, nil
}

// ==================== Analytics ====================

// Get device analytics
func (c *UserDeviceClient) GetDeviceAnalytics(ctx context.Context, orgID string, fromDate, toDate time.Time, groupBy string) (*userdevicepb.GetDeviceAnalyticsResponse, error) {
    if c.client == nil {
        return &userdevicepb.GetDeviceAnalyticsResponse{
            TotalDevices:   500,
            ActiveDevices:  350,
            NewDevices:     50,
        }, nil
    }
    
    req := &userdevicepb.GetDeviceAnalyticsRequest{
        OrganizationId: orgID,
        GroupBy:        groupBy,
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestamppb.New(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestamppb.New(toDate)
    }
    
    resp, err := c.client.GetDeviceAnalytics(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get device analytics failed: %w", err)
    }
    
    return resp, nil
}

// ==================== Mock Functions ====================

func mockDevice(userID, deviceName string, platform userdevicepb.DevicePlatform) *userdevicepb.Device {
    return &userdevicepb.Device{
        DeviceId:     "mock-device-id",
        UserId:       userID,
        DeviceName:   deviceName,
        Platform:     platform,
        Status:       userdevicepb.DeviceStatus_ACTIVE,
        IsTrusted:    true,
        FirstSeenAt:  timestamppb.Now(),
        LastSeenAt:   timestamppb.Now(),
        RegisteredAt: timestamppb.Now(),
    }
}

func mockFirebaseToken(userID, deviceID, fcmToken string) *userdevicepb.FirebaseToken {
    return &userdevicepb.FirebaseToken{
        TokenId:     "mock-token-id",
        DeviceId:    deviceID,
        UserId:      userID,
        FcmToken:    fcmToken,
        IsActive:    true,
        UsageCount:  10,
        CreatedAt:   timestamppb.Now(),
        LastUsedAt:  timestamppb.Now(),
        ExpiresAt:   timestamppb.New(time.Now().Add(30 * 24 * time.Hour)),
    }
}

func mockSessionToken(userID string, sessionType userdevicepb.SessionType) *userdevicepb.SessionToken {
    return &userdevicepb.SessionToken{
        SessionId:   "mock-session-id",
        UserId:      userID,
        SessionType: sessionType,
        Status:      userdevicepb.SessionStatus_ACTIVE,
        IssuedAt:    timestamppb.Now(),
        ExpiresAt:   timestamppb.New(time.Now().Add(1 * time.Hour)),
    }
}

func mockWhiteLabelSession(brandID string) *userdevicepb.WhiteLabelSession {
    return &userdevicepb.WhiteLabelSession{
        SessionId:  "mock-wl-session-id",
        BrandId:    brandID,
        Theme:      "dark",
        LogoUrl:    "https://example.com/logo.png",
        Status:userdevicepb.SessionStatus_ACTIVE,
        IssuedAt:   timestamppb.Now(),
        ExpiresAt:  timestamppb.New(time.Now().Add(30 * time.Minute)),
    }
}

func mockPaymentSession(paymentID, amount, currency string) *userdevicepb.PaymentSession {
    return &userdevicepb.PaymentSession{
        SessionId:  "mock-payment-session-id",
        PaymentId:  paymentID,
        Amount:     amount,
        Currency:   currency,
        Status:     "pending",
        CreatedAt:  timestamppb.Now(),
        ExpiresAt:  timestamppb.New(time.Now().Add(1 * time.Hour)),
    }
}

func mockPaymentSessionCompleted(paymentID string) *userdevicepb.PaymentSession {
    return &userdevicepb.PaymentSession{
        SessionId:     "mock-payment-session-id",
        PaymentId:     paymentID,
        Status:        "completed",
        CreatedAt:     timestamppb.Now(),
        CompletedAt:   timestamppb.Now(),
    }
}

// ==================== Example Usage ====================

func main() {
    client, err := NewUserDeviceClient("user-session-store:50078")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    userID := "user-789"
    
    // Register a device
    device, err := client.RegisterDevice(ctx, userID, orgID, "iPhone 15 Pro", "17.0", "2.0.1", "iPhone15,2", "Apple", "192.168.1.100", userdevicepb.DevicePlatform_IOS, map[string]string{
        "color": "black",
    }, []string{"push", "biometric"})
    if err != nil {
        log.Printf("Failed to register device: %v", err)
    } else {
        log.Printf("Device registered: %s (%s)", device.DeviceId, device.DeviceName)
    }
    
    // Register Firebase token for push notifications
    token, err := client.RegisterFirebaseToken(ctx, userID, orgID, device.DeviceId, "fcm_token_12345", "apns_token_67890", "fcm", "", map[string]string{
        "app_version": "2.0.1",
        "build":       "123",
    })
    if err != nil {
        log.Printf("Failed to register Firebase token: %v", err)
    } else {
        log.Printf("Firebase token registered: %s", token.TokenId)
    }
    
    // Create a session
    session, sessionToken, err := client.CreateSession(ctx, userID, orgID, device.DeviceId, "192.168.1.100", "Mozilla/5.0...", userdevicepb.SessionType_AUTHENTICATION, []string{"read", "write"}, map[string]string{
        "role": "user",
    }, 60, nil)
    if err != nil {
        log.Printf("Failed to create session: %v", err)
    } else {
        log.Printf("Session created: %s (expires: %v)", session.SessionId, session.ExpiresAt)
        log.Printf("Session token: %s", sessionToken)
    }
    
    // Validate the session
    valid, validatedSession, err := client.ValidateSession(ctx, sessionToken, userID, orgID, []string{"read"})
    if err != nil {
        log.Printf("Failed to validate session: %v", err)
    } else if valid {
        log.Printf("Session is valid for user: %s", validatedSession.UserId)
    }
    
    // Send a push notification
    pushResp, err := client.SendPushNotification(ctx, userID, orgID, "Price Alert", "TX has reached $100", "https://example.com/icon.png", "OPEN_TRADE", map[string]string{
        "trade_id": "trade-123",
        "price":    "100.00",
    }, userdevicepb.NotificationPriority_HIGH, 3600, false, device.DeviceId, "")
    if err != nil {
        log.Printf("Failed to send push notification: %v", err)
    } else {
        log.Printf("Push notification sent: %s (delivered to %d devices)", pushResp.NotificationId, pushResp.DeliveryCount)
    }
    
    // Create a white-label session
    wlSession, wlToken, err := client.CreateWhiteLabelSession(ctx, userID, orgID, "brand-acme", "dark", "192.168.1.100", "Mozilla/5.0...", 30, map[string]string{
        "feature_flags": "new_ui",
    })
    if err != nil {
        log.Printf("Failed to create white-label session: %v", err)
    } else {
        log.Printf("White-label session created for brand: %s", wlSession.BrandId)
        
        // Validate white-label session
        valid, _, config, err := client.ValidateWhiteLabelSession(ctx, wlToken, "brand-acme")
        if err != nil {
            log.Printf("Failed to validate white-label session: %v", err)
        } else if valid {
            log.Printf("White-label session valid with config: %s", config)
        }
    }
    
    // Create a payment session
    paymentSession, paymentToken, checkoutURL, err := client.CreatePaymentSession(ctx, userID, orgID, "payment-123", "100.00", "USD", "stripe", "https://example.com/success", "https://example.com/cancel", "https://api.example.com/webhook", "card", 15, map[string]string{
        "product_id": "product-456",
    })
    if err != nil {
        log.Printf("Failed to create payment session: %v", err)
    } else {
        log.Printf("Payment session created: %s", paymentSession.SessionId)
        log.Printf("Checkout URL: %s", checkoutURL)
        
        // Complete payment session when payment is done
        completed, err := client.CompletePaymentSession(ctx, paymentSession.SessionId, userID, orgID, "pi_123456", "tx_789012", true, "")
        if err != nil {
            log.Printf("Failed to complete payment: %v", err)
        } else {
            log.Printf("Payment completed: %s", completed.Status)
        }
    }
    
    // Get all devices for user
    devices, total, active, err := client.GetDevices(ctx, userID, orgID, false)
    if err != nil {
        log.Printf("Failed to get devices: %v", err)
    } else {
        log.Printf("User has %d devices (%d active)", total, active)
        for _, d := range devices {
            log.Printf("  - %s (%s) - last seen: %v", d.DeviceName, d.Platform, d.LastSeenAt)
        }
    }
    
    // List user sessions
    sessions, totalSessions, activeSessions, err := client.ListUserSessions(ctx, userID, orgID, false, 20, 0)
    if err != nil {
        log.Printf("Failed to list sessions: %v", err)
    } else {
        log.Printf("User has %d sessions (%d active)", totalSessions, activeSessions)
        for _, s := range sessions {
            log.Printf("  - Session %s (%s) - expires: %v", s.SessionId, s.SessionType, s.ExpiresAt)
        }
    }
    
    // Cleanup expired tokens
    cleanup, err := client.CleanupExpiredTokens(ctx, orgID, 30, false)
    if err != nil {
        log.Printf("Failed to cleanup tokens: %v", err)
    } else {
        log.Printf("Cleaned up %d expired tokens, affected %d devices", cleanup.TokensRemoved, cleanup.DevicesAffected)
    }
    
    // Get token stats
    stats, err := client.GetTokenStats(ctx, orgID, time.Now().AddDate(0, -1, 0), time.Now())
    if err != nil {
        log.Printf("Failed to get token stats: %v", err)
    } else {
        log.Printf("Token stats: %d total, %d active, %d expired", stats.TotalTokens, stats.ActiveTokens, stats.ExpiredTokens)
        log.Printf("New tokens last 24h: %d", stats.TokensCreatedLast24h)
    }
}
Save the file:

Ctrl+O, Enter, Ctrl+X

4. User Device Docker Compose
bash
nano ~/dev/TXdocumentation/user-device/docker-compose.yml
yaml
version: '3.8'

services:
  user-device-service:
    image: sologenic/user-device-service:latest
    environment:
      - USER_DEVICE_SERVICE_PORT=50078
      - USER_SESSION_STORE=user-session-store:50078
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=user_devices
      - POSTGRES_USER=user_device_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - FCM_API_KEY=${FCM_API_KEY}
      - FCM_PROJECT_ID=${FCM_PROJECT_ID}
      - APNS_KEY_ID=${APNS_KEY_ID}
      - APNS_TEAM_ID=${APNS_TEAM_ID}
      - APNS_AUTH_KEY_PATH=/app/certs/AuthKey.p8
      - TOKEN_EXPIRY_DAYS=30
      - SESSION_EXPIRY_MINUTES=60
      - MAX_DEVICES_PER_USER=10
      - MAX_SESSIONS_PER_USER=5
      - ENABLE_TOKEN_CLEANUP=true
      - CLEANUP_INTERVAL_HOURS=24
      - LOG_LEVEL=info
    ports:
      - "50078:50078"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
    volumes:
      - ./certs:/app/certs
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50078"]
      interval: 30s
      timeout: 10s
      retries: 3

  user-session-store:
    image: sologenic/user-session-store:latest
    environment:
      - USER_SESSION_STORE_PORT=50079
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=user_devices
      - POSTGRES_USER=user_device_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50079:50079"
    networks:
      - internal
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=user_devices
      - POSTGRES_USER=user_device_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user_device_user -d user_devices"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - internal
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  internal:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
Save the file:

Ctrl+O, Enter, Ctrl+X

5. User Device Environment File
bash
nano ~/dev/TXdocumentation/user-device/.env
bash
# Database Configuration
DB_PASSWORD=your_secure_password

# Service Configuration
USER_SESSION_STORE=user-session-store:50079
USER_SESSION_STORE_TESTING=FALSE

# Firebase Cloud Messaging (FCM)
FCM_API_KEY=your_fcm_api_key
FCM_PROJECT_ID=your_firebase_project_id

# Apple Push Notification Service (APNS)
APNS_KEY_ID=your_apns_key_id
APNS_TEAM_ID=your_apple_team_id
# APNS_AUTH_KEY_PATH is set in docker-compose volume mount

# Token Configuration
TOKEN_EXPIRY_DAYS=30
SESSION_EXPIRY_MINUTES=60

# Limits
MAX_DEVICES_PER_USER=10
MAX_SESSIONS_PER_USER=5

# Cleanup
ENABLE_TOKEN_CLEANUP=true
CLEANUP_INTERVAL_HOURS=24

# Logging
LOG_LEVEL=info
