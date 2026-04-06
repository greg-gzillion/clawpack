# Send Multisig Transaction

This tutorial describes the complete flow from creating a multisig account to broadcasting a transaction on TX Blockchain.

## Overview

Multisignature (multisig) accounts require multiple signatures to authorize a transaction. This is useful for:
- Shared treasury accounts
- Corporate governance
- Escrow services
- Enhanced security

## Prerequisites

- [ ] `txd` installed ([Installation Guide](../getting-started/install-txd.md))
- [ ] Network variables configured ([Network Variables](../getting-started/network-variables.md))
- [ ] Funded account (for fees)

---

## Step 1: Set Up Testnet Environment

```bash
# Set testnet endpoints
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"

# Create convenience arguments
export TX_NODE_ARGS="--node=$TX_NODE"
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
Step 2: Add Individual Keys
Option 1: Generate Keys Locally
bash
# Generate three keys for multisig participants
txd keys add k1 $TX_CHAIN_ID_ARGS --keyring-backend test
txd keys add k2 $TX_CHAIN_ID_ARGS --keyring-backend test
txd keys add k3 $TX_CHAIN_ID_ARGS --keyring-backend test

# Generate recipient key
txd keys add recipient $TX_CHAIN_ID_ARGS --keyring-backend test

# List all keys
txd keys list --keyring-backend test
Option 2: Add Public Keys from External Participants
If participants provide their public keys:

bash
# Add public keys from other participants
txd keys add k1 --pubkey='{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A8kOpeBMbmri5rvLjlqN6kOuNzRVUnr2vtinCkKMmwKU"}' $TX_CHAIN_ID_ARGS --keyring-backend test

txd keys add k2 --pubkey='{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"Aul+q9bj3zZTADlKbLcpmn/roDj2d0DJIHIQiyCQM8Fk"}' $TX_CHAIN_ID_ARGS --keyring-backend test

txd keys add k3 --pubkey='{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A3AcsNQ+FNwnUovxN/6/sa/vVN+Lc89IksZQKpLyAQ16"}' $TX_CHAIN_ID_ARGS --keyring-backend test
List All Keys
bash
txd keys list --keyring-backend test
Expected output:

text
- name: k1
  type: local
  address: testcore1qj7d46j56khz4ysvvgt5elghhu6p3fxepzme7y
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A8kOpeBMbmri5rvLjlqN6kOuNzRVUnr2vtinCkKMmwKU"}'
  mnemonic: ""

- name: k2
  type: local
  address: testcore1xj8k5y8v5f8zq7p3x2w4l8k9j3h5g2f1d8s7a6d
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"Aul+q9bj3zZTADlKbLcpmn/roDj2d0DJIHIQiyCQM8Fk"}'
  mnemonic: ""

- name: k3
  type: local
  address: testcore1y7k9l0m1n2b3v4c5x6z7a8s9d0f1g2h3j4k5l6
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A3AcsNQ+FNwnUovxN/6/sa/vVN+Lc89IksZQKpLyAQ16"}'
  mnemonic: ""
Step 3: Create Multisig Account
Create a 2-of-3 multisig account (requires 2 out of 3 signatures):

bash
txd keys add k1k2k3 \
  --multisig "k1,k2,k3" \
  --multisig-threshold 2 \
  $TX_CHAIN_ID_ARGS \
  --keyring-backend test
Expected output:

text
- name: k1k2k3
  type: multi
  address: testcore13purcatgmnadw3606rcyatmt60ys6e37mcnaar
  pubkey: '{"@type":"/cosmos.crypto.multisig.LegacyAminoPubKey","threshold":2,"public_keys":[{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A8kOpeBMbmri5rvLjlqN6kOuNzRVUnr2vtinCkKMmwKU"},{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"Aul+q9bj3zZTADlKbLcpmn/roDj2d0DJIHIQiyCQM8Fk"},{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A3AcsNQ+FNwnUovxN/6/sa/vVN+Lc89IksZQKpLyAQ16"}]}'
  mnemonic: ""
Get Multisig Address
bash
MULTISIG_ADDR=$(txd keys show --address k1k2k3 --keyring-backend test)
echo "Multisig Address: $MULTISIG_ADDR"
Step 4: Fund the Multisig Account
Option A: Use Faucet
Go to TX Testnet Faucet

Enter the multisig address (starts with testcore...)

Request tokens

Option B: Send from Another Account
bash
# If you have a funded account
txd tx bank send my-wallet $MULTISIG_ADDR 10000000$TX_DENOM \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  --gas auto --gas-adjustment 1.3 \
  -y
Check Multisig Balance
bash
txd query bank balances $MULTISIG_ADDR $TX_NODE_ARGS
Step 5: Generate Unsigned Transaction
Create a JSON file for the unsigned transaction to send funds to recipient:

bash
RECIPIENT_ADDR=$(txd keys show --address recipient --keyring-backend test)

txd tx bank send $MULTISIG_ADDR $RECIPIENT_ADDR 700$TX_DENOM \
  --from $MULTISIG_ADDR \
  --generate-only \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  > bank-unsigned-tx.json
Verify Transaction Content
bash
cat bank-unsigned-tx.json
Example output:

json
{
  "body": {
    "messages": [
      {
        "@type": "/cosmos.bank.v1beta1.MsgSend",
        "from_address": "testcore13purcatgmnadw3606rcyatmt60ys6e37mcnaar",
        "to_address": "testcore1lyru5pvjymya9xq0rsg406fss45sama8e9dqrs",
        "amount": [
          {
            "denom": "utestcore",
            "amount": "700"
          }
        ]
      }
    ],
    "memo": "",
    "timeout_height": "0"
  },
  "auth_info": {
    "signer_infos": [],
    "fee": {
      "amount": [
        {
          "denom": "utestcore",
          "amount": "300000"
        }
      ],
      "gas_limit": "200000"
    }
  },
  "signatures": []
}
Step 6: Add First Signature
Sign from k1
bash
txd tx sign bank-unsigned-tx.json \
  --multisig $MULTISIG_ADDR \
  --from k1 \
  --output-document k1sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test
Add Signature to Multisig Transaction
bash
txd tx multisign bank-unsigned-tx.json k1k2k3 k1sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  > bank-signed-tx.json
Try Broadcasting (Should Fail - Needs 2 Signatures)
bash
txd tx broadcast bank-signed-tx.json \
  -y -b block \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS
Expected result: Transaction will fail because only 1 of 2 required signatures is present.

Step 7: Add Second Signature
Sign from k2
bash
txd tx sign bank-unsigned-tx.json \
  --multisig $MULTISIG_ADDR \
  --from k2 \
  --output-document k2sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test
Combine Signatures
bash
txd tx multisign bank-unsigned-tx.json k1k2k3 k1sign.json k2sign.json \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  --keyring-backend test \
  > bank-signed-tx.json
Step 8: Broadcast Transaction
bash
txd tx broadcast bank-signed-tx.json \
  -y -b block \
  $TX_NODE_ARGS \
  $TX_CHAIN_ID_ARGS
Expected output:

json
{
  "code": 0,
  "txhash": "2A4F3E8B9C1D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3E4F5A6B7C8D9E0F",
  "raw_log": "[{\"events\":...}]"
}
Step 9: Verify Transaction
Check Recipient Balance
bash
RECIPIENT_ADDR=$(txd keys show --address recipient --keyring-backend test)

txd query bank balances $RECIPIENT_ADDR $TX_NODE_ARGS
Check Multisig Balance
bash
txd query bank balances $MULTISIG_ADDR $TX_NODE_ARGS
View Transaction on Explorer
Copy the txhash from broadcast output

Visit TX Testnet Explorer

Search for the transaction hash

Complete Script Example
bash
#!/bin/bash
# multisig-transfer.sh - Complete multisig transaction flow

set -e

# Configuration
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_NODE_ARGS="--node=$TX_NODE"
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"

echo "=== 1. Creating keys ==="
txd keys add k1 --keyring-backend test $TX_CHAIN_ID_ARGS
txd keys add k2 --keyring-backend test $TX_CHAIN_ID_ARGS
txd keys add k3 --keyring-backend test $TX_CHAIN_ID_ARGS
txd keys add recipient --keyring-backend test $TX_CHAIN_ID_ARGS

echo "=== 2. Creating multisig account ==="
txd keys add k1k2k3 --multisig "k1,k2,k3" --multisig-threshold 2 --keyring-backend test $TX_CHAIN_ID_ARGS

MULTISIG_ADDR=$(txd keys show --address k1k2k3 --keyring-backend test)
RECIPIENT_ADDR=$(txd keys show --address recipient --keyring-backend test)

echo "Multisig Address: $MULTISIG_ADDR"
echo "Recipient Address: $RECIPIENT_ADDR"

echo "=== 3. Fund multisig (manual) ==="
echo "Please fund $MULTISIG_ADDR from faucet"
read -p "Press Enter after funding..."

echo "=== 4. Generating unsigned tx ==="
txd tx bank send $MULTISIG_ADDR $RECIPIENT_ADDR 700$TX_DENOM \
  --from $MULTISIG_ADDR \
  --generate-only \
  $TX_CHAIN_ID_ARGS \
  $TX_NODE_ARGS \
  > bank-unsigned-tx.json

echo "=== 5. Adding signatures ==="
txd tx sign bank-unsigned-tx.json --multisig $MULTISIG_ADDR --from k1 \
  --output-document k1sign.json $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test

txd tx multisign bank-unsigned-tx.json k1k2k3 k1sign.json \
  $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test > bank-signed-tx.json

txd tx sign bank-unsigned-tx.json --multisig $MULTISIG_ADDR --from k2 \
  --output-document k2sign.json $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test

txd tx multisign bank-unsigned-tx.json k1k2k3 k1sign.json k2sign.json \
  $TX_CHAIN_ID_ARGS $TX_NODE_ARGS --keyring-backend test > bank-signed-tx.json

echo "=== 6. Broadcasting ==="
txd tx broadcast bank-signed-tx.json -y -b block $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

echo "=== 7. Verifying ==="
txd query bank balances $RECIPIENT_ADDR $TX_NODE_ARGS

echo "✅ Multisig transaction complete!"
Multisig Configuration Options
Different Thresholds
Threshold	Description	Use Case
1-of-2	Any single signature	Simple shared account
2-of-2	Both signatures required	Joint account
2-of-3	Majority (2 of 3)	Council/DAO
3-of-5	Supermajority	High security
Create Different Multisig Configurations
bash
# 1-of-2 multisig
txd keys add multisig-1of2 --multisig "k1,k2" --multisig-threshold 1

# 2-of-2 multisig
txd keys add multisig-2of2 --multisig "k1,k2" --multisig-threshold 2

# 3-of-5 multisig
txd keys add multisig-3of5 --multisig "k1,k2,k3,k4,k5" --multisig-threshold 3
Troubleshooting
Error: "signature verification failed"
Solution: Ensure you have the correct number of signatures for the threshold.

Error: "account sequence mismatch"
Solution: Wait for previous transaction to complete or sync your client:

bash
txd query account $MULTISIG_ADDR $TX_NODE_ARGS
Error: "insufficient funds"
Solution: Check multisig balance:

bash
txd query bank balances $MULTISIG_ADDR $TX_NODE_ARGS
Missing Signatures
List signatures in the transaction:

bash
cat bank-signed-tx.json | jq '.signatures | length'
Best Practices
Store mnemonics securely - Each multisig participant must secure their key

Verify addresses - Double-check multisig and recipient addresses

Test with small amounts - Test the flow before large transfers

Use keyring-backend test for development, os for production

Keep signature order consistent - Use the same order when combining signatures

Next Steps
Smart FT with ACL

Ledger Nano with CLI

Transfer funds with CLI

Resources
Special Addresses

Gas Price Guide

Network Variables
