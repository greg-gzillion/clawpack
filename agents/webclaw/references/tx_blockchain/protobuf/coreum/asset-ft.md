# Coreum Asset FT (Fungible Tokens) - Protobuf Documentation

## Service: Msg

| Method | Request | Response | Description |
|--------|---------|----------|-------------|
| Issue | MsgIssue | EmptyResponse | Issue a new fungible token |
| Mint | MsgMint | EmptyResponse | Mint new fungible tokens |
| Burn | MsgBurn | EmptyResponse | Burn fungible tokens |
| Freeze | MsgFreeze | EmptyResponse | Freeze a portion of tokens in an account |
| Unfreeze | MsgUnfreeze | EmptyResponse | Unfreeze frozen tokens |
| SetFrozen | MsgSetFrozen | EmptyResponse | Set absolute frozen amount |
| GloballyFreeze | MsgGloballyFreeze | EmptyResponse | Freeze token globally |
| GloballyUnfreeze | MsgGloballyUnfreeze | EmptyResponse | Unfreeze token globally |
| Clawback | MsgClawback | EmptyResponse | Confiscate tokens to admin |
| SetWhitelistedLimit | MsgSetWhitelistedLimit | EmptyResponse | Set whitelist limit |
| TransferAdmin | MsgTransferAdmin | EmptyResponse | Change token admin |
| ClearAdmin | MsgClearAdmin | EmptyResponse | Remove token admin |
| UpdateParams | MsgUpdateParams | EmptyResponse | Update module parameters |
| UpdateDEXUnifiedRefAmount | MsgUpdateDEXUnifiedRefAmount | EmptyResponse | Update DEX unified ref amount |
| UpdateDEXWhitelistedDenoms | MsgUpdateDEXWhitelistedDenoms | EmptyResponse | Update DEX whitelisted denoms |

## Service: Query

| Method | Request | Response | HTTP Endpoint |
|--------|---------|----------|---------------|
| Params | QueryParamsRequest | QueryParamsResponse | `/coreum/asset/ft/v1/params` |
| Tokens | QueryTokensRequest | QueryTokensResponse | `/coreum/asset/ft/v1/tokens` |
| Token | QueryTokenRequest | QueryTokenResponse | `/coreum/asset/ft/v1/tokens/{denom}` |
| TokenUpgradeStatuses | QueryTokenUpgradeStatusesRequest | QueryTokenUpgradeStatusesResponse | `/coreum/asset/ft/v1/tokens/{denom}/upgrade-statuses` |
| Balance | QueryBalanceRequest | QueryBalanceResponse | `/coreum/asset/ft/v1/accounts/{account}/balances/summary/{denom}` |
| FrozenBalances | QueryFrozenBalancesRequest | QueryFrozenBalancesResponse | `/coreum/asset/ft/v1/accounts/{account}/balances/frozen` |
| FrozenBalance | QueryFrozenBalanceRequest | QueryFrozenBalanceResponse | `/coreum/asset/ft/v1/accounts/{account}/balances/frozen/{denom}` |
| WhitelistedBalances | QueryWhitelistedBalancesRequest | QueryWhitelistedBalancesResponse | `/coreum/asset/ft/v1/accounts/{account}/balances/whitelisted` |
| WhitelistedBalance | QueryWhitelistedBalanceRequest | QueryWhitelistedBalanceResponse | `/coreum/asset/ft/v1/accounts/{account}/balances/whitelisted/{denom}` |
| DEXSettings | QueryDEXSettingsRequest | QueryDEXSettingsResponse | `/coreum/asset/ft/v1/tokens/{denom}/dex-settings` |

## Types

### Token

| Field | Type | Description |
|-------|------|-------------|
| denom | string | Token denomination |
| issuer | string | Issuer address |
| symbol | string | Token symbol |
| subunit | string | Smallest unit name |
| precision | uint32 | Decimal precision |
| description | string | Token description |
| globally_frozen | bool | Global freeze status |
| features | Feature[] | Enabled features |
| burn_rate | string | Burn rate (0-1) |
| send_commission_rate | string | Send commission rate (0-1) |
| version | uint32 | Token version |
| uri | string | Metadata URI |
| uri_hash | string | URI hash |
| extension_cw_address | string | CW extension address |
| admin | string | Admin address |
| dex_settings | DEXSettings | DEX configuration |

### DEXSettings

| Field | Type | Description |
|-------|------|-------------|
| unified_ref_amount | string | Approximate amount to buy 1 USD |
| whitelisted_denoms | string[] | List of denoms to trade with |

### Features (Enum)

| Name | Number | Description |
|------|--------|-------------|
| minting | 0 | Can mint new tokens |
| burning | 1 | Can burn tokens |
| freezing | 2 | Can freeze accounts |
| whitelisting | 3 | Whitelist feature |
| ibc | 4 | IBC transfer support |
| block_smart_contracts | 5 | Block SC interactions |
| clawback | 6 | Admin clawback |
| extension | 7 | CW extension support |
| dex_block | 8 | Block DEX trading |
| dex_whitelisted_denoms | 9 | DEX whitelist denoms |
| dex_order_cancellation | 10 | DEX order cancellation |
| dex_unified_ref_amount_change | 11 | Change unified ref amount |

### MsgIssue

| Field | Type | Description |
|-------|------|-------------|
| issuer | string | Issuer address |
| symbol | string | Token symbol |
| subunit | string | Smallest unit name |
| precision | uint32 | Decimal precision |
| initial_amount | string | Initial supply |
| description | string | Token description |
| features | Feature[] | Enabled features |
| burn_rate | string | Burn rate |
| send_commission_rate | string | Commission rate |
| uri | string | Metadata URI |
| uri_hash | string | URI hash |
| extension_settings | ExtensionIssueSettings | CW extension settings |
| dex_settings | DEXSettings | DEX settings |

### Events

| Event | Description |
|-------|-------------|
| EventIssued | Emitted on MsgIssue |
| EventAdminTransferred | Admin change |
| EventAdminCleared | Admin removed |
| EventFrozenAmountChanged | Frozen amount change |
| EventWhitelistedAmountChanged | Whitelist limit change |
| EventAmountClawedBack | Tokens confiscated |
| EventDEXSettingsChanged | DEX settings updated |
| EventDEXLockedAmountChanged | DEX locked amount change |
| EventDEXExpectedToReceiveAmountChanged | DEX expected amount change |
