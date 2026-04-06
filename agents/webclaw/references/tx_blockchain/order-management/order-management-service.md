# Order Management Service

The Order Management Service provides RESTful interfaces for creating and submitting trading orders on the blockchain.

## Prerequisites for Trading

Before a user can place an order, two prerequisites are automatically satisfied:

### 1. Asset Issuance (Lazy Issuance)
- **Purpose:** Ensure asset exists on smart contract
- **Check:** `IsIssuedInSmartContract` flag
- **Action:** If false, automatically issue via `IssueAsset` function
- **Cost:** 10 COREUM (AssetIssuanceFund)

### 2. User Whitelisting (Lazy Whitelisting)
- **Purpose:** Authorize user's wallet to trade the asset
- **Check:** Query `UserAssetList` for user/asset combination
- **Action:** If no record, set max hold limit and create `WHITELISTED` record

## Happy Path Workflow
Step 1: User places order via POST /order/create-tx
↓
Step 2: Asset Issuance Check (Lazy)
├─ Check: IsIssuedInSmartContract
├─ If FALSE → Issue asset (10 COREUM)
└─ If TRUE → Continue
↓
Step 3: User Whitelisting Check (Lazy)
├─ Query UserAssetList
├─ If NO RECORD → Whitelist user
├─ If WHITELISTED → Continue
└─ If OTHER STATUS → Block trading
↓
Step 4: Order Processing
├─ Validate notional limits
├─ Check available funds
├─ Create smart contract message
└─ Return unsigned transaction
↓
Step 5: User signs transaction (offline)
↓
Step 6: Submit signed tx via POST /order/submit-tx
↓
Step 7: Broadcast to blockchain
↓
Step 8: Order created on-chain

text

## API Endpoints

### POST /api/ordermgt/order/create-tx

Creates an unsigned transaction for buy/sell/cancel orders.

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer Firebase JWT token |
| OrganizationID | Yes | Organization UUID |
| Network | Yes | mainnet, testnet, devnet |
| Content-Type | Yes | application/json |

**Request Body:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| order_type | string | Yes | "purchase", "sale", or "cancel" |
| denom | string | Yes | Asset denomination |
| amount | string | Yes | Order amount |
| amount_exp | string | Yes | Amount exponent (10^exp) |
| instruction | object | Yes | Limit price and options |
| hold | object | Yes | Fund hold details |
| order_id | string | For cancel | Order ID to cancel |

