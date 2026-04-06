# Holdings Service

The Holdings Service provides API interfaces for managing and tracking user holdings within an organization. It enables portfolio management, performance tracking, and historical analysis of asset positions.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Holdings Service │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ REST API Endpoints (Authenticated) │ │
│ ├───────────────┬───────────────┬─────────────────────────────────────┤ │
│ │ GET /holdings │ GET /holdings │ GET /holdings/graph │ │
│ │ /get │ /list │ (Portfolio Performance) │ │
│ │ (Single │ (Portfolio) │ │ │
│ │ Holding) │ │ │ │
│ └───────────────┴───────────────┴─────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Calculation Engine │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Real-time metric calculation │ │
│ │ • Portfolio aggregation │ │
│ │ • Historical performance analysis │ │
│ │ • Decimal precision for financial accuracy │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Data Sources │ │
│ ├───────────────┬───────────────┬───────────────┬─────────────────────┤ │
│ │ Holdings Store│ AED Store │ User Store │ Role Store │ │
│ │ (Cost basis, │ (Market │ (User auth) │ (Permissions) │ │
│ │ history) │ prices) │ │ │ │
│ │ Feature Flag │ Auth Firebase │ Organization │ Blockchain │ │
│ │ Store │ Service │ Store │ (Wallet balances) │ │
│ └───────────────┴───────────────┴───────────────┴─────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Role Requirements

| Endpoint | Required Role | Description |
|----------|---------------|-------------|
| GET /api/holdings/get | NORMAL_USER | Retrieve single holding by denom |
| GET /api/holdings/list | NORMAL_USER | Retrieve user's portfolio |
| GET /api/holdings/graph | NORMAL_USER | Retrieve portfolio performance over time |

**Note:** All authenticated requests must include:
- `Authorization` header (Bearer token from Firebase)
- `OrganizationID` header (organization UUID)
- `Network` header (mainnet, testnet, devnet)

## Data Models

### Holding Object

| Field | Type | Description |
|-------|------|-------------|
| UserID | string | User account identifier |
| OrganizationID | string | Organization UUID |
| MetaData | MetaData | Creation/update timestamps and network |
| Denom | string | Asset denomination (unique identifier) |
| Quantity | Decimal | Current quantity held |
| CostBasis | Decimal | Total cost basis of the holding |
| Metrics | Metrics | Calculated performance metrics |

### Metrics Object

| Field | Type | Description |
|-------|------|-------------|
| PortfolioPercentage | Decimal | Percentage of total portfolio value |
| CurrentValue | Decimal | Current market value (Quantity × CurrentPrice) |
| UnrealizedPnL | Decimal | Unrealized profit/loss (CurrentValue - CostBasis) |
| RealizedPnL | Decimal | Realized gains/losses from completed trades |
| AveragePrice | Decimal | Average price paid per unit (CostBasis ÷ Quantity) |
| CurrentPrice | Decimal | Latest market price from AED service |

### Portfolio Object

| Field | Type | Description |
|-------|------|-------------|
| UserID | string | User account identifier |
| OrganizationID | string | Organization UUID |
| Network | int | Network (1=mainnet, 2=testnet, 3=devnet) |
| Holdings | []Holding | List of user's holdings |
| TotalMarketValue | Decimal | Sum of all CurrentValue |
| TotalCostBasis | Decimal | Sum of all CostBasis |
| TotalUnrealizedPL | Decimal | Total unrealized profit/loss |
| TotalRealizedPL | Decimal | Total realized profit/loss |

### Decimal Object

| Field | Type | Description |
|-------|------|-------------|
| Value | int64 | Scaled integer value |
| Exp | int32 | Exponent (negative for decimal places) |

**Example:** `{"Value": 92642, "Exp": -2}` = 926.42

### MetaData Object

| Field | Type | Description |
|-------|------|-------------|
| Network | int | Network identifier |
| CreatedAt | Timestamp | Creation timestamp |
| UpdatedAt | Timestamp | Last update timestamp |

### Timestamp Object

| Field | Type | Description |
|-------|------|-------------|
| seconds | int64 | Unix timestamp in seconds |
| nanos | int32 | Nanoseconds offset |

### Period Object (Graph)

| Field | Type | Description |
|-------|------|-------------|
| Type | int | Period type (3=daily, 4=weekly, 5=hourly) |
| Duration | int | Number of period units |

### AED Value Object (Graph)

| Field | Type | Description |
|-------|------|-------------|
| Field | int | Value field type (4=CLOSE) |
| Float64Val | float64 | Floating point value |

