# IBC WASM Transfer Tutorial

This tutorial covers building an IBC-enabled smart contract to transfer tokens on TX Blockchain using CosmWasm and Rust.

> **Full Repository:** [IBC Wasm Transfer Tutorial](https://github.com/tokenize-x/tx-ibc-wasm-transfer-tutorial)

## Prerequisites

- Rust development environment
- TX node running locally
- TX CLI `txd` installed
- Docker

## Contract Structure

The main contract code is in `contract.rs`, which uses `msg.rs` that defines our `ExecuteMsg` and `InstantiateMsg`. It also imports utilities from `cosmwasm_std`.
ibc-wasm-transfer-tutorial/
├── src/
│ ├── contract.rs # Main contract logic
│ ├── msg.rs # Message definitions
│ ├── state.rs # State management
│ └── lib.rs # Module exports
├── Cargo.toml
├── Makefile
└── README.md

text

## Core Concepts in contract.rs

### Imports and Dependencies

```rust
use cosmwasm_std::{
    to_binary, Binary, Coin, CosmosMsg, Deps, DepsMut, Env, MessageInfo,
    Response, StdResult,
};
These imports from cosmwasm_std facilitate the creation, execution, and management of the smart contract on the TX blockchain.

Contract Metadata
Every contract should specify its name and version from Cargo.toml:

rust
const CONTRACT_NAME: &str = env!("CARGO_PKG_NAME");
const CONTRACT_VERSION: &str = env!("CARGO_PKG_VERSION");
Contract Entry Points
1. Instantiation
Instantiation initializes a smart contract on the blockchain (similar to deploying on Ethereum).

rust
#[cfg_attr(not(feature = "library"), entry_point)]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    _msg: InstantiateMsg,
) -> StdResult<Response> {
    set_contract_version(deps.storage, CONTRACT_NAME, CONTRACT_VERSION)?;
    
    Ok(Response::new()
        .add_attribute("method", "instantiate"))
}
Parameters:

deps: DepsMut - Mutable reference to contract's dependencies (storage access)

_env: Env - Blockchain environment info (block height, time)

_info: MessageInfo - Transaction info (sender address)

_msg: InstantiateMsg - Custom instantiation data

2. Execution
The execute function processes all transactions sent to the contract.

rust
#[cfg_attr(not(feature = "library"), entry_point)]
pub fn execute(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    msg: ExecuteMsg,
) -> StdResult<Response> {
    match msg {
        ExecuteMsg::Transfer { channel_id, to_address, amount, timeout } => {
            transfer(channel_id, to_address, amount, timeout)
        }
    }
}
IBC Token Transfer Function
The transfer function handles the IBC token transfer logic:

rust
fn transfer(
    channel_id: String,
    to_address: String,
    amount: Coin,
    timeout: IbcTimeout,
) -> StdResult<Response> {
    // Create IBC transfer message
    let ibc_transfer_msg: CosmosMsg = IbcMsg::Transfer {
        channel_id,
        to_address,
        amount,
        timeout,
    }
    .into();

    // Create response with the IBC message
    let res = Response::new()
        .add_attribute("method", "transfer")
        .add_message(ibc_transfer_msg);

    Ok(res)
}
Parameters Explained:

Parameter	Type	Description
channel_id	String	Unique identifier for the IBC channel (routes transfer between chains)
to_address	String	Recipient's address on the destination blockchain
amount	Coin	Token denomination and amount (e.g., 100 utx)
timeout	IbcTimeout	Time/block height by which transfer must complete
Makefile Commands
The Makefile provides commands for development and testing:

makefile
# Development Commands
make dev          # Build project
make test         # Run tests

# Build & Deploy
make build        # Build WASM with Docker
make deploy       # Deploy contract
make instantiate  # Create a new instance of contract

# Query Commands
make get_count           # Retrieve stored count value
make get_timeout_count   # Retrieve stored timeout count value

# IBC Commands
make channels                # Get IBC channels
make ibc_transfer_cli        # Issue IBC transfer via CLI
make ibc_transfer_wasm_timeout  # Execute IBC transfer with timestamp timeout
Detailed Command Explanations
1. Query IBC Channels
makefile
channels:
	txd query ibc channel channels $TX_CHAIN_ID_ARGS $TX_NODE_ARGS
This queries all available IBC channels on the chain.

2. IBC Transfer with Timeout (via Wasm)
makefile
ibc_transfer_wasm_timeout:
	txd tx wasm execute $CONTRACT_ADDRESS \
	    "{\"transfer\":{
	        \"channel_id\":\"channel-2\",
	        \"to_address\":\"osmo1pwvcapna75slt3uscvupfe52492yuzhflhakem\",
	        \"amount\":{\"amount\":\"2188\",\"denom\":\"udevcore\"},
	        \"timeout\":{\"timestamp\":\"9999999000001000000\"}
	    }}" \
	    --from $DEV_WALLET -b block -y $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Note: Using 9999999000001000000 as a timeout makes the transaction expire on Saturday, November 20, 2286 5:30:00.001 PM (demo purposes only).

Deploying the Contract
Build the WASM Contract
bash
# Clone the repository
git clone https://github.com/tokenize-x/tx-ibc-wasm-transfer-tutorial.git
cd tx-ibc-wasm-transfer-tutorial

# Build with Docker
make build
Deploy to Blockchain
bash
# Store the contract
RES=$(txd tx wasm store artifacts/ibc_wasm_transfer_tutorial.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Code ID: $CODE_ID"
Instantiate the Contract
bash
make instantiate
This runs:

bash
txd tx wasm instantiate $CODE_ID "{}" \
    --amount="10000000$TX_DENOM" \
    --no-admin \
    --label "dev test" \
    --from $DEV_WALLET \
    --gas auto --gas-adjustment 1.3 -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Command Breakdown:

Flag	Description
--amount	Initial funds transferred to contract
--no-admin	Disables admin functions (no contract updates)
--label	Human-readable identifier for the contract
--from	Wallet paying gas fees
--gas auto	Auto-estimate gas
--gas-adjustment 1.3	30% buffer for gas estimation
-b block	Wait for block inclusion
Execute IBC Transfer
Send IBC Transfer via Wasm
bash
make ibc_transfer_wasm_timeout
This calls the contract's transfer function, which creates:

rust
let ibc_transfer_msg: CosmosMsg = IbcMsg::Transfer {
    channel_id,
    to_address,
    amount,
    timeout,
}
Verifying Successful IBC Transfer
Transaction Message (from Explorer)
json
{
    "msg": {
        "transfer": {
            "amount": {
                "denom": "ucore",
                "amount": "1"
            },
            "timeout": {
                "timestamp": "9999999000001000000"
            },
            "channel_id": "channel-2",
            "to_address": "osmo16mwdyj2mmujsf39w0cd82389hlhp82qnzw6fda"
        }
    },
    "@type": "/cosmwasm.wasm.v1.MsgExecuteContract",
    "funds": [],
    "sender": "core10zt2r5p2zh9ltcyg98zt2gtmcypkqgq3qsfj74",
    "contract": "core14lr9zdfn0d5gxjwafh3mg5nrrculj4dndunynve452zws2lzyd3smqrkpz"
}
Transaction Logs
Successful IBC transfers will have these events in the logs:

json
[
    {
        "events": [
            {
                "type": "coin_received",
                "attributes": [
                    {"key": "receiver", "value": "core12k2pyuylm9t7ugdvz67h9pg4gmmvhn5vvgafk0"},
                    {"key": "amount", "value": "1ucore"}
                ]
            },
            {
                "type": "coin_spent",
                "attributes": [
                    {"key": "spender", "value": "core14lr9zdfn0d5gxjwafh3mg5nrrculj4dndunynve452zws2lzyd3smqrkpz"},
                    {"key": "amount", "value": "1ucore"}
                ]
            },
            {
                "type": "ibc_transfer",
                "attributes": [
                    {"key": "sender", "value": "core14lr9zdfn0d5gxjwafh3mg5nrrculj4dndunynve452zws2lzyd3smqrkpz"},
                    {"key": "receiver", "value": "osmo16mwdyj2mmujsf39w0cd82389hlhp82qnzw6fda"}
                ]
            },
            {
                "type": "send_packet",
                "attributes": [
                    {"key": "packet_data", "value": "{\"amount\":\"1\",\"denom\":\"ucore\",\"receiver\":\"osmo16mwdyj2mmujsf39w0cd82389hlhp82qnzw6fda\",\"sender\":\"core14lr9zdfn0d5gxjwafh3mg5nrrculj4dndunynve452zws2lzyd3smqrkpz\"}"},
                    {"key": "packet_timeout_timestamp", "value": "9999999000001000000"},
                    {"key": "packet_src_channel", "value": "channel-2"},
                    {"key": "packet_dst_channel", "value": "channel-2188"}
                ]
            },
            {
                "type": "wasm",
                "attributes": [
                    {"key": "_contract_address", "value": "core14lr9zdfn0d5gxjwafh3mg5nrrculj4dndunynve452zws2lzyd3smqrkpz"},
                    {"key": "method", "value": "transfer"}
                ]
            }
        ]
    }
]
Unit Tests
rust
#[cfg(test)]
mod tests {
    use super::*;
    use cosmwasm_std::testing::{mock_dependencies, mock_env, mock_info};
    use cosmwasm_std::{coins, from_binary};

    #[test]
    fn transfer() {
        let mut deps = mock_dependencies();
        let env = mock_env();
        let info = mock_info("sender", &coins(1000, "ucore"));
        
        // Instantiate contract
        let msg = InstantiateMsg {};
        let res = instantiate(deps.as_mut(), env.clone(), info.clone(), msg).unwrap();
        
        // Execute transfer
        let transfer_msg = ExecuteMsg::Transfer {
            channel_id: "channel-2".to_string(),
            to_address: "osmo1...".to_string(),
            amount: Coin::new(100, "ucore"),
            timeout: IbcTimeout::with_timestamp(env.block.time.plus_seconds(600)),
        };
        
        let res = execute(deps.as_mut(), env, info, transfer_msg).unwrap();
        
        // Verify IBC message was created
        assert_eq!(res.messages.len(), 1);
    }
}
Complete Workflow
bash
# 1. Set up environment variables
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export DENOM="utestcore"
export TX_NODE_ARGS="--node=$RPC_URL"
export TX_CHAIN_ID_ARGS="--chain-id=$CHAIN_ID"

# 2. Create wallet
txd keys add dev-wallet

# 3. Fund wallet from faucet

# 4. Build contract
make build

# 5. Store contract
RES=$(txd tx wasm store artifacts/ibc_wasm_transfer_tutorial.wasm \
    --from dev-wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)
CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')

# 6. Instantiate contract
txd tx wasm instantiate $CODE_ID "{}" \
    --amount="10000000$DENOM" \
    --no-admin --label "ibc-transfer" \
    --from dev-wallet --gas auto --gas-adjustment 1.3 -b block -y \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# 7. Get contract address
CONTRACT_ADDRESS=$(txd query wasm list-contract-by-code $CODE_ID \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')

# 8. Query IBC channels
txd query ibc channel channels $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# 9. Execute IBC transfer
txd tx wasm execute $CONTRACT_ADDRESS \
    '{"transfer":{
        "channel_id":"channel-2",
        "to_address":"osmo1...",
        "amount":{"amount":"1000000","denom":"utestcore"},
        "timeout":{"timestamp":"9999999000001000000"}
    }}' \
    --from dev-wallet -b block -y $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Troubleshooting
Issue	Solution
out of gas	Increase --gas-adjustment to 1.5 or higher
channel not found	Verify channel ID exists with make channels
timeout error	Increase timeout timestamp or use height-based timeout
invalid packet	Check destination address format matches target chain
contract not found	Verify contract address is correct
Resources
IBC Smart Contract Call Tutorial

IBC Channels

Keplr IBC Transfer Guide

CosmWasm IBC Docs

IBC Protocol

Conclusion
This tutorial covered a basic IBC transfer contract flow including:

Contract structure and entry points

IBC transfer message creation

Deploying and instantiating WASM contracts

Executing cross-chain IBC transfers

Verifying transfer success via transaction logs

text

---

Now update the IBC README to include this tutorial:

```bash
nano ~/dev/TXdocumentation/ibc/README.md
Add this section:

markdown
## WASM Developer Tutorials

### IBC WASM Transfer Tutorial

For a complete guide on building IBC-enabled smart contracts:

📖 **[IBC WASM Transfer Tutorial](./ibc-wasm-transfer-tutorial.md)**

This tutorial covers:
- Contract structure and entry points (instantiate, execute)
- IBC token transfer function implementation
- Makefile commands for development and deployment
- Deploying and instantiating WASM contracts
- Executing IBC transfers with timeouts
- Transaction verification and log analysis
