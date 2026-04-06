# IBC Smart Contract Call Tutorial

This tutorial showcases a simple CosmWasm Smart Contract that communicates with the same Smart Contract deployed on a different chain. These contracts 'ping-pong' messages to each other incrementing a counter stored on each contract.

## Prerequisites

To complete this tutorial, you need to:

- Install Rust and Cargo
- Be familiar with the Rust programming language
- Have a general understanding of how the TX blockchain works
- Follow the instruction to install `txd` binary
- Set the network variables (use both mainnet and testnet)
- Have a general understanding of IBC and the Hermes Relayer

## Source Code

The complete source code is located at: [tx-ibc-contract-tutorial](https://github.com/tokenize-x/tx-ibc-contract-tutorial.git)

## IBC Channel Overview

To connect Smart Contracts using IBC we must first create a channel between them. Channels are established through a four-way handshake, with each step initiated by a relayer:

### Channel Handshake Phases

| Phase | State | Description |
|-------|-------|-------------|
| **ChanOpenInit** | Chain A → INIT | Sets chain A to INIT state, calls `OnChanOpenInit` for custom validation |
| **ChanOpenTry** | Chain B → TRY | Sets chain B to TRY state, calls `OnChanOpenTry` for counterparty validation |
| **ChanOpenAck** | Chain A → OPEN | Sets chain A to OPEN state, calls `OnChanOpenAck` to finalize version |
| **ChanOpenConfirm** | Chain B → OPEN | Sets chain B to OPEN state, applies CONFIRM logic |

### Required IBC Entry Points in Contract

```rust
// ibc.rs - Required entry points for IBC functionality

// 1. Handle channel opening handshake (OpenInit and OpenTry)
ibc_channel_open()

// 2. Handle channel connection (OpenAck and OpenConfirm)
ibc_channel_connect()

// 3. Handle channel closure (timeout, malicious validators, light client attack)
ibc_channel_close()

// 4. Handle incoming IBC messages (packets)
ibc_packet_receive()

// 5. Handle packet acknowledgements
ibc_packet_ack()

// 6. Handle packet timeouts
ibc_packet_timeout()
Once these entry points are defined, when we instantiate our contract, it will be assigned an IBC port used as an endpoint for the channel the relayer creates.

Set Up Contracts
Build the Smart Contract
bash
# Clone the repository
git clone git@github.com:tokenize-x/tx-ibc-contract-tutorial.git
cd ibc-contract-tutorial/ibc-call

# Build the contract
make build
Deploy on Two Different Chains
For this tutorial, we use TX testnet and devnet. In production, you'd use two different mainnets.

On Chain A (Testnet)
bash
# Store contract
RES=$(txd tx wasm store artifacts/ibc_tutorial.wasm \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS)

CODE_ID=$(echo $RES | jq -r '.logs[0].events[-1].attributes[-1].value')
echo "Code ID: $CODE_ID"

# Instantiate contract
txd tx wasm instantiate $CODE_ID '{}' \
    --from wallet --label "ibc-contract" -b block -y --no-admin \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS

# Capture contract address
CONTRACT_ADDRESS=$(txd query wasm list-contract-by-code $CODE_ID \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contracts[-1]')
echo "Contract address: $CONTRACT_ADDRESS"

# Obtain IBC port
IBC_PORT=$(txd query wasm contract $CONTRACT_ADDRESS \
    --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS | jq -r '.contract_info.ibc_port_id')
echo "IBC Port: $IBC_PORT"
On Chain B (Devnet)
bash
# Same commands but with devnet configuration
export CHAIN_ID="txchain-devnet-1"
export RPC_URL="https://rpc.devnet.tx.dev:443"

# Store, instantiate, and capture contract address and IBC port
# (Repeat the same steps as above)
Example IBC Port Output:

text
IBC Port: wasm.testcore120dn2cr7tqnvup0p6qv2gft5zyjuh8nqhjdzyytc0xapcm08hmzsyv6kd6
This IBC port is the endpoint for the IBC channel we'll create with the relayer.

Set Up Hermes Relayer
Configure Hermes
First, configure Hermes for both chains. Create ~/.hermes/config.toml:

toml
[[chains]]
id = 'txchain-testnet-1'
rpc_addr = 'https://rpc.testnet.tx.dev:443'
grpc_addr = 'https://grpc.testnet.tx.dev:443'
websocket_addr = 'ws://rpc.testnet.tx.dev:443/websocket'
rpc_timeout = '10s'
account_prefix = 'testcore'
key_name = 'testnet-wallet'
store_prefix = 'ibc'
default_gas = 100000
max_gas = 2000000
gas_price = { price = 0.025, denom = 'utestcore' }
gas_adjustment = 1.1
max_msg_num = 30
max_tx_size = 180000
clock_drift = '5s'
max_block_time = '2s'
trusting_period = '14days'
trust_threshold = { numerator = '1', denominator = '3' }

[[chains]]
id = 'txchain-devnet-1'
rpc_addr = 'https://rpc.devnet.tx.dev:443'
grpc_addr = 'https://grpc.devnet.tx.dev:443'
websocket_addr = 'ws://rpc.devnet.tx.dev:443/websocket'
rpc_timeout = '10s'
account_prefix = 'devcore'
key_name = 'devnet-wallet'
store_prefix = 'ibc'
default_gas = 100000
max_gas = 2000000
gas_price = { price = 0.025, denom = 'udevcore' }
gas_adjustment = 1.1
max_msg_num = 30
max_tx_size = 180000
clock_drift = '5s'
max_block_time = '2s'
trusting_period = '14days'
trust_threshold = { numerator = '1', denominator = '3' }
Create IBC Channel
bash
hermes create channel \
    --a-chain txchain-testnet-1 \
    --b-chain txchain-devnet-1 \
    --a-port wasm.testcore120dn2cr7tqnvup0p6qv2gft5zyjuh8nqhjdzyytc0xapcm08hmzsyv6kd6 \
    --b-port wasm.devcore1u8qeahf3aql7xzx25lamtwafrrc63khtwwsg32t9x8azaqa3p6zs2nsekz \
    --channel-version counter-1
Note: The IBC version argument (counter-1) is defined in the contract (ibc.rs):

rust
// Define the version for IBC
pub const IBC_VERSION: &str = "counter-1";
Start the Relayer
bash
hermes start
Once the relayer is running, note the channel IDs that have been established. These are needed to send packets to the right place (contracts can have multiple channels connected to their port).

Execute Contracts
Assume the channel IDs from Hermes are channel-2105 (testnet) and channel-82 (devnet) - your numbers will differ.

Send IBC Packet
Send a packet from the contract on testnet to the contract on devnet:

bash
INCREMENT='{"increment": { "channel": "channel-2105" }}'

txd tx wasm execute $CONTRACT_ADDRESS "$INCREMENT" \
    --from wallet --gas auto --gas-adjustment 1.3 -y -b block --output json \
    $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
⏱️ Note: Packets may take time to be relayed. If the relayer isn't running, packets won't be relayed.

Query Counter on Destination Chain
Query the counter value on the devnet contract:

bash
QUERY='{"get_count": {"channel": "channel-82"}}'

txd query wasm contract-state smart devcore1u8qeahf3aql7xzx25lamtwafrrc63khtwwsg32t9x8azaqa3p6zs2nsekz \
    "$QUERY" --output json $TX_NODE_ARGS $TX_CHAIN_ID_ARGS
Example Output:

json
{
  "data": {
    "count": 1
  }
}
The packet was successfully received and the counter value was updated!

Contract Implementation Details
IBC Packet Receive Entry Point
rust
// Entry point for receiving IBC packets
#[cfg_attr(not(feature = "library"), entry_point)]
pub fn ibc_packet_receive(
    deps: DepsMut,
    env: Env,
    msg: IbcPacketReceiveMsg,
) -> Result<IbcReceiveResponse, Never> {
    // Handle packet and ensure we always ACK regardless of success or failure
    match do_ibc_packet_receive(deps, env, msg) {
        Ok(response) => Ok(response),
        Err(error) => Ok(IbcReceiveResponse::new()
            .add_attribute("method", "ibc_packet_receive")
            .add_attribute("error", error.to_string())
            .set_ack(make_ack_fail(error.to_string()))),
    }
}
Inner Logic for Packet Reception
rust
pub fn do_ibc_packet_receive(
    deps: DepsMut,
    _env: Env,
    msg: IbcPacketReceiveMsg,
) -> Result<IbcReceiveResponse, ContractError> {
    let channel = msg.packet.dest.channel_id;
    let msg: IbcExecuteMsg = from_binary(&msg.packet.data)?;

    match msg {
        IbcExecuteMsg::Increment {} => execute_increment(deps, channel),
    }
}
Extending the Contract
This example has only one message (Increment), but you can extend it to process as many IBC packets as your cross-chain application needs:

rust
pub enum IbcExecuteMsg {
    Increment {},
    Transfer { amount: Uint128, recipient: String },
    UpdateConfig { new_param: String },
    // Add more message types as needed
}
Different Contracts on Different Chains
The contracts can be different as long as the IBC logic is defined correctly. Packets sent from one contract must be able to be processed by the counterparty.

Requirements:

Both contracts must implement the IBC entry points

The sending contract's packet data must be deserializable by the receiving contract

Channel version must match or be negotiated properly

Complete Example Flow
bash
# 1. Deploy contract on testnet
# 2. Deploy contract on devnet
# 3. Get IBC ports from both contracts
# 4. Create channel with Hermes
# 5. Start Hermes relayer
# 6. Send increment from testnet
# 7. Query counter on devnet
# 8. Send increment from devnet back to testnet
# 9. Verify counters incremented on both chains
Troubleshooting
Issue	Solution
Channel handshake fails	Verify IBC_VERSION matches on both contracts
Packets not relayed	Ensure Hermes is running with both chains configured
Timeout errors	Increase timeout height or check relayer connection
Invalid port	Verify IBC port format: wasm.<contract-address>
ACK failure	Check receiving contract's ibc_packet_receive logic
Resources
IBC Channel Overview

Keplr IBC Transfer Guide

Hermes Relayer Documentation

CosmWasm IBC Docs

text

---

Now update the IBC README to include this tutorial:

```bash
nano ~/dev/TXdocumentation/ibc/README.md
Add this section:

markdown
## Smart Contract IBC Tutorial

For a complete walkthrough of contract-to-contract IBC communication:

📖 **[IBC Smart Contract Call Tutorial](./ibc-smart-contract-call.md)**

This tutorial covers:
- IBC channel handshake phases (OpenInit, OpenTry, OpenAck, OpenConfirm)
- Required IBC entry points for CosmWasm contracts
- Deploying contracts on multiple chains
- Setting up Hermes relayer
- Sending IBC packets between contracts
- Querying cross-chain state
- Extending contracts with custom IBC messages
