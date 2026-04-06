# TX WASM SDK

TX WASM SDK contains Rust data types for WASM smart contracts interacting with TX Blockchain, enabling issuance and execution of on-chain messages for Smart Tokens.

## Overview

The TX WASM SDK provides:
- Rust data types for CosmWasm contracts
- Generated protobuf types for chain compatibility
- Smart Token message support (AssetFT, AssetNFT)
- Integration with tx-test-tube for testing
- gRPC support for Rust clients

## Proto Types Generation

Proto types are generated using [tx-rust-protobuf](https://github.com/tokenize-x/tx-rust-protobuf) based on the current chain version.

### Generate Protobuf Types

```bash
# Clone the repository
git clone https://github.com/tokenize-x/tx-rust-protobuf.git
cd tx-rust-protobuf

# Generate protobuf types for specific chain version
./generate.sh --version v6.1.0

# Output will be in ./src directory
Generated Types Include
assetft.rs - Fungible Token messages

assetnft.rs - Non-Fungible Token messages

bank.rs - Bank module messages

staking.rs - Staking module messages

wasm.rs - WASM module messages

feemodel.rs - Fee model queries

Dependencies
Add to your Cargo.toml:

toml
[dependencies]
cosmwasm-std = "1.5.0"
cosmwasm-schema = "1.5.0"
cw-storage-plus = "1.2.0"
schemars = "0.8"
serde = { version = "1.0", default-features = false, features = ["derive"] }
thiserror = { version = "1.0" }

# TX WASM SDK (generated protobuf types)
tx-wasm-sdk = { git = "https://github.com/tokenize-x/tx-wasm-sdk", tag = "v1.0.0" }
Using AssetFT Messages
Issue Fungible Token
rust
use cosmwasm_std::{DepsMut, Env, MessageInfo, Response, Uint128};
use tx_wasm_sdk::assetft::{MsgIssue, Feature};

pub fn issue_token(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    symbol: String,
    subunit: String,
    precision: u32,
    initial_amount: Uint128,
    features: Vec<Feature>,
) -> Result<Response, ContractError> {
    
    let issue_msg = MsgIssue {
        issuer: info.sender.to_string(),
        symbol,
        subunit,
        precision,
        initial_amount,
        description: Some("My FT token".to_string()),
        features: Some(features.iter().map(|f| *f as i32).collect()),
        burn_rate: Some("0.02".to_string()),
        send_commission_rate: Some("0.03".to_string()),
        uri: None,
        uri_hash: None,
    };
    
    let response = Response::new()
        .add_attribute("action", "issue_token")
        .add_attribute("issuer", issue_msg.issuer)
        .add_attribute("symbol", issue_msg.symbol);
    
    Ok(response)
}
Mint Tokens
rust
use tx_wasm_sdk::assetft::MsgMint;
use cosmwasm_std::Coin;

pub fn mint_tokens(
    sender: String,
    denom: String,
    amount: Uint128,
) -> MsgMint {
    MsgMint {
        sender,
        coin: Some(Coin {
            denom,
            amount: amount.into(),
        }),
    }
}
Burn Tokens
rust
use tx_wasm_sdk::assetft::MsgBurn;

pub fn burn_tokens(
    sender: String,
    denom: String,
    amount: Uint128,
) -> MsgBurn {
    MsgBurn {
        sender,
        coin: Some(Coin {
            denom,
            amount: amount.into(),
        }),
    }
}
Freeze Tokens
rust
use tx_wasm_sdk::assetft::MsgFreeze;

pub fn freeze_account(
    sender: String,
    account: String,
    denom: String,
    amount: Uint128,
) -> MsgFreeze {
    MsgFreeze {
        sender,
        account,
        coin: Some(Coin {
            denom,
            amount: amount.into(),
        }),
    }
}
Transfer Admin
rust
use tx_wasm_sdk::assetft::MsgTransferAdmin;

pub fn transfer_admin(
    sender: String,
    account: String,
    denom: String,
) -> MsgTransferAdmin {
    MsgTransferAdmin {
        sender,
        account,
        denom,
    }
}
Using AssetNFT Messages
Issue NFT Class
rust
use tx_wasm_sdk::assetnft::{MsgIssueClass, ClassFeature};

pub fn issue_nft_class(
    issuer: String,
    symbol: String,
    name: String,
    description: String,
    features: Vec<ClassFeature>,
) -> MsgIssueClass {
    MsgIssueClass {
        issuer,
        symbol,
        name,
        description,
        uri: None,
        uri_hash: None,
        data: None,
        features: Some(features.iter().map(|f| *f as i32).collect()),
        royalty_rate: Some("0.05".to_string()),
    }
}
Mint NFT
rust
use tx_wasm_sdk::assetnft::MsgMint;
use cosmwasm_std::Binary;

pub fn mint_nft(
    sender: String,
    class_id: String,
    id: String,
    uri: String,
    uri_hash: String,
    data: Option<Binary>,
) -> MsgMint {
    MsgMint {
        sender,
        class_id,
        id,
        uri: Some(uri),
        uri_hash: Some(uri_hash),
        recipient: None,  // Defaults to sender
        data,
    }
}
Send NFT
rust
use tx_wasm_sdk::nft::MsgSend;

pub fn send_nft(
    sender: String,
    receiver: String,
    class_id: String,
    id: String,
) -> MsgSend {
    MsgSend {
        sender,
        receiver,
        class_id,
        id,
    }
}
Complete Smart Contract Example
rust
// contract.rs
use cosmwasm_std::{
    to_binary, Binary, Deps, DepsMut, Env, MessageInfo, Response, 
    StdResult, Uint128, Coin
};
use cosmwasm_schema::{cw_serde, QueryResponses};
use tx_wasm_sdk::assetft::{MsgIssue, MsgMint, MsgBurn, Feature};
use tx_wasm_sdk::CoreumMsg;

#[cw_serde]
pub struct InstantiateMsg {
    pub token_symbol: String,
    pub token_subunit: String,
    pub token_precision: u32,
    pub initial_supply: Uint128,
}

#[cw_serde]
pub enum ExecuteMsg {
    Mint { amount: Uint128 },
    Burn { amount: Uint128 },
    Transfer { to: String, amount: Uint128 },
}

#[cw_serde]
#[derive(QueryResponses)]
pub enum QueryMsg {
    #[returns(TokenInfoResponse)]
    TokenInfo {},
    #[returns(BalanceResponse)]
    Balance { address: String },
}

#[cw_serde]
pub struct TokenInfoResponse {
    pub denom: String,
    pub symbol: String,
    pub precision: u32,
    pub admin: String,
}

#[cw_serde]
pub struct BalanceResponse {
    pub balance: Uint128,
}

pub struct Contract;

#[entry_point]
pub fn instantiate(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    msg: InstantiateMsg,
) -> Result<Response<CoreumMsg>, ContractError> {
    // Store contract state
    let denom = format!("{}-{}", msg.token_subunit, env.contract.address);
    
    CONFIG.save(deps.storage, &Config {
        denom: denom.clone(),
        symbol: msg.token_symbol,
        precision: msg.token_precision,
        admin: info.sender.clone(),
    })?;
    
    // Issue FT token
    let issue_msg = CoreumMsg::AssetFT(tx_wasm_sdk::assetft::Msg::Issue(MsgIssue {
        issuer: info.sender.to_string(),
        symbol: msg.token_symbol,
        subunit: msg.token_subunit,
        precision: msg.token_precision,
        initial_amount: msg.initial_supply.into(),
        description: Some("Managed by smart contract".to_string()),
        features: Some(vec![Feature::Minting as i32, Feature::Burning as i32]),
        burn_rate: Some("0.01".to_string()),
        send_commission_rate: Some("0.02".to_string()),
        uri: None,
        uri_hash: None,
    }));
    
    Ok(Response::new()
        .add_attribute("action", "instantiate")
        .add_attribute("denom", denom)
        .add_attribute("admin", info.sender)
        .add_message(issue_msg))
}

#[entry_point]
pub fn execute(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> Result<Response<CoreumMsg>, ContractError> {
    let config = CONFIG.load(deps.storage)?;
    
    match msg {
        ExecuteMsg::Mint { amount } => {
            // Only admin can mint
            if info.sender != config.admin {
                return Err(ContractError::Unauthorized);
            }
            
            let mint_msg = CoreumMsg::AssetFT(tx_wasm_sdk::assetft::Msg::Mint(MsgMint {
                sender: info.sender.to_string(),
                coin: Some(Coin {
                    denom: config.denom,
                    amount: amount.into(),
                }),
            }));
            
            Ok(Response::new()
                .add_attribute("action", "mint")
                .add_attribute("amount", amount)
                .add_message(mint_msg))
        }
        
        ExecuteMsg::Burn { amount } => {
            let burn_msg = CoreumMsg::AssetFT(tx_wasm_sdk::assetft::Msg::Burn(MsgBurn {
                sender: info.sender.to_string(),
                coin: Some(Coin {
                    denom: config.denom,
                    amount: amount.into(),
                }),
            }));
            
            Ok(Response::new()
                .add_attribute("action", "burn")
                .add_attribute("amount", amount)
                .add_message(burn_msg))
        }
        
        ExecuteMsg::Transfer { to, amount } => {
            // Bank send is handled by standard bank module
            let send_msg = cosmwasm_std::BankMsg::Send {
                to_address: to,
                amount: vec![Coin {
                    denom: config.denom,
                    amount: amount.into(),
                }],
            };
            
            Ok(Response::new()
                .add_attribute("action", "transfer")
                .add_attribute("amount", amount)
                .add_message(send_msg))
        }
    }
}

#[entry_point]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    let config = CONFIG.load(deps.storage)?;
    
    match msg {
        QueryMsg::TokenInfo {} => {
            let response = TokenInfoResponse {
                denom: config.denom,
                symbol: config.symbol,
                precision: config.precision,
                admin: config.admin.to_string(),
            };
            to_binary(&response)
        }
        
        QueryMsg::Balance { address } => {
            // Query bank balance
            let balance = deps.querier.query_balance(address, config.denom)?;
            let response = BalanceResponse {
                balance: balance.amount,
            };
            to_binary(&response)
        }
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone)]
pub struct Config {
    pub denom: String,
    pub symbol: String,
    pub precision: u32,
    pub admin: cosmwasm_std::Addr,
}

pub const CONFIG: cw_storage_plus::Item<Config> = cw_storage_plus::Item::new("config");
Using with tx-test-tube
rust
// tests/integration.rs
use cosmwasm_std::Uint128;
use tx_test_tube::{Account, Module, Runner};
use tx_wasm_sdk::assetft::{Feature, MsgIssue};

#[test]
fn test_token_issuance() {
    let runner = Runner::new();
    let admin = runner.init_account();
    
    // Issue token using SDK types
    let issue_msg = MsgIssue {
        issuer: admin.address(),
        symbol: "TEST".to_string(),
        subunit: "utest".to_string(),
        precision: 6,
        initial_amount: Uint128::new(1_000_000).into(),
        description: Some("Test token".to_string()),
        features: Some(vec![Feature::Minting as i32]),
        burn_rate: Some("0.01".to_string()),
        send_commission_rate: Some("0.02".to_string()),
        uri: None,
        uri_hash: None,
    };
    
    let result = runner
        .module::<assetft::AssetFTModule>()
        .issue(&issue_msg, &admin);
    
    assert!(result.is_ok());
}
Feature Flags Reference
AssetFT Features
Feature	Value	Description
Feature::Minting	0	Allow minting new tokens
Feature::Burning	1	Allow burning tokens
Feature::Freezing	2	Allow freezing accounts
Feature::Whitelisting	3	Restrict token reception
Feature::Extension	4	WASM extension support
AssetNFT Features
Feature	Value	Description
ClassFeature::Burning	0	Allow burning NFTs
ClassFeature::Freezing	1	Allow freezing NFTs
ClassFeature::Whitelisting	2	Restrict NFT transfers
ClassFeature::DisableSending	3	Block all transfers
Useful Links
TX Website

TX Documentation

Smart Contract Examples

tx-rust-protobuf

tx-test-tube

Next Steps
Read TX Modules Specification

Read CosmWasm Documentation

Check Deploy First WASM Contract

Check Testing Multiple Contracts
