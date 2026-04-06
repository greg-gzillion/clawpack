# Trade Profile Service (Trade Profile Proto)

The Trade Profile proto provides all the functionality required to interact with the trade profile service. Trade profiles represent user trading preferences, strategies, risk settings, and automated trading configurations.

## Overview

The Trade Profile service is a gRPC-based system that handles:
- User trading preferences and settings
- Risk management configurations
- Automated trading strategies
- Trading limits and restrictions
- API key management for trading
- Trading bot configurations
- Alert and notification settings
- Trading session management

## Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│ Client Applications │
│ (Trading UI, Trading Bots, Mobile App, API Clients, Analytics) │
└───────────────────────────────────┬─────────────────────────────────────────┘
│ gRPC
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Trade Profile Service │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Profile │ │ Risk │ │ Strategy │ │ API Key │ │
│ │ Management │ │ Management │ │ Engine │ │ Manager │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Alert │ │ Trading │ │ Session │ │
│ │ Config │ │ Limits │ │ Manager │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ │
└───────────────────────────────────┬─────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Storage Layer │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Profile │ │ Redis Cache │ │ PostgreSQL │ │ Encrypted │ │
│ │ Store │ │ (Session) │ │ (Settings) │ │ Vault (Keys)│ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Environment Variables

### Required Variables

| Variable | Description | Format | Example |
|----------|-------------|--------|---------|
| `TRADE_PROFILE_STORE` | gRPC endpoint for trade profile store service | `host:port` | `trade-profile-store:50074` |
| `TRADE_PROFILE_STORE_TESTING` | Enable test mode with in-memory buffer | `TRUE` | `TRUE` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MAX_ACTIVE_SESSIONS` | Maximum concurrent trading sessions per user | `5` |
| `SESSION_TIMEOUT_MINUTES` | Trading session timeout in minutes | `30` |
| `MAX_API_KEYS_PER_USER` | Maximum API keys per user | `10` |
| `RATE_LIMIT_REQUESTS` | Rate limit requests per minute | `1000` |
| `ENABLE_2FA_REQUIRED` | Require 2FA for trading | `false` |
| `MAX_DAILY_TRADING_LIMIT` | Maximum daily trading volume | `1000000` |

## Proto Definition

```protobuf
syntax = "proto3";

package tradeprofile.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/struct.proto";

// Trade Profile Service Definition
service TradeProfileService {
    // Profile management
    rpc CreateTradeProfile(CreateTradeProfileRequest) returns (CreateTradeProfileResponse);
    rpc GetTradeProfile(GetTradeProfileRequest) returns (GetTradeProfileResponse);
    rpc UpdateTradeProfile(UpdateTradeProfileRequest) returns (UpdateTradeProfileResponse);
    rpc DeleteTradeProfile(DeleteTradeProfileRequest) returns (DeleteTradeProfileResponse);
    
    // Trading preferences
    rpc UpdateTradingPreferences(UpdateTradingPreferencesRequest) returns (UpdateTradingPreferencesResponse);
    rpc GetTradingPreferences(GetTradingPreferencesRequest) returns (GetTradingPreferencesResponse);
    
    // Risk management
    rpc UpdateRiskSettings(UpdateRiskSettingsRequest) returns (UpdateRiskSettingsResponse);
    rpc GetRiskSettings(GetRiskSettingsRequest) returns (GetRiskSettingsResponse);
    rpc CheckRiskLimits(CheckRiskLimitsRequest) returns (CheckRiskLimitsResponse);
    
    // Trading limits
    rpc SetTradingLimits(SetTradingLimitsRequest) returns (SetTradingLimitsResponse);
    rpc GetTradingLimits(GetTradingLimitsRequest) returns (GetTradingLimitsResponse);
    rpc GetCurrentUsage(GetCurrentUsageRequest) returns (GetCurrentUsageResponse);
    
    // API Key management
    rpc CreateAPIKey(CreateAPIKeyRequest) returns (CreateAPIKeyResponse);
    rpc GetAPIKeys(GetAPIKeysRequest) returns (GetAPIKeysResponse);
    rpc RevokeAPIKey(RevokeAPIKeyRequest) returns (RevokeAPIKeyResponse);
    rpc RotateAPIKey(RotateAPIKeyRequest) returns (RotateAPIKeyResponse);
    
    // Trading sessions
    rpc StartTradingSession(StartTradingSessionRequest) returns (StartTradingSessionResponse);
    rpc EndTradingSession(EndTradingSessionRequest) returns (EndTradingSessionResponse);
    rpc GetActiveSessions(GetActiveSessionsRequest) returns (GetActiveSessionsResponse);
    rpc ExtendSession(ExtendSessionRequest) returns (ExtendSessionResponse);
    
    // Trading strategies (bot configs)
    rpc CreateStrategy(CreateStrategyRequest) returns (CreateStrategyResponse);
    rpc GetStrategies(GetStrategiesRequest) returns (GetStrategiesResponse);
    rpc UpdateStrategy(UpdateStrategyRequest) returns (UpdateStrategyResponse);
    rpc DeleteStrategy(DeleteStrategyRequest) returns (DeleteStrategyResponse);
    rpc ActivateStrategy(ActivateStrategyRequest) returns (ActivateStrategyResponse);
    rpc DeactivateStrategy(DeactivateStrategyRequest) returns (DeactivateStrategyResponse);
    
    // Alert configurations
    rpc CreateAlertConfig(CreateAlertConfigRequest) returns (CreateAlertConfigResponse);
    rpc GetAlertConfigs(GetAlertConfigsRequest) returns (GetAlertConfigsResponse);
    rpc UpdateAlertConfig(UpdateAlertConfigRequest) returns (UpdateAlertConfigResponse);
    rpc DeleteAlertConfig(DeleteAlertConfigRequest) returns (DeleteAlertConfigResponse);
    rpc TriggerAlert(TriggerAlertRequest) returns (TriggerAlertResponse);
    
    // Whitelist/Blacklist
    rpc AddToWhitelist(AddToWhitelistRequest) returns (AddToWhitelistResponse);
    rpc RemoveFromWhitelist(RemoveFromWhitelistRequest) returns (RemoveFromWhitelistResponse);
    rpc GetWhitelist(GetWhitelistRequest) returns (GetWhitelistResponse);
    rpc AddToBlacklist(AddToBlacklistRequest) returns (AddToBlacklistResponse);
    rpc RemoveFromBlacklist(RemoveFromBlacklistRequest) returns (RemoveFromBlacklistResponse);
    rpc GetBlacklist(GetBlacklistRequest) returns (GetBlacklistResponse);
}

// ==================== Core Profile Messages ====================

enum TradingExperience {
    TRADING_EXPERIENCE_UNSPECIFIED = 0;
    BEGINNER = 1;
    INTERMEDIATE = 2;
    ADVANCED = 3;
    EXPERT = 4;
    INSTITUTIONAL = 5;
}

enum RiskTolerance {
    RISK_TOLERANCE_UNSPECIFIED = 0;
    CONSERVATIVE = 1;
    MODERATE = 2;
    AGGRESSIVE = 3;
    VERY_AGGRESSIVE = 4;
}

enum OrderTypePreference {
    ORDER_TYPE_PREFERENCE_UNSPECIFIED = 0;
    MARKET_ONLY = 1;
    LIMIT_ONLY = 2;
    ALL_TYPES = 3;
}

