# Document Service

The Document Service provides RESTful interfaces for managing documents, including retrieving document metadata, listing available documents, and signing documents. Documents can include legal agreements, terms and conditions, contracts, and other important files that require user acknowledgement or signature.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Document Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├───────────────┬───────────────┬─────────────────────────────────────┤ │
│ │ GET /get │ GET /list │ PUT /sign │ │
│ │ (By MD5SUM) │ (With filter) │ (Sign document) │ │
│ └───────────────┴───────────────┴─────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Document Store│ User Store │ Role Store │ Organization │ │
│ │ │ │ │ Store │ │
│ │ Feature Flag │ Auth Firebase │ File Service │ │ │
│ │ Store │ Service │ │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Storage Layer │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Document Metadata Database │ │
│ │ • File Storage (via File Service) │ │
│ │ • User Signature Records │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/doc/get | ORGANIZATION_ADMINISTRATOR | Get document by MD5SUM |
| GET /api/doc/list | ORGANIZATION_ADMINISTRATOR | List documents with filtering |
| PUT /api/doc/sign | NORMAL_USER | Sign a document |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Organization ID in `OrganizationID` header (tenant isolation)
- Network in `Network` header (mainnet, testnet, devnet)

## Data Models

### Document Object

| Field | Type | Description |
|-------|------|-------------|
| OrganizationID | string | Organization UUID that owns the document |
| Name | string | Document name/identifier |
| Version | string | Document version (e.g., "1.0.0", "2.1.0") |
| Description | string | Human-readable document description |
| File | FileObject | File metadata (reference, extension, name, MD5SUM) |
| SignatureRequired | bool | Whether signature is required for this document |
| Status | string | Document status (ACTIVE, INACTIVE, ARCHIVED) |

### FileObject

| Field | Type | Description |
|-------|------|-------------|
| Reference | string | File reference ID (from file service) |
| Extension | string | File extension (e.g., "pdf", "docx", "txt") |
| Name | string | Display name of the file |
| MD5SUM | string | MD5 checksum of the file content |

### UserSignatureRecord

| Field | Type | Description |
|-------|------|-------------|
| UserID | string | User account ID who signed |
| DocumentName | string | Name of the signed document |
| SignedVersion | string | Version that was signed |
| DocumentState | int | State of the document when signed |
| FileMD5SUM | string | MD5SUM of the signed document |
| SignedAt | Timestamp | When the document was signed |
| OrganizationID | string | Organization UUID |

### DocumentState Values

| State ID | State Name | Description |
|----------|------------|-------------|
| 1 | DRAFT | Document in draft, not ready for signing |
| 2 | PUBLISHED | Document published and available for signing |
| 3 | SUPERSEDED | Document replaced by newer version |
| 4 | EXPIRED | Document no longer valid |
| 5 | REVOKED | Document revoked by organization |

### Document Status Values

| Status | Description |
|--------|-------------|
| ACTIVE | Document is active and available |
| INACTIVE | Document is temporarily unavailable |
| ARCHIVED | Document is archived (read-only) |

## API Endpoints

### GET /api/doc/get

