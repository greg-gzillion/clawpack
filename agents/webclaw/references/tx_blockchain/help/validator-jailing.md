# Validator Jailing and Unjailing on TX Blockchain

## Overview

Validators on the TX blockchain can be jailed for misbehavior. There are two types of misbehavior that can result in jailing:

1. **Uptime Misbehavior** (Temporary jailing)
2. **Double Signing Misbehavior** (Permanent removal)

## Types of Misbehavior

### 1. Uptime Misbehavior (Liveness Failure)

A validator gets jailed for uptime issues when:
- Missing more than 50% of blocks in a period of **34,000 blocks** (~47 hours on TX)

**Punishment:**
- Jailed for **60 seconds**
- **0.5%** of the validator's stake is burned
- During jail period, the operator cannot unjail

**Resolution:**
- Wait for the 60-second jail period to expire
- Submit an unjail transaction

### 2. Double Signing Misbehavior (Equivocation)

A validator gets permanently removed (tombstoned) when:
- Signing two different blocks at the same height
- Any form of consensus equivocation

**Punishment:**
- **5%** of total delegations slashed
- **Permanently removed** from validator set ("tombstoned")
- Cannot be unjailed

**Resolution:**
- Must create a **new validator** with a new consensus key
- Delegators need to re-delegate to the new validator

## How to Unjail Your Validator (Uptime Only)

### Prerequisites

- Jail period has expired (60 seconds for uptime misbehavior)
- Your validator is running and synced
- You have access to the validator operator key

### Step 1: Check Validator Status

```bash
# Check if your validator is jailed
txd query staking validator <validator-address>

# Example output showing jailed status
jailed: true
status: BOND_STATUS_UNBONDING
Step 2: Wait for Jail Period to Expire
For uptime misbehavior, the jail period is 60 seconds. Check the jail time:

bash
# Check when validator was jailed
txd query slashing signing-info <consensus-pubkey>
Step 3: Submit Unjail Transaction
Once the jail period has expired, submit the unjail transaction:

bash
txd tx slashing unjail \
  --from <your-validator-operator-key> \
  --chain-id <chain-id> \
  --node <rpc-node-url> \
  --gas auto \
  --gas-prices <gas-price>
Example:

bash
txd tx slashing unjail \
  --from myvalidator \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:26657 \
  --gas auto \
  --gas-prices 10utx
Step 4: Verify Unjail Success
bash
# Check validator status again
txd query staking validator <validator-address>

# Should show:
jailed: false
status: BOND_STATUS_BONDED
Step 5: Monitor Recovery
After unjailing, monitor your validator's performance:

bash
# Check missed blocks counter
txd query slashing signing-info <consensus-pubkey>

# Check validator voting power
txd query staking validator <validator-address> --output json | jq .tokens
Common Unjail Issues and Solutions
Issue 1: "validator not jailed"
Error: validator <address> is not jailed

Solution: The validator is not jailed. Check if it's actually jailed first using txd query staking validator.

Issue 2: "jail period not yet expired"
Error: cannot unjail validator due to jail period not expired

Solution: Wait for the 60-second jail period to complete. Check using:

bash
txd query slashing signing-info <consensus-pubkey>
Issue 3: "insufficient funds for gas"
Error: insufficient funds for gas

Solution: Ensure your validator operator account has enough TX tokens for gas:

bash
txd query bank balances <operator-address>
Issue 4: "validator is tombstoned"
Error: validator is tombstoned; cannot be unjailed

Solution: The validator committed double-signing and is permanently removed. You must:

Create a new validator with a new consensus key

Inform your delegators to redelegate

Automated Monitoring and Auto-Unjailing
Setting up Auto-Unjail Script
Create a script to automatically unjail when possible:

bash
#!/bin/bash

# auto-unjail.sh
VALIDATOR_ADDR="txvaloper1..."
CHAIN_ID="tx-mainnet-1"
RPC_NODE="https://rpc.tx.org:26657"

# Check if validator is jailed
JAILED=$(txd query staking validator $VALIDATOR_ADDR \
  --node $RPC_NODE \
  --chain-id $CHAIN_ID \
  --output json | jq -r '.jailed')

if [ "$JAILED" == "true" ]; then
  echo "Validator is jailed, attempting unjail..."
  
  txd tx slashing unjail \
    --from validator-key \
    --chain-id $CHAIN_ID \
    --node $RPC_NODE \
    --gas auto \
    --gas-prices 10utx \
    --yes
    
  echo "Unjail transaction submitted"
else
  echo "Validator is not jailed"
fi
Setting up Cron Job
bash
# Run every 5 minutes
*/5 * * * * /usr/local/bin/auto-unjail.sh >> /var/log/validator-unjail.log 2>&1
Using Systemd for Validator Monitoring
Create a systemd service to monitor and auto-unjail:

bash
# /etc/systemd/system/validator-monitor.service
[Unit]
Description=TX Validator Monitor
After=network.target

[Service]
Type=simple
User=tx
ExecStart=/usr/local/bin/validator-monitor.sh
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
Prevention Best Practices
To avoid being jailed in the first place:

1. High Availability Setup
Run multiple sentry nodes

Use a reliable VPS provider

Implement failover mechanisms

2. Monitoring and Alerts
bash
# Set up alerting for missed blocks
txd query slashing signing-info <consensus-pubkey> \
  --output json | jq '.missed_blocks_counter'
3. Regular Maintenance
Keep validator software updated

Monitor disk space and CPU usage

Set up backup consensus keys

4. Resource Requirements
Minimum: 4 CPU cores, 16GB RAM, 500GB SSD

Recommended: 8 CPU cores, 32GB RAM, 1TB NVMe SSD

Validator Recovery Checklist
Immediate Actions (First 5 minutes)
Check if jail is from uptime or double-signing

Verify validator is running and syncing

Check network connectivity to peers

Review logs for errors

Short-term Recovery (First hour)
Wait for jail period if uptime misbehavior

Submit unjail transaction

Monitor validator performance

Announce incident to delegators

Long-term Actions
Investigate root cause

Implement monitoring improvements

Update documentation

Consider HA setup if not already

Network-Specific Information
Mainnet
Parameter	Value
Chain ID	tx-mainnet-1
Jail Period	60 seconds
Slashing for Downtime	0.5%
Slashing for Double-Sign	5%
Blocks for Downtime	34,000 blocks
Testnet
Parameter	Value
Chain ID	tx-testnet-1
Jail Period	60 seconds
Slashing for Downtime	0.5%
Slashing for Double-Sign	5%
Blocks for Downtime	34,000 blocks
Devnet
Parameter	Value
Chain ID	tx-devnet-1
Jail Period	10 seconds (reduced)
Slashing	May be disabled
Useful Commands Reference
bash
# Query validator info
txd query staking validator <valoper-address>

# Query validator delegations
txd query staking delegations-to <valoper-address>

# Query slashing parameters
txd query slashing params

# Query signing info
txd query slashing signing-info <consensus-pubkey>

# Unjail validator
txd tx slashing unjail --from <key-name>

# Get validator address from operator address
txd keys show <key-name> --bech=val

# Check validator commission
txd query staking validator <valoper-address> | grep commission

# Monitor validator uptime
watch -n 10 'txd query slashing signing-info <consensus-pubkey>'
Emergency Contacts
If you need additional support:

Discord: Join the TX Foundation Discord for community support

GitHub: Report issues at github.com/tx-foundation

Bug Bounty: Report security issues through the bug bounty program

Related Documentation
Validator Setup Guide

Monitoring Best Practices

Slashing Conditions

Network Variables
