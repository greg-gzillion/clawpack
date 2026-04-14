# Asset FT Extension Tutorial

Develop, deploy, and use WASM contracts as fungible smart token extensions.

## Overview

Asset FT Extensions add custom logic to token transfers using CosmWasm. Every transfer is intercepted by the contract, which can:
- Modify transfer behavior
- Apply custom fees
- Implement complex whitelisting
- Burn or mint tokens conditionally
- Reject transfers based on rules
- Integrate with IBC
- Block smart contract transfers

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
cd tx-tutorials/tutorials/wasm/extension
Branches: extension/simple, extension/reject, extension/whitelist, extension/send-commission-rate, extension/burn-rate, extension/block-smart-contract, extension/ibc

Setup Accounts
bash
# Create accounts
txd keys add ft-admin $TX_CHAIN_ID_ARGS
txd keys add ft-receiver-1 $TX_CHAIN_ID_ARGS
txd keys add ft-receiver-2 $TX_CHAIN_ID_ARGS

# Fund via faucet at https://faucet.testnet.tx.dev

# Export addresses
export FT_ADMIN=$(txd keys show ft-admin --address $TX_CHAIN_ID_ARGS)
export FT_RECEIVER_1=$(txd keys show ft-receiver-1 --address $TX_CHAIN_ID_ARGS)
export FT_RECEIVER_2=$(txd keys show ft-receiver-2 --address $TX_CHAIN_ID_ARGS)

# Check balance
txd query bank balances $FT_ADMIN --denom $DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Build and Deploy Contract
bash
# Build WASM
docker run --rm -v "$(pwd)":/code \
  --mount type=volume,source="$(basename "$(pwd)")_cache",target=/target \
  --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
  cosmwasm/optimizer:0.15.0