// Main Trade Profile message
message TradeProfile {
    string profile_id = 1;
    string user_id = 2;
    string organization_id = 3;
    
    // Basic info
    string display_name = 4;
    string bio = 5;
    TradingExperience experience_level = 6;
    RiskTolerance risk_tolerance = 7;
    
    // Trading preferences
    TradingPreferences preferences = 8;
    
    // Risk settings
    RiskSettings risk_settings = 9;
    
    // Trading limits
    TradingLimits limits = 10;
    
    // Status
    bool is_active = 11;
    bool is_verified = 12;
    google.protobuf.Timestamp verified_at = 13;
    
    // Timestamps
    google.protobuf.Timestamp created_at = 14;
    google.protobuf.Timestamp updated_at = 15;
    google.protobuf.Timestamp last_active_at = 16;
    
    // Metadata
    map<string, string> metadata = 17;
    repeated string tags = 18;
}

// Trading preferences
message TradingPreferences {
    string default_asset_pair = 1;
    OrderTypePreference default_order_type = 2;
    string default_time_in_force = 3;           // GTC, IOC, FOK, DAY
    bool enable_market_orders = 4;
    bool enable_stop_orders = 5;
    bool enable_trailing_stop = 6;
    bool enable_margin_trading = 7;
    double default_leverage = 8;                 // 1.0, 2.0, 5.0, etc.
    bool show_advanced_charts = 9;
    string quote_currency = 10;                  // USD, EUR, BTC, etc.
    int32 price_precision = 11;                  // Decimal places for prices
    int32 amount_precision = 12;                 // Decimal places for amounts
    string theme = 13;                           // light, dark, system
    string language = 14;                        // en, es, fr, etc.
    bool email_notifications = 15;
    bool push_notifications = 16;
    map<string, string> custom_preferences = 17;
}

// Risk settings
message RiskSettings {
    double max_position_size_percent = 1;        // Max % of portfolio per position
    double max_daily_loss_percent = 2;           // Max daily loss % before stop
    double max_drawdown_percent = 3;             // Max drawdown % before stop
    double max_leverage = 4;                     // Maximum allowed leverage
    bool enable_stop_loss_default = 5;
    double default_stop_loss_percent = 6;
    bool enable_take_profit_default = 7;
    double default_take_profit_percent = 8;
    bool require_confirm_large_trades = 9;
    double large_trade_threshold = 10;           // Threshold for confirmation
    bool enable_circuit_breakers = 11;
    int32 circuit_breaker_trades = 12;           // Number of trades to trigger
    int32 circuit_breaker_duration_seconds = 13; // Cool-down period
    bool enable_trading_hours = 14;
    string trading_start_time = 15;              // HH:MM in UTC
    string trading_end_time = 16;                // HH:MM in UTC
    repeated string restricted_assets = 17;      // Assets not allowed to trade
    map<string, string> custom_rules = 18;
}

// Trading limits
message TradingLimits {
    string daily_trade_volume_limit = 1;         // Max daily trade volume
    string weekly_trade_volume_limit = 2;        // Max weekly trade volume
    string monthly_trade_volume_limit = 3;       // Max monthly trade volume
    int32 daily_trade_count_limit = 4;           // Max trades per day
    int32 weekly_trade_count_limit = 5;          // Max trades per week
    string max_order_size = 6;                   // Max size per order
    string min_order_size = 7;                   // Min size per order
    string max_position_value = 8;               // Max position value per asset
    map<string, string> asset_specific_limits = 9; // Per-asset limits
}

// Current usage statistics
message CurrentUsage {
    string today_volume = 1;
    int32 today_trades = 2;
    string week_volume = 3;
    int32 week_trades = 4;
    string month_volume = 5;
    int32 month_trades = 6;
    map<string, string> asset_volumes = 7;
    double current_drawdown_percent = 8;
    string current_loss_today = 9;
}

// API Key
message APIKey {
    string key_id = 1;
    string name = 2;
    string api_key = 3;                          // Partial/masked in responses
    string api_secret = 4;                       // Only returned on creation
    repeated string permissions = 5;             // trade, read, withdraw, etc.
    repeated string allowed_assets = 6;          // Empty means all
    repeated string allowed_ip_addresses = 7;    // IP whitelist
    google.protobuf.Timestamp expires_at = 8;
    google.protobuf.Timestamp last_used_at = 9;
    google.protobuf.Timestamp created_at = 10;
    bool is_active = 11;
    int32 usage_count = 12;
    string created_by = 13;
}

// Trading session
message TradingSession {
    string session_id = 1;
    string user_id = 2;
    string device_id = 3;
    string device_name = 4;
    string ip_address = 5;
    string user_agent = 6;
    google.protobuf.Timestamp started_at = 7;
    google.protobuf.Timestamp last_activity_at = 8;
    google.protobuf.Timestamp expires_at = 9;
    bool is_active = 10;
    int32 trade_count = 11;
    string volume = 12;
}

// Trading strategy (bot configuration)
message TradingStrategy {
    string strategy_id = 1;
    string user_id = 2;
    string name = 3;
    string description = 4;
    string strategy_type = 5;                    // grid, dca, arbitrage, momentum, etc.
    google.protobuf.Struct configuration = 6;    // Strategy-specific config
    bool is_active = 7;
    bool is_default = 8;
    string risk_level = 9;                       // conservative, moderate, aggressive
    repeated string asset_pairs = 10;
    string total_invested = 11;
    string total_return = 12;
    double roi_percent = 13;
    google.protobuf.Timestamp created_at = 14;
    google.protobuf.Timestamp updated_at = 15;
    google.protobuf.Timestamp last_run_at = 16;
    map<string, string> metadata = 17;
}

// Alert configuration
message AlertConfig {
    string alert_id = 1;
    string user_id = 2;
    string name = 3;
    string alert_type = 4;                       // price, volume, indicator, system
    string condition = 5;                        // above, below, crosses, etc.
    string value = 6;                            // Threshold value
    string asset_pair = 7;
    string indicator = 8;                        // RSI, MACD, EMA, etc.
    repeated string notification_methods = 9;    // email, push, webhook, sms
    string webhook_url = 10;
    bool is_active = 11;
    int32 trigger_count = 12;
    google.protobuf.Timestamp last_triggered_at = 13;
    google.protobuf.Timestamp created_at = 14;
    google.protobuf.Timestamp updated_at = 15;
    map<string, string> metadata = 16;
}

// Whitelist/Blacklist entries
message WhitelistEntry {
    string entry_id = 1;
    string user_id = 2;
    string entry_type = 3;                       // address, asset, ip
    string value = 4;
    string reason = 5;
    google.protobuf.Timestamp created_at = 6;
    google.protobuf.Timestamp expires_at = 7;
    string created_by = 8;
}

message BlacklistEntry {
    string entry_id = 1;
    string user_id = 2;
    string entry_type = 3;                       // address, asset, ip, user
    string value = 4;
    string reason = 5;
    google.protobuf.Timestamp created_at = 6;
    google.protobuf.Timestamp expires_at = 7;
    string created_by = 8;
}

// ==================== Request/Response Messages ====================

message CreateTradeProfileRequest {
    string user_id = 1;
    string organization_id = 2;
    string display_name = 3;
    string bio = 4;
    TradingExperience experience_level = 5;
    RiskTolerance risk_tolerance = 6;
    map<string, string> metadata = 7;
    repeated string tags = 8;
}

