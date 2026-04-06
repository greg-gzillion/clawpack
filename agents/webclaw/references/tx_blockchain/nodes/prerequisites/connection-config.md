# Connection Configuration - Node Setup

This document describes the common connection configuration for any type of node (full, validator, or sentry).

## Prerequisites

- [ ] Node initialized (`txd init`)
- [ ] Environment variables set ([Network Variables](./network-variables.md))
- [ ] `crudini` installed (`sudo apt install crudini -y`)
- [ ] Public IP address configured

## Critical Consensus Setting

> ⚠️ **Important**: If you use your own or custom config, set `consensus.timeout_commit` to `1s` for proper block timing.

```bash
crudini --set $TX_HOME/config/config.toml consensus timeout_commit "1s"
Node Configuration Path
bash
# Set config path variable
export TX_NODE_CONFIG="$TX_HOME/config/config.toml"

# Verify it exists
ls -la $TX_NODE_CONFIG
Public IP Configuration
Step 1: Get Your Public IP
Your node must have a public IP address to be discoverable by other nodes.

bash
# Get your public IP
export TX_EXTERNAL_IP=$(curl -s ifconfig.me)
echo "Your public IP: $TX_EXTERNAL_IP"

# Or set manually
# export TX_EXTERNAL_IP="your-actual-public-ip"
Step 2: Verify IP is Reachable (Optional)
bash
# From your local machine, ping the IP
ping -c 4 $TX_EXTERNAL_IP

# From the server, check if port is open
nc -zv localhost 26656
Step 3: Update Config with External IP
bash
# Disable strict address book (allows dynamic peers)
crudini --set $TX_NODE_CONFIG p2p addr_book_strict false

# Set external address for peer discovery
crudini --set $TX_NODE_CONFIG p2p external_address "\"tcp://$TX_EXTERNAL_IP:26656\""
RPC and P2P Configuration
Enable RPC (Port 26657)
RPC allows queries and transaction broadcasting:

bash
# Bind to all interfaces (0.0.0.0) for external access
crudini --set $TX_NODE_CONFIG rpc laddr "\"tcp://0.0.0.0:26657\""

# For local-only access (more secure):
# crudini --set $TX_NODE_CONFIG rpc laddr "\"tcp://127.0.0.1:26657\""
Enable P2P (Port 26656)
P2P allows peer-to-peer communication for block propagation:

bash
# Bind to all interfaces for peer connections
crudini --set $TX_NODE_CONFIG p2p laddr "\"tcp://0.0.0.0:26656\""
Complete Configuration Commands
Run all these commands to configure your node:

bash
#!/bin/bash
# Complete connection configuration

export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"
export TX_NODE_CONFIG="$TX_HOME/config/config.toml"

# Consensus
crudini --set $TX_NODE_CONFIG consensus timeout_commit "1s"

# P2P Settings
crudini --set $TX_NODE_CONFIG p2p addr_book_strict false
crudini --set $TX_NODE_CONFIG p2p external_address "\"tcp://$TX_EXTERNAL_IP:26656\""
crudini --set $TX_NODE_CONFIG p2p laddr "\"tcp://0.0.0.0:26656\""

# RPC Settings
crudini --set $TX_NODE_CONFIG rpc laddr "\"tcp://0.0.0.0:26657\""

echo "✅ Connection configuration complete"
Firewall Configuration
Open Required Ports
bash
# Allow P2P (required for node communication)
sudo ufw allow 26656/tcp

# Allow RPC (optional - for queries)
sudo ufw allow 26657/tcp

# Allow REST API (optional)
sudo ufw allow 1317/tcp

# Allow gRPC (optional)
sudo ufw allow 9090/tcp

# Enable firewall if not already enabled
sudo ufw enable

# Check status
sudo ufw status
Cloud Provider Settings
If using cloud providers (AWS, GCP, Azure), also configure security groups:

Provider	Service	Port	Source
AWS	Security Group	26656	0.0.0.0/0
AWS	Security Group	26657	Your IP (or 0.0.0.0/0)
GCP	Firewall Rule	26656	0.0.0.0/0
Azure	NSG Rule	26656	Any
Port Summary
Port	Protocol	Purpose	Required	External Access
26656	TCP	P2P (peer communication)	✅ Yes	Yes (public)
26657	TCP	RPC (queries, txs)	⚠️ Optional	Limited/Internal
1317	TCP	REST API	⚠️ Optional	Internal only
9090	TCP	gRPC	⚠️ Optional	Internal only
26660	TCP	Prometheus metrics	⚠️ Optional	Internal only
Verification
Check Configuration
bash
# Verify settings
crudini --get $TX_NODE_CONFIG p2p external_address
crudini --get $TX_NODE_CONFIG rpc laddr
crudini --get $TX_NODE_CONFIG p2p laddr

# Should show your public IP
echo "External address: $(crudini --get $TX_NODE_CONFIG p2p external_address)"
Test Connectivity
bash
# From another machine, test RPC access
curl -s http://$TX_EXTERNAL_IP:26657/status | jq .result.node_info.network

# Check if node is reachable via P2P
nc -zv $TX_EXTERNAL_IP 26656
Troubleshooting
Port Not Accessible
bash
# Check if port is listening
sudo netstat -tulpn | grep 26656

# Check firewall
sudo ufw status verbose

# Check cloud provider security groups
Connection Refused
bash
# Verify config file syntax
cat $TX_NODE_CONFIG | grep -E "laddr|external_address"

# Ensure node is running
sudo systemctl status txd

# Check logs
sudo journalctl -u txd -f
IP Address Changes
If your IP changes (non-static), update it:

bash
# Get new IP
export TX_EXTERNAL_IP=$(curl -s ifconfig.me)

# Update config
crudini --set $TX_NODE_CONFIG p2p external_address "\"tcp://$TX_EXTERNAL_IP:26656\""

# Restart node
sudo systemctl restart txd
Security Recommendations
RPC Port: Consider restricting RPC access to trusted IPs only

Firewall: Only expose P2P port (26656) to the public

Internal Services: Keep REST API and gRPC behind internal network

Rate Limiting: Implement rate limiting on public RPC endpoints

Next Steps
After configuring connections:

Set up seeds and peers

Start your full node

Configure monitoring

Resources
Network Variables

System Requirements

Troubleshooting Guide
