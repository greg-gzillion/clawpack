#!/bin/bash
# Phoenix Auction - Build and Deploy for Coreum
set -e

echo "=== Phoenix Auction Build & Deploy ==="

# 1. Clean
echo "1. Cleaning..."
cargo clean
rm -rf artifacts

# 2. Build
echo "2. Building..."
cargo build --release --target wasm32-unknown-unknown
echo "✅ Build: $(ls -lh target/wasm32-unknown-unknown/release/phoenix_auction.wasm | awk '{print $5}')"

# 3. Install wasm-tools if needed
if ! command -v wasm-tools &> /dev/null; then
    echo "Installing wasm-tools..."
    cargo install wasm-tools --force
fi

# 4. Transform for Coreum
echo "3. Transforming for Coreum..."
mkdir -p artifacts
wasm-tools print target/wasm32-unknown-unknown/release/phoenix_auction.wasm \
    -o artifacts/contract.wat 2>/dev/null
sed -i 's/memory\.copy/drop drop drop/g' artifacts/contract.wat
sed -i 's/memory\.fill/drop drop drop/g' artifacts/contract.wat
wasm-tools parse artifacts/contract.wat \
    -o artifacts/phoenix_auction_coreum.wasm
echo "✅ Coreum-ready: $(ls -lh artifacts/phoenix_auction_coreum.wasm | awk '{print $5}')"

# 5. Deploy
echo -e "\n4. Ready to deploy!"
echo "Run:"
echo "cored tx wasm store artifacts/phoenix_auction_coreum.wasm \\"
echo "  --from testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6 \\"
echo "  --chain-id coreum-testnet-1 \\"
echo "  --node https://full-node.testnet-1.coreum.dev:26657 \\"
echo "  --gas auto --gas-adjustment 2.0 --fees 350000utestcore \\"
echo "  --yes --broadcast-mode sync"
