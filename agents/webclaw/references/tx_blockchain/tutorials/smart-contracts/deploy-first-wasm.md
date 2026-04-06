# Deploy First WASM Contract

Deploy, instantiate, and interact with CosmWasm smart contracts on TX Blockchain using a nameservice contract example.

## What Is CosmWasm?

CosmWasm is a smart contract platform for Cosmos SDK-based blockchains featuring:

- **Multi-chain Compatibility** - Run on any blockchain with CosmWasm module
- **Rust Language** - Memory-safe, high-performance smart contracts
- **IBC Integration** - Cross-chain messaging and interoperability
- **Customizable** - Flexible for various application needs

## Prerequisites

```bash
# Verify requirements
rustc --version && cargo --version
txd version
jq --version
docker --version

# Set testnet variables
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export DENOM="utestcore"
export KEYRING_BACKEND=test

export TX_NODE_ARGS="--node=$RPC_URL"
export TX_CHAIN_ID_ARGS="--chain-id=$CHAIN_ID --keyring-backend=$KEYRING_BACKEND"
Source Code
bash
# Clone the contracts repository
git clone https://github.com/tokenize-x/tx-cw-contracts.git

# Navigate to nameservice contract
cd tx-cw-contracts/contracts/nameservice
Setup Account
bash
# Generate wallet
txd keys add wallet $TX_CHAIN_ID_ARGS

# Fund via faucet at https://faucet.testnet.tx.dev

# Check balance
txd query bank balances $(txd keys show wallet -a $TX_CHAIN_ID_ARGS) \
    --denom $DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Build Contract
bash
# Build optimized WASM using CosmWASM optimizer
docker run --rm -v "$(pwd)":/code \
  --mount type=volume,source="$(basename "$(pwd)")_cache",target=/target \
  --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
  cosmwasm/optimizer:0.15.0
Note: This may take several minutes. If you get "could not find Cargo.toml", ensure you're in cw-contracts/contracts/nameservice directory.

Deploy Contract
List Existing Contracts
bash
txd query wasm list-code $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Store Contract on Chain
bash
RES=$(txd tx wasm store artifacts/cw_nameservice.wasm \
    --from wallet \
    --gas auto --gas-adjustment 1.3 \
    -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

echo $RES

# Extract Code ID
CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Code ID: $CODE_ID"
Verify Deployment
bash
txd query wasm code-info $CODE_ID $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Instantiate Contract
Instantiate Message Structure
rust
pub struct InstantiateMsg {
    pub purchase_price: Coin,
    pub transfer_price: Coin,
}
Instantiate Command
bash
INIT="{\"purchase_price\":{\"amount\":\"100\",\"denom\":\"$DENOM\"},\"transfer_price\":{\"amount\":\"999\",\"denom\":\"$DENOM\"}}"

txd tx wasm instantiate $CODE_ID "$INIT" \
    --from wallet \
    --label "name service" \
    -b block -y --no-admin \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Get Contract Address
bash
# List contracts by code ID
txd query wasm list-contract-by-code $CODE_ID --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

CONTRACT_ADDRESS=$(txd query wasm contract-by-code $CODE_ID --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Contract Address: $CONTRACT_ADDRESS"
Interact with Contract
Execute Messages
rust
pub enum ExecuteMsg {
    Register { name: String },
    Transfer { name: String, to: String },
}
Register a Name
bash
REGISTER='{"register":{"name":"fred"}}'

txd tx wasm execute $CONTRACT_ADDRESS "$REGISTER" \
    --amount 100$DENOM \
    --from wallet -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Query Name Record
rust
pub enum QueryMsg {
    ResolveRecord { name: String },
}
bash
NAME_QUERY='{"resolve_record": {"name": "fred"}}'

txd query wasm contract-state smart $CONTRACT_ADDRESS "$NAME_QUERY" \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Expected output shows wallet address as owner.

Create New Owner Account
bash
txd keys add new-owner $TX_CHAIN_ID_ARGS

RECIPIENT_ADDRESS=$(txd keys show new-owner -a $TX_CHAIN_ID_ARGS)
echo "New Owner: $RECIPIENT_ADDRESS"
Transfer Name Ownership
bash
TRANSFER="{\"transfer\":{\"name\":\"fred\",\"to\":\"$RECIPIENT_ADDRESS\"}}"

txd tx wasm execute $CONTRACT_ADDRESS "$TRANSFER" \
    --amount 999$DENOM \
    --from wallet -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Verify Transfer
bash
NAME_QUERY='{"resolve_record": {"name": "fred"}}'

txd query wasm contract-state smart $CONTRACT_ADDRESS "$NAME_QUERY" \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
The owner should now be the new-owner address.

Complete Script
bash
#!/bin/bash
# deploy-first-wasm.sh - Complete WASM deployment script

set -e

# Configuration
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export DENOM="utestcore"
export KEYRING_BACKEND=test
export TX_NODE_ARGS="--node=$RPC_URL"
export TX_CHAIN_ID_ARGS="--chain-id=$CHAIN_ID --keyring-backend=$KEYRING_BACKEND"

# Setup account
echo "=== Setting up wallet ==="
txd keys add wallet $TX_CHAIN_ID_ARGS 2>/dev/null || true
WALLET=$(txd keys show wallet -a $TX_CHAIN_ID_ARGS)
echo "Wallet: $WALLET"

# Check balance
echo "Checking balance..."
txd query bank balances $WALLET --denom $DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Clone and build
echo "=== Building contract ==="
git clone https://github.com/tokenize-x/tx-cw-contracts.git 2>/dev/null || true
cd tx-cw-contracts/contracts/nameservice

docker run --rm -v "$(pwd)":/code \
    --mount type=volume,source="$(basename "$(pwd)")_cache",target=/target \
    --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
    cosmwasm/optimizer:0.15.0

# Deploy
echo "=== Deploying contract ==="
RES=$(txd tx wasm store artifacts/cw_nameservice.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Code ID: $CODE_ID"

# Instantiate
echo "=== Instantiating contract ==="
INIT="{\"purchase_price\":{\"amount\":\"100\",\"denom\":\"$DENOM\"},\"transfer_price\":{\"amount\":\"999\",\"denom\":\"$DENOM\"}}"
txd tx wasm instantiate $CODE_ID "$INIT" \
    --from wallet --label "name service" -b block -y --no-admin \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get contract address
CONTRACT_ADDRESS=$(txd query wasm list-contract-by-code $CODE_ID --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Contract: $CONTRACT_ADDRESS"

# Register name
echo "=== Registering name ==="
REGISTER='{"register":{"name":"fred"}}'
txd tx wasm execute $CONTRACT_ADDRESS "$REGISTER" \
    --amount 100$DENOM --from wallet -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Query name
echo "=== Querying name ==="
NAME_QUERY='{"resolve_record": {"name": "fred"}}'
txd query wasm contract-state smart $CONTRACT_ADDRESS "$NAME_QUERY" \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

echo "✅ WASM contract deployment complete!"
Query Commands Summary
Operation	Command
List code IDs	txd query wasm list-code $TX_NODE_ARGS
Get code info	txd query wasm code-info $CODE_ID $TX_NODE_ARGS
List contracts by code	txd query wasm list-contract-by-code $CODE_ID $TX_NODE_ARGS
Query contract state	txd query wasm contract-state smart $CONTRACT_ADDRESS '$QUERY' $TX_NODE_ARGS
Get contract balance	txd query bank balances $CONTRACT_ADDRESS $TX_NODE_ARGS
Execute Commands Summary
Operation	Command
Store contract	txd tx wasm store artifacts/contract.wasm --from wallet
Instantiate	txd tx wasm instantiate $CODE_ID '$INIT' --from wallet --label "label"
Execute	txd tx wasm execute $CONTRACT_ADDRESS '$MSG' --from wallet
Migrate	txd tx wasm migrate $CONTRACT_ADDRESS $NEW_CODE_ID '{}' --from wallet
Contract Structure Reference
Nameservice Contract Messages
InstantiateMsg:

json
{
    "purchase_price": { "amount": "100", "denom": "utestcore" },
    "transfer_price": { "amount": "999", "denom": "utestcore" }
}
ExecuteMsg:

json
{ "register": { "name": "fred" } }
{ "transfer": { "name": "fred", "to": "testcore1..." } }
QueryMsg:

json
{ "resolve_record": { "name": "fred" } }
{ "config": {} }
Troubleshooting
Cargo.toml Not Found
bash
# Ensure you're in the correct directory
pwd
# Should be: .../cw-contracts/contracts/nameservice

# List contents
ls -la
# Should show Cargo.toml and src/
Out of Gas Error
bash
# Increase gas limit
txd tx wasm store artifacts/cw_nameservice.wasm \
    --from wallet --gas 500000 --gas-adjustment 1.5 ...
Insufficient Funds
bash
# Check balance
txd query bank balances $WALLET --denom $DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Fund via faucet if needed
Contract Not Found
bash
# Verify contract address
echo $CONTRACT_ADDRESS

# Check if contract exists
txd query wasm contract $CONTRACT_ADDRESS $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Next Steps
Read TX Modules Specification

Read CosmWasm Documentation

Check Smart FT with WASM tutorial

Check Asset FT Extension tutorial

