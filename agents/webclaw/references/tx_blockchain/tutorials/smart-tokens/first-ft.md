# Create and Manage Fungible Token with CLI

This tutorial will guide you through the process of using the AssetFT module to create and manage Fungible Tokens (FT) on TX Blockchain using the command line.

> **Note**: Each subsequent section depends on the previous one. Follow the steps in order.

## Prerequisites

### Step 1: Set Up Network Variables

```bash
# Chain ID for testnet
export CHAIN_ID="txchain-testnet-1"

# RPC endpoint
export RPC_URL="https://rpc.testnet.tx.dev:443"

# Keyring backend (os for production, test for development)
export KEYRING_BACKEND=test

# Verify settings
echo "Chain ID: $CHAIN_ID"
echo "RPC URL: $RPC_URL"
For other networks (mainnet, devnet), find CHAIN_ID and RPC_URL values on the Network Variables page.

Step 2: Install txd Binary
Make sure txd is installed:

bash
txd version
# Should output: v6.1.0 or higher
If not installed, follow the Install txd guide.

Step 3: Create or Import Accounts
You need two accounts for this tutorial:

FT Admin - Issues and manages the token

Receiver - Receives tokens

Option A: Generate New Accounts via Faucet
Go to TX Testnet Faucet

Click "Generate Funded Wallet" twice to get two accounts

Save both mnemonics

Option B: Import Existing Accounts
bash
# Import admin account
txd keys add ft-admin --recover --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID
# Enter the admin mnemonic when prompted

# Import receiver account
txd keys add ft-receiver-1 --recover --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID
# Enter the receiver mnemonic when prompted
List All Keys
bash
txd keys list --keyring-backend=$KEYRING_BACKEND
Step 4: Export Addresses to Environment Variables
bash
# Export admin address
export FT_ADMIN=$(txd keys show ft-admin --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)

# Export receiver address
export FT_RECEIVER_1=$(txd keys show ft-receiver-1 --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)

# Verify addresses
echo "Admin: $FT_ADMIN"
echo "Receiver: $FT_RECEIVER_1"
Part 1: Issue Your First Fungible Token
Command Structure
bash
txd tx assetft issue [symbol] [subunit] [precision] [initial_amount] [description] \
  --from [admin] \
  --features=burning,freezing,minting,whitelisting \
  --send-commission-rate=0.02 \
  --uri=<uri> \
  --uri-hash=<hash> \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Parameter Explanation
Parameter	Example	Description
symbol	MYFT	Display name for UI (e.g., "BTC")
subunit	cmyft	On-chain denomination (minimum unit). "c" prefix = centi (10^-2)
precision	2	Decimal places (100 subunit = 1 symbol)
initial_amount	100	Initial supply in subunit units
description	"My first FT token"	Human-readable description
Issue Command
bash
txd tx assetft issue MYFT cmyft 2 100 "My first FT token" \
  --from $FT_ADMIN \
  --features=burning,freezing,minting,whitelisting \
  --send-commission-rate=0.02 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Expected Output
json
{
  "code": 0,
  "txhash": "2A4F3E8B9C1D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3E4F5A6B7C8D9E0F",
  "raw_log": "[{\"events\":...}]"
}
💡 Important: Copy the transaction hash and go to the Block Explorer to see the transaction status. Transactions may appear with some delay due to indexing.

⚠️ Note: You can only issue one unique FT per account address. Each token must have a unique subunit.

Get Token Denom
Your new token has a unique denom consisting of the subunit and your account address:

bash
export FT_DENOM=cmyft-$FT_ADMIN
echo "Token Denom: $FT_DENOM"
# Example: cmyft-testcore1z0f5qlw5k90qn0ll5m6d7k8802j3qntylnt6mv
Check Token Balance
bash
txd query bank balances $FT_ADMIN \
  --denom=$FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

text
amount: "100"
denom: cmyft-testcore1z0f5qlw5k90qn0ll5m6d7k8802j3qntylnt6mv
Query Token Details
bash
txd query assetft token $FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

yaml
token:
  burn_rate: "0.000000000000000000"
  denom: cmyft-testcore1m4mm44zh9unlpg74nnqxmvwrkm5a20tmaes2z7
  description: My first FT token
  features:
  - burning
  - freezing
  - minting
  - whitelisting
  globally_frozen: false
  issuer: testcore1m4mm44zh9unlpg74nnqxmvwrkm5a20tmaes2z7
  precision: 2
  send_commission_rate: "0.020000000000000000"
  subunit: cmyft
  symbol: MYFT
Part 2: Minting Additional Tokens
Since we enabled the minting feature, the token admin can mint additional tokens.

Mint Command
bash
# Mint 100 more tokens
txd tx assetft mint 100$FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Verify Minted Balance
bash
txd query bank balances $FT_ADMIN \
  --denom=$FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

text
amount: "200"
denom: cmyft-testcore1m4mm44zh9unlpg74nnqxmvwrkm5a20tmaes2z7
Check Total Supply
bash
txd query bank total \
  --denom=$FT_DENOM \
  --node=$RPC_URL
Expected output:

text
amount: "200"
denom: cmyft-testcore1m4mm44zh9unlpg74nnqxmvwrkm5a20tmaes2z7
💡 Note: Minting is not affected by global freeze.

Part 3: Whitelisting and Bank Send
Since we enabled the whitelisting feature, we must whitelist an account before sending tokens. Otherwise, the transaction will fail with: balance whitelisted error.

Set Whitelisted Limit
bash
# Syntax: txd tx assetft set-whitelisted-limit [account_address] [amount] --from [sender]
txd tx assetft set-whitelisted-limit $FT_RECEIVER_1 1000$FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Check Whitelisted Balance
bash
txd query assetft whitelisted-balance $FT_RECEIVER_1 $FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

yaml
balance:
  amount: "1000"
  denom: cmyft-testcore1m4mm44zh9unlpg74nnqxmvwrkm5a20tmaes2z7
💡 Note: Each set-whitelisted-limit command overrides the existing whitelisting limit. You can whitelist more tokens than issued.

Send Tokens
bash
txd tx bank send $FT_ADMIN $FT_RECEIVER_1 200$FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Verify Received Tokens
bash
txd query bank balances $FT_RECEIVER_1 \
  --denom=$FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

text
amount: "200"
denom: cmyft-testcore1m4mm44zh9unlpg74nnqxmvwrkm5a20tmaes2z7
Part 4: Freezing
Freezing locks up Fungible Tokens on a specific account or globally.

Command	Description
freeze	Freeze specific amount for an account
unfreeze	Unfreeze frozen tokens
globally-freeze	Freeze all tokens (no operations except admin)
globally-unfreeze	Unfreeze all tokens
Freeze Specific Account
bash
# Syntax: txd tx assetft freeze [account_address] [amount] --from [sender]
txd tx assetft freeze $FT_RECEIVER_1 100$FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
💡 Note: You can freeze any amount for an account, even if it exceeds the account's balance.

Try to Send Frozen Tokens (Will Fail)
bash
# Attempt to send 101 tokens (100 frozen, 101 > available)
txd tx bank send $FT_RECEIVER_1 $FT_ADMIN 101$FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Expected error:

text
failed to execute message; message index: 0: 101cmyft-... is not available,
available 100cmyft-...: insufficient funds
Check Frozen Balance
bash
# Syntax: txd query assetft frozen-balance [account] [denom]
txd query assetft frozen-balance $FT_RECEIVER_1 $FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

yaml
balance:
  amount: "100"
  denom: cmyft-testcore1m4mm44zh9unlpg74nnqxmvwrkm5a20tmaes2z7
Unfreeze Tokens
bash
txd tx assetft unfreeze $FT_RECEIVER_1 100$FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Verify Frozen Balance is Zero
bash
txd query assetft frozen-balance $FT_RECEIVER_1 $FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

text
amount: "0"
💡 Note: You cannot unfreeze more tokens than the account has frozen.

Globally Freeze All Tokens
bash
txd tx assetft globally-freeze $FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
After global freeze, all token operations are disabled. Even sending tokens to the admin will fail.

Try to Send During Global Freeze (Will Fail)
bash
txd tx bank send $FT_RECEIVER_1 $FT_ADMIN 100$FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Expected error:

text
coins are not spendable: cmyft-... is globally frozen
Globally Unfreeze
bash
txd tx assetft globally-unfreeze $FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
💡 Note: Even during global freeze, the token admin can still perform operations with their tokens.

Part 5: Send Commission Rate
The send commission rate applies a commission when tokens are transferred between accounts, except when one participant is the token admin.

Create Third Account
bash
# Import third account
txd keys add ft-receiver-2 --recover --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID

# Export address
export FT_RECEIVER_2=$(txd keys show ft-receiver-2 --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)

# Whitelist the third account
txd tx assetft set-whitelisted-limit $FT_RECEIVER_2 200$FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Check Initial Balances
bash
# Receiver 1 balance
txd query bank balances $FT_RECEIVER_1 --denom=$FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID
# amount: "200"

# Admin balance
txd query bank balances $FT_ADMIN --denom=$FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID
# amount: "0"
Send Tokens with Commission
bash
# Send 100 tokens from receiver1 to receiver2
txd tx bank send $FT_RECEIVER_1 $FT_RECEIVER_2 100$FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Check Balances After Commission
bash
# Receiver 1 balance (sent 100, commission 2% = 2 tokens deducted)
txd query bank balances $FT_RECEIVER_1 --denom=$FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID
# amount: "98"

# Receiver 2 balance (received 100)
txd query bank balances $FT_RECEIVER_2 --denom=$FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID
# amount: "100"

# Admin balance (received commission: 2 tokens)
txd query bank balances $FT_ADMIN --denom=$FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID
# amount: "2"
Part 6: Burn Rate
Burn rate works similarly to send commission rate, but instead of sending tokens to the admin, tokens are burned (removed from circulation).

💡 Note: Burn rate was set to 0 in this example. To enable burn rate, use --burn-rate=0.12 during token issuance.

Part 7: Burning Tokens
bash
# Burn 10 tokens from receiver1
txd tx assetft burn 10$FT_DENOM \
  --from $FT_RECEIVER_1 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Verify Burn
bash
# Check balance after burn
txd query bank balances $FT_RECEIVER_1 --denom=$FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID
# amount: "88"

# Check total supply after burn
txd query bank total --denom=$FT_DENOM --node=$RPC_URL
# amount: "190"
Part 8: Transfer Admin
Transfer administrative rights to another account. The new admin can then manage the token.

bash
txd tx assetft transfer-admin $FT_RECEIVER_1 $FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Verify New Admin
bash
txd query assetft token $FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID | grep admin
# admin: testcore1... (receiver address)
Part 9: Clear Admin
Remove administrative rights forever. After this, no one has special privileges.

bash
txd tx assetft clear-admin $FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Verify Admin is Cleared
bash
txd query assetft token $FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID
If admin is cleared, the admin field will be empty or absent.

⚠️ Warning: Clearing admin is irreversible. After this, no one can mint, freeze, or perform other admin actions.

Feature Reference Table
Feature	Command Flag	Description	Admin Only
Minting	--features=minting	Create additional tokens	✅
Burning	--features=burning	Destroy tokens	❌ (anyone with tokens)
Freezing	--features=freezing	Lock account tokens	✅
Whitelisting	--features=whitelisting	Restrict token reception	✅
Complete Script Example
bash
#!/bin/bash
# ft-cli-tutorial.sh - Complete FT CLI tutorial script

set -e

# Configuration
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export KEYRING_BACKEND=test

echo "=== Setting up accounts ==="
export FT_ADMIN=$(txd keys show ft-admin --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)
export FT_RECEIVER_1=$(txd keys show ft-receiver-1 --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)

echo "Admin: $FT_ADMIN"
echo "Receiver: $FT_RECEIVER_1"

echo "=== Issuing Token ==="
txd tx assetft issue MYFT cmyft 2 100 "My first FT token" \
  --from $FT_ADMIN \
  --features=burning,freezing,minting,whitelisting \
  --send-commission-rate=0.02 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

export FT_DENOM=cmyft-$FT_ADMIN
echo "Token Denom: $FT_DENOM"

echo "=== Minting Tokens ==="
txd tx assetft mint 100$FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

echo "=== Whitelisting Receiver ==="
txd tx assetft set-whitelisted-limit $FT_RECEIVER_1 1000$FT_DENOM \
  --from $FT_ADMIN \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

echo "=== Sending Tokens ==="
txd tx bank send $FT_ADMIN $FT_RECEIVER_1 200$FT_DENOM \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

echo "=== Final Balances ==="
echo "Admin balance:"
txd query bank balances $FT_ADMIN --denom=$FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID
echo "Receiver balance:"
txd query bank balances $FT_RECEIVER_1 --denom=$FT_DENOM --node=$RPC_URL --chain-id=$CHAIN_ID

echo "✅ FT CLI tutorial complete!"
FAQ
What if an account with non-zero balance is removed from the whitelist?
If an account's non-zero balance is removed from the whitelist:

The account can still spend any tokens it has received

New tokens cannot be sent to this account (transaction will fail)

Can I issue multiple tokens from the same account?
No. Each account can only issue one unique FT. The subunit must be unique per account.

What happens if I try to mint more than the maximum supply?
There is no hard maximum supply. You can mint unlimited tokens if the minting feature is enabled.

Next Steps
Create and manage NFT with CLI

Smart FT with WASM

Asset FT Extension

Resources
AssetFT Module Documentation

Network Variables

Testnet Faucet

Block Explorer
