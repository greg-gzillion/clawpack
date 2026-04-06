# MiniCMS Service

The MiniCMS Service provides lightweight content management functionality, enabling clients to retrieve active content blocks configured for specific pages and organizations.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ MiniCMS Service Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ REST API Endpoints (Unauthenticated) │ │
│ ├─────────────────────────────┬───────────────────────────────────────┤ │
│ │ GET /api/minicms/get │ GET /api/minicms/list │ │
│ │ (Get single content block) │ (List content with pagination) │ │
│ └─────────────────────────────┴───────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Content Filtering Engine │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Status check (active/inactive) │ │
│ │ • Time-based activation (ActiveFrom / ActiveUntil) │ │
│ │ • Organization isolation │ │
│ │ • Language filtering │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Data Sources │ │
│ ├─────────────────────────────┬───────────────────────────────────────┤ │
│ │ Organization Store │ Role Store │ │
│ │ (Tenant isolation) │ (Access control) │ │
│ │ Auth Firebase Service │ Feature Flag Store (optional) │ │
│ │ (Authentication) │ (Feature management) │ │
│ └─────────────────────────────┴───────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Key Features

- **Lightweight CMS**: Simple content management without complex overhead
- **Time-based Activation**: Schedule content to appear during specific time ranges
- **Organization Isolation**: Each tenant accesses only their content
- **Multi-language Support**: Content can be localized per language
- **Pagination Support**: Efficiently list content with limit/offset
- **Status Management**: Activate/deactivate content blocks

## Data Models

### ContentDetails Object

| Field | Type | Description |
|-------|------|-------------|
| ContentID | string | Unique identifier for the content block |
| BackgroundImage | File | Optional background image reference |
| Title | string | Content title/heading |
| Content | string | Main content body (HTML/text supported) |
| CallToAction | string | URL or action link |
| ActiveFrom | Timestamp | Start time for content activation |
| ActiveUntil | Timestamp | End time for content activation |
| Status | bool | Active status (true = active, false = inactive) |
| Identifier | string | Logical grouping identifier (e.g., "homepage_banner") |
| Language | Language | Language specification |
| OrganizationID | string | Organization UUID for tenant isolation |

### File Object

| Field | Type | Description |
|-------|------|-------------|
| Reference | string | Storage reference path (e.g., "cms/images/banner") |
| Extension | string | File extension (e.g., "jpg", "png", "webp") |
| Name | string | Optional display name for the file |

### Language Object

| Field | Type | Description |
|-------|------|-------------|
| Language | string | Language code (e.g., "en-US", "es-ES", "ja-JP") |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset (optional) |

### Metadata Object

| Field | Type | Description |
|-------|------|-------------|
| CreatedAt | Timestamp | Content creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |

### Audit Object

| Field | Type | Description |
|-------|------|-------------|
| ChangedAt | Timestamp | Last change timestamp |

### Content List Response

| Field | Type | Description |
|-------|------|-------------|
| Content | []ContentDetails | Array of content blocks |
| MetaData | Metadata | Response metadata |
| Audit | Audit | Audit information |

## API Endpoints

### GET /api/minicms/get

Retrieves a single piece of active content for the requested ContentID.

#### Headers

| Header | Description | Required | Example |
|--------|-------------|----------|---------|
| OrganizationID | Organization UUID | Yes | `215a551d-...-9284f40d1340` |
| Network | Network environment | Yes | `mainnet`, `testnet`, `devnet` |

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| content_id | string | Unique content identifier | Yes |

#### Content Activation Logic

Content will **ONLY** be returned if **ALL** conditions are met:

