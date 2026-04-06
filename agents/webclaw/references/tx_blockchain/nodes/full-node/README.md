# Run a Full Node

## Overview
A full node syncs the entire blockchain and can query data, but does not participate in consensus.

## Step 1: Initialize Node

```bash
# Initialize node
txd init <YOUR_MONIKER> --chain-id <CHAIN_ID>

# Example:
txd init my-full-node --chain-id txchain-testnet-1
Step 2: Download Genesis
bash
# Testnet
wget -O ~/.txd/config/genesis.json https://raw.githubusercontent.com/tokenize-x/testnet/main/genesis.json

# Mainnet
# wget -O ~/.txd/config/genesis.json https://raw.githubusercontent.com/tokenize-x/mainnet/main/genesis.json

# Verify genesis
txd validate-genesis
Step 3: Configure Node
bash
# Set minimum gas price
sed -i 's/minimum-gas-prices = ""/minimum-gas-prices = "0.0625utestcore"/' ~/.txd/config/app.toml

# Set seeds
sed -i 's/seeds = ""/seeds = "seed.testnet.tx.dev:26656"/' ~/.txd/config/config.toml

# Set persistent peers (optional)
sed -i 's/persistent_peers = ""/persistent_peers = "peer1.testnet.tx.dev:26656,peer2.testnet.tx.dev:26656"/' ~/.txd/config/config.toml

# Enable RPC (optional)
sed -i 's/laddr = "tcp://127.0.0.1:26657"/laddr = "tcp://0.0.0.0:26657"/' ~/.txd/config/config.toml
Step 4: Start Node
bash
# Start node
txd start

# Or run as background service
txd start &
Step 5: Create Systemd Service (Recommended)
bash
# Create service file
sudo nano /etc/systemd/system/txd.service
ini
[Unit]
Description=TX Full Node
After=network-online.target

[Service]
User=greg
ExecStart=/usr/local/bin/txd start
Restart=always
RestartSec=3
LimitNOFILE=4096

[Install]
WantedBy=multi-user.target
bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable txd
sudo systemctl start txd

# Check status
sudo systemctl status txd

# View logs
sudo journalctl -u txd -f
Step 6: Verify Node Sync
bash
# Check sync status
txd status 2>&1 | jq .SyncInfo

# Check if node is catching up
curl -s http://localhost:26657/status | jq .result.sync_info.catching_up

# Check block height
curl -s http://localhost:26657/status | jq .result.sync_info.latest_block_height
Step 7: Query Node
bash
# Get node info
txd query staking validators --node http://localhost:26657

# Check balance
txd query bank balances <ADDRESS> --node http://localhost:26657

# Query blocks
curl -s http://localhost:26657/block | jq .result.block.header
Troubleshooting
Node Not Syncing
bash
# Check peers
curl -s http://localhost:26657/net_info | jq .result.peers

# Add more peers
sed -i 's/seeds = ".*"/seeds = "seed1:26656,seed2:26656"/' ~/.txd/config/config.toml

# Reset and restart
txd tendermint unsafe-reset-all
sudo systemctl restart txd
Insufficient Disk Space
bash
# Check disk usage
df -h ~/.txd/data/

# Prune old state (run when node is stopped)
txd prune
Resources
Network Variables

System Requirements

Troubleshooting
# Run a Full Node

## Overview
A full node syncs the entire blockchain and can query data, but does not participate in consensus.

## Quick Start

For detailed step-by-step instructions, see the [Complete Setup Guide](./setup-guide.md).

### Basic Commands

```bash
# Initialize node
txd init <moniker> --chain-id txchain-testnet-1

# Download genesis
wget -O ~/.txd/config/genesis.json https://raw.githubusercontent.com/tokenize-x/testnet/main/genesis.json

# Start node
txd start
Prerequisites
System Requirements

Install txd

Network Variables

Documentation
Complete Setup Guide - Detailed step-by-step instructions

State Sync Guide - Fast sync configuration

Troubleshooting - Common issues and solutions

Next Steps
Run a Validator Node

Configure Monitoring

Set Up Backup

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

## ✅ Verify Full Node Documentation

```bash
# Show full node documentation structure
ls -la ~/dev/TXdocumentation/nodes/full-node/
