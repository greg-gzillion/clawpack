# Testing Multiple Contracts

Test contract workspaces with multi-contract interactions using the CosmWasm multitest library.

## Overview

This tutorial demonstrates how to test multiple interacting contracts using the `cw-multi-test` framework. Example uses a secure messaging POC with three contracts:
- **Controller** - Orchestrates interactions between contracts
- **Profiles** - Manages user profiles and identities
- **Messages** - Handles message storage and retrieval

## Prerequisites

```bash
# Verify requirements
rustc --version && cargo --version

# Clone the repository
git clone git@github.com:tokenize-x/secure-messaging-poc.git
cd secure-messaging-poc
Workspace Structure
text
├── contracts/
│   ├── controller/
│   │   ├── Cargo.toml
│   │   └── src/
│   ├── messages/
│   │   ├── Cargo.toml
│   │   └── src/
│   └── profiles/
│       ├── Cargo.toml
│       └── src/
├── packages/
│   └── utils/
│       ├── Cargo.toml
│       └── src/
├── Cargo.lock
└── Cargo.toml
Dev Dependencies
Add to contracts/controller/Cargo.toml:

toml
[dev-dependencies]
cw-multi-test = "0.16.5"
profiles = { path = "../profiles" }
messages = { path = "../messages" }
Contract Wrappers
Create wrappers for each contract to store code IDs:

rust
use cosmwasm_std::{Empty, Coin, coins};
use cw_multi_test::{App, AppBuilder, Contract, ContractWrapper};
use controller::contract::{execute, instantiate, query, reply};
use profiles::contract::{execute as profilesExecute, instantiate as profilesInstantiate, query as profilesQuery};
use messages::contract::{execute as messagesExecute, instantiate as messagesInstantiate, query as messagesQuery};

fn controller_contract() -> Box<dyn Contract<Empty>> {
    let contract = ContractWrapper::new(execute, instantiate, query)
        .with_reply(reply);  // Add reply entry point if needed
    Box::new(contract)
}

fn profiles_contract() -> Box<dyn Contract<Empty>> {
    let contract = ContractWrapper::new(profilesExecute, profilesInstantiate, profilesQuery);
    Box::new(contract)
}

fn messages_contract() -> Box<dyn Contract<Empty>> {
    let contract = ContractWrapper::new(messagesExecute, messagesInstantiate, messagesQuery);
    Box::new(contract)
}
Initialize Test App
Basic App (No Balances)
rust
let mut app = App::default();
App with Custom Balances
rust
use cw_multi_test::{AppBuilder, BankKeeper, BasicAppBuilder};
use cosmwasm_std::{Addr, coins};

const DENOM: &str = "ucore";

#[test]
fn test_with_balances() {
    let admin = Addr::unchecked("admin");
    
    let mut app = AppBuilder::new().build(|router, _api, storage| {
        router
            .bank
            .init_balance(storage, &admin, coins(10000, DENOM))
            .unwrap();
    });
    
    // Your test code here
}
Store Contracts
rust
#[test]
fn test_contract_interactions() {
    let admin = Addr::unchecked("admin");
    let mut app = AppBuilder::new().build(|router, _api, storage| {
        router
            .bank
            .init_balance(storage, &admin, coins(10000, DENOM))
            .unwrap();
    });

    // Store contracts
    let code_id_controller = app.store_code(controller_contract());
    let code_id_profiles = app.store_code(profiles_contract());
    let code_id_messages = app.store_code(messages_contract());
    
    // Rest of test...
}
Instantiate Controller Contract
rust
use controller::msg::{ControllerInstantiateMsg, ControllerQueryMsg, ControllerExecuteMsg};
use profiles::msg::{ProfilesQueryMsg, ProfileInfo};
use messages::msg::Config;

let contract_addr = app
    .instantiate_contract(
        code_id_controller,
        admin.clone(),
        &ControllerInstantiateMsg {
            code_id_profiles,
            code_id_messages,
            message_max_len: 5000,
            message_query_default_limit: 50,
            message_query_max_limit: 500,
            create_profile_cost: Some(coin(100, DENOM)),
            send_message_cost: Some(coin(10, DENOM)),
        },
        &[],  // No funds on instantiation
        "Controller",
        None,  // No admin
    )
    .unwrap();
Query Contracts
Query Controller Configuration
rust
let resp: Config = app
    .wrap()
    .query_wasm_smart(contract_addr.clone(), &ControllerQueryMsg::Config {})
    .unwrap();

assert_eq!(resp.message_max_len, 5000);
Query Contract Addresses
rust
use controller::msg::ContractAddressesResponse;

let resp: ContractAddressesResponse = app
    .wrap()
    .query_wasm_smart(contract_addr.clone(), &ControllerQueryMsg::ContractAddresses {})
    .unwrap();

let profiles_addr = resp.profiles_contract_addr;
let messages_addr = resp.messages_contract_addr;
Query Profiles Contract Directly
rust
let profile_info: ProfileInfo = app
    .wrap()
    .query_wasm_smart(
        profiles_addr,
        &ProfilesQueryMsg::AddressInfo { address: admin.to_string() },
    )
    .unwrap();
Execute Contract Calls
Create Profile (with Funds)
rust
let msg_create_profile = &ControllerExecuteMsg::CreateProfile {
    user_id: "myuser".to_owned(),
    pubkey: "mypubkey".to_owned(),
};

let send_funds = coins(100, DENOM);

app.execute_contract(
    admin.clone(),
    contract_addr.clone(),
    msg_create_profile,
    &send_funds,
)
.unwrap();
Send Message
rust
let msg_send_message = &ControllerExecuteMsg::SendMessage {
    to_user_id: "otheruser".to_owned(),
    content: "Hello, world!".to_owned(),
};

let send_funds = coins(10, DENOM);

app.execute_contract(
    admin.clone(),
    contract_addr.clone(),
    msg_send_message,
    &send_funds,
)
.unwrap();
Complete Integration Test Example
rust
#[cfg(test)]
mod tests {
    use super::*;
    use cosmwasm_std::{Addr, Coin, coins};
    use cw_multi_test::{App, AppBuilder, ContractWrapper};
    use controller::contract::{execute, instantiate, query, reply};
    use controller::msg::{ControllerInstantiateMsg, ControllerExecuteMsg, ControllerQueryMsg};
    use profiles::msg::ProfilesQueryMsg;

    const DENOM: &str = "ucore";

    fn setup_app() -> (App, Addr, Addr, u64, u64, u64) {
        let admin = Addr::unchecked("admin");
        
        let mut app = AppBuilder::new().build(|router, _api, storage| {
            router
                .bank
                .init_balance(storage, &admin, coins(10000, DENOM))
                .unwrap();
        });

        let code_id_controller = app.store_code(controller_contract());
        let code_id_profiles = app.store_code(profiles_contract());
        let code_id_messages = app.store_code(messages_contract());

        let contract_addr = app
            .instantiate_contract(
                code_id_controller,
                admin.clone(),
                &ControllerInstantiateMsg {
                    code_id_profiles,
                    code_id_messages,
                    message_max_len: 5000,
                    message_query_default_limit: 50,
                    message_query_max_limit: 500,
                    create_profile_cost: Some(coin(100, DENOM)),
                    send_message_cost: Some(coin(10, DENOM)),
                },
                &[],
                "Controller",
                None,
            )
            .unwrap();

        (app, admin, contract_addr, code_id_controller, code_id_profiles, code_id_messages)
    }

    #[test]
    fn test_create_profile() {
        let (mut app, admin, contract_addr, _, _, _) = setup_app();

        // Create profile
        let msg = ControllerExecuteMsg::CreateProfile {
            user_id: "alice".to_owned(),
            pubkey: "alice_pubkey".to_owned(),
        };
        
        app.execute_contract(
            admin.clone(),
            contract_addr.clone(),
            &msg,
            &coins(100, DENOM),
        )
        .unwrap();

        // Verify profile exists
        let resp: ContractAddressesResponse = app
            .wrap()
            .query_wasm_smart(contract_addr.clone(), &ControllerQueryMsg::ContractAddresses {})
            .unwrap();

        let profile_info: ProfileInfo = app
            .wrap()
            .query_wasm_smart(
                resp.profiles_contract_addr,
                &ProfilesQueryMsg::AddressInfo { address: admin.to_string() },
            )
            .unwrap();

        assert_eq!(profile_info.user_id, "alice");
    }

    #[test]
    fn test_create_profile_insufficient_funds() {
        let (mut app, admin, contract_addr, _, _, _) = setup_app();

        // Try to create profile with insufficient funds
        let msg = ControllerExecuteMsg::CreateProfile {
            user_id: "bob".to_owned(),
            pubkey: "bob_pubkey".to_owned(),
        };
        
        let result = app.execute_contract(
            admin.clone(),
            contract_addr.clone(),
            &msg,
            &coins(1, DENOM),  // Not enough (needs 100)
        );

        assert!(result.is_err());
    }

    #[test]
    fn test_send_message() {
        let (mut app, admin, contract_addr, _, _, _) = setup_app();

        // Create profile for sender
        let create_msg = ControllerExecuteMsg::CreateProfile {
            user_id: "alice".to_owned(),
            pubkey: "alice_pubkey".to_owned(),
        };
        
        app.execute_contract(
            admin.clone(),
            contract_addr.clone(),
            &create_msg,
            &coins(100, DENOM),
        )
        .unwrap();

        // Create profile for recipient (different address needed)
        let recipient = Addr::unchecked("recipient");
        app.execute_contract(
            recipient.clone(),
            contract_addr.clone(),
            &create_msg,
            &coins(100, DENOM),
        )
        .unwrap();

        // Send message
        let send_msg = ControllerExecuteMsg::SendMessage {
            to_user_id: "alice".to_owned(),
            content: "Hello Alice!".to_owned(),
        };
        
        app.execute_contract(
            recipient,
            contract_addr.clone(),
            &send_msg,
            &coins(10, DENOM),
        )
        .unwrap();

        // Verify message was sent (query messages)
        // Add assertions here
    }
}
Run Tests
bash
# Run all tests in workspace
cargo test

# Run tests for specific package
cargo test --package controller

# Run specific test
cargo test test_create_profile --package controller

# Run with output
cargo test -- --nocapture
Build Multiple Contracts
Build all contracts in workspace using workspace optimizer:

bash
docker run --rm -v "$(pwd)":/code \
  --mount type=volume,source="$(basename "$(pwd)")_cache",target=/target \
  --mount type=volume,source=registry_cache,target=/usr/local/cargo/registry \
  cosmwasm/optimizer:0.15.0
Artifacts will be in /artifacts folder.

Common Test Patterns
Testing Contract Replies
rust
fn controller_contract_with_reply() -> Box<dyn Contract<Empty>> {
    let contract = ContractWrapper::new(execute, instantiate, query)
        .with_reply(reply);
    Box::new(contract)
}
Testing with Custom Block Time
rust
use cw_multi_test::AppSettings;

let mut app = App::new(|router, api, storage| {
    // Setup...
});

// Advance time
app.update_block(|block| {
    block.time = block.time.plus_seconds(3600);
    block.height += 1;
});
Testing with Multiple Users
rust
let users = vec![
    Addr::unchecked("user1"),
    Addr::unchecked("user2"),
    Addr::unchecked("user3"),
];

for user in &users {
    app.execute_contract(
        user.clone(),
        contract_addr.clone(),
        &create_profile_msg,
        &coins(100, DENOM),
    ).unwrap();
}
Testing Error Conditions
rust
#[test]
fn test_unauthorized_access() {
    let (mut app, admin, contract_addr, _, _, _) = setup_app();
    let unauthorized = Addr::unchecked("hacker");

    let msg = ControllerExecuteMsg::DeleteProfile {
        user_id: "admin".to_owned(),
    };

    let result = app.execute_contract(
        unauthorized,
        contract_addr,
        &msg,
        &[],
    );

    assert!(result.is_err());
    assert!(result.unwrap_err().to_string().contains("unauthorized"));
}
Test Helper Functions
rust
fn create_profile(
    app: &mut App,
    contract_addr: &Addr,
    user: &Addr,
    user_id: &str,
    pubkey: &str,
) -> Result<app::Response, anyhow::Error> {
    let msg = ControllerExecuteMsg::CreateProfile {
        user_id: user_id.to_string(),
        pubkey: pubkey.to_string(),
    };
    app.execute_contract(user.clone(), contract_addr.clone(), &msg, &coins(100, DENOM))
}

fn get_profile(
    app: &App,
    profiles_addr: &Addr,
    address: &Addr,
) -> ProfileInfo {
    app.wrap()
        .query_wasm_smart(
            profiles_addr.clone(),
            &ProfilesQueryMsg::AddressInfo { 
                address: address.to_string() 
            },
        )
        .unwrap()
}
Next Steps
Read TX Modules Specification

Read CosmWasm Documentation

Check Deploy First WASM Contract tutorial

Explore Smart FT with WASM
