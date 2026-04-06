# How to Unjail a Validator on TX Blockchain

This guide provides step-by-step instructions for checking validator jailing status and unjailing a validator when possible.

## Prerequisites

Before starting, ensure you have:
- Access to the validator node
- The validator owner account (key) available
- `txd` CLI installed and configured
- Network connectivity to the TX blockchain

---

## Step 1: Check the Reason for Jailing

First, examine the signing info to determine why your validator was jailed.

### Check All Validators Signing Info

```bash
txd query slashing signing-infos --node=<RPC_URL> --chain-id=<CHAIN_ID>
Example:

bash
txd query slashing signing-infos --node=https://rpc.tx.org:26657 --chain-id=tx-mainnet-1
Check Specific Validator
bash
txd query slashing signing-info <validator-consensus-pubkey> --node=<RPC_URL>
Get validator consensus pubkey:

bash
txd tendermint show-validator
Understanding the Output
The command shows us the status of all validators, where you can see the jailed one and check the reason.

Example Output:

yaml
signing_infos:
- address: txvalcons1abc123...
  jailed_until: "2024-01-15T10:30:00Z"
  tombstoned: false
  missed_blocks_counter: 17500
- address: txvalcons1def456...
  jailed_until: "9999-12-31T23:59:59Z"
  tombstoned: true
  missed_blocks_counter: 0
Step 2: Determine Jailing Type
Case A: Jailed for Being Offline (Recoverable)
Characteristics:

tombstoned: false

jailed_until is a reasonable time (e.g., 60 seconds from now)

Reason: Validator missed >50% of blocks in the last 34,000 blocks

Example:

yaml
jailed_until: "2024-01-15T10:30:00Z"  # Reasonable future time
tombstoned: false                       # Can be unjailed
Action: ✅ You can unjail this validator (see Step 3)

Case B: Jailed for Double Signing (Tombstoned)
Characteristics:

tombstoned: true

jailed_until: "9999-12-31T23:59:59Z" (essentially forever)

Reason: Two replicas with the same priv_validator_key.json file

Example:

yaml
jailed_until: "9999-12-31T23:59:59Z"  # Effectively permanent
tombstoned: true                        # Cannot be unjailed
Action: ❌ This validator is permanently tombstoned. No way to unjail.

Double Signing Scenario Details
When double signing occurs:

One validator will be tombstoned with jailed_until: "9999-12-31T23:59:59Z" and tombstoned: true

Another replica may be jailed with reasonable jailed_until time and tombstoned: false

Important: You can unjail the non-tombstoned replica after fixing the duplicate key issue.

Step 3: Fix the Reason for Jailing
For Offline Jailing
Before unjailing, fix the underlying issue:

Check validator status:

bash
systemctl status txd
Check logs for errors:

bash
journalctl -u txd -f --lines=100
Ensure validator is synced:

bash
txd status | jq .sync_info
Common fixes:

Restart the validator: systemctl restart txd

Check network connectivity

Verify peers are connected

Ensure sufficient resources (CPU, RAM, disk)

For Double Signing
If you have duplicate priv_validator_key.json files:

Identify all locations where the key exists

Keep only one copy on the primary validator

Remove or backup the duplicate key files

Restart validators with unique keys

Unjail the non-tombstoned replica

Warning: The tombstoned validator cannot be recovered. Create a new validator with a new consensus key.

Step 4: Send Unjail Transaction
If the validator is jailed but not tombstoned, send the unjail transaction.

Basic Unjail Command
bash
txd tx slashing unjail --from {VALIDATOR_OWNER_ACCOUNT}
Where:

{VALIDATOR_OWNER_ACCOUNT} - Name or address of the account that owns the validator (the staker account)

Complete Unjail Command with Parameters
bash
txd tx slashing unjail \
  --from <validator-owner-account> \
  --chain-id <CHAIN_ID> \
  --node <RPC_URL> \
  --gas auto \
  --gas-prices <GAS_PRICE> \
  --gas-adjustment 1.5 \
  --yes
Examples
Example 1: Using account name

bash
txd tx slashing unjail \
  --from myvalidator \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:26657 \
  --gas auto \
  --gas-prices 10utx \
  --yes
Example 2: Using account address

bash
txd tx slashing unjail \
  --from tx1abc123def456... \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:26657 \
  --gas 200000 \
  --gas-prices 10utx \
  --yes
Example 3: Testnet unjail

bash
txd tx slashing unjail \
  --from myvalidator \
  --chain-id tx-testnet-1 \
  --node https://rpc.testnet.tx.org:26657 \
  --gas auto \
  --gas-prices 10utx \
  --yes
Understanding the Parameters
Parameter	Description
--from	Name or address of the validator owner account
--chain-id	Network identifier (tx-mainnet-1, tx-testnet-1, etc.)
--node	RPC endpoint URL
--gas	Gas limit (auto recommended)
--gas-prices	Price per unit of gas (e.g., 10utx)
--gas-adjustment	Multiplier for auto gas estimation
--yes	Skip confirmation prompt
Step 5: Verify Unjail Success
Check Validator Status
bash
txd query staking validator <validator-operator-address> --node=<RPC_URL>
Expected output after successful unjail:

yaml
jailed: false
status: BOND_STATUS_BONDED
tombstoned: false
Check Signing Info
bash
txd query slashing signing-info <consensus-pubkey> --node=<RPC_URL>
Expected output:

yaml
jailed_until: "1970-01-01T00:00:00Z"  # Zero time (not jailed)
tombstoned: false
Monitor Validator Performance
bash
# Check if validator is signing blocks
txd query tendermint-validator-set --node=<RPC_URL> | grep <your-validator>

# Check missed blocks counter (should reset)
txd query slashing signing-info <consensus-pubkey> | grep missed_blocks_counter

# Check validator voting power
txd query staking validator <validator-operator-address> | grep tokens
Optional: Check Validator's State via Status Command
If your validator is up and running, you can check its state by sending the next command:

bash
txd status --node={YOUR_RPC_ADDRESS}
Where: {YOUR_RPC_ADDRESS} is your validator's public HTTP address (e.g., http://localhost:26657 or https://validator.yourdomain.com:26657)

Example:

bash
txd status --node=http://localhost:26657
Expected output:

json
{
  "node_info": {
    "id": "a1b2c3d4...",
    "listen_addr": "tcp://0.0.0.0:26656",
    "network": "tx-mainnet-1",
    "version": "v1.2.3"
  },
  "sync_info": {
    "latest_block_height": "12345678",
    "latest_block_time": "2024-01-15T10:35:00Z",
    "catching_up": false
  },
  "validator_info": {
    "address": "txvalcons1abc...",
    "voting_power": "1000000"
  }
}
Complete Unjail Script
Here's a complete script to automate the unjailing process:

bash
#!/bin/bash
# /usr/local/bin/tx-unjail.sh

set -e

# Configuration
VALIDATOR_OWNER="myvalidator"           # Your validator owner account name
CHAIN_ID="tx-mainnet-1"                 # Network chain ID
RPC_NODE="https://rpc.tx.org:26657"     # RPC endpoint
GAS_PRICES="10utx"                      # Gas price

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Checking validator jailing status...${NC}"

# Get validator operator address
VALIDATOR_OP_ADDR=$(txd keys show $VALIDATOR_OWNER --bech=val --address 2>/dev/null)
if [ -z "$VALIDATOR_OP_ADDR" ]; then
    echo -e "${RED}Error: Could not find validator owner account${NC}"
    exit 1
fi

# Check if validator is jailed
JAILED=$(txd query staking validator $VALIDATOR_OP_ADDR \
    --node $RPC_NODE \
    --chain-id $CHAIN_ID \
    --output json 2>/dev/null | jq -r '.jailed')

if [ "$JAILED" != "true" ]; then
    echo -e "${GREEN}Validator is not jailed. No action needed.${NC}"
    exit 0
fi

# Check if tombstoned
TOMBSTONED=$(txd query staking validator $VALIDATOR_OP_ADDR \
    --node $RPC_NODE \
    --chain-id $CHAIN_ID \
    --output json 2>/dev/null | jq -r '.tombstoned')

if [ "$TOMBSTONED" == "true" ]; then
    echo -e "${RED}Validator is tombstoned! Cannot unjail. Create a new validator.${NC}"
    exit 1
fi

# Get consensus pubkey
CONSENSUS_PUBKEY=$(txd tendermint show-validator)

# Check jailed until time
JAILED_UNTIL=$(txd query slashing signing-info $CONSENSUS_PUBKEY \
    --node $RPC_NODE \
    --chain-id $CHAIN_ID \
    --output json 2>/dev/null | jq -r '.jailed_until')

echo -e "${YELLOW}Validator is jailed until: $JAILED_UNTIL${NC}"

# Check if jail period has expired
CURRENT_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)
if [[ "$JAILED_UNTIL" > "$CURRENT_TIME" ]]; then
    echo -e "${YELLOW}Jail period not yet expired. Waiting...${NC}"
    sleep 60
fi

# Attempt unjail
echo -e "${YELLOW}Attempting to unjail validator...${NC}"

txd tx slashing unjail \
    --from $VALIDATOR_OWNER \
    --chain-id $CHAIN_ID \
    --node $RPC_NODE \
    --gas auto \
    --gas-prices $GAS_PRICES \
    --gas-adjustment 1.5 \
    --yes \
    --output json

# Wait for transaction to process
sleep 10

# Verify unjail success
JAILED=$(txd query staking validator $VALIDATOR_OP_ADDR \
    --node $RPC_NODE \
    --chain-id $CHAIN_ID \
    --output json 2>/dev/null | jq -r '.jailed')

if [ "$JAILED" == "false" ]; then
    echo -e "${GREEN}Successfully unjailed validator!${NC}"
    
    # Check validator status
    STATUS=$(txd status --node $RPC_NODE 2>/dev/null | jq -r '.validator_info.voting_power')
    echo -e "${GREEN}Validator voting power: $STATUS${NC}"
else
    echo -e "${RED}Failed to unjail validator. Check logs.${NC}"
    exit 1
fi
Make Script Executable
bash
chmod +x /usr/local/bin/tx-unjail.sh
Set Up Cron Job for Automatic Unjailing
bash
# Run every 5 minutes
*/5 * * * * /usr/local/bin/tx-unjail.sh >> /var/log/tx-unjail.log 2>&1
Troubleshooting Common Issues
Issue 1: "account not found"
Error:

text
Error: account tx1abc123... not found
Solution:

Ensure the account has been funded

Wait for node to sync

Check you're using the correct keyring backend

Issue 2: "insufficient fees"
Error:

text
Error: insufficient fees
Solution:

bash
# Increase gas prices
txd tx slashing unjail --from myvalidator --gas-prices 20utx

# Or use more gas
txd tx slashing unjail --from myvalidator --gas 300000
Issue 3: "validator not jailed"
Error:

text
Error: validator is not jailed
Solution:

Check the validator status again

Wait for the jail period to start

Verify you're checking the correct validator

Issue 4: "jail period not yet expired"
Error:

text
Error: cannot unjail validator due to jail period not expired
Solution:

Wait for the jail period to complete (typically 60 seconds)

Check jailed_until time in signing info

Issue 5: "validator is tombstoned"
Error:

text
Error: validator is tombstoned; cannot be unjailed
Solution:

This validator cannot be recovered

Create a new validator with a new consensus key

Inform delegators to redelegate

Prevention Best Practices
To avoid being jailed in the future:

1. High Availability Setup
Run multiple sentry nodes

Use different cloud providers

Implement failover mechanisms

2. Monitoring
bash
# Monitor missed blocks
watch -n 10 'txd query slashing signing-info $(txd tendermint show-validator)'

# Monitor validator status
watch -n 10 'txd query staking validator $(txd keys show myvalidator --bech=val --address)'
3. Alerting
Set up alerts for:

Missed block rate > 10%

Validator status changes

High memory/CPU usage

4. Regular Maintenance
Keep software updated

Monitor disk space

Regular backups of consensus key

Network-Specific Information
Mainnet
Parameter	Value
Chain ID	tx-mainnet-1
Jail Period	60 seconds
Slashing	0.5% for downtime
RPC Endpoint	https://rpc.tx.org:26657
Testnet
Parameter	Value
Chain ID	tx-testnet-1
Jail Period	60 seconds
Slashing	0.5% for downtime
RPC Endpoint	https://rpc.testnet.tx.org:26657
Devnet
Parameter	Value
Chain ID	tx-devnet-1
Jail Period	10 seconds
Slashing	Disabled or reduced
RPC Endpoint	https://rpc.devnet.tx.org:26657
Quick Reference Commands
bash
# Check all signing infos
txd query slashing signing-infos --node=<RPC> --chain-id=<CHAIN_ID>

# Check specific validator signing info
txd query slashing signing-info $(txd tendermint show-validator)

# Check validator staking info
txd query staking validator $(txd keys show <owner> --bech=val --address)

# Unjail validator
txd tx slashing unjail --from <owner>

# Check validator status
txd status --node=<YOUR_RPC_ADDRESS>

# Check validator missed blocks
txd query slashing signing-info $(txd tendermint show-validator) | grep missed_blocks_counter
Support
If you continue to experience issues:

Check Discord: Join #validator-chat on Discord

Review Logs: journalctl -u txd -f --lines=100

Community Help: GitHub Discussions

Emergency Contact: validators@tx.org

Remember: Always fix the underlying issue before unjailing, or the validator will be jailed again!

text

**Save the file:**
- `Ctrl+O`, `Enter`, `Ctrl+X`

Now let's create a visual flowchart for the unjail process:

```bash
nano ~/dev/TXdocumentation/help/unjail-flowchart.md
markdown
# Validator Unjail Process Flowchart

