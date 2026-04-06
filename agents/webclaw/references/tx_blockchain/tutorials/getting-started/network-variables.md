# Setup CLI Network Variables

> **Note**: If you are looking for Validator Network Variables, go to the [Node Setup Guide](../../nodes/prerequisites/network-variables.md)

This document describes the commands to set up environment variables depending on the type of network you want to use.

## Network Comparison Table

| Parameter | Mainnet | Testnet | Devnet | Znet (Localnet) |
|-----------|---------|---------|--------|-----------------|
| **Chain ID** | `tx-mainnet-1` | `txchain-testnet-1` | `txchain-devnet-1` | `txchain-local` |
| **Denom** | `utx` | `utestcore` | `udevcore` | `udevcore` |
| **RPC URL** | `https://rpc.tx.org:443` | `https://rpc.testnet.tx.dev:443` | `https://rpc.devnet.tx.dev:443` | `http://localhost:26657` |
| **gRPC URL** | `grpc.tx.org:443` | `grpc.testnet.tx.dev:443` | `grpc.devnet.tx.dev:443` | `localhost:9090` |
| **REST URL** | `https://api.tx.org:443` | `https://api.testnet.tx.dev:443` | `https://api.devnet.tx.dev:443` | `http://localhost:1317` |
| **Binary Version** | v6.1.0 | v6.1.0 | Latest devnet release | Built via crust |
| **Explorer API** | `https://hasura.tx.org/v1/graphql` | `https://hasura.testnet.tx.dev/v1/graphql` | `https://hasura.devnet.tx.dev/v1/graphql` | `http://localhost:8080/v1/graphql` |

> ⚠️ **Important**: The binary version may be higher than v6.1.0 depending on when you're reading this. Always check the [releases page](https://github.com/tokenize-x/tx-chain/releases) for the latest version.

---

## ⚠️ Important Warnings

### Public RPC Nodes

> Our public RPC nodes are stable, but there is always a risk of DDoS attacks. If you're building your own product (wallet, explorer, etc.), it is **recommended to run your own RPC node**.

> **Rate Limiting**: If you frequently query the node (for indexing, etc.), we recommend running your own RPC node as public endpoints have rate limiting.

### Alternative Public Endpoints

If you need additional public endpoints, you can use these community-maintained options:

**RPC Endpoints:**
https://tx-rpc.publicnode.com:443
https://tx-rpc.ibs.team
https://tx.rpc.silknodes.io

text

**gRPC Endpoints:**
tx-grpc.publicnode.com:443

text

**REST Endpoints:**
https://tx-rest.publicnode.com
https://tx-api.ibs.team
https://tx.api.silknodes.io

text

---

## Step-by-Step Setup

### Step 1: Choose Your Network

Select which network you want to connect to:

