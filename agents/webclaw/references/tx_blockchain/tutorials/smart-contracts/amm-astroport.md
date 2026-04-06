# AMM (Automated Market Maker) with Astroport

Deploy a complete AMM application on TX Blockchain using Astroport, one of the most popular CosmWasm AMMs.

## Overview

This tutorial deploys a complete AMM ecosystem including:
- **CW20 Token** - AMM governance/reward token
- **Pool Contracts** - XYK and Stable pools for trading
- **Factory Contract** - Manages pool creation
- **Router Contract** - Routes trades to appropriate pools
- **Generator Contract** - Distributes rewards to liquidity providers
- **Vesting Contract** - Manages reward vesting schedules
- **Staking Contract** - Staking for fee collection
- **Maker Contract** - Collects and distributes swap fees
- **Whitelist Contract** - Manages 3rd party rewards

## Prerequisites

```bash
# Verify requirements
rustc --version && cargo --version
txd version
jq --version

# Set testnet variables
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export DENOM="utestcore"
export KEYRING_BACKEND=test

export TX_NODE_ARGS="--node=$RPC_URL"
export TX_CHAIN_ID_ARGS="--chain-id=$CHAIN_ID --keyring-backend=$KEYRING_BACKEND"
Source Code
bash
# Clone Astroport repository
git clone git@github.com:astroport-fi/astroport-core.git
cd astroport-core

# Build all optimized smart contracts
./scripts/build_release.sh
Artifacts will be in /artifacts directory.

Setup Admin Account
bash
# Generate admin wallet
RES=$(txd keys add wallet $TX_CHAIN_ID_ARGS --output json)
OWNER=$(echo $RES | jq -r '.address')
echo "Admin address: $OWNER"

# Fund via faucet at https://faucet.testnet.tx.dev

# Check balance
txd query bank balances $OWNER --denom $DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Deploy Token Contract
bash
# Deploy CW20 token contract
RES=$(txd tx wasm store artifacts/astroport_token.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_TOKEN=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Token Code ID: $CODE_ID_TOKEN"

# Instantiate AMM token
INIT='{"name":"MYAMMTOKEN", "symbol":"TOKENSYMBOL", "decimals":6, "initial_balances": [],"mint":{"minter":'\""$OWNER"\"'}}'

txd tx wasm instantiate $CODE_ID_TOKEN "$INIT" \
    --from wallet --label "mytoken" -b block -y --no-admin \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get token contract address
CONTRACT_ADDRESS_TOKEN=$(txd query wasm list-contract-by-code $CODE_ID_TOKEN \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Token Contract: $CONTRACT_ADDRESS_TOKEN"
Deploy Pool Contracts
bash
# Deploy XYK pool contract
RES=$(txd tx wasm store artifacts/astroport_pair.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_PAIR=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "XYK Pool Code ID: $CODE_ID_PAIR"

# Deploy Stable pool contract
RES=$(txd tx wasm store artifacts/astroport_pair_stable.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_PAIR_STABLE=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Stable Pool Code ID: $CODE_ID_PAIR_STABLE"
Deploy Whitelist Contract
bash
RES=$(txd tx wasm store artifacts/astroport_whitelist.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_WHITELIST=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Whitelist Code ID: $CODE_ID_WHITELIST"
Deploy Coin Registry Contract
bash
RES=$(txd tx wasm store artifacts/astroport_native_coin_registry.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_REGISTRY=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Registry Code ID: $CODE_ID_REGISTRY"

# Instantiate registry
INIT='{"owner":'\""$OWNER"\"'}'

txd tx wasm instantiate $CODE_ID_REGISTRY "$INIT" \
    --from wallet --label "registry" -b block -y --no-admin \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get registry address
CONTRACT_ADDRESS_REGISTRY=$(txd query wasm list-contract-by-code $CODE_ID_REGISTRY \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Registry Contract: $CONTRACT_ADDRESS_REGISTRY"
Deploy Factory Contract
bash
RES=$(txd tx wasm store artifacts/astroport_factory.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_FACTORY=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Factory Code ID: $CODE_ID_FACTORY"

# Instantiate factory with pool configurations
INIT='{"pair_configs":[
    {
        "code_id":'"$CODE_ID_PAIR"',
        "pair_type": {"xyk":{}},
        "total_fee_bps": 1000,
        "maker_fee_bps": 500,
        "is_disabled":false,
        "is_generator_disabled":false
    },
    {
        "code_id":'"$CODE_ID_PAIR_STABLE"',
        "pair_type": {"stable":{}},
        "total_fee_bps": 1000,
        "maker_fee_bps": 500,
        "is_disabled":false,
        "is_generator_disabled":false
    }
],
"token_code_id": '"$CODE_ID_TOKEN"',
"owner": '\""$OWNER"\"',
"whitelist_code_id": '"$CODE_ID_WHITELIST"',
"coin_registry_address": '\""$CONTRACT_ADDRESS_REGISTRY"\"'}'

txd tx wasm instantiate $CODE_ID_FACTORY "$INIT" \
    --from wallet --label "factory" -b block -y --no-admin \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get factory address
CONTRACT_ADDRESS_FACTORY=$(txd query wasm list-contract-by-code $CODE_ID_FACTORY \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Factory Contract: $CONTRACT_ADDRESS_FACTORY"
Deploy Router Contract
bash
RES=$(txd tx wasm store artifacts/astroport_router.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_ROUTER=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Router Code ID: $CODE_ID_ROUTER"

# Instantiate router
INIT='{"astroport_factory": '\""$CONTRACT_ADDRESS_FACTORY"\"'}'

txd tx wasm instantiate $CODE_ID_ROUTER "$INIT" \
    --from wallet --label "router" -b block -y --no-admin \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get router address
CONTRACT_ADDRESS_ROUTER=$(txd query wasm list-contract-by-code $CODE_ID_ROUTER \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Router Contract: $CONTRACT_ADDRESS_ROUTER"
Deploy Vesting Contract
bash
RES=$(txd tx wasm store artifacts/astroport_vesting.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_VESTING=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Vesting Code ID: $CODE_ID_VESTING"

# Instantiate vesting contract
INIT='{"owner": '\""$OWNER"\"', "vesting_token": {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}}}'

txd tx wasm instantiate $CODE_ID_VESTING "$INIT" \
    --from wallet --label "vesting" -b block -y --no-admin \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get vesting address
CONTRACT_ADDRESS_VESTING=$(txd query wasm list-contract-by-code $CODE_ID_VESTING \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Vesting Contract: $CONTRACT_ADDRESS_VESTING"
Deploy Generator Contract
bash
RES=$(txd tx wasm store artifacts/astroport_generator.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_GENERATOR=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Generator Code ID: $CODE_ID_GENERATOR"

# Instantiate generator
INIT='{"owner": '\""$OWNER"\"',
    "factory": '\""$CONTRACT_ADDRESS_FACTORY"\"',
    "astro_token": {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}},
    "tokens_per_block": "100",
    "start_block": "400000",
    "vesting_contract": '\""$CONTRACT_ADDRESS_VESTING"\"',
    "whitelist_code_id": '"$CODE_ID_WHITELIST"'}'

txd tx wasm instantiate $CODE_ID_GENERATOR "$INIT" \
    --from wallet --label "generator" -b block -y --no-admin \
    --gas auto --gas-adjustment 1.3 $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get generator address
CONTRACT_ADDRESS_GENERATOR=$(txd query wasm list-contract-by-code $CODE_ID_GENERATOR \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Generator Contract: $CONTRACT_ADDRESS_GENERATOR"
Deploy Staking Contract
bash
RES=$(txd tx wasm store artifacts/astroport_staking.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_STAKING=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Staking Code ID: $CODE_ID_STAKING"

# Instantiate staking contract
INIT='{"owner": '\""$OWNER"\"',
    "token_code_id": '"$CODE_ID_TOKEN"',
    "deposit_token_addr": '\""$CONTRACT_ADDRESS_TOKEN"\"'}'

txd tx wasm instantiate $CODE_ID_STAKING "$INIT" \
    --from wallet --label "staking" -b block -y --no-admin \
    --gas auto --gas-adjustment 1.3 $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get staking address
CONTRACT_ADDRESS_STAKING=$(txd query wasm list-contract-by-code $CODE_ID_STAKING \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Staking Contract: $CONTRACT_ADDRESS_STAKING"
Deploy Maker Contract
bash
RES=$(txd tx wasm store artifacts/astroport_maker.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID_MAKER=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Maker Code ID: $CODE_ID_MAKER"

# Instantiate maker contract
INIT='{"owner": '\""$OWNER"\"',
    "astro_token": {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}},
    "factory_contract": '\""$CONTRACT_ADDRESS_FACTORY"\"',
    "staking_contract": '\""$CONTRACT_ADDRESS_STAKING"\"'}'

txd tx wasm instantiate $CODE_ID_MAKER "$INIT" \
    --from wallet --label "maker" -b block -y --no-admin \
    --gas auto --gas-adjustment 1.3 $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get maker address
CONTRACT_ADDRESS_MAKER=$(txd query wasm list-contract-by-code $CODE_ID_MAKER \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Maker Contract: $CONTRACT_ADDRESS_MAKER"
Configure Factory Contract
bash
# Update factory with maker and generator addresses
EXEC='{"update_config": {
    "fee_address": '\""$CONTRACT_ADDRESS_MAKER"\"',
    "generator_address": '\""$CONTRACT_ADDRESS_GENERATOR"\"'
}}'

txd tx wasm execute $CONTRACT_ADDRESS_FACTORY "$EXEC" \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
AMM Interaction Examples
Create a Liquidity Pool
bash
# Create XYK pool with AMM token and native token
EXEC='{"create_pair": {
    "pair_type": {"xyk":{}},
    "asset_infos": [
        {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}},
        {"native_token": {"denom": "utestcore"}}
    ]
}}'

txd tx wasm execute $CONTRACT_ADDRESS_FACTORY "$EXEC" \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Query pool info
QUERY='{"pair": {
    "asset_infos": [
        {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}},
        {"native_token": {"denom": "utestcore"}}
    ]
}}'

RES=$(txd query wasm contract-state smart $CONTRACT_ADDRESS_FACTORY "$QUERY" \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS --output json)

CONTRACT_ADDRESS_POOL=$(echo $RES | jq -r '.data.contract_addr')
LIQUIDITY_TOKEN=$(echo $RES | jq -r '.data.liquidity_token')
echo "Pool Contract: $CONTRACT_ADDRESS_POOL"
echo "Liquidity Token: $LIQUIDITY_TOKEN"
Mint AMM Tokens
bash
# Mint tokens to admin address
EXEC='{"mint": {
    "recipient": '\""$OWNER"\"',
    "amount": "1000000000"
}}'

txd tx wasm execute $CONTRACT_ADDRESS_TOKEN "$EXEC" \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Provide Liquidity
bash
# Increase allowance for pool contract
EXEC='{"increase_allowance": {
    "spender": '\""$CONTRACT_ADDRESS_POOL"\"',
    "amount": "1000000"
}}'

txd tx wasm execute $CONTRACT_ADDRESS_TOKEN "$EXEC" \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Provide liquidity
EXEC='{"provide_liquidity": {
    "assets": [
        {
            "info": {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}},
            "amount": "1000000"
        },
        {
            "info": {"native_token": {"denom": "utestcore"}},
            "amount": "1000000"
        }
    ]
}}'

txd tx wasm execute $CONTRACT_ADDRESS_POOL "$EXEC" \
    --amount 1000000utestcore \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Query Pool State
bash
# Query pool reserves
QUERY='{"pool":{}}'
txd query wasm contract-state smart $CONTRACT_ADDRESS_POOL "$QUERY" \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Query LP token balance
QUERY='{"balance": {"address": '\""$OWNER"\"'}}'
txd query wasm contract-state smart $LIQUIDITY_TOKEN "$QUERY" \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Swap Tokens
bash
# Swap native token for AMM token
EXEC='{"swap": {
    "offer_asset": {
        "info": {"native_token": {"denom": "utestcore"}},
        "amount": "100000"
    },
    "belief_price": "1",
    "max_spread": "0.02",
    "to": '\""$OWNER"\"'
}}'

txd tx wasm execute $CONTRACT_ADDRESS_POOL "$EXEC" \
    --amount 100000utestcore \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Contract Addresses Summary
Contract	Variable	Purpose
Token	$CONTRACT_ADDRESS_TOKEN	AMM governance/reward token
Factory	$CONTRACT_ADDRESS_FACTORY	Manages pool creation
Router	$CONTRACT_ADDRESS_ROUTER	Routes trades
Generator	$CONTRACT_ADDRESS_GENERATOR	Distributes rewards
Vesting	$CONTRACT_ADDRESS_VESTING	Reward vesting
Staking	$CONTRACT_ADDRESS_STAKING	Fee staking
Maker	$CONTRACT_ADDRESS_MAKER	Fee collection
Registry	$CONTRACT_ADDRESS_REGISTRY	Coin info
Whitelist	Code ID only	3rd party rewards
Complete Setup Script
bash
#!/bin/bash
# deploy-amm.sh - Complete AMM deployment script

set -e

# Configuration
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export DENOM="utestcore"
export KEYRING_BACKEND=test

export TX_NODE_ARGS="--node=$RPC_URL"
export TX_CHAIN_ID_ARGS="--chain-id=$CHAIN_ID --keyring-backend=$KEYRING_BACKEND"

# Setup admin
echo "=== Setting up admin ==="
txd keys add wallet $TX_CHAIN_ID_ARGS 2>/dev/null || true
OWNER=$(txd keys show wallet -a $TX_CHAIN_ID_ARGS)
echo "Admin: $OWNER"

# Clone and build
echo "=== Building contracts ==="
git clone git@github.com:astroport-fi/astroport-core.git 2>/dev/null || true
cd astroport-core
./scripts/build_release.sh

# Deploy token
echo "=== Deploying token ==="
RES=$(txd tx wasm store artifacts/astroport_token.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_TOKEN=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

INIT='{"name":"MYAMMTOKEN", "symbol":"TOKENSYMBOL", "decimals":6, "initial_balances": [],"mint":{"minter":'\""$OWNER"\"'}}'
txd tx wasm instantiate $CODE_ID_TOKEN "$INIT" --from wallet --label "mytoken" -b block -y --no-admin $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

CONTRACT_ADDRESS_TOKEN=$(txd query wasm list-contract-by-code $CODE_ID_TOKEN --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Token: $CONTRACT_ADDRESS_TOKEN"

# Deploy pools
echo "=== Deploying pools ==="
RES=$(txd tx wasm store artifacts/astroport_pair.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_PAIR=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

RES=$(txd tx wasm store artifacts/astroport_pair_stable.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_PAIR_STABLE=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

# Deploy whitelist
echo "=== Deploying whitelist ==="
RES=$(txd tx wasm store artifacts/astroport_whitelist.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_WHITELIST=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

# Deploy registry
echo "=== Deploying registry ==="
RES=$(txd tx wasm store artifacts/astroport_native_coin_registry.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_REGISTRY=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

INIT='{"owner":'\""$OWNER"\"'}'
txd tx wasm instantiate $CODE_ID_REGISTRY "$INIT" --from wallet --label "registry" -b block -y --no-admin $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
CONTRACT_ADDRESS_REGISTRY=$(txd query wasm list-contract-by-code $CODE_ID_REGISTRY --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')

# Deploy factory
echo "=== Deploying factory ==="
RES=$(txd tx wasm store artifacts/astroport_factory.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_FACTORY=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

INIT='{"pair_configs":[{"code_id":'"$CODE_ID_PAIR"',"pair_type":{"xyk":{}},"total_fee_bps":1000,"maker_fee_bps":500,"is_disabled":false,"is_generator_disabled":false},{"code_id":'"$CODE_ID_PAIR_STABLE"',"pair_type":{"stable":{}},"total_fee_bps":1000,"maker_fee_bps":500,"is_disabled":false,"is_generator_disabled":false}],"token_code_id":'"$CODE_ID_TOKEN"',"owner":'\""$OWNER"\"',"whitelist_code_id":'"$CODE_ID_WHITELIST"',"coin_registry_address":'\""$CONTRACT_ADDRESS_REGISTRY"\"'}'
txd tx wasm instantiate $CODE_ID_FACTORY "$INIT" --from wallet --label "factory" -b block -y --no-admin $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
CONTRACT_ADDRESS_FACTORY=$(txd query wasm list-contract-by-code $CODE_ID_FACTORY --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')

# Deploy router
echo "=== Deploying router ==="
RES=$(txd tx wasm store artifacts/astroport_router.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_ROUTER=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

INIT='{"astroport_factory": '\""$CONTRACT_ADDRESS_FACTORY"\"'}'
txd tx wasm instantiate $CODE_ID_ROUTER "$INIT" --from wallet --label "router" -b block -y --no-admin $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
CONTRACT_ADDRESS_ROUTER=$(txd query wasm list-contract-by-code $CODE_ID_ROUTER --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')

# Deploy vesting
echo "=== Deploying vesting ==="
RES=$(txd tx wasm store artifacts/astroport_vesting.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_VESTING=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

INIT='{"owner": '\""$OWNER"\"', "vesting_token": {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}}}'
txd tx wasm instantiate $CODE_ID_VESTING "$INIT" --from wallet --label "vesting" -b block -y --no-admin $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
CONTRACT_ADDRESS_VESTING=$(txd query wasm list-contract-by-code $CODE_ID_VESTING --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')

# Deploy generator
echo "=== Deploying generator ==="
RES=$(txd tx wasm store artifacts/astroport_generator.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_GENERATOR=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

INIT='{"owner": '\""$OWNER"\"',"factory": '\""$CONTRACT_ADDRESS_FACTORY"\"',"astro_token": {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}},"tokens_per_block": "100","start_block": "400000","vesting_contract": '\""$CONTRACT_ADDRESS_VESTING"\"',"whitelist_code_id": '"$CODE_ID_WHITELIST"'}'
txd tx wasm instantiate $CODE_ID_GENERATOR "$INIT" --from wallet --label "generator" -b block -y --no-admin --gas auto --gas-adjustment 1.3 $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
CONTRACT_ADDRESS_GENERATOR=$(txd query wasm list-contract-by-code $CODE_ID_GENERATOR --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')

# Deploy staking
echo "=== Deploying staking ==="
RES=$(txd tx wasm store artifacts/astroport_staking.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_STAKING=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

INIT='{"owner": '\""$OWNER"\"',"token_code_id": '"$CODE_ID_TOKEN"',"deposit_token_addr": '\""$CONTRACT_ADDRESS_TOKEN"\"'}'
txd tx wasm instantiate $CODE_ID_STAKING "$INIT" --from wallet --label "staking" -b block -y --no-admin --gas auto --gas-adjustment 1.3 $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
CONTRACT_ADDRESS_STAKING=$(txd query wasm list-contract-by-code $CODE_ID_STAKING --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')

# Deploy maker
echo "=== Deploying maker ==="
RES=$(txd tx wasm store artifacts/astroport_maker.wasm --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID_MAKER=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

INIT='{"owner": '\""$OWNER"\"',"astro_token": {"token": {"contract_addr":'\""$CONTRACT_ADDRESS_TOKEN"\"'}},"factory_contract": '\""$CONTRACT_ADDRESS_FACTORY"\"',"staking_contract": '\""$CONTRACT_ADDRESS_STAKING"\"'}'
txd tx wasm instantiate $CODE_ID_MAKER "$INIT" --from wallet --label "maker" -b block -y --no-admin --gas auto --gas-adjustment 1.3 $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
CONTRACT_ADDRESS_MAKER=$(txd query wasm list-contract-by-code $CODE_ID_MAKER --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')

# Update factory
echo "=== Configuring factory ==="
EXEC='{"update_config": {"fee_address": '\""$CONTRACT_ADDRESS_MAKER"\"', "generator_address": '\""$CONTRACT_ADDRESS_GENERATOR"\"'}}'
txd tx wasm execute $CONTRACT_ADDRESS_FACTORY "$EXEC" --from wallet --gas auto --gas-adjustment 1.3 -y -b block $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

echo "✅ AMM deployment complete!"
echo "Factory: $CONTRACT_ADDRESS_FACTORY"
echo "Router: $CONTRACT_ADDRESS_ROUTER"
echo "Token: $CONTRACT_ADDRESS_TOKEN"
Next Steps
Read Astroport Documentation

Read TX Modules Specification

Check Smart FT with WASM

Explore Deploy First WASM Contract
