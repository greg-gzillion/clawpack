#!/bin/bash
set -e

echo "🚀 Deploying PhoenixPME Auction Contract..."
echo "=========================================="

# Configuration
WALLET="testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6"
CHAIN_ID="coreum-testnet-1"
RPC_NODE="https://full-node.testnet-1.coreum.dev:26657"
WASM_FILE="target/wasm32-unknown-unknown/release/phoenix_auction.wasm"

echo "📦 Contract: $WASM_FILE"
echo "👛 Wallet: $WALLET"
echo "🔗 Chain: $CHAIN_ID"
echo "🌐 Node: $RPC_NODE"

# Check if WASM file exists
if [ ! -f "$WASM_FILE" ]; then
    echo "❌ WASM file not found: $WASM_FILE"
    echo "Run: RUSTFLAGS='-C target-feature=-bulk-memory' cargo build --release --target wasm32-unknown-unknown"
    exit 1
fi

echo ""
echo "📤 Storing contract on $CHAIN_ID..."

# Deploy
TX_OUTPUT=$(cored tx wasm store "$WASM_FILE" \
  --from "$WALLET" \
  --chain-id "$CHAIN_ID" \
  --node "$RPC_NODE" \
  --gas auto \
  --gas-adjustment 2.0 \
  --fees 100000utestcore \
  --yes \
  --output json)

# Extract transaction hash
if echo "$TX_OUTPUT" | grep -q "txhash"; then
    TX_HASH=$(echo "$TX_OUTPUT" | jq -r '.txhash')
    echo "✅ Transaction submitted!"
    echo "📝 TX Hash: $TX_HASH"
    
    echo ""
    echo "⏳ Waiting 10 seconds for confirmation..."
    sleep 10
    
    echo ""
    echo "🔍 Checking transaction status..."
    TX_STATUS=$(cored q tx "$TX_HASH" --node "$RPC_NODE" --output json 2>/dev/null | jq -r '.tx_response.code // "unknown"')
    
    if [ "$TX_STATUS" = "0" ]; then
        echo "🎉 Contract deployed successfully!"
        
        # Get Code ID
        CODE_ID=$(cored q tx "$TX_HASH" --node "$RPC_NODE" --output json | jq -r '.tx_response.logs[].events[] | select(.type=="store_code") | .attributes[] | select(.key=="code_id") | .value')
        echo "🔢 Code ID: $CODE_ID"
        
        echo ""
        echo "🏗️ Ready to instantiate with:"
        echo "cored tx wasm instantiate $CODE_ID \\"
        echo "  '{\"admin\":\"$WALLET\",\"insurance_pool\":\"$WALLET\",\"token_denom\":\"utestusd-$WALLET\"}' \\"
        echo "  --from $WALLET \\"
        echo "  --label \"PhoenixPME Auction v1.0\" \\"
        echo "  --chain-id $CHAIN_ID \\"
        echo "  --node $RPC_NODE \\"
        echo "  --fees 50000utestcore \\"
        echo "  --yes"
        
        # Save to file for reference
        echo "CODE_ID=$CODE_ID" > .deployment
        echo "TX_HASH=$TX_HASH" >> .deployment
        echo "Deployed: $(date)" >> .deployment
        
    else
        echo "❌ Transaction failed with code: $TX_STATUS"
        echo "Check details: cored q tx $TX_HASH --node $RPC_NODE"
    fi
else
    echo "❌ Deployment failed!"
    echo "Error output:"
    echo "$TX_OUTPUT"
fi
