#!/bin/bash
# Coreum testnet health check

RPC_URL="https://full-node.testnet-1.coreum.dev:26657"

echo "🪙 Coreum Testnet Health Check - $(date)"
echo "========================================="

if curl -s -o /dev/null -w "%{http_code}" "$RPC_URL/status" | grep -q "200"; then
    echo "✅ RPC endpoint responsive"
    STATUS=$(curl -s "$RPC_URL/status")
    LATEST_BLOCK=$(echo "$STATUS" | jq -r '.result.sync_info.latest_block_height')
    echo "📦 Latest Block: $LATEST_BLOCK"
else
    echo "❌ RPC endpoint unreachable"
fi
