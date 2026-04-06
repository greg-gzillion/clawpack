# AI Agent Learning Guide for TX Blockchain

## 📚 Learning Path for Complete Understanding

### Phase 1: Core Concepts (Start Here)
1. [README.md](README.md) - Project overview
2. [VISION.md](VISION.md) - Vision and goals
3. [MANIFESTO.md](MANIFESTO.md) - Core principles
4. [TX-Blockchain.md](TX-Blockchain.md) - Technical overview
5. [architecture/](architecture/) - System architecture

### Phase 2: Network & Node Operations
1. [nodes/prerequisites/install-txd.md](nodes/prerequisites/install-txd.md)
2. [nodes/prerequisites/network-variables.md](nodes/prerequisites/network-variables.md)
3. [nodes/full-node/setup-guide.md](nodes/full-node/setup-guide.md)
4. [nodes/validator-node/README.md](nodes/validator-node/README.md)
5. [nodes/troubleshooting/README.md](nodes/troubleshooting/README.md)

### Phase 3: CLI Basics
1. [tutorials/getting-started/install-txd.md](tutorials/getting-started/install-txd.md)
2. [tutorials/gas-price.md](tutorials/gas-price.md)
3. [tutorials/cli/transfer-funds.md](tutorials/cli/transfer-funds.md)
4. [tutorials/cli/ledger-nano.md](tutorials/cli/ledger-nano.md)

### Phase 4: Smart Tokens (Core Feature)
1. [tutorials/smart-tokens/first-ft.md](tutorials/smart-tokens/first-ft.md)
2. [tutorials/smart-tokens/first-nft.md](tutorials/smart-tokens/first-nft.md)
3. [tutorials/smart-tokens/asset-ft-extension.md](tutorials/smart-tokens/asset-ft-extension.md)
4. [tutorials/smart-tokens/smart-ft-wasm.md](tutorials/smart-tokens/smart-ft-wasm.md)

### Phase 5: Smart Contracts (WASM)
1. [tutorials/smart-contracts/deploy-first-wasm.md](tutorials/smart-contracts/deploy-first-wasm.md)
2. [tutorials/smart-contracts/cosmjs-with-wasm.md](tutorials/smart-contracts/cosmjs-with-wasm.md)
3. [tutorials/smart-contracts/tx-wasm-sdk.md](tutorials/smart-contracts/tx-wasm-sdk.md)
4. [tutorials/smart-contracts/testing-multiple-contracts.md](tutorials/smart-contracts/testing-multiple-contracts.md)

### Phase 6: DeFi & AMM
1. [tutorials/smart-contracts/amm-astroport.md](tutorials/smart-contracts/amm-astroport.md)

### Phase 7: Application Development
1. [tutorials/build-apps/web-app.md](tutorials/build-apps/web-app.md)
2. [tutorials/build-apps/crust.md](tutorials/build-apps/crust.md)
3. [tutorials/typescript/transfer-funds.md](tutorials/typescript/transfer-funds.md)
4. [tutorials/typescript/coreum-js.md](tutorials/typescript/coreum-js.md)

### Phase 8: Integration & APIs
1. [tutorials/integrate/cex-integration.md](tutorials/integrate/cex-integration.md)
2. [tutorials/integrate/wallet-integration.md](tutorials/integrate/wallet-integration.md)
3. [api/explorer-api.md](api/explorer-api.md)

### Phase 9: Module Deep Dive
Review each module directory in `/modules/`:
- assetft - Fungible Token mechanics
- assetnft - NFT mechanics
- wasm - Smart contract execution
- ibc - Cross-chain communication
- feemodel - Dynamic fee calculation
- staking - Validator delegation

## 🔑 Key Concepts Summary

### Network Constants
- **Mainnet Chain ID**: `txchain-mainnet-1`
- **Testnet Chain ID**: `txchain-testnet-1`
- **Bech32 Prefix**: `tx` (mainnet), `testcore` (testnet)
- **Coin Type**: 990
- **Native Denom**: `utx` (mainnet), `utestcore` (testnet)
- **Decimals**: 6
- **Block Time**: ~1.6 seconds
- **Validators**: 64

### Core Modules
| Module | Purpose |
|--------|---------|
| assetft | Fungible token creation/management |
| assetnft | NFT class and token management |
| bank | Token transfers and balances |
| wasm | CosmWasm smart contracts |
| ibc | Cross-chain IBC transfers |
| feemodel | Dynamic gas pricing |

### Development Workflows
1. **Token Creation**: Issue FT/NFT with custom features
2. **Smart Contracts**: Deploy WASM contracts with CosmWasm
3. **Web Apps**: Build with Next.js + CosmJS + Keplr
4. **Local Dev**: Use Crust for local testnet

## 📊 Quick Reference Commands

```bash
# CLI Basics
txd version
txd keys list
txd query bank balances <address>

# Transactions
txd tx bank send <from> <to> <amount> --chain-id=<chain-id>

# Smart Tokens
txd tx assetft issue <symbol> <subunit> <precision> <amount> <description>
txd tx assetnft issue-class <symbol> <name> <description>

# WASM
txd tx wasm store <contract.wasm>
txd tx wasm instantiate <code-id> '<init-msg>'

# Queries
txd query assetft token <denom>
txd query wasm contract-state smart <contract-addr> '<query>'
🎯 What Your AI Agent Should Master
Token Economics - Supply, inflation, fee model

Smart Tokens - FT/NFT features (minting, burning, freezing, whitelisting)

WASM Integration - Contract deployment and interaction

IBC Protocol - Cross-chain token transfers

Validator Operations - Staking, delegation, rewards

Application Development - Web apps with CosmJS

Exchange Integration - Deposit/withdrawal flows

📞 Essential Resources
Website: https://tx.org

Explorer: https://explorer.tx.org

Testnet Faucet: https://faucet.testnet.tx.dev

GitHub: https://github.com/tokenize-x/tx-chain

Documentation: https://docs.tx.org