1. **Status = true** (content is marked active)
2. **Current UTC time >= ActiveFrom** (if ActiveFrom is set)
3. **Current UTC time <= ActiveUntil** (if ActiveUntil is set)
┌─────────────────────────────────────────────────────────────────────────────┐
│ Content Activation Timeline │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ActiveFrom = March 1, 2024 │
│ ActiveUntil = March 31, 2024 │
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Time Axis │ │
│ │ │ │
│ │ Feb 28 Mar 1 Mar 15 Mar 31 Apr 1 │ │
│ │ │ │ │ │ │ │ │
│ │ ▼ ▼ ▼ ▼ ▼ │ │
│ │ [INACTIVE] [ACTIVE───────ACTIVE───────ACTIVE] [INACTIVE] │ │
│ │ │ │
│ │ • Before Mar 1: Content not returned │ │
│ │ • Mar 1 - Mar 31: Content returned (if Status = true) │ │
│ │ • After Mar 31: Content not returned │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

#### Example Request

```bash
curl -X GET "https://api.sologenic.org/api/minicms/get?content_id=1234-5678" \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Network: mainnet"
Example Response
json
{
  "Content": {
    "ContentID": "1234-5678",
    "BackgroundImage": {
      "Reference": "cms/images/marketing_banner",
      "Extension": "jpg",
      "Name": "banner"
    },
    "Title": "Welcome to Solotex",
    "Content": "Asset tokenization and trading platform",
    "CallToAction": "https://solotex.com",
    "ActiveFrom": {
      "seconds": 1741900000
    },
    "ActiveUntil": {
      "seconds": 1745500000
    },
    "Status": true,
    "Identifier": "markets_top_left_block",
    "Language": {
      "Language": "en-US"
    },
    "OrganizationID": "215a551d-9284-4f72-ae9d-9284f40d1340"
  },
  "MetaData": {
    "CreatedAt": {
      "seconds": 1741890000
    },
    "UpdatedAt": {
      "seconds": 1741980000
    },
    "Network": 2
  },
  "Audit": {
    "ChangedAt": {
      "seconds": 1741983951
    }
  }
}
GET /api/minicms/list
Lists content with pagination support. The list can be filtered by identifier.

Headers
Header	Description	Required	Example
OrganizationID	Organization UUID	Yes	215a551d-...-9284f40d1340
Network	Network environment	Yes	mainnet, testnet, devnet
Query Parameters
Parameter	Type	Description	Required	Default
identifier	string	Filter by logical identifier	No	-
limit	integer	Maximum number of results	No	20
offset	integer	Number of results to skip	No	0
Note: Only active content (Status = true, within time range) is returned in the list.

Pagination Behavior
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Pagination Example                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Total Results: 45                                                          │
│  Default: limit=20, offset=0                                                │
│                                                                             │
│  Page 1: offset=0, limit=20  → Returns items 1-20                          │
│  Page 2: offset=20, limit=20 → Returns items 21-40                         │
│  Page 3: offset=40, limit=20 → Returns items 41-45                         │
│                                                                             │
│  Response includes no total count - use count endpoint if needed           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Example Request
bash
curl -X GET "https://api.sologenic.org/api/minicms/list?identifier=markets_bottom_left_block&offset=0&limit=10" \
  -H "Content-Type: application/json" \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Network: mainnet"
Example Response
json
{
  "Content": [
    {
      "ContentID": "1234-5678",
      "BackgroundImage": {
        "Reference": "cms/images/marketing_banner",
        "Extension": "jpg",
        "Name": "banner"
      },
      "Title": "Welcome to Solotex",
      "Content": "Asset tokenization and trading platform",
      "CallToAction": "https://solotex.com",
      "ActiveFrom": {
        "seconds": 1741900000
      },
      "ActiveUntil": {
        "seconds": 1745500000
      },
      "Status": true,
      "Identifier": "markets_bottom_left_block",
      "Language": {
        "Language": "en-US"
      },
      "OrganizationID": "215a551d-9284-4f72-ae9d-9284f40d1340"
    },
    {
      "ContentID": "5678-1234",
      "BackgroundImage": {
        "Reference": "cms/images/another_banner",
        "Extension": "jpg",
        "Name": "banner"
      },
      "Title": "Special Promotion",
      "Content": "Limited time offer on tokenized assets",
      "CallToAction": "https://solotex.com/promo",
      "ActiveFrom": {
        "seconds": 1742000000
      },
      "ActiveUntil": {
        "seconds": 1743000000
      },
      "Status": true,
      "Identifier": "markets_bottom_left_block",
      "Language": {
        "Language": "en-US"
      },
      "OrganizationID": "215a551d-9284-4f72-ae9d-9284f40d1340"
    }
  ],
  "MetaData": {
    "CreatedAt": {
      "seconds": 1741890000
    },
    "UpdatedAt": {
      "seconds": 1741980000
    },
    "Network": 2
  },
  "Audit": {
    "ChangedAt": {
      "seconds": 1741983951
    }
  }
}
Content Identifier Naming Conventions
Recommended Identifier Patterns
Use Case	Identifier Pattern	Example
Homepage Banners	homepage_banner_{position}	homepage_banner_top, homepage_banner_bottom
Marketing Blocks	marketing_{section}_{location}	marketing_hero_left, marketing_sidebar_right
Announcements	announcement_{type}	announcement_maintenance, announcement_feature
Legal Content	legal_{document_type}	legal_terms, legal_privacy, legal_cookies
Product Features	feature_{product_name}	feature_tokenization, feature_trading
Footer Sections	footer_{column}_{position}	footer_col1_about, footer_col2_links
Multi-language Support
For multi-language content, use the same Identifier with different Language codes:

text
Identifier: "homepage_welcome_message"
├── Language: "en-US" → "Welcome to our platform"
├── Language: "es-ES" → "Bienvenido a nuestra plataforma"
├── Language: "ja-JP" → "プラットフォームへようこそ"
└── Language: "zh-CN" → "欢迎来到我们的平台"
Integration Examples
JavaScript/React Component
javascript
// MiniCMS Client
class MiniCMSClient {
  constructor(baseUrl, organizationId, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.organizationId = organizationId;
    this.network = network;
  }

  async getContent(contentId) {
    const response = await fetch(
      `${this.baseUrl}/api/minicms/get?content_id=${encodeURIComponent(contentId)}`,
      {
        headers: this._getHeaders()
      }
    );

    if (!response.ok) {
      if (response.status === 404) {
        return null; // Content not found or inactive
      }
      throw new Error(`Failed to fetch content: ${response.statusText}`);
    }

    return response.json();
  }

  async listContent(identifier = null, limit = 20, offset = 0) {
    let url = `${this.baseUrl}/api/minicms/list?limit=${limit}&offset=${offset}`;
    if (identifier) {
      url += `&identifier=${encodeURIComponent(identifier)}`;
    }

    const response = await fetch(url, {
      headers: this._getHeaders()
    });

    if (!response.ok) {
      throw new Error(`Failed to list content: ${response.statusText}`);
    }

    return response.json();
  }

  async getContentByIdentifier(identifier, language = 'en-US') {
    const result = await this.listContent(identifier);
    const content = result.Content || [];
    
    // Find content matching language (fallback to first if exact match not found)
    let matched = content.find(c => c.Language?.Language === language);
    if (!matched && content.length > 0) {
      matched = content[0];
    }
    
    return matched;
  }

  _getHeaders() {
    return {
      'OrganizationID': this.organizationId,
      'Network': this.network
    };
  }
}

// React Component Example
function MarketingBanner({ contentId }) {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const client = new MiniCMSClient(
      'https://api.sologenic.org',
      '215a551d-9284-4f72-ae9d-9284f40d1340',
      'mainnet'
    );

    client.getContent(contentId)
      .then(response => {
        if (response && response.Content) {
          setContent(response.Content);
        }
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [contentId]);

  if (loading) return <div className="banner-loading">Loading...</div>;
  if (error) return <div className="banner-error">Failed to load content</div>;
  if (!content) return null;

  const backgroundStyle = content.BackgroundImage ? {
    backgroundImage: `url(/api/file/download?filename=${encodeURIComponent(content.BackgroundImage.Reference)}.${content.BackgroundImage.Extension})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center'
  } : {};

  return (
    <div className="marketing-banner" style={backgroundStyle}>
      <div className="banner-content">
        <h2>{content.Title}</h2>
        <div dangerouslySetInnerHTML={{ __html: content.Content }} />
        {content.CallToAction && (
          <a href={content.CallToAction} className="cta-button">
            Learn More →
          </a>
        )}
      </div>
    </div>
  );
}

