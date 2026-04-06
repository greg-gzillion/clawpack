# Node Troubleshooting Guide

This document covers common issues and solutions for TX Blockchain nodes.

## Network Connection Issues

### Node Not Visible to Other Nodes

Your node must be visible to other nodes within the network.

**Check if your node is reachable:**

```bash
# From your local machine, ping the node
ping YOUR_NODE_PUBLIC_IP

# Test P2P port connectivity
nc -zv YOUR_NODE_PUBLIC_IP 26656

# Check if node is connected to peers
curl -s http://localhost:26657/net_info | jq '.result.peers | length'
Solutions:

Ensure firewall allows port 26656 (P2P)

Verify external_address in config.toml is correct

Check cloud provider security groups

Ensure node has a public IP address

Verify external address config:

bash
crudini --get $TX_HOME/config/config.toml p2p external_address
# Should show: "tcp://YOUR_IP:26656"
Configuration File Parsing Errors
Error: "File contains parsing errors"
If your crudini version is below 0.9.3, you might encounter:

text
Error parsing ~/.txd/txchain-testnet-1/config/app.toml: File contains parsing errors: <???>
[line 104]: ]
Solution 1: Update crudini

bash
# Check current version
crudini --version

# Update to latest version
sudo apt update
sudo apt install crudini

# Or install from source for latest version
pip3 install --upgrade crudini
Solution 2: Manual config fix

Open app.toml and replace:

toml
global-labels = [
]
With:

toml
global-labels = []
One-liner fix:

bash
sed -i 's/global-labels = \[/global-labels = \[\]/g' $TX_HOME/config/app.toml
sed -i '/^\]$/d' $TX_HOME/config/app.toml
Validator Missing Blocks
High Missed Block Count
Your validator should maintain > 95% uptime. If you're missing blocks, check the following:

Check uptime:

Validators.info

Mintscan

Common Causes and Solutions
1. Insufficient Hardware Resources
Check system resources:

bash
# CPU usage
top -bn1 | grep "Cpu(s)"

# Memory usage
free -h

# Disk I/O
iostat -x 1
Requirements:

⚠️ Critical: Must use NVMe SSD (not HDD or network storage)

Minimum 4+ CPU cores

16+ GB RAM

2. High I/O Wait
Install htop to monitor I/O wait:

bash
sudo apt install htop -y
htop
Look for high %wa (I/O wait) values. If consistently > 10%:

Upgrade to NVMe SSD

Reduce other disk-intensive processes

Consider dedicated bare-metal server

3. Network Latency
Check network connectivity:

bash
# Check ping to other nodes
ping -c 10 rpc.tx.org

# Check network stats
netstat -s | grep -i error

# Monitor peer connections
curl -s http://localhost:26657/net_info | jq '.result.peers[] | .node_info.moniker'
4. Check Validator Status
bash
# Check if validator is jailed
txd query staking validator $(txd keys show validator -a --bech=val) | jq .jailed

# Check missed blocks counter
txd query slashing signing-info $(txd tendermint show-validator) | jq .missed_blocks_counter

# Check validator status
txd query staking validator $(txd keys show validator -a --bech=val) | jq .status
Recovery Steps
If validator is jailed:

bash
# Unjail validator
txd tx slashing unjail --from validator --chain-id $TX_CHAIN_ID --node $TX_NODE -y

# Wait for next block (~6 seconds)
# Check if active again
If node is out of sync:

bash
# Check sync status
curl -s http://localhost:26657/status | jq .result.sync_info

# If catching_up = true, wait for sync
# If severely behind, consider state sync
Node Won't Start
Check Logs
bash
# With systemd
sudo journalctl -u txd -n 100

# Without systemd
tail -100 $TX_HOME/txd.log
Common Startup Issues
Corrupted state:

bash
# Reset node (keeps keys)
txd tendermint unsafe-reset-all
Missing genesis file:

bash
# Download genesis
wget -O $TX_HOME/config/genesis.json <genesis-url>

# Verify
txd validate-genesis
Port already in use:

bash
# Check port conflicts
sudo netstat -tulpn | grep -E "26656|26657"

# Change ports in config.toml if needed
Insufficient disk space:

bash
# Check disk usage
df -h $TX_HOME

# Prune old data if needed
txd prune
State Sync Issues
Node Stuck at Specific Height
Check state sync configuration:

bash
crudini --get $TX_HOME/config/config.toml statesync enable
crudini --get $TX_HOME/config/config.toml statesync rpc_servers
Solutions:

Verify RPC servers are reachable

Increase trust period: crudini --set $TX_HOME/config/config.toml statesync trust_period "336h"

Reset and retry with different snapshot height

Reset state sync:

bash
txd tendermint unsafe-reset-all
# Reconfigure state sync and restart
Cosmovisor Issues
Binary Not Found
bash
# Check binary location
ls -la $TX_HOME/cosmovisor/genesis/bin/txd

# Check permissions (must be a+x, not just u+x)
ls -la $TX_HOME/cosmovisor/genesis/bin/txd
# Should show: -rwxr-xr-x

# Fix permissions
chmod a+x $TX_HOME/cosmovisor/genesis/bin/txd
Upgrade Not Triggering
bash
# Check upgrade plan
txd q upgrade plan

# Verify binary in upgrades directory
ls -la $TX_HOME/cosmovisor/upgrades/*/bin/txd

# Check cosmovisor logs
sudo journalctl -u txd -f | grep -i upgrade
RPC Connection Issues
Cannot Connect to RPC
Check if RPC is enabled:

bash
crudini --get $TX_HOME/config/config.toml rpc laddr
# Should show: "tcp://0.0.0.0:26657" or "tcp://127.0.0.1:26657"
Test RPC locally:

bash
curl -s http://localhost:26657/status | jq .
Test RPC remotely:

bash
curl -s http://YOUR_NODE_IP:26657/status | jq .
Firewall issues:

bash
# Allow RPC port
sudo ufw allow 26657/tcp
Performance Issues
High Memory Usage
bash
# Check memory usage
ps aux --sort=-%mem | head -10

# Check Go garbage collection
export GODEBUG=gctrace=1
Solutions:

Reduce cache size in config.toml

Add swap space

Upgrade RAM

High CPU Usage
bash
# Identify CPU-heavy processes
top -c

# Check if node is catching up
curl -s http://localhost:26657/status | jq .result.sync_info.catching_up
Solutions:

Wait for sync to complete

Optimize pruning settings

Upgrade CPU

Diagnostic Commands
Quick Health Check
bash
#!/bin/bash
# node-health.sh - Check node health

echo "=== Node Status ==="
curl -s http://localhost:26657/status | jq .result.sync_info

echo -e "\n=== Peer Count ==="
curl -s http://localhost:26657/net_info | jq '.result.peers | length'

echo -e "\n=== Validator Status ==="
txd query staking validator $(txd keys show validator -a --bech=val) 2>/dev/null | jq .status

echo -e "\n=== Missed Blocks ==="
txd query slashing signing-info $(txd tendermint show-validator) 2>/dev/null | jq .missed_blocks_counter

echo -e "\n=== Disk Usage ==="
df -h $TX_HOME

echo -e "\n=== Memory Usage ==="
free -h
Network Diagnostics
bash
# Test peer connectivity
for peer in $(curl -s http://localhost:26657/net_info | jq -r '.result.peers[].node_info.listen_addr'); do
    echo "Testing $peer..."
    nc -zv ${peer%:*} ${peer#*:} 2>&1
done

# Check for slow peers
curl -s http://localhost:26657/consensus_state | jq '.result.round_state.votes'
Getting Help
If you're still unable to resolve the issue:

Check the documentation:

System Requirements

Network Variables

Validator Setup

Join the community:

Discord Server

Telegram Group

Forum

Gather debug info:

bash
# Collect diagnostic information
./node-health.sh > debug-info.txt
echo "TX_HOME=$TX_HOME" >> debug-info.txt
echo "TX_CHAIN_ID=$TX_CHAIN_ID" >> debug-info.txt
txd version >> debug-info.txt
Resources
Upgrade Guide

State Sync Guide

Upgrade History

Validator Funding
