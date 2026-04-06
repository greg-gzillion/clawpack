# Create and Manage Fungible Token with Golang

This document provides instructions and examples on how to use our `pkg/client` package to create and manage fungible tokens (FT) on TX Blockchain using Go.

## Overview

| Operation | Description |
|-----------|-------------|
| **Issue** | Create a new fungible token |
| **Mint** | Increase token supply |
| **Burn** | Decrease token supply |
| **Send** | Transfer tokens between accounts |
| **Freeze** | Lock portion of an account's balance |
| **Transfer Admin** | Change token administration |
| **Clear Admin** | Remove administrative rights |

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
    "fmt"
    "log"

    "github.com/cosmos/cosmos-sdk/codec"
    "github.com/cosmos/cosmos-sdk/crypto/hd"
    "github.com/cosmos/cosmos-sdk/crypto/keyring"
    sdk "github.com/cosmos/cosmos-sdk/types"
    sdkmath "github.com/cosmos/cosmos-sdk/types/math"
    "github.com/cosmos/cosmos-sdk/types/module"
    "github.com/cosmos/cosmos-sdk/x/auth"
    banktypes "github.com/cosmos/cosmos-sdk/x/bank/types"
    "github.com/cosmos/gogoproto/grpc"
    "google.golang.org/grpc/credentials"

    "github.com/tokenize-x/tx-chain/v3/pkg/client"
    coreumconfig "github.com/tokenize-x/tx-chain/v3/pkg/config"
    "github.com/tokenize-x/tx-chain/v3/pkg/config/constant"
    assetfttypes "github.com/tokenize-x/tx-chain/v3/x/assetft/types"
)

const (
    // Get this from faucet - NEVER hardcode in production!
    senderMnemonic = "" // Put your mnemonic here

    chainID          = constant.ChainIDTest
    addressPrefix    = constant.AddressPrefixTest
    denom            = constant.DenomTest
    nodeAddress      = "grpc.testnet.tx.dev:443"
)
Step 2: Setup Client (Same as Transfer Tutorial)
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
        assetfttypes.AppModuleBasic{},
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
Step 3: Create (Issue) a Fungible Token
go
func issueToken(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    senderAddress sdk.AccAddress,
    symbol, subunit, description string,
    precision uint32,
    initialAmount int64,
    features []assetfttypes.Feature,
) error {
    
    msgIssue := &assetfttypes.MsgIssue{
        Issuer:        senderAddress.String(),
        Symbol:        symbol,
        Subunit:       subunit,
        Precision:     precision,
        InitialAmount: sdkmath.NewInt(initialAmount),
        Description:   description,
        Features:      features,
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgIssue,
    )
    if err != nil {
        return fmt.Errorf("failed to issue token: %w", err)
    }

    fmt.Printf("✅ Token issued successfully!\n")
    fmt.Printf("   Symbol: %s\n", symbol)
    fmt.Printf("   Subunit: %s\n", subunit)
    fmt.Printf("   Denom: %s-%s\n", subunit, senderAddress.String())
    fmt.Printf("   Initial Supply: %d %s\n", initialAmount, subunit)
    
    return nil
}
Token Parameters Explained
Parameter	Example	Description
Symbol	"ABC"	Display name for UI purposes
Subunit	"uabc"	On-chain denomination (minimum unit)
Precision	6	Decimal places (1,000,000 subunit = 1 symbol)
InitialAmount	100,000,000	Initial supply in subunit units
Description	"ABC Coin"	Human-readable description
Available Features
Feature	Constant	Description
Minting	assetfttypes.Feature_minting	Allow additional token creation
Burning	assetfttypes.Feature_burning	Allow token destruction
Freezing	assetfttypes.Feature_freezing	Allow freezing account balances
Whitelisting	assetfttypes.Feature_whitelisting	Allow whitelist management
go
// Example: Token with all features
features := []assetfttypes.Feature{
    assetfttypes.Feature_minting,
    assetfttypes.Feature_burning,
    assetfttypes.Feature_freezing,
    assetfttypes.Feature_whitelisting,
}

