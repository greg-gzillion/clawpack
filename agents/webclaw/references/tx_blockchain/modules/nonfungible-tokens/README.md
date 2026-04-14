# Non-Fungible Tokens - Asset NFT Module

## Overview
The `assetnft` module allows public users of the blockchain to create and manage non-fungible tokens (NFTs) on TX blockchain with advanced features like freezing, whitelisting, and soulbound capabilities.

## Architecture: wnft Module Integration
TX uses the Cosmos SDK nft module wrapped into the `wnft` module to intercept transfer operations and inject custom logic from the assetnft module.
┌─────────────────────────────────────┐
│ assetnft Module │
│ (Custom logic, features, ACL) │
└──────────────┬──────────────────────┘
│ intercepts
▼
┌─────────────────────────────────────┐
│ wnft Module │
│ (Wraps nft module) │
└──────────────┬──────────────────────┘
│
▼
┌─────────────────────────────────────┐
│ Cosmos SDK NFT Module │
│ (Class storage, ownership) │
└─────────────────────────────────────┘

text

**Important**: Data is split between modules:
- **assetnft**: Features, freezing, whitelisting, class definitions
- **nft**: Class metadata, token ownership, token data

## NFT Class Features

When issuing an NFT class, the admin configures these features (immutable after issuance):

| Feature | Description |
|---------|-------------|
| `minting` | Issuer can mint new NFTs in class (always enabled) |
| `burning` | Holders can burn their NFTs |
| `freezing` | Issuer can freeze specific NFTs |
| `whitelisting` | Restrict NFT recipients to approved accounts |
| `disable sending` | Prevent direct transfers (force DEX usage) |
| `soulbound` | NFTs cannot be transferred except by issuer |
| `update data` | Allow updating NFT metadata |

## Minting

### Minting Fee
- Fee charged when minting NFTs
- Configurable via governance parameters
- Current value: 0 (configurable)
- Burned after collection

### Data Types for NFT Minting

**DataBytes** (Immutable):
- Contains immutable data bytes array
- Cannot be changed after minting

**DataDynamic** (Mutable):
- Contains list of `DataDynamicItem`
- Each item can be updated by specified editors

