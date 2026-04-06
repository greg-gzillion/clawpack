Custom Params Module
Overview
The Custom Params module allows governance to manage and update network parameters across various modules without requiring full software upgrades. This provides flexibility for fine-tuning the network's behavior.

Key Features
Parameter management - Update module parameters via governance

Staking parameters - Adjust staking-related parameters

Flexible configuration - Modify network behavior without code changes

Governance-controlled - All parameter changes require governance approval

Parameters
Staking Parameters
Parameter	Description	Default
MaxValidators	Maximum number of active validators	150
UnbondingTime	Time to unbond staked tokens	21 days
MaxEntries	Maximum unbonding entries	7
HistoricalEntries	Historical entries to keep	10000
BondDenom	Bonding token denom	utx
Distribution Parameters
Parameter	Description	Default
CommunityTax	Tax for community pool	0.02 (2%)
BaseProposerReward	Base reward for block proposers	0.01 (1%)
BonusProposerReward	Bonus reward for proposers	0.04 (4%)
WithdrawAddrEnabled	Enable withdraw address changes	true
Slashing Parameters
Parameter	Description	Default
SignedBlocksWindow	Window for liveness tracking	10000 blocks
MinSignedPerWindow	Minimum signed blocks required	0.05 (5%)
DowntimeJailDuration	Jail duration for downtime	10 minutes
SlashFractionDoubleSign	Slash fraction for double sign	0.05 (5%)
SlashFractionDowntime	Slash fraction for downtime	0.0001 (0.01%)
Parameter Updates
Update Staking Params
bash
txd tx customparams update-staking-params \
  --max-validators=150 \
  --unbonding-time="504h" \
  --max-entries=7 \
  --historical-entries=10000 \
  --bond-denom="utx" \
  --from gov-module \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:443 \
  -y
Update Distribution Params
bash
txd tx customparams update-distribution-params \
  --community-tax=0.02 \
  --base-proposer-reward=0.01 \
  --bonus-proposer-reward=0.04 \
  --withdraw-addr-enabled=true \
  --from gov-module \
  --chain-id tx-mainnet-1 \
  -y
Update Slashing Params
bash
txd tx customparams update-slashing-params \
  --signed-blocks-window=10000 \
  --min-signed-per-window=0.05 \
  --downtime-jail-duration="600s" \
  --slash-fraction-double-sign=0.05 \
  --slash-fraction-downtime=0.0001 \
  --from gov-module \
  -y
Queries
Get Staking Params
bash
txd query customparams staking-params \
  --node https://rpc.testnet-1.coreum.dev:443
Get Distribution Params
bash
txd query customparams distribution-params \
  --node https://rpc.testnet-1.coreum.dev:443
Get Slashing Params
bash
txd query customparams slashing-params \
  --node https://rpc.testnet-1.coreum.dev:443
Governance Integration
Parameter changes require:
- Proposal submission
- Deposit period
- Voting period
- Threshold met
- Execution

## Proto Definitions
For detailed structure, refer to:

params.proto

tx.proto

query.proto

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

Now let's create the final module documentation:

## 📄 Module 12: WASM/CosmWasm Module

```bash
nano ~/dev/TXdocumentation/modules/wasm/README.md
Paste this content:

markdown
# WASM / CosmWasm Module

## Overview
The WASM module enables Smart Contract functionality on TX Blockchain through CosmWasm. It allows uploading, instantiating, and executing WebAssembly-based smart contracts.

## Module Capabilities
- **Store Code** - Upload WASM binaries
- **Instantiate** - Create contract instances
- **Execute** - Call contract methods
- **Query** - Read contract state
- **Migrate** - Upgrade contract code
- **Admin** - Manage contract permissions
- **Pin/Unpin** - Cache contracts for faster execution

## Contract Lifecycle

### 1. Store Code
```bash
txd tx wasm store contract.wasm \
  --from wallet \
  --chain-id txchain-testnet-1 \
  --node https://full-node.testnet.tx.dev:26657 \
  --gas auto --gas-adjustment 1.3 \
  -y
2. Get Code ID
bash
CODE_ID=$(txd query wasm list-code \
  --node https://full-node.testnet.tx.dev:26657 \
  --output json | jq '.[-1].code_id')
echo "Code ID: $CODE_ID"
3. Instantiate Contract
bash
txd tx wasm instantiate $CODE_ID '{"owner":"'$(txd keys show wallet -a)'"}' \
  --from wallet \
  --label "my-contract" \
  --chain-id txchain-testnet-1 \
  --node https://full-node.testnet.tx.dev:26657 \
  --admin admin-address \
  --gas auto --gas-adjustment 1.3 \
  -y
4. Execute Contract
bash
txd tx wasm execute $CONTRACT_ADDRESS '{"transfer":{"recipient":"address","amount":"100"}}' \
  --from wallet \
  --chain-id txchain-testnet-1 \
  --node https://full-node.testnet.tx.dev:26657 \
  --gas auto --gas-adjustment 1.3 \
  -y
