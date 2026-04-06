# CEX Integration Guide

This document provides information required by exchanges to integrate trading of TX tokens.

## Contact Information

**Technical Staff Contact:**
- **Name:** Reza Bashash
- **Email:** reza@tx.org
- **Twitter:** @rezabashash

## Important Links

| Resource | URL |
|----------|-----|
| Official Website | https://tx.org |
| Source Code | https://github.com/tokenize-x/tx-chain |
| Block Explorer | https://explorer.tx.org |
| Documentation | https://docs.tx.org |
| Faucet (Testnet) | https://faucet.testnet.tx.dev |

## Project Information

| Parameter | Value |
|-----------|-------|
| Project Name | TX |
| Token Name | TX |
| Token Symbol | TX |
| Token Decimals | 6 digits |
| Consensus | BPoS (Tendermint) |
| Block Time | ~1.6 seconds |
| Confirmations Required | 1 |
| Validators | 64 |
| Transaction Model | Account Model |

## Token Supply

### Initial Supply
- **500,000,000 TX** set in genesis block

### Total Supply
- No ceiling - total supply grows
- Inflation is proportional to difference between current TVL and target TVL (67%)
- Initial inflation: 10%
- Maximum inflation: 20%
- Minimum inflation: 0% (when TVL ≥ 67%)

## Functions of TX Token

1. **Staking and Delegating** - Stake to validators
2. **Voting** - Participate in governance
3. **Paying Fees** - Transaction and gas fees

## TX Allocation Plan

| Allocation | Percentage |
|------------|------------|
| SOLO Community Airdrop | 20% |
| TX Community Airdrop | 30% |
| Validators' Reward Pool | 10% |
| dApp Developers | 10% |
| Operation (maintenance, teams, investors) | 30% |

## Transaction Model

We use the **Account Model** where each account holds balances of TX tokens. This is implemented by the standard Bank module of Cosmos SDK.

### Base Implementation
- Based on Cosmos SDK with added custom functionalities
- Transferring TX works same as standard bank module

### Account Activation
- Accounts do not require activation
- Account existence starts when it receives any funds

### Signatures
- Multi-signature supported for legacy amino-encoded transactions
- Offline signing supported (sign now, broadcast later)
- Each account maintains incremental sequence number
- Valid, expected sequence number must be included in transaction

### Transaction Expiry
- Transactions never expire
- Executed in FIFO order

## Consensus

| Parameter | Value |
|-----------|-------|
| Algorithm | BPoS (Bonded Proof of Stake) |
| Implementation | Tendermint |
| Block Time | 1.6 seconds (not fixed) |
| Confirmations | 1 block |
| Validators | 64 |

### Validator Voting Power
- Voting power proportional to stake
- Validators get rewards for validating blocks
- Validators earn commission on delegated stake

## Smart Contracts

- **Support:** YES
- **Platform:** CosmWasm
- **Type:** WASM smart contracts

## Token Issuance

- TX blockchain supports token issuance
- Can receive tokens from other chains via IBC protocol

## Transaction Success/Failure

Transactions included in a block may fail, indicated by:
- Non-zero status code
- **Fee is charged even on failure**

## Fee Model

To understand tx chain fees, read about the [tx gas price](../../gas-price.md).

## Code Examples

### Prerequisites

Before broadcasting transactions, you need a funded test account:

