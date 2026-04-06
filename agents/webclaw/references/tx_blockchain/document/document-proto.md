# Document Profile Service (Document Proto)

The Document Profile proto provides all the functionality required to interact with the document service. It supports document management, versioning, access control, and document processing workflows.

## Overview

The Document Profile service is a gRPC-based system that handles:
- Document upload, storage, and retrieval
- Document versioning and history
- Document metadata management
- Access control and permissions
- Document validation and verification
- Document signing (digital signatures)
- Document templates
- Document search and indexing

## Architecture
┌─────────────────────────────────────────────────────────┐
│ Client Applications │
│ (KYC/AML, Trading, Compliance, User Profiles) │
└───────────────────┬─────────────────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────────────────┐
│ Document Profile Service │
│ - Document CRUD │
│ - Version Control │
│ - Access Management │
│ - Digital Signing │
│ - Template Engine │
└───────────────────┬─────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Storage Layer │
│ - Document Store (PostgreSQL + S3) │
│ - Metadata Store (PostgreSQL) │
│ - Cache Layer (Redis) │
│ - Search Index (Elasticsearch) │
└─────────────────────────────────────────────────────────┘

text

## Environment Variables

### Required Variables

| Variable | Description | Format | Example |
|----------|-------------|--------|---------|
| `DOCUMENT_STORE` | gRPC endpoint for document store service | `host:port` | `document-store:50064` |
| `DOCUMENT_STORE_TESTING` | Enable test mode with in-memory buffer | `TRUE` | `TRUE` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MAX_DOCUMENT_SIZE_MB` | Maximum document size in MB | `10` |
| `ALLOWED_FILE_TYPES` | Comma-separated allowed MIME types | `application/pdf,image/jpeg,image/png` |
| `DOCUMENT_RETENTION_DAYS` | Document retention period | `2555` (7 years) |
| `SIGNATURE_REQUIRED` | Require digital signatures | `true` |
| `ENCRYPT_AT_REST` | Enable encryption at rest | `true` |
| `VERSION_LIMIT` | Maximum versions per document | `100` |

## Proto Definition

```protobuf
syntax = "proto3";

package document.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Document Profile Service Definition
service DocumentProfileService {
    // Document CRUD operations
    rpc CreateDocument(CreateDocumentRequest) returns (CreateDocumentResponse);
    rpc GetDocument(GetDocumentRequest) returns (GetDocumentResponse);
    rpc UpdateDocument(UpdateDocumentRequest) returns (UpdateDocumentResponse);
    rpc DeleteDocument(DeleteDocumentRequest) returns (DeleteDocumentResponse);
    
    // Document content operations
    rpc UploadDocumentContent(stream UploadDocumentContentRequest) returns (UploadDocumentContentResponse);
    rpc DownloadDocumentContent(DownloadDocumentContentRequest) returns (stream DownloadDocumentContentResponse);
    rpc GetDocumentPreview(GetDocumentPreviewRequest) returns (GetDocumentPreviewResponse);
    
    // Version management
    rpc GetDocumentVersions(GetDocumentVersionsRequest) returns (GetDocumentVersionsResponse);
    rpc GetDocumentVersion(GetDocumentVersionRequest) returns (GetDocumentVersionResponse);
    rpc RestoreDocumentVersion(RestoreDocumentVersionRequest) returns (RestoreDocumentVersionResponse);
    
    // Document signing
    rpc RequestDocumentSignature(RequestDocumentSignatureRequest) returns (RequestDocumentSignatureResponse);
    rpc SignDocument(SignDocumentRequest) returns (SignDocumentResponse);
    rpc GetSignatureStatus(GetSignatureStatusRequest) returns (GetSignatureStatusResponse);
    rpc VerifyDocumentSignature(VerifyDocumentSignatureRequest) returns (VerifyDocumentSignatureResponse);
    
    // Document templates
    rpc CreateDocumentTemplate(CreateDocumentTemplateRequest) returns (CreateDocumentTemplateResponse);
    rpc GetDocumentTemplate(GetDocumentTemplateRequest) returns (GetDocumentTemplateResponse);
    rpc ListDocumentTemplates(ListDocumentTemplatesRequest) returns (ListDocumentTemplatesResponse);
    rpc GenerateDocumentFromTemplate(GenerateDocumentFromTemplateRequest) returns (GenerateDocumentFromTemplateResponse);
    
    // Access control
    rpc ShareDocument(ShareDocumentRequest) returns (ShareDocumentResponse);
    rpc RevokeDocumentAccess(RevokeDocumentAccessRequest) returns (RevokeDocumentAccessResponse);
    rpc GetDocumentAccess(GetDocumentAccessRequest) returns (GetDocumentAccessResponse);
    
    // Search and listing
    rpc ListDocuments(ListDocumentsRequest) returns (ListDocumentsResponse);
    rpc SearchDocuments(SearchDocumentsRequest) returns (SearchDocumentsResponse);
    rpc GetDocumentsByType(GetDocumentsByTypeRequest) returns (GetDocumentsByTypeResponse);
    
    // Document validation
    rpc ValidateDocument(ValidateDocumentRequest) returns (ValidateDocumentResponse);
    rpc VerifyDocumentAuthenticity(VerifyDocumentAuthenticityRequest) returns (VerifyDocumentAuthenticityResponse);
    
    // Compliance
    rpc GetComplianceDocuments(GetComplianceDocumentsRequest) returns (GetComplianceDocumentsResponse);
    rpc ArchiveDocument(ArchiveDocumentRequest) returns (ArchiveDocumentResponse);
}

