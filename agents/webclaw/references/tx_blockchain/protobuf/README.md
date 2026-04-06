# TX Blockchain - Protobuf Documentation

Complete Protocol Buffer documentation for all TX Blockchain modules.

## Directory Structure
protobuf/
├── README.md # This index file
├── coreum/
│ ├── asset-ft.md # Fungible tokens
│ ├── asset-nft.md # Non-fungible tokens
│ ├── dex.md # DEX order book
│ ├── feemodel.md # Fee model
│ ├── customparams.md # Custom parameters
│ └── delay.md # Delay module
├── cosmos-sdk/
│ ├── auth.md # Authentication
│ ├── bank.md # Bank/balances
│ ├── staking.md # Staking/validators
│ ├── distribution.md # Rewards
│ ├── gov.md # Governance
│ ├── slashing.md # Slashing
│ ├── upgrade.md # Upgrades
│ ├── feegrant.md # Fee grants
│ ├── group.md # Group accounts
│ ├── nft.md # Basic NFT
│ ├── evidence.md # Evidence
│ ├── crisis.md # Crisis
│ ├── mint.md # Minting
│ ├── params.md # Parameters
│ ├── tx.md # Transaction service
│ ├── base.md # Base types
│ └── crypto.md # Cryptography
├── cosmwasm/
│ └── wasm.md # CosmWasm smart contracts
└── tendermint/
├── abci.md # ABCI interface
├── types.md # Block/transaction types
└── crypto.md # Tendermint crypto

text

## Coreum Modules (TX Blockchain Specific)

| Module | Description | Documentation |
|--------|-------------|---------------|
| Asset FT | Fungible token management (issue, mint, burn, freeze) | [asset-ft.md](coreum/asset-ft.md) |
| Asset NFT | Non-fungible token management (classes, mint, freeze) | [asset-nft.md](coreum/asset-nft.md) |
| DEX | Order book DEX with limit/market orders | [dex.md](coreum/dex.md) |
| Fee Model | Dynamic gas pricing model | [feemodel.md](coreum/feemodel.md) |
| Custom Params | Staking parameters | [customparams.md](coreum/customparams.md) |
| Delay | Delayed execution | [delay.md](coreum/delay.md) |

## Cosmos SDK Modules

| Module | Description | Documentation |
|--------|-------------|---------------|
| Auth | Account management | [auth.md](cosmos-sdk/auth.md) |
| Authz | Authorization grants | [authz.md](cosmos-sdk/authz.md) |
| Bank | Token transfers | [bank.md](cosmos-sdk/bank.md) |
| Staking | Validator delegation | [staking.md](cosmos-sdk/staking.md) |
| Distribution | Reward distribution | [distribution.md](cosmos-sdk/distribution.md) |
| Gov | Governance proposals | [gov.md](cosmos-sdk/gov.md) |
| Slashing | Validator penalties | [slashing.md](cosmos-sdk/slashing.md) |
| Upgrade | Software upgrades | [upgrade.md](cosmos-sdk/upgrade.md) |
| FeeGrant | Fee allowances | [feegrant.md](cosmos-sdk/feegrant.md) |
| Group | Multi-sig groups | [group.md](cosmos-sdk/group.md) |
| NFT | Basic NFT support | [nft.md](cosmos-sdk/nft.md) |
| Evidence | Misbehavior evidence | [evidence.md](cosmos-sdk/evidence.md) |
| Crisis | Invariant checks | [crisis.md](cosmos-sdk/crisis.md) |
| Mint | Token minting | [mint.md](cosmos-sdk/mint.md) |
| Params | Module parameters | [params.md](cosmos-sdk/params.md) |
| Circuit | Circuit breaker | [circuit.md](cosmos-sdk/circuit.md) |
| Consensus | Consensus params | [consensus.md](cosmos-sdk/consensus.md) |

## CosmWasm

| Module | Description | Documentation |
|--------|-------------|---------------|
| Wasm | Smart contract execution | [wasm.md](cosmwasm/wasm.md) |

## Tendermint/CometBFT

| Module | Description | Documentation |
|--------|-------------|---------------|
| ABCI | Application interface | [abci.md](tendermint/abci.md) |
| Types | Block, transaction, vote types | [types.md](tendermint/types.md) |
| Crypto | Cryptographic primitives | [crypto.md](tendermint/crypto.md) |

## Quick Reference

### Common HTTP Endpoints

| Endpoint | Description |
|----------|-------------|
| `/cosmos/bank/v1beta1/balances/{address}` | Get account balances |
| `/cosmos/staking/v1beta1/validators` | List validators |
| `/cosmos/gov/v1/proposals` | List proposals |
| `/cosmwasm/wasm/v1/contract/{address}` | Get contract info |
| `/coreum/asset/ft/v1/tokens` | List fungible tokens |
| `/coreum/asset/nft/v1/classes` | List NFT classes |
| `/coreum/dex/v1/order-books` | List order books |

### Common gRPC Methods

| Service | Method | Description |
|---------|--------|-------------|
| `Msg` (bank) | `Send` | Transfer tokens |
| `Msg` (staking) | `Delegate` | Delegate tokens |
| `Msg` (gov) | `SubmitProposal` | Submit proposal |
| `Msg` (wasm) | `ExecuteContract` | Execute contract |
| `Msg` (asset/ft) | `Issue` | Issue token |
| `Msg` (dex) | `PlaceOrder` | Place DEX order |

### Common Enums

| Enum | Values |
|------|--------|
| `VoteOption` | YES, NO, ABSTAIN, NO_WITH_VETO |
| `BondStatus` | BONDED, UNBONDING, UNBONDED |
| `OrderType` | LIMIT, MARKET |
| `Side` | BUY, SELL |
| `TimeInForce` | GTC, IOC, FOK |
| `AccessType` | NOBODY, EVERYBODY, ANY_OF_ADDRESSES |
