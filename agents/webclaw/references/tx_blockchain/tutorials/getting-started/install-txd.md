# Install txd

This document provides instructions on how to install the release binaries of `txd`.

## Choose Your Installation Method

| Method | OS Support | Difficulty | Use Case |
|--------|------------|------------|----------|
| **Prebuilt Binary (Linux)** | Linux only | Easy | CLI interaction, quick start |
| **Build from Sources** | Linux, macOS | Medium | Development, custom builds |
| **Prebuilt (macOS)** | macOS only | Easy | Development on Mac |
| **Prebuilt (Windows/WSL)** | Windows | Medium | Windows development |
| **Docker** | All | Easy | Containerized environment |

---

## Method 1: Install Prebuilt txd (Linux)

> **Note**: This option supports Linux OS only. Use this for CLI interaction with the chain.

### Prerequisites

- [ ] Network variables set up ([Network Variables](./network-variables.md))
- [ ] `curl` installed: `sudo apt install curl -y`

### Step 1: Create Directory Structure

```bash
# Create bin directory
mkdir -p $TX_HOME/bin
Step 2: Download txd Binary
bash
# Download binary
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME

# Move to bin directory
mv $TX_BINARY_NAME $TX_HOME/bin/txd
If you get a 404 error:

bash
# Verify the URL
echo https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME

# Check available releases
curl -s https://api.github.com/repos/tokenize-x/tx-chain/releases | jq '.[].tag_name'

# Update TX_VERSION to a valid version
export TX_VERSION="v6.1.0"
Step 3: Add to PATH and Make Executable
bash
# Add to PATH
export PATH=$PATH:$TX_HOME/bin

# Make executable
chmod +x $TX_HOME/bin/txd

# Make PATH permanent
echo 'export PATH="$PATH:$HOME/.txd/bin"' >> ~/.bashrc
source ~/.bashrc
Step 4: Verify Installation
bash
# Check version
txd version

# Expected output: v6.1.0
Method 2: Build from Sources
Prerequisites
bash
# Install Go 1.21+
wget https://golang.org/dl/go1.21.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc

# Install build tools
sudo apt install -y git make gcc
Step 1: Clone Repository
bash
git clone https://github.com/tokenize-x/tx-chain.git
cd tx-chain
Step 2: Build Binary
bash
# Checkout desired version
git checkout v6.1.0

# Build
make build

# Binary is at ./build/txd
Step 3: Install
bash
# Install to /usr/local/bin
sudo make install

# Or copy manually
cp ./build/txd /usr/local/bin/txd
Step 4: Verify
bash
txd version
For more details, see the Build and Play documentation.

Method 3: Install Prebuilt txd (macOS)
Step 1: Export Network Variables
Open Terminal and set variables:

bash
# For testnet
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_VERSION="v6.1.0"
export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"
export TX_BINARY_NAME=$(uname -m | sed 's/arm64/txd-darwin-arm64/' | sed 's/x86_64/txd-darwin-amd64/')
Step 2: Configure .bash_profile
bash
nano ~/.bash_profile
Add these lines:

bash
# TX Blockchain Environment
export PATH="/Users/$USER/.txd/bin:$PATH"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_DENOM="utestcore"
export TX_VERSION="v6.1.0"
export TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
export TX_NODE_ARGS="--node=$TX_NODE"
export TX_CHAIN_ID="txchain-testnet-1"
export TX_HOME="$HOME/.txd/$TX_CHAIN_ID"
export TX_BINARY_NAME=$(uname -m | sed 's/arm64/txd-darwin-arm64/' | sed 's/x86_64/txd-darwin-amd64/')
Save: Ctrl+O, Enter, Ctrl+X

Step 3: Apply Changes
bash
source ~/.bash_profile
Step 4: Download and Install
bash
# Create directory
mkdir -p $TX_HOME/bin

# Download binary
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME

# Move and make executable
mv $TX_BINARY_NAME $TX_HOME/bin/txd
chmod +x $TX_HOME/bin/txd

# Add to PATH
export PATH=$PATH:$TX_HOME/bin
Step 5: Verify
bash
txd version
Method 4: Install Prebuilt (Windows/WSL)
Step 1: Find PowerShell
Press Windows + X and select "Windows PowerShell (Admin)"

Step 2: Install Microsoft WSL
Follow Microsoft's WSL Installation Guide

Step 3: Start WSL
powershell
# In PowerShell, start WSL
wsl

# Or start specific distribution
wsl -d Ubuntu
Step 4: Configure Environment Variables
bash
# Open bash configuration
nano ~/.bashrc
Add these variables at the end:

bash
# TX Blockchain Environment
export TX_CHAIN_ID="txchain-testnet-1"
export TX_DENOM="utestcore"
export TX_PREFIX="testcore"
export TX_NODE="https://rpc.testnet.tx.dev:443"
export TX_VERSION="v6.1.0"
export TX_HOME=$HOME/.txd/"$TX_CHAIN_ID"
export TX_BINARY_NAME=$(arch | sed s/aarch64/txd-linux-arm64/ | sed s/x86_64/txd-linux-amd64/)
Step 5: Apply and Verify
bash
source ~/.bashrc

# Verify variables
echo $TX_CHAIN_ID
echo $TX_HOME
Step 6: Download and Install
bash
# Create directory
mkdir -p $TX_HOME/bin

# Download binary
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME

# Move and make executable
mv $TX_BINARY_NAME $TX_HOME/bin/txd
chmod +x $TX_HOME/bin/txd

# Add to PATH
export PATH=$PATH:$TX_HOME/bin
echo 'export PATH="$PATH:$HOME/.txd/bin"' >> ~/.bashrc
Step 7: Verify
bash
txd version
Method 5: Set Up txd Using Docker
Step 1: Install Docker
Download Docker from the official website

Step 2: Create Dockerfile
Create a file named Dockerfile:

dockerfile
# Use Alpine Linux for the final image
FROM alpine:latest as base

# Install necessary packages
RUN apk add --no-cache ca-certificates curl bash

# Set environment variables
ENV TX_CHAIN_ID="txchain-testnet-1"
ENV TX_DENOM="utestcore"
ENV TX_NODE="https://rpc.testnet.tx.dev:443"
ENV TX_VERSION="v6.1.0"

ENV TX_CHAIN_ID_ARGS="--chain-id=$TX_CHAIN_ID"
ENV TX_NODE_ARGS="--node=$TX_NODE"

ENV TX_HOME="/root/.txd/$TX_CHAIN_ID"
ENV TX_BINARY_NAME="txd-linux-amd64"

# Create directories
RUN mkdir -p $TX_HOME/bin

# Download the txd binary
RUN curl -Lo $TX_HOME/bin/txd https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME

# Make the binary executable
RUN chmod +x $TX_HOME/bin/txd

# Add the binary to PATH
ENV PATH=$PATH:$TX_HOME/bin

# Expose necessary ports
EXPOSE 26656 26657 9090 9091 1317 6060 26660

# Keep container running
CMD ["tail", "-f", "/dev/null"]
Step 3: Build Docker Image
bash
docker build -t tx-txd .
Step 4: Run Docker Container
bash
docker run -d \
  --name tx-txd-container \
  -p 26656:26656 \
  -p 26657:26657 \
  -p 9090:9090 \
  -p 9091:9091 \
  -p 1317:1317 \
  -p 6060:6060 \
  -p 26660:26660 \
  tx-txd
Step 5: Verify Container
bash
# Check container is running
docker ps

# Access container shell
docker exec -it tx-txd-container /bin/bash

# Test binary
txd version
Verification Checklist
After installation, run these checks:

bash
# 1. Check version
txd version

# 2. Check help
txd --help

# 3. Check node connection
txd status --node $TX_NODE

# 4. Check wallet creation
txd keys add test-key --keyring-backend test

# 5. Check balance query
txd query bank balances $(txd keys show test-key -a --keyring-backend test) --node $TX_NODE
Troubleshooting
404 Error When Downloading
bash
# Check available versions
curl -s https://api.github.com/repos/tokenize-x/tx-chain/releases | jq '.[].tag_name'

# Set correct version
export TX_VERSION="v6.1.0"
Permission Denied
bash
# Fix permissions
chmod +x $TX_HOME/bin/txd

# Or use sudo for system-wide install
sudo cp $TX_HOME/bin/txd /usr/local/bin/
Command Not Found
bash
# Check if binary exists
ls -la $TX_HOME/bin/txd

# Verify PATH
echo $PATH

# Add to PATH permanently
echo 'export PATH="$PATH:$HOME/.txd/bin"' >> ~/.bashrc
source ~/.bashrc
macOS Architecture Issues
bash
# Check architecture
uname -m

# For Apple Silicon (M1/M2/M3)
export TX_BINARY_NAME="txd-darwin-arm64"

# For Intel Mac
export TX_BINARY_NAME="txd-darwin-amd64"
Next Steps
Set up CLI Network Variables

Transfer funds with CLI

Gas Price Guide

Special Addresses

Resources
txd Releases

Node Setup Guide

Troubleshooting

