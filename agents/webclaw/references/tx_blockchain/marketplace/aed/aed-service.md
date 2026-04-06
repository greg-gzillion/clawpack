# Asset Epoch Data (AED) Service

The Asset Epoch Data Service provides RESTful interfaces for retrieving financial market data including price charts, tickers, and trading statistics for trading pairs. This service handles OHLCV (Open, High, Low, Close, Volume) data with support for multiple timeframes and sparse data representation for efficient transmission.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Asset Epoch Data (AED) Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ API Endpoints │ │
│ ├─────────────────────────┬───────────────────────────────────────────┤ │
│ │ GET /aed/chart │ GET /aed/tickers │ │
│ │ (OHLCV chart data) │ (Real-time tickers) │ │
│ └─────────────────────────┴───────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬───────────────┬───────────────────┤ │
│ │ AED Store │ Asset Store │ User Store │ Role Store │ │
│ │ (OHLCV data) │ (Symbol info) │ │ │ │
│ └───────────────┴───────────────┴───────────────┴───────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Data Sources │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • OHLC Database (Time-series data) │ │
│ │ • In-Memory Cache (Fast lookups) │ │
│ │ • Asset Metadata Store │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /aed/chart | ORGANIZATION_ADMINISTRATOR | Get OHLCV chart data for symbol |
| GET /aed/tickers | ORGANIZATION_ADMINISTRATOR | Get real-time tickers for symbols |

**Note:** All authenticated endpoints require:
- Valid Firebase token in `Authorization` header (prepended with `Bearer:`)
- Organization ID in `OrganizationID` header (tenant isolation)
- Network in `Network` header (mainnet, testnet, devnet)

## Data Models

### AED (Asset Epoch Data) Object

| Field | Type | Description |
|-------|------|-------------|
| OrganizationID | string | Organization UUID |
| Symbol | string | Trading pair symbol (format: `{base}_{issuer}:{quote}_{issuer}`) |
| Timestamp | Timestamp | Start time of the period |
| Period | Period | Time period configuration |
| MetaData | MetaData | Creation/update timestamps and network |
| Value | []Value | OHLCV and derived values |
| Series | int | Data series type (1=PRICE, 2=FUNDAMENTAL, 3=USER_PERFORMANCE - rejected) |

### Period Object

| Field | Type | Description |
|-------|------|-------------|
| Type | int | Period type (1=MINUTE, 2=HOUR, 3=DAY, 4=WEEK) |
| Duration | int | Number of units (e.g., 5 for 5 minutes) |

### Value Object

| Field | Type | Description |
|-------|------|-------------|
| Field | int | Value field identifier (see Field Values) |
| Float64Val | float64 | Floating point value (for price/ratio fields) |
| Int64Val | int64 | Integer value (for count fields) |

### Ticker Object

| Field | Type | Description |
|-------|------|-------------|
| Symbol | string | Trading pair symbol |
| OpenTime | int64 | Period open timestamp (seconds) |
| CloseTime | int64 | Period close timestamp (seconds) |
| OpenPrice | float64 | Opening price |
| HighPrice | float64 | Highest price in period |
| LowPrice | float64 | Lowest price in period |
| LastPrice | float64 | Last (current) price |
| FirstPrice | float64 | First price in period |
| Volume | float64 | Trading volume (base currency) |
| InvertedVolume | float64 | Trading volume (quote currency) |
| Inverted | bool | Whether price is inverted |
| MarketCap | float64 | Market capitalization |
| EPS | float64 | Earnings per share |
| PERatio | float64 | Price-to-earnings ratio |
| Yield | float64 | Dividend yield percentage |

### MetaData Object

| Field | Type | Description |
|-------|------|-------------|
| Network | int | Network identifier (1=mainnet, 2=testnet, 3=devnet) |
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

### Series Values

| Series ID | Series Name | Description |
|-----------|-------------|-------------|
| 1 | PRICE | Price-based OHLCV data |
| 2 | FUNDAMENTAL | Fundamental analysis data (EPS, PE, Yield) |
| 3 | USER_PERFORMANCE | **REJECTED** - Use /graph endpoint in holdings service |

### Field Values (Value.Field)