**DataDynamicItem Structure**:
```rust
pub struct DataDynamicItem {
    pub data: Binary,
    pub editors: Vec<DataEditor>,  // admin, owner, or both
}
Data Editors:

Editor	Permission
admin	Class admin can update data
owner	NFT owner can update data
both	Both admin and owner can update
empty	No one can update (immutable)
Feature Details
Burning
If burning feature enabled:

NFT holders can burn their own NFTs

Issuer can burn NFTs regardless of feature

Burned NFTs are permanently removed

Freezing
If freezing feature enabled:

Issuer can freeze any NFT in the class

Frozen NFTs cannot be transferred

Issuer can unfreeze frozen NFTs

Useful for compliance or dispute resolution

Whitelisting
If whitelisting feature enabled:

Admin maintains whitelist per NFT

Only whitelisted accounts can receive specific NFTs

Admin can add/remove accounts from whitelist

Use Cases:

KYC/AML compliance

Regulated collectibles

Restricted distribution

Disable Sending
If disable sending feature enabled:

NFTs cannot be directly transferred between users

Forces transfers through DEX

Enables royalty enforcement

Creator always receives royalty on secondary sales

Soulbound
If soulbound feature enabled:

NFTs cannot be transferred by anyone except issuer

Perfect for:

Reputation tokens (TRUST/DONT_TRUST)

Identity credentials

Achievement badges

Governance weights (PHNX)

Prevents trading of non-transferable assets

Update Data
If update data feature enabled:

Data can be modified after minting

Editors control who can update:

Admin only

Owner only

Both admin and owner

No one (immutable)

Class Management
Issue Class
bash
txd tx assetnft issue-class SYMBOL "Class Name" "Description" \
  --from wallet \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  --features soulbound,freezing,whitelisting \
  -y
Mint NFT
bash
txd tx assetnft mint CLASS-ID TOKEN-ID \
  --from wallet \
  --uri "https://metadata.url/token.json" \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  -y
Update NFT Data
bash
txd tx assetnft update-data CLASS-ID TOKEN-ID \
  --data '{"key":"value"}' \
  --from wallet \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  -y
Freeze NFT
bash
txd tx assetnft freeze CLASS-ID TOKEN-ID \
  --from admin \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  -y
Unfreeze NFT
bash
txd tx assetnft unfreeze CLASS-ID TOKEN-ID \
  --from admin \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  -y
Add to Whitelist
bash
txd tx assetnft add-to-whitelist CLASS-ID TOKEN-ID address \
  --from admin \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  -y
Remove from Whitelist
bash
txd tx assetnft remove-from-whitelist CLASS-ID TOKEN-ID address \
  --from admin \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  -y
Queries
List NFT Classes
bash
txd query assetnft classes \
  --node https://rpc.testnet-1.coreum.dev:443
Get Class Info
bash
txd query assetnft class CLASS-ID \
  --node https://rpc.testnet-1.coreum.dev:443
List NFTs in Class
bash
txd query assetnft nfts --class-id CLASS-ID \
  --node https://rpc.testnet-1.coreum.dev:443
Get NFT Details
bash
txd query assetnft nft --class-id CLASS-ID --id TOKEN-ID \
  --node https://rpc.testnet-1.coreum.dev:443
Get NFT Balance
bash
txd query assetnft balance address \
  --node https://rpc.testnet-1.coreum.dev:443
Get Whitelisted Accounts
bash
txd query assetnft whitelist CLASS-ID TOKEN-ID \
  --node https://rpc.testnet-1.coreum.dev:443
Get Frozen NFTs
bash
txd query assetnft frozen CLASS-ID \
  --node https://rpc.testnet-1.coreum.dev:443
PhoenixPME NFT Examples
TRUST Token (Soulbound)
bash
# Issue class
txd tx assetnft issue-class TRUST "Trust Token" \
  "Positive reputation for successful trades" \
  --from phoenix-admin \
  --features soulbound \
  -y

# Mint to user after successful trade
txd tx assetnft mint TRUST trust-${USER_ADDRESS} \
  --from phoenix-admin \
  --uri "https://api.phoenixpme.com/metadata/trust/${USER_ADDRESS}" \
  -y
DONT_TRUST Token (Soulbound)
bash
# Issue class
txd tx assetnft issue-class DONT_TRUST "Distrust Token" \
  "Negative reputation for failed obligations" \
  --from phoenix-admin \
  --features soulbound \
  -y

# Mint to user after failed trade
txd tx assetnft mint DONT_TRUST distrust-${USER_ADDRESS} \
  --from phoenix-admin \
  --uri "https://api.phoenixpme.com/metadata/dont-trust/${USER_ADDRESS}" \
  -y
PHNX Token (Soulbound)
bash
# Issue class
txd tx assetnft issue-class PHNX "Phoenix Governance" \
  "Governance weight token - 1 per 1 TESTUSD fee" \
  --from phoenix-admin \
  --features soulbound \
  -y

# Mint to user based on fee generation
txd tx assetnft mint PHNX phnx-${USER_ADDRESS}-${ID} \
  --from phoenix-admin \
  --uri "https://api.phoenixpme.com/metadata/phnx/${USER_ADDRESS}/${ID}" \
  -y
Proto Definitions
For detailed structure, refer to:

events.proto

tx.proto

query.proto

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

## 📄 Module 3: Deterministic Gas

```bash
nano ~/dev/TXdocumentation/modules/deterministic-gas/README.md
Paste this content:

markdown
# Deterministic Gas Model

## Overview
TX uses a deterministic gas model where gas costs are known before transaction execution. For most transaction types, gas is fixed and predictable.

## Formula
Gas = FixedGas + max((GasForBytes + GasForSignatures - TxBaseGas), 0) + Σ(Gas for each message)

text

## Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `FixedGas` | 65,000 | Base gas per transaction |
| `TxBaseGas` | 21,480 | Threshold for free bytes/signatures |
| `SigVerifyCost` | 1,000 | Gas per signature verification |
| `TxSizeCostPerByte` | 10 | Gas per byte of transaction |
| `FreeSignatures` | 1 | Free signatures included |
| `FreeBytes` | 2,048 | Free bytes included |
| `WriteCostPerByte` | 30 | Gas for storing data |

## Gas Calculations

### Bytes & Signatures
GasForBytes = TxByteSize × TxSizeCostPerByte
GasForSignatures = NumOfSigs × SigVerifyCost

text

**Free Threshold**: 
- 1 signature and 2048 bytes are free
- Only pay for extra signatures/bytes

### Examples

**Example 1**: 1 signature, 1000 bytes
Extra bytes = max(0, (1000 - 2048) × 10) = 0
Extra sigs = max(0, (1 - 1) × 1000) = 0
Total = 65,000 + 0 + Σ(MsgGas)

text

**Example 2**: 2 signatures, 2050 bytes
Extra bytes = (2050 - 2048) × 10 = 20
Extra sigs = (2 - 1) × 1000 = 1,000
Total = 65,000 + 1,020 + Σ(MsgGas)

text

## Deterministic Messages

