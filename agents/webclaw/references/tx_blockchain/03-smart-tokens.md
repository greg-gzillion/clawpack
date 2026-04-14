# Smart Tokens on TX Blockchain

## Overview
Smart tokens are natively issued tokens on the TX chain that are wrapped around Smart Contracts. They are highly customizable and designed to be lightweight and flexible while remaining extendable.

## Key Characteristics
- **Native to chain** - Exist on chain's storage and memory
- **No Smart Contract calls** - Interacting doesn't require calling Smart Contract functions
- **Object-oriented** - Tokens are objects/classes inheriting characteristics from global token definition
- **Extendable** - Add non-deterministic Smart Contract-like functions for specific use cases

## Core Architecture
┌─────────────────────────────────────────────┐
│ Smart Token Class │
├─────────────────────────────────────────────┤
│ Default Functions (All tokens share) │
│ • Minting • Sending • Burning │
│ • Freezing • Clawback • Whitelisting │
├─────────────────────────────────────────────┤
│ Extensions (Optional Smart Contract) │
│ • Custom logic • Dividend distribution │
│ • Game mechanics • Interactive features │
└─────────────────────────────────────────────┘

text

## Default Features (Available for All Smart Tokens)

| Feature | Description |
|---------|-------------|
| **Issuance (Minting)** | Create new tokens |
| **Access Control List (ACL)** | Manage token permissions |
| **Burning** | Permanently remove tokens |
| **Freezing & Global Freezing** | Freeze individual accounts or all activity |
| **Whitelisting** | Restrict transfers to approved addresses |
| **Block Smart Contracts** | Prevent transfers to Smart Contracts |
| **Burn Rate** | Automatic burning on transfers |
| **Send Fee** | Tax on transfers |
| **IBC Compatibility** | Cross-chain transfers |
| **Smart Contract Integration** | Extend functionality |
| **Clawback** | Admin recovery of tokens |
| **Transferring Admin** | Change token admin |
| **Clear Admin** | Remove admin permanently |
| **Extension** | Smart Contract override functionality |

## ACL Flags (Immutable After Issuance)

Upon token issuance, the admin sets these flags which CANNOT be changed later:

| Flag | Description |
|------|-------------|
| `can_mint` | Ability to mint new tokens |
| `can_burn` | Ability to burn tokens |
| `can_whitelist` | Ability to manage whitelist |
| `can_partial_freeze` | Ability to freeze individual accounts |
| `can_global_freeze` | Ability to freeze all token activity |
| `can_send` | Ability to send tokens |
| `token_transferrable_using_ibc` | IBC transfer capability |
| `block_sending_to_smart_contracts` | Block Smart Contract transfers |
| `can_clawback` | Ability to clawback tokens |
| `token_managed_by_extension` | Smart Contract extension control |

## Benefits of Native Smart Tokens

### 1. Speed
Native tokens are predictable with known code execution, making transactions faster than Smart Contract calls.

### 2. Cost-Efficiency
- **Fixed fees** based on known computational complexity
- **Not dependent** on gas offered by caller
- **Bulk discounts** for transaction batches (SaaS-style pricing)

### 3. Predictability
- Execution time is known
- Cost is known
- Responses are deterministic
- Enables robust, bug-free applications

### 4. Security
- **Audited code** - Core implementation audited multiple times
- **Open source** - Publicly inspectable
- **No custom contract vulnerabilities** - Main features are safe
- **Only extensions need auditing** - Keep core features secure

### 5. Extendibility
Smart Contracts can be attached for customization:
- Dividend functions for tokenized shares
- Interactive NFTs that act like games
- Custom logic for specific use cases

## Feature Details

### Issuance
The initial phase where admin defines:
- Asset settings
- Initial amount
- Allowed features
- Default ACL

Initial amount minted to recipient account. Features set at issuance CANNOT be changed later.

### Minting
If `can_mint` flag is set:
- Admin can mint additional tokens
- Total supply increases
- If not set, supply is fixed forever

