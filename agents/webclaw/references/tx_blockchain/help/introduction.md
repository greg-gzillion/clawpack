# TX Blockchain Introduction

## Overview

TX is a **3rd-generation layer-1 enterprise-grade blockchain** built to serve as a core infrastructure for decentralized applications with **ISO20022 compatibility**, **IBC interoperability**, and novel **Smart Tokens**.

The TX network guarantees:
- Elevated throughput
- Cost-effective fees
- Unparalleled scalability

WASM-based smart contracts enable diverse use cases, while the low-latency, Proof of Stake (PoS) network propels rapid, secure, and modular applications, expediting decentralized tech adoption in large-scale organizations.

## Native Token: $TX

**$TX** is the native token for TX, used for interacting with the blockchain's various features, including:
- Consensus protocol participation
- Decentralized exchange (DEX) operations
- Staking and delegation
- Governance participation
- Transaction fee payment
- Smart token interactions

## Established Use Case

An established use case for a network like TX is the **Sologenic Ecosystem**, which currently resides on the XRP Ledger. The TX blockchain brings together Coreum and Sologenic into a unified protocol, enabling compliant tokenization and lifecycle management of real-world assets.

## Environmental Benefits

TX is:
- **Fast** - Rapid transaction processing with ~1-2 second block times
- **Low cost** - Minimal transaction fees regardless of network load
- **Environmentally friendly** - No high energy consumption

### Energy Efficiency

By leveraging a **Bonded Proof of Stake (BPoS)** consensus mechanism, TX is not subject to the high energy costs that other blockchains are criticized for. Unlike Proof of Work (PoW) chains that consume massive amounts of electricity, TX achieves consensus through staked tokens rather than computational competition.

Furthermore, TX's scalability and throughput ensure that the operation of the network does not incur the exorbitant fees that hinder other blockchains. Even during periods of high demand, transaction costs remain predictable and affordable.

---

## Features

The ecosystem natively supports the following features:

### 1. Smart Contracts

A **Smart Contract** is an executable piece of code that runs on top of the blockchain to facilitate, execute, and enforce an agreement between parties without the involvement of a trusted third party.

TX provides Smart Contracts functionality using **WASM (WebAssembly)** , enabling:
- Multi-language support (Rust, Go, AssemblyScript)
- High-performance execution
- Deterministic computation
- Secure sandboxed environment

> **More details:** See the [Smart Contracts documentation](smart-contracts.md)

### 2. Smart Tokens

Except for the native token **$TX**, the TX Network also provides the ability to create custom tokens with advanced features:

| Feature | Description |
|---------|-------------|
| **Issuance (Minting)** | Create new tokens with customizable supply |
| **Access Control List (ACL)** | Define permissions for token operations |
| **Burning** | Permanently remove tokens from circulation |
| **Freezing** | Temporarily disable specific token transfers |
| **Global Freezing** | Disable all transfers of a token |
| **Whitelisting** | Restrict token transfers to approved addresses |
| **Burn Rate** | Configure percentage of tokens burned per transfer |
| **Clawback** | Ability to recover tokens from addresses |
| **Send Fee (Commission Rate)** | Set fees for token transfers |
| **IBC Compatibility** | Enable cross-chain transfers via IBC |
| **Smart Contract Integration** | Programmable token behavior |
| **Transferring Admin** | Change token administrator |
| **Clear Admin** | Remove administrative privileges |
| **Extension** | Add custom functionality to tokens |

> **More details:** See the [Smart Tokens documentation](smart-tokens.md)

### 3. Fee Model

TX's Fee Model introduces several novel ideas into the Cosmos Ecosystem, which makes the chain more resilient to load spikes and also makes it simpler to interact with the chain.

#### Key Innovations

**Deterministic Gas:**
- Gas is deterministic for most transaction types
- For example, if you want to transfer tokens, you know exactly how much gas you need without interacting with the chain in any way
- No need for gas estimation queries before submitting transactions

**Dynamic Gas Pricing:**
- The gas price is determined based on the load on the system
- The Fee Model module calculates the minimum gas price required by the chain based on configurable parameters
- Automatically adjusts to network demand

**Benefits:**
- Predictable transaction costs
- Resilience to spam attacks
- Fair pricing during congestion
- Simplified developer experience

> **More details:** See the [Fee Model documentation](fee-model.md)

### 4. Decentralized Exchange (DEX)

The DEX supports the trading of **$TX** as well as any issued assets found on TX.

#### Key Features

