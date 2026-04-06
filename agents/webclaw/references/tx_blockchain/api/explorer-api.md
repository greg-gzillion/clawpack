# Explorer API - Beta

GraphQL API for TX Blockchain indexed data.

## Endpoints

| Network | Endpoint |
|---------|----------|
| Testnet | `https://hasura.testnet-1.tx.org/v1/graphql` |
| Mainnet | `https://hasura.tx.org/v1/graphql` |

## GraphQL Playground Setup

### 1. Install
```bash
npm install -g graphql-playground
2. Create .graphqlconfig
json
{
  "name": "Explorer Schema",
  "schemaPath": "schema.graphql",
  "extensions": {
    "endpoints": {
      "Remote TX GraphQL Endpoint": {
        "url": "https://hasura.testnet-1.tx.org/v1/graphql",
        "headers": {"user-agent": "JS GraphQL"},
        "introspect": true
      }
    }
  }
}
3. Query Example
graphql
{
    messages_by_address(
        args: {
            addresses: "{testcore1sxu4sumja8c53gvyn7cctqlsqm27w6jh0dnvdm}", 
            limit: "50"
        }
    ) {
        value
        type
        transaction_hash
    }
}
text

```bash
# 2. Create IBC documentation
mkdir -p ~/dev/TXdocumentation/ibc
nano ~/dev/TXdocumentation/ibc/README.md
bash
# 3. Create ISO20022 documentation
mkdir -p ~/dev/TXdocumentation/iso20022
nano ~/dev/TXdocumentation/iso20022/README.md
bash
# 4. Create a master index for AI agent
nano ~/dev/TXdocumentation/INDEX.md
Paste this comprehensive index:

markdown
# TX Blockchain Documentation Index

## 📚 Complete Documentation Map for AI Agent

### 🏗️ Core Blockchain
| File | Description |
|------|-------------|
| [README.md](README.md) | Project overview |
| [VISION.md](VISION.md) | Project vision and goals |
| [MANIFESTO.md](MANIFESTO.md) | Core principles |
| [TX-Blockchain.md](TX-Blockchain.md) | Technical overview |

### 🔧 Node Operations (`/nodes`)
| File | Description |
|------|-------------|
| [prerequisites/install-txd.md](nodes/prerequisites/install-txd.md) | Install txd binary |
| [prerequisites/network-variables.md](nodes/prerequisites/network-variables.md) | Network configuration |
| [full-node/setup-guide.md](nodes/full-node/setup-guide.md) | Run a full node |
| [validator-node/README.md](nodes/validator-node/README.md) | Validator setup |
| [sentry-node/setup-guide.md](nodes/sentry-node/setup-guide.md) | Sentry node config |
| [troubleshooting/README.md](nodes/troubleshooting/README.md) | Common issues |
| [troubleshooting/upgrade-guide.md](nodes/troubleshooting/upgrade-guide.md) | Chain upgrades |
| [troubleshooting/upgrade-history.md](nodes/troubleshooting/upgrade-history.md) | Upgrade history |

### 📖 Tutorials (`/tutorials`)

#### Getting Started
| File | Description |
|------|-------------|
| [gas-price.md](tutorials/gas-price.md) | Fee model explained |
| [getting-started/install-txd.md](tutorials/getting-started/install-txd.md) | Install CLI |
| [getting-started/network-variables.md](tutorials/getting-started/network-variables.md) | Network endpoints |
| [getting-started/special-addresses.md](tutorials/getting-started/special-addresses.md) | System addresses |

#### CLI Tutorials
| File | Description |
|------|-------------|
| [cli/transfer-funds.md](tutorials/cli/transfer-funds.md) | Send tokens |
| [cli/multisig-transaction.md](tutorials/cli/multisig-transaction.md) | Multi-signature |
| [cli/smart-ft-acl.md](tutorials/cli/smart-ft-acl.md) | FT access control |
| [cli/ledger-nano.md](tutorials/cli/ledger-nano.md) | Ledger hardware wallet |