**Example Request - Purchase:**
```bash
curl -X POST "https://api.sologenic.org/api/ordermgt/order/create-tx" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: sologenic" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "order_type": "purchase",
    "denom": "suamzn_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
    "amount": "1",
    "amount_exp": "0",
    "instruction": {
        "limit_price": "250",
        "limit_price_exp": "0",
        "options": {
            "order_type": "limit",
            "fill_or_kill": false,
            "expires_at": "2024-11-29T23:59:59Z"
        }
    },
    "hold": {
        "denom": "utestcore",
        "amount": "1000",
        "amount_exp": "1"
    }
}'
Example Response:

json
{
  "msg_hash": "a1b2c3d4e5f6789012345678901234567890abcdef",
  "tx_to_sign": {
    "sender": "testcore1hphhtkzz0tmxqwvn74gm8d3r9770a0gc50fcgc",
    "contract": "testcore1et29cek95pl0zralsf43u4uply0g9nmxnj7fyt9yfy74spch7fpq3f8j0e",
    "msg": "base64EncodedMessage",
    "funds": [{"denom": "utestcore", "amount": "10000"}]
  }
}
Example Request - Sale:

bash
curl -X POST "https://api.sologenic.org/api/ordermgt/order/create-tx" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: sologenic" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "order_type": "sale",
    "denom": "suamzn_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
    "amount": "5",
    "amount_exp": "0",
    "instruction": {
        "limit_price": "260",
        "limit_price_exp": "0",
        "options": {"order_type": "limit", "fill_or_kill": false}
    },
    "hold": {
        "denom": "suamzn_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
        "amount": "5",
        "amount_exp": "0"
    }
}'
Example Request - Cancel:

bash
curl -X POST "https://api.sologenic.org/api/ordermgt/order/create-tx" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: sologenic" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "order_type": "cancel",
    "denom": "suamzn_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
    "order_id": "12345",
    "amount": "0",
    "amount_exp": "0",
    "instruction": {"options": {}},
    "hold": {"denom": "utestcore", "amount": "0", "amount_exp": "0"}
}'
POST /api/ordermgt/order/submit-tx
Submits a signed transaction to the blockchain.

Headers: Same as create-tx endpoint

Request Body:

Field	Type	Required	Description
TX	string	Yes	Base64-encoded signed transaction
Example Request:

bash
curl -X POST "https://api.sologenic.org/api/ordermgt/order/submit-tx" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"TX": "base64EncodedSignedTransaction"}'
Example Response:

json
{
  "tx_hash": "7FFE0685ACDFB25D298E596F4C4812D89649B802CA103F95054FD5F0C092211D",
  "order_details": {
    "id": 211,
    "creator": "testcore1hphhtkzz0tmxqwvn74gm8d3r9770a0gc50fcgc",
    "denom": "mstr_v1-testcore1et29cek95pl0zralsf43u4uply0g9nmxnj7fyt9yfy74spch7fpq3f8j0e",
    "amount": "1",
    "amount_exp": "0",
    "order_type": "purchase",
    "order_state": "open",
    "funds_sent": {"denom": "utestcore", "amount": "10000"}
  }
}
Data Models
Order Types
Type	Description
purchase	Buy order
sale	Sell order
cancel	Cancel existing order
Order States
State	Description
open	Active, waiting to be filled
filled	Completely filled
partially_filled	Partially filled
cancelled	Cancelled by user
expired	Expired without being filled
failed	Processing failed
Order Instruction Options
Field	Type	Required	Description
order_type	string	Yes	"limit" or "market"
fill_or_kill	bool	No	Execute fully or not at all (default: false)
expires_at	string	No	ISO 8601 expiry timestamp
Environment Variables
Variable	Description	Example
ACCOUNT_STORE	Account store service	localhost:50051
USER_STORE	User store service	localhost:50049
ROLE_STORE	Role store service	localhost:50066
ASSET_STORE	Asset store service	localhost:50056
OPEN_SEARCH_STORE	OpenSearch store	localhost:50057
WALLET_MIDDLEWARE	Wallet middleware	localhost:50088
ORGANIZATION_STORE	Organization store	localhost:50062
AUTH_FIREBASE_SERVICE	Firebase auth	localhost:50075
SMART_CONTRACT_ADDRESS	Smart contract address	core1...
SMART_CONTRACT_ISSUER_ADDRESS	Issuer address	core1...
WUSDC_DENOM	WUSDC denomination	wusdc
COREUM_DENOM	Coreum denomination	utestcore
HASHING_SALT	Salt for message hashing	your-salt-here
LOG_LEVEL	Log level	info/debug/error
Integration Examples
JavaScript/React Client
javascript
class OrderManagementClient {
  constructor(baseUrl, token, organizationId, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.token = token;
    this.organizationId = organizationId;
    this.network = network;
  }

  async createOrder(orderData) {
    const response = await fetch(`${this.baseUrl}/api/ordermgt/order/create-tx`, {
      method: 'POST',
      headers: this._getHeaders(),
      body: JSON.stringify(orderData)
    });
    if (!response.ok) throw new Error('Failed to create order');
    return response.json();
  }

  async submitTransaction(signedTx) {
    const response = await fetch(`${this.baseUrl}/api/ordermgt/order/submit-tx`, {
      method: 'POST',
      headers: this._getHeaders(),
      body: JSON.stringify({ TX: signedTx })
    });
    if (!response.ok) throw new Error('Failed to submit transaction');
    return response.json();
  }

  async createPurchaseOrder(denom, amount, limitPrice, holdDenom, holdAmount) {
    return this.createOrder({
      order_type: 'purchase',
      denom,
      amount: amount.toString(),
      amount_exp: '0',
      instruction: {
        limit_price: limitPrice.toString(),
        limit_price_exp: '0',
        options: { order_type: 'limit', fill_or_kill: false }
      },
      hold: { denom: holdDenom, amount: holdAmount.toString(), amount_exp: '0' }
    });
  }

  async createSaleOrder(denom, amount, limitPrice) {
    return this.createOrder({
      order_type: 'sale',
      denom,
      amount: amount.toString(),
      amount_exp: '0',
      instruction: {
        limit_price: limitPrice.toString(),
        limit_price_exp: '0',
        options: { order_type: 'limit', fill_or_kill: false }
      },
      hold: { denom, amount: amount.toString(), amount_exp: '0' }
    });
  }

  async cancelOrder(denom, orderId) {
    return this.createOrder({
      order_type: 'cancel',
      denom,
      order_id: orderId,
      amount: '0',
      amount_exp: '0',
      instruction: { options: {} },
      hold: { denom: 'utestcore', amount: '0', amount_exp: '0' }
    });
  }

  _getHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.token}`,
      'OrganizationID': this.organizationId,
      'Network': this.network
    };
  }
}

