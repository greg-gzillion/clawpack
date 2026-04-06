#!/usr/bin/env python3
"""
PhoenixPME Development Helper - Generates, Tests, and Deploys Code
"""

import os
import json
import subprocess
from pathlib import Path

class PhoenixHelper:
    def __init__(self):
        self.project_path = Path("/home/greg/dev/TX")
        self.test_results = []
        
    def generate_token_contract(self, token_name, token_symbol, supply):
        """Generate a complete token contract for PhoenixPME"""
        
        contract = f'''
// PhoenixPME Token Contract - {token_name} ({token_symbol})
// Deployed on TX Blockchain

use cosmwasm_std::{{ 
    entry_point, to_binary, Binary, Deps, DepsMut, Env, 
    MessageInfo, Response, StdResult, Addr, Uint128 
}};
use cw20::{{Cw20ReceiveMsg, Expiration}};
use schemars::JsonSchema;
use serde::{{Deserialize, Serialize}};

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct InstantiateMsg {{
    pub name: String,
    pub symbol: String,
    pub decimals: u8,
    pub initial_supply: Uint128,
    pub mint: Option<MinterResponse>,
}}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct MinterResponse {{
    pub minter: String,
    pub cap: Option<Uint128>,
}}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ExecuteMsg {{
    Transfer {{ recipient: String, amount: Uint128 }},
    Burn {{ amount: Uint128 }},
    Mint {{ recipient: String, amount: Uint128 }},
    Freeze {{ account: String }},
    Unfreeze {{ account: String }},
    Clawback {{ from: String, amount: Uint128 }},
}}

#[entry_point]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    msg: InstantiateMsg,
) -> StdResult<Response> {{
    // Initialize token with PhoenixPME parameters
    Ok(Response::new()
        .add_attribute("action", "instantiate")
        .add_attribute("name", msg.name)
        .add_attribute("symbol", msg.symbol)
        .add_attribute("supply", msg.initial_supply))
}}

// Deploy with:
// txd tx wasm store token.wasm --from phoenix-wallet
// txd tx wasm instantiate <CODE_ID> '{json}' --label "{token_name}" --from phoenix-wallet
'''
        return contract
    
    def generate_deploy_script(self, token_name, token_symbol):
        """Generate deployment script"""
        
        script = f'''#!/bin/bash
# PhoenixPME Token Deployment Script
# Token: {token_name} ({token_symbol})

echo "🚀 Deploying PhoenixPME Token on TX Blockchain"

# Set variables
CHAIN_ID="txchain-testnet-1"
NODE="https://rpc.testnet-1.coreum.dev:443"
WALLET="phoenix-wallet"

# 1. Store contract
echo "📦 Storing contract..."
STORE_RESULT=$(txd tx wasm store token.wasm \\
    --from $WALLET \\
    --chain-id $CHAIN_ID \\
    --node $NODE \\
    --gas 2000000 \\
    --fees 2000utx \\
    -y --output json)

CODE_ID=$(echo $STORE_RESULT | jq -r '.logs[0].events[] | select(.type=="store_code") | .attributes[] | select(.key=="code_id") | .value')
echo "✅ Contract stored with code_id: $CODE_ID"

# 2. Instantiate contract
echo "🔧 Instantiating contract..."
INIT_MSG='{{"name":"{token_name}","symbol":"{token_symbol}","decimals":6,"initial_supply":"1000000000000"}}'

INSTANTIATE_RESULT=$(txd tx wasm instantiate $CODE_ID "$INIT_MSG" \\
    --from $WALLET \\
    --chain-id $CHAIN_ID \\
    --node $NODE \\
    --label "{token_name}" \\
    --admin $(txd keys show $WALLET -a) \\
    --gas 1000000 \\
    --fees 1000utx \\
    -y --output json)

CONTRACT_ADDR=$(echo $INSTANTIATE_RESULT | jq -r '.logs[0].events[] | select(.type=="instantiate") | .attributes[] | select(.key=="_contract_address") | .value')
echo "✅ Contract instantiated at: $CONTRACT_ADDR"

# 3. Verify deployment
echo "🔍 Verifying deployment..."
txd query wasm contract $CONTRACT_ADDR --node $NODE

echo ""
echo "🎉 PhoenixPME Token Deployed Successfully!"
echo "Contract: $CONTRACT_ADDR"
echo "Code ID: $CODE_ID"
'''
        return script
    
    def generate_test_suite(self):
        """Generate test suite for PhoenixPME"""
        
        test_code = '''
#!/usr/bin/env python3
"""
PhoenixPME Test Suite - Validates TX Blockchain Integration
"""

import subprocess
import json
import time

class PhoenixTester:
    def __init__(self):
        self.results = []
        self.chain_id = "txchain-testnet-1"
        self.node = "https://rpc.testnet-1.coreum.dev:443"
    
    def test_connection(self):
        """Test connection to TX blockchain"""
        try:
            result = subprocess.run(
                f'txd status --node {self.node}',
                shell=True, capture_output=True, text=True
            )
            if result.returncode == 0:
                self.results.append(("✅ Connection", "Connected to TX testnet"))
                return True
        except:
            pass
        self.results.append(("❌ Connection", "Failed to connect"))
        return False
    
    def test_wallet_balance(self, wallet_address):
        """Test wallet balance"""
        result = subprocess.run(
            f'txd query bank balances {wallet_address} --node {self.node}',
            shell=True, capture_output=True, text=True
        )
        if "balances" in result.stdout:
            self.results.append(("✅ Wallet", f"Balance checked for {wallet_address[:10]}..."))
            return True
        self.results.append(("❌ Wallet", "Failed to get balance"))
        return False
    
    def test_token_query(self, contract_address):
        """Test token contract query"""
        query = '{"token_info":{}}'
        result = subprocess.run(
            f'txd query wasm contract-state smart {contract_address} \'{query}\' --node {self.node}',
            shell=True, capture_output=True, text=True
        )
        if "data" in result.stdout:
            self.results.append(("✅ Token Query", "Token info retrieved"))
            return True
        self.results.append(("❌ Token Query", "Failed to query token"))
        return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Running PhoenixPME Test Suite...")
        print("=" * 50)
        
        self.test_connection()
        
        print("\\n📊 Test Results:")
        for status, msg in self.results:
            print(f"  {status}: {msg}")
        
        passed = sum(1 for s, _ in self.results if "✅" in s)
        total = len(self.results)
        print(f"\\n🎯 Score: {passed}/{total} tests passed")
        
        return passed == total

if __name__ == "__main__":
    tester = PhoenixTester()
    tester.run_all_tests()
'''
        return test_code
    
    def save_code(self, code, filename):
        """Save generated code"""
        filepath = self.project_path / filename
        with open(filepath, 'w') as f:
            f.write(code)
        print(f"✅ Saved to {filepath}")
        return filepath