// ==================== Document Messages ====================

message Document {
    string document_id = 1;             // Unique document ID
    string document_type = 2;           // kyc_id, proof_of_address, trading_agreement, etc.
    string document_name = 3;           // User-friendly name
    string description = 4;             // Document description
    string mime_type = 5;               // File MIME type
    int64 file_size_bytes = 6;          // File size in bytes
    string file_hash = 7;               // SHA-256 hash for integrity
    
    // Ownership and access
    string owner_id = 8;                // User ID of owner
    string organization_id = 9;         // Organization context
    repeated string shared_with = 10;   // User IDs with access
    map<string, string> permissions = 11; // Fine-grained permissions
    
    // Version info
    int32 version = 12;                 // Current version number
    int32 version_count = 13;           // Total versions
    
    // Status
    string status = 14;                 // draft, pending, signed, archived, deleted
    bool is_verified = 15;              // Whether document is verified
    bool is_signed = 16;                // Whether document is digitally signed
    
    // Signatures
    repeated Signature signatures = 17; // Digital signatures
    
    // Metadata
    map<string, string> metadata = 18;  // Custom metadata
    google.protobuf.Timestamp created_at = 19;
    google.protobuf.Timestamp updated_at = 20;
    google.protobuf.Timestamp expires_at = 21;
    google.protobuf.Timestamp archived_at = 22;
    
    // Storage references
    string storage_path = 23;           // Path in storage
    string preview_url = 24;            // Preview image URL
    string download_url = 25;           // Temporary download URL
}

message Signature {
    string signature_id = 1;
    string signer_id = 2;
    string signer_name = 3;
    string signer_email = 4;
    string signature_data = 5;          // Digital signature
    string certificate_id = 6;          // Certificate identifier
    google.protobuf.Timestamp signed_at = 7;
    string ip_address = 8;
    string user_agent = 9;
    bool is_valid = 10;
}

message DocumentTemplate {
    string template_id = 1;
    string template_name = 2;
    string template_type = 3;
    string content = 4;                 // Template content (HTML, Markdown)
    map<string, string> variables = 5;  // Available variables
    string organization_id = 6;
    string created_by = 7;
    google.protobuf.Timestamp created_at = 8;
    google.protobuf.Timestamp updated_at = 9;
    bool is_active = 10;
}

// ==================== CRUD Requests/Responses ====================

