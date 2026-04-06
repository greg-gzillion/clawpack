# TX - XRPL Bridge Integration Guide

This guide explains how to integrate the TX - XRPL Bridge into your project.

## Prerequisites

Before proceeding, ensure you have completed the previous tutorials and understand how to:
- Connect your wallet
- Retrieve the sender account
- Obtain a signing client

## Generating the Smart Contract Interface

Before interacting with the smart contract, you need to generate the client and message composer using `ts-codegen`.

### Generate Client

```bash
ts-codegen generate \
  --plugin client \
  --schema ./schema \
  --out ./ts \
  --name Bridge \
  --no-bundle
Generate Message Composer
bash
ts-codegen generate \
  --plugin message-composer \
  --schema ./schema \
  --out ./ts \
  --name Bridge \
  --no-bundle
Move generated files (Bridge.client.ts, Bridge.message-composer.ts, Bridge.types.ts) into a folder named contract.

Initialize Bridge Components
typescript
const signingClient = <define signingClient here>;
const sender = "testcore123...";
const bridgeContractAddress = "testcore1d90zv8wrwsalluqcezca22zds3dzvjj06fs0v88sh6shhven8pjsgq539p";

const bridgeClient = BridgeClient(signingClient, sender, bridgeContractAddress);
const bridgeMsgComposer = BridgeMsgComposer(sender, bridgeContractAddress);
BridgeClient Methods
Method	Description
config()	Retrieves contract configuration
coreumTokens()	Returns TX-based registered assets
xrplTokens()	Returns XRPL-based registered assets
pendingRefunds()	Fetches unprocessed bridge transactions
claimRefund()	Claims pending refunds
sendToXrpl()	Bridges assets from TX to XRPL
Query Examples
Get Contract Config
typescript
export type BridgeState = "active" | "halted";

export interface Config {
  bridge_state: BridgeState;
  bridge_xrpl_address: string;
  evidence_threshold: number;
  relayers: Relayer[];
  trust_set_limit_amount: Uint128;
  used_ticket_sequence_threshold: number;
  xrpl_base_fee: number;
}

const getConfig = async () => {
  try {
    return await bridgeClient.config();
  } catch (error) {
    console.log(error);
    return null;
  }
}
Get Coreum Tokens
typescript
export interface CoreumToken {
  bridging_fee: Uint128;
  decimals: number;
  denom: string;
  max_holding_amount: Uint128;
  sending_precision: number;
  state: TokenState;
  xrpl_currency: string;
}

const getCoreumTokens = async () => {
  try {
    const response = await bridgeClient.coreumTokens({});
    return response.tokens;
  } catch (error) {
    console.log(error);
    return [];
  }
}
Get XRPL Tokens
typescript
export interface XRPLToken {
  bridging_fee: Uint128;
  coreum_denom: string;
  currency: string;
  issuer: string;
  max_holding_amount: Uint128;
  sending_precision: number;
  state: TokenState;
}

const getXRPLTokens = async () => {
  try {
    const response = await bridgeClient.xrplTokens({});
    return response.tokens;
  } catch (error) {
    console.log(error);
    return [];
  }
}
Get Pending Refunds
typescript
export interface PendingRefund {
  coin: Coin;
  id: string;
  xrpl_tx_hash?: string | null;
}

const getPendingRefunds = async (address: string) => {
  try {
    const response = await bridgeClient.pendingRefunds({ address });
    return response.pending_refunds;
  } catch (error) {
    console.log(error);
    return [];
  }
}
Transaction Examples
Claim Refund
typescript
import { calculateFee } from "@cosmjs/stargate";

const claimRefund = async (refundId: string) => {
  try {
    let fee: StdFee | "auto" = "auto";
    const msg = bridgeMsgComposer.claimRefund({ pendingRefundId: refundId });
    
    const estimatedFee = await getTxFee([msg]);
    if (estimatedFee?.fee) fee = estimatedFee.fee;

    return await bridgeClient.claimRefund({ pendingRefundId: refundId }, fee);
  } catch (error) {
    console.log(error);
    return null;
  }
};
Send to XRPL
typescript
interface SendToXrplArgs {
  recipient: string;
  funds?: Coin[];
  deliverAmount?: string;
}

const sendToXrpl = async ({ recipient, funds, deliverAmount }: SendToXrplArgs) => {
  try {
    let fee: StdFee | "auto" = "auto";
    const denom = funds?.[0].denom;
    
    const msg = bridgeMsgComposer.sendToXrpl({ recipient, deliverAmount }, funds);
    const estimatedFee = await getTxFee([msg]);
    if (estimatedFee?.fee) fee = estimatedFee.fee;

    return await bridgeClient.sendToXrpl(
      { recipient, ...(denom?.includes("xrpl") && deliverAmount ? { deliverAmount } : {}) },
      fee,
      "",
      funds
    );
  } catch (error) {
    console.log(error);
    return null;
  }
};
Send from XRPL to TX
typescript
const convertStringToHex = (value: string) => {
  let hex = '';
  value.split('').forEach((char: string) => {
    hex += char.charCodeAt(0).toString(16).padStart(2, "0");
  });
  return hex;
};

const sendToCoreum = async ({
  xrplAccount,
  recipient,
  amount,
  currency,
  fee,
  deliverAmount,
  tokenIssuer,
}: SendToCosmosArgs) => {
  const contractConfig = await getBridgeContractConfig();

  let currencyAmount = Big(amount).mul(Big(10).pow(6)).toString();
  let sendMaxAmount = amount;

  if (currency.toLowerCase() !== "xrp") {
    const currencyInfo = { currency, issuer: tokenIssuer };
    currencyAmount = { ...currencyInfo, value: deliverAmount };
    sendMaxAmount = { ...currencyInfo, value: amount };
  }

  const memoData = JSON.stringify({
    type: "coreumbridge-xrpl-v1",
    coreum_recipient: recipient,
  });

  const sendTx = {
    TransactionType: "Payment",
    Account: xrplAccount,
    Destination: contractConfig.bridge_xrpl_address,
    Amount: currencyAmount,
    Memos: [{ Memo: { MemoData: convertStringToHex(memoData) } }],
    ...(currency.toLowerCase() !== "xrp" && { SendMax: sendMaxAmount }),
    ...(fee ? { Fee: fee } : {}),
  };

  return await xrplClient?.submit(sendTx);
};
Fee Estimation
typescript
import {
  GasPrice,
  QueryClient,
  calculateFee,
  createProtobufRpcClient,
  decodeCosmosSdkDecFromProto,
} from "@cosmjs/stargate";

const getGasPrice = async () => {
  const feeModel = getFeeModel();
  if (!feeModel) return null;

  const gasPriceMultiplier = 1.1;
  const minGasPriceRes = await feeModel.MinGasPrice({});
  const minGasPrice = decodeCosmosSdkDecFromProto(
    minGasPriceRes.minGasPrice?.amount || ""
  );

  let gasPrice = minGasPrice.toFloatApproximation() * gasPriceMultiplier;
  
  return GasPrice.fromString(`${gasPrice}${minGasPriceRes.minGasPrice?.denom || ""}`);
};

const getTxFee = async (msgs: readonly EncodeObject[]) => {
  const gasPrice = await getGasPrice();
  const gasWanted = await signingClient.simulate(account, msgs, "");
  const totalGasWanted = Big(gasWanted).mul(1.2).toFixed(0);
  
  return { fee: calculateFee(+totalGasWanted, gasPrice) };
};
Complete Flow Example
typescript
// 1. Get bridge configuration
const config = await getBridgeContractConfig();
console.log(`Bridge XRPL Address: ${config.bridge_xrpl_address}`);

// 2. Get available tokens
const coreumTokens = await getCoreumTokens();
const xrplTokens = await getXRPLTokens();

// 3. Send tokens from TX to XRPL
const sendResult = await sendToXrpl({
  recipient: "rXRPLAddress...",
  funds: [{ amount: "1000000", denom: "utestcore" }]
});

// 4. Check for pending refunds
const refunds = await getPendingRefunds(sender);
for (const refund of refunds) {
  await claimRefund(refund.id);
}
Troubleshooting
Issue	Solution
Transaction timeout	Increase gas limit or retry
Insufficient funds	Check balance and bridging fee
Invalid recipient address	Verify XRPL address format
Bridge halted	Check bridge_state in config
text

---

## ISO 20022 Documentation Content

For `~/dev/TXdocumentation/iso20022/README.md`:

```bash
nano ~/dev/TXdocumentation/iso20022/README.md
Paste:

markdown
# ISO 20022 Compliance on TX Blockchain

## Overview

TX Blockchain is designed with native ISO 20022 compliance for financial messaging and interoperability.

## Key Features

- **Native ISO 20022 Message Format** - Financial messages follow ISO 20022 standard
- **SWIFT Compatibility** - Seamless integration with traditional banking
- **Rich Data Structure** - Enhanced payment information
- **Global Reach** - Cross-border payment optimization

## Message Types Supported

| Message Type | Description |
|--------------|-------------|
| pacs.008 | Financial Institution Transfer |
| pacs.009 | Financial Institution Credit Transfer |
| camt.053 | Bank-to-Customer Account Report |
| camt.054 | Bank-to-Customer Debit Credit Notification |

## Integration Guide

### Message Structure

```json
{
  "message_id": "TX2024001",
  "creation_date": "2024-01-15T10:30:00Z",
  "payment_info": {
    "instruction_id": "INST001",
    "end_to_end_id": "E2E001",
    "amount": "1000.00",
    "currency": "USD"
  },
  "debtor": {
    "name": "Sender Name",
    "address": "123 Main St",
    "account": "testcore1..."
  },
  "creditor": {
    "name": "Receiver Name",
    "address": "456 Oak Ave",
    "account": "testcore2..."
  }
}
Benefits
Interoperability - Works with existing financial systems

Rich Data - More transaction information

Compliance - Meets regulatory requirements

Global Standards - Unified messaging format