### Series Types

| Series ID | Series Name | Description | Minimum Window |
|-----------|-------------|-------------|----------------|
| 1 | ASSET_PERFORMANCE | Individual asset performance | 1 month |
| 2 | INTERNAL_TRADES | Internal trade data (crypto) | 1 day |
| 3 | USER_PERFORMANCE | User portfolio performance | 1 month |

### Window Options by Series

#### USER_PERFORMANCE (Series 3)

| Window | Description | Bucket Type | Max Data Points |
|--------|-------------|-------------|-----------------|
| 1mo | Last month | Daily | ~30 |
| 3mo | Last 3 months | Daily | ~90 |
| 6mo | Last 6 months | Daily | ~180 |
| 1y | Last year | Daily | ~365 |
| ytd | Year to date (Jan 1 to today) | Daily | ~365 |
| all | All available data (up to 10 years) | Weekly | ~520 |

#### INTERNAL_TRADES (Series 2)

| Window | Description | Bucket Type | Max Data Points |
|--------|-------------|-------------|-----------------|
| 1d | Last 24 hours | Hourly | 24 |
| 1w | Last 7 days | Daily | 7 |
| 1mo | Last month | Daily | ~30 |
| 3mo | Last 3 months | Daily | ~90 |
| 6mo | Last 6 months | Daily | ~180 |
| 1y | Last year | Daily | ~365 |

### Period Types

| Type ID | Period Type | Description |
|---------|-------------|-------------|
| 3 | DAILY | Daily buckets (start of day) |
| 4 | WEEKLY | Weekly buckets (start of week - Monday) |
| 5 | HOURLY | Hourly buckets (for crypto trades) |

### Field Values (AED)

| Field ID | Field Name | Description |
|----------|------------|-------------|
| 4 | CLOSE | Closing value (portfolio value at period end) |

## API Endpoints

### GET /api/holdings/get

Retrieves a single holding for a user and denomination.

#### Headers

| Header | Description | Required |
|--------|-------------|----------|
| Authorization | Bearer <firebase_token> | Yes |
| OrganizationID | Organization UUID | Yes |
| Network | mainnet, testnet, devnet | Yes |

#### Query Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| denom | string | Asset denomination identifier | Yes |

#### Example Request

