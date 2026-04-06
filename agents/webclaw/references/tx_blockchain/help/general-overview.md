# General Overview

## TX Blockchain at a Glance

TX is a **3rd-generation Layer-1 blockchain** designed for enterprise-grade decentralized applications. Built with the Cosmos SDK and utilizing the CometBFT consensus engine, TX combines institutional compliance features with high-performance blockchain technology.

## Core Philosophy

### Enterprise-First Design
TX prioritizes the needs of large-scale organizations and regulated financial institutions, offering:
- Compliance at the protocol level
- Predictable transaction costs
- High throughput and low latency
- Legal and regulatory readiness

### Interoperability by Default
Through IBC (Inter-Blockchain Communication), TX connects natively to over 100 blockchains, enabling:
- Seamless asset transfers
- Cross-chain smart contract calls
- Shared security and liquidity

### User Empowerment
TX puts control back in users' hands with:
- Self-custody of assets
- Transparent governance
- Open-source software
- Permissionless innovation

## Key Differentiators

### 1. ISO20022 Compliance
TX is compatible with ISO20022, the global standard for financial messaging. This enables:
- Seamless integration with traditional banking systems
- Structured data formats for compliance
- Interoperability with legacy financial infrastructure

### 2. Smart Tokens (Not Just Smart Contracts)
Unlike other blockchains where tokens are simple smart contracts, TX has native **Smart Tokens** with built-in features:
- Programmable compliance (KYC/AML)
- Transfer rules and whitelisting
- Freezing and clawback capabilities
- Configurable fees at the token level

### 3. Bonded Proof of Stake (BPoS)
TX uses a Bonded Proof of Stake consensus mechanism that:
- Secures the network through economic bonding
- Slashes misbehaving validators
- Rewards active participation
- Consumes minimal energy

### 4. WASM Smart Contracts
TX uses WebAssembly (WASM) for smart contracts, offering:
- Multiple programming languages (Rust, Go, AssemblyScript)
- Near-native execution speed
- Deterministic execution
- Smaller attack surface than EVM

## Network Statistics

| Metric | Value |
|--------|-------|
| **Block time** | ~1-2 seconds |
| **Finality** | ~1-2 seconds (deterministic) |
| **Maximum TPS** | 7,000+ |
| **Validators** | Up to 150 |
| **Governance quorum** | 40% |
| **Passing threshold** | 51% |
| **Unbonding period** | 21 days |

## Consensus Mechanism Details

### Bonded Proof of Stake (BPoS)

**How it works:**
1. Validators bond (stake) $TX tokens
2. Network selects top validators by stake weight
3. Validators produce and validate blocks
4. Rewards distributed to validators and delegators
5. Misbehavior results in slashing (loss of staked tokens)

**Slashing Conditions:**

| Offense | Slashing Percentage | Jail Period |
|---------|---------------------|-------------|
| Double signing | 5% | Permanent (tombstoned) |
| Downtime (missed >50% of blocks) | 0.5% | 60 seconds |
| Unresponsiveness | 0.01% | 10 minutes |

### Validator Economics

**Rewards distribution:**
- Block proposer: 5% of block rewards
- Validator commission: Configurable (typically 5-10%)
- Delegators: Remainder after commission
- Community pool: Small percentage for ecosystem funding

## Governance Model

TX uses on-chain governance where $TX holders vote on proposals.

### Proposal Types

| Type | Description | Voting Period |
|------|-------------|---------------|
| **Text** | Non-binding community sentiment | 7 days |
| **Parameter Change** | Modify network parameters | 7 days |
| **Software Upgrade** | Schedule network upgrade | 14 days |
| **Community Spend** | Allocate funds from community pool | 7 days |
| **Token Addition** | Add new token to DEX | 5 days |

### Voting Process
Proposal Submitted
│
▼
Deposit Period (7 days)
(Must raise deposit to proceed)
│
▼
Voting Period (7-14 days)
│
├── Voters cast ballots
│ - Yes
│ - No
│ - No with Veto
│ - Abstain
│
▼
Quorum Check (>40% participation)
│
▼
Threshold Check (>51% Yes)
│
▼
Proposal Implemented OR Rejected