- **Native integration** - Built directly into the blockchain, not a separate application
- **Low fees** - Minimal trading costs compared to centralized exchanges
- **Secure** - No custody of funds; trades settle on-chain
- **Fast execution** - Transaction finality in seconds
- **Any trading pair** - Users can trade assets by choosing any trading pair

#### Supported Assets

| Asset Type | Examples |
|------------|----------|
| Native token | $TX |
| Smart tokens | Any custom token issued on TX |
| IBC tokens | Tokens from 100+ IBC-connected chains |
| Wrapped assets | Bridged assets from other networks |

> **Release Date:** Check TX's Roadmap for DEX release date.

### 5. Bridges

**Bridges** (or Cross-chain crypto bridges) are applications that enable the transfer of assets between different blockchains.

TX supports two types of bridges:

#### Decentralized Bridge (IBC)

| Feature | Description |
|---------|-------------|
| **Technology** | Inter-Blockchain Communication (IBC) protocol |
| **Security** | Trustless, light-client verification |
| **Connected chains** | 100+ Cosmos SDK chains |
| **Asset transfer** | Native, no wrapping required |
| **Speed** | Fast finality (seconds) |

#### Centralized Bridge

| Feature | Description |
|---------|-------------|
| **Technology** | Handled by TX |
| **Security** | Federated multi-sig approach |
| **Supported chains** | Non-IBC chains (Ethereum, BSC, etc.) |
| **Asset transfer** | Wrapped representation |
| **Speed** | Dependent on source/destination chains |

---

## Technical Specifications

| Specification | Value |
|---------------|-------|
| **Layer** | Layer 1 |
| **Generation** | 3rd Generation |
| **Consensus** | Bonded Proof of Stake (BPoS) |
| **Smart Contracts** | WASM-based |
| **Interoperability** | IBC-enabled |
| **Compliance** | ISO20022 compatible |
| **Block time** | ~1-2 seconds |
| **Finality** | Deterministic |
| **Throughput** | 7,000+ TPS |

---

## Comparison with Other Blockchains

| Feature | TX | Bitcoin | Ethereum | Solana |
|---------|-----|---------|----------|--------|
| **Consensus** | BPoS | PoW | PoS | PoH+PoS |
| **Energy efficient** | ✅ | ❌ | ✅ | ✅ |
| **Low fees** | ✅ | ❌ | ❌ | ✅ |
| **IBC compatible** | ✅ | ❌ | ❌ | ❌ |
| **ISO20022** | ✅ | ❌ | ❌ | ❌ |
| **Smart Tokens** | ✅ | ❌ | ❌ | ❌ |
| **WASM smart contracts** | ✅ | ❌ | ❌ | ❌ |
| **Enterprise focus** | ✅ | ❌ | ❌ | ❌ |

---

## Use Cases

### 1. Real-World Asset Tokenization
- Tokenized securities
- Real estate fractional ownership
- Commodity trading
- Private debt and credit

### 2. Regulated Financial Services
- KYC/AML compliant tokens
- Transfer rule enforcement
- Investor whitelisting
- Regulatory reporting

### 3. DeFi Applications
- Decentralized exchange
- Lending and borrowing
- Yield farming
- Staking derivatives

### 4. Cross-Chain Interoperability
- Asset transfers via IBC
- Cross-chain DeFi
- Multi-chain NFT bridges
- Unified liquidity

### 5. Enterprise Solutions
- Supply chain tracking
- Payment processing
- Identity management
- Document verification

---

## Getting Started

### For Developers

1. [Set up development environment](setup.md)
2. [Write your first smart contract](first-contract.md)
3. [Create a Smart Token](smart-tokens-guide.md)
4. [Deploy on testnet](testnet.md)

### For Validators

1. [Validator requirements](validator-setup.md)
2. [Install TX node](node-installation.md)
3. [Configure and stake](staking-guide.md)
4. [Monitor and maintain](validator-maintenance.md)

### For Users

1. [Create a wallet](wallet-setup.md)
2. [Acquire $TX tokens](acquire-tx.md)
3. [Stake and delegate](staking.md)
4. [Participate in governance](governance.md)

---

## Documentation Navigation

- **Previous:** [General Overview](general-overview.md)
- **Next:** [Smart Contracts](smart-contracts.md)

---

## Additional Resources

| Resource | Link |
|----------|------|
| **Website** | https://tx.org/ |
| **GitHub** | https://github.com/tx-foundation/tx |
| **Discord** | [Join Discord](https://discord.gg/tx) |
| **Twitter** | https://twitter.com/tx_blockchain |
| **Whitepaper** | [MiCA White Paper](../regulatory/mica-whitepaper.md) |

---

*Last updated: 2026-04-02 | Version: 1.0*
