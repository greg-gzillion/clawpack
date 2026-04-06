# Run a Full Node - Complete Setup Guide

## Important Note for Devnet

> ⚠️ **Attention**: If you are planning to run a node against the devnet (either a full node or a validator node), be mindful that the devnet might be restarted without prior notice (i.e., block height set to 0 and all state removed). You should be prepared to act accordingly by removing all state and starting from zero.

## Prerequisites

Before starting, ensure you have:

- [ ] System requirements met ([System Requirements](../prerequisites/system-requirements.md))
- [ ] `txd` binary installed ([Install txd](../prerequisites/install-txd.md))
- [ ] Network variables configured ([Network Variables](../prerequisites/network-variables.md))
- [ ] `crudini` installed: `sudo apt install crudini -y`
- [ ] `jq` installed: `sudo apt install jq -y`

## Step 1: Set Up Node Prerequisites

### Set the Moniker
The moniker is your node's display name:

```bash
export MONIKER="full"
Set Chain ID
Choose your network:

bash
# For testnet:
export TX_CHAIN_ID="txchain-testnet-1"
export TX_CHAIN_ID_ARGS="--chain-id $TX_CHAIN_ID"

# For mainnet:
# export TX_CHAIN_ID="tx-mainnet-1"
# export TX_CHAIN_ID_ARGS="--chain-id $TX_CHAIN_ID"

# For devnet:
# export TX_CHAIN_ID="txchain-local"
# export TX_CHAIN_ID_ARGS="--chain-id $TX_CHAIN_ID"
Step 2: Initialize the Node
The init command creates a default node configuration:

bash
txd init $MONIKER $TX_CHAIN_ID_ARGS
This creates:

~/.txd/config/config.toml - Tendermint configuration

~/.txd/config/app.toml - Application configuration

~/.txd/data/ - Blockchain data directory

Step 3: Set Configuration Path Variables
bash
# Set config paths for easy reference
TX_HOME=~/.txd
TX_APP_CONFIG=$TX_HOME/config/app.toml
TX_NODE_CONFIG=$TX_HOME/config/config.toml

echo "App config: $TX_APP_CONFIG"
echo "Node config: $TX_NODE_CONFIG"
Step 4: Configure the Node
Download Genesis File
bash
# Testnet
wget -O $TX_HOME/config/genesis.json https://raw.githubusercontent.com/tokenize-x/testnet/main/genesis.json

# Mainnet
# wget -O $TX_HOME/config/genesis.json https://raw.githubusercontent.com/tokenize-x/mainnet/main/genesis.json

# Verify genesis
txd validate-genesis
Set Minimum Gas Price
bash
# Set minimum gas price to prevent spam
crudini --set $TX_APP_CONFIG minimum-gas-prices "0.0625utestcore"
(Optional) Enable REST API
REST API is disabled by default. Enable if needed:

bash
# Enable API
crudini --set $TX_APP_CONFIG api enable true

# Enable Swagger UI for API documentation
crudini --set $TX_APP_CONFIG api swagger true
Note: If you face "File contains parsing errors" issues, check the Troubleshooting section.

(Optional) Enable Prometheus Monitoring
bash
# Enable Prometheus metrics endpoint
crudini --set $TX_NODE_CONFIG instrumentation prometheus true
Metrics will be available at http://localhost:26660/metrics

(Optional) Configure State Sync Snapshots
If you want your node to provide state snapshots for other nodes:

bash
# Set snapshot interval (in blocks)
crudini --set $TX_APP_CONFIG state-sync snapshot-interval 500

# Number of recent snapshots to keep
crudini --set $TX_APP_CONFIG state-sync snapshot-keep-recent 3
This configuration is required for state-sync servers that provide snapshots for other nodes.

Step 5: Enable State Sync (Fast Sync)
State sync allows your node to sync quickly by downloading snapshots instead of processing all blocks from genesis.

Get State Sync Servers
bash
# Testnet state sync servers (get from documentation or community)
export TX_STATE_SYNC_SERVERS="https://rpc.testnet.tx.dev:443,https://rpc2.testnet.tx.dev:443"

# Mainnet state sync servers
# export TX_STATE_SYNC_SERVERS="https://rpc.tx.org:443,https://rpc2.tx.org:443"
Get Trusted Block Hash and Height
bash
# Get current block details from first server
CURRENT_BLOCK_DETAILS=$(curl -s ${TX_STATE_SYNC_SERVERS%%,*}/block | jq -r '.result.block.header.height + " " + .result.block_id.hash')
CURRENT_BLOCK_HEIGHT=$(echo $CURRENT_BLOCK_DETAILS | awk '{print $1}')
echo "Current block height: $CURRENT_BLOCK_HEIGHT"

# Set trusted block height (current - 10000)
TRUSTED_BLOCK_HEIGHT=$((CURRENT_BLOCK_HEIGHT - 10000))
echo "Trusted block height: $TRUSTED_BLOCK_HEIGHT"

# Get trusted block hash
TRUSTED_BLOCK_DETAILS=$(curl -s "${TX_STATE_SYNC_SERVERS%%,*}/block?height=${TRUSTED_BLOCK_HEIGHT}" | jq -r '.result.block.header.height + "\n" + .result.block_id.hash')
TRUSTED_BLOCK_HASH=$(echo $TRUSTED_BLOCK_DETAILS | tail -1)

echo "Trusted block hash: $TRUSTED_BLOCK_HASH"
Note: If you see "Failure writing output to destination" error, check if jq is installed.

Verify Trusted Data
bash
echo "height: $TRUSTED_BLOCK_HEIGHT, hash: $TRUSTED_BLOCK_HASH"
# Output should be similar to:
# height: 1425435, hash: 9ADD8B2035F6B79F58B75D6F66A4B9B148787204553344295C7117417AEB856C
Enable State Sync in Config
bash
# Enable state sync
crudini --set $TX_NODE_CONFIG statesync enable true

# Set RPC servers
crudini --set $TX_NODE_CONFIG statesync rpc_servers "\"$TX_STATE_SYNC_SERVERS\""

# Set trusted height and hash
crudini --set $TX_NODE_CONFIG statesync trust_height $TRUSTED_BLOCK_HEIGHT
crudini --set $TX_NODE_CONFIG statesync trust_hash "\"$TRUSTED_BLOCK_HASH\""
Step 6: Configure Seeds and Peers
Set Seed Nodes
bash
# Testnet seeds
crudini --set $TX_NODE_CONFIG seeds "seed.testnet.tx.dev:26656"

# Mainnet seeds
# crudini --set $TX_NODE_CONFIG seeds "seed.tx.org:26656"
Set Persistent Peers (Optional)
bash
# Add persistent peers for more reliable connections
crudini --set $TX_NODE_CONFIG persistent_peers "peer1.testnet.tx.dev:26656,peer2.testnet.tx.dev:26656"
Step 7: Start the Node
Option 1: Start with Cosmovisor (Recommended)
Cosmovisor automatically handles chain upgrades.

bash
# Install cosmovisor
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@latest

# Set up cosmovisor
export DAEMON_NAME=txd
export DAEMON_HOME=$TX_HOME

# Start node with cosmovisor
cosmovisor run start $TX_CHAIN_ID_ARGS
Option 2: Start with txd Directly
bash
# Start node
txd start $TX_CHAIN_ID_ARGS
Step 8: Create Systemd Service (Recommended)
To ensure your node restarts automatically:

bash
# Create service file
sudo nano /etc/systemd/system/txd.service
Paste:

ini
[Unit]
Description=TX Full Node
After=network-online.target

[Service]
User=$USER
ExecStart=/usr/local/bin/txd start --chain-id $TX_CHAIN_ID
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
Step 9: Monitor Sync Status
Check if Node is Catching Up
bash
# Check sync status
echo "catching_up: $(txd status 2>/dev/null | jq -r '.SyncInfo.catching_up')"
If output is true, node is still syncing

If output is false, node is fully synced

Check Current Block Height
bash
# Get current block height
curl -s http://localhost:26657/status | jq .result.sync_info.latest_block_height
Monitor Logs for Progress
bash
# Look for increasing height values
sudo journalctl -u txd -f | grep height

# Or if running without systemd
txd start 2>&1 | grep height
If the height value is increasing, your node is syncing successfully!

Step 10: Verify Node is Working
Query Node Info
bash
# Get node info
txd status 2>/dev/null | jq .NodeInfo

# Check network
curl -s http://localhost:26657/status | jq .result.node_info.network

# Check peers
curl -s http://localhost:26657/net_info | jq '.result.peers | length'
Query a Block
bash
# Query latest block
txd query block --node http://localhost:26657

# Or using curl
curl -s http://localhost:26657/block | jq .result.block.header
Troubleshooting
Node Won't Sync
bash
# Check peer count
curl -s http://localhost:26657/net_info | jq '.result.peers | length'

# Add more seeds if peer count is low
crudini --set $TX_NODE_CONFIG seeds "seed1:26656,seed2:26656"

# Restart node
sudo systemctl restart txd
State Sync Issues
bash
# Clear state and restart sync
txd tendermint unsafe-reset-all

# Restart node
sudo systemctl restart txd
Configuration Parse Errors
If you see "File contains parsing errors" with crudini:

bash
# Check config file syntax
cat $TX_APP_CONFIG | grep -v "^#" | grep -v "^$"

# Manually edit config
nano $TX_APP_CONFIG
Resources
Validator Node Guide

State Sync Documentation

Troubleshooting Guide

Network Variables