## Decision Tree for Unjailing
┌─────────────────────────┐
│ Validator is Jailed? │
└────────────┬────────────┘
│
┌────────────┴────────────┐
│ │
Yes No
│ │
▼ ▼
┌──────────────────┐ ┌──────────────────┐
│ Check Signing │ │ No Action Needed │
│ Info with: │ └──────────────────┘
│ txd q slashing │
│ signing-infos │
└────────┬─────────┘
│
▼
┌──────────────────┐
│ Examine Output: │
│ - jailed_until │
│ - tombstoned │
└────────┬─────────┘
│
┌────────┴────────┐
│ │
tombstoned tombstoned
= false = true
│ │
▼ ▼
┌─────────────────┐ ┌─────────────────────────┐
│ Reasonable │ │ jailed_until = │
│ jailed_until │ │ 9999-12-31T23:59:59Z │
│ (e.g., 60 sec) │ │ │
└────────┬────────┘ └──────────┬──────────────┘
│ │
▼ ▼
┌─────────────────┐ ┌─────────────────────────┐
│ OFFLINE │ │ DOUBLE SIGNING │
│ JAILING │ │ JAILING │
└────────┬────────┘ └──────────┬──────────────┘
│ │
▼ ▼
┌─────────────────┐ ┌─────────────────────────┐
│ ✅ Can Unjail │ │ ❌ Cannot Unjail │
│ │ │ (Permanently Tombstoned)│
└────────┬────────┘ └──────────┬──────────────┘
│ │
▼ ▼
┌─────────────────┐ ┌─────────────────────────┐
│ 1. Fix Issue │ │ Create New Validator │
│ 2. Wait for │ │ with New Consensus Key │
│ jail period │ │ │
│ 3. Send unjail │ └─────────────────────────┘
│ transaction │
└────────┬────────┘
│
▼
┌─────────────────┐
│ Verify with: │
│ txd status │
│ --node={RPC} │
└─────────────────┘