| Field ID | Field Name | Type | Description |
|----------|------------|------|-------------|
| 1 | OPEN | Float64 | Opening price |
| 2 | HIGH | Float64 | Highest price |
| 3 | LOW | Float64 | Lowest price |
| 4 | CLOSE | Float64 | Closing price |
| 5 | VOLUME | Float64 | Trading volume (base) |
| 6 | PERIOD_COUNT | Int64 | Number of trades/periods |
| 7 | INVERTED_VOLUME | Float64 | Trading volume (quote) |
| 8 | MARKET_CAP | Float64 | Market capitalization |
| 9 | EPS | Float64 | Earnings per share |
| 10 | PE_RATIO | Float64 | Price-to-earnings ratio |
| 11 | YIELD | Float64 | Dividend yield |
| 12 | PERIOD_START | Int64 | Period start timestamp |
| 13 | PERIOD_END | Int64 | Period end timestamp |

### Network Values

| Network ID | Network Name | Description |
|------------|--------------|-------------|
| 1 | mainnet | Production network |
| 2 | testnet | Testing network |
| 3 | devnet | Development network |

## API Endpoints

### GET /aed/chart

Loads price chart data for a symbol over a specified period. Returns sparse OHLCV data optimized for chart rendering.

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
| symbol | string | Trading pair symbol | Yes |
| series | int | Data series (1=PRICE, 2=FUNDAMENTAL) | Yes |
| period | string | Time period (see Period Values) | Yes |
| from | int64 | From timestamp (seconds since epoch) | No |
| to | int64 | To timestamp (seconds since epoch) | No |
| backfill | bool | Backfill first gap if no exact record (default: true) | No |
| allowcache | bool | Use in-memory cache, fill gaps (default: true) | No |

#### Period Values

| Period String | Description | Duration |
|---------------|-------------|----------|
| 1m | 1 minute | 1 minute |
| 3m | 3 minutes | 3 minutes |
| 5m | 5 minutes | 5 minutes |
| 15m | 15 minutes | 15 minutes |
| 30m | 30 minutes | 30 minutes |
| 1h | 1 hour | 1 hour |
| 3h | 3 hours | 3 hours |
| 6h | 6 hours | 6 hours |
| 12h | 12 hours | 12 hours |
| 1d | 1 day | 1 day |
| 3d | 3 days | 3 days |
| 1w | 1 week | 1 week |

#### Cache and Backfill Behavior

| allowcache | backfill | Behavior |
|------------|----------|----------|
| true | true | Use cache, fill first, middle, and end gaps |
| true | false | Use cache, fill middle and end gaps only |
| false | any | Direct database query, no gap filling (sparse data) |

**Note:** When `allowcache=false`, data is returned directly from the database without filling gaps, which may result in sparse data. This guarantees the smallest data sets over the wire (fast) and smaller caches which are easier to manage.

#### Symbol Format

Trading pairs follow the format:
{base_asset}{issuer}:{quote_asset}{issuer}

text

Example:
suwusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28:sumsft_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28

text

#### Example Request

