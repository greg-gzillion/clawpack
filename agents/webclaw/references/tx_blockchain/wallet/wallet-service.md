# Wallet Service

The Wallet Service provides API interfaces that allow users to calculate available funds and determine buying power based on on-chain assets and future brokerage integration.

## Key Terminology

| Term | Description | Source |
|------|-------------|--------|
| On-chain funds | On-chain cash (e.g., wrapped Fiat-WUSD) in the user's wallet | Blockchain (on-chain) |
| Brokerage Funds | Off-chain cash held in the user's brokerage account (off-chain) | Brokerage (future) |
| Buying Power | Total purchasing capacity, combining on-chain assets (with margin) and brokerage funds (with multiplier) | Hybrid (on-chain + off-chain) |
| Asset Margin Percentage | The collateral value percentage of an asset (e.g., 50% → 10,000 BTC → 5,000 buying power contribution) | Asset |
| User Multiplier | User profile-based multiplier for brokerage funds (based on risk profile, trading history) | User.TradeProfile |

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Wallet Service Architecture │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ GET /api/user/funds │ │
│ │ GET /api/user/buying-power │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Wallet Service Core │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Fund Calculation Engine │ │
│ │ • Buying Power Aggregator │ │
│ │ • Collateral Valuation │ │
│ │ • Margin Calculator │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ┌───────────────────────────┼───────────────────────────┐ │
│ ▼ ▼ ▼ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ On-chain │ │ Brokerage │ │ Asset │ │
│ │ Wallet │ │ (Future) │ │ Store │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## API Endpoints Overview

### Authenticated Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/funds` | Returns available funds (stablecoins) for a wallet address |
| GET | `/api/user/buying-power` | Returns buying power calculation for a wallet address |

### Authentication Requirements

All endpoints require:
- Valid Firebase JWT token in `Authorization` header (format: `Bearer: eyJhb....`)
- `OrganizationID` header for tenant isolation
- `Network` header (mainnet, testnet, devnet)

## API Endpoints Details

### GET /api/user/funds

Returns the available funds for a specific wallet address. This endpoint focuses on immediately available stablecoins that can be used for trading.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| address | string | Yes | Blockchain wallet address |

**Example Request:**

