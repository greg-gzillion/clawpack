# Cosmos NFT Module (x/nft)

## Overview
`x/nft` is an implementation of a Cosmos SDK module, per [ADR 43](https://github.com/cosmos/cosmos-sdk/blob/main/docs/architecture/adr-043-nft-module.md), that allows you to:
- Create NFT classifications
- Create NFTs
- Transfer NFTs
- Update NFTs
- Support various queries

The module is fully compatible with the ERC721 specification.

## Relationship to TX Asset NFT Module
┌─────────────────────────────────────────────────────────────┐
│ TX Asset NFT Module (assetnft) │
│ • Custom features (freezing, whitelisting, soulbound) │
│ • Admin controls │
│ • Extended functionality │
└──────────────────────────┬──────────────────────────────────┘
│ wraps
▼
┌─────────────────────────────────────────────────────────────┐
│ Cosmos NFT Module (x/nft) │
│ • Core NFT storage │
│ • Basic transfers │
│ • Class and NFT management │
└─────────────────────────────────────────────────────────────┘

text

The TX Asset NFT module wraps the Cosmos NFT module to add custom features like freezing, whitelisting, soulbound capabilities, and admin controls.

## Concepts

### Class
A `Class` describes the common characteristics of a class of NFTs. Under this class, you can create a variety of NFTs. This is equivalent to an ERC721 contract on Ethereum.

**Class Structure**:
```protobuf
message Class {
  string id = 1;           // Unique identifier
  string name = 2;         // Display name
  string symbol = 3;       // Trading symbol
  string description = 4;  // Description
  string uri = 5;          // Off-chain metadata URI
  string uri_hash = 6;     // Hash of URI content
  google.protobuf.Any data = 7;  // Extensible data
}
NFT (Non-Fungible Token)
NFTs represent unique, non-interchangeable tokens. This implementation is fully compatible with the Ethereum ERC721 standard.

NFT Structure:

protobuf
message NFT {
  string class_id = 1;     // Parent class identifier
  string id = 2;           // Unique NFT identifier within class
  string uri = 3;          // Off-chain metadata URI
  string uri_hash = 4;     // Hash of URI content
  google.protobuf.Any data = 5;  // Extensible data
}
State Management
Class Storage
Stores class definitions keyed by class ID.

text
Key: 0x01 | classID
Value: ProtocolBuffer(Class)
NFT Storage
Stores NFT definitions keyed by class ID and NFT ID.

text
Key: 0x02 | classID | 0x00 | nftID
Value: ProtocolBuffer(NFT)
NFTOfClassByOwner Index
Enables querying all NFTs using classID and owner.

text
Key: 0x03 | owner | 0x00 | classID | 0x00 | nftID
Value: 0x01
Owner Index
Tracks NFT ownership separately from the NFT record.

text
Key: 0x04 | classID | 0x00 | nftID
Value: owner (address)
Total Supply
Tracks the number of NFTs under a specific class.

text
Key: 0x05 | classID
Value: totalSupply (uint64)
State Diagram
text
┌─────────────────────────────────────────────────────────────────┐
│ State Storage Structure │
├─────────────────────────────────────────────────────────────────┤
│ │
│ Class Store │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ classID → Class {id, name, symbol, description, ...} │ │
│ └─────────────────────────────────────────────────────────┘ │
│ │
│ NFT Store │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ (classID, nftID) → NFT {class_id, id, uri, ...} │ │
│ └─────────────────────────────────────────────────────────┘ │
│ │
│ Owner Index │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ (classID, nftID) → owner_address │ │
│ └─────────────────────────────────────────────────────────┘ │
│ │
│ Owner-to-NFT Index │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ (owner, classID, nftID) → 1 │ │
│ └─────────────────────────────────────────────────────────┘ │
│ │
│ Total Supply │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ classID → totalSupply │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
Messages
MsgSend
Transfer ownership of an NFT.

Message Structure:

protobuf
message MsgSend {
  string class_id = 1;   // NFT class ID
  string id = 2;         // NFT ID
  string sender = 3;     // Current owner
  string receiver = 4;   // New owner
}
Validation Rules:

Condition	Failure
Class does not exist	❌ Transaction fails
NFT does not exist	❌ Transaction fails
Sender is not owner	❌ Transaction fails
Example:

bash
txd tx nft send <class-id> <nft-id> <receiver> \
  --from sender \
  --chain-id txchain-testnet-1 \
  --node https://rpc.testnet-1.coreum.dev:443 \
  -y
MsgMint
Create a new NFT within a class.

Note: In the base Cosmos NFT module, minting may be restricted. TX's assetnft module provides public minting with configurable features.

Queries
Class Queries
Query Class:

bash
txd query nft class <class-id> \
  --node https://rpc.testnet-1.coreum.dev:443
Query Classes:

bash
txd query nft classes \
  --node https://rpc.testnet-1.coreum.dev:443
NFT Queries
Query NFT:

bash
txd query nft nft <class-id> <nft-id> \
  --node https://rpc.testnet-1.coreum.dev:443
Query NFTs by Class:

bash
txd query nft nfts --class-id <class-id> \
  --node https://rpc.testnet-1.coreum.dev:443
Query NFTs by Owner:

bash
txd query nft nfts --owner <address> \
  --node https://rpc.testnet-1.coreum.dev:443
Query NFTs by Owner and Class:

bash
txd query nft nfts --owner <address> --class-id <class-id> \
  --node https://rpc.testnet-1.coreum.dev:443
Supply Queries
Query Total Supply:

bash
txd query nft supply --class-id <class-id> \
  --node https://rpc.testnet-1.coreum.dev:443
Events
The nft module emits events for state changes:

EventSend
Emitted when an NFT is transferred.

json
{
  "type": "nft_send",
  "attributes": {
    "class_id": "CLASS_ID",
    "id": "NFT_ID",
    "sender": "sender_address",
    "receiver": "receiver_address"
  }
}
EventMint
Emitted when an NFT is minted.

json
{
  "type": "nft_mint",
  "attributes": {
    "class_id": "CLASS_ID",
    "id": "NFT_ID",
    "owner": "owner_address"
  }
}
EventBurn
Emitted when an NFT is burned.

json
{
  "type": "nft_burn",
  "attributes": {
    "class_id": "CLASS_ID",
    "id": "NFT_ID",
    "owner": "owner_address"
  }
}
ERC721 Compatibility
The x/nft module is designed to be compatible with ERC721, the standard for non-fungible tokens on Ethereum.

ERC721 Method	x/nft Equivalent
balanceOf(address)	Query nfts by owner → count
ownerOf(tokenId)	Query nft → owner from index
safeTransferFrom(from, to, tokenId)	MsgSend
transferFrom(from, to, tokenId)	MsgSend
approve(to, tokenId)	Not implemented (use assetnft for advanced features)
getApproved(tokenId)	Not implemented
setApprovalForAll(operator, approved)	Not implemented
isApprovedForAll(owner, operator)	Not implemented
Extension with Data Field
The data field in both Class and NFT is of type google.protobuf.Any, allowing chains to extend functionality:

protobuf
message Class {
  // ... other fields
  google.protobuf.Any data = 7;  // Custom data
}

message NFT {
  // ... other fields
  google.protobuf.Any data = 5;  // Custom data
}
This enables:

Custom metadata

Chain-specific features

Future extensions without breaking changes

Integration with TX Asset NFT
TX's assetnft module builds on x/nft by:

Feature	x/nft Base	assetnft Enhancement
Minting	Restricted	Public with admin controls
Burning	Not supported	Configurable burning
Freezing	Not supported	Admin freezing capability
Whitelisting	Not supported	Account whitelisting
Soulbound	Not supported	Non-transferable NFTs
Admin controls	No	Full admin management
Proto Definitions
For detailed structure, refer to the proto definitions in the Cosmos SDK codebase:

nft.proto

tx.proto

query.proto

event.proto

References
ADR 43: NFT Module

ERC721 Standard

TX Asset NFT Module

