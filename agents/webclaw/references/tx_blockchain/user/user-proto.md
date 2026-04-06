# User Service (User Proto)

The User proto provides all the functionality required to interact with the user service. The user service is multi-organizational, meaning a user can be part of multiple organizations.

## Overview

The User service is a gRPC-based system that handles:
- User details and profile information
- KYC (Know Your Customer) verification
- Funding sources (wallets, bank accounts, broker accounts)
- Compliance tracking and questions
- Multi-organizational user management
- User cloning across organizations
- Audit trails for user changes

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Web UI, Mobile App, Admin Dashboard, KYC Providers, Compliance) │
└───────────────────────────────────┬─────────────────────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ User Service │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ User │ │ KYC │ │ Funding │ │ Compliance │ │
│ │ Management │ │ Management │ │ Management │ │ Tracker │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Organization│ │ Clone │ │ Audit │ │
│ │ Management │ │ Engine │ │ Logger │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────────────┬─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Storage Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ User Store │ │ KYC Store │ │ Funding │ │ Audit Store │ │
│ │ (PostgreSQL)│ │ (PostgreSQL)│ │ Store │ │ (Timescale) │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│ ┌─────────────┐ ┌─────────────┐ │
│ │ Redis Cache │ │ Document │ │
│ │ (Session) │ │ Store (S3) │ │
│ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Multi-Organizational Design

The user service is multi-organizational. A user can be part of multiple organizations, managed in the `OrganizationIDs` field.

