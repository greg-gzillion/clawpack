# Reference Service (com-be-reference-service)

Generic reference tracking system for follows, likes, watches, votes, and visits across different subsystems.

## Overview

The Reference Service provides a unified system for tracking user interactions with various objects across the platform. It supports different action types and maintains relationships between users and references.

## Core Functionalities

| Action | Behavior | Description |
|--------|----------|-------------|
| Follow | Boolean (binary) | Follow a user or system (e.g., Market index) |
| Like | Boolean (binary) | Like a granular/low-level object (e.g., NFT, Token) |
| Visit | Permanent (last only) | Track page visits (only keeps most recent) |
| Watch | Boolean (binary) | Watch a group/high-level object (e.g., collection) |
| Vote | Boolean (binary) | Vote on an object (upvote/downvote on polls) |

### Key Behavioral Differences

**Boolean Actions (Follow/Like/Watch/Vote):**
- User either has a record or not
- Creation timestamp recorded on action
- Removal deletes the record entirely

**Visit Action:**
- Permanent tracking (never deleted)
- Only keeps the most recent visit
- Uses CreatedAt and UpdatedAt to track visit times

## API Endpoints Overview

### Unauthenticated Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/reference/list` | Returns list of references for account |
| GET | `/api/reference/count` | Returns count of references for account |
| GET | `/api/reference/alltime` | Returns all-time counts for references |
| GET | `/api/reference/votecount` | Returns vote counts (up/down) for references |
| GET | `/api/reference/getByKey` | Returns single reference by key |

### Authenticated Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/reference/add` | Add a reference |
| DELETE | `/api/reference/delete` | Delete a reference |
| POST | `/api/reference/vote` | Vote on an object |

## Reference Types (Enums)

Reference types are passed as integer values. Import the model and use constants.

| Type | Value | Description |
|------|-------|-------------|
| NFT_LIKE | 1 | Like an NFT |
| IDO_FOLLOW | 2 | Follow an IDO |
| NFT_WATCH | 3 | Watch an NFT collection |
| MARKET_INDEX_FOLLOW | 4 | Follow market index |
| POLL_VOTE | 5 | Vote on a poll |
| COLLECTION_WATCH | 6 | Watch a collection |
| TOKEN_LIKE | 7 | Like a token |
| USER_FOLLOW | 8 | Follow a user |
| COMMENT_LIKE | 9 | Like a comment |
| ARTICLE_VISIT | 10 | Visit an article |

## API Endpoints Details

### GET /api/reference/list

Returns list of references for a specific account.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| reference_type | int/string | Yes | Reference type enum value |
| account | string | Yes | XRP address or email |
| reference_keys | string | No | Base64-encoded JSON array (max 20) |
| before_reference_id | int | No | Pagination cursor |

**Reference Keys Format:**