Retrieves a document by its MD5SUM. This endpoint requires organization administrator privileges.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Content-Type | application/json | Yes |
| Network | mainnet, testnet, devnet | Yes |
| OrganizationID | Organization UUID | Yes |
| Authorization | Bearer <firebase_token> | Yes |

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| md5sum | string | MD5 checksum of the document file | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/doc/get?md5sum=d41d8cd98f00b204e9800998ecf8427e" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "Document": {
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    "Name": "TermsAndConditions",
    "Version": "2.1.0",
    "Description": "Legal terms and conditions for platform usage",
    "File": {
      "Reference": "file-ref-123e4567-e89b-12d3-a456-426614174000",
      "Extension": "pdf",
      "Name": "Terms and Conditions v2.1.pdf",
      "MD5SUM": "d41d8cd98f00b204e9800998ecf8427e"
    },
    "SignatureRequired": true,
    "Status": "ACTIVE"
  }
}
Error Responses
Status Code	Description
200	Success - Document found
400	Bad request - Missing md5sum parameter
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Document does not exist
500	Internal server error
GET /api/doc/list
Retrieves a list of documents based on provided filter parameters. This endpoint requires organization administrator privileges.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required
signature_required	bool	Filter by signature requirement	No
offset	int	Number of items to skip for pagination	No (default: 0)
limit	int	Maximum items to return	No (default: 20)
status	string	Filter by document status	No
name	string	Filter by document name (partial match)	No
Example Request
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/doc/list?signature_required=true&offset=0&limit=10" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "Documents": [
    {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "TermsAndConditions",
      "Version": "2.1.0",
      "Description": "Legal terms and conditions for platform usage",
      "File": {
        "Reference": "file-ref-123e4567-e89b-12d3-a456-426614174000",
        "Extension": "pdf",
        "Name": "Terms and Conditions v2.1.pdf",
        "MD5SUM": "d41d8cd98f00b204e9800998ecf8427e"
      },
      "SignatureRequired": true,
      "Status": "ACTIVE"
    },
    {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Name": "PrivacyPolicy",
      "Version": "1.5.0",
      "Description": "Privacy policy for user data protection",
      "File": {
        "Reference": "file-ref-456f7890-e89b-12d3-a456-426614174001",
        "Extension": "pdf",
        "Name": "Privacy Policy v1.5.pdf",
        "MD5SUM": "e99a18c428cb38d5f260853678922e03"
      },
      "SignatureRequired": true,
      "Status": "ACTIVE"
    }
  ],
  "Offset": 10
}
Error Responses
Status Code	Description
200	Success - Returns array (may be empty)
400	Bad request - Invalid filter parameters
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
500	Internal server error
PUT /api/doc/sign
Signs a document. This stores a reference to the signed document in the user's record. The user acknowledges agreement to the document's terms.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Request Body
Field	Type	Description	Required
Name	string	Document name being signed	Yes
SignedVersion	string	Version of the document being signed	Yes
DocumentState	int	State of the document when signed (see DocumentState Values)	Yes
FileMD5SUM	string	MD5 checksum of the signed document file	Yes
Example Request
bash
curl -X PUT \
  "https://api.admin.sologenic.org/api/doc/sign" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet" \
  -d '{
    "Name": "TermsAndConditions",
    "SignedVersion": "2.1.0",
    "DocumentState": 2,
    "FileMD5SUM": "d41d8cd98f00b204e9800998ecf8427e"
  }'
