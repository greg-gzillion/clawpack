package user

import (
    "context"
    "fmt"
    "log"
    "os"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/metadata"
    
    userpb "github.com/sologenic/user/client/go"
    "google.golang.org/protobuf/types/known/timestamppb"
)

type UserClient struct {
    client      userpb.UserServiceClient
    adminClient userpb.AdminUserServiceClient
    conn        *grpc.ClientConn
    token       string
}

// Create new user client
func NewUserClient(addr string) (*UserClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("USER_STORE_TESTING"); testingMode == "TRUE" {
            return &UserClient{}, nil
        }
        return nil, fmt.Errorf("USER_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to user service: %w", err)
    }
    
    return &UserClient{
        client:      userpb.NewUserServiceClient(conn),
        adminClient: userpb.NewAdminUserServiceClient(conn),
        conn:        conn,
    }, nil
}

func (c *UserClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *UserClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *UserClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Create a new user
func (c *UserClient) CreateUser(ctx context.Context, userDetails *userpb.UserDetails, password, orgID string, sendWelcomeEmail bool) (*userpb.User, error) {
    if c.client == nil {
        return mockUser(userDetails), nil
    }
    
    req := &userpb.CreateUserRequest{
        User:             userDetails,
        Password:         password,
        OrganizationId:   orgID,
        SendWelcomeEmail: sendWelcomeEmail,
    }
    
    resp, err := c.client.CreateUser(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create user failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("user creation failed: %s", resp.Message)
    }
    
    return resp.User, nil
}

// Get user by ID
func (c *UserClient) GetUser(ctx context.Context, userID, orgID string, includeKYC, includeFunding bool) (*userpb.User, error) {
    if c.client == nil {
        return mockUserByID(userID), nil
    }
    
    req := &userpb.GetUserRequest{
        UserId:         userID,
        OrganizationId: orgID,
        IncludeKyc:     includeKYC,
        IncludeFunding: includeFunding,
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

// Get user by email
func (c *UserClient) GetUserByEmail(ctx context.Context, email, orgID string) (*userpb.User, error) {
    if c.client == nil {
        return mockUserByEmail(email), nil
    }
    
    req := &userpb.GetUserByEmailRequest{
        Email:          email,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetUserByEmail(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get user by email failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.User, nil
}

// Update user
func (c *UserClient) UpdateUser(ctx context.Context, userID, orgID string, email, phoneNumber, firstName, lastName *string, address *userpb.Address, preferences *userpb.UserPreferences, metadata map[string]string, updateReason string) (*userpb.User, bool, error) {
    if c.client == nil {
        return mockUserUpdate(userID), false, nil
    }
    
    req := &userpb.UpdateUserRequest{
        UserId:         userID,
        OrganizationId: orgID,
        UpdateReason:   updateReason,
        Metadata:       metadata,
    }
    
    if email != nil {
        req.Email = &userpb.UpdateUserRequest_Email{Email: *email}
    }
    if phoneNumber != nil {
        req.PhoneNumber = &userpb.UpdateUserRequest_PhoneNumber{PhoneNumber: *phoneNumber}
    }
    if firstName != nil {
        req.FirstName = &userpb.UpdateUserRequest_FirstName{FirstName: *firstName}
    }
    if lastName != nil {
        req.LastName = &userpb.UpdateUserRequest_LastName{LastName: *lastName}
    }
    if address != nil {
        req.PrimaryAddress = address
    }
    if preferences != nil {
        req.Preferences = preferences
    }
    
    resp, err := c.client.UpdateUser(c.getContext(ctx), req)
    if err != nil {
        return nil, false, fmt.Errorf("update user failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, false, fmt.Errorf("user update failed: %s", resp.Message)
    }
    
    return resp.User, resp.RequiresReview, nil
}

// Submit KYC
func (c *UserClient) SubmitKYC(ctx context.Context, userID, orgID string, kycDetails *userpb.KYCDetails) (string, userpb.KYCStatus, error) {
    if c.client == nil {
        return "mock-kyc-id", userpb.KYCStatus_PENDING, nil
    }
    
    req := &userpb.SubmitKYCRequest{
        UserId:         userID,
        OrganizationId: orgID,
        KycDetails:     kycDetails,
    }
    
    resp, err := c.client.SubmitKYC(c.getContext(ctx), req)
    if err != nil {
        return "", userpb.KYC_STATUS_UNSPECIFIED, fmt.Errorf("submit KYC failed: %w", err)
    }
    
    if !resp.Submitted {
        return "", userpb.KYC_STATUS_UNSPECIFIED, fmt.Errorf("KYC submission failed: %s", resp.Message)
    }
    
    return resp.KycId, resp.Status, nil
}

// Get KYC status
func (c *UserClient) GetKYCStatus(ctx context.Context, userID, orgID string) (*userpb.KYCStatus, *userpb.KYCLevel, *userpb.KYCDetails, error) {
    if c.client == nil {
        status := userpb.KYCStatus_VERIFIED
        level := userpb.KYCLevel_LEVEL_2
        return &status, &level, nil, nil
    }
    
    req := &userpb.GetKYCStatusRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetKYCStatus(c.getContext(ctx), req)
    if err != nil {
        return nil, nil, nil, fmt.Errorf("get KYC status failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil, nil, nil
    }
    
    return &resp.Status, &resp.Level, resp.Details, nil
}

// Add wallet
func (c *UserClient) AddWallet(ctx context.Context, userID, orgID string, wallet *userpb.Wallet) (*userpb.Wallet, error) {
    if c.client == nil {
        return wallet, nil
    }
    
    req := &userpb.AddWalletRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Wallet:         wallet,
    }
    
    resp, err := c.client.AddWallet(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("add wallet failed: %w", err)
    }
    
    if !resp.Added {
        return nil, fmt.Errorf("wallet addition failed")
    }
    
    return resp.Wallet, nil
}

// Get wallets
func (c *UserClient) GetWallets(ctx context.Context, userID, orgID string) ([]*userpb.Wallet, error) {
    if c.client == nil {
        return []*userpb.Wallet{mockWallet()}, nil
    }
    
    req := &userpb.GetWalletsRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetWallets(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get wallets failed: %w", err)
    }
    
    return resp.Wallets, nil
}

// Add bank account
func (c *UserClient) AddBankAccount(ctx context.Context, userID, orgID string, bankAccount *userpb.BankAccount) (*userpb.BankAccount, bool, error) {
    if c.client == nil {
        return bankAccount, true, nil
    }
    
    req := &userpb.AddBankAccountRequest{
        UserId:       userID,
        OrganizationId: orgID,
        BankAccount:  bankAccount,
    }
    
    resp, err := c.client.AddBankAccount(c.getContext(ctx), req)
    if err != nil {
        return nil, false, fmt.Errorf("add bank account failed: %w", err)
    }
    
    if !resp.Added {
        return nil, false, fmt.Errorf("bank account addition failed")
    }
    
    return resp.BankAccount, resp.RequiresVerification, nil
}

// Get compliance questions
func (c *UserClient) GetComplianceQuestions(ctx context.Context, orgID, jurisdiction string) ([]*userpb.ComplianceQuestion, error) {
    if c.client == nil {
        return []*userpb.ComplianceQuestion{}, nil
    }
    
    req := &userpb.GetComplianceQuestionsRequest{
        OrganizationId: orgID,
        Jurisdiction:   jurisdiction,
    }
    
    resp, err := c.client.GetComplianceQuestions(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get compliance questions failed: %w", err)
    }
    
    return resp.Questions, nil
}

// Submit compliance answers
func (c *UserClient) SubmitComplianceAnswers(ctx context.Context, userID, orgID string, answers []*userpb.ComplianceAnswer) (bool, bool, error) {
    if c.client == nil {
        return true, false, nil
    }
    
    req := &userpb.SubmitComplianceAnswersRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Answers:        answers,
    }
    
    resp, err := c.client.SubmitComplianceAnswers(c.getContext(ctx), req)
    if err != nil {
        return false, false, fmt.Errorf("submit compliance answers failed: %w", err)
    }
    
    if !resp.Submitted {
        return false, false, fmt.Errorf("compliance submission failed: %s", resp.Message)
    }
    
    return resp.Submitted, resp.RequiresReview, nil
}

// Upload document
func (c *UserClient) UploadDocument(ctx context.Context, userID, orgID, documentType, documentName string, content []byte, contentType string) (string, error) {
    if c.client == nil {
        return "mock-doc-id", nil
    }
    
    req := &userpb.UploadDocumentRequest{
        UserId:         userID,
        OrganizationId: orgID,
        DocumentType:   documentType,
        DocumentName:   documentName,
        DocumentContent: content,
        ContentType:    contentType,
    }
    
    resp, err := c.client.UploadDocument(c.getContext(ctx), req)
    if err != nil {
        return "", fmt.Errorf("upload document failed: %w", err)
    }
    
    if !resp.Uploaded {
        return "", fmt.Errorf("document upload failed")
    }
    
    return resp.DocumentId, nil
}

// Sign document
func (c *UserClient) SignDocument(ctx context.Context, userID, orgID, documentID, signature, ipAddress, userAgent string) (time.Time, error) {
    if c.client == nil {
        return time.Now(), nil
    }
    
    req := &userpb.SignDocumentRequest{
        UserId:         userID,
        OrganizationId: orgID,
        DocumentId:     documentID,
        Signature:      signature,
        IpAddress:      ipAddress,
        UserAgent:      userAgent,
    }
    
    resp, err := c.client.SignDocument(c.getContext(ctx), req)
    if err != nil {
        return time.Time{}, fmt.Errorf("sign document failed: %w", err)
    }
    
    if !resp.Signed {
        return time.Time{}, fmt.Errorf("document signing failed: %s", resp.Message)
    }
    
    return resp.SignedAt.AsTime(), nil
}

// Clone user to another organization
func (c *UserClient) CloneUserToOrganization(ctx context.Context, userID, sourceOrgID, targetOrgID string, config *userpb.CloneConfiguration) (*userpb.User, bool, error) {
    if c.client == nil {
        return mockUserClone(userID), false, nil
    }
    
    req := &userpb.CloneUserToOrganizationRequest{
        UserId:               userID,
        SourceOrganizationId: sourceOrgID,
        TargetOrganizationId: targetOrgID,
        Config:               config,
    }
    
    resp, err := c.client.CloneUserToOrganization(c.getContext(ctx), req)
    if err != nil {
        return nil, false, fmt.Errorf("clone user failed: %w", err)
    }
    
    if !resp.Cloned {
        return nil, false, fmt.Errorf("user clone failed: %s", resp.Message)
    }
    
    return resp.User, resp.RequiresReview, nil
}

// Get user's organizations
func (c *UserClient) GetUserOrganizations(ctx context.Context, userID string) ([]*userpb.OrganizationInfo, error) {
    if c.client == nil {
        return []*userpb.OrganizationInfo{mockOrgInfo()}, nil
    }
    
    req := &userpb.GetUserOrganizationsRequest{
        UserId: userID,
    }
    
    resp, err := c.client.GetUserOrganizations(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get user organizations failed: %w", err)
    }
    
    return resp.Organizations, nil
}

// Switch organization
func (c *UserClient) SwitchOrganization(ctx context.Context, userID, currentOrgID, targetOrgID string) (*userpb.User, error) {
    if c.client == nil {
        return mockUserSwitch(userID, targetOrgID), nil
    }
    
    req := &userpb.SwitchOrganizationRequest{
        UserId:                 userID,
        CurrentOrganizationId:  currentOrgID,
        TargetOrganizationId:   targetOrgID,
    }
    
    resp, err := c.client.SwitchOrganization(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("switch organization failed: %w", err)
    }
    
    if !resp.Switched {
        return nil, fmt.Errorf("organization switch failed: %s", resp.Message)
    }
    
    return resp.User, nil
}

// Enable MFA
func (c *UserClient) EnableMFA(ctx context.Context, userID, orgID, method, phoneNumber string) (string, string, []string, error) {
    if c.client == nil {
        return "secret123", "qr-code-data", []string{"backup1", "backup2"}, nil
    }
    
    req := &userpb.EnableMFARequest{
        UserId:       userID,
        OrganizationId: orgID,
        Method:       method,
        PhoneNumber:  phoneNumber,
    }
    
    resp, err := c.client.EnableMFA(c.getContext(ctx), req)
    if err != nil {
        return "", "", nil, fmt.Errorf("enable MFA failed: %w", err)
    }
    
    if !resp.Enabled {
        return "", "", nil, fmt.Errorf("MFA enable failed")
    }
    
    return resp.Secret, resp.QrCode, resp.BackupCodes, nil
}

// Disable MFA
func (c *UserClient) DisableMFA(ctx context.Context, userID, orgID, factorID string) error {
    if c.client == nil {
        return nil
    }
    
    req := &userpb.DisableMFARequest{
        UserId:         userID,
        OrganizationId: orgID,
        FactorId:       factorID,
    }
    
    resp, err := c.client.DisableMFA(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("disable MFA failed: %w", err)
    }
    
    if !resp.Disabled {
        return fmt.Errorf("MFA disable failed")
    }
    
    return nil
}

// Update preferences
func (c *UserClient) UpdatePreferences(ctx context.Context, userID, orgID string, preferences *userpb.UserPreferences) (*userpb.UserPreferences, error) {
    if c.client == nil {
        return preferences, nil
    }
    
    req := &userpb.UpdatePreferencesRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Preferences:    preferences,
    }
    
    resp, err := c.client.UpdatePreferences(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update preferences failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("preferences update failed")
    }
    
    return resp.Preferences, nil
}

// Admin: Get user (with audit)
func (c *UserClient) AdminGetUser(ctx context.Context, userID, orgID string, includeFullHistory bool) (*userpb.User, *userpb.UserAuditSummary, error) {
    if c.adminClient == nil {
        return mockUserByID(userID), nil, nil
    }
    
    req := &userpb.AdminGetUserRequest{
        UserId:             userID,
        OrganizationId:     orgID,
IncludeFullHistory: includeFullHistory,
    }
    
    resp, err := c.adminClient.AdminGetUser(c.getContext(ctx), req)
    if err != nil {
        return nil, nil, fmt.Errorf("admin get user failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil, nil
    }
    
    return resp.User, resp.AuditSummary, nil
}

// Admin: List users with filters
func (c *UserClient) AdminListUsers(ctx context.Context, orgID string, filter *userpb.AdminUserFilter, limit, offset int32) ([]*userpb.User, int32, error) {
    if c.adminClient == nil {
        return []*userpb.User{}, 0, nil
    }
    
    req := &userpb.AdminListUsersRequest{
        OrganizationId: orgID,
        Filter:         filter,
        Limit:          limit,
        Offset:         offset,
        SortBy:         "created_at",
        SortOrder:      "desc",
    }
    
    resp, err := c.adminClient.AdminListUsers(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("admin list users failed: %w", err)
    }
    
    return resp.Users, resp.TotalCount, nil
}

// Admin: Suspend user
func (c *UserClient) AdminSuspendUser(ctx context.Context, userID, orgID, reason string, suspendUntil *time.Time) (*userpb.User, error) {
    if c.adminClient == nil {
        return mockUserSuspended(userID), nil
    }
    
    req := &userpb.AdminSuspendUserRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Reason:         reason,
    }
    
    if suspendUntil != nil {
        req.SuspendUntil = timestamppb.New(*suspendUntil)
    }
    
    resp, err := c.adminClient.AdminSuspendUser(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("admin suspend user failed: %w", err)
    }
    
    if !resp.Suspended {
        return nil, fmt.Errorf("user suspension failed")
    }
    
    return resp.User, nil
}

// Admin: Review KYC
func (c *UserClient) AdminReviewKYC(ctx context.Context, userID, orgID, kycID string, approved bool, rejectionReason string, newLevel userpb.KYCLevel, reviewerNotes string) (userpb.KYCStatus, userpb.KYCLevel, error) {
    if c.adminClient == nil {
        return userpb.KYCStatus_VERIFIED, newLevel, nil
    }
    
    req := &userpb.AdminReviewKYCRequest{
        UserId:         userID,
        OrganizationId: orgID,
        KycId:          kycID,
        Approved:       approved,
        RejectionReason: rejectionReason,
        NewLevel:       newLevel,
        ReviewerNotes:  reviewerNotes,
    }
    
    resp, err := c.adminClient.AdminReviewKYC(c.getContext(ctx), req)
    if err != nil {
        return userpb.KYC_STATUS_UNSPECIFIED, userpb.KYC_LEVEL_UNSPECIFIED, fmt.Errorf("admin review KYC failed: %w", err)
    }
    
    if !resp.Reviewed {
        return userpb.KYC_STATUS_UNSPECIFIED, userpb.KYC_LEVEL_UNSPECIFIED, fmt.Errorf("KYC review failed")
    }
    
    return resp.Status, resp.Level, nil
}

// Mock functions for testing
func mockUser(details *userpb.UserDetails) *userpb.User {
    return &userpb.User{
        User: details,
        Metadata: &userpb.MetaData{
            CreatedAt: timestamppb.Now(),
        },
        OrganizationIds: []string{details.OrganizationId},
    }
}

func mockUserByID(userID string) *userpb.User {
    return &userpb.User{
        User: &userpb.UserDetails{
            UserId:    userID,
            Email:     "test@example.com",
            FirstName: "Test",
            LastName:  "User",
            Status:    userpb.UserStatus_ACTIVE,
        },
        OrganizationIds: []string{"org-123"},
    }
}

func mockUserByEmail(email string) *userpb.User {
    return &userpb.User{
        User: &userpb.UserDetails{
            UserId:    "user-123",
            Email:     email,
            FirstName: "Test",
            LastName:  "User",
            Status:    userpb.UserStatus_ACTIVE,
        },
    }
}

func mockUserUpdate(userID string) *userpb.User {
    return &userpb.User{
        User: &userpb.UserDetails{
            UserId:    userID,
            Email:     "updated@example.com",
            FirstName: "Updated",
            LastName:  "Name",
            Status:    userpb.UserStatus_ACTIVE,
            UpdatedAt: timestamppb.Now(),
        },
    }
}

func mockUserClone(userID string) *userpb.User {
    return &userpb.User{
        User: &userpb.UserDetails{
            UserId:         userID,
            OrganizationId: "new-org-456",
            Status:         userpb.UserStatus_ACTIVE,
        },
        OrganizationIds: []string{"org-123", "new-org-456"},
    }
}

func mockUserSwitch(userID, orgID string) *userpb.User {
    return &userpb.User{
        User: &userpb.UserDetails{
            UserId:         userID,
            OrganizationId: orgID,
            Status:         userpb.UserStatus_ACTIVE,
        },
        OrganizationIds: []string{orgID},
    }
}

func mockUserSuspended(userID string) *userpb.User {
    return &userpb.User{
        User: &userpb.UserDetails{
            UserId: userID,
            Status: userpb.UserStatus_SUSPENDED,
        },
    }
}

func mockWallet() *userpb.Wallet {
    return &userpb.Wallet{
        WalletId:     "wallet-123",
        WalletAddress: "0x1234567890abcdef",
        AssetSymbol:  "TX",
        Balance:      "1000.00",
        IsDefault:    true,
        IsVerified:   true,
        CreatedAt:    timestamppb.Now(),
    }
}

func mockOrgInfo() *userpb.OrganizationInfo {
    return &userpb.OrganizationInfo{
        OrganizationId:   "org-123",
        OrganizationName: "Test Organization",
        Status:           userpb.UserStatus_ACTIVE,
        JoinedAt:         timestamppb.Now(),
        IsDefault:        true,
    }
}

// Example usage
func main() {
    client, err := NewUserClient("user-store:50076")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    
    // Create a new user
    userDetails := &userpb.UserDetails{
        Email:       "john.doe@example.com",
        PhoneNumber: "+1234567890",
        FirstName:   "John",
        LastName:    "Doe",
        UserType:    userpb.UserType_INDIVIDUAL,
        PrimaryAddress: &userpb.Address{
            AddressLine1: "123 Main St",
            City:         "New York",
            State:        "NY",
            PostalCode:   "10001",
            Country:      "USA",
            CountryCode:  "US",
        },
    }
    
    user, err := client.CreateUser(ctx, userDetails, "SecurePass123!", orgID, true)
    if err != nil {
        log.Printf("Failed to create user: %v", err)
    } else {
        log.Printf("User created: %s (%s)", user.User.UserId, user.User.Email)
    }
    
    // Get user
    retrievedUser, err := client.GetUser(ctx, user.User.UserId, orgID, true, true)
    if err != nil {
        log.Printf("Failed to get user: %v", err)
    } else if retrievedUser != nil {
        log.Printf("Retrieved user: %s %s", retrievedUser.User.FirstName, retrievedUser.User.LastName)
    }
    
    // Submit KYC
    kycDetails := &userpb.KYCDetails{
        Level: userpb.KYCLevel_LEVEL_2,
        IdentityDocuments: []*userpb.IdentityDocument{
            {
                DocumentType:    "passport",
                DocumentNumber:  "AB123456",
                IssuingCountry:  "US",
                FirstName:       "John",
                LastName:        "Doe",
                DateOfBirth:     "1990-01-01",
            },
        },
    }
    
    kycID, status, err := client.SubmitKYC(ctx, user.User.UserId, orgID, kycDetails)
    if err != nil {
        log.Printf("Failed to submit KYC: %v", err)
    } else {
        log.Printf("KYC submitted: %s (status: %v)", kycID, status)
    }
    
    // Add wallet
    wallet := &userpb.Wallet{
        WalletAddress: "0xabcdef1234567890",
        AssetSymbol:   "TX",
        IsDefault:     true,
    }
    
    addedWallet, err := client.AddWallet(ctx, user.User.UserId, orgID, wallet)
    if err != nil {
        log.Printf("Failed to add wallet: %v", err)
    } else {
        log.Printf("Wallet added: %s", addedWallet.WalletAddress)
    }
    
    // Get compliance questions
    questions, err := client.GetComplianceQuestions(ctx, orgID, "US")
    if err != nil {
        log.Printf("Failed to get compliance questions: %v", err)
    } else {
        log.Printf("Found %d compliance questions", len(questions))
    }
    
    // Clone user to another organization
    cloneConfig := &userpb.CloneConfiguration{
        CloneKyc:           true,
        CloneTradeProfile:  false,
        ClonePreferences:   true,
        SendNotification:   true,
        RequireReview:      false,
        DisableUserUntilReview: false,
    }
    
    clonedUser, requiresReview, err := client.CloneUserToOrganization(ctx, user.User.UserId, orgID, "org-456", cloneConfig)
    if err != nil {
        log.Printf("Failed to clone user: %v", err)
    } else {
        log.Printf("User cloned to org: %s (requires review: %v)", clonedUser.User.OrganizationId, requiresReview)
    }
    
    // Get user's organizations
    orgs, err := client.GetUserOrganizations(ctx, user.User.UserId)
    if err != nil {
        log.Printf("Failed to get organizations: %v", err)
    } else {
        log.Printf("User is in %d organizations", len(orgs))
        for _, org := range orgs {
            log.Printf("  - %s (%s)", org.OrganizationName, org.OrganizationId)
        }
    }
    
    // Enable MFA
    secret, qrCode, backupCodes, err := client.EnableMFA(ctx, user.User.UserId, orgID, "totp", "")
    if err != nil {
        log.Printf("Failed to enable MFA: %v", err)
    } else {
        log.Printf("MFA enabled - Secret: %s", secret)
        log.Printf("Backup codes: %v", backupCodes)
        _ = qrCode
    }
    
    // Update preferences
    preferences := &userpb.UserPreferences{
        Language:           "en",
        Timezone:           "America/New_York",
        Currency:           "USD",
        Theme:              "dark",
        EmailNotifications: true,
        PushNotifications:  true,
    }
    
    updatedPrefs, err := client.UpdatePreferences(ctx, user.User.UserId, orgID, preferences)
    if err != nil {
        log.Printf("Failed to update preferences: %v", err)
    } else {
        log.Printf("Preferences updated: theme=%s", updatedPrefs.Theme)
    }
}
Save the file:

Ctrl+O, Enter, Ctrl+X

4. User Docker Compose
bash
nano ~/dev/TXdocumentation/user/docker-compose.yml
yaml
version: '3.8'

services:
  user-service:
    image: sologenic/user-service:latest
    environment:
      - USER_SERVICE_PORT=50076
      - USER_STORE=user-store:50076
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=users
      - POSTGRES_USER=user_service_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - S3_ENDPOINT=minio:9000
      - S3_BUCKET=user-documents
      - S3_ACCESS_KEY=${S3_ACCESS_KEY}
      - S3_SECRET_KEY=${S3_SECRET_KEY}
      - MAX_USERS_PER_QUERY=100
      - KYC_RETENTION_DAYS=2555
      - CLONE_BATCH_SIZE=100
      - CACHE_TTL_SECONDS=300
      - REQUIRE_EMAIL_VERIFICATION=true
      - REQUIRE_PHONE_VERIFICATION=false
      - LOG_LEVEL=info
    ports:
      - "50076:50076"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
      - minio
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50076"]
      interval: 30s
      timeout: 10s
      retries: 3

  user-store:
    image: sologenic/user-store:latest
    environment:
      - USER_STORE_PORT=50077
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=users
      - POSTGRES_USER=user_service_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50077:50077"
    networks:
      - internal
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=users
      - POSTGRES_USER=user_service_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user_service_user -d users"]
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

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=${S3_ACCESS_KEY}
      - MINIO_ROOT_PASSWORD=${S3_SECRET_KEY}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    networks:
      - internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

networks:
  internal:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  minio_data:
Save the file:

Ctrl+O, Enter, Ctrl+X

5. User Environment File
bash
nano ~/dev/TXdocumentation/user/.env
bash
# Database Configuration
DB_PASSWORD=your_secure_password

# S3/MinIO Configuration
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin123

# Service Configuration
USER_STORE=user-store:50077
USER_STORE_TESTING=FALSE

# Business Rules
MAX_USERS_PER_QUERY=100
KYC_RETENTION_DAYS=2555
CLONE_BATCH_SIZE=100

# Cache Configuration
CACHE_TTL_SECONDS=300

# Verification Requirements
REQUIRE_EMAIL_VERIFICATION=true
REQUIRE_PHONE_VERIFICATION=false

# Logging
LOG_LEVEL=info
