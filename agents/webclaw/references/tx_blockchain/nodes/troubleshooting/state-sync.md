# State Sync Configuration

## Overview
State sync allows a new node to join the network quickly by downloading a snapshot of the application state at a recent height, rather than replaying all blocks from genesis.

## Benefits
- **Fast sync**: Hours instead of days/weeks
- **Low storage**: Doesn't require full block history
- **Quick recovery**: Rapidly restore failed nodes

## Prerequisites

- [ ] `txd` installed and configured
- [ ] Node initialized (`txd init`)
- [ ] Network variables set ([Network Variables](../prerequisites/network-variables.md))

## Step 1: Get State Sync Servers

### Testnet State Sync Servers
```bash
export TX_STATE_SYNC_SERVERS="https://rpc-01.testnet-1.tx.org:443,https://archive.rpc.testnet-1.tx.org:443"
Mainnet State Sync Servers
bash
export TX_STATE_SYNC_SERVERS="https://rpc-01.mainnet-1.tx.org:443,https://rpc-02.mainnet-1.tx.org:443"
Step 2: Get Trusted Block Height and Hash
bash
# Get current block height from first server
CURRENT_BLOCK_DETAILS=$(curl -s ${TX_STATE_SYNC_SERVERS%%,*}/block | jq -r '.result.block.header.height + " " + .result.block_id.hash')
CURRENT_BLOCK_HEIGHT=$(echo $CURRENT_BLOCK_DETAILS | awk '{print $1}')
echo "Current block height: $CURRENT_BLOCK_HEIGHT"

# Set trusted height (current - 1000 blocks)
TRUSTED_BLOCK_HEIGHT=$((CURRENT_BLOCK_HEIGHT - 1000))
echo "Trusted block height: $TRUSTED_BLOCK_HEIGHT"

# Get trusted block hash
TRUSTED_BLOCK_HASH=$(curl -s "${TX_STATE_SYNC_SERVERS%%,*}/block?height=${TRUSTED_BLOCK_HEIGHT}" | jq -r '.result.block_id.hash')
echo "Trusted block hash: $TRUSTED_BLOCK_HASH"

# Verify
echo "height: $TRUSTED_BLOCK_HEIGHT, hash: $TRUSTED_BLOCK_HASH"
Step 3: Configure State Sync
bash
# Set config path
export TX_NODE_CONFIG="$TX_HOME/config/config.toml"

# Enable state sync
crudini --set $TX_NODE_CONFIG statesync enable true

# Set RPC servers
crudini --set $TX_NODE_CONFIG statesync rpc_servers "\"$TX_STATE_SYNC_SERVERS\""

# Set trusted height and hash
crudini --set $TX_NODE_CONFIG statesync trust_height $TRUSTED_BLOCK_HEIGHT
crudini --set $TX_NODE_CONFIG statesync trust_hash "\"$TRUSTED_BLOCK_HASH\""

# Optional: Set trust period (default: 2 weeks)
crudini --set $TX_NODE_CONFIG statesync trust_period "336h"
Step 4: Reset Node and Start Sync
bash
# Reset any existing state
txd tendermint unsafe-reset-all

# Start node with cosmovisor
cosmovisor run start --chain-id $TX_CHAIN_ID
Step 5: Monitor Sync Progress
bash
# Check if node is syncing
curl -s http://localhost:26657/status | jq .result.sync_info

# Watch sync progress
watch -n 2 'curl -s http://localhost:26657/status | jq .result.sync_info'
Complete State Sync Script
bash
#!/bin/bash
# state-sync.sh - Configure and start state sync

export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"

# Set state sync servers (change for your network)
export TX_STATE_SYNC_SERVERS="https://rpc-01.testnet-1.tx.org:443,https://archive.rpc.testnet-1.tx.org:443"

# Get trusted height and hash
CURRENT_HEIGHT=$(curl -s ${TX_STATE_SYNC_SERVERS%%,*}/block | jq -r .result.block.header.height)
TRUSTED_HEIGHT=$((CURRENT_HEIGHT - 1000))
TRUSTED_HASH=$(curl -s "${TX_STATE_SYNC_SERVERS%%,*}/block?height=${TRUSTED_HEIGHT}" | jq -r .result.block_id.hash)

# Configure state sync
crudini --set $TX_HOME/config/config.toml statesync enable true
crudini --set $TX_HOME/config/config.toml statesync rpc_servers "\"$TX_STATE_SYNC_SERVERS\""
crudini --set $TX_HOME/config/config.toml statesync trust_height $TRUSTED_HEIGHT
crudini --set $TX_HOME/config/config.toml statesync trust_hash "\"$TRUSTED_HASH\""

# Reset and start
txd tendermint unsafe-reset-all
cosmovisor run start --chain-id $TX_CHAIN_ID
Troubleshooting
State Sync Stuck
bash
# Check peer count
curl -s http://localhost:26657/net_info | jq '.result.peers | length'

# Verify state sync config
crudini --get $TX_HOME/config/config.toml statesync enable
crudini --get $TX_HOME/config/config.toml statesync rpc_servers
Trusted Height Too Old
bash
# Use a more recent height (current - 100)
TRUSTED_HEIGHT=$((CURRENT_HEIGHT - 100))
Snapshots Not Available
bash
# Check if node provides snapshots
curl -s ${TX_STATE_SYNC_SERVERS%%,*}/snapshot | jq .
Notes
State sync nodes don't have full block history

For archive nodes, use regular txd start without state sync

Trust period should be > (unbonding period + block time)

Minimum snapshot interval: 500 blocks

Resources
Full Node Setup

Troubleshooting Guide

Network Variables

