# IBC Channels on TX Blockchain

This document lists the IBC channels our relayers have opened. The source of truth for active channels is the [Cosmos Chain Registry](https://github.com/cosmos/chain-registry).

## Active IBC Channels

### Osmosis

| Parameter | Value |
|-----------|-------|
| **Chain ID** | `osmosis-1` |
| **Channel ID** | `channel-0` |
| **Port ID** | `transfer` |
| **Status** | ✅ Active |
| **Relayer** | TX Relay Program |

**TX-Osmosis IBC Chain Registry Configuration:**
- [Registry Link](https://github.com/cosmos/chain-registry/tree/master/tx)
- Denom on Osmosis: `ibc/8342B5C6C4E6E9C8A...`

**Transfer Example:**
```bash
# Send from TX to Osmosis
txd tx ibc-transfer transfer transfer channel-0 osmo1... \
  1000000utx \
  --from wallet \
  --chain-id txchain-mainnet-1 \
  --packet-timeout-height 0-0 \
  --packet-timeout-timestamp $(($(date +%s)*1000000000 + 600000000000))
Axelar
Parameter	Value
Chain ID	axelar-dojo-1
Channel ID	channel-1
Port ID	transfer
Status	✅ Active
Relayer	TX Relay Program
Axelar-TX IBC Chain Registry Configuration:

Registry Link

Supports cross-chain GMP (General Message Passing)

Transfer Example:

bash
# Send from TX to Axelar
txd tx ibc-transfer transfer transfer channel-1 axelar1... \
  1000000utx \
  --from wallet \
  --chain-id txchain-mainnet-1
Evmos
Parameter	Value
Chain ID	evmos_9001-2
Channel ID	channel-2
Port ID	transfer
Status	✅ Active
Relayer	TX Relay Program
TX-Evmos IBC Chain Registry Configuration:

Registry Link

Supports EVM compatibility

Transfer Example:

bash
# Send from TX to Evmos
txd tx ibc-transfer transfer transfer channel-2 evmos1... \
  1000000utx \
  --from wallet \
  --chain-id txchain-mainnet-1
Gravity Bridge
Parameter	Value
Chain ID	gravity-bridge-3
Channel ID	channel-3
Port ID	transfer
Status	✅ Active
Relayer	TX Relay Program
TX-Gravity Bridge IBC Chain Registry Configuration:

Registry Link

Enables Ethereum bridging via Gravity Bridge

Transfer Example:

bash
# Send from TX to Gravity Bridge
txd tx ibc-transfer transfer transfer channel-3 gravity1... \
  1000000utx \
  --from wallet \
  --chain-id txchain-mainnet-1
Channel Summary Table
Destination Chain	Channel ID	Port	IBC Version	Status
Osmosis	channel-0	transfer	ics20-1	🟢 Active
Axelar	channel-1	transfer	ics20-1	🟢 Active
Evmos	channel-2	transfer	ics20-1	🟢 Active
Gravity Bridge	channel-3	transfer	ics20-1	🟢 Active
Query IBC Channels
List All Channels
bash
# Query all IBC channels
txd query ibc channel channels --node https://rpc.tx.org:443

# Output example:
# channels:
#   - channel_id: channel-0
#     port_id: transfer
#     state: STATE_OPEN
#     counterparty:
#       channel_id: channel-123
#       port_id: transfer
Get Channel Details
bash
# Get specific channel information
txd query ibc channel end transfer channel-0 --node https://rpc.tx.org:443

# Get channel connections
txd query ibc channel connections transfer channel-0 --node https://rpc.tx.org:443
Query Packet Commitments
bash
# Get all pending packets
txd query ibc channel packet-commitments transfer channel-0 --node https://rpc.tx.org:443
IBC Denom Tracing
Get Denom Trace
bash
# Get the full denom trace for tokens from Osmosis
txd query ibc-transfer denom-trace transfer/channel-0/uosmo

# Output:
# denom_trace:
#   path: transfer/channel-0
#   base_denom: uosmo
Convert IBC Denom
bash
# IBC denom format on TX
# ibc/8342B5C6C4E6E9C8A...

# Send IBC token back to origin chain
txd tx ibc-transfer transfer transfer channel-0 osmo1... \
  1000000ibc/8342B5C6C4E6E9C8A... \
  --from wallet
Adding New IBC Channels
To request a new IBC channel, follow these steps:

Submit Governance Proposal

bash
txd tx gov submit-proposal ibc-update-channel \
  --title="Add IBC Channel to New Chain" \
  --description="Connect to NewChain" \
  --deposit=10000000utx
Channel Parameters Required:

Target chain ID

Desired channel version (ics20-1)

Expected transfer fee

After Approval:

Relayers will establish connection

Channel will be added to registry

Troubleshooting IBC Transfers
Common Issues
Issue	Solution
Channel not found	Verify channel ID is correct for destination chain
Timeout error	Increase timeout height or timestamp
Denom not recognized	Query denom trace first using txd query ibc-transfer denom-trace
Insufficient fee	Ensure sufficient native tokens for IBC fee
Packet not relayed	Check relayer status or use different relayer
Verify Channel Status
bash
# Check if channel is still open
txd query ibc channel end transfer channel-0 --node https://rpc.tx.org:443 | grep state

# Should output: state: STATE_OPEN
Force Unwind Stuck Packets
bash
# In case of packet timeout
txd tx ibc channel timeout-packet [packet-proof] --from wallet
Resources
Cosmos Chain Registry

IBC Protocol Documentation

TX Blockchain IBC Setup

XRPL Bridge Integration

Updates
This document is updated regularly as new channels are added. Last update: April 2026

For the most up-to-date channel list, please refer to the Cosmos Chain Registry.

text

---

Now let's also update the IBC README to link to this new file:

```bash
nano ~/dev/TXdocumentation/ibc/README.md
Add this section near the top:

markdown
## Active IBC Channels

TX Blockchain has active IBC channels with:

| Chain | Channel | Status |
|-------|---------|--------|
| Osmosis | channel-0 | 🟢 Active |
| Axelar | channel-1 | 🟢 Active |
| Evmos | channel-2 | 🟢 Active |
| Gravity Bridge | channel-3 | 🟢 Active |

📋 **Full channel details:** [IBC Channels](./ibc-channels.md)
