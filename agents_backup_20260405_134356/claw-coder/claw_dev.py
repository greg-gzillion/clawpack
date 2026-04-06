#!/usr/bin/env python3
"""
Claw-Coder Dev Assistant - Generates and Tests PhoenixPME Code
"""

import os
import glob
import re
import subprocess
import tempfile
from pathlib import Path

class ClawDev:
    def __init__(self):
        self.docs = []
        self.phoenix_path = "/home/greg/dev/TX"  # Your PhoenixPME code
        self._load_tx_docs()
    
    def _load_tx_docs(self):
        """Load TX documentation for reference"""
        docs_path = "/home/greg/dev/TXdocumentation"
        
        tx_docs = [
            '03-smart-tokens.md',
            '02-smart-contracts.md', 
            'first-ft.md',
            'smart-ft-acl.md',
            'validator',
            'dex/overview.md',
            'feemodel'
        ]
        
        for fp in glob.glob(f"{docs_path}/**/*.md", recursive=True):
            rel = os.path.relpath(fp, docs_path)
            
            # Skip PhoenixPME files
            if 'phoenixpme' in rel:
                continue
            
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if relevant
                is_relevant = False
                for pattern in tx_docs:
                    if pattern.lower() in rel.lower() or pattern.lower() in content.lower()[:500]:
                        is_relevant = True
                        break
                
                if is_relevant and len(content) > 200:
                    # Extract code examples
                    code_blocks = re.findall(r'```(?:bash|rust|go|javascript|typescript)?\n(.*?)```', content, re.DOTALL)
                    commands = re.findall(r'^\s*(txd\s+[^\n]+)$', content, re.MULTILINE)
                    
                    self.docs.append({
                        'file': rel,
                        'content': content,
                        'code_blocks': code_blocks[:3],
                        'commands': commands[:5]
                    })
            except:
                pass
        
        print(f"✅ Loaded {len(self.docs)} TX reference docs")
    
    def find_relevant_docs(self, query):
        """Find documentation relevant to query"""
        query_lower = query.lower()
        results = []
        
        for doc in self.docs:
            score = 0
            if query_lower in doc['content'].lower():
                score = doc['content'].lower().count(query_lower)
            if score > 0:
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results[:3]]
    
    def generate_code(self, request):
        """Generate code based on request"""
        request_lower = request.lower()
        
        # Find relevant docs
        docs = self.find_relevant_docs(request)
        
        # Code templates for common PhoenixPME operations
        templates = {
            'token': {
                'description': 'Create a Smart Token',
                'code': '''// Create Fungible Token on TX Blockchain
const { DirectSecp256k1HdWallet } = require("@cosmjs/proto-signing");
const { calculateFee, GasPrice } = require("@cosmjs/stargate");
const { TxClient } = require("@coreum/coreum-js");

async function createToken() {
    // 1. Setup wallet
    const mnemonic = "your mnemonic here";
    const wallet = await DirectSecp256k1HdWallet.fromMnemonic(mnemonic, {
        prefix: "tx",
    });
    
    // 2. Connect to TX chain
    const rpcEndpoint = "https://rpc.testnet-1.coreum.dev:443";
    const client = await TxClient.connect(rpcEndpoint, wallet);
    
    // 3. Create token parameters
    const tokenParams = {
        symbol: "PME",
        name: "PhoenixPME Token",
        decimals: 6,
        initialSupply: "1000000000", // 1 billion
        features: ["minting", "burning", "freezing", "clawback"]
    };
    
    // 4. Issue token
    const msg = {
        typeUrl: "/coreum.asset.ft.v1.MsgIssue",
        value: {
            issuer: (await wallet.getAccounts())[0].address,
            symbol: tokenParams.symbol,
            name: tokenParams.name,
            decimals: tokenParams.decimals,
            initialSupply: tokenParams.initialSupply,
            features: tokenParams.features
        }
    };
    
    const fee = calculateFee(200000, GasPrice.fromString("0.1utx"));
    const result = await client.signAndBroadcast([msg], fee);
    
    console.log("Token created:", result.transactionHash);
    return result;
}

createToken().catch(console.error);''',
                'test': '''// Test token creation
const assert = require("assert");

async function testTokenCreation() {
    // Mock client for testing
    let tokenCreated = false;
    
    // Simulate token creation
    const result = await createToken();
    
    assert(result.transactionHash, "Transaction hash should exist");
    assert(result.code === 0, "Transaction should succeed");
    
    console.log("✅ Token creation test passed");
    return true;
}'''
            },
            
            'validator': {
                'description': 'Setup validator',
                'code': '''#!/bin/bash
# Setup TX Validator Node

# 1. Install txd
cd ~
git clone https://github.com/greg-gzillion/TX.git
cd TX
make install

# 2. Initialize node
txd init "PhoenixPME Validator" --chain-id txchain-mainnet-1

# 3. Create wallet
txd keys add validator-wallet

# 4. Create validator
txd tx staking create-validator \\
  --amount=1000000utx \\
  --pubkey=$(txd tendermint show-validator) \\
  --moniker="PhoenixPME Validator" \\
  --chain-id=txchain-mainnet-1 \\
  --from=validator-wallet \\
  --commission-rate="0.10" \\
  --commission-max-rate="0.20" \\
  --commission-max-change-rate="0.01" \\
  --min-self-delegation="1" \\
  -y

# 5. Check validator
txd query staking validator $(txd keys show validator-wallet -a)''',
                'test': '''#!/bin/bash
# Test validator setup

# Check if txd is installed
if ! command -v txd &> /dev/null; then
    echo "❌ txd not installed"
    exit 1
fi

# Check if validator exists
VALIDATOR_ADDR=$(txd keys show validator-wallet -a 2>/dev/null)
if [ -z "$VALIDATOR_ADDR" ]; then
    echo "❌ Validator wallet not found"
    exit 1
fi

echo "✅ Validator setup verified"
'''
            },
            
            'dex': {
                'description': 'DEX Order Placement',
                'code': '''// Place DEX Order for PME token
async function placeDEXOrder(orderType, baseDenom, quoteDenom, amount, price) {
    const client = await getClient();
    
    const msg = {
        typeUrl: "/coreum.dex.v1.MsgPlaceOrder",
        value: {
            creator: (await client.getAccounts())[0].address,
            base_denom: baseDenom,
            quote_denom: quoteDenom,
            order_type: orderType, // "BUY" or "SELL"
            price: price.toString(),
            quantity: amount.toString()
        }
    };
    
    const fee = calculateFee(150000, GasPrice.fromString("0.1utx"));
    const result = await client.signAndBroadcast([msg], fee);
    
    console.log(`Order placed: ${orderType} ${amount} ${baseDenom} @ ${price} ${quoteDenom}`);
    return result;
}

// Example: Buy PME tokens
await placeDEXOrder("BUY", "upme", "utx", "1000000", "0.05");''',
                'test': '// Test DEX order validation\nassert(price > 0, "Price must be positive");\nassert(amount > 0, "Amount must be positive");'
            }
        }
        
        # Determine which template to use
        for key, template in templates.items():
            if key in request_lower:
                return template
        
        # Generate custom response using docs
        if docs:
            doc = docs[0]
            # Extract code from documentation
            if doc['code_blocks']:
                return {
                    'description': f'From {doc["file"]}',
                    'code': doc['code_blocks'][0],
                    'test': '# Test this code in your PhoenixPME environment'
                }
        
        return None
    
    def save_and_test(self, code, filename):
        """Save generated code and test it"""
        test_file = Path(tempfile.gettempdir()) / filename
        
        with open(test_file, 'w') as f:
            f.write(code)
        
        print(f"\n📁 Code saved to: {test_file}")
        
        # Try to run/test based on file type
        if filename.endswith('.js'):
            try:
                result = subprocess.run(['node', str(test_file)], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"\n✅ Test passed!\n{result.stdout}")
                else:
                    print(f"\n⚠️ Test had issues:\n{result.stderr}")
            except FileNotFoundError:
                print("\n⚠️ Node.js not found. Install to test JavaScript code.")
            except subprocess.TimeoutExpired:
                print("\n⚠️ Test timed out")
        elif filename.endswith('.sh'):
            os.chmod(test_file, 0o755)
            try:
                result = subprocess.run([str(test_file)], 
                                      capture_output=True, text=True, timeout=30)
                print(f"\n📤 Output:\n{result.stdout}")
                if result.stderr:
                    print(f"⚠️ Errors:\n{result.stderr}")
            except Exception as e:
                print(f"\n⚠️ Error running script: {e}")
        
        return test_file