```bash
curl -X GET \
  "https://api.sologenic.org/api/user/funds?address=testcore15ms2zan4z3y9d29rxsyan5v5vecc04ycts2c85" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet"
Example Response:

json
[
  {
    "Denom": {
      "Currency": {
        "Symbol": "wusdc",
        "Version": "1"
      },
      "Subunit": "suwusdc_1",
      "Issuer": "testcore13s2mmgg4uu4fn8mue6s3lgn74jwdupndjtqah8uxufugtajkeq2qgznc28",
      "Precision": 2
    },
    "RawAmount": {
      "Value": 500000,
      "Exp": -2
    },
    "AssetMarginPercentage": 1
  }
]
Response Fields:

Field	Type	Description
Denom	object	Asset denomination details
Denom.Currency.Symbol	string	Currency symbol (e.g., "wusdc")
Denom.Currency.Version	string	Currency version
Denom.Subunit	string	Subunit denomination
Denom.Issuer	string	Asset issuer address
Denom.Precision	int	Decimal precision
RawAmount.Value	int64	Raw amount value
RawAmount.Exp	int	Exponent (10^exp multiplier)
AssetMarginPercentage	float	Collateral percentage (1 = 100%)
GET /api/user/buying-power
Returns the total buying power calculation for a specific wallet address, including all contributing factors.

Query Parameters:

Parameter	Type	Required	Description
address	string	Yes	Blockchain wallet address
Example Request:

bash
curl -X GET \
  "https://api.sologenic.org/api/user/buying-power?address=testcore15ms2zan4z3y9d29rxsyan5v5vecc04ycts2c85" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer: eyJhbGciOiJSUzI1NiIs..." \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -H "Network: testnet"
Example Response:

json
{
  "AvailableOnchainFund": {
    "Value": 5000
  },
  "Collateral": {
    "Value": 10719422298797452,
    "Exp": -13
  },
  "BrokerageFund": {},
  "Total": {
    "Value": 60719422298797452,
    "Exp": -13
  },
  "Currency": "wusdc"
}
Response Fields:

Field	Type	Description
AvailableOnchainFund	Amount	Immediately available stablecoins
Collateral	Amount	Value from other assets with margin applied
BrokerageFund	Amount	Off-chain brokerage funds (future)
Total	Amount	Total buying power
Currency	string	Currency denomination (e.g., "wusdc")
Amount Object:

Field	Type	Description
Value	int64	Amount value
Exp	int	Exponent (10^exp multiplier)
Calculation Logic
Available On-chain Funds
text
AvailableOnchainFund = Σ(Stablecoin_Balance × AssetMarginPercentage)

Where:
- Stablecoin_Balance: Balance of stablecoins in wallet
- AssetMarginPercentage: Collateral factor (1 = 100%)
Collateral Value
text
Collateral = Σ(Non_Stablecoin_Asset_Balance × Market_Price × AssetMarginPercentage)

Where:
- Non_Stablecoin_Asset_Balance: Balance of non-stablecoin assets
- Market_Price: Current market price of the asset
- AssetMarginPercentage: Collateral factor (0.5 = 50%)
Total Buying Power
text
Total = AvailableOnchainFund + Collateral + BrokerageFund

Where:
- AvailableOnchainFund: Immediate stablecoin funds
- Collateral: Value of other assets with margin
- BrokerageFund: Off-chain funds (with user multiplier)
Asset Margin Percentages
Asset Type	Margin Percentage	Description
Stablecoins	100% (1.0)	Full value usable
Major Cryptocurrencies	70-80%	BTC, ETH, etc.
Mid-cap Assets	50-60%	Moderate volatility
Small-cap Assets	30-40%	Higher volatility
Highly Volatile	10-20%	Extreme volatility
Illiquid Assets	0-10%	Low liquidity
Integration Examples
JavaScript/React Client
javascript
class WalletServiceClient {
  constructor(baseUrl, token = null, organizationId = null, network = 'mainnet') {
    this.baseUrl = baseUrl;
    this.token = token;
    this.organizationId = organizationId;
    this.network = network;
  }

  setAuth(token, organizationId) {
    this.token = token;
    this.organizationId = organizationId;
  }

  async getUserFunds(address) {
    const response = await fetch(
      `${this.baseUrl}/api/user/funds?address=${encodeURIComponent(address)}`,
      {
        headers: this._getAuthHeaders()
      }
    );
    
    if (!response.ok) {
      throw new Error(`Failed to fetch funds: ${response.status}`);
    }
    
    return response.json();
  }

  async getBuyingPower(address) {
    const response = await fetch(
      `${this.baseUrl}/api/user/buying-power?address=${encodeURIComponent(address)}`,
      {
        headers: this._getAuthHeaders()
      }
    );
    
    if (!response.ok) {
      throw new Error(`Failed to fetch buying power: ${response.status}`);
    }
    
    return response.json();
  }

  // Helper: Format amount from value and exponent
  static formatAmount(value, exp) {
    return value * Math.pow(10, exp);
  }

  // Helper: Get human-readable balance
  formatFunds(funds) {
    return funds.map(fund => ({
      symbol: fund.Denom.Currency.Symbol,
      amount: WalletServiceClient.formatAmount(
        fund.RawAmount.Value,
        fund.RawAmount.Exp
      ),
      marginPercentage: fund.AssetMarginPercentage,
      usableAmount: fund.RawAmount.Value * fund.AssetMarginPercentage * 
                    Math.pow(10, fund.RawAmount.Exp)
    }));
  }

  // Helper: Get formatted buying power
  formatBuyingPower(buyingPower) {
    const format = (amount) => {
      if (!amount.Value) return 0;
      return amount.Value * Math.pow(10, amount.Exp || 0);
    };

    return {
      availableOnchain: format(buyingPower.AvailableOnchainFund),
      collateral: format(buyingPower.Collateral),
      brokerage: format(buyingPower.BrokerageFund),
      total: format(buyingPower.Total),
      currency: buyingPower.Currency
    };
  }

  _getAuthHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer: ${this.token}`,
      'OrganizationID': this.organizationId,
      'Network': this.network
    };
  }
}

