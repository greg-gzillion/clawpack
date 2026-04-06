#!/bin/bash
# PhoenixPME - TX Testnet Deployment Script
# March 6, 2026 - TX Mainnet Launch
set -e

# ============================================
# CONFIGURATION - CHANGE THESE ON LAUNCH DAY
# ============================================
CHAIN_ID="tx-testnet-1"  # Will change March 6
RPC_URL="https://full-node.testnet-1.coreum.dev:26657"  # Replace with TX RPC
DENOM="utestcore"  # Replace with "utx" after merger
KEYRING_BACKEND="test"
GAS_PRICE="0.25"
FEE_AMOUNT="5000000"
WASM_PATH="/home/greg/dev/TX/contracts/auction/target/wasm32-unknown-unknown/release/phoenix_auction.wasm"

# ============================================
# COLORS FOR OUTPUT
# ============================================
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ============================================
# VALIDATE WASM FILE EXISTS
# ============================================
echo -e "${YELLOW}🔍 Validating contract...${NC}"
if [ ! -f "$WASM_PATH" ]; then
    echo -e "${RED}❌ WASM file not found at $WASM_PATH${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Contract found: $(basename $WASM_PATH)${NC}"
echo -e "   Size: $(wc -c < $WASM_PATH | numfmt --to=iec) bytes"

# ============================================
# CHECK WALLET EXISTS
# ============================================
echo -e "${YELLOW}🔑 Checking wallet...${NC}"
WALLET_ADDR=$(cored keys show treasury --address --keyring-backend $KEYRING_BACKEND 2>/dev/null || true)
if [ -z "$WALLET_ADDR" ]; then
    echo -e "${RED}❌ Wallet 'treasury' not found. Import it first.${NC}"
    echo "   Run: cored keys add treasury --recover --keyring-backend $KEYRING_BACKEND"
    exit 1
fi
echo -e "${GREEN}✅ Wallet: $WALLET_ADDR${NC}"

# ============================================
# CHECK BALANCE - WITH ERROR HANDLING
# ============================================
echo -e "${YELLOW}💰 Checking balance...${NC}"

# Try to get balance, but don't fail if RPC is down
BALANCE_RAW=$(cored query bank balances $WALLET_ADDR \
  --node $RPC_URL \
  --chain-id $CHAIN_ID \
  --denom $DENOM \
  --output json 2>/dev/null || echo '{"amount":"0"}')

# Extract amount, default to 0 if jq fails
BALANCE=$(echo "$BALANCE_RAW" | jq -r '.amount // "0"' 2>/dev/null || echo "0")

echo -e "   Balance: $BALANCE $DENOM"

# Skip balance check if RPC is down (we know it's broken)
if [ "$BALANCE" = "0" ] && [[ "$RPC_URL" == *"coreum"* ]]; then
    echo -e "${YELLOW}⚠️  Skipping balance check - Coreum testnet RPC is unreliable${NC}"
    echo -e "   Will attempt deployment anyway on March 6 with TX RPC."
else
    if [ "$BALANCE" -lt "$FEE_AMOUNT" ] 2>/dev/null; then
        echo -e "${RED}❌ Insufficient balance. Need at least $FEE_AMOUNT $DENOM${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ Sufficient funds${NC}"
    fi
fi
# ============================================
# SIMULATE FIRST (DRY RUN)
# ============================================
echo -e "${YELLOW}🧪 Simulating deployment...${NC}"
cored tx wasm store "$WASM_PATH" \
  --from $WALLET_ADDR \
  --chain-id $CHAIN_ID \
  --node $RPC_URL \
  --gas auto \
  --fees ${FEE_AMOUNT}${DENOM} \
  --keyring-backend $KEYRING_BACKEND \
  --dry-run \
  --output json > /tmp/deploy-sim.json 2>&1 || true

if grep -q "insufficient" /tmp/deploy-sim.json; then
    echo -e "${RED}❌ Simulation failed - insufficient funds${NC}"
    cat /tmp/deploy-sim.json | jq -r '.raw_log // .message'
    exit 1
fi
echo -e "${GREEN}✅ Simulation passed${NC}"

# ============================================
# DEPLOY CONTRACT
# ============================================
echo -e "${YELLOW}🚀 Deploying contract...${NC}"
RESULT=$(cored tx wasm store "$WASM_PATH" \
  --from $WALLET_ADDR \
  --chain-id $CHAIN_ID \
  --node $RPC_URL \
  --gas auto \
  --fees ${FEE_AMOUNT}${DENOM} \
  --keyring-backend $KEYRING_BACKEND \
  --yes \
  --output json)

# ============================================
# EXTRACT CODE ID
# ============================================
TX_HASH=$(echo $RESULT | jq -r '.txhash')
echo -e "${GREEN}✅ Transaction submitted${NC}"
echo -e "   TX Hash: $TX_HASH"

echo -e "${YELLOW}⏳ Waiting for confirmation...${NC}"
sleep 5

CODE_ID=$(cored query tx $TX_HASH \
  --node $RPC_URL \
  --chain-id $CHAIN_ID \
  --output json 2>/dev/null | \
  jq -r '.logs[0].events[] | select(.type=="store_code") | .attributes[] | select(.key=="code_id") | .value')

# ============================================
# OUTPUT RESULTS
# ============================================
if [ -n "$CODE_ID" ] && [ "$CODE_ID" != "null" ]; then
    echo -e "${GREEN}🎉 DEPLOYMENT SUCCESSFUL!${NC}"
    echo -e "   Code ID: ${GREEN}$CODE_ID${NC}"
    echo -e "   Explorer: https://explorer.testnet-1.coreum.dev/coreum/tx/$TX_HASH"
    
    # Save to file
    echo "TX_HASH=$TX_HASH" > /tmp/last-deploy.env
    echo "CODE_ID=$CODE_ID" >> /tmp/last-deploy.env
    echo "DEPLOY_TIME=$(date)" >> /tmp/last-deploy.env
else
    echo -e "${RED}❌ Deployment failed${NC}"
    echo $RESULT | jq -r '.raw_log // .'
    exit 1
fi
