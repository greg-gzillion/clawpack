# Create and Manage Non-Fungible Token with Golang

This document provides instructions and examples on how to use our `pkg/client` package to create and manage non-fungible tokens (NFT) on TX Blockchain using Go.

## Overview

| Operation | Description |
|-----------|-------------|
| **Issue Class** | Create an NFT class (collection) |
| **Mint NFT** | Create a new NFT within a class |
| **Send NFT** | Transfer NFT to another account |
| **Burn NFT** | Destroy an NFT |
| **Freeze NFT** | Lock an NFT (prevent transfers) |
| **Update Data** | Modify NFT metadata |
| **Transfer Class Admin** | Change class ownership |

## Prerequisites

- [ ] Go 1.21+ installed
- [ ] `txd` module installed (`go get github.com/tokenize-x/tx-chain/v3`)
- [ ] Funded testnet account (from faucet)
- [ ] Completed [Transfer funds with Golang](./transfer-funds.md)

---

## Complete Code

The complete code with `go.mod` file can be found in the [TX Blockchain examples repository](https://github.com/tokenize-x/tx-chain/tree/main/examples/go).

> 💡 **Tip**: If you have issues with `go mod tidy`, copy the `go.mod` file from the example above.

---

## Step 1: Import Required Packages

```go
package main

import (
    "context"
    "crypto/tls"
    "encoding/json"
    "fmt"
    "log"

    "github.com/cosmos/cosmos-sdk/codec"
    codectypes "github.com/cosmos/cosmos-sdk/codec/types"
    "github.com/cosmos/cosmos-sdk/crypto/hd"
    "github.com/cosmos/cosmos-sdk/crypto/keyring"
    sdk "github.com/cosmos/cosmos-sdk/types"
    "github.com/cosmos/cosmos-sdk/types/module"
    "github.com/cosmos/cosmos-sdk/x/auth"
    "github.com/cosmos/cosmos-sdk/x/nft"
    "github.com/cosmos/gogoproto/grpc"
    "google.golang.org/grpc/credentials"

    "github.com/tokenize-x/tx-chain/v3/pkg/client"
    coreumconfig "github.com/tokenize-x/tx-chain/v3/pkg/config"
    "github.com/tokenize-x/tx-chain/v3/pkg/config/constant"
    assetnfttypes "github.com/tokenize-x/tx-chain/v3/x/assetnft/types"
)

const (
    // Get this from faucet - NEVER hardcode in production!
    senderMnemonic = "" // Put your mnemonic here

    chainID          = constant.ChainIDTest
    addressPrefix    = constant.AddressPrefixTest
    nodeAddress      = "grpc.testnet.tx.dev:443"
)
Step 2: Setup Client
go
func setupConfig() {
    config := sdk.GetConfig()
    config.SetBech32PrefixForAccount(addressPrefix, addressPrefix+"pub")
    config.SetCoinType(constant.CoinType)
    config.Seal()
}

func setupClient() (client.Context, client.Factory, *grpc.ClientConn) {
    modules := module.NewBasicManager(
        auth.AppModuleBasic{},
        assetnfttypes.AppModuleBasic{},
        nft.AppModuleBasic{},
    )

    encodingConfig := coreumconfig.NewEncodingConfig(modules)

    pc, ok := encodingConfig.Codec.(codec.GRPCCodecProvider)
    if !ok {
        panic("failed to cast codec to codec.GRPCCodecProvider")
    }

    grpcClient, err := grpc.Dial(
        nodeAddress,
        grpc.WithDefaultCallOptions(grpc.ForceCodec(pc.GRPCCodec())),
        grpc.WithTransportCredentials(credentials.NewTLS(&tls.Config{MinVersion: tls.VersionTLS12})),
    )
    if err != nil {
        panic(err)
    }

    clientCtx := client.NewContext(client.DefaultContextConfig(), modules).
        WithChainID(string(chainID)).
        WithGRPCClient(grpcClient).
        WithKeyring(keyring.NewInMemory(encodingConfig.Codec)).
        WithBroadcastMode(flags.BroadcastSync)

    txFactory := client.Factory{}.
        WithKeybase(clientCtx.Keyring()).
        WithChainID(clientCtx.ChainID()).
        WithTxConfig(clientCtx.TxConfig()).
        WithSimulateAndExecute(true)

    return clientCtx, txFactory, grpcClient
}
Step 3: Create (Issue) an NFT Class
An NFT class is a container for a set of NFTs having the same purpose (like a collection).

go
func issueNFTClass(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    senderAddress sdk.AccAddress,
    symbol, name, description string,
    features []assetnfttypes.ClassFeature,
) (string, error) {
    
    msgIssueClass := &assetnfttypes.MsgIssueClass{
        Issuer:      senderAddress.String(),
        Symbol:      symbol,
        Name:        name,
        Description: description,
        Features:    features,
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgIssueClass,
    )
    if err != nil {
        return "", fmt.Errorf("failed to issue class: %w", err)
    }

    // Build class ID from symbol and issuer address
    classID := assetnfttypes.BuildClassID(symbol, senderAddress)
    
    fmt.Printf("✅ NFT Class issued successfully!\n")
    fmt.Printf("   Symbol: %s\n", symbol)
    fmt.Printf("   Name: %s\n", name)
    fmt.Printf("   Class ID: %s\n", classID)
    
    return classID, nil
}
Class Parameters Explained
Parameter	Example	Description
Symbol	"PUNK"	Unique identifier for the class
Name	"CyberPunks"	Display name of the collection
Description	"Limited edition punks"	Human-readable description
Features	[freezing]	Enabled features for this class
Available Class Features
Feature	Constant	Description
Freezing	assetnfttypes.ClassFeature_freezing	Allow freezing individual NFTs
Whitelisting	assetnfttypes.ClassFeature_whitelisting	Allow whitelist management
Burnable	assetnfttypes.ClassFeature_burnable	Allow NFT burning
go
// Example: Class with freezing feature only
features := []assetnfttypes.ClassFeature{
    assetnfttypes.ClassFeature_freezing,
}

// Example: Class with all features
features := []assetnfttypes.ClassFeature{
    assetnfttypes.ClassFeature_freezing,
    assetnfttypes.ClassFeature_whitelisting,
    assetnfttypes.ClassFeature_burnable,
}
Step 4: Query Class Information
go
func queryClassInfo(
    ctx context.Context,
    clientCtx client.Context,
    classID string,
) (*assetnfttypes.QueryClassResponse, error) {
    
    assetnftClient := assetnfttypes.NewQueryClient(clientCtx)
    
    res, err := assetnftClient.Class(ctx, &assetnfttypes.QueryClassRequest{
        ClassId: classID,
    })
    if err != nil {
        return nil, fmt.Errorf("failed to query class: %w", err)
    }
    
    fmt.Printf("Class Info:\n")
    fmt.Printf("  Class ID: %s\n", res.Class.ClassId)
    fmt.Printf("  Name: %s\n", res.Class.Name)
    fmt.Printf("  Symbol: %s\n", res.Class.Symbol)
    fmt.Printf("  Issuer: %s\n", res.Class.Issuer)
    fmt.Printf("  Features: %v\n", res.Class.Features)
    
    return res, nil
}
Step 5: Mint an NFT
go
func mintNFT(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    senderAddress sdk.AccAddress,
    classID, nftID string,
    data *codectypes.Any, // Optional metadata
) error {
    
    msgMint := &assetnfttypes.MsgMint{
        Sender:  senderAddress.String(),
        ClassID: classID,
        ID:      nftID,
        Data:    data, // Can be nil for no metadata
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgMint,
    )
    if err != nil {
        return fmt.Errorf("failed to mint NFT: %w", err)
    }
    
    fmt.Printf("✅ NFT Minted successfully!\n")
    fmt.Printf("   Class ID: %s\n", classID)
    fmt.Printf("   NFT ID: %s\n", nftID)
    
    return nil
}
Step 6: Query NFT Owner
go
func queryNFTOwner(
    ctx context.Context,
    clientCtx client.Context,
    classID, nftID string,
) (string, error) {
    
    nftClient := nft.NewQueryClient(clientCtx)
    
    resp, err := nftClient.Owner(ctx, &nft.QueryOwnerRequest{
        ClassId: classID,
        Id:      nftID,
    })
    if err != nil {
        return "", fmt.Errorf("failed to query owner: %w", err)
    }
    
    fmt.Printf("NFT Owner: %s\n", resp.Owner)
    return resp.Owner, nil
}
Step 7: Query NFT Details
go
func queryNFTDetails(
    ctx context.Context,
    clientCtx client.Context,
    classID, nftID string,
) (*nft.QueryNFTResponse, error) {
    
    nftClient := nft.NewQueryClient(clientCtx)
    
    resp, err := nftClient.NFT(ctx, &nft.QueryNFTRequest{
        ClassId: classID,
        Id:      nftID,
    })
    if err != nil {
        return nil, fmt.Errorf("failed to query NFT: %w", err)
    }
    
    fmt.Printf("NFT Details:\n")
    fmt.Printf("  Class ID: %s\n", resp.Nft.ClassId)
    fmt.Printf("  ID: %s\n", resp.Nft.Id)
    fmt.Printf("  URI: %s\n", resp.Nft.Uri)
    fmt.Printf("  URI Hash: %s\n", resp.Nft.UriHash)
    
    return resp, nil
}
Step 8: Send NFT
go
func sendNFT(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    senderAddress sdk.AccAddress,
    recipientAddress sdk.AccAddress,
    classID, nftID string,
) error {
    
    msgSend := &nft.MsgSend{
        Sender:   senderAddress.String(),
        Receiver: recipientAddress.String(),
        Id:       nftID,
        ClassId:  classID,
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgSend,
    )
    if err != nil {
        return fmt.Errorf("failed to send NFT: %w", err)
    }
    
    fmt.Printf("✅ NFT Sent successfully!\n")
    fmt.Printf("   From: %s\n", senderAddress.String())
    fmt.Printf("   To: %s\n", recipientAddress.String())
    fmt.Printf("   NFT: %s/%s\n", classID, nftID)
    
    return nil
}
Step 9: Freeze NFT (Requires freezing feature)
go
func freezeNFT(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    adminAddress sdk.AccAddress,
    classID, nftID string,
) error {
    
    msgFreeze := &assetnfttypes.MsgFreeze{
        Sender:  adminAddress.String(),
        ClassID: classID,
        ID:      nftID,
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(adminAddress),
        txFactory,
        msgFreeze,
    )
    if err != nil {
        return fmt.Errorf("failed to freeze NFT: %w", err)
    }
    
    fmt.Printf("✅ NFT Frozen: %s/%s\n", classID, nftID)
    return nil
}

func unfreezeNFT(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    adminAddress sdk.AccAddress,
    classID, nftID string,
) error {
    
    msgUnfreeze := &assetnfttypes.MsgUnfreeze{
        Sender:  adminAddress.String(),
        ClassID: classID,
        ID:      nftID,
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(adminAddress),
        txFactory,
        msgUnfreeze,
    )
    if err != nil {
        return fmt.Errorf("failed to unfreeze NFT: %w", err)
    }
    
    fmt.Printf("✅ NFT Unfrozen: %s/%s\n", classID, nftID)
    return nil
}
Step 10: Burn NFT (Requires burnable feature)
go
func burnNFT(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    ownerAddress sdk.AccAddress,
    classID, nftID string,
) error {
    
    msgBurn := &assetnfttypes.MsgBurn{
        Sender:  ownerAddress.String(),
        ClassID: classID,
        ID:      nftID,
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(ownerAddress),
        txFactory,
        msgBurn,
    )
    if err != nil {
        return fmt.Errorf("failed to burn NFT: %w", err)
    }
    
    fmt.Printf("✅ NFT Burned: %s/%s\n", classID, nftID)
    return nil
}
Step 11: Update NFT Data (Dynamic NFT)
go
func mintDynamicNFT(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    senderAddress sdk.AccAddress,
    classID, nftID string,
    initialData []byte,
) error {
    
    // Create dynamic data structure
    dataDynamic := assetnfttypes.DataDynamic{
        Items: []assetnfttypes.DataDynamicItem{
            {
                Editors: []assetnfttypes.DataEditor{
                    assetnfttypes.DataEditor_owner,
                },
                Data: initialData,
            },
        },
    }
    
    // Convert to Any type
    data, err := codectypes.NewAnyWithValue(&dataDynamic)
    if err != nil {
        return fmt.Errorf("failed to create dynamic data: %w", err)
    }
    
    msgMint := &assetnfttypes.MsgMint{
        Sender:  senderAddress.String(),
        ClassID: classID,
        ID:      nftID,
        Data:    data,
    }
    
    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgMint,
    )
    if err != nil {
        return fmt.Errorf("failed to mint dynamic NFT: %w", err)
    }
    
    fmt.Printf("✅ Dynamic NFT Minted: %s/%s\n", classID, nftID)
    return nil
}

func updateNFTData(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    senderAddress sdk.AccAddress,
    classID, nftID string,
    itemIndex uint64,
    newData []byte,
) error {
    
    msgUpdateData := &assetnfttypes.MsgUpdateData{
        Sender:  senderAddress.String(),
        ClassID: classID,
        ID:      nftID,
        Items: []assetnfttypes.DataDynamicIndexedItem{
            {
                Index: itemIndex,
                Data:  newData,
            },
        },
    }
    
    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgUpdateData,
    )
    if err != nil {
        return fmt.Errorf("failed to update NFT data: %w", err)
    }
    
    fmt.Printf("✅ NFT Data Updated: %s/%s\n", classID, nftID)
    return nil
}
Step 12: Transfer Class Admin
go
func transferClassAdmin(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    currentAdmin sdk.AccAddress,
    newAdmin sdk.AccAddress,
    classID string,
) error {
    
    msgTransferClass := &assetnfttypes.MsgTransferClass{
        Sender:  currentAdmin.String(),
        ClassID: classID,
        Account: newAdmin.String(),
    }
    
    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(currentAdmin),
        txFactory,
        msgTransferClass,
    )
    if err != nil {
        return fmt.Errorf("failed to transfer class admin: %w", err)
    }
    
    fmt.Printf("✅ Class Admin Transferred from %s to %s\n", 
        currentAdmin.String(), newAdmin.String())
    return nil
}
Complete Example: Full NFT Lifecycle
go
package main

import (
    "context"
    "crypto/tls"
    "encoding/json"
    "fmt"
    "log"

    "github.com/cosmos/cosmos-sdk/codec"
    codectypes "github.com/cosmos/cosmos-sdk/codec/types"
    "github.com/cosmos/cosmos-sdk/crypto/hd"
    "github.com/cosmos/cosmos-sdk/crypto/keyring"
    sdk "github.com/cosmos/cosmos-sdk/types"
    "github.com/cosmos/cosmos-sdk/types/module"
    "github.com/cosmos/cosmos-sdk/x/auth"
    "github.com/cosmos/cosmos-sdk/x/nft"
    "github.com/cosmos/gogoproto/grpc"
    "google.golang.org/grpc/credentials"

    "github.com/tokenize-x/tx-chain/v3/pkg/client"
    coreumconfig "github.com/tokenize-x/tx-chain/v3/pkg/config"
    "github.com/tokenize-x/tx-chain/v3/pkg/config/constant"
    assetnfttypes "github.com/tokenize-x/tx-chain/v3/x/assetnft/types"
)

const (
    senderMnemonic = "your twelve word mnemonic here"
    
    chainID       = constant.ChainIDTest
    addressPrefix = constant.AddressPrefixTest
    nodeAddress   = "grpc.testnet.tx.dev:443"
)

func main() {
    // Setup
    setupConfig()
    clientCtx, txFactory, grpcClient := setupClient()
    defer grpcClient.Close()

    // Import sender account
    senderInfo, err := clientCtx.Keyring().NewAccount(
        "sender",
        senderMnemonic,
        "",
        sdk.GetConfig().GetFullBIP44Path(),
        hd.Secp256k1,
    )
    if err != nil {
        log.Fatalf("Failed to import account: %v", err)
    }

    senderAddress, err := senderInfo.GetAddress()
    if err != nil {
        log.Fatalf("Failed to get address: %v", err)
    }
    fmt.Printf("Sender Address: %s\n", senderAddress.String())

    ctx := context.Background()

    // Create recipient account
    recipientInfo, _, err := clientCtx.Keyring().NewMnemonic(
        "recipient",
        keyring.English,
        sdk.GetConfig().GetFullBIP44Path(),
        "",
        hd.Secp256k1,
    )
    if err != nil {
        log.Fatalf("Failed to create recipient: %v", err)
    }

    recipientAddress, err := recipientInfo.GetAddress()
    if err != nil {
        log.Fatalf("Failed to get recipient address: %v", err)
    }
    fmt.Printf("Recipient Address: %s\n", recipientAddress.String())

    // ============================================
    // Step 1: Issue NFT Class
    // ============================================
    fmt.Println("\n=== 1. Issuing NFT Class ===")
    
    classSymbol := "PUNK"
    features := []assetnfttypes.ClassFeature{
        assetnfttypes.ClassFeature_freezing,
        assetnfttypes.ClassFeature_burnable,
    }
    
    msgIssueClass := &assetnfttypes.MsgIssueClass{
        Issuer:      senderAddress.String(),
        Symbol:      classSymbol,
        Name:        "CyberPunks Collection",
        Description: "Limited edition cyberpunk avatars",
        Features:    features,
    }
    
    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgIssueClass,
    )
    if err != nil {
        log.Fatalf("Failed to issue class: %v", err)
    }
    
    classID := assetnfttypes.BuildClassID(classSymbol, senderAddress)
    fmt.Printf("Class ID: %s\n", classID)

    // ============================================
    // Step 2: Mint Static NFT
    // ============================================
    fmt.Println("\n=== 2. Minting Static NFT ===")
    
    nftID := "punk-001"
    msgMint := &assetnfttypes.MsgMint{
        Sender:  senderAddress.String(),
        ClassID: classID,
        ID:      nftID,
    }
    
    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgMint,
    )
    if err != nil {
        log.Fatalf("Failed to mint NFT: %v", err)
    }
    fmt.Printf("Minted NFT: %s/%s\n", classID, nftID)

    // ============================================
    // Step 3: Query NFT Owner
    // ============================================
    fmt.Println("\n=== 3. Querying NFT Owner ===")
    
    nftClient := nft.NewQueryClient(clientCtx)
    ownerResp, err := nftClient.Owner(ctx, &nft.QueryOwnerRequest{
        ClassId: classID,
        Id:      nftID,
    })
    if err != nil {
        log.Fatalf("Failed to query owner: %v", err)
    }
    fmt.Printf("Owner: %s\n", ownerResp.Owner)

    // ============================================
    // Step 4: Send NFT to Recipient
    // ============================================
    fmt.Println("\n=== 4. Sending NFT ===")
    
    msgSend := &nft.MsgSend{
        Sender:   senderAddress.String(),
        Receiver: recipientAddress.String(),
        Id:       nftID,
        ClassId:  classID,
    }
    
    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgSend,
    )
    if err != nil {
        log.Fatalf("Failed to send NFT: %v", err)
    }
    fmt.Printf("Sent NFT from %s to %s\n", senderAddress.String(), recipientAddress.String())

    // ============================================
    // Step 5: Verify New Owner
    // ============================================
    fmt.Println("\n=== 5. Verifying New Owner ===")
    
    ownerResp, err = nftClient.Owner(ctx, &nft.QueryOwnerRequest{
        ClassId: classID,
        Id:      nftID,
    })
    if err != nil {
        log.Fatalf("Failed to query owner: %v", err)
    }
    fmt.Printf("New Owner: %s\n", ownerResp.Owner)

    // ============================================
    // Step 6: Freeze NFT (Admin only)
    // ============================================
    fmt.Println("\n=== 6. Freezing NFT ===")
    
    msgFreeze := &assetnfttypes.MsgFreeze{
        Sender:  senderAddress.String(),
        ClassID: classID,
        ID:      nftID,
    }
    
    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgFreeze,
    )
    if err != nil {
        log.Fatalf("Failed to freeze NFT: %v", err)
    }
    fmt.Printf("Frozen NFT: %s/%s\n", classID, nftID)

    // ============================================
    // Step 7: Mint Dynamic NFT with Metadata
    // ============================================
    fmt.Println("\n=== 7. Minting Dynamic NFT ===")
    
    dynamicNFTID := "dynamic-punk-001"
    
    // Initial metadata
    initialMetadata := map[string]interface{}{
        "name":        "Dynamic Punk #1",
        "description": "An NFT with updatable metadata",
        "image":       "ipfs://QmExample",
        "attributes": []map[string]interface{}{
            {"trait_type": "Background", "value": "Purple"},
            {"trait_type": "Eyes", "value": "Blue"},
            {"trait_type": "Mouth", "value": "Smile"},
        },
    }
    
    initialData, err := json.Marshal(initialMetadata)
    if err != nil {
        log.Fatalf("Failed to marshal metadata: %v", err)
    }
    
    dataDynamic := assetnfttypes.DataDynamic{
        Items: []assetnfttypes.DataDynamicItem{
            {
                Editors: []assetnfttypes.DataEditor{
                    assetnfttypes.DataEditor_owner,
                },
                Data: initialData,
            },
        },
    }
    
    data, err := codectypes.NewAnyWithValue(&dataDynamic)
    if err != nil {
        log.Fatalf("Failed to create dynamic data: %v", err)
    }
    
    msgMintDynamic := &assetnfttypes.MsgMint{
        Sender:  senderAddress.String(),
        ClassID: classID,
        ID:      dynamicNFTID,
        Data:    data,
    }
    
    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgMintDynamic,
    )
    if err != nil {
        log.Fatalf("Failed to mint dynamic NFT: %v", err)
    }
    fmt.Printf("Minted Dynamic NFT: %s/%s\n", classID, dynamicNFTID)

    // ============================================
    // Step 8: Query Dynamic NFT Data
    // ============================================
    fmt.Println("\n=== 8. Querying Dynamic NFT Data ===")
    
    nftResp, err := nftClient.NFT(ctx, &nft.QueryNFTRequest{
        ClassId: classID,
        Id:      dynamicNFTID,
    })
    if err != nil {
        log.Fatalf("Failed to query NFT: %v", err)
    }
    
    var storedDataDynamic assetnfttypes.DataDynamic
    err = storedDataDynamic.Unmarshal(nftResp.Nft.Data.Value)
    if err != nil {
        log.Fatalf("Failed to unmarshal data: %v", err)
    }
    fmt.Printf("NFT Data: %s\n", string(storedDataDynamic.Items[0].Data))

    // ============================================
    // Step 9: Update Dynamic NFT Data
    // ============================================
    fmt.Println("\n=== 9. Updating Dynamic NFT Data ===")
    
    updatedMetadata := map[string]interface{}{
        "name":        "Dynamic Punk #1 (Updated)",
        "description": "This NFT has been updated!",
        "image":       "ipfs://QmUpdatedExample",
        "attributes": []map[string]interface{}{
            {"trait_type": "Background", "value": "Neon Blue"},
            {"trait_type": "Eyes", "value": "Green"},
            {"trait_type": "Mouth", "value": "Laughing"},
            {"trait_type": "Rarity", "value": "Legendary"},
        },
    }
    
    updatedData, err := json.Marshal(updatedMetadata)
    if err != nil {
        log.Fatalf("Failed to marshal updated metadata: %v", err)
    }
    
    msgUpdateData := &assetnfttypes.MsgUpdateData{
        Sender:  senderAddress.String(),
        ClassID: classID,
        ID:      dynamicNFTID,
        Items: []assetnfttypes.DataDynamicIndexedItem{
            {
                Index: 0,
                Data:  updatedData,
            },
        },
    }
    
    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgUpdateData,
    )
    if err != nil {
        log.Fatalf("Failed to update NFT data: %v", err)
    }
    fmt.Println("NFT Data Updated!")

    // ============================================
    // Step 10: Verify Updated Data
    // ============================================
    fmt.Println("\n=== 10. Verifying Updated Data ===")
    
    nftResp, err = nftClient.NFT(ctx, &nft.QueryNFTRequest{
        ClassId: classID,
        Id:      dynamicNFTID,
    })
    if err != nil {
        log.Fatalf("Failed to query NFT: %v", err)
    }
    
    err = storedDataDynamic.Unmarshal(nftResp.Nft.Data.Value)
    if err != nil {
        log.Fatalf("Failed to unmarshal data: %v", err)
    }
    fmt.Printf("Updated NFT Data: %s\n", string(storedDataDynamic.Items[0].Data))

    // ============================================
    // Step 11: Query All NFTs in Class
    // ============================================
    fmt.Println("\n=== 11. Querying All NFTs in Class ===")
    
    nftsResp, err := nftClient.NFTs(ctx, &nft.QueryNFTsRequest{
        ClassId: classID,
    })
    if err != nil {
        log.Fatalf("Failed to query NFTs: %v", err)
    }
    
    fmt.Printf("Total NFTs in class: %d\n", len(nftsResp.Nfts))
    for _, nftItem := range nftsResp.Nfts {
        fmt.Printf("  - %s\n", nftItem.Id)
    }

    fmt.Println("\n✅ NFT management complete!")
}
Expected Output
text
Sender Address: testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq
Recipient Address: testcore1x8k5y8v5f8zq7p3x2w4l8k9j3h5g2f1d8s7a6d

=== 1. Issuing NFT Class ===
Class ID: punk-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== 2. Minting Static NFT ===
Minted NFT: punk-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq/punk-001

=== 3. Querying NFT Owner ===
Owner: testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== 4. Sending NFT ===
Sent NFT from testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq to testcore1x8k5y8v5f8zq7p3x2w4l8k9j3h5g2f1d8s7a6d

=== 5. Verifying New Owner ===
New Owner: testcore1x8k5y8v5f8zq7p3x2w4l8k9j3h5g2f1d8s7a6d

=== 6. Freezing NFT ===
Frozen NFT: punk-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq/punk-001

=== 7. Minting Dynamic NFT ===
Minted Dynamic NFT: punk-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq/dynamic-punk-001

=== 8. Querying Dynamic NFT Data ===
NFT Data: {"name":"Dynamic Punk #1","description":"An NFT with updatable metadata","image":"ipfs://QmExample","attributes":[{"trait_type":"Background","value":"Purple"},{"trait_type":"Eyes","value":"Blue"},{"trait_type":"Mouth","value":"Smile"}]}

=== 9. Updating Dynamic NFT Data ===
NFT Data Updated!

=== 10. Verifying Updated Data ===
Updated NFT Data: {"name":"Dynamic Punk #1 (Updated)","description":"This NFT has been updated!","image":"ipfs://QmUpdatedExample","attributes":[{"trait_type":"Background","value":"Neon Blue"},{"trait_type":"Eyes","value":"Green"},{"trait_type":"Mouth","value":"Laughing"},{"trait_type":"Rarity","value":"Legendary"}]}

=== 11. Querying All NFTs in Class ===
Total NFTs in class: 2
  - punk-001
  - dynamic-punk-001

✅ NFT management complete!
Error Handling
go
// Check for specific NFT errors
if err != nil {
    if strings.Contains(err.Error(), "class not found") {
        fmt.Println("NFT class does not exist")
    } else if strings.Contains(err.Error(), "nft not found") {
        fmt.Println("NFT ID not found in class")
    } else if strings.Contains(err.Error(), "unauthorized") {
        fmt.Println("Not authorized - check class admin or owner")
    } else if strings.Contains(err.Error(), "feature not enabled") {
        fmt.Println("This feature was not enabled during class issuance")
    } else if strings.Contains(err.Error(), "frozen") {
        fmt.Println("NFT is frozen and cannot be transferred")
    } else {
        fmt.Printf("Unexpected error: %v\n", err)
    }
}
Data Editor Types
Editor	Constant	Description
Owner	assetnfttypes.DataEditor_owner	NFT owner can edit data
Issuer	assetnfttypes.DataEditor_issuer	Class issuer can edit data
Whitelist	assetnfttypes.DataEditor_whitelist	Whitelisted accounts can edit data
go
// Example: Allow both owner and issuer to edit
dataDynamic := assetnfttypes.DataDynamic{
    Items: []assetnfttypes.DataDynamicItem{
        {
            Editors: []assetnfttypes.DataEditor{
                assetnfttypes.DataEditor_owner,
                assetnfttypes.DataEditor_issuer,
            },
            Data: initialData,
        },
    },
}
Next Steps
Smart FT with WASM

Deploy first WASM contract

IBC Transfer Using CLI

Resources
AssetNFT Module Documentation

NFT Module Documentation

TX Blockchain Go Client

Testnet Faucet

Block Explorer
