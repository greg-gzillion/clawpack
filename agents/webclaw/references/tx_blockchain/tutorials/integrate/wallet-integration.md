# Wallet Integration Guide

This document provides the necessary information for wallet developers to integrate TX Blockchain. Since TX is built with the Cosmos SDK, the process is largely similar to other Cosmos-based chains, with a few key differences in fee handling and fungible token management.

## Overview

| Topic | Key Difference from Standard Cosmos SDK |
|-------|------------------------------------------|
| **Gas Price** | Dynamic, based on on-chain `feemodel` module |
| **Gas Estimation** | More deterministic, but using `simulate` endpoint is still recommended |
| **Fungible Tokens (FT)** | Uses `assetft` module in conjunction with `bank` module |
| **NFTs** | Uses `assetnft` module with `nft` module |

## Network Endpoints

### Testnet

| Service | Endpoint |
|---------|----------|
| RPC | `https://rpc.testnet.tx.dev:443` |
| gRPC | `grpc.testnet.tx.dev:443` |
| REST API | `https://rest.testnet.tx.dev:443` |
| Faucet | `https://faucet.testnet.tx.dev` |

### Mainnet

| Service | Endpoint |
|---------|----------|
| RPC | `https://rpc.tx.org:443` |
| gRPC | `grpc.tx.org:443` |
| REST API | `https://rest.tx.org:443` |

## Key Configuration Parameters

| Parameter | Testnet Value | Mainnet Value |
|-----------|---------------|----------------|
| Chain ID | `txchain-testnet-1` | `txchain-mainnet-1` |
| Address Prefix | `testcore` | `core` |
| Native Denom | `utestcore` | `utx` |
| Coin Type (BIP44) | `990` | `990` |
| HD Path | `m/44'/990'/0'/0/0` | `m/44'/990'/0'/0/0` |

## 1. Gas Price Integration

TX Blockchain uses a dynamic fee model. The minimum gas price is set by governance and can change over time.

### Fetching Current Gas Price

**Using gRPC (Recommended):**