// React Component Example
function WalletDashboard({ walletAddress }) {
  const [funds, setFunds] = useState([]);
  const [buyingPower, setBuyingPower] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const client = new WalletServiceClient(
    'https://api.sologenic.org',
    localStorage.getItem('token'),
    localStorage.getItem('orgId'),
    'mainnet'
  );

  useEffect(() => {
    if (walletAddress) {
      loadWalletData();
    }
  }, [walletAddress]);

  async function loadWalletData() {
    setLoading(true);
    setError(null);
    
    try {
      const [fundsData, buyingPowerData] = await Promise.all([
        client.getUserFunds(walletAddress),
        client.getBuyingPower(walletAddress)
      ]);
      
      setFunds(client.formatFunds(fundsData));
      setBuyingPower(client.formatBuyingPower(buyingPowerData));
    } catch (err) {
      setError(err.message);
      console.error('Failed to load wallet data:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div className="loading">Loading wallet data...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="wallet-dashboard">
      <h2>Wallet Dashboard</h2>
      <p className="wallet-address">Address: {walletAddress}</p>

      {/* Buying Power Section */}
      {buyingPower && (
        <div className="buying-power-section">
          <h3>Total Buying Power</h3>
          <div className="buying-power-amount">
            {buyingPower.total.toFixed(2)} {buyingPower.currency.toUpperCase()}
          </div>
          
          <div className="buying-power-breakdown">
            <div className="breakdown-item">
              <span>Available On-chain:</span>
              <strong>{buyingPower.availableOnchain.toFixed(2)}</strong>
            </div>
            <div className="breakdown-item">
              <span>Collateral Value:</span>
              <strong>{buyingPower.collateral.toFixed(2)}</strong>
            </div>
            {buyingPower.brokerage > 0 && (
              <div className="breakdown-item">
                <span>Brokerage Funds:</span>
                <strong>{buyingPower.brokerage.toFixed(2)}</strong>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Funds Section */}
      <div className="funds-section">
        <h3>Available Funds</h3>
        <div className="funds-list">
          {funds.map((fund, idx) => (
            <div key={idx} className="fund-card">
              <div className="fund-header">
                <span className="fund-symbol">{fund.symbol.toUpperCase()}</span>
                <span className="fund-amount">{fund.amount.toFixed(4)}</span>
              </div>
              <div className="fund-details">
                <div className="detail-row">
                  <span>Usable Amount:</span>
                  <strong>{fund.usableAmount.toFixed(4)}</strong>
                </div>
                <div className="detail-row">
                  <span>Margin Percentage:</span>
                  <strong>{fund.marginPercentage * 100}%</strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Refresh Button */}
      <button onClick={loadWalletData} className="refresh-button">
        Refresh Data
      </button>
    </div>
  );
}

// Custom Hook for Wallet Data
function useWalletData(walletAddress) {
  const [data, setData] = useState({ funds: [], buyingPower: null, loading: true, error: null });
  
  const client = useMemo(() => new WalletServiceClient(
    'https://api.sologenic.org',
    localStorage.getItem('token'),
    localStorage.getItem('orgId'),
    'mainnet'
  ), []);

  useEffect(() => {
    if (!walletAddress) return;

    let mounted = true;

    async function fetchData() {
      try {
        const [fundsData, buyingPowerData] = await Promise.all([
          client.getUserFunds(walletAddress),
          client.getBuyingPower(walletAddress)
        ]);

        if (mounted) {
          setData({
            funds: client.formatFunds(fundsData),
            buyingPower: client.formatBuyingPower(buyingPowerData),
            loading: false,
            error: null
          });
        }
      } catch (error) {
        if (mounted) {
          setData(prev => ({
            ...prev,
            loading: false,
            error: error.message
          }));
        }
      }
    }

    fetchData();

    // Refresh every 30 seconds
    const interval = setInterval(fetchData, 30000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [walletAddress, client]);

  return data;
}

export { WalletServiceClient, WalletDashboard, useWalletData };
Python Client
python
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from decimal import Decimal
from enum import IntEnum

@dataclass
class Denom:
    symbol: str
    version: str
    subunit: str
    issuer: str
    precision: int

@dataclass
class RawAmount:
    value: int
    exp: int

    def to_decimal(self) -> Decimal:
        return Decimal(self.value) * Decimal(10) ** Decimal(self.exp)

@dataclass
class Fund:
    denom: Denom
    raw_amount: RawAmount
    asset_margin_percentage: float

    @property
    def amount(self) -> Decimal:
        return self.raw_amount.to_decimal()
    
    @property
    def usable_amount(self) -> Decimal:
        return self.amount * Decimal(self.asset_margin_percentage)

@dataclass
class BuyingPower:
    available_onchain: Optional[RawAmount]
    collateral: Optional[RawAmount]
    brokerage: Optional[RawAmount]
    total: RawAmount
    currency: str

    @property
    def total_decimal(self) -> Decimal:
        return self.total.to_decimal()
    
    @property
    def available_onchain_decimal(self) -> Decimal:
        return self.available_onchain.to_decimal() if self.available_onchain else Decimal(0)
    
    @property
    def collateral_decimal(self) -> Decimal:
        return self.collateral.to_decimal() if self.collateral else Decimal(0)
    
    @property
    def brokerage_decimal(self) -> Decimal:
        return self.brokerage.to_decimal() if self.brokerage else Decimal(0)

class WalletServiceClient:
    def __init__(self, base_url: str, token: Optional[str] = None,
                 organization_id: Optional[str] = None, network: str = 'mainnet'):
        self.base_url = base_url
        self.token = token
        self.organization_id = organization_id
        self.network = network
    
    def set_auth(self, token: str, organization_id: str):
        """Set authentication credentials"""
        self.token = token
        self.organization_id = organization_id
    
    def get_user_funds(self, address: str) -> List[Fund]:
        """Get available funds for a wallet address"""
        response = requests.get(
            f"{self.base_url}/api/user/funds",
            params={'address': address},
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        
        funds_data = response.json()
        return [self._parse_fund(fund) for fund in funds_data]
    
    def get_buying_power(self, address: str) -> BuyingPower:
        """Get buying power for a wallet address"""
        response = requests.get(
            f"{self.base_url}/api/user/buying-power",
            params={'address': address},
            headers=self._get_auth_headers()
        )
        response.raise_for_status()
        
        data = response.json()
        return self._parse_buying_power(data)
    
    def _parse_fund(self, data: Dict[str, Any]) -> Fund:
        denom_data = data['Denom']
        denom = Denom(
            symbol=denom_data['Currency']['Symbol'],
            version=denom_data['Currency']['Version'],
            subunit=denom_data['Subunit'],
            issuer=denom_data['Issuer'],
            precision=denom_data['Precision']
        )
        
        raw_amount = RawAmount(
            value=data['RawAmount']['Value'],
            exp=data['RawAmount']['Exp']
        )
        
        return Fund(
            denom=denom,
            raw_amount=raw_amount,
            asset_margin_percentage=data['AssetMarginPercentage']
        )
    
    def _parse_buying_power(self, data: Dict[str, Any]) -> BuyingPower:
        def parse_amount(amount_data):
            if not amount_data:
                return None
            return RawAmount(
                value=amount_data.get('Value', 0),
                exp=amount_data.get('Exp', 0)
            )
        
        return BuyingPower(
            available_onchain=parse_amount(data.get('AvailableOnchainFund')),
            collateral=parse_amount(data.get('Collateral')),
            brokerage=parse_amount(data.get('BrokerageFund')),
            total=parse_amount(data['Total']),
            currency=data['Currency']
        )
    
    def _get_auth_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer: {self.token}',
            'OrganizationID': self.organization_id,
            'Network': self.network
        }

# Usage Example
def main():
    client = WalletServiceClient(
        base_url='https://api.sologenic.org',
        network='mainnet'
    )
    
    # Set authentication
    client.set_auth(
        token='firebase-jwt-token',
        organization_id='72c4c072-2fe4-4f72-ae9d-d9d52a05fd71'
    )
    
    wallet_address = 'testcore15ms2zan4z3y9d29rxsyan5v5vecc04ycts2c85'
    
    # Get available funds
    funds = client.get_user_funds(wallet_address)
    print(f"Found {len(funds)} fund(s):")
    for fund in funds:
        print(f"  {fund.denom.symbol}: {fund.amount:.4f} "
              f"(usable: {fund.usable_amount:.4f}, "
              f"margin: {fund.asset_margin_percentage * 100}%)")
    
    # Get buying power
    buying_power = client.get_buying_power(wallet_address)
    print(f"\nBuying Power ({buying_power.currency.upper()}):")
    print(f"  Available On-chain: {buying_power.available_onchain_decimal:.4f}")
    print(f"  Collateral Value: {buying_power.collateral_decimal:.4f}")
    print(f"  Brokerage Funds: {buying_power.brokerage_decimal:.4f}")
    print(f"  TOTAL: {buying_power.total_decimal:.4f}")

# Run example
# main()
Go Client
go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "math"
    "net/http"
    "net/url"
    "strconv"
    "time"
)

type WalletServiceClient struct {
    baseURL        string
    token          string
    organizationID string
    network        string
    httpClient     *http.Client
}

type Denom struct {
    Currency  Currency `json:"Currency"`
    Subunit   string   `json:"Subunit"`
    Issuer    string   `json:"Issuer"`
    Precision int      `json:"Precision"`
}

type Currency struct {
    Symbol  string `json:"Symbol"`
    Version string `json:"Version"`
}

type RawAmount struct {
    Value int64 `json:"Value"`
    Exp   int   `json:"Exp"`
}

func (r *RawAmount) ToFloat64() float64 {
    return float64(r.Value) * math.Pow(10, float64(r.Exp))
}

type Fund struct {
    Denom                 Denom      `json:"Denom"`
    RawAmount             RawAmount  `json:"RawAmount"`
    AssetMarginPercentage float64    `json:"AssetMarginPercentage"`
}

func (f *Fund) GetAmount() float64 {
    return f.RawAmount.ToFloat64()
}

func (f *Fund) GetUsableAmount() float64 {
    return f.GetAmount() * f.AssetMarginPercentage
}

type BuyingPower struct {
    AvailableOnchain *RawAmount `json:"AvailableOnchainFund"`
    Collateral       *RawAmount `json:"Collateral"`
    BrokerageFund    *RawAmount `json:"BrokerageFund"`
    Total            RawAmount  `json:"Total"`
    Currency         string     `json:"Currency"`
}

func (b *BuyingPower) GetAvailableOnchain() float64 {
    if b.AvailableOnchain == nil {
        return 0
    }
    return b.AvailableOnchain.ToFloat64()
}

func (b *BuyingPower) GetCollateral() float64 {
    if b.Collateral == nil {
        return 0
    }
    return b.Collateral.ToFloat64()
}

func (b *BuyingPower) GetBrokerage() float64 {
    if b.BrokerageFund == nil {
        return 0
    }
    return b.BrokerageFund.ToFloat64()
}

func (b *BuyingPower) GetTotal() float64 {
    return b.Total.ToFloat64()
}

func NewWalletServiceClient(baseURL, network string) *WalletServiceClient {
    return &WalletServiceClient{
        baseURL:    baseURL,
        network:    network,
        httpClient: &http.Client{Timeout: 30 * time.Second},
    }
}

func (c *WalletServiceClient) SetAuth(token, organizationID string) {
    c.token = token
    c.organizationID = organizationID
}

func (c *WalletServiceClient) GetUserFunds(address string) ([]Fund, error) {
    params := url.Values{}
    params.Add("address", address)
    
    reqURL := fmt.Sprintf("%s/api/user/funds?%s", c.baseURL, params.Encode())
    
    req, err := http.NewRequest("GET", reqURL, nil)
    if err != nil {
        return nil, err
    }
    
    c.setAuthHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var funds []Fund
    if err := json.Unmarshal(body, &funds); err != nil {
        return nil, err
    }
    
    return funds, nil
}

func (c *WalletServiceClient) GetBuyingPower(address string) (*BuyingPower, error) {
    params := url.Values{}
    params.Add("address", address)
    
    reqURL := fmt.Sprintf("%s/api/user/buying-power?%s", c.baseURL, params.Encode())
    
    req, err := http.NewRequest("GET", reqURL, nil)
    if err != nil {
        return nil, err
    }
    
    c.setAuthHeaders(req)
    
    resp, err := c.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }
    
    var buyingPower BuyingPower
    if err := json.Unmarshal(body, &buyingPower); err != nil {
        return nil, err
    }
    
    return &buyingPower, nil
}

func (c *WalletServiceClient) setAuthHeaders(req *http.Request) {
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer: "+c.token)
    req.Header.Set("OrganizationID", c.organizationID)
    req.Header.Set("Network", c.network)
}

// Usage Example
func main() {
    client := NewWalletServiceClient("https://api.sologenic.org", "mainnet")
    
    // Set authentication
    client.SetAuth(
        "firebase-jwt-token",
        "72c4c072-2fe4-4f72-ae9d-d9d52a05fd71",
    )
    
    walletAddress := "testcore15ms2zan4z3y9d29rxsyan5v5vecc04ycts2c85"
    
    // Get funds
    funds, err := client.GetUserFunds(walletAddress)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Found %d fund(s):\n", len(funds))
    for _, fund := range funds {
        fmt.Printf("  %s: %.4f (usable: %.4f, margin: %.0f%%)\n",
            fund.Denom.Currency.Symbol,
            fund.GetAmount(),
            fund.GetUsableAmount(),
            fund.AssetMarginPercentage*100,
        )
    }
    
    // Get buying power
    buyingPower, err := client.GetBuyingPower(walletAddress)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("\nBuying Power (%s):\n", buyingPower.Currency)
    fmt.Printf("  Available On-chain: %.4f\n", buyingPower.GetAvailableOnchain())
    fmt.Printf("  Collateral Value: %.4f\n", buyingPower.GetCollateral())
    fmt.Printf("  Brokerage Funds: %.4f\n", buyingPower.GetBrokerage())
    fmt.Printf("  TOTAL: %.4f\n", buyingPower.GetTotal())
}
Environment Variables
Variable	Description	Required
HTTP_CONFIG	HTTP server configuration	Yes
AUTH_FIREBASE_SERVICE	Firebase authentication endpoint	Yes
USER_STORE	User service endpoint	Yes
WALLET_MIDDLEWARE	Wallet middleware endpoint	Yes
ORGANIZATION_STORE	Organization service endpoint	Yes
FEATURE_FLAG_STORE	Feature flag endpoint	No
ROLE_STORE	Role service endpoint	No
Example Configuration
bash
# Required
HTTP_CONFIG='{"port":":8080","cors":{"allowedOrigins":["*"]}}'
AUTH_FIREBASE_SERVICE=auth-service:50075
USER_STORE=user-store:50049
WALLET_MIDDLEWARE=wallet-middleware:50088
ORGANIZATION_STORE=organization-store:50062

# Optional
FEATURE_FLAG_STORE=feature-flag-store:50055
ROLE_STORE=role-store:50066
LOG_LEVEL=info
Docker Compose Example
yaml
version: '3.8'

services:
  wallet-service:
    image: sologenic/wallet-service:latest
    environment:
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
      - AUTH_FIREBASE_SERVICE=auth-service:50075
      - USER_STORE=user-store:50049
      - WALLET_MIDDLEWARE=wallet-middleware:50088
      - ORGANIZATION_STORE=organization-store:50062
      - LOG_LEVEL=info
    ports:
      - "8080:8080"
    networks:
      - internal

  wallet-middleware:
    image: sologenic/wallet-middleware:latest
    environment:
      - CHAIN_RPC_URL=https://rpc.testnet.coreum.com
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Responses
Status	Code	Description
400	Bad Request	Invalid address format
401	Unauthorized	Missing or invalid token
403	Forbidden	User not active or insufficient permissions
404	Not Found	Wallet address not found
500	Internal Error	Server-side error
Example Error Response
json
{
  "error": "Invalid wallet address",
  "code": 400,
  "details": "The provided address format is invalid for the specified network"
}
Troubleshooting
Issue	Possible Cause	Solution
Funds not showing	Wrong network	Verify Network header matches wallet network
Zero buying power	No funds or collateral	Check wallet balance and asset margin
Calculation mismatch	Asset margin percentages	Verify asset configuration
Address not found	Invalid address format	Check address for network compatibility
Authentication error	Expired token	Refresh Firebase token
Best Practices
Performance
Cache buying power calculations (30-second TTL)

Batch requests when possible

Implement request timeouts

Use connection pooling

Accuracy
Real-time price feeds for collateral

Regular margin percentage updates

Handle decimal precision correctly

Validate addresses before processing

Security
Always validate authentication

Use OrganizationID for isolation

Never expose private keys

Rate limit by address

Calculation Examples
Example 1: Simple Stablecoin Funds
Wallet:

1000 WUSDC (stablecoin, margin 100%)

Result:

text
Available On-chain: 1000
Collateral: 0
Total Buying Power: 1000
Example 2: Mixed Assets
Wallet:

1000 WUSDC (margin 100%)

0.5 BTC (price: 50,000 WUSDC, margin 75%)

Result:

text
Available On-chain: 1000
Collateral: 0.5 × 50000 × 0.75 = 18,750
Total Buying Power: 19,750
Example 3: With Brokerage (Future)
Wallet:

1000 WUSDC (margin 100%)

Brokerage: 5000 WUSDC (multiplier 2x)

Result:

text
Available On-chain: 1000
Brokerage: 5000 × 2 = 10,000
Total Buying Power: 11,000
Related Services
Service	Description
Wallet Middleware	On-chain balance queries
User Store	User trade profiles and multipliers
Asset Store	Asset margin percentages
Organization Store	Tenant configuration
Auth Firebase Service	Token validation
Feature Flag Store	Feature toggles
License
This documentation is part of the TX Marketplace platform.