#### Golang Tutorials
| File | Description |
|------|-------------|
| [golang/transfer-funds.md](tutorials/golang/transfer-funds.md) | Send tokens with Go |
| [golang/first-ft.md](tutorials/golang/first-ft.md) | Create fungible tokens |
| [golang/first-nft.md](tutorials/golang/first-nft.md) | Create NFTs |

#### TypeScript Tutorials
| File | Description |
|------|-------------|
| [typescript/transfer-funds.md](tutorials/typescript/transfer-funds.md) | CosmJS basics |
| [typescript/coreum-js.md](tutorials/typescript/coreum-js.md) | coreum-js SDK |

#### Smart Tokens
| File | Description |
|------|-------------|
| [smart-tokens/first-ft.md](tutorials/smart-tokens/first-ft.md) | FT CLI guide |
| [smart-tokens/first-nft.md](tutorials/smart-tokens/first-nft.md) | NFT CLI guide |
| [smart-tokens/asset-ft-extension.md](tutorials/smart-tokens/asset-ft-extension.md) | WASM FT extensions |
| [smart-tokens/smart-ft-wasm.md](tutorials/smart-tokens/smart-ft-wasm.md) | Smart FT with WASM |

#### Smart Contracts
| File | Description |
|------|-------------|
| [smart-contracts/deploy-first-wasm.md](tutorials/smart-contracts/deploy-first-wasm.md) | First WASM contract |
| [smart-contracts/testing-multiple-contracts.md](tutorials/smart-contracts/testing-multiple-contracts.md) | Multi-contract testing |
| [smart-contracts/cosmjs-with-wasm.md](tutorials/smart-contracts/cosmjs-with-wasm.md) | CosmJS + WASM |
| [smart-contracts/tx-wasm-sdk.md](tutorials/smart-contracts/tx-wasm-sdk.md) | Rust WASM SDK |
| [smart-contracts/amm-astroport.md](tutorials/smart-contracts/amm-astroport.md) | Deploy AMM |

#### Build Apps
| File | Description |
|------|-------------|
| [build-apps/web-app.md](tutorials/build-apps/web-app.md) | React + Next.js app |
| [build-apps/crust.md](tutorials/build-apps/crust.md) | Local dev environment |

#### Integration
| File | Description |
|------|-------------|
| [integrate/cex-integration.md](tutorials/integrate/cex-integration.md) | Exchange integration |
| [integrate/wallet-integration.md](tutorials/integrate/wallet-integration.md) | Wallet integration |

### 🔌 Modules (`/modules`)
- assetft - Fungible Token module
- assetnft - Non-Fungible Token module
- bank - Token transfers
- staking - Validator staking
- wasm - Smart contracts
- ibc - Cross-chain IBC
- feemodel - Dynamic fees
- distribution - Reward distribution
- gov - Governance
- authz - Authorization
- vesting - Vesting accounts

### 🌐 Networks
- **Mainnet**: `txchain-mainnet-1`
- **Testnet**: `txchain-testnet-1`
- **Devnet**: `txchain-devnet-1`

### 🔑 Key Constants
- **Bech32 Prefix**: `tx` (mainnet), `testcore` (testnet)
- **Coin Type**: 990
- **Denom**: `utx` (mainnet), `utestcore` (testnet)
- **Precision**: 6 decimals
- **Block Time**: ~1.6 seconds

## 🚀 Quick Reference

### Send Tokens (CLI)
```bash
txd tx bank send <from> <to> <amount><denom> --chain-id=txchain-testnet-1
Query Balance
bash
txd query bank balances <address> --denom utestcore
Create FT Token
bash
txd tx assetft issue MYFT umyft 6 1000000 "My Token" --from <admin>
Deploy WASM Contract
bash
txd tx wasm store contract.wasm --from wallet
txd tx wasm instantiate <code-id> '{}' --from wallet --label "my-contract"
📞 Support & Resources
Website: https://tx.org

Explorer: https://explorer.tx.org

Faucet: https://faucet.testnet.tx.dev

GitHub: https://github.com/tokenize-x/tx-chain

