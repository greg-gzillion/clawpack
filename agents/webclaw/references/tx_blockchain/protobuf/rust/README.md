# TX Rust Protobuf

A tool to generate Rust protobuf structures for interacting with the TX Blockchain using gRPC and Rust.

## Overview

This tool automates the generation of Rust bindings for TX Blockchain's protobuf definitions, making it easy to build Rust applications that interact with the chain via gRPC.

## How It Works

The tool performs the following steps:

1. **Clone repositories** - Downloads Cosmos-SDK, WASMD, and TX Blockchain repos
2. **Extract protos** - Pulls protobuf definitions for required modules
3. **Generate bindings** - Uses `buf build` and `buf generate` to create Rust structures
4. **Transform** - Applies compatibility transformations for the `tx-wasm-sdk`

## Architecture Flow
┌─────────────────────────────────────────────────────────────────────────────┐
│ Rust Protobuf Generation Process │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Clone │────▶│ Extract │────▶│ buf build │ │
│ │ Repos │ │ Protos │ │ generate │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │ │ │
│ ▼ ▼ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Cosmos-SDK │ │ Coreum │ │ Raw Rust │ │
│ │ WASMD │ │ Modules │ │ Protobufs │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │
│ ▼ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ tx-wasm-sdk │◀────│ Transform │◀────│ Generated │ │
│ │ Compatible │ │ Apply │ │ Rust Code │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Prerequisites

### Rust Installation