# Store contract
RES=$(txd tx wasm store artifacts/extension.wasm \
    --from $FT_ADMIN --gas auto --gas-adjustment 1.4 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Code ID: $CODE_ID"

# Verify
txd query wasm code-info $CODE_ID $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Issue Token with Extension
bash
# Issue FT with extension
txd tx assetft issue MYFT cmyft 2 100000000 "My FT token with extension" \
    --from $FT_ADMIN \
    --features=burning,freezing,minting,whitelisting,extension \
    --burn-rate=0.02 \
    --send-commission-rate=0.03 \
    --extension_code_id=$CODE_ID \
    --extension_label=my-extension \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS \
    -y -b block --gas auto --gas-adjustment 1.4

# Get token info
export FT_DENOM=cmyft-$FT_ADMIN
echo "Token Denom: $FT_DENOM"

# Get extension address
RES=$(txd query assetft token $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS --output json)
EXTENSION_ADDR=$(echo $RES | jq -r '.token.extension_cw_address')
echo "Extension Address: $EXTENSION_ADDR"
Extension Parameters
Parameter	Description
--extension_code_id	Code ID of deployed WASM contract
--extension_label	Optional label for extension
--extension_funds	Funds to transfer on instantiation
--extension_issuance_msg	JSON data passed to WASM
Extension Transfer Flow
When Alice sends tokens to Bob:

Tokens transfer to extension contract

Contract sudo entrypoint called with ExtensionTransfer

Contract decides action

Sudo Message Structure
rust
#[entry_point]
pub fn sudo(deps: DepsMut<CoreumQueries>, env: Env, msg: SudoMsg) -> CoreumResult<ContractError> {
    match msg {
        SudoMsg::ExtensionTransfer {
            sender, recipient, transfer_amount, commission_amount, burn_amount, context,
        } => sudo_extension_transfer(
            deps, env, transfer_amount, sender, recipient, 
            commission_amount, burn_amount, context,
        ),
    }
}
Example 1: Keep Tokens (No Forward)
rust
pub fn sudo_extension_transfer(
    _deps: DepsMut<CoreumQueries>,
    _env: Env,
    _amount: Uint128,
    _sender: String,
    _recipient: String,
    _commission_amount: Uint128,
    _burn_amount: Uint128,
    _context: TransferContext,
) -> CoreumResult<ContractError> {
    Ok(Response::new())  // Tokens stay in extension
}
Test:

bash
txd tx bank send $FT_ADMIN $FT_RECEIVER_1 10$FT_DENOM -y -b block $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
txd query bank balances $EXTENSION_ADDR --denom $FT_DENOM $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Example 2: Forward to Recipient
rust
pub fn sudo_extension_transfer(
    deps: DepsMut<CoreumQueries>,
    _env: Env,
    amount: Uint128,
    _sender: String,
    recipient: String,
    _commission_amount: Uint128,
    _burn_amount: Uint128,
    _context: TransferContext,
) -> CoreumResult<ContractError> {
    let denom = DENOM.load(deps.storage)?;

    let transfer_msg = cosmwasm_std::BankMsg::Send {
        to_address: recipient,
        amount: vec![Coin { amount, denom }],
    };

    Ok(Response::new()
        .add_attribute("method", "execute_transfer")
        .add_message(transfer_msg))
}
Update contract:

bash
# Rebuild
docker run --rm -v "$(pwd)":/code \
    --mount type=volume,source="$(basename "$(pwd)")_cache",target=/target \
    --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
    cosmwasm/optimizer:0.15.0

# Store new version
RES=$(txd tx wasm store artifacts/extension.wasm \
    --from $FT_ADMIN --gas auto --gas-adjustment 1.4 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

# Migrate
txd tx wasm migrate $EXTENSION_ADDR $CODE_ID '{}' \
    --from $FT_ADMIN -y -b block $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Example 3: Reject Specific Amounts
rust
pub fn sudo_extension_transfer(
    deps: DepsMut<CoreumQueries>,
    _env: Env,
    amount: Uint128,
    _sender: String,
    recipient: String,
    _commission_amount: Uint128,
    _burn_amount: Uint128,
    _context: TransferContext,
) -> CoreumResult<ContractError> {
    let denom = DENOM.load(deps.storage)?;

    if amount == Uint128::new(7) {
        return Err(ContractError::Std(StdError::generic_err("7 is not allowed")));
    }

    let transfer_msg = cosmwasm_std::BankMsg::Send {
        to_address: recipient,
        amount: vec![Coin { amount, denom }],
    };

    Ok(Response::new()
        .add_attribute("method", "execute_transfer")
        .add_message(transfer_msg))
}
Test rejection:

bash
txd tx bank send $FT_ADMIN $FT_RECEIVER_1 7$FT_DENOM -y -b block $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
# Error: 7 is not allowed
Example 4: Custom Whitelisting
rust
pub struct IssuanceMsg {
    pub parent_denom: Option<String>,
}

pub fn sudo_extension_transfer(
    deps: DepsMut<CoreumQueries>,
    _env: Env,
    amount: Uint128,
    _sender: String,
    recipient: String,
    _commission_amount: Uint128,
    _burn_amount: Uint128,
    _context: TransferContext,
) -> CoreumResult<ContractError> {
    let denom = DENOM.load(deps.storage)?;
    let token = query_token(deps.as_ref(), &denom)?;

    if let Some(features) = &token.features {
        if features.contains(&assetft::WHITELISTING) {
            assert_whitelisting(deps.as_ref(), &recipient, &token.denom, amount)?;
        }
    }

    let transfer_msg = cosmwasm_std::BankMsg::Send {
        to_address: recipient,
        amount: vec![Coin { amount, denom }],
    };

    Ok(Response::new()
        .add_attribute("method", "execute_transfer")
        .add_message(transfer_msg))
}

fn assert_whitelisting(
    deps: Deps<CoreumQueries>,
    account: &str,
    denom: &str,
    amount: Uint128,
) -> Result<(), ContractError> {
    let parent_denom = PARENT_DENOM.load(deps.storage).unwrap_or_default();
    
    // Check parent token whitelist first
    if !parent_denom.is_empty() {
        let whitelisted = query_whitelisted_balance(deps, account, &parent_denom)?;
        if whitelisted.amount.gt(&Uint128::zero()) {
            return Ok(());
        }
    }

    let bank_balance = query_bank_balance(deps, account, denom)?;
    let whitelisted_balance = query_whitelisted_balance(deps, account, denom)?;

    if amount + bank_balance.amount > whitelisted_balance.amount {
        return Err(ContractError::WhitelistingError {});
    }

    Ok(())
}
Issue second token with parent reference:

bash
txd tx assetft issue MYFT2 cmyft2 2 1000000 "Second FT token" \
    --from $FT_ADMIN \
    --features=whitelisting,extension \
    --extension_code_id=$CODE_ID \
    --extension_issuance_msg='{"parent_denom": "'$FT_DENOM'"}' \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS -y -b block --gas auto --gas-adjustment 1.4
Example 5: Split Commission
rust
pub fn sudo_extension_transfer(
    deps: DepsMut<CoreumQueries>,
    _env: Env,
    amount: Uint128,
    _sender: String,
    recipient: String,
    commission_amount: Uint128,
    _burn_amount: Uint128,
    _context: TransferContext,
) -> CoreumResult<ContractError> {
    let denom = DENOM.load(deps.storage)?;
    let token = query_token(deps.as_ref(), &denom)?;

    let transfer_msg = cosmwasm_std::BankMsg::Send {
        to_address: recipient,
        amount: vec![Coin { amount, denom: denom.clone() }],
    };

    let mut response = Response::new()
        .add_attribute("method", "execute_transfer")
        .add_message(transfer_msg);

    if !commission_amount.is_zero() {
        if let Some(admin) = &token.admin {
            let admin_commission = commission_amount.div(Uint128::new(2));
            let admin_msg = cosmwasm_std::BankMsg::Send {
                to_address: admin.to_string(),
                amount: vec![Coin { amount: admin_commission, denom }],
            };
            response = response
                .add_attribute("admin_commission", admin_commission.to_string())
                .add_message(admin_msg);
        }
    }

    Ok(response)
}
Example 6: Dynamic Burn Rate
rust
pub fn sudo_extension_transfer(
    deps: DepsMut<CoreumQueries>,
    _env: Env,
    amount: Uint128,
    sender: String,
    recipient: String,
    _commission_amount: Uint128,
    burn_amount: Uint128,
    _context: TransferContext,
) -> CoreumResult<ContractError> {
    let denom = DENOM.load(deps.storage)?;
    let token = query_token(deps.as_ref(), &denom)?;

    let transfer_msg = cosmwasm_std::BankMsg::Send {
        to_address: recipient,
        amount: vec![Coin { amount: amount.clone(), denom: denom.clone() }],
    };

    let mut response = Response::new()
        .add_attribute("method", "execute_transfer")
        .add_message(transfer_msg);

    if !burn_amount.is_zero() {
        // Dynamic burn based on amount
        let new_burn = match amount.u128() {
            0..=200 => burn_amount,
            201..=400 => burn_amount.div(Uint128::new(2)),
            _ => burn_amount.div(Uint128::new(5)),
        };

        let burn_msg = CoreumMsg::AssetFT(assetft::Msg::Burn {
            coin: cosmwasm_std::coin(new_burn.u128(), &token.denom),
        });
        response = response.add_message(burn_msg);

        // Refund excess
        if new_burn < burn_amount {
            let refund = burn_amount - new_burn;
            let refund_msg = cosmwasm_std::BankMsg::Send {
                to_address: sender,
                amount: vec![Coin { amount: refund, denom }],
            };
            response = response.add_message(refund_msg);
        }
    }

    Ok(response)
}
Example 7: Block Smart Contract Transfers
rust
pub fn sudo_extension_transfer(
    deps: DepsMut<CoreumQueries>,
    _env: Env,
    amount: Uint128,
    _sender: String,
    recipient: String,
    _commission_amount: Uint128,
    _burn_amount: Uint128,
    context: TransferContext,
) -> CoreumResult<ContractError> {
    let denom = DENOM.load(deps.storage)?;
    let token = query_token(deps.as_ref(), &denom)?;

    // Allow only this extension contract
    if Some(recipient.clone()) != token.extension_cw_address {
        if context.recipient_is_smart_contract {
            return Err(ContractError::SmartContractBlocked {});
        }
    }

    let transfer_msg = cosmwasm_std::BankMsg::Send {
        to_address: recipient,
        amount: vec![Coin { amount, denom }],
    };

    Ok(Response::new()
        .add_attribute("method", "execute_transfer")
        .add_message(transfer_msg))
}
Example 8: IBC Transfer Restrictions
rust
pub fn sudo_extension_transfer(
    deps: DepsMut<CoreumQueries>,
    _env: Env,
    amount: Uint128,
    _sender: String,
    recipient: String,
    _commission_amount: Uint128,
    _burn_amount: Uint128,
    context: TransferContext,
) -> CoreumResult<ContractError> {
    let denom = DENOM.load(deps.storage)?;

    // Block IBC outgoing transfers over 100 tokens
    if matches!(context.ibc_purpose, IBCPurpose::Out) && amount > Uint128::new(100) {
        return Err(ContractError::IBCDisabled {});
    }

    let transfer_msg = cosmwasm_std::BankMsg::Send {
        to_address: recipient,
        amount: vec![Coin { amount, denom }],
    };

    Ok(Response::new()
        .add_attribute("method", "execute_transfer")
        .add_message(transfer_msg))
}
Limitations
A token cannot have extension feature together with:

IBC feature

Block smart contract feature

The extension already handles these scenarios.

Next Steps
Read TX Modules Specification

Read CosmWasm Documentation

Explore other tutorials

Quick Reference
Operation	Command
Build contract	docker run ... cosmwasm/optimizer:0.15.0
Store contract	txd tx wasm store artifacts/extension.wasm --from $FT_ADMIN
Issue with extension	txd tx assetft issue ... --features=extension --extension_code_id=$CODE_ID
Migrate extension	txd tx wasm migrate $EXTENSION_ADDR $CODE_ID '{}' --from $FT_ADMIN
Query extension	txd query assetft token $FT_DENOM
