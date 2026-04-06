#!/bin/bash
# Complete build and deploy for Coreum
set -e

echo "=== Phoenix Auction Build & Deploy ==="
echo ""

# 1. Build
echo "🔨 Building contract..."
export RUSTFLAGS="-C target-feature=-bulk-memory"
cargo build --release --target wasm32-unknown-unknown

# 2. Check for bulk memory
echo "🔍 Checking for bulk memory ops..."
python3 << 'PYTHON'
import sys

with open('target/wasm32-unknown-unknown/release/phoenix_auction.wasm', 'rb') as f:
    data = f.read()

fc_count = sum(1 for b in data if b == 0xfc)
print(f"Original: {len(data)} bytes, {fc_count} bulk memory ops")

if fc_count == 0:
    print("✅ Already clean!")
    import shutil
    shutil.copy('target/wasm32-unknown-unknown/release/phoenix_auction.wasm', 'artifacts/phoenix_auction_coreum.wasm')
else:
    print(f"⚠ Needs patching...")
PYTHON

# 3. Patch if needed
if [ -f "patch_wasm.py" ]; then
    echo "🛠 Patching bulk memory ops..."
    python3 patch_wasm.py target/wasm32-unknown-unknown/release/phoenix_auction.wasm artifacts/phoenix_auction_coreum.wasm
fi

# 4. Deploy
echo -e "\n🚀 Ready to deploy!"
echo "Contract: artifacts/phoenix_auction_coreum.wasm"
ls -lh artifacts/phoenix_auction_coreum.wasm

read -p "Deploy to Coreum testnet? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Deploying..."
    cored tx wasm store artifacts/phoenix_auction_coreum.wasm \
        --from testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6 \
        --chain-id coreum-testnet-1 \
        --node https://full-node.testnet-1.coreum.dev:26657 \
        --gas auto \
        --gas-adjustment 2.0 \
        --fees 350000utestcore \
        --yes \
        --broadcast-mode sync
    
    echo -e "\n✅ Deployment submitted!"
    echo "Check with: cored query tx <txhash> --node https://full-node.testnet-1.coreum.dev:26657"
fi

echo -e "\n=== Next Steps ==="
echo "1. After deployment, note the code_id"
echo "2. Instantiate: cored tx wasm instantiate <code_id> '{\"admin\":\"your_address\",\"insurance_pool\":\"pool_address\",\"token_denom\":\"utestcore\"}' ..."
echo "3. Interact with your auction contract!"
