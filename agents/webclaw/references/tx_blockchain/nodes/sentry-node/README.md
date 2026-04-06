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

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

### 2. Create Network Variables (if missing)

```bash
# Check if network-variables.md exists
ls ~/dev/TXdocumentation/nodes/prerequisites/network-variables.md

# If not, create it
nano ~/dev/TXdocumentation/nodes/prerequisites/network-variables.md
If it doesn't exist, paste:

markdown
# Network Variables

## Mainnet

| Variable | Value |
|----------|-------|
| **Chain ID** | `tx-mainnet-1` |
| **Denom** | `utx` |
| **Bech32 Prefix** | `core` |
| **Seed Nodes** | `seed.tx.org:26656` |
| **Persistent Peers** | `peer1.tx.org:26656,peer2.tx.org:26656` |
| **RPC Endpoint** | `https://rpc.tx.org:443` |
| **API Endpoint** | `https://api.tx.org:443` |
| **Genesis File** | `https://raw.githubusercontent.com/tokenize-x/mainnet/main/genesis.json` |
| **Minimum Gas Price** | `0.0625utx` |

## Testnet

| Variable | Value |
|----------|-------|
| **Chain ID** | `txchain-testnet-1` |
| **Denom** | `utestcore` |
| **Bech32 Prefix** | `testcore` |
| **Seed Nodes** | `seed.testnet.tx.dev:26656` |
| **Persistent Peers** | `peer1.testnet.tx.dev:26656,peer2.testnet.tx.dev:26656` |
| **RPC Endpoint** | `https://rpc.testnet.tx.dev:443` |
| **API Endpoint** | `https://api.testnet.tx.dev:443` |
| **Genesis File** | `https://raw.githubusercontent.com/tokenize-x/testnet/main/genesis.json` |
| **Minimum Gas Price** | `0.0625utestcore` |

## Devnet / Local

| Variable | Value |
|----------|-------|
| **Chain ID** | `txchain-local` |
| **Denom** | `udevcore` |
| **Bech32 Prefix** | `testcore` |
| **Seed Nodes** | (none) |
| **RPC Endpoint** | `http://localhost:26657` |
| **API Endpoint** | `http://localhost:1317` |
Save: Ctrl+O, Enter, Ctrl+X

3. Create System Requirements (if missing)
bash
# Check if system-requirements.md exists
ls ~/dev/TXdocumentation/nodes/prerequisites/system-requirements.md

# If not, create it
nano ~/dev/TXdocumentation/nodes/prerequisites/system-requirements.md
If it doesn't exist, paste:

markdown
# System Requirements for TX Nodes

## Minimum Requirements (Testnet/Development)

| Component | Requirement |
|-----------|-------------|
| **CPU** | 2+ cores |
| **RAM** | 8 GB |
| **Storage** | 100 GB SSD |
| **Network** | 10 Mbps |

## Recommended Requirements (Mainnet Production)

| Component | Requirement |
|-----------|-------------|
| **CPU** | 4+ cores (8+ recommended) |
| **RAM** | 16 GB (32 GB recommended) |
| **Storage** | 500 GB - 1 TB SSD/NVMe |
| **Network** | 100 Mbps+ |

## Storage Growth Estimates

| Network | Initial Size | Monthly Growth | Yearly Growth |
|---------|--------------|----------------|---------------|
| Testnet | ~10 GB | ~5 GB | ~70 GB |
| Mainnet | ~20 GB | ~10-15 GB | ~150-200 GB |

## Network Requirements

- **Ports**: 26656 (P2P), 26657 (RPC), 1317 (API)
- **Firewall**: Allow incoming connections on P2P port
- **Static IP**: Recommended for validator nodes
- **Uptime**: 99.9%+ for validators

## Operating System

- **Linux**: Ubuntu 20.04/22.04 LTS (recommended)
- **macOS**: Development only
- **Windows**: Not recommended for production

## Dependencies

- Go 1.21+
- Git
- Make
- GCC
- jq (for JSON processing)
Save: Ctrl+O, Enter, Ctrl+X

4. Create Validator Funds Guide
bash
nano ~/dev/TXdocumentation/nodes/prerequisites/validator-funds.md
Paste:

markdown
# Validator Funding Requirements

## Minimum Staking Requirement

| Network | Minimum Self-Delegation | Recommended |
|---------|------------------------|-------------|
| **Mainnet** | 1,000,000 TX | 2,000,000+ TX |
| **Testnet** | 1,000,000 utestcore | 2,000,000+ utestcore |
| **Devnet** | 1,000,000 udevcore | N/A |

## Cost Breakdown

### Initial Costs

| Item | Cost (Mainnet) |
|------|----------------|
| **Self-delegation** | 1,000,000 TX (~$50,000 - $100,000) |
| **Hardware** | $1,000 - $5,000/year |
| **Network** | $100 - $500/month |
| **Setup** | $0 - $1,000 (DIY or consultant) |

### Ongoing Costs

| Item | Monthly Cost |
|------|--------------|
| **Server hosting** | $50 - $200 |
| **Bandwidth** | $20 - $100 |
| **Monitoring** | $0 - $50 |
| **Maintenance** | $0 - $500 (time) |

## Total Supply Considerations

### Mainnet
- **Total Supply**: 1,000,000,000 TX
- **Active Set**: 150 validators
- **Avg Stake per Validator**: ~6,666,666 TX
- **Minimum**: 1,000,000 TX (may not guarantee active set)

### Testnet
- **Total Supply**: Unlimited (faucet)
- **Active Set**: 150 validators
- **Minimum**: 1,000,000 utestcore

## ROI Expectations

### Staking Rewards
- **Annual Inflation**: ~7%
- **Validator Commission**: 5-20%
- **Delegator Share**: 80-95% of rewards

### Example Calculation (Mainnet)
Total Stake: 2,000,000 TX
Annual Rewards (7%): 140,000 TX
Commission (10%): 14,000 TX
Net Validator Rewards: 126,000 TX (~$6,300 - $12,600/year)

text

## Getting Tokens

### Testnet
1. Visit faucet: https://faucet.testnet.tx.dev
2. Enter your testcore address
3. Request tokens
4. Repeat until you have sufficient stake

### Mainnet
1. Participate in pre-launch sales
2. Purchase from exchanges post-launch
3. Apply for community grants
4. Bootstrap with testnet rewards

## Resources
- [Network Variables](./network-variables.md)
- [Validator Setup](../validator-node/README.md)
- [Faucet](../../ecosystem/faucet/README.md)
Save: Ctrl+O, Enter, Ctrl+X

5. Verify Complete Structure
bash
# Show complete node documentation structure
tree ~/dev/TXdocumentation/nodes -L 2
You should now see:

text
/home/greg/dev/TXdocumentation/nodes
├── full-node
│   └── README.md
├── prerequisites
│   ├── install-txd.md
│   ├── network-variables.md
│   ├── README.md
│   ├── system-requirements.md
│   └── validator-funds.md
├── sentry-node
│   └── README.md
├── troubleshooting
│   ├── README.md
│   └── upgrade-guide.md
└── validator-node
    └── README.md

5 directories, 10 files