// Example: Token with minting only
features := []assetfttypes.Feature{
    assetfttypes.Feature_minting,
}
Step 4: Query Token Information
go
func queryTokenInfo(
    ctx context.Context,
    clientCtx client.Context,
    denom string,
) (*assetfttypes.QueryTokenResponse, error) {
    
    assetftClient := assetfttypes.NewQueryClient(clientCtx)
    
    res, err := assetftClient.Token(ctx, &assetfttypes.QueryTokenRequest{
        Denom: denom,
    })
    if err != nil {
        return nil, fmt.Errorf("failed to query token: %w", err)
    }
    
    fmt.Printf("Token Info:\n")
    fmt.Printf("  Denom: %s\n", res.Token.Denom)
    fmt.Printf("  Symbol: %s\n", res.Token.Symbol)
    fmt.Printf("  Admin: %s\n", res.Token.Admin)
    fmt.Printf("  Features: %v\n", res.Token.Features)
    
    return res, nil
}
Step 5: Query Token Balance
go
func queryBalance(
    ctx context.Context,
    clientCtx client.Context,
    address string,
    denom string,
) (sdk.Coin, error) {
    
    bankClient := banktypes.NewQueryClient(clientCtx)
    
    resp, err := bankClient.Balance(ctx, &banktypes.QueryBalanceRequest{
        Address: address,
        Denom:   denom,
    })
    if err != nil {
        return sdk.Coin{}, fmt.Errorf("failed to query balance: %w", err)
    }
    
    fmt.Printf("Balance for %s: %s\n", address, resp.Balance.String())
    return *resp.Balance, nil
}
Step 6: Send Tokens
go
func sendTokens(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    fromAddress sdk.AccAddress,
    toAddress sdk.AccAddress,
    denom string,
    amount int64,
) error {
    
    msgSend := &banktypes.MsgSend{
        FromAddress: fromAddress.String(),
        ToAddress:   toAddress.String(),
        Amount:      sdk.NewCoins(sdk.NewInt64Coin(denom, amount)),
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(fromAddress),
        txFactory,
        msgSend,
    )
    if err != nil {
        return fmt.Errorf("failed to send tokens: %w", err)
    }
    
    fmt.Printf("✅ Sent %d %s to %s\n", amount, denom, toAddress.String())
    return nil
}
Step 7: Mint Additional Tokens (Requires minting feature)
go
func mintTokens(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    adminAddress sdk.AccAddress,
    denom string,
    amount int64,
    recipient sdk.AccAddress,
) error {
    
    msgMint := &assetfttypes.MsgMint{
        Sender:    adminAddress.String(),
        Coin:      sdk.NewInt64Coin(denom, amount),
        Recipient: recipient.String(),
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(adminAddress),
        txFactory,
        msgMint,
    )
    if err != nil {
        return fmt.Errorf("failed to mint tokens: %w", err)
    }
    
    fmt.Printf("✅ Minted %d %s to %s\n", amount, denom, recipient.String())
    return nil
}
Step 8: Burn Tokens (Requires burning feature)
go
func burnTokens(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    fromAddress sdk.AccAddress,
    denom string,
    amount int64,
) error {
    
    msgBurn := &assetfttypes.MsgBurn{
        Sender: fromAddress.String(),
        Coin:   sdk.NewInt64Coin(denom, amount),
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(fromAddress),
        txFactory,
        msgBurn,
    )
    if err != nil {
        return fmt.Errorf("failed to burn tokens: %w", err)
    }
    
    fmt.Printf("✅ Burned %d %s\n", amount, denom)
    return nil
}
Step 9: Freeze Tokens (Requires freezing feature)
go
func freezeTokens(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    adminAddress sdk.AccAddress,
    targetAddress sdk.AccAddress,
    denom string,
    amount int64,
) error {
    
    msgFreeze := &assetfttypes.MsgFreeze{
        Sender:  adminAddress.String(),
        Account: targetAddress.String(),
        Coin:    sdk.NewInt64Coin(denom, amount),
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(adminAddress),
        txFactory,
        msgFreeze,
    )
    if err != nil {
        return fmt.Errorf("failed to freeze tokens: %w", err)
    }
    
    fmt.Printf("✅ Frozen %d %s for account %s\n", amount, denom, targetAddress.String())
    return nil
}

