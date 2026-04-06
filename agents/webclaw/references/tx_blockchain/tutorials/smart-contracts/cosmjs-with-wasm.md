# Using CosmJS with WASM Contracts

Use CosmJS package to instantiate, execute, and query CosmWasm smart contracts on TX Blockchain.

## Overview

This tutorial covers:
- Installing CosmJS dependencies
- Generating TypeScript types from contract schemas
- Instantiating smart contracts
- Executing contract methods
- Querying contract state
- Using browser wallet extensions

## Prerequisites

```bash
# Install Node.js 16+ and npm
node --version
npm --version

# Set testnet variables
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export DENOM="utestcore"
export PREFIX="testcore"
Installing Dependencies
bash
# Create project
mkdir cosmjs-wasm-tutorial
cd cosmjs-wasm-tutorial
npm init -y

# Install CosmJS dependencies
npm install @cosmjs/stargate @cosmjs/cosmwasm-stargate @cosmjs/tendermint-rpc @cosmjs/amino @cosmjs/crypto

# Install additional utilities
npm install @bufbuild/protobuf @bufbuild/protoc-gen-es
Prepare Test Account
Get funded account from TX Testnet Faucet

typescript
// config.ts
export const config = {
    prefix: "testcore",
    hdPath: "m/44'/990'/0'/0/0",
    denom: "utestcore",
    rpcEndpoint: "https://rpc.testnet.tx.dev:443",
    // !!! NEVER hardcode mnemonics in production !!!
    senderMnemonic: "your twelve or twenty four word mnemonic here"
};
Generate TypeScript Types from Smart Contract
Step 1: Add Schema Binary to Contract
In your contract's src/bin/schema.rs:

rust
use cosmwasm_schema::write_api;
use your_contract_name::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};

fn main() {
    write_api! {
        instantiate: InstantiateMsg,
        execute: ExecuteMsg,
        query: QueryMsg,
    }
}
Step 2: Generate JSON Schema
bash
# Run inside your contract folder
cargo run --bin schema
This creates a schema/ folder with JSON files.

Step 3: Install ts-codegen
bash
npm install -g @cosmwasm/ts-codegen
Step 4: Generate TypeScript Code
bash
cosmwasm-ts-codegen generate \
    --plugin client \
    --schema ./schema \
    --out ./ts \
    --name MyProject \
    --no-bundle
This generates:

MyProject.types.ts - TypeScript types for all messages

MyProject.client.ts - Client with contract methods

Network Configuration
typescript
// network.ts
import { GasPrice } from "@cosmjs/stargate";
import { Tendermint34Client } from "@cosmjs/tendermint-rpc";
import { QueryClient } from "@cosmjs/stargate";
import { setupWasmExtension } from "@cosmjs/cosmwasm-stargate";
import { createProtobufRpcClient } from "@cosmjs/stargate";
import { HttpBatchClient } from "@cosmjs/tendermint-rpc";

export async function setupClients(rpcEndpoint: string) {
    const httpClient = new HttpBatchClient(rpcEndpoint);
    const tendermintClient = await Tendermint34Client.create(httpClient);
    const queryClient = QueryClient.withExtensions(tendermintClient, setupWasmExtension);
    const rpcClient = createProtobufRpcClient(queryClient);
    
    return { tendermintClient, queryClient, rpcClient };
}
Gas Price Function
typescript
// gas.ts
import { GasPrice, decodeCosmosSdkDecFromProto } from "@cosmjs/stargate";
import { QueryClientImpl as FeemodelQueryClient } from "./generated/coreum/feemodel/v1/query";

export async function getGasPriceWithMultiplier(
    feemodelQueryClient: FeemodelQueryClient,
    multiplier: number = 1.1
): Promise<GasPrice> {
    const recommendedGasPriceRes = await feemodelQueryClient.RecommendedGasPrice({ 
        AfterBlocks: 10 
    });
    const recommendedGasPrice = decodeCosmosSdkDecFromProto(
        recommendedGasPriceRes.low?.amount || ""
    );
    let gasPrice = recommendedGasPrice.toFloatApproximation() * multiplier;
    return GasPrice.fromString(`${gasPrice}${recommendedGasPriceRes.low?.denom || ""}`);
}
Prepare Sender Client
typescript
// client.ts
import { DirectSecp256k1HdWallet } from "@cosmjs/proto-signing";
import { SigningCosmWasmClient } from "@cosmjs/cosmwasm-stargate";
import { stringToPath } from "@cosmjs/crypto";
import { config } from "./config";
import { getGasPriceWithMultiplier } from "./gas";
import { setupClients } from "./network";

async function setupSenderClient() {
    const { rpcClient } = await setupClients(config.rpcEndpoint);
    const feemodelQueryClient = new FeemodelQueryClient(rpcClient);
    
    console.log("Preparing sender wallet...");
    const senderWallet = await DirectSecp256k1HdWallet.fromMnemonic(config.senderMnemonic, {
        prefix: config.prefix,
        hdPaths: [stringToPath(config.hdPath)],
    });
    
    const [sender] = await senderWallet.getAccounts();
    console.log(`Sender address: ${sender.address}`);
    
    const gasPrice = await getGasPriceWithMultiplier(feemodelQueryClient);
    
    const senderClient = await SigningCosmWasmClient.connectWithSigner(
        config.rpcEndpoint,
        senderWallet,
        { gasPrice }
    );
    
    return { senderClient, sender, feemodelQueryClient };
}
Instantiate a Smart Contract
Using Generated Types
typescript
// instantiate.ts
import { InstantiateMsg } from "./ts/MyProject.types";

async function instantiateContract(
    senderClient: SigningCosmWasmClient,
    senderAddress: string,
    codeId: number
) {
    const instantiateMsg: InstantiateMsg = {
        field1: "value",
        field2: "value"
    };
    
    const instantiateResult = await senderClient.instantiate(
        senderAddress,
        codeId,
        instantiateMsg,
        "my-contract-label",
        "auto",  // Auto-calculate gas
        {
            amount: [{ denom: "utestcore", amount: "0" }]
        }
    );
    
    console.log(`Contract instantiated at: ${instantiateResult.contractAddress}`);
    return instantiateResult;
}
Without Generated Types
typescript
async function instantiateContractManual(
    senderClient: SigningCosmWasmClient,
    senderAddress: string,
    codeId: number
) {
    const instantiateMsg = { 
        field1: "value", 
        field2: "value" 
    };
    
    const instantiateResult = await senderClient.instantiate(
        senderAddress,
        codeId,
        instantiateMsg,
        "my-contract-label",
        "auto",
        {}
    );
    
    console.log(`Contract instantiated at: ${instantiateResult.contractAddress}`);
    return instantiateResult;
}
Execute a Smart Contract
Using Generated Client
typescript
// execute.ts
import { MyProjectClient } from "./ts/MyProject.client";

async function executeWithGeneratedClient(
    senderClient: SigningCosmWasmClient,
    senderAddress: string,
    contractAddress: string
) {
    const client = new MyProjectClient(
        senderClient, 
        senderAddress, 
        contractAddress
    );
    
    const executeResult = await client.messageName({
        field1: "value",
        field2: "value"
    });
    
    console.log(`Execute result: ${executeResult.transactionHash}`);
    return executeResult;
}
Without Generated Types
typescript
async function executeManual(
    senderClient: SigningCosmWasmClient,
    senderAddress: string,
    contractAddress: string
) {
    const executeMsg = {
        message_name: {
            field1: "value",
            field2: "value"
        }
    };
    
    const executeResult = await senderClient.execute(
        senderAddress,
        contractAddress,
        executeMsg,
        "auto",  // Auto-calculate gas
        "optional memo"
    );
    
    console.log(`Execute result: ${executeResult.transactionHash}`);
    return executeResult;
}
Query a Smart Contract
Using Generated Client
typescript
// query.ts
import { CosmWasmClient } from "@cosmjs/cosmwasm-stargate";
import { MyProjectQueryClient } from "./ts/MyProject.client";

async function queryWithGeneratedClient(
    rpcEndpoint: string,
    contractAddress: string
) {
    const cwClient = await CosmWasmClient.connect(rpcEndpoint);
    const queryClient = new MyProjectQueryClient(cwClient, contractAddress);
    
    const queryResponse = await queryClient.queryName({
        field1: "value",
        field2: "value"
    });
    
    console.log(`Query response: ${JSON.stringify(queryResponse)}`);
    return queryResponse;
}
Without Generated Types
typescript
async function queryManual(
    queryClient: CosmWasmClient,
    contractAddress: string
) {
    const queryMsg = {
        query_name: {
            field1: "value",
            field2: "value"
        }
    };
    
    const queryResponse = await queryClient.queryContractSmart(
        contractAddress,
        queryMsg
    );
    
    console.log(`Query response: ${JSON.stringify(queryResponse)}`);
    return queryResponse;
}
Complete Example
typescript
// index.ts
import { DirectSecp256k1HdWallet } from "@cosmjs/proto-signing";
import { SigningCosmWasmClient, CosmWasmClient } from "@cosmjs/cosmwasm-stargate";
import { stringToPath } from "@cosmjs/crypto";
import { GasPrice } from "@cosmjs/stargate";

// Configuration
const config = {
    prefix: "testcore",
    hdPath: "m/44'/990'/0'/0/0",
    denom: "utestcore",
    rpcEndpoint: "https://rpc.testnet.tx.dev:443",
    mnemonic: "your mnemonic here",  // !!! NEVER hardcode in production !!!
    codeId: 123  // Your contract code ID
};

// Nameservice contract messages
interface InstantiateMsg {
    purchase_price: { amount: string; denom: string };
    transfer_price: { amount: string; denom: string };
}

interface ExecuteMsg {
    register?: { name: string };
    transfer?: { name: string; to: string };
}

interface QueryMsg {
    resolve_record?: { name: string };
    config?: Record<string, never>;
}

async function main() {
    try {
        // Setup wallet
        const wallet = await DirectSecp256k1HdWallet.fromMnemonic(config.mnemonic, {
            prefix: config.prefix,
            hdPaths: [stringToPath(config.hdPath)]
        });
        
        const [account] = await wallet.getAccounts();
        console.log(`Account: ${account.address}`);
        
        // Connect client
        const client = await SigningCosmWasmClient.connectWithSigner(
            config.rpcEndpoint,
            wallet,
            { gasPrice: GasPrice.fromString("0.1utestcore") }
        );
        
        // Instantiate contract
        const instantiateMsg: InstantiateMsg = {
            purchase_price: { amount: "100", denom: config.denom },
            transfer_price: { amount: "999", denom: config.denom }
        };
        
        const instantiateResult = await client.instantiate(
            account.address,
            config.codeId,
            instantiateMsg,
            "nameservice",
            "auto",
            { amount: [{ denom: config.denom, amount: "0" }] }
        );
        
        const contractAddress = instantiateResult.contractAddress;
        console.log(`Contract: ${contractAddress}`);
        
        // Register a name
        const registerMsg: ExecuteMsg = { register: { name: "fred" } };
        
        const registerResult = await client.execute(
            account.address,
            contractAddress,
            registerMsg,
            "auto",
            "",
            [{ denom: config.denom, amount: "100" }]
        );
        console.log(`Register tx: ${registerResult.transactionHash}`);
        
        // Query the name
        const queryClient = await CosmWasmClient.connect(config.rpcEndpoint);
        const queryMsg: QueryMsg = { resolve_record: { name: "fred" } };
        
        const queryResult = await queryClient.queryContractSmart(
            contractAddress,
            queryMsg
        );
        console.log(`Query result: ${JSON.stringify(queryResult)}`);
        
        // Transfer ownership
        const newOwner = "testcore1recipientaddress";
        const transferMsg: ExecuteMsg = { transfer: { name: "fred", to: newOwner } };
        
        const transferResult = await client.execute(
            account.address,
            contractAddress,
            transferMsg,
            "auto",
            "",
            [{ denom: config.denom, amount: "999" }]
        );
        console.log(`Transfer tx: ${transferResult.transactionHash}`);
        
        // Verify new owner
        const newQueryResult = await queryClient.queryContractSmart(
            contractAddress,
            queryMsg
        );
        console.log(`New owner: ${JSON.stringify(newQueryResult)}`);
        
    } catch (error) {
        console.error("Error:", error);
    }
}

main();
Using Browser Wallet Extensions
Keplr Wallet Integration
typescript
// browser.ts
import { SigningCosmWasmClient } from "@cosmjs/cosmwasm-stargate";
import { OfflineSigner } from "@cosmjs/proto-signing";

declare global {
    interface Window {
        keplr?: any;
    }
}

async function connectKeplr(): Promise<OfflineSigner> {
    if (!window.keplr) {
        throw new Error("Keplr extension not installed");
    }
    
    const chainId = "txchain-testnet-1";
    
    await window.keplr.enable(chainId);
    const offlineSigner = window.keplr.getOfflineSigner(chainId);
    
    return offlineSigner;
}

async function createClientWithKeplr() {
    const offlineSigner = await connectKeplr();
    const rpcEndpoint = "https://rpc.testnet.tx.dev:443";
    
    const client = await SigningCosmWasmClient.connectWithSigner(
        rpcEndpoint,
        offlineSigner,
        { gasPrice: GasPrice.fromString("0.1utestcore") }
    );
    
    return client;
}
Cosmos-Kit Integration
bash
npm install cosmos-kit @cosmjs/launchpad
typescript
// cosmos-kit-setup.ts
import { ChainProvider } from '@cosmos-kit/react';
import { wallets as keplrWallets } from '@cosmos-kit/keplr';

const chains = [{
    chainName: "txchain-testnet",
    chainId: "txchain-testnet-1",
    rpc: "https://rpc.testnet.tx.dev:443",
    rest: "https://api.testnet.tx.dev:443",
    bip44: { coinType: 990 },
    bech32Config: {
        bech32PrefixAccAddr: "testcore",
        bech32PrefixAccPub: "testcorepub",
        bech32PrefixValAddr: "testcorevaloper",
        bech32PrefixValPub: "testcorevaloperpub",
        bech32PrefixConsAddr: "testcorevalcons",
        bech32PrefixConsPub: "testcorevalconspub"
    },
    currencies: [{
        coinDenom: "TCORE",
        coinMinimalDenom: "utestcore",
        coinDecimals: 6
    }],
    feeCurrencies: [{
        coinDenom: "TCORE",
        coinMinimalDenom: "utestcore",
        coinDecimals: 6
    }]
}];
Complete Project Structure
text
cosmjs-wasm-tutorial/
├── src/
│   ├── index.ts           # Main application
│   ├── config.ts          # Configuration
│   ├── network.ts         # Network setup
│   ├── gas.ts             # Gas price utilities
│   ├── client.ts          # Client setup
│   ├── instantiate.ts     # Contract instantiation
│   ├── execute.ts         # Contract execution
│   ├── query.ts           # Contract queries
│   └── ts/                # Generated TypeScript files
│       ├── MyProject.client.ts
│       └── MyProject.types.ts
├── package.json
├── tsconfig.json
└── README.md
Package.json Scripts
json
{
    "scripts": {
        "start": "ts-node src/index.ts",
        "build": "tsc",
        "generate": "cosmwasm-ts-codegen generate --plugin client --schema ./schema --out ./src/ts --name MyProject --no-bundle"
    }
}
Troubleshooting
Common Errors
Error	Solution
account sequence mismatch	Wait a few seconds and retry
insufficient funds	Fund account via faucet
contract not found	Verify contract address
out of gas	Increase gas limit or use "auto"
Debugging
typescript
// Enable debug logging
process.env.DEBUG = "cosmjs*";

// Log transaction details
console.log("Transaction:", {
    hash: result.transactionHash,
    gasUsed: result.gasUsed,
    gasWanted: result.gasWanted,
    code: result.code,
    rawLog: result.rawLog
});
Next Steps
Read TX Modules Specification

Read CosmWasm Documentation

Check Deploy First WASM Contract

Check Testing Multiple Contracts
