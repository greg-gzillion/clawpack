# Fungible Tokens - Asset FT Module

## Overview
The `assetft` module allows public users of the blockchain to create and manage fungible tokens on TX blockchain with advanced features like freezing, whitelisting, clawback, and IBC compatibility.

## Architecture: wbank Module Integration
TX uses the native Cosmos SDK bank module wrapped into the `wbank` module to intercept send operations and inject custom logic from the assetft module.
┌─────────────────────────────────────┐
│ assetft Module │
│ (Custom logic, features, ACL) │
└──────────────┬──────────────────────┘
│ intercepts
▼
┌─────────────────────────────────────┐
│ wbank Module │
│ (Wraps bank module) │
└──────────────┬──────────────────────┘
│
▼
┌─────────────────────────────────────┐
│ Cosmos SDK Bank Module │
│ (Balance tracking, transfers) │
└─────────────────────────────────────┘

text

**Important**: Data is split between modules:
- **assetft**: Features, freezing, whitelisting, admin roles
- **bank**: Balances, total supply

## Token Creation (Issue)

### Denom Naming Convention
Denoms are created as: `{subunit}-{issuer_address}`

**Example**:
- Subunit: `satoshi`
- Issuer: `core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8`
- Denom: `satoshi-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8`

### Symbol and Precision
- **Symbol**: Display name (e.g., BTC)
- **Precision**: Decimal places (e.g., 8 for satoshis)
- Formula: `1 BTC = 10^8 satoshi`

### Issuance Fee
When issuing a token, an issuance fee is paid on top of execution fee and burned. Amount controlled by governance.

## Token Features (Immutable After Issuance)

| Feature | Description |
|---------|-------------|
| `minting` | Admin can mint additional tokens |
| `burning` | Holders can burn tokens |
| `freezing` | Freeze individual accounts |
| `whitelisting` | Restrict to approved addresses |
| `ibc` | Cross-chain transfers |
| `block smart contracts` | Prevent transfers to contracts |
| `clawback` | Admin recovery of tokens |
| `transferring admin` | Change token admin |
| `clear admin` | Remove admin permanently |
| `extension` | Smart Contract override |

## Token Features Details

### Minting
If enabled, admin can mint new tokens. All minted tokens go to admin account.

### Burning
- **Admin**: Can burn their own tokens regardless of feature
- **Holders**: Can burn their tokens if feature enabled

### Burn Rate
Value between 0 and 1:
- On each transfer, additional tokens burned from sender
- Calculated: `burn_amount = transfer_amount × burn_rate` (rounded up)
- Applied to IBC transfers if IBC enabled
- Not applied when sender is smart contract

### Send Commission Rate
Value between 0 and 1:
- Calculated amount transferred to admin account
- Applied to IBC transfers if IBC enabled
- Not applied when sender is smart contract

### Freezing/Unfreeze
If freezing feature enabled:
- Admin can freeze accounts up to specific amount
- Frozen amount can exceed current balance
- User can only send tokens above frozen amount
- Admin cannot freeze own account
- Cannot burn frozen tokens if both features enabled

**Example**:
Account holds: 800 ABC
Frozen: 1000 ABC
Result: Cannot send any (800 ≤ 1000)

text
Account receives +400 ABC
New balance: 1200 ABC
Frozen: 1000 ABC
Result: Can send 200 ABC

text

### Global Freeze/Unfreeze
- Admin can freeze ALL transfers of token
- Only admin can send during global freeze
- Affects IBC transfers if enabled

### Whitelisting
If whitelisting enabled:
- Admin sets whitelisted limit per account
- Admin account whitelisted to infinity
- Account can only receive up to whitelisted limit

**Example**:
Whitelisted limit: 500 ABC
Current balance: 300 ABC
Can receive: Up to 200 ABC

text

### Unlimited Freezing/Whitelisting
To freeze/unlimited amount:
1. Check total supply
2. Freeze/whitelist amount ≥ total supply
3. Account for future minting

### IBC Compatibility
If IBC feature enabled:
- Tokens can be transferred to/from other chains
- Uses Cosmos IBC protocol
- If disabled, tokens never leave TX chain

### Block Smart Contracts
If enabled:
- Tokens cannot be sent to smart contracts
- Can be issued from smart contract and sent back
- Cannot send to other contracts

### Clawback
If clawback enabled:
- Admin can confiscate up to user's balance
- Cannot clawback from own account
- Cannot clawback from module accounts
- **Warning**: Clawback from escrow breaks IBC

### Transferring Admin
- Admin role can be transferred to another account
- All privileges transfer with role
- Denom always includes original issuer address

### Clear Admin
- Remove admin permanently
- No one has special privileges after
- Token becomes fully decentralized

### Extension
Powerful feature allowing smart contract to override token functionality.

**Sudo Message Structure**:
```rust
#[cw_serde]
pub enum SudoMsg {
    ExtensionTransfer {
        recipient: String,
        sender: String,
        transfer_amount: Uint128,
        commission_amount: Uint128,
        burn_amount: Uint128,
        context: TransferContext,
    },
}

#[cw_serde]
pub struct TransferContext {
    sender_is_smart_contract: bool,
    recipient_is_smart_contract: bool,
    ibc_purpose: IBCPurpose,
}
Context Fields:

Field	Description
recipient	Account receiving amount
sender	Account sending amount
transfer_amount	Amount to send
commission_amount	Amount × commission rate
burn_amount	Amount × burn rate
sender_is_smart_contract	Transfer from contract
recipient_is_smart_contract	Transfer to contract
ibc_purpose	IBC transfer type
⚠️ Note: Extension not compatible with IBC or Block Smart Contract features.

DEX Integration
DEX Block: Prevent token trading on DEX

DEX Whitelisted Denoms: Specify allowed trading pairs

DEX Unified Ref Amount: Reference amount for trading

Proto Definitions
For detailed structure, refer to:

events.proto

tx.proto

query.proto

params.proto