Example Response
json
{
  "Success": true,
  "Message": "Document signed successfully",
  "SignedAt": {
    "seconds": 1700000000,
    "nanos": 123456000
  }
}
Error Responses
Status Code	Description
200	Success - Document signed
400	Bad request - Missing required fields
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions or document not available for signing
404	Not found - Document not found
409	Conflict - Document already signed by user
500	Internal server error
Document Lifecycle
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Document Lifecycle                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Document Creation (Admin)                                         │   │
│  │    • Document uploaded to file service                               │   │
│  │    • Metadata stored in document store                               │   │
│  │    • Status: DRAFT, SignatureRequired: true/false                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Document Published (Admin)                                        │   │
│  │    • Status set to PUBLISHED (2)                                     │   │
│  │    • Document becomes available for signing                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. User Signs Document                                               │   │
│  │    • User acknowledges and signs document                            │   │
│  │    • Signature record stored in user profile                         │   │
│  │    • Timestamp recorded                                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. Document Update (Admin)                                           │   │
│  │    • New version created                                             │   │
│  │    • Old version marked SUPERSEDED (3)                               │   │
│  │    • Users may need to sign new version                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 5. Document Expiration/Revocation (Admin)                            │   │
│  │    • Status set to EXPIRED (4) or REVOKED (5)                        │   │
│  │    • Document no longer available for signing                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Document Signing Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Document Signing Flow                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User Action: Request to perform action requiring document agreement       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Example: User wants to trade, but needs to sign Terms & Conditions   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Check User's Signed Documents                                     │   │
│  │    • Query user record for signed documents                          │   │
│  │    • Check if required document is signed                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │                               │                       │
│                    ▼                               ▼                       │
│           ┌──────────────┐                ┌──────────────┐                │
│           │ Already      │                │ Not Signed   │                │
│           │ Signed       │                │ Yet          │                │
│           └──────────────┘                └──────────────┘                │
│                    │                               │                       │
│                    ▼                               ▼                       │
│           ┌──────────────┐                ┌──────────────┐                │
│           │ Proceed to   │                │ Present      │                │
│           │ Action       │                │ Document to  │                │
│           │              │                │ User         │                │
│           └──────────────┘                └──────────────┘                │
│                                                    │                       │
│                                                    ▼                       │
│                                           ┌──────────────┐                │
│                                           │ User Reviews │                │
│                                           │ Document     │                │
│                                           └──────────────┘                │
│                                                    │                       │
│                                                    ▼                       │
│                                           ┌──────────────┐                │
│                                           │ User Signs   │                │
│                                           │ (PUT /sign)  │                │
│                                           └──────────────┘                │
│                                                    │                       │
│                                                    ▼                       │
│                                           ┌──────────────┐                │
│                                           │ Record Stored│                │
│                                           │ in User      │                │
│                                           │ Profile      │                │
│                                           └──────────────┘                │
│                                                    │                       │
│                                                    ▼                       │
│                                           ┌──────────────┐                │
│                                           │ Proceed to   │                │
│                                           │ Action       │                │
│                                           └──────────────┘                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Document Types and Use Cases
Legal Agreements
Document Type	Description	Signature Required
Terms and Conditions	Platform usage terms	Yes
Privacy Policy	Data handling and privacy	Yes
Cookie Policy	Cookie usage disclosure	No
EULA	End-user license agreement	Yes
Compliance Documents
Document Type	Description	Signature Required
KYC Consent	Consent for KYC verification	Yes
Risk Disclosure	Trading risk acknowledgment	Yes
Tax Forms	Tax reporting forms (W-9, W-8BEN)	Yes
AML Policy	Anti-money laundering policy acknowledgment	Yes
Transaction Documents
Document Type	Description	Signature Required
Trade Confirmation	Confirmation of trade execution	Yes
Transfer Authorization	Authorization for asset transfer	Yes
Withdrawal Request	Fund withdrawal request	Yes
Signature Verification
Checking if User Signed a Document
javascript
// Example: Check if user has signed Terms and Conditions
async function hasUserSignedDocument(userId, documentName, version) {
  const response = await fetch('/api/user/get-signed-documents', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer: ${token}`,
      'OrganizationID': orgId,
      'Network': 'mainnet'
    }
  });
  
  const signedDocs = await response.json();
  
  return signedDocs.some(doc => 
    doc.Name === documentName && 
    doc.SignedVersion === version
  );
}

// Usage
const hasSigned = await hasUserSignedDocument(
  'user123', 
  'TermsAndConditions', 
  '2.1.0'
);

if (!hasSigned) {
  // Redirect user to sign document
  showDocumentSignatureModal();
}
Getting Document for Signing
javascript
// Get document by MD5SUM
async function getDocumentForSigning(md5sum) {
  const response = await fetch(`/api/doc/get?md5sum=${md5sum}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer: ${token}`,
      'OrganizationID': orgId,
      'Network': 'mainnet'
    }
  });
  
  return await response.json();
}

// Sign document
async function signDocument(documentName, version, md5sum) {
  const response = await fetch('/api/doc/sign', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer: ${token}`,
      'OrganizationID': orgId,
      'Network': 'mainnet'
    },
    body: JSON.stringify({
      Name: documentName,
      SignedVersion: version,
      DocumentState: 2, // PUBLISHED
      FileMD5SUM: md5sum
    })
  });
  
  return response.ok;
}
Integration Examples
React Component for Document Signing
jsx
import React, { useState, useEffect } from 'react';

