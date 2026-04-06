# TX TypeScript Protobuf

Instructions and tooling for generating TypeScript protobuf files to interact with the TX Blockchain using gRPC.

## Overview

This tool generates TypeScript bindings from TX Blockchain's protobuf definitions, enabling type-safe gRPC communication from Node.js and browser applications.

## Architecture Flow
┌─────────────────────────────────────────────────────────────────────────────┐
│ TypeScript Protobuf Generation Process │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Clone │────▶│ Clone │────▶│ Copy │ │
│ │ tx-chain │ │ Cosmos-SDK │ │ Protos │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ TX Proto │ │ Cosmos Proto│ │ Combined │ │
│ │ Files │ │ Files │ │ Proto Dir │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │
│ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ TypeScript │◀────│ buf │◀────│ buf.gen.yaml│ │
│ │ Output │ │ generate │ │ Template │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Prerequisites

### Install Required Packages

```bash
# Install Buf CLI, protoc-gen-es, and runtime library
npm install @bufbuild/protobuf @bufbuild/protoc-gen-es @bufbuild/buf
Global Installation (Alternative)
bash
# Install buf globally
npm install -g @bufbuild/buf

# Verify installation
buf --version
How It Works
The tool performs these steps:

Clone TX Chain - Gets TX Blockchain protobuf definitions

Clone Cosmos-SDK - Gets Cosmos SDK protobuf definitions

Copy Protos - Combines all proto files into one directory

Generate - Runs buf generate to create TypeScript files

Step-by-Step Guide
Step 1: Clone TX Chain Repository
bash
# Clone TX Chain (master branch)
git clone git@github.com:tokenize-x/tx-chain.git

# Or clone a specific branch
git clone --branch develop git@github.com:tokenize-x/tx-chain.git
Step 2: Clone Cosmos SDK Repository
bash
# Clone Cosmos SDK (v0.47.5 branch)
git clone --branch v0.47.5 git@github.com:cosmos/cosmos-sdk.git

# Other versions you might use:
# git clone --branch v0.50.9 git@github.com:cosmos/cosmos-sdk.git
Step 3: Combine Proto Files
bash
# Create a directory for combined protos
mkdir -p ./combined-proto

# Copy Cosmos SDK protos
cp -r ./cosmos-sdk/proto/* ./combined-proto/

# Copy TX Chain protos
cp -r ./tx-chain/proto/* ./combined-proto/

# Verify the structure
ls -la ./combined-proto/
Step 4: Configure buf.gen.yaml
Create buf.gen.yaml in your project root:

yaml
# buf.gen.yaml
version: v2
plugins:
  - local: protoc-gen-es
    out: ts-protos
    opt:
      - target=ts
      - import_extension=.ts
Step 5: Generate TypeScript Protobufs
bash
# Run buf generate with the template
npx buf generate ./combined-proto --template buf.gen.yaml -o ./ts-protos

# Or if buf is installed globally
buf generate ./combined-proto --template buf.gen.yaml -o ./ts-protos
Output Structure
After generation, the ts-protos directory will contain:

text
ts-protos/
├── cosmos/
│   ├── auth/
│   │   └── v1beta1/
│   │       ├── auth_pb.ts
│   │       ├── genesis_pb.ts
│   │       ├── query_pb.ts
│   │       └── tx_pb.ts
│   ├── bank/
│   │   └── v1beta1/
│   │       ├── bank_pb.ts
│   │       ├── query_pb.ts
│   │       └── tx_pb.ts
│   ├── base/
│   │   └── v1beta1/
│   │       └── coin_pb.ts
│   ├── distribution/
│   │   └── v1beta1/
│   │       ├── distribution_pb.ts
│   │       ├── query_pb.ts
│   │       └── tx_pb.ts
│   ├── gov/
│   │   └── v1/
│   │       ├── gov_pb.ts
│   │       ├── query_pb.ts
│   │       └── tx_pb.ts
│   ├── staking/
│   │   └── v1beta1/
│   │       ├── query_pb.ts
│   │       ├── staking_pb.ts
│   │       └── tx_pb.ts
│   └── ...
├── coreum/
│   ├── asset/
│   │   ├── ft/
│   │   │   └── v1/
│   │   │       ├── authz_pb.ts
│   │   │       ├── event_pb.ts
│   │   │       ├── params_pb.ts
│   │   │       ├── query_pb.ts
│   │   │       ├── token_pb.ts
│   │   │       └── tx_pb.ts
│   │   └── nft/
│   │       └── v1/
│   │           ├── authz_pb.ts
│   │           ├── event_pb.ts
│   │           ├── nft_pb.ts
│   │           ├── params_pb.ts
│   │           ├── query_pb.ts
│   │           └── tx_pb.ts
│   └── dex/
│       └── v1/
│           ├── event_pb.ts
│           ├── order_pb.ts
│           ├── params_pb.ts
│           ├── query_pb.ts
│           └── tx_pb.ts
└── cosmwasm/
    └── wasm/
        └── v1/
            ├── authz_pb.ts
            ├── ibc_pb.ts
            ├── proposal_legacy_pb.ts
            ├── query_pb.ts
            ├── tx_pb.ts
            └── types_pb.ts
Using the Generated Code
Installation
bash
# Install required dependencies
npm install @bufbuild/protobuf @bufbuild/connect @bufbuild/connect-web
Importing Modules
typescript
// Import Cosmos SDK modules
import { MsgSend } from "./ts-protos/cosmos/bank/v1beta1/tx_pb";
import { QueryBalanceRequest } from "./ts-protos/cosmos/bank/v1beta1/query_pb";
import { Coin } from "./ts-protos/cosmos/base/v1beta1/coin_pb";

// Import Coreum modules
import { MsgIssue } from "./ts-protos/coreum/asset/ft/v1/tx_pb";
import { MsgPlaceOrder, OrderType, Side } from "./ts-protos/coreum/dex/v1/tx_pb";

// Import CosmWasm modules
import { MsgExecuteContract } from "./ts-protos/cosmwasm/wasm/v1/tx_pb";
Example 1: Query Bank Balance
typescript
import { createGrpcWebTransport, createClient } from "@bufbuild/connect-web";
import { QueryClient } from "./ts-protos/cosmos/bank/v1beta1/query_pb";

// Create transport to TX Blockchain
const transport = createGrpcWebTransport({
  baseUrl: "https://grpc.testnet.tx.dev",
});

// Create query client
const client = createClient(QueryClient, transport);

// Query balance
async function getBalance(address: string, denom: string) {
  const request = new QueryBalanceRequest({
    address: address,
    denom: denom,
  });
  
  const response = await client.balance(request);
  console.log(`Balance: ${response.balance?.amount} ${response.balance?.denom}`);
  return response.balance;
}

// Usage
await getBalance("testcore1abc123...", "utestcore");
Example 2: Create and Sign Transfer Transaction
typescript
import { MsgSend } from "./ts-protos/cosmos/bank/v1beta1/tx_pb";
import { Coin } from "./ts-protos/cosmos/base/v1beta1/coin_pb";
import { DirectSecp256k1HdWallet } from "@cosmjs/proto-signing";

async function sendTokens() {
  // Create wallet from mnemonic
  const wallet = await DirectSecp256k1HdWallet.fromMnemonic(
    "your mnemonic here",
    { prefix: "testcore" }
  );
  
  // Get account info
  const [account] = await wallet.getAccounts();
  
  // Create send message
  const sendMsg = new MsgSend({
    fromAddress: account.address,
    toAddress: "testcore1recipient...",
    amount: [new Coin({
      denom: "utestcore",
      amount: "1000000", // 1 token (6 decimals)
    })],
  });
  
  // Create transaction
  const tx = {
    body: {
      messages: [sendMsg],
      memo: "Transfer from TypeScript",
    },
    authInfo: {
      fee: {
        amount: [new Coin({ denom: "utestcore", amount: "5000" })],
        gasLimit: BigInt(200000),
      },
    },
  };
  
  // Sign and broadcast (using cosmjs)
  // ... signing logic here
}
Example 3: Issue a Fungible Token
typescript
import { MsgIssue, Feature } from "./ts-protos/coreum/asset/ft/v1/tx_pb";
import { DEXSettings } from "./ts-protos/coreum/asset/ft/v1/token_pb";

async function issueToken(sender: string) {
  // Create DEX settings
  const dexSettings = new DEXSettings({
    unifiedRefAmount: "1",
    whitelistedDenoms: ["ucore", "uusdc"],
  });
  
  // Create issue message
  const issueMsg = new MsgIssue({
    issuer: sender,
    symbol: "MYTOKEN",
    subunit: "umytoken",
    precision: 6,
    initialAmount: "1000000000", // 1000 tokens
    description: "My custom token",
    features: [
      Feature.MINTING,
      Feature.BURNING,
      Feature.IBC,
    ],
    burnRate: "0.01",      // 1% burn on transfers
    sendCommissionRate: "0.001", // 0.1% commission
    uri: "https://example.com/token-metadata.json",
    dexSettings: dexSettings,
  });
  
  return issueMsg;
}
Example 4: Place DEX Order
typescript
import { MsgPlaceOrder, OrderType, Side, TimeInForce } from "./ts-protos/coreum/dex/v1/tx_pb";

async function placeLimitOrder(sender: string) {
  const orderMsg = new MsgPlaceOrder({
    sender: sender,
    type: OrderType.LIMIT,
    id: crypto.randomUUID(),
    baseDenom: "ucore",
    quoteDenom: "uusdc",
    price: "50000",           // 1 ucore = 50000 uusdc
    quantity: "1000000",      // 1 ucore
    side: Side.BUY,
    timeInForce: TimeInForce.GTC,
  });
  
  return orderMsg;
}
Example 5: Execute CosmWasm Contract
typescript
import { MsgExecuteContract } from "./ts-protos/cosmwasm/wasm/v1/tx_pb";
import { Coin } from "./ts-protos/cosmos/base/v1beta1/coin_pb";

async function executeContract(sender: string, contractAddress: string) {
  const executeMsg = new MsgExecuteContract({
    sender: sender,
    contract: contractAddress,
    msg: new TextEncoder().encode(JSON.stringify({
      transfer: {
        recipient: "core1recipient...",
        amount: "100",
      },
    })),
    funds: [
      new Coin({
        denom: "ucore",
        amount: "100",
      }),
    ],
  });
  
  return executeMsg;
}
Example 6: Query DEX Order Book
typescript
import { createGrpcWebTransport, createClient } from "@bufbuild/connect-web";
import { QueryClient } from "./ts-protos/coreum/dex/v1/query_pb";

async function getOrderBook(baseDenom: string, quoteDenom: string) {
  const transport = createGrpcWebTransport({
    baseUrl: "https://grpc.testnet.tx.dev",
  });
  
  const client = createClient(QueryClient, transport);
  
  const request = {
    baseDenom: baseDenom,
    quoteDenom: quoteDenom,
  };
  
  const response = await client.orderBookOrders(request);
  console.log("Buy orders:", response.orders?.filter(o => o.side === Side.BUY));
  console.log("Sell orders:", response.orders?.filter(o => o.side === Side.SELL));
  
  return response;
}
Advanced Configuration
Custom buf.gen.yaml with Multiple Plugins
yaml
# buf.gen.yaml
version: v2
plugins:
  # Generate TypeScript files
  - local: protoc-gen-es
    out: ts-protos
    opt:
      - target=ts
      - import_extension=.ts
  
  # Generate JavaScript files (optional)
  - local: protoc-gen-es
    out: js-protos
    opt:
      - target=js
  
  # Generate type declarations (optional)
  - local: protoc-gen-es
    out: types
    opt:
      - target=ts
      - output_types_only=true
Package.json Scripts
json
{
  "scripts": {
    "proto:clone:tx": "git clone --depth 1 git@github.com:tokenize-x/tx-chain.git",
    "proto:clone:cosmos": "git clone --depth 1 --branch v0.47.5 git@github.com:cosmos/cosmos-sdk.git",
    "proto:copy": "mkdir -p proto && cp -r ./cosmos-sdk/proto/* ./proto/ && cp -r ./tx-chain/proto/* ./proto/",
    "proto:generate": "buf generate ./proto --template buf.gen.yaml -o ./src/protos",
    "proto:clean": "rm -rf proto cosmos-sdk tx-chain",
    "proto:all": "npm run proto:clone:tx && npm run proto:clone:cosmos && npm run proto:copy && npm run proto:generate && npm run proto:clean"
  }
}
Automation Script (generate.sh)
bash
#!/bin/bash

# generate.sh - Automated TypeScript Protobuf Generator

set -e

# Configuration
COSMOS_SDK_VERSION=${COSMOS_SDK_VERSION:-"v0.47.5"}
TX_BRANCH=${TX_BRANCH:-"master"}
OUTPUT_DIR=${OUTPUT_DIR:-"./src/protos"}

echo "🔧 Generating TypeScript Protobufs for TX Blockchain"
echo "   Cosmos SDK Version: $COSMOS_SDK_VERSION"
echo "   TX Branch: $TX_BRANCH"
echo "   Output Directory: $OUTPUT_DIR"

# Clean previous generations
rm -rf ./proto ./cosmos-sdk ./tx-chain

# Clone repositories
echo "📦 Cloning Cosmos SDK..."
git clone --depth 1 --branch $COSMOS_SDK_VERSION git@github.com:cosmos/cosmos-sdk.git

echo "📦 Cloning TX Chain..."
git clone --depth 1 --branch $TX_BRANCH git@github.com:tokenize-x/tx-chain.git

# Create proto directory
mkdir -p ./proto

# Copy proto files
echo "📋 Copying proto files..."
cp -r ./cosmos-sdk/proto/* ./proto/
cp -r ./tx-chain/proto/* ./proto/

# Generate TypeScript files
echo "🔨 Generating TypeScript files..."
npx buf generate ./proto --template buf.gen.yaml -o $OUTPUT_DIR

# Clean up
echo "🧹 Cleaning up..."
rm -rf ./proto ./cosmos-sdk ./tx-chain

echo "✅ Generation complete! Output in $OUTPUT_DIR"
Using with Connect-Web
Setup gRPC-Web Client
typescript
// client.ts
import { createGrpcWebTransport, createClient } from "@bufbuild/connect-web";
import { QueryClient as BankQueryClient } from "./protos/cosmos/bank/v1beta1/query_pb";
import { QueryClient as DexQueryClient } from "./protos/coreum/dex/v1/query_pb";
import { QueryClient as WasmQueryClient } from "./protos/cosmwasm/wasm/v1/query_pb";

class TXBlockchainClient {
  private transport;
  
  public bank: ReturnType<typeof createClient<BankQueryClient>>;
  public dex: ReturnType<typeof createClient<DexQueryClient>>;
  public wasm: ReturnType<typeof createClient<WasmQueryClient>>;
  
  constructor(endpoint: string) {
    this.transport = createGrpcWebTransport({
      baseUrl: endpoint,
    });
    
    this.bank = createClient(BankQueryClient, this.transport);
    this.dex = createClient(DexQueryClient, this.transport);
    this.wasm = createClient(WasmQueryClient, this.transport);
  }
}

// Usage
const client = new TXBlockchainClient("https://grpc.testnet.tx.dev");
const balance = await client.bank.balance({
  address: "testcore1...",
  denom: "utestcore",
});
Troubleshooting
Issue: Buf not found
bash
# Install buf locally
npm install @bufbuild/buf

# Use npx
npx buf generate ...

# Or install globally
npm install -g @bufbuild/buf
Issue: Clone permission denied
bash
# Use HTTPS instead of SSH
git clone https://github.com/tokenize-x/tx-chain.git
git clone https://github.com/cosmos/cosmos-sdk.git
Issue: Duplicate proto definitions
bash
# Copy with overwrite
cp -rf ./cosmos-sdk/proto/* ./proto/
cp -rf ./tx-chain/proto/* ./proto/
Issue: TypeScript compilation errors
bash
# Ensure tsconfig.json has correct settings
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
Issue: Large proto files cause memory issues
bash
# Generate incrementally
buf generate --path ./proto/cosmos/bank
buf generate --path ./proto/coreum/asset
buf generate --path ./proto/cosmwasm/wasm
Complete Example Project
File Structure
text
tx-ts-client/
├── src/
│   ├── protos/           # Generated protobufs
│   ├── client.ts         # Main client
│   ├── wallet.ts         # Wallet utilities
│   └── index.ts          # Entry point
├── buf.gen.yaml          # Buf configuration
├── package.json
├── tsconfig.json
└── generate.sh           # Generation script
package.json
json
{
  "name": "tx-ts-client",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "proto:generate": "./generate.sh",
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@bufbuild/connect-web": "^0.13.0",
    "@bufbuild/protobuf": "^1.7.0",
    "@cosmjs/proto-signing": "^0.32.0",
    "@cosmjs/stargate": "^0.32.0"
  },
  "devDependencies": {
    "@bufbuild/buf": "^1.32.0",
    "@bufbuild/protoc-gen-es": "^1.7.0",
    "typescript": "^5.3.0"
  }
}
tsconfig.json
json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "lib": ["ES2020", "DOM"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
Resources
Resource	Link
GitHub Repository	https://github.com/tokenize-x/tx-ts-protobuf
@bufbuild/protobuf	https://www.npmjs.com/package/@bufbuild/protobuf
@bufbuild/connect-web	https://www.npmjs.com/package/@bufbuild/connect-web
Buf Documentation	https://buf.build/docs
CosmJS Documentation	https://cosmjs.tech
TX Blockchain	https://tx.org
License
This project is licensed under the Apache 2.0 License.

text

Now update the main Protobuf README:

```bash
nano ~/dev/TXdocumentation/protobuf/README.md
Add this section:

markdown
## TypeScript Protobuf Generator

Instructions and tooling for generating TypeScript protobuf files for TX Blockchain.

📖 **[TypeScript Protobuf Documentation](./typescript/README.md)**

**Features:**
- Generates type-safe TypeScript bindings
- Uses Buf CLI for modern protobuf tooling
- Supports all Cosmos SDK, Coreum, and CosmWasm modules
- Compatible with @bufbuild/connect-web for gRPC-web
- Includes automation scripts

**Quick Start:**
```bash
# Install dependencies
npm install @bufbuild/protobuf @bufbuild/protoc-gen-es @bufbuild/buf

# Clone repositories
git clone git@github.com:tokenize-x/tx-chain.git
git clone --branch v0.47.5 git@github.com:cosmos/cosmos-sdk.git

# Combine protos and generate
cp -r ./cosmos-sdk/proto/* ./tx-chain/proto/
npx buf generate ./tx-chain/proto --template buf.gen.yaml -o ./ts-protos
Generated Modules:

Cosmos SDK (auth, bank, staking, gov, distribution)

Coreum (asset/ft, asset/nft, dex)

CosmWasm (wasm)