text

## Detailed Unjail Process Flow
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: DETECT JAILING │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ txd query slashing signing-infos │
│ │ │
│ ▼ │
│ ┌────────────────────────────────────┐ │
│ │ Is validator in the signing_infos? │ │
│ └────────────┬───────────────────────┘ │
│ │ │
│ ┌───────┴───────┐ │
│ │ │ │
│ Yes No │
│ │ │ │
│ ▼ ▼ │
│ [Continue] [Validator OK] │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: CHECK JAILING TYPE │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ Examine: tombstoned field │
│ │ │
│ ┌─────────┴─────────┐ │
│ │ │ │
│ tombstoned tombstoned │
│ = false = true │
│ │ │ │
│ ▼ ▼ │
│ ┌─────────────┐ ┌─────────────────────────────────┐ │
│ │ OFFLINE │ │ DOUBLE SIGNING │ │
│ │ Jailing │ │ Jailing │ │
│ └──────┬──────┘ └───────────────┬─────────────────┘ │
│ │ │ │
│ ▼ ▼ │
│ [Recoverable] [Permanent Loss] │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: FIX THE ISSUE │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ OFFLINE JAILING: DOUBLE SIGNING: │
│ ┌─────────────────────────┐ ┌─────────────────────────┐ │
│ │ • Check validator sync │ │ • Identify duplicate │ │
│ │ • Restart if needed │ │ priv_validator_key │ │
│ │ • Verify network peers │ │ • Remove/backup dups │ │
│ │ • Check resource usage │ │ • Keep only one copy │ │
│ │ • Review logs for errors│ │ • Restart validators │ │
│ └───────────┬─────────────┘ └───────────┬─────────────┘ │
│ │ │ │
│ ▼ ▼ │
│ [Continue] [New validator required] │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: WAIT FOR JAIL PERIOD │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ Check jailed_until field │
│ │ │
│ ▼ │
│ ┌────────────────────────────────────────┐ │
│ │ Current time >= jailed_until? │ │
│ └────────────┬───────────────────────────┘ │
│ │ │
│ ┌───────┴───────┐ │
│ │ │ │
│ Yes No │
│ │ │ │
│ ▼ ▼ │
│ [Continue] [Wait] → [Sleep 10s] → [Check again] │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 5: SEND UNJAIL TRANSACTION │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ txd tx slashing unjail --from {VALIDATOR_OWNER_ACCOUNT} │
│ │ │
│ ▼ │
│ ┌────────────────────────────────────────┐ │
│ │ Transaction successful? │ │
│ └────────────┬───────────────────────────┘ │
│ │ │
│ ┌───────┴───────┐ │
│ │ │ │
│ Yes No │
│ │ │ │
│ ▼ ▼ │
│ [Continue] [Troubleshoot] → [Check: │
│ - Account balance │
│ - Gas settings │
│ - Network connectivity] │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: VERIFY UNJAIL │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ Method 1: Check staking info │
│ txd query staking validator <valoper> │
│ │ │
│ ▼ │
│ Expected: jailed: false, status: BOND_STATUS_BONDED │
│ │
│ Method 2: Check signing info │
│ txd query slashing signing-info <consensus-pubkey> │
│ │ │
│ ▼ │
│ Expected: jailed_until: "1970-01-01T00:00:00Z" │
│ │
│ Method 3: Check validator status │
│ txd status --node={YOUR_RPC_ADDRESS} │
│ │ │
│ ▼ │
│ Expected: catching_up: false, voting_power > 0 │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 7: MONITOR │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ • Watch missed blocks counter │ │
│ │ • Monitor validator signing activity │ │
│ │ • Set up alerts for future jailing │ │
│ │ • Review why jailing occurred │ │
│ │ • Implement preventive measures │ │
│ └─────────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Quick Command Reference by Scenario

