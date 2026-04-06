# Using coreum-js SDK to Interact with TX Network

This tutorial shows how to use the `coreum-js` library for issuing, minting, and sending fungible tokens (FT) and non-fungible tokens (NFT) on TX Blockchain.

## Overview

`coreum-js` is a JavaScript/TypeScript SDK that simplifies interaction with TX Blockchain. It provides:
- Easy client initialization
- Built-in message builders for FT and NFT operations
- Automatic transaction signing and broadcasting
- Query support for balances, tokens, and NFTs

## Prerequisites

- [ ] Node.js 16+ installed
- [ ] npm package manager
- [ ] Funded testnet account (from faucet)

---

## Installation

```bash
# Create project directory
mkdir coreum-js-tutorial
cd coreum-js-tutorial

# Initialize npm project
npm init -y

# Install coreum-js library
npm install coreum-js

# Create main file
touch index.js
package.json
json
{
  "name": "coreum-js-tutorial",
  "version": "1.0.0",
  "description": "TX Blockchain coreum-js tutorial",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "ft": "node ft-example.js",
    "nft": "node nft-example.js"
  },
  "dependencies": {
    "coreum-js": "^1.0.0"
  }
}
Part 1: Issuing, Minting, and Sending FT Token
Step 1: Get a Mnemonic
Go to TX Testnet Faucet

Click "Generate Funded Wallet" button

Copy the mnemonic (12 or 24 words)

⚠️ CAUTION:

Never hardcode your production mnemonic in code

Doing so may result in complete funds loss

Use environment variables or secure key management in production

Step 2: Create FT Example File
bash
touch ft-example.js
Step 3: Complete FT Example Code
javascript
const { Client, Bank, FT } = require("coreum-js");

// ============================================
// CONFIGURATION
// ============================================

// Replace with your own mnemonic from faucet
// Generate at: https://faucet.testnet.tx.dev
const issuerMnemonic = "your twelve or twenty four word mnemonic here";

// IMPORTANT: If using the mnemonic from tutorial, provide unique subunit and symbol
// because tokens within one account must be unique
const subunit = "umyft";
const symbol = "MYFT";

// Network selection: "testnet", "mainnet", or "devnet"
const network = "testnet";

// Recipient address (replace with your own or use the one below)
const receiver = "testcore1xa6mlzdjt669600kwumk35ep0d8gvcyf9z8fww";

// ============================================
// MAIN FUNCTION
// ============================================

async function main() {
    try {
        // ============================================
        // 1. INITIALIZE CLIENT
        // ============================================
        console.log("=== Initializing Client ===");
        
        // Create client for testnet
        const coreum = new Client({ network: network });
        
        // Connect using mnemonic (accesses private key)
        await coreum.connectWithMnemonic(issuerMnemonic);
        
        // Get the issuer address (stored automatically by Client)
        const issuer = coreum.address;
        console.log(`Issuer address: ${issuer}`);
        
        // Define modules we'll use
        const { bank, ft } = coreum.queryClients;
        
        // ============================================
        // 2. ISSUE FUNGIBLE TOKEN (FT)
        // ============================================
        console.log("\n=== Issuing Fungible Token ===");
        
        const issueFtMsg = FT.Issue({
            issuer: issuer,
            symbol: symbol,
            subunit: subunit,
            precision: "6",
            initialAmount: "100000000",
            description: "My first FT token",
            // Features can be: "minting", "burning", "freezing", "whitelisting"
            features: ["minting"],
        });
        console.log("Issue message:", JSON.stringify(issueFtMsg, null, 2));
        
        // Broadcast the transaction
        const issueBroadcastResponse = await coreum.sendTx([issueFtMsg]);
        console.log("Issue broadcast response:", issueBroadcastResponse);
        
        // FT denom is: subunit-issuer_address
        const ftDenom = `${subunit}-${issuer}`;
        console.log(`FT Denom: ${ftDenom}`);
        
        // ============================================
        // 3. QUERY TOKEN DETAILS
        // ============================================
        console.log("\n=== Querying Token Details ===");
        
        const tokenDetails = await ft.token(ftDenom);
        console.log("Token details:", JSON.stringify(tokenDetails, null, 2));
        
        // ============================================
        // 4. MINT MORE TOKENS
        // ============================================
        console.log("\n=== Minting Additional Tokens ===");
        
        const mintFtMsg = FT.Mint({
            sender: issuer,
            coin: {
                denom: ftDenom,
                amount: "1",
            }
        });
        console.log("Mint message:", JSON.stringify(mintFtMsg, null, 2));
        
        const mintBroadcastResponse = await coreum.sendTx([mintFtMsg]);
        console.log("Mint broadcast response:", mintBroadcastResponse);
        
        // ============================================
        // 5. CHECK BALANCE
        // ============================================
        console.log("\n=== Checking Issuer Balance ===");
        
        const issuerBalances = await bank.allBalances(issuer);
        console.log("Issuer balances:", JSON.stringify(issuerBalances, null, 2));
        // Initial: 100,000,000 + Minted: 1 = 100,000,001 ftDenom
        
        // ============================================
        // 6. SEND TOKENS
        // ============================================
        console.log("\n=== Sending Tokens ===");
        
        const bankSendMsg = Bank.Send({
            fromAddress: issuer,
            toAddress: receiver,
            amount: [
                {
                    denom: ftDenom,
                    // amount in subunits: 1,000,000 umyft = 1 MYFT (precision 6)
                    amount: "1000000",
                },
            ],
        });
        console.log("Bank send message:", JSON.stringify(bankSendMsg, null, 2));
        
        const bankSendBroadcastResponse = await coreum.sendTx([bankSendMsg]);
        console.log("Send broadcast response:", bankSendBroadcastResponse);
        
        // ============================================
        // 7. CHECK RECIPIENT BALANCE
        // ============================================
        console.log("\n=== Checking Recipient Balance ===");
        
        const receiverBalances = await bank.allBalances(receiver);
        console.log("Recipient balances:", JSON.stringify(receiverBalances, null, 2));
        
        console.log("\n✅ FT operations completed successfully!");
        
    } catch (error) {
        console.error("Error:", error.message);
        if (error.stack) console.error(error.stack);
    }
}

// Run the example
main();
Step 4: Run FT Example
bash
node ft-example.js
Expected FT Output
text
=== Initializing Client ===
Issuer address: testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== Issuing Fungible Token ===
Issue message: {
  "@type": "/coreum.asset.ft.v1.MsgIssue",
  "issuer": "testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq",
  "symbol": "MYFT",
  "subunit": "umyft",
  "precision": 6,
  "initialAmount": "100000000",
  "description": "My first FT token",
  "features": ["minting"]
}
Issue broadcast response: { code: 0, transactionHash: "0x..." }
FT Denom: umyft-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== Querying Token Details ===
Token details: {
  "token": {
    "denom": "umyft-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq",
    "issuer": "testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq",
    "symbol": "MYFT",
    "precision": 6
  }
}

=== Minting Additional Tokens ===
Mint broadcast response: { code: 0, transactionHash: "0x..." }

=== Checking Issuer Balance ===
Issuer balances: {
  "balances": [
    { "denom": "utestcore", "amount": "999000000" },
    { "denom": "umyft-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq", "amount": "100000001" }
  ]
}

=== Sending Tokens ===
Send broadcast response: { code: 0, transactionHash: "0x..." }

=== Checking Recipient Balance ===
Recipient balances: {
  "balances": [
    { "denom": "umyft-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq", "amount": "1000000" }
  ]
}

✅ FT operations completed successfully!
Part 2: Issuing and Minting NFT Token
Step 1: Create NFT Example File
bash
touch nft-example.js
Step 2: Complete NFT Example Code
javascript
const { Client, NFT, convertStringToAny } = require('coreum-js');

// ============================================
// CONFIGURATION
// ============================================

// Replace with your own mnemonic from faucet
// Generate at: https://faucet.testnet.tx.dev
const issuerMnemonic = "your twelve or twenty four word mnemonic here";

// Network selection: "testnet", "mainnet", or "devnet"
const network = "testnet";

// ============================================
// MAIN FUNCTION
// ============================================

async function main() {
    try {
        // ============================================
        // 1. INITIALIZE CLIENT
        // ============================================
        console.log("=== Initializing Client ===");
        
        // Create client for testnet
        const coreum = new Client({ network: network });
        
        // Connect using mnemonic
        await coreum.connectWithMnemonic(issuerMnemonic);
        
        // Get issuer address
        const issuer = coreum.address;
        console.log(`Issuer address: ${issuer}`);
        
        // ============================================
        // 2. ISSUE NFT CLASS
        // ============================================
        console.log("\n=== Issuing NFT Class ===");
        
        const smartTokenClass = 'CLASS_CUSTOM';
        const classId = `${smartTokenClass}-${issuer}`.toLowerCase();
        console.log(`Class ID: ${classId}`);
        
        const issueNFTMsg = NFT.IssueClass({
            issuer: issuer,
            symbol: smartTokenClass,
            name: smartTokenClass,
            description: "My first Smart Token Class",
            uri: '',
            uriHash: '',
            data: undefined,
            features: [],
            royaltyRate: '0',
        });
        console.log("Issue NFT message:", JSON.stringify(issueNFTMsg, null, 2));
        
        // Broadcast the transaction
        const issueBroadcastResponse = await coreum.sendTx([issueNFTMsg]);
        console.log("Issue broadcast response:", issueBroadcastResponse);
        
        // ============================================
        // 3. MINT NFT
        // ============================================
        console.log("\n=== Minting NFT ===");
        
        // Define NFT ID
        const nftId = `NFT_${smartTokenClass}-0`;
        console.log(`NFT ID: ${nftId}`);
        
        // Prepare encoded data for NFT (can be any string or JSON)
        const nftData = convertStringToAny(JSON.stringify({
            name: "My First NFT",
            description: "This is my first NFT on TX Blockchain",
            image: "ipfs://QmExample",
            attributes: [
                { trait_type: "Rarity", value: "Common" },
                { trait_type: "Color", value: "Blue" }
            ]
        }));
        
        const nftMintMsg = NFT.Mint({
            sender: issuer,
            classId: classId,
            id: nftId,
            uri: '',
            uriHash: '',
            recipient: issuer,
            data: nftData,
        });
        console.log("Mint NFT message:", JSON.stringify(nftMintMsg, null, 2));
        
        // Broadcast the transaction
        const mintBroadcastResponse = await coreum.sendTx([nftMintMsg]);
        console.log("Mint broadcast response:", mintBroadcastResponse);
        
        // ============================================
        // 4. QUERY NFT
        // ============================================
        console.log("\n=== Querying NFT ===");
        
        const { nft } = coreum.queryClients;
        
        const nftDetails = await nft.nFT({
            classId: classId,
            id: nftId,
        });
        console.log("NFT details:", JSON.stringify(nftDetails, null, 2));
        
        // ============================================
        // 5. QUERY NFT OWNER
        // ============================================
        console.log("\n=== Querying NFT Owner ===");
        
        const ownerDetails = await nft.owner({
            classId: classId,
            id: nftId,
        });
        console.log("NFT Owner:", ownerDetails.owner);
        
        console.log("\n✅ NFT operations completed successfully!");
        
    } catch (error) {
        console.error("Error:", error.message);
        if (error.stack) console.error(error.stack);
    }
}

// Run the example
main();
Step 3: Run NFT Example
bash
node nft-example.js
Expected NFT Output
text
=== Initializing Client ===
Issuer address: testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== Issuing NFT Class ===
Class ID: class_custom-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq
Issue broadcast response: { code: 0, transactionHash: "0x..." }

=== Minting NFT ===
NFT ID: NFT_CLASS_CUSTOM-0
Mint broadcast response: { code: 0, transactionHash: "0x..." }

=== Querying NFT ===
NFT details: {
  "nft": {
    "classId": "class_custom-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq",
    "id": "NFT_CLASS_CUSTOM-0",
    "uri": "",
    "uriHash": ""
  }
}

=== Querying NFT Owner ===
NFT Owner: testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

✅ NFT operations completed successfully!
Advanced Examples
Sending NFT to Another Address
javascript
async function sendNFT() {
    const coreum = new Client({ network: "testnet" });
    await coreum.connectWithMnemonic(issuerMnemonic);
    
    const issuer = coreum.address;
    const classId = "class_custom-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq";
    const nftId = "NFT_CLASS_CUSTOM-0";
    const recipient = "testcore1xa6mlzdjt669600kwumk35ep0d8gvcyf9z8fww";
    
    const sendNFTMsg = NFT.Send({
        sender: issuer,
        receiver: recipient,
        classId: classId,
        id: nftId,
    });
    
    const response = await coreum.sendTx([sendNFTMsg]);
    console.log("NFT sent:", response);
}
Burning NFT
javascript
async function burnNFT() {
    const coreum = new Client({ network: "testnet" });
    await coreum.connectWithMnemonic(issuerMnemonic);
    
    const issuer = coreum.address;
    const classId = "class_custom-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq";
    const nftId = "NFT_CLASS_CUSTOM-0";
    
    const burnNFTMsg = NFT.Burn({
        sender: issuer,
        classId: classId,
        id: nftId,
    });
    
    const response = await coreum.sendTx([burnNFTMsg]);
    console.log("NFT burned:", response);
}
Querying All Tokens
javascript
async function queryAllTokens() {
    const coreum = new Client({ network: "testnet" });
    await coreum.connectWithMnemonic(issuerMnemonic);
    
    const { ft } = coreum.queryClients;
    
    // Get all tokens
    const tokens = await ft.tokens({});
    console.log("All tokens:", tokens);
    
    // Get token by denom
    const denom = "umyft-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq";
    const token = await ft.token(denom);
    console.log("Token:", token);
}
Querying All NFTs in a Class
javascript
async function queryNFTsInClass() {
    const coreum = new Client({ network: "testnet" });
    await coreum.connectWithMnemonic(issuerMnemonic);
    
    const { nft } = coreum.queryClients;
    const classId = "class_custom-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq";
    
    const nfts = await nft.nFTs({ classId: classId });
    console.log("NFTs in class:", nfts);
}
Network Configuration
Network	Parameter	Value
Testnet	network	"testnet"
Mainnet	network	"mainnet"
Devnet	network	"devnet"
Custom RPC Endpoint
javascript
const coreum = new Client({ 
    network: "testnet",
    rpcUrl: "https://custom-rpc.testnet.tx.dev:443"
});
FT Features Reference
Feature	Description	Constant
Minting	Allow additional token creation	"minting"
Burning	Allow token destruction	"burning"
Freezing	Allow freezing account balances	"freezing"
Whitelisting	Allow whitelist management	"whitelisting"
FT with Multiple Features
javascript
const issueFtMsg = FT.Issue({
    issuer: issuer,
    symbol: "POWER",
    subunit: "upower",
    precision: "18",
    initialAmount: "1000000000000000000",
    description: "Power Token with full features",
    features: ["minting", "burning", "freezing", "whitelisting"],
});
Error Handling
javascript
async function safeMain() {
    try {
        const coreum = new Client({ network: "testnet" });
        await coreum.connectWithMnemonic(issuerMnemonic);
        
        // Operations...
        
    } catch (error) {
        if (error.message.includes("account sequence mismatch")) {
            console.error("Sequence mismatch - wait and retry");
        } else if (error.message.includes("insufficient funds")) {
            console.error("Insufficient funds - check balance");
        } else if (error.message.includes("already exists")) {
            console.error("Token already exists - use unique symbol/subunit");
        } else {
            console.error("Unexpected error:", error.message);
        }
    }
}
Complete Project Structure
text
coreum-js-tutorial/
├── index.js           # Main entry point
├── ft-example.js      # Fungible token example
├── nft-example.js     # Non-fungible token example
├── package.json
└── node_modules/
Quick Reference
FT Operations
Operation	Method
Issue Token	FT.Issue({...})
Mint Token	FT.Mint({...})
Burn Token	FT.Burn({...})
Freeze Account	FT.Freeze({...})
Query Token	ft.token(denom)
NFT Operations
Operation	Method
Issue Class	NFT.IssueClass({...})
Mint NFT	NFT.Mint({...})
Send NFT	NFT.Send({...})
Burn NFT	NFT.Burn({...})
Query NFT	nft.nFT({...})
Next Steps
Deploy first WASM contract

Create and manage my first FT

IBC Transfer Using CLI

Resources
coreum-js GitHub

TX Testnet Faucet

TX Block Explorer

Network Variables

Gas Price Guide