message CreateTradeProfileResponse {
    TradeProfile profile = 1;
    bool created = 2;
    string message = 3;
}

message GetTradeProfileRequest {
    string user_id = 1;
    string organization_id = 2;
    string profile_id = 3;                       // Optional
}

message GetTradeProfileResponse {
    TradeProfile profile = 1;
    bool found = 2;
}

message UpdateTradeProfileRequest {
    string user_id = 1;
    string organization_id = 2;
    optional string display_name = 3;
    optional string bio = 4;
    optional TradingExperience experience_level = 5;
    optional RiskTolerance risk_tolerance = 6;
    optional bool is_active = 7;
    map<string, string> metadata = 8;
    repeated string tags = 9;
}

message UpdateTradeProfileResponse {
    TradeProfile profile = 1;
    bool updated = 2;
    string message = 3;
}

message DeleteTradeProfileRequest {
    string user_id = 1;
    string organization_id = 2;
    bool permanent = 3;
}

message DeleteTradeProfileResponse {
    bool deleted = 1;
    string message = 2;
}

// Trading preferences requests/responses
message UpdateTradingPreferencesRequest {
    string user_id = 1;
    string organization_id = 2;
    TradingPreferences preferences = 3;
}

message UpdateTradingPreferencesResponse {
    TradingPreferences preferences = 1;
    bool updated = 2;
}

message GetTradingPreferencesRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetTradingPreferencesResponse {
    TradingPreferences preferences = 1;
    bool found = 2;
}

// Risk settings requests/responses
message UpdateRiskSettingsRequest {
    string user_id = 1;
    string organization_id = 2;
    RiskSettings settings = 3;
}

message UpdateRiskSettingsResponse {
    RiskSettings settings = 1;
    bool updated = 2;
}

message GetRiskSettingsRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetRiskSettingsResponse {
    RiskSettings settings = 1;
    bool found = 2;
}

message CheckRiskLimitsRequest {
    string user_id = 1;
    string organization_id = 2;
    string asset_pair = 3;
    string side = 4;                             // buy, sell
    string quantity = 5;
    string price = 6;
    double leverage = 7;
}

message CheckRiskLimitsResponse {
    bool allowed = 1;
    repeated string violations = 2;
    string message = 3;
}

// Trading limits requests/responses
message SetTradingLimitsRequest {
    string user_id = 1;
    string organization_id = 2;
    TradingLimits limits = 3;
}

message SetTradingLimitsResponse {
    TradingLimits limits = 1;
    bool set = 2;
}

message GetTradingLimitsRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetTradingLimitsResponse {
    TradingLimits limits = 1;
    bool found = 2;
}

message GetCurrentUsageRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetCurrentUsageResponse {
    CurrentUsage usage = 1;
    bool found = 2;
}

// API Key requests/responses
message CreateAPIKeyRequest {
    string user_id = 1;
    string organization_id = 2;
    string name = 3;
    repeated string permissions = 4;
    repeated string allowed_assets = 5;
    repeated string allowed_ip_addresses = 6;
    google.protobuf.Timestamp expires_at = 7;
}

message CreateAPIKeyResponse {
    APIKey api_key = 1;
    bool created = 2;
    string message = 3;
}

message GetAPIKeysRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_inactive = 3;
}

message GetAPIKeysResponse {
    repeated APIKey api_keys = 1;
    int32 total_count = 2;
}

message RevokeAPIKeyRequest {
    string user_id = 1;
    string organization_id = 2;
    string key_id = 3;
}

message RevokeAPIKeyResponse {
    bool revoked = 1;
    string message = 2;
}

message RotateAPIKeyRequest {
    string user_id = 1;
    string organization_id = 2;
    string key_id = 3;
}

message RotateAPIKeyResponse {
    APIKey new_api_key = 1;
    bool rotated = 2;
}

// Trading session requests/responses
message StartTradingSessionRequest {
    string user_id = 1;
    string organization_id = 2;
    string device_id = 3;
    string device_name = 4;
    string ip_address = 5;
    string user_agent = 6;
}

message StartTradingSessionResponse {
    TradingSession session = 1;
    bool started = 2;
    string message = 3;
}

message EndTradingSessionRequest {
    string user_id = 1;
    string organization_id = 2;
    string session_id = 3;
}

message EndTradingSessionResponse {
    bool ended = 1;
    string message = 2;
}

message GetActiveSessionsRequest {
    string user_id = 1;
    string organization_id = 2;
}

message GetActiveSessionsResponse {
    repeated TradingSession sessions = 1;
    int32 active_count = 2;
}

message ExtendSessionRequest {
    string user_id = 1;
    string organization_id = 2;
    string session_id = 3;
    int32 extend_minutes = 4;
}

message ExtendSessionResponse {
    TradingSession session = 1;
    bool extended = 2;
}

// Trading strategy requests/responses
message CreateStrategyRequest {
    string user_id = 1;
    string organization_id = 2;
    string name = 3;
    string description = 4;
    string strategy_type = 5;
    google.protobuf.Struct configuration = 6;
    string risk_level = 7;
    repeated string asset_pairs = 8;
    map<string, string> metadata = 9;
}

message CreateStrategyResponse {
    TradingStrategy strategy = 1;
    bool created = 2;
    string message = 3;
}

message GetStrategiesRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_inactive = 3;
    string strategy_type = 4;
}

message GetStrategiesResponse {
    repeated TradingStrategy strategies = 1;
    int32 total_count = 2;
}

message UpdateStrategyRequest {
    string user_id = 1;
    string organization_id = 2;
    string strategy_id = 3;
    optional string name = 4;
    optional string description = 5;
    optional google.protobuf.Struct configuration = 6;
    optional string risk_level = 7;
    repeated string asset_pairs = 8;
    map<string, string> metadata = 9;
}

message UpdateStrategyResponse {
    TradingStrategy strategy = 1;
    bool updated = 2;
}

message DeleteStrategyRequest {
    string user_id = 1;
    string organization_id = 2;
    string strategy_id = 3;
}

message DeleteStrategyResponse {
    bool deleted = 1;
}

message ActivateStrategyRequest {
    string user_id = 1;
    string organization_id = 2;
    string strategy_id = 3;
}

message ActivateStrategyResponse {
    bool activated = 1;
    TradingStrategy strategy = 2;
}

message DeactivateStrategyRequest {
    string user_id = 1;
    string organization_id = 2;
    string strategy_id = 3;
}

message DeactivateStrategyResponse {
    bool deactivated = 1;
    TradingStrategy strategy = 2;
}

// Alert configuration requests/responses
message CreateAlertConfigRequest {
    string user_id = 1;
    string organization_id = 2;
    string name = 3;
    string alert_type = 4;
    string condition = 5;
    string value = 6;
    string asset_pair = 7;
    string indicator = 8;
    repeated string notification_methods = 9;
    string webhook_url = 10;
    map<string, string> metadata = 11;
}

message CreateAlertConfigResponse {
    AlertConfig alert = 1;
    bool created = 2;
}

message GetAlertConfigsRequest {
    string user_id = 1;
    string organization_id = 2;
    bool include_inactive = 3;
    string alert_type = 4;
}

message GetAlertConfigsResponse {
    repeated AlertConfig alerts = 1;
    int32 total_count = 2;
}

message UpdateAlertConfigRequest {
    string user_id = 1;
    string organization_id = 2;
    string alert_id = 3;
    optional string name = 4;
    optional string condition = 5;
    optional string value = 6;
    optional bool is_active = 7;
    repeated string notification_methods = 8;
    optional string webhook_url = 9;
}