```bash
# Install Rust 1.75.0 (required version)
rustup default 1.75.0

# Verify installation
rustc --version
# Should output: rustc 1.75.0
Buf CLI (Required for generation)
bash
# Install buf (macOS)
brew install bufbuild/buf/buf

# Install buf (Linux)
curl -sSL https://github.com/bufbuild/buf/releases/latest/download/buf-Linux-x86_64 -o /usr/local/bin/buf
chmod +x /usr/local/bin/buf

# Verify installation
buf --version
Git (Required for cloning)
bash
git --version
Installation
Clone the Repository
bash
git clone https://github.com/tokenize-x/tx-rust-protobuf
cd tx-rust-protobuf
Run the Generator
bash
cargo run
This generates Rust protobuf structures in the OUT_DIR folder specified in main.rs:

rust
// The directory where proto files will be generated
const OUT_DIR: &str = "transformed-protos";
Configuration
Version Configuration
Modify the constants in main.rs to use different versions:

rust
// Version of the Cosmos SDK being used
const COSMOS_SDK_VERSION: &str = "v0.50.9";

// Version of WASMD being used
const WASMD_VERSION: &str = "v0.53.0";
Module Configuration
Add or remove modules in the INCLUDE_MODS constant:

rust
const INCLUDE_MODS: [&str; 14] = [
    // Cosmos SDK Modules
    "/cosmos/auth",
    "/cosmos/authz",
    "/cosmos/bank",
    "/cosmos/base",
    "/cosmos/distribution",
    "/cosmos/gov",
    "/cosmos/feegrant",
    "/cosmos/staking",
    "/cosmos/nft",
    "/cosmos/group",
    
    // Coreum Modules (TX Blockchain)
    "/coreum/asset",
    "/coreum/dex",
    
    // CosmWasm Module
    "/cosmwasm/wasm",
];
Supported Modules
Module	Path	Description
cosmos/auth	/cosmos/auth	Account authentication
cosmos/authz	/cosmos/authz	Authorization grants
cosmos/bank	/cosmos/bank	Token transfers
cosmos/base	/cosmos/base	Base types (coin, etc.)
cosmos/distribution	/cosmos/distribution	Reward distribution
cosmos/gov	/cosmos/gov	Governance proposals
cosmos/feegrant	/cosmos/feegrant	Fee allowances
cosmos/staking	/cosmos/staking	Validator staking
cosmos/nft	/cosmos/nft	Basic NFT support
cosmos/group	/cosmos/group	Group accounts
coreum/asset	/coreum/asset	FT and NFT assets
coreum/dex	/coreum/dex	DEX order book
cosmwasm/wasm	/cosmwasm/wasm	Smart contracts
Output Structure
After running cargo run, the generated files will be in:

text
transformed-protos/
├── cosmos/
│   ├── auth/
│   │   └── v1beta1/
│   ├── bank/
│   │   └── v1beta1/
│   ├── base/
│   │   └── v1beta1/
│   ├── distribution/
│   │   └── v1beta1/
│   ├── gov/
│   │   └── v1/
│   ├── staking/
│   │   └── v1beta1/
│   └── ...
├── coreum/
│   ├── asset/
│   │   ├── ft/
│   │   │   └── v1/
│   │   └── nft/
│   │       └── v1/
│   └── dex/
│       └── v1/
└── cosmwasm/
    └── wasm/
        └── v1/
Using the Generated Code
Add to Cargo.toml
toml
[dependencies]
# Prost for protobuf handling
prost = "0.12"
prost-types = "0.12"

# Tonic for gRPC
tonic = "0.10"
tonic-build = "0.10"

# For JSON serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# For base64 encoding
base64 = "0.21"

# For hex encoding
hex = "0.4"
Include Generated Code
rust
// Include the generated protobuf modules
pub mod cosmos {
    pub mod auth {
        pub mod v1beta1 {
            include!("generated/cosmos.auth.v1beta1.rs");
        }
    }
    pub mod bank {
        pub mod v1beta1 {
            include!("generated/cosmos.bank.v1beta1.rs");
        }
    }
    // ... other modules
}

pub mod coreum {
    pub mod asset {
        pub mod ft {
            pub mod v1 {
                include!("generated/coreum.asset.ft.v1.rs");
            }
        }
        pub mod nft {
            pub mod v1 {
                include!("generated/coreum.asset.nft.v1.rs");
            }
        }
    }
    pub mod dex {
        pub mod v1 {
            include!("generated/coreum.dex.v1.rs");
        }
    }
}
Example: Query Bank Balance
rust
use cosmos::bank::v1beta1::{QueryBalanceRequest, QueryBalanceResponse};
use cosmos::base::v1beta1::Coin;
use tonic::transport::Channel;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Connect to TX Blockchain gRPC endpoint
    let channel = Channel::from_static("https://grpc.testnet.tx.dev:443")
        .connect()
        .await?;
    
    // Create bank query client
    let mut client = cosmos::bank::v1beta1::query_client::QueryClient::new(channel);
    
    // Build request
    let request = QueryBalanceRequest {
        address: "testcore1..." .to_string(),
        denom: "utestcore".to_string(),
    };
    
    // Execute query
    let response = client.balance(request).await?;
    let balance = response.into_inner().balance.unwrap();
    
    println!("Balance: {} {}", balance.amount, balance.denom);
    
    Ok(())
}
Example: Place DEX Order
rust
use coreum::dex::v1::{MsgPlaceOrder, OrderType, Side, TimeInForce};

fn create_limit_order() -> MsgPlaceOrder {
    MsgPlaceOrder {
        sender: "devcore1...".to_string(),
        r#type: OrderType::Limit as i32,
        id: uuid::Uuid::new_v4().to_string(),
        base_denom: "ucore".to_string(),
        quote_denom: "uusdc".to_string(),
        price: "50000".to_string(),  // 1 ucore = 50000 uusdc
        quantity: "1000000".to_string(), // 1 ucore (6 decimals)
        side: Side::Buy as i32,
        good_til: None,
        time_in_force: TimeInForce::Gtc as i32,
    }
}
Example: Instantiate CosmWasm Contract
rust
use cosmwasm::wasm::v1::{MsgInstantiateContract, AccessConfig, AccessType};

fn create_instantiate_msg() -> MsgInstantiateContract {
    MsgInstantiateContract {
        sender: "core1...".to_string(),
        admin: Some("core1...".to_string()),
        code_id: 1,
        label: "my-contract".to_string(),
        msg: b"{\"owner\":\"core1...\"}".to_vec(),
        funds: vec![
            Coin {
                denom: "ucore".to_string(),
                amount: "1000000".to_string(),
            }
        ],
    }
}
Custom Transformations
The tool applies transformations to make generated code compatible with tx-wasm-sdk:

Common Transformations
Type mappings - Converts protobuf types to Rust-native types

Field naming - Ensures snake_case naming conventions

Optional handling - Converts protobuf optional fields to Option<T>

Serde derives - Adds Serialize/Deserialize derives where needed

Clone/Copy - Implements common traits for better ergonomics

Adding Custom Transformations
To add transformations, modify the transform function in main.rs:

rust
fn transform_generated_code(output_dir: &Path) -> Result<()> {
    // Apply regex replacements
    // Modify field types
    // Add derive attributes
    // Custom logic for specific types
    
    Ok(())
}
Integration with tx-wasm-sdk
The generated protobufs are designed to work seamlessly with tx-wasm-sdk:

rust
use tx_wasm_sdk::{TxClient, Wallet};
use coreum::dex::v1::MsgPlaceOrder;

async fn place_order(wallet: &Wallet, order: MsgPlaceOrder) -> Result<String> {
    let client = TxClient::connect("https://rpc.testnet.tx.dev:443").await?;
    
    // Sign and broadcast the transaction
    let response = client
        .sign_and_broadcast(wallet, order)
        .await?;
    
    Ok(response.txhash)
}
Troubleshooting
Issue: buf command not found
bash
# Install buf
brew install bufbuild/buf/buf  # macOS
# or
npm install -g @bufbuild/buf  # Node.js alternative
Issue: Rust version mismatch
bash
# Set correct Rust version
rustup default 1.75.0

# Verify
rustc --version
Issue: Clone fails due to network
bash
# Increase git buffer size
git config --global http.postBuffer 524288000

# Use SSH instead of HTTPS
git clone git@github.com:cosmos/cosmos-sdk.git
Issue: Out of memory during generation
bash
# Increase memory limit for cargo
export RUSTFLAGS="-C target-cpu=native"
cargo run --release
Complete Example: Full Workflow
rust
// main.rs - Complete example using generated protobufs

use cosmos::bank::v1beta1::{MsgSend, QueryBalanceRequest};
use cosmos::base::v1beta1::Coin;
use coreum::dex::v1::{MsgPlaceOrder, OrderType, Side, TimeInForce};
use cosmwasm::wasm::v1::{MsgExecuteContract, MsgInstantiateContract};
use tonic::transport::Channel;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1. Connect to chain
    let channel = Channel::from_static("https://grpc.testnet.tx.dev:443")
        .connect()
        .await?;
    
    // 2. Query balance
    let mut bank_client = cosmos::bank::v1beta1::query_client::QueryClient::new(channel.clone());
    let balance_req = QueryBalanceRequest {
        address: "testcore1...".to_string(),
        denom: "utestcore".to_string(),
    };
    let balance_res = bank_client.balance(balance_req).await?;
    println!("Balance: {:?}", balance_res.into_inner());
    
    // 3. Create transfer message
    let send_msg = MsgSend {
        from_address: "testcore1...".to_string(),
        to_address: "testcore2...".to_string(),
        amount: vec![Coin {
            denom: "utestcore".to_string(),
            amount: "1000000".to_string(),
        }],
    };
    
    // 4. Create DEX order
    let order_msg = MsgPlaceOrder {
        sender: "testcore1...".to_string(),
        r#type: OrderType::Limit as i32,
        id: uuid::Uuid::new_v4().to_string(),
        base_denom: "ucore".to_string(),
        quote_denom: "uusdc".to_string(),
        price: "50000".to_string(),
        quantity: "1000000".to_string(),
        side: Side::Buy as i32,
        good_til: None,
        time_in_force: TimeInForce::Gtc as i32,
    };
    
    // 5. Create contract execute message
    let exec_msg = MsgExecuteContract {
        sender: "testcore1...".to_string(),
        contract: "core1contract...".to_string(),
        msg: b"{\"transfer\":{\"recipient\":\"core1...\",\"amount\":\"100\"}}".to_vec(),
        funds: vec![Coin {
            denom: "ucore".to_string(),
            amount: "100".to_string(),
        }],
    };
    
    println!("Ready to sign and broadcast transactions");
    
    Ok(())
}
Environment Variables
Variable	Description	Default
OUT_DIR	Output directory for generated code	transformed-protos
COSMOS_SDK_VERSION	Cosmos SDK version	v0.50.9
WASMD_VERSION	WASMD version	v0.53.0
BUF_CACHE_DIR	Buf cache directory	~/.cache/buf
Build Script Integration
Add to your build.rs:

rust
fn main() {
    // Generate protobufs during build
    std::process::Command::new("cargo")
        .arg("run")
        .current_dir("../tx-rust-protobuf")
        .status()
        .unwrap();
    
    // Tell cargo to rerun if the generator changes
    println!("cargo:rerun-if-changed=../tx-rust-protobuf");
}
Resources
Resource	Link
GitHub Repository	https://github.com/tokenize-x/tx-rust-protobuf
tx-wasm-sdk	https://github.com/tokenize-x/tx-wasm-sdk
Buf Documentation	https://buf.build/docs
Prost Documentation	https://docs.rs/prost
Tonic Documentation	https://docs.rs/tonic
License
This project is licensed under the Apache 2.0 License.

text

Now update the main Protobuf README to include the Rust tool:

```bash
nano ~/dev/TXdocumentation/protobuf/README.md
Add this section:

markdown
## Rust Protobuf Generator

A tool to generate Rust protobuf structures for interacting with TX Blockchain via gRPC.

📖 **[Rust Protobuf Documentation](./rust/README.md)**

**Features:**
- Automatically clones Cosmos-SDK, WASMD, and Coreum repositories
- Extracts protobuf definitions for configured modules
- Generates Rust bindings using `buf`
- Applies compatibility transformations for `tx-wasm-sdk`
- Configurable module selection and versions

**Quick Start:**
```bash
git clone https://github.com/tokenize-x/tx-rust-protobuf
cd tx-rust-protobuf
rustup default 1.75.0
cargo run
Generated Modules:

Cosmos SDK (auth, bank, staking, gov, distribution, etc.)

Coreum (asset/ft, asset/nft, dex)

CosmWasm (wasm)

text

Verify the structure:

```bash
ls -la ~/dev/TXdocumentation/protobuf/rust/
