# Record Service (Record Proto)

The Record proto provides all the functionality required to interact with the record service. Records are items like tax records, compliance documents, transaction histories, audit logs, and other permanent records.

## Overview

The Record service is a gRPC-based system that handles:
- Tax records and reporting
- Compliance documentation
- Transaction records
- Audit trails
- Permanent record storage
- Record verification and authentication
- Record retention and archiving
- Regulatory reporting

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Tax Reporting, Compliance, Audit, Accounting, Analytics) │
└───────────────────────────────────┬─────────────────────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Record Service │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Record │ │ Tax Record │ │ Compliance │ │ Audit │ │
│ │ Management │ │ Engine │ │ Manager │ │ Logger │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────────────┬─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Storage Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Record Store│ │ Archive │ │ S3/OSS │ │ Immutable │ │
│ │ (PostgreSQL)│ │ Store │ │ Storage │ │ Ledger │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Environment Variables

### Required Variables

| Variable | Description | Format | Example |
|----------|-------------|--------|---------|
| `RECORD_STORE` | gRPC endpoint for record store service | `host:port` | `record-store:50070` |
| `RECORD_STORE_TESTING` | Enable test mode with in-memory buffer | `TRUE` | `TRUE` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RECORD_RETENTION_DAYS` | Record retention period in days | `2555` (7 years) |
| `TAX_YEAR_START_MONTH` | Tax year start month | `1` (January) |
| `AUDIT_LOG_ENABLED` | Enable audit logging | `true` |
| `RECORD_ENCRYPTION_ENABLED` | Encrypt sensitive records | `true` |
| `MAX_RECORDS_PER_QUERY` | Maximum records per query | `1000` |
| `ARCHIVE_BUCKET` | Archive storage bucket | `record-archive` |

## Proto Definition

```protobuf
syntax = "proto3";

package record.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/struct.proto";

// Record Service Definition
service RecordService {
    // Record CRUD operations
    rpc CreateRecord(CreateRecordRequest) returns (CreateRecordResponse);
    rpc GetRecord(GetRecordRequest) returns (GetRecordResponse);
    rpc UpdateRecord(UpdateRecordRequest) returns (UpdateRecordResponse);
    rpc DeleteRecord(DeleteRecordRequest) returns (DeleteRecordResponse);
    rpc ListRecords(ListRecordsRequest) returns (ListRecordsResponse);
    
    // Tax record operations
    rpc CreateTaxRecord(CreateTaxRecordRequest) returns (CreateTaxRecordResponse);
    rpc GetTaxRecord(GetTaxRecordRequest) returns (GetTaxRecordResponse);
    rpc GetTaxSummary(GetTaxSummaryRequest) returns (GetTaxSummaryResponse);
    rpc GenerateTaxReport(GenerateTaxReportRequest) returns (GenerateTaxReportResponse);
    rpc GetTaxYearRecords(GetTaxYearRecordsRequest) returns (GetTaxYearRecordsResponse);
    
    // Compliance record operations
    rpc CreateComplianceRecord(CreateComplianceRecordRequest) returns (CreateComplianceRecordResponse);
    rpc GetComplianceStatus(GetComplianceStatusRequest) returns (GetComplianceStatusResponse);
    rpc SubmitRegulatoryReport(SubmitRegulatoryReportRequest) returns (SubmitRegulatoryReportResponse);
    
    // Audit operations
    rpc GetAuditTrail(GetAuditTrailRequest) returns (GetAuditTrailResponse);
    rpc VerifyRecord(VerifyRecordRequest) returns (VerifyRecordResponse);
    
    // Record retention
    rpc ArchiveRecord(ArchiveRecordRequest) returns (ArchiveRecordResponse);
    rpc RestoreRecord(RestoreRecordRequest) returns (RestoreRecordResponse);
    rpc GetRetentionPolicy(GetRetentionPolicyRequest) returns (GetRetentionPolicyResponse);
    
    // Search and export
    rpc SearchRecords(SearchRecordsRequest) returns (SearchRecordsResponse);
    rpc ExportRecords(ExportRecordsRequest) returns (ExportRecordsResponse);
}

// ==================== Core Record Messages ====================

enum RecordType {
    RECORD_TYPE_UNSPECIFIED = 0;
    TAX = 1;                    // Tax record
    COMPLIANCE = 2;             // Compliance document
    TRANSACTION = 3;            // Transaction record
    AUDIT = 4;                  // Audit log entry
    REGULATORY = 5;             // Regulatory filing
    LEGAL = 6;                  // Legal document
    FINANCIAL = 7;              // Financial statement
    USER_CONSENT = 8;           // User consent record
    AGREEMENT = 9;              // Signed agreement
    CERTIFICATE = 10;           // Certificate (KYC, etc.)
    REPORT = 11;                // Generated report
}

enum RecordStatus {
    RECORD_STATUS_UNSPECIFIED = 0;
    ACTIVE = 1;                 // Active record
    ARCHIVED = 2;               // Archived (not deleted)
    DELETED = 3;                // Soft deleted
    PENDING_VERIFICATION = 4;   // Awaiting verification
    VERIFIED = 5;               // Verified authentic
    REJECTED = 6;               // Rejected
    EXPIRED = 7;                // Expired retention
}

// Main Record message
message Record {
    string record_id = 1;               // Unique record ID
    string record_number = 2;           // Human-readable record number
    RecordType record_type = 3;         // Type of record
    RecordStatus status = 4;            // Current status
    
    // Ownership
    string user_id = 5;                 // Associated user
    string organization_id = 6;         // Organization context
    string created_by = 7;              // User who created
    
    // Content
    string title = 8;                   // Record title
    string description = 9;             // Description
    string content_type = 10;           // MIME type (application/json, text/csv, etc.)
    bytes content = 11;                 // Record content (encrypted)
    string content_hash = 12;           // SHA-256 hash for integrity
    
    // Storage
    string storage_path = 13;           // Path in storage
    string storage_bucket = 14;         // Storage bucket name
    int64 size_bytes = 15;              // Record size
    
    // Metadata
    map<string, string> metadata = 16;  // Custom metadata
    repeated string tags = 17;          // Searchable tags
    
    // Verification
    bool verified = 18;                 // Whether record is verified
    string verified_by = 19;            // Who verified
    google.protobuf.Timestamp verified_at = 20;
    string verification_method = 21;    // How verified
    
    // Timestamps
    google.protobuf.Timestamp created_at = 22;
    google.protobuf.Timestamp updated_at = 23;
    google.protobuf.Timestamp archived_at = 24;
    google.protobuf.Timestamp expires_at = 25;  // Retention expiry
    google.protobuf.Timestamp deleted_at = 26;
    
    // Versioning
    int32 version = 27;                 // Record version
    string previous_version_id = 28;    // Link to previous version
    
    // Audit
    string audit_id = 29;               // Associated audit entry
    repeated string references = 30;    // Related record IDs
}

