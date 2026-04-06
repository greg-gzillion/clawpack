# Run a Validator Node

## Overview
A validator node participates in consensus and produces blocks. Validators stake TX tokens and earn rewards.

## Requirements

- **Stake**: Minimum 1,000,000 TX
- **Hardware**: 4+ CPU cores, 16+ GB RAM, 500+ GB SSD
- **Uptime**: 99.9%+ required
- **Static IP**: Recommended
- **Security**: Hardware security module (HSM) recommended

## Step 1: Set Up Full Node First

Ensure you have a synced full node before proceeding:

```bash
# Wait for full sync
curl -s http://localhost:26657/status | jq .result.sync_info.catching_up
# Should return false
Step 2: Create Validator Wallet
bash
# Create wallet
txd keys add validator-key

# Save address and mnemonic securely
echo "Validator Address: $(txd keys show validator-key -a)"
Step 3: Get Tokens for Staking
Testnet: Use faucet

Mainnet: Purchase TX tokens or receive from community pool

Step 4: Check Balance
bash
# Check balance
txd query bank balances $(txd keys show validator-key -a) \
  --node http://localhost:26657
Step 5: Create Validator
bash
# Get validator pubkey
txd tendermint show-validator

# Create validator
txd tx staking create-validator \
  --amount=1000000utestcore \
  --pubkey=$(txd tendermint show-validator) \
  --moniker="<YOUR_MONIKER>" \
  --identity="<KEYBASE_ID>" \
  --website="<WEBSITE>" \
  --details="<DESCRIPTION>" \
  --commission-rate="0.05" \
  --commission-max-rate="0.20" \
  --commission-max-change-rate="0.01" \
  --min-self-delegation="1000000" \
  --from=validator-key \
  --chain-id=txchain-testnet-1 \
  --node=http://localhost:26657 \
  --gas=auto --gas-adjustment=1.3 \
  -y
Step 6: Verify Validator
bash
# Check validator
txd query staking validator $(txd keys show validator-key -a --bech=val) \
  --node http://localhost:26657

# Check if validator is in active set
txd query staking validators --node http://localhost:26657 | \
  jq '.validators[] | select(.status=="BOND_STATUS_BONDED") | .description.moniker'
Step 7: Monitor Validator
bash
# Check signing info
txd query slashing signing-info $(txd tendermint show-validator) \
  --node http://localhost:26657

# Check missed blocks
txd query slashing signing-info $(txd tendermint show-validator) \
  --node http://localhost:26657 | jq .missed_blocks_counter

# Check validator status
txd query staking validator $(txd keys show validator-key -a --bech=val) \
  --node http://localhost:26657 | jq .status
Step 8: Claim Rewards
bash
# Claim rewards
txd tx distribution withdraw-rewards $(txd keys show validator-key -a --bech=val) \
  --from validator-key \
  --chain-id txchain-testnet-1 \
  --node http://localhost:26657 \
  --gas=auto \
  -y

# Claim all rewards (including delegations)
txd tx distribution withdraw-all-rewards \
  --from validator-key \
  --chain-id txchain-testnet-1 \
  --node http://localhost:26657 \
  -y
Step 9: Delegate More Tokens
bash
# Delegate additional tokens to your validator
txd tx staking delegate $(txd keys show validator-key -a --bech=val) 500000utestcore \
  --from validator-key \
  --chain-id txchain-testnet-1 \
  --node http://localhost:26657 \
  -y
Validator Management
Edit Validator
bash
txd tx staking edit-validator \
  --moniker="New Name" \
  --identity="New Identity" \
  --website="https://new-website.com" \
  --details="Updated description" \
  --from validator-key \
  --chain-id txchain-testnet-1 \
  --node http://localhost:26657 \
  -y
Unjail Validator
bash
# If validator gets jailed
txd tx slashing unjail \
  --from validator-key \
  --chain-id txchain-testnet-1 \
  --node http://localhost:26657 \
  -y
Unbond Tokens
bash
# Unbond tokens (21 day unbonding period)
txd tx staking unbond $(txd keys show validator-key -a --bech=val) 500000utestcore \
  --from validator-key \
  --chain-id txchain-testnet-1 \
  --node http://localhost:26657 \
  -y
Security Best Practices
Key Management
Never expose private keys

Use hardware wallet (Ledger, D'Cent) for mainnet

Backup mnemonics offline

Use separate keys for validator and funds

Node Security
bash
# Run validator behind sentry nodes
# Firewall rules
sudo ufw allow 26656/tcp  # P2P
sudo ufw allow 22/tcp     # SSH
sudo ufw enable

# Regular updates
sudo apt update && sudo apt upgrade -y

# Monitor logs
sudo journalctl -u txd -f
Monitoring
bash
# Set up monitoring script
cat > ~/monitor_validator.sh << 'EOF'
#!/bin/bash
CATCHING_UP=$(curl -s http://localhost:26657/status | jq .result.sync_info.catching_up)
MISSED_BLOCKS=$(txd query slashing signing-info $(txd tendermint show-validator) -o json | jq .missed_blocks_counter)

echo "Catching up: $CATCHING_UP"
echo "Missed blocks: $MISSED_BLOCKS"

if [ "$MISSED_BLOCKS" -gt 50 ]; then
    echo "Warning: High missed blocks count!"
fi
EOF

chmod +x ~/monitor_validator.sh
Resources
Validator Requirements

Network Variables

Troubleshooting

Upgrade Guide

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

### 7. Run a Sentry Node

```bash
nano ~/dev/TXdocumentation/nodes/sentry-node/README.md
Paste:

