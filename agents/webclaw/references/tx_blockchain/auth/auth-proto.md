# Auth Service (Auth Proto)

The Auth proto provides all the functionality required to interact with the auth service. It supports token validation, user management, session handling, and permission checking across the platform.

## Overview

The Auth service is a gRPC-based authentication system that handles:
- Token validation and verification
- User session management
- Role and permission checking
- Organization-based access control
- Multi-factor authentication support

## Architecture
┌─────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Web, Mobile, Backend Services) │
└───────────────────┬─────────────────────────────────────┘
│ gRPC/HTTP
▼
┌─────────────────────────────────────────────────────────┐
│ Auth Service │
│ - Token Validation │
│ - Session Management │
│ - Permission Checking │
│ - User Management │
└───────────────────┬─────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Storage Layer │
│ - Session Store (Redis) │
│ - User Store (PostgreSQL) │
│ - Token Blacklist (Redis) │
└─────────────────────────────────────────────────────────┘

text

## Proto Definition

```protobuf
syntax = "proto3";

package auth.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Auth Service Definition
service AuthService {
    // Token Management
    rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
    rpc RefreshToken(RefreshTokenRequest) returns (RefreshTokenResponse);
    rpc RevokeToken(RevokeTokenRequest) returns (RevokeTokenResponse);
    
    // Session Management
    rpc GetSession(GetSessionRequest) returns (GetSessionResponse);
    rpc ListSessions(ListSessionsRequest) returns (ListSessionsResponse);
    rpc RevokeSession(RevokeSessionRequest) returns (RevokeSessionResponse);
    rpc RevokeAllSessions(RevokeAllSessionsRequest) returns (RevokeAllSessionsResponse);
    
    // User Management
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
    rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
    rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
    
    // Permission Management
    rpc CheckPermission(CheckPermissionRequest) returns (CheckPermissionResponse);
    rpc GetUserPermissions(GetUserPermissionsRequest) returns (GetUserPermissionsResponse);
    rpc AddUserRole(AddUserRoleRequest) returns (AddUserRoleResponse);
    rpc RemoveUserRole(RemoveUserRoleRequest) returns (RemoveUserRoleResponse);
    
    // Organization Management
    rpc GetUserOrganizations(GetUserOrganizationsRequest) returns (GetUserOrganizationsResponse);
    rpc SwitchOrganization(SwitchOrganizationRequest) returns (SwitchOrganizationResponse);
}

// ==================== Token Messages ====================

message ValidateTokenRequest {
    string token = 1;                   // JWT token to validate
    string organization_id = 2;         // Organization context
    bool check_blacklist = 3;           // Check if token is blacklisted
}

message ValidateTokenResponse {
    bool valid = 1;                     // Token validity
    TokenClaims claims = 2;             // Token claims if valid
    string error = 3;                   // Error message if invalid
}

message TokenClaims {
    string user_id = 1;                 // User ID
    string email = 2;                   // User email
    string organization_id = 3;         // Current organization
    repeated string roles = 4;          // User roles
    repeated string permissions = 5;    // User permissions
    google.protobuf.Timestamp issued_at = 6;
    google.protobuf.Timestamp expires_at = 7;
    string token_id = 8;                // Unique token identifier
    map<string, string> custom_claims = 9;
}

message RefreshTokenRequest {
    string refresh_token = 1;           // Refresh token
    string organization_id = 2;         // Organization context
}

message RefreshTokenResponse {
    string access_token = 1;            // New access token
    string refresh_token = 2;           // New refresh token
    google.protobuf.Timestamp expires_at = 3;
}

message RevokeTokenRequest {
    string token = 1;                   // Token to revoke
    string organization_id = 2;         // Organization context
}

message RevokeTokenResponse {
    bool success = 1;
    string message = 2;
}

// ==================== Session Messages ====================

message Session {
    string session_id = 1;              // Unique session ID
    string user_id = 2;                 // User ID
    string ip_address = 3;              // Client IP address
    string user_agent = 4;              // Client user agent
    string device_id = 5;               // Device identifier
    string organization_id = 6;         // Organization context
    google.protobuf.Timestamp created_at = 7;
    google.protobuf.Timestamp last_activity = 8;
    google.protobuf.Timestamp expires_at = 9;
    bool is_active = 10;
    map<string, string> metadata = 11;
}

message GetSessionRequest {
    string session_id = 1;              // Session ID
    string user_id = 2;                 // User ID (alternative)
}

message GetSessionResponse {
    Session session = 1;
    bool found = 2;
}

message ListSessionsRequest {
    string user_id = 1;                 // User ID
    string organization_id = 2;         // Organization context
    bool only_active = 3;               // Filter active sessions
    int32 limit = 4;                    // Pagination limit
    int32 offset = 5;                   // Pagination offset
}

message ListSessionsResponse {
    repeated Session sessions = 1;
    int32 total_count = 2;
}

message RevokeSessionRequest {
    string session_id = 1;              // Session to revoke
    string user_id = 2;                 // User ID (for admin)
    string organization_id = 3;         // Organization context
}

message RevokeSessionResponse {
    bool success = 1;
    string message = 2;
}

message RevokeAllSessionsRequest {
    string user_id = 1;                 // User ID
    string organization_id = 2;         // Organization context
    string reason = 3;                  // Revocation reason
}

message RevokeAllSessionsResponse {
    bool success = 1;
    int32 sessions_revoked = 2;
}

// ==================== User Messages ====================

message User {
    string user_id = 1;                 // Unique user ID
    string email = 2;                   // User email
    string name = 3;                    // Display name
    string phone_number = 4;            // Phone number
    string photo_url = 5;               // Profile photo URL
    bool email_verified = 6;            // Email verification status
    bool phone_verified = 7;            // Phone verification status
    string status = 8;                  // active, suspended, deleted
    repeated string roles = 9;          // Assigned roles
    map<string, string> metadata = 10;  // User metadata
    google.protobuf.Timestamp created_at = 11;
    google.protobuf.Timestamp updated_at = 12;
    google.protobuf.Timestamp last_login = 13;
    string default_organization_id = 14;
}

message GetUserRequest {
    string user_id = 1;                 // User ID
    string email = 2;                   // Email (alternative)
    string organization_id = 3;         // Organization context
}

message GetUserResponse {
    User user = 1;
    bool found = 2;
}

message ListUsersRequest {
    string organization_id = 1;         // Organization context
    string role_filter = 2;             // Filter by role
    string status_filter = 3;           // Filter by status
    string search = 4;                  // Search by name or email
    int32 limit = 5;                    // Pagination limit (max 100)
    int32 offset = 6;                   // Pagination offset
}

message ListUsersResponse {
    repeated User users = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

message UpdateUserRequest {
    string user_id = 1;                 // User ID to update
    string organization_id = 2;         // Organization context
    optional string name = 3;           // Updated name
    optional string phone_number = 4;   // Updated phone
    optional string photo_url = 5;      // Updated photo
    optional string status = 6;         // Updated status
    optional map<string, string> metadata = 7;
}

message UpdateUserResponse {
    User user = 1;
    bool updated = 2;
}

message DeleteUserRequest {
    string user_id = 1;                 // User ID to delete
    string organization_id = 2;         // Organization context
    bool permanent = 3;                 // Permanent deletion
}

message DeleteUserResponse {
    bool success = 1;
    string message = 2;
}

// ==================== Permission Messages ====================

message Permission {
    string resource = 1;                // Resource identifier
    string action = 2;                  // Action (read, write, delete, admin)
    string effect = 3;                  // allow, deny
    map<string, string> conditions = 4; // Condition constraints
}

message CheckPermissionRequest {
    string user_id = 1;                 // User ID
    string organization_id = 2;         // Organization context
    string resource = 3;                // Resource to check
    string action = 4;                  // Action to perform
    map<string, string> context = 5;    // Request context
}

message CheckPermissionResponse {
    bool allowed = 1;                   // Permission granted
    string reason = 2;                  // Reason if denied
    repeated string required_permissions = 3;
}

message GetUserPermissionsRequest {
    string user_id = 1;                 // User ID
    string organization_id = 2;         // Organization context
    string resource_filter = 3;         // Filter by resource
}

message GetUserPermissionsResponse {
    repeated Permission permissions = 1;
}

message AddUserRoleRequest {
    string user_id = 1;                 // User ID
    string organization_id = 2;         // Organization context
    string role = 3;                    // Role to add
    string granted_by = 4;              // Admin user ID
}

message AddUserRoleResponse {
    bool success = 1;
    string message = 2;
}

message RemoveUserRoleRequest {
    string user_id = 1;                 // User ID
    string organization_id = 2;         // Organization context
    string role = 3;                    // Role to remove
}

message RemoveUserRoleResponse {
    bool success = 1;
    string message = 2;
}

// ==================== Organization Messages ====================

message OrganizationMembership {
    string organization_id = 1;
    string organization_name = 2;
    string role = 3;
    bool is_default = 4;
    google.protobuf.Timestamp joined_at = 5;
}

message GetUserOrganizationsRequest {
    string user_id = 1;                 // User ID
}

message GetUserOrganizationsResponse {
    repeated OrganizationMembership organizations = 1;
}

message SwitchOrganizationRequest {
    string user_id = 1;                 // User ID
    string organization_id = 2;         // Target organization
    string token = 3;                   // Current token
}

message SwitchOrganizationResponse {
    string new_token = 1;               // New token with updated claims
    string message = 2;
}
Building the Required Files
Build Script
Create bin/build.sh:

bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Auth proto build...${NC}"

# Check if proto file exists
if [ ! -f "auth.proto" ] && [ ! -f "proto/auth.proto" ]; then
    echo -e "${RED}Error: No auth.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "auth.proto" ]; then
    PROTO_FILE="auth.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/auth.proto"
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
    
    # Install required packages if not present
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing npm dependencies...${NC}"
        npm install
    fi
    
    # Check for protoc-gen-ts
    if ! command -v protoc-gen-ts &> /dev/null; then
        echo -e "${YELLOW}Installing protoc-gen-ts...${NC}"
        npm install -g protoc-gen-ts
    fi
    
    # Check for protoc-gen-grpc-web
    if ! command -v protoc-gen-grpc-web &> /dev/null; then
        echo -e "${YELLOW}Installing protoc-gen-grpc-web...${NC}"
        npm install -g protoc-gen-grpc-web
    fi
    
    # Generate TypeScript files
    protoc \
        --plugin=protoc-gen-ts=./node_modules/.bin/protoc-gen-ts \
        --ts_out=client/typescript \
        --proto_path=${PROTO_PATH} \
        ${PROTO_FILE}
    
    protoc \
        --plugin=protoc-gen-grpc-web=./node_modules/.bin/protoc-gen-grpc-web \
        --grpc-web_out=import_style=typescript,mode=grpcwebtext:client/typescript \
        --proto_path=${PROTO_PATH} \
        ${PROTO_FILE}
    
    echo -e "${GREEN}TypeScript files generated successfully${NC}"
else
    echo -e "${YELLOW}Skipping TypeScript generation (package.json or tsconfig.json not found)${NC}"
fi

# Generate documentation
echo -e "${BLUE}Generating documentation...${NC}"
if command -v protoc-gen-doc &> /dev/null; then
    protoc \
        --doc_out=build \
        --doc_opt=markdown,auth-api.md \
        --proto_path=${PROTO_PATH} \
        ${PROTO_FILE}
    echo -e "${GREEN}Documentation generated${NC}"
else
    echo -e "${YELLOW}Skipping documentation generation (protoc-gen-doc not installed)${NC}"
fi

# Add generated files to git
echo -e "${YELLOW}Adding generated files to git...${NC}"
git add client/go/*.go 2>/dev/null || true
git add client/typescript/*.ts 2>/dev/null || true
git add build/ 2>/dev/null || true

echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}Generated files:${NC}"
echo "  - client/go/auth.pb.go"
echo "  - client/go/auth_grpc.pb.go"
if [ -f "client/typescript/auth.ts" ]; then
    echo "  - client/typescript/auth.ts"
fi
echo "  - build/auth-api.md"

# Show file sizes
echo -e "\n${BLUE}File sizes:${NC}"
ls -lh client/go/*.pb.go 2>/dev/null || echo "Go files not found"
if [ -f "client/typescript/auth.ts" ]; then
    ls -lh client/typescript/auth.ts 2>/dev/null
fi
Make the script executable:

bash
chmod +x bin/build.sh
Run Build
bash
./bin/build.sh
Pre-commit Hook Setup
Install pre-commit
bash
# Install pre-commit using Homebrew (macOS)
brew install pre-commit

# Or using pip (Linux/Windows)
pip install pre-commit
Create Makefile
Create Makefile in the root directory:

makefile
.PHONY: build clean test lint proto pre-commit

# Variables
PROTO_FILE := $(wildcard *.proto proto/*.proto)
GO_CLIENT_DIR := client/go
TS_CLIENT_DIR := client/typescript
BUILD_DIR := build

# Default target
all: proto build

# Generate protobuf files
proto:
	@echo "Generating protobuf files..."
	@./bin/build.sh

# Build the project
build:
	@echo "Building project..."
	@if [ -f "go.mod" ]; then \
		echo "Building Go modules..."; \
		go mod download; \
		go build ./...; \
	fi
	@if [ -f "package.json" ]; then \
		echo "Building TypeScript project..."; \
		npm run build; \
	fi

# Run tests
test:
	@echo "Running tests..."
	@if [ -f "go.mod" ]; then \
		go test -v ./...; \
	fi
	@if [ -f "package.json" ]; then \
		npm test; \
	fi

# Lint the code
lint:
	@echo "Linting code..."
	@if [ -f "go.mod" ]; then \
		golangci-lint run; \
	fi
	@if [ -f "package.json" ]; then \
		npm run lint; \
	fi

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -rf $(GO_CLIENT_DIR)/*.pb.go
	@rm -rf $(TS_CLIENT_DIR)/*.ts
	@rm -rf $(BUILD_DIR)
	@if [ -f "go.mod" ]; then \
		go clean; \
	fi
	@if [ -f "package.json" ]; then \
		rm -rf node_modules dist; \
	fi

# Pre-commit hook
pre-commit:
	@echo "Running pre-commit checks..."
	@make lint
	@make test
	@make proto
	@git add $(GO_CLIENT_DIR)/*.pb.go 2>/dev/null || true
	@git add $(TS_CLIENT_DIR)/*.ts 2>/dev/null || true
	@echo "Pre-commit checks passed!"

# Install pre-commit hook
install-hook:
	@echo "Installing pre-commit hook..."
	@pre-commit install
	@echo "Pre-commit hook installed successfully!"

# Help
help:
	@echo "Available targets:"
	@echo "  make proto        - Generate protobuf files"
	@echo "  make build        - Build the project"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Lint the code"
	@echo "  make clean        - Clean generated files"
	@echo "  make pre-commit   - Run pre-commit checks"
	@echo "  make install-hook - Install git pre-commit hook"
Create pre-commit configuration
Create .pre-commit-config.yaml in the root directory:

yaml
repos:
  # Pre-commit hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: detect-private-key

  # Go hooks
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet
      - id: go-imports
      - id: go-cyclo
        args: [-over=15]
      - id: validate-toml
      - id: no-go-testing
      - id: golangci-lint
      - id: go-critic
      - id: go-unit-tests

  # TypeScript hooks
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.0.0
    hooks:
      - id: eslint
        files: \.(js|ts|jsx|tsx)$
        additional_dependencies:
          - eslint@8.56.0
          - typescript@5.3.3
          - '@typescript-eslint/eslint-plugin@6.19.0'
          - '@typescript-eslint/parser@6.19.0'

  # Proto hooks
  - repo: https://github.com/grpc-ecosystem/grpc-health-probe
    rev: v0.4.24
    hooks:
      - id: grpc-health-probe

  # Custom build hook
  - repo: local
    hooks:
      - id: build-proto
        name: Build protobuf files
        entry: ./bin/build.sh
        language: script
        files: \.proto$
        pass_filenames: false
        
      - id: run-tests
        name: Run tests
        entry: make test
        language: system
        files: \.go$|\.ts$
        pass_filenames: false
        
      - id: check-modules
        name: Check Go modules
        entry: go mod tidy
        language: system
        files: go\.mod|go\.sum
        pass_filenames: false
Install Pre-commit Hook
bash
# Install the pre-commit hook
pre-commit install

# Install the pre-commit hook for commit-msg (optional)
pre-commit install --hook-type commit-msg

# Run against all files manually
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate
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
    "google.golang.org/grpc/metadata"
    
    authpb "github.com/sologenic/auth/client/go"
)

type AuthClient struct {
    client authpb.AuthServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new auth client
func NewAuthClient(addr string) (*AuthClient, error) {
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to auth service: %w", err)
    }
    
    return &AuthClient{
        client: authpb.NewAuthServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *AuthClient) Close() error {
    return c.conn.Close()
}

// SetAuthToken sets the authentication token for requests
func (c *AuthClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *AuthClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Validate token
func (c *AuthClient) ValidateToken(ctx context.Context, token, orgID string) (*authpb.ValidateTokenResponse, error) {
    req := &authpb.ValidateTokenRequest{
        Token:          token,
        OrganizationId: orgID,
        CheckBlacklist: true,
    }
    
    resp, err := c.client.ValidateToken(ctx, req)
    if err != nil {
        return nil, fmt.Errorf("token validation failed: %w", err)
    }
    
    return resp, nil
}

// Refresh token
func (c *AuthClient) RefreshToken(ctx context.Context, refreshToken, orgID string) (*authpb.RefreshTokenResponse, error) {
    req := &authpb.RefreshTokenRequest{
        RefreshToken:   refreshToken,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.RefreshToken(ctx, req)
    if err != nil {
        return nil, fmt.Errorf("token refresh failed: %w", err)
    }
    
    return resp, nil
}

// Revoke token
func (c *AuthClient) RevokeToken(ctx context.Context, token, orgID string) error {
    req := &authpb.RevokeTokenRequest{
        Token:          token,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.RevokeToken(ctx, req)
    if err != nil {
        return fmt.Errorf("token revocation failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("revocation failed: %s", resp.Message)
    }
    
    return nil
}

// Get user by ID
func (c *AuthClient) GetUser(ctx context.Context, userID, orgID string) (*authpb.User, error) {
    req := &authpb.GetUserRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetUser(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get user failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.User, nil
}

// List users with pagination
func (c *AuthClient) ListUsers(ctx context.Context, orgID string, limit, offset int32) ([]*authpb.User, int32, error) {
    req := &authpb.ListUsersRequest{
        OrganizationId: orgID,
        Limit:          limit,
        Offset:         offset,
    }
    
    resp, err := c.client.ListUsers(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("list users failed: %w", err)
    }
    
    return resp.Users, resp.TotalCount, nil
}

// Update user
func (c *AuthClient) UpdateUser(ctx context.Context, userID, orgID string, name, phoneNumber, photoURL *string) (*authpb.User, error) {
    req := &authpb.UpdateUserRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    if name != nil {
        req.Name = &authpb.UpdateUserRequest_Name{Name: *name}
    }
    if phoneNumber != nil {
        req.PhoneNumber = &authpb.UpdateUserRequest_PhoneNumber{PhoneNumber: *phoneNumber}
    }
    if photoURL != nil {
        req.PhotoUrl = &authpb.UpdateUserRequest_PhotoUrl{PhotoUrl: *photoURL}
    }
    
    resp, err := c.client.UpdateUser(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update user failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("user not updated")
    }
    
    return resp.User, nil
}

// Check permission
func (c *AuthClient) CheckPermission(ctx context.Context, userID, orgID, resource, action string, contextMap map[string]string) (bool, error) {
    req := &authpb.CheckPermissionRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Resource:       resource,
        Action:         action,
        Context:        contextMap,
    }
    
    resp, err := c.client.CheckPermission(c.getContext(ctx), req)
    if err != nil {
        return false, fmt.Errorf("permission check failed: %w", err)
    }
    
    return resp.Allowed, nil
}

// Add user role
func (c *AuthClient) AddUserRole(ctx context.Context, userID, orgID, role, grantedBy string) error {
    req := &authpb.AddUserRoleRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Role:           role,
        GrantedBy:      grantedBy,
    }
    
    resp, err := c.client.AddUserRole(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("add role failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("add role failed: %s", resp.Message)
    }
    
    return nil
}

// Get user sessions
func (c *AuthClient) GetUserSessions(ctx context.Context, userID, orgID string) ([]*authpb.Session, error) {
    req := &authpb.ListSessionsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        OnlyActive:     true,
        Limit:          100,
    }
    
    resp, err := c.client.ListSessions(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("list sessions failed: %w", err)
    }
    
    return resp.Sessions, nil
}

// Revoke session
func (c *AuthClient) RevokeSession(ctx context.Context, sessionID, userID, orgID string) error {
    req := &authpb.RevokeSessionRequest{
        SessionId:      sessionID,
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.RevokeSession(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("revoke session failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("revoke failed: %s", resp.Message)
    }
    
    return nil
}

// Switch organization
func (c *AuthClient) SwitchOrganization(ctx context.Context, userID, orgID, token string) (string, error) {
    req := &authpb.SwitchOrganizationRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Token:          token,
    }
    
    resp, err := c.client.SwitchOrganization(ctx, req)
    if err != nil {
        return "", fmt.Errorf("switch organization failed: %w", err)
    }
    
    return resp.NewToken, nil
}

// Example usage
func main() {
    client, err := NewAuthClient("auth-service:50075")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    
    // Validate token
    token := "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
    validation, err := client.ValidateToken(ctx, token, "org-123")
    if err != nil {
        log.Printf("Validation error: %v", err)
    } else if validation.Valid {
        log.Printf("Token valid for user: %s", validation.Claims.Email)
        
        // Check permission
        allowed, err := client.CheckPermission(ctx,
            validation.Claims.UserId,
            "org-123",
            "trading",
            "execute",
            map[string]string{"amount": "1000"},
        )
        if err != nil {
            log.Printf("Permission check error: %v", err)
        } else if allowed {
            log.Println("User has permission to execute trades")
        } else {
            log.Println("User does not have trading permission")
        }
    } else {
        log.Printf("Invalid token: %s", validation.Error)
    }
}
TypeScript Client
typescript
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import * as path from 'path';

interface TokenClaims {
    userId: string;
    email: string;
    organizationId: string;
    roles: string[];
    permissions: string[];
    issuedAt: Date;
    expiresAt: Date;
    tokenId: string;
    customClaims: Record<string, string>;
}

interface User {
    userId: string;
    email: string;
    name: string;
    phoneNumber?: string;
    photoUrl?: string;
    emailVerified: boolean;
    phoneVerified: boolean;
    status: string;
    roles: string[];
    metadata: Record<string, string>;
    createdAt: Date;
    updatedAt: Date;
    lastLogin?: Date;
    defaultOrganizationId: string;
}

interface Session {
    sessionId: string;
    userId: string;
    ipAddress: string;
    userAgent: string;
    deviceId?: string;
    organizationId: string;
    createdAt: Date;
    lastActivity: Date;
    expiresAt: Date;
    isActive: boolean;
    metadata: Record<string, string>;
}

class AuthClient {
    private client: any;
    private token: string | null = null;
    
    constructor(serviceUrl: string) {
        const PROTO_PATH = path.join(__dirname, '../proto/auth.proto');
        const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
            keepCase: true,
            longs: String,
            enums: String,
            defaults: true,
            oneofs: true
        });
        const proto = grpc.loadPackageDefinition(packageDefinition);
        this.client = new proto.auth.v1.AuthService(
            serviceUrl,
            grpc.credentials.createInsecure()
        );
    }
    
    setAuthToken(token: string): void {
        this.token = token;
    }
    
    private getMetadata(): grpc.Metadata {
        const metadata = new grpc.Metadata();
        if (this.token) {
            metadata.set('authorization', `Bearer ${this.token}`);
        }
        return metadata;
    }
    
    async validateToken(token: string, organizationId: string): Promise<{ valid: boolean; claims?: TokenClaims; error?: string }> {
        return new Promise((resolve, reject) => {
            this.client.ValidateToken(
                { token, organization_id: organizationId, check_blacklist: true },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        valid: response.valid,
                        claims: response.claims ? {
                            userId: response.claims.user_id,
                            email: response.claims.email,
                            organizationId: response.claims.organization_id,
                            roles: response.claims.roles,
                            permissions: response.claims.permissions,
                            issuedAt: new Date(response.claims.issued_at.seconds * 1000),
                            expiresAt: new Date(response.claims.expires_at.seconds * 1000),
                            tokenId: response.claims.token_id,
                            customClaims: response.claims.custom_claims
                        } : undefined,
                        error: response.error
                    });
                }
            );
        });
    }
    
    async refreshToken(refreshToken: string, organizationId: string): Promise<{ accessToken: string; refreshToken: string; expiresAt: Date }> {
        return new Promise((resolve, reject) => {
            this.client.RefreshToken(
                { refresh_token: refreshToken, organization_id: organizationId },
                this.getMetadata(),
                (err: any, response: any) => {
                    if
if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        accessToken: response.access_token,
                        refreshToken: response.refresh_token,
                        expiresAt: new Date(response.expires_at.seconds * 1000)
                    });
                }
            );
        });
    }
    
    async revokeToken(token: string, organizationId: string): Promise<void> {
        return new Promise((resolve, reject) => {
            this.client.RevokeToken(
                { token, organization_id: organizationId },
                this.getMetadata(),
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
    
    async getUser(userId: string, organizationId: string): Promise<User | null> {
        return new Promise((resolve, reject) => {
            this.client.GetUser(
                { user_id: userId, organization_id: organizationId },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.found) {
                        resolve(null);
                        return;
                    }
                    
                    const user = response.user;
                    resolve({
                        userId: user.user_id,
                        email: user.email,
                        name: user.name,
                        phoneNumber: user.phone_number,
                        photoUrl: user.photo_url,
                        emailVerified: user.email_verified,
                        phoneVerified: user.phone_verified,
                        status: user.status,
                        roles: user.roles,
                        metadata: user.metadata,
                        createdAt: new Date(user.created_at.seconds * 1000),
                        updatedAt: new Date(user.updated_at.seconds * 1000),
                        lastLogin: user.last_login ? new Date(user.last_login.seconds * 1000) : undefined,
                        defaultOrganizationId: user.default_organization_id
                    });
                }
            );
        });
    }
    
    async listUsers(organizationId: string, options?: { limit?: number; offset?: number; role?: string; status?: string; search?: string }): Promise<{ users: User[]; totalCount: number; hasMore: boolean }> {
        return new Promise((resolve, reject) => {
            this.client.ListUsers(
                {
                    organization_id: organizationId,
                    limit: options?.limit || 100,
                    offset: options?.offset || 0,
                    role_filter: options?.role,
                    status_filter: options?.status,
                    search: options?.search
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    const users = response.users.map((user: any) => ({
                        userId: user.user_id,
                        email: user.email,
                        name: user.name,
                        phoneNumber: user.phone_number,
                        photoUrl: user.photo_url,
                        emailVerified: user.email_verified,
                        phoneVerified: user.phone_verified,
                        status: user.status,
                        roles: user.roles,
                        metadata: user.metadata,
                        createdAt: new Date(user.created_at.seconds * 1000),
                        updatedAt: new Date(user.updated_at.seconds * 1000),
                        lastLogin: user.last_login ? new Date(user.last_login.seconds * 1000) : undefined,
                        defaultOrganizationId: user.default_organization_id
                    }));
                    
                    resolve({
                        users,
                        totalCount: response.total_count,
                        hasMore: response.has_more
                    });
                }
            );
        });
    }
    
    async checkPermission(userId: string, organizationId: string, resource: string, action: string, context?: Record<string, string>): Promise<boolean> {
        return new Promise((resolve, reject) => {
            this.client.CheckPermission(
                {
                    user_id: userId,
                    organization_id: organizationId,
                    resource,
                    action,
                    context: context || {}
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve(response.allowed);
                }
            );
        });
    }
    
    async addUserRole(userId: string, organizationId: string, role: string, grantedBy: string): Promise<void> {
        return new Promise((resolve, reject) => {
            this.client.AddUserRole(
                {
                    user_id: userId,
                    organization_id: organizationId,
                    role,
                    granted_by: grantedBy
                },
                this.getMetadata(),
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
    
    async getUserSessions(userId: string, organizationId: string): Promise<Session[]> {
        return new Promise((resolve, reject) => {
            this.client.ListSessions(
                {
                    user_id: userId,
                    organization_id: organizationId,
                    only_active: true,
                    limit: 100
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    const sessions = response.sessions.map((session: any) => ({
                        sessionId: session.session_id,
                        userId: session.user_id,
                        ipAddress: session.ip_address,
                        userAgent: session.user_agent,
                        deviceId: session.device_id,
                        organizationId: session.organization_id,
                        createdAt: new Date(session.created_at.seconds * 1000),
                        lastActivity: new Date(session.last_activity.seconds * 1000),
                        expiresAt: new Date(session.expires_at.seconds * 1000),
                        isActive: session.is_active,
                        metadata: session.metadata
                    }));
                    
                    resolve(sessions);
                }
            );
        });
    }
    
    async revokeSession(sessionId: string, userId: string, organizationId: string): Promise<void> {
        return new Promise((resolve, reject) => {
            this.client.RevokeSession(
                {
                    session_id: sessionId,
                    user_id: userId,
                    organization_id: organizationId
                },
                this.getMetadata(),
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
    
    async switchOrganization(userId: string, organizationId: string, token: string): Promise<string> {
        return new Promise((resolve, reject) => {
            this.client.SwitchOrganization(
                {
                    user_id: userId,
                    organization_id: organizationId,
                    token
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve(response.new_token);
                }
            );
        });
    }
}

// React hook for authentication
import { useEffect, useState } from 'react';

function useAuth(organizationId: string) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [permissions, setPermissions] = useState<string[]>([]);
    
    const client = new AuthClient(process.env.REACT_APP_AUTH_SERVICE_URL!);
    
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            setLoading(false);
            return;
        }
        
        client.setAuthToken(token);
        
        client.validateToken(token, organizationId)
            .then(async (result) => {
                if (result.valid && result.claims) {
                    const userData = await client.getUser(result.claims.userId, organizationId);
                    setUser(userData);
                    setPermissions(result.claims.permissions);
                } else {
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                }
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, [organizationId]);
    
    const hasPermission = (resource: string, action: string): boolean => {
        return permissions.some(perm => {
            const [permResource, permAction] = perm.split(':');
            return permResource === resource && (permAction === action || permAction === '*');
        });
    };
    
    const logout = async () => {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                await client.revokeToken(token, organizationId);
            } catch (err) {
                console.error('Failed to revoke token:', err);
            }
        }
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        setPermissions([]);
    };
    
    return { user, loading, error, permissions, hasPermission, logout };
}

// Protected route component
function ProtectedRoute({ children, requiredPermission }: { children: React.ReactNode; requiredPermission?: { resource: string; action: string } }) {
    const { user, loading, hasPermission } = useAuth(process.env.REACT_APP_ORG_ID!);
    
    if (loading) {
        return <div>Loading...</div>;
    }
    
    if (!user) {
        return <div>Please log in</div>;
    }
    
    if (requiredPermission && !hasPermission(requiredPermission.resource, requiredPermission.action)) {
        return <div>Access denied</div>;
    }
    
    return <>{children}</>;
}

export { AuthClient, useAuth, ProtectedRoute };
Package.json for TypeScript Project
json
{
  "name": "auth-proto",
  "version": "1.0.0",
  "description": "Auth service protobuf definitions and clients",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "npm run proto && tsc",
    "proto": "./bin/build.sh",
    "test": "jest",
    "lint": "eslint src/**/*.ts",
    "clean": "rm -rf dist client/typescript/*.ts",
    "pre-commit": "npm run lint && npm run test && npm run proto"
  },
  "dependencies": {
    "@grpc/grpc-js": "^1.10.0",
    "@grpc/proto-loader": "^0.7.0",
    "google-protobuf": "^3.21.2"
  },
  "devDependencies": {
    "@types/jest": "^29.5.0",
    "@types/node": "^20.0.0",
    "@typescript-eslint/eslint-plugin": "^6.19.0",
    "@typescript-eslint/parser": "^6.19.0",
    "eslint": "^8.56.0",
    "jest": "^29.7.0",
    "protoc-gen-ts": "^0.8.6",
    "ts-jest": "^29.1.0",
    "typescript": "^5.3.3"
  }
}
tsconfig.json
json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020", "DOM"],
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "client"]
}
Docker Compose Example
yaml
version: '3.8'

services:
  auth-service:
    image: sologenic/auth-service:latest
    environment:
      - AUTH_SERVICE_PORT=50075
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - USER_STORE=user-store:50049
      - ORGANIZATION_STORE=organization-store:50062
      - JWT_SECRET=${JWT_SECRET}
      - TOKEN_EXPIRY=3600
      - REFRESH_TOKEN_EXPIRY=86400
      - LOG_LEVEL=info
    ports:
      - "50075:50075"
    networks:
      - internal
    depends_on:
      - redis
      - user-store
      - organization-store
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50075"]
      interval: 30s
      timeout: 10s
      retries: 3

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

  user-store:
    image: sologenic/user-store:latest
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=users
      - DB_USER=user_store
      - DB_PASSWORD=${DB_PASSWORD}
    networks:
      - internal
    depends_on:
      - postgres

  organization-store:
    image: sologenic/organization-store:latest
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=organizations
      - DB_USER=org_store
      - DB_PASSWORD=${DB_PASSWORD}
    networks:
      - internal
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=auth
      - POSTGRES_USER=auth_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal

networks:
  internal:
    driver: bridge

volumes:
  redis_data:
  postgres_data:
Git Ignore
Create .gitignore:

gitignore
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out

# Go workspace
go.work
go.work.sum

# Generated files
*.pb.go
*_grpc.pb.go
*.pb.cc
*.pb.h

# TypeScript
node_modules/
dist/
*.tsbuildinfo

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Build artifacts
build/
bin/
Best Practices
Development Workflow
Update proto file - Make changes to auth.proto

Run build script - ./bin/build.sh or make proto

Commit changes - Pre-commit hook will auto-generate files

Update clients - Regenerate client code if needed

Version Control
Always commit generated .pb.go files

Commit TypeScript generated files

Don't commit node_modules/

Don't commit build artifacts

Testing
go
// Example test for auth client
func TestValidateToken(t *testing.T) {
    client, err := NewAuthClient("localhost:50075")
    assert.NoError(t, err)
    defer client.Close()
    
    ctx := context.Background()
    resp, err := client.ValidateToken(ctx, "test-token", "test-org")
    assert.NoError(t, err)
    assert.NotNil(t, resp)
}
Troubleshooting
Issue	Possible Cause	Solution
Build fails	Missing protoc	Install protoc compiler
Go files not generated	Wrong proto path	Check PROTO_FILE variable
TypeScript not generated	Missing package.json	Create package.json file
Pre-commit hook not running	Hook not installed	Run pre-commit install
Generated files not committed	Git ignore pattern	Check .gitignore rules
Import errors	Wrong module path	Verify Go module name
License
This documentation is part of the TX Marketplace platform.