text

### Voting Power
- 1 $TX = 1 vote
- Staked tokens have voting power
- Unbonding tokens lose voting power
- Delegators vote separately from validators

## Security Model

### Economic Security
- Minimum validator stake: 100,000 $TX
- Total stake required for network security: Multi-million $TX
- Slashing provides economic disincentive for misbehavior

### Technical Security
- Regular security audits (CertiK, others)
- Bug bounty program (up to $50,000)
- Formal verification for critical modules
- Testnet deployment before mainnet upgrades

### Operational Security
- Sentry node architecture recommended
- Hardware security modules (HSM) support
- Multi-signature for administrative functions
- Emergency pause mechanism

## Ecosystem Components

### Core Modules

| Module | Purpose |
|--------|---------|
| **Bank** | Token transfers and balance management |
| **Staking** | Validator bonding and delegation |
| **Slashing** | Penalties for misbehavior |
| **Governance** | On-chain voting and proposals |
| **Distribution** | Reward distribution |
| **Fee Model** | Dynamic gas pricing |
| **Smart Tokens** | Custom token creation and management |
| **WASM** | Smart contract execution |
| **IBC** | Cross-chain communication |
| **DEX** | Decentralized exchange |
| **TokenHub** | Token lifecycle management |

### Future Modules (Roadmap)

| Module | Expected Release |
|--------|------------------|
| **Privacy Module** | Q3 2026 |
| **ZK-Rollups** | Q4 2026 |
| **Oracle Module** | Q1 2027 |
| **Liquid Staking** | Q2 2027 |

## Tokenomics Summary

### $TX Token Utility

| Use Case | Description |
|----------|-------------|
| **Transaction fees** | Gas for all network operations |
| **Staking** | Secure the network and earn rewards |
| **Governance** | Vote on protocol changes |
| **DEX trading** | Base pair for all trading |
| **Smart token creation** | Fee for issuing new tokens |
| **Validator bonding** | Minimum stake requirement |

### Supply Overview

| Component | Amount | Percentage |
|-----------|--------|------------|
| Genesis circulating supply | ~1.93B | ~1.9% |
| PSE allocation | 100B | ~98.1% |
| **Total supply** | **~101.93B** | **100%** |

### Inflation Schedule

| Year | Inflation Rate | Purpose |
|------|----------------|---------|
| Year 1-3 | 7-10% | Bootstrapping security |
| Year 4-5 | 5-7% | Mature network |
| Year 6-7 | 2-5% | Stable rewards |
| Year 8+ | 1-2% | Long-term sustainability |

## Compliance Features

### Built-in Compliance Tools

1. **KYC/AML Integration**
   - Whitelisting capabilities
   - Transfer restrictions
   - Address verification

2. **Travel Rule Support**
   - ISO20022 structured data
   - Transfer information sharing
   - Regulatory reporting

3. **Audit Trail**
   - Complete transaction history
   - Token lifecycle events
   - Compliance monitoring

4. **Administrative Controls**
   - Freezing authority
   - Clawback capability
   - Role-based access

## Getting Involved

### Developer Community
- [GitHub Repository](https://github.com/tx-foundation/tx)
- [Developer Documentation](https://docs.tx.org)
- [Technical Discord Channel](https://discord.gg/tx-dev)

### Validator Community
- [Validator Program](https://tx.org/validators)
- [Testnet Validator Onboarding](https://testnet.tx.org/validators)
- [Validator Telegram Group](https://t.me/tx-validators)

### User Community
- [Discord Support](https://discord.gg/tx)
- [Telegram Announcements](https://t.me/tx_announcements)
- [Twitter/X](https://twitter.com/tx_blockchain)

## Documentation Navigation

- **Previous:** None (First page)
- **Next:** [Introduction](introduction.md)

---
*Last updated: 2026-04-02*