// Example: Dynamic Content Block
function DynamicContentBlock({ identifier, language = 'en-US' }) {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const client = new MiniCMSClient(
      'https://api.sologenic.org',
      '215a551d-9284-4f72-ae9d-9284f40d1340',
      'mainnet'
    );

    client.getContentByIdentifier(identifier, language)
      .then(content => setContent(content))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [identifier, language]);

  if (loading) return <div>Loading content...</div>;
  if (!content) return null;

  return (
    <div className="dynamic-block">
      <h3>{content.Title}</h3>
      <div>{content.Content}</div>
      {content.CallToAction && (
        <a href={content.CallToAction} target="_blank" rel="noopener noreferrer">
          {content.CallToActionText || 'Learn More'}
        </a>
      )}
    </div>
  );
}

export { MiniCMSClient, MarketingBanner, DynamicContentBlock };
Node.js Backend Integration
javascript
// Node.js MiniCMS Client
const https = require('https');

class MiniCMSClient {
  constructor(baseUrl, organizationId, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.organizationId = organizationId;
    this.network = network;
  }

  async getContent(contentId) {
    const url = `${this.baseUrl}/api/minicms/get?content_id=${encodeURIComponent(contentId)}`;
    const response = await this._request(url);
    return response;
  }

  async listContent(identifier = null, limit = 20, offset = 0) {
    let url = `${this.baseUrl}/api/minicms/list?limit=${limit}&offset=${offset}`;
    if (identifier) {
      url += `&identifier=${encodeURIComponent(identifier)}`;
    }
    return this._request(url);
  }

