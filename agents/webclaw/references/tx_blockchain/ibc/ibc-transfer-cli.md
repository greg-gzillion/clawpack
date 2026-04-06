# IBC Transfer Using CLI

Inter-Blockchain Communication (IBC) is a protocol that allows different blockchains to communicate with each other, enabling the transfer of tokens and other data across chains. In this guide, we'll dive into how to use the CLI to test IBC transfers, specifically between TX and Osmosis chains.

## Prerequisites

1. **Install the CLI tools**: Ensure you have both `txd` and `osmosisd` CLI tools installed and accessible from your terminal.

   ```bash
   # Verify installations
   txd version
   osmosisd version
Configure your CLI: Set up your CLI with the necessary chain configurations, keys, and other required parameters.

bash
# Add TX wallet
txd keys add my-wallet

# Add Osmosis wallet (if needed)
osmosisd keys add my-osmo-wallet
IBC Channel Information
Direction	Source Chain	Source Channel	Destination Channel
TX → Osmosis	TX	channel-2	channel-2188
Osmosis → TX	Osmosis	channel-2188	channel-2
Tutorial
1. Sending Tokens to Osmosis from TX
To initiate an IBC transfer from TX to Osmosis, use the txd CLI tool.

Command Syntax
bash
txd tx ibc-transfer transfer transfer [channel-id] [destination-address] [amount] \
    --from [sender-key] \
    --chain-id [chain-id] \
    --node [rpc-endpoint] \
    --packet-timeout-height [timeout-height] \
    --packet-timeout-timestamp [timeout-timestamp]
Example: Send 1000 ucore to Osmosis
bash
txd tx ibc-transfer transfer transfer channel-2 \
    osmo16q5ca0kz5tl0arxnt4ynzyk5xs5tq24lfrywnx \
    1000ucore \
    --from dev-wallet \
    --chain-id txchain-testnet-1 \
    --node https://rpc.testnet.tx.dev:443 \
    --packet-timeout-height 0-0 \
    --packet-timeout-timestamp $(($(date +%s)*1000000000 + 600000000000))
Parameters Explained
Parameter	Description
transfer	Port ID for IBC transfers
channel-2	IBC channel ID from TX to Osmosis
destination-address	Recipient's Osmosis address
amount	Amount in smallest denomination (e.g., ucore)
--from	Your TX wallet key name
--packet-timeout-height	Block height timeout (0-0 = disabled)
--packet-timeout-timestamp	Timestamp timeout (nanoseconds, 10 min default)
2. Sending Tokens back to TX from Osmosis
To transfer tokens from Osmosis back to TX, use the osmosisd CLI tool.

Command Syntax
bash
osmosisd tx ibc-transfer transfer transfer [channel-id] [destination-address] [amount] \
    --fees [fee-amount] \
    --from [sender-key] \
    --chain-id [chain-id] \
    --node [rpc-endpoint]
Example: Send IBC tokens back to TX
bash
osmosisd tx ibc-transfer transfer transfer channel-2188 \
    core1msa5mwyvjqlc4nj4ym2q8nqrs0dq9t6nx27mu7 \
    1000ibc/927661F31AA9C5801D58104292A35053097B393CFFA0D9B6CB450A3D66D747FA \
    --fees 875uosmo \
    --from test \
    --chain-id osmosis-1 \
    --node https://rpc.osmosis.zone:443
Parameters Explained
Parameter	Description
channel-2188	IBC channel ID from Osmosis to TX
destination-address	Recipient's TX address
ibc/927661F3...	IBC token denomination (hashed format)
--fees 875uosmo	Transaction fee in Osmosis uosmo
--chain-id osmosis-1	Osmosis mainnet chain ID
Understanding IBC Token Denomination (denom)
The IBC token denomination format appears unconventional compared to what most blockchain developers might be accustomed to. Let's understand why it's structured this way and how to determine the correct denom for your transfers.

The IBC Token Denomination Format
The denom for IBC transfers has a specific format: ibc/HASH

Part	Description
ibc/	Prefix indicating the token follows IBC token standards
HASH	SHA-256 hash of the IBC path: ibc-port/ibc-channel/native-denom
Why Hashed Format?
The hashed format ensures a unique identifier for tokens across different chains, preventing naming conflicts or ambiguities. Since tokens can be sent across multiple chains, each with its native denominations, the IBC protocol adopts this hashing mechanism to generate a unique identifier for every token on every chain.

Generating the IBC Token Denomination
Use this script to derive the denomination format:

bash
#!/bin/sh
# Run with "ibc-port/ibc-channel/native-denom" as an argument
IBCD="$1"
echo -n $IBCD | openssl dgst -sha256 | awk '{print "ibc/" toupper($2)}'
Usage Steps
Save the script to a file (e.g., get_ibc_denom.sh):

bash
nano get_ibc_denom.sh
Make it executable:

bash
chmod +x get_ibc_denom.sh
Run the script with the appropriate argument:

bash
./get_ibc_denom.sh "transfer/channel-2/ucore"
Example output:

text
ibc/927661F31AA9C5801D58104292A35053097B393CFFA0D9B6CB450A3D66D747FA
Manual Hash Generation (Alternative)
bash
# Generate hash for TX to Osmosis path
echo -n "transfer/channel-2/ucore" | sha256sum | tr 'a-f' 'A-F' | awk '{print "ibc/" $1}'

# Output: ibc/927661F31AA9C5801D58104292A35053097B393CFFA0D9B6CB450A3D66D747FA
Common IBC Paths
TX to Osmosis
Component	Value
Port	transfer
Channel	channel-2
Native Denom	ucore
IBC Path	transfer/channel-2/ucore
IBC Denom	ibc/927661F31AA9C5801D58104292A35053097B393CFFA0D9B6CB450A3D66D747FA
Osmosis to TX
Component	Value
Port	transfer
Channel	channel-2188
Native Denom	uosmo
IBC Path	transfer/channel-2188/uosmo
IBC Denom	ibc/ED07A3391A112B175915CD8FAF43A2DA8E6F5DFC04D1434C0B2B1D41681D5F9F
Verifying IBC Transfers
Query IBC Transfer Status on TX
bash
# Check packet commitments
txd query ibc channel packet-commitments transfer channel-2 \
    --node https://rpc.testnet.tx.dev:443

# Check packet acknowledgements
txd query ibc channel packet-acknowledgements transfer channel-2 \
    --node https://rpc.testnet.tx.dev:443
Query Balance After Transfer
bash
# Check TX balance (original denom)
txd query bank balances core1... --denom ucore \
    --node https://rpc.testnet.tx.dev:443

# Check IBC token balance on Osmosis
osmosisd query bank balances osmo1... --denom ibc/927661F31AA9C5801D58104292A35053097B393CFFA0D9B6CB450A3D66D747FA \
    --node https://rpc.osmosis.zone:443
Complete Transfer Example
Step 1: Prepare Wallets
bash
# Create TX wallet
txd keys add tx-sender
TX_ADDRESS=$(txd keys show tx-sender -a)
echo "TX Address: $TX_ADDRESS"

# Create Osmosis wallet (or use existing)
osmosisd keys add osmo-receiver
OSMO_ADDRESS=$(osmosisd keys show osmo-receiver -a)
echo "Osmosis Address: $OSMO_ADDRESS"
Step 2: Fund TX Wallet
Use the TX Testnet Faucet to fund your wallet.

Step 3: Send IBC Transfer from TX to Osmosis
bash
txd tx ibc-transfer transfer transfer channel-2 \
    $OSMO_ADDRESS \
    1000000ucore \
    --from tx-sender \
    --chain-id txchain-testnet-1 \
    --node https://rpc.testnet.tx.dev:443 \
    --packet-timeout-timestamp $(($(date +%s)*1000000000 + 600000000000)) \
    -y
Step 4: Monitor Transfer
bash
# Watch for packet events
txd query txs --events "message.action=/ibc.applications.transfer.v1.MsgTransfer" \
    --node https://rpc.testnet.tx.dev:443 | jq '.txs[-1]'
Step 5: Verify on Osmosis
bash
# Query the IBC denom balance
IBC_DENOM="ibc/927661F31AA9C5801D58104292A35053097B393CFFA0D9B6CB450A3D66D747FA"
osmosisd query bank balances $OSMO_ADDRESS --denom $IBC_DENOM \
    --node https://rpc.osmosis.zone:443
Step 6: Send Back to TX (Optional)
bash
osmosisd tx ibc-transfer transfer transfer channel-2188 \
    $TX_ADDRESS \
    500000$IBC_DENOM \
    --fees 875uosmo \
    --from osmo-receiver \
    --chain-id osmosis-1 \
    --node https://rpc.osmosis.zone:443 \
    --packet-timeout-timestamp $(($(date +%s)*1000000000 + 600000000000)) \
    -y
Troubleshooting
Issue	Solution
channel not found	Verify channel ID is correct for your network
insufficient funds	Ensure you have enough tokens for transfer + fees
timeout error	Increase timeout timestamp or use height-based timeout
invalid denom	Generate correct IBC denom using the script above
packet not relayed	Check if relayer is active or wait longer
sequence mismatch	Wait a few seconds and retry
IBC Explorer Links
Chain	Explorer
TX Blockchain	https://explorer.tx.org
Osmosis	https://explorer.osmosis.zone
Resources
IBC Channels

Keplr IBC Transfer Guide

IBC Smart Contract Call Tutorial

IBC WASM Transfer Tutorial

Conclusion
You've now learned how to use the CLI to test IBC transfers between TX and Osmosis. Remember to:

✅ Double-check addresses before initiating transfers

✅ Verify channel IDs for your target network

✅ Generate correct IBC denoms using the provided script

✅ Monitor both source and destination explorers

✅ Account for transaction fees on both chains

text

---

Now update the IBC README to include this CLI guide:

```bash
nano ~/dev/TXdocumentation/ibc/README.md
Add this section:

markdown
## CLI User Guides

### IBC Transfer Using CLI

For step-by-step CLI instructions for IBC transfers between TX and Osmosis:

📖 **[IBC Transfer Using CLI](./ibc-transfer-cli.md)**

This guide covers:
- Sending tokens from TX to Osmosis
- Sending tokens back from Osmosis to TX
- Understanding IBC token denominations
- Generating IBC denom hashes
- Verifying transfer status
- Complete end-to-end examples
