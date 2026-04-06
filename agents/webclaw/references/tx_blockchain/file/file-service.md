# File Service

The File Service provides RESTful and gRPC interfaces for file management, including temporary upload storage, permanent file commitment, and file download capabilities. The service uses Google Cloud Storage with automatic garbage collection for temporary files.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ File Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ REST API Endpoints │ │
│ ├───────────────┬───────────────┬─────────────────────────────────────┤ │
│ │ POST /upload │ GET /download │ GET /exist │ │
│ │ (Authenticated│ (Public) │ (Authenticated) │ │
│ │ - Temp Store) │ │ │ │
│ └───────────────┴───────────────┴─────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ gRPC Interface (Internal) │ │
│ │ │ │
│ │ Commit(TempFileName, PermanentPath, AllowOverwrite, Network) │ │
│ │ → Moves file from temp to permanent storage │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Google Cloud Storage │ │
│ ├─────────────────────────────┬───────────────────────────────────────┤ │
│ │ Temp Bucket │ Permanent Bucket │ │
│ │ • 30-day TTL │ • No auto-deletion │ │
│ │ • Public readable │ • Application-managed │ │
│ │ • Auto-cleanup │ • Structured paths │ │
│ └─────────────────────────────┴───────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬─────────────────────────────────────┤ │
│ │ Organization │ Role Store │ Auth Firebase │ │
│ │ Store │ │ Service │ │
│ └───────────────┴───────────────┴─────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Storage Architecture

### Temp Bucket Configuration

| Property | Setting | Rationale |
|----------|---------|-----------|
| Location Type | Single region | Lowest cost |
| Storage Class | Standard | Balance of cost and performance |
| Access Control | Uniform | Simplified management |
| Public Access | Allowed (object viewer) | Files are publicly readable via hashed URLs |
| Lifecycle Rule | Delete after 30 days | Automatic garbage collection |
| Versioning | Disabled | Not needed for temp files |

### Temp File Naming Convention

Temp files are made unique by the file service using:
{address_of_uploader}{network}{temp_filename}

text

Example: `rL54wzknUXxqiC8Tzs6mzLi3QJTtX5uVK6_mainnet_butterfly_300.jpg`

### Permanent File Path Structure

Permanent files follow application-defined structure:
{app}/{internal_app_structure1}/{internal_app_structure2}/.../{final_file_name}

text

Example: `nft/rExzpKuv1tgATE6FZvgoaXtguXMMjW3AqYbR/410446e5-e59e-4573-a7d2-b2bf7622775b`

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| POST /api/file/upload | NORMAL_USER | Upload file to temporary storage |
| GET /api/file/exist | NORMAL_USER | Check if file exists |
| GET /api/file/download | None (Public) | Download file (temp or committed) |
| Commit (gRPC) | Internal Service | Move file from temp to permanent |

**Note:** All authenticated requests must include:
- `Network` header (mainnet, testnet, devnet)
- `OrganizationID` header (organization UUID)
- `Authorization` header (Bearer token from Firebase)

## Data Models

### Upload Response

