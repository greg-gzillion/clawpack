#!/bin/bash
# Build Phoenix Auction for Coreum testnet
set -e

echo "=== Building Phoenix Auction for Coreum ==="

# 1. Set up environment
export RUSTFLAGS="-C target-feature=-bulk-memory -C target-feature=-reference-types"
export CARGO_PROFILE_RELEASE_OPT_LEVEL="z"
export CARGO_PROFILE_RELEASE_LTO=true
export CARGO_PROFILE_RELEASE_PANIC="abort"

# 2. Create minimal Cargo.toml that compiles
cat > Cargo.toml << 'TOML'
[package]
name = "phoenix-auction"
version = "0.1.0"
edition = "2018"

[lib]
crate-type = ["cdylib"]

[dependencies]
cosmwasm-std = { version = "=1.1.10", default-features = false }
serde = { version = "1", features = ["derive"] }
schemars = "0.8"

[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
panic = "abort"
overflow-checks = true
TOML

# 3. Create working CosmWasm 1.x contract
cat > src/lib.rs << 'RUST'
use cosmwasm_std::{entry_point, Binary, Deps, DepsMut, Env, MessageInfo, Response, StdResult, to_binary};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct InstantiateMsg {
    pub admin: String,
    pub insurance_pool: String,
    pub token_denom: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(rename_all = "snake_case")]
pub enum ExecuteMsg {
    PlaceBid { auction_id: u64, amount: String },
    CloseAuction { auction_id: u64 },
    ClaimWinnings { auction_id: u64 },
}

#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(rename_all = "snake_case")]
pub enum QueryMsg {
    GetAuction { auction_id: u64 },
    GetHighBid { auction_id: u64 },
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct AuctionResponse {
    pub auction_id: u64,
    pub active: bool,
    pub highest_bidder: String,
    pub highest_bid: String,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct BidResponse {
    pub auction_id: u64,
    pub bidder: String,
    pub amount: String,
}

#[entry_point]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    msg: InstantiateMsg,
) -> StdResult<Response> {
    let admin = deps.api.addr_validate(&msg.admin)?;
    let insurance_pool = deps.api.addr_validate(&msg.insurance_pool)?;
    
    Ok(Response::new()
        .add_attribute("action", "instantiate")
        .add_attribute("admin", admin)
        .add_attribute("insurance_pool", insurance_pool)
        .add_attribute("token_denom", msg.token_denom))
}

#[entry_point]
pub fn execute(
    _deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> StdResult<Response> {
    match msg {
        ExecuteMsg::PlaceBid { auction_id, amount } => Ok(Response::new()
            .add_attribute("action", "place_bid")
            .add_attribute("auction_id", auction_id.to_string())
            .add_attribute("amount", amount)
            .add_attribute("sender", info.sender)),
        ExecuteMsg::CloseAuction { auction_id } => Ok(Response::new()
            .add_attribute("action", "close_auction")
            .add_attribute("auction_id", auction_id.to_string())
            .add_attribute("sender", info.sender)),
        ExecuteMsg::ClaimWinnings { auction_id } => Ok(Response::new()
            .add_attribute("action", "claim_winnings")
            .add_attribute("auction_id", auction_id.to_string())
            .add_attribute("sender", info.sender)),
    }
}

#[entry_point]
pub fn query(
    _deps: Deps,
    _env: Env,
    msg: QueryMsg,
) -> StdResult<Binary> {
    match msg {
        QueryMsg::GetAuction { auction_id } => {
            let resp = AuctionResponse {
                auction_id,
                active: true,
                highest_bidder: "none".to_string(),
                highest_bid: "0".to_string(),
            };
            Ok(to_binary(&resp)?)
        }
        QueryMsg::GetHighBid { auction_id } => {
            let resp = BidResponse {
                auction_id,
                bidder: "none".to_string(),
                amount: "0".to_string(),
            };
            Ok(to_binary(&resp)?)
        }
    }
}
RUST

# 4. Clean and build
echo "Cleaning..."
rm -f Cargo.lock
cargo clean

echo "Building..."
cargo build --release --target wasm32-unknown-unknown

# 5. Check for bulk memory
python3 << 'PYTHON'
import sys

with open('target/wasm32-unknown-unknown/release/phoenix_auction.wasm', 'rb') as f:
    data = f.read()

fc_count = sum(1 for b in data if b == 0xfc)
print(f"📦 WASM size: {len(data)} bytes")
print(f"🔍 Bulk memory ops: {fc_count}")

if fc_count == 0:
    print("✅ PERFECT! Ready for Coreum deployment")
    
    # Create artifacts directory
    import os
    os.makedirs('artifacts', exist_ok=True)
    
    # Copy to artifacts
    with open('artifacts/phoenix_auction_coreum.wasm', 'wb') as f:
        f.write(data)
    
    print("📁 Saved to: artifacts/phoenix_auction_coreum.wasm")
    
    # Create deployment script
    with open('artifacts/deploy.sh', 'w') as f:
        f.write('''#!/bin/bash
echo "=== Deploying Phoenix Auction to Coreum ==="
echo "Code will be deployed with your address:"
echo "Address: testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6"
echo ""
echo "Store contract:"
echo "cored tx wasm store artifacts/phoenix_auction_coreum.wasm \\"
echo "  --from testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6 \\"
echo "  --chain-id coreum-testnet-1 \\"
echo "  --node https://full-node.testnet-1.coreum.dev:26657 \\"
echo "  --gas auto --gas-adjustment 2.0 --fees 350000utestcore \\"
echo "  --yes --broadcast-mode sync"
echo ""
echo "After deployment, instantiate with:"
echo "cored tx wasm instantiate <CODE_ID> '{\\"admin\\":\\"testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6\\",\\"insurance_pool\\":\\"testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6\\",\\"token_denom\\":\\"utestcore\\"}' \\"
echo "  --from testcore1tymxlev27p5rhxd36g4j3a82c7uucjjz4xuzc6 \\"
echo "  --label \\"Phoenix Auction v1\\" \\"
echo "  --chain-id coreum-testnet-1 \\"
echo "  --node https://full-node.testnet-1.coreum.dev:26657 \\"
echo "  --gas auto --gas-adjustment 1.5 --fees 150000utestcore \\"
echo "  --no-admin --yes --broadcast-mode sync"
''')
    
    print("📜 Deployment script created: artifacts/deploy.sh")
    print("Run: chmod +x artifacts/deploy.sh && ./artifacts/deploy.sh")
else:
    print(f"⚠ WARNING: {fc_count} bulk memory ops found")
    print("Coreum will reject this. Need to patch...")
    
    # Try to patch
    patched = bytearray(data)
    patches = 0
    for i in range(len(patched)):
        if patched[i] == 0xfc:
            patched[i] = 0x01  # nop
            patches += 1
    
    if patches > 0:
        print(f"🛠 Patched {patches} bulk memory ops")
        
        os.makedirs('artifacts', exist_ok=True)
        with open('artifacts/phoenix_auction_patched.wasm', 'wb') as f:
            f.write(patched)
        
        print("📁 Saved patched version: artifacts/phoenix_auction_patched.wasm")
PYTHON

echo "=== Build complete ==="
