# Special Addresses on TX Blockchain

## Overview

Special addresses are addresses that have a special function or purpose in the TX blockchain and are **not controlled by any private key**. These addresses are used for various purposes such as the community pool, IBC escrow, and module accounts.

> ⚠️ **Important**: These addresses have no private keys and cannot sign transactions. They are controlled by the chain itself or governance.

---

## Module Accounts

In the Cosmos SDK, each module has a module account with an address that has no private key and is only controlled by the chain itself and governance.

### Complete Module Accounts List

| Module | Name | Address | String Identifier |
|--------|------|---------|-------------------|
| x/auth | Auth module | `core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx` | `fee_collector` |
| x/assetft | AssetFT module | `core1mqaw387xfk0xuernjq9cfmmej2ucay80h4nc4h` | `assetft` |
| x/assetnft | AssetNFT module | `core1eqp67ulg76qc2d37ewyvlseztjpuctfxcxqvrf` | `assetnft` |
| x/distribution | Distribution module | `core1jv65s3grqf6v6jl3dp4t6c9t9rk99cd853u8wy` | `distribution` |
| x/gov | Governance module | `core10d07y265gmmuvt4z0w9aw880jnsr700jfvt73g` | `gov` |
| x/ibc | IBC Module | `core1yl6hdjhmkf37639730gffanpzndzdpmha3wjsc` | `transfer` |
| x/nft | NFT Module | `core1hr93qzcjspaa32px0qqywlh9hf9a8plguk7dqu` | `nft` |
| x/staking | Bonded Pool | `core1fl48vsnmsdzcv85q5d2q4z5ajdha8yu3x4357v` | `bonded_tokens_pool` |
| x/staking | Not-Bonded Pool | `core1tygms3xhhs3yv487phx3dw4a95jn7t7lj4d9gc` | `not_bonded_tokens_pool` |

### Query Module Account Balance

