# Smart FT with WASM

Develop, deploy, and use WASM fungible smart tokens with airdrop functionality.

## Overview

This tutorial creates a smart contract that:
- Issues a fungible token (FT) with minting feature
- Implements 10% send commission rate
- Provides airdrop functionality
- Allows owner to mint additional tokens for airdrops
- Users can claim airdrops by calling the contract

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
git clone https://github.com/tokenize-x/tx-tutorials.git
cd tx-tutorials/tutorials/wasm/ft-airdrop
Setup Account
bash
# Create deployer account
txd keys add wasm-deployer $TX_CHAIN_ID_ARGS

# Fund via faucet at https://faucet.testnet.tx.dev

# Check balance
txd query bank balances $(txd keys show wasm-deployer -a $TX_CHAIN_ID_ARGS) \
    --denom $DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Build Contract
bash
# Build WASM using CosmWASM optimizer
docker run --rm -v "$(pwd)":/code \
  --mount type=volume,source="$(basename "$(pwd)")_cache",target=/target \
  --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
  cosmwasm/optimizer:0.15.0
Deploy Contract
bash
# Store contract on chain
RES=$(txd tx wasm store artifacts/ft_airdrop.wasm \
    --from wasm-deployer --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Code ID: $CODE_ID"

# Verify deployment
txd query wasm code-info $CODE_ID $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Contract Structure
Instantiate Message
rust
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct InstantiateMsg {
    pub symbol: String,
    pub subunit: String,
    pub precision: u32,
    pub initial_amount: Uint128,
    pub airdrop_amount: Uint128,
}
Instantiate Function
rust
#[entry_point]
pub fn instantiate(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    msg: InstantiateMsg,
) -> Result<Response<CoreumMsg>, ContractError> {
    let issue_msg = CoreumMsg::AssetFT(assetft::Msg::Issue {
        symbol: msg.symbol,
        subunit: msg.subunit.clone(),
        precision: msg.precision,
        initial_amount: msg.initial_amount,
        description: None,
        features: Some(vec![0]), // 0 = minting feature
        burn_rate: Some("0".into()),
        send_commission_rate: Some("0.1".into()), // 10% commission
    });

    let denom = format!("{}-{}", msg.subunit, env.contract.address).to_lowercase();

    let state = State {
        owner: info.sender.into(),
        denom,
        minted_for_airdrop: msg.initial_amount,
        airdrop_amount: msg.airdrop_amount,
    };
    STATE.save(deps.storage, &state)?;

    Ok(Response::new()
        .add_attribute("owner", state.owner)
        .add_attribute("denom", state.denom)
        .add_message(issue_msg))
}
Instantiate Contract
bash
SUBUNIT=mysubunit

txd tx wasm instantiate $CODE_ID \
    "{\"symbol\":\"mysymbol\",\"subunit\":\"$SUBUNIT\",\"precision\":6,\"initial_amount\":\"1000000000\",\"airdrop_amount\":\"1000000\"}" \
    --amount="10000000$DENOM" \
    --no-admin \
    --label "My smart token" \
    --from wasm-deployer \
    --gas auto --gas-adjustment 1.3 -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Parameter Explanation:

Parameter	Value	Description
symbol	"mysymbol"	Token display symbol
subunit	"mysubunit"	On-chain denomination
precision	6	Decimal places
initial_amount	1000000000	Initial supply
airdrop_amount	1000000	Amount per airdrop
--amount	10000000utestcore	Funds for contract to mint tokens
Get Contract Address
bash
# List contracts by code ID
txd query wasm list-contract-by-code $CODE_ID --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

CONTRACT_ADDRESS=$(txd query wasm list-contract-by-code $CODE_ID --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Contract address: $CONTRACT_ADDRESS"

# Build token denom
FT_DENOM="$SUBUNIT-$CONTRACT_ADDRESS"
echo "Created denom: $FT_DENOM"

# Verify on explorer
echo "https://explorer.testnet.tx.dev/accounts/$CONTRACT_ADDRESS"
Query Token Info
bash
# Check total supply
txd query bank total --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Check denom metadata
txd query bank denom-metadata --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Check FT token details
txd query assetft token $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Execute Messages
Execute Message Structure
rust
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ExecuteMsg {
    MintForAirdrop { amount: u128 },
    ReceiveAirdrop {},
}
Receive Airdrop
rust
fn receive_airdrop(deps: DepsMut, info: MessageInfo) -> Result<Response<CoreumMsg>, ContractError> {
    let mut state = STATE.load(deps.storage)?;
    
    if state.minted_for_airdrop < state.airdrop_amount {
        return Err(ContractError::CustomError {
            val: "not enough minted".into(),
        });
    }
    
    let send_msg = cosmwasm_std::BankMsg::Send {
        to_address: info.sender.into(),
        amount: vec![Coin {
            amount: state.airdrop_amount,
            denom: state.denom.clone(),
        }],
    };

    state.minted_for_airdrop = state.minted_for_airdrop - state.airdrop_amount;
    STATE.save(deps.storage, &state)?;

    Ok(Response::new()
        .add_attribute("method", "receive_airdrop")
        .add_attribute("denom", state.denom)
        .add_attribute("amount", state.airdrop_amount.to_string())
        .add_message(send_msg))
}
Claim Airdrop:

bash
txd tx wasm execute $CONTRACT_ADDRESS '{"receive_airdrop":{}}' \
    --from wasm-deployer -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Check Balance After Airdrop
bash
txd query bank balances $(txd keys show wasm-deployer -a $TX_CHAIN_ID_ARGS) \
    --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Query Contract State
Query Message Structure
rust
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum QueryMsg {
    Token {},
    MintedForAirdrop {},
}
Query Remaining Airdrop Amount
rust
fn minted_for_airdrop(deps: Deps<CoreumQueries>) -> StdResult<Binary> {
    let state = STATE.load(deps.storage)?;
    let res = AmountResponse {
        amount: state.minted_for_airdrop,
    };
    to_binary(&res)
}
Query Command:

bash
txd query wasm contract-state smart $CONTRACT_ADDRESS '{"minted_for_airdrop": {}}' \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Mint More for Airdrop
Mint Function
rust
fn mint_for_airdrop(
    deps: DepsMut,
    info: MessageInfo,
    amount: u128,
) -> Result<Response<CoreumMsg>, ContractError> {
    let mut state = STATE.load(deps.storage)?;
    
    // Only owner can mint
    if info.sender != state.owner {
        return Err(ContractError::Unauthorized {});
    }

    let msg = CoreumMsg::AssetFT(assetft::Msg::Mint {
        coin: Coin::new(amount, state.denom.clone()),
    });

    state.minted_for_airdrop = state.minted_for_airdrop + Uint128::new(amount);
    STATE.save(deps.storage, &state)?;

    Ok(Response::new()
        .add_attribute("method", "mint_for_airdrop")
        .add_attribute("denom", state.denom)
        .add_attribute("amount", amount.to_string())
        .add_message(msg))
}
Mint More Tokens:

bash
txd tx wasm execute $CONTRACT_ADDRESS \
    "{\"mint_for_airdrop\":{\"amount\":\"5000000\"}}" \
    --from wasm-deployer -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Verify Updated Airdrop Amount:

bash
txd query wasm contract-state smart $CONTRACT_ADDRESS '{"minted_for_airdrop": {}}' \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Send Commission Rate Demo
The contract has a 10% send commission rate. When tokens are sent, 10% goes to the contract (admin).

Create Recipient Account
bash
txd keys add recipient $TX_CHAIN_ID_ARGS
Check Initial Balances
bash
# Deployer balance
echo "Deployer balance:"
txd query bank balances $(txd keys show wasm-deployer -a $TX_CHAIN_ID_ARGS) \
    --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Contract balance
echo "Contract balance:"
txd query bank balances $CONTRACT_ADDRESS \
    --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Send Tokens
bash
txd tx bank send $(txd keys show wasm-deployer -a $TX_CHAIN_ID_ARGS) \
    $(txd keys show recipient -a $TX_CHAIN_ID_ARGS) \
    1000$FT_DENOM \
    --from wasm-deployer -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Check Balances After Send
bash
# Recipient received 1000 tokens
echo "Recipient balance:"
txd query bank balances $(txd keys show recipient -a $TX_CHAIN_ID_ARGS) \
    --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Deployer sent 1000 + 10% commission (100 tokens to contract)
echo "Deployer balance:"
txd query bank balances $(txd keys show wasm-deployer -a $TX_CHAIN_ID_ARGS) \
    --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Contract received 10% commission
echo "Contract balance:"
txd query bank balances $CONTRACT_ADDRESS \
    --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Complete Example Script
bash
#!/bin/bash
# smart-ft-wasm-demo.sh - Complete Smart FT WASM demo

set -e

# Configuration
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export DENOM="utestcore"
export KEYRING_BACKEND=test
export TX_NODE_ARGS="--node=$RPC_URL"
export TX_CHAIN_ID_ARGS="--chain-id=$CHAIN_ID --keyring-backend=$KEYRING_BACKEND"

# Setup account
echo "=== Setting up account ==="
txd keys add wasm-deployer $TX_CHAIN_ID_ARGS 2>/dev/null || true
DEPLOYER=$(txd keys show wasm-deployer -a $TX_CHAIN_ID_ARGS)
echo "Deployer: $DEPLOYER"

# Check balance
echo "Checking balance..."
txd query bank balances $DEPLOYER --denom $DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Build contract
echo "=== Building contract ==="
cd tx-tutorials/tutorials/wasm/ft-airdrop
docker run --rm -v "$(pwd)":/code \
    --mount type=volume,source="$(basename "$(pwd)")_cache",target=/target \
    --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
    cosmwasm/optimizer:0.15.0

# Deploy
echo "=== Deploying contract ==="
RES=$(txd tx wasm store artifacts/ft_airdrop.wasm \
    --from wasm-deployer --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Code ID: $CODE_ID"

# Instantiate
echo "=== Instantiating contract ==="
SUBUNIT="mysubunit"
txd tx wasm instantiate $CODE_ID \
    "{\"symbol\":\"mysymbol\",\"subunit\":\"$SUBUNIT\",\"precision\":6,\"initial_amount\":\"1000000000\",\"airdrop_amount\":\"1000000\"}" \
    --amount="10000000$DENOM" \
    --no-admin \
    --label "My smart token" \
    --from wasm-deployer \
    --gas auto --gas-adjustment 1.3 -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Get contract address
CONTRACT_ADDRESS=$(txd query wasm list-contract-by-code $CODE_ID --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Contract: $CONTRACT_ADDRESS"

FT_DENOM="$SUBUNIT-$CONTRACT_ADDRESS"
echo "Token Denom: $FT_DENOM"

# Claim airdrop
echo "=== Claiming airdrop ==="
txd tx wasm execute $CONTRACT_ADDRESS '{"receive_airdrop":{}}' \
    --from wasm-deployer -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Check balance
echo "=== Final balance ==="
txd query bank balances $DEPLOYER --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

echo "✅ Smart FT WASM demo complete!"
Query Methods Summary
Query	Command
Minted for airdrop	txd query wasm contract-state smart $CONTRACT_ADDRESS '{"minted_for_airdrop": {}}'
Token info	txd query assetft token $FT_DENOM
Contract balance	txd query bank balances $CONTRACT_ADDRESS --denom $FT_DENOM
Execute Methods Summary
Method	Command
Receive airdrop	txd tx wasm execute $CONTRACT_ADDRESS '{"receive_airdrop":{}}'
Mint for airdrop	txd tx wasm execute $CONTRACT_ADDRESS '{"mint_for_airdrop":{"amount":"5000000"}}'
Next Steps
Read TX Modules Specification

Read CosmWasm Documentation

Check Asset FT Extension tutorial

Explore other tutorials

Troubleshooting
Insufficient Funds Error
bash
# Ensure contract has funds for minting
txd query bank balances $CONTRACT_ADDRESS --denom $DENOM
Unauthorized Error
bash
# Only the contract owner (wasm-deployer) can mint
# Verify you're using the correct account
txd keys list
Not Enough Minted Error
bash
# Mint more tokens before claiming airdrop
txd tx wasm execute $CONTRACT_ADDRESS '{"mint_for_airdrop":{"amount":"10000000"}}'
