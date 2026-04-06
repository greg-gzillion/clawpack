# Run a Sentry Node - Complete Setup Guide

## Overview
A sentry node acts as a protective shield for validator nodes, preventing DDoS attacks and hiding the validator's IP address from the public network.

For additional information about this node type, see the [Sentry Node Architecture Overview](./README.md).

## Prerequisites

Before starting, ensure you have:

- [ ] System requirements met ([System Requirements](../prerequisites/system-requirements.md))
- [ ] `txd` binary installed ([Install txd](../prerequisites/install-txd.md))
- [ ] Network variables configured ([Network Variables](../prerequisites/network-variables.md))
- [ ] `crudini` installed: `sudo apt install crudini -y`
- [ ] Validator node already set up (for peer information)

## Step 1: Set Up Node Prerequisites

### Set the Moniker
Choose a unique name for your sentry node:

```bash
export MONIKER="sentry1"
Set Chain ID
Choose your network:

bash
# For testnet:
export TX_CHAIN_ID="txchain-testnet-1"
export TX_CHAIN_ID_ARGS="--chain-id $TX_CHAIN_ID"

# For mainnet:
# export TX_CHAIN_ID="tx-mainnet-1"
# export TX_CHAIN_ID_ARGS="--chain-id $TX_CHAIN_ID"
Set Home Directory
bash
export TX_HOME=~/.txd
Step 2: Initialize the Node
bash
txd init $MONIKER $TX_CHAIN_ID_ARGS
This creates the default node configuration in $TX_HOME/config/.

Step 3: Download Genesis and Configure Network
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
# Set minimum gas price
crudini --set $TX_HOME/config/app.toml minimum-gas-prices "0.0625utestcore"
Step 4: Capture Validator Peer Information
⚠️ Important: These commands must be executed on the validator node.

bash
# On the validator node, get the peer ID and IP
echo "TX_VALIDATOR_PEER=$(txd tendermint show-node-id)@$TX_EXTERNAL_IP:26656"
echo "TX_VALIDATOR_ID=$(txd tendermint show-node-id)"
If TX_EXTERNAL_IP is not set, configure it in your validator's config.toml:

bash
# On validator node
crudini --set $TX_HOME/config/config.toml p2p external_address "tcp://$TX_EXTERNAL_IP:26656"
Step 5: Set Validator Peer Variables on Sentry Node
bash
# On sentry node, set these variables (from validator node output)
export TX_VALIDATOR_PEER="<validator-peer-id>@<validator-ip>:26656"
export TX_VALIDATOR_ID="<validator-node-id>"
Example:

bash
export TX_VALIDATOR_PEER="86c5be788da1ebd1c5a7f52d5e2f159039ee218c@10.0.0.1:26656"
export TX_VALIDATOR_ID="86c5be788da1ebd1c5a7f52d5e2f159039ee218c"
Step 6: Configure Sentry Node
Set the node config path:

bash
TX_NODE_CONFIG=$TX_HOME/config/config.toml
Configure P2P Settings
bash
# Enable peer exchange (sentry nodes should be public)
crudini --set $TX_NODE_CONFIG p2p pex true

# Set validator as persistent peer (always maintain connection)
crudini --set $TX_NODE_CONFIG p2p persistent_peers "\"$TX_VALIDATOR_PEER\""

# Hide validator ID from other peers
crudini --set $TX_NODE_CONFIG p2p private_peer_ids "\"$TX_VALIDATOR_ID\""

# Always allow connection to validator
crudini --set $TX_NODE_CONFIG p2p unconditional_peer_ids "\"$TX_VALIDATOR_ID\""
Configure Seeds (Optional)
Add seeds for initial peer discovery:

bash
# Testnet seeds
crudini --set $TX_NODE_CONFIG seeds "seed.testnet.tx.dev:26656"

# Mainnet seeds
# crudini --set $TX_NODE_CONFIG seeds "seed.tx.org:26656"
Configure External Address
Set your sentry node's public IP:

bash
export TX_EXTERNAL_IP="<your-sentry-public-ip>"
crudini --set $TX_NODE_CONFIG p2p external_address "\"tcp://$TX_EXTERNAL_IP:26656\""
Step 7: Capture Sentry Peer Information
⚠️ Important: These commands must be executed on the sentry node.

bash
# Get the sentry node's peer string (for other nodes to connect)
echo "$(txd tendermint show-node-id)@$TX_EXTERNAL_IP:26656"

# Get the sentry node's ID
echo "$(txd tendermint show-node-id)"
Save these values for configuring the validator node and other sentries.

Step 8: Start the Sentry Node
Option 1: Start with Cosmovisor (Recommended)
bash
# Install cosmovisor if not already installed
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@latest

# Set up cosmovisor
export DAEMON_NAME=txd
export DAEMON_HOME=$TX_HOME

# Start node with cosmovisor
cosmovisor run start $TX_CHAIN_ID_ARGS
Option 2: Start with txd Directly
bash
txd start $TX_CHAIN_ID_ARGS
Step 9: Create Systemd Service
To ensure your sentry node restarts automatically:

bash
sudo nano /etc/systemd/system/txd-sentry.service
Paste:

ini
[Unit]
Description=TX Sentry Node
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
sudo systemctl enable txd-sentry
sudo systemctl start txd-sentry

# Check status
sudo systemctl status txd-sentry

# View logs
sudo journalctl -u txd-sentry -f
Step 10: Repeat for Multiple Sentry Nodes
For redundancy, run multiple sentry nodes (2-3 recommended). Repeat steps 1-9 for each sentry node.

After setting up all sentry nodes, collect their peer strings:

bash
# Example of multiple sentry peers
# sentry1: 86c5be788da1ebd1c5a7f52d5e2f159039ee218c@172.19.0.6:26656
# sentry2: 095f7e0a462cf749027ee22913d77619fe1c2267@172.29.0.8:26656
# sentry3: 2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b@172.30.0.10:26656
Step 11: Configure Validator Node to Connect to Sentries
Now go back to the validator node to connect it to the sentry nodes.

On Validator Node:
bash
# Set sentry peers (comma-separated list from all sentry nodes)
export TX_SENTRY_PEERS="sentry1-peer@sentry1-ip:26656,sentry2-peer@sentry2-ip:26656,sentry3-peer@sentry3-ip:26656"

# Set sentry IDs (comma-separated list)
export TX_SENTRY_IDS="sentry1-id,sentry2-id,sentry3-id"
Example:

bash
export TX_SENTRY_PEERS="86c5be788da1ebd1c5a7f52d5e2f159039ee218c@172.19.0.6:26656,095f7e0a462cf749027ee22913d77619fe1c2267@172.29.0.8:26656"
export TX_SENTRY_IDS="86c5be788da1ebd1c5a7f52d5e2f159039ee218c,095f7e0a462cf749027ee22913d77619fe1c2267"
Configure Validator Node
bash
# Set config path
TX_NODE_CONFIG=$TX_HOME/config/config.toml

# Disable peer exchange (validator should not be public)
crudini --set $TX_NODE_CONFIG p2p pex false

# Set sentries as persistent peers
crudini --set $TX_NODE_CONFIG p2p persistent_peers "\"$TX_SENTRY_PEERS\""

# Hide sentry IDs from other peers
crudini --set $TX_NODE_CONFIG p2p private_peer_ids "\"$TX_SENTRY_IDS\""

# Always allow connection to sentries
crudini --set $TX_NODE_CONFIG p2p unconditional_peer_ids "\"$TX_SENTRY_IDS\""

# Disable strict address book (allow sentry IPs)
crudini --set $TX_NODE_CONFIG p2p addr_book_strict false
Restart Validator Node
bash
sudo systemctl restart txd

# Check logs
sudo journalctl -u txd -f
Step 12: Verify Sentry Setup
On Sentry Node:
bash
# Check if connected to validator
curl -s http://localhost:26657/net_info | jq '.result.peers[] | select(.node_info.moniker=="validator")'

# Check peer count
curl -s http://localhost:26657/net_info | jq '.result.peers | length'

# Check if sentry is public (should have many peers)
curl -s http://localhost:26657/net_info | jq '.result.peers | length' # Should be > 0
On Validator Node:
bash
# Check if connected to sentries
curl -s http://localhost:26657/net_info | jq '.result.peers[] | select(.node_info.moniker | contains("sentry"))'

# Should show sentry1, sentry2, sentry3 connections
Network Topology After Setup
text
┌─────────────────────────────────────────────────────────────┐
│ Public Internet │
└─────────────────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Sentry 1 │ │ Sentry 2 │ │ Sentry 3 │
│ (Public) │ │ (Public) │ │ (Public) │
└─────────────┘ └─────────────┘ └─────────────┘
         │              │              │
         └──────────────┼──────────────┘
                        ▼
              ┌─────────────────┐
              │ Validator Node │
              │ (Private) │
              └─────────────────┘
Troubleshooting
Sentry Not Connecting to Validator
bash
# Check if validator is reachable
ping <validator-ip>

# Check if port is open
nc -zv <validator-ip> 26656

# Check validator's P2P config
# Validator should have pex=false and sentries in persistent_peers
Validator Not Connecting to Sentries
bash
# On validator, check persistent_peers setting
crudini --get $TX_NODE_CONFIG p2p persistent_peers

# Check sentry addresses are correct
# Should be: <node-id>@<ip>:26656
Connection Refused
bash
# Check firewall rules
sudo ufw status

# Ensure P2P port is open on sentries
sudo ufw allow 26656/tcp

# On validator, ensure it's only allowing sentry connections
sudo ufw allow from <sentry-ip> to any port 26656
Resources
Sentry Node Overview

Validator Node Setup

Network Variables

Troubleshooting Guide

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

### Update Sentry Node README

```bash
nano ~/dev/TXdocumentation/nodes/sentry-node/README.md
Replace with concise overview:

