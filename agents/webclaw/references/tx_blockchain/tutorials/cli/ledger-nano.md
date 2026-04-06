# Ledger Nano with CLI: Support and Usage

This tutorial shows you how to utilize a Ledger device with the Cosmos Ledger app and `txd` CLI on TX Blockchain.

## Overview

Using a hardware wallet for storing crypto keys significantly enhances the security of your digital assets. The Ledger device functions as a secure enclave that contains the seed and private keys, and the signing process for transactions occurs entirely within the device—ensuring that no private data is ever transmitted externally.

| Feature | Benefit |
|---------|---------|
| **Private keys never leave device** | Immune to software-based attacks |
| **Physical confirmation required** | Prevents unauthorized transactions |
| **Seed phrase offline storage** | Protection from online threats |
| **Transaction review on device** | Verify details before signing |

> ⚠️ **DISCLAIMER**: Since Ledger limits HD paths, CORE `--coin-type=990` is currently not supported. We will use ATOM `--coin-type=118` (path `m/44/118`), which works perfectly for TX Blockchain.

---

## Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| **Ledger Live** | Latest | Installed on your machine |
| **Cosmos (ATOM) App** | v2.34.12+ | On Ledger device |
| **txd CLI** | v1.0.0+ | `txd version` |
| **Network Variables** | Configured | See [Network Variables](../getting-started/network-variables.md) |

### Install Cosmos App on Ledger

1. Open **Ledger Live** on your computer
2. Go to **Manager** tab
3. Search for **"Cosmos"**
4. Click **Install** on the Cosmos (ATOM) application
5. Verify app version is **v2.34.12 or above**

> 📌 **Note**: The Cosmos app works with TX Blockchain because TX is built on Cosmos SDK.

---

## Instructions

### Step 1: Prepare Your Ledger Device