message CreateDocumentRequest {
    string document_type = 1;
    string document_name = 2;
    string description = 3;
    string mime_type = 4;
    bytes content = 5;                  // Document content (for small files)
    map<string, string> metadata = 6;
    string owner_id = 7;
    string organization_id = 8;
    repeated string shared_with = 9;
    google.protobuf.Timestamp expires_at = 10;
}

message CreateDocumentResponse {
    Document document = 1;
    bool created = 2;
    string upload_url = 3;              // For large file uploads
}

message GetDocumentRequest {
    string document_id = 1;
    string organization_id = 2;
    bool include_content = 3;           // Include document content
}

message GetDocumentResponse {
    Document document = 1;
    bytes content = 2;                  // Optional document content
    bool found = 3;
}

message UpdateDocumentRequest {
    string document_id = 1;
    optional string document_name = 2;
    optional string description = 3;
    map<string, string> metadata = 4;
    string organization_id = 5;
    bytes content = 6;                  // New content (creates new version)
}

message UpdateDocumentResponse {
    Document document = 1;
    bool updated = 2;
    bool new_version_created = 3;
    int32 new_version_number = 4;
}

message DeleteDocumentRequest {
    string document_id = 1;
    string organization_id = 2;
    bool permanent = 3;                 // Permanent deletion vs soft delete
}

message DeleteDocumentResponse {
    bool success = 1;
    string message = 2;
}

// ==================== Content Upload/Download ====================

message UploadDocumentContentRequest {
    string document_id = 1;
    string organization_id = 2;
    bytes chunk = 3;                    // File chunk
    int32 chunk_number = 4;
    int32 total_chunks = 5;
    string file_name = 6;
    string mime_type = 7;
}

message UploadDocumentContentResponse {
    bool success = 1;
    string document_id = 2;
    int32 uploaded_chunks = 3;
    string message = 4;
}

message DownloadDocumentContentRequest {
    string document_id = 1;
    string organization_id = 2;
    string version = 3;                 // Optional specific version
}

message DownloadDocumentContentResponse {
    bytes chunk = 1;
    int32 chunk_number = 2;
    int32 total_chunks = 3;
    string document_id = 4;
}

message GetDocumentPreviewRequest {
    string document_id = 1;
    string organization_id = 2;
    int32 page = 3;                     // Page number for preview
    int32 width = 4;                    // Preview width
    int32 height = 5;                   // Preview height
}

message GetDocumentPreviewResponse {
    bytes preview_image = 1;
    string mime_type = 2;
    int32 total_pages = 3;
}

// ==================== Version Management ====================

message DocumentVersion {
    int32 version = 1;
    string document_id = 2;
    string file_hash = 3;
    int64 file_size_bytes = 4;
    string created_by = 5;
    string change_note = 6;
    google.protobuf.Timestamp created_at = 7;
    map<string, string> metadata = 8;
}

message GetDocumentVersionsRequest {
    string document_id = 1;
    string organization_id = 2;
    int32 limit = 3;
    int32 offset = 4;
}

message GetDocumentVersionsResponse {
    repeated DocumentVersion versions = 1;
    int32 total_count = 2;
}

message GetDocumentVersionRequest {
    string document_id = 1;
    int32 version = 2;
    string organization_id = 3;
    bool include_content = 4;
}

message GetDocumentVersionResponse {
    DocumentVersion version = 1;
    bytes content = 2;
    bool found = 3;
}

message RestoreDocumentVersionRequest {
    string document_id = 1;
    int32 version = 2;
    string organization_id = 3;
    string change_note = 4;
}

message RestoreDocumentVersionResponse {
    Document document = 1;
    bool success = 2;
    int32 new_version = 3;
}

// ==================== Digital Signatures ====================

message RequestDocumentSignatureRequest {
    string document_id = 1;
    repeated string signer_ids = 2;
    repeated string signer_emails = 3;
    string signing_order = 4;           // sequential, parallel
    google.protobuf.Timestamp deadline = 5;
    string organization_id = 6;
    string message = 7;                 // Optional message to signers
}