markdown
# Run a Sentry Node

## Overview
Sentry nodes protect validator nodes from DDoS attacks by acting as a buffer between the validator and the public network.

## Architecture
┌─────────────────────────────────────────────────────────────┐
│ Public Internet │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Sentry Nodes (Public, 2-3 recommended) │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Validator Node (Private, no public P2P) │
└─────────────────────────────────────────────────────────────┘

text

## Quick Setup

For detailed step-by-step instructions, see the [Complete Setup Guide](./setup-guide.md).

### Key Configuration Points

**Sentry Node:**
- `pex = true` - Public peer exchange
- `persistent_peers = "<validator-id>@<validator-ip>:26656"`
- `private_peer_ids = "<validator-id>"`
- `unconditional_peer_ids = "<validator-id>"`

**Validator Node:**
- `pex = false` - Private, no peer exchange
- `persistent_peers = "<sentry1-id>@<sentry1-ip>:26656,<sentry2-id>@<sentry2-ip>:26656"`
- `private_peer_ids = "<sentry1-id>,<sentry2-id>"`
- `unconditional_peer_ids = "<sentry1-id>,<sentry2-id>"`
- `addr_book_strict = false`

## Prerequisites

- [System Requirements](../prerequisites/system-requirements.md)
- [Install txd](../prerequisites/install-txd.md)
- [Network Variables](../prerequisites/network-variables.md)
- Validator node already set up

## Documentation

- [Complete Setup Guide](./setup-guide.md) - Detailed step-by-step instructions
- [Validator Node Setup](../validator-node/README.md)
- [Troubleshooting](../troubleshooting/README.md)

## Benefits

- **DDoS Protection**: Validator IP hidden from public
- **High Availability**: Multiple sentries ensure redundancy
- **Network Isolation**: Validator only communicates with trusted sentries
- **Scalability**: Add more sentries as needed
