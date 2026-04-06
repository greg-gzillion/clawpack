# Feature Flag Service (User Facing)

The Feature Flag Service provides a RESTful interface for retrieving active feature flags. This service is designed for **client-side (frontend) consumption** to enable progressive feature rollouts, A/B testing, and conditional feature availability based on organization, network, or user segments.

## Architecture Overview
┌─────────────────────────────────────────────────────────────────────────────┐
│ Feature Flag Service (User Facing) │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Public Endpoint (Unauthenticated) │ │
│ │ │ │
│ │ GET /api/featureflag/list │ │
│ │ (Returns active feature flags only) │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Feature Flag Resolution │ │
│ ├─────────────────────────────────────────────────────────────────────┤ │
│ │ • Filter by OrganizationID (tenant isolation) │ │
│ │ • Filter by Network (mainnet/testnet/devnet) │ │
│ │ • Filter by Status = ACTIVE only │ │
│ │ • Exclude disabled and future features │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Core Services │ │
│ ├───────────────┬───────────────┬─────────────────────────────────────┤ │
│ │ Feature Flag │ Organization │ HTTP Config │ │
│ │ Store │ Store │ │ │
│ └───────────────┴───────────────┴─────────────────────────────────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ Client-Side Caching │ │
│ │ │ │
│ │ • Frontend caches response for configured TTL │ │
│ │ • Reduces requests to feature flag service │ │
│ │ • Cache invalidation on expiry │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Security & Design Principles

### Important Security Considerations

**Deliberate Information Hiding:** The service intentionally does NOT return:

- Disabled features (status = DISABLED)
- Future features (scheduled for future release)
- Experimental features not yet ready for production
- Features in development

### Why This Matters

| Risk | Mitigation |
|------|------------|
| **Malicious Discovery** | Attackers cannot infer upcoming features or unannounced products by examining API responses |
| **Marketing Leaks** | Prevents accidental disclosure of new features that could spoil announcements or roadmaps |
| **Competitive Intelligence** | Competitors cannot determine development priorities from feature flag data |
| **Unfinished Features** | Users cannot discover or attempt to access incomplete functionality |

### Example of Hidden Data

