# Firebase Auth Service

The Firebase Auth Service provides functionality to interact with the Google Firebase authentication API. It handles token validation, user signout, and administrative user session management.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Firebase Auth Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Functions │ │
│ ├───────────────────┬───────────────────┬─────────────────────────────┤ │
│ │ ValidateToken │ Signout │ SignoutUserByEmail │ │
│ │ (Token validation)│ (Token-based) │ (Email-based admin) │ │
│ └───────────────────┴───────────────────┴─────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Integration Layer │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • HTTP Server (RESTful endpoints) │ │
│ │ • gRPC Server (Internal communication) │ │
│ │ • Organization Store (Tenant isolation) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ External Systems │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Google Firebase Authentication API │ │
│ │ • Firebase Admin SDK │ │
│ │ • User Session Store │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Integration with HTTP Server

The Firebase Auth Service is integrated into the HTTP server such that day-to-day development is the same as with any other auth service. Authentication is handled automatically by the middleware.

### Authorization Header Format

All authenticated requests must include the `Authorization` header with a Firebase token prepended by `Bearer:` (note the colon after Bearer).

```bash
Authorization: Bearer: eyJhbGciOiJSUzI1NiIsImtpZCI6...
Important: The format is Bearer: (with colon), not Bearer (with space).

Example Authenticated Request
bash
curl -X POST "https://api.sologenic.org/api/somecall" \
    -H "Network: devnet" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIsImtpZCI6..."
Core Functions
ValidateToken
Validates a Firebase token and returns the user ID (email address) if the user is authenticated.

Function Signature
text
ValidateToken(token string) (userID string, err error)
Parameters
Parameter	Type	Description
token	string	Firebase token prepended with "Bearer:"
Returns
Return	Type	Description
userID	string	User's email address (Firebase UID)
err	error	Error if validation fails
Token Validation Process
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Token Validation Flow                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Request with Authorization Header                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Authorization: Bearer: eyJhbGciOiJSUzI1NiIs...                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Extract Token                                                     │   │
│  │    • Remove "Bearer:" prefix                                         │   │
│  │    • Validate token format                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Verify with Firebase                                              │   │
│  │    • Check token signature                                           │   │
│  │    • Verify expiration (not expired)                                 │   │
│  │    • Check audience and issuer                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │                               │                       │
│                    ▼                               ▼                       │
│           ┌──────────────┐                ┌──────────────┐                │
│           │ Valid Token  │                │ Invalid Token│                │
│           │ Return UserID│                │ Return Error │                │
│           └──────────────┘                └──────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Validation Rules
Rule	Description
Signature	Token must be signed by Firebase private key
Expiration	Token must not be expired
Audience	Token audience must match Firebase project ID
Issuer	Token issuer must be https://securetoken.google.com/{projectId}
Format	Must be valid JWT format
Example Usage (Internal)
go
// Within HTTP middleware
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        authHeader := r.Header.Get("Authorization")
        if authHeader == "" {
            http.Error(w, "Missing authorization header", http.StatusUnauthorized)
            return
        }
        
        userID, err := authService.ValidateToken(authHeader)
        if err != nil {
            http.Error(w, "Invalid token", http.StatusUnauthorized)
            return
        }
        
        // Add user ID to context for downstream handlers
        ctx := context.WithValue(r.Context(), "userID", userID)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
Signout
Signs out a user by invalidating their Firebase token.

Function Signature
text
Signout(token string) error
Parameters
Parameter	Type	Description
token	string	Firebase token prepended with "Bearer:"
Returns
Return	Type	Description
err	error	Error if signout fails
Signout Process
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Signout Flow                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Request: POST /api/logout                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Authorization: Bearer: eyJhbGciOiJSUzI1NiIs...                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Extract and Validate Token                                        │   │
│  │    • Verify token is valid                                           │   │
│  │    • Extract user ID                                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Revoke Token                                                      │   │
│  │    • Invalidate token in Firebase                                    │   │
│  │    • Clear server-side session                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. Return Response                                                   │   │
│  │    • 200 OK on success                                               │   │
│  │    • 401 Unauthorized on failure                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Example Usage
go
// Logout handler
func logoutHandler(w http.ResponseWriter, r *http.Request) {
    authHeader := r.Header.Get("Authorization")
    if authHeader == "" {
        http.Error(w, "Missing authorization header", http.StatusUnauthorized)
        return
    }
    
    err := authService.Signout(authHeader)
    if err != nil {
        http.Error(w, "Failed to sign out", http.StatusInternalServerError)
        return
    }
    
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{
        "message": "Successfully signed out",
    })
}
SignoutUserByEmail
Signs out a user by their email address. This method is used when a token is not available or for administrative forced signouts.

Function Signature
text
SignoutUserByEmail(email string) error
Parameters
Parameter	Type	Description
email	string	User's email address (Firebase UID)
Returns
Return	Type	Description
err	error	Error if signout fails
Use Cases
Use Case	Description
Admin Force Signout	Administrator can sign out a malicious user
Maintenance	Sign out all users during system maintenance
Security Breach	Immediately revoke access for compromised accounts
Account Deletion	Sign out user before deleting account
Suspension	Force sign out suspended users
Admin Force Signout Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Admin Force Signout Flow                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Admin Action: Force signout user@example.com                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Internal Service Call                                                │   │
│  │ SignoutUserByEmail("user@example.com")                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Validate Email                                                    │   │
│  │    • Check email format                                              │   │
│  │    • Verify user exists in Firebase                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Revoke All User Sessions                                         │   │
│  │    • Invalidate all tokens for user                                  │   │
│  │    • Clear all active sessions                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. Result                                                            │   │
│  │    • User is immediately signed out                                  │   │
│  │    • Subsequent requests with old tokens fail                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Example Usage (Admin)
go
// Admin endpoint to force signout a user
func adminForceSignoutHandler(w http.ResponseWriter, r *http.Request) {
    // Verify admin permissions first
    if !isAdmin(r) {
        http.Error(w, "Forbidden", http.StatusForbidden)
        return
    }
    
    var req struct {
        Email string `json:"email"`
    }
    
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }
    
    err := authService.SignoutUserByEmail(req.Email)
    if err != nil {
        http.Error(w, "Failed to sign out user", http.StatusInternalServerError)
        return
    }
    
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{
        "message": "User successfully signed out",
        "email": req.Email,
    })
}
Bulk Signout Example
go
// Sign out all users in an organization
func signoutOrganizationUsers(orgID string, authService AuthService, userStore UserStore) error {
    users, err := userStore.GetUsersByOrganization(orgID)
    if err != nil {
        return err
    }
    
    for _, user := range users {
        if err := authService.SignoutUserByEmail(user.Email); err != nil {
            // Log error but continue with other users
            log.Printf("Failed to sign out user %s: %v", user.Email, err)
        }
    }
    
    return nil
}
HTTP Integration Examples
Protected Endpoint with Auth Middleware
go
package main

import (
    "net/http"
    "github.com/sologenic/com-fs-auth-firebase-service"
)

func main() {
    // Initialize auth service
    authService := firebase.NewAuthService()
    
    // Create HTTP server with auth middleware
    mux := http.NewServeMux()
    
    // Protected endpoints
    mux.HandleFunc("/api/user/profile", authMiddleware(authService, profileHandler))
    mux.HandleFunc("/api/user/settings", authMiddleware(authService, settingsHandler))
    mux.HandleFunc("/api/logout", logoutHandler(authService))
    
    // Admin endpoints (with additional admin check)
    mux.HandleFunc("/api/admin/signout", adminAuthMiddleware(authService, adminForceSignoutHandler))
    
    http.ListenAndServe(":8080", mux)
}

func authMiddleware(authService AuthService, next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        authHeader := r.Header.Get("Authorization")
        if authHeader == "" {
            http.Error(w, "Missing authorization header", http.StatusUnauthorized)
            return
        }
        
        userID, err := authService.ValidateToken(authHeader)
        if err != nil {
            http.Error(w, "Invalid or expired token", http.StatusUnauthorized)
            return
        }
        
        // Add user ID to request context
        ctx := context.WithValue(r.Context(), "userID", userID)
        next.ServeHTTP(w, r.WithContext(ctx))
    }
}
Client-Side Token Management
javascript
// Firebase client-side token management
import { getAuth, signInWithEmailAndPassword, signOut } from "firebase/auth";

// Login and get token
async function login(email, password) {
    const auth = getAuth();
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const token = await userCredential.user.getIdToken();
    
    // Store token for API calls
    localStorage.setItem('firebaseToken', token);
    return token;
}

// Make authenticated API call
async function apiCall(endpoint, data) {
    const token = localStorage.getItem('firebaseToken');
    const response = await fetch(`https://api.sologenic.org${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer: ${token}`,
            'Network': 'mainnet'
        },
        body: JSON.stringify(data)
    });
    
    if (response.status === 401) {
        // Token expired, refresh and retry
        const auth = getAuth();
        const newToken = await auth.currentUser.getIdToken(true);
        localStorage.setItem('firebaseToken', newToken);
        return apiCall(endpoint, data); // Retry with new token
    }
    
    return response.json();
}