```go
// Golang
import (
    "context"
    "fmt"
    feemodeltypes "github.com/tokenize-x/tx-chain/v3/x/feemodel/types"
)

func getMinGasPrice(ctx context.Context, client feemodeltypes.QueryClient) (sdk.Dec, string, error) {
    resp, err := client.MinGasPrice(ctx, &feemodeltypes.QueryMinGasPriceRequest{})
    if err != nil {
        return sdk.ZeroDec(), "", err
    }
    if resp.MinGasPrice == nil {
        return sdk.ZeroDec(), "", fmt.Errorf("no min gas price set")
    }
    
    amount, err := sdk.NewDecFromStr(resp.MinGasPrice.Amount)
    if err != nil {
        return sdk.ZeroDec(), "", err
    }
    
    return amount, resp.MinGasPrice.Denom, nil
}
Using REST API:

bash
# Query current minimum gas price
curl https://rest.testnet.tx.dev/cosmos/feemodel/v1/min_gas_price

# Example response:
# {
#   "min_gas_price": {
#     "amount": "0.0625",
#     "denom": "utestcore"
#   }
# }
Gas Price Multiplier
It is recommended to apply a multiplier to the minimum gas price to ensure transaction inclusion, especially during network congestion.

Priority	Multiplier	Use Case
Low	1.0	Non-urgent transactions
Standard	1.1	Regular transfers
High	1.3	Time-sensitive transactions
Urgent	1.5	Critical operations
TypeScript Example:

typescript
async function getGasPriceWithMultiplier(
    multiplier: number = 1.1
): Promise<GasPrice> {
    const response = await fetch('https://rest.testnet.tx.dev/cosmos/feemodel/v1/min_gas_price');
    const data = await response.json();
    const minPrice = parseFloat(data.min_gas_price.amount);
    const gasPrice = minPrice * multiplier;
    return GasPrice.fromString(`${gasPrice}${data.min_gas_price.denom}`);
}
2. Gas Estimation
TX Blockchain uses a deterministic gas model. While you can estimate gas using the simulation endpoint, the gas consumption is more predictable than standard Cosmos SDK.

Using Simulation Endpoint (Recommended)
Golang:

go
import (
    "context"
    "github.com/cosmos/cosmos-sdk/client/tx"
    "github.com/cosmos/cosmos-sdk/types/tx/signing"
)

func estimateGas(
    ctx context.Context,
    clientCtx client.Context,
    msgs ...sdk.Msg,
) (uint64, error) {
    txFactory := tx.Factory{}.
        WithChainID(clientCtx.ChainID()).
        WithTxConfig(clientCtx.TxConfig()).
        WithSignMode(signing.SignMode_SIGN_MODE_DIRECT)
    
    _, gas, err := tx.CalculateGas(
        clientCtx,
        txFactory,
        msgs...,
    )
    if err != nil {
        return 0, err
    }
    
    // Apply a small buffer (1.1x)
    return uint64(float64(gas) * 1.1), nil
}
TypeScript:

typescript
import { SigningStargateClient } from "@cosmjs/stargate";

async function estimateGas(
    client: SigningStargateClient,
    senderAddress: string,
    msgs: EncodeObject[]
): Promise<number> {
    const gasEstimate = await client.simulate(senderAddress, msgs, "");
    // Add 10% buffer for safety
    return Math.floor(gasEstimate * 1.1);
}
Known Gas Values (for reference only)
Transaction Type	Approximate Gas
Bank Send (1 recipient)	80,000 - 110,000
Bank Multi-Send (2 recipients)	120,000 - 150,000
FT Issue	150,000 - 200,000
FT Mint	50,000 - 70,000
NFT Class Issue	100,000 - 130,000
NFT Mint	60,000 - 80,000
⚠️ Warning: These values may change after chain upgrades. Always use simulation for production.

3. Fungible Token (FT) Integration
FTs on TX Blockchain are managed by the assetft module, which wraps the standard bank module. Token information is split between modules.

Token Denom Convention
text
denom = {subunit}-{issuer_address}

Example: uabc-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8
Query Token Information
Get Token Details (assetft module):

bash
# CLI
txd query assetft token cmyft-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8

# REST
curl https://rest.testnet.tx.dev/coreum/asset/ft/v1/tokens/cmyft-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8
Response includes:

denom - Unique token identifier

issuer - Admin address

symbol - Display symbol (e.g., "BTC")

subunit - Base unit (e.g., "satoshi")

precision - Decimal places

features - Enabled features (minting, burning, freezing, whitelisting)

burn_rate - Burn percentage on transfers

send_commission_rate - Commission percentage on transfers

Get Token Balance (bank module):

bash
# CLI
txd query bank balances core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8 --denom=cmyft-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8

# REST
curl https://rest.testnet.tx.dev/cosmos/bank/v1beta1/balances/core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8?denom=cmyft-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8
Get Token Supply (bank module):

bash
# CLI
txd query bank total --denom=cmyft-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8

# REST
curl https://rest.testnet.tx.dev/cosmos/bank/v1beta1/supply/cmyft-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8
Get Token Metadata (bank module):

bash
# CLI
txd query bank denom-metadata --denom=cmyft-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8

# REST
curl https://rest.testnet.tx.dev/cosmos/bank/v1beta1/denoms_metadata/cmyft-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8
FT Features Impact on Wallets
Feature	Impact on Wallet Operations
Freezing	Some tokens may be frozen and not spendable. Check frozen-balance before displaying balance.
Whitelisting	Users can only receive tokens if whitelisted. Transfer failures may occur.
Burn Rate	When sending, a percentage of tokens is burned. Display expected burn to users.
Commission Rate	When sending, a percentage goes to token admin. Display expected commission.
Displaying Correct FT Balance
go
// Golang - Get spendable balance considering frozen tokens
func getSpendableFTBalance(
    ctx context.Context,
    assetftClient assetfttypes.QueryClient,
    bankClient banktypes.QueryClient,
    address string,
    denom string,
) (sdk.Coin, error) {
    // Get total balance from bank module
    bankResp, err := bankClient.Balance(ctx, &banktypes.QueryBalanceRequest{
        Address: address,
        Denom:   denom,
    })
    if err != nil {
        return sdk.Coin{}, err
    }
    
    // Get frozen balance from assetft module
    frozenResp, err := assetftClient.FrozenBalance(ctx, &assetfttypes.QueryFrozenBalanceRequest{
        Account: address,
        Denom:   denom,
    })
    if err != nil {
        // Token might not have freezing feature
        return *bankResp.Balance, nil
    }
    
    // Calculate spendable balance
    total := bankResp.Balance.Amount
    frozen := frozenResp.Balance.Amount
    spendable := total.Sub(frozen)
    
    return sdk.NewCoin(denom, spendable), nil
}
4. Non-Fungible Token (NFT) Integration
NFTs are managed by the assetnft module, which works with the standard nft module.

Class ID Convention
text
class_id = {symbol}-{issuer_address}

Example: punk-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8
Query NFTs
Get NFTs owned by an address:

bash
# CLI
txd query nft balance core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8 punk-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8

# REST
curl "https://rest.testnet.tx.dev/coreum/nft/v1beta1/balance/core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8?class_id=punk-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8"
Get NFT details:

bash
# CLI
txd query nft nft punk-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8 nft-001

# REST
curl https://rest.testnet.tx.dev/coreum/nft/v1beta1/nfts/punk-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8/nft-001
Check if NFT is frozen:

bash
# CLI
txd query assetnft frozen punk-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8 nft-001

# REST
curl https://rest.testnet.tx.dev/coreum/asset/nft/v1/frozen/punk-core1tr3w86yesnj8f290l6ve02cqhae8x4ze0nk0a8/nft-001
5. Transaction Construction
Standard Bank Send
Golang:

go
import (
    banktypes "github.com/cosmos/cosmos-sdk/x/bank/types"
)

func buildBankSendMsg(fromAddress, toAddress string, amount sdk.Coin) sdk.Msg {
    return &banktypes.MsgSend{
        FromAddress: fromAddress,
        ToAddress:   toAddress,
        Amount:      sdk.NewCoins(amount),
    }
}
TypeScript (CosmJS):

typescript
import { MsgSend } from "cosmjs-types/cosmos/bank/v1beta1/tx";
import { Coin } from "@cosmjs/amino";

const sendMsg: MsgSendEncodeObject = {
    typeUrl: "/cosmos.bank.v1beta1.MsgSend",
    value: MsgSend.fromPartial({
        fromAddress: senderAddress,
        toAddress: recipientAddress,
        amount: [{
            denom: "utestcore",
            amount: "1000000",
        } as Coin],
    }),
};
FT Issue Transaction
go
import (
    sdkmath "github.com/cosmos/cosmos-sdk/types/math"
    assetfttypes "github.com/tokenize-x/tx-chain/v3/x/assetft/types"
)

func buildFTIssueMsg(issuer string, subunit string, symbol string, precision uint32, initialAmount int64) sdk.Msg {
    return &assetfttypes.MsgIssue{
        Issuer:        issuer,
        Symbol:        symbol,
        Subunit:       subunit,
        Precision:     precision,
        InitialAmount: sdkmath.NewInt(initialAmount),
        Description:   "Token description",
        Features: []assetfttypes.Feature{
            assetfttypes.Feature_minting,
            assetfttypes.Feature_burning,
        },
    }
}
FT Send (Same as Bank Send)
FTs use the standard bank.MsgSend for transfers.

6. Account Management
Deriving Address from Mnemonic
TypeScript (CosmJS):

typescript
import { DirectSecp256k1HdWallet } from "@cosmjs/proto-signing";
import { stringToPath } from "@cosmjs/crypto";

const mnemonic = "your twelve word mnemonic here";
const prefix = "core"; // or "testcore" for testnet
const hdPath = "m/44'/990'/0'/0/0";

const wallet = await DirectSecp256k1HdWallet.fromMnemonic(mnemonic, {
    prefix: prefix,
    hdPaths: [stringToPath(hdPath)],
});

const [account] = await wallet.getAccounts();
console.log(`Address: ${account.address}`);
BIP44 Path
text
m/44'/990'/0'/0/0
Where:

44' - BIP44 purpose

990' - TX Blockchain coin type

0' - Account index

0 - Change (external addresses)

0 - Address index

Bech32 Prefixes
Network	Account Prefix	Public Key Prefix
Mainnet	core	corepub
Testnet	testcore	testcorepub
Devnet	testcore	testcorepub
7. IBC Token Support
TX Blockchain supports IBC (Inter-Blockchain Communication). IBC tokens follow the standard Cosmos SDK IBC denomination format:

text
ibc/{hash}

Example: ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2
Query IBC Token Metadata
bash
# Get denom trace
curl https://rest.testnet.tx.dev/ibc/apps/transfer/v1/denom_traces/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2

# Response example:
# {
#   "denom_trace": {
#     "path": "transfer/channel-0",
#     "base_denom": "uatom"
#   }
# }
8. Error Handling for Wallets
Common Error Codes
Code	Error	Description	Wallet Action
11	insufficient funds	Account lacks funds	Show insufficient balance error
12	account sequence mismatch	Sequence number incorrect	Retry with latest sequence
13	invalid address	Address format wrong	Validate address format
18	signature verification failed	Invalid signature	Regenerate signature
19	out of gas	Gas limit too low	Increase gas limit
32	token is frozen	FT/NFT frozen	Display frozen status
Handling FT-Specific Errors
typescript
function handleFTError(error: any): string {
    const errorMessage = error.message || String(error);
    
    if (errorMessage.includes("is frozen")) {
        return "Some tokens are frozen and cannot be sent";
    }
    if (errorMessage.includes("whitelisted")) {
        return "Recipient is not whitelisted for this token";
    }
    if (errorMessage.includes("globally frozen")) {
        return "Token is globally frozen, no transfers allowed";
    }
    if (errorMessage.includes("feature not enabled")) {
        return "This operation is not enabled for this token";
    }
    if (errorMessage.includes("unauthorized")) {
        return "You don't have permission for this operation";
    }
    
    return errorMessage;
}
9. Complete Wallet Integration Checklist
Required Features
Address derivation (BIP44 with coin type 990)

Balance query (native + FTs)

Transaction construction (bank send)

Transaction signing

Transaction broadcasting

Fee calculation (dynamic gas price)

Gas estimation (simulation endpoint)

Transaction history query

IBC token support

Recommended Features
FT metadata display (symbol, precision, logo)

Frozen balance display

Commission/burn rate warnings

NFT balance display

NFT details (image, metadata)

Multi-signature support

Staking/delegation support

Governance voting

Network Configuration for Wallets
json
{
  "mainnet": {
    "chainId": "txchain-mainnet-1",
    "chainName": "TX Blockchain",
    "rpc": "https://rpc.tx.org:443",
    "rest": "https://rest.tx.org:443",
    "bech32Prefix": "core",
    "bip44": { "coinType": 990 },
    "currencies": [{
      "coinDenom": "TX",
      "coinMinimalDenom": "utx",
      "coinDecimals": 6
    }],
    "feeCurrencies": [{
      "coinDenom": "TX",
      "coinMinimalDenom": "utx",
      "coinDecimals": 6,
      "gasPriceStep": { "low": 0.0625, "average": 0.06875, "high": 0.075 }
    }]
  },
  "testnet": {
    "chainId": "txchain-testnet-1",
    "chainName": "TX Testnet",
    "rpc": "https://rpc.testnet.tx.dev:443",
    "rest": "https://rest.testnet.tx.dev:443",
    "bech32Prefix": "testcore",
    "bip44": { "coinType": 990 },
    "currencies": [{
      "coinDenom": "TCORE",
      "coinMinimalDenom": "utestcore",
      "coinDecimals": 6
    }],
    "feeCurrencies": [{
      "coinDenom": "TCORE",
      "coinMinimalDenom": "utestcore",
      "coinDecimals": 6,
      "gasPriceStep": { "low": 0.0625, "average": 0.06875, "high": 0.075 }
    }]
  }
}
Next Steps
Review CEX Integration Guide

Read Gas Price Guide

Explore Node Setup Guide

Check AssetFT Module Documentation

Resources
CosmJS Documentation

TX Blockchain Source Code

Keplr Wallet Integration

IBC Protocol Documentation