```json
// What the API returns (ACTIVE only)
{
  "FeatureFlags": [
    {"Name": "new_dashboard", "Enabled": true},
    {"Name": "dark_mode", "Enabled": true}
  ]
}

// What is NOT returned (DISABLED, FUTURE, EXPERIMENTAL)
{
  "FeatureFlags": [
    {"Name": "ai_trading", "Enabled": false},      // ❌ Not returned
    {"Name": "quantum_encryption", "Enabled": false}, // ❌ Not returned
    {"Name": "mobile_app_v2", "ScheduledDate": "2025-01-01"} // ❌ Not returned
  ]
}
Role Requirements
Endpoint	Required Role	Description
GET /api/featureflag/list	None (Public)	List active feature flags
Note: This endpoint is intentionally public (unauthenticated) because feature flags determine UI behavior and feature availability. Authentication is not required as feature flags are not sensitive data - they only indicate what features are currently active, not user-specific data.

Headers
Header	Description	Required	Example
Network	Network environment	Yes	mainnet, testnet, devnet
OrganizationID	Organization UUID	Yes	72c4c072-2fe4-4f72-ae9d-d9d52a05fd71
Content-Type	Response format	Yes	application/json
Note: Unlike most other services, this endpoint does NOT require an Authorization header because feature flags are public configuration data.

Data Models
FeatureFlag Object
Field	Type	Description
Name	string	Unique feature identifier (e.g., "new_dashboard", "dark_mode")
Enabled	bool	Whether the feature is currently active
Description	string	Human-readable feature description (optional)
Metadata	map[string]interface{}	Additional feature-specific configuration (optional)
FeatureFlags Response Object
json
{
  "FeatureFlags": [
    {
      "Name": "string",
      "Enabled": "boolean",
      "Description": "string",
      "Metadata": {}
    }
  ]
}
Feature Status Values (Admin Only)
Status	Description	Returned to Users
ACTIVE	Feature is live and available	✅ Yes
DISABLED	Feature is turned off	❌ No
EXPERIMENTAL	Internal testing only	❌ No
FUTURE	Scheduled for future release	❌ No
DEPRECATED	Being phased out	❌ No
BETA	Limited beta release	✅ Yes (if enabled for organization)
Feature Flag Naming Convention
Prefix	Purpose	Example
ui_	UI component flags	ui_new_dashboard, ui_dark_mode
api_	API endpoint flags	api_v2_trading, api_websocket
payment_	Payment method flags	payment_crypto, payment_bank_transfer
kyc_	KYC process flags	kyc_automated, kyc_video_verification
reporting_	Reporting features	reporting_advanced_analytics
beta_	Beta features	beta_ai_assistant, beta_social_trading
API Endpoint
GET /api/featureflag/list
Retrieves all active feature flags for the specified organization and network. The response should be cached client-side to reduce server load.

Headers
Header	Description	Required
Content-Type	application/json	Yes
Network	mainnet, testnet, devnet	Yes
OrganizationID	Organization UUID	Yes
Query Parameters
None. All filtering is done via headers.

Example Request
bash
curl -X GET \
  "https://api.sologenic.org/api/featureflag/list" \
  -H "Content-Type: application/json" \
  -H "Network: mainnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71"
Example Response
json
{
  "FeatureFlags": [
    {
      "Name": "new_dashboard",
      "Enabled": true,
      "Description": "Enhanced dashboard with real-time analytics",
      "Metadata": {
        "rollout_percentage": 100,
        "min_version": "2.0.0"
      }
    },
    {
      "Name": "dark_mode",
      "Enabled": true,
      "Description": "Dark theme for the platform",
      "Metadata": {
        "default_theme": "system"
      }
    },
    {
      "Name": "advanced_charting",
      "Enabled": false,
      "Description": "TradingView advanced charts integration",
      "Metadata": {
        "libraries": ["tradingview", "chartjs"]
      }
    },
    {
      "Name": "social_trading",
      "Enabled": false,
      "Description": "Follow and copy successful traders",
      "Metadata": {
        "min_followers": 100
      }
    },
    {
      "Name": "api_v2",
      "Enabled": true,
      "Description": "Version 2 of the REST API",
      "Metadata": {
        "rate_limit": 1000,
        "endpoints": ["/api/v2/trades", "/api/v2/orders"]
      }
    }
  ]
}
Empty Response (No Active Features)
json
{
  "FeatureFlags": []
}
Client-Side Caching
Caching Strategy
TODO: The following will be true after caching is introduced:

The fetched FeatureFlags is to be cached for a period of time to reduce the number of requests to the feature flag service. Once the cache expires, FE will call the service again to get the latest FeatureFlags.

Recommended Cache Configuration
Environment	Cache TTL	Rationale
Production	5 minutes	Balance between freshness and performance
Staging	1 minute	More frequent updates for testing
Development	0 seconds (no cache)	Immediate reflection of changes
Frontend Caching Implementation
javascript
// Feature Flag Cache Manager
class FeatureFlagCache {
  constructor(ttlSeconds = 300) { // Default 5 minutes
    this.ttl = ttlSeconds * 1000;
    this.cache = null;
    this.lastFetched = null;
    this.pendingRequest = null;
  }

  async getFeatureFlags(forceRefresh = false) {
    // Return cached data if still valid
    if (!forceRefresh && this.isValid()) {
      return this.cache;
    }

    // Prevent multiple simultaneous requests
    if (this.pendingRequest) {
      return this.pendingRequest;
    }

    // Fetch fresh data
    this.pendingRequest = this.fetchFromAPI();
    try {
      this.cache = await this.pendingRequest;
      this.lastFetched = Date.now();
      return this.cache;
    } finally {
      this.pendingRequest = null;
    }
  }

  isValid() {
    if (!this.cache || !this.lastFetched) {
      return false;
    }
    return (Date.now() - this.lastFetched) < this.ttl;
  }

  async fetchFromAPI() {
    const response = await fetch('/api/featureflag/list', {
      headers: {
        'Content-Type': 'application/json',
        'Network': this.getNetwork(),
        'OrganizationID': this.getOrganizationId()
      }
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch feature flags');
    }
    
    const data = await response.json();
    return data.FeatureFlags;
  }

  getNetwork() {
    return localStorage.getItem('network') || 'mainnet';
  }

  getOrganizationId() {
    return localStorage.getItem('organizationId');
  }

  // Check if a specific feature is enabled
  isEnabled(featureName) {
    const flags = this.cache || [];
    const feature = flags.find(f => f.Name === featureName);
    return feature ? feature.Enabled : false;
  }

  // Get feature metadata
  getMetadata(featureName) {
    const flags = this.cache || [];
    const feature = flags.find(f => f.Name === featureName);
    return feature ? feature.Metadata : null;
  }

  // Clear cache (useful for logout or manual refresh)
  clear() {
    this.cache = null;
    this.lastFetched = null;
  }
}

// Singleton instance
const featureFlags = new FeatureFlagCache(300); // 5 minutes TTL

// Usage
async function initializeApp() {
  // Load feature flags on app start
  await featureFlags.getFeatureFlags();
  
  // Check specific features
  if (featureFlags.isEnabled('dark_mode')) {
    enableDarkMode();
  }
  
  if (featureFlags.isEnabled('new_dashboard')) {
    loadNewDashboard();
  } else {
    loadLegacyDashboard();
  }
}
Integration Examples
React Hook Implementation
jsx
import React, { createContext, useContext, useEffect, useState } from 'react';

// Feature Flag Context
const FeatureFlagContext = createContext(null);

// Feature Flag Provider
export function FeatureFlagProvider({ children, ttlSeconds = 300 }) {
  const [flags, setFlags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastFetched, setLastFetched] = useState(null);

  const fetchFeatureFlags = async (forceRefresh = false) => {
    // Check cache
    if (!forceRefresh && lastFetched && (Date.now() - lastFetched) < ttlSeconds * 1000) {
      return flags;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/featureflag/list', {
        headers: {
          'Content-Type': 'application/json',
          'Network': process.env.REACT_APP_NETWORK || 'mainnet',
          'OrganizationID': localStorage.getItem('organizationId')
        }
      });
      
      const data = await response.json();
      setFlags(data.FeatureFlags || []);
      setLastFetched(Date.now());
      return data.FeatureFlags;
    } catch (error) {
      console.error('Failed to fetch feature flags:', error);
      return flags;
    } finally {
      setLoading(false);
    }
  };

  const isEnabled = (featureName) => {
    const feature = flags.find(f => f.Name === featureName);
    return feature ? feature.Enabled : false;
  };

  const getMetadata = (featureName) => {
    const feature = flags.find(f => f.Name === featureName);
    return feature ? feature.Metadata : null;
  };

  useEffect(() => {
    fetchFeatureFlags();
  }, []);

  return (
    <FeatureFlagContext.Provider value={{
      flags,
      loading,
      isEnabled,
      getMetadata,
      refresh: () => fetchFeatureFlags(true)
    }}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

// Custom hook for using feature flags
export function useFeatureFlag(featureName) {
  const context = useContext(FeatureFlagContext);
  if (!context) {
    throw new Error('useFeatureFlag must be used within FeatureFlagProvider');
  }
  return context.isEnabled(featureName);
}

// Feature Flag Component
export function Feature({ name, children, fallback = null }) {
  const isEnabled = useFeatureFlag(name);
  return isEnabled ? children : fallback;
}

// Usage Examples
function App() {
  return (
    <FeatureFlagProvider>
      <Dashboard />
    </FeatureFlagProvider>
  );
}

function Dashboard() {
  const isDarkMode = useFeatureFlag('dark_mode');
  const isNewDashboard = useFeatureFlag('new_dashboard');
  const featureFlags = useContext(FeatureFlagContext);

  return (
    <div className={isDarkMode ? 'dark-theme' : 'light-theme'}>
      {/* Conditional rendering based on feature flag */}
      <Feature name="new_dashboard">
        <NewDashboard />
      </Feature>
      
      <Feature name="new_dashboard" fallback={<LegacyDashboard />}>
        <NewDashboard />
      </Feature>

      {/* Conditional logic */}
      {isNewDashboard ? <NewDashboard /> : <LegacyDashboard />}

      {/* Refresh button for admin testing */}
      <button onClick={() => featureFlags.refresh()}>
        Refresh Features
      </button>
    </div>
  );
}
Vue.js Plugin
javascript
// feature-flags.js
const FEATURE_FLAGS_KEY = Symbol('featureFlags');

export default {
  install(app, options = {}) {
    const ttl = options.ttl || 300; // 5 minutes default
    
    const state = reactive({
      flags: [],
      loading: false,
      lastFetched: null
    });

    const fetchFlags = async (forceRefresh = false) => {
      // Check cache
      if (!forceRefresh && state.lastFetched && 
          (Date.now() - state.lastFetched) < ttl * 1000) {
        return state.flags;
      }

      state.loading = true;
      try {
        const response = await fetch('/api/featureflag/list', {
          headers: {
            'Content-Type': 'application/json',
            'Network': import.meta.env.VITE_NETWORK || 'mainnet',
            'OrganizationID': localStorage.getItem('organizationId')
          }
        });
        
        const data = await response.json();
        state.flags = data.FeatureFlags || [];
        state.lastFetched = Date.now();
        return state.flags;
      } catch (error) {
        console.error('Failed to fetch feature flags:', error);
        return state.flags;
      } finally {
        state.loading = false;
      }
    };

    const isEnabled = (featureName) => {
      const feature = state.flags.find(f => f.Name === featureName);
      return feature ? feature.Enabled : false;
    };

    const getMetadata = (featureName) => {
      const feature = state.flags.find(f => f.Name === featureName);
      return feature ? feature.Metadata : null;
    };

    // Fetch on plugin initialization
    fetchFlags();

    // Provide global properties
    app.config.globalProperties.$featureFlags = {
      isEnabled,
      getMetadata,
      refresh: () => fetchFlags(true)
    };

    // Provide for composition API
    app.provide(FEATURE_FLAGS_KEY, {
      flags: readonly(state.flags),
      loading: readonly(state.loading),
      isEnabled,
      getMetadata,
      refresh: () => fetchFlags(true)
    });
  }
};

// Usage in component (Options API)
export default {
  mounted() {
    if (this.$featureFlags.isEnabled('dark_mode')) {
      this.enableDarkMode();
    }
  }
};

// Usage in component (Composition API)
import { inject } from 'vue';

export default {
  setup() {
    const featureFlags = inject(FEATURE_FLAGS_KEY);
    
    const showNewFeature = computed(() => 
      featureFlags.isEnabled('new_dashboard')
    );
    
    return { showNewFeature };
  }
};
Angular Service
typescript
// feature-flags.service.ts
import { Injectable, Inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, shareReplay, tap } from 'rxjs/operators';

export interface FeatureFlag {
  Name: string;
  Enabled: boolean;
  Description?: string;
  Metadata?: Record<string, any>;
}

@Injectable({
  providedIn: 'root'
})
export class FeatureFlagsService {
  private cache$: Observable<FeatureFlag[]> | null = null;
  private cacheTime = 300000; // 5 minutes in milliseconds
  private lastFetch = 0;

  constructor(private http: HttpClient) {}

  getFeatureFlags(forceRefresh = false): Observable<FeatureFlag[]> {
    const now = Date.now();
    
    // Return cached data if still valid
    if (!forceRefresh && this.cache$ && (now - this.lastFetch) < this.cacheTime) {
      return this.cache$;
    }

    // Fetch fresh data
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Network': localStorage.getItem('network') || 'mainnet',
      'OrganizationID': localStorage.getItem('organizationId') || ''
    });

    this.cache$ = this.http.get<{FeatureFlags: FeatureFlag[]}>('/api/featureflag/list', { headers })
      .pipe(
        map(response => response.FeatureFlags || []),
        tap(() => this.lastFetch = Date.now()),
        shareReplay(1),
        catchError(error => {
          console.error('Failed to fetch feature flags:', error);
          return of([]);
        })
      );

    return this.cache$;
  }

  isEnabled(featureName: string): Observable<boolean> {
    return this.getFeatureFlags().pipe(
      map(flags => {
        const feature = flags.find(f => f.Name === featureName);
        return feature ? feature.Enabled : false;
      })
    );
  }

  getMetadata(featureName: string): Observable<Record<string, any> | null> {
    return this.getFeatureFlags().pipe(
      map(flags => {
        const feature = flags.find(f => f.Name === featureName);
        return feature ? feature.Metadata : null;
      })
    );
  }

  refresh(): void {
    this.cache$ = null;
    this.lastFetch = 0;
  }
}

// Usage in component
@Component({
  selector: 'app-dashboard',
  template: `
    <div *ngIf="isNewDashboard$ | async">
      <app-new-dashboard></app-new-dashboard>
    </div>
    <div *ngIf="!(isNewDashboard$ | async)">
      <app-legacy-dashboard></app-legacy-dashboard>
    </div>
  `
})
export class DashboardComponent {
  isNewDashboard$: Observable<boolean>;

  constructor(private featureFlags: FeatureFlagsService) {
    this.isNewDashboard$ = this.featureFlags.isEnabled('new_dashboard');
  }
}
Vanilla JavaScript
javascript
// feature-flags.js
class FeatureFlagManager {
  constructor(options = {}) {
    this.ttl = options.ttl || 300; // seconds
    this.cache = null;
    this.lastFetch = null;
    this.listeners = [];
  }

  async init() {
    await this.fetchFlags();
    return this;
  }

  async fetchFlags(forceRefresh = false) {
    // Check cache
    if (!forceRefresh && this.isCacheValid()) {
      return this.cache;
    }

    try {
      const response = await fetch('/api/featureflag/list', {
        headers: {
          'Content-Type': 'application/json',
          'Network': this.getNetwork(),
          'OrganizationID': this.getOrganizationId()
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      this.cache = data.FeatureFlags || [];
      this.lastFetch = Date.now();
      
      // Notify listeners of update
      this.notifyListeners();
      
      return this.cache;
    } catch (error) {
      console.error('Failed to fetch feature flags:', error);
      return this.cache || [];
    }
  }

  isCacheValid() {
    if (!this.cache || !this.lastFetch) {
      return false;
    }
    return (Date.now() - this.lastFetch) < this.ttl * 1000;
  }

  isEnabled(featureName) {
    if (!this.cache) {
      console.warn(`Feature flags not loaded yet for: ${featureName}`);
      return false;
    }
    const feature = this.cache.find(f => f.Name === featureName);
    return feature ? feature.Enabled : false;
  }

  getMetadata(featureName) {
    if (!this.cache) {
      return null;
    }
    const feature = this.cache.find(f => f.Name === featureName);
    return feature ? feature.Metadata : null;
  }

  getNetwork() {
    return localStorage.getItem('network') || 'mainnet';
  }

  getOrganizationId() {
    return localStorage.getItem('organizationId');
  }

  subscribe(callback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }

  notifyListeners() {
    this.listeners.forEach(callback => callback(this.cache));
  }

  clearCache() {
    this.cache = null;
    this.lastFetch = null;
  }
}

// Initialize singleton
const featureFlags = new FeatureFlagManager({ ttl: 300 });

// Usage
async function main() {
  await featureFlags.init();
  
  // Check features
  if (featureFlags.isEnabled('dark_mode')) {
    document.body.classList.add('dark-theme');
  }
  
  // React to changes (e.g., after organization switch)
  featureFlags.subscribe((flags) => {
    console.log('Feature flags updated:', flags);
    // Re-render UI based on new flags
  });
  
  // Manual refresh (e.g., after admin changes)
  document.getElementById('refresh-features').addEventListener('click', () => {
    featureFlags.fetchFlags(true);
  });
}

main();
Use Cases
Progressive Feature Rollout
javascript
// Roll out new feature to 10% of users initially
const rolloutPercentage = featureFlags.getMetadata('ai_assistant')?.rollout_percentage || 0;
const userId = getCurrentUserId();
const hash = hashCode(userId) % 100;

if (featureFlags.isEnabled('ai_assistant') && hash < rolloutPercentage) {
  enableAIAssistant();
}
A/B Testing
javascript
// A/B test different UI variants
const variant = featureFlags.getMetadata('new_checkout')?.variant || 'A';

switch(variant) {
  case 'A':
    renderCheckoutVariantA();
    break;
  case 'B':
    renderCheckoutVariantB();
    break;
  default:
    renderLegacyCheckout();
}
Environment-Specific Features
javascript
// Different features per network
const network = getCurrentNetwork();

if (network === 'mainnet') {
  // Production: limited features
  if (featureFlags.isEnabled('real_trading')) {
    enableRealTrading();
  }
} else if (network === 'testnet') {
  // Testnet: all features for testing
  if (featureFlags.isEnabled('experimental_features')) {
    enableExperimentalFeatures();
  }
}
Organization Tier Features
javascript
// Features based on organization subscription tier
const tier = getOrganizationTier();

switch(tier) {
  case 'enterprise':
    if (featureFlags.isEnabled('advanced_reporting')) {
      enableAdvancedReporting();
    }
    // Fall through
  case 'professional':
    if (featureFlags.isEnabled('api_access')) {
      enableAPIAccess();
    }
    // Fall through
  case 'basic':
    enableBasicFeatures();
}
Start Parameters
Required Environment Variables
Environment Variable	Description	Source
HTTP_CONFIG	HTTP server configuration	com-be-http-lib
FEATURE_FLAG_STORE	Feature flag service endpoint	com-fs-feature-flag-model
ORGANIZATION_STORE	Organization service endpoint	com-fs-organization-model
GRPC_APPEND	Suffix for service URL	Configuration
GRPC_APPEND Explanation
The GRPC_APPEND parameter is the segment of the service URL that follows the service keyword.

Example:

Given URL: https://com-be-my-service-dfjiao-ijgao.a.run.app

Extract portion after "service" including the hyphen: dfjiao-ijgao.a.run.app

This allows the service to dynamically construct gRPC endpoints.

Example Environment Configuration
bash
# Required
FEATURE_FLAG_STORE=localhost:50055
ORGANIZATION_STORE=localhost:50060

# Optional
LOG_LEVEL=info
CACHE_TTL_SECONDS=300
MAX_FEATURE_FLAGS=100

# HTTP Configuration
HTTP_CONFIG='{
  "port": ":8080",
  "cors": {
    "allowedOrigins": ["http://localhost:3000", "https://app.sologenic.org"]
  },
  "timeouts": {
    "read": "5s",
    "write": "5s",
    "idle": "10s",
    "shutdown": "10s"
  }
}'

# gRPC Service suffix
GRPC_APPEND="dfjiao-ijgao.a.run.app"
Docker Compose Example
yaml
version: '3.8'

services:
  feature-flag-service:
    image: sologenic/feature-flag-service:latest
    environment:
      - FEATURE_FLAG_STORE=feature-flag-store:50055
      - ORGANIZATION_STORE=organization-service:50060
      - LOG_LEVEL=info
      - CACHE_TTL_SECONDS=300
      - GRPC_APPEND=local
      - HTTP_CONFIG={"port":":8080","cors":{"allowedOrigins":["*"]}}
    ports:
      - "8080:8080"
    networks:
      - internal

  feature-flag-store:
    image: sologenic/feature-flag-store:latest
    environment:
      - DATABASE_URL=postgres://user:pass@postgres:5432/feature_flags
    networks:
      - internal

  organization-service:
    image: sologenic/organization-service:latest
    environment:
      - ORGANIZATION_STORE=organization-store:50060
    networks:
      - internal

networks:
  internal:
    driver: bridge
Error Responses
Bad Request (400) - Missing Headers
json
{
  "error": "Bad Request",
  "message": "Missing required header: OrganizationID",
  "required_headers": ["Network", "OrganizationID"]
}
Bad Request (400) - Invalid Network
json
{
  "error": "Bad Request",
  "message": "Invalid network value",
  "valid_values": ["mainnet", "testnet", "devnet"],
  "received": "invalid_network"
}
Internal Server Error (500)
json
{
  "error": "Internal Server Error",
  "message": "Failed to retrieve feature flags",
  "request_id": "req_12345"
}
Troubleshooting
Common Issues
Issue	Possible Cause	Solution
Missing headers	Network or OrganizationID not provided	Add required headers to request
Empty response	No active features for organization	Check feature flag configuration in admin panel
Stale data	Client cache not expired	Reduce cache TTL or force refresh
Feature not showing	Feature status is not ACTIVE	Enable feature in admin panel
Wrong network	Feature configured for different network	Verify network header matches feature configuration
Debugging
bash
# Enable debug logging
LOG_LEVEL=debug

# Test endpoint with curl
curl -X GET "https://api.sologenic.org/api/featureflag/list" \
  -H "Content-Type: application/json" \
  -H "Network: testnet" \
  -H "OrganizationID: 72c4c072-2fe4-4f72-ae9d-d9d52a05fd71" \
  -v

# Check response time
time curl -X GET "https://api.sologenic.org/api/featureflag/list" \
  -H "Network: mainnet" \
  -H "OrganizationID: test-org"

# Monitor cache behavior (add to frontend)
console.log('Cache age:', (Date.now() - lastFetch) / 1000, 'seconds');
Best Practices
Frontend Implementation
Practice	Recommendation
Cache duration	5 minutes for production
Error handling	Fall back to cached or default values
Refresh strategy	Manual refresh button for admins
Loading states	Show skeleton UI while loading
Default behavior	Assume features are disabled on error
Feature Flag Naming
Practice	Example
Use descriptive names	enable_advanced_charting not flag_123
Group related features	ui_, api_, payment_ prefixes
Version in name	api_v2, dashboard_v3
Avoid boolean negatives	enable_feature not disable_feature
Performance Optimization
javascript
// Batch multiple feature checks
const features = ['new_dashboard', 'dark_mode', 'api_v2'];
const enabledFeatures = features.filter(name => featureFlags.isEnabled(name));

// Preload feature flags on app initialization
await featureFlags.getFeatureFlags();

// Use web workers for heavy flag processing
const worker = new Worker('feature-flag-worker.js');
worker.postMessage({ flags: featureFlags.cache });
Security Considerations
Concern	Mitigation
Feature enumeration	Only return ACTIVE features
Cache poisoning	Validate response structure
Header injection	Sanitize header inputs
Rate limiting	Implement per-IP rate limits
Related Services
Service	Description
Feature Flag Store	Storage backend for feature flags
Admin Feature Flag Service	Management interface for feature flags
Organization Service	Organization context for flag resolution
Admin Account Service	Role-based access control
License
This documentation is part of the TX Marketplace platform.

text

Now let's verify the documentation was created:

```bash
ls -la ~/dev/TXdocumentation/feature-flag/