```bash
curl -X GET \
  "https://api.admin.sologenic.org/api/aed/chart?symbol=suwusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28:sumsft_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28&series=2&period=5m&from=1743687000&to=1743701400" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet"
Example Response
json
{
  "AEDs": [
    {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Symbol": "suwusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28:sumsft_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
      "Timestamp": {
        "seconds": 1743687000
      },
      "Period": {
        "Type": 1,
        "Duration": 5
      },
      "MetaData": {
        "Network": 2,
        "UpdatedAt": {
          "seconds": 1745972243,
          "nanos": 177630000
        },
        "CreatedAt": {
          "seconds": 1745972242,
          "nanos": 122181000
        }
      },
      "Value": [
        {
          "Field": 1,
          "Float64Val": 320.65819262974753
        },
        {
          "Field": 2,
          "Float64Val": 321.00428602312036
        },
        {
          "Field": 3,
          "Float64Val": 319.6604219196984
        },
        {
          "Field": 4,
          "Float64Val": 319.6604219196984
        },
        {
          "Field": 5,
          "Float64Val": 25.906950396334995
        },
        {
          "Field": 6,
          "Int64Val": 5
        },
        {
          "Field": 8,
          "Float64Val": 2397453164397.7383
        },
        {
          "Field": 9,
          "Float64Val": 5.158400859304637
        },
        {
          "Field": 10,
          "Float64Val": 28.2097248007264
        },
        {
          "Field": 11,
          "Float64Val": 0.5204631011271763
        },
        {
          "Field": 12,
          "Int64Val": 1743687000
        },
        {
          "Field": 13,
          "Int64Val": 1743687240
        }
      ],
      "Series": 2
    },
    {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Symbol": "suwusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28:sumsft_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
      "Timestamp": {
        "seconds": 1743687300
      },
      "Period": {
        "Type": 1,
        "Duration": 5
      },
      "MetaData": {
        "Network": 2,
        "UpdatedAt": {
          "seconds": 1745972244,
          "nanos": 807874000
        },
        "CreatedAt": {
          "seconds": 1745972243,
          "nanos": 580059000
        }
      },
      "Value": [
        {
          "Field": 1,
          "Float64Val": 319.5315898274127
        },
        {
          "Field": 2,
          "Float64Val": 319.70894400381826
        },
        {
          "Field": 3,
          "Float64Val": 318.697741396257
        },
        {
          "Field": 4,
          "Float64Val": 319.18733795815683
        },
        {
          "Field": 5,
          "Float64Val": 30.049074476775246
        },
        {
          "Field": 6,
          "Int64Val": 5
        },
        {
          "Field": 8,
          "Float64Val": 2393905034686.1763
        },
        {
          "Field": 9,
          "Float64Val": 5.373756432510579
        },
        {
          "Field": 10,
          "Float64Val": 29.66575234790458
        },
        {
          "Field": 11,
          "Float64Val": 0.6820568237845774
        },
        {
          "Field": 12,
          "Int64Val": 1743687300
        },
        {
          "Field": 13,
          "Int64Val": 1743687540
        }
      ],
      "Series": 2
    }
  ]
}
Response Data Interpretation
The response contains an array of AED objects, each representing one time period. The Value array contains key-value pairs where Field identifies the data type and the corresponding Float64Val or Int64Val contains the value.

For chart rendering:

Map Field: 1 to OPEN price

Map Field: 2 to HIGH price

Map Field: 3 to LOW price

Map Field: 4 to CLOSE price

Map Field: 5 to VOLUME

Error Responses
Status Code	Description
200	Success - Returns chart data (may be empty)
400	Bad request - Invalid parameters
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
404	Not found - Symbol not found
500	Internal server error
GET /aed/tickers
Retrieves real-time ticker information for specified symbols.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Authorization	Bearer <firebase_token>	Yes
Query Parameters
Parameter	Type	Description	Required
symbols	string	Base64 encoded array of symbols (max 20, URL < 2KB)	Yes
series	int	Data series (1=PRICE, 2=FUNDAMENTAL)	No (default: 1)
Important: While there is no direct limit in the application, it is advised to keep the total length of the URL below 2KB (2048 bytes) to prevent browser failures.

Example Request
bash
# Symbols array: ["suwusdc_1-...:sumsft_1-..."]
SYMBOLS_BASE64="WyJzdXd1c2RjXzEtdGVzdGNvcmUxM3MybW1nZzR1dTRmbjhtdWU2czNsZ243NGp3ZHVwbmRqdHFhaDh1eHVmdWd0YWprZXEycWd6bmMyODpzdWFhcGxfMS10ZXN0Y29yZTEzczJtbWdnNHV1NGZuOG11ZTZzM2xnbjc0andkdXBuZGp0cWFoOHV4dWZ1Z3RhamtlcTJxZ3puYzI4Il0="

curl -X GET \
  "https://api.admin.sologenic.org/api/aed/tickers?symbols=${SYMBOLS_BASE64}&series=2" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet"
Example Response
json
{
  "tickers": [
    {
      "Symbol": "suwusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28:suaapl_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
      "OpenTime": 1746125992,
      "CloseTime": 1746212392,
      "OpenPrice": 169.00978514008708,
      "HighPrice": 169.00978514008708,
      "LowPrice": 169.00978514008708,
      "LastPrice": 169.00978514008708,
      "FirstPrice": 0,
      "Volume": 0,
      "InvertedVolume": 0,
      "Inverted": false,
      "MarketCap": 2525374784819.8413,
      "EPS": 5.46566917649556,
      "PERatio": 27.81760241146561,
      "Yield": 0.593260650413186
    }
  ]
}
Ticker Field Descriptions
Field	Description	Calculation
OpenTime	Period start timestamp	Unix seconds
CloseTime	Period end timestamp	Unix seconds
OpenPrice	Opening price	First trade price
HighPrice	Highest price	Max price in period
LowPrice	Lowest price	Min price in period
LastPrice	Current price	Most recent trade
FirstPrice	First price	First trade price
Volume	Trading volume	Sum of base volume
InvertedVolume	Inverted volume	Sum of quote volume
Inverted	Inverted flag	Price inversion indicator
MarketCap	Market cap	LastPrice × circulating supply
EPS	Earnings per share	Net earnings / shares outstanding
PERatio	P/E ratio	LastPrice / EPS
Yield	Dividend yield	Annual dividend / LastPrice × 100
Error Responses
Status Code	Description
200	Success - Returns tickers (may be empty)
400	Bad request - Invalid symbols format or empty array
401	Unauthorized - Invalid or missing token
403	Forbidden - Insufficient permissions
413	Payload too large - Symbols array too large
500	Internal server error
Sparse Data Representation
The AED service returns sparse data, meaning that if there is no data for a given interval, the interval is not returned. This approach provides:

Benefit	Description
Smaller payloads	Less data over the wire (faster)
Smaller caches	Easier to manage
Efficient rendering	Client expands sparse data
Sparse Data Example
If requesting 5-minute candles for 1 hour (12 candles) but only 3 have trades:

json
{
  "AEDs": [
    { "Timestamp": { "seconds": 1743687000 }, ... },  // 00:00
    { "Timestamp": { "seconds": 1743687300 }, ... },  // 00:05 (gap)
    { "Timestamp": { "seconds": 1743687600 }, ... },  // 00:10 (gap)
    // Missing: 00:15, 00:20, 00:25, 00:30, 00:35, 00:40, 00:45, 00:50, 00:55
    { "Timestamp": { "seconds": 1743690000 }, ... }   // 01:00
  ]
}
Client rendering code must expand the data by filling missing intervals with the last known value or null.

Pagination with Offset
A call returning a list of values can return an offset. Use this offset in the subsequent call to get the next set of data. If there is no more data to be returned, the offset is not returned or set to 0.

json
{
  "AEDs": [...],
  "Offset": 100  // Use this in next request
}
Next request:

text
GET /aed/chart?symbol=...&period=5m&offset=100
Chart Data Examples
1-Day Chart with 5-Minute Candles
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/aed/chart?symbol=BTCUSDC&series=1&period=5m&from=1735689600&to=1735776000" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: mainnet"
Weekly Chart with 1-Hour Candles
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/aed/chart?symbol=ETHUSDC&series=1&period=1h&from=1735171200&to=1735776000" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: mainnet"
Fundamental Data Chart
bash
curl -X GET \
  "https://api.admin.sologenic.org/api/aed/chart?symbol=AAPLUSDC&series=2&period=1d&from=1733097600&to=1735776000" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: mainnet"
Symbol Encoding for Tickers
Creating Base64 Encoded Symbols Array
bash
# Python example
import json
import base64

symbols = [
    "BTCUSDC_1-issuer:ETHUSDC_1-issuer",
    "AAPLUSDC_1-issuer:MSFTUSDC_1-issuer"
]

symbols_json = json.dumps(symbols)
symbols_base64 = base64.b64encode(symbols_json.encode()).decode()
print(symbols_base64)
bash
# Command line example
echo -n '["BTCUSDC_1-issuer:ETHUSDC_1-issuer","AAPLUSDC_1-issuer:MSFTUSDC_1-issuer"]' | base64
JavaScript/TypeScript Example
javascript
const symbols = [
  "BTCUSDC_1-issuer:ETHUSDC_1-issuer",
  "AAPLUSDC_1-issuer:MSFTUSDC_1-issuer"
];

const symbolsBase64 = btoa(JSON.stringify(symbols));
const url = `/api/aed/tickers?symbols=${encodeURIComponent(symbolsBase64)}`;
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	github.com/sologenic/com-be-http-lib/http/
AUTH_FIREBASE_SERVICE	Firebase authentication service	github.com/sologenic/com-fs-auth-firebase-service
AED_STORE	AED store endpoint (OHLCV data)	github.com/sologenic/com-fs-aed-model
ASSET_STORE	Asset store endpoint	github.com/sologenic/com-fs-asset-model
USER_STORE	User store endpoint	github.com/sologenic/com-fs-user-model
ROLE_STORE	Role store endpoint	github.com/sologenic/com-fs-role-model
FEATURE_FLAG_STORE	Feature flag service endpoint	github.com/sologenic/com-fs-feature-flag-model
ORGANIZATION_STORE	Organization service endpoint	github.com/sologenic/com-fs-organization-model
Optional Environment Variables
Environment Variable	Description	Default
LOG_LEVEL	Logging level (info, debug, warn, error)	info
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
  "message": "Insufficient permissions for this operation. Required role: ORGANIZATION_ADMINISTRATOR"
}
Bad Request (400) - Invalid Period
json
{
  "error": "Bad Request",
  "message": "Invalid period value",
  "details": "Period must be one of: 1m, 3m, 5m, 15m, 30m, 1h, 3h, 6h, 12h, 1d, 3d, 1w"
}
Bad Request (400) - Series Not Allowed
json
{
  "error": "Bad Request",
  "message": "Series not supported",
  "details": "Series 3 (USER_PERFORMANCE) is not supported. Use /graph endpoint in com-be-holdings-service"
}
Bad Request (400) - Too Many Symbols
json
{
  "error": "Bad Request",
  "message": "Too many symbols",
  "details": "Maximum 20 symbols allowed per request"
}
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Symbol not found",
  "details": "No data found for symbol: BTCUSDC"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
No data returned	Symbol doesn't exist	Verify symbol format and existence
Sparse data	No trades in period	Check if market is active
Slow response	Large date range	Reduce range or increase period
URL too long	Too many symbols	Limit symbols to 20 or use POST
USER_PERFORMANCE rejected	Wrong endpoint	Use holdings service /graph endpoint
Cache not working	allowcache=false	Set allowcache=true for gap filling
Debugging
Enable debug logging:

bash
LOG_LEVEL=debug
Check symbol existence:

bash
# First check if symbol exists via asset service
curl -X GET /api/asset/get?symbol=BTCUSDC \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet"
Test chart data with small range:

bash
# Start with small date range
curl -X GET "/api/aed/chart?symbol=BTCUSDC&series=1&period=1h&from=$(date -d '1 hour ago' +%s)&to=$(date +%s)" \
  -H "Authorization: Bearer <token>" \
  -H "OrganizationID: <org-id>" \
  -H "Network: testnet"
Best Practices
Chart Data
Use Appropriate Periods:

1m-30m for intraday trading

1h-6h for daily analysis

1d-1w for long-term trends

Limit Date Ranges: Request only necessary time ranges to reduce payload size

Enable Caching: Set allowcache=true for better performance and gap filling

Handle Sparse Data: Client should implement data expansion for missing intervals

Tickers
Batch Requests: Request multiple symbols in one call (up to 20)

Monitor URL Length: Keep symbols array encoded URL under 2KB

Refresh Appropriately:

Price tickers: Every 1-5 seconds

Fundamental data: Daily or weekly

Performance Optimization
Scenario	Recommended Period	Cache Setting
Real-time trading	1m, 5m	allowcache=true
Technical analysis	15m, 1h	allowcache=true
Daily overview	1d	allowcache=true
Historical backtesting	1d, 1w	allowcache=false
Fundamental analysis	1d	allowcache=true
Related Services
Service	Description
Admin Asset Service	Asset and symbol information
Holdings Service	User performance graphs (USER_PERFORMANCE series)
Organization Service	Tenant organization management
Admin Account Service	User and role management
License
This documentation is part of the TX Marketplace platform.

text

Now update the marketplace README to include the AED Service:

```bash
nano ~/dev/TXdocumentation/marketplace/README.md
Add the AED Service section:

