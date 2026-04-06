#!/bin/bash
echo "=== PHOENIX PME TESTNET DEPLOYMENT ==="
echo "Purpose: Prove the auction system works on real blockchain"
echo ""

# Step 1: Build optimized contract
echo "1. Building contract..."
cd contracts/phoenix-escrow
cargo wasm
WASM_SIZE=$(stat -f%z target/wasm32-unknown-unknown/release/*.wasm)
echo "✅ Contract built: $WASM_SIZE bytes"

# Step 2: Show deployment commands
echo -e "\n2. Deployment Commands:"
cat << 'DEPLOYCMDS'
# On Juno Testnet:
# junod tx wasm store target/wasm32-unknown-unknown/release/phoenix_escrow.wasm \
#   --from <your-wallet> \
#   --chain-id uni-6 \
#   --gas-prices 0.075ujunox \
#   --gas auto \
#   --gas-adjustment 1.3 \
#   --node https://juno-testnet-rpc.polkachu.com:443 \
#   --output json -y

# After storing, instantiate:
# junod tx wasm instantiate <CODE_ID> \
#   '{"admin": "<your-address>"}' \
#   --from <your-wallet> \
#   --label "Phoenix PME Test v1.0" \
#   --no-admin \
#   --chain-id uni-6 \
#   --gas-prices 0.075ujunox \
#   --node https://juno-testnet-rpc.polkachu.com:443
DEPLOYCMDS

echo -e "\n3. Test Transactions to Run:"
cat << 'TESTTX'
# Test 1: Create Auction
# junod tx wasm execute <CONTRACT_ADDRESS> \
#   '{"create_auction": {
#     "item_id": "test_platinum_bar",
#     "description": "1oz Platinum Bar .9995 Proof of Concept",
#     "metal_type": "platinum",
#     "product_form": "bar",
#     "weight": 31,
#     "starting_price": "100000"
#   }}' \
#   --from <your-wallet> \
#   --amount 100ujunox \  # Listing fee
#   --chain-id uni-6

# Test 2: Place Bid  
# junod tx wasm execute <CONTRACT_ADDRESS> \
#   '{"place_bid": {"auction_id": 1}}' \
#   --from <bidder-wallet> \
#   --amount 110000ujunox \  # Bid amount
#   --chain-id uni-6

# Test 3: End Auction (after time)
# junod tx wasm execute <CONTRACT_ADDRESS> \
#   '{"end_auction": {"auction_id": 1}}' \
#   --from <any-wallet> \
#   --chain-id uni-6
TESTTX

echo -e "\n✅ Deployment script ready"
echo "Next: Install junod, get testnet tokens, deploy!"