message UpdateAlertConfigResponse {
    AlertConfig alert = 1;
    bool updated = 2;
}

message DeleteAlertConfigRequest {
    string user_id = 1;
    string organization_id = 2;
    string alert_id = 3;
}

message DeleteAlertConfigResponse {
    bool deleted = 1;
}

message TriggerAlertRequest {
    string user_id = 1;
    string organization_id = 2;
    string alert_id = 3;
    string trigger_value = 4;
    map<string, string> context = 5;
}

message TriggerAlertResponse {
    bool triggered = 1;
    repeated string notifications_sent = 2;
}

// Whitelist/Blacklist requests/responses
message AddToWhitelistRequest {
    string user_id = 1;
    string organization_id = 2;
    string entry_type = 3;
    string value = 4;
    string reason = 5;
    google.protobuf.Timestamp expires_at = 6;
}

message AddToWhitelistResponse {
    WhitelistEntry entry = 1;
    bool added = 2;
}

message RemoveFromWhitelistRequest {
    string user_id = 1;
    string organization_id = 2;
    string entry_id = 3;
}

message RemoveFromWhitelistResponse {
    bool removed = 1;
}

message GetWhitelistRequest {
    string user_id = 1;
    string organization_id = 2;
    string entry_type = 3;
}

message GetWhitelistResponse {
    repeated WhitelistEntry entries = 1;
    int32 total_count = 2;
}

message AddToBlacklistRequest {
    string user_id = 1;
    string organization_id = 2;
    string entry_type = 3;
    string value = 4;
    string reason = 5;
    google.protobuf.Timestamp expires_at = 6;
}

message AddToBlacklistResponse {
    BlacklistEntry entry = 1;
    bool added = 2;
}

message RemoveFromBlacklistRequest {
    string user_id = 1;
    string organization_id = 2;
    string entry_id = 3;
}

message RemoveFromBlacklistResponse {
    bool removed = 1;
}

message GetBlacklistRequest {
    string user_id = 1;
    string organization_id = 2;
    string entry_type = 3;
}

message GetBlacklistResponse {
    repeated BlacklistEntry entries = 1;
    int32 total_count = 2;
}
Save the file:

Ctrl+O, Enter, Ctrl+X

2. Trade Profile Build Script
bash
mkdir -p ~/dev/TXdocumentation/trade-profile/bin
nano ~/dev/TXdocumentation/trade-profile/bin/build.sh
bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}Starting Trade Profile proto build...${NC}"

# Check if proto file exists
if [ ! -f "trade-profile.proto" ] && [ ! -f "proto/trade-profile.proto" ]; then
    echo -e "${RED}Error: No trade-profile.proto file found in root or proto/ directory${NC}"
    exit 1
fi

# Determine proto file location
if [ -f "trade-profile.proto" ]; then
    PROTO_FILE="trade-profile.proto"
    PROTO_PATH="."
else
    PROTO_FILE="proto/trade-profile.proto"
    PROTO_PATH="proto"
fi

echo -e "${BLUE}Using proto file: ${PROTO_FILE}${NC}"

# Check for required tools
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        exit 1
    fi
}

check_command protoc
check_command protoc-gen-go
check_command protoc-gen-go-grpc

# Create directories
echo -e "${YELLOW}Creating build directories...${NC}"
mkdir -p build
mkdir -p client/go
mkdir -p client/typescript

# Generate Go files
echo -e "${BLUE}Generating Go protobuf files...${NC}"
protoc \
    --go_out=client/go \
    --go_opt=paths=source_relative \
    --go-grpc_out=client/go \
    --go-grpc_opt=paths=source_relative \
    --proto_path=${PROTO_PATH} \
    ${PROTO_FILE}

# Check for TypeScript project
if [ -f "package.json" ] && [ -f "tsconfig.json" ]; then
    echo -e "${BLUE}TypeScript project detected. Generating TypeScript files...${NC}"
    
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing npm dependencies...${NC}"
        npm install
    fi
    
    if command -v protoc-gen-ts &> /dev/null; then
        protoc \
            --plugin=protoc-gen-ts=$(which protoc-gen-ts) \
            --ts_out=client/typescript \
            --proto_path=${PROTO_PATH} \
            ${PROTO_FILE}
    fi
    
    if command -v protoc-gen-grpc-web &> /dev/null; then
        protoc \
            --plugin=protoc-gen-grpc-web=$(which protoc-gen-grpc-web) \
            --grpc-web_out=import_style=typescript,mode=grpcwebtext:client/typescript \
            --proto_path=${PROTO_PATH} \
            ${PROTO_FILE}
    fi
    
    echo -e "${GREEN}TypeScript files generated successfully${NC}"
else
    echo -e "${YELLOW}Skipping TypeScript generation (package.json or tsconfig.json not found)${NC}"
fi

# Generate documentation
echo -e "${BLUE}Generating documentation...${NC}"
if command -v protoc-gen-doc &> /dev/null; then
    protoc \
        --doc_out=build \
        --doc_opt=markdown,trade-profile-api.md \
        --proto_path=${PROTO_PATH} \
        ${PROTO_FILE}
    echo -e "${GREEN}Documentation generated${NC}"
fi