message RequestDocumentSignatureResponse {
    bool success = 1;
    repeated string signature_request_ids = 2;
    string message = 3;
}

message SignDocumentRequest {
    string document_id = 1;
    string signature_data = 2;          // Digital signature
    string certificate_id = 3;          // Certificate to use
    string organization_id = 4;
    string ip_address = 5;
    string user_agent = 6;
}

message SignDocumentResponse {
    Signature signature = 1;
    bool success = 2;
    string message = 3;
}

message GetSignatureStatusRequest {
    string document_id = 1;
    string organization_id = 2;
}

message GetSignatureStatusResponse {
    string document_id = 1;
    string status = 2;                  // unsigned, partial, signed, expired
    repeated Signature signatures = 3;
    int32 required_signatures = 4;
    int32 completed_signatures = 5;
}

message VerifyDocumentSignatureRequest {
    string document_id = 1;
    string signature_id = 2;
    string organization_id = 3;
}

message VerifyDocumentSignatureResponse {
    bool valid = 1;
    string certificate_info = 2;
    google.protobuf.Timestamp verified_at = 3;
    string verification_details = 4;
}

// ==================== Document Templates ====================

message CreateDocumentTemplateRequest {
    string template_name = 1;
    string template_type = 2;
    string content = 3;
    map<string, string> variables = 4;
    string organization_id = 5;
}

message CreateDocumentTemplateResponse {
    DocumentTemplate template = 1;
    bool created = 2;
}

message GetDocumentTemplateRequest {
    string template_id = 1;
    string organization_id = 2;
}

message GetDocumentTemplateResponse {
    DocumentTemplate template = 1;
    bool found = 2;
}

message ListDocumentTemplatesRequest {
    string organization_id = 1;
    string template_type = 2;
    int32 limit = 3;
    int32 offset = 4;
}

message ListDocumentTemplatesResponse {
    repeated DocumentTemplate templates = 1;
    int32 total_count = 2;
}

message GenerateDocumentFromTemplateRequest {
    string template_id = 1;
    map<string, string> variables = 2;
    string document_name = 3;
    string document_type = 4;
    string owner_id = 5;
    string organization_id = 6;
    map<string, string> metadata = 7;
}

message GenerateDocumentFromTemplateResponse {
    Document document = 1;
    bool generated = 2;
    string content_preview = 3;
}

// ==================== Access Control ====================

message ShareDocumentRequest {
    string document_id = 1;
    repeated string user_ids = 2;
    repeated string emails = 3;
    string permission = 4;              // view, edit, sign, admin
    google.protobuf.Timestamp expires_at = 5;
    string organization_id = 6;
}

message ShareDocumentResponse {
    bool success = 1;
    repeated string shared_with = 2;
    string message = 3;
}

message RevokeDocumentAccessRequest {
    string document_id = 1;
    string user_id = 2;
    string organization_id = 3;
}

message RevokeDocumentAccessResponse {
    bool success = 1;
    string message = 2;
}

message GetDocumentAccessRequest {
    string document_id = 1;
    string organization_id = 2;
}

message GetDocumentAccessResponse {
    string owner_id = 1;
    repeated string shared_with = 2;
    map<string, string> permissions = 3;
}

// ==================== Search and Listing ====================

message ListDocumentsRequest {
    string owner_id = 1;
    string document_type = 2;
    string status = 3;
    string organization_id = 4;
    int32 limit = 5;
    int32 offset = 6;
    string sort_by = 7;                 // created_at, updated_at, name
    string sort_order = 8;              // asc, desc
}

