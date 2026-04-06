#!/bin/bash
set -e

echo "🚀 Deploying to Coreum Testnet (wasmd v0.60.2 compatible)..."
echo "=========================================================="

# Configuration
WALLET="testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6"
CHAIN_ID="coreum-testnet-1"
RPC_NODE="https://full-node.testnet-1.coreum.dev:26657"
ORIGINAL_WASM="target/wasm32-unknown-unknown/release/phoenix_auction.wasm"
OPTIMIZED_WASM="target/wasm32-unknown-unknown/release/phoenix_auction_coreum.wasm"

# Step 1: Build with bulk memory disabled
echo "🔨 Step 1: Building contract..."
RUSTFLAGS="-C target-feature=-bulk-memory" cargo build --release --target wasm32-unknown-unknown

# Step 2: Optimize with wasm-opt
echo "🔧 Step 2: Optimizing for Coreum compatibility..."
which wasm-opt >/dev/null 2>&1 || { echo "Installing wasm-opt..."; sudo apt update && sudo apt install binaryen -y; }

wasm-opt "$ORIGINAL_WASM" \
  -Oz \
  --disable-bulk-memory \
  --disable-sign-ext \
  --disable-mutable-globals \
  --disable-nontrapping-float-to-int \
  --disable-simd \
  --disable-tail-call \
  --disable-reference-types \
  --disable-multivalue \
  -o "$OPTIMIZED_WASM"

echo "📦 Original: $(ls -lh "$ORIGINAL_WASM" | awk '{print $5}')"
echo "📦 Optimized: $(ls -lh "$OPTIMIZED_WASM" | awk '{print $5}')"

# Step 3: Deploy
echo "📤 Step 3: Deploying to $CHAIN_ID..."
TX_OUTPUT=$(cored tx wasm store "$OPTIMIZED_WASM" \
  --from "$WALLET" \
  --chain-id "$CHAIN_ID" \
  --node "$RPC_NODE" \
  --gas auto \
  --gas-adjustment 2.0 \
  --fees 150000utestcore \
  --yes \
  --output json 2>&1)

# Check if successful
if echo "$TX_OUTPUT" | grep -q "txhash"; then
    TX_HASH=$(echo "$TX_OUTPUT" | jq -r '.txhash')
    echo "✅ Transaction submitted: $TX_HASH"
    
    echo "⏳ Waiting 15 seconds..."
    sleep 15
    
    echo "🔍 Checking status..."
    TX_STATUS=$(cored q tx "$TX_HASH" --node "$RPC_NODE" --output json 2>/dev/null | jq -r '.tx_response.code // "unknown"')
    
    if [ "$TX_STATUS" = "0" ]; then
        echo "🎉 SUCCESS! Contract deployed!"
        
        CODE_ID=$(cored q tx "$TX_HASH" --node "$RPC_NODE" --output json | jq -r '.tx_response.logs[].events[] | select(.type=="store_code") | .attributes[] | select(.key=="code_id") | .value')
        echo "🔢 Code ID: $CODE_ID"
        
        # Save deployment info
        echo "CODE_ID=$CODE_ID" > .deployment
        echo "TX_HASH=$TX_HASH" >> .deployment
        echo "WASM_FILE=$OPTIMIZED_WASM" >> .deployment
        echo "DATE=$(date)" >> .deployment
        
        echo ""
        echo "🏗️ Instantiate with:"
        echo "cored tx wasm instantiate $CODE_ID '{\"admin\":\"$WALLET\",\"insurance_pool\":\"$WALLET\",\"token_denom\":\"utestusd-$WALLET\"}' --from $WALLET --label \"PhoenixPME v1.0\" --chain-id $CHAIN_ID --node $RPC_NODE --fees 50000utestcore --yes"
    else
        echo "❌ Transaction failed: $TX_STATUS"
    fi
else
    echo "❌ Deployment failed!"
    echo "Error: $TX_OUTPUT"
fi