### Access Control List (ACL)
Flexible permission management:
```bash
# Example ACL configuration
can_administrate: account1
can_partial_freeze: account2
can_mint: account3, account4
can_burn: all
Burning
When enabled, authorized holders can burn tokens to reduce total supply.

Use Case: Tokenized shares - burning represents shares moved off-chain.

Freezing
Two types:

Partial Freeze: Freeze specific account balance

Global Freeze: Block all transfers except to admin

Use Case: Hold funds until conditions met (e.g., check clearing).

Whitelisting
Restrict token holders to KYC/AML verified accounts:

bash
# Whitelist configuration
- Admin defines allowed addresses
- Only whitelisted addresses can receive tokens
- Optional: `whitelist_everyone` flag
- Removed addresses keep existing balance but can't receive more
Use Cases: Stock shares, CBDC, regulated assets.

Block Smart Contracts
Prevent token transfers to Smart Contracts.

Use Case: Tokens not meant for DeFi applications.

Burn Rate
Define percentage of transferred amount to be burned:

Number between 0 and 1

Charged to sender in addition to transfer amount

Not applied to admin transactions

Send Fee
Define percentage transferred to admin (tax):

Number between 0 and 1

Charged to sender in addition to transfer amount

Not applied to admin transactions

IBC Compatibility
Assets can be transferred to/from IBC-supported chains:

Uses Cosmos SDK IBC capability

Tokens represented as tokenized versions on other chains

Requires proper relayers

Smart Contract Integration
Developers can extend Smart Token functionality through Smart Contracts:

Issue tokens

Mint/burn

Whitelist/blacklist

Freeze/unfreeze balances

Block/allow Smart Contract transfers

Clawback
Admin can confiscate tokens if feature enabled:

Cannot exceed user's balance

Cannot clawback from own account

Cannot clawback from module accounts

Warning: Clawback from escrow breaks IBC

Transferring Admin
Admin role can be transferred to another account:

All privileges transfer

Denom includes issuer address permanently

Clear Admin
Remove admin permanently:

No one has special privileges

Token becomes truly decentralized

Extension Feature (Advanced)
Extension allows Smart Contract to override token functionality:

Extension Message Structure
rust
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
Context Fields
Field	Description
recipient	Account receiving the amount
sender	Account sending the amount
transfer_amount	Amount to be sent
commission_amount	Amount × commission rate (if set)
burn_amount	Amount × burn rate (if set)
context.sender_is_smart_contract	Transfer from Smart Contract
context.recipient_is_smart_contract	Transfer to Smart Contract
context.ibc_purpose	IBC transfer type (outgoing/incoming/acknowledged/timed-out)
⚠️ Note: Extension is NOT compatible with IBC or Block Smart Contract features.

Token Types & Use Cases
Token Type	Features	Use Cases
Stablecoins	minting, burning, freezing, clawback	CBDC, fiat-backed
Crypto	IBC, transfer	Wrapped assets
NFTs	minting, burning, soulbound	Digital art, collectibles
Stocks	whitelisting, burning, clawback	Tokenized securities
CBDCs	whitelisting, freezing, clawback	Central bank digital currency
Game Assets	extension, minting, burning	In-game items, interactive NFTs
Quick Commands
Create Fungible Token
bash
txd tx assetft issue SYMBOL denom 6 1000000000 \
  --name "Token Name" \
  --from wallet \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  --features minting,burning,freezing,clawback \
  -y
Create NFT Class
bash
txd tx assetnft issue-class SYMBOL "Class Name" "Description" \
  --from wallet \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  --features soulbound \
  -y
Query Token Info
bash
txd query assetft token denom --node https://rpc.testnet-1.coreum.dev:443
Query NFT
bash
txd query assetnft nft --class-id CLASS-ID --id TOKEN-ID \
  --node https://rpc.testnet-1.coreum.dev:443
