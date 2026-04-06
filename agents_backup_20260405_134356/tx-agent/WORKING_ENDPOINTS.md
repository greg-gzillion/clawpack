# Coreum Testnet - Working Endpoints (Verified April 2026)

## Network Information
- **Chain ID:** coreum-testnet-1
- **Denom:** utestcore

## RPC Endpoints
| Type | URL | Status |
| Type | URL | Status |
|------|-----|--------|
| RPC | https://full-node.testnet-1.coreum.dev:26657 | ✅ Working |
| REST/LCD | https://full-node.testnet-1.coreum.dev:1317 | ✅ Working |

## Faucet
curl -X POST https://faucet.testnet-1.coreum.dev/claim -H 'Content-Type: application/json' -d '{"address": "YOUR_WALLET_ADDRESS", "denom": "utestcore"}'

## Verification
curl -s https://full-node.testnet-1.coreum.dev:26657/status | jq '.result.sync_info.latest_block_height'