```json
[
  "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008",
  "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000009"
]
Example Request (No Pagination):

bash
curl -H "Network: testnet" \
  "https://api.sologenic.org/api/reference/list?reference_type=3&account=rHfvKjmoHZtsgFzwa3xcuERnhN1GgXgSCp"
Example Request (With Pagination):

bash
curl -H "Network: testnet" \
  "https://api.sologenic.org/api/reference/list?reference_type=3&account=rHfvKjmoHZtsgFzwa3xcuERnhN1GgXgSCp&before_reference_id=150"
Example Request (With Reference Keys):

bash
# Encode reference keys array to base64
REF_KEYS=$(echo -n '[
  "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008",
  "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000009"
]' | base64 -w 0)

curl -H "Network: testnet" \
  "https://api.sologenic.org/api/reference/list?reference_type=3&account=rHfvKjmoHZtsgFzwa3xcuERnhN1GgXgSCp&reference_keys=${REF_KEYS}"
Success Response:

json
{
  "References": [
    {
      "Reference": {
        "ReferenceID": 1747426781762399450,
        "Account": "dev.sologenic@gmail.com",
        "ReferenceType": 1,
        "ReferenceKey": "11",
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
      },
      "MetaData": {
        "Network": 2,
        "UpdatedAt": {
          "seconds": 1747426781,
          "nanos": 762400271
        },
        "CreatedAt": {
          "seconds": 1747426781,
          "nanos": 633295001
        },
        "UpdatedByAccount": "dev.sologenic@gmail.com"
      },
      "Audit": {
        "ChangedBy": "dev.sologenic@gmail.com",
        "ChangedAt": {
          "seconds": 1747426781,
          "nanos": 762399961
        }
      }
    }
  ]
}
GET /api/reference/count
Returns the count of references for a specific account.

Query Parameters:

Parameter	Type	Required	Description
reference_type	int/string	Yes	Reference type enum value
account	string	Yes	XRP address or email
Example Request:

bash
curl -H "Network: testnet" \
  "https://api.sologenic.org/api/reference/count?reference_type=3&account=rHfvKjmoHZtsgFzwa3xcuERnhN1GgXgSCp"
Success Response:

json
5
GET /api/reference/alltime
Returns all-time counts for references. Provides real-time counts without updating Algolia.

Query Parameters:

Parameter	Type	Required	Description
reference_type	int/string	Yes	Reference type enum value
reference_keys	string	Yes	Base64-encoded JSON array (max 20)
Example Request:

bash
REF_KEYS=$(echo -n '[
  {"ReferenceKey": "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008", "ReferenceType": "nft_likes"}
]' | base64 -w 0)

curl -H "Network: testnet" \
  "https://api.sologenic.org/api/reference/alltime?reference_type=1&reference_keys=${REF_KEYS}"
Success Response:

json
{
  "Counts": [
    {
      "Count": 1,
      "ReferenceType": 1,
      "ReferenceKey": "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008",
      "Network": "mainnet"
    }
  ]
}
GET /api/reference/votecount
Returns vote counts (upvotes/downvotes) for references.

Query Parameters:

Parameter	Type	Required	Description
reference_type	int/string	Yes	Reference type enum value
reference_keys	string	Yes	Base64-encoded JSON array (max 20)
Example Request:

bash
REF_KEYS=$(echo -n '["1"]' | base64 -w 0)

curl -H "Network: testnet" \
  "https://api.sologenic.org/api/reference/votecount?reference_type=4&reference_keys=${REF_KEYS}"
Success Response:

json
{
  "UpVotes": [
    {
      "Count": 1,
      "ReferenceType": 9,
      "ReferenceKey": "1",
      "Network": "mainnet"
    }
  ],
  "DownVotes": []
}
GET /api/reference/getByKey
Returns a single reference record matching the provided reference key.

Query Parameters:

Parameter	Type	Required	Description
reference_key	string	Yes	Unique reference key (not base64 encoded)
Headers:

Network required (mainnet, testnet)

Authorization required (Bearer token)

Example Request:

bash
curl -H "Network: testnet" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  "https://api.sologenic.org/api/reference/getByKey?reference_key=00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008"
Success Response:

json
{
  "Reference": {
    "ReferenceID": 1747426781762399450,
    "Account": "dev.sologenic@gmail.com",
    "ReferenceType": 1,
    "ReferenceKey": "11",
    "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
  },
  "MetaData": {
    "Network": 2,
    "UpdatedAt": {
      "seconds": 1747426781,
      "nanos": 762400271
    },
    "CreatedAt": {
      "seconds": 1747426781,
      "nanos": 633295001
    },
    "UpdatedByAccount": "dev.sologenic@gmail.com"
  },
  "Audit": {
    "ChangedBy": "dev.sologenic@gmail.com",
    "ChangedAt": {
      "seconds": 1747426781,
      "nanos": 762399961
    }
  }
}
POST /api/reference/add
Adds a reference. Two types of references:

Key-Value Pair: NFT with NFT ID

System Level: e.g., ido_follow with ReferenceKey same as ReferenceType

Headers:

Authorization required (Bearer token)

Network required

Request Body (Key-Value Pair):

json
{
  "ReferenceKey": "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008",
  "ReferenceType": 3
}
Request Body (System Level):

json
{
  "ReferenceKey": "ido_follow",
  "ReferenceType": 2
}
Example Request:

bash
curl -X POST "https://api.sologenic.org/api/reference/add" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: testnet" \
  -d '{
    "ReferenceKey": "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008",
    "ReferenceType": 3
  }'
Success Response: HTTP 200 OK

DELETE /api/reference/delete
Deletes a reference or vote.

Headers:

Authorization required (Bearer token)

Network required

Request Body:

json
{
  "ReferenceKey": "23456",
  "ReferenceType": 3
}
Example Request:

bash
curl -X DELETE "https://api.sologenic.org/api/reference/delete" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: testnet" \
  -d '{
    "ReferenceKey": "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008",
    "ReferenceType": 3
  }'
Success Response: HTTP 200 OK

POST /api/reference/vote
Votes on an object (similar to add).

Headers:

Authorization required (Bearer token)

Network required

Request Body:

Field	Type	Required	Description
ReferenceKey	string	Yes	Reference identifier
ReferenceType	int	Yes	Reference type enum
VoteType	int	Yes	1=upvote, 2=downvote
Example Request:

bash
curl -X POST "https://api.sologenic.org/api/reference/vote" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "Network: testnet" \
  -d '{
    "ReferenceKey": "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008",
    "ReferenceType": 2,
    "VoteType": 1
  }'
Success Response: HTTP 200 OK

Error Responses
422 - ACCOUNT PARAM INVALID
json
{
  "errors": [
    {
      "name": "account.invalid"
    }
  ]
}
422 - REFERENCE_TYPE PARAM INVALID
json
{
  "errors": [
    {
      "name": "reference_type.invalid"
    }
  ]
}
422 - REFERENCE_KEY PARAM INVALID
json
{
  "errors": [
    {
      "name": "reference_key.invalid"
    }
  ]
}
Integration Examples
JavaScript/React Client
javascript
class ReferenceServiceClient {
  constructor(baseUrl, network = 'mainnet', token = null) {
    this.baseUrl = baseUrl;
    this.network = network;
    this.token = token;
  }

  setAuth(token) {
    this.token = token;
  }

  // Unauthenticated endpoints
  async listReferences(referenceType, account, options = {}) {
    const params = new URLSearchParams({
      reference_type: referenceType,
      account: account
    });
    
    if (options.referenceKeys) {
      const keysBase64 = btoa(JSON.stringify(options.referenceKeys));
      params.append('reference_keys', keysBase64);
    }
    
    if (options.beforeReferenceId) {
      params.append('before_reference_id', options.beforeReferenceId);
    }
    
    const response = await fetch(
      `${this.baseUrl}/api/reference/list?${params.toString()}`,
      { headers: this._getHeaders(false) }
    );
    return response.json();
  }

  async getCount(referenceType, account) {
    const response = await fetch(
      `${this.baseUrl}/api/reference/count?reference_type=${referenceType}&account=${account}`,
      { headers: this._getHeaders(false) }
    );
    return response.json();
  }

  async getAllTimeCounts(referenceType, referenceKeys) {
    const keysBase64 = btoa(JSON.stringify(referenceKeys));
    const response = await fetch(
      `${this.baseUrl}/api/reference/alltime?reference_type=${referenceType}&reference_keys=${keysBase64}`,
      { headers: this._getHeaders(false) }
    );
    return response.json();
  }

  async getVoteCounts(referenceType, referenceKeys) {
    const keysBase64 = btoa(JSON.stringify(referenceKeys));
    const response = await fetch(
      `${this.baseUrl}/api/reference/votecount?reference_type=${referenceType}&reference_keys=${keysBase64}`,
      { headers: this._getHeaders(false) }
    );
    return response.json();
  }

  async getByKey(referenceKey) {
    const response = await fetch(
      `${this.baseUrl}/api/reference/getByKey?reference_key=${referenceKey}`,
      { headers: this._getHeaders(true) }
    );
    return response.json();
  }

  // Authenticated endpoints
  async addReference(referenceKey, referenceType) {
    const response = await fetch(`${this.baseUrl}/api/reference/add`, {
      method: 'POST',
      headers: this._getHeaders(true),
      body: JSON.stringify({ ReferenceKey: referenceKey, ReferenceType: referenceType })
    });
    return response;
  }

  async deleteReference(referenceKey, referenceType) {
    const response = await fetch(`${this.baseUrl}/api/reference/delete`, {
      method: 'DELETE',
      headers: this._getHeaders(true),
      body: JSON.stringify({ ReferenceKey: referenceKey, ReferenceType: referenceType })
    });
    return response;
  }

  async vote(referenceKey, referenceType, voteType) {
    const response = await fetch(`${this.baseUrl}/api/reference/vote`, {
      method: 'POST',
      headers: this._getHeaders(true),
      body: JSON.stringify({ 
        ReferenceKey: referenceKey, 
        ReferenceType: referenceType,
        VoteType: voteType 
      })
    });
    return response;
  }

  // Convenience methods
  async likeNFT(nftId) {
    return this.addReference(nftId, 1); // NFT_LIKE = 1
  }

  async unlikeNFT(nftId) {
    return this.deleteReference(nftId, 1);
  }

  async followIDO(idoId) {
    return this.addReference(idoId, 2); // IDO_FOLLOW = 2
  }

  async unfollowIDO(idoId) {
    return this.deleteReference(idoId, 2);
  }

  async watchCollection(collectionId) {
    return this.addReference(collectionId, 6); // COLLECTION_WATCH = 6
  }

  async unwatchCollection(collectionId) {
    return this.deleteReference(collectionId, 6);
  }

  async upvote(referenceKey, referenceType) {
    return this.vote(referenceKey, referenceType, 1);
  }

  async downvote(referenceKey, referenceType) {
    return this.vote(referenceKey, referenceType, 2);
  }

  _getHeaders(requireAuth) {
    const headers = {
      'Content-Type': 'application/json',
      'Network': this.network
    };
    
    if (requireAuth && this.token) {
      headers['Authorization'] = `Bearer: ${this.token}`;
    }
    
    return headers;
  }
}

// React Component Example
function NFTLikeButton({ nftId, initialLikes = 0 }) {
  const [likes, setLikes] = useState(initialLikes);
  const [liked, setLiked] = useState(false);
  const [loading, setLoading] = useState(false);

  const client = new ReferenceServiceClient(
    'https://api.sologenic.org',
    'mainnet',
    localStorage.getItem('token')
  );

  useEffect(() => {
    checkIfLiked();
  }, [nftId]);

  async function checkIfLiked() {
    try {
      const result = await client.listReferences(1, localStorage.getItem('account'), {
        referenceKeys: [nftId]
      });
      setLiked(result.References && result.References.length > 0);
    } catch (error) {
      console.error('Failed to check like status:', error);
    }
  }

  async function toggleLike() {
    setLoading(true);
    try {
      if (liked) {
        await client.unlikeNFT(nftId);
        setLiked(false);
        setLikes(prev => prev - 1);
      } else {
        await client.likeNFT(nftId);
        setLiked(true);
        setLikes(prev => prev + 1);
      }
    } catch (error) {
      console.error('Failed to toggle like:', error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <button 
      onClick={toggleLike} 
      disabled={loading}
      className={`like-button ${liked ? 'liked' : ''}`}
    >
      {liked ? '❤️' : '🤍'} {likes}
    </button>
  );
}

function VoteComponent({ pollId, onVote }) {
  const [userVote, setUserVote] = useState(null);
  const [voteCounts, setVoteCounts] = useState({ upvotes: 0, downvotes: 0 });

  const client = new ReferenceServiceClient(
    'https://api.sologenic.org',
    'mainnet',
    localStorage.getItem('token')
  );

  useEffect(() => {
    loadVoteCounts();
    checkUserVote();
  }, [pollId]);

  async function loadVoteCounts() {
    try {
      const result = await client.getVoteCounts(5, [pollId]); // POLL_VOTE = 5
      setVoteCounts({
        upvotes: result.UpVotes?.[0]?.Count || 0,
        downvotes: result.DownVotes?.[0]?.Count || 0
      });
    } catch (error) {
      console.error('Failed to load vote counts:', error);
    }
  }

  async function checkUserVote() {
    try {
      const result = await client.listReferences(5, localStorage.getItem('account'), {
        referenceKeys: [pollId]
      });
      if (result.References && result.References.length > 0) {
        // Additional logic to determine vote type would be here
      }
    } catch (error) {
      console.error('Failed to check user vote:', error);
    }
  }

  async function handleVote(voteType) {
    try {
      await client.vote(pollId, 5, voteType);
      setUserVote(voteType);
      await loadVoteCounts();
      if (onVote) onVote(voteType);
    } catch (error) {
      console.error('Failed to vote:', error);
    }
  }

  return (
    <div className="vote-component">
      <button onClick={() => handleVote(1)} className="upvote">
        👍 {voteCounts.upvotes}
      </button>
      <button onClick={() => handleVote(2)} className="downvote">
        👎 {voteCounts.downvotes}
      </button>
    </div>
  );
}

export { ReferenceServiceClient, NFTLikeButton, VoteComponent };
Python Client
python
import requests
import base64
import json
from typing import Optional, Dict, Any, List
from enum import IntEnum

class ReferenceType(IntEnum):
    NFT_LIKE = 1
    IDO_FOLLOW = 2
    NFT_WATCH = 3
    MARKET_INDEX_FOLLOW = 4
    POLL_VOTE = 5
    COLLECTION_WATCH = 6
    TOKEN_LIKE = 7
    USER_FOLLOW = 8
    COMMENT_LIKE = 9
    ARTICLE_VISIT = 10

class VoteType(IntEnum):
    UPVOTE = 1
    DOWNVOTE = 2

class ReferenceServiceClient:
    def __init__(self, base_url: str, network: str = 'mainnet', token: Optional[str] = None):
        self.base_url = base_url
        self.network = network
        self.token = token
    
    def set_auth(self, token: str):
        """Set authentication token"""
        self.token = token
    
    # Unauthenticated endpoints
    def list_references(self, reference_type: int, account: str, 
                        reference_keys: Optional[List[str]] = None,
                        before_reference_id: Optional[int] = None) -> Dict[str, Any]:
        """List references for an account"""
        params = {
            'reference_type': reference_type,
            'account': account
        }
        
        if reference_keys:
            keys_json = json.dumps(reference_keys)
            params['reference_keys'] = base64.b64encode(keys_json.encode()).decode()
        
        if before_reference_id:
            params['before_reference_id'] = before_reference_id
        
        response = requests.get(
            f"{self.base_url}/api/reference/list",
            params=params,
            headers=self._get_headers(require_auth=False)
        )
        response.raise_for_status()
        return response.json()
    
    def get_count(self, reference_type: int, account: str) -> int:
        """Get count of references for an account"""
        response = requests.get(
            f"{self.base_url}/api/reference/count",
            params={'reference_type': reference_type, 'account': account},
            headers=self._get_headers(require_auth=False)
        )
        response.raise_for_status()
        return response.json()
    
    def get_alltime_counts(self, reference_type: int, reference_keys: List[str]) -> Dict:
        """Get all-time counts for references"""
        keys_json = json.dumps(reference_keys)
        keys_base64 = base64.b64encode(keys_json.encode()).decode()
        
        response = requests.get(
            f"{self.base_url}/api/reference/alltime",
            params={
                'reference_type': reference_type,
                'reference_keys': keys_base64
            },
            headers=self._get_headers(require_auth=False)
        )
        response.raise_for_status()
        return response.json()
    
    def get_vote_counts(self, reference_type: int, reference_keys: List[str]) -> Dict:
        """Get vote counts for references"""
        keys_json = json.dumps(reference_keys)
        keys_base64 = base64.b64encode(keys_json.encode()).decode()
        
        response = requests.get(
            f"{self.base_url}/api/reference/votecount",
            params={
                'reference_type': reference_type,
                'reference_keys': keys_base64
            },
            headers=self._get_headers(require_auth=False)
        )
        response.raise_for_status()
        return response.json()
    
    def get_by_key(self, reference_key: str) -> Dict:
        """Get reference by key"""
        response = requests.get(
            f"{self.base_url}/api/reference/getByKey",
            params={'reference_key': reference_key},
            headers=self._get_headers(require_auth=True)
        )
        response.raise_for_status()
        return response.json()
    
    # Authenticated endpoints
    def add_reference(self, reference_key: str, reference_type: int) -> None:
        """Add a reference"""
        response = requests.post(
            f"{self.base_url}/api/reference/add",
            headers=self._get_headers(require_auth=True),
            json={'ReferenceKey': reference_key, 'ReferenceType': reference_type}
        )
        response.raise_for_status()
    
    def delete_reference(self, reference_key: str, reference_type: int) -> None:
        """Delete a reference"""
        response = requests.delete(
            f"{self.base_url}/api/reference/delete",
            headers=self._get_headers(require_auth=True),
            json={'ReferenceKey': reference_key, 'ReferenceType': reference_type}
        )
        response.raise_for_status()
    
    def vote(self, reference_key: str, reference_type: int, vote_type: VoteType) -> None:
        """Vote on an object"""
        response = requests.post(
            f"{self.base_url}/api/reference/vote",
            headers=self._get_headers(require_auth=True),
            json={
                'ReferenceKey': reference_key,
                'ReferenceType': reference_type,
                'VoteType': int(vote_type)
            }
        )
        response.raise_for_status()
    
    # Convenience methods
    def like_nft(self, nft_id: str) -> None:
        """Like an NFT"""
        self.add_reference(nft_id, ReferenceType.NFT_LIKE)
    
    def unlike_nft(self, nft_id: str) -> None:
        """Unlike an NFT"""
        self.delete_reference(nft_id, ReferenceType.NFT_LIKE)
    
    def follow_ido(self, ido_id: str) -> None:
        """Follow an IDO"""
        self.add_reference(ido_id, ReferenceType.IDO_FOLLOW)
    
    def unfollow_ido(self, ido_id: str) -> None:
        """Unfollow an IDO"""
        self.delete_reference(ido_id, ReferenceType.IDO_FOLLOW)
    
    def watch_collection(self, collection_id: str) -> None:
        """Watch a collection"""
        self.add_reference(collection_id, ReferenceType.COLLECTION_WATCH)
    
    def unwatch_collection(self, collection_id: str) -> None:
        """Unwatch a collection"""
        self.delete_reference(collection_id, ReferenceType.COLLECTION_WATCH)
    
    def upvote(self, reference_key: str, reference_type: int) -> None:
        """Upvote an object"""
        self.vote(reference_key, reference_type, VoteType.UPVOTE)
    
    def downvote(self, reference_key: str, reference_type: int) -> None:
        """Downvote an object"""
        self.vote(reference_key, reference_type, VoteType.DOWNVOTE)
    
    def _get_headers(self, require_auth: bool = False) -> Dict[str, str]:
        headers = {
            'Content-Type': 'application/json',
            'Network': self.network
        }
        
        if require_auth and self.token:
            headers['Authorization'] = f'Bearer: {self.token}'
        
        return headers

# Usage Example
def main():
    client = ReferenceServiceClient(
        base_url='https://api.sologenic.org',
        network='mainnet',
        token='firebase-jwt-token'
    )
    
    account = 'rHfvKjmoHZtsgFzwa3xcuERnhN1GgXgSCp'
    nft_id = '00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008'
    
    # Get NFT like count
    counts = client.get_alltime_counts(ReferenceType.NFT_LIKE, [nft_id])
    print(f"NFT likes: {counts}")
    
    # Like an NFT
    client.like_nft(nft_id)
    print(f"Liked NFT: {nft_id}")
    
    # Get user's liked NFTs
    liked = client.list_references(ReferenceType.NFT_LIKE, account, reference_keys=[nft_id])
    print(f"User liked status: {liked}")
    
    # Unlike the NFT
    client.unlike_nft(nft_id)
    print(f"Unliked NFT: {nft_id}")

# Run example
# main()
Go Client
go
package main

import (
    "bytes"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "net/url"
    "strconv"
    "time"
)

type ReferenceType int

const (
    NFTLike            ReferenceType = 1
    IDOFollow          ReferenceType = 2
    NFTWatch           ReferenceType = 3
    MarketIndexFollow  ReferenceType = 4
    PollVote           ReferenceType = 5
    CollectionWatch    ReferenceType = 6
    TokenLike          ReferenceType = 7
    UserFollow         ReferenceType = 8
    CommentLike        ReferenceType = 9
    ArticleVisit       ReferenceType = 10
)

type VoteType int

const (
    UpVote   VoteType = 1
    DownVote VoteType = 2
)

type ReferenceServiceClient struct {
    baseURL string
    network string
    token   string
    client  *http.Client
}

type Reference struct {
    ReferenceID    int64  `json:"ReferenceID"`
    Account        string `json:"Account"`
    ReferenceType  int    `json:"ReferenceType"`
    ReferenceKey   string `json:"ReferenceKey"`
    OrganizationID string `json:"OrganizationID"`
}

type Metadata struct {
    Network          int       `json:"Network"`
    UpdatedAt        Timestamp `json:"UpdatedAt"`
    CreatedAt        Timestamp `json:"CreatedAt"`
    UpdatedByAccount string    `json:"UpdatedByAccount"`
}

type Timestamp struct {
    Seconds int64 `json:"seconds"`
    Nanos   int32 `json:"nanos"`
}

type Audit struct {
    ChangedBy string    `json:"ChangedBy"`
    ChangedAt Timestamp `json:"ChangedAt"`
}

type ReferenceResponse struct {
    Reference Reference `json:"Reference"`
    MetaData  Metadata  `json:"MetaData"`
    Audit     Audit     `json:"Audit"`
}

type ListReferencesResponse struct {
    References []ReferenceResponse `json:"References"`
}

func NewReferenceServiceClient(baseURL, network, token string) *ReferenceServiceClient {
    return &ReferenceServiceClient{
        baseURL: baseURL,
        network: network,
        token:   token,
        client:  &http.Client{Timeout: 30 * time.Second},
    }
}

// Unauthenticated endpoints
func (c *ReferenceServiceClient) ListReferences(referenceType ReferenceType, account string, referenceKeys []string, beforeReferenceID *int64) (*ListReferencesResponse, error) {
    params := url.Values{}
    params.Add("reference_type", strconv.Itoa(int(referenceType)))
    params.Add("account", account)
    
    if len(referenceKeys) > 0 {
        keysJSON, err := json.Marshal(referenceKeys)
        if err != nil {
            return nil, err
        }
        keysBase64 := base64.URLEncoding.EncodeToString(keysJSON)
        params.Add("reference_keys", keysBase64)
    }
    
    if beforeReferenceID != nil {
        params.Add("before_reference_id", strconv.FormatInt(*beforeReferenceID, 10))
    }
    
    reqURL := fmt.Sprintf("%s/api/reference/list?%s", c.baseURL, params.Encode())
    
    req, err := http.NewRequest("GET", reqURL, nil)
    if err != nil {
        return nil, err
    }
    
    c.setHeaders(req, false)
    
    resp, err := c.client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result ListReferencesResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return &result, nil
}

func (c *ReferenceServiceClient) GetCount(referenceType ReferenceType, account string) (int, error) {
    reqURL := fmt.Sprintf("%s/api/reference/count?reference_type=%d&account=%s", 
        c.baseURL, referenceType, account)
    
    req, err := http.NewRequest("GET", reqURL, nil)
    if err != nil {
        return 0, err
    }
    
    c.setHeaders(req, false)
    
    resp, err := c.client.Do(req)
    if err != nil {
        return 0, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return 0, err
    }
    
    var count int
    if err := json.Unmarshal(body, &count); err != nil {
return 0, err
    }
    
    return count, nil
}

func (c *ReferenceServiceClient) GetAllTimeCounts(referenceType ReferenceType, referenceKeys []string) (map[string]interface{}, error) {
    keysJSON, err := json.Marshal(referenceKeys)
    if err != nil {
        return nil, err
    }
    keysBase64 := base64.URLEncoding.EncodeToString(keysJSON)
    
    reqURL := fmt.Sprintf("%s/api/reference/alltime?reference_type=%d&reference_keys=%s", 
        c.baseURL, referenceType, keysBase64)
    
    req, err := http.NewRequest("GET", reqURL, nil)
    if err != nil {
        return nil, err
    }
    
    c.setHeaders(req, false)
    
    resp, err := c.client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return result, nil
}

func (c *ReferenceServiceClient) GetVoteCounts(referenceType ReferenceType, referenceKeys []string) (map[string]interface{}, error) {
    keysJSON, err := json.Marshal(referenceKeys)
    if err != nil {
        return nil, err
    }
    keysBase64 := base64.URLEncoding.EncodeToString(keysJSON)
    
    reqURL := fmt.Sprintf("%s/api/reference/votecount?reference_type=%d&reference_keys=%s", 
        c.baseURL, referenceType, keysBase64)
    
    req, err := http.NewRequest("GET", reqURL, nil)
    if err != nil {
        return nil, err
    }
    
    c.setHeaders(req, false)
    
    resp, err := c.client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return result, nil
}

func (c *ReferenceServiceClient) GetByKey(referenceKey string) (*ReferenceResponse, error) {
    reqURL := fmt.Sprintf("%s/api/reference/getByKey?reference_key=%s", c.baseURL, referenceKey)
    
    req, err := http.NewRequest("GET", reqURL, nil)
    if err != nil {
        return nil, err
    }
    
    c.setHeaders(req, true)
    
    resp, err := c.client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var result ReferenceResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return &result, nil
}

// Authenticated endpoints
func (c *ReferenceServiceClient) AddReference(referenceKey string, referenceType ReferenceType) error {
    payload := map[string]interface{}{
        "ReferenceKey":  referenceKey,
        "ReferenceType": int(referenceType),
    }
    
    jsonPayload, err := json.Marshal(payload)
    if err != nil {
        return err
    }
    
    req, err := http.NewRequest("POST", fmt.Sprintf("%s/api/reference/add", c.baseURL), bytes.NewBuffer(jsonPayload))
    if err != nil {
        return err
    }
    
    c.setHeaders(req, true)
    
    resp, err := c.client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("failed to add reference: status %d", resp.StatusCode)
    }
    
    return nil
}

func (c *ReferenceServiceClient) DeleteReference(referenceKey string, referenceType ReferenceType) error {
    payload := map[string]interface{}{
        "ReferenceKey":  referenceKey,
        "ReferenceType": int(referenceType),
    }
    
    jsonPayload, err := json.Marshal(payload)
    if err != nil {
        return err
    }
    
    req, err := http.NewRequest("DELETE", fmt.Sprintf("%s/api/reference/delete", c.baseURL), bytes.NewBuffer(jsonPayload))
    if err != nil {
        return err
    }
    
    c.setHeaders(req, true)
    
    resp, err := c.client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("failed to delete reference: status %d", resp.StatusCode)
    }
    
    return nil
}

func (c *ReferenceServiceClient) Vote(referenceKey string, referenceType ReferenceType, voteType VoteType) error {
    payload := map[string]interface{}{
        "ReferenceKey":  referenceKey,
        "ReferenceType": int(referenceType),
        "VoteType":      int(voteType),
    }
    
    jsonPayload, err := json.Marshal(payload)
    if err != nil {
        return err
    }
    
    req, err := http.NewRequest("POST", fmt.Sprintf("%s/api/reference/vote", c.baseURL), bytes.NewBuffer(jsonPayload))
    if err != nil {
        return err
    }
    
    c.setHeaders(req, true)
    
    resp, err := c.client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return fmt.Errorf("failed to vote: status %d", resp.StatusCode)
    }
    
    return nil
}

// Convenience methods
func (c *ReferenceServiceClient) LikeNFT(nftID string) error {
    return c.AddReference(nftID, NFTLike)
}

func (c *ReferenceServiceClient) UnlikeNFT(nftID string) error {
    return c.DeleteReference(nftID, NFTLike)
}

func (c *ReferenceServiceClient) FollowIDO(idoID string) error {
    return c.AddReference(idoID, IDOFollow)
}

func (c *ReferenceServiceClient) UnfollowIDO(idoID string) error {
    return c.DeleteReference(idoID, IDOFollow)
}

func (c *ReferenceServiceClient) WatchCollection(collectionID string) error {
    return c.AddReference(collectionID, CollectionWatch)
}

func (c *ReferenceServiceClient) UnwatchCollection(collectionID string) error {
    return c.DeleteReference(collectionID, CollectionWatch)
}

func (c *ReferenceServiceClient) UpVote(referenceKey string, referenceType ReferenceType) error {
    return c.Vote(referenceKey, referenceType, UpVote)
}

func (c *ReferenceServiceClient) DownVote(referenceKey string, referenceType ReferenceType) error {
    return c.Vote(referenceKey, referenceType, DownVote)
}

func (c *ReferenceServiceClient) setHeaders(req *http.Request, requireAuth bool) {
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Network", c.network)
    
    if requireAuth && c.token != "" {
        req.Header.Set("Authorization", fmt.Sprintf("Bearer: %s", c.token))
    }
}

// Example usage
func main() {
    client := NewReferenceServiceClient("https://api.sologenic.org", "mainnet", "your-firebase-token")
    
    // Like an NFT
    err := client.LikeNFT("00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008")
    if err != nil {
        fmt.Printf("Error liking NFT: %v\n", err)
    }
    
    // Get all-time counts
    counts, err := client.GetAllTimeCounts(NFTLike, []string{
        "00082EE0A19D0322C71F859F8C7A7D8584D234E97DB949C3B72E91A300000008",
    })
    if err != nil {
        fmt.Printf("Error getting counts: %v\n", err)
    }
    fmt.Printf("Counts: %v\n", counts)
}
Environment Variables
Variable	Required	Description
ORGANIZATION_STORE	Yes	Organization store endpoint
REFERENCE_STORE_ENDPOINT	Yes	Reference store endpoint
AUTH_SERVICE_ENDPOINT	Yes	Auth service endpoint
HTTP_CONFIG	Yes	HTTP server configuration
ACCOUNT_STORE	Yes	Account store endpoint
LOG_LEVEL	No	Logging level (default: info)
Docker Compose Example
yaml
version: '3.8'

services:
  reference-service:
    image: sologenic/com-be-reference-service:latest
    environment:
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
      - ORGANIZATION_STORE=organization-store:50062
      - REFERENCE_STORE_ENDPOINT=reference-store:50070
      - AUTH_SERVICE_ENDPOINT=auth-service:50075
      - ACCOUNT_STORE=account-store:50045
      - LOG_LEVEL=info
    ports:
      - "8080:8080"
    networks:
      - internal
    depends_on:
      - reference-store
      - organization-store
      - auth-service
      - account-store

  reference-store:
    image: sologenic/com-fs-reference-store:latest
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=references
      - DB_USER=reference_user
      - DB_PASSWORD=${DB_PASSWORD}
    networks:
      - internal

  organization-store:
    image: sologenic/com-fs-organization-store:latest
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=organizations
    networks:
      - internal

  auth-service:
    image: sologenic/com-fs-auth-service:latest
    environment:
      - FIREBASE_PROJECT_ID=${FIREBASE_PROJECT_ID}
    networks:
      - internal

networks:
  internal:
    driver: bridge
Best Practices
Performance
Cache reference counts with 30-second TTL

Batch reference key queries (max 20 per request)

Use pagination for large result sets

Implement connection pooling for database

Accuracy
Validate reference keys before processing

Handle duplicate keys gracefully

Ensure proper timestamp precision

Maintain referential integrity

Security
Always validate authentication tokens

Use OrganizationID for data isolation

Implement rate limiting by account

Never expose internal reference IDs

Troubleshooting
Issue	Possible Cause	Solution
References not found	Invalid reference key	Verify reference key format
Authentication failed	Expired or invalid token	Refresh Firebase token
Count mismatch	Duplicate references	Check for duplicate entries
Pagination issues	Invalid reference_id	Use valid reference_id cursor
Network errors	Wrong network header	Verify Network header value
License
This documentation is part of the TX Marketplace platform.






















