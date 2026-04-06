# IBC Transfer to Osmosis Using Keplr Wallet

This guide walks you through the steps involved in sending an IBC transfer to Osmosis using the Keplr wallet.

## Prerequisites

- Keplr wallet installed ([download here](https://www.keplr.app/))
- TX Blockchain added to Keplr
- Sufficient balance of tokens on TX Blockchain
- Developer Mode enabled in Keplr

## Step-by-Step Guide

### 1. Open Keplr Wallet

Start by opening your Keplr wallet extension in your browser.

### 2. Navigate to Advanced IBC Transaction

In your Keplr wallet, navigate to the section where you can initiate an advanced IBC transaction.

> **⚠️ Note:** If you do not have "Developer Mode" enabled on your Keplr Wallet, you will not see this option. To enable developer mode, go to **Settings → Advanced**, and enable **"Developer Mode"**.

### 3. Select Asset

Choose the asset/token you want to transfer (e.g., `utx` or `utestcore`). Ensure you have sufficient balance for the transfer including fees.

### 4. Choose Destination Chain

#### Adding IBC Transfer Channel in Keplr

You must first add the IBC Transfer Channel to Keplr:

1. Click on destination chain selector
2. You will see **"Add New IBC Transfer Channel"** with a **"+"** icon
3. Choose the relevant destination chain (Osmosis)

Next, add the IBC Channel configuration:

| Parameter | Value |
|-----------|-------|
| **Source Channel ID** | `channel-0` |
| **Destination Chain** | Osmosis |
| **Port ID** | `transfer` |

> **📋 Reference:** You can find the relevant configurations for TX here: [TX IBC Channels](./ibc-channels.md)

### 5. Enter Wallet Address

Provide the recipient's wallet address on the destination chain (Osmosis format: `osmo1...`)

### 6. Enter Amount

Specify the amount of the asset you wish to transfer. Remember to account for transaction fees.

### 7. Review Transaction

Review all the details of the transfer:
- Source chain (TX Blockchain)
- Destination chain (Osmosis)
- Amount being sent
- Recipient address
- Estimated fees

### 7a. Confirm Transaction Details

Keplr might ask you to confirm the transaction details once more. Double-check and proceed.

### 7b. Approve Transaction

Ensure all transaction data is correct including:
- Amount
- Destination address
- Asset type
- Channel information

### 10. Final Transaction Confirmation

Before the transaction is broadcasted, confirm it for the last time. This is the final step before the transaction is sent to the network.

### 11. Transaction Explorer

Once the transaction is confirmed, you can view it on TX's blockchain explorer.

> **⏱️ Important:** IBC transactions might not be instantaneous. There's a brief delay between sending the transaction from the source chain and receiving it on the destination chain. Additionally, if a transaction timeouts for any reason, this will be visible on the source chain, not the destination chain. Always monitor the source chain's explorer for any timeout or error messages.

### 12. Transaction Hash

This is the unique identifier for your transaction. You can use it to track the status of your transfer.

### 13. Explorer Transaction Messages

In the blockchain explorer, you can see detailed messages associated with your transaction.

#### Transfer Message Example

```json
{
    "memo": "",
    "@type": "/ibc.applications.transfer.v1.MsgTransfer",
    "token": {
        "denom": "ucore",
        "amount": "52931"
    },
    "sender": "core10zt2r5p2zh9ltcyg98zt2gtmcypkqgq3qsfj74",
    "receiver": "osmo1pwvcapna75slt3uscvupfe52492yuzhflhakem",
    "source_port": "transfer",
    "source_channel": "channel-2",
    "timeout_height": {
        "revision_height": "10958485",
        "revision_number": "1"
    },
    "timeout_timestamp": "0"
}
Transfer Logs Example
json
[
    {
        "events": [
            {
                "type": "coin_received",
                "attributes": [
                    {
                        "key": "receiver",
                        "value": "core12k2pyuylm9t7ugdvz67h9pg4gmmvhn5vvgafk0"
                    },
                    {
                        "key": "amount",
                        "value": "52931ucore"
                    }
                ]
            },
            {
                "type": "coin_spent",
                "attributes": [
                    {
                        "key": "spender",
                        "value": "core10zt2r5p2zh9ltcyg98zt2gtmcypkqgq3qsfj74"
                    },
                    {
                        "key": "amount",
                        "value": "52931ucore"
                    }
                ]
            },
            {
                "type": "ibc_transfer",
                "attributes": [
                    {
                        "key": "sender",
                        "value": "core10zt2r5p2zh9ltcyg98zt2gtmcypkqgq3qsfj74"
                    },
                    {
                        "key": "receiver",
                        "value": "osmo1pwvcapna75slt3uscvupfe52492yuzhflhakem"
                    }
                ]
            },
            {
                "type": "message",
                "attributes": [
                    {
                        "key": "action",
                        "value": "/ibc.applications.transfer.v1.MsgTransfer"
                    },
                    {
                        "key": "sender",
                        "value": "core10zt2r5p2zh9ltcyg98zt2gtmcypkqgq3qsfj74"
                    },
                    {
                        "key": "module",
                        "value": "ibc_channel"
                    },
                    {
                        "key": "module",
                        "value": "transfer"
                    }
                ]
            },
            {
                "type": "send_packet",
                "attributes": [
                    {
                        "key": "packet_data",
                        "value": "{\"amount\":\"52931\",\"denom\":\"ucore\",\"receiver\":\"osmo1pwvcapna75slt3uscvupfe52492yuzhflhakem\",\"sender\":\"core10zt2r5p2zh9ltcyg98zt2gtmcypkqgq3qsfj74\"}"
                    },
                    {
                        "key": "packet_data_hex",
                        "value": "7b22616d6f756e74223a223532393331222c2264656e6f6d223a2275636f7265222c227265636569766572223a226f736d6f317077766361706e613735736c74337573637675706665353234393279757a68666c68616b656d222c2273656e646572223a22636f726531307a7432723570327a68396c7463796739387a743267746d6379706b716771337173666a3734227d"
                    },
                    {
                        "key": "packet_timeout_height",
                        "value": "1-10958485"
                    },
                    {
                        "key": "packet_timeout_timestamp",
                        "value": "0"
                    },
                    {
                        "key": "packet_sequence",
                        "value": "17"
                    },
                    {
                        "key": "packet_src_port",
                        "value": "transfer"
                    },
                    {
                        "key": "packet_src_channel",
                        "value": "channel-2"
                    },
                    {
                        "key": "packet_dst_port",
                        "value": "transfer"
                    },
                    {
                        "key": "packet_dst_channel",
                        "value": "channel-2188"
                    },
                    {
                        "key": "packet_channel_ordering",
                        "value": "ORDER_UNORDERED"
                    },
                    {
                        "key": "packet_connection",
                        "value": "connection-3"
                    }
                ]
            },
            {
                "type": "transfer",
                "attributes": [
                    {
                        "key": "recipient",
                        "value": "core12k2pyuylm9t7ugdvz67h9pg4gmmvhn5vvgafk0"
                    },
                    {
                        "key": "sender",
                        "value": "core10zt2r5p2zh9ltcyg98zt2gtmcypkqgq3qsfj74"
                    },
                    {
                        "key": "amount",
                        "value": "52931ucore"
                    }
                ]
            }
        ]
    }
]
14. Verify Successful Transfer to Osmosis
After the transfer completes, you can verify your tokens have arrived on Osmosis:

Open Keplr and switch to Osmosis chain

Check your balance

Tokens will appear as "CORE on Osmosis" with an IBC label

The denom will be in IBC format: ibc/8342B5C6C4E6E9C8A...

Channel Configuration Reference
Network	Source Channel	Destination Channel	Port
Mainnet	channel-0	channel-2188	transfer
Testnet	channel-2	channel-2188	transfer
Troubleshooting
Issue	Solution
"Developer Mode" not showing	Go to Settings → Advanced → Enable Developer Mode
Channel not found	Ensure channel is registered in IBC Chain Registry
Transaction timeout	Increase timeout height or retry
Insufficient balance	Check balance includes fees
Recipient address invalid	Verify address format matches destination chain
Important Notes
⏱️ IBC transfers take 1-5 minutes to complete

🔍 Monitor the source chain explorer for timeout errors

💰 Always keep extra tokens for transaction fees

🔐 Double-check recipient addresses before signing

📋 Save transaction hash for reference

Resources
TX IBC Channels

IBC Overview

Keplr Wallet Support

Osmosis Explorer

text

---

Now let's update the IBC README to link to this new guide:

```bash
nano ~/dev/TXdocumentation/ibc/README.md
Add this section:

markdown
## User Guides

### Keplr Wallet IBC Transfers

For step-by-step instructions on sending IBC transfers using Keplr wallet:

📖 **[IBC Transfer to Osmosis Using Keplr Wallet](./keplr-ibc-transfer-osmosis.md)**

This guide covers:
- Enabling Developer Mode in Keplr
- Adding IBC transfer channels
- Step-by-step transaction walkthrough
- Transaction verification on explorers
- Troubleshooting common issues
