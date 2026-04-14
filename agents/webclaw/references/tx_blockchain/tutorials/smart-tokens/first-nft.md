# Create and Manage Non-Fungible Token with CLI

This tutorial will guide you through the process of using the AssetNFT module to create and manage Non-Fungible Tokens (NFT) on TX Blockchain using the command line.

> **Note**: Each subsequent section depends on the previous one. Follow the steps in order.

## Prerequisites

### Step 1: Install txd Binary

Make sure `txd` is installed:

```bash
txd version
# Should output: v6.1.0 or higher
Step 2: Set Up Network Variables
bash
# Chain ID for testnet
export CHAIN_ID="txchain-testnet-1"

# RPC endpoint
export RPC_URL="https://rpc.testnet.tx.dev:443"

# Keyring backend
export KEYRING_BACKEND=test

# Verify settings
echo "Chain ID: $CHAIN_ID"
echo "RPC URL: $RPC_URL"
For other networks (mainnet, devnet), find relevant values on the Network Variables page.

Step 3: Create or Import Accounts
You need two accounts for this tutorial:

NFT Issuer - Creates the NFT class and mints NFTs

NFT Receiver - Receives NFTs

Option A: Generate New Accounts via Faucet
Go to TX Testnet Faucet

Click "Generate Funded Wallet" twice to get two accounts

Save both mnemonics

Option B: Import Existing Accounts
bash
# Import issuer account
txd keys add nft-issuer-wallet --recover --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID
# Enter the issuer mnemonic when prompted

# Import receiver account
txd keys add nft-receiver-wallet --recover --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID
# Enter the receiver mnemonic when prompted
Step 4: Export Addresses to Environment Variables
bash
# Export issuer address
export NFT_ISSUER_ADDRESS=$(txd keys show nft-issuer-wallet --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)

# Export receiver address
export NFT_RECEIVER_ADDRESS=$(txd keys show nft-receiver-wallet --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)

# Verify addresses
echo "Issuer: $NFT_ISSUER_ADDRESS"
echo "Receiver: $NFT_RECEIVER_ADDRESS"
Step 5: Set NFT Class ID
The NFT class ID uniquely identifies a group of NFT objects. It is constructed from the symbol and issuer address:

bash
export NFT_CLASS_ID="puppysmartnft1-$NFT_ISSUER_ADDRESS"
echo "NFT Class ID: $NFT_CLASS_ID"
# Example: puppysmartnft1-testcore105hmczwh0tkha2h5lu9rr07xtegzsm49d3hxq7
Part 1: Create NFT Class
Command Structure
bash
txd tx assetnft issue-class [symbol] [name] [description] [uri] [uri_hash] \
  --from [issuer] \
  --features=burning,freezing,whitelisting,disable_sending \
  [flags]
Parameter Explanation
Parameter	Example	Description
symbol	puppysmartnft1	Unique class identifier
name	"Puppy NFTs"	Display name of the collection
description	"A collection of awesome puppy NFTs"	Human-readable description
uri	"http://puppy-nfts.com"	Metadata URI
uri_hash	"somehash"	Hash of the metadata
Available Features
Feature	Description
burning	Allow NFT owners to burn (destroy) their NFTs
freezing	Allow issuer to freeze specific NFTs
whitelisting	Restrict NFT transfers to whitelisted addresses
disable_sending	Prevent all transfers (issuer can still send)
Issue Class Command
bash
txd tx assetnft issue-class puppysmartnft1 "Puppy NFTs" \
  "A collection of awesome puppy NFTs" \
  "http://puppy-nfts.com" "somehash" \
  --from $NFT_ISSUER_ADDRESS \
  --features=burning,freezing,whitelisting \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Expected Output
json
{
  "code": 0,
  "txhash": "2A4F3E8B9C1D5E6F7A8B9C0D1E2F3A4B5C6D7E8F9A0B1C2D3E4F5A6B7C8D9E0F",
  "raw_log": "[{\"events\":...}]"
}
💡 Important: Copy the transaction hash and go to the Block Explorer to see the transaction status.

Query All NFT Classes
bash
txd query nft classes \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

yaml
classes:
- data: null
  description: A collection of awesome puppy NFTs
  id: puppysmartnft1-testcore105hmczwh0tkha2h5lu9rr07xtegzsm49d3hxq7
  name: Puppy NFTs
  symbol: puppysmartnft1
  uri: http://puppy-nfts.com
  uri_hash: somehash
💡 Note: Your new class ID consists of the symbol provided and the issuer account address.

Part 2: Mint NFTs
Now we will mint NFTs within the created class.

Command Structure
bash
txd tx assetnft mint [class-id] [id] [uri] [uri_hash] --from [sender] [flags]
Mint First NFT
bash
txd tx assetnft mint $NFT_CLASS_ID puppysmartnft-1 \
  "http://puppy-nfts.com/puppynft-1" "somehash" \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Mint Second NFT
bash
txd tx assetnft mint $NFT_CLASS_ID puppysmartnft-2 \
  "http://puppy-nfts.com/puppynft-2" "somehash" \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Query All NFTs in Class
bash
txd query nft nfts \
  --class-id=$NFT_CLASS_ID \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

yaml
nfts:
- class_id: puppysmartnft1-testcore105hmczwh0tkha2h5lu9rr07xtegzsm49d3hxq7
  data: null
  id: puppysmartnft-1
  uri: http://puppy-nfts.com/puppynft-1
  uri_hash: somehash
- class_id: puppysmartnft1-testcore105hmczwh0tkha2h5lu9rr07xtegzsm49d3hxq7
  data: null
  id: puppysmartnft-2
  uri: http://puppy-nfts.com/puppynft-2
  uri_hash: somehash
Part 3: Whitelisting
Since we enabled the whitelisting feature, we must whitelist an address before sending NFTs to it.

Whitelist Command
bash
# Syntax: txd tx assetnft whitelist [class-id] [nft-id] [account] --from [issuer]
txd tx assetnft whitelist $NFT_CLASS_ID puppysmartnft-1 $NFT_RECEIVER_ADDRESS \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Part 4: Sending and Querying NFTs
Send NFT
bash
# Syntax: txd tx nft send [class-id] [nft-id] [receiver] --from [sender]
txd tx nft send $NFT_CLASS_ID puppysmartnft-1 $NFT_RECEIVER_ADDRESS \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Query NFT Balance (Count)
bash
# Query number of NFTs owned by receiver in this class
txd query nft balance $NFT_RECEIVER_ADDRESS $NFT_CLASS_ID \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

text
amount: "1"
Query NFT Owner
bash
# Query owner of a specific NFT
txd query nft owner $NFT_CLASS_ID puppysmartnft-1 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

text
owner: testcore1k9575m9egrlmymnyd29p5g0p5e94d930tg67sv
Part 5: Freezing
Freezing, if enabled for NFT class, allows the issuer to freeze specific NFTs. A frozen NFT cannot be transferred until unfrozen by the issuer.

Freeze NFT
bash
# Syntax: txd tx assetnft freeze [class-id] [nft-id] --from [issuer]
txd tx assetnft freeze $NFT_CLASS_ID puppysmartnft-1 \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Query Frozen Status
bash
# Check if NFT is frozen
txd query assetnft frozen $NFT_CLASS_ID puppysmartnft-1 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

text
frozen: true
Attempt to Send Frozen NFT (Will Fail)
bash
# Try to send frozen NFT back to issuer (should fail)
txd tx nft send $NFT_CLASS_ID puppysmartnft-1 $NFT_ISSUER_ADDRESS \
  --from $NFT_RECEIVER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -b=block
Expected error (in raw_log):

text
nft with classID:... and ID:... is frozen: unauthorized
💡 Note: The -b=block flag waits for the transaction to be committed in a block.

Unfreeze NFT
bash
txd tx assetnft unfreeze $NFT_CLASS_ID puppysmartnft-1 \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Send After Unfreeze (Success)
bash
txd tx nft send $NFT_CLASS_ID puppysmartnft-1 $NFT_ISSUER_ADDRESS \
  --from $NFT_RECEIVER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -b=block
Verify New Owner
bash
txd query nft owner $NFT_CLASS_ID puppysmartnft-1 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output shows the issuer address.

Part 6: Class Freeze
Class freeze freezes all NFTs of a class held by a specific account.

Send NFT Back to Receiver First
bash
txd tx nft send $NFT_CLASS_ID puppysmartnft-1 $NFT_RECEIVER_ADDRESS \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Class Freeze Command
bash
# Freeze all NFTs of this class held by the receiver
txd tx assetnft class-freeze $NFT_CLASS_ID $NFT_RECEIVER_ADDRESS \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -b=block
Attempt to Send During Class Freeze (Will Fail)
bash
txd tx nft send $NFT_CLASS_ID puppysmartnft-1 $NFT_ISSUER_ADDRESS \
  --from $NFT_RECEIVER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -b=block
Expected error (in raw_log):

text
nft with classID:... and ID:... is frozen: unauthorized
Class Unfreeze
bash
# Remove class freeze for the receiver
txd tx assetnft class-unfreeze $NFT_CLASS_ID $NFT_RECEIVER_ADDRESS \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -b=block
Send After Class Unfreeze (Success)
bash
txd tx nft send $NFT_CLASS_ID puppysmartnft-1 $NFT_ISSUER_ADDRESS \
  --from $NFT_RECEIVER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -b=block
Part 7: Burning NFTs
If the burning feature is enabled on NFT class level, an owner can burn (destroy) their NFTs.

Query NFT Before Burning
bash
txd query nft nft $NFT_CLASS_ID puppysmartnft-2 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected output:

yaml
nft:
  class_id: puppysmartnft1-testcore105hmczwh0tkha2h5lu9rr07xtegzsm49d3hxq7
  data: null
  id: puppysmartnft-2
  uri: http://puppy-nfts.com/puppynft-2
  uri_hash: somehash
Burn NFT
bash
# Syntax: txd tx assetnft burn [class-id] [nft-id] --from [owner]
txd tx assetnft burn $NFT_CLASS_ID puppysmartnft-2 \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Verify NFT is Burned
bash
txd query nft nft $NFT_CLASS_ID puppysmartnft-2 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Expected error:

text
not found nft: class: puppysmartnft1-..., id: puppysmartnft-2: nft does not exist: invalid request
Part 8: Update NFT Data
Update the data of a specified NFT with information from a data file.

Create Data File
bash
# Create a JSON data file
cat > /tmp/nft-data.json << EOF
{
  "name": "Updated Puppy NFT",
  "description": "This NFT has been updated!",
  "image": "ipfs://QmUpdatedImage",
  "attributes": [
    { "trait_type": "Breed", "value": "Golden Retriever" },
    { "trait_type": "Age", "value": "2 years" },
    { "trait_type": "Rarity", "value": "Legendary" }
  ]
}
EOF
Update NFT Data
bash
# Syntax: txd tx assetnft update-data [class-id] [nft-id] --from [issuer] --data-file [file]
txd tx assetnft update-data $NFT_CLASS_ID puppysmartnft-1 \
  --from $NFT_ISSUER_ADDRESS \
  --data-file /tmp/nft-data.json \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND
Verify Updated Data
bash
txd query nft nft $NFT_CLASS_ID puppysmartnft-1 \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID
Feature Reference Table
Feature	Command Flag	Description	Who Can Use
Burning	--features=burning	Destroy NFTs	Owner
Freezing	--features=freezing	Lock specific NFTs	Issuer
Whitelisting	--features=whitelisting	Restrict transfers	Issuer
Disable Sending	--features=disable_sending	Prevent all transfers	Issuer
Complete Script Example
bash
#!/bin/bash
# nft-cli-tutorial.sh - Complete NFT CLI tutorial script

set -e

# Configuration
export CHAIN_ID="txchain-testnet-1"
export RPC_URL="https://rpc.testnet.tx.dev:443"
export KEYRING_BACKEND=test

echo "=== Setting up accounts ==="
export NFT_ISSUER_ADDRESS=$(txd keys show nft-issuer-wallet --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)
export NFT_RECEIVER_ADDRESS=$(txd keys show nft-receiver-wallet --address --keyring-backend=$KEYRING_BACKEND --chain-id=$CHAIN_ID)

echo "Issuer: $NFT_ISSUER_ADDRESS"
echo "Receiver: $NFT_RECEIVER_ADDRESS"

export NFT_CLASS_ID="puppysmartnft1-$NFT_ISSUER_ADDRESS"
echo "Class ID: $NFT_CLASS_ID"

echo "=== Creating NFT Class ==="
txd tx assetnft issue-class puppysmartnft1 "Puppy NFTs" \
  "A collection of awesome puppy NFTs" \
  "http://puppy-nfts.com" "somehash" \
  --from $NFT_ISSUER_ADDRESS \
  --features=burning,freezing,whitelisting \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

echo "=== Minting NFTs ==="
txd tx assetnft mint $NFT_CLASS_ID puppysmartnft-1 \
  "http://puppy-nfts.com/puppynft-1" "somehash" \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

txd tx assetnft mint $NFT_CLASS_ID puppysmartnft-2 \
  "http://puppy-nfts.com/puppynft-2" "somehash" \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

echo "=== Whitelisting Receiver ==="
txd tx assetnft whitelist $NFT_CLASS_ID puppysmartnft-1 $NFT_RECEIVER_ADDRESS \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

echo "=== Sending NFT ==="
txd tx nft send $NFT_CLASS_ID puppysmartnft-1 $NFT_RECEIVER_ADDRESS \
  --from $NFT_ISSUER_ADDRESS \
  --node=$RPC_URL \
  --chain-id=$CHAIN_ID \
  --keyring-backend=$KEYRING_BACKEND \
  -y

echo "=== Verifying ==="
echo "Receiver balance:"
txd query nft balance $NFT_RECEIVER_ADDRESS $NFT_CLASS_ID \
  --node=$RPC_URL --chain-id=$CHAIN_ID

echo "NFT owner:"
txd query nft owner $NFT_CLASS_ID puppysmartnft-1 \
  --node=$RPC_URL --chain-id=$CHAIN_ID

echo "✅ NFT CLI tutorial complete!"
FAQ
Can a token always be burned by its owner?
No. When a token is frozen, it cannot be burned. Also, the burning feature must be enabled on the NFT class level.

Does burning feature always need to be enabled to burn a token?
In general, yes. However, the issuer of a token can always burn it (while they own it), regardless of the feature setting.

Can all tokens within an NFT class be frozen/unfrozen at once?
No. There is no single command to freeze all NFTs in a class. However, this can be done programmatically by iterating over the NFTs in a class.

How do I get a list of all NFTs in a class?
bash
txd query nft nfts --class-id=$NFT_CLASS_ID --node=$RPC_URL --chain-id=$CHAIN_ID
Next Steps
Smart FT with WASM

Asset FT Extension

IBC Transfer Using CLI

Resources
AssetNFT Module Documentation

NFT Module Documentation

Network Variables

Testnet Faucet

Block Explorer

