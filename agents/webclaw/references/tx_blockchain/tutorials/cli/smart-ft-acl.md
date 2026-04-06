# Smart FT with Access Control List (ACL)

This tutorial explains how to create a Multisig account and grant different permissions to individual addresses using the Authz Module, enabling each address to have different permissions for the management of TX Blockchain assets.

## Overview

| Component | Purpose |
|-----------|---------|
| **Multisig Account** | Shared control requiring multiple signatures |
| **Authz Module** | Grants/revokes permissions to execute messages |
| **AssetFT Module** | Fungible token issuance and management |
| **ACL Pattern** | Granular permission separation (mint, burn, freeze, etc.) |

## Prerequisites

- [ ] `txd` installed ([Installation Guide](../getting-started/install-txd.md))
- [ ] Network variables configured ([Network Variables](../getting-started/network-variables.md))
- [ ] Multisig account created ([Multisig Tutorial](./multisig-transaction.md))
- [ ] Funded multisig account

---

## Step 1: Set Up Environment

```bash
# Set testnet endpoints
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"

# Create convenience arguments
export TX_NODE_ARGS="--node=$TX_NODE"
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"

# Get multisig address
export MULTISIG_ADDR=$(txd keys show --address k1k2k3 --keyring-backend test)
echo "Multisig Address: $MULTISIG_ADDR"
Step 2: Issue an FT from Multisig
Generate Unsigned Issuance Transaction
bash
txd tx assetft issue MYFT umyft 6 1000000 "Multisig token" \
  --from $MULTISIG_ADDR \
  --features=burning,freezing,minting,whitelisting \
  --send-commission-rate=0.02 \
  --generate-only \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  > asset-issuance.json
Parameter Explanation
Parameter	Value	Description
MYFT	Symbol	Display name for UI (e.g., "BTC")
umyft	Subunit	On-chain denomination, minimum tradable unit
6	Precision	Decimal places (1,000,000 umyft = 1 MYFT)
1000000	Initial amount	1 MYFT (1,000,000 umyft)
burning	Feature	Allow token burning
freezing	Feature	Allow account freezing
minting	Feature	Allow additional minting
whitelisting	Feature	Allow whitelist management
0.02	Send commission	2% commission on transfers
Verify Transaction Content
bash
cat asset-issuance.json | jq .
Expected output:

json
{
  "body": {
    "messages": [
      {
        "@type": "/coreum.asset.ft.v1.MsgIssue",
        "issuer": "testcore1ywrydndyqmpx88ch7n3pcsq7g4p7rwrj46rs4c",
        "symbol": "MYFT",
        "subunit": "umyft",
        "precision": 6,
        "initial_amount": "1000000",
        "description": "Multisig token",
        "features": ["burning", "freezing", "minting", "whitelisting"],
        "burn_rate": "0.000000000000000000",
        "send_commission_rate": "0.020000000000000000"
      }
    ]
  }
}
Step 3: Sign and Broadcast with Multisig
First Signature (k1)
bash
txd tx sign asset-issuance.json \
  --multisig $MULTISIG_ADDR \
  --from k1 \
  --output-document signerkey1sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test
Note: In a real scenario, the unsigned transaction would be sent to each multisig member to sign individually.

Combine First Signature
bash
txd tx multisign asset-issuance.json k1k2k3 signerkey1sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  > asset-issuance-signed.json
Test Broadcast (Should Fail)
bash
txd tx broadcast asset-issuance-signed.json -y -b block \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS
Expected error:

text
signature verification failed; please verify account number and sequence
Second Signature (k2)
bash
txd tx sign asset-issuance.json \
  --multisig $MULTISIG_ADDR \
  --from k2 \
  --output-document signerkey2sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test
Combine Both Signatures
bash
txd tx multisign asset-issuance.json k1k2k3 \
  signerkey1sign.json signerkey2sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  > asset-issuance-signed.json
Broadcast Final Transaction
bash
txd tx broadcast asset-issuance-signed.json -y -b block \
  $TX_NODE_ARGS \
  $TX_CHAIN_ID_ARGS
Step 4: Grant Minting Permissions via Authz
Create a Minter Account
bash
# Create dedicated minter account
txd keys add minter --keyring-backend test $TX_CHAIN_ID_ARGS

# Get minter address
MINTER_ADDR=$(txd keys show --address minter --keyring-backend test)
echo "Minter Address: $MINTER_ADDR"

# Fund minter account (for gas fees)
# Use faucet or send from funded account
Generate Authz Grant Transaction
bash
txd tx authz grant $MINTER_ADDR generic \
  --msg-type=/coreum.asset.ft.v1.MsgMint \
  --from $MULTISIG_ADDR \
  --generate-only \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  > authz-mint-unsigned.json
Understanding Authz Grant
Field	Value	Description
granter	Multisig address	Account giving permission
grantee	Minter address	Account receiving permission
msg-type	/coreum.asset.ft.v1.MsgMint	Allowed message type
expiration	1 year	Grant validity period
Verify Authz Transaction
bash
cat authz-mint-unsigned.json | jq .
Expected output includes:

json
{
  "body": {
    "messages": [
      {
        "@type": "/cosmos.authz.v1beta1.MsgGrant",
        "granter": "testcore1ywrydndyqmpx88ch7n3pcsq7g4p7rwrj46rs4c",
        "grantee": "testcore17dj6sxlcugcs5zugx294dvnsudxvxuykn3s2qg",
        "grant": {
          "authorization": {
            "@type": "/cosmos.authz.v1beta1.GenericAuthorization",
            "msg": "/coreum.asset.ft.v1.MsgMint"
          },
          "expiration": "2024-07-06T15:23:16Z"
        }
      }
    ]
  }
}
Sign with Multisig Members
bash
# Sign with k1
txd tx sign authz-mint-unsigned.json \
  --multisig $MULTISIG_ADDR \
  --from k1 \
  --output-document signerkey1sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test

# Sign with k2
txd tx sign authz-mint-unsigned.json \
  --multisig $MULTISIG_ADDR \
  --from k2 \
  --output-document signerkey2sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test
Combine and Broadcast Authz Grant
bash
# Combine signatures
txd tx multisign authz-mint-unsigned.json k1k2k3 \
  signerkey1sign.json signerkey2sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  > authz-mint-signed.json

# Broadcast
txd tx broadcast authz-mint-signed.json -y -b block \
  $TX_NODE_ARGS \
  $TX_CHAIN_ID_ARGS
Step 5: Mint Tokens Using Authz
Set Token Denom
bash
# The FT denom is constructed as: subunit-issuer_address
export FT_DENOM="umyft-$MULTISIG_ADDR"
echo "Token Denom: $FT_DENOM"

# Check initial balance
txd query bank balances $MULTISIG_ADDR $TX_NODE_ARGS
Create and Execute Mint Transaction
bash
# Create mint transaction from multisig
txd tx assetft mint 200$FT_DENOM \
  --from $MULTISIG_ADDR \
  $TX_NODE_ARGS \
  $TX_CHAIN_ID_ARGS \
  --generate-only \
  > mint-tx.json

# Execute via authz (minter executes on behalf of multisig)
txd tx authz exec mint-tx.json \
  --from $MINTER_ADDR \
  -b block \
  $TX_NODE_ARGS \
  $TX_CHAIN_ID_ARGS \
  --keyring-backend test
Verify Minting Success
bash
txd query bank balances $MULTISIG_ADDR \
  --denom=$FT_DENOM \
  $TX_NODE_ARGS \
  $TX_CHAIN_ID_ARGS
Expected output:

text
amount: "1000200"
denom: umyft-testcore1tm5fzez64negxc0jl0hg869g35w4c5f9e9qm5c
The original 1,000,000 + 200 minted = 1,000,200 umyft

Step 6: Additional Authz Permissions
Grant Burn Permission
bash
# Create burner account
txd keys add burner --keyring-backend test $TX_CHAIN_ID_ARGS
BURNER_ADDR=$(txd keys show --address burner --keyring-backend test)

# Grant burn permission
txd tx authz grant $BURNER_ADDR generic \
  --msg-type=/coreum.asset.ft.v1.MsgBurn \
  --from $MULTISIG_ADDR \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  -y
Grant Freeze Permission
bash
# Create freezer account
txd keys add freezer --keyring-backend test $TX_CHAIN_ID_ARGS
FREEZER_ADDR=$(txd keys show --address freezer --keyring-backend test)

# Grant freeze permission
txd tx authz grant $FREEZER_ADDR generic \
  --msg-type=/coreum.asset.ft.v1.MsgFreeze \
  --from $MULTISIG_ADDR \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  -y
Grant Whitelist Permission
bash
# Create whitelist manager account
txd keys add whitelister --keyring-backend test $TX_CHAIN_ID_ARGS
WHITELISTER_ADDR=$(txd keys show --address whitelister --keyring-backend test)

# Grant whitelist permission
txd tx authz grant $WHITELISTER_ADDR generic \
  --msg-type=/coreum.asset.ft.v1.MsgSetWhitelistedLimit \
  --from $MULTISIG_ADDR \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  -y
Complete AssetFT Message Types for Authz
Message Type	Permission	Use Case
/coreum.asset.ft.v1.MsgIssue	Issue new token	Initial creation
/coreum.asset.ft.v1.MsgMint	Mint additional tokens	Increase supply
/coreum.asset.ft.v1.MsgBurn	Burn tokens	Decrease supply
/coreum.asset.ft.v1.MsgFreeze	Freeze account	Security hold
/coreum.asset.ft.v1.MsgUnfreeze	Unfreeze account	Release hold
/coreum.asset.ft.v1.MsgSetWhitelistedLimit	Manage whitelist	Compliance
/coreum.asset.ft.v1.MsgGloballyFreeze	Global freeze	Emergency
/coreum.asset.ft.v1.MsgGloballyUnfreeze	Global unfreeze	Emergency end
Complete AssetNFT Message Types for Authz
Message Type	Permission	Use Case
/coreum.asset.nft.v1.MsgIssueClass	Issue NFT class	Create collection
/coreum.asset.nft.v1.MsgMint	Mint NFT	Create NFT
/coreum.asset.nft.v1.MsgBurn	Burn NFT	Destroy NFT
/coreum.asset.nft.v1.MsgFreeze	Freeze NFT	Lock NFT
/coreum.asset.nft.v1.MsgUnfreeze	Unfreeze NFT	Unlock NFT
/coreum.asset.nft.v1.MsgAddToWhitelist	Add to whitelist	Allow access
/coreum.asset.nft.v1.MsgRemoveFromWhitelist	Remove from whitelist	Revoke access
Step 7: Query and Manage Authz Grants
List All Grants
bash
# List grants given by multisig
txd query authz grants-by-granter $MULTISIG_ADDR $TX_NODE_ARGS

# List grants received by minter
txd query authz grants-by-grantee $MINTER_ADDR $TX_NODE_ARGS
Check Specific Grant
bash
txd query authz grant $MULTISIG_ADDR $MINTER_ADDR \
  --msg-type=/coreum.asset.ft.v1.MsgMint \
  $TX_NODE_ARGS
Revoke a Grant
bash
txd tx authz revoke $MINTER_ADDR \
  --msg-type=/coreum.asset.ft.v1.MsgMint \
  --from $MULTISIG_ADDR \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  -y
Complete ACL Script Example
bash
#!/bin/bash
# acl-setup.sh - Complete ACL setup with multisig

set -e

# Configuration
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_NODE_ARGS="--node=$TX_NODE"
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"

echo "=== 1. Creating Multisig ==="
txd keys add acl-k1 --keyring-backend test $TX_CHAIN_ID_ARGS
txd keys add acl-k2 --keyring-backend test $TX_CHAIN_ID_ARGS
txd keys add acl-k3 --keyring-backend test $TX_CHAIN_ID_ARGS

txd keys add acl-multisig \
  --multisig "acl-k1,acl-k2,acl-k3" \
  --multisig-threshold 2 \
  --keyring-backend test \
  $TX_CHAIN_ID_ARGS

MULTISIG_ADDR=$(txd keys show --address acl-multisig --keyring-backend test)
echo "Multisig Address: $MULTISIG_ADDR"

echo "=== 2. Create Role Accounts ==="
txd keys add acl-minter --keyring-backend test $TX_CHAIN_ID_ARGS
txd keys add acl-burner --keyring-backend test $TX_CHAIN_ID_ARGS
txd keys add acl-freezer --keyring-backend test $TX_CHAIN_ID_ARGS

echo "=== 3. Fund Multisig (Manual) ==="
echo "Please fund $MULTISIG_ADDR from faucet"
read -p "Press Enter after funding..."

echo "=== 4. Issue Token from Multisig ==="
txd tx assetft issue ACLTOKEN uacltoken 6 1000000 "ACL Token" \
  --from $MULTISIG_ADDR \
  --features=burning,freezing,minting \
  --generate-only \
  $TX_CHAIN_ID_ARGS $TX_NODE_ARGS > acl-issue.json

# Sign with k1 and k2
txd tx sign acl-issue.json --multisig $MULTISIG_ADDR --from acl-k1 \
  --output-document acl-k1-sign.json $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test
txd tx sign acl-issue.json --multisig $MULTISIG_ADDR --from acl-k2 \
  --output-document acl-k2-sign.json $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test

txd tx multisign acl-issue.json acl-multisig acl-k1-sign.json acl-k2-sign.json \
  $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test > acl-issue-signed.json

txd tx broadcast acl-issue-signed.json -y -b block $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

echo "=== 5. Grant Permissions ==="
MINTER_ADDR=$(txd keys show --address acl-minter --keyring-backend test)
BURNER_ADDR=$(txd keys show --address acl-burner --keyring-backend test)

# Grant mint permission (requires multisig)
txd tx authz grant $MINTER_ADDR generic \
  --msg-type=/coreum.asset.ft.v1.MsgMint \
  --from $MULTISIG_ADDR \
  --generate-only \
  $TX_CHAIN_ID_ARGS $TX_NODE_ARGS > acl-grant-mint.json

txd tx sign acl-grant-mint.json --multisig $MULTISIG_ADDR --from acl-k1 \
  --output-document acl-grant-mint-k1.json $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test
txd tx sign acl-grant-mint.json --multisig $MULTISIG_ADDR --from acl-k2 \
  --output-document acl-grant-mint-k2.json $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test

txd tx multisign acl-grant-mint.json acl-multisig \
  acl-grant-mint-k1.json acl-grant-mint-k2.json \
  $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test > acl-grant-mint-signed.json

txd tx broadcast acl-grant-mint-signed.json -y -b block $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

echo "=== 6. Mint Using Authz ==="
export FT_DENOM="uacltoken-$MULTISIG_ADDR"

txd tx assetft mint 500$FT_DENOM --from $MULTISIG_ADDR \
  --generate-only $TX_CHAIN_ID_ARGS $TX_NODE_ARGS > acl-mint.json

txd tx authz exec acl-mint.json --from $MINTER_ADDR -b block \
  $TX_NODE_ARGS $TX_CHAIN_ID_ARGS --keyring-backend test

echo "=== 7. Verify ==="
txd query bank balances $MULTISIG_ADDR --denom=$FT_DENOM $TX_NODE_ARGS

echo "✅ ACL setup complete!"
UI Alternative: Cosmos Multisig UI
For a graphical interface, you can use the Cosmos Multisig UI:

Visit: https://multisig.cosmos.network/

Select "TX" from the network dropdown (top right)

Or configure custom network settings for testnet/devnet

UI Workflow
Step	Action
1	Create multisig using addresses or public keys
2	Create transaction using the multisig
3	Members connect wallets and sign individually
4	Any member broadcasts once threshold is met
Important: If using addresses to create a multisig, those addresses must have been created on-chain (received funds) so their public keys are available.

Troubleshooting
"Signature verification failed"
Ensure you have enough signatures for the multisig threshold.

bash
# Check number of signatures
cat signed-tx.json | jq '.signatures | length'
"Authorization not found"
Verify the grant exists:

bash
txd query authz grant $MULTISIG_ADDR $MINTER_ADDR \
  --msg-type=/coreum.asset.ft.v1.MsgMint \
  $TX_NODE_ARGS
"Insufficient funds for fees"
Fund the executing account (minter, burner, etc.):

bash
# Send small amount for gas
txd tx bank send $MULTISIG_ADDR $MINTER_ADDR 1000000$TX_DENOM \
  $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test -y
Best Practices
Practice	Reason
Use separate keys for different roles	Principle of least privilege
Set grant expiration dates	Time-bound access
Test on testnet first	Validate workflow
Keep multisig threshold > 50%	Prevent deadlock
Monitor authz grants	Track who has permissions
Revoke unused grants	Reduce attack surface
Next Steps
Ledger Nano with CLI

Smart FT with WASM

Asset FT Extension

Resources
Authz Module Documentation

AssetFT Module Documentation

Multisig Tutorial

Gas Price Guide

