#!/bin/bash
echo "=== TRACKING DEPLOYMENT ==="
echo "Check recent transactions from your address:"

YOUR_ADDRESS="testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6"

# Get latest transaction
cored query txs --events "message.sender='$YOUR_ADDRESS'" \
  --node https://full-node.testnet-1.coreum.dev:26657 \
  --chain-id coreum-testnet-1 \
  --limit 1 --output json | jq -r '.txs[0] | "Tx hash: \(.txhash)\nHeight: \(.height)\nTimestamp: \(.timestamp)"'

echo -e "\n=== CHECKING YOUR CONTRACTS ==="
cored query wasm list-code \
  --node https://full-node.testnet-1.coreum.dev:26657 \
  --chain-id coreum-testnet-1 \
  --limit 10 --output json | jq -r --arg ADDR "$YOUR_ADDRESS" '.code_infos[] | select(.creator==$ADDR) | "Your code_id: \(.code_id)"'
