# TX Blockchain - Comprehensive FAQ

## Getting Started

### How to point `txd` to a specific network?

By default, `txd` binary points to the local node (localhost:26657). To point it to a specific node, use two flags: `--node` and `--chain-id`.

**Example:**
```bash
txd status --node=https://rpc.tx.org:26657 --chain-id=tx-mainnet-1
Network variables can be found at the network variables page.

How to fix account not found error?
This error typically appears as:

text
Error: rpc error: code = NotFound desc = rpc error: code = NotFound desc = account testcore1q07ldrjnr8xtsy3rz82yxqcdrffu3uw3daslrw not found: key not found
Two possible causes:

Zero balance account - Your account has zero balance and is not visible on the network. Fund it before using it.

Unsynced RPC node - The RPC node you used is not fully synced. Use another RPC node or wait for sync completion.

Solution:

bash
# Check if account exists
txd query account <address> --node=<synced-node>

# Fund the account first if zero balance
How to fix key not found error?
This error appears as:

text
Error: testcore1f2dyj8dhdv62ytrkuvn832ezzjdcpg2jhrtzvy.info: key not found
Possible causes:

RPC_URL and/or chain-id belong to different networks

Wrong keyring backend specified

Solution:

bash
# Specify the correct keyring backend
txd tx bank send ... --keyring-backend=test

# Or check your keys in the correct keyring
txd keys list --keyring-backend=test
Integration
How can I integrate tx into my real estate brokerage?
TX is designed specifically to tokenize real-world assets like real estate. Integration details vary depending on whether your property is rental, commercial, or residential.

Steps to integrate:

Contact the TX team for a tailored implementation

Define token economics for your property

Set up compliance rules using TX's compliance modules

Launch your real estate token on TX blockchain

Contact the team through the official website for guidance.

Technology
What makes the tx blockchain unique?
TX blockchain offers several unique features:

Cross-Chain Routing - Native IBC and XRPL integration

Native Asset Programmability - Smart Tokens with WASM support

Compliance-First Design - Built-in KYC/AML capabilities

Proven Stability - 1-second finality

Organic Orderbook DEX - With AMM liquidity routing

Staking
How can I delegate my tokens to a validator?
You can delegate your $TX tokens through any supported wallet:

Supported wallets:

Leap Wallet

Cosmostation

Fox Wallet

Keplr

And more...

Methods:

Direct wallet delegation - Most wallets offer delegation as a built-in feature

Third-party dashboard - Use Restake.app or similar platforms

Steps:

Connect your wallet to a supported interface

Navigate to the "Staking" section

Choose a validator from the list

Enter the amount to delegate

Confirm the transaction

Token Creation
What is the process for creating a new token on TX?
Method 1: TokenHub (Recommended)

Access the TokenHub interface

Click "Create New Token"

Fill in token parameters (name, symbol, supply, etc.)

Submit and pay the creation fee

Your token is deployed automatically

Method 2: CLI (Advanced users)

bash
txd tx tokenhub create-token \
  --name="My Token" \
  --symbol="MYT" \
  --supply="1000000" \
  --from=<your-account>
Important: Test on testnet first before mainnet deployment.

Bug Reporting
How can I report bugs or issues in TX?
Reporting channels:

GitHub Issues - Report bugs at github.com/tx-foundation

Discord Server - Join the TX Foundation Discord for community support

Bug Bounty Program - Report security issues for rewards

What to include:

Clear description of the issue

Steps to reproduce

Expected vs actual behavior

Screenshots or logs

Environment details

Validator Management
How does tx handle misbehaving validators?
TX uses a slashing mechanism for two types of misbehavior:

1. Uptime Misbehavior (Liveness)
Trigger: Missing >50% of blocks in 34,000 blocks (~47 hours)

Punishment: Jailed for 60 seconds, 0.5% stake burned

Recovery: Auto-unjail after 60 seconds, then submit unjail tx

2. Double Signing Misbehavior (Equivocation)
Trigger: Signing two blocks at the same height

Punishment: 5% slashing, permanent removal (tombstoned)

Recovery: Must create new validator with new consensus key

How to unjail a validator?
For uptime misbehavior:

bash
# Wait 60 seconds, then submit:
txd tx slashing unjail --from <validator-key>
For double-signing:

Cannot unjail - validator is permanently tombstoned

Must create a new validator with a new consensus key

Network Information
Network Endpoints
Network	RPC	Chain ID
Mainnet	https://rpc.tx.org:26657	tx-mainnet-1
Testnet	https://rpc.testnet.tx.org:26657	tx-testnet-1
Devnet	https://rpc.devnet.tx.org:26657	tx-devnet-1
Block Parameters
Parameter	Value
Block Time	~1 second
Blocks per Year	~31,536,000
Voting Period	~10 seconds
Troubleshooting
Common Error Codes
Error	Meaning	Solution
account not found	Zero balance or unsynced node	Fund account or change node
key not found	Wrong keyring or network	Check keyring-backend and chain-id
insufficient fees	Gas too low	Increase gas or gas-prices
out of gas	Transaction too complex	Estimate gas with --gas auto
unauthorized	Insufficient permissions	Check account privileges
Support Resources
Documentation: docs.tx.org

Discord: Join the TX Foundation Discord

GitHub: github.com/tx-foundation

Bug Bounty: tx.org/bug-bounty

Additional Help
If you can't find what you're looking for:

Search the docs - Use the search bar at the top

Ask the community - Join Discord for real-time help

Contact support - Reach out through the official website

File an issue - Create a GitHub issue for documentation improvements

text

**Save the file:**
- `Ctrl+O`, `Enter`, `Ctrl+X`

Now let's create a validator recovery guide:

```bash
nano ~/dev/TXdocumentation/help/validator-recovery.md
markdown
# Validator Recovery Guide

