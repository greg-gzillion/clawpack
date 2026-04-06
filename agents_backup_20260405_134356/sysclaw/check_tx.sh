#!/bin/bash
# TX Blockchain health check

echo "🪙 TX Blockchain Health Check - $(date)"
echo "========================================="

# Testnet check
TESTNET_RPC="https://full-node.testnet-1.tx.dev:26657"

if curl -s -o /dev/null -w "%{http_code}" "$TESTNET_RPC/status" | grep -q "200"; then
    echo "✅ Testnet RPC responsive"
    
    STATUS=$(curl -s "$TESTNET_RPC/status")
    LATEST_BLOCK=$(echo "$STATUS" | jq -r '.result.sync_info.latest_block_height')
    CATCHING_UP=$(echo "$STATUS" | jq -r '.result.sync_info.catching_up')
    
    echo "📦 Latest Block: $LATEST_BLOCK"
    echo "🔄 Catching Up: $CATCHING_UP"
else
    echo "❌ Testnet RPC unreachable"
fi

echo ""
echo "🔗 Useful Links:"
echo "   Website: https://tx.org"
echo "   Docs: https://docs.tx.org"
echo "   GitHub: https://github.com/tokenize-x/tx-chain"
echo "   Explorer: https://explorer.tx.org"
