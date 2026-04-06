# Comment Service (Comment Proto)

The Comment proto provides all the functionality required to interact with the comment service. It supports creating, reading, updating, and deleting comments across different entities with hierarchical threading, reactions, and moderation features.

## Overview

The Comment service is a gRPC-based system that handles:
- Hierarchical comment threads (nested replies)
- Reactions (likes, dislikes, emojis)
- Moderation and spam filtering
- User mentions and notifications
- Comment reporting and flagging
- Sorting and filtering

## Architecture
┌─────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Web, Mobile, Backend Services) │
└───────────────────┬─────────────────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────────────────┐
│ Comment Service │
│ - Thread Management │
│ - Reaction Handling │
│ - Moderation Queue │
│ - Notification Triggers │
└───────────────────┬─────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Storage Layer │
│ - Comment Store (PostgreSQL) │
│ - Reaction Store (Redis) │
│ - Search Index (Elasticsearch) │
└─────────────────────────────────────────────────────────┘

text

## Environment Variables

### Required Variables

| Variable | Description | Format | Example |
|----------|-------------|--------|---------|
| `COMMENT_STORE` | gRPC endpoint for comment store service | `host:port` | `comment-store:50060` |
| `COMMENT_STORE_TESTING` | Enable test mode with in-memory buffer | `TRUE` | `TRUE` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `COMMENT_CACHE_TTL` | Cache TTL in seconds | `60` |
| `MAX_COMMENT_DEPTH` | Maximum reply nesting depth | `10` |
| `MAX_COMMENT_LENGTH` | Maximum comment characters | `5000` |
| `MODERATION_ENABLED` | Enable content moderation | `true` |
| `SPAM_THRESHOLD` | Spam detection threshold | `0.7` |

## Proto Definition

