# TX Blockchain Faucet

## Overview
The TX faucet provides testnet tokens for developers and users to test applications.

## Access the Faucet
**URL**: [https://faucet.testnet.tx.dev](https://faucet.testnet.tx.dev)

## How to Get Testnet Tokens

### Method 1: Web Interface
1. Go to the faucet URL
2. Enter your testnet address (starts with `testcore...`)
3. Complete verification if required
4. Click "Request Tokens"

### Method 2: Generate Wallet First

**Via Wallet Interface**:
1. Go to [wallet page](https://wallet.tx.org)
2. Connect or install a wallet
3. Create account there

**Via CLI (Advanced)**:
```bash
export TX_CHAIN_ID="txchain-testnet-1"
txd keys add my-wallet --chain-id=$TX_CHAIN_ID
Method 3: Generate Funded Wallet
Click the "Generate Funded Wallet" button on the faucet page.

Network Variables
Network	Chain ID	Faucet URL
Mainnet	tx-mainnet-1	N/A (real tokens)
Testnet	txchain-testnet-1	https://faucet.testnet.tx.dev
Devnet	txchain-local	Built-in
Important Notes
Faucet tokens are for testing only

Rate limits may apply

Tokens have no real value

Use testcore prefix addresses
