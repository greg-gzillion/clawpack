# Transfer Funds with CLI

This tutorial provides step-by-step instructions on how to use the `txd` CLI to transfer funds and stake tokens on TX Blockchain.

> **Note**: We are using testnet for this example. For mainnet, replace the network variables accordingly.

---

## Prerequisites

- [ ] `txd` installed ([Installation Guide](../getting-started/install-txd.md))
- [ ] Network variables configured ([Network Variables](../getting-started/network-variables.md))

---

## Step 1: Configure Testnet Environment

Set up your CLI to point to the testnet:

```bash
# Set testnet endpoints
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_CHAIN_ID="txchain-testnet-1"

# Create convenience arguments
export TX_NODE_ARGS="--node=$TX_NODE"
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"

# Verify configuration
echo "Node: $TX_NODE"
echo "Chain ID: $TX_CHAIN_ID"
Verify Connection
bash
# Check node status
txd status $TX_NODE_ARGS

# Check network name (should match $TX_CHAIN_ID)
txd status $TX_NODE_ARGS | jq .NodeInfo.network

# If you don't have jq installed:
# sudo apt install jq -y  # Ubuntu/Debian
# brew install jq          # macOS
Step 2: Get a Funded Account
Option A: Generate Funded Wallet via Faucet
Go to the TX Testnet Faucet

Click "Generate Funded Wallet"

Copy the wallet mnemonic (12 or 24 words)

Store it in a safe place - this is the only way to recover your account!

Option B: Create New Wallet and Request Funds
bash
# Create a new wallet
txd keys add my-sender-wallet --keyring-backend test

# Get the address
MY_ADDRESS=$(txd keys show my-sender-wallet -a --keyring-backend test)
echo "My address: $MY_ADDRESS"

# Request funds from faucet (using web browser)
# Visit: https://faucet.testnet.tx.dev
# Enter your address starting with "testcore..."
Import Wallet from Mnemonic
bash
# Import using mnemonic
txd keys add my-sender-wallet --recover --keyring-backend test

# Enter your mnemonic when prompted
# You will be asked to enter your bip39 mnemonic
List All Wallets
bash
txd keys list --keyring-backend test
Step 3: Check Account Balance
bash
# Get your address
MY_ADDRESS=$(txd keys show my-sender-wallet -a --keyring-backend test)

# Check balance
txd query bank balances $MY_ADDRESS $TX_NODE_ARGS

# Expected output:
# balances:
# - amount: "1000000000"
#   denom: utestcore
Step 4: Transfer Funds
Understanding the Command Structure
bash
txd tx bank send [from_key_or_address] [to_address] [amount] [flags]
Parameter	Description	Example
from_key_or_address	Your wallet name or address	my-sender-wallet
to_address	Recipient's address	testcore1...
amount	Amount with denom	1000000utestcore
Send Tokens
bash
# Replace with actual recipient address
RECIPIENT_ADDRESS="testcore1snn05vrzvnwy7t0g00rr7hva63hmwxuuv7nrj0"

# Send 1 testcore (1,000,000 utestcore)
txd tx bank send my-sender-wallet $RECIPIENT_ADDRESS 1000000utestcore \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  --gas auto --gas-adjustment 1.3 \
  -y
Understanding the Output
json
{
  "code": 0,
  "txhash": "2A4F3E8B9C1D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3E4F5A6B7C8D9E0F",
  "raw_log": "[{\"events\":...}]"
}
code: 0 - Success! Transaction was broadcasted

code: not 0 - Failed local validation, fix the issue and retry

Verify the Transaction
Copy the txhash from the output

Go to TX Testnet Explorer

Paste the transaction hash in the search bar

View transaction details

Step 5: Send Staking Transaction
View Staking Commands
bash
txd tx staking --help

# Available commands:
#   create-validator  Create new validator with self-delegation
#   delegate          Delegate liquid tokens to a validator
#   edit-validator    Edit an existing validator account
#   redelegate        Redelegate from one validator to another
#   unbond            Unbond shares from a validator
Delegate Tokens to a Validator
bash
# Command structure
# txd tx staking delegate [validator-addr] [amount] --from [delegator-addr] [flags]

# Example: Delegate 1 testcore to a validator
txd tx staking delegate testcorevaloper14x4ux30sadvg90k2xd8fte5vnhhh0uvkxf4rgm \
  1000000utestcore \
  --from my-sender-wallet \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  --gas auto --gas-adjustment 1.3 \
  -y
Find Validators to Delegate To
bash
# List all validators
txd query staking validators $TX_NODE_ARGS

# Get validator addresses
txd query staking validators $TX_NODE_ARGS \
  --output json | jq '.validators[] | .operator_address'

# Get validator details
txd query staking validator testcorevaloper14x4ux30sadvg90k2xd8fte5vnhhh0uvkxf4rgm $TX_NODE_ARGS
Check Your Delegations
bash
# Check delegations from your address
MY_ADDRESS=$(txd keys show my-sender-wallet -a --keyring-backend test)

txd query staking delegations $MY_ADDRESS $TX_NODE_ARGS
Step 6: Claim Staking Rewards
bash
# Claim rewards from a specific validator
txd tx distribution withdraw-rewards testcorevaloper14x4ux30sadvg90k2xd8fte5vnhhh0uvkxf4rgm \
  --from my-sender-wallet \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  --gas auto --gas-adjustment 1.3 \
  -y

# Claim all rewards from all validators
txd tx distribution withdraw-all-rewards \
  --from my-sender-wallet \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  --gas auto --gas-adjustment 1.3 \
  -y
Common CLI Commands Reference
Query Commands
bash
# Get node status
txd status $TX_NODE_ARGS

# Get account balance
txd query bank balances $MY_ADDRESS $TX_NODE_ARGS

# Get transaction details
txd query tx <TX_HASH> $TX_NODE_ARGS

# Get block details
txd query block --height <BLOCK_HEIGHT> $TX_NODE_ARGS

# Get validator info
txd query staking validator <VALIDATOR_ADDR> $TX_NODE_ARGS
Transaction Commands
bash
# Send tokens
txd tx bank send <from> <to> <amount> $TX_CHAIN_ID_ARGS $TX_NODE_ARGS -y

# Delegate to validator
txd tx staking delegate <validator> <amount> --from <wallet> $TX_CHAIN_ID_ARGS $TX_NODE_ARGS -y

# Unbond from validator
txd tx staking unbond <validator> <amount> --from <wallet> $TX_CHAIN_ID_ARGS $TX_NODE_ARGS -y

# Redelegate to another validator
txd tx staking redelegate <src_validator> <dst_validator> <amount> --from <wallet> $TX_CHAIN_ID_ARGS $TX_NODE_ARGS -y
Using --help Flag
Always use --help to discover available commands:

bash
# Main help
txd --help

# Transaction help
txd tx --help

# Bank module help
txd tx bank --help

# Specific command help
txd tx bank send --help
Troubleshooting
Transaction Failed (code != 0)
Common issues:

Error	Solution
Insufficient funds	Check balance with txd query bank balances
Invalid address	Verify address starts with testcore (testnet)
Gas estimation failed	Increase --gas-adjustment to 1.5
Chain ID mismatch	Verify $TX_CHAIN_ID is correct
Node connection	Check $TX_NODE is accessible
Low Gas Price
bash
# Use higher gas price
txd tx bank send ... \
  --gas-prices 0.075utestcore \
  --gas auto --gas-adjustment 1.3
Transaction Not Found
bash
# Wait a few seconds for propagation
sleep 6

# Query again
txd query tx <TX_HASH> $TX_NODE_ARGS
Best Practices
Always test on testnet first

Use --gas auto --gas-adjustment 1.3 for automatic gas calculation

Store mnemonics offline in a secure location

Verify transaction hash on explorer after broadcast

Use --keyring-backend test for development, os for production

Next Steps
Send multisig Transaction

Smart FT with ACL

Ledger Nano with CLI

Gas Price Guide

Resources
Special Addresses

Network Variables

Testnet Faucet

Block Explorer