func unfreezeTokens(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    adminAddress sdk.AccAddress,
    targetAddress sdk.AccAddress,
    denom string,
) error {
    
    msgUnfreeze := &assetfttypes.MsgUnfreeze{
        Sender:  adminAddress.String(),
        Account: targetAddress.String(),
        Coin:    sdk.NewInt64Coin(denom, 0), // 0 means unfreeze all
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(adminAddress),
        txFactory,
        msgUnfreeze,
    )
    if err != nil {
        return fmt.Errorf("failed to unfreeze tokens: %w", err)
    }
    
    fmt.Printf("✅ Unfroze tokens for account %s\n", targetAddress.String())
    return nil
}
Step 10: Transfer Admin Rights
go
func transferAdmin(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    currentAdmin sdk.AccAddress,
    newAdmin sdk.AccAddress,
    denom string,
) error {
    
    msgTransferAdmin := &assetfttypes.MsgTransferAdmin{
        Sender:  currentAdmin.String(),
        Account: newAdmin.String(),
        Denom:   denom,
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(currentAdmin),
        txFactory,
        msgTransferAdmin,
    )
    if err != nil {
        return fmt.Errorf("failed to transfer admin: %w", err)
    }
    
    fmt.Printf("✅ Admin transferred from %s to %s\n", currentAdmin.String(), newAdmin.String())
    return nil
}
Step 11: Clear Admin Rights
go
func clearAdmin(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    adminAddress sdk.AccAddress,
    denom string,
) error {
    
    msgClearAdmin := &assetfttypes.MsgClearAdmin{
        Sender: adminAddress.String(),
        Denom:  denom,
    }

    _, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(adminAddress),
        txFactory,
        msgClearAdmin,
    )
    if err != nil {
        return fmt.Errorf("failed to clear admin: %w", err)
    }
    
    fmt.Printf("✅ Admin rights cleared for %s\n", denom)
    return nil
}
Complete Example: Full Token Lifecycle
go
package main

import (
    "context"
    "crypto/tls"
    "fmt"
    "log"

    "github.com/cosmos/cosmos-sdk/codec"
    "github.com/cosmos/cosmos-sdk/crypto/hd"
    "github.com/cosmos/cosmos-sdk/crypto/keyring"
    sdk "github.com/cosmos/cosmos-sdk/types"
    sdkmath "github.com/cosmos/cosmos-sdk/types/math"
    "github.com/cosmos/cosmos-sdk/types/module"
    "github.com/cosmos/cosmos-sdk/x/auth"
    banktypes "github.com/cosmos/cosmos-sdk/x/bank/types"
    "github.com/cosmos/gogoproto/grpc"
    "google.golang.org/grpc/credentials"

    "github.com/tokenize-x/tx-chain/v3/pkg/client"
    coreumconfig "github.com/tokenize-x/tx-chain/v3/pkg/config"
    "github.com/tokenize-x/tx-chain/v3/pkg/config/constant"
    assetfttypes "github.com/tokenize-x/tx-chain/v3/x/assetft/types"
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
    // Step 1: Issue Token
    // ============================================
    fmt.Println("\n=== 1. Issuing Token ===")
    
    subunit := "uabc"
    denom := subunit + "-" + senderAddress.String()
    
    msgIssue := &assetfttypes.MsgIssue{
        Issuer:        senderAddress.String(),
        Symbol:        "ABC",
        Subunit:       subunit,
        Precision:     6,
        InitialAmount: sdkmath.NewInt(100_000_000),
        Description:   "ABC Coin - Example fungible token",
        Features: []assetfttypes.Feature{
            assetfttypes.Feature_minting,
            assetfttypes.Feature_burning,
            assetfttypes.Feature_freezing,
        },
    }

    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgIssue,
    )
    if err != nil {
        log.Fatalf("Failed to issue token: %v", err)
    }
    fmt.Printf("✅ Token issued! Denom: %s\n", denom)

    // ============================================
    // Step 2: Query Initial Balance
    // ============================================
    fmt.Println("\n=== 2. Querying Initial Balance ===")
    
    bankClient := banktypes.NewQueryClient(clientCtx)
    balanceResp, err := bankClient.Balance(ctx, &banktypes.QueryBalanceRequest{
        Address: senderAddress.String(),
        Denom:   denom,
    })
    if err != nil {
        log.Printf("Warning: %v", err)
    } else {
        fmt.Printf("Admin Balance: %s\n", balanceResp.Balance.String())
    }

    // ============================================
    // Step 3: Send Tokens
    // ============================================
    fmt.Println("\n=== 3. Sending Tokens ===")
    
    msgSend := &banktypes.MsgSend{
        FromAddress: senderAddress.String(),
        ToAddress:   recipientAddress.String(),
        Amount:      sdk.NewCoins(sdk.NewInt64Coin(denom, 1_000_000)),
    }

    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgSend,
    )
    if err != nil {
        log.Fatalf("Failed to send: %v", err)
    }
    fmt.Printf("✅ Sent 1,000,000 %s to recipient\n", denom)

    // ============================================
    // Step 4: Query Recipient Balance
    // ============================================
    fmt.Println("\n=== 4. Querying Recipient Balance ===")
    
    balanceResp, err = bankClient.Balance(ctx, &banktypes.QueryBalanceRequest{
        Address: recipientAddress.String(),
        Denom:   denom,
    })
    if err != nil {
        log.Printf("Warning: %v", err)
    } else {
        fmt.Printf("Recipient Balance: %s\n", balanceResp.Balance.String())
    }

    // ============================================
    // Step 5: Freeze Tokens (Admin only)
    // ============================================
    fmt.Println("\n=== 5. Freezing Tokens ===")
    
    msgFreeze := &assetfttypes.MsgFreeze{
        Sender:  senderAddress.String(),
        Account: recipientAddress.String(),
        Coin:    sdk.NewInt64Coin(denom, 500_000),
    }

    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgFreeze,
    )
    if err != nil {
        log.Fatalf("Failed to freeze: %v", err)
    }
    fmt.Printf("✅ Frozen 500,000 %s for recipient\n", denom)

    // ============================================
    // Step 6: Mint More Tokens
    // ============================================
    fmt.Println("\n=== 6. Minting More Tokens ===")
    
    msgMint := &assetfttypes.MsgMint{
        Sender:    senderAddress.String(),
        Coin:      sdk.NewInt64Coin(denom, 50_000_000),
        Recipient: senderAddress.String(),
    }

    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgMint,
    )
    if err != nil {
        log.Fatalf("Failed to mint: %v", err)
    }
    fmt.Printf("✅ Minted 50,000,000 %s\n", denom)

    // ============================================
    // Step 7: Query Updated Admin Balance
    // ============================================
    fmt.Println("\n=== 7. Querying Updated Admin Balance ===")
    
    balanceResp, err = bankClient.Balance(ctx, &banktypes.QueryBalanceRequest{
        Address: senderAddress.String(),
        Denom:   denom,
    })
    if err != nil {
        log.Printf("Warning: %v", err)
    } else {
        fmt.Printf("Admin Balance: %s\n", balanceResp.Balance.String())
    }

    // ============================================
    // Step 8: Transfer Admin Rights
    // ============================================
    fmt.Println("\n=== 8. Transferring Admin Rights ===")
    
    msgTransferAdmin := &assetfttypes.MsgTransferAdmin{
        Sender:  senderAddress.String(),
        Account: recipientAddress.String(),
        Denom:   denom,
    }

    _, err = client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddress),
        txFactory,
        msgTransferAdmin,
    )
    if err != nil {
        log.Fatalf("Failed to transfer admin: %v", err)
    }
    fmt.Printf("✅ Admin transferred to recipient\n")

    // ============================================
    // Step 9: Verify New Admin
    // ============================================
    fmt.Println("\n=== 9. Verifying New Admin ===")
    
    assetftClient := assetfttypes.NewQueryClient(clientCtx)
    tokenResp, err := assetftClient.Token(ctx, &assetfttypes.QueryTokenRequest{
        Denom: denom,
    })
    if err != nil {
        log.Printf("Warning: %v", err)
    } else {
        fmt.Printf("New Token Admin: %s\n", tokenResp.Token.Admin)
    }

    fmt.Println("\n✅ Fungible token management complete!")
}
Expected Output
text
Sender Address: testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq
Recipient Address: testcore1x8k5y8v5f8zq7p3x2w4l8k9j3h5g2f1d8s7a6d