5. Query Contract
bash
txd query wasm contract-state smart $CONTRACT_ADDRESS '{"balance":{"address":"address"}}' \
  --node https://full-node.testnet.tx.dev:26657
Contract Management
Migrate Contract
bash
txd tx wasm migrate $CONTRACT_ADDRESS $NEW_CODE_ID '{"migration_params":{}}' \
  --from admin \
  --chain-id txchain-testnet-1 \
  --node https://full-node.testnet.tx.dev:26657 \
  -y
Update Admin
bash
txd tx wasm update-admin $CONTRACT_ADDRESS new-admin-address \
  --from admin \
  --chain-id txchain-testnet-1 \
  -y
Clear Admin
bash
txd tx wasm clear-admin $CONTRACT_ADDRESS \
  --from admin \
  --chain-id txchain-testnet-1 \
  -y
Pin Code (Cache for fast execution)
bash
txd tx wasm pin $CODE_ID \
  --from validator \
  --chain-id txchain-testnet-1 \
  -y
Unpin Code
bash
txd tx wasm unpin $CODE_ID \
  --from validator \
  -y
Queries
List Codes
bash
txd query wasm list-code \
  --node https://full-node.testnet.tx.dev:26657
List Contracts by Code
bash
txd query wasm list-contracts-by-code $CODE_ID \
  --node https://full-node.testnet.tx.dev:26657
Get Contract Info
bash
txd query wasm contract $CONTRACT_ADDRESS \
  --node https://full-node.testnet.tx.dev:26657
Get Contract State (All)
bash
txd query wasm contract-state all $CONTRACT_ADDRESS \
  --node https://full-node.testnet.tx.dev:26657
Get Raw Contract State
bash
txd query wasm contract-state raw $CONTRACT_ADDRESS <key> \
  --node https://full-node.testnet.tx.dev:26657
Get Pinned Codes
bash
txd query wasm pinned \
  --node https://full-node.testnet.tx.dev:26657
Contract Development
Rust Contract Template
rust
use cosmwasm_std::{
    entry_point, to_binary, Binary, Deps, DepsMut, Env, MessageInfo, 
    Response, StdResult, Storage
};
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct InstantiateMsg {
    pub owner: String,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ExecuteMsg {
    Transfer { recipient: String, amount: u128 },
    Burn { amount: u128 },
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum QueryMsg {
    Balance { address: String },
    Owner {},
}

#[entry_point]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: InstantiateMsg,
) -> StdResult<Response> {
    // Store owner
    deps.storage.set(b"owner", msg.owner.as_bytes());
    Ok(Response::new()
        .add_attribute("method", "instantiate")
        .add_attribute("owner", msg.owner))
}

#[entry_point]
pub fn execute(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> StdResult<Response> {
    match msg {
        ExecuteMsg::Transfer { recipient, amount } => {
            // Transfer logic
            Ok(Response::new()
                .add_attribute("action", "transfer")
                .add_attribute("recipient", recipient)
                .add_attribute("amount", amount.to_string()))
        }
        ExecuteMsg::Burn { amount } => {
            // Burn logic
            Ok(Response::new()
                .add_attribute("action", "burn")
                .add_attribute("amount", amount.to_string()))
        }
    }
}

#[entry_point]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    match msg {
        QueryMsg::Balance { address } => {
            // Query balance
            to_binary(&0u128)
        }
        QueryMsg::Owner {} => {
            let owner = String::from_utf8(deps.storage.get(b"owner").unwrap_or_default())?;
            to_binary(&owner)
        }
    }
}
Build Commands
bash
# Development build
cargo build --target wasm32-unknown-unknown

# Release build
cargo build --release --target wasm32-unknown-unknown

# Optimized build (production)
docker run --rm -v "$(pwd)":/code \
  cosmwasm/workspace-optimizer:0.12.13
Parameters
Parameter	Description	Default
max_wasm_code_size	Max contract size	1MB
max_gas	Max gas per contract execution	10,000,000
instantiate_default_permission	Default instantiate permission	Everybody
Proto Definitions
For detailed structure, refer to:

wasm.proto

tx.proto

query.proto

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## 🎉 Documentation Complete!

You now have a complete TX Blockchain documentation library:
~/dev/TXdocumentation/
├── 01-introduction.md
├── 02-smart-contracts.md
├── 03-smart-tokens.md
├── 04-fee-model.md
├── 05-deployment.md
└── modules/
├── fungible-tokens/README.md
├── nonfungible-tokens/README.md
├── dex/
│ ├── overview.md
│ └── prices-limits.md
├── feemodel/README.md
├── deterministic-gas/README.md
├── governance/README.md
├── ibc/README.md
├── staking/README.md
├── pse/README.md
├── custom-params/README.md
└── wasm/README.md