```protobuf
message User {
    UserDetails user = 1;
    metadata.MetaData metadata = 2;
    audit.Audit audit = 3;
    repeated string organization_ids = 4; // List of organizations where the user is part of (cloned into)
}
User Cloning
When cloning a user to a separate organization, the base OrganizationID in user details is set to the OrganizationID of the user being cloned to. This field is redundant but present for legacy reasons.

Cloning Configuration
When cloning a user, the organization configuration determines which parts of the user are cloned.

Never Cloned
User.organization_ids - TX classified information

User.audit - Each organization starts its own history for the user from the moment of cloning

Always Cloned (Initial Clone)
UserDetails except BrokerAccount, BankAccount, ComplianceQuestions, TradeProfile, Wallets, KYCDetails

From UserDetails.Wallets - the TX wallet is always cloned

From UserDetails.UserDocumentCompliance - signed TX documents are always cloned

Often Cloned
KYCDetails - If KYC Reliance is enabled

Never Cloned (Typically)
UserDetails.UserTradeProfile, UserDetails.TradeProfileDetails - Trading profiles tend to be specific to 1-2 organizations per jurisdiction

Cloning Changes Propagation
Optional changes can be propagated from TX organization to users in other organizations, controlled by organization configuration.

Propagation Actions
Send notification to organization admin(s)

Review user - set review flag to true

Disable user - set review flag to true and disable

Cloned Fields Conditions
Never cloned - TX classified information or organization-specific fields

Conditionally cloned - Organization can state whether changes should propagate (e.g., address changes)

Proto File Structure
The proto has been split into multiple files for easier maintenance:

File	Description
user.proto	User details and related information
user-kyc.proto	KYC details
user-fundings.proto	Funding details (wallet, bank accounts, broker accounts)
user-compliance.proto	Compliance details (questions and answers)
user-filters.proto	Filters for user and admin user queries
user-grpc.proto	GRPC service for user + related messages
adminuser-grpc.proto	GRPC service for admin user operations
Environment Variables
Required Variables
Variable	Description	Format	Example
USER_STORE	gRPC endpoint for user store service	host:port	user-store:50076
USER_STORE_TESTING	Enable test mode with in-memory buffer	TRUE	TRUE
Optional Variables
Variable	Description	Default
MAX_USERS_PER_QUERY	Maximum users per query	100
KYC_RETENTION_DAYS	KYC document retention in days	2555 (7 years)
CLONE_BATCH_SIZE	Users per clone batch	100
CACHE_TTL_SECONDS	User cache TTL	300
REQUIRE_EMAIL_VERIFICATION	Require email verification	true
REQUIRE_PHONE_VERIFICATION	Require phone verification	false
Proto Definitions
user.proto - User Details
protobuf
syntax = "proto3";

package user.v1;

import "google/protobuf/timestamp.proto";
import "user-kyc.proto";
import "user-fundings.proto";
import "user-compliance.proto";

// User status enum
enum UserStatus {
    USER_STATUS_UNSPECIFIED = 0;
    ACTIVE = 1;                 // User is active
    INACTIVE = 2;               // User is inactive
    SUSPENDED = 3;              // User is suspended
    PENDING_VERIFICATION = 4;   // Awaiting verification
    PENDING_KYC = 5;            // Awaiting KYC completion
    PENDING_REVIEW = 6;         // Under review
    BLOCKED = 7;                // User is blocked
    DELETED = 8;                // User deleted
}

// User type enum
enum UserType {
    USER_TYPE_UNSPECIFIED = 0;
    INDIVIDUAL = 1;             // Individual person
    BUSINESS = 2;               // Business entity
    INSTITUTIONAL = 3;          // Institutional investor
    DEVELOPER = 4;              // Developer account
    SERVICE_ACCOUNT = 5;        // Service account
}

// User details message
message UserDetails {
    // Core identifiers
    string user_id = 1;
    string organization_id = 2;     // Legacy - primary organization
    string email = 3;
    string phone_number = 4;
    
    // Personal information
    string first_name = 5;
    string last_name = 6;
    string middle_name = 7;
    string display_name = 8;
    
    // Business information (for business accounts)
    string business_name = 9;
    string business_registration_number = 10;
    string tax_id = 11;
    
    // Address information
    Address primary_address = 12;
    Address mailing_address = 13;
    
    // Date of birth / incorporation
    google.protobuf.Timestamp date_of_birth = 14;
    google.protobuf.Timestamp incorporation_date = 15;
    
    // Verification status
    UserStatus status = 16;
    UserType user_type = 17;
    bool email_verified = 18;
    bool phone_verified = 19;
    google.protobuf.Timestamp email_verified_at = 20;
    google.protobuf.Timestamp phone_verified_at = 21;
    
    // KYC information
    KYCDetails kyc_details = 22;
    
    // Funding sources
    repeated Wallet wallets = 23;
    repeated BankAccount bank_accounts = 24;
    repeated BrokerAccount broker_accounts = 25;
    
    // Compliance
    repeated ComplianceQuestion compliance_questions = 26;
    repeated ComplianceAnswer compliance_answers = 27;
    repeated UserDocumentCompliance documents = 28;
    
    // Trading profile
    UserTradeProfile trade_profile = 29;
    TradeProfileDetails trade_profile_details = 30;
    
    // Preferences
    UserPreferences preferences = 31;
    
    // Security
    UserSecuritySettings security_settings = 32;
    repeated MFAFactor mfa_factors = 33;
    
    // Timestamps
    google.protobuf.Timestamp created_at = 34;
    google.protobuf.Timestamp updated_at = 35;
    google.protobuf.Timestamp last_login_at = 36;
    google.protobuf.Timestamp last_activity_at = 37;
    
    // Metadata
    map<string, string> metadata = 38;
    repeated string tags = 39;
}

// Address message
message Address {
    string address_line1 = 1;
    string address_line2 = 2;
    string city = 3;
    string state = 4;
    string postal_code = 5;
    string country = 6;
    string country_code = 7;        // ISO 3166-1 alpha-2
}

// User preferences
message UserPreferences {
    string language = 1;            // en, es, fr, etc.
    string timezone = 2;            // America/New_York
    string currency = 3;            // USD, EUR, etc.
    string theme = 4;               // light, dark, system
    bool email_notifications = 5;
    bool push_notifications = 6;
    bool sms_notifications = 7;
    bool marketing_emails = 8;
    map<string, string> custom_preferences = 9;
}

// User security settings
message UserSecuritySettings {
    bool two_factor_enabled = 1;
    repeated string two_factor_methods = 2;     // sms, authenticator, hardware
    google.protobuf.Timestamp password_last_changed = 3;
    bool password_expires_soon = 4;
    int32 failed_login_attempts = 5;
    google.protobuf.Timestamp last_failed_login = 6;
    bool account_locked = 7;
    google.protobuf.Timestamp account_locked_until = 8;
    repeated string trusted_devices = 9;
    repeated string trusted_ip_addresses = 10;
}

// MFA Factor
message MFAFactor {
    string factor_id = 1;
    string factor_type = 2;         // sms, totp, webauthn, recovery
    string factor_name = 3;
    bool is_primary = 4;
    bool is_active = 5;
    google.protobuf.Timestamp created_at = 6;
    google.protobuf.Timestamp last_used_at = 7;
}

// User trade profile
message UserTradeProfile {
    string profile_id = 1;
    string experience_level = 2;    // beginner, intermediate, advanced, expert
    string investment_objective = 3; // growth, income, preservation, speculation
    string risk_tolerance = 4;       // conservative, moderate, aggressive
    string time_horizon = 5;         // short, medium, long
    repeated string approved_asset_classes = 6;
    map<string, string> trading_limits = 7;
    google.protobuf.Timestamp last_reviewed_at = 8;
    string reviewed_by = 9;
}

// Trade profile details
message TradeProfileDetails {
    bool margin_trading_enabled = 1;
    bool derivatives_trading_enabled = 2;
    bool options_trading_enabled = 3;
    string max_leverage = 4;
    repeated string approved_derivatives = 5;
    map<string, string> custom_limits = 6;
}

// User document compliance
message UserDocumentCompliance {
    string document_id = 1;
    string document_type = 2;       // w9, w8ben, agreement, disclosure
    string document_name = 3;
    string document_version = 4;
    bytes document_content = 5;
    string document_hash = 6;
    bool is_signed = 7;
    google.protobuf.Timestamp signed_at = 8;
    string signed_by = 9;
    string ip_address = 10;
    string user_agent = 11;
    google.protobuf.Timestamp expires_at = 12;
    bool is_valid = 13;
}

// Main User message
message User {
    UserDetails user = 1;
    metadata.MetaData metadata = 2;
    audit.Audit audit = 3;
    repeated string organization_ids = 4; // List of organizations where the user is part of (cloned into)
}

// Metadata
message MetaData {
    string created_by = 1;
    string updated_by = 2;
    string source_system = 3;
    map<string, string> custom_metadata = 4;
}

// Audit
message Audit {
    google.protobuf.Timestamp created_at = 1;
    google.protobuf.Timestamp updated_at = 2;
    int32 version = 3;
    repeated AuditEntry entries = 4;
}

message AuditEntry {
    string action = 1;
    string field_name = 2;
    string old_value = 3;
    string new_value = 4;
    string performed_by = 5;
    google.protobuf.Timestamp performed_at = 6;
    string ip_address = 7;
    string reason = 8;
}
user-kyc.proto - KYC Details
protobuf
syntax = "proto3";

package user.v1;

import "google/protobuf/timestamp.proto";

// KYC Status
enum KYCStatus {
    KYC_STATUS_UNSPECIFIED = 0;
    NOT_STARTED = 1;
    PENDING = 2;
    IN_REVIEW = 3;
    VERIFIED = 4;
    REJECTED = 5;
    EXPIRED = 6;
    REQUIRES_UPDATE = 7;
}

// KYC Level
enum KYCLevel {
    KYC_LEVEL_UNSPECIFIED = 0;
    LEVEL_0 = 1;    // Basic - email/phone
    LEVEL_1 = 2;    // Identity verification
    LEVEL_2 = 3;    // Address verification
    LEVEL_3 = 4;    // Enhanced due diligence
    LEVEL_4 = 5;    // Institutional KYC
}

// KYC Details
message KYCDetails {
    string kyc_id = 1;
    KYCStatus status = 2;
    KYCLevel level = 3;
    
    // Identity documents
    repeated IdentityDocument identity_documents = 4;
    
    // Address verification
    repeated AddressDocument address_documents = 5;
    
    // Business verification (for business accounts)
    BusinessVerification business_verification = 6;
    
    // Enhanced due diligence
    EnhancedDueDiligence edd = 7;
    
    // Verification results
    VerificationResult verification_result = 8;
    
    // Sanctions screening
    SanctionsScreening sanctions_screening = 9;
    
    // Timestamps
    google.protobuf.Timestamp submitted_at = 10;
    google.protobuf.Timestamp verified_at = 11;
    google.protobuf.Timestamp expires_at = 12;
    google.protobuf.Timestamp last_reviewed_at = 13;
    
    // Review information
    string reviewed_by = 14;
    string rejection_reason = 15;
    repeated string notes = 16;
}

// Identity Document
message IdentityDocument {
    string document_id = 1;
    string document_type = 2;   // passport, driver_license, national_id, residence_permit
    string document_number = 3;
    string issuing_country = 4;
    google.protobuf.Timestamp issue_date = 5;
    google.protobuf.Timestamp expiry_date = 6;
    string first_name = 7;
    string last_name = 8;
    string date_of_birth = 9;
    bytes front_image = 10;
    bytes back_image = 11;
    bytes selfie_image = 12;
    bool is_verified = 13;
    string verification_method = 14;    // manual, automated, hybrid
    double verification_score = 15;
    string verified_by = 16;
    google.protobuf.Timestamp verified_at = 17;
}

// Address Document
message AddressDocument {
    string document_id = 1;
    string document_type = 2;   // utility_bill, bank_statement, government_letter
    string address = 3;
    google.protobuf.Timestamp issue_date = 4;
    bytes document_image = 5;
    bool is_verified = 6;
    string verified_by = 7;
    google.protobuf.Timestamp verified_at = 8;
}

// Business Verification
message BusinessVerification {
    string registration_number = 1;
    string legal_name = 2;
    string trading_name = 3;
    string business_type = 4;   // corporation, llc, partnership, sole_proprietorship
    string jurisdiction = 5;
    google.protobuf.Timestamp incorporation_date = 6;
    repeated Director directors = 7;
    repeated Shareholder shareholders = 8;
    repeated BeneficialOwner beneficial_owners = 9;
    bytes certificate_of_incorporation = 10;
    bytes memorandum_articles = 11;
    bytes proof_of_address = 12;
    bool is_verified = 13;
}

// Director
message Director {
    string full_name = 1;
    string position = 2;
    string date_of_birth = 3;
    string nationality = 4;
    string address = 5;
}

// Shareholder
message Shareholder {
    string name = 1;
    string share_percentage = 2;
    string share_class = 3;
}

// Beneficial Owner
message BeneficialOwner {
    string full_name = 1;
    string ownership_percentage = 2;
    string date_of_birth = 3;
    string nationality = 4;
    string address = 5;
}

// Enhanced Due Diligence
message EnhancedDueDiligence {
    string source_of_funds = 1;
    string source_of_wealth = 2;
    string estimated_net_worth = 3;
    string estimated_annual_income = 4;
    string occupation = 5;
    string employer_name = 6;
    bool politically_exposed_person = 7;
    string pep_details = 8;
    bool family_member_pep = 9;
    bool close_associate_pep = 10;
    repeated string additional_questions = 11;
    repeated string additional_answers = 12;
    bytes supporting_documents = 13;
}

// Verification Result
message VerificationResult {
    bool identity_verified = 1;
    bool address_verified = 2;
    bool business_verified = 3;
    bool sanctions_passed = 4;
    bool pep_screening_passed = 5;
    double overall_score = 6;
    string risk_level = 7;          // low, medium, high, critical
    repeated string flags = 8;
    string recommendation = 9;
}

// Sanctions Screening
message SanctionsScreening {
    bool screened = 1;
    google.protobuf.Timestamp last_screened_at = 2;
    repeated string sanctions_lists = 3;
    bool matches_found = 4;
    repeated SanctionsMatch matches = 5;
    string screening_provider = 6;
    string screening_reference = 7;
}

// Sanctions Match
message SanctionsMatch {
    string list_name = 1;
    string matched_name = 2;
    string match_score = 3;
    string match_type = 4;          // exact, fuzzy, partial
    string additional_info = 5;
}
user-fundings.proto - Funding Sources
protobuf
syntax = "proto3";

package user.v1;

import "google/protobuf/timestamp.proto";

// Wallet
message Wallet {
    string wallet_id = 1;
    string wallet_address = 2;
    string asset_type = 3;          // TX, BTC, ETH, etc.
    string asset_symbol = 4;
    string balance = 5;
    bool is_default = 6;
    bool is_verified = 7;
    google.protobuf.Timestamp created_at = 8;
    google.protobuf.Timestamp last_used_at = 9;
    map<string, string> metadata = 10;
}

// Bank Account
message BankAccount {
    string account_id = 1;
    string bank_name = 2;
    string account_holder_name = 3;
    string account_number = 4;      // Masked
    string routing_number = 5;      // Masked
    string iban = 6;                // Masked
    string swift_code = 7;
    string account_type = 8;        // checking, savings, business
    string currency = 9;
    bool is_default = 10;
    bool is_verified = 11;
    VerificationStatus verification_status = 12;
    google.protobuf.Timestamp verified_at = 13;
    google.protobuf.Timestamp created_at = 14;
    map<string, string> metadata = 15;
}

// Broker Account
message BrokerAccount {
    string broker_account_id = 1;
    string broker_name = 2;
    string broker_account_number = 3;   // Masked
    string account_type = 4;            // individual, joint, corporate
    string account_status = 5;          // active, pending, closed
    google.protobuf.Timestamp opened_at = 6;
    bool is_default = 7;
    bool is_verified = 8;
    map<string, string> broker_metadata = 9;
    google.protobuf.Timestamp created_at = 10;
}

// Verification Status
enum VerificationStatus {
    VERIFICATION_STATUS_UNSPECIFIED = 0;
    UNVERIFIED = 1;
    PENDING = 2;
    VERIFIED = 3;
    FAILED = 4;
    EXPIRED = 5;
}
user-compliance.proto - Compliance
protobuf
syntax = "proto3";

package user.v1;

import "google/protobuf/timestamp.proto";

// Compliance Question
message ComplianceQuestion {
    string question_id = 1;
    string question_text = 2;
    string question_category = 3;   // regulatory, suitability, risk
    string answer_type = 4;         // boolean, text, select, multi_select
    repeated string options = 5;     // For select/multi_select
    bool is_required = 6;
    int32 order = 7;
    string regulation = 8;          // Reference regulation
}

// Compliance Answer
message ComplianceAnswer {
    string answer_id = 1;
    string question_id = 2;
    string answer_value = 3;
    google.protobuf.Timestamp answered_at = 4;
    string answered_by = 5;
    bool requires_review = 6;
    string review_notes = 7;
    google.protobuf.Timestamp reviewed_at = 8;
    string reviewed_by = 9;
}
user-grpc.proto - User Service
protobuf
syntax = "proto3";

package user.v1;

import "user.proto";
import "user-kyc.proto";
import "user-fundings.proto";
import "user-filters.proto";

// User Service Definition
service UserService {
    // User management
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
    rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
    rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
    
    // User search and filters
    rpc SearchUsers(SearchUsersRequest) returns (SearchUsersResponse);
    rpc GetUserByEmail(GetUserByEmailRequest) returns (GetUserByEmailResponse);
    rpc GetUserByPhone(GetUserByPhoneRequest) returns (GetUserByPhoneResponse);
    
    // KYC operations
    rpc SubmitKYC(SubmitKYCRequest) returns (SubmitKYCResponse);
    rpc GetKYCStatus(GetKYCStatusRequest) returns (GetKYCStatusResponse);
    rpc UpdateKYC(UpdateKYCRequest) returns (UpdateKYCResponse);
    rpc VerifyKYC(VerifyKYCRequest) returns (VerifyKYCResponse);
    
    // Funding operations
    rpc AddWallet(AddWalletRequest) returns (AddWalletResponse);
    rpc RemoveWallet(RemoveWalletRequest) returns (RemoveWalletResponse);
    rpc GetWallets(GetWalletsRequest) returns (GetWalletsResponse);
    rpc AddBankAccount(AddBankAccountRequest) returns (AddBankAccountResponse);
    rpc RemoveBankAccount(RemoveBankAccountRequest) returns (RemoveBankAccountResponse);
    rpc GetBankAccounts(GetBankAccountsRequest) returns (GetBankAccountsResponse);
    rpc AddBrokerAccount(AddBrokerAccountRequest) returns (AddBrokerAccountResponse);
    rpc RemoveBrokerAccount(RemoveBrokerAccountRequest) returns (RemoveBrokerAccountResponse);
    rpc GetBrokerAccounts(GetBrokerAccountsRequest) returns (GetBrokerAccountsResponse);
    
    // Compliance operations
    rpc GetComplianceQuestions(GetComplianceQuestionsRequest) returns (GetComplianceQuestionsResponse);
    rpc SubmitComplianceAnswers(SubmitComplianceAnswersRequest) returns (SubmitComplianceAnswersResponse);
    
    // Document operations
    rpc UploadDocument(UploadDocumentRequest) returns (UploadDocumentResponse);
    rpc GetDocuments(GetDocumentsRequest) returns (GetDocumentsResponse);
    rpc SignDocument(SignDocumentRequest) returns (SignDocumentResponse);
    
    // Multi-organization operations
    rpc CloneUserToOrganization(CloneUserToOrganizationRequest) returns (CloneUserToOrganizationResponse);
    rpc GetUserOrganizations(GetUserOrganizationsRequest) returns (GetUserOrganizationsResponse);
    rpc SwitchOrganization(SwitchOrganizationRequest) returns (SwitchOrganizationResponse);
    
    // Security operations
    rpc ChangePassword(ChangePasswordRequest) returns (ChangePasswordResponse);
    rpc EnableMFA(EnableMFARequest) returns (EnableMFAResponse);
    rpc DisableMFA(DisableMFARequest) returns (DisableMFAResponse);
    rpc GetMFAMethods(GetMFAMethodsRequest) returns (GetMFAMethodsResponse);
    rpc VerifyMFA(VerifyMFARequest) returns (VerifyMFAResponse);
    
    // Preferences
    rpc UpdatePreferences(UpdatePreferencesRequest) returns (UpdatePreferencesResponse);
    rpc GetPreferences(GetPreferencesRequest) returns (GetPreferencesResponse);
}

// Request/Response Messages
message CreateUserRequest {
    UserDetails user = 1;
    string password = 2;
    string organization_id = 3;
    bool send_welcome_email = 4;
}

message CreateUserResponse {
    User user = 1;
    bool created = 2;
    string message = 3;
}

message GetUserRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_kyc = 3;
    bool include_funding = 4;
}

message GetUserResponse {
    User user = 1;
    bool found = 2;
}

message UpdateUserRequest {
    string user_id = 1;
    string organization_id = 2;
    optional string email = 3;
    optional string phone_number = 4;
    optional string first_name = 5;
    optional string last_name = 6;
    optional Address primary_address = 7;
    optional UserPreferences preferences = 8;
    map<string, string> metadata = 9;
    string update_reason = 10;
}

message UpdateUserResponse {
    User user = 1;
    bool updated = 2;
    bool requires_review = 3;
    string message = 4;
}

message DeleteUserRequest {
    string user_id = 1;
    string organization_id = 2;
    bool permanent = 3;
    string reason = 4;
}

message DeleteUserResponse {
    bool deleted = 1;
    string message = 2;
}

message ListUsersRequest {
    string organization_id = 1;
    UserFilter filter = 2;
    int32 limit = 3;
    int32 offset = 4;
    string sort_by = 5;
    string sort_order = 6;
}

message ListUsersResponse {
    repeated User users = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

message SearchUsersRequest {
    string organization_id = 1;
    string query = 2;
    repeated string fields = 3;
    int32 limit = 4;
    int32 offset = 5;
}

message SearchUsersResponse {
    repeated User users = 1;
    int32 total_count = 2;
}

message GetUserByEmailRequest {
    string email = 1;
    string organization_id = 2;
}

message GetUserByEmailResponse {
    User user = 1;
    bool found = 2;
}

message GetUserByPhoneRequest {
    string phone_number = 1;
    string organization_id = 2;
}

message GetUserByPhoneResponse {
    User user = 1;
    bool found = 2;
}

// KYC Messages
message SubmitKYCRequest {
    string user_id = 1;
    string organization_id = 2;
    KYCDetails kyc_details = 3;
}

message SubmitKYCResponse {
    string kyc_id = 1;
    bool submitted = 2;
    KYCStatus status = 3;
    string message = 4;
}

message GetKYCStatusRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetKYCStatusResponse {
    KYCStatus status = 1;
    KYCLevel level = 2;
    KYCDetails details = 3;
    bool found = 4;
}

message UpdateKYCRequest {
    string user_id = 1;
    string organization_id = 2;
    KYCDetails kyc_details = 3;
    string update_reason = 4;
}

message UpdateKYCResponse {
    bool updated = 1;
    KYCStatus status = 2;
    string message = 3;
}

message VerifyKYCRequest {
    string user_id = 1;
    string organization_id = 2;
    string kyc_id = 3;
    bool approved = 4;
    string rejection_reason = 5;
    string verified_by = 6;
    KYCLevel new_level = 7;
}

message VerifyKYCResponse {
    bool verified = 1;
    KYCStatus status = 2;
    KYCLevel level = 3;
    string message = 4;
}

// Funding Messages
message AddWalletRequest {
    string user_id = 1;
    string organization_id = 2;
    Wallet wallet = 3;
}

message AddWalletResponse {
    Wallet wallet = 1;
    bool added = 2;
}

message RemoveWalletRequest {
    string user_id = 1;
    string organization_id = 2;
    string wallet_id = 3;
}

message RemoveWalletResponse {
    bool removed = 1;
}

message GetWalletsRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetWalletsResponse {
    repeated Wallet wallets = 1;
    int32 total_count = 2;
}

message AddBankAccountRequest {
    string user_id = 1;
    string organization_id = 2;
    BankAccount bank_account = 3;
}

message AddBankAccountResponse {
    BankAccount bank_account = 1;
    bool added = 2;
    bool requires_verification = 3;
}

message RemoveBankAccountRequest {
    string user_id = 1;
    string organization_id = 2;
    string account_id = 3;
}

message RemoveBankAccountResponse {
    bool removed = 1;
}

message GetBankAccountsRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetBankAccountsResponse {
    repeated BankAccount bank_accounts = 1;
    int32 total_count = 2;
}

message AddBrokerAccountRequest {
    string user_id = 1;
    string organization_id = 2;
    BrokerAccount broker_account = 3;
}

message AddBrokerAccountResponse {
    BrokerAccount broker_account = 1;
    bool added = 2;
}

message RemoveBrokerAccountRequest {
    string user_id = 1;
    string organization_id = 2;
    string broker_account_id = 3;
}

message RemoveBrokerAccountResponse {
    bool removed = 1;
}

message GetBrokerAccountsRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetBrokerAccountsResponse {
    repeated BrokerAccount broker_accounts = 1;
    int32 total_count = 2;
}

// Compliance Messages
message GetComplianceQuestionsRequest {
    string organization_id = 1;
    string jurisdiction = 2;
}

message GetComplianceQuestionsResponse {
    repeated ComplianceQuestion questions = 1;
    int32 total_count = 2;
}

message SubmitComplianceAnswersRequest {
    string user_id = 1;
    string organization_id = 2;
    repeated ComplianceAnswer answers = 3;
}

message SubmitComplianceAnswersResponse {
    bool submitted = 1;
    bool requires_review = 2;
    string message = 3;
}

// Document Messages
message UploadDocumentRequest {
    string user_id = 1;
    string organization_id = 2;
    string document_type = 3;
    string document_name = 4;
    bytes document_content = 5;
    string content_type = 6;
}

message UploadDocumentResponse {
    string document_id = 1;
    bool uploaded = 2;
    string document_hash = 3;
}

message GetDocumentsRequest {
    string user_id = 1;
    string organization_id = 2;
    string document_type = 3;
}

message GetDocumentsResponse {
    repeated UserDocumentCompliance documents = 1;
    int32 total_count = 2;
}

message SignDocumentRequest {
    string user_id = 1;
    string organization_id = 2;
    string document_id = 3;
    string signature = 4;
    string ip_address = 5;
    string user_agent = 6;
}

message SignDocumentResponse {
    bool signed = 1;
    google.protobuf.Timestamp signed_at = 2;
    string message = 3;
}

// Multi-Organization Messages
message CloneUserToOrganizationRequest {
    string user_id = 1;
    string source_organization_id = 2;
    string target_organization_id = 3;
    CloneConfiguration config = 4;
}

message CloneConfiguration {
    bool clone_kyc = 1;
    bool clone_trade_profile = 2;
    bool clone_preferences = 3;
    bool send_notification = 4;
    bool require_review = 5;
    bool disable_user_until_review = 6;
}

message CloneUserToOrganizationResponse {
    User user = 1;
    bool cloned = 2;
    bool requires_review = 3;
    string message = 4;
}

message GetUserOrganizationsRequest {
    string user_id = 1;
}

message GetUserOrganizationsResponse {
    repeated OrganizationInfo organizations = 1;
    int32 total_count = 2;
}

message OrganizationInfo {
    string organization_id = 1;
    string organization_name = 2;
    UserStatus status = 3;
    google.protobuf.Timestamp joined_at = 4;
    bool is_default = 5;
}

message SwitchOrganizationRequest{
    string user_id = 1;
    string current_organization_id = 2;
    string target_organization_id = 3;
}

message SwitchOrganizationResponse {
    bool switched = 1;
    User user = 2;
    string message = 3;
}

// Security Messages
message ChangePasswordRequest {
    string user_id = 1;
    string organization_id = 2;
    string current_password = 3;
    string new_password = 4;
}

message ChangePasswordResponse {
    bool changed = 1;
    string message = 2;
}

message EnableMFARequest {
    string user_id = 1;
    string organization_id = 2;
    string method = 3;              // sms, totp, webauthn
    string phone_number = 4;        // For SMS method
}

message EnableMFAResponse {
    bool enabled = 1;
    string secret = 2;              // For TOTP
    string qr_code = 3;             // For TOTP
    repeated string backup_codes = 4;
}

message DisableMFARequest {
    string user_id = 1;
    string organization_id = 2;
    string factor_id = 3;
}

message DisableMFAResponse {
    bool disabled = 1;
}

message GetMFAMethodsRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetMFAMethodsResponse {
    repeated MFAFactor factors = 1;
    bool has_active_mfa = 2;
}

message VerifyMFARequest {
    string user_id = 1;
    string organization_id = 2;
    string factor_id = 3;
    string verification_code = 4;
}

message VerifyMFAResponse {
    bool verified = 1;
    string message = 2;
}

// Preferences Messages
message UpdatePreferencesRequest {
    string user_id = 1;
    string organization_id = 2;
    UserPreferences preferences = 3;
}

message UpdatePreferencesResponse {
    UserPreferences preferences = 1;
    bool updated = 2;
}

message GetPreferencesRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetPreferencesResponse {
    UserPreferences preferences = 1;
    bool found = 2;
}
user-filters.proto - Filters
protobuf
syntax = "proto3";

package user.v1;

import "user.proto";

// User filter for queries
message UserFilter {
    optional UserStatus status = 1;
    optional UserType user_type = 2;
    optional KYCStatus kyc_status = 3;
    optional string country = 4;
    optional google.protobuf.Timestamp created_after = 5;
    optional google.protobuf.Timestamp created_before = 6;
    optional bool email_verified = 7;
    optional bool phone_verified = 8;
    repeated string tags = 9;
    string search_query = 10;
}

// Admin user filter (extended for admin users)
message AdminUserFilter {
    UserFilter base_filter = 1;
    optional bool requires_review = 2;
    optional bool kyc_expiring_soon = 3;
    optional bool has_compliance_flags = 4;
    optional string risk_level = 5;
    optional google.protobuf.Timestamp last_login_after = 6;
    optional google.protobuf.Timestamp last_login_before = 7;
}
adminuser-grpc.proto - Admin User Service
protobuf
syntax = "proto3";

package user.v1;

import "user.proto";
import "user-filters.proto";

// Admin User Service - For administrative operations
service AdminUserService {
    // User management (admin)
    rpc AdminGetUser(AdminGetUserRequest) returns (AdminGetUserResponse);
    rpc AdminListUsers(AdminListUsersRequest) returns (AdminListUsersResponse);
    rpc AdminUpdateUser(AdminUpdateUserRequest) returns (AdminUpdateUserResponse);
    rpc AdminSuspendUser(AdminSuspendUserRequest) returns (AdminSuspendUserResponse);
    rpc AdminReactivateUser(AdminReactivateUserRequest) returns (AdminReactivateUserResponse);
    
    // KYC administration
    rpc AdminReviewKYC(AdminReviewKYCRequest) returns (AdminReviewKYCResponse);
    rpc AdminGetKYCQueue(AdminGetKYCQueueRequest) returns (AdminGetKYCQueueResponse);
    rpc AdminUpdateKYCLevel(AdminUpdateKYCLevelRequest) returns (AdminUpdateKYCLevelResponse);
    
    // Compliance administration
    rpc AdminGetComplianceQueue(AdminGetComplianceQueueRequest) returns (AdminGetComplianceQueueResponse);
    rpc AdminReviewCompliance(AdminReviewComplianceRequest) returns (AdminReviewComplianceResponse);
    
    // Organization administration
    rpc AdminCloneUsersToOrganization(AdminCloneUsersToOrganizationRequest) returns (AdminCloneUsersToOrganizationResponse);
    rpc AdminGetCloneStatus(AdminGetCloneStatusRequest) returns (AdminGetCloneStatusResponse);
    
    // Audit
    rpc AdminGetUserAuditTrail(AdminGetUserAuditTrailRequest) returns (AdminGetUserAuditTrailResponse);
    rpc AdminGetUserHistory(AdminGetUserHistoryRequest) returns (AdminGetUserHistoryResponse);
    
    // Reporting
    rpc AdminGenerateUserReport(AdminGenerateUserReportRequest) returns (AdminGenerateUserReportResponse);
    rpc AdminExportUsers(AdminExportUsersRequest) returns (AdminExportUsersResponse);
}

// Admin request/response messages
message AdminGetUserRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_full_history = 3;
}

message AdminGetUserResponse {
    User user = 1;
    bool found = 2;
    UserAuditSummary audit_summary = 3;
}

message AdminListUsersRequest {
    string organization_id = 1;
    AdminUserFilter filter = 2;
    int32 limit = 3;
    int32 offset = 4;
    string sort_by = 5;
    string sort_order = 6;
}

message AdminListUsersResponse {
    repeated User users = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

message AdminUpdateUserRequest {
    string user_id = 1;
    string organization_id = 2;
    UserDetails user_details = 3;
    string admin_notes = 4;
    bool bypass_review = 5;
}

message AdminUpdateUserResponse {
    User user = 1;
    bool updated = 2;
    string message = 3;
}

message AdminSuspendUserRequest {
    string user_id = 1;
    string organization_id = 2;
    string reason = 3;
    google.protobuf.Timestamp suspend_until = 4;
}

message AdminSuspendUserResponse {
    bool suspended = 1;
    User user = 2;
}

message AdminReactivateUserRequest {
    string user_id = 1;
    string organization_id = 2;
    string reason = 3;
}

message AdminReactivateUserResponse {
    bool reactivated = 1;
    User user = 2;
}

message AdminReviewKYCRequest {
    string user_id = 1;
    string organization_id = 2;
    string kyc_id = 3;
    bool approved = 4;
    string rejection_reason = 5;
    KYCLevel new_level = 6;
    string reviewer_notes = 7;
}

message AdminReviewKYCResponse {
    bool reviewed = 1;
    KYCStatus status = 2;
    KYCLevel level = 3;
}

message AdminGetKYCQueueRequest {
    string organization_id = 1;
    int32 limit = 2;
    int32 offset = 3;
}

message AdminGetKYCQueueResponse {
    repeated KYCQueueItem items = 1;
    int32 total_count = 2;
}

message KYCQueueItem {
    User user = 1;
    KYCDetails kyc_details = 2;
    google.protobuf.Timestamp submitted_at = 3;
    int32 days_pending = 4;
    string priority = 5;
}

message AdminUpdateKYCLevelRequest {
    string user_id = 1;
    string organization_id = 2;
    KYCLevel new_level = 3;
    string reason = 4;
}

message AdminUpdateKYCLevelResponse {
    bool updated = 1;
    KYCLevel level = 2;
}

message AdminGetComplianceQueueRequest {
    string organization_id = 1;
    int32 limit = 2;
    int32 offset = 3;
}

message AdminGetComplianceQueueResponse {
    repeated ComplianceQueueItem items = 1;
    int32 total_count = 2;
}

message ComplianceQueueItem {
    User user = 1;
    repeated ComplianceAnswer answers = 2;
    google.protobuf.Timestamp submitted_at = 3;
    bool requires_review = 4;
}

message AdminReviewComplianceRequest {
    string user_id = 1;
    string organization_id = 2;
    bool approved = 3;
    string reviewer_notes = 4;
}

message AdminReviewComplianceResponse {
    bool reviewed = 1;
    string message = 2;
}

message AdminCloneUsersToOrganizationRequest {
    repeated string user_ids = 1;
    string source_organization_id = 2;
    string target_organization_id = 3;
    CloneConfiguration config = 4;
    string initiated_by = 5;
}

message AdminCloneUsersToOrganizationResponse {
    string batch_id = 1;
    int32 total_users = 2;
    string status = 3;  // pending, processing, completed
}

message AdminGetCloneStatusRequest {
    string batch_id = 1;
}

message AdminGetCloneStatusResponse {
    string status = 1;
    int32 processed = 2;
    int32 total = 3;
    int32 successful = 4;
    int32 failed = 5;
    repeated string failed_users = 6;
    google.protobuf.Timestamp started_at = 7;
    google.protobuf.Timestamp completed_at = 8;
}

message AdminGetUserAuditTrailRequest {
    string user_id = 1;
    string organization_id = 2;
    google.protobuf.Timestamp from_date = 3;
    google.protobuf.Timestamp to_date = 4;
    int32 limit = 5;
    int32 offset = 6;
}

message AdminGetUserAuditTrailResponse {
    repeated AuditEntry entries = 1;
    int32 total_count = 2;
}

message UserAuditSummary {
    int32 total_changes = 1;
    google.protobuf.Timestamp last_change = 2;
    string last_changed_by = 3;
    int32 kyc_updates = 4;
    int32 profile_updates = 5;
    int32 security_updates = 6;
}

message AdminGetUserHistoryRequest {
    string user_id = 1;
    string organization_id = 2;
    google.protobuf.Timestamp from_date = 3;
    google.protobuf.Timestamp to_date = 4;
}

message AdminGetUserHistoryResponse {
    repeated UserHistoryEntry history = 1;
    int32 total_entries = 2;
}

message UserHistoryEntry {
    google.protobuf.Timestamp timestamp = 1;
    string event_type = 2;
    string event_description = 3;
    string performed_by = 4;
    string ip_address = 5;
    map<string, string> details = 6;
}

message AdminGenerateUserReportRequest {
    string organization_id = 1;
    AdminUserFilter filter = 2;
    string report_format = 3;   // CSV, JSON, PDF
    string report_type = 4;      // summary, detailed, kyc, compliance
}

message AdminGenerateUserReportResponse {
    string report_id = 1;
    string download_url = 2;
    int64 file_size_bytes = 3;
    int32 user_count = 4;
    google.protobuf.Timestamp expires_at = 5;
}

message AdminExportUsersRequest {
    string organization_id = 1;
    AdminUserFilter filter = 2;
    string export_format = 3;    // CSV, JSON
    repeated string fields = 4;   // Specific fields to export
}

message AdminExportUsersResponse {
    string export_id = 1;
    string download_url = 2;
    int32 user_count = 3;
    google.protobuf.Timestamp expires_at = 4;
}
Save the file:

Ctrl+O, Enter, Ctrl+X

Now let me create the build script and Go client for the User service:

2. User Build Script
bash
mkdir -p ~/dev/TXdocumentation/user/bin
nano ~/dev/TXdocumentation/user/bin/build.sh
bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting User proto build...${NC}"

# Check if proto files exist
PROTO_FILES=("user.proto" "user-kyc.proto" "user-fundings.proto" "user-compliance.proto" "user-filters.proto" "user-grpc.proto" "adminuser-grpc.proto")
FOUND_FILES=()

for file in "${PROTO_FILES[@]}"; do
    if [ -f "$file" ] || [ -f "proto/$file" ]; then
        FOUND_FILES+=("$file")
    fi
done

if [ ${#FOUND_FILES[@]} -eq 0 ]; then
    echo -e "${RED}Error: No user proto files found in root or proto/ directory${NC}"
    exit 1
fi

echo -e "${BLUE}Found proto files: ${FOUND_FILES[*]}${NC}"

# Determine proto path
if [ -f "user.proto" ]; then
    PROTO_PATH="."
else
    PROTO_PATH="proto"
fi

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

# Generate Go files for each proto
echo -e "${BLUE}Generating Go protobuf files...${NC}"
for proto_file in "${FOUND_FILES[@]}"; do
    if [ -f "${PROTO_PATH}/$proto_file" ]; then
        protoc \
            --go_out=client/go \
            --go_opt=paths=source_relative \
            --go-grpc_out=client/go \
            --go-grpc_opt=paths=source_relative \
            --proto_path=${PROTO_PATH} \
            ${PROTO_PATH}/$proto_file
        echo -e "  Generated: $proto_file"
    fi
done

# Check for TypeScript project
if [ -f "package.json" ] && [ -f "tsconfig.json" ]; then
    echo -e "${BLUE}TypeScript project detected. Generating TypeScript files...${NC}"
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing npm dependencies...${NC}"
        npm install
    fi
    
    for proto_file in "${FOUND_FILES[@]}"; do
        if [ -f "${PROTO_PATH}/$proto_file" ]; then
            if command -v protoc-gen-ts &> /dev/null; then
                protoc \
                    --plugin=protoc-gen-ts=$(which protoc-gen-ts) \
                    --ts_out=client/typescript \
                    --proto_path=${PROTO_PATH} \
                    ${PROTO_PATH}/$proto_file
            fi
            
            if command -v protoc-gen-grpc-web &> /dev/null; then
                protoc \
                    --plugin=protoc-gen-grpc-web=$(which protoc-gen-grpc-web) \
                    --grpc-web_out=import_style=typescript,mode=grpcwebtext:client/typescript \
                    --proto_path=${PROTO_PATH} \
                    ${PROTO_PATH}/$proto_file
            fi
        fi
    done
    
    echo -e "${GREEN}TypeScript files generated successfully${NC}"
else
    echo -e "${YELLOW}Skipping TypeScript generation (package.json or tsconfig.json not found)${NC}"
fi

# Generate documentation
echo -e "${BLUE}Generating documentation...${NC}"
if command -v protoc-gen-doc &> /dev/null; then
    protoc \
        --doc_out=build \
        --doc_opt=markdown,user-api.md \
        --proto_path=${PROTO_PATH} \
        ${PROTO_PATH}/user.proto
    echo -e "${GREEN}Documentation generated${NC}"
fi

# Add generated files to git
echo -e "${YELLOW}Adding generated files to git...${NC}"
git add client/go/*.pb.go 2>/dev/null || true
git add client/typescript/*.ts 2>/dev/null || true
git add build/ 2>/dev/null || true

echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}Generated files:${NC}"
echo "  - client/go/*.pb.go"
echo "  - client/go/*_grpc.pb.go"
if [ -d "client/typescript" ]; then
    echo "  - client/typescript/*.ts"
fi
echo "  - build/user-api.md"