# Add generated files to git
echo -e "${YELLOW}Adding generated files to git...${NC}"
git add client/go/*.pb.go 2>/dev/null || true
git add client/typescript/*.ts 2>/dev/null || true
git add build/ 2>/dev/null || true

echo -e "${GREEN}Build complete!${NC}"
echo -e "${GREEN}Generated files:${NC}"
echo "  - client/go/trade_profile.pb.go"
echo "  - client/go/trade_profile_grpc.pb.go"
if [ -f "client/typescript/trade_profile.ts" ]; then
    echo "  - client/typescript/trade_profile.ts"
fi
echo "  - build/trade-profile-api.md"
Save and make executable:

Ctrl+O, Enter, Ctrl+X

chmod +x ~/dev/TXdocumentation/trade-profile/bin/build.sh

3. Trade Profile Go Client
bash
mkdir -p ~/dev/TXdocumentation/trade-profile/client/go
nano ~/dev/TXdocumentation/trade-profile/client/go/trade_profile_client.go
go
package tradeprofile

import (
    "context"
    "fmt"
    "log"
    "os"
    "time"
    
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    "google.golang.org/grpc/metadata"
    
    tradeprofilePb "github.com/sologenic/trade-profile/client/go"
    "google.golang.org/protobuf/types/known/timestamppb"
)

type TradeProfileClient struct {
    client tradeprofilePb.TradeProfileServiceClient
    conn   *grpc.ClientConn
    token  string
}

// Create new trade profile client
func NewTradeProfileClient(addr string) (*TradeProfileClient, error) {
    // Check for testing mode
    if addr == "" {
        if testingMode := os.Getenv("TRADE_PROFILE_STORE_TESTING"); testingMode == "TRUE" {
            return &TradeProfileClient{}, nil
        }
        return nil, fmt.Errorf("TRADE_PROFILE_STORE environment variable not set and not in testing mode")
    }
    
    conn, err := grpc.Dial(addr,
        grpc.WithTransportCredentials(insecure.NewCredentials()),
        grpc.WithTimeout(10*time.Second),
        grpc.WithBlock(),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to connect to trade profile service: %w", err)
    }
    
    return &TradeProfileClient{
        client: tradeprofilePb.NewTradeProfileServiceClient(conn),
        conn:   conn,
    }, nil
}

func (c *TradeProfileClient) Close() error {
    if c.conn != nil {
        return c.conn.Close()
    }
    return nil
}

// SetAuthToken sets the authentication token for requests
func (c *TradeProfileClient) SetAuthToken(token string) {
    c.token = token
}

// Get authenticated context
func (c *TradeProfileClient) getContext(ctx context.Context) context.Context {
    if c.token != "" {
        return metadata.AppendToOutgoingContext(ctx, "authorization", "Bearer "+c.token)
    }
    return ctx
}

// Create a new trade profile
func (c *TradeProfileClient) CreateTradeProfile(ctx context.Context, req *tradeprofilePb.CreateTradeProfileRequest) (*tradeprofilePb.TradeProfile, error) {
    if c.client == nil {
        return mockTradeProfile(req), nil
    }
    
    resp, err := c.client.CreateTradeProfile(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create trade profile failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("trade profile creation failed: %s", resp.Message)
    }
    
    return resp.Profile, nil    return resp.Profile, nil
}

// Get trade profile
func (c *TradeProfileClient) GetTradeProfile(ctx context.Context, userID, orgID string) (*tradeprofilePb.TradeProfile, error) {
    if c.client == nil {
        return mockTradeProfileByID(userID), nil
    }
    
    req := &tradeprofilePb.GetTradeProfileRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetTradeProfile(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get trade profile failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Profile, nil
}

// Update trade profile
func (c *TradeProfileClient) UpdateTradeProfile(ctx context.Context, userID, orgID string, displayName, bio *string, experienceLevel *tradeprofilePb.TradingExperience, riskTolerance *tradeprofilePb.RiskTolerance) (*tradeprofilePb.TradeProfile, error) {
    if c.client == nil {
        return mockTradeProfileUpdate(userID), nil
    }
    
    req := &tradeprofilePb.UpdateTradeProfileRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    if displayName != nil {
        req.DisplayName = &tradeprofilePb.UpdateTradeProfileRequest_DisplayName{DisplayName: *displayName}
    }
    if bio != nil {
        req.Bio = &tradeprofilePb.UpdateTradeProfileRequest_Bio{Bio: *bio}
    }
    if experienceLevel != nil {
        req.ExperienceLevel = &tradeprofilePb.UpdateTradeProfileRequest_ExperienceLevel{ExperienceLevel: *experienceLevel}
    }
    if riskTolerance != nil {
        req.RiskTolerance = &tradeprofilePb.UpdateTradeProfileRequest_RiskTolerance{RiskTolerance: *riskTolerance}
    }
    
    resp, err := c.client.UpdateTradeProfile(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update trade profile failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("trade profile update failed: %s", resp.Message)
    }
    
    return resp.Profile, nil
}

// Update trading preferences
func (c *TradeProfileClient) UpdateTradingPreferences(ctx context.Context, userID, orgID string, preferences *tradeprofilePb.TradingPreferences) (*tradeprofilePb.TradingPreferences, error) {
    if c.client == nil {
        return mockTradingPreferences(), nil
    }
    
    req := &tradeprofilePb.UpdateTradingPreferencesRequest{
        UserId:      userID,
        OrganizationId: orgID,
        Preferences: preferences,
    }
    
    resp, err := c.client.UpdateTradingPreferences(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update trading preferences failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("preferences update failed")
    }
    
    return resp.Preferences, nil
}

// Get trading preferences
func (c *TradeProfileClient) GetTradingPreferences(ctx context.Context, userID, orgID string) (*tradeprofilePb.TradingPreferences, error) {
    if c.client == nil {
        return mockTradingPreferences(), nil
    }
    
    req := &tradeprofilePb.GetTradingPreferencesRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetTradingPreferences(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get trading preferences failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Preferences, nil
}

// Update risk settings
func (c *TradeProfileClient) UpdateRiskSettings(ctx context.Context, userID, orgID string, settings *tradeprofilePb.RiskSettings) (*tradeprofilePb.RiskSettings, error) {
    if c.client == nil {
        return mockRiskSettings(), nil
    }
    
    req := &tradeprofilePb.UpdateRiskSettingsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Settings:       settings,
    }
    
    resp, err := c.client.UpdateRiskSettings(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("update risk settings failed: %w", err)
    }
    
    if !resp.Updated {
        return nil, fmt.Errorf("risk settings update failed")
    }
    
    return resp.Settings, nil
}

// Get risk settings
func (c *TradeProfileClient) GetRiskSettings(ctx context.Context, userID, orgID string) (*tradeprofilePb.RiskSettings, error) {
    if c.client == nil {
        return mockRiskSettings(), nil
    }
    
    req := &tradeprofilePb.GetRiskSettingsRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetRiskSettings(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get risk settings failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Settings, nil
}

// Check risk limits for a potential trade
func (c *TradeProfileClient) CheckRiskLimits(ctx context.Context, userID, orgID, assetPair, side, quantity, price string, leverage float64) (bool, []string, error) {
    if c.client == nil {
        return true, nil, nil
    }
    
    req := &tradeprofilePb.CheckRiskLimitsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        AssetPair:      assetPair,
        Side:           side,
        Quantity:       quantity,
        Price:          price,
        Leverage:       leverage,
    }
    
    resp, err := c.client.CheckRiskLimits(c.getContext(ctx), req)
    if err != nil {
        return false, nil, fmt.Errorf("check risk limits failed: %w", err)
    }
    
    return resp.Allowed, resp.Violations, nil
}

// Create an API key for programmatic trading
func (c *TradeProfileClient) CreateAPIKey(ctx context.Context, userID, orgID, name string, permissions, allowedAssets, allowedIPs []string, expiresAt *time.Time) (*tradeprofilePb.APIKey, error) {
    if c.client == nil {
        return mockAPIKey(), nil
    }
    
    req := &tradeprofilePb.CreateAPIKeyRequest{
        UserId:            userID,
        OrganizationId:    orgID,
        Name:              name,
        Permissions:       permissions,
        AllowedAssets:     allowedAssets,
        AllowedIpAddresses: allowedIPs,
    }
    
    if expiresAt != nil {
        req.ExpiresAt = timestamppb.New(*expiresAt)
    }
    
    resp, err := c.client.CreateAPIKey(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create API key failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("API key creation failed: %s", resp.Message)
    }
    
    return resp.ApiKey, nil
}

// Get all API keys for a user
func (c *TradeProfileClient) GetAPIKeys(ctx context.Context, userID, orgID string, includeInactive bool) ([]*tradeprofilePb.APIKey, error) {
    if c.client == nil {
        return []*tradeprofilePb.APIKey{mockAPIKey()}, nil
    }
    
    req := &tradeprofilePb.GetAPIKeysRequest{
        UserId:          userID,
        OrganizationId:  orgID,
        IncludeInactive: includeInactive,
    }
    
    resp, err := c.client.GetAPIKeys(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get API keys failed: %w", err)
    }
    
    return resp.ApiKeys, nil
}

// Revoke an API key
func (c *TradeProfileClient) RevokeAPIKey(ctx context.Context, userID, orgID, keyID string) error {
    if c.client == nil {
        return nil
    }
    
    req := &tradeprofilePb.RevokeAPIKeyRequest{
        UserId:         userID,
        OrganizationId: orgID,
        KeyId:          keyID,
    }
    
    resp, err := c.client.RevokeAPIKey(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("revoke API key failed: %w", err)
    }
    
    if !resp.Revoked {
        return fmt.Errorf("API key revocation failed: %s", resp.Message)
    }
    
    return nil
}

// Start a trading session
func (c *TradeProfileClient) StartTradingSession(ctx context.Context, userID, orgID, deviceID, deviceName, ipAddress, userAgent string) (*tradeprofilePb.TradingSession, error) {
    if c.client == nil {
        return mockTradingSession(), nil
    }
    
    req := &tradeprofilePb.StartTradingSessionRequest{
        UserId:         userID,
        OrganizationId: orgID,
        DeviceId:       deviceID,
        DeviceName:     deviceName,
        IpAddress:      ipAddress,
        UserAgent:      userAgent,
    }
    
    resp, err := c.client.StartTradingSession(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("start trading session failed: %w", err)
    }
    
    if !resp.Started {
        return nil, fmt.Errorf("session start failed: %s", resp.Message)
    }
    
    return resp.Session, nil
}

// End a trading session
func (c *TradeProfileClient) EndTradingSession(ctx context.Context, userID, orgID, sessionID string) error {
    if c.client == nil {
        return nil
    }
    
    req := &tradeprofilePb.EndTradingSessionRequest{
        UserId:         userID,
        OrganizationId: orgID,
        SessionId:      sessionID,
    }
    
    resp, err := c.client.EndTradingSession(c.getContext(ctx), req)
    if err != nil {
        return fmt.Errorf("end trading session failed: %w", err)
    }
    
    if !resp.Ended {
        return fmt.Errorf("session end failed: %s", resp.Message)
    }
    
    return nil
}

// Get active trading sessions
func (c *TradeProfileClient) GetActiveSessions(ctx context.Context, userID, orgID string) ([]*tradeprofilePb.TradingSession, error) {
    if c.client == nil {
        return []*tradeprofilePb.TradingSession{mockTradingSession()}, nil
    }
    
    req := &tradeprofilePb.GetActiveSessionsRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetActiveSessions(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get active sessions failed: %w", err)
    }
    
    return resp.Sessions, nil
}

// Create a trading strategy (bot config)
func (c *TradeProfileClient) CreateStrategy(ctx context.Context, userID, orgID, name, description, strategyType, riskLevel string, config *structpb.Struct, assetPairs []string) (*tradeprofilePb.TradingStrategy, error) {
    if c.client == nil {
        return mockTradingStrategy(), nil
    }
    
    req := &tradeprofilePb.CreateStrategyRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Name:           name,
        Description:    description,
        StrategyType:   strategyType,
        Configuration:  config,
        RiskLevel:      riskLevel,
        AssetPairs:     assetPairs,
    }
    
    resp, err := c.client.CreateStrategy(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create strategy failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("strategy creation failed: %s", resp.Message)
    }
    
    return resp.Strategy, nil
}

// Get user's trading strategies
func (c *TradeProfileClient) GetStrategies(ctx context.Context, userID, orgID string, includeInactive bool, strategyType string) ([]*tradeprofilePb.TradingStrategy, error) {
    if c.client == nil {
        return []*tradeprofilePb.TradingStrategy{mockTradingStrategy()}, nil
    }
    
    req := &tradeprofilePb.GetStrategiesRequest{
        UserId:          userID,
        OrganizationId:  orgID,
        IncludeInactive: includeInactive,
        StrategyType:    strategyType,
    }
    
    resp, err := c.client.GetStrategies(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get strategies failed: %w", err)
    }
    
    return resp.Strategies, nil
}

// Activate a trading strategy
func (c *TradeProfileClient) ActivateStrategy(ctx context.Context, userID, orgID, strategyID string) (*tradeprofilePb.TradingStrategy, error) {
    if c.client == nil {
        return mockTradingStrategy(), nil
    }
    
    req := &tradeprofilePb.ActivateStrategyRequest{
        UserId:         userID,
        OrganizationId: orgID,
        StrategyId:     strategyID,
    }
    
    resp, err := c.client.ActivateStrategy(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("activate strategy failed: %w", err)
    }
    
    if !resp.Activated {
        return nil, fmt.Errorf("strategy activation failed")
    }
    
    return resp.Strategy, nil
}

// Deactivate a trading strategy
func (c *TradeProfileClient) DeactivateStrategy(ctx context.Context, userID, orgID, strategyID string) (*tradeprofilePb.TradingStrategy, error) {
    if c.client == nil {
        return mockTradingStrategy(), nil
    }
    
    req := &tradeprofilePb.DeactivateStrategyRequest{
        UserId:         userID,
        OrganizationId: orgID,
        StrategyId:     strategyID,
    }
    
    resp, err := c.client.DeactivateStrategy(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("deactivate strategy failed: %w", err)
    }
    
    if !resp.Deactivated {
        return nil, fmt.Errorf("strategy deactivation failed")
    }
    
    return resp.Strategy, nil
}

// Create an alert configuration
func (c *TradeProfileClient) CreateAlertConfig(ctx context.Context, userID, orgID, name, alertType, condition, value, assetPair, indicator string, notificationMethods []string, webhookURL string) (*tradeprofilePb.AlertConfig, error) {
    if c.client == nil {
        return mockAlertConfig(), nil
    }
    
    req := &tradeprofilePb.CreateAlertConfigRequest{
        UserId:               userID,
        OrganizationId:       orgID,
        Name:                 name,
        AlertType:            alertType,
        Condition:            condition,
        Value:                value,
        AssetPair:            assetPair,
        Indicator:            indicator,
        NotificationMethods:  notificationMethods,
        WebhookUrl:           webhookURL,
    }
    
    resp, err := c.client.CreateAlertConfig(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("create alert config failed: %w", err)
    }
    
    if !resp.Created {
        return nil, fmt.Errorf("alert config creation failed")
    }
    
    return resp.Alert, nil
}

// Get alert configurations
func (c *TradeProfileClient) GetAlertConfigs(ctx context.Context, userID, orgID string, includeInactive bool, alertType string) ([]*tradeprofilePb.AlertConfig, error) {
    if c.client == nil {
        return []*tradeprofilePb.AlertConfig{mockAlertConfig()}, nil
    }
    
    req := &tradeprofilePb.GetAlertConfigsRequest{
        UserId:          userID,
        OrganizationId:  orgID,
        IncludeInactive: includeInactive,
        AlertType:       alertType,
    }
    
    resp, err := c.client.GetAlertConfigs(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get alert configs failed: %w", err)
    }
    
    return resp.Alerts, nil
}

// Set trading limits
func (c *TradeProfileClient) SetTradingLimits(ctx context.Context, userID, orgID string, limits *tradeprofilePb.TradingLimits) (*tradeprofilePb.TradingLimits, error) {
    if c.client == nil {
        return mockTradingLimits(), nil
    }
    
    req := &tradeprofilePb.SetTradingLimitsRequest{
        UserId:         userID,
        OrganizationId: orgID,
        Limits:         limits,
    }
    
    resp, err := c.client.SetTradingLimits(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("set trading limits failed: %w", err)
    }
    
    if !resp.Set {
        return nil, fmt.Errorf("set trading limits failed")
    }
    
    return resp.Limits, nil
}

// Get current usage statistics
func (c *TradeProfileClient) GetCurrentUsage(ctx context.Context, userID, orgID string) (*tradeprofilePb.CurrentUsage, error) {
    if c.client == nil {
        return mockCurrentUsage(), nil
    }
    
    req := &tradeprofilePb.GetCurrentUsageRequest{
        UserId:         userID,
        OrganizationId: orgID,
    }
    
    resp, err := c.client.GetCurrentUsage(c.getContext(ctx), req)
    if err != nil {
        return nil, fmt.Errorf("get current usage failed: %w", err)
    }
    
    if !resp.Found {
        return nil, nil
    }
    
    return resp.Usage, nil
}

// Mock functions for testing
func mockTradeProfile(req *tradeprofilePb.CreateTradeProfileRequest) *tradeprofilePb.TradeProfile {
    return &tradeprofilePb.TradeProfile{
        ProfileId:        "mock-profile-id",
        UserId:           req.UserId,
        DisplayName:      req.DisplayName,
        ExperienceLevel:  req.ExperienceLevel,
        RiskTolerance:    req.RiskTolerance,
        IsActive:         true,
        CreatedAt:        timestamppb.Now(),
        UpdatedAt:        timestamppb.Now(),
    }
}

func mockTradeProfileByID(userID string) *tradeprofilePb.TradeProfile {
    return &tradeprofilePb.TradeProfile{
        ProfileId:       "mock-profile-id",
        UserId:          userID,
        DisplayName:     "Test User",
        ExperienceLevel: tradeprofilePb.TradingExperience_INTERMEDIATE,
        RiskTolerance:   tradeprofilePb.RiskTolerance_MODERATE,
        IsActive:        true,
    }
}

func mockTradeProfileUpdate(userID string) *tradeprofilePb.TradeProfile {
    return &tradeprofilePb.TradeProfile{
        ProfileId:       "mock-profile-id",
        UserId:          userID,
        DisplayName:     "Updated Name",
        ExperienceLevel: tradeprofilePb.TradingExperience_ADVANCED,
        RiskTolerance:   tradeprofilePb.RiskTolerance_AGGRESSIVE,
        IsActive:        true,
        UpdatedAt:       timestamppb.Now(),
    }
}

func mockTradingPreferences() *tradeprofilePb.TradingPreferences {
    return &tradeprofilePb.TradingPreferences{
        DefaultAssetPair:     "TX/USD",
        DefaultOrderType:     tradeprofilePb.OrderTypePreference_LIMIT_ONLY,
        DefaultTimeInForce:   "GTC",
        EnableMarketOrders:   true,
        EnableStopOrders:     true,
        EnableMarginTrading:  false,
        DefaultLeverage:      1.0,
        QuoteCurrency:        "USD",
        Theme:                "dark",
        Language:             "en",
        EmailNotifications:   true,
        PushNotifications:    true,
    }
}

func mockRiskSettings() *tradeprofilePb.RiskSettings {
    return &tradeprofilePb.RiskSettings{
        MaxPositionSizePercent:     20.0,
        MaxDailyLossPercent:        10.0,
        MaxDrawdownPercent:         25.0,
        MaxLeverage:                3.0,
        EnableStopLossDefault:      true,
        DefaultStopLossPercent:     5.0,
        EnableTakeProfitDefault:    true,
        DefaultTakeProfitPercent:   15.0,
        RequireConfirmLargeTrades:  true,
        LargeTradeThreshold:        "10000.00",
        EnableCircuitBreakers:      true,
        CircuitBreakerTrades:       5,
        CircuitBreakerDurationSeconds: 300,
    }
}

func mockAPIKey() *tradeprofilePb.APIKey {
    return &tradeprofilePb.APIKey{
        KeyId:       "mock-key-id",
        Name:        "Test API Key",
        ApiKey:      "tx_test_xxxxx",
        Permissions: []string{"trade", "read"},
        IsActive:    true,
        CreatedAt:   timestamppb.Now(),
    }
}

func mockTradingSession() *tradeprofilePb.TradingSession {
    return &tradeprofilePb.TradingSession{
        SessionId:        "mock-session-id",
        DeviceName:       "Chrome Browser",
        IpAddress:        "192.168.1.1",
        IsActive:         true,
        StartedAt:        timestamppb.Now(),
        LastActivityAt:   timestamppb.Now(),
        ExpiresAt:        timestamppb.New(time.Now().Add(30 * time.Minute)),
    }
}

func mockTradingStrategy() *tradeprofilePb.TradingStrategy {
    return &tradeprofilePb.TradingStrategy{
        StrategyId:   "mock-strategy-id",
        Name:         "Grid Trading Bot",
        StrategyType: "grid",
        IsActive:     true,
        RiskLevel:    "moderate",
        AssetPairs:   []string{"TX/USD", "BTC/USD"},
        CreatedAt:    timestamppb.Now(),
    }
}

func mockAlertConfig() *tradeprofilePb.AlertConfig {
    return &tradeprofilePb.AlertConfig{
        AlertId:              "mock-alert-id",
        Name:                 "Price Alert",
        AlertType:            "price",
        Condition:            "above",
        Value:                "100.00",
        AssetPair:            "TX/USD",
        NotificationMethods:  []string{"email", "push"},
        IsActive:             true,
        CreatedAt:            timestamppb.Now(),
    }
}

func mockTradingLimits() *tradeprofilePb.TradingLimits {
    return &tradeprofilePb.TradingLimits{
        DailyTradeVolumeLimit:   "100000.00",
        WeeklyTradeVolumeLimit:  "500000.00",
        MonthlyTradeVolumeLimit: "2000000.00",
        DailyTradeCountLimit:    100,
        WeeklyTradeCountLimit:   500,
        MaxOrderSize:            "10000.00",
        MinOrderSize:            "10.00",
        MaxPositionValue:        "50000.00",
    }
}

func mockCurrentUsage() *tradeprofilePb.CurrentUsage {
    return &tradeprofilePb.CurrentUsage{
        TodayVolume:     "25000.00",
        TodayTrades:     25,
        WeekVolume:      "150000.00",
        WeekTrades:      150,
        MonthVolume:     "500000.00",
        MonthTrades:     500,
        CurrentDrawdownPercent: 2.5,
        CurrentLossToday:       "500.00",
    }
}

// Example usage
func main() {
    client, err := NewTradeProfileClient("trade-profile-store:50074")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    
    ctx := context.Background()
    orgID := "org-123"
    userID := "user-789"
    
    // Create a trade profile
    profile, err := client.CreateTradeProfile(ctx, &tradeprofilePb.CreateTradeProfileRequest{
        UserId:          userID,
        OrganizationId:  orgID,
        DisplayName:     "Advanced Trader",
        Bio:             "Experienced crypto trader",
        ExperienceLevel: tradeprofilePb.TradingExperience_ADVANCED,
        RiskTolerance:   tradeprofilePb.RiskTolerance_AGGRESSIVE,
    })
    if err != nil {
        log.Printf("Failed to create profile: %v", err)
    } else {
        log.Printf("Profile created: %s", profile.ProfileId)
    }
    
    // Update trading preferences
    prefs := &tradeprofilePb.TradingPreferences{
        DefaultAssetPair:    "TX/USD",
        DefaultOrderType:    tradeprofilePb.OrderTypePreference_LIMIT_ONLY,
        DefaultTimeInForce:  "GTC",
        EnableMarketOrders:  true,
        EnableStopOrders:    true,
        QuoteCurrency:       "USD",
        Theme:               "dark",
        EmailNotifications:  true,
        PushNotifications:   true,
    }
    
    updatedPrefs, err := client.UpdateTradingPreferences(ctx, userID, orgID, prefs)
    if err != nil {
        log.Printf("Failed to update preferences: %v", err)
    } else {
        log.Printf("Preferences updated: %s", updatedPrefs.DefaultAssetPair)
    }
    
    // Update risk settings
    riskSettings := &tradeprofilePb.RiskSettings{
        MaxPositionSizePercent:    15.0,
        MaxDailyLossPercent:       8.0,
        MaxDrawdownPercent:        20.0,
        MaxLeverage:               2.0,
        EnableStopLossDefault:     true,
        DefaultStopLossPercent:    5.0,
        EnableTakeProfitDefault:   true,
        DefaultTakeProfitPercent:  12.0,
        RequireConfirmLargeTrades: true,
        LargeTradeThreshold:       "5000.00",
    }
    
    settings, err := client.UpdateRiskSettings(ctx, userID, orgID, riskSettings)
    if err != nil {
        log.Printf("Failed to update risk settings: %v", err)
    } else {
        log.Printf("Risk settings updated: max position %.1f%%", settings.MaxPositionSizePercent)
    }
    
    // Check risk limits before a trade
    allowed, violations, err := client.CheckRiskLimits(ctx, userID, orgID, "TX/USD", "buy", "1000.00", "50.00", 1.0)
    if err != nil {
        log.Printf("Failed to check risk limits: %v", err)
    } else if allowed {
        log.Printf("Trade is allowed")
    } else {
        log.Printf("Trade blocked: %v", violations)
    }
    
    // Create API key for bot trading
    apiKey, err := client.CreateAPIKey(ctx, userID, orgID, "Trading Bot", 
        []string{"trade", "read"}, []string{"TX", "USD"}, []string{"192.168.1.0/24"}, nil)
    if err != nil {
        log.Printf("Failed to create API key: %v", err)
    } else {
        log.Printf("API Key created: %s (secret: %s)", apiKey.ApiKey, apiKey.ApiSecret)
    }
    
    // Start a trading session
    session, err := client.StartTradingSession(ctx, userID, orgID, "device-123", "Chrome on Windows", "192.168.1.100", "Mozilla/5.0...")
    if err != nil {
        log.Printf("Failed to start session: %v", err)
    } else {
        log.Printf("Session started: %s", session.SessionId)
        
        // End session when done
        defer client.EndTradingSession(ctx, userID, orgID, session.SessionId)
    }
    
    // Create a grid trading strategy
    config := &structpb.Struct{
        Fields: map[string]*structpb.Value{
            "upper_price":   structpb.NewStringValue("100.00"),
            "lower_price":   structpb.NewStringValue("50.00"),
            "grid_levels":   structpb.NewNumberValue(10),
            "quantity_per_grid": structpb.NewStringValue("100.00"),
        },
    }
    
    strategy, err := client.CreateStrategy(ctx, userID, orgID, "Grid Bot", "Automated grid trading", "grid", "moderate", config, []string{"TX/USD"})
    if err != nil {
        log.Printf("Failed to create strategy: %v", err)
    } else {
        log.Printf("Strategy created: %s", strategy.Name)
        
        // Activate the strategy
        activated, err := client.ActivateStrategy(ctx, userID, orgID, strategy.StrategyId)
        if err != nil {
            log.Printf("Failed to activate strategy: %v", err)
        } else {
            log.Printf("Strategy activated: %s", activated.Name)
        }
    }
    
    // Create a price alert
    alert, err := client.CreateAlertConfig(ctx, userID, orgID, "TX Price Alert", "price", "above", "100.00", "TX/USD", "", []string{"email", "push"}, "")
    if err != nil {
        log.Printf("Failed to create alert: %v", err)
    } else {
        log.Printf("Alert created: %s", alert.Name)
    }
    
    // Get current usage statistics
    usage, err := client.GetCurrentUsage(ctx, userID, orgID)
    if err != nil {
        log.Printf("Failed to get usage: %v", err)
    } else {
        log.Printf("Today's trading: $%s volume, %d trades", usage.TodayVolume, usage.TodayTrades)
        log.Printf("Current drawdown: %.1f%%", usage.CurrentDrawdownPercent)
    }
    
    // Get active sessions
    sessions, err := client.GetActiveSessions(ctx, userID, orgID)
    if err != nil {
        log.Printf("Failed to get sessions: %v", err)
    } else {
        log.Printf("Active sessions: %d", len(sessions))
    }
}
Save the file:

Ctrl+O, Enter, Ctrl+X

4. Trade Profile Docker Compose
bash
nano ~/dev/TXdocumentation/trade-profile/docker-compose.yml
yaml
version: '3.8'

services:
  trade-profile-service:
    image: sologenic/trade-profile-service:latest
    environment:
      - TRADE_PROFILE_SERVICE_PORT=50074
      - TRADE_PROFILE_STORE=trade-profile-store:50074
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=trade_profiles
      - POSTGRES_USER=trade_profile_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - VAULT_ADDR=http://vault:8200
      - MAX_ACTIVE_SESSIONS=5
      - SESSION_TIMEOUT_MINUTES=30
      - MAX_API_KEYS_PER_USER=10
      - RATE_LIMIT_REQUESTS=1000
      - ENABLE_2FA_REQUIRED=false
      - MAX_DAILY_TRADING_LIMIT=1000000
      - LOG_LEVEL=info
    ports:
      - "50074:50074"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
      - vault
    healthcheck:
      test: ["CMD", "grpc_health_probe", "-addr=:50074"]
      interval: 30s
      timeout: 10s
      retries: 3

  trade-profile-store:
    image: sologenic/trade-profile-store:latest
    environment:
      - TRADE_PROFILE_STORE_PORT=50075
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=trade_profiles
      - POSTGRES_USER=trade_profile_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - VAULT_ADDR=http://vault:8200
    ports:
      - "50075:50075"
    networks:
      - internal
    depends_on:
      - postgres
      - redis
      - vault

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=trade_profiles
      - POSTGRES_USER=trade_profile_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U trade_profile_user -d trade_profiles"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - internal
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  vault:
    image: vault:1.15
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=${VAULT_TOKEN}
      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    cap_add:
      - IPC_LOCK
    ports:
      - "8200:8200"
    networks:
      - internal
    healthcheck:
      test: ["CMD", "vault", "status"]
      interval: 30s
      timeout: 10s
      retries: 5

networks:
  internal:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
Save the file:

Ctrl+O, Enter, Ctrl+X

5. Trade Profile Environment File
bash
nano ~/dev/TXdocumentation/trade-profile/.env
bash
# Database Configuration
DB_PASSWORD=your_secure_password

# Vault Configuration
VAULT_TOKEN=dev-only-token

# Service Configuration
TRADE_PROFILE_STORE=trade-profile-store:50075
TRADE_PROFILE_STORE_TESTING=FALSE

# Session Configuration
MAX_ACTIVE_SESSIONS=5
SESSION_TIMEOUT_MINUTES=30

# API Key Configuration
MAX_API_KEYS_PER_USER=10

# Rate Limiting
RATE_LIMIT_REQUESTS=1000

# Security
ENABLE_2FA_REQUIRED=false
MAX_DAILY_TRADING_LIMIT=1000000

# Logging
LOG_LEVEL=info