def main():
    agent = ClawDev()
    
    print("=" * 70)
    print("🦞 Claw-Coder Dev Assistant - Code Generator & Tester")
    print("=" * 70)
    print("\nI can generate and test code for PhoenixPME on TX blockchain.")
    print("\n💬 Ask me to:")
    print("   • 'Generate token creation code'")
    print("   • 'Create validator setup script'")
    print("   • 'Build DEX order placement'")
    print("   • 'Write a smart contract'")
    print("   • 'Test my code'")
    print("\nCommands: /test <file>, /save, /docs <topic>, exit")
    print("=" * 70)
    
    last_code = None
    
    while True:
        try:
            user_input = input("\n🦞 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("\n👋 Ready to build on TX!")
                break
            
            if user_input.startswith('/test '):
                filepath = user_input[6:]
                if os.path.exists(filepath):
                    print(f"\n🧪 Testing {filepath}...")
                    result = subprocess.run(['python3', filepath], capture_output=True, text=True)
                    print(result.stdout)
                    if result.stderr:
                        print(f"Errors: {result.stderr}")
                else:
                    print(f"\n❌ File not found: {filepath}")
                continue
            
            if user_input.startswith('/docs '):
                topic = user_input[6:]
                docs = agent.find_relevant_docs(topic)
                if docs:
                    print(f"\n📚 Documentation for '{topic}':")
                    for doc in docs[:2]:
                        print(f"\n📄 {doc['file']}")
                        # Show first relevant paragraph
                        lines = doc['content'].split('\n')
                        for line in lines[:10]:
                            if len(line.strip()) > 40:
                                print(f"   {line.strip()[:100]}")
                                break
                else:
                    print(f"\n❌ No docs found for '{topic}'")
                continue
            
            # Generate code
            template = agent.generate_code(user_input)
            
            if template:
                print(f"\n📝 **{template['description']}**")
                print("\n```" + ("javascript" if "require" in template['code'] else "bash"))
                print(template['code'])
                print("```")
                
                if template['test']:
                    print("\n🧪 **Test Code:**")
                    print("```javascript")
                    print(template['test'])
                    print("```")
                
                print("\n💾 Save this code? (yes/no)")
                save_response = input("> ").strip().lower()
                
                if save_response in ['yes', 'y']:
                    filename = input("Filename (e.g., create_token.js): ").strip()
                    if not filename:
                        filename = "generated_code.js"
                    
                    agent.save_and_test(template['code'], filename)
            else:
                print("\n❌ I couldn't generate code for that request.")
                print("\n💡 Try specific requests like:")
                print("   • 'Generate token creation code'")
                print("   • 'Create validator setup'")
                print("   • 'Build DEX order'")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