  async getActiveContent(identifier, language = 'en-US') {
    const result = await this.listContent(identifier);
    const contents = result.Content || [];
    
    // Filter by language and active status
    const active = contents.filter(c => 
      c.Language?.Language === language && 
      c.Status === true &&
      this._isCurrentlyActive(c)
    );
    
    return active;
  }

  async getContentMap(identifiers, language = 'en-US') {
    const results = await Promise.all(
      identifiers.map(async id => ({
        identifier: id,
        content: await this.getContentByIdentifier(id, language)
      }))
    );
    
    return results.reduce((map, item) => {
      map[item.identifier] = item.content;
      return map;
    }, {});
  }

  async getContentByIdentifier(identifier, language = 'en-US') {
    const result = await this.listContent(identifier);
    const content = result.Content || [];
    
    // Find content by language
    let matched = content.find(c => c.Language?.Language === language);
    if (!matched && content.length > 0) {
      matched = content[0]; // Fallback to first available
    }
    
    return matched;
  }

  _isCurrentlyActive(content) {
    const now = Math.floor(Date.now() / 1000);
    
    if (content.Status !== true) return false;
    
    if (content.ActiveFrom && content.ActiveFrom.seconds > now) return false;
    if (content.ActiveUntil && content.ActiveUntil.seconds < now) return false;
    
    return true;
  }

  _request(url) {
    return new Promise((resolve, reject) => {
      const options = {
        headers: {
          'OrganizationID': this.organizationId,
          'Network': this.network
        }
      };
      
      https.get(url, options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(e);
          }
        });
      }).on('error', reject);
    });
  }
}