```bash
curl -X GET \
  "https://api.sologenic.org/api/holdings/get?denom=suaapl_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "UserID": "nick.luong@sologenic.org",
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "MetaData": {
    "Network": 2,
    "UpdatedAt": {
      "seconds": 1752596311,
      "nanos": 246733436
    },
    "CreatedAt": {
      "seconds": 1751895150,
      "nanos": 539847111
    }
  },
  "Denom": "suaapl_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
  "Quantity": {
    "Value": 5,
    "Exp": 0
  },
  "CostBasis": {
    "Value": 92642,
    "Exp": -2
  },
  "Metrics": {
    "PortfolioPercentage": {
      "Value": 17,
      "Exp": -2
    },
    "CurrentValue": {
      "Value": 94080,
      "Exp": -2
    },
    "UnrealizedPnL": {
      "Value": 1438,
      "Exp": -2
    },
    "RealizedPnL": {
      "Value": -960,
      "Exp": -2
    },
    "AveragePrice": {
      "Value": 1852840,
      "Exp": -4
    },
    "CurrentPrice": {
      "Value": 18816,
      "Exp": -2
    }
  }
}
GET /api/holdings/list
Retrieves a list of holdings for a user, representing their complete portfolio.

Headers
Header	Description	Required
Authorization	Bearer <firebase_token>	Yes
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Query Parameters
None.

Example Request
bash
curl -X GET \
  "https://api.sologenic.org/api/holdings/list" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "UserID": "nick.luong@sologenic.org",
  "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
  "Network": 2,
  "Holdings": [
    {
      "UserID": "nick.luong@sologenic.org",
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "MetaData": {
        "Network": 2,
        "UpdatedAt": {
          "seconds": 1752614489,
          "nanos": 504990000
        },
        "CreatedAt": {
          "seconds": 1752614489,
          "nanos": 505001000
        }
      },
      "Denom": "suusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
      "Quantity": {
        "Value": 1,
        "Exp": 3
      },
      "CostBasis": {
        "Value": 1,
        "Exp": 3
      },
      "Metrics": {
        "PortfolioPercentage": {
          "Value": 18,
          "Exp": -2
        },
        "CurrentValue": {
          "Value": 1,
          "Exp": 3
        },
        "UnrealizedPnL": {
          "Exp": 3
        },
        "RealizedPnL": {},
        "AveragePrice": {
          "Value": 10000,
          "Exp": -4
        },
        "CurrentPrice": {
          "Value": 1
        }
      }
    }
  ],
  "TotalMarketValue": {
    "Value": 569590,
    "Exp": -2
  },
  "TotalCostBasis": {
    "Value": 575530,
    "Exp": -2
  },
  "TotalUnrealizedPL": {
    "Value": -5940,
    "Exp": -2
  },
  "TotalRealizedPL": {
    "Value": -6648,
    "Exp": -2
  }
}
GET /api/holdings/graph
Retrieves portfolio performance over time as Asset Epoch Data (AEDs). Returns the user's total portfolio value calculated at regular time intervals over a specified date range.

Headers
Header	Description	Required
Authorization	Bearer <firebase_token>	Yes
OrganizationID	Organization UUID	Yes
Network	mainnet, testnet, devnet	Yes
Query Parameters
Parameter	Type	Description	Required	Default
window	string	Time range (1d, 1w, 1mo, 3mo, 6mo, 1y, ytd, all)	Yes	-
series	int	Data series type (1, 2, or 3)	No	3 (USER_PERFORMANCE)
Example Request
bash
curl -X GET \
  "https://api.sologenic.org/api/holdings/graph?window=1mo&series=3" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: mainnet"
Example Response
json
{
  "Portfolio": [
    {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Symbol": "suwusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28:nick.luong@sologenic.org_72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Timestamp": {
        "seconds": 1750464000
      },
      "Period": {
        "Type": 3,
        "Duration": 1
      },
      "MetaData": {
        "Network": 2
      },
      "Value": [
        {
          "Field": 4,
          "Float64Val": 2000
        }
      ]
    },
    {
      "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Symbol": "suwusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28:nick.luong@sologenic.org_72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
      "Timestamp": {
        "seconds": 1750550400
      },
      "Period": {
        "Type": 3,
        "Duration": 1
      },
      "MetaData": {
        "Network": 2
      },
      "Value": [
        {
          "Field": 4,
          "Float64Val": 2000
        }
      ]
    }
  ],
  "Denoms": {
    "suaapl_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28": [
      {
        "OrganizationID": "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
        "Symbol": "suwusdc_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28:suaapl_1-testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
        "Timestamp": {
          "seconds": 1750636800
        },
        "Period": {
          "Type": 3,
          "Duration": 1
        },
        "MetaData": {
          "Network": 2
        },
        "Value": [
          {
            "Field": 4,
            "Float64Val": 69305.8811425729
          }
        ]
      }
    ]
  }
}
Calculation Logic
Data Flow Diagram
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Holding Calculation Flow                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Get Wallet Assets (Blockchain)                                    │   │
│  │    • Fetch current quantities for user's address                     │   │
│  │    • Output: asset_quantities map                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 2. Get Stored Data (Holdings Store)                                  │   │
│  │    • Retrieve cost basis for each asset                              │   │
│  │    • Retrieve realized P&L history                                   │   │
│  │    • Output: cost_basis_map, realized_pl_map                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 3. Get Market Prices (AED Store)                                     │   │
│  │    • Fetch latest closing prices for each asset                      │   │
│  │    • Output: current_price_map                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 4. Calculate Per-Holding Metrics                                     │   │
│  │    For each asset:                                                   │   │
│  │      CurrentValue = Quantity × CurrentPrice                         │   │
│  │      TotalReturn = CurrentValue - CostBasis                         │   │
│  │      AveragePrice = CostBasis ÷ Quantity                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ 5. Calculate Portfolio Totals                                        │   │
│  │    TotalMarketValue = Σ CurrentValue                                │   │
│  │    PortfolioPercentage = CurrentValue ÷ TotalMarketValue            │   │
│  │    TotalUnrealizedPL = Σ (CurrentValue - CostBasis)                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Holding-Level Calculations
Metric	Formula	Data Source
Quantity	blockchain_balance	Blockchain wallet
CostBasis	stored_cost_basis	Holdings Store
CurrentPrice	aed.close	AED Store (latest)
CurrentValue	Quantity × CurrentPrice	Calculated
TotalReturn (Unrealized P&L)	CurrentValue - CostBasis	Calculated
AveragePrice	CostBasis ÷ Quantity	Calculated
Portfolio-Level Calculations
Metric	Formula
TotalMarketValue	Σ(holding.CurrentValue)
TotalCostBasis	Σ(holding.CostBasis)
TotalUnrealizedPL	TotalMarketValue - TotalCostBasis
PortfolioPercentage	holding.CurrentValue ÷ TotalMarketValue × 100
Graph Calculation Flow
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Graph Endpoint Calculation Flow                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Request: GET /holdings/graph?window=1mo&series=3                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ 1. Get Current Holdings                                      │    │   │
│  │  │    • Fetch user's current asset holdings                     │    │   │
│  │  │    • Determine which assets to track historically            │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                          │                                          │   │
│  │                          ▼                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ 2. Generate Time Buckets                                     │    │   │
│  │  │    • Based on window parameter (1mo = daily buckets)         │    │   │
│  │  │    • Create timestamps for each period                       │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                          │                                          │   │
│  │                          ▼                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ 3. Fetch Historical Prices                                   │    │   │
│  │  │    • For each asset in holdings                              │    │   │
│  │  │    • Get closing prices for each time bucket                 │    │   │
│  │  │    • From AED Store                                          │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                          │                                          │   │
│  │                          ▼                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ 4. Calculate Portfolio Value Per Bucket                      │    │   │
│  │  │    For each time bucket:                                     │    │   │
│  │  │      portfolio_value = Σ (quantity × historical_price)       │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                          │                                          │   │
│  │                          ▼                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │ 5. Create AEDs                                               │    │   │
│  │  │    • One AED per time bucket                                 │    │   │
│  │  │    • Value = portfolio_value at period start                 │    │   │
│  │  │    • Field = CLOSE (4)                                       │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
Time Bucketing Strategy
Daily Buckets (1w, 1mo, 3mo, 6mo, 1y, ytd)
text
Timeline: 2024-01-01 to 2024-01-31 (1 month)
┌─────────────────────────────────────────────────────────────────────────────┐
│ Day 1    Day 2    Day 3    ...    Day 30   Day 31                          │
│  │        │        │              │        │                               │
│  ▼        ▼        ▼              ▼        ▼                               │
│ AED     AED      AED            AED      AED                               │
│(Jan 1) (Jan 2)  (Jan 3)       (Jan 30) (Jan 31)                           │
│                                                                             │
│ Each AED represents portfolio value at START of that day                   │
│ Price used: Previous day's closing price (or same day if available)        │
└─────────────────────────────────────────────────────────────────────────────┘
Weekly Buckets (all - 10 years)
text
Timeline: Weekly intervals starting Monday
┌─────────────────────────────────────────────────────────────────────────────┐
│ Week 1   Week 2   Week 3   ...    Week 520                                 │
│  │        │        │              │                                        │
│  ▼        ▼        ▼              ▼                                        │
│ AED     AED      AED            AED                                        │
│(Mon)    (Mon)    (Mon)         (Mon)                                       │
│                                                                             │
│ Each AED represents portfolio value at START of that week                  │
│ Price used: Previous week's closing price                                  │
└─────────────────────────────────────────────────────────────────────────────┘
Hourly Buckets (1d - crypto)
text
Timeline: Last 24 hours
┌─────────────────────────────────────────────────────────────────────────────┐
│ Hour 1  Hour 2  Hour 3  ...    Hour 24                                     │
│   │       │       │              │                                          │
│   ▼       ▼       ▼              ▼                                          │
│  AED     AED     AED            AED                                        │
│(Hour 1) (Hour 2) (Hour 3)     (Hour 24)                                   │
│                                                                             │
│ Each AED represents portfolio value at START of that hour                  │
│ Price used: Previous hour's closing price                                  │
└─────────────────────────────────────────────────────────────────────────────┘
Decimal Precision
Precision by Field
Field	Typical Precision	Example	Decimal Places
Quantity	Asset-specific	5.123456	6
Price	4 decimal places	188.1600	4
Value	2 decimal places	940.80	2
Percentage	2 decimal places	17.25%	2
P&L	2 decimal places	14.38	2
Decimal Representation
json
{
  "Value": 92642,  // Scaled integer
  "Exp": -2        // 2 decimal places → 926.42
}
Conversion:

text
Actual Value = Value × 10^Exp

Example: 92642 × 10^-2 = 926.42
Integration Examples
React Portfolio Component
jsx
import React, { useState, useEffect } from 'react';

function Portfolio() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const fetchPortfolio = async () => {
    try {
      const response = await fetch('/api/holdings/list', {
        headers: {
          'Authorization': `Bearer: ${localStorage.getItem('token')}`,
          'OrganizationID': localStorage.getItem('orgId'),
          'Network': 'mainnet'
        }
      });

      if (!response.ok) throw new Error('Failed to fetch portfolio');

      const data = await response.json();
      setPortfolio(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatDecimal = (decimal) => {
    if (!decimal) return '0.00';
    const value = decimal.Value * Math.pow(10, decimal.Exp || 0);
    return value.toFixed(2);
  };

  const formatPercentage = (decimal) => {
    if (!decimal) return '0.00%';
    const value = decimal.Value * Math.pow(10, decimal.Exp || 0);
    return `${value.toFixed(2)}%`;
  };

  if (loading) return <div>Loading portfolio...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!portfolio) return null;

  return (
    <div className="portfolio">
      <h2>Your Portfolio</h2>
      
      <div className="portfolio-summary">
        <div className="summary-card">
          <h3>Total Value</h3>
          <p>${formatDecimal(portfolio.TotalMarketValue)}</p>
        </div>
        <div className="summary-card">
          <h3>Total Return</h3>
          <p className={portfolio.TotalUnrealizedPL.Value >= 0 ? 'positive' : 'negative'}>
            ${formatDecimal(portfolio.TotalUnrealizedPL)}
          </p>
        </div>
        <div className="summary-card">
          <h3>Realized P&L</h3>
          <p className={portfolio.TotalRealizedPL.Value >= 0 ? 'positive' : 'negative'}>
            ${formatDecimal(portfolio.TotalRealizedPL)}
          </p>
        </div>
      </div>

      <div className="holdings-table">
        <table>
          <thead>
            <tr>
              <th>Asset</th>
              <th>Quantity</th>
              <th>Avg Price</th>
              <th>Current Price</th>
              <th>Value</th>
              <th>Return</th>
              <th>Allocation</th>
            </tr>
          </thead>
          <tbody>
            {portfolio.Holdings.map((holding) => (
              <tr key={holding.Denom}>
                <td>{holding.Denom.split('_')[0]}</td>
                <td>{formatDecimal(holding.Quantity)}</td>
                <td>${formatDecimal(holding.Metrics.AveragePrice)}</td>
                <td>${formatDecimal(holding.Metrics.CurrentPrice)}</td>
                <td>${formatDecimal(holding.Metrics.CurrentValue)}</td>
                <td className={holding.Metrics.UnrealizedPnL.Value >= 0 ? 'positive' : 'negative'}>
                  ${formatDecimal(holding.Metrics.UnrealizedPnL)}
                </td>
                <td>{formatPercentage(holding.Metrics.PortfolioPercentage)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Portfolio;
React Portfolio Chart Component
jsx
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

function PortfolioPerformanceChart({ window: timeWindow = '1mo' }) {
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPerformanceData();
  }, [timeWindow]);

  const fetchPerformanceData = async () => {
    try {
      const response = await fetch(
        `/api/holdings/graph?window=${timeWindow}&series=3`,
        {
          headers: {
            'Authorization': `Bearer: ${localStorage.getItem('token')}`,
            'OrganizationID': localStorage.getItem('orgId'),
            'Network': 'mainnet'
          }
        }
      );

      if (!response.ok) throw new Error('Failed to fetch performance data');

      const data = await response.json();
      
      // Transform AED data for charting
      const chartData = {
        labels: data.Portfolio.map(aed => 
          new Date(aed.Timestamp.seconds * 1000).toLocaleDateString()
        ),
        datasets: [
          {
            label: 'Portfolio Value',
            data: data.Portfolio.map(aed => aed.Value[0].Float64Val),
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
            tension: 0.4
          }
        ]
      };

      setPerformanceData(chartData);
    } catch (err) {
      console.error('Error fetching performance data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getWindowLabel = () => {
    const windows = {
      '1mo': '1 Month',
      '3mo': '3 Months',
      '6mo': '6 Months',
      '1y': '1 Year',
      'ytd': 'Year to Date',
      'all': 'All Time'
    };
    return windows[timeWindow] || timeWindow;
  };

  if (loading) return <div>Loading chart...</div>;
  if (!performanceData) return null;

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `Portfolio Performance (${getWindowLabel()})`
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            let label = context.dataset.label || '';
            if (label) label += ': ';
            label += `$${context.raw.toFixed(2)}`;
            return label;
          }
        }
      }
    },
    scales: {
      y: {
        ticks: {
          callback: (value) => `$${value.toFixed(2)}`
        }
      }
    }
  };

  return (
    <div className="portfolio-chart">
      <Line data={performanceData} options={options} />
    </div>
  );
}

export default PortfolioPerformanceChart;
Node.js Holdings Client
javascript
class HoldingsServiceClient {
  constructor(baseUrl, token, orgId, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.token = token;
    this.orgId = orgId;
    this.network = network;
  }

  async getHolding(denom) {
    const response = await fetch(
      `${this.baseUrl}/api/holdings/get?denom=${encodeURIComponent(denom)}`,
      {
        headers: this._getHeaders()
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch holding: ${response.statusText}`);
    }

    return response.json();
  }

  async getPortfolio() {
    const response = await fetch(
      `${this.baseUrl}/api/holdings/list`,
      {
        headers: this._getHeaders()
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch portfolio: ${response.statusText}`);
    }

    return response.json();
  }

  async getPerformanceGraph(window, series = 3) {
    const response = await fetch(
      `${this.baseUrl}/api/holdings/graph?window=${window}&series=${series}`,
      {
        headers: this._getHeaders()
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch performance graph: ${response.statusText}`);
    }

    return response.json
  }

  // Utility method to format decimal values
  formatDecimal(decimal) {
    if (!decimal) return 0;
    return decimal.Value * Math.pow(10, decimal.Exp || 0);
  }

  // Get total portfolio value in base currency
  async getTotalPortfolioValue() {
    const portfolio = await this.getPortfolio();
    return this.formatDecimal(portfolio.TotalMarketValue);
  }

  // Get asset allocation percentages
  async getAssetAllocation() {
    const portfolio = await this.getPortfolio();
    
    const allocation = portfolio.Holdings.map(holding => ({
      denom: holding.Denom,
      percentage: this.formatDecimal(holding.Metrics.PortfolioPercentage),
      value: this.formatDecimal(holding.Metrics.CurrentValue)
    }));
    
    // Sort by percentage descending
    allocation.sort((a, b) => b.percentage - a.percentage);
    
    return allocation;
  }

  // Calculate portfolio return percentage
  async getPortfolioReturnPercentage() {
    const portfolio = await this.getPortfolio();
    const totalValue = this.formatDecimal(portfolio.TotalMarketValue);
    const totalCost = this.formatDecimal(portfolio.TotalCostBasis);
    
    if (totalCost === 0) return 0;
    return ((totalValue - totalCost) / totalCost) * 100;
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
async function main() {
  const client = new HoldingsServiceClient(
    'https://api.sologenic.org',
    'firebase-token',
    'org-uuid',
    'mainnet'
  );

  // Get full portfolio
  const portfolio = await client.getPortfolio();
  console.log('Total Portfolio Value:', client.formatDecimal(portfolio.TotalMarketValue));
  
  // Get asset allocation
  const allocation = await client.getAssetAllocation();
  console.log('Asset Allocation:', allocation);
  
  // Get portfolio return
  const returnPercent = await client.getPortfolioReturnPercentage();
  console.log('Portfolio Return:', returnPercent.toFixed(2), '%');
  
  // Get performance graph data
  const performance = await client.getPerformanceGraph('1mo', 3);
  console.log('Performance Data Points:', performance.Portfolio.length);
}

main();
Python Holdings Client
python
import requests
from typing import Optional, Dict, List
from decimal import Decimal

class HoldingsServiceClient:
    def __init__(self, base_url: str, token: str, org_id: str, network: str = 'mainnet'):
        self.base_url = base_url
        self.token = token
        self.org_id = org_id
        self.network = network
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer: {self.token}',
            'OrganizationID': self.org_id,
            'Network': self.network
        }
    
    def _format_decimal(self, decimal_dict: Dict) -> Decimal:
        """Convert decimal dictionary to Decimal object"""
        if not decimal_dict:
            return Decimal(0)
        value = decimal_dict.get('Value', 0)
        exp = decimal_dict.get('Exp', 0)
        return Decimal(value) * Decimal(10) ** Decimal(exp)
    
    def get_holding(self, denom: str) -> Dict:
        """Get a single holding by denom"""
        response = requests.get(
            f'{self.base_url}/api/holdings/get',
            params={'denom': denom},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_portfolio(self) -> Dict:
        """Get user's complete portfolio"""
        response = requests.get(
            f'{self.base_url}/api/holdings/list',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_performance_graph(self, window: str, series: int = 3) -> Dict:
        """Get portfolio performance over time"""
        response = requests.get(
            f'{self.base_url}/api/holdings/graph',
            params={'window': window, 'series': series},
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_total_value(self) -> Decimal:
        """Get total portfolio value"""
        portfolio = self.get_portfolio()
        return self._format_decimal(portfolio.get('TotalMarketValue'))
    
    def get_asset_allocation(self) -> List[Dict]:
        """Get asset allocation percentages"""
        portfolio = self.get_portfolio()
        allocation = []
        
        for holding in portfolio.get('Holdings', []):
            allocation.append({
                'denom': holding.get('Denom'),
                'percentage': self._format_decimal(holding.get('Metrics', {}).get('PortfolioPercentage')),
                'value': self._format_decimal(holding.get('Metrics', {}).get('CurrentValue')),
                'quantity': self._format_decimal(holding.get('Quantity'))
            })
        
        # Sort by percentage descending
        allocation.sort(key=lambda x: x['percentage'], reverse=True)
        return allocation
    
    def get_portfolio_return(self) -> Dict:
        """Get portfolio return metrics"""
        portfolio = self.get_portfolio()
        total_value = self._format_decimal(portfolio.get('TotalMarketValue'))
        total_cost = self._format_decimal(portfolio.get('TotalCostBasis'))
        
        unrealized_pl = self._format_decimal(portfolio.get('TotalUnrealizedPL'))
        realized_pl = self._format_decimal(portfolio.get('TotalRealizedPL'))
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'unrealized_pl': unrealized_pl,
            'realized_pl': realized_pl,
            'total_return': unrealized_pl + realized_pl,
            'return_percentage': ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
        }

# Usage
client = HoldingsServiceClient(
    base_url='https://api.sologenic.org',
    token='firebase-token',
    org_id='org-uuid',
    network='mainnet'
)

# Get portfolio
portfolio = client.get_portfolio()
print(f"Total Portfolio Value: ${client.get_total_value():,.2f}")

# Get allocation
allocation = client.get_asset_allocation()
for asset in allocation[:5]:  # Top 5 holdings
    print(f"{asset['denom']}: {asset['percentage']:.2f}% (${asset['value']:,.2f})")

# Get return metrics
returns = client.get_portfolio_return()
print(f"Total Return: ${returns['total_return']:,.2f} ({returns['return_percentage']:.2f}%)")

# Get performance data
performance = client.get_performance_graph('1mo')
print(f"Performance Data Points: {len(performance.get('Portfolio', []))}")
Use Cases
Portfolio Dashboard
javascript
// Display portfolio summary with real-time data
async function renderPortfolioDashboard() {
  const portfolio = await holdingsClient.getPortfolio();
  
  return {
    totalValue: formatDecimal(portfolio.TotalMarketValue),
    dailyChange: calculateDailyChange(portfolio.Holdings),
    topPerformers: getTopPerformers(portfolio.Holdings, 5),
    assetAllocation: calculateAssetAllocation(portfolio.Holdings),
    returnsYTD: calculateYTDReturns(portfolio.Holdings)
  };
}
Performance Analytics
javascript
// Calculate portfolio performance metrics
async function calculatePerformanceMetrics() {
  const performance = await holdingsClient.getPerformanceGraph('1y');
  const values = performance.Portfolio.map(p => p.Value[0].Float64Val);
  
  return {
    startValue: values[0],
    endValue: values[values.length - 1],
    totalReturn: ((values[values.length - 1] - values[0]) / values[0]) * 100,
    maxDrawdown: calculateMaxDrawdown(values),
    volatility: calculateStandardDeviation(values),
    sharpeRatio: calculateSharpeRatio(values)
  };
}
Risk Assessment
javascript
// Analyze portfolio risk based on holdings
async function assessPortfolioRisk() {
  const portfolio = await holdingsClient.getPortfolio();
  const allocation = await holdingsClient.getAssetAllocation();
  
  return {
    concentrationRisk: allocation[0]?.percentage > 40 ? 'High' : 'Moderate',
    diversificationScore: calculateDiversification(allocation),
    volatilityExposure: calculateVolatilityExposure(portfolio.Holdings),
    recommendedRebalance: generateRebalanceRecommendations(allocation)
  };
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	com-be-http-lib
AED_STORE	Asset Exchange Details service endpoint	com-fs-aed-model
HOLDINGS_STORE	Holdings service endpoint	com-fs-holdings-model
USER_STORE	User service endpoint	com-fs-user-model
ROLE_STORE	Role service endpoint	com-fs-role-model
FEATURE_FLAG_STORE	Feature flag service endpoint	com-fs-feature-flag-model
AUTH_FIREBASE_SERVICE	Firebase authentication service	com-fs-auth-firebase-model
ORGANIZATION_STORE	Organization service endpoint	com-fs-admin-organization-model
BASE_CURRENCY	Base currency for values (e.g., USD)	Configuration
Example Environment Configuration
bash
# Required
AED_STORE=localhost:50057
HOLDINGS_STORE=localhost:50058
USER_STORE=localhost:50049
ROLE_STORE=localhost:50066
FEATURE_FLAG_STORE=localhost:50055
AUTH_FIREBASE_SERVICE=localhost:50070
ORGANIZATION_STORE=localhost:50060
BASE_CURRENCY=USD

# Optional
LOG_LEVEL=info
CACHE_TTL_SECONDS=60
MAX_HOLDINGS_PER_USER=1000

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
  holdings-service:
    image: sologenic/holdings-service:latest
    environment:
      - AED_STORE=aed-store:50057
      - HOLDINGS_STORE=holdings-store:50058
      - USER_STORE=user-service:50049
      - ROLE_STORE=role-store:50066
      - FEATURE_FLAG_STORE=feature-flag-store:50055
      - AUTH_FIREBASE_SERVICE=auth-service:50070
      - ORGANIZATION_STORE=organization-service:50060
      - BASE_CURRENCY=USD
      - LOG_LEVEL=info
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
    networks:
      - internal

  holdings-store:
    image: sologenic/holdings-store:latest
    environment:
      - DATABASE_URL=postgres://user:pass@postgres:5432/holdings
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Responses
Not Found (404)
json
{
  "error": "Not Found",
  "message": "Holding not found for denom: suaapl_1-testcore..."
}
Bad Request (400)
json
{
  "error": "Bad Request",
  "message": "Invalid window parameter",
  "valid_values": ["1d", "1w", "1mo", "3mo", "6mo", "1y", "ytd", "all"]
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
  "message": "Access denied for organization"
}
Internal Server Error (500)
json
{
  "error": "Internal Server Error",
  "message": "Failed to calculate portfolio metrics",
  "request_id": "req_12345"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Empty holdings list	No assets in wallet	User has no holdings
Missing prices	AED data unavailable	Check AED service connectivity
Stale data	Cache not refreshed	Reduce cache TTL or force refresh
Decimal precision errors	Incorrect Exp value	Verify decimal formatting
Graph returns empty	No historical data	Ensure window has sufficient data
Portfolio percentage mismatch	Calculation timing	Holdings may be from different timestamps
Debugging Commands
bash
# Enable debug logging
LOG_LEVEL=debug

# Test single holding endpoint
curl -X GET "https://api.sologenic.org/api/holdings/get?denom=test_denom" \
  -H "Authorization: Bearer: $TOKEN" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v

# Test portfolio endpoint
curl -X GET "https://api.sologenic.org/api/holdings/list" \
  -H "Authorization: Bearer: $TOKEN" \
  -H "OrganizationID: $ORG_ID" \
  -H "Network: mainnet" \
  -v

# Test graph endpoint with different windows
for window in 1mo 3mo 1y all; do
  echo "Testing window: $window"
  curl -X GET "https://api.sologenic.org/api/holdings/graph?window=$window&series=3" \
    -H "Authorization: Bearer: $TOKEN" \
    -H "OrganizationID: $ORG_ID" \
    -H "Network: mainnet" \
    -s | jq '.Portfolio | length'
done
Best Practices
Performance
Practice	Recommendation
Caching	Cache portfolio data for 60 seconds
Pagination	Implement for large holdings lists
Batch requests	Fetch all holdings at once, not individually
Graph optimization	Use appropriate window sizes (avoid 'all' for dashboards)
Data Accuracy
Practice	Recommendation
Decimal precision	Always use Decimal for financial calculations
Real-time prices	Fetch latest prices on each request
Cost basis	Update after each trade
Reconciliation	Regularly reconcile with blockchain
Security
Practice	Recommendation
Authorization	Verify user owns the requested holdings
Rate limiting	Implement per-user rate limits
Data isolation	Enforce organization-level isolation
Related Services
Service	Description
AED Store	Market price data
User Store	User authentication and profiles
Role Store	Permission management
Organization Store	Tenant isolation
Trade Service	Trade execution and cost basis updates
License
This documentation is part of the TX Marketplace platform.
