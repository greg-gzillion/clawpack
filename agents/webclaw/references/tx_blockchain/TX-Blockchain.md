# TX Blockchain Complete Documentation

## Overview
TX Blockchain is a high-performance, EVM-compatible blockchain built on the Cosmos SDK, combining Coreum and Sologenic technologies. It's designed for real-world asset tokenization and DeFi applications.

## Network Information

### Mainnet (Launching March 6, 2026)
- **Chain ID**: tx-mainnet-1
- **Bech32 Prefix**: core
- **Denom**: utx (6 decimals)
- **Block Time**: ~6 seconds
- **RPC Endpoint**: https://rpc.tx.org:443
- **REST API**: https://api.tx.org:443
- **Explorer**: https://explorer.tx.org

### Testnet
- **Chain ID**: txchain-testnet-1
- **Bech32 Prefix**: testcore
- **Denom**: utestcore (6 decimals)
- **Block Time**: ~6 seconds
- **RPC Endpoints**:
  - https://full-node.testnet.tx.dev:26657
  - https://rpc.testnet.tx.dev:443
- **REST Endpoints**:
  - https://full-node.testnet.tx.dev:1317
  - https://api.testnet.tx.dev:443
- **Faucet**: https://faucet.testnet.tx.dev
- **Explorer**: https://explorer.testnet.tx.dev

## Wallet Management

### Creating a Wallet
```bash
# Testnet wallet
txd keys add my-wallet --keyring-backend test

# Mainnet wallet (after March 6)
txd keys add my-wallet

# Address format:
# Testnet: testcore1...
# Mainnet: core1...
# Create the main directory and subdirectories
mkdir -p ~/dev/TXdocumentation/{network,contracts,development,deployment,api,guides,reference}

echo "📁 Created documentation structure:"
tree ~/dev/TXdocumentation -L 1
cat > ~/dev/TXdocumentation/network/README.md << 'EOF'
# TX Blockchain Network Configuration

## Network Types

### Mainnet
- **Status**: Launching March 6, 2026
- **Chain ID**: `tx-mainnet-1`
- **Address Prefix**: `core`
- **Denom**: `utx` (6 decimals)
- **Block Time**: ~6 seconds

### Testnet
- **Status**: Active
- **Chain ID**: `txchain-testnet-1`
- **Address Prefix**: `testcore`
- **Denom**: `utestcore` (6 decimals)
- **Block Time**: ~6 seconds

### Devnet / Local
- **Chain ID**: `txchain-local`
- **Address Prefix**: `testcore`
- **Denom**: `udevcore`

## Endpoints

### Testnet RPC
- Primary: `https://full-node.testnet.tx.dev:26657`
- Backup: `https://rpc.testnet.tx.dev:443`

### Testnet REST/LCD
- Primary: `https://full-node.testnet.tx.dev:1317`
- Backup: `https://api.testnet.tx.dev:443`

### Mainnet RPC (Post-March 6)
- `https://rpc.tx.org:443`
- `https://rpc.mainnet.tx.org:26657`

## Faucets
- **Testnet**: `https://faucet.testnet.tx.dev`
- **Devnet**: Built into local chain

## Explorers
- **Testnet**: `https://explorer.testnet.tx.dev`
- **Mainnet**: `https://explorer.tx.org` (after launch)