// ==================== Tax Record Messages ====================

enum TaxType {
    TAX_TYPE_UNSPECIFIED = 0;
    CAPITAL_GAINS = 1;          // Capital gains tax
    INCOME_TAX = 2;             // Income tax
    SALES_TAX = 3;              // Sales/VAT tax
    WITHHOLDING_TAX = 4;        // Withholding tax
    CORPORATE_TAX = 5;          // Corporate tax
    PROPERTY_TAX = 6;           // Property/asset tax
}

enum TaxFilingStatus {
    FILING_STATUS_UNSPECIFIED = 0;
    NOT_FILED = 1;              // Not yet filed
    PENDING = 2;                // Filed, pending processing
    FILED = 3;                  // Successfully filed
    AMENDED = 4;                // Amended filing
    REJECTED = 5;               // Rejected by authority
    AUDIT = 6;                  // Under audit
}

message TaxRecord {
    string tax_record_id = 1;
    string user_id = 2;
    string organization_id = 3;
    TaxType tax_type = 4;
    int32 tax_year = 5;
    string tax_period = 6;              // Q1, Q2, Q3, Q4, ANNUAL
    TaxFilingStatus filing_status = 7;
    
    // Financial details
    string total_income = 8;            // Total income (string for precision)
    string total_deductions = 9;        // Total deductions
    string taxable_income = 10;         // Taxable income
    string tax_due = 11;                // Tax amount due
    string tax_paid = 12;               // Tax already paid
    string tax_refund = 13;             // Refund amount (if any)
    string tax_liability = 14;          // Net liability
    
    // Trading specific
    string total_trading_volume = 15;   // Total trading volume
    string total_realized_gain = 16;    // Realized gains
    string total_realized_loss = 17;    // Realized losses
    string net_capital_gain = 18;       // Net capital gain
    int32 total_trades = 19;            // Number of trades
    
    // Asset holdings
    map<string, string> asset_holdings = 20;  // Asset -> value
    map<string, string> asset_cost_basis = 21; // Asset -> cost basis
    
    // Filing details
    string filing_id = 22;              // Authority filing ID
    string filing_authority = 23;       // IRS, HMRC, etc.
    google.protobuf.Timestamp filing_date = 24;
    google.protobuf.Timestamp due_date = 25;
    google.protobuf.Timestamp paid_date = 26;
    
    // Supporting documents
    repeated string supporting_document_ids = 27;
    string tax_form_data = 28;          // Form data (JSON)
    string prepared_by = 29;
    string reviewed_by = 30;
    
    // Additional info
    string notes = 31;
    map<string, string> metadata = 32;
    google.protobuf.Timestamp created_at = 33;
    google.protobuf.Timestamp updated_at = 34;
}

message CreateTaxRecordRequest {
    string user_id = 1;
    string organization_id = 2;
    TaxType tax_type = 3;
    int32 tax_year = 4;
    string tax_period = 5;
    string total_income = 6;
    string total_deductions = 7;
    string tax_paid = 8;
    map<string, string> asset_holdings = 9;
    map<string, string> asset_cost_basis = 10;
    string notes = 11;
    map<string, string> metadata = 12;
}

message CreateTaxRecordResponse {
    TaxRecord tax_record = 1;
    bool created = 2;
    string message = 3;
}

message GetTaxRecordRequest {
    string tax_record_id = 1;
    string user_id = 2;
    string organization_id = 3;
    int32 tax_year = 4;                 // Alternative lookup
    TaxType tax_type = 5;
}

message GetTaxRecordResponse {
    TaxRecord tax_record = 1;
    bool found = 2;
}

message GetTaxSummaryRequest {
    string user_id = 1;
    string organization_id = 2;
    int32 tax_year = 3;
}

message GetTaxSummaryResponse {
    int32 tax_year = 1;
    string total_tax_due = 2;
    string total_tax_paid = 3;
    string total_tax_refund = 4;
    string total_net_liability = 5;
    string total_trading_volume = 6;
    string total_capital_gain = 7;
    int32 total_trades = 8;
    map<string, TaxTypeSummary> tax_type_summaries = 9;
    FilingDeadline next_deadline = 10;
}

message TaxTypeSummary {
    TaxType tax_type = 1;
    string tax_due = 2;
    string tax_paid = 3;
    TaxFilingStatus filing_status = 4;
}

message FilingDeadline {
    TaxType tax_type = 1;
    google.protobuf.Timestamp deadline = 2;
    int32 days_remaining = 3;
}

message GenerateTaxReportRequest {
    string user_id = 1;
    string organization_id = 2;
    int32 tax_year = 3;
    string report_format = 4;           // PDF, CSV, JSON, XML
    bool include_transactions = 5;
    bool include_trade_history = 6;
    string output_language = 7;         // en, es, fr, etc.
}

message GenerateTaxReportResponse {
    string report_id = 1;
    string download_url = 2;
    int64 file_size_bytes = 3;
    google.protobuf.Timestamp generated_at = 4;
    string report_format = 5;
}

message GetTaxYearRecordsRequest {
    string user_id = 1;
    string organization_id = 2;
    int32 tax_year = 3;
    int32 limit = 4;
    int32 offset = 5;
}

message GetTaxYearRecordsResponse {
    repeated TaxRecord tax_records = 1;
    int32 total_count = 2;
}