| Message Type | Gas |
|--------------|-----|
| `/coreum.asset.ft.v1.MsgBurn` | 35,000 |
| `/coreum.asset.ft.v1.MsgClawback` | 15,500 |
| `/coreum.asset.ft.v1.MsgClearAdmin` | 8,500 |
| `/coreum.asset.ft.v1.MsgFreeze` | 8,500 |
| `/coreum.asset.ft.v1.MsgGloballyFreeze` | 5,000 |
| `/coreum.asset.ft.v1.MsgGloballyUnfreeze` | 5,000 |
| `/coreum.asset.ft.v1.MsgIssue` | 70,000 |
| `/coreum.asset.ft.v1.MsgMint` | 31,000 |
| `/coreum.asset.ft.v1.MsgSetFrozen` | 8,500 |
| `/coreum.asset.ft.v1.MsgSetWhitelistedLimit` | 9,000 |
| `/coreum.asset.ft.v1.MsgTransferAdmin` | 10,000 |
| `/coreum.asset.ft.v1.MsgUnfreeze` | 8,500 |
| `/coreum.asset.ft.v1.MsgUpgradeTokenV1` | 25,000 |
| `/coreum.asset.nft.v1.MsgAddToClassWhitelist` | 7,000 |
| `/coreum.asset.nft.v1.MsgAddToWhitelist` | 7,000 |
| `/coreum.asset.nft.v1.MsgBurn` | 26,000 |
| `/coreum.asset.nft.v1.MsgClassFreeze` | 8,000 |
| `/coreum.asset.nft.v1.MsgClassUnfreeze` | 5,000 |
| `/coreum.asset.nft.v1.MsgFreeze` | 8,000 |
| `/coreum.asset.nft.v1.MsgRemoveFromClassWhitelist` | 3,500 |
| `/coreum.asset.nft.v1.MsgRemoveFromWhitelist` | 3,500 |
| `/coreum.asset.nft.v1.MsgUnfreeze` | 5,000 |
| `/coreum.dex.v1.MsgPlaceOrder` | 10,000 |
| `/coreum.nft.v1beta1.MsgSend` | 25,000 |
| `/cosmos.authz.v1beta1.MsgGrant` | 28,000 |
| `/cosmos.authz.v1beta1.MsgRevoke` | 8,000 |
| `/cosmos.bank.v1beta1.MsgSend` | Special (see below) |
| `/cosmos.bank.v1beta1.MsgMultiSend` | Special (see below) |
| `/cosmos.distribution.v1beta1.MsgSetWithdrawAddress` | 5,000 |
| `/cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward` | 79,000 |
| `/cosmos.distribution.v1beta1.MsgWithdrawValidatorCommission` | 22,000 |
| `/cosmos.gov.v1.MsgDeposit` | 65,000 |
| `/cosmos.gov.v1.MsgVote` | 6,000 |
| `/cosmos.gov.v1.MsgVoteWeighted` | 6,500 |
| `/cosmos.staking.v1beta1.MsgDelegate` | 83,000 |
| `/cosmos.staking.v1beta1.MsgUndelegate` | 112,000 |
| `/cosmos.staking.v1beta1.MsgBeginRedelegate` | 157,000 |
| `/cosmos.staking.v1beta1.MsgCreateValidator` | 117,000 |
| `/cosmos.staking.v1beta1.MsgEditValidator` | 13,000 |
| `/ibc.applications.transfer.v1.MsgTransfer` | 54,000 |

## Special Cases

### `/cosmos.bank.v1beta1.MsgSend`
Gas = 50,000 × NumberOfCoins

text

### `/cosmos.bank.v1beta1.MsgMultiSend`
Gas = 35,000 × (NumberOfInputs + NumberOfOutputs)

text

### `/cosmos.authz.v1beta1.MsgExec`
Gas = 1,500 + Σ(Gas of each child message)

text

### `/coreum.asset.nft.v1.MsgIssueClass`
Gas = 16,000 + (DataSize × WriteCostPerByte)

text

### `/coreum.asset.nft.v1.MsgMint`
Gas = 39,000 + (DataSize × WriteCostPerByte)

text

### `/coreum.asset.ft.v1.MsgUpdateDEXWhitelistedDenoms`
Gas = 10,000 + (10,000 × NumberOfDenoms)

text

## Non-Deterministic Messages

These messages involve smart contracts or complex logic, gas calculated after execution:

| Message Type |
|--------------|
| `/cosmwasm.wasm.v1.MsgExecuteContract` |
| `/cosmwasm.wasm.v1.MsgInstantiateContract` |
| `/cosmwasm.wasm.v1.MsgStoreCode` |
| `/cosmos.gov.v1.MsgSubmitProposal` |
| `/ibc.core.channel.v1.MsgRecvPacket` |
| `/ibc.core.client.v1.MsgCreateClient` |
| Any message with token having `extension` feature |

## Extensions Impact
If a token has the `extension` feature enabled, these messages become non-deterministic:
- `/ibc.applications.transfer.v1.MsgTransfer`
- `/coreum.asset.ft.v1.MsgIssue`
- `/cosmos.bank.v1beta1.MsgSend`
- `/cosmos.bank.v1beta1.MsgMultiSend`
- And others involving that token

## Proto Definitions
For detailed structure, refer to the proto definitions in the tx codebase.