// Logout
async function logout() {
    const auth = getAuth();
    await signOut(auth);
    localStorage.removeItem('firebaseToken');
    
    // Also call backend signout
    await fetch('https://api.sologenic.org/api/logout', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer: ${localStorage.getItem('firebaseToken')}`
        }
    });
}
Testing
Test Program
There is a test program to test the service. The test program is a simple gRPC client that sends a token to the service and expects a response.

Running the Test
bash
# Build the test client
go build -o auth-test-client ./test/client

# Run with token from Firebase console
./auth-test-client --token="eyJhbGciOiJSUzI1NiIsImtpZCI6..."
Test Client Example
go
package main

import (
    "context"
    "flag"
    "log"
    "time"
    
    "google.golang.org/grpc"
    pb "github.com/sologenic/com-fs-auth-firebase-service/proto"
)

func main() {
    token := flag.String("token", "", "Firebase token to test")
    serverAddr := flag.String("addr", "localhost:50051", "gRPC server address")
    flag.Parse()
    
    if *token == "" {
        log.Fatal("Token is required")
    }
    
    conn, err := grpc.Dial(*serverAddr, grpc.WithInsecure())
    if err != nil {
        log.Fatalf("Failed to connect: %v", err)
    }
    defer conn.Close()
    
    client := pb.NewAuthServiceClient(conn)
    
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    // Test ValidateToken
    resp, err := client.ValidateToken(ctx, &pb.ValidateTokenRequest{
        Token: *token,
    })
    if err != nil {
        log.Fatalf("ValidateToken failed: %v", err)
    }
    
    log.Printf("Token valid! User ID: %s", resp.UserId)
}
Obtaining Test Token
To obtain a test token from Firebase Console:

Open Firebase Console

Go to Authentication → Users

Find the test user

In browser console (F12), run:

javascript
firebase.auth().currentUser.getIdToken().then(token => console.log(token))
Copy the token for testing

Start Parameters
Required Environment Variables
Environment Variable	Description	Source
GRPC_PORT	Port the service listens on for gRPC requests	Configuration
FIREBASE_CONFIG	Path to JSON file with Firebase Admin SDK credentials	Firebase Console
EXPIRE	Expiry time in days for the token	Configuration
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-model
Environment Variable Details
GRPC_PORT
The port on which the gRPC server listens for internal requests.

bash
GRPC_PORT=50051
FIREBASE_CONFIG
Points to a secret JSON file with the Firebase Admin SDK authentication token. Download this from Firebase Console:

Go to Firebase Console → Project Settings → Service Accounts

Click "Generate New Private Key"

Save the JSON file securely

Set FIREBASE_CONFIG to the path of this file

bash
FIREBASE_CONFIG=/etc/secrets/firebase-admin-sdk.json
Example Firebase Admin SDK JSON structure:

json
{
  "type": "service_account",
  "project_id": "sologenic-platform",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk@sologenic-platform.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
EXPIRE
Expiry time in days for the token. This controls how long a token remains valid before requiring refresh.

bash
EXPIRE=7  # 7 days
ORGANIZATION_STORE
The organization service endpoint for tenant isolation.

bash
ORGANIZATION_STORE=localhost:50060
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
ENABLE_GRPC_REFLECTION	Enable gRPC reflection for debugging	false
TOKEN_REFRESH_THRESHOLD	Hours before expiry to auto-refresh	24
Complete Environment Configuration Example
bash
# Required
GRPC_PORT=50051
FIREBASE_CONFIG=/etc/secrets/firebase-admin-sdk.json
EXPIRE=7
ORGANIZATION_STORE=localhost:50060

# Optional
LOG_LEVEL=debug
ENABLE_GRPC_REFLECTION=true
TOKEN_REFRESH_THRESHOLD=24

# HTTP Server Configuration (if serving HTTP)
HTTP_CONFIG='{
  "port": ":8080",
  "cors": {
    "allowedOrigins": ["http://localhost:3000", "https://app.sologenic.org"]
  },
  "timeouts": {
    "read": "10s",
    "write": "10s",
    "idle": "10s",
    "shutdown": "10s"
  }
}'
Docker Environment Example
dockerfile
# Dockerfile
FROM golang:1.21-alpine

ENV GRPC_PORT=50051
ENV FIREBASE_CONFIG=/app/secrets/firebase.json
ENV EXPIRE=7
ENV ORGANIZATION_STORE=organization-service:50060
ENV LOG_LEVEL=info

COPY --chown=nonroot:nonroot ./secrets/firebase.json /app/secrets/firebase.json
COPY ./bin/auth-service /app/

EXPOSE 50051

USER nonroot
ENTRYPOINT ["/app/auth-service"]
Kubernetes Deployment Example
yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: auth-service
        image: sologenic/auth-service:latest
        env:
        - name: GRPC_PORT
          value: "50051"
        - name: EXPIRE
          value: "7"
        - name: ORGANIZATION_STORE
          value: "organization-service:50060"
        - name: LOG_LEVEL
          value: "info"
        envFrom:
        - secretRef:
            name: firebase-config
        ports:
        - containerPort: 50051
          name: grpc
---
apiVersion: v1
kind: Secret
metadata:
  name: firebase-config
type: Opaque
stringData:
  FIREBASE_CONFIG: /etc/secrets/firebase.json
  # Mounted via volume from secret
Error Responses
Invalid Token Format
json
{
  "error": "invalid_token_format",
  "message": "Authorization header must start with 'Bearer:'",
  "status_code": 401
}
Token Expired
json
{
  "error": "token_expired",
  "message": "Firebase token has expired",
  "expires_at": "2024-12-01T00:00:00Z",
  "status_code": 401
}
Invalid Signature
json
{
  "error": "invalid_signature",
  "message": "Token signature verification failed",
  "status_code": 401
}
User Not Found (SignoutUserByEmail)
json
{
  "error": "user_not_found",
  "message": "No user found with email: user@example.com",
  "status_code": 404
}
Firebase Configuration Error
json
{
  "error": "configuration_error",
  "message": "Firebase Admin SDK not properly configured",
  "status_code": 500
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Token validation fails	Wrong header format	Use Bearer: with colon, not space
Token expired	Token lifetime exceeded	Refresh token client-side
Invalid signature	Wrong Firebase project	Verify token from correct project
Signout doesn't work	Token already invalid	Use SignoutUserByEmail as fallback
Admin SDK error	Missing or invalid credentials	Download fresh Firebase service account JSON
Organization isolation fails	ORGANIZATION_STORE not configured	Set ORGANIZATION_STORE environment variable
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Test token validation manually:

bash
# Using grpcurl
grpcurl -plaintext -d '{"token":"Bearer: eyJhbGci..."}' \
  localhost:50051 auth.AuthService/ValidateToken
Check Firebase Admin SDK connectivity:

go
import "firebase.google.com/go"

func checkFirebaseConnection() error {
    app, err := firebase.NewApp(context.Background(), nil)
    if err != nil {
        return fmt.Errorf("failed to initialize Firebase app: %v", err)
    }
    
    client, err := app.Auth(context.Background())
    if err != nil {
        return fmt.Errorf("failed to get Auth client: %v", err)
    }
    
    // Try to get a user to verify connectivity
    _, err = client.GetUser(context.Background(), "test@example.com")
    if err != nil {
        return fmt.Errorf("Firebase connection test failed: %v", err)
    }
    
    return nil
}
Best Practices
Security
Use HTTPS Always: Never send tokens over HTTP in production

Short Token Lifetimes: Use reasonable expiration (7 days or less)

Rotate Service Account Keys: Regularly rotate Firebase Admin SDK keys

Audit Signouts: Log all admin force signout actions

Validate Organization: Always verify organization isolation

Token Management
Auto-Refresh: Implement automatic token refresh before expiry

Store Securely: Never store tokens in localStorage for sensitive apps (use httpOnly cookies)

Revoke on Logout: Always call backend Signout on user logout

Handle 401 Gracefully: Redirect to login on authentication failure

Performance
Scenario	Recommendation
High traffic	Increase gRPC server instances
Token validation	Cache validation results briefly (seconds)
Batch operations	Use SignoutUserByEmail for bulk operations
Integration Tips
Middleware Pattern: Use auth middleware for all protected routes

Context Propagation: Pass user ID through request context

Fallback Signout: Use SignoutUserByEmail when token is unavailable

Monitoring: Monitor token validation failure rates

Related Services
Service	Description
Organization Service	Tenant isolation and organization validation
Admin Account Service	User role and permission management
User Service	User profile management
License
This documentation is part of the TX Marketplace platform.
