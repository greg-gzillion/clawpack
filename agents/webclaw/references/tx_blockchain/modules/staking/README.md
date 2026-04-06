# Staking Module

## Overview
TX Blockchain uses a Bonded Proof of Stake (BPoS) consensus mechanism where validators stake $TX to secure the network. Users can delegate their tokens to validators and earn rewards.

## Staking Concepts

### Validators
- Node operators who validate blocks
- Must stake minimum 1,000,000 $TX
- Responsible for network security
- Earn rewards and commission

### Delegators
- Token holders who delegate to validators
- Earn portion of validator rewards
- Share in slashing risk
- No need to run infrastructure

### Staking
- Lock tokens to support network
- Earn staking rewards
- Participate in governance

## Validator Requirements

### Minimum Requirements
- **Minimum self-delegation**: 1,000,000 $TX
- **Hardware**: 4+ CPU, 16GB+ RAM, 500GB+ SSD
- **Uptime**: 95%+ required
- **Security**: Validator keys secured

### Validator Creation
```bash
txd tx staking create-validator \
  --amount=1000000utx \
  --pubkey=$(txd tendermint show-validator) \
  --moniker="My Validator" \
  --identity="ABC123" \
  --website="https://myvalidator.com" \
  --details="Reliable validator with 99% uptime" \
  --commission-rate="0.05" \
  --commission-max-rate="0.20" \
  --commission-max-change-rate="0.01" \
  --min-self-delegation="1000000" \
  --from=wallet \
  --chain-id=tx-mainnet-1 \
  --node=https://rpc.tx.org:443 \
  -y
Delegation
Delegate Tokens
bash
txd tx staking delegate corevaloper1... 1000000utx \
  --from wallet \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:443 \
  -y
Undelegate Tokens
bash
txd tx staking unbond corevaloper1... 500000utx \
  --from wallet \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:443 \
  -y
Redelegate Tokens
bash
txd tx staking redelegate corevaloper1... corevaloper2... 500000utx \
  --from wallet \
  --chain-id tx-mainnet-1 \
  --node https://rpc.tx.org:443 \
  -y
Staking Rewards
Reward Calculation
Rewards are calculated based on:

Total stake in validator

Validator commission rate

Delegator share

Inflation rate

Claim Rewards
bash
# Claim from specific validator
txd tx distribution withdraw-rewards corevaloper1... \
  --from wallet \
  --chain-id tx-mainnet-1 \
  -y

# Claim all rewards
txd tx distribution withdraw-all-rewards \
  --from wallet \
  --chain-id tx-mainnet-1 \
  -y
Compound Rewards
bash
# Withdraw and restake in same transaction
txd tx distribution withdraw-rewards corevaloper1... \
  --from wallet \
  --chain-id tx-mainnet-1 \
  --compound \
  -y
Slashing
Slashing Conditions
Double signing: 5% slashing + jail

Downtime: 0.01% slashing per missed block

Jail period: 10 minutes

Unjail Validator
bash
txd tx slashing unjail \
  --from validator \
  --chain-id tx-mainnet-1 \
  -y
Queries
Get Validators
bash
# List all validators
txd query staking validators \
  --node https://rpc.testnet-1.coreum.dev:443

# Get validator details
txd query staking validator corevaloper1... \
  --node https://rpc.testnet-1.coreum.dev:443
Get Delegations
bash
# Get delegations to validator
txd query staking delegations-to corevaloper1... \
  --node https://rpc.testnet-1.coreum.dev:443

# Get delegations from address
txd query staking delegations wallet-address \
  --node https://rpc.testnet-1.coreum.dev:443
Get Rewards
bash
# Get delegator rewards
txd query distribution rewards wallet-address \
  --node https://rpc.testnet-1.coreum.dev:443

# Get validator commission
txd query distribution commission corevaloper1... \
  --node https://rpc.testnet-1.coreum.dev:443
Get Staking Parameters
bash
txd query staking params \
  --node https://rpc.testnet-1.coreum.dev:443
Parameters
Parameter	Current	Description
unbonding_time	21 days	Time to unbond tokens
max_validators	150	Max active validators
max_entries	7	Max unbonding entries
historical_entries	10000	Historical entries
bond_denom	utx	Staking token denom
Commission Rates
Rate	Description
commission-rate	Current commission percentage
commission-max-rate	Maximum possible commission
commission-max-change-rate	Maximum daily change
Staking Economics
Inflation Rate
Initial: 7% annual

Adjusts based on bonded ratio

Target bonded ratio: 67%

Reward Distribution
Validators: Commission + delegator share

Delegators: Share of rewards minus commission

Community pool: Portion of inflation

Bonded Proof of Stake (BPoS)
How BPoS Works
Tokens are bonded (locked) for staking

Validators produce blocks proportional to stake

Delegators share rewards proportionally

Slashing penalizes misbehavior

Advantages
Energy efficient (no mining)

Economically secure

Decentralized

Low barrier to entry

Proto Definitions
For detailed structure, refer to:

staking.proto

distribution.proto

slashing.proto

