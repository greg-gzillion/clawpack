# Open Search Service

The Open Search Service provides API interfaces for interacting with the Elasticsearch/OpenSearch system, enabling powerful search capabilities across assets, orders, and trades.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Open Search Service Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ REST API Endpoints │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ /assets │ /orders │ /trades │ /tx/assets │ │
│ │ (Asset │ (Order │ (Trade │ (Transaction Asset │ │
│ │ Search) │ Search) │ Search) │ Search) │ │
│ │ │ │ │ │ │
│ │ │ /rawquery │ │ │ │
│ │ │ (Raw ES │ │ │ │
│ │ │ Query) │ │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Query Processing Engine │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Base64 query decoding │ │
│ │ • AND/OR logic parsing │ │
│ │ • Field mapping and validation │ │
│ │ • Security filtering (UserID, OrganizationID) │ │
│ │ • Pagination (page, limit) │ │
│ │ • Sorting (order_by, dir) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Data Sources │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ OpenSearch │ User Store │ Role Store │ Organization Store │ │
│ │ Store │ │ │ │ │
│ │ Feature Flag │ Auth Firebase │ HTTP Config │ │ │
│ │ Store │ Service │ │ │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Query Structure

### Query Object Definition

```protobuf
message Query {
    string Field = 1;           // Field name to search on
    string Value = 2;           // Value to match
    Operator Operator = 3;      // Comparison operator
    FieldType FieldType = 4;    // Type of field
    repeated Query Query = 5;   // Nested queries (for OR logic)
}
Query Operators
Operator	Description	Use Case
EQUALS	Exact match	Status = 3
CONTAINS	Substring match	Name contains "BTC"
STARTS_WITH	Prefix match	Denom starts with "su"
ENDS_WITH	Suffix match	Email ends with "@sologenic.org"
GREATER_THAN	> comparison	Amount > 1000
LESS_THAN	< comparison	Price < 50000
GREATER_THAN_EQUALS	>= comparison	CreatedAt >= timestamp
LESS_THAN_EQUALS	<= comparison	UpdatedAt <= timestamp
Field Types
FieldType	Description	Example
STRING	Text field	"Asset Name"
NUMBER	Numeric field	12345
DATE	Timestamp field	2024-01-01T00:00:00Z
BOOLEAN	True/false	true
KEYWORD	Exact match keyword	"ACTIVE"
Query Logic
AND Logic
Multiple query conditions in a single array - ALL conditions must be satisfied:

json
{
    "Query": [
        { "Field": "AssetDetails.OrganizationID", "Value": "org-123" },
        { "Field": "AssetDetails.Status", "Value": "3" },
        { "Field": "AssetDetails.Type", "Value": "1" }
    ]
}
Result: Assets where OrganizationID = "org-123" AND Status = 3 AND Type = 1

OR Logic
Nested query conditions within a parent query - ANY nested condition can be satisfied:

json
{
    "Query": [
        {
            "Field": "AssetDetails.OrganizationID",
            "Value": "org-123",
            "Query": [
                { "Field": "AssetDetails.Status", "Value": "3" },
                { "Field": "AssetDetails.Type", "Value": "1" }
            ]
        }
    ]
}
Result: Assets where OrganizationID = "org-123" AND (Status = 3 OR Type = 1)

Complex Nested Logic
Combining multiple AND/OR conditions:

json
{
    "Query": [
        {
            "Field": "AssetDetails.Status",
            "Value": "2",
            "Query": [
                {
                    "Field": "AssetDetails.Type",
                    "Value": "1",
                    "Query": [
                        { "Field": "AssetDetails.Exchange", "Value": "1" },
                        { "Field": "AssetDetails.Exchange", "Value": "2" }
                    ]
                },
                { "Field": "AssetDetails.Type", "Value": "3" }
            ]
        }
    ]
}
Result: Assets where Status = 2 AND ( (Type = 1 AND (Exchange = 1 OR Exchange = 2)) OR Type = 3 )

Field Names and Mapping
Asset Fields
Field Path	Type	Description
AssetDetails.ID	string	Asset unique identifier
AssetDetails.OrganizationID	string	Organization UUID
AssetDetails.Status	int	Asset status (1=Draft, 2=Active, 3=Suspended)
AssetDetails.Type	int	Asset type (1=Equity, 2=Commodity, 3=Crypto)
AssetDetails.Name	string	Asset display name
AssetDetails.ExchangeTickerSymbol	string	Ticker symbol on exchange
AssetDetails.Exchange	int	Exchange identifier
AssetDetails.InternalDescription	string	Internal description
AssetDetails.MinTransactionAmount	int64	Minimum transaction amount
AssetDetails.TradingMarginPercentage	float	Trading margin percentage
AssetDetails.AssetMarginPercentage	float	Asset margin percentage
AssetDetails.SmartContractIssuerAddr	string	Smart contract address
MetaData.Network	int	Network (1=mainnet, 2=testnet, 3=devnet)
MetaData.CreatedAt.seconds	int64	Creation timestamp (seconds)
MetaData.CreatedAt.nanos	int32	Creation timestamp (nanoseconds)
MetaData.UpdatedAt.seconds	int64	Last update timestamp (seconds)
MetaData.UpdatedAt.nanos	int32	Last update timestamp (nanoseconds)
Audit.ChangedBy	string	User who made last change
Audit.ChangedAt.seconds	int64	Change timestamp (seconds)
Audit.Reason	string	Reason for change
Order Fields
Field Path	Type	Description
Instruction.OrderID	int64	Order identifier
Instruction.Creator	string	Order creator address
Instruction.Denom	string	Asset denomination
Instruction.Amount	int64	Order amount (scaled)
Instruction.AmountExp	int32	Amount exponent
Instruction.LimitPrice	int64	Limit price (scaled)
Instruction.LimitPriceExp	int32	Price exponent
Instruction.OrderType	int	Order type (1=Limit, 2=Market)
InternalOrderState	int	Internal order state
BrokerOrderDetails.Status	int	Broker order status
BrokerOrderDetails.Side	int	Order side (1=Buy, 2=Sell)
BrokerOrderDetails.Type	int	Order type
OrganizationID	string	Organization UUID
UserID	string	User identifier
TXID	string	Transaction hash
CreatedAt.seconds	int64	Creation timestamp
UpdatedAt.seconds	int64	Last update timestamp
Trade Fields
Field Path	Type	Description
UserID	string	User identifier
OrderKey	string	Associated order key
Amount.Value	int64	Trade amount (scaled)
Amount.Exp	int32	Amount exponent
Price	int64	Trade price
Side	int	Trade side (1=Buy, 2=Sell)
OrganizationID	string	Organization UUID
TXID	string	Transaction hash
BlockHeight	int64	Blockchain block height
BlockTime.seconds	int64	Block timestamp
Status	int	Trade status
Enriched	bool	Whether trade data is enriched
Processed	bool	Whether trade is processed
API Endpoints
GET /api/search/assets
Search for assets with optional authentication.

Headers
Header	Description	Required
Authorization	Bearer token	No (optional for public assets)
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Query Parameters
Parameter	Type	Description	Required	Default
query	string	Base64-encoded Query object	Yes	-
page	int	Page number (0-indexed)	No	0
order_by	string	Field to sort by	No	UpdatedAt
dir	int	Sort direction (0=asc, 1=desc)	No	1 (desc)
Sorting Notes
For timestamp fields, use lowercase subfield: MetaData.UpdatedAt.seconds or CreatedAt.nanos

Field must exist in the model definition

Default sort is UpdatedAt descending (newest first)

If dir is specified, order_by is required

Example Request
bash
# First, create and encode a query
QUERY='{"Query":[{"Field":"AssetDetails.Status","Value":"2"},{"Field":"AssetDetails.Type","Value":"1"}]}'
ENCODED_QUERY=$(echo -n "$QUERY" | base64 -w 0)

curl -X GET "https://api.sologenic.org/api/search/assets?query=${ENCODED_QUERY}&page=1&order_by=UpdatedAt&dir=1" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Network: mainnet"
Example Response
json
{
  "Results": [
    {
      "Data": "{\"AssetDetails\":{\"ID\":\"gnhm_1_9a81fae8-f245-4c47-be94-b7d683dff6ef_testcore1mp52apfwjgpd4fkqqf8lkysy9pwnhkm9kxqrvp\",\"OrganizationID\":\"9a81fae8-f245-4c47-be94-b7d683dff6ef\",\"Status\":2,\"Type\":1,\"Name\":\"Trinidad and Tobago Dollar\",\"ExchangeTickerSymbol\":\"TRIN\",\"Exchange\":2,\"InternalDescription\":\"Compatible sustainable monitoring\",\"MinTransactionAmount\":68566,\"TradingMarginPercentage\":0.213,\"LogoFile\":{\"Reference\":\"testnet/logo/9a81fae8-f245-4c47-be94-b7d683dff6ef/TRIN_2\",\"Extension\":\"image/jpeg\",\"Name\":\"logoo.jpeg\"},\"AssetMarginPercentage\":0.03,\"Denom\":{\"Currency\":{\"Symbol\":\"GNHM\",\"Version\":\"1\"},\"Subunit\":\"sugnhm_1\",\"Precision\":4,\"Description\":\"A withdrawal of TOP 498.30 occurred at Gleason, Gulgowski and Rolfson using a card ending in ****5722 for account ***9041.\"},\"SmartContractIssuerAddr\":\"testcore1mp52apfwjgpd4fkqqf8lkysy9pwnhkm9kxqrvp\"},\"MetaData\":{\"Network\":2,\"UpdatedAt\":{\"seconds\":1752219576,\"nanos\":920473992},\"CreatedAt\":{\"seconds\":1752219576,\"nanos\":920450906}},\"Audit\":{\"ChangedBy\":\"iso-admin@mailinator.org\",\"ChangedAt\":{\"seconds\":1752219576,\"nanos\":920474402}}}",
      "CreatedAt": {
        "nanos": 368224824
      },
      "UpdatedAt": {
        "nanos": 368224954
      },
      "Key": "gnhm_1_9a81fae8-f245-4c47-be94-b7d683dff6ef_testcore1mp52apfwjgpd4fkqqf8lkysy9pwnhkm9kxqrvp",
      "Network": "testnet"
    }
  ],
  "Total": 100
}
GET /api/search/orders
Search for orders (authenticated only).

Headers
Header	Description	Required
Authorization	Bearer token	Yes
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Query Parameters
Parameter	Type	Description	Required	Default
query	string	Base64-encoded Query object	Yes	-
page	int	Page number (0-indexed)	No	0
order_by	string	Field to sort by	No	UpdatedAt
dir	int	Sort direction (0=asc, 1=desc)	No	1 (desc)
Security Note
The backend automatically filters results by the authenticated user's UserID and OrganizationID. Do not include these fields in your query.

Example Request
bash
curl -X GET "https://api.sologenic.org/api/search/orders?query=${ENCODED_QUERY}&page=2" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Network: mainnet"
Example Response
json
{
  "Results": [
    {
      "Data": "{\"Network\":2,\"SmartContractAddr\":\"testcore13s2mmgg4uu4...qah8uxufugtajkeq2qgznc28\",\"Instruction\":{\"OrderID\":1234,\"Creator\":\"testcore15ms2zan4z3y9d29rxsyan5v5vecc04ycts2c85\",\"Denom\":\"suaapl_1-testcore13s2mmgg4uu4...qah8uxufugtajkeq2qgznc28\",\"Amount\":100,\"AmountExp\":2,\"LimitPrice\":15000,\"LimitPriceExp\":2,\"OrderDetailType\":2,\"OrderType\":1},\"CreatedAt\":{\"seconds\":1752191886,\"nanos\":414533000},\"UpdatedAt\":{\"seconds\":1752191889,\"nanos\":202828000},\"TransactionType\":1,\"TXID\":\"someTXID-123456-test\",\"GasFee\":1000000,\"DetectedAt\":{\"seconds\":1752191886,\"nanos\":414534000},\"Height\":123456,\"InternalOrderState\":6,\"BrokerOrderDetails\":{\"BrokerAssignedID\":\"someBrokerID-123456-test\",\"ClientOrderID\":{\"Network\":2,\"SmartContractAddr\":\"testcore13s2mmgg4uu4...qah8uxufugtajkeq2qgznc28\",\"OrderID\":123},\"SubmittedAt\":{\"seconds\":1752191886,\"nanos\":414521000},\"FilledAt\":{\"seconds\":1752191886,\"nanos\":414522000},\"ExpiredAt\":{\"seconds\":1752191886,\"nanos\":414523000},\"CancelledAt\":{\"seconds\":1752191886,\"nanos\":414524000},\"AssetID\":\"someAssetID-123456-test\",\"Symbol\":\"suaapl_1-testcore13s2mmgg4uu4...qah8uxufugtajkeq2qgznc28\",\"AssetClass\":1,\"OrderClass\":1,\"Type\":1,\"Side\":1,\"TimeInForce\":1,\"CreatedAt\":{\"seconds\":1752191886,\"nanos\":414524000},\"UpdatedAt\":{\"seconds\":1752191886,\"nanos\":414525000},\"Status\":2,\"PartialPrice\":{\"Value\":15000,\"Exp\":2},\"PartialQty\":{\"Value\":100,\"Exp\":2}},\"InstanceID\":\"someInstanceID-123456-test\",\"BlockTime\":{\"seconds\":1752191886,\"nanos\":414535000},\"Sequence\":123,\"OrganizationID\":\"72c4c072-2fe4-4f72-ae9d-d9d52a05fd71\",\"UserID\":\"test@test.com\"}",
      "CreatedAt": {
        "nanos": 771019217
      },
      "UpdatedAt": {
        "nanos": 771019507
      },
      "Key": "someTXID-123456-test",
      "Network": "testnet"
    }
  ],
  "Total": 100
}
GET /api/search/trades
Search for trades (authenticated only).

Headers
Header	Description	Required
Authorization	Bearer token	Yes
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Query Parameters
Parameter	Type	Description	Required	Default
query	string	Base64-encoded Query object	Yes	-
page	int	Page number (0-indexed)	No	0
order_by	string	Field to sort by	No	UpdatedAt
dir	int	Sort direction (0=asc, 1=desc)	No	1 (desc)
Security Note
The backend automatically filters results by the authenticated user's UserID and OrganizationID. Do not include these fields in your query.

Example Request
bash
curl -X GET "https://api.sologenic.org/api/search/trades?query=${ENCODED_QUERY}&page=2" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 215a551d-9284-4f72-ae9d-9284f40d1340" \
  -H "Network: mainnet"
Example Response
json
{
  "Results": [
    {
      "Data": "{\"UserID\":\"nick.luong@sologenic.org\",\"OrderKey\":\"1234-testcore13s2mmgg4uu4f...ah8uxufugtajkeq2qgznc28-2\",\"Sequence\":123,\"Amount\":{\"Value\":100,\"Exp\":2},\"Price\":1500000,\"Denom1\":{\"Currency\":{\"Symbol\":\"WUSDC\",\"Version\":\"1\"},\"Subunit\":\"suwusdc_1\",\"Issuer\":\"testcore13s2mmgg4uu4f...ah8uxufugtajkeq2qgznc28\"},\"Denom2\":{\"Currency\":{\"Symbol\":\"AAPL\",\"Version\":\"1\"},\"Subunit\":\"suaapl_1\",\"Issuer\":\"testcore13s2mmgg4uu4f...ah8uxufugtajkeq2qgznc28\"},\"Side\":1,\"BlockTime\":{\"seconds\":1752191886,\"nanos\":414535000},\"OrganizationID\":\"72c4c072-2fe4-4f72-ae9d-d9d52a05fd71\",\"MetaData\":{\"Network\":2,\"UpdatedAt\":{\"seconds\":1752191889,\"nanos\":202828000},\"CreatedAt\":{\"seconds\":1752191886,\"nanos\":414533000}},\"TXID\":\"someTXID-123456-test\",\"BlockHeight\":123456,\"Enriched\":true,\"Processed\":true,\"Status\":6}",
      "CreatedAt": {
        "nanos": 601903226
      },
      "UpdatedAt": {
        "nanos": 601903466
      },
      "Key": "someTXID-123456-test",
      "Network": "testnet"
    }
  ],
  "Total": 100
}
GET /api/search/tx/assets
Search for assets for transaction purposes (no authentication required).

Headers
Header	Description	Required
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Query Parameters
Parameter	Type	Description	Required	Default
query	string	Base64-encoded Query object	Yes	-
page	int	Page number (0-indexed)	No	0
order_by	string	Field to sort by	No	UpdatedAt
dir	int	Sort direction (0=asc, 1=desc)	No	1 (desc)
Special Access
Sologenic organization users can see all assets regardless of organization

Other organizations only see their own assets

Example Request
bash
curl -X GET "https://api.sologenic.org/api/search/tx/assets?query=${ENCODED_QUERY}&page=1&order_by=UpdatedAt&dir=1" \
  -H "OrganizationID: 9a81fae8-f245-4c47-be94-b7d683dff6ef" \
  -H "Network: mainnet"
GET /api/search/rawquery
Execute a raw OpenSearch query against the assets index.

Headers
Header	Description	Required
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	No (but recommended)
Query Parameters
Parameter	Type	Description	Required
query	string	Base64-encoded raw OpenSearch query	Yes
Security Warning
This endpoint does NOT automatically filter by organization or user. Use with extreme caution in production.

Example Raw Query
json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "Data.AssetDetails.Status": "3" } }
      ]
    }
  },
  "from": 20,
  "size": 20,
  "sort": [
    { "Data.MetaData.UpdatedAt.seconds": { "order": "desc" } }
  ]
}
Example Request
bash
# Create and encode raw query
RAW_QUERY='{"query":{"bool":{"must":[{"match":{"Data.AssetDetails.Status":"3"}}]}},"from":20,"size":20,"sort":[{"Data.MetaData.UpdatedAt.seconds":{"order":"desc"}}]}'
ENCODED_QUERY=$(echo -n "$RAW_QUERY" | base64 -w 0)

curl -X GET "https://api.sologenic.org/api/search/rawquery?query=${ENCODED_QUERY}" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
Query Construction Examples
Example 1: Basic Asset Search
Requirement: Find active equity assets with "Dollar" in the name

javascript
const query = {
  Query: [
    { Field: "AssetDetails.Status", Value: "2" },
    { Field: "AssetDetails.Type", Value: "1" },
    { Field: "AssetDetails.Name", Operator: "CONTAINS", Value: "Dollar" }
  ]
};
Example 2: Date Range Search
Requirement: Find assets created in the last 30 days

javascript
const thirtyDaysAgo = Math.floor(Date.now() / 1000) - (30 * 24 * 60 * 60);
const query = {
  Query: [
    { 
      Field: "MetaData.CreatedAt.seconds", 
      Operator: "GREATER_THAN_EQUALS", 
      Value: thirtyDaysAgo.toString(),
      FieldType: "DATE"
    }
  ]
};
Example 3: Complex OR Logic
Requirement: Find assets that are either (Type=1 AND Exchange=1) OR (Type=3)

javascript
const query = {
  Query: [
    {
      Field: "AssetDetails.Type",
      Value: "1",
      Query: [
        { Field: "AssetDetails.Exchange", Value: "1" }
      ]
    },
    {
      Field: "AssetDetails.Type",
      Value: "3"
    }
  ]
};
Example 4: Multi-field Search with AND/OR
Requirement: Find active assets that are either equity OR commodity, AND have margin < 0.05

javascript
const query = {
  Query: [
    {
      Field: "AssetDetails.Status",
      Value: "2",
      Query: [
        {
          Field: "AssetDetails.Type",
          Value: "1",
          Query: [
            { Field: "AssetDetails.TradingMarginPercentage", Operator: "LESS_THAN", Value: "0.05" }
          ]
        },
        {
          Field: "AssetDetails.Type",
          Value: "2",
          Query: [
            { Field: "AssetDetails.TradingMarginPercentage", Operator: "LESS_THAN", Value: "0.05" }
          ]
        }
      ]
    }
  ]
};
Pagination Details
Page Calculation
text
Total Results: 95
Page Size: 20 (fixed)

Page 0: items 0-19   (offset: 0)
Page 1: items 20-39  (offset: 20)
Page 2: items 40-59  (offset: 40)
Page 3: items 60-79  (offset: 60)
Page 4: items 80-94  (offset: 80)
Response Fields
Field	Type	Description
Results	[]Result	Array of search results (max 20)
Total	int	Total number of matching records
Result Object
Field	Type	Description
Data	string	JSON string of the actual data object
CreatedAt	Timestamp	Record creation timestamp
UpdatedAt	Timestamp	Record last update timestamp
Key	string	Unique record identifier
Network	string	Network environment
Integration Examples
JavaScript/React Client
javascript
class OpenSearchClient {
  constructor(baseUrl, organizationId, network = 'mainnet', token = null) {
    this.baseUrl = baseUrl;
    this.organizationId = organizationId;
    this.network = network;
    this.token = token;
  }

  // Build and encode a query
  static buildQuery(conditions, nestedLogic = null) {
    const query = { Query: conditions };
    if (nestedLogic) {
      query.Query[0].Query = nestedLogic;
    }
    return Buffer.from(JSON.stringify(query)).toString('base64');
  }

  // Simple equality condition
  static equals(field, value) {
    return { Field: field, Value: value };
  }

  // Contains condition (substring)
  static contains(field, value) {
    return { Field: field, Operator: 'CONTAINS', Value: value };
  }

  // Range condition
  static range(field, operator, value, fieldType = 'NUMBER') {
    return { Field: field, Operator: operator, Value: value, FieldType: fieldType };
  }

  async searchAssets(query, page = 0, orderBy = 'UpdatedAt', dir = 1) {
    const url = this._buildUrl('/api/search/assets', query, page, orderBy, dir);
    const response = await fetch(url, { headers: this._getHeaders() });
    return response.json();
  }

  async searchOrders(query, page = 0, orderBy = 'UpdatedAt', dir = 1) {
    const url = this._buildUrl('/api/search/orders', query, page, orderBy, dir);
    const response = await fetch(url, { headers: this._getHeaders(true) });
    return response.json();
  }

  async searchTrades(query, page = 0, orderBy = 'UpdatedAt', dir = 1) {
    const url = this._buildUrl('/api/search/trades', query, page, orderBy, dir);
    const response = await fetch(url, { headers: this._getHeaders(true) });
    return response.json();
  }

  async searchTxAssets(query, page = 0, orderBy = 'UpdatedAt', dir = 1) {
    const url = this._buildUrl('/api/search/tx/assets', query, page, orderBy, dir);
    const response = await fetch(url, { headers: this._getHeaders() });
    return response.json();
  }

  async rawQuery(rawQuery) {
    const encoded = Buffer.from(JSON.stringify(rawQuery)).toString('base64');
    const url = `${this.baseUrl}/api/search/rawquery?query=${encoded}`;
    const response = await fetch(url, { headers: this._getHeaders() });
    return response.json();
  }

  _buildUrl(endpoint, query, page, orderBy, dir) {
    let url = `${this.baseUrl}${endpoint}?query=${query}&page=${page}`;
    if (orderBy) url += `&order_by=${orderBy}`;
    if (dir !== undefined) url += `&dir=${dir}`;
    return url;
  }

  _getHeaders(requireAuth = false) {
    const headers = {
      'OrganizationID': this.organizationId,
      'Network': this.network
    };
    
    if (requireAuth && this.token) {
      headers['Authorization'] = `Bearer: ${this.token}`;
    }
    
    return headers;
  }
}

// Usage Example
async function searchExamples() {
  const client = new OpenSearchClient(
    'https://api.sologenic.org',
    '215a551d-9284-4f72-ae9d-9284f40d1340',
    'mainnet',
    'eyJhbGciOiJSUzI1NiIs...'
  );

  // Search for active assets
  const query = OpenSearchClient.buildQuery([
    OpenSearchClient.equals('AssetDetails.Status', '2'),
    OpenSearchClient.equals('AssetDetails.Type', '1')
  ]);
  
  const assets = await client.searchAssets(query, 0, 'AssetDetails.Name', 0);
  console.log(`Found ${assets.Total} assets`);
  assets.Results.forEach(result => {
    const data = JSON.parse(result.Data);
    console.log(`- ${data.AssetDetails.Name}`);
  });

  // Search for orders with amount > 1000
  const orderQuery = OpenSearchClient.buildQuery([
    OpenSearchClient.range('Instruction.Amount', 'GREATER_THAN', '1000')
  ]);
  
  const orders = await client.searchOrders(orderQuery);
  console.log(`Found ${orders.Total} orders`);

  // Complex nested query
  const complexQuery = OpenSearchClient.buildQuery(
    [OpenSearchClient.equals('AssetDetails.Status', '2')],
    [
      OpenSearchClient.equals('AssetDetails.Type', '1'),
      OpenSearchClient.equals('AssetDetails.Type', '2')
    ]
  );
  
  const complexAssets = await client.searchAssets(complexQuery);
  console.log(`Found ${complexAssets.Total} assets matching complex criteria`);
}
Python Client
python
import base64
import json
import requests
from typing import Optional, Dict, List, Any
from enum import Enum
from dataclasses import dataclass

class Operator(Enum):
    EQUALS = "EQUALS"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"
    ENDS_WITH = "ENDS_WITH"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN_EQUALS = "GREATER_THAN_EQUALS"
    LESS_THAN_EQUALS = "LESS_THAN_EQUALS"

class FieldType(Enum):
    STRING = "STRING"
    NUMBER = "NUMBER"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"
    KEYWORD = "KEYWORD"

@dataclass
class QueryCondition:
    field: str
    value: str
    operator: Operator = Operator.EQUALS
    field_type: FieldType = FieldType.STRING
    nested: Optional[List['QueryCondition']] = None

class OpenSearchClient:
    def __init__(self, base_url: str, organization_id: str, network: str = 'mainnet', token: Optional[str] = None):
        self.base_url = base_url
        self.organization_id = organization_id
        self.network = network
        self.token = token
    
    @staticmethod
    def build_query(conditions: List[QueryCondition]) -> str:
        """Build and encode a query object"""
        query_obj = {"Query": []}
        
        for cond in conditions:
            query_item = {
                "Field": cond.field,
                "Value": cond.value,
                "Operator": cond.operator.value,
                "FieldType": cond.field_type.value
            }
            if cond.nested:
                query_item["Query"] = [
                    {
                        "Field": n.field,
                        "Value": n.value,
                        "Operator": n.operator.value,
                        "FieldType": n.field_type.value
                    }
                    for n in cond.nested
                ]
            query_obj["Query"].append(query_item)
        
        json_str = json.dumps(query_obj)
        return base64.b64encode(json_str.encode()).decode()
    
    @staticmethod
    def equals(field: str, value: str) -> QueryCondition:
        return QueryCondition(field=field, value=value, operator=Operator.EQUALS)
    
    @staticmethod
    def contains(field: str, value: str) -> QueryCondition:
        return QueryCondition(field=field, value=value, operator=Operator.CONTAINS)
    
    @staticmethod
    def greater_than(field: str, value: str) -> QueryCondition:
        return QueryCondition(field=field, value=value, operator=Operator.GREATER_THAN, field_type=FieldType.NUMBER)
    
    def search_assets(self, query: str, page: int = 0, order_by: str = 'UpdatedAt', dir: int = 1) -> Dict:
        """Search for assets"""
        url = self._build_url('/api/search/assets', query, page, order_by, dir)
        response = requests
 response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def search_orders(self, query: str, page: int = 0, order_by: str = 'UpdatedAt', dir: int = 1) -> Dict:
        """Search for orders (requires authentication)"""
        url = self._build_url('/api/search/orders', query, page, order_by, dir)
        response = requests.get(url, headers=self._get_headers(require_auth=True))
        response.raise_for_status()
        return response.json()
    
    def search_trades(self, query: str, page: int = 0, order_by: str = 'UpdatedAt', dir: int = 1) -> Dict:
        """Search for trades (requires authentication)"""
        url = self._build_url('/api/search/trades', query, page, order_by, dir)
        response = requests.get(url, headers=self._get_headers(require_auth=True))
        response.raise_for_status()
        return response.json()
    
    def search_tx_assets(self, query: str, page: int = 0, order_by: str = 'UpdatedAt', dir: int = 1) -> Dict:
        """Search for transaction assets"""
        url = self._build_url('/api/search/tx/assets', query, page, order_by, dir)
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def raw_query(self, raw_query: Dict) -> Dict:
        """Execute raw OpenSearch query"""
        encoded = base64.b64encode(json.dumps(raw_query).encode()).decode()
        url = f"{self.base_url}/api/search/rawquery?query={encoded}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def _build_url(self, endpoint: str, query: str, page: int, order_by: str, dir: int) -> str:
        url = f"{self.base_url}{endpoint}?query={query}&page={page}"
        if order_by:
            url += f"&order_by={order_by}"
        if dir is not None:
            url += f"&dir={dir}"
        return url
    
    def _get_headers(self, require_auth: bool = False) -> Dict[str, str]:
        headers = {
            'OrganizationID': self.organization_id,
            'Network': self.network
        }
        
        if require_auth and self.token:
            headers['Authorization'] = f'Bearer: {self.token}'
        
        return headers

# Usage Example
client = OpenSearchClient(
    base_url='https://api.sologenic.org',
    organization_id='215a551d-9284-4f72-ae9d-9284f40d1340',
    network='mainnet',
    token='eyJhbGciOiJSUzI1NiIs...'
)

# Search for active equity assets
query = OpenSearchClient.build_query([
    OpenSearchClient.equals('AssetDetails.Status', '2'),
    OpenSearchClient.equals('AssetDetails.Type', '1')
])

assets = client.search_assets(query, page=0, order_by='AssetDetails.Name', dir=0)
print(f"Found {assets['Total']} assets")

for result in assets['Results']:
    data = json.loads(result['Data'])
    asset = data['AssetDetails']
    print(f"- {asset['Name']} ({asset['ExchangeTickerSymbol']})")

# Search for high-value orders
order_query = OpenSearchClient.build_query([
    OpenSearchClient.greater_than('Instruction.Amount', '10000')
])

orders = client.search_orders(order_query)
print(f"Found {orders['Total']} orders")
Go Client
go
package opensearch

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

type Operator string

const (
    OpEquals            Operator = "EQUALS"
    OpContains          Operator = "CONTAINS"
    OpStartsWith        Operator = "STARTS_WITH"
    OpEndsWith          Operator = "ENDS_WITH"
    OpGreaterThan       Operator = "GREATER_THAN"
    OpLessThan          Operator = "LESS_THAN"
    OpGreaterThanEquals Operator = "GREATER_THAN_EQUALS"
    OpLessThanEquals    Operator = "LESS_THAN_EQUALS"
)

type FieldType string

const (
    TypeString  FieldType = "STRING"
    TypeNumber  FieldType = "NUMBER"
    TypeDate    FieldType = "DATE"
    TypeBoolean FieldType = "BOOLEAN"
    TypeKeyword FieldType = "KEYWORD"
)

type QueryCondition struct {
    Field     string      `json:"Field"`
    Value     string      `json:"Value"`
    Operator  Operator    `json:"Operator"`
    FieldType FieldType   `json:"FieldType"`
    Nested    []QueryCondition `json:"Query,omitempty"`
}

type Query struct {
    Query []QueryCondition `json:"Query"`
}

type SearchResult struct {
    Data      string    `json:"Data"`
    CreatedAt Timestamp `json:"CreatedAt"`
    UpdatedAt Timestamp `json:"UpdatedAt"`
    Key       string    `json:"Key"`
    Network   string    `json:"Network"`
}

type Timestamp struct {
    Seconds int64 `json:"seconds"`
    Nanos   int32 `json:"nanos"`
}

type SearchResponse struct {
    Results []SearchResult `json:"Results"`
    Total   int            `json:"Total"`
}

type Client struct {
    baseURL        string
    organizationID string
    network        string
    token          string
    httpClient     *http.Client
}

func NewClient(baseURL, organizationID, network, token string) *Client {
    return &Client{
        baseURL:        baseURL,
        organizationID: organizationID,
        network:        network,
        token:          token,
        httpClient:     &http.Client{Timeout: 30 * time.Second},
    }
}

func (c *Client) BuildQuery(conditions []QueryCondition) (string, error) {
    query := Query{Query: conditions}
    jsonBytes, err := json.Marshal(query)
    if err != nil {
        return "", err
    }
    return base64.URLEncoding.EncodeToString(jsonBytes), nil
}

func (c *Client) Equals(field, value string) QueryCondition {
    return QueryCondition{
        Field:     field,
        Value:     value,
        Operator:  OpEquals,
        FieldType: TypeString,
    }
}

func (c *Client) Contains(field, value string) QueryCondition {
    return QueryCondition{
        Field:     field,
        Value:     value,
        Operator:  OpContains,
        FieldType: TypeString,
    }
}

func (c *Client) GreaterThan(field, value string) QueryCondition {
    return QueryCondition{
        Field:     field,
        Value:     value,
        Operator:  OpGreaterThan,
        FieldType: TypeNumber,
    }
}

func (c *Client) SearchAssets(query string, page int, orderBy string, dir int) (*SearchResponse, error) {
    url := c.buildURL("/api/search/assets", query, page, orderBy, dir)
    return c.doRequest(url, false)
}

func (c *Client) SearchOrders(query string, page int, orderBy string, dir int) (*SearchResponse, error) {
    url := c.buildURL("/api/search/orders", query, page, orderBy, dir)
    return c.doRequest(url, true)
}

func (c *Client) SearchTrades(query string, page int, orderBy string, dir int) (*SearchResponse, error) {
    url := c.buildURL("/api/search/trades", query, page, orderBy, dir)
    return c.doRequest(url, true)
}

func (c *Client) SearchTxAssets(query string, page int, orderBy string, dir int) (*SearchResponse, error) {
    url := c.buildURL("/api/search/tx/assets", query, page, orderBy, dir)
    return c.doRequest(url, false)
}

func (c *Client) RawQuery(rawQuery interface{}) (*SearchResponse, error) {
    jsonBytes, err := json.Marshal(rawQuery)
    if err != nil {
        return nil, err
    }
    
    encoded := base64.URLEncoding.EncodeToString(jsonBytes)
    url := fmt.Sprintf("%s/api/search/rawquery?query=%s", c.baseURL, encoded)
    return c.doRequest(url, false)
}

func (c *Client) buildURL(endpoint, query string, page int, orderBy string, dir int) string {
    u := fmt.Sprintf("%s%s?query=%s&page=%d", c.baseURL, endpoint, query, page)
    if orderBy != "" {
        u += fmt.Sprintf("&order_by=%s", orderBy)
    }
    if dir >= 0 {
        u += fmt.Sprintf("&dir=%d", dir)
    }
    return u
}

func (c *Client) doRequest(urlStr string, requireAuth bool) (*SearchResponse, error) {
    req, err := http.NewRequest("GET", urlStr, nil)
    if err != nil {
        return nil, err
    }
    
    req.Header.Set("OrganizationID", c.organizationID)
    req.Header.Set("Network", c.network)
    
    if requireAuth && c.token != "" {
        req.Header.Set("Authorization", "Bearer: "+c.token)
    }
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status code: %d, body: %s", resp.StatusCode, string(body))
    }
    
    var result SearchResponse
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }
    
    return &result, nil
}

// Usage example
func main() {
    client := NewClient(
        "https://api.sologenic.org",
        "215a551d-9284-4f72-ae9d-9284f40d1340",
        "mainnet",
        "eyJhbGciOiJSUzI1NiIs...",
    )
    
    // Search for active assets
    query, _ := client.BuildQuery([]QueryCondition{
        client.Equals("AssetDetails.Status", "2"),
        client.Equals("AssetDetails.Type", "1"),
    })
    
    assets, err := client.SearchAssets(query, 0, "AssetDetails.Name", 0)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Found %d assets\n", assets.Total)
    for _, result := range assets.Results {
        var data map[string]interface{}
        json.Unmarshal([]byte(result.Data), &data)
        assetDetails := data["AssetDetails"].(map[string]interface{})
        fmt.Printf("- %s\n", assetDetails["Name"])
    }
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
OPEN_SEARCH_STORE	OpenSearch service endpoint	fs-open-search-model
ORGANIZATION_STORE	Organization service endpoint	com-fs-organization-model
USER_STORE	User service endpoint	com-fs-user-model
ROLE_STORE	Role service endpoint	com-fs-role-model
AUTH_FIREBASE_SERVICE	Firebase authentication	com-fs-auth-firebase-model
HTTP_CONFIG	HTTP server configuration	com-be-http-lib
Optional Environment Variables
Environment Variable	Description	Source
FEATURE_FLAG_STORE	Feature flag service	com-fs-feature-flag-model
SOLOGENIC_ORGANIZATION_ID	Special org ID with full access	Configuration
Example Environment Configuration
bash
# Required
OPEN_SEARCH_STORE=open-search-store:50062
ORGANIZATION_STORE=organization-service:50060
USER_STORE=user-service:50049
ROLE_STORE=role-store:50066
AUTH_FIREBASE_SERVICE=auth-service:50070

# Optional
FEATURE_FLAG_STORE=feature-flag-store:50055
SOLOGENIC_ORGANIZATION_ID=sologenic-platform
LOG_LEVEL=info
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100

# HTTP Configuration
HTTP_CONFIG='{
  "port": ":8080",
  "cors": {
    "allowedOrigins": ["http://localhost:3000", "https://app.sologenic.org"]
  },
  "timeouts": {
    "read": "30s",
    "write": "30s",
    "idle": "30s",
    "shutdown": "10s"
  }
}'
Docker Compose Example
yaml
version: '3.8'

services:
  open-search-service:
    image: sologenic/open-search-service:latest
    environment:
      - OPEN_SEARCH_STORE=open-search-store:50062
      - ORGANIZATION_STORE=organization-service:50060
      - USER_STORE=user-service:50049
      - ROLE_STORE=role-store:50066
      - AUTH_FIREBASE_SERVICE=auth-service:50070
      - LOG_LEVEL=info
      - SOLOGENIC_ORGANIZATION_ID=sologenic-platform
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
    networks:
      - internal

  open-search-store:
    image: sologenic/open-search-store:latest
    environment:
      - OPENSEARCH_HOSTS=https://opensearch:9200
      - OPENSEARCH_USERNAME=admin
      - OPENSEARCH_PASSWORD=admin
    networks:
      - internal

  opensearch:
    image: opensearchproject/opensearch:latest
    environment:
      - discovery.type=single-node
      - plugins.security.disabled=true
    ports:
      - "9200:9200"
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Responses
Bad Request (400) - Invalid Query
json
{
  "error": "Bad Request",
  "message": "Invalid query format: base64 decode failed"
}
Bad Request (400) - Invalid Field
json
{
  "error": "Bad Request",
  "message": "Invalid field name: AssetDetails.InvalidField",
  "valid_fields": ["AssetDetails.Status", "AssetDetails.Type", "AssetDetails.Name"]
}
Unauthorized (401)
json
{
  "error": "Unauthorized",
  "message": "Authentication required for this endpoint"
}
Forbidden (403)
json
{
  "error": "Forbidden",
  "message": "Access denied for organization: 215a551d-9284-4f72-ae9d-9284f40d1340"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Endpoint not found: /api/search/invalid"
}
Internal Server Error (500)
json
{
  "error": "Internal Server Error",
  "message": "Failed to execute search query",
  "request_id": "req_12345"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Empty results	Wrong field name	Check exact field name in model
Query decode error	Invalid base64	Ensure proper base64 encoding
Sorting doesn't work	Wrong field case	Use lowercase for timestamp subfields
Authentication required	Missing token for orders/trades	Include valid Authorization header
Organization filter missing	Header not sent	Always include OrganizationID
Slow queries	Complex nested logic	Simplify query or add indexes
Page out of range	Invalid page number	Page starts at 0, max (Total/20)
Debugging Commands
bash
# Test base64 encoding
echo -n '{"Query":[{"Field":"AssetDetails.Status","Value":"2"}]}' | base64

# Test asset search with curl
QUERY=$(echo -n '{"Query":[{"Field":"AssetDetails.Status","Value":"2"}]}' | base64 -w 0)
curl -X GET "https://api.sologenic.org/api/search/assets?query=${QUERY}&page=0" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v | jq '.Total'

# Test raw query
RAW_QUERY='{"query":{"match_all":{}},"size":5}'
ENCODED=$(echo -n "$RAW_QUERY" | base64 -w 0)
curl -X GET "https://api.sologenic.org/api/search/rawquery?query=${ENCODED}" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v | jq '.Results | length'

# Check OpenSearch cluster health
curl -X GET "https://opensearch:9200/_cluster/health" \
  -u admin:admin \
  -k
Best Practices
Query Construction
Practice	Recommendation
Field names	Use exact field names from protobuf definitions
Nested fields	Use dot notation (e.g., AssetDetails.Status)
Timestamp sorting	Use lowercase subfield (UpdatedAt.seconds)
Query complexity	Limit nesting depth to 3-4 levels
Base64 encoding	Use standard base64 without line breaks
Performance
Practice	Recommendation
Page size	Fixed at 20 results per page
Result limits	Use specific queries to reduce result set
Index usage	Query indexed fields for better performance
Caching	Implement client-side caching for frequent queries
Security
Practice	Recommendation
Authentication	Always require auth for orders/trades
Organization isolation	Never omit OrganizationID header
User filtering	Backend adds UserID for user-specific endpoints
Raw query	Restrict to admin use only
Input validation	Validate all query parameters
Related Services
Service	Description
OpenSearch Store	Elasticsearch/OpenSearch data access layer
Organization Store	Tenant isolation and validation
User Store	User authentication and preferences
Role Store	Permission management
Auth Firebase Service	Token validation
Feature Flag Store	Feature toggles for search functionality
License
This documentation is part of the TX Marketplace platform.