```bash
# 1. Connect Ledger device via USB
# 2. Enter your PIN to unlock
# 3. Open Cosmos (ATOM) app on the device
# 4. Wait for "Cosmos Ready" or "Application is ready"
Step 2: Set Up Ledger Account in txd
Add a key referencing your Ledger device:

bash
# Basic syntax
txd keys add [name] --chain-id=[chain-id] --ledger --coin-type=118

# Example for testnet
txd keys add ledger-1 \
  --chain-id=txchain-testnet-1 \
  --ledger \
  --coin-type=118
With Keyring Backend (More Secure)
bash
# Using keyring-backend=test (development)
txd keys add ledger-2 \
  --chain-id=txchain-testnet-1 \
  --keyring-backend=test \
  --ledger \
  --coin-type=118

# Using keyring-backend=os (production - OS credential store)
txd keys add ledger-prod \
  --chain-id=tx-mainnet-1 \
  --keyring-backend=os \
  --ledger \
  --coin-type=118
Keyring Backend Options
Backend	Security	Use Case
test	Low	Development only
os	High	Production (macOS Keychain, Windows Credential Manager)
file	Medium	Encrypted file on disk
kwallet	High	KDE Wallet
pass	High	Linux pass utility
Step 3: Verify Your Address
Display your address on the Ledger device:

bash
# Show address (will display on Ledger screen)
txd keys show ledger-1 -d \
  --chain-id=txchain-testnet-1
⚠️ Important: Before executing this command, make sure to:

Unlock your device using the PIN

Open the Cosmos app

Confirm the address shown on your device matches the CLI output

Expected output:

text
- name: ledger-1
  type: ledger
  address: testcore1x8k5y8v5f8zq7p3x2w4l8k9j3h5g2f1d8s7a6d
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A8kOpeBMbmri5rvLjlqN6kOuNzRVUnr2vtinCkKMmwKU"}'
Step 4: Fund Your Ledger Account
Get your address:

bash
LEDGER_ADDR=$(txd keys show ledger-1 -a --chain-id=txchain-testnet-1)
echo $LEDGER_ADDR
Fund via Faucet:

Navigate to TX Testnet Faucet

Enter your Ledger address (starts with testcore...)

Click Request Funds

Wait for confirmation

Verify balance:

bash
txd query bank balances $LEDGER_ADDR \
  --node=https://rpc.testnet.tx.dev:443
Step 5: Sign and Send a Transaction
Check Available Commands
bash
txd tx bank send --help
Send Transaction
bash
# Syntax
# txd tx bank send <keyName> <destinationAddress> <amount><denom> [flags]

# Example: Send 1 testcore
txd tx bank send ledger-1 \
  testcore1snn05vrzvnwy7t0g00rr7hva63hmwxuuv7nrj0 \
  1000000utestcore \
  --chain-id=txchain-testnet-1 \
  --node=https://rpc.testnet.tx.dev:443 \
  --keyring-backend=test \
  --ledger \
  --gas auto --gas-adjustment=1.3 \
  -y
Transaction Flow
Step	Action
1	CLI prepares transaction
2	You respond Y to confirm
3	Ledger prompts to review transaction
4	Scroll through JSON on Ledger screen
5	Press both buttons to sign
6	Transaction broadcasts to network
⚠️ Security Tip: Always carefully examine the transaction JSON displayed on your Ledger screen. Verify:

Recipient address

Amount being sent

Fee amount

Chain ID

Step 6: Advanced Transaction Types
Delegate to Validator
bash
txd tx staking delegate \
  testcorevaloper14x4ux30sadvg90k2xd8fte5vnhhh0uvkxf4rgm \
  1000000utestcore \
  --from ledger-1 \
  --chain-id=txchain-testnet-1 \
  --node=https://rpc.testnet.tx.dev:443 \
  --keyring-backend=test \
  --ledger \
  --gas auto --gas-adjustment=1.3 \
  -y
Claim Staking Rewards
bash
txd tx distribution withdraw-all-rewards \
  --from ledger-1 \
  --chain-id=txchain-testnet-1 \
  --node=https://rpc.testnet.tx.dev:443 \
  --keyring-backend=test \
  --ledger \
  --gas auto --gas-adjustment=1.3 \
  -y
Vote on Governance Proposal
bash
txd tx gov vote 1 yes \
  --from ledger-1 \
  --chain-id=txchain-testnet-1 \
  --node=https://rpc.testnet.tx.dev:443 \
  --keyring-backend=test \
  --ledger \
  --gas auto --gas-adjustment=1.3 \
  -y
Ledger Nano + Keplr Wallet
This section shows how to use your Ledger device with the Keplr browser extension.

Prerequisites
Cosmos app installed on Ledger

Ledger connected and unlocked

Keplr extension installed

Step 1: Connect Ledger to Keplr
Click the Keplr extension icon in your browser

Select Connect Hardware Wallet from the menu

Ensure your Ledger is unlocked and Cosmos app is open

Follow the Keplr pop-up instructions

Select the address you want to use

Step 2: Add TX Blockchain to Keplr
Method A: Via TX Docs (Recommended)
Navigate to TX Docs Network Page

Click the Add to Keplr button for your desired network:

Mainnet

Testnet

Devnet

Approve the request in Keplr

Method B: Manual Addition
Open Keplr extension

Click burger menu (☰) → Manage Chain Visibility

Search for "TX"

Select TX Testnet 1 (or Mainnet)

Click Save

Step 3: Fund Your Ledger Account via Keplr
In Keplr, ensure TX Testnet 1 is selected

Click Deposit button

Click Copy next to your address

Go to Faucet

Paste address and click Request Funds

Step 4: Send Funds Using Keplr + Ledger
In Keplr, click on TESTCORE asset

Click Send

Enter destination address and amount

Click Next → Approve

Confirm on Ledger device:

Review transaction details

Press both buttons to sign

Wait for confirmation

📌 Note: Every transaction requires confirmation on your Ledger device. Keplr will prompt you when ready.

Step 5: Verify Transaction
bash
# Check balance after transfer
txd query bank balances $LEDGER_ADDR \
  --node=https://rpc.testnet.tx.dev:443
Complete Script Example
bash
#!/bin/bash
# ledger-setup.sh - Complete Ledger setup and test

set -e

# Configuration
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"

echo "=== 1. Adding Ledger Key ==="
txd keys add ledger-main \
  --chain-id=$TX_CHAIN_ID \
  --keyring-backend=test \
  --ledger \
  --coin-type=118

LEDGER_ADDR=$(txd keys show ledger-main -a --chain-id=$TX_CHAIN_ID)
echo "Ledger Address: $LEDGER_ADDR"

echo "=== 2. Please fund the address from faucet ==="
echo "Faucet URL: https://faucet.testnet.tx.dev"
read -p "Press Enter after funding..."

echo "=== 3. Checking Balance ==="
txd query bank balances $LEDGER_ADDR --node=$TX_NODE

echo "=== 4. Sending Test Transaction ==="
RECIPIENT="testcore1snn05vrzvnwy7t0g00rr7hva63hmwxuuv7nrj0"

txd tx bank send ledger-main $RECIPIENT 10000$TX_DENOM \
  --chain-id=$TX_CHAIN_ID \
  --node=$TX_NODE \
  --keyring-backend=test \
  --ledger \
  --gas auto --gas-adjustment=1.3 \
  -y

echo "=== 5. Updated Balance ==="
txd query bank balances $LEDGER_ADDR --node=$TX_NODE

echo "✅ Ledger setup complete!"
Troubleshooting
"No Ledger device found"
Error:

text
failed to initialize ledger device: ledger not available
Solutions:

bash
# 1. Check USB connection
lsusb | grep -i ledger

# 2. Restart Ledger device
# Unplug, wait 5 seconds, reconnect

# 3. Check if Cosmos app is open
# Ledger screen should show "Cosmos Ready"

# 4. On Linux, add udev rules
sudo wget -O /etc/udev/rules.d/20-ledger.rules https://raw.githubusercontent.com/LedgerHQ/udev-rules/master/20-ledger.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
"Cosmos app not open"
Error:

text
Please open Cosmos app on Ledger
Solution:

On Ledger, press both buttons to navigate

Find and open Cosmos app

Wait for "Application is ready"

Retry the command

"Invalid coin type"
Error:

text
coin type 990 not supported
Solution:
Use coin type 118 instead:

bash
txd keys add ledger-1 --ledger --coin-type=118
"Signature verification failed"
Error:

text
signature verification failed
Solutions:

bash
# 1. Verify chain ID
echo $TX_CHAIN_ID

# 2. Check account sequence
txd query account $LEDGER_ADDR --node=$TX_NODE

# 3. Reset Ledger and retry
# Close Cosmos app, reopen, retry command
Keplr: "Chain not visible"
Solution:

Open Keplr → ☰ → Manage Chain Visibility

Search "TX"

Enable TX Testnet 1

Save

Keplr: "Transaction rejected on device"
Solution:

On Ledger, scroll through all transaction fields

Ensure you reach the end

Press both buttons to sign

If still failing, close and reopen Cosmos app

Security Best Practices
Practice	Why
Never share seed phrase	Seed phrase controls all funds
Verify addresses on device	Prevents address replacement attacks
Review transaction JSON	Ensures correct recipient and amount
Use keyring-backend=os	OS-level encryption for stored references
Keep Ledger firmware updated	Latest security patches
Use testnet first	Validate workflow before mainnet
Store seed phrase offline	Paper or metal backup, never digital
Supported Networks
Network	Chain ID	Coin Type	Works
Mainnet	tx-mainnet-1	118	✅
Testnet	txchain-testnet-1	118	✅
Devnet	txchain-devnet-1	118	✅
Local	txchain-local	118	✅
Quick Reference Commands
bash
# Add Ledger key
txd keys add my-ledger --ledger --coin-type=118

# Show address (display on device)
txd keys show my-ledger -d

# Get address (CLI only)
txd keys show my-ledger -a

# List all keys
txd keys list

# Delete key (doesn't affect Ledger)
txd keys delete my-ledger

# Send transaction
txd tx bank send my-ledger <to> <amount> --ledger

# Delegate
txd tx staking delegate <validator> <amount> --from my-ledger --ledger

# Vote
txd tx gov vote <proposal-id> <option> --from my-ledger --ledger
Next Steps
Transfer funds with CLI

Send multisig Transaction

Smart FT with ACL

Resources
Ledger Support Page

Cosmos App on Ledger

Keplr Extension

TX Testnet Faucet

Network Variables
