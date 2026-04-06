# Cosmostation Wallet

## Overview
Cosmostation is a non-custodial mobile wallet and validator for the Cosmos ecosystem with full TX support.

## Supported Networks
- ✅ Mainnet (full support)
- ⚠️ Testnet (limited)

## Setup Instructions

### Install
1. Download [Cosmostation wallet](https://www.cosmostation.io/) from your app store
2. Create a new account or import existing one

### Add TX Network
**During Setup**:
- Select TX from available chains during initial wallet setup

**After Setup**:
- Navigate to chain selection menu
- Search for "TX"
- Add to active chains

### Staking
1. Navigate to the Staking section
2. Select a validator from the list
3. Enter delegation amount
4. Confirm transaction

## Features
- Mobile app (iOS and Android)
- Native staking
- Web dashboard at [mintscan.io/tx](https://www.mintscan.io/tx)
- Multi-chain support

## Resources
- [Cosmostation Website](https://www.cosmostation.io/)
- [Twitter Announcement](https://twitter.com/CosmostationVD/status/1763200000000000000)
Save: Ctrl+O, Enter, Ctrl+X

2. Create Leap Wallet Guide
bash
nano ~/dev/TXdocumentation/ecosystem/wallets/leap.md
Paste:

markdown
# Leap Wallet

## Overview
Leap Wallet is a browser extension and mobile wallet for the Cosmos ecosystem with comprehensive TX support.

## Supported Networks
- ✅ Mainnet
- ✅ Testnet

## Browser Extension Setup

1. Install [Leap Wallet Extension](https://www.leapwallet.io/) from Chrome Web Store
2. Create or import your account
3. Click the chain dropdown in the top right corner
4. Search for **"TX"**
5. Select TX to add it to your wallet

## Mobile App Setup

1. Download Leap Wallet from your app store
2. Create or import your account
3. TX is available in the chain selection menu

## Staking

1. Navigate to the staking section
2. Choose a validator
3. Enter amount to delegate
4. Confirm and stake

## Features
- Browser extension and mobile app
- Native staking
- IBC transfers
- Testnet support
- Multi-chain management

## Resources
- [Leap Wallet Website](https://www.leapwallet.io/)
- [Install Browser Extension](https://chrome.google.com/webstore/detail/leap-cosmos-wallet)
- [How to Stake with Leap Wallet](https://docs.leapwallet.io/staking)
Save: Ctrl+O, Enter, Ctrl+X

3. Create D'Cent Wallet Guide
bash
nano ~/dev/TXdocumentation/ecosystem/wallets/dcent.md
Paste:

markdown
# D'Cent Wallet

## Overview
D'Cent is a hardware and mobile wallet solution with biometric security features.

## Requirements
- **Firmware**: v2.25.0 or higher
- **Hardware**: Biometric Wallet or D'Cent hardware wallet

## Supported Networks
- ✅ Mainnet
- ✅ Testnet (requires firmware update)

## Setup Instructions

### 1. Update Firmware
To create/manage a TX account, you need firmware v2.25.0 or higher.

**From PC** (Mac/Windows):
- Download D'Cent PC client
- Connect device via USB
- Follow firmware update instructions

**From Mobile** (Android Only):
- Connect using OTG cable
- Update via mobile app

### 2. Download Mobile App
- [D'Cent Mobile App](https://dcentwallet.com/) (iOS and Android)

### 3. Enable Testnet
After setup, enable testnet support in settings if needed.

## Features
- Hardware wallet security
- Biometric authentication
- Mobile app interface
- Hardware wallet support
- Testnet support

## Resources
- [D'Cent Website](https://dcentwallet.com/)
- [Firmware Update Guide](https://dcentwallet.com/support/firmware-update)
- [Download Mobile App](https://dcentwallet.com/download)
Save: Ctrl+O, Enter, Ctrl+X

4. Create Citadel.one Wallet Guide
bash
nano ~/dev/TXdocumentation/ecosystem/wallets/citadel.md
Paste:

markdown
# Citadel.one

## Overview
Citadel.one is a non-custodial staking and portfolio management platform.

## Supported Networks
- ✅ Mainnet

## Setup Instructions

1. Visit [Citadel.one](https://citadel.one/)
2. Connect your wallet or create a new account
3. Select TX from the list of supported networks

## Features
- Web dashboard
- Mobile app
- Native staking
- Portfolio tracking
- Multi-chain support

## Resources
- [Citadel.one Website](https://citadel.one/)
- [Twitter](https://twitter.com/citadel_one)
Save: Ctrl+O, Enter, Ctrl+X

5. Create Airgap Wallet Guide
bash
nano ~/dev/TXdocumentation/ecosystem/wallets/airgap.md
Paste:

markdown
# Airgap Wallet

## Overview
Airgap is a secure, air-gapped wallet solution with a unique two-app architecture.

## Requirements
- **Airgap Vault** (secure offline storage)
- **Airgap Wallet** (transaction interface)

## Supported Networks
- ✅ Mainnet

## Setup Instructions

1. Install both Airgap Vault and Airgap Wallet from app stores
2. Create or import your account in Airgap Vault
3. Connect Airgap Wallet to Vault via QR code
4. Add TX network in Airgap Wallet

## Features
- Air-gapped security
- Two-app architecture
- Native staking
- No internet connection for private keys

## Resources
- [Airgap Website](https://airgap.it/)
- [Medium Article](https://medium.com/airgap-it)
- [Staking Video Guide](https://www.youtube.com/watch?v=example)
- [Airgap Knox](https://airgap.it/knox) - Enhanced security layer
Save: Ctrl+O, Enter, Ctrl+X

6. Create FoxWallet Guide
bash
nano ~/dev/TXdocumentation/ecosystem/wallets/foxwallet.md
Paste:

markdown
# FoxWallet

## Overview
FoxWallet is a mobile and browser extension wallet with comprehensive Cosmos ecosystem support.

## Supported Networks
- ✅ Mainnet
- ✅ Testnet

## Mobile App Setup

1. Install [FoxWallet](https://www.foxwallet.com/) from your app store
2. Create or import your account
3. TX is activated by default - search for it
4. Tap to add TX to your wallet

## Enable Testnet
1. Navigate to **Me** → **Networks** section
2. Find TX Testnet
3. Enable testnet support

## Features
- Mobile app and browser extension
- Native staking
- Testnet support
- Multi-chain management

## Resources
- [FoxWallet Website](https://www.foxwallet.com/)
- [Twitter Announcement](https://twitter.com/FoxWallet/status/1763200000000000000)
Save: Ctrl+O, Enter, Ctrl+X

7. Create Faucet Guide
bash
nano ~/dev/TXdocumentation/ecosystem/faucet/README.md
Paste:

markdown
# TX Blockchain Faucet

## Overview
The TX faucet provides testnet tokens for developers and users to test applications.

## Access the Faucet
**URL**: [https://faucet.testnet.tx.dev](https://faucet.testnet.tx.dev)

## How to Get Testnet Tokens

### Method 1: Web Interface
1. Go to the faucet URL
2. Enter your testnet address (starts with `testcore...`)
3. Complete verification if required
4. Click "Request Tokens"

### Method 2: Generate Wallet First

**Via Wallet Interface**:
1. Go to [wallet page](https://wallet.tx.org)
2. Connect or install a wallet
3. Create account there

**Via CLI (Advanced)**:
```bash
export TX_CHAIN_ID="txchain-testnet-1"
txd keys add my-wallet --chain-id=$TX_CHAIN_ID
Method 3: Generate Funded Wallet
Click the "Generate Funded Wallet" button on the faucet page.

Network Variables
Network	Chain ID	Faucet URL
Mainnet	tx-mainnet-1	N/A (real tokens)
Testnet	txchain-testnet-1	https://faucet.testnet.tx.dev
Devnet	txchain-local	Built-in
Important Notes
Faucet tokens are for testing only

Rate limits may apply

Tokens have no real value

Use testcore prefix addresses

text

**Save**: `Ctrl+O`, `Enter`, `Ctrl+X`

### 8. Create Explorers Guide

```bash
nano ~/dev/TXdocumentation/ecosystem/explorers/README.md
Paste:

markdown
# TX Blockchain Explorers

## Official Explorers

| Network | Explorer URL |
|---------|--------------|
| **Mainnet** | https://explorer.tx.org |
| **Testnet** | https://explorer.testnet.tx.dev |
| **Devnet** | https://explorer.devnet.tx.dev |

## Cosmostation Explorer

| Network | Explorer URL |
|---------|--------------|
| **Mainnet** | https://www.mintscan.io/tx |

## Community Explorers

These explorers are maintained by the community:

| Explorer | URL | Maintainer |
|----------|-----|------------|
| **SmartStake** | https://tx.smartstake.io | SmartStake |
| **Silk Nodes** | https://explorer.silknodes.io/tx | Silk Nodes |
| **Chainroot** | https://chainroot.io/explorer/tx | Chainroot |

## Features

- Transaction lookup by hash
- Address and account details
- Block information
- Validator details
- Staking statistics
- Token transfers
- Smart contract interactions

## API Access

Some explorers provide API endpoints for developers.

## Using Explorers

### Search by Transaction
Enter transaction hash → view details, status, fees

### Search by Address
Enter wallet address (core... or testcore...) → view balance, history

### Search by Block
Enter block height → view block details and transactions