// ==================== Compliance Record Messages ====================

enum ComplianceType {
    COMPLIANCE_TYPE_UNSPECIFIED = 0;
    KYC = 1;                    // Know Your Customer
    AML = 2;                    // Anti-Money Laundering
    SANCTIONS = 3;              // Sanctions screening
    PEP = 4;                    // Politically Exposed Person
    ACCREDITATION = 5;          // Accredited investor
    LICENSING = 6;              // Professional license
    REGISTRATION = 7;           // Regulatory registration
    CERTIFICATION = 8;          // Compliance certification
}

enum ComplianceStatus {
    COMPLIANCE_STATUS_UNSPECIFIED = 0;
    PENDING = 1;                // Pending review
    IN_REVIEW = 2;              // Under review
    APPROVED = 3;               // Approved
    REJECTED = 4;               // Rejected
    EXPIRED = 5;                // Expired
    SUSPENDED = 6;              // Suspended
    REQUIRES_RENEWAL = 7;       // Needs renewal
}

message ComplianceRecord {
    string compliance_record_id = 1;
    string user_id = 2;
    string organization_id = 3;
    ComplianceType compliance_type = 4;
    ComplianceStatus status = 5;
    
    // Document details
    string document_id = 6;             // Associated document record
    string document_type = 7;           // Passport, ID, Utility Bill, etc.
    string document_number = 8;
    string issuing_authority = 9;
    google.protobuf.Timestamp issued_date = 10;
    google.protobuf.Timestamp expiry_date = 11;
    
    // Verification results
    string verification_score = 12;
    repeated string verification_checks = 13;
    string risk_level = 14;             // low, medium, high
    repeated string flags = 15;         // Compliance flags
    string notes = 16;
    
    // Review details
    string reviewed_by = 17;
    google.protobuf.Timestamp reviewed_at = 18;
    string rejection_reason = 19;
    
    // Timestamps
    google.protobuf.Timestamp submitted_at = 20;
    google.protobuf.Timestamp approved_at = 21;
    google.protobuf.Timestamp expires_at = 22;
    google.protobuf.Timestamp created_at = 23;
    google.protobuf.Timestamp updated_at = 24;
}

message CreateComplianceRecordRequest {
    string user_id = 1;
    string organization_id = 2;
    ComplianceType compliance_type = 3;
    string document_id = 4;
    string document_type = 5;
    string document_number = 6;
    string issuing_authority = 7;
    google.protobuf.Timestamp issued_date = 8;
    google.protobuf.Timestamp expiry_date = 9;
    string notes = 10;
}

message CreateComplianceRecordResponse {
    ComplianceRecord compliance_record = 1;
    bool created = 2;
    string message = 3;
}

message GetComplianceStatusRequest {
    string user_id = 1;
    string organization_id = 2;
    ComplianceType compliance_type = 3;
}

message GetComplianceStatusResponse {
    ComplianceStatus status = 1;
    ComplianceRecord latest_record = 2;
    bool is_compliant = 3;
    repeated string missing_requirements = 4;
    google.protobuf.Timestamp next_renewal_date = 5;
}

message SubmitRegulatoryReportRequest {
    string organization_id = 1;
    string report_type = 2;
    string reporting_period = 3;
    bytes report_content = 4;
    string content_format = 5;
    map<string, string> metadata = 6;
}

message SubmitRegulatoryReportResponse {
    string submission_id = 1;
    bool submitted = 2;
    string confirmation_number = 3;
    google.protobuf.Timestamp submitted_at = 4;
    string message = 5;
}

// ==================== Audit Messages ====================

message AuditEntry {
    string audit_id = 1;
    string record_id = 2;               // Affected record
    string user_id = 3;                 // User who performed action
    string action = 4;                  // CREATE, READ, UPDATE, DELETE, VERIFY
    string previous_state = 5;          // JSON of previous state
    string new_state = 6;               // JSON of new state
    string ip_address = 7;
    string user_agent = 8;
    google.protobuf.Timestamp timestamp = 9;
    string reason = 10;
    map<string, string> metadata = 11;
}

message GetAuditTrailRequest {
    string record_id = 1;
    string user_id = 2;
    google.protobuf.Timestamp from_date = 3;
    google.protobuf.Timestamp to_date = 4;
    int32 limit = 5;
    int32 offset = 6;
}

message GetAuditTrailResponse {
    repeated AuditEntry audit_entries = 1;
    int32 total_count = 2;
}

message VerifyRecordRequest {
    string record_id = 1;
    string verifier_id = 2;
    string verification_method = 3;
    string notes = 4;
}

message VerifyRecordResponse {
    bool verified = 1;
    string verification_hash = 2;
    google.protobuf.Timestamp verified_at = 3;
    string message = 4;
}

// ==================== Record Retention ====================

message ArchiveRecordRequest {
    string record_id = 1;
    string reason = 2;
    string archived_by = 3;
}

message ArchiveRecordResponse {
    bool archived = 1;
    Record record = 2;
    string archive_location = 3;
}

message RestoreRecordRequest {
    string record_id = 1;
    string reason = 2;
    string restored_by = 3;
}

message RestoreRecordResponse {
    bool restored = 1;
    Record record = 2;
}

message GetRetentionPolicyRequest {
    RecordType record_type = 1;
}

message GetRetentionPolicyResponse {
    RecordType record_type = 1;
    int32 retention_days = 2;
    bool requires_approval_for_deletion = 3;
    bool requires_encryption = 4;
    string regulatory_reference = 5;
}

// ==================== CRUD Operations ====================

message CreateRecordRequest {
    RecordType record_type = 1;
    string title = 2;
    string description = 3;
    string content_type = 4;
    bytes content = 5;
    string user_id = 6;
    string organization_id = 7;
    map<string, string> metadata = 8;
    repeated string tags = 9;
    google.protobuf.Timestamp expires_at = 10;
}

message CreateRecordResponse {
    Record record = 1;
    bool created = 2;
    string message = 3;
}

message GetRecordRequest {
    string record_id = 1;
    string record_number = 2;
    string user_id = 3;
    string organization_id = 4;
    bool include_content = 5;
}

