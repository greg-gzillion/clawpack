# TX Blockchain Tutorials

Welcome to the TX Blockchain tutorials! This section provides step-by-step guides for developers and users.

## 📚 Tutorial Categories

### 🚀 Getting Started
- [Set up CLI Network Variables](./getting-started/network-variables.md)
- [Install txd](./getting-started/install-txd.md)
- [Special Addresses](./getting-started/special-addresses.md)

### 💻 CLI Tutorials
- [Transfer funds with CLI](./cli/transfer-funds.md)
- [Send multisig Transaction](./cli/multisig-transaction.md)
- [Smart FT with Access Control List (ACL)](./cli/smart-ft-acl.md)
- [Ledger Nano with CLI: Support and Usage](./cli/ledger-nano.md)

### 🐹 Golang Tutorials
- [Transfer funds with Golang](./golang/transfer-funds.md)
- [Create and manage my first FT with Golang](./golang/first-ft.md)
- [Create and manage my first NFT with Golang](./golang/first-nft.md)

### 📘 TypeScript/JavaScript Tutorials
- [Transfer funds with Typescript](./typescript/transfer-funds.md)
- [Using CosmJS](./typescript/cosmjs.md)
- [Using coreum-js SDK to interact with tx network](./typescript/coreum-js.md)

### 📝 Smart Contracts Tutorials
- [tx WASM SDK](./smart-contracts/wasm-sdk.md)
- [Deploy first WASM contract](./smart-contracts/deploy-first-contract.md)
- [Testing multiple contracts](./smart-contracts/testing-contracts.md)
- [Using CosmJS with WASM contracts](./smart-contracts/cosmjs-wasm.md)

### 🪙 Smart Tokens Tutorials
- [Create and manage my first FT](./smart-tokens/first-ft.md)
- [Create and manage my first NFT](./smart-tokens/first-nft.md)
- [Smart FT with WASM](./smart-tokens/smart-ft-wasm.md)
- [Asset FT Extension](./smart-tokens/asset-ft-extension.md)

### 🔗 Integration Tutorials
- [CEX integration](./integrate/cex-integration.md)
- [Wallet integration](./integrate/wallet-integration.md)
- [Explorer API - Beta](./integrate/explorer-api.md)
- [XRPL Bridge Integration](./integrate/xrpl-bridge.md)

### 🏗️ Build Apps Tutorials
- [Crust for Development](./build-apps/crust.md)
- [Web app](./build-apps/web-app.md)
- [AMM](./build-apps/amm.md)

### 🌐 IBC Tutorials
- [IBC Channels](./ibc/channels.md)
- [IBC Transfer to Osmosis Using Keplr Wallet](./ibc/transfer-osmosis-keplr.md)
- [IBC Smart Contract Call Tutorial](./ibc/smart-contract-call.md)
- [IBC WASM Transfer Tutorial](./ibc/wasm-transfer.md)
- [IBC Transfer Using CLI](./ibc/transfer-cli.md)

### 💱 ISO20022 Tutorials
- [Introduction to ISO20022](./iso20022/introduction.md)
- [ISO20022 Client](./iso20022/client.md)

## 🎯 Quick Start

Choose your path:

| I want to... | Start here |
|--------------|------------|
| Use CLI commands | [CLI Tutorials](./cli/transfer-funds.md) |
| Build with Go | [Golang Tutorials](./golang/transfer-funds.md) |
| Build with TypeScript | [TypeScript Tutorials](./typescript/transfer-funds.md) |
| Deploy smart contracts | [Smart Contracts Tutorials](./smart-contracts/deploy-first-contract.md) |
| Create tokens | [Smart Tokens Tutorials](./smart-tokens/first-ft.md) |
| Integrate with exchange | [CEX Integration](./integrate/cex-integration.md) |

## 📋 Prerequisites

Before starting tutorials, ensure you have:

- [ ] `txd` installed ([Installation Guide](../nodes/prerequisites/install-txd.md))
- [ ] Network variables configured ([Network Variables](./getting-started/network-variables.md))
- [ ] Wallet with testnet tokens ([Faucet](../ecosystem/faucet/README.md))

## 🔗 Related Documentation

- [TX Blockchain Documentation](../README.md)
- [Node Setup Guide](../nodes/full-node/setup-guide.md)
- [Smart Contract Development](../modules/wasm/README.md)

## 💬 Need Help?

- [Discord](https://discord.com/invite/VgkhYeWmTd)
- [GitHub Issues](https://github.com/tokenize-x/tx-chain/issues)
Save with Ctrl+O, Enter, Ctrl+X

2. Getting Started - Network Variables
bash
nano ~/dev/TXdocumentation/tutorials/getting-started/network-variables.md
markdown
# Set up CLI Network Variables

## Overview

Setting up network variables makes CLI interaction with TX Blockchain much easier. This tutorial covers configuring environment variables for testnet and mainnet.

## Prerequisites

- [ ] `txd` installed
- [ ] Terminal access

## Step 1: Choose Your Network

### Testnet (Recommended for learning)

```bash
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_API="https://api.testnet.tx.dev:443"
Mainnet
bash
export TX_CHAIN_ID="tx-mainnet-1"
export TX_DENOM="utx"
export TX_PREFIX="core"
export TX_NODE="https://rpc.tx.org:443"
export TX_API="https://api.tx.org:443"
Step 2: Create Convenience Aliases
bash
# Create aliases for common commands
alias txcli="txd --chain-id $TX_CHAIN_ID --node $TX_NODE"
alias txq="txd query --chain-id $TX_CHAIN_ID --node $TX_NODE"
Step 3: Make Variables Permanent
Add to ~/.bashrc or ~/.zshrc:

bash
# TX Blockchain Testnet Configuration
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_API="https://api.testnet.tx.dev:443"
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
export TX_NODE_ARGS="--node=$TX_NODE"

# Convenience aliases
alias txcli="txd --chain-id $TX_CHAIN_ID --node $TX_NODE"
alias txq="txd query --chain-id $TX_CHAIN_ID --node $TX_NODE"
Reload:

bash
source ~/.bashrc
Step 4: Verify Configuration
bash
# Check chain ID
echo $TX_CHAIN_ID

# Test connection
curl -s $TX_NODE/status | jq .result.node_info.network

# Query node info
txd status --node $TX_NODE
Quick Reference Script
bash
#!/bin/bash
# tx-env.sh - Quick network configuration

case "$1" in
  testnet)
    export TX_CHAIN_ID="txchain-testnet-1"
    export TX_DENOM="utestcore"
    export TX_PREFIX="testcore"
    export TX_NODE="https://rpc.testnet.tx.dev:443"
    echo "Switched to TESTNET"
    ;;
  mainnet)
    export TX_CHAIN_ID="tx-mainnet-1"
    export TX_DENOM="utx"
    export TX_PREFIX="core"
    export TX_NODE="https://rpc.tx.org:443"
    echo "Switched to MAINNET"
    ;;
  *)
    echo "Usage: source tx-env.sh [testnet|mainnet]"
    ;;
esac

export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
export TX_NODE_ARGS="--node=$TX_NODE"
Usage:

bash
source tx-env.sh testnet
Next Steps
Install txd

Transfer funds with CLI

Resources
Network Variables Reference

Troubleshooting