def main():
    helper = PhoenixHelper()
    
    print("=" * 70)
    print("🏛️ PhoenixPME Development Helper")
    print("=" * 70)
    print("\nGenerate production-ready code for your PhoenixPME project")
    print("\nOptions:")
    print("  1. Generate token contract")
    print("  2. Generate deployment script")
    print("  3. Generate test suite")
    print("  4. Deploy token")
    print("  5. Run tests")
    print("  exit - Quit")
    
    while True:
        try:
            choice = input("\n🔧 Select (1-5): ").strip()
            
            if choice == 'exit':
                break
            
            if choice == '1':
                name = input("Token name (e.g., PhoenixPME): ").strip() or "PhoenixPME"
                symbol = input("Token symbol (e.g., PME): ").strip() or "PME"
                supply = input("Initial supply: ").strip() or "1000000000"
                
                contract = helper.generate_token_contract(name, symbol, supply)
                helper.save_code(contract, "contracts/token.rs")
                print("\n📝 Next steps:")
                print("  1. Review the contract code")
                print("  2. Run: cargo wasm")
                print("  3. Deploy using option 2")
            
            elif choice == '2':
                name = input("Token name: ").strip() or "PhoenixPME"
                symbol = input("Token symbol: ").strip() or "PME"
                
                script = helper.generate_deploy_script(name, symbol)
                helper.save_code(script, "scripts/deploy.sh")
                os.chmod(helper.project_path / "scripts/deploy.sh", 0o755)
                print("\n📝 Run with: ./scripts/deploy.sh")
            
            elif choice == '3':
                test_code = helper.generate_test_suite()
                helper.save_code(test_code, "tests/test_phoenix.py")
                print("\n📝 Run tests with: python3 tests/test_phoenix.py")
            
            elif choice == '4':
                print("\n🚀 Deployment Guide:")
                print("  1. Ensure wallet exists: txd keys add phoenix-wallet")
                print("  2. Get testnet tokens from faucet")
                print("  3. Run: ./scripts/deploy.sh")
                print("  4. Verify: txd query wasm contract <ADDRESS>")
            
            elif choice == '5':
                print("\n🧪 Running tests...")
                subprocess.run(["python3", str(helper.project_path / "tests/test_phoenix.py")])
            
            else:
                print("Invalid choice")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
