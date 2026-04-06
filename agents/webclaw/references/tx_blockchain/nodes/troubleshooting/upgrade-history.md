# TX Blockchain Upgrade History

## Running a Node with Full Block History

To run a node with **full block history** (not state sync), you need:

1. Run with **cosmovisor** (not `txd` directly)
2. Provide **all binaries** the chain has used from genesis
3. Place binaries in the correct directory structure

### Directory Structure for Full History

If the network had upgrades `v1`, `v2`, and `v3`, the structure should be:
cosmovisor/
├── genesis/
│ └── bin/
│ └── txd # Genesis version
└── upgrades/
├── v1/
│ └── bin/
│ └── txd # v1 upgrade version
├── v2/
│ └── bin/
│ └── txd # v2 upgrade version
└── v3/
└── bin/
└── txd # v3 upgrade version

text

> ⚠️ **Important**: Each `txd` binary must have its specific version corresponding to the tables below. Find binaries at the [txd releases page](https://github.com/tokenize-x/tx-chain/releases).

### Running Full History Node

All steps are the same as the [full node setup](../full-node/setup-guide.md), **except**:
- **DO NOT** enable state sync
- **DO** provide all historical binaries
- The node will replay all blocks from genesis

---

## Mainnet Upgrade History

| Name | Height | Version | Cosmovisor |
|------|--------|---------|------------|
| genesis | 0 | v1.0.0 | v1.3.0 |
| v2 | 6,947,500 | v2.0.2 | v1.3.0 |
| v3 | 13,480,000 | v3.0.3 | v1.5.0 |
| v4 | 23,338,750 | v4.0.1 | v1.5.0 |
| v4patch1 | 25,891,000 | v4.1.0 | v1.5.0 |
| v4patch2 | 32,312,000 | v4.1.2 | v1.5.0 |
| v5 | 39,810,000 | v5.0.0 | v1.5.0 |
| v6 | 66,484,000 | v6.0.1 | v1.5.0 |
| v6 | 67,170,000 | v6.1.0 | v1.5.0 |

### Mainnet Binary Setup Script

```bash
#!/bin/bash
# Setup full history node for Mainnet

export TX_HOME="$HOME/.txd/tx-mainnet-1"

# Create directory structure
mkdir -p $TX_HOME/cosmovisor/genesis/bin
mkdir -p $TX_HOME/cosmovisor/upgrades/v2/bin
mkdir -p $TX_HOME/cosmovisor/upgrades/v3/bin
mkdir -p $TX_HOME/cosmovisor/upgrades/v4/bin
mkdir -p $TX_HOME/cosmovisor/upgrades/v4patch1/bin
mkdir -p $TX_HOME/cosmovisor/upgrades/v4patch2/bin
mkdir -p $TX_HOME/cosmovisor/upgrades/v5/bin
mkdir -p $TX_HOME/cosmovisor/upgrades/v6/bin

# Download and place binaries (replace URLs with actual release URLs)
# genesis (v1.0.0)
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/v1.0.0/txd-linux-amd64
chmod a+x txd-linux-amd64
mv txd-linux-amd64 $TX_HOME/cosmovisor/genesis/bin/txd

# v2 (v2.0.2)
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/v2.0.2/txd-linux-amd64
chmod a+x txd-linux-amd64
mv txd-linux-amd64 $TX_HOME/cosmovisor/upgrades/v2/bin/txd

# Continue for all upgrade versions...

echo "✅ Mainnet full history binaries installed"
Testnet Upgrade History
Name	Height	Version	Cosmovisor
genesis	0	v0.1.1	v1.3.0
v1	3,233,700	v1.0.0	v1.3.0
v2	8,728,400	v2.0.0	v1.3.0
v2patch1	9,122,200	v2.0.2	v1.3.0
v3	14,980,000	v3.0.0	v1.5.0
v3patch1	15,385,000	v3.0.1	v1.5.0
v3patch2	15,684,437	v3.0.3	v1.5.0
v4	25,540,114	v4.0.1	v1.5.0
v4patch1	28,217,000	v4.1.0	v1.5.0
v4patch2	34,074,369	v4.1.2	v1.5.0
v5	43,480,734	v5.0.0	v1.5.0
v6	76,897,000	v6.0.0	v1.5.0
v6.1	TBD	v6.1.0	v1.5.0
Testnet Binary Setup Script
bash
#!/bin/bash
# Setup full history node for Testnet

export TX_HOME="$HOME/.txd/txchain-testnet-1"

# Create directory structure for all upgrades
UPGRADES="v1 v2 v2patch1 v3 v3patch1 v3patch2 v4 v4patch1 v4patch2 v5 v6"

mkdir -p $TX_HOME/cosmovisor/genesis/bin

for upgrade in $UPGRADES; do
    mkdir -p $TX_HOME/cosmovisor/upgrades/$upgrade/bin
done

# Download genesis binary (v0.1.1)
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/v0.1.1/txd-linux-amd64
chmod a+x txd-linux-amd64
mv txd-linux-amd64 $TX_HOME/cosmovisor/genesis/bin/txd

# Download v1 (v1.0.0)
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/v1.0.0/txd-linux-amd64
chmod a+x txd-linux-amd64
mv txd-linux-amd64 $TX_HOME/cosmovisor/upgrades/v1/bin/txd

# Continue for each upgrade...

echo "✅ Testnet full history binaries installed"
Quick Reference: Binary Versions by Height
Mainnet
Height Range	Version	Binary
0 - 6,947,499	v1.0.0	txd-v1.0.0
6,947,500 - 13,479,999	v2.0.2	txd-v2.0.2
13,480,000 - 23,338,749	v3.0.3	txd-v3.0.3
23,338,750 - 25,890,999	v4.0.1	txd-v4.0.1
25,891,000 - 32,311,999	v4.1.0	txd-v4.1.0
32,312,000 - 39,809,999	v4.1.2	txd-v4.1.2
39,810,000 - 66,483,999	v5.0.0	txd-v5.0.0
66,484,000 - 67,169,999	v6.0.1	txd-v6.0.1
67,170,000+	v6.1.0	txd-v6.1.0
Testnet
Height Range	Version	Binary
0 - 3,233,699	v0.1.1	txd-v0.1.1
3,233,700 - 8,728,399	v1.0.0	txd-v1.0.0
8,728,400 - 9,122,199	v2.0.0	txd-v2.0.0
9,122,200 - 14,979,999	v2.0.2	txd-v2.0.2
14,980,000 - 15,384,999	v3.0.0	txd-v3.0.0
15,385,000 - 15,684,436	v3.0.1	txd-v3.0.1
15,684,437 - 25,540,113	v3.0.3	txd-v3.0.3
25,540,114 - 28,216,999	v4.0.1	txd-v4.0.1
28,217,000 - 34,074,368	v4.1.0	txd-v4.1.0
34,074,369 - 43,480,733	v4.1.2	txd-v4.1.2
43,480,734 - 76,896,999	v5.0.0	txd-v5.0.0
76,897,000+	v6.0.0	txd-v6.0.0
Setting Up Full History Node - Step by Step
Step 1: Install Cosmovisor
bash
# Follow the install-txd guide for cosmovisor installation
Step 2: Create Directory Structure
bash
export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"

# Create base structure
mkdir -p $TX_HOME/cosmovisor/genesis/bin
mkdir -p $TX_HOME/cosmovisor/upgrades
Step 3: Install All Historical Binaries
bash
# For each upgrade in the history:
# 1. Download binary
# 2. Place in upgrades/<upgrade-name>/bin/txd
# 3. Make executable (chmod a+x)
Step 4: Initialize and Start
bash
# Initialize node
txd init my-node --chain-id $TX_CHAIN_ID

# Download genesis file
wget -O $TX_HOME/config/genesis.json <genesis-url>

# Start with cosmovisor
cosmovisor run start --chain-id $TX_CHAIN_ID
Important Notes
Storage Requirements: Full history nodes require significantly more storage (2TB+ for mainnet)

Sync Time: Can take days or weeks to sync from genesis

Alternatives: Use state sync for faster sync if full history isn't required

Binary Verification: Always verify binary versions match the upgrade table

Cosmovisor Version: Ensure cosmovisor version matches requirements

Resources
State Sync Guide

Upgrade Guide

Full Node Setup

txd Releases