### Scenario 1: Offline Jailing (Recoverable)

```bash
# 1. Check status
txd query slashing signing-infos --node=<RPC>

# 2. Fix issue (restart validator)
systemctl restart txd

# 3. Wait for jail period (60 seconds)
sleep 60

# 4. Unjail
txd tx slashing unjail --from <owner> --chain-id <CHAIN_ID> --node=<RPC>

# 5. Verify
txd query staking validator <valoper> --node=<RPC>
Scenario 2: Double Signing (Tombstoned)
bash
# 1. Identify tombstoned validator
txd query slashing signing-infos --node=<RPC>

# 2. Remove duplicate priv_validator_key.json
rm /path/to/duplicate/priv_validator_key.json

# 3. Keep only one copy on primary validator

# 4. Create new validator (tombstoned one is lost)
txd tx staking create-validator --from <new-owner> ...

# 5. Inform delegators to redelegate
Scenario 3: Unknown Jailing
bash
# 1. Get full details
VALIDATOR=$(txd keys show <owner> --bech=val --address)
CONS_PUBKEY=$(txd tendermint show-validator)

# 2. Check both staking and slashing info
txd query staking validator $VALIDATOR --node=<RPC>
txd query slashing signing-info $CONS_PUBKEY --node=<RPC>

# 3. Based on output, follow appropriate scenario
Monitoring Dashboard
bash
# Create a monitoring script
cat > /usr/local/bin/validator-monitor.sh << 'EOF'
#!/bin/bash

VALIDATOR_OWNER="myvalidator"
RPC_NODE="https://rpc.tx.org:26657"
CHAIN_ID="tx-mainnet-1"

while true; do
    clear
    echo "=== TX Validator Monitor ==="
    echo "Time: $(date)"
    echo ""
    
    # Get validator info
    VALOPER=$(txd keys show $VALIDATOR_OWNER --bech=val --address 2>/dev/null)
    if [ -n "$VALOPER" ]; then
        echo "Validator Operator: $VALOPER"
        
        JAILED=$(txd query staking validator $VALOPER --node=$RPC_NODE --chain-id=$CHAIN_ID -o json 2>/dev/null | jq -r '.jailed')
        echo "Jailed: $JAILED"
        
        STATUS=$(txd query staking validator $VALOPER --node=$RPC_NODE --chain-id=$CHAIN_ID -o json 2>/dev/null | jq -r '.status')
        echo "Status: $STATUS"
        
        VOTING_POWER=$(txd query staking validator $VALOPER --node=$RPC_NODE --chain-id=$CHAIN_ID -o json 2>/dev/null | jq -r '.tokens')
        echo "Voting Power: $VOTING_POWER"
    fi
    
    # Get signing info
    CONS_PUBKEY=$(txd tendermint show-validator 2>/dev/null)
    if [ -n "$CONS_PUBKEY" ]; then
        echo ""
        echo "Signing Info:"
        txd query slashing signing-info $CONS_PUBKEY --node=$RPC_NODE --chain-id=$CHAIN_ID 2>/dev/null
    fi
    
    sleep 10
done
EOF

chmod +x /usr/local/bin/validator-monitor.sh
Summary Decision Matrix
Condition	tombstoned	jailed_until	Can Unjail?	Action
Offline jailing	false	Reasonable time	✅ Yes	Fix issue → Wait → Unjail
Double signing (primary)	false	Reasonable time	✅ Yes	Fix duplicate key → Unjail
Double signing (secondary)	true	9999-12-31	❌ No	Create new validator
Unknown	false	Current/past	✅ Yes	Attempt unjail
Unknown	true	Any	❌ No	Create new validator
Remember: Always check tombstoned status first. If true, the validator cannot be recovered!

text

**Save the file:**
- `Ctrl+O`, `Enter`, `Ctrl+X`

Now let's verify all the validator unjail documentation:

```bash
ls -la ~/dev/TXdocumentation/help/ | grep -E "unjail|validator"
