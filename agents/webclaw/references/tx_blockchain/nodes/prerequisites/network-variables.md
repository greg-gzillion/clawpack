# Network Variables - TX Blockchain

## Network Comparison

| Parameter | Mainnet | Testnet | Devnet | Znet (Local) |
|-----------|---------|---------|--------|--------------|
| **Chain ID** | `tx-mainnet-1` | `txchain-testnet-1` | `txchain-devnet-1` | `txchain-local` |
| **Denom** | `utx` | `utestcore` | `udevcore` | `udevcore` |
| **Bech32 Prefix** | `core` | `testcore` | `testcore` | `testcore` |
| **RPC URL** | `https://rpc.tx.org:443` | `https://rpc.testnet.tx.dev:443` | `https://rpc.devnet.tx.dev:443` | `http://localhost:26657` |
| **API URL** | `https://api.tx.org:443` | `https://api.testnet.tx.dev:443` | `https://api.devnet.tx.dev:443` | `http://localhost:1317` |
| **Cosmovisor Version** | v1.5.0 | v1.5.0 | v1.5.0 | v1.5.0 |
| **Binary Version** | v6.1.0 | v6.1.0 | Latest | Built locally |
| **Upgrade Name** | Check releases | Check releases | `genesis` | `genesis` |

## State Sync Servers

| Network | State Sync Servers |
|---------|-------------------|
| **Mainnet** | `https://rpc-01.tx.org:443,https://rpc-02.tx.org:443` |
| **Testnet** | `https://rpc-01.testnet.tx.dev:443,https://archive.rpc.testnet.tx.dev:443` |
| **Devnet** | Not supported |
| **Znet** | Not supported |

## ⚠️ Important Warnings

> **Public RPC Nodes**: Our public RPC nodes are stable, but there is always a risk of DDoS attacks. If you're building your own product (wallet, explorer, etc.), it is **recommended to run your own RPC node**.

> **Rate Limiting**: If you frequently query the node (for indexing, etc.), we recommend running your own RPC node as public endpoints have rate limiting.

> **Alternative RPC Providers**: You can also use our partners' services:
> - Nownodes
> - Zeeve
> - Allnodes

## Environment Variables Setup

### For Mainnet:
```bash
export TX_CHAIN_ID="tx-mainnet-1"
export TX_DENOM="utx"
export TX_PREFIX="core"
export TX_NODE="https://rpc.tx.org:443"
export TX_API="https://api.tx.org:443"
export TX_COSMOVISOR_VERSION="v1.5.0"
export TX_VERSION="v6.1.0"
export UPGRADE_NAME="genesis"
For Testnet:
bash
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_API="https://api.testnet.tx.dev:443"
export TX_COSMOVISOR_VERSION="v1.5.0"
export TX_VERSION="v6.1.0"
export UPGRADE_NAME="genesis"
For Devnet:
bash
export TX_CHAIN_ID="txchain-devnet-1"
export TX_DENOM="udevcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.devnet.tx.dev:443"
export TX_API="https://api.devnet.tx.dev:443"
export TX_COSMOVISOR_VERSION="v1.5.0"
export TX_VERSION="latest"
export UPGRADE_NAME="genesis"
For Local Znet:
bash
export TX_CHAIN_ID="txchain-local"
export TX_DENOM="udevcore"
export TX_PREFIX="testcore"
export TX_NODE="http://localhost:26657"
export TX_API="http://localhost:1317"
export TX_COSMOVISOR_VERSION="v1.5.0"
export UPGRADE_NAME="genesis"
Derived Variables
bash
# Common args
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
export TX_NODE_ARGS="--node=$TX_NODE"

# Home directory
export TX_HOME=$HOME/.txd/"$TX_CHAIN_ID"

# Binary name based on architecture
export TX_BINARY_NAME=$(arch | sed s/aarch64/txd-linux-arm64/ | sed s/x86_64/txd-linux-amd64/)

# Cosmovisor archive name
export COSMOVISOR_TAR_NAME=cosmovisor-$TX_COSMOVISOR_VERSION-linux-$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/).tar.gz
Make Variables Permanent
Add to ~/.bashrc or ~/.profile:

bash
# TX Blockchain Network (change network as needed)
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
export TX_NODE_ARGS="--node=$TX_NODE"
Verify Settings
bash
# Check current variables
echo "Chain ID: $TX_CHAIN_ID"
echo "Denom: $TX_DENOM"
echo "RPC: $TX_NODE"
echo "Home: $TX_HOME"

# Test connection
curl -s $TX_NODE/status | jq .result.node_info.network
Resources
System Requirements

Install txd

Full Node Setup

Validator Setup