message GetRecordResponse {
    Record record = 1;
    bytes content = 2;                  // If include_content true
    bool found = 3;
}

message UpdateRecordRequest {
    string record_id = 1;
    optional string title = 2;
    optional string description = 3;
    optional bytes content = 4;
    map<string, string> metadata = 5;
    repeated string tags = 6;
    string user_id = 7;
    string organization_id = 8;
    string update_reason = 9;
}

message UpdateRecordResponse {
    Record record = 1;
    bool updated = 2;
    int32 new_version = 3;
}

message DeleteRecordRequest {
    string record_id = 1;
    string user_id = 2;
    string organization_id = 3;
    bool permanent = 4;                 // Permanent vs soft delete
    string reason = 5;
}

message DeleteRecordResponse {
    bool success = 1;
    string message = 2;
}

message ListRecordsRequest {
    string user_id = 1;
    string organization_id = 2;
    RecordType record_type = 3;
    RecordStatus status = 4;
    google.protobuf.Timestamp from_date = 5;
    google.protobuf.Timestamp to_date = 6;
    int32 limit = 7;
    int32 offset = 8;
    string sort_by = 9;
    string sort_order = 10;
}

message ListRecordsResponse {
    repeated Record records = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

// ==================== Search and Export ====================

message SearchRecordsRequest {
    string user_id = 1;
    string organization_id = 2;
    string query = 3;                   // Search query
    repeated RecordType record_types = 4;
    repeated string tags = 5;
    google.protobuf.Timestamp from_date = 6;
    google.protobuf.Timestamp to_date = 7;
    int32 limit = 8;
    int32 offset = 9;
}

message SearchRecordsResponse {
    repeated Record records = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

message ExportRecordsRequest {
    string user_id = 1;
    string organization_id = 2;
    repeated string record_ids = 3;
    string export_format = 4;           // CSV, JSON, XML, PDF
    string date_range = 5;
    bool include_deleted = 6;
}

message ExportRecordsResponse {
    string export_id = 1;
    string download_url = 2;
    int64 file_size_bytes = 3;
    int32 record_count = 4;
    google.protobuf.Timestamp expires_at = 5;
}
Building the Required Files
Create the build script:

bash
mkdir -p ~/dev/TXdocumentation/record/bin
nano ~/dev/TXdocumentation/record/bin/build.sh
bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting Record proto build...${NC}"

# Check if proto file exists
if [ ! -f "record.proto" ] && [ ! -f "proto/record.proto" ]; then
    echo -e "${RED}Error: No record.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "record.proto" ]; then
    PROTO_FILE="record.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/record.proto"
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
        --doc_opt=markdown,record-api.md \
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
echo "  - client/go/record.pb.go"
echo "  - client/go/record_grpc.pb.go"
if [ -f "client/typescript/record.ts" ]; then
    echo "  - client/typescript/record.ts"
fi
echo "  - build/record-api.md"
Make it executable:

bash
chmod +x ~/dev/TXdocumentation/record/bin/build.sh
Client Implementation
Go Client
Create the Go client:

bash
nano ~/dev/TXdocumentation/record/client/go/record_client.go
go
package record

import (
    "context"
    "fmt"
    "log"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/metadata"
    
    recordpb "github.com/sologenic/record/client/go"
)

type RecordClient struct {
    client recordpb.RecordServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new record client
func NewRecordClient(addr string) (*RecordClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("RECORD_STORE_TESTING"); testingMode == "TRUE" {
            return &RecordClient{}, nil
        }
        return nil, fmt.Errorf("RECORD_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to record service: %w", err)
    }
    
    return &RecordClient{
        client: recordpb.NewRecordServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *RecordClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *RecordClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *RecordClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Create a new record
func (c *RecordClient) CreateRecord(ctx context.Context, req *recordpb.CreateRecordRequest) (*recordpb.Record, error) {
    if c.client == nil {
        return mockRecord(req), nil
    }
    
    resp, err := c.client.CreateRecord(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create record failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("record creation failed: %s", resp.Message)
    }
    
    return resp.Record, nil
}

// Get record by ID
func (c *RecordClient) GetRecord(ctx context.Context, recordID, userID, orgID string, includeContent bool) (*recordpb.Record, []byte, error) {
    if c.client == nil {
        return nil, nil, nil
    }
    
    req := &recordpb.GetRecordRequest{
        RecordId:       recordID,
        UserId:         userID,
        OrganizationId: orgID,
        IncludeContent: includeContent,
    }
    
    resp, err := c.client.GetRecord(c.getContext(ctx), req)
    if err != nil {
        return nil, nil, fmt.Errorf("get record failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil, nil
    }
    
    return resp.Record, resp.Content, nil
}

// Create tax record
func (c *RecordClient) CreateTaxRecord(ctx context.Context, req *recordpb.CreateTaxRecordRequest) (*recordpb.TaxRecord, error) {
    if c.client == nil {
        return mockTaxRecord(req), nil
    }
    
    resp, err := c.client.CreateTaxRecord(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create tax record failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("tax record creation failed: %s", resp.Message)
    }
    
    return resp.TaxRecord, nil
}

// Get tax summary for a user
func (c *RecordClient) GetTaxSummary(ctx context.Context, userID, orgID string, taxYear int32) (*recordpb.GetTaxSummaryResponse, error) {
    if c.client == nil {
        return &recordpb.GetTaxSummaryResponse{
            TaxYear: taxYear,
        }, nil
    }
    
    req := &recordpb.GetTaxSummaryRequest{
        UserId:         userID,
        OrganizationId: orgID,
        TaxYear:        taxYear,
    }
    
    resp, err := c.client.GetTaxSummary(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get tax summary failed: %w", err)
    }
    
    return resp, nil
}

// Generate tax report
func (c *RecordClient) GenerateTaxReport(ctx context.Context, userID, orgID string, taxYear int32, format string, includeTransactions bool) (*recordpb.GenerateTaxReportResponse, error) {
    if c.client == nil {
        return &recordpb.GenerateTaxReportResponse{
            ReportId:     "test-report-id",
            DownloadUrl:  "https://example.com/report.pdf",
            ReportFormat: format,
        }, nil
    }
    
    req := &recordpb.GenerateTaxReportRequest{
        UserId:               userID,
        OrganizationId:       orgID,
        TaxYear:              taxYear,
        ReportFormat:         format,
        IncludeTransactions:  includeTransactions,
        IncludeTradeHistory:  true,
        OutputLanguage:       "en",
    }
    
    resp, err := c.client.GenerateTaxReport(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("generate tax report failed: %w", err)
    }
    
    return resp, nil
}

// Create compliance record
func (c *RecordClient) CreateComplianceRecord(ctx context.Context, req *recordpb.CreateComplianceRecordRequest) (*recordpb.ComplianceRecord, error) {
    if c.client == nil {
        return mockComplianceRecord(req), nil
    }
    
    resp, err := c.client.CreateComplianceRecord(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create compliance record failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("compliance record creation failed: %s", resp.Message)
    }
    
    return resp.ComplianceRecord, nil
}

// Get compliance status
func (c *RecordClient) GetComplianceStatus(ctx context.Context, userID, orgID string, complianceType recordpb.ComplianceType) (*recordpb.GetComplianceStatusResponse, error) {
    if c.client == nil {
        return &recordpb.GetComplianceStatusResponse{
            Status:       recordpb.ComplianceStatus_APPROVED,
            IsCompliant:  true,
        }, nil
    }
    
    req := &recordpb.GetComplianceStatusRequest{
UserId:         userID,
        OrganizationId: orgID,
        ComplianceType: complianceType,
    }
    
    resp, err := c.client.GetComplianceStatus(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get compliance status failed: %w", err)
    }
    
    return resp, nil
}

// Get audit trail for a record
func (c *RecordClient) GetAuditTrail(ctx context.Context, recordID, userID string, fromDate, toDate time.Time, limit, offset int32) ([]*recordpb.AuditEntry, int32, error) {
    if c.client == nil {
        return []*recordpb.AuditEntry{}, 0, nil
    }
    
    req := &recordpb.GetAuditTrailRequest{
        RecordId: recordID,
        UserId:   userID,
        Limit:    limit,
        Offset:   offset,
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestampFromTime(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestampFromTime(toDate)
    }
    
    resp, err := c.client.GetAuditTrail(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("get audit trail failed: %w", err)
    }
    
    return resp.AuditEntries, resp.TotalCount, nil
}

// Verify a record
func (c *RecordClient) VerifyRecord(ctx context.Context, recordID, verifierID, verificationMethod, notes string) (*recordpb.VerifyRecordResponse, error) {
    if c.client == nil {
        return &recordpb.VerifyRecordResponse{
            Verified:       true,
            VerificationHash: "test-hash",
            VerifiedAt:     timestampNow(),
        }, nil
    }
    
    req := &recordpb.VerifyRecordRequest{
        RecordId:           recordID,
        VerifierId:         verifierID,
        VerificationMethod: verificationMethod,
        Notes:              notes,
    }
    
    resp, err := c.client.VerifyRecord(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("verify record failed: %w", err)
    }
    
    return resp, nil
}

// Archive a record
func (c *RecordClient) ArchiveRecord(ctx context.Context, recordID, reason, archivedBy string) (*recordpb.Record, error) {
    if c.client == nil {
        return &recordpb.Record{
            RecordId: recordID,
            Status:   recordpb.RecordStatus_ARCHIVED,
        }, nil
    }
    
    req := &recordpb.ArchiveRecordRequest{
        RecordId:   recordID,
        Reason:     reason,
        ArchivedBy: archivedBy,
    }
    
    resp, err := c.client.ArchiveRecord(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("archive record failed: %w", err)
    }
    
    if !resp.Archived {
        return nil, fmt.Errorf("archive failed")
    }
    
    return resp.Record, nil
}

// Restore an archived record
func (c *RecordClient) RestoreRecord(ctx context.Context, recordID, reason, restoredBy string) (*recordpb.Record, error) {
    if c.client == nil {
        return &recordpb.Record{
            RecordId: recordID,
            Status:   recordpb.RecordStatus_ACTIVE,
        }, nil
    }
    
    req := &recordpb.RestoreRecordRequest{
        RecordId:   recordID,
        Reason:     reason,
        RestoredBy: restoredBy,
    }
    
    resp, err := c.client.RestoreRecord(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("restore record failed: %w", err)
    }
    
    if !resp.Restored {
        return nil, fmt.Errorf("restore failed")
    }
    
    return resp.Record, nil
}

// Search records
func (c *RecordClient) SearchRecords(ctx context.Context, userID, orgID, query string, recordTypes []recordpb.RecordType, tags []string, fromDate, toDate time.Time, limit, offset int32) ([]*recordpb.Record, int32, error) {
    if c.client == nil {
        return []*recordpb.Record{}, 0, nil
    }
    
    req := &recordpb.SearchRecordsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Query:          query,
        RecordTypes:    recordTypes,
        Tags:           tags,
        Limit:          limit,
        Offset:         offset,
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestampFromTime(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestampFromTime(toDate)
    }
    
    resp, err := c.client.SearchRecords(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("search records failed: %w", err)
    }
    
    return resp.Records, resp.TotalCount, nil
}

// Export records
func (c *RecordClient) ExportRecords(ctx context.Context, userID, orgID string, recordIDs []string, exportFormat, dateRange string) (*recordpb.ExportRecordsResponse, error) {
    if c.client == nil {
        return &recordpb.ExportRecordsResponse{
            ExportId:      "test-export-id",
            DownloadUrl:   "https://example.com/export.csv",
            RecordCount:   int32(len(recordIDs)),
        }, nil
    }
    
    req := &recordpb.ExportRecordsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        RecordIds:      recordIDs,
        ExportFormat:   exportFormat,
        DateRange:      dateRange,
        IncludeDeleted: false,
    }
    
    resp, err := c.client.ExportRecords(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("export records failed: %w", err)
    }
    
    return resp, nil
}

// List records with filters
func (c *RecordClient) ListRecords(ctx context.Context, userID, orgID string, recordType recordpb.RecordType, status recordpb.RecordStatus, fromDate, toDate time.Time, limit, offset int32) ([]*recordpb.Record, int32, error) {
    if c.client == nil {
        return []*recordpb.Record{}, 0, nil
    }
    
    req := &recordpb.ListRecordsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        RecordType:     recordType,
        Status:         status,
        Limit:          limit,
        Offset:         offset,
        SortBy:         "created_at",
        SortOrder:      "desc",
    }
    
    if !fromDate.IsZero() {
        req.FromDate = timestampFromTime(fromDate)
    }
    if !toDate.IsZero() {
        req.ToDate = timestampFromTime(toDate)
    }
    
    resp, err := c.client.ListRecords(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("list records failed: %w", err)
    }
    
    return resp.Records, resp.TotalCount, nil
}

// Get retention policy
func (c *RecordClient) GetRetentionPolicy(ctx context.Context, recordType recordpb.RecordType) (*recordpb.GetRetentionPolicyResponse, error) {
    if c.client == nil {
        return &recordpb.GetRetentionPolicyResponse{
            RecordType:                  recordType,
            RetentionDays:               2555, // 7 years
            RequiresApprovalForDeletion: true,
            RequiresEncryption:          true,
        }, nil
    }
    
    req := &recordpb.GetRetentionPolicyRequest{
        RecordType: recordType,
    }
    
    resp, err := c.client.GetRetentionPolicy(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get retention policy failed: %w", err)
    }
    
    return resp, nil
}

// Submit regulatory report
func (c *RecordClient) SubmitRegulatoryReport(ctx context.Context, orgID, reportType, reportingPeriod string, reportContent []byte, contentFormat string) (*recordpb.SubmitRegulatoryReportResponse, error) {
    if c.client == nil {
        return &recordpb.SubmitRegulatoryReportResponse{
            SubmissionId:       "test-submission-id",
            Submitted:          true,
            ConfirmationNumber: "CONF-12345",
            SubmittedAt:        timestampNow(),
        }, nil
    }
    
    req := &recordpb.SubmitRegulatoryReportRequest{
        OrganizationId:  orgID,
        ReportType:      reportType,
        ReportingPeriod: reportingPeriod,
        ReportContent:   reportContent,
        ContentFormat:   contentFormat,
    }
    
    resp, err := c.client.SubmitRegulatoryReport(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("submit regulatory report failed: %w", err)
    }
    
    return resp, nil
}

// Update record
func (c *RecordClient) UpdateRecord(ctx context.Context, recordID, userID, orgID, updateReason string, title, description *string, content []byte, metadata map[string]string, tags []string) (*recordpb.Record, error) {
    if c.client == nil {
        return &recordpb.Record{
            RecordId: recordID,
            Version:  2,
        }, nil
    }
    
    req := &recordpb.UpdateRecordRequest{
        RecordId:     recordID,
        UserId:       userID,
        OrganizationId: orgID,
        UpdateReason: updateReason,
    }
    
    if title != nil {
        req.Title = &recordpb.UpdateRecordRequest_Title{Title: *title}
    }
    if description != nil {
        req.Description = &recordpb.UpdateRecordRequest_Description{Description: *description}
    }
    if content != nil {
        req.Content = content
    }
    if len(metadata) > 0 {
        req.Metadata = metadata
    }
    if len(tags) > 0 {
        req.Tags = tags
    }
    
    resp, err := c.client.UpdateRecord(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update record failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("record update failed")
    }
    
    return resp.Record, nil
}

// Delete record (soft delete)
func (c *RecordClient) DeleteRecord(ctx context.Context, recordID, userID, orgID, reason string, permanent bool) error {
    if c.client == nil {
        return nil
    }
    
    req := &recordpb.DeleteRecordRequest{
        RecordId:     recordID,
        UserId:       userID,
        OrganizationId: orgID,
        Permanent:    permanent,
        Reason:       reason,
    }
    
    resp, err := c.client.DeleteRecord(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("delete record failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("delete failed: %s", resp.Message)
    }
    
    return nil
}

// Mock functions for testing
func mockRecord(req *recordpb.CreateRecordRequest) *recordpb.Record {
    return &recordpb.Record{
        RecordId:     "mock-record-id",
        RecordNumber: "REC-2024-001",
        RecordType:   req.RecordType,
        Status:       recordpb.RecordStatus_ACTIVE,
        Title:        req.Title,
        Description:  req.Description,
        UserId:       req.UserId,
        Version:      1,
        CreatedAt:    timestampNow(),
        UpdatedAt:    timestampNow(),
    }
}

func mockTaxRecord(req *recordpb.CreateTaxRecordRequest) *recordpb.TaxRecord {
    return &recordpb.TaxRecord{
        TaxRecordId:       "mock-tax-id",
        UserId:            req.UserId,
        TaxType:           req.TaxType,
        TaxYear:           req.TaxYear,
        TaxPeriod:         req.TaxPeriod,
        FilingStatus:      recordpb.TaxFilingStatus_NOT_FILED,
        TotalIncome:       req.TotalIncome,
        TotalDeductions:   req.TotalDeductions,
        TaxPaid:           req.TaxPaid,
        CreatedAt:         timestampNow(),
        UpdatedAt:         timestampNow(),
    }
}

func mockComplianceRecord(req *recordpb.CreateComplianceRecordRequest) *recordpb.ComplianceRecord {
    return &recordpb.ComplianceRecord{
        ComplianceRecordId: "mock-compliance-id",
        UserId:             req.UserId,
        ComplianceType:     req.ComplianceType,
        Status:             recordpb.ComplianceStatus_PENDING,
        DocumentId:         req.DocumentId,
        DocumentType:       req.DocumentType,
        SubmittedAt:        timestampNow(),
        CreatedAt:          timestampNow(),
        UpdatedAt:          timestampNow(),
    }
}

func timestampNow() *google_protobuf.Timestamp {
    return &google_protobuf.Timestamp{
        Seconds: time.Now().Unix(),
        Nanos:   int32(time.Now().Nanosecond()),
    }
}

func timestampFromTime(t time.Time) *google_protobuf.Timestamp {
    return &google_protobuf.Timestamp{
        Seconds: t.Unix(),
        Nanos:   int32(t.Nanosecond()),
    }
}

// Example usage
func main() {
    client, err := NewRecordClient("record-store:50070")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    userID := "user-789"
    
    // Create a tax record
    taxReq := &recordpb.CreateTaxRecordRequest{
        UserId:         userID,
        OrganizationId: orgID,
        TaxType:        recordpb.TaxType_CAPITAL_GAINS,
        TaxYear:        2024,
        TaxPeriod:      "ANNUAL",
        TotalIncome:    "50000.00",
        TotalDeductions: "10000.00",
        TaxPaid:        "8000.00",
        AssetHoldings: map[string]string{
            "TX":  "25000.00",
            "USD": "15000.00",
        },
        AssetCostBasis: map[string]string{
            "TX": "20000.00",
        },
    }
    
    taxRecord, err := client.CreateTaxRecord(ctx, taxReq)
    if err != nil {
        log.Printf("Failed to create tax record: %v", err)
    } else {
        log.Printf("Tax record created: %s for year %d", taxRecord.TaxRecordId, taxRecord.TaxYear)
    }
    
    // Get tax summary
    summary, err := client.GetTaxSummary(ctx, userID, orgID, 2024)
    if err != nil {
        log.Printf("Failed to get tax summary: %v", err)
    } else {
        log.Printf("Tax Summary 2024:")
        log.Printf("  Total Tax Due: $%s", summary.TotalTaxDue)
        log.Printf("  Total Tax Paid: $%s", summary.TotalTaxPaid)
        log.Printf("  Net Liability: $%s", summary.TotalNetLiability)
        log.Printf("  Total Trades: %d", summary.TotalTrades)
    }
    
    // Generate tax report
    report, err := client.GenerateTaxReport(ctx, userID, orgID, 2024, "PDF", true)
    if err != nil {
        log.Printf("Failed to generate tax report: %v", err)
    } else {
        log.Printf("Tax report generated: %s", report.DownloadUrl)
    }
    
    // Create a compliance record (KYC)
    complianceReq := &recordpb.CreateComplianceRecordRequest{
        UserId:           userID,
        OrganizationId:   orgID,
        ComplianceType:   recordpb.ComplianceType_KYC,
        DocumentId:       "doc-123",
        DocumentType:     "PASSPORT",
        DocumentNumber:   "AB123456",
        IssuingAuthority: "US State Department",
        IssuedDate:       timestampFromTime(time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC)),
        ExpiryDate:       timestampFromTime(time.Date(2030, 1, 1, 0, 0, 0, 0, time.UTC)),
    }
    
    compliance, err := client.CreateComplianceRecord(ctx, complianceReq)
    if err != nil {
        log.Printf("Failed to create compliance record: %v", err)
    } else {
        log.Printf("Compliance record created: %s (status: %v)", compliance.ComplianceRecordId, compliance.Status)
    }
    
    // Get compliance status
    complianceStatus, err := client.GetComplianceStatus(ctx, userID, orgID, recordpb.ComplianceType_KYC)
    if err != nil {
        log.Printf("Failed to get compliance status: %v", err)
    } else {
        log.Printf("KYC Status: %v (Compliant: %v)", complianceStatus.Status, complianceStatus.IsCompliant)
        if len(complianceStatus.MissingRequirements) > 0 {
            log.Printf("Missing requirements: %v", complianceStatus.MissingRequirements)
        }
    }
    
    // Create a regular record
    createReq := &recordpb.CreateRecordRequest{
        RecordType:     recordpb.RecordType_FINANCIAL,
        Title:          "Monthly Statement",
        Description:    "January 2024 Statement",
        ContentType:    "application/json",
        Content:        []byte(`{"month":"January","balance":"10000"}`),
        UserId:         userID,
        OrganizationId: orgID,
        Tags:           []string{"statement", "january", "2024"},
        Metadata: map[string]string{
            "period": "monthly",
            "year":   "2024",
        },
    }
    
    record, err := client.CreateRecord(ctx, createReq)
    if err != nil {
        log.Printf("Failed to create record: %v", err)
    } else {
        log.Printf("Record created: %s - %s", record.RecordId, record.Title)
        
        // Verify the record
        verifyResp, err := client.VerifyRecord(ctx, record.RecordId, "auditor-001", "MANUAL_REVIEW", "All documents verified")
        if err != nil {
            log.Printf("Failed to verify record: %v", err)
        } else if verifyResp.Verified {
            log.Printf("Record verified at: %v", verifyResp.VerifiedAt)
        }
    }
    
    // Search for records
    records, total, err := client.SearchRecords(ctx, userID, orgID, "statement", 
        []recordpb.RecordType{recordpb.RecordType_FINANCIAL}, 
        []string{"statement"}, time.Time{}, time.Time{}, 20, 0)
    if err != nil {
        log.Printf("Failed to search records: %v", err)
    } else {
        log.Printf("Found %d records (total: %d)", len(records), total)
        for _, r := range records {
            log.Printf("  - %s: %s (%v)", r.RecordId, r.Title, r.Status)
        }
    }
    
    // Get audit trail
    if record != nil {
        auditEntries, totalAudit, err := client.GetAuditTrail(ctx, record.RecordId, userID, time.Time{}, time.Time{}, 50, 0)
        if err != nil {
            log.Printf("Failed to get audit trail: %v", err)
        } else {
            log.Printf("Audit trail has %d entries (total: %d)", len(auditEntries), totalAudit)
            for _, entry := range auditEntries {
                log.Printf("  - %s: %s by %s at %v", entry.AuditId, entry.Action, entry.UserId, entry.Timestamp)
            }
        }
    }
    
    // Get retention policy
    policy, err := client.GetRetentionPolicy(ctx, recordpb.RecordType_TAX)
    if err != nil {
        log.Printf("Failed to get retention policy: %v", err)
    } else {
        log.Printf("Tax records retention: %d days", policy.RetentionDays)
        log.Printf("Requires encryption: %v", policy.RequiresEncryption)
    }
}
Docker Compose Example
bash
nano ~/dev/TXdocumentation/record/docker-compose.yml
yaml
version: '3.8'

services:
  record-service:
    image: sologenic/record-service:latest
    environment:
      - RECORD_SERVICE_PORT=50070
      - RECORD_STORE=record-store:50070
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=records
      - POSTGRES_USER=record_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - S3_ENDPOINT=minio:9000
      - S3_BUCKET=record-storage
      - S3_ACCESS_KEY=${S3_ACCESS_KEY}
      - S3_SECRET_KEY=${S3_SECRET_KEY}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - RECORD_RETENTION_DAYS=2555
      - TAX_YEAR_START_MONTH=1
      - AUDIT_LOG_ENABLED=true
      - RECORD_ENCRYPTION_ENABLED=true
      - MAX_RECORDS_PER_QUERY=1000
      - LOG_LEVEL=info
    ports:
      - "50070:50070"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
      - minio
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50070"]
      interval: 30s
      timeout: 10s
      retries: 3

  record-store:
    image: sologenic/record-store:latest
    environment:
      - RECORD_STORE_PORT=50071
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=records
      - POSTGRES_USER=record_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "50071:50071"
    networks:
      - internal
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=records
      - POSTGRES_USER=record_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U record_user -d records"]
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
Environment Setup (.env file)
bash
nano ~/dev/TXdocumentation/record/.env
bash
# Database Configuration
DB_PASSWORD=your_secure_password

# S3/MinIO Configuration
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin123

# Service Configuration
RECORD_STORE=record-store:50071
RECORD_STORE_TESTING=FALSE

# Record Retention
RECORD_RETENTION_DAYS=2555
TAX_YEAR_START_MONTH=1

# Security
AUDIT_LOG_ENABLED=true
RECORD_ENCRYPTION_ENABLED=true

# Performance
MAX_RECORDS_PER_QUERY=1000

# Logging
LOG_LEVEL=info
Database Schema (Reference)
sql
-- Records table
CREATE TABLE records (
    record_id UUID PRIMARY KEY,
    record_number VARCHAR(50) UNIQUE NOT NULL,
    record_type VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    organization_id VARCHAR(100),
    title VARCHAR(255),
    description TEXT,
    content_type VARCHAR(50),
    content_hash VARCHAR(64),
    storage_path TEXT,
    storage_bucket VARCHAR(100),
    size_bytes BIGINT,
    verified BOOLEAN DEFAULT FALSE,
    verified_by VARCHAR(100),
    verified_at TIMESTAMP,
    version INTEGER DEFAULT 1,
    previous_version_id UUID,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    archived_at TIMESTAMP,
    expires_at TIMESTAMP,
    deleted_at TIMESTAMP,
    INDEX idx_user_status (user_id, status),
    INDEX idx_record_type (record_type),
    INDEX idx_created_at (created_at)
);

-- Tax records table
CREATE TABLE tax_records (
    tax_record_id UUID PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    organization_id VARCHAR(100),
    tax_type VARCHAR(30) NOT NULL,
    tax_year INTEGER NOT NULL,
    tax_period VARCHAR(10),
    filing_status VARCHAR(20),
    total_income DECIMAL(40,18),
    total_deductions DECIMAL(40,18),
    taxable_income DECIMAL(40,18),
    tax_due DECIMAL(40,18),
    tax_paid DECIMAL(40,18),
    tax_refund DECIMAL(40,18),
    net_capital_gain DECIMAL(40,18),
    total_trades INTEGER,
    filing_id VARCHAR(100),
    filing_authority VARCHAR(100),
    filing_date TIMESTAMP,
    due_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    INDEX idx_user_year (user_id, tax_year),
    INDEX idx_filing_status (filing_status)
);

-- Compliance records table
CREATE TABLE compliance_records (
    compliance_record_id UUID PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    organization_id VARCHAR(100),
    compliance_type VARCHAR(30) NOT NULL,
    status VARCHAR(20) NOT NULL,
    document_id VARCHAR(100),
    document_type VARCHAR(50),
    document_number VARCHAR(100),
    issuing_authority VARCHAR(100),
    issued_date DATE,
    expiry_date DATE,
    verification_score DECIMAL(5,2),
    risk_level VARCHAR(10),
    reviewed_by VARCHAR(100),
    reviewed_at TIMESTAMP,
    rejection_reason TEXT,
    submitted_at TIMESTAMP,
    approved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    INDEX idx_user_type (user_id, compliance_type),
    INDEX idx_status (status),
    INDEX idx_expiry (expiry_date)
);

-- Audit entries table
CREATE TABLE audit_entries (
    audit_id UUID PRIMARY KEY,
    record_id UUID REFERENCES records(record_id),
    user_id VARCHAR(100) NOT NULL,
    action VARCHAR(20) NOT NULL,
    previous_state JSONB,
    new_state JSONB,
    ip_address INET,
    user_agent TEXT,
    reason TEXT,
    metadata JSONB,
    timestamp TIMESTAMPTZ NOT NULL,
    INDEX idx_record (record_id),
    INDEX idx_user (user_id),
    INDEX idx_timestamp (timestamp)
);

-- Record tags junction table
CREATE TABLE record_tags (
    record_id UUID REFERENCES records(record_id),
    tag VARCHAR(100),
    PRIMARY KEY (record_id, tag)
);
Testing Mode
The client automatically detects test mode when RECORD_STORE_TESTING=TRUE is set:

bash
# Run in test mode
export RECORD_STORE_TESTING=TRUE
go test ./...
Error Handling
go
// Example error handling
record, err := client.CreateRecord(ctx, req)
if err != nil {
    if strings.Contains(err.Error(), "RECORD_EXISTS") {
        // Handle duplicate record
    } else if strings.Contains(err.Error(), "INVALID_CONTENT") {
        // Handle invalid content
    } else if strings.Contains(err.Error(), "STORAGE_ERROR") {
        // Handle storage failure
    } else if strings.Contains(err.Error(), "ENCRYPTION_FAILED") {
        // Handle encryption error
    }
    log.Printf("Error: %v", err)
}
License
This documentation is part of the TX Marketplace platform.