markdown
# Run a Sentry Node

## Overview
Sentry nodes protect validator nodes from DDoS attacks by acting as a buffer between the validator and the public network.

## Architecture
┌─────────────────────────────────────────────────────────┐
│ Public Internet │
└─────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Sentry Node 1 │ Sentry Node 2 │ Sentry Node 3 │
└─────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Validator Node (private, no public P2P) │
└─────────────────────────────────────────────────────────┘

text

## Prerequisites

- **2-3 sentry nodes** for redundancy
- **Static IPs** for sentry nodes
- **Private network** between sentry and validator
- **Firewall configured**

## Step 1: Configure Sentry Node

```bash
# Initialize sentry node
txd init sentry-node --chain-id txchain-testnet-1

# Download genesis
wget -O ~/.txd/config/genesis.json https://raw.githubusercontent.com/tokenize-x/testnet/main/genesis.json

# Configure sentry
sed -i 's/seeds = ""/seeds = "seed.testnet.tx.dev:26656"/' ~/.txd/config/config.toml

# Enable P2P
sed -i 's/pex = false/pex = true/' ~/.txd/config/config.toml

# Set persistent peers (other sentries)
sed -i 's/persistent_peers = ""/persistent_peers = "sentry2:26656,sentry3:26656"/' ~/.txd/config/config.toml

# Disable private peer list
sed -i 's/private_peer_ids = ""/private_peer_ids = "<validator-node-id>"/' ~/.txd/config/config.toml

# Start sentry
txd start
Step 2: Configure Validator Node
bash
# On validator node
sed -i 's/seeds = ""/seeds = ""/' ~/.txd/config/config.toml

# Set sentries as persistent peers
sed -i 's/persistent_peers = ""/persistent_peers = "sentry1:26656,sentry2:26656,sentry3:26656"/' ~/.txd/config/config.toml

# Disable P2P peering
sed -i 's/pex = true/pex = false/' ~/.txd/config/config.toml

# Set private peer IDs
sed -i 's/private_peer_ids = ""/private_peer_ids = "<sentry1-id>,<sentry2-id>,<sentry3-id>"/' ~/.txd/config/config.toml

# Restart validator
sudo systemctl restart txd
Step 3: Configure Firewall
Sentry Node Firewall
bash
# Allow public P2P
sudo ufw allow 26656/tcp

# Allow validator private connection
sudo ufw allow from <validator-ip> to any port 26656

# Deny all other
sudo ufw default deny incoming
sudo ufw enable
Validator Node Firewall
bash
# Only allow sentry nodes
sudo ufw allow from <sentry1-ip> to any port 26656
sudo ufw allow from <sentry2-ip> to any port 26656
sudo ufw allow from <sentry3-ip> to any port 26656

# Allow SSH
sudo ufw allow 22/tcp

# Deny all other
sudo ufw default deny incoming
sudo ufw enable
Step 4: Verify Setup
bash
# On sentry, check peers
curl -s http://sentry1:26657/net_info | jq .result.peers[].node_info.id

# On validator, check sentry connections
curl -s http://validator:26657/net_info | jq .result.peers[].node_info.id
Monitoring Sentry Nodes
bash
# Check peer count
curl -s http://localhost:26657/net_info | jq '.result.peers | length'

# Check if validator is connected
curl -s http://localhost:26657/net_info | jq '.result.peers[] | select(.node_info.moniker=="validator")'

# Monitor logs
sudo journalctl -u txd -f
Resources
Validator Node

Full Node

Troubleshooting

