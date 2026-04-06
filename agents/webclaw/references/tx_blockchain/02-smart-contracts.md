# Smart Contracts on TX Blockchain

## Overview
TX uses **WebAssembly (WASM)** as the engine for Smart Contracts through the **CosmWasm** platform. Smart contracts are computer programs stored on the blockchain that execute custom functions.

## Why WASM?
- **Portability** - Runs anywhere WASM runs
- **Performance** - Near-native execution speed
- **Security** - Memory-safe by design
- **Language Flexibility** - Write in Rust, C/C++, JavaScript, Kotlin, Go
- **Small Footprint** - Optimized bytecode for on-chain storage

## Supported Languages
| Language | Status | Recommended For |
|----------|--------|-----------------|
| Rust | ✅ Full support | Production contracts |
| C/C++ | ✅ Supported | Performance-critical |
| JavaScript/TypeScript | ✅ Supported | Rapid prototyping |
| Kotlin | ✅ Supported | Android/Java devs |
| Go | ✅ Supported | Cosmos SDK devs |

## CosmWasm Platform
CosmWasm is the platform TX uses to handle WASM Smart Contracts. It forms an important pillar of the Cosmos SDK with key advantages:

### IBC Compatibility
Smart Contracts can interact with contracts on other blockchains using IBC protocol.

### Actor Model Architecture
Contracts communicate via messages in a "fire and forget" manner:
- **No direct calls** - Prevents re-entrance attacks
- **Isolated state** - Each contract has exclusive access to its state
- **Cross-chain messages** - IBC enables cross-chain contract communication

## Contract Lifecycle

### Phase 1: Upload
Compiled WASM binary is uploaded to the blockchain. No state or address exists yet.

```bash
txd tx wasm store contract.wasm \
  --from wallet \
  --chain-id txchain-testnet-1 \
  --node https://full-node.testnet.tx.dev:26657 \
  --gas auto --gas-adjustment 1.3 \
  -y