=== 1. Issuing Token ===
✅ Token issued! Denom: uabc-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== 2. Querying Initial Balance ===
Admin Balance: 100000000uabc-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== 3. Sending Tokens ===
✅ Sent 1,000,000 uabc-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq to recipient

=== 4. Querying Recipient Balance ===
Recipient Balance: 1000000uabc-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== 5. Freezing Tokens ===
✅ Frozen 500,000 uabc-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq for recipient

=== 6. Minting More Tokens ===
✅ Minted 50,000,000 uabc-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== 7. Querying Updated Admin Balance ===
Admin Balance: 149000000uabc-testcore1zuelfk5fz02v9x7gnsy2t7ps83m8vljx5wqdfq

=== 8. Transferring Admin Rights ===
✅ Admin transferred to recipient

=== 9. Verifying New Admin ===
New Token Admin: testcore1x8k5y8v5f8zq7p3x2w4l8k9j3h5g2f1d8s7a6d

✅ Fungible token management complete!
Error Handling
go
// Check for specific errors
if err != nil {
    if strings.Contains(err.Error(), "already exists") {
        fmt.Println("Token denom already exists")
    } else if strings.Contains(err.Error(), "unauthorized") {
        fmt.Println("Not authorized - check admin permissions")
    } else if strings.Contains(err.Error(), "feature not enabled") {
        fmt.Println("This feature was not enabled during token issuance")
    } else {
        fmt.Printf("Unexpected error: %v\n", err)
    }
}
Next Steps
Create and manage NFT with Golang

Smart FT with WASM

Asset FT Extension

Resources
AssetFT Module Documentation

TX Blockchain Go Client

Testnet Faucet

Block Explorer