```json
{
  "Filename": "base64_encoded_temp_filename_string"
}
Temp Filename Structure (Decoded)
json
{
  "Address": "rL54wzknUXxqiC8Tzs6mzLi3QJTtX5uVK6",
  "Network": "mainnet",
  "TempFilename": "butterfly_300.jpg",
  "ExternalKeys": [
    {
      "Key": "collection_id",
      "Value": "rExzpKuv1tgATE6FZvgoaXtguXMMjW3AqYbR"
    },
    {
      "Key": "nft_uuid",
      "Value": "410446e5-e59e-4573-a7d2-b2bf7622775b"
    }
  ]
}
Exist Response
json
{
  "Exist": true
}
Commit Request (gRPC)
Field	Type	Description
TempFileName	string	Temp filename from upload response
PermanentPath	string	Base64 encoded permanent path with final filename
AllowOverwrite	bool	Whether to overwrite if file exists
Network	string	Network environment
Commit Response (gRPC)
Field	Type	Description
FileFound	bool	Whether temp file was found
PublicURL	string	Publicly accessible file URL
Network	string	Network environment
API Endpoints
POST /api/file/upload (Authenticated)
Uploads a file to temporary storage. Returns a base64-encoded temp filename that must be used for commit and download operations.

Headers
Header	Description	Required
Content-Type	multipart/form-data	Yes
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
address	XRP/blockchain address	Yes
Request Body
Field	Type	Description	Required
file	file	File attachment	Yes
Note: Multiple attachments are not allowed. Each request can upload only one file.

Example Request
bash
curl --location 'https://api.sologenic.org/api/file/upload' \
  --header 'address: rL54wzknUXxqiC8Tzs6mzLi3QJTtX5uVK6' \
  --header 'Content-Type: multipart/form-data' \
  --header 'Authorization: Bearer: eyJhbGciOiJSUzI1NiIs...' \
  --header 'Network: mainnet' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --form 'file=@"/Users/username/Downloads/butterfly_300.jpg"'
Example Response
json
{
  "Filename": "eyJBZGRyZXNzIjoickw1NHd6a25VWHhxaUM4VHpzNm16TGkzUUpUdFg1dVZLNiIsIk5ldHdvcmsiOiJtYWlubmV0IiwiVGVtcEZpbGVuYW1lIjoiYnV0dGVyZmx5XzMwMC5qcGciLCJFeHRlcm5hbEtleXMiOlt7IktleSI6ImNvbGxlY3Rpb25faWQiLCJWYWx1ZSI6InJFeXpwS3V2MXRnQVRFNkZadmdvYVh0Z3VYTU1qV3lxYlIifSx7IktleSI6Im5mdF91aWQiLCJWYWx1ZSI6IjQxMDQ0NmU1LWU1OWUtNDU3My1hN2QyLWIyYmY3NjIyNzc1YiJ9XX0="
}
Error Responses
Status Code	Description
400	Bad request - missing file or invalid headers
401	Unauthorized - invalid or missing token
413	Payload too large - file exceeds size limit
500	Internal server error
GET /api/file/download (Public)
Downloads a file from temporary or permanent storage. The service automatically determines whether the filename refers to a temp file or committed file.

Headers
Header	Description	Required
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Note: Authorization is NOT required for downloads (public access).

Query Parameters
Parameter	Type	Description	Required
filename	string	Base64-encoded filename	Yes
Filename Resolution Logic
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Filename Resolution Logic                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  filename parameter (base64)                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Decode base64 to string                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Can it be parsed as temporary file structure?                        │   │
│  │ (Contains Address, Network, TempFilename fields)                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
│            ┌─────────────┴─────────────┐                                   │
│            │ Yes                       │ No                                │
│            ▼                           ▼                                   │
│  ┌─────────────────┐         ┌─────────────────────────────────────────┐  │
│  │ Temporary File  │         │ Committed File                          │  │
│  │ • Look in temp  │         │ • Use string as full path               │  │
│  │   bucket        │         │ • Look in permanent bucket              │  │
│  │ • Return stream │         │ • Return stream                         │  │
│  └─────────────────┘         └─────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Example Request
bash
curl --location 'https://api.sologenic.org/api/file/download?filename=bmZ0L3JFeXpwS3V2MXRnQVRFNkZadmdvYVh0Z3VYTU1qV3lxYlIvNDEwNDQ2ZTUtZTU5ZS00NTczLWE3ZDItYjJiZjc2MjI3NzVi' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --header 'Network: mainnet' \
  --output downloaded_file.jpg
Response
The response status code is 200 with binary stream of the file. No JSON body is returned.

Content-Type	Description
image/jpeg	JPEG image
image/png	PNG image
application/pdf	PDF document
application/octet-stream	Generic binary file
Example Response Headers
text
HTTP/1.1 200 OK
Content-Type: image/jpeg
Content-Length: 245760
Content-Disposition: inline; filename="butterfly_300.jpg"
Cache-Control: public, max-age=3600
Error Responses
Status Code	Description
400	Bad request - missing filename
404	File not found
500	Internal server error
GET /api/file/exist (Authenticated)
Checks if a file exists in storage. Can check both temporary and committed files.

Headers
Header	Description	Required
Authorization	Bearer <firebase_token>	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Query Parameters
Parameter	Type	Description	Required	Default
filename	string	Base64-encoded filename	Yes	-
committed	boolean	Check committed file location	No	false
Example Request (Temp File)
bash
curl --location 'https://api.sologenic.org/api/file/exist?filename=eyJBZGRyZXNzIjoickw1NHd6a25VWHhxaUM4VHpzNm16TGkzUUpUdFg1dVZLNiIsIk5ldHdvcmsiOiJtYWlubmV0IiwiVGVtcEZpbGVuYW1lIjoiYnV0dGVyZmx5XzMwMC5qcGciLCJFeHRlcm5hbEtleXMiOlt7IktleSI6ImNvbGxlY3Rpb25faWQiLCJWYWx1ZSI6InJFeXpwS3V2MXRnQVRFNkZadmdvYVh0Z3VYTU1qV3lxYlIifSx7IktleSI6Im5mdF91aWQiLCJWYWx1ZSI6IjQxMDQ0NmU1LWU1OWUtNDU3My1hN2QyLWIyYmY3NjIyNzc1YiJ9XX0=' \
  --header 'Authorization: Bearer: eyJhbGciOiJSUzI1NiIs...' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --header 'Network: mainnet'
Example Request (Committed File)
bash
curl --location 'https://api.sologenic.org/api/file/exist?filename=bmZ0L3JFeXpwS3V2MXRnQVRFNkZadmdvYVh0Z3VYTU1qV3lxYlIvNDEwNDQ2ZTUtZTU5ZS00NTczLWE3ZDItYjJiZjc2MjI3NzVi&committed=true' \
  --header 'Authorization: Bearer: eyJhbGciOiJSUzI1NiIs...' \
  --header 'OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71' \
  --header 'Network: mainnet'
Example Response
json
{
  "Exist": true
}
gRPC Interface
Commit Service
Moves a temporary file to its permanent location. This is an internal gRPC endpoint used by backend services.

Proto Definition
protobuf
service FileService {
    rpc Commit(CommitRequest) returns (CommitResponse);
}

message CommitRequest {
    string TempFileName = 1;    // Temp filename from upload
    string PermanentPath = 2;   // Base64 encoded permanent path
    bool AllowOverwrite = 3;     // Overwrite if exists
    string Network = 4;          // Network environment
}

message CommitResponse {
    bool FileFound = 1;          // Temp file found
    string PublicURL = 2;        // Public URL of committed file
    string Network = 3;          // Network environment
}
Commit Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Commit Flow                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Service calls Commit(TempFileName, PermanentPath, AllowOverwrite)         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ 1. Validate TempFileName exists in temp bucket              │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                          │                                          │   │
│  │            ┌─────────────┴─────────────┐                           │   │
│  │            │ Found                     │ Not Found                  │   │
│  │            ▼                           ▼                           │   │
│  │  ┌─────────────────┐         ┌─────────────────────────────────┐  │   │
│  │  │ 2. Check if     │         │ Return FileFound: false          │  │   │
│  │  │ permanent file  │         │ Client must re-upload            │  │   │
│  │  │ exists          │         └─────────────────────────────────┘  │   │
│  │  └─────────────────┘                                               │   │
│  │            │                                                        │   │
│  │            ▼                                                        │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │ 3. If exists and AllowOverwrite = false:                    │   │   │
│  │  │    Return error (file already exists)                       │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │            │                                                        │   │
│  │            ▼                                                        │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │ 4. Move file from temp to permanent location                │   │   │
│  │  │    • Copy object                                             │   │   │
│  │  │    • Delete temp object                                      │   │   │
│  │  │    • Set appropriate permissions                             │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │            │                                                        │   │
│  │            ▼                                                        │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │ 5. Return FileFound: true and PublicURL                     │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Go gRPC Client Example
go
package main

import (
    "context"
    "encoding/base64"
    "log"
    "time"

    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    
    filepb "github.com/sologenic/com-file-service/proto"
)

type FileServiceClient struct {
    client filepb.FileServiceClient
    conn   *grpc.ClientConn
}

func NewFileServiceClient(endpoint string) (*FileServiceClient, error) {
    conn, err := grpc.Dial(
        endpoint,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
    )
    if err != nil {
        return nil, err
    }
    
    return &FileServiceClient{
        client: filepb.NewFileServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *FileServiceClient) Close() error {
    return c.conn.Close()
}

func (c *FileServiceClient) CommitFile(
    ctx context.Context,
    tempFileName string,
    permanentPath string,
    allowOverwrite bool,
    network string,
) (*filepb.CommitResponse, error) {
    // Encode permanent path to base64
    encodedPath := base64.StdEncoding.EncodeToString([]byte(permanentPath))
    
    request := &filepb.CommitRequest{
        TempFileName:   tempFileName,
        PermanentPath:  encodedPath,
        AllowOverwrite: allowOverwrite,
        Network:        network,
    }
    
    return c.client.Commit(ctx, request)
}

// Usage
func main() {
    client, err := NewFileServiceClient("file-service:50051")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    
    // Commit a file
    response, err := client.CommitFile(
        ctx,
        "temp_filename_from_upload",
        "nft/collection123/nft456/image.jpg",
        false, // Don't overwrite if exists
        "mainnet",
    )
    if err != nil {
        log.Printf("Commit failed: %v", err)
        return
    }
    
    if !response.FileFound {
        log.Println("Temp file not found, need to re-upload")
        return
    }
    
    log.Printf("File committed successfully! Public URL: %s", response.PublicURL)
}
Integration Examples
Complete Upload-Then-Commit Flow
javascript
// Complete file upload and commit flow
class FileServiceClient {
  constructor(baseUrl, token, orgId, network, address) {
    this.baseUrl = baseUrl;
    this.token = token;
    this.orgId = orgId;
    this.network = network;
    this.address = address;
  }

  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/api/file/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer: ${this.token}`,
        'OrganizationID': this.orgId,
        'Network': this.network,
        'address': this.address
      },
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data.Filename; // Base64 encoded temp filename
  }

  async checkFileExists(filename, committed = false) {
    const url = `${this.baseUrl}/api/file/exist?filename=${encodeURIComponent(filename)}&committed=${committed}`;
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer: ${this.token}`,
        'OrganizationID': this.orgId,
        'Network': this.network
      }
    });

    if (!response.ok) {
      return false;
    }

    const data = await response.json();
    return data.Exist;
  }

  async downloadFile(filename) {
    const url = `${this.baseUrl}/api/file/download?filename=${encodeURIComponent(filename)}`;
    
    const response = await fetch(url, {
      headers: {
        'OrganizationID': this.orgId,
        'Network': this.network
      }
    });

    if (!response.ok) {
      throw new Error(`Download failed: ${response.statusText}`);
    }

    return response; // Returns Response object with body stream
  }

  async saveToLocal(filename, outputPath) {
    const response = await this.downloadFile(filename);
    
    // Save to file system (Node.js example)
    const buffer = await response.arrayBuffer();
    const fs = require('fs');
    fs.writeFileSync(outputPath, Buffer.from(buffer));
    
    return outputPath;
  }

  async displayImage(filename, imageElement) {
    const response = await this.downloadFile(filename);
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    imageElement.src = url;
    return url;
  }
}

// Usage
async function example() {
  const client = new FileServiceClient(
    'https://api.sologenic.org',
    'firebase-token',
    'org-uuid',
    'mainnet',
    'rL54wzknUXxqiC8Tzs6mzLi3QJTtX5uVK6'
  );

  // 1. Upload file
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const tempFilename = await client.uploadFile(file);
  console.log('Uploaded temp file:', tempFilename);

  // 2. Check if file exists
  const exists = await client.checkFileExists(tempFilename);
  console.log('File exists in temp:', exists);

  // 3. Download and display (preview)
  const imgElement = document.getElementById('preview');
  await client.displayImage(tempFilename, imgElement);

  // 4. Later, commit the file (via backend gRPC)
  // This would be called from your backend service
}
React File Upload Component
jsx
import React, { useState, useCallback } from 'react';

function FileUploader({ onUploadComplete, onCommitComplete }) {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [tempFilename, setTempFilename] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = useCallback(async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    setError(null);
    setUploadProgress(0);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      // Upload file
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/file/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer: ${localStorage.getItem('token')}`,
          'OrganizationID': localStorage.getItem('orgId'),
          'Network': 'mainnet',
          'address': localStorage.getItem('address')
        },
        body: formData
      });

      clearInterval(progressInterval);

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      setTempFilename(data.Filename);
      setUploadProgress(100);

      // Create preview
      const previewResponse = await fetch(`/api/file/download?filename=${encodeURIComponent(data.Filename)}`, {
        headers: {
          'OrganizationID': localStorage.getItem('orgId'),
          'Network': 'mainnet'
        }
      });
      
      const blob = await previewResponse.blob();
      const url = URL.createObjectURL(blob);
      setPreviewUrl(url);

      onUploadComplete?.(data.Filename);

    } catch (err) {
      setError(err.message);
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  }, [onUploadComplete]);

  const handleCommit = async () => {
    if (!tempFilename) return;

    setUploading(true);
    try {
      // Call your backend to commit the file
      const response = await fetch('/api/nft/commit-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer: ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          tempFilename: tempFilename,
          permanentPath: `nft/${collectionId}/${nftId}/image.jpg`,
          allowOverwrite: false
        })
      });

      if (!response.ok) {
        throw new Error('Commit failed');
      }

      onCommitComplete?.();
      
      // Clear preview
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
        setPreviewUrl(null);
      }
      
      setTempFilename(null);

    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-uploader">
      <input
        type="file"
        onChange={handleFileSelect}
        disabled={uploading}
        accept="image/*,application/pdf"
      />
      
      {uploading && (
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${uploadProgress}%` }}
          />
          <span>{uploadProgress}%</span>
        </div>
      )}
      
      {previewUrl && (
        <div className="preview">
          <img src={previewUrl} alt="Preview" />
          <button onClick={handleCommit} disabled={uploading}>
            Commit File
          </button>
        </div>
      )}
      
      {error && (
        <div className="error">
          Error: {error}
        </div>
      )}
    </div>
  );
}

export default FileUploader;
Node.js Backend Commit Handler
javascript
// Backend service to handle file commits
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const PROTO_PATH = './proto/file-service.proto';

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const fileProto = grpc.loadPackageDefinition(packageDefinition);

class FileCommitService {
  constructor(fileServiceEndpoint) {
    this.client = new fileProto.file.FileService(
      fileServiceEndpoint,
      grpc.credentials.createInsecure()
    );
  }

  async commitFile(tempFileName, permanentPath, allowOverwrite, network) {
    return new Promise((resolve, reject) => {
      // Encode permanent path to base64
      const encodedPath = Buffer.from(permanentPath).toString('base64');

      const request = {
        TempFileName: tempFileName,
        PermanentPath: encodedPath,
        AllowOverwrite: allowOverwrite,
        Network: network
      };

      this.client.Commit(request, (error, response) => {
        if (error) {
          reject(error);
        } else {
          resolve(response);
        }
      });
    });
  }

  async commitNFTImage(tempFilename, collectionId, nftId, allowOverwrite = false) {
    const permanentPath = `nft/${collectionId}/${nftId}/image.jpg`;
    return this.commitFile(
      tempFilename,
      permanentPath,
      allowOverwrite,
      'mainnet'
    );
  }

  async commitDocument(tempFilename, userId, documentType, fileName, allowOverwrite = false) {
    const permanentPath = `documents/${userId}/${documentType}/${fileName}`;
    return this.commitFile(
      tempFilename,
      permanentPath,
      allowOverwrite,
      'mainnet'
    );
  }
}

// Express route handler
app.post('/api/nft/commit-image', async (req, res) => {
  const { tempFilename, permanentPath, allowOverwrite } = req.body;
  const network = req.headers.network || 'mainnet';

  try {
    const fileService = new FileCommitService('file-service:50051');
    const response = await fileService.commitFile(
      tempFilename,
      permanentPath,
      allowOverwrite,
      network
    );

    if (!response.FileFound) {
      return res.status(404).json({
        error: 'Temp file not found',
        message: 'The temporary file no longer exists. Please re-upload.'
      });
    }

    res.json({
      success: true,
      publicUrl: response.PublicURL,
      network: response.Network
    });

  } catch (error) {
    console.error('Commit error:', error);
    res.status(500).json({
      error: 'Commit failed',
      message: error.message
    });
  }
});
Garbage Collection
Temp Bucket Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Temp Bucket Garbage Collection                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  File Uploaded to Temp Bucket                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ • File stored with creation timestamp                                │   │
│  │ • TTL = 30 days from creation                                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Normal Processing (seconds to minutes)                               │   │
│  │ • File is committed via gRPC                                         │   │
│  │ • File moved to permanent location                                   │   │
│  │ • Temp file deleted                                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ If Not Committed (abandoned upload)                                  │   │
│  │ • File remains in temp bucket                                        │   │
│  │ • After 30 days, lifecycle rule triggers deletion                    │   │
│  │ • No manual cleanup required                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  Expected Percentiles:                                                      │
│  • 99%: Processed within 24 hours                                          │
│  • 99.99%: Processed within 5 days                                         │
│  • 30-day TTL is sufficient for all normal use cases                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
GCS Lifecycle Rule Configuration
bash
# Set lifecycle rule for temp bucket
gsutil lifecycle set lifecycle.json gs://your-temp-bucket
lifecycle.json:

json
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {
        "age": 30,
        "isLive": true
      }
    }
  ]
}
GCS Bucket Setup
Step-by-Step Temp Bucket Configuration
bash
# 1. Create bucket
gsutil mb -l us-central1 -c standard gs://your-temp-bucket

# 2. Disable public access prevention
gsutil iam ch allUsers:objectViewer gs://your-temp-bucket

# 3. Set lifecycle rule
cat > lifecycle.json << EOF
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 30}
    }
  ]
}
EOF

gsutil lifecycle set lifecycle.json gs://your-temp-bucket

# 4. Verify configuration
gsutil lifecycle get gs://your-temp-bucket
Bucket Properties Summary
Property	Temp Bucket	Permanent Bucket
Location	us-central1	us-central1
Storage Class	Standard	Standard
Public Access	AllUsers:objectViewer	Application-managed
Lifecycle	Delete after 30 days	None
Versioning	Disabled	Optional
Encryption	Google-managed	Google-managed
Nginx Configuration
Increasing Request Body Size
For large file uploads (up to 100MB), configure nginx ingress:

yaml
# file-service.yaml.erb
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: file-service-ingress
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"
spec:
  rules:
  - host: api.sologenic.org
    http:
      paths:
      - path: /api/file
        pathType: Prefix
        backend:
          service:
            name: file-service
            port:
              number: 8080
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	com-be-http-lib
PROJECT_ID	Google Cloud project ID	GCP
CREDENTIALS_LOC
CREDENTIALS_LOCATION	Google Cloud credentials location	GCP
ORGANIZATION_STORE	Organization service endpoint	com-fs-organization-model
ROLE_STORE	Role store endpoint	com-be-admin-role-store
AUTH_FIREBASE_SERVICE	Firebase auth service endpoint	com-fs-auth-firebase-service
Example Environment Configuration
bash
# Required
PROJECT_ID=sologenic-platform
CREDENTIALS_LOCATION=/secrets/gcp-credentials.json
ORGANIZATION_STORE=organization-service:50060
ROLE_STORE=role-store:50066
AUTH_FIREBASE_SERVICE=auth-service:50070

# Optional
LOG_LEVEL=info
MAX_FILE_SIZE_MB=100
ALLOWED_MIME_TYPES=image/jpeg,image/png,image/gif,application/pdf
TEMP_BUCKET=sologenic-temp-files
PERMANENT_BUCKET=sologenic-permanent-files

# HTTP Configuration
HTTP_CONFIG='{
  "port": ":8080",
  "cors": {
    "allowedOrigins": ["http://localhost:3000", "https://app.sologenic.org"]
  },
  "timeouts": {
    "read": "30s",
    "write": "30s",
    "idle": "60s",
    "shutdown": "10s"
  }
}'
Docker Compose Example
yaml
version: '3.8'

services:
  file-service:
    image: sologenic/file-service:latest
    environment:
      - PROJECT_ID=${GCP_PROJECT_ID}
      - CREDENTIALS_LOCATION=/secrets/gcp-credentials.json
      - ORGANIZATION_STORE=organization-service:50060
      - ROLE_STORE=role-store:50066
      - AUTH_FIREBASE_SERVICE=auth-service:50070
      - LOG_LEVEL=info
      - MAX_FILE_SIZE_MB=100
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
      - "50051:50051"
    volumes:
      - ./secrets:/secrets
    networks:
      - internal

  organization-service:
    image: sologenic/organization-service:latest
    networks:
      - internal

  role-store:
    image: sologenic/role-store:latest
    networks:
      - internal

  auth-service:
    image: sologenic/auth-service:latest
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Responses
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Missing required parameter: filename",
  "required_params": ["filename"]
}
Unauthorized (401)
json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "File not found",
  "filename": "base64_encoded_filename"
}
Payload Too Large (413)
json
{
  "error": "Payload Too Large",
  "message": "File size exceeds maximum allowed size",
  "max_size_mb": 100,
  "actual_size_mb": 150
}
Conflict (409) - File Already Exists
json
{
  "error": "Conflict",
  "message": "File already exists at permanent location",
  "permanent_path": "nft/collection123/nft456/image.jpg",
  "allow_overwrite": false
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Upload fails with 413	File too large	Increase nginx proxy-body-size
Temp file not found	TTL expired	Re-upload file (30-day window)
Download returns 404	Wrong filename encoding	Verify base64 encoding
Commit fails	Temp file already committed	Check if file exists in permanent location
CORS errors	Missing CORS headers	Configure HTTP_CONFIG CORS settings
Slow uploads	Network latency	Increase proxy timeouts
Debugging Commands
bash
# Check GCS bucket contents
gsutil ls gs://your-temp-bucket/

# Check file age
gsutil ls -l gs://your-temp-bucket/

# Test upload with curl
curl -X POST https://api.sologenic.org/api/file/upload \
  -H "Authorization: Bearer: $TOKEN" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -H "address: $ADDRESS" \
  -F "file=@test.jpg" \
  -v

# Test download
curl -X GET "https://api.sologenic.org/api/file/download?filename=$FILENAME" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  --output downloaded.jpg \
  -v

# Check file existence
curl -X GET "https://api.sologenic.org/api/file/exist?filename=$FILENAME&committed=true" \
  -H "Authorization: Bearer: $TOKEN" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet"
Best Practices
File Upload
Practice	Recommendation
File size limit	100MB maximum
Allowed types	Images, PDFs, Documents
Client-side validation	Validate file type before upload
Progress indicators	Show upload progress to users
Retry logic	Implement exponential backoff
Security
Concern	Mitigation
File enumeration	Use hashed, unguessable filenames
MIME type spoofing	Validate MIME type server-side
Malicious files	Scan files for malware
Rate limiting	Limit uploads per user/IP
Public access	Temp files are public but unguessable
Performance
Scenario	Recommendation
Large files	Use chunked upload
Many small files	Batch commit operations
High throughput	Increase replica count
Geographic distribution	Use CDN for permanent files
Data Management
Practice	Recommendation
Commit promptly	Commit within 24 hours
Clean up	Let TTL handle abandoned uploads
Permanent paths	Use consistent naming convention
Backups	Backup permanent bucket regularly
Testing FE
Running Test Frontend
bash
# Navigate to app root
cd /path/to/app

# Run test script
./bin/test.sh

# Open browser to localhost:3000
Testing Notes
PermanentFileName input should be in plain text (not base64 encoded)

The testing FE automatically encodes it to base64

Check "Filename" checkbox for temporary file downloads

The service differentiates temp vs committed without extra parameters

Related Services
Service	Description
Organization Service	Tenant isolation
Role Service	Access control
Auth Service	Authentication
Admin File Service	File management admin endpoints
License
This documentation is part of the TX Marketplace platform.