## Quick Reference: How to Unjail Your Validator

### Step-by-Step Unjail Process

1. **Check if validator is jailed:**
```bash
txd query staking validator <validator-address> | grep jailed
Wait for jail period (60 seconds for uptime issues)

Submit unjail transaction:

bash
txd tx slashing unjail --from <validator-key-name> --chain-id <chain-id> --node <rpc-url>
Verify unjail success:

bash
txd query staking validator <validator-address> | grep jailed
# Should show: jailed: false
Detailed Recovery Procedures
Scenario 1: Uptime Jailing (Recoverable)
Symptoms:

Validator missed >50% of recent blocks

Status shows jailed: true

Can still recover

Recovery steps:

Identify why validator went down (network, hardware, software)

Fix the underlying issue

Ensure validator is running and synced

Wait 60 seconds for jail period

Submit unjail transaction

Monitor for 30 minutes to ensure stability

Scenario 2: Double-Signing (Tombstoned)
Symptoms:

Status shows jailed: true and tombstoned: true

Cannot unjail

Recovery steps:

Accept that this validator is permanently removed

Create a new validator with a new consensus key

Announce to delegators to redelegate

Set up new validator infrastructure

Register new validator on-chain

Build new delegator base

Scenario 3: Network Issues
Symptoms:

Validator is running but missing blocks

Not jailed yet but high miss rate

Recovery steps:

Check network connectivity

Verify peer connections

Ensure firewall allows required ports

Check for DDoS attacks

Implement sentry node architecture

Automated Recovery Script
Create this script to auto-handle unjailing:

bash
#!/bin/bash
# /usr/local/bin/auto-unjail.sh

VALIDATOR_ADDR="txvaloper1..."  # Replace with your validator address
CHAIN_ID="tx-mainnet-1"          # Replace with your chain ID
RPC_NODE="https://rpc.tx.org:26657"
KEY_NAME="validator"              # Replace with your key name

# Log file
LOG_FILE="/var/log/validator-unjail.log"

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> $LOG_FILE
}

# Check validator status
check_validator() {
    txd query staking validator $VALIDATOR_ADDR \
        --node $RPC_NODE \
        --chain-id $CHAIN_ID \
        --output json 2>/dev/null
}

# Attempt unjail
attempt_unjail() {
    log_message "Attempting to unjail validator"
    
    txd tx slashing unjail \
        --from $KEY_NAME \
        --chain-id $CHAIN_ID \
        --node $RPC_NODE \
        --gas auto \
        --gas-prices 10utx \
        --yes \
        --output json 2>&1 | tee -a $LOG_FILE
    
    sleep 10
    
    # Verify unjail
    JAILED=$(check_validator | jq -r '.jailed')
    if [ "$JAILED" == "false" ]; then
        log_message "Successfully unjailed validator"
        return 0
    else
        log_message "Failed to unjail validator"
        return 1
    fi
}

# Main loop
main() {
    JAILED=$(check_validator | jq -r '.jailed')
    TOMBSTONED=$(check_validator | jq -r '.tombstoned')
    
    if [ "$TOMBSTONED" == "true" ]; then
        log_message "ERROR: Validator is tombstoned! Cannot recover. Create new validator."
        exit 1
    fi
    
    if [ "$JAILED" == "true" ]; then
        log_message "Validator is jailed, attempting recovery..."
        attempt_unjail
    else
        log_message "Validator is not jailed"
    fi
}

main
Monitoring Setup
Prometheus Alert for Jailing
yaml
# prometheus-alert.yml
groups:
- name: validator
  rules:
  - alert: ValidatorJailed
    expr: validator_jailed == 1
    for: 0m
    labels:
      severity: critical
    annotations:
      summary: "Validator {{ $labels.validator }} is jailed"
      description: "Validator has been jailed. Check logs and unjail if possible."
Grafana Dashboard Query
sql
-- Check missed blocks over time
SELECT 
    timestamp,
    missed_blocks_counter
FROM validator_metrics
WHERE validator_address = 'txvaloper1...'
ORDER BY timestamp DESC
LIMIT 100;
Prevention Checklist
Infrastructure
Run multiple sentry nodes

Use different cloud providers

Implement DDoS protection

Set up monitoring and alerting

Regular backup of consensus key

Software
Keep txd updated to latest version

Use stable, tested releases

Monitor disk space

Set up log rotation

Configure proper time synchronization (NTP)

Operations
Document recovery procedures

Practice recovery drills

Have emergency contact list

Set up redundant signing infrastructure

Monitor validator performance daily

Emergency Contacts
Resource	Contact
Technical Support	Discord #validator-support
Security Issues	security@tx.org
Bug Bounty	bugbounty@tx.org
Emergency Hotline	Contact through Discord
Related Documentation
Validator Setup Guide

Sentry Node Configuration

Monitoring Best Practices

Slashing Conditions