// Express Route Example
app.get('/api/page/:pageId/content', async (req, res) => {
  const { pageId } = req.params;
  const organizationId = req.headers.organizationid;
  const network = req.headers.network || 'mainnet';
  
  // Content identifiers for this page
  const pageContentMap = {
    'homepage': ['hero_banner', 'feature_blocks', 'testimonials', 'cta_section'],
    'markets': ['markets_header', 'markets_filters', 'markets_listing'],
    'profile': ['profile_welcome', 'profile_stats', 'profile_actions']
  };
  
  const identifiers = pageContentMap[pageId] || [];
  
  try {
    const client = new MiniCMSClient(
      'https://api.sologenic.org',
      organizationId,
      network
    );
    
    const contentMap = await client.getContentMap(identifiers, 'en-US');
    
    res.json({
      page: pageId,
      content: contentMap,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = { MiniCMSClient };
Python Client
python
import requests
from typing import Optional, Dict, List, Any
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class File:
    reference: str
    extension: str
    name: Optional[str] = None

@dataclass
class ContentDetails:
    content_id: str
    title: str
    content: str
    call_to_action: str
    status: bool
    identifier: str
    organization_id: str
    background_image: Optional[File] = None
    active_from: Optional[datetime] = None
    active_until: Optional[datetime] = None
    language: Optional[str] = None

class MiniCMSClient:
    def __init__(self, base_url: str, organization_id: str, network: str = 'mainnet'):
        self.base_url = base_url
        self.organization_id = organization_id
        self.network = network
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'OrganizationID': self.organization_id,
            'Network': self.network
        }
    
    def get_content(self, content_id: str) -> Optional[Dict[str, Any]]:
        """Get single content block by ID"""
        response = requests.get(
            f'{self.base_url}/api/minicms/get',
            params={'content_id': content_id},
            headers=self._get_headers()
        )
        
        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        return response.json()
    
    def list_content(self, identifier: Optional[str] = None, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """List content with pagination and optional identifier filter"""
        params = {'limit': limit, 'offset': offset}
        if identifier:
            params['identifier'] = identifier
        
        response = requests.get(
            f'{self.base_url}/api/minicms/list',
            params=params,
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_active_by_identifier(self, identifier: str, language: str = 'en-US') -> Optional[Dict[str, Any]]:
        """Get active content by identifier and language"""
        result = self.list_content(identifier)
        contents = result.get('Content', [])
        
        # Filter by language and active status
        active = [
            c for c in contents 
            if c.get('Language', {}).get('Language') == language 
            and self._is_currently_active(c)
        ]
        
        return active[0] if active else None
    
    def get_all_active_by_identifier(self, identifier: str) -> List[Dict[str, Any]]:
        """Get all active content for an identifier (all languages)"""
        result = self.list_content(identifier)
        contents = result.get('Content', [])
        
        return [c for c in contents if self._is_currently_active(c)]
    
    def get_content_map(self, identifiers: List[str], language: str = 'en-US') -> Dict[str, Optional[Dict[str, Any]]]:
        """Get multiple content blocks by identifiers"""
        content_map = {}
        for identifier in identifiers:
            content_map[identifier] = self.get_active_by_identifier(identifier, language)
        return content_map
    
    def _is_currently_active(self, content: Dict[str, Any]) -> bool:
        """Check if content is active based on status and time range"""
        now = datetime.utcnow().timestamp()
        
        if not content.get('Status', False):
            return False
        
        active_from = content.get('ActiveFrom')
        if active_from and active_from.get('seconds', 0) > now:
            return False
        
        active_until = content.get('ActiveUntil')
        if active_until and active_until.get('seconds', 0) < now:
            return False
        
        return True

# Flask Route Example
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/cms/<identifier>')
def get_cms_content(identifier):
    organization_id = request.headers.get('OrganizationID')
    network = request.headers.get('Network', 'mainnet')
    language = request.args.get('language', 'en-US')
    
    if not organization_id:
        return jsonify({'error': 'OrganizationID header required'}), 400
    
    client = MiniCMSClient(
        base_url='https://api.sologenic.org',
        organization_id=organization_id,
        network=network
    )
    
    content = client.get_active_by_identifier(identifier, language)
    
    if not content:
        return jsonify({'error': 'Content not found'}), 404
    
    return jsonify(content)

# Usage example
if __name__ == '__main__':
    client = MiniCMSClient(
        base_url='https://api.sologenic.org',
        organization_id='215a551d-9284-4f72-ae9d-9284f40d1340',
        network='mainnet'
    )
    
    # Get single content
    content = client.get_content('1234-5678')
    if content:
        print(f"Title: {content['Content']['Title']}")
    
    # List content by identifier
    banners = client.get_all_active_by_identifier('homepage_banner')
    for banner in banners:
        print(f"Banner: {banner['Title']} - {banner['Language']['Language']}")
    
    # Get content map
    content_map = client.get_content_map(['hero_banner', 'feature_blocks', 'cta_section'])
    for key, value in content_map.items():
        if value:
            print(f"{key}: {value['Title']}")
Go Client
go
package minicms

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "net/url"
    "time"
)

type File struct {
    Reference string  `json:"Reference"`
    Extension string  `json:"Extension"`
    Name      *string `json:"Name,omitempty"`
}

type Language struct {
    Language string `json:"Language"`
}

type Timestamp struct {
    Seconds int64 `json:"seconds"`
    Nanos   int32 `json:"nanos"`
}

type ContentDetails struct {
    ContentID       string     `json:"ContentID"`
    BackgroundImage *File      `json:"BackgroundImage,omitempty"`
    Title           string     `json:"Title"`
    Content         string     `json:"Content"`
    CallToAction    string     `json:"CallToAction"`
    ActiveFrom      *Timestamp `json:"ActiveFrom,omitempty"`
    ActiveUntil     *Timestamp `json:"ActiveUntil,omitempty"`
    Status          bool       `json:"Status"`
    Identifier      string     `json:"Identifier"`
    Language        *Language  `json:"Language,omitempty"`
    OrganizationID  string     `json:"OrganizationID"`
}

type Metadata struct {
    CreatedAt Timestamp `json:"CreatedAt"`
    UpdatedAt Timestamp `json:"UpdatedAt"`
    Network   int       `json:"Network"`
}

type Audit struct {
    ChangedAt Timestamp `json:"ChangedAt"`
}

type GetContentResponse struct {
    Content  ContentDetails `json:"Content"`
    MetaData Metadata       `json:"MetaData"`
    Audit    Audit          `json:"Audit"`
}

type ListContentResponse struct {
    Content  []ContentDetails `json:"Content"`
    MetaData Metadata         `json:"MetaData"`
    Audit    Audit            `json:"Audit"`
}

type Client struct {
    baseURL        string
    organizationID string
    network        string
    httpClient     *http.Client
}

func NewClient(baseURL, organizationID, network string) *Client {
    return &Client{
        baseURL:        baseURL,
        organizationID: organizationID,
        network:        network,
        httpClient:     &http.Client{Timeout: 30 * time.Second},
    }
}

func (c *Client) GetContent(contentID string) (*GetContentResponse, error) {
    endpoint := fmt.Sprintf("%s/api/minicms/get?content_id=%s", c.baseURL, url.QueryEscape(contentID))
    
    req, err := http.NewRequest("GET", endpoint, nil)
    if err != nil {
        return nil, err
    }
    
    req.Header.Set("OrganizationID", c.organizationID)
    req.Header.Set("Network", c.network)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode == http.StatusNotFound {
        return nil, nil
    }
    
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result GetContentResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return &result, nil
}

func (c *Client) ListContent(identifier string, limit, offset int) (*ListContentResponse, error) {
    params := url.Values{}
    params.Set("limit", fmt.Sprintf("%d", limit))
    params.Set("offset", fmt.Sprintf("%d", offset))
    if identifier != "" {
        params.Set("identifier", identifier)
    }
    
    endpoint := fmt.Sprintf("%s/api/minicms/list?%s", c.baseURL, params.Encode())
    
    req, err := http.NewRequest("GET", endpoint, nil)
    if err != nil {
        return nil, err
    }
    
    req.Header.Set("OrganizationID", c.organizationID)
    req.Header.Set("Network", c.network)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
    }
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result ListContentResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return &result, nil
}

func (c *Client) GetActiveByIdentifier(identifier, language string) (*ContentDetails, error) {
    result, err := c.ListContent(identifier, 100, 0)
    if err != nil {
        return nil, err
    }
    
    now := time.Now().Unix()
    
    for _, content := range result.Content {
        // Check status
        if !content.Status {
            continue
        }
        
        // Check time range
        if content.ActiveFrom != nil && content.ActiveFrom.Seconds > now {
            continue
        }
        if content.ActiveUntil != nil && content.ActiveUntil.Seconds < now {
            continue
        }
        
        // Check language
        if content.Language != nil && content.Language.Language == language {
            return &content, nil
        }
    }
    
    // Fallback to first active content without language match
    for _, content := range result.Content {
        if content.Status {
            if content.ActiveFrom == nil || content.ActiveFrom.Seconds <= now {
                if content.ActiveUntil == nil || content.ActiveUntil.Seconds >= now {
                    return &content, nil
                }
            }
        }
    }
    
    return nil, nil
}

// Usage example
func main() {
    client := NewClient(
        "https://api.sologenic.org",
        "215a551d-9284-4f72-ae9d-9284f40d1340",
        "mainnet",
    )
    
    // Get single content
    content, err := client.GetContent("1234-5678")
    if err != nil {
        panic(err)
    }
    if content != nil {
        fmt.Printf("Title: %s\n", content.Content.Title)
    }
    
    // List content by identifier
    banners, err := client.ListContent("homepage_banner", 10, 0)
    if err != nil {
        panic(err)
    }
    fmt.Printf("Found %d banners\n", len(banners.Content))
    
    // Get active by identifier and language
    active, err := client.GetActiveByIdentifier("hero_banner", "en-US")
    if err != nil {
        panic(err)
    }
    if active != nil {
        fmt.Printf("Active banner: %s\n", active.Title)
    }
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	com-be-http-lib
AUTH_FIREBASE_SERVICE	Firebase authentication service	com-fs-auth-firebase-service
ROLE_STORE	Role service endpoint	com-fs-role-model
ORGANIZATION_STORE	Organization service endpoint	com-fs-organization-model
Optional Environment Variables
Environment Variable	Description	Source
FEATURE_FLAG_STORE	Feature flag service endpoint	com-fs-feature-flag-model
Example Environment Configuration
bash
# Required
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
}
}'
AUTH_FIREBASE_SERVICE=auth-service:50070
ROLE_STORE=role-store:50066
ORGANIZATION_STORE=organization-service:50060

# Optional
FEATURE_FLAG_STORE=feature-flag-store:50055
LOG_LEVEL=info
CACHE_TTL_SECONDS=300
MAX_PAGE_SIZE=100
Docker Compose Example
yaml
version: '3.8'

services:
  minicms-service:
    image: sologenic/minicms-service:latest
    environment:
      - ORGANIZATION_STORE=organization-service:50060
      - AUTH_FIREBASE_SERVICE=auth-service:50070
      - ROLE_STORE=role-store:50066
      - FEATURE_FLAG_STORE=feature-flag-store:50055
      - LOG_LEVEL=info
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
    networks:
      - internal

  organization-service:
    image: sologenic/organization-service:latest
    networks:
      - internal

  auth-service:
    image: sologenic/auth-service:latest
    networks:
      - internal

  role-store:
    image: sologenic/role-store:latest
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Responses
Not Found (404) - Content Not Active
json
{
  "error": "Not Found",
  "message": "Content not found or inactive",
  "content_id": "1234-5678"
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Missing required parameter: content_id"
}
Bad Request (400) - Invalid Pagination
json
{
  "error": "Bad Request",
  "message": "Invalid pagination parameters",
  "details": {
    "limit": "must be between 1 and 100",
    "offset": "must be non-negative"
  }
}
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
  "message": "Access denied for organization",
  "organization_id": "215a551d-...-9284f40d1340"
}
Internal Server Error (500)
json
{
  "error": "Internal Server Error",
  "message": "Failed to retrieve content",
  "request_id": "req_12345"
}
Use Cases
Homepage Hero Banner
javascript
// Display time-sensitive promotional banner
const heroBanner = await client.getActiveByIdentifier('homepage_hero', 'en-US');
if (heroBanner) {
  // Banner is automatically filtered by ActiveFrom/ActiveUntil
  renderHeroBanner(heroBanner);
}
Multi-language Announcement Bar
javascript
// Show announcements in user's preferred language
const userLanguage = getUserLanguage(); // e.g., 'es-ES'
const announcement = await client.getActiveByIdentifier('announcement_top', userLanguage);
if (announcement) {
  renderAnnouncementBar(announcement);
}
Footer Links by Region
javascript
// Different footer content for different regions
const region = getUserRegion(); // 'US', 'EU', 'APAC'
const footerContent = await client.getContentByIdentifier(`footer_${region.toLowerCase()}`);
Scheduled Marketing Campaigns
javascript
// Content automatically appears/disappears based on schedule
const campaignContent = await client.getActiveByIdentifier('summer_sale_campaign');
// Active only during configured date range
Best Practices
Content Management
Practice	Recommendation
Identifier naming	Use consistent, descriptive identifiers (e.g., homepage_hero_banner)
Time ranges	Always set ActiveFrom/ActiveUntil for time-sensitive content
Status management	Use Status=false to temporarily disable content without deleting
Language fallback	Implement fallback logic when requested language unavailable
Caching	Implement client-side caching with ETags or Cache-Control headers
Performance
Practice	Recommendation
Batch requests	Use list endpoint with identifier to fetch related content
Pagination	Always use limit/offset for list endpoints
CDN caching	Cache content responses at CDN level for high-traffic pages
Image optimization	Use appropriate image formats and sizes for BackgroundImage
Security
Practice	Recommendation
Organization isolation	Always validate OrganizationID header
Input validation	Sanitize content_id and identifier parameters
HTML sanitization	Sanitize Content field if it contains user-generated HTML
Rate limiting	Implement per-organization rate limits
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Content not returned	Status = false	Enable content in CMS admin
Content not returned	Outside time range	Check ActiveFrom/ActiveUntil dates
Empty list response	Wrong identifier	Verify identifier spelling
Wrong language returned	Language not set	Set Language field in content
404 on get endpoint	Content ID wrong	Verify content_id value
Pagination not working	Invalid limit/offset	Use positive integers only
Debugging Commands
bash
# Test get endpoint
curl -X GET "https://api.sologenic.org/api/minicms/get?content_id=$CONTENT_ID" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v

# Test list endpoint with identifier
curl -X GET "https://api.sologenic.org/api/minicms/list?identifier=$IDENTIFIER&limit=5&offset=0" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v | jq '.Content[] | {id: .ContentID, title: .Title, active: .Status}'

# Check time activation
curl -X GET "https://api.sologenic.org/api/minicms/get?content_id=$CONTENT_ID" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v | jq '{active_from: .Content.ActiveFrom, active_until: .Content.ActiveUntil, now: now}'
Related Services
Service	Description
File Service	BackgroundImage file storage and retrieval
Organization Service	Tenant isolation and validation
Role Service	Access control for CMS admin endpoints
Auth Firebase Service	Authentication for admin operations
Feature Flag Store	Feature toggles for CMS functionality
License
This documentation is part of the TX Marketplace platform.