function DocumentSigningModal({ documentName, version, md5sum, onSigned, onCancel }) {
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [signing, setSigning] = useState(false);
  const [agreed, setAgreed] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDocument();
  }, [md5sum]);

  const loadDocument = async () => {
    try {
      const response = await fetch(`/api/doc/get?md5sum=${md5sum}`, {
        headers: {
          'Authorization': `Bearer: ${localStorage.getItem('token')}`,
          'OrganizationID': localStorage.getItem('orgId'),
          'Network': 'mainnet'
        }
      });
      
      const data = await response.json();
      setDocument(data.Document);
      
      // Load actual file content from file service
      const fileResponse = await fetch(`/api/file/get?reference=${data.Document.File.Reference}`);
      const fileBlob = await fileResponse.blob();
      const fileUrl = URL.createObjectURL(fileBlob);
      setDocument(prev => ({ ...prev, fileUrl }));
      
    } catch (err) {
      setError('Failed to load document');
    } finally {
      setLoading(false);
    }
  };

  const handleSign = async () => {
    setSigning(true);
    try {
      const response = await fetch('/api/doc/sign', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer: ${localStorage.getItem('token')}`,
          'OrganizationID': localStorage.getItem('orgId'),
          'Network': 'mainnet'
        },
        body: JSON.stringify({
          Name: documentName,
          SignedVersion: version,
          DocumentState: 2,
          FileMD5SUM: md5sum
        })
      });
      
      if (response.ok) {
        onSigned();
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Failed to sign document');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setSigning(false);
    }
  };

  if (loading) {
    return <div className="modal">Loading document...</div>;
  }

  if (error) {
    return (
      <div className="modal error">
        <h3>Error</h3>
        <p>{error}</p>
        <button onClick={onCancel}>Close</button>
      </div>
    );
  }

  return (
    <div className="modal">
      <h2>Sign {document?.Name}</h2>
      <p>Version: {document?.Version}</p>
      <p>{document?.Description}</p>
      
      <div className="document-preview">
        <iframe src={document?.fileUrl} title="Document" />
      </div>
      
      <label className="checkbox-label">
        <input
          type="checkbox"
          checked={agreed}
          onChange={(e) => setAgreed(e.target.checked)}
        />
        I have read and agree to the {document?.Name}
      </label>
      
      <div className="modal-actions">
        <button onClick={onCancel} disabled={signing}>
          Cancel
        </button>
        <button 
          onClick={handleSign} 
          disabled={!agreed || signing}
          className="primary"
        >
          {signing ? 'Signing...' : 'Sign Document'}
        </button>
      </div>
    </div>
  );
}
Node.js Document Service Client
javascript
class DocumentService {
  constructor(baseUrl, token, orgId, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.token = token;
    this.orgId = orgId;
    this.network = network;
  }

  async getDocument(md5sum) {
    const response = await fetch(
      `${this.baseUrl}/api/doc/get?md5sum=${md5sum}`,
      {
        headers: this._getHeaders()
      }
    );
    
    if (!response.ok) {
      throw new Error(`Failed to get document: ${response.statusText}`);
    }
    
    return response.json();
  }

  async listDocuments(filters = {}) {
    const params = new URLSearchParams();
    if (filters.signatureRequired !== undefined) {
      params.append('signature_required', filters.signatureRequired);
    }
    if (filters.offset !== undefined) {
      params.append('offset', filters.offset);
    }
    if (filters.limit !== undefined) {
      params.append('limit', filters.limit);
    }
    if (filters.status) {
      params.append('status', filters.status);
    }
    if (filters.name) {
      params.append('name', filters.name);
    }
    
    const response = await fetch(
      `${this.baseUrl}/api/doc/list?${params.toString()}`,
      {
        headers: this._getHeaders()
      }
    );
    
    if (!response.ok) {
      throw new Error(`Failed to list documents: ${response.statusText}`);
    }
    
    return response.json();
  }

  async signDocument(documentName, version, md5sum) {
    const response = await fetch(`${this.baseUrl}/api/doc/sign`, {
      method: 'PUT',
      headers: {
        ...this._getHeaders(),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        Name: documentName,
        SignedVersion: version,
        DocumentState: 2, // PUBLISHED
        FileMD5SUM: md5sum
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Failed to sign document');
    }
    
    return response.json();
  }

  async requireSignature(documentName, version, md5sum) {
    // Check if user has already signed
    const hasSigned = await this._checkUserSigned(documentName, version);
    
    if (!hasSigned) {
      // Present document for signing
      const document = await this.getDocument(md5sum);
      return {
        required: true,
        document: document.Document
      };
    }
    
    return { required: false };
  }

  async _checkUserSigned(documentName, version) {
    // This would call a user service endpoint to check signed documents
    const response = await fetch(`${this.baseUrl}/api/user/signed-documents`, {
      headers: this._getHeaders()
    });
    
    const signedDocs = await response.json();
    return signedDocs.some(doc => 
      doc.Name === documentName && doc.SignedVersion === version
    );
  }

  _getHeaders() {
    return {
      'Authorization': `Bearer: ${this.token}`,
      'OrganizationID': this.orgId,
      'Network': this.network
    };
  }
}

// Usage
const docService = new DocumentService(
  'https://api.sologenic.org',
  'firebase-token',
  'org-uuid',
  'mainnet'
);

// List signature-required documents
const docs = await docService.listDocuments({ signatureRequired: true });

// Check if user needs to sign Terms and Conditions
const { required, document } = await docService.requireSignature(
  'TermsAndConditions',
  '2.1.0',
  'd41d8cd98f00b204e9800998ecf8427e'
);

if (required) {
  // Present document to user
  console.log('User must sign:', document.Name);
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/http/
DOCUMENT_STORE	Document service endpoint	github.com/sologenic/com-fs-document-model
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
USER_STORE	User management service	github.com/sologenic/com-fs-user-model
ROLE_STORE	Role management service	github.com/sologenic/com-fs-role-model
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-model
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
PAGE_SIZE	Default page size for list endpoints	20
MAX_PAGE_SIZE	Maximum page size allowed	100
Example Environment Configuration
bash
# Required
DOCUMENT_STORE=localhost:50062
AUTH_FIREBASE_SERVICE=localhost:50070
USER_STORE=localhost:50049
ROLE_STORE=localhost:50066
ORGANIZATION_STORE=localhost:50060
FEATURE_FLAG_STORE=localhost:50055

# Optional
LOG_LEVEL=debug
PAGE_SIZE=50
MAX_PAGE_SIZE=200

# HTTP Configuration
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
Docker Compose Example
yaml
version: '3.8'

services:
  document-service:
    image: sologenic/document-service:latest
    environment:
      - DOCUMENT_STORE=document-store:50062
      - AUTH_FIREBASE_SERVICE=auth-service:50070
      - USER_STORE=user-service:50049
      - ROLE_STORE=role-service:50066
      - ORGANIZATION_STORE=organization-service:50060
      - FEATURE_FLAG_STORE=feature-flag-service:50055
      - LOG_LEVEL=info
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
    networks:
      - internal

  document-store:
    image: sologenic/document-store:latest
    environment:
      - DATABASE_URL=postgres://user:pass@postgres:5432/documents
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Responses
Unauthorized (401)
json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token"
}
Forbidden (403)
json
{
  "error": "Forbidden",
  "message": "Insufficient permissions to access document",
  "required_role": "ORGANIZATION_ADMINISTRATOR"
}
Bad Request (400) - Missing MD5SUM
json
{
  "error": "Bad Request",
  "message": "Missing required parameter: md5sum"
}
Bad Request (400) - Invalid Document State
json
{
  "error": "Bad Request",
  "message": "Invalid document state",
  "details": "Document state must be one of: 1 (DRAFT), 2 (PUBLISHED), 3 (SUPERSEDED), 4 (EXPIRED), 5 (REVOKED)",
  "received": 6
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Document not found",
  "md5sum": "d41d8cd98f00b204e9800998ecf8427e"
}
Conflict (409) - Already Signed
json
{
  "error": "Conflict",
  "message": "Document already signed by user",
  "document_name": "TermsAndConditions",
  "signed_version": "2.1.0",
  "signed_at": "2024-01-01T00:00:00Z"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Document not found	Wrong MD5SUM	Verify MD5SUM matches document file
Cannot sign document	Document not in PUBLISHED state	Ensure document state is 2 (PUBLISHED)
Already signed	User previously signed this version	Check user's signed documents record
Permission denied	Missing admin role	Use ORGANIZATION_ADMINISTRATOR role for GET endpoints
File not loading	File reference invalid	Verify file exists in file service
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Test document retrieval:

bash
curl -X GET "/api/doc/get?md5sum=<md5sum>" \
  -H "Authorization: Bearer: <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet" \
  -v
List documents with filter:

bash
curl -X GET "/api/doc/list?signature_required=true&offset=0" \
  -H "Authorization: Bearer: <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet"
Check user signed documents:

bash
# This would be a user service endpoint
curl -X GET "/api/user/signed-documents" \
  -H "Authorization: Bearer: <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet"
Best Practices
Document Management
Version Control: Always increment version numbers for document updates

MD5SUM Verification: Use MD5SUM to ensure document integrity

Clear Descriptions: Provide meaningful document descriptions

Status Management: Use appropriate status values (ACTIVE, INACTIVE, ARCHIVED)

Signature Collection
Explicit Consent: Always require checkbox confirmation before signing

Document Preview: Show document content before requesting signature

Timestamp Recording: Record exact time of signature for legal compliance

Audit Trail: Maintain audit trail of all signatures

Compliance
GDPR Compliance: Store signature consent records

Legal Validity: Ensure signature records meet legal requirements

Data Retention: Follow document retention policies

Access Control: Restrict document access based on roles

Performance
Scenario	Recommendation
Large document lists	Use pagination with offset/limit
Document preview	Stream files rather than downloading fully
Multiple signatures	Batch sign requests when possible
Security
Secure Storage: Store documents in secure file service

Integrity Checking: Use MD5SUM to verify document integrity

Access Logging: Log all document access and signatures

Token Validation: Always validate authentication tokens

Related Services
Service	Description
File Service	Document file storage and retrieval
User Service	User profile and signed documents storage
Admin Document Service	Document administration (create, update, delete)
Organization Service	Tenant isolation
Admin Account Service	User and role management
License
This documentation is part of the TX Marketplace platform.