```bash
# Query any module account balance
txd query bank balances core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE

# Query fee collector (transaction fees go here)
txd query bank balances core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx
Community Pool
Overview
The community pool is a special account that holds funds for public goods and community initiatives. It is controlled entirely by governance - proposals must be submitted and voted on to spend funds.

Community Pool Address
text
core1jv65s3grqf6v6jl3dp4t6c9t9rk99cd853u8wy
📌 Note: This is the same as the distribution module account address, which also contains uncollected staking rewards.

Funding Sources
Source	Percentage
Community Tax	5% of staking rewards
Transaction Fees	Portion of fees
Slashing Penalties	Portion of slashed funds
Query Community Pool
bash
# Get community pool balance
txd query distribution community-pool \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE

# Example output
# pool:
# - amount: "1000000000"
#   denom: utx
Query via API
bash
# REST API
curl -s https://api.testnet.tx.dev/cosmos/distribution/v1beta1/community_pool | jq .

# gRPC
grpcurl -plaintext rpc.testnet.tx.dev:9090 \
  cosmos.distribution.v1beta1.Query/CommunityPool
Community Pool Spending
Funds can only be spent via governance proposal:

bash
# Submit community pool spend proposal
txd tx gov submit-proposal community-pool-spend \
  --title="Community Grant" \
  --description="Funding for ecosystem development" \
  --recipient="core1recipientaddress" \
  --amount="1000000utx" \
  --deposit="1000000utx" \
  --from=proposer \
  --chain-id=$TX_CHAIN_ID \
  --node=$TX_NODE \
  -y
IBC Escrow Addresses
Overview
The IBC module uses escrow addresses for each channel and port to hold tokens when they are transferred from TX Blockchain to another chain. When tokens are bridged back, they are sent from the escrow address to the recipient.

Escrow Address Format
text
IBC Escrow Address = hash(port + channel)
Common IBC Escrow Addresses
Channel	Port	Counterparty	Escrow Address
channel-0	transfer	Cosmos Hub	core1...
channel-1	transfer	Osmosis	core1...
channel-2	transfer	Osmosis	core12k2pyuylm9t7ugdvz67h9pg4gmmvhn5vvgafk0
channel-3	transfer	Juno	core1...
Query IBC Escrow Balance
bash
# Query escrow address balance
txd query bank balances core12k2pyuylm9t7ugdvz67h9pg4gmmvhn5vvgafk0 \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE

# Query IBC transfer escrow for specific channel
txd query ibc-transfer escrow-address transfer channel-2
IBC Escrow Flow
text
TX Blockchain                    Other Chain (Osmosis)
      │                                  │
      │  1. Send Tokens                   │
      │  ─────────────────────────────────►
      │                                  │
      │  2. Tokens Locked in Escrow       │
      │  core12k2pyuylm...                │
      │                                  │
      │  3. Vouchers Minted               │
      │  ibc/27394FB092...                │
      │                                  │
      │  4. Return Tokens                 │
      │  ◄─────────────────────────────────
      │                                  │
      │  5. Vouchers Burned               │
      │  Tokens Released from Escrow      │
Fee Collector Address
The fee collector accumulates all transaction fees from the network.

text
Address: core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx
Name: fee_collector
Query Fee Collector
bash
# View collected fees
txd query bank balances core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE

# View distribution of fees
txd query distribution fee-pool \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE
Staking Pool Addresses
Bonded Tokens Pool
Holds tokens that are actively staked (bonded) with validators.

text
Address: core1fl48vsnmsdzcv85q5d2q4z5ajdha8yu3x4357v
Name: bonded_tokens_pool
Not-Bonded Tokens Pool
Holds tokens that are in unbonding process.

text
Address: core1tygms3xhhs3yv487phx3dw4a95jn7t7lj4d9gc
Name: not_bonded_tokens_pool
Query Staking Pools
bash
# Query bonded pool
txd query staking pool \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE

# Output shows:
# bonded_tokens: "1000000000000"
# not_bonded_tokens: "50000000000"
Governance Address
The governance module account holds proposal deposits.

text
Address: core10d07y265gmmuvt4z0w9aw880jnsr700jfvt73g
Name: gov
Query Governance Module
bash
# View proposal deposits
txd query gov deposits 1 \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE

# View governance parameters
txd query gov params \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE
Asset Module Addresses
AssetFT (Fungible Tokens)
text
Address: core1mqaw387xfk0xuernjq9cfmmej2ucay80h4nc4h
Name: assetft
AssetNFT (Non-Fungible Tokens)
text
Address: core1eqp67ulg76qc2d37ewyvlseztjpuctfxcxqvrf
Name: assetnft
Query Asset Modules
bash
# Query assetFT module parameters
txd query assetft params \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE

# Query assetNFT classes
txd query assetnft classes \
  --chain-id $TX_CHAIN_ID \
  --node $TX_NODE
Quick Reference Table
Purpose	Address	Module
Fee Collection	core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx	x/auth
Community Pool	core1jv65s3grqf6v6jl3dp4t6c9t9rk99cd853u8wy	x/distribution
Governance	core10d07y265gmmuvt4z0w9aw880jnsr700jfvt73g	x/gov
Bonded Staking	core1fl48vsnmsdzcv85q5d2q4z5ajdha8yu3x4357v	x/staking
Unbonding Staking	core1tygms3xhhs3yv487phx3dw4a95jn7t7lj4d9gc	x/staking
IBC Transfer	core1yl6hdjhmkf37639730gffanpzndzdpmha3wjsc	x/ibc
AssetFT	core1mqaw387xfk0xuernjq9cfmmej2ucay80h4nc4h	x/assetft
AssetNFT	core1eqp67ulg76qc2d37ewyvlseztjpuctfxcxqvrf	x/assetnft
NFT	core1hr93qzcjspaa32px0qqywlh9hf9a8plguk7dqu	x/nft
Important Notes
No Private Keys: These addresses cannot sign transactions

Governance Controlled: Module accounts are controlled by the chain

Immutable: Special addresses are fixed and cannot be changed

Testnet Prefix: On testnet, addresses start with testcore instead of core

Testnet Equivalents
For testnet, replace core prefix with testcore:

bash
# Mainnet
core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx

# Testnet
testcore17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx
Common Use Cases
1. Checking Community Pool for Grants
bash
# Monitor community pool balance
COMMUNITY_POOL=$(txd query distribution community-pool -o json | jq -r '.pool[0].amount')
echo "Community Pool: $COMMUNITY_POOL utx"
2. Tracking IBC Transfers
bash
# Monitor escrow address for incoming transfers
ESCROW_ADDR="core12k2pyuylm9t7ugdvz67h9pg4gmmvhn5vvgafk0"
txd query bank balances $ESCROW_ADDR --watch
3. Verifying Fee Collection
bash
# Check fees collected in last block
FEE_COLLECTOR="core17xpfvakm2amg962yls6f84z3kell8c5lrhmmvx"
txd query bank balances $FEE_COLLECTOR
Next Steps
Transfer funds with CLI

Send multisig Transaction

IBC Transfer Using CLI

Resources
Governance Module

IBC Module

Distribution Module