markdown
## Asset Epoch Data (AED) Service

The Asset Epoch Data Service provides RESTful interfaces for retrieving financial market data including price charts, tickers, and trading statistics.

📖 **[AED Service Documentation](./aed/aed-service.md)**

**Key Features:**
- OHLCV chart data with multiple timeframes
- Real-time ticker information
- Fundamental data (EPS, P/E ratio, yield)
- Sparse data representation for efficiency
- In-memory caching with gap filling
- Pagination support

**Time Periods:**
| Period | Description |
|--------|-------------|
| 1m, 3m, 5m, 15m, 30m | Minute intervals |
| 1h, 3h, 6h, 12h | Hour intervals |
| 1d, 3d, 1w | Day/week intervals |

**Data Series:**
| Series | Description |
|--------|-------------|
| PRICE (1) | OHLCV price data |
| FUNDAMENTAL (2) | EPS, P/E ratio, yield |

**Quick Examples:**
```bash
# Get chart data
GET /aed/chart?symbol=BTCUSDC&series=1&period=1h&from=1735689600&to=1735776000

# Get tickers (base64 encoded symbols)
GET /aed/tickers?symbols=<base64_symbols_array>&series=2
OHLCV Fields:

Field	Description
OPEN (1)	Opening price
HIGH (2)	Highest price
LOW (3)	Lowest price
CLOSE (4)	Closing price
VOLUME (5)	Trading volume
Required Role: ORGANIZATION_ADMINISTRATOR