message ListDocumentsResponse {
    repeated Document documents = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

message SearchDocumentsRequest {
    string query = 1;
    string organization_id = 2;
    repeated string document_types = 3;
    string owner_id = 4;
    google.protobuf.Timestamp from_date = 5;
    google.protobuf.Timestamp to_date = 6;
    int32 limit = 7;
    int32 offset = 8;
}

message SearchDocumentsResponse {
    repeated Document documents = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

message GetDocumentsByTypeRequest {
    string document_type = 1;
    string owner_id = 2;
    string organization_id = 3;
    int32 limit = 4;
    int32 offset = 5;
}

message GetDocumentsByTypeResponse {
    repeated Document documents = 1;
    int32 total_count = 2;
}

// ==================== Validation and Compliance ====================

message ValidateDocumentRequest {
    string document_id = 1;
    string organization_id = 2;
    repeated string validation_rules = 3; // Specific rules to check
}

message ValidateDocumentResponse {
    bool valid = 1;
    repeated ValidationError errors = 2;
    repeated ValidationWarning warnings = 3;
}

message ValidationError {
    string field = 1;
    string message = 2;
    string code = 3;
}

message ValidationWarning {
    string field = 1;
    string message = 2;
    string code = 3;
}

message VerifyDocumentAuthenticityRequest {
    string document_id = 1;
    string organization_id = 2;
}

message VerifyDocumentAuthenticityResponse {
    bool authentic = 1;
    bool tampered = 2;
    string original_hash = 3;
    string current_hash = 4;
    google.protobuf.Timestamp last_verified = 5;
}

message GetComplianceDocumentsRequest {
    string user_id = 1;
    string organization_id = 2;
    string compliance_type = 3;         // kyc, aml, trading
}

message GetComplianceDocumentsResponse {
    repeated Document documents = 1;
    map<string, bool> requirements_met = 2;
}

message ArchiveDocumentRequest {
    string document_id = 1;
    string organization_id = 2;
    string archive_reason = 3;
}

message ArchiveDocumentResponse {
    bool success = 1;
    Document document = 2;
}
Building the Required Files
Create the build script:

bash
mkdir -p ~/dev/TXdocumentation/document/bin
nano ~/dev/TXdocumentation/document/bin/build.sh
bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting Document proto build...${NC}"

# Check if proto file exists
if [ ! -f "document.proto" ] && [ ! -f "proto/document.proto" ]; then
    echo -e "${RED}Error: No document.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "document.proto" ]; then
    PROTO_FILE="document.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/document.proto"
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
        --doc_opt=markdown,document-api.md \
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
echo "  - client/go/document.pb.go"
echo "  - client/go/document_grpc.pb.go"
if [ -f "client/typescript/document.ts" ]; then
    echo "  - client/typescript/document.ts"
fi
echo "  - build/document-api.md"
Make it executable:

bash
chmod +x ~/dev/TXdocumentation/document/bin/build.sh
Client Implementation
Go Client
Create the Go client:

bash
nano ~/dev/TXdocumentation/document/client/go/document_client.go
go
package document

import (
    "context"
    "fmt"
    "io"
    "log"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/metadata"
    
    documentpb "github.com/sologenic/document/client/go"
)

type DocumentClient struct {
    client documentpb.DocumentProfileServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new document client
func NewDocumentClient(addr string) (*DocumentClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("DOCUMENT_STORE_TESTING"); testingMode == "TRUE" {
            // Use in-memory test client
            return &DocumentClient{}, nil
        }
        return nil, fmt.Errorf("DOCUMENT_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to document service: %w", err)
    }
    
    return &DocumentClient{
        client: documentpb.NewDocumentProfileServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *DocumentClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *DocumentClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *DocumentClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Create a new document
func (c *DocumentClient) CreateDocument(ctx context.Context, req *documentpb.CreateDocumentRequest) (*documentpb.CreateDocumentResponse, error) {
    if c.client == nil {
        // Mock response for testing
        return &documentpb.CreateDocumentResponse{
            Document: &documentpb.Document{
                DocumentId:   "test-doc-id",
                DocumentName: req.DocumentName,
                Status:       "draft",
                CreatedAt:    timestampNow(),
            },
            Created: true,
        }, nil
    }
    
    resp, err := c.client.CreateDocument(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create document failed: %w", err)
    }
    
    return resp, nil
}

// Get a document by ID
func (c *DocumentClient) GetDocument(ctx context.Context, documentID, orgID string, includeContent bool) (*documentpb.GetDocumentResponse, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &documentpb.GetDocumentRequest{
        DocumentId:     documentID,
        OrganizationId: orgID,
        IncludeContent: includeContent,
    }
    
    resp, err := c.client.GetDocument(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get document failed: %w", err)
    }
    
    return resp, nil
}

// Update a document
func (c *DocumentClient) UpdateDocument(ctx context.Context, documentID, orgID string, name, description *string, metadata map[string]string, content []byte) (*documentpb.UpdateDocumentResponse, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &documentpb.UpdateDocumentRequest{
        DocumentId:     documentID,
        OrganizationId: orgID,
        Metadata:       metadata,
    }
    
    if name != nil {
        req.DocumentName = &documentpb.UpdateDocumentRequest_DocumentName{DocumentName: *name}
    }
    if description != nil {
        req.Description = &documentpb.UpdateDocumentRequest_Description{Description: *description}
    }
    if content != nil {
        req.Content = content
    }
    
    resp, err := c.client.UpdateDocument(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update document failed: %w", err)
    }
    
    return resp, nil
}

// Delete a document
func (c *DocumentClient) DeleteDocument(ctx context.Context, documentID, orgID string, permanent bool) error {
    if c.client == nil {
        return nil
    }
    
    req := &documentpb.DeleteDocumentRequest{
        DocumentId:     documentID,
        OrganizationId: orgID,
        Permanent:      permanent,
    }
    
    resp, err := c.client.DeleteDocument(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("delete document failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("delete failed: %s", resp.Message)
    }
    
    return nil
}

// Upload document content in chunks
func (c *DocumentClient) UploadDocumentContent(ctx context.Context, documentID, orgID, fileName, mimeType string, reader io.Reader) error {
    if c.client == nil {
        return nil
    }
    
    stream, err := c.client.UploadDocumentContent(c.getContext(ctx))
    if err != nil {
        return fmt.Errorf("failed to create upload stream: %w", err)
    }
    
    const chunkSize = 1024 * 1024 // 1MB chunks
    buf := make([]byte, chunkSize)
    chunkNumber := 1
    var totalChunks int
    
    // Read file to determine total chunks
    fileContent, err := io.ReadAll(reader)
    if err != nil {
        return fmt.Errorf("failed to read file: %w", err)
    }
    
    totalChunks = (len(fileContent) + chunkSize - 1) / chunkSize
    
    // Send chunks
    for i := 0; i < len(fileContent); i += chunkSize {
        end := i + chunkSize
        if end > len(fileContent) {
            end = len(fileContent)
        }
        
        req := &documentpb.UploadDocumentContentRequest{
            DocumentId:     documentID,
            OrganizationId: orgID,
            Chunk:          fileContent[i:end],
            ChunkNumber:    int32(chunkNumber),
            TotalChunks:    int32(totalChunks),
            FileName:       fileName,
            MimeType:       mimeType,
        }
        
        if err := stream.Send(req); err != nil {
            return fmt.Errorf("failed to send chunk %d: %w", chunkNumber, err)
        }
        
        chunkNumber++
    }
    
    resp, err := stream.CloseAndRecv()
    if err != nil {
        return fmt.Errorf("failed to complete upload: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("upload failed: %s", resp.Message)
    }
    
    log.Printf("Upload complete: %d chunks uploaded", resp.UploadedChunks)
    return nil
}

// Download document content
func (c *DocumentClient) DownloadDocumentContent(ctx context.Context, documentID, orgID, version string) ([]byte, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &documentpb.DownloadDocumentContentRequest{
        DocumentId:     documentID,
        OrganizationId: orgID,
        Version:        version,
    }
    
    stream, err := c.client.DownloadDocumentContent(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("failed to create download stream: %w", err)
    }
    
    var content []byte
    for {
        resp, err := stream.Recv()
        if err == io.EOF {
            break
        }
        if err != nil {
            return nil, fmt.Errorf("failed to receive chunk: %w", err)
        }
        
        content = append(content, resp.Chunk...)
    }
    
    return content, nil
}

// List documents
func (c *DocumentClient) ListDocuments(ctx context.Context, ownerID, docType, status, orgID string, limit, offset int32) ([]*documentpb.Document, int32, error) {
    if c.client == nil {
        return []*documentpb.Document{}, 0, nil
    }
    
    req := &documentpb.ListDocumentsRequest{
        OwnerId:        ownerID,
        DocumentType:   docType,
        Status:         status,
        OrganizationId: orgID,
        Limit:          limit,
        Offset:         offset,
        SortBy:         "created_at",
        SortOrder:      "desc",
    }
    
    resp, err := c.client.ListDocuments(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("list documents failed: %w", err)
    }
    
    return resp.Documents, resp.TotalCount, nil
}

// Search documents
func (c *DocumentClient) SearchDocuments(ctx context.Context, query, orgID string, docTypes []string, limit, offset int32) ([]*documentpb.Document, int32, error) {
    if c.client == nil {
        return []*documentpb.Document{}, 0, nil
    }
    
    req := &documentpb.SearchDocumentsRequest{
        Query:          query,
        OrganizationId: orgID,
        DocumentTypes:  docTypes,
        Limit:          limit,
        Offset:         offset,
    }
    
    resp, err := c.client.SearchDocuments(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("search documents failed: %w", err)
    }
    
    return resp.Documents, resp.TotalCount, nil
}

// Request document signature
func (c *DocumentClient) RequestDocumentSignature(ctx context.Context, documentID, orgID string, signerIDs, signerEmails []string, deadline time.Time) error {
    if c.client == nil {
        return nil
    }
    
    req := &documentpb.RequestDocumentSignatureRequest{
        DocumentId:     documentID,
        SignerIds:      signerIDs,
        SignerEmails:   signerEmails,
        SigningOrder:   "parallel",
        Deadline:       timestampFromTime(deadline),
        OrganizationId: orgID,
    }
    
    resp, err := c.client.RequestDocumentSignature(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("request signature failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("signature request failed: %s", resp.Message)
    }
    
    return nil
}

// Sign a document
func (c *DocumentClient) SignDocument(ctx context.Context, documentID, signatureData, certificateID, orgID, ipAddress, userAgent string) error {
    if c.client == nil {
        return nil
    }
    
    req := &documentpb.SignDocumentRequest{
        DocumentId:     documentID,
        SignatureData:  signatureData,
        CertificateId:  certificateID,
        OrganizationId: orgID,
        IpAddress:      ipAddress,
        UserAgent:      userAgent,
    }
    
    resp, err := c.client.SignDocument(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("sign document failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("signature failed: %s", resp.Message)
    }
    
    return nil
}

// Generate document from template
func (c *DocumentClient) GenerateDocumentFromTemplate(ctx context.Context, templateID string, variables map[string]string, documentName, docType, ownerID, orgID string) (*documentpb.Document, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &documentpb.GenerateDocumentFromTemplateRequest{
        TemplateId:     templateID,
        Variables:      variables,
        DocumentName:   documentName,
        DocumentType:   docType,
        OwnerId:        ownerID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GenerateDocumentFromTemplate(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("generate document failed: %w", err)
    }
    
    if !resp.Generated {
        return nil, fmt.Errorf("document generation failed")
    }
    
    return resp.Document,nil
}

// Helper functions
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
    client, err := NewDocumentClient("document-store:50064")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    
    // Create a document
    createReq := &documentpb.CreateDocumentRequest{
        DocumentType:   "kyc_id",
        DocumentName:   "Passport Copy",
        Description:    "Government-issued passport",
        MimeType:       "application/pdf",
        OwnerId:        "user-789",
        OrganizationId: orgID,
        Metadata: map[string]string{
            "verification_level": "level_2",
            "expiry_date":        "2030-01-01",
        },
    }
    
    createResp, err := client.CreateDocument(ctx, createReq)
    if err != nil {
        log.Printf("Failed to create document: %v", err)
    } else {
        log.Printf("Document created: %s", createResp.Document.DocumentId)
        
        // Upload content if needed
        if createResp.UploadUrl != "" {
            // Handle large file upload
        }
    }
    
    // List user documents
    docs, total, err := client.ListDocuments(ctx, "user-789", "kyc_id", "active", orgID, 20, 0)
    if err != nil {
        log.Printf("Failed to list documents: %v", err)
    } else {
        log.Printf("Found %d documents (total: %d)", len(docs), total)
        
        for _, doc := range docs {
            log.Printf("- %s (%s): %s", doc.DocumentName, doc.DocumentType, doc.Status)
        }
    }
    
    // Request signature
    err = client.RequestDocumentSignature(ctx, createResp.Document.DocumentId, orgID, 
        []string{"approver-1", "approver-2"}, 
        []string{"admin@example.com"}, 
        time.Now().Add(7*24*time.Hour))
    if err != nil {
        log.Printf("Failed to request signature: %v", err)
    }
}
Docker Compose Example
bash
nano ~/dev/TXdocumentation/document/docker-compose.yml
yaml
version: '3.8'

services:
  document-service:
    image: sologenic/document-service:latest
    environment:
      - DOCUMENT_SERVICE_PORT=50064
      - DOCUMENT_STORE=document-store:50064
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=documents
      - POSTGRES_USER=document_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - S3_BUCKET=documents
      - S3_REGION=us-east-1
      - S3_ENDPOINT=${S3_ENDPOINT}
      - MAX_DOCUMENT_SIZE_MB=10
      - ALLOWED_FILE_TYPES=application/pdf,image/jpeg,image/png
      - SIGNATURE_REQUIRED=true
      - ENCRYPT_AT_REST=true
      - LOG_LEVEL=info
    ports:
      - "50064:50064"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
      - minio
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50064"]
      interval: 30s
      timeout: 10s
      retries: 3

  document-store:
    image: sologenic/document-store:latest
    environment:
      - DOCUMENT_STORE_PORT=50065
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=documents
      - POSTGRES_USER=document_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - S3_BUCKET=documents
      - S3_REGION=us-east-1
      - S3_ENDPOINT=${S3_ENDPOINT}
    ports:
      - "50065:50065"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
      - minio

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=documents
      - POSTGRES_USER=document_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U document_user -d documents"]
      interval: 10s
      timeout: 5s
      retries: 5

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

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=${MINIO_PASSWORD}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    networks:
      - internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - internal
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9200/_cluster/health"]
      interval: 30s
      timeout: 10s
      retries: 5

networks:
  internal:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  minio_data:
  elasticsearch_data:
Environment Setup (.env file)
bash
nano ~/dev/TXdocumentation/document/.env
bash
# Database Configuration
DB_PASSWORD=your_secure_password

# S3/MinIO Configuration
S3_ENDPOINT=http://minio:9000
MINIO_PASSWORD=minio_secure_password

# Service Configuration
DOCUMENT_STORE=document-store:50065
DOCUMENT_STORE_TESTING=FALSE

# Business Rules
MAX_DOCUMENT_SIZE_MB=10
ALLOWED_FILE_TYPES=application/pdf,image/jpeg,image/png
SIGNATURE_REQUIRED=true
ENCRYPT_AT_REST=true

# Logging
LOG_LEVEL=info
Testing Mode
The client automatically detects test mode when DOCUMENT_STORE_TESTING=TRUE is set:

bash
# Run in test mode
export DOCUMENT_STORE_TESTING=TRUE
go test ./...
Error Handling
go
// Example error handling
resp, err := client.CreateDocument(ctx, req)
if err != nil {
    if strings.Contains(err.Error(), "SIGNATURE_REQUIRED") {
        // Handle missing signature
    } else if strings.Contains(err.Error(), "INVALID_FILE_TYPE") {
        // Handle invalid file type
    } else if strings.Contains(err.Error(), "FILE_TOO_LARGE") {
        // Handle file size error
    }
    log.Printf("Error: %v", err)
}
License
This documentation is part of the TX Marketplace platform.