```protobuf
syntax = "proto3";

package comment.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// Comment Service Definition
service CommentService {
    // Comment CRUD operations
    rpc CreateComment(CreateCommentRequest) returns (CreateCommentResponse);
    rpc GetComment(GetCommentRequest) returns (GetCommentResponse);
    rpc UpdateComment(UpdateCommentRequest) returns (UpdateCommentResponse);
    rpc DeleteComment(DeleteCommentRequest) returns (DeleteCommentResponse);
    
    // Comment listing and threading
    rpc ListComments(ListCommentsRequest) returns (ListCommentsResponse);
    rpc GetCommentThread(GetCommentThreadRequest) returns (GetCommentThreadResponse);
    rpc GetReplies(GetRepliesRequest) returns (GetRepliesResponse);
    
    // Reactions
    rpc AddReaction(AddReactionRequest) returns (AddReactionResponse);
    rpc RemoveReaction(RemoveReactionRequest) returns (RemoveReactionResponse);
    rpc GetReactions(GetReactionsRequest) returns (GetReactionsResponse);
    
    // Moderation
    rpc ReportComment(ReportCommentRequest) returns (ReportCommentResponse);
    rpc ModerateComment(ModerateCommentRequest) returns (ModerateCommentResponse);
    rpc GetReportedComments(GetReportedCommentsRequest) returns (GetReportedCommentsResponse);
    
    // User interactions
    rpc GetUserComments(GetUserCommentsRequest) returns (GetUserCommentsResponse);
    rpc GetUserMentions(GetUserMentionsRequest) returns (GetUserMentionsResponse);
    
    // Statistics
    rpc GetCommentStats(GetCommentStatsRequest) returns (GetCommentStatsResponse);
    rpc GetEntityStats(GetEntityStatsRequest) returns (GetEntityStatsResponse);
}

// ==================== Comment Messages ====================

message Comment {
    string comment_id = 1;              // Unique comment ID
    string entity_type = 2;             // Entity type (post, article, product)
    string entity_id = 3;               // Entity identifier
    string parent_comment_id = 4;       // Parent comment ID (for replies)
    string author_id = 5;               // Author user ID
    string author_name = 6;             // Author display name
    string author_avatar = 7;           // Author avatar URL
    string content = 8;                 // Comment content
    string content_html = 9;            // HTML formatted content
    repeated string mentions = 10;      // Mentioned user IDs
    repeated string attachments = 11;   // Attachment URLs
    int32 like_count = 12;              // Number of likes
    int32 reply_count = 13;             // Number of replies
    string status = 14;                 // active, hidden, deleted, flagged
    bool is_edited = 15;                // Whether comment was edited
    google.protobuf.Timestamp created_at = 16;
    google.protobuf.Timestamp updated_at = 17;
    google.protobuf.Timestamp deleted_at = 18;
    string organization_id = 19;        // Organization context
    map<string, string> metadata = 20;  // Additional metadata
    int32 depth = 21;                   // Thread depth level
    string path = 22;                   // Thread path (for ordering)
}

message CreateCommentRequest {
    string entity_type = 1;             // Entity type
    string entity_id = 2;               // Entity ID
    string parent_comment_id = 3;       // Parent comment (optional)
    string content = 4;                 // Comment content
    repeated string mentions = 5;       // Mentioned users
    repeated string attachments = 6;    // Attachments
    string author_id = 7;               // Author ID
    string author_name = 8;             // Author name
    string author_avatar = 9;           // Author avatar
    string organization_id = 10;        // Organization context
    map<string, string> metadata = 11;  // Additional metadata
}

message CreateCommentResponse {
    Comment comment = 1;
    bool created = 2;
    bool requires_moderation = 3;       // If comment needs moderation
}

message GetCommentRequest {
    string comment_id = 1;
    string organization_id = 2;
}

message GetCommentResponse {
    Comment comment = 1;
    bool found = 2;
}

message UpdateCommentRequest {
    string comment_id = 1;
    string content = 2;                 // Updated content
    repeated string mentions = 3;       // Updated mentions
    repeated string attachments = 4;    // Updated attachments
    string organization_id = 5;
}

message UpdateCommentResponse {
    Comment comment = 1;
    bool updated = 2;
}

message DeleteCommentRequest {
    string comment_id = 1;
    string organization_id = 2;
    bool soft_delete = 3;               // Soft delete vs permanent
}

message DeleteCommentResponse {
    bool success = 1;
    string message = 2;
}

// ==================== Listing and Threading ====================

message ListCommentsRequest {
    string entity_type = 1;
    string entity_id = 2;
    string parent_comment_id = 3;       // Filter by parent
    string sort_by = 4;                 // newest, oldest, popular
    int32 limit = 5;                    // Max comments (default 20, max 100)
    int32 offset = 6;                   // Pagination offset
    string status_filter = 7;           // Filter by status
    string organization_id = 8;
    bool include_replies = 9;           // Include nested replies
    int32 max_depth = 10;               // Max reply depth
}

message ListCommentsResponse {
    repeated Comment comments = 1;
    int32 total_count = 2;
    bool has_more = 3;
    map<string, int32> reply_counts = 4; // Reply counts per comment
}

message GetCommentThreadRequest {
    string comment_id = 1;
    int32 max_depth = 2;                // Max thread depth
    string organization_id = 3;
}

message GetCommentThreadResponse {
    Comment root_comment = 1;
    repeated Comment replies = 2;       // Flattened replies
    map<string, repeated Comment> threaded_replies = 3; // Threaded structure
}

message GetRepliesRequest {
    string comment_id = 1;
    string organization_id = 2;
    string sort_by = 3;
    int32 limit = 4;
    int32 offset = 5;
}

message GetRepliesResponse {
    repeated Comment replies = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

// ==================== Reactions ====================

message Reaction {
    string reaction_id = 1;
    string comment_id = 2;
    string user_id = 3;
    string reaction_type = 4;           // like, dislike, heart, laugh, sad, angry
    google.protobuf.Timestamp created_at = 5;
}

message AddReactionRequest {
    string comment_id = 1;
    string user_id = 2;
    string reaction_type = 3;
    string organization_id = 4;
}

message AddReactionResponse {
    Reaction reaction = 1;
    bool added = 2;
    int32 total_count = 3;              // Updated total for this reaction type
}

message RemoveReactionRequest {
    string comment_id = 1;
    string user_id = 2;
    string reaction_type = 3;
    string organization_id = 4;
}

message RemoveReactionResponse {
    bool removed = 1;
    int32 total_count = 2;              // Updated total for this reaction type
}

message GetReactionsRequest {
    string comment_id = 1;
    string organization_id = 2;
    bool include_user_reaction = 3;     // Include current user's reaction
    string user_id = 4;                 // For user reaction check
}

message GetReactionsResponse {
    map<string, int32> reaction_counts = 1;  // reaction_type -> count
    string user_reaction = 2;                // Current user's reaction (if any)
    repeated Reaction recent_reactions = 3;  // Most recent reactions
}

// ==================== Moderation ====================

message Report {
    string report_id = 1;
    string comment_id = 2;
    string reporter_id = 3;
    string reason = 4;
    string details = 5;
    string status = 6;                  // pending, reviewed, dismissed, action_taken
    google.protobuf.Timestamp created_at = 7;
    google.protobuf.Timestamp reviewed_at = 8;
    string reviewed_by = 9;
    string action_taken = 10;
}

message ReportCommentRequest {
    string comment_id = 1;
    string reporter_id = 2;
    string reason = 3;
    string details = 4;
    string organization_id = 5;
}

message ReportCommentResponse {
    Report report = 1;
    bool reported = 2;
    string message = 3;
}

message ModerateCommentRequest {
    string comment_id = 1;
    string moderator_id = 2;
    string action = 3;                  // approve, hide, delete, flag
    string reason = 4;
    string organization_id = 5;
}

message ModerateCommentResponse {
    bool success = 1;
    Comment comment = 2;
    string message = 3;
}

message GetReportedCommentsRequest {
    string organization_id = 1;
    string status = 2;                  // Filter by status
    int32 limit = 3;
    int32 offset = 4;
}

message GetReportedCommentsResponse {
    repeated ReportedComment reported_comments = 1;
    int32 total_count = 2;
}

message ReportedComment {
    Comment comment = 1;
    repeated Report reports = 2;
    int32 report_count = 3;
}

// ==================== User Interactions ====================

message GetUserCommentsRequest {
    string user_id = 1;
    string organization_id = 2;
    string entity_type = 3;             // Optional filter
    int32 limit = 4;
    int32 offset = 5;
    google.protobuf.Timestamp since = 6; // Comments since date
}

message GetUserCommentsResponse {
    repeated Comment comments = 1;
    int32 total_count = 2;
    bool has_more = 3;
}

message GetUserMentionsRequest {
    string user_id = 1;
    string organization_id = 2;
    bool only_unread = 3;
    int32 limit = 4;
    int32 offset = 5;
}

message GetUserMentionsResponse {
    repeated Mention mentions = 1;
    int32 total_count = 2;
    int32 unread_count = 3;
}

message Mention {
    string mention_id = 1;
    string comment_id = 2;
    string mentioned_user_id = 3;
    string mentioned_by = 4;
    Comment comment = 5;
    bool read = 6;
    google.protobuf.Timestamp created_at = 7;
}

// ==================== Statistics ====================

message GetCommentStatsRequest {
    string comment_id = 1;
    string organization_id = 2;
}

message GetCommentStatsResponse {
    int32 total_reactions = 1;
    map<string, int32> reaction_breakdown = 2;
    int32 reply_count = 3;
    int32 report_count = 4;
    double engagement_score = 5;        // Calculated engagement metric
}

message GetEntityStatsRequest {
    string entity_type = 1;
    string entity_id = 2;
    string organization_id = 3;
    google.protobuf.Timestamp since = 4;
    google.protobuf.Timestamp until = 5;
}

message GetEntityStatsResponse {
    int32 total_comments = 1;
    int32 unique_commenters = 2;
    int32 total_reactions = 3;
    int32 avg_comments_per_day = 4;
    double engagement_rate = 5;
    map<string, int32> comments_by_status = 6;
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

echo -e "${GREEN}Starting Comment proto build...${NC}"

# Check if proto file exists
if [ ! -f "comment.proto" ] && [ ! -f "proto/comment.proto" ]; then
    echo -e "${RED}Error: No comment.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "comment.proto" ]; then
    PROTO_FILE="comment.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/comment.proto"
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
    
    # Generate TypeScript files
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
        --doc_opt=markdown,comment-api.md \
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
echo "  - client/go/comment.pb.go"
echo "  - client/go/comment_grpc.pb.go"
if [ -f "client/typescript/comment.ts" ]; then
    echo "  - client/typescript/comment.ts"
fi
echo "  - build/comment-api.md"

# Show file sizes
echo -e "\n${BLUE}File sizes:${NC}"
ls -lh client/go/*.pb.go 2>/dev/null || echo "Go files not found"
if [ -f "client/typescript/comment.ts" ]; then
    ls -lh client/typescript/comment.ts 2>/dev/null
fi
Make the script executable:

bash
chmod +x bin/build.sh
Run Build
bash
./bin/build.sh
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
    
    commentpb "github.com/sologenic/comment/client/go"
)

type CommentClient struct {
    client commentpb.CommentServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new comment client
func NewCommentClient(addr string) (*CommentClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("COMMENT_STORE_TESTING"); testingMode == "TRUE" {
            // Use in-memory test client
            return &CommentClient{}, nil
        }
        return nil, fmt.Errorf("COMMENT_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to comment service: %w", err)
    }
    
    return &CommentClient{
        client: commentpb.NewCommentServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *CommentClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *CommentClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *CommentClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Create a new comment
func (c *CommentClient) CreateComment(ctx context.Context, req *commentpb.CreateCommentRequest) (*commentpb.CreateCommentResponse, error) {
    if c.client == nil {
        // Mock response for testing
        return &commentpb.CreateCommentResponse{
            Comment: &commentpb.Comment{
                CommentId: "test-comment-id",
                Content:   req.Content,
                CreatedAt: timestampNow(),
            },
            Created: true,
        }, nil
    }
    
    resp, err := c.client.CreateComment(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create comment failed: %w", err)
    }
    
    return resp, nil
}

// Get a comment by ID
func (c *CommentClient) GetComment(ctx context.Context, commentID, orgID string) (*commentpb.Comment, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &commentpb.GetCommentRequest{
        CommentId:      commentID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetComment(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get comment failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Comment, nil
}

// Update a comment
func (c *CommentClient) UpdateComment(ctx context.Context, commentID, content, orgID string) (*commentpb.Comment, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &commentpb.UpdateCommentRequest{
        CommentId:      commentID,
        Content:        content,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.UpdateComment(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update comment failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("comment not updated")
    }
    
    return resp.Comment, nil
}

// Delete a comment
func (c *CommentClient) DeleteComment(ctx context.Context, commentID, orgID string, softDelete bool) error {
    if c.client == nil {
        return nil
    }
    
    req := &commentpb.DeleteCommentRequest{
        CommentId:      commentID,
        OrganizationId: orgID,
        SoftDelete:     softDelete,
    }
    
    resp, err := c.client.DeleteComment(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("delete comment failed: %w", err)
    }
    
    if !resp.Success {
        return fmt.Errorf("delete failed: %s", resp.Message)
    }
    
    return nil
}

// List comments for an entity
func (c *CommentClient) ListComments(ctx context.Context, entityType, entityID, orgID string, limit, offset int32) ([]*commentpb.Comment, int32, error) {
    if c.client == nil {
        return []*commentpb.Comment{}, 0, nil
    }
    
    req := &commentpb.ListCommentsRequest{
        EntityType:     entityType,
        EntityId:       entityID,
        OrganizationId: orgID,
        SortBy:         "newest",
        Limit:          limit,
        Offset:         offset,
        IncludeReplies: true,
        MaxDepth:       5,
    }
    
    resp, err := c.client.ListComments(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("list comments failed: %w", err)
    }
    
    return resp.Comments, resp.TotalCount, nil
}

// Get comment thread
func (c *CommentClient) GetCommentThread(ctx context.Context, commentID, orgID string, maxDepth int32) (*commentpb.GetCommentThreadResponse, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &commentpb.GetCommentThreadRequest{
        CommentId:      commentID,
        OrganizationId: orgID,
        MaxDepth:       maxDepth,
    }
    
    resp, err := c.client.GetCommentThread(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get comment thread failed: %w", err)
    }
    
    return resp, nil
}

// Add reaction to comment
func (c *CommentClient) AddReaction(ctx context.Context, commentID, userID, reactionType, orgID string) error {
    if c.client == nil {
        return nil
    }
    
    req := &commentpb.AddReactionRequest{
        CommentId:      commentID,
        UserId:         userID,
        ReactionType:   reactionType,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.AddReaction(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("add reaction failed: %w", err)
    }
    
    if !resp.Added {
        return fmt.Errorf("reaction not added")
    }
    
    return nil
}

// Remove reaction from comment
func (c *CommentClient) RemoveReaction(ctx context.Context, commentID, userID, reactionType, orgID string) error {
    if c.client == nil {
        return nil
    }
    
    req := &commentpb.RemoveReactionRequest{
        CommentId:      commentID,
        UserId:         userID,
        ReactionType:   reactionType,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.RemoveReaction(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("remove reaction failed: %w", err)
    }
    
    if !resp.Removed {
        return fmt.Errorf("reaction not removed")
    }
    
    return nil
}

// Get reactions for a comment
func (c *CommentClient) GetReactions(ctx context.Context, commentID, userID, orgID string) (map[string]int32, string, error) {
    if c.client == nil {
        return map[string]int32{}, "", nil
    }
    
    req := &commentpb.GetReactionsRequest{
        CommentId:          commentID,
        OrganizationId:     orgID,
        IncludeUserReaction: true,
        UserId:             userID,
    }
    
    resp, err := c.client.GetReactions(c.getContext(ctx), req)
    if err != nil {
        return nil, "", fmt.Errorf("get reactions failed: %w", err)
    }
    
    return resp.ReactionCounts, resp.UserReaction, nil
}

// Report a comment
func (c *CommentClient) ReportComment(ctx context.Context, commentID, reporterID, reason, details, orgID string) error {
    if c.client == nil {
        return nil
    }
    
    req := &commentpb.ReportCommentRequest{
        CommentId:      commentID,
        ReporterId:     reporterID,
        Reason:         reason,
        Details:        details,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.ReportComment(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("report comment failed: %w", err)
    }
    
    if !resp.Reported {
        return fmt.Errorf("report failed: %s", resp.Message)
    }
    
    return nil
}

// Get user's comments
func (c *CommentClient) GetUserComments(ctx context.Context, userID, orgID string, limit, offset int32) ([]*commentpb.Comment, int32, error) {
    if c.client == nil {
        return []*commentpb.Comment{}, 0, nil
    }
    
    req := &commentpb.GetUserCommentsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Limit:          limit,
        Offset:         offset,
    }
    
    resp, err := c.client.GetUserComments(c.getContext(ctx), req)
    if err != nil {
        return nil, 0, fmt.Errorf("get user comments failed: %w", err)
    }
    
    return resp.Comments, resp.TotalCount, nil
}

// Get comment statistics
func (c *CommentClient) GetCommentStats(ctx context.Context, commentID, orgID string) (*commentpb.GetCommentStatsResponse, error) {
    if c.client == nil {
        return nil, nil
    }
    
    req := &commentpb.GetCommentStatsRequest{
        CommentId:      commentID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetCommentStats(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get comment stats failed: %w", err)
    }
    
    return resp, nil
}

// Helper function to create timestamp
func timestampNow() *google_protobuf.Timestamp {
    return &google_protobuf.Timestamp{
        Seconds: time.Now().Unix(),
        Nanos:   int32(time.Now().Nanosecond()),
    }
}

// Example usage
func main() {
    // Initialize client (will auto-detect testing mode)
    client, err := NewCommentClient("comment-store:50060")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    
    // Create a comment
    createReq := &commentpb.CreateCommentRequest{
        EntityType:     "article",
        EntityId:       "article-456",
        Content:        "Great article! Very informative.",
        AuthorId:       "user-789",
        AuthorName:     "John Doe",
        OrganizationId: orgID,
        Mentions:       []string{"user-101", "user-102"},
    }
    
    createResp, err := client.CreateComment(ctx, createReq)
    if err != nil {
        log.Printf("Failed to create comment: %v", err)
    } else {
        log.Printf("Comment created: %s", createResp.Comment.CommentId)
        
        if createResp.RequiresModeration {
            log.Println("Comment requires moderation before being visible")
        }
    }
    
    // List comments for an article
    comments, total, err := client.ListComments(ctx, "article", "article-456", orgID, 20, 0)
    if err != nil {
        log.Printf("Failed to list comments: %v", err)
    } else {
        log.Printf("Found %d comments (total: %d)", len(comments), total)
        
        for _, comment := range comments {
            log.Printf("- %s: %s (Likes: %d, Replies: %d)", 
                comment.AuthorName, comment.Content, comment.LikeCount, comment.ReplyCount)
        }
    }
    
    // Add a reaction
    if createResp != nil && createResp.Comment != nil {
        err = client.AddReaction(ctx, createResp.Comment.CommentId, "user-789", "like", orgID)
        if err != nil {
            log.Printf("Failed to add reaction: %v", err)
        } else {
            log.Println("Added like to comment")
        }
        
        // Get reactions
        reactions, userReaction, err := client.GetReactions(ctx, createResp.Comment.CommentId, "user-789", orgID)
        if err != nil {
            log.Printf("Failed to get reactions: %v", err)
        } else {
            log.Printf("Reactions: %v", reactions)
            log.Printf("Your reaction: %s", userReaction)
        }
    }
}
TypeScript Client
typescript
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';
import * as path from 'path';

interface Comment {
    commentId: string;
    entityType: string;
    entityId: string;
    parentCommentId?: string;
    authorId: string;
    authorName: string;
    authorAvatar?: string;
    content: string;
    contentHtml?: string;
    mentions: string[];
    attachments: string[];
    likeCount: number;
    replyCount: number;
    status: string;
    isEdited: boolean;
    createdAt: Date;
    updatedAt: Date;
    deletedAt?: Date;
    organizationId: string;
    metadata: Record<string, string>;
    depth: number;
    path: string;
}

interface Reaction {
    reactionId: string;
    commentId: string;
    userId: string;
    reactionType: string;
    createdAt: Date;
}

class CommentClient {
    private client: any;
    private token: string | null = null;
    private isTestMode: boolean;
    
    constructor(serviceUrl?: string) {
        // Check for test mode
        this.isTestMode = process.env.COMMENT_STORE_TESTING === 'TRUE';
        
        if (!this.isTestMode && !serviceUrl) {
            throw new Error('COMMENT_STORE environment variable not set and not in testing mode');
        }
        
        if (!this.isTestMode) {
            const PROTO_PATH = path.join(__dirname, '../proto/comment.proto');
            const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
                keepCase: true,
                longs: String,
                enums: String,
                defaults: true,
                oneofs: true
            });
            const proto = grpc.loadPackageDefinition(packageDefinition);
            this.client = new proto.comment.v1.CommentService(
                serviceUrl,
                grpc.credentials.createInsecure()
            );
        }
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
    
    async createComment(request: {
        entityType: string;
        entityId: string;
        content: string;
        authorId: string;
        authorName: string;
        authorAvatar?: string;
        parentCommentId?: string;
        mentions?: string[];
        attachments?: string[];
        organizationId: string;
        metadata?: Record<string, string>;
    }): Promise<{ comment: Comment; created: boolean; requiresModeration: boolean }> {
        if (this.isTestMode) {
            return {
                comment: {
                    commentId: 'test-comment-id',
                    entityType: request.entityType,
                    entityId: request.entityId,
                    authorId: request.authorId,
                    authorName: request.authorName,
                    content: request.content,
                    mentions: request.mentions || [],
                    attachments: request.attachments || [],
                    likeCount: 0,
                    replyCount: 0,
                    status: 'active',
                    isEdited: false,
                    createdAt: new Date(),
                    updatedAt: new Date(),
                    organizationId: request.organizationId,
                    metadata: request.metadata || {},
                    depth: 0,
                    path: ''
                },
                created: true,
                requiresModeration: false
            };
        }
        
        return new Promise((resolve, reject) => {
            this.client.CreateComment(
                {
                    entity_type: request.entityType,
                    entity_id: request.entityId,
                    parent_comment_id: request.parentCommentId,
                    content: request.content,
                    mentions: request.mentions || [],
                    attachments: request.attachments || [],
                    author_id: request.authorId,
                    author_name: request.authorName,
                    author_avatar: request.authorAvatar,
                    organization_id: request.organizationId,
                    metadata: request.metadata || {}
                },
this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        comment: this.mapToComment(response.comment),
                        created: response.created,
                        requiresModeration: response.requires_moderation
                    });
                }
            );
        });
    }
    
    async getComment(commentId: string, organizationId: string): Promise<Comment | null> {
        if (this.isTestMode) {
            return null;
        }
        
        return new Promise((resolve, reject) => {
            this.client.GetComment(
                { comment_id: commentId, organization_id: organizationId },
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
                    
                    resolve(this.mapToComment(response.comment));
                }
            );
        });
    }
    
    async updateComment(commentId: string, content: string, organizationId: string, mentions?: string[], attachments?: string[]): Promise<Comment> {
        if (this.isTestMode) {
            return {
                commentId,
                entityType: 'test',
                entityId: 'test',
                authorId: 'test',
                authorName: 'Test User',
                content,
                mentions: mentions || [],
                attachments: attachments || [],
                likeCount: 0,
                replyCount: 0,
                status: 'active',
                isEdited: true,
                createdAt: new Date(),
                updatedAt: new Date(),
                organizationId,
                metadata: {},
                depth: 0,
                path: ''
            };
        }
        
        return new Promise((resolve, reject) => {
            this.client.UpdateComment(
                {
                    comment_id: commentId,
                    content,
                    mentions: mentions || [],
                    attachments: attachments || [],
                    organization_id: organizationId
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.updated) {
                        reject(new Error('Comment not updated'));
                        return;
                    }
                    
                    resolve(this.mapToComment(response.comment));
                }
            );
        });
    }
    
    async deleteComment(commentId: string, organizationId: string, softDelete: boolean = true): Promise<void> {
        if (this.isTestMode) {
            return;
        }
        
        return new Promise((resolve, reject) => {
            this.client.DeleteComment(
                {
                    comment_id: commentId,
                    organization_id: organizationId,
                    soft_delete: softDelete
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
    
    async listComments(options: {
        entityType: string;
        entityId: string;
        organizationId: string;
        parentCommentId?: string;
        sortBy?: 'newest' | 'oldest' | 'popular';
        limit?: number;
        offset?: number;
        statusFilter?: string;
        includeReplies?: boolean;
        maxDepth?: number;
    }): Promise<{ comments: Comment[]; totalCount: number; hasMore: boolean; replyCounts: Record<string, number> }> {
        if (this.isTestMode) {
            return { comments: [], totalCount: 0, hasMore: false, replyCounts: {} };
        }
        
        return new Promise((resolve, reject) => {
            this.client.ListComments(
                {
                    entity_type: options.entityType,
                    entity_id: options.entityId,
                    parent_comment_id: options.parentCommentId,
                    sort_by: options.sortBy || 'newest',
                    limit: options.limit || 20,
                    offset: options.offset || 0,
                    status_filter: options.statusFilter,
                    organization_id: options.organizationId,
                    include_replies: options.includeReplies ?? true,
                    max_depth: options.maxDepth || 5
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        comments: response.comments.map((c: any) => this.mapToComment(c)),
                        totalCount: response.total_count,
                        hasMore: response.has_more,
                        replyCounts: response.reply_counts || {}
                    });
                }
            );
        });
    }
    
    async getCommentThread(commentId: string, organizationId: string, maxDepth: number = 10): Promise<{ rootComment: Comment; replies: Comment[]; threadedReplies: Record<string, Comment[]> }> {
        if (this.isTestMode) {
            return { rootComment: {} as Comment, replies: [], threadedReplies: {} };
        }
        
        return new Promise((resolve, reject) => {
            this.client.GetCommentThread(
                {
                    comment_id: commentId,
                    organization_id: organizationId,
                    max_depth: maxDepth
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    const threadedReplies: Record<string, Comment[]> = {};
                    if (response.threaded_replies) {
                        for (const [key, value] of Object.entries(response.threaded_replies)) {
                            threadedReplies[key] = (value as any[]).map((c: any) => this.mapToComment(c));
                        }
                    }
                    
                    resolve({
                        rootComment: this.mapToComment(response.root_comment),
                        replies: (response.replies || []).map((c: any) => this.mapToComment(c)),
                        threadedReplies
                    });
                }
            );
        });
    }
    
    async getReplies(commentId: string, organizationId: string, options?: { sortBy?: string; limit?: number; offset?: number }): Promise<{ replies: Comment[]; totalCount: number; hasMore: boolean }> {
        if (this.isTestMode) {
            return { replies: [], totalCount: 0, hasMore: false };
        }
        
        return new Promise((resolve, reject) => {
            this.client.GetReplies(
                {
                    comment_id: commentId,
                    organization_id: organizationId,
                    sort_by: options?.sortBy || 'newest',
                    limit: options?.limit || 20,
                    offset: options?.offset || 0
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        replies: (response.replies || []).map((c: any) => this.mapToComment(c)),
                        totalCount: response.total_count,
                        hasMore: response.has_more
                    });
                }
            );
        });
    }
    
    async addReaction(commentId: string, userId: string, reactionType: string, organizationId: string): Promise<{ reaction: Reaction; totalCount: number }> {
        if (this.isTestMode) {
            return {
                reaction: {
                    reactionId: 'test-reaction-id',
                    commentId,
                    userId,
                    reactionType,
                    createdAt: new Date()
                },
                totalCount: 1
            };
        }
        
        return new Promise((resolve, reject) => {
            this.client.AddReaction(
                {
                    comment_id: commentId,
                    user_id: userId,
                    reaction_type: reactionType,
                    organization_id: organizationId
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    if (!response.added) {
                        reject(new Error('Reaction not added'));
                        return;
                    }
                    
                    resolve({
                        reaction: this.mapToReaction(response.reaction),
                        totalCount: response.total_count
                    });
                }
            );
        });
    }
    
    async removeReaction(commentId: string, userId: string, reactionType: string, organizationId: string): Promise<{ removed: boolean; totalCount: number }> {
        if (this.isTestMode) {
            return { removed: true, totalCount: 0 };
        }
        
        return new Promise((resolve, reject) => {
            this.client.RemoveReaction(
                {
                    comment_id: commentId,
                    user_id: userId,
                    reaction_type: reactionType,
                    organization_id: organizationId
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        removed: response.removed,
                        totalCount: response.total_count
                    });
                }
            );
        });
    }
    
    async getReactions(commentId: string, organizationId: string, userId?: string): Promise<{ reactionCounts: Record<string, number>; userReaction: string | null; recentReactions: Reaction[] }> {
        if (this.isTestMode) {
            return { reactionCounts: {}, userReaction: null, recentReactions: [] };
        }
        
        return new Promise((resolve, reject) => {
            this.client.GetReactions(
                {
                    comment_id: commentId,
                    organization_id: organizationId,
                    include_user_reaction: !!userId,
                    user_id: userId
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        reactionCounts: response.reaction_counts || {},
                        userReaction: response.user_reaction || null,
                        recentReactions: (response.recent_reactions || []).map((r: any) => this.mapToReaction(r))
                    });
                }
            );
        });
    }
    
    async reportComment(commentId: string, reporterId: string, reason: string, organizationId: string, details?: string): Promise<{ reported: boolean; message: string }> {
        if (this.isTestMode) {
            return { reported: true, message: 'Report submitted' };
        }
        
        return new Promise((resolve, reject) => {
            this.client.ReportComment(
                {
                    comment_id: commentId,
                    reporter_id: reporterId,
                    reason,
                    details: details || '',
                    organization_id: organizationId
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        reported: response.reported,
                        message: response.message
                    });
                }
            );
        });
    }
    
    async moderateComment(commentId: string, moderatorId: string, action: 'approve' | 'hide' | 'delete' | 'flag', organizationId: string, reason?: string): Promise<{ success: boolean; comment: Comment; message: string }> {
        if (this.isTestMode) {
            return { success: true, comment: {} as Comment, message: 'Moderation action applied' };
        }
        
        return new Promise((resolve, reject) => {
            this.client.ModerateComment(
                {
                    comment_id: commentId,
                    moderator_id: moderatorId,
                    action,
                    reason: reason || '',
                    organization_id: organizationId
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        success: response.success,
                        comment: this.mapToComment(response.comment),
                        message: response.message
                    });
                }
            );
        });
    }
    
    async getUserComments(userId: string, organizationId: string, options?: { entityType?: string; limit?: number; offset?: number; since?: Date }): Promise<{ comments: Comment[]; totalCount: number; hasMore: boolean }> {
        if (this.isTestMode) {
            return { comments: [], totalCount: 0, hasMore: false };
        }
        
        return new Promise((resolve, reject) => {
            this.client.GetUserComments(
                {
                    user_id: userId,
                    organization_id: organizationId,
                    entity_type: options?.entityType,
                    limit: options?.limit || 20,
                    offset: options?.offset || 0,
                    since: options?.since ? { seconds: Math.floor(options.since.getTime() / 1000) } : undefined
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        comments: (response.comments || []).map((c: any) => this.mapToComment(c)),
                        totalCount: response.total_count,
                        hasMore: response.has_more
                    });
                }
            );
        });
    }
    
    async getUserMentions(userId: string, organizationId: string, options?: { onlyUnread?: boolean; limit?: number; offset?: number }): Promise<{ mentions: any[]; totalCount: number; unreadCount: number }> {
        if (this.isTestMode) {
            return { mentions: [], totalCount: 0, unreadCount: 0 };
        }
        
        return new Promise((resolve, reject) => {
            this.client.GetUserMentions(
                {
                    user_id: userId,
                    organization_id: organizationId,
                    only_unread: options?.onlyUnread || false,
                    limit: options?.limit || 20,
                    offset: options?.offset || 0
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        mentions: response.mentions || [],
                        totalCount: response.total_count,
                        unreadCount: response.unread_count
                    });
                }
            );
        });
    }
    
    async getCommentStats(commentId: string, organizationId: string): Promise<{
        totalReactions: number;
        reactionBreakdown: Record<string, number>;
        replyCount: number;
        reportCount: number;
        engagementScore: number;
    }> {
        if (this.isTestMode) {
            return {
                totalReactions: 0,
                reactionBreakdown: {},
                replyCount: 0,
                reportCount: 0,
                engagementScore: 0
            };
        }
        
        return new Promise((resolve, reject) => {
            this.client.GetCommentStats(
                {
                    comment_id: commentId,
                    organization_id: organizationId
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        totalReactions: response.total_reactions,
                        reactionBreakdown: response.reaction_breakdown || {},
                        replyCount: response.reply_count,
                        reportCount: response.report_count,
                        engagementScore: response.engagement_score
                    });
                }
            );
        });
    }
    
    async getEntityStats(entityType: string, entityId: string, organizationId: string, options?: { since?: Date; until?: Date }): Promise<{
        totalComments: number;
        uniqueCommenters: number;
        totalReactions: number;
        avgCommentsPerDay: number;
        engagementRate: number;
        commentsByStatus: Record<string, number>;
    }> {
        if (this.isTestMode) {
            return {
                totalComments: 0,
                uniqueCommenters: 0,
                totalReactions: 0,
                avgCommentsPerDay: 0,
                engagementRate: 0,
                commentsByStatus: {}
            };
        }
        
        return new Promise((resolve, reject) => {
            this.client.GetEntityStats(
                {
                    entity_type: entityType,
                    entity_id: entityId,
                    organization_id: organizationId,
                    since: options?.since ? { seconds: Math.floor(options.since.getTime() / 1000) } : undefined,
                    until: options?.until ? { seconds: Math.floor(options.until.getTime() / 1000) } : undefined
                },
                this.getMetadata(),
                (err: any, response: any) => {
                    if (err) {
                        reject(err);
                        return;
                    }
                    
                    resolve({
                        totalComments: response.total_comments,
                        uniqueCommenters: response.unique_commenters,
                        totalReactions: response.total_reactions,
                        avgCommentsPerDay: response.avg_comments_per_day,
                        engagementRate: response.engagement_rate,
                        commentsByStatus: response.comments_by_status || {}
                    });
                }
            );
        });
    }
    
    // Helper method to map protobuf comment to TypeScript Comment
    private mapToComment(protoComment: any): Comment {
        if (!protoComment) return {} as Comment;
        
        return {
            commentId: protoComment.comment_id,
            entityType: protoComment.entity_type,
            entityId: protoComment.entity_id,
            parentCommentId: protoComment.parent_comment_id,
            authorId: protoComment.author_id,
            authorName: protoComment.author_name,
            authorAvatar: protoComment.author_avatar,
            content: protoComment.content,
            contentHtml: protoComment.content_html,
            mentions: protoComment.mentions || [],
            attachments: protoComment.attachments || [],
            likeCount: protoComment.like_count,
            replyCount: protoComment.reply_count,
            status: protoComment.status,
            isEdited: protoComment.is_edited,
            createdAt: new Date(protoComment.created_at?.seconds * 1000),
            updatedAt: new Date(protoComment.updated_at?.seconds * 1000),
            deletedAt: protoComment.deleted_at ? new Date(protoComment.deleted_at.seconds * 1000) : undefined,
            organizationId: protoComment.organization_id,
            metadata: protoComment.metadata || {},
            depth: protoComment.depth,
            path: protoComment.path
        };
    }
    
    // Helper method to map protobuf reaction to TypeScript Reaction
    private mapToReaction(protoReaction: any): Reaction {
        if (!protoReaction) return {} as Reaction;
        
        return {
            reactionId: protoReaction.reaction_id,
            commentId: protoReaction.comment_id,
            userId: protoReaction.user_id,
            reactionType: protoReaction.reaction_type,
            createdAt: new Date(protoReaction.created_at?.seconds * 1000)
        };
    }
}

// React hook for comments
import { useEffect, useState, useCallback } from 'react';

interface UseCommentsOptions {
    entityType: string;
    entityId: string;
    organizationId: string;
    initialLimit?: number;
    autoLoad?: boolean;
}

function useComments(options: UseCommentsOptions) {
    const [comments, setComments] = useState<Comment[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [hasMore, setHasMore] = useState(false);
    const [totalCount, setTotalCount] = useState(0);
    const [offset, setOffset] = useState(0);
    
    const client = new CommentClient(process.env.COMMENT_STORE);
    
    const loadComments = useCallback(async (reset: boolean = false) => {
        const currentOffset = reset ? 0 : offset;
        
        setLoading(true);
        setError(null);
        
        try {
            const response = await client.listComments({
                entityType: options.entityType,
                entityId: options.entityId,
                organizationId: options.organizationId,
                limit: options.initialLimit || 20,
                offset: currentOffset,
                includeReplies: true,
                maxDepth: 5
            });
            
            if (reset) {
                setComments(response.comments);
                setOffset(response.comments.length);
            } else {
                setComments(prev => [...prev, ...response.comments]);
                setOffset(prev => prev + response.comments.length);
            }
            
            setHasMore(response.hasMore);
            setTotalCount(response.totalCount);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load comments');
        } finally {
            setLoading(false);
        }
    }, [options.entityType, options.entityId, options.organizationId, options.initialLimit, offset]);
    
    const loadMore = useCallback(() => {
        if (!loading && hasMore) {
            loadComments(false);
        }
    }, [loading, hasMore, loadComments]);
    
    const addComment = useCallback(async (content: string, authorId: string, authorName: string, parentCommentId?: string) => {
        try {
            const response = await client.createComment({
                entityType: options.entityType,
                entityId: options.entityId,
                content,
                authorId,
                authorName,
                organizationId: options.organizationId,
                parentCommentId
            });
            
            if (response.created) {
                // Refresh comments to show the new one
                await loadComments(true);
            }
            
            return response;
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to add comment');
            throw err;
        }
    }, [options.entityType, options.entityId, options.organizationId, loadComments]);
    
    const addReaction = useCallback(async (commentId: string, userId: string, reactionType: string) => {
        try {
            await client.addReaction(commentId, userId, reactionType, options.organizationId);
            
            // Update local state
            setComments(prev => prev.map(comment => {
                if (comment.commentId === commentId) {
                    const newLikeCount = reactionType === 'like' 
                        ? comment.likeCount + 1 
                        : comment.likeCount;
                    return { ...comment, likeCount: newLikeCount };
                }
                return comment;
            }));
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to add reaction');
            throw err;
        }
    }, [options.organizationId]);
    
    const deleteComment = useCallback(async (commentId: string) => {
        try {
            await client.deleteComment(commentId, options.organizationId, true);
            
            // Remove from local state
            setComments(prev => prev.filter(comment => comment.commentId !== commentId));
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to delete comment');
            throw err;
        }
    }, [options.organizationId]);
    
    useEffect(() => {
        if (options.autoLoad !== false) {
            loadComments(true);
        }
    }, [options.entityType, options.entityId, options.organizationId]);
    
    return {
        comments,
        loading,
        error,
        hasMore,
        totalCount,
        loadComments: () => loadComments(true),
        loadMore,
        addComment,
        addReaction,
        deleteComment
    };
}

// React hook for single comment thread
function useCommentThread(commentId: string, organizationId: string, maxDepth: number = 10) {
    const [thread, setThread] = useState<{ rootComment: Comment | null; replies: Comment[]; threadedReplies: Record<string, Comment[]> }>({
        rootComment: null,
        replies: [],
        threadedReplies: {}
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    const client = new CommentClient(process.env.COMMENT_STORE);
    
    const loadThread = useCallback(async () => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await client.getCommentThread(commentId, organizationId, maxDepth);
            setThread({
                rootComment: response.rootComment,
                replies: response.replies,
                threadedReplies: response.threadedReplies
            });
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load comment thread');
        } finally {
            setLoading(false);
        }
    }, [commentId, organizationId, maxDepth]);
    
    const addReply = useCallback(async (content: string, authorId: string, authorName: string, parentCommentId?: string) => {
        const client = new CommentClient(process.env.COMMENT_STORE);
        
        try {
            const response = await client.createComment({
                entityType: thread.rootComment?.entityType || '',
                entityId: thread.rootComment?.entityId || '',
                content,
                authorId,
                authorName,
                organizationId,
                parentCommentId: parentCommentId || commentId
            });
            
            if (response.created) {
                await loadThread();
            }
            
            return response;
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to add reply');
            throw err;
        }
    }, [thread.rootComment, organizationId, commentId, loadThread]);
    
    useEffect(() => {
        if (commentId) {
            loadThread();
        }
    }, [commentId]);
    
    return {
        ...thread,
        loading,
        error,
        loadThread,
        addReply
    };
}

export { 
    CommentClient, 
    useComments, 
    useCommentThread,
    Comment,
    Reaction
};
Docker Compose Example
Create docker-compose.yml:

yaml
version: '3.8'

services:
  comment-service:
    image: sologenic/comment-service:latest
    environment:
      - COMMENT_SERVICE_PORT=50060
      - COMMENT_STORE=comment-store:50060
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=comments
      - POSTGRES_USER=comment_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - ELASTICSEARCH_HOST=elasticsearch
      - ELASTICSEARCH_PORT=9200
      - MAX_COMMENT_DEPTH=10
      - MAX_COMMENT_LENGTH=5000
      - MODERATION_ENABLED=true
      - SPAM_THRESHOLD=0.7
      - LOG_LEVEL=info
    ports:
      - "50060:50060"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
      - elasticsearch
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50060"]
      interval: 30s
      timeout: 10s
      retries: 3

  comment-store:
    image: sologenic/comment-store:latest
    environment:
      - COMMENT_STORE_PORT=50061
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=comments
      - POSTGRES_USER=comment_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - CACHE_TTL=60
    ports:
      - "50061:50061"
    networks:
      - internal
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=comments
      - POSTGRES_USER=comment_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U comment_user -d comments"]
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
  elasticsearch_data:
Environment Setup (.env file)
bash
# Database Configuration
DB_PASSWORD=your_secure_password

# Service Configuration
COMMENT_STORE=comment-store:50061
COMMENT_STORE_TESTING=FALSE

# Cache Configuration
COMMENT_CACHE_TTL=60

# Business Rules
MAX_COMMENT_DEPTH=10
MAX_COMMENT_LENGTH=5000

# Moderation
MODERATION_ENABLED=true
SPAM_THRESHOLD=0.7

# Logging
LOG_LEVEL=info
Testing Mode
The client automatically detects test mode when COMMENT_STORE_TESTING=TRUE is set. In test mode:

No gRPC connection is established

In-memory mock responses are used

No external dependencies required

bash
# Run in test mode
export COMMENT_STORE_TESTING=TRUE
go test ./...
Error Handling
go
// Example error handling in Go
resp, err := client.CreateComment(ctx, req)
if err != nil {
    if strings.Contains(err.Error(), "SPAM_DETECTED") {
        // Handle spam
    } else if strings.Contains(err.Error(), "RATE_LIMIT") {
        // Implement backoff
    }
    log.Printf("Error: %v", err)
}
License
This documentation is part of the TX Marketplace platform.