// Usage
const client = new OrderManagementClient(
  'https://api.sologenic.org',
  'your-firebase-jwt',
  'your-org-id',
  'mainnet'
);

const order = await client.createPurchaseOrder('asset-denom', '10', '250', 'wusdc', '2500');
console.log('Order created:', order);
Python Client
python
import requests
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum

class OrderType(str, Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    CANCEL = "cancel"

class OrderManagementClient:
    def __init__(self, base_url: str, token: str, organization_id: str, network: str = 'mainnet'):
        self.base_url = base_url
        self.token = token
        self.organization_id = organization_id
        self.network = network
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an order transaction"""
        response = requests.post(
            f"{self.base_url}/api/ordermgt/order/create-tx",
            headers=self._get_headers(),
            json=order_data
        )
        response.raise_for_status()
        return response.json()
    
    def submit_transaction(self, signed_tx: str) -> Dict[str, Any]:
        """Submit a signed transaction"""
        response = requests.post(
            f"{self.base_url}/api/ordermgt/order/submit-tx",
            headers=self._get_headers(),
            json={"TX": signed_tx}
        )
        response.raise_for_status()
        return response.json()
    
    def purchase(self, denom: str, amount: str, limit_price: str, hold_denom: str, hold_amount: str) -> Dict:
        return self.create_order({
            "order_type": "purchase",
            "denom": denom,
            "amount": amount,
            "amount_exp": "0",
            "instruction": {
                "limit_price": limit_price,
                "limit_price_exp": "0",
                "options": {"order_type": "limit", "fill_or_kill": False}
            },
            "hold": {"denom": hold_denom, "amount": hold_amount, "amount_exp": "0"}
        })
    
    def sell(self, denom: str, amount: str, limit_price: str) -> Dict:
        return self.create_order({
            "order_type": "sale",
            "denom": denom,
            "amount": amount,
            "amount_exp": "0",
            "instruction": {
                "limit_price": limit_price,
                "limit_price_exp": "0",
                "options": {"order_type": "limit", "fill_or_kill": False}
            },
            "hold": {"denom": denom, "amount": amount, "amount_exp": "0"}
        })
    
    def cancel(self, denom: str, order_id: str) -> Dict:
        return self.create_order({
            "order_type": "cancel",
            "denom": denom,
            "order_id": order_id,
            "amount": "0",
            "amount_exp": "0",
            "instruction": {"options": {}},
            "hold": {"denom": "utestcore", "amount": "0", "amount_exp": "0"}
        })
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'OrganizationID': self.organization_id,
            'Network': self.network
        }

# Usage
client = OrderManagementClient(
    base_url='https://api.sologenic.org',
    token='your-firebase-jwt',
    organization_id='your-org-id',
    network='mainnet'
)

# Create purchase order
order = client.purchase('asset-denom', '10', '250', 'wusdc', '2500')
print(f"Order created: {order['msg_hash']}")

# Submit signed transaction
result = client.submit_transaction('base64-signed-tx')
print(f"Transaction hash: {result['tx_hash']}")
Go Client
go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"
)

type OrderManagementClient struct {
    baseURL        string
    token          string
    organizationID string
    network        string
    httpClient     *http.Client
}

func NewOrderManagementClient(baseURL, token, organizationID, network string) *OrderManagementClient {
    return &OrderManagementClient{
        baseURL:        baseURL,
        token:          token,
        organizationID: organizationID,
        network:        network,
        httpClient:     &http.Client{Timeout: 30 * time.Second},
    }
}

type OrderRequest struct {
    OrderType  string                 `json:"order_type"`
    Denom      string                 `json:"denom"`
    Amount     string                 `json:"amount"`
    AmountExp  string                 `json:"amount_exp"`
    Instruction map[string]interface{} `json:"instruction"`
    Hold       map[string]interface{} `json:"hold"`
    OrderID    string                 `json:"order_id,omitempty"`
}

type OrderResponse struct {
    MsgHash   string                 `json:"msg_hash"`
    TxToSign  map[string]interface{} `json:"tx_to_sign"`
}

type SubmitResponse struct {
    TxHash       string                 `json:"tx_hash"`
    OrderDetails map[string]interface{} `json:"order_details"`
}

func (c *OrderManagementClient) CreateOrder(orderReq *OrderRequest) (*OrderResponse, error) {
    jsonData, err := json.Marshal(orderReq)
    if err != nil {
        return nil, err
    }

    req, err := http.NewRequest("POST", c.baseURL+"/api/ordermgt/order/create-tx", bytes.NewBuffer(jsonData))
    if err != nil {
        return nil, err
    }

    c.setHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    var result OrderResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }

    return &result, nil
}

func (c *OrderManagementClient) SubmitTransaction(signedTx string) (*SubmitResponse, error) {
    reqBody := map[string]string{"TX": signedTx}
    jsonData, err := json.Marshal(reqBody)
    if err != nil {
        return nil, err
    }

    req, err := http.NewRequest("POST", c.baseURL+"/api/ordermgt/order/submit-tx", bytes.NewBuffer(jsonData))
    if err != nil {
        return nil, err
    }

    c.setHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    var result SubmitResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }

    return &result, nil
}

func (c *OrderManagementClient) Purchase(denom, amount, limitPrice, holdDenom, holdAmount string) (*OrderResponse, error) {
    return c.CreateOrder(&OrderRequest{
        OrderType: "purchase",
        Denom:     denom,
        Amount:    amount,
        AmountExp: "0",
        Instruction: map[string]interface{}{
            "limit_price":     limitPrice,
            "limit_price_exp": "0",
            "options": map[string]interface{}{
                "order_type":   "limit",
                "fill_or_kill": false,
            },
        },
        Hold: map[string]interface{}{
            "denom":      holdDenom,
            "amount":     holdAmount,
            "amount_exp": "0",
        },
    })
}

func (c *OrderManagementClient) setHeaders(req *http.Request) {
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer "+c.token)
    req.Header.Set("OrganizationID", c.organizationID)
    req.Header.Set("Network", c.network)
}

// Usage
func main() {
    client := NewOrderManagementClient(
        "https://api.sologenic.org",
        "your-firebase-jwt",
        "your-org-id",
        "mainnet",
    )

    order, err := client.Purchase("asset-denom", "10", "250", "wusdc", "2500")
    if err != nil {
        panic(err)
    }
    fmt.Printf("Order created: %s\n", order.MsgHash)
}
Error Responses
Status	Code	Description
400	Bad Request	Invalid request format or missing fields
401	Unauthorized	Missing or invalid authentication token
403	Forbidden	User not authorized for this operation
404	Not Found	Endpoint or resource not found
409	Conflict	Order already exists or state conflict
500	Internal Error	Server-side error
Docker Compose Example
yaml
version: '3.8'

services:
  order-management-service:
    image: sologenic/order-management-service:latest
    environment:
      - ACCOUNT_STORE=account-store:50051
      - USER_STORE=user-store:50049
      - ROLE_STORE=role-store:50066
      - ASSET_STORE=asset-store:50056
      - OPEN_SEARCH_STORE=open-search-store:50057
      - WALLET_MIDDLEWARE=wallet-middleware:50088
      - ORGANIZATION_STORE=organization-store:50062
      - AUTH_FIREBASE_SERVICE=auth-service:50075
      - SMART_CONTRACT_ADDRESS=core1...
      - LOG_LEVEL=info
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
Troubleshooting
Issue	Solution
"Asset not issued"	Service auto-issues, ensure 10 COREUM available
"User not whitelisted"	Auto-whitelisting occurs on first trade
"Insufficient funds"	Check hold amount vs available balance
"Order creation fails"	Verify denom format and network
"Transaction invalid"	Ensure proper signing before submission
This documentation covers the complete Order Management Service API.