1. Go to [TX Testnet Faucet](https://faucet.testnet.tx.dev)
2. Click "Generate Funded Wallet"
3. Save your mnemonic (NEVER hardcode in production!)

> **⚠️ Security Warning:** Never use mnemonic directly in code in production. Use keyring (os/file) for secure key storage.

---

## Golang Examples

### Skeleton

```go
package main

import (
    "github.com/tokenize-x/tx-chain/v3/pkg/client"
    "github.com/tokenize-x/tx-chain/pkg/config/constant"
)

func main() {
    const (
        walletMnemonic = "" // put mnemonic here

        chainID          = constant.ChainIDTest
        addressPrefix    = constant.AddressPrefixTest
        denom            = constant.DenomTest
        recipientAddress = "testcore1534s8rz2e36lwycr6gkm9vpfe5yf67wkuca7zs"
        nodeAddress      = "grpc.testnet.tx.dev:443"
    )
}
Configure Client
go
import (
    "context"
    "crypto/tls"
    "fmt"

    "github.com/cosmos/cosmos-sdk/client/flags"
    "github.com/cosmos/cosmos-sdk/crypto/hd"
    "github.com/cosmos/cosmos-sdk/crypto/keyring"
    sdk "github.com/cosmos/cosmos-sdk/types"
    "github.com/cosmos/cosmos-sdk/types/module"
    "github.com/cosmos/cosmos-sdk/x/auth"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials"

    "github.com/tokenize-x/tx-chain/v3/pkg/client"
    coreumconfig "github.com/tokenize-x/tx-chain/v3/pkg/config"
    "github.com/tokenize-x/tx-chain/v3/pkg/config/constant"
)

func setupClient(mnemonic string) (client.Context, client.Factory, sdk.AccAddress) {
    // Configure Cosmos SDK
    config := sdk.GetConfig()
    config.SetBech32PrefixForAccount(addressPrefix, addressPrefix+"pub")
    config.SetCoinType(constant.CoinType)
    config.Seal()

    // Setup modules
    modules := module.NewBasicManager(auth.AppModuleBasic{})

    encodingConfig := coreumconfig.NewEncodingConfig(modules)

    pc, ok := encodingConfig.Codec.(codec.GRPCCodecProvider)
    if !ok {
        panic("failed to cast codec to codec.GRPCCodecProvider")
    }

    // Connect gRPC (use WithInsecure() for local development)
    grpcClient, err := grpc.Dial(
        nodeAddress,
        grpc.WithDefaultCallOptions(grpc.ForceCodec(pc.GRPCCodec())),
        grpc.WithTransportCredentials(credentials.NewTLS(&tls.Config{MinVersion: tls.VersionTLS12})),
    )
    if err != nil {
        panic(err)
    }

    // Create client context
    clientCtxConfig := client.DefaultContextConfig()
    clientCtxConfig.GasConfig.GasAdjustment = 1.0
    clientCtxConfig.GasConfig.GasPriceAdjustment = sdk.MustNewDecFromStr("1.1")
    
    clientCtx := client.NewContext(clientCtxConfig, modules).
        WithChainID(string(chainID)).
        WithGRPCClient(grpcClient).
        WithKeyring(keyring.NewInMemory(encodingConfig.Codec)).
        WithBroadcastMode(flags.BroadcastSync)

    // Create tx factory
    txFactory := client.Factory{}.
        WithKeybase(clientCtx.Keyring()).
        WithChainID(clientCtx.ChainID()).
        WithTxConfig(clientCtx.TxConfig()).
        WithSimulateAndExecute(true)

    // Import account from mnemonic
    senderInfo, err := clientCtx.Keyring().NewAccount(
        "exchange-wallet",
        mnemonic,
        "",
        sdk.GetConfig().GetFullBIP44Path(),
        hd.Secp256k1,
    )
    if err != nil {
        panic(err)
    }

    senderAddress, _ := senderInfo.GetAddress()
    fmt.Printf("Sender address: %s\n", senderAddress.String())

    return clientCtx, txFactory, senderAddress
}
Send Coins
go
import (
    banktypes "github.com/cosmos/cosmos-sdk/x/bank/types"
)

func sendCoins(
    ctx context.Context,
    clientCtx client.Context,
    txFactory client.Factory,
    senderAddr sdk.AccAddress,
    recipient string,
    amount sdk.Coin,
) (string, error) {
    // Validate addresses
    if _, err := sdk.AccAddressFromBech32(recipient); err != nil {
        return "", err
    }

    // Create message
    msg := &banktypes.MsgSend{
        FromAddress: senderAddr.String(),
        ToAddress:   recipient,
        Amount:      sdk.NewCoins(amount),
    }

    // Broadcast transaction
    result, err := client.BroadcastTx(
        ctx,
        clientCtx.WithFromAddress(senderAddr),
        txFactory,
        msg,
    )
    if err != nil {
        return "", err
    }
    fmt.Printf("Tx hash: %s\n", result.TxHash)

    return result.TxHash, nil
}
Query Balance
go
func queryBalance(ctx context.Context, clientCtx client.Context, address string) error {
    bankClient := banktypes.NewQueryClient(clientCtx)
    balances, err := bankClient.AllBalances(ctx, &banktypes.QueryAllBalancesRequest{
        Address: address,
    })
    if err != nil {
        return err
    }
    fmt.Printf("Balances: %s\n", balances.Balances)
    return nil
}
Query Block
go
import (
    "github.com/cosmos/cosmos-sdk/client/grpc/tmservice"
)

func queryBlock(ctx context.Context, clientCtx client.Context) error {
    tmClient := tmservice.NewServiceClient(clientCtx)
    
    // Get latest block
    latestBlock, err := tmClient.GetLatestBlock(ctx, &tmservice.GetLatestBlockRequest{})
    if err != nil {
        return err
    }
    fmt.Printf("Latest block height: %d\n", latestBlock.Block.Header.Height)
    
    // Get block by height
    block, err := tmClient.GetBlockByHeight(ctx, &tmservice.GetBlockByHeightRequest{
        Height: latestBlock.Block.Header.Height,
    })
    if err != nil {
        return err
    }
    fmt.Printf("Block time: %s\n", block.Block.Header.Time)
    
    return nil
}
Query Transaction by Hash
go
import (
    sdktx "github.com/cosmos/cosmos-sdk/types/tx"
)

func queryTx(ctx context.Context, clientCtx client.Context, txHash string) (*sdktx.GetTxResponse, error) {
    txClient := sdktx.NewServiceClient(clientCtx)
    
    tx, err := txClient.GetTx(ctx, &sdktx.GetTxRequest{Hash: txHash})
    if err != nil {
        return nil, err
    }
    
    fmt.Printf("Tx code: %d\n", tx.TxResponse.Code)
    fmt.Printf("Tx success: %v\n", tx.TxResponse.Code == 0)
    
    return tx, nil
}
Detect Balance Changes
go
func balanceUpdates(tx *sdktx.GetTxResponse, denom string) {
    for _, event := range tx.TxResponse.Events {
        switch event.Type {
        case "coin_received":
            var receiver, amount string
            for _, attr := range event.Attributes {
                switch string(attr.Key) {
                case "receiver":
                    receiver = string(attr.Value)
                case "amount":
                    amount = string(attr.Value)
                }
            }
            coins, _ := sdk.ParseCoinsNormalized(amount)
            if denomAmount := coins.AmountOf(denom); !denomAmount.IsZero() {
                fmt.Printf("%s received %s\n", receiver, sdk.NewCoin(denom, denomAmount))
            }
            
        case "coin_spent":
            var spender, amount string
            for _, attr := range event.Attributes {
                switch string(attr.Key) {
                case "spender":
                    spender = string(attr.Value)
                case "amount":
                    amount = string(attr.Value)
                }
            }
            coins, _ := sdk.ParseCoinsNormalized(amount)
            if denomAmount := coins.AmountOf(denom); !denomAmount.IsZero() {
                fmt.Printf("%s spent %s\n", spender, sdk.NewCoin(denom, denomAmount))
            }
        }
    }
}
Complete Golang Example
go
package main

import (
    "context"
    "fmt"
    "log"

    sdk "github.com/cosmos/cosmos-sdk/types"
)

const (
    senderMnemonic    = "your twelve word mnemonic here"
    recipientAddress  = "testcore1534s8rz2e36lwycr6gkm9vpfe5yf67wkuca7zs"
)

func main() {
    ctx := context.Background()
    
    // Setup client
    clientCtx, txFactory, senderAddr := setupClient(senderMnemonic)
    
    // Send coins
    txHash, err := sendCoins(
        ctx, clientCtx, txFactory, senderAddr,
        recipientAddress,
        sdk.NewInt64Coin("utestcore", 9_000_000),
    )
    if err != nil {
        log.Fatalf("Failed to send: %v", err)
    }
    
    // Query recipient balance
    if err := queryBalance(ctx, clientCtx, recipientAddress); err != nil {
        log.Printf("Balance query failed: %v", err)
    }
    
    // Query block
    if err := queryBlock(ctx, clientCtx); err != nil {
        log.Printf("Block query failed: %v", err)
    }
    
    // Query transaction
    tx, err := queryTx(ctx, clientCtx, txHash)
    if err != nil {
        log.Printf("Tx query failed: %v", err)
    } else {
        balanceUpdates(tx, "utestcore")
    }
    
    fmt.Println("✅ Complete!")
}
TypeScript Examples
Skeleton
typescript
import { StdFee } from "@cosmjs/amino";
import { stringToPath } from "@cosmjs/crypto";
import { DirectSecp256k1HdWallet, AccountData, parseCoins, Coin } from "@cosmjs/proto-signing";
import {
    calculateFee,
    GasPrice,
    SigningStargateClient,
    DeliverTxResponse,
} from "@cosmjs/stargate";
import { IndexedTx, isDeliverTxSuccess } from "@cosmjs/stargate/build/stargateclient";
import { Event, Attribute } from "@cosmjs/stargate";

const txAccountPrefix = "testcore";
const txHDPath = "m/44'/990'/0'/0/0";
const txDenom = "utestcore";
const txRpcEndpoint = "https://rpc.testnet.tx.dev:443";
const recipientAddress = "testcore1534s8rz2e36lwycr6gkm9vpfe5yf67wkuca7zs";
const senderMnemonic = ""; // Put your mnemonic here

const main = (async function() {
    // Code here
})();

export default main;
Configure Client & Send Coins
typescript
async function setupAndSend() {
    console.log("Preparing sender wallet...");
    const senderWallet = await DirectSecp256k1HdWallet.fromMnemonic(senderMnemonic, {
        prefix: txAccountPrefix,
        hdPaths: [stringToPath(txHDPath)],
    });
    
    const [sender] = await senderWallet.getAccounts();
    console.log(`Sender address: ${sender.address}`);
    
    const senderClient = await SigningStargateClient.connectWithSigner(
        txRpcEndpoint,
        senderWallet
    );
    
    // Send tokens
    const amount: Coin = {
        denom: txDenom,
        amount: "9000000",
    };
    
    console.log(`Sending ${amount.amount}${amount.denom} to recipient...`);
    
    const gasPrice = GasPrice.fromString(`0.0625${txDenom}`);
    const sendGas = 111_000;
    const fee: StdFee = calculateFee(sendGas, gasPrice);
    
    const result = await senderClient.sendTokens(
        sender.address,
        recipientAddress,
        [amount],
        fee
    );
    
    if (!isDeliverTxSuccess(result)) {
        throw new Error(`Send failed: ${result.rawLog}`);
    }
    
    console.log(`Successfully sent! Tx hash: ${result.transactionHash}`);
    return { senderClient, result, sender };
}
Query Balance
typescript
async function queryBalance(client: SigningStargateClient, address: string) {
    const balance = await client.getBalance(address, txDenom);
    console.log(`Balance for ${address}: ${balance.amount}${balance.denom}`);
    return balance;
}
Query Block
typescript
async function queryBlock(client: SigningStargateClient) {
    // Latest block
    const latestBlock = await client.getBlock();
    console.log(`Latest block height: ${latestBlock.header.height}`);
    console.log(`Latest block time: ${latestBlock.header.time}`);
    
    // Block by height
    const block = await client.getBlock(latestBlock.header.height);
    console.log(`Block hash: ${block.header.hash}`);
    
    return block;
}
Query Transaction
typescript
async function queryTx(client: SigningStargateClient, txHash: string): Promise<IndexedTx> {
    const tx = await client.getTx(txHash);
    console.log(`Transaction height: ${tx.height}`);
    console.log(`Transaction code: ${tx.code}`);
    console.log(`Transaction success: ${tx.code === 0}`);
    return tx;
}
Detect Balance Changes
typescript
function balanceUpdates(tx: IndexedTx, denom: string) {
    tx.events.forEach((event: Event) => {
        switch (event.type) {
            case 'coin_received':
                let receiver = '';
                let amount = '';
                event.attributes.forEach((attr: Attribute) => {
                    switch (attr.key) {
                        case "receiver":
                            receiver = attr.value;
                            break;
                        case "amount":
                            amount = attr.value;
                            break;
                    }
                });
                
                parseCoins(amount).forEach((coin: Coin) => {
                    if (coin.denom === denom) {
                        console.log(`${receiver} received ${coin.amount}${coin.denom}`);
                    }
                });
                break;
                
            case 'coin_spent':
                let spender = '';
                let spentAmount = '';
                event.attributes.forEach((attr: Attribute) => {
                    switch (attr.key) {
                        case "spender":
                            spender = attr.value;
                            break;
                        case "amount":
                            spentAmount = attr.value;
                            break;
                    }
                });
                
                parseCoins(spentAmount).forEach((coin: Coin) => {
                    if (coin.denom === denom) {
                        console.log(`${spender} spent ${coin.amount}${coin.denom}`);
                    }
                });
                break;
        }
    });
}
Complete TypeScript Example
typescript
import { DirectSecp256k1HdWallet } from "@cosmjs/proto-signing";
import { SigningStargateClient, GasPrice, calculateFee } from "@cosmjs/stargate";
import { stringToPath } from "@cosmjs/crypto";
import { isDeliverTxSuccess } from "@cosmjs/stargate/build/stargateclient";

const txAccountPrefix = "testcore";
const txHDPath = "m/44'/990'/0'/0/0";
const txDenom = "utestcore";
const txRpcEndpoint = "https://rpc.testnet.tx.dev:443";
const recipientAddress = "testcore1534s8rz2e36lwycr6gkm9vpfe5yf67wkuca7zs";
const senderMnemonic = "your twelve word mnemonic here";

async function main() {
    try {
        // Setup wallet
        const wallet = await DirectSecp256k1HdWallet.fromMnemonic(senderMnemonic, {
            prefix: txAccountPrefix,
            hdPaths: [stringToPath(txHDPath)],
        });
        
        const [sender] = await wallet.getAccounts();
        console.log(`Sender: ${sender.address}`);
        
        // Connect client
        const client = await SigningStargateClient.connectWithSigner(txRpcEndpoint, wallet);
        
        // Check initial balance
        const initialBalance = await client.getBalance(sender.address, txDenom);
        console.log(`Initial balance: ${initialBalance.amount}${txDenom}`);
        
        // Send tokens
        const amount = { denom: txDenom, amount: "9000000" };
        const gasPrice = GasPrice.fromString(`0.0625${txDenom}`);
        const fee = calculateFee(111_000, gasPrice);
        
        const result = await client.sendTokens(sender.address, recipientAddress, [amount], fee);
        
        if (!isDeliverTxSuccess(result)) {
            throw new Error(`Transaction failed: ${result.rawLog}`);
        }
        
        console.log(`Tx hash: ${result.transactionHash}`);
        
        // Check recipient balance
        const recipientBalance = await client.getBalance(recipientAddress, txDenom);
        console.log(`Recipient balance: ${recipientBalance.amount}${txDenom}`);
        
        // Get latest block
        const block = await client.getBlock();
        console.log(`Block height: ${block.header.height}`);
        
        // Get transaction details
        const tx = await client.getTx(result.transactionHash);
        console.log(`Tx success: ${tx.code === 0}`);
        
        // Detect balance changes
        tx.events.forEach(event => {
            if (event.type === 'coin_received') {
                event.attributes.forEach(attr => {
                    if (attr.key === 'receiver') {
                        console.log(`Receiver: ${attr.value}`);
                    }
                    if (attr.key === 'amount') {
                        console.log(`Amount: ${attr.value}`);
                    }
                });
            }
        });
        
        console.log("✅ Complete!");
        
    } catch (error) {
        console.error("Error:", error);
    }
}

main();
Transaction Events That Change Balance Without User Signature
These messages may change account balance without the account's interaction:

Message Type	Description
bank.MsgMultiSend	Multiple token transfers
bank.MsgSend	Single token transfer
authz.MsgExec	Authorized execution
distribution.MsgWithdrawDelegatorReward	Claim staking rewards
distribution.MsgWithdrawValidatorCommission	Claim validator commission
ibc.MsgTransfer	IBC token transfer
vesting.MsgCreateVestingAccount	Create vesting account
wasm.MsgExecuteContract	Smart contract execution
Audits
Our code is being audited. Results will be shared upon completion.

Network Endpoints
Testnet
Service	Endpoint
RPC	https://rpc.testnet.tx.dev:443
gRPC	grpc.testnet.tx.dev:443
REST API	https://rest.testnet.tx.dev:443
Faucet	https://faucet.testnet.tx.dev
Mainnet
Service	Endpoint
RPC	https://rpc.tx.org:443
gRPC	grpc.tx.org:443
REST API	https://rest.tx.org:443
Next Steps
Review Gas Price Guide

Check Node Setup Guide

Explore Validator Guide
