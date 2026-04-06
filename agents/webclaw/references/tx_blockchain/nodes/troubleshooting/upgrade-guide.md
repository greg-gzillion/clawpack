k# How to Upgrade Your Node

This guide describes instructions specific to each planned upgrade of the `txd` binary.

## Before the Upgrade

### Prerequisites

> ⚠️ **Critical**: You must run your node with **cosmovisor** (not directly with the `txd` binary). Cosmovisor automatically handles stopping the node and replacing the binary when an upgrade should be applied.

If you're currently running a validator using `txd` directly, you should switch to cosmovisor by following the [Cosmovisor Setup Guide](#).

### Governance Proposal

When a new version of the binary is released, a governance proposal is created.

**Check proposals:**
- [Block Explorer](https://explorer.tx.org/proposals)
- CLI: `txd q gov proposals`

### Voting

All stakeholders and delegators may vote to support or decline the upgrade proposal. If a delegator doesn't vote, their voting power supports the validator's vote.

**Vote command:**
```bash
txd tx gov vote [proposal-id] [option] [flags]

# Options: yes, no, no_with_veto, abstain
Getting Upgrade Plan Info
If more than 50% of voting power votes "yes" (and "no with veto" is less than 30%), a new upgrade plan is created.

Query pending upgrade plan:

bash
txd q upgrade plan
Example output:

json
{
  "height": "30012",
  "info": "binary version",
  "name": "v6.1.0",
  "time": "0001-01-01T00:00:00Z"
}
height: Block height when upgrade will be applied

name: Upgrade name/version

info: Binary version details

⚠️ Warning: Your node must be prepared for the upgrade before the specified height. Otherwise, after reaching that height, your validator will stop and risk being slashed for being offline.

Upgrade Types
Mainnet Upgrade (v6.1.0)
Environment Variables:

bash
export TX_BINARY_NAME=$(arch | sed s/aarch64/txd-linux-arm64/ | sed s/x86_64/txd-linux-amd64/)
export TX_CHAIN_ID="tx-mainnet-1"
export NEW_TXD_VERSION="v6.1.0"
export UPGRADE_NAME="v6.1.0"

# TX home directory
export TX_HOME=$HOME/.txd/"$TX_CHAIN_ID"
Testnet Upgrade (v6.1.0)
Important: For upgrades involving transition from Coreum to TX, there are one-time prerequisites. Follow the migration steps.

Environment Variables:

bash
export TX_BINARY_NAME=$(arch | sed s/aarch64/txd-linux-arm64/ | sed s/x86_64/txd-linux-amd64/)
export TX_CHAIN_ID="txchain-testnet-1"
export NEW_TXD_VERSION="v6.1.0"
export UPGRADE_NAME="v6.1.0"

# TX home directory
export TX_HOME=$HOME/.txd/"$TX_CHAIN_ID"
Step-by-Step Upgrade Process
Step 1: Download New Binary
bash
cd $HOME

# Download the new binary
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/$NEW_TXD_VERSION/$TX_BINARY_NAME
Step 2: Verify Binary
bash
# Make executable
# NOTE: Use a+x (all users), not just u+x. Cosmovisor requires this.
chmod a+x $HOME/$TX_BINARY_NAME

# Verify version
$HOME/$TX_BINARY_NAME version
Expected output: The version should match $NEW_TXD_VERSION. If it doesn't match, STOP immediately! Continuing will cause serious problems.

Step 3: Verify Permissions
Ensure the binary is executable by the user running cosmovisor:

bash
# Check permissions
ls -la $HOME/$TX_BINARY_NAME

# Should show: -rwxr-xr-x (all users can execute)
Step 4: Create Upgrade Directory
Cosmovisor requires the new binary in a specific location:

bash
# Create the upgrade directory
mkdir -p "$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin"

# Verify directory created
ls -la "$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin"
Step 5: Move Binary to Upgrade Location
bash
# Move binary to cosmovisor upgrades directory
mv $HOME/$TX_BINARY_NAME "$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin/txd"

# Verify
ls -la "$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin/txd"
Step 6: Create Current Symlink (If Needed)
For the upgrade to take effect automatically:

bash
# Create symlink to current upgrade
ln -sf "$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME" "$TX_HOME/cosmovisor/current"
Step 7: Monitor Upgrade
Cosmovisor will automatically:

Detect the upgrade height

Stop the node

Switch to the new binary

Restart the node

Monitor logs:

bash
sudo journalctl -u txd -f

# Or if running directly
cosmovisor run start --chain-id $TX_CHAIN_ID
Complete Upgrade Script
bash
#!/bin/bash
# upgrade-node.sh - Automated node upgrade

set -e

# Configuration
export TX_CHAIN_ID="txchain-testnet-1"  # Change for mainnet
export NEW_TXD_VERSION="v6.1.0"
export UPGRADE_NAME="v6.1.0"
export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"

echo "🚀 Starting upgrade to $NEW_TXD_VERSION"

# Download binary
echo "📦 Downloading binary..."
cd $HOME
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/$NEW_TXD_VERSION/txd-linux-amd64
export TX_BINARY_NAME="txd-linux-amd64"

# Verify
echo "🔍 Verifying binary..."
chmod a+x $HOME/$TX_BINARY_NAME
VERSION=$($HOME/$TX_BINARY_NAME version)
if [ "$VERSION" != "$NEW_TXD_VERSION" ]; then
    echo "❌ Version mismatch! Expected $NEW_TXD_VERSION, got $VERSION"
    exit 1
fi
echo "✅ Version verified: $VERSION"

# Create upgrade directory
echo "📁 Creating upgrade directory..."
mkdir -p "$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin"

# Move binary
echo "📦 Installing binary..."
mv $HOME/$TX_BINARY_NAME "$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin/txd"

# Create symlink
ln -sf "$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME" "$TX_HOME/cosmovisor/current"

echo "✅ Upgrade prepared!"
echo "📊 Upgrade will activate at the scheduled height"
echo "📝 Monitor logs: sudo journalctl -u txd -f"
Post-Upgrade Verification
Check Node Version
bash
# After upgrade height is reached
txd version

# Check node status
txd status | jq .NodeInfo.version
Verify Validator is Active
bash
# Check if validator is in active set
txd query staking validators --limit=100 | \
  jq '.validators[] | select(.description.moniker=="your-moniker") | .status'
# Should show: BOND_STATUS_BONDED
Check Missed Blocks
bash
# Verify no excessive missed blocks
txd query slashing signing-info $(txd tendermint show-validator) | \
  jq .missed_blocks_counter
# Should be low (0-10)
Troubleshooting
Node Won't Start After Upgrade
bash
# Check logs
sudo journalctl -u txd -n 100

# Check binary permissions
ls -la $TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin/txd

# Manually test binary
$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin/txd version
Upgrade Height Missed
If your node missed the upgrade height:

bash
# Check current height vs upgrade height
curl -s http://localhost:26657/status | jq .result.sync_info.latest_block_height

# If past upgrade height, you may need to:
# 1. Manually switch binary
# 2. Resync from snapshot
# 3. Use state sync
Version Mismatch
bash
# Check expected version from governance
txd q upgrade plan

# Check current binary version
txd version

# If mismatch, re-download correct version
Upgrade History
Version	Height	Network	Date	Description
v6.1.0	TBD	Mainnet	2026	TX Mainnet Launch
v6.1.0	TBD	Testnet	2026	TX Testnet Migration
v6.0.0	Genesis	Both	2025	Initial Launch
Resources
Cosmovisor Setup

Governance Guide

Troubleshooting

State Sync