#### For Mainnet (Production)
```bash
export TX_CHAIN_ID="tx-mainnet-1"
export TX_DENOM="utx"
export TX_PREFIX="core"
export TX_NODE="https://rpc.tx.org:443"
export TX_API="https://api.tx.org:443"
export TX_GRPC="grpc.tx.org:443"
export TX_VERSION="v6.1.0"
For Testnet (Development)
bash
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_API="https://api.testnet.tx.dev:443"
export TX_GRPC="grpc.testnet.tx.dev:443"
export TX_VERSION="v6.1.0"
For Devnet (Testing)
bash
export TX_CHAIN_ID="txchain-devnet-1"
export TX_DENOM="udevcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.devnet.tx.dev:443"
export TX_API="https://api.devnet.tx.dev:443"
export TX_GRPC="grpc.devnet.tx.dev:443"
export TX_VERSION="latest"
For Local Znet (Development)
bash
export TX_CHAIN_ID="txchain-local"
export TX_DENOM="udevcore"
export TX_PREFIX="testcore"
export TX_NODE="http://localhost:26657"
export TX_API="http://localhost:1317"
export TX_GRPC="localhost:9090"
export TX_VERSION="dev"
Step 2: Set Derived Variables
bash
# Common arguments for CLI commands
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
export TX_NODE_ARGS="--node=$TX_NODE"

# Set home directory based on chain ID
export TX_HOME=$HOME/.txd/"$TX_CHAIN_ID"

# Binary name based on architecture
export TX_BINARY_NAME=$(arch | sed s/aarch64/txd-linux-arm64/ | sed s/x86_64/txd-linux-amd64/)

# Cosmovisor version (if using)
export TX_COSMOVISOR_VERSION="v1.5.0"
Step 3: Create Convenience Aliases
bash
# Create aliases for common commands
alias txcli="txd $TX_CHAIN_ID_ARGS $TX_NODE_ARGS"
alias txq="txd query $TX_CHAIN_ID_ARGS $TX_NODE_ARGS"
alias txtx="txd tx $TX_CHAIN_ID_ARGS $TX_NODE_ARGS"

# Query helper
alias txbalance="txd query bank balances $TX_NODE_ARGS"
alias txstatus="curl -s $TX_NODE/status | jq ."
Step 4: Make Variables Permanent
Add to ~/.bashrc or ~/.zshrc:

bash
# TX Blockchain - Testnet Configuration (change network as needed)
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_API="https://api.testnet.tx.dev:443"
export TX_GRPC="grpc.testnet.tx.dev:443"
export TX_VERSION="v6.1.0"

export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
export TX_NODE_ARGS="--node=$TX_NODE"
export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"
export TX_BINARY_NAME=$(arch | sed s/aarch64/txd-linux-arm64/ | sed s/x86_64/txd-linux-amd64/)

# Convenience aliases
alias txcli="txd $TX_CHAIN_ID_ARGS $TX_NODE_ARGS"
alias txq="txd query $TX_CHAIN_ID_ARGS $TX_NODE_ARGS"
alias txtx="txd tx $TX_CHAIN_ID_ARGS $TX_NODE_ARGS"
alias txbalance="txd query bank balances $TX_NODE_ARGS"
alias txstatus="curl -s $TX_NODE/status | jq ."
Reload your shell:

bash
source ~/.bashrc
Quick Network Switcher Script
Create a script to quickly switch between networks:

bash
#!/bin/bash
# tx-env.sh - Quick network configuration switcher

case "$1" in
  mainnet)
    export TX_CHAIN_ID="tx-mainnet-1"
    export TX_DENOM="utx"
    export TX_PREFIX="core"
    export TX_NODE="https://rpc.tx.org:443"
    export TX_API="https://api.tx.org:443"
    export TX_GRPC="grpc.tx.org:443"
    export TX_VERSION="v6.1.0"
    echo "🟢 Switched to MAINNET"
    ;;
  testnet)
    export TX_CHAIN_ID="txchain-testnet-1"
    export TX_DENOM="utestcore"
    export TX_PREFIX="testcore"
    export TX_NODE="https://rpc.testnet.tx.dev:443"
    export TX_API="https://api.testnet.tx.dev:443"
    export TX_GRPC="grpc.testnet.tx.dev:443"
    export TX_VERSION="v6.1.0"
    echo "🟡 Switched to TESTNET"
    ;;
  devnet)
    export TX_CHAIN_ID="txchain-devnet-1"
    export TX_DENOM="udevcore"
    export TX_PREFIX="testcore"
    export TX_NODE="https://rpc.devnet.tx.dev:443"
    export TX_API="https://api.devnet.tx.dev:443"
    export TX_GRPC="grpc.devnet.tx.dev:443"
    export TX_VERSION="latest"
    echo "🔵 Switched to DEVNET"
    ;;
  local)
    export TX_CHAIN_ID="txchain-local"
    export TX_DENOM="udevcore"
    export TX_PREFIX="testcore"
    export TX_NODE="http://localhost:26657"
    export TX_API="http://localhost:1317"
    export TX_GRPC="localhost:9090"
    export TX_VERSION="dev"
    echo "⚪ Switched to LOCALNET"
    ;;
  *)
    echo "Usage: source tx-env.sh [mainnet|testnet|devnet|local]"
    echo ""
    echo "Examples:"
    echo "  source tx-env.sh testnet  # Switch to testnet"
    echo "  source tx-env.sh mainnet  # Switch to mainnet"
    return 1
    ;;
esac

# Set derived variables
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
export TX_NODE_ARGS="--node=$TX_NODE"
export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"
export TX_BINARY_NAME=$(arch | sed s/aarch64/txd-linux-arm64/ | sed s/x86_64/txd-linux-amd64/)

echo "✅ Environment configured for $TX_CHAIN_ID"
echo "   RPC: $TX_NODE"
echo "   Denom: $TX_DENOM"
Save as ~/tx-env.sh and use:

bash
source ~/tx-env.sh testnet
source ~/tx-env.sh mainnet
Verification Commands
Test Connection
bash
# Check if RPC is reachable
curl -s $TX_NODE/status | jq .result.node_info.network

# Should return your chain ID
Query Chain Info
bash
# Get chain ID
txd status --node $TX_NODE | jq .NodeInfo.network

# Get latest block height
curl -s $TX_NODE/status | jq .result.sync_info.latest_block_height

# Get node info
txd status --node $TX_NODE | jq .NodeInfo
Check Balance
bash
# Check your wallet balance
txd query bank balances $(txd keys show my-wallet -a) $TX_NODE_ARGS

# Check module account
txd query bank balances core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx $TX_NODE_ARGS
Environment Variables Reference
Variable	Description	Example
TX_CHAIN_ID	Network chain ID	txchain-testnet-1
TX_DENOM	Token denomination	utestcore
TX_PREFIX	Address prefix	testcore
TX_NODE	RPC endpoint URL	https://rpc.testnet.tx.dev:443
TX_API	REST API URL	https://api.testnet.tx.dev:443
TX_GRPC	gRPC endpoint	grpc.testnet.tx.dev:443
TX_VERSION	Binary version	v6.1.0
TX_CHAIN_ID_ARGS	Chain ID CLI arg	--chain-id=txchain-testnet-1
TX_NODE_ARGS	Node CLI arg	--node=https://rpc.testnet.tx.dev:443
TX_HOME	txd home directory	/home/user/.txd/txchain-testnet-1
TX_BINARY_NAME	Binary filename	txd-linux-amd64
Common Issues
Connection Refused
bash
# Check if RPC is accessible
curl -v $TX_NODE/status

# Try alternative endpoint
export TX_NODE="https://tx-rpc.publicnode.com:443"
Wrong Chain ID
bash
# Verify chain ID from node
curl -s $TX_NODE/status | jq .result.node_info.network

# Compare with your TX_CHAIN_ID
echo $TX_CHAIN_ID
Rate Limiting
If you encounter rate limiting:

bash
# Reduce query frequency
sleep 1  # Add delay between queries

# Or run your own node
# Follow: Node Setup Guide
Next Steps
Install txd

Special Addresses

Transfer funds with CLI

Gas Price Guide

Resources
Node Network Variables

Troubleshooting Guide

txd Releases
