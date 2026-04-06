Install txd - Complete Guide
This document provides instructions for installing the txd binary using three different methods.

Choose Your Installation Method
Method	Linux Support	Cosmovisor	Use Case
Install with Cosmovisor	✅ Only	✅ Yes	Production nodes (recommended)
Install Prebuilt Binary	✅ Only	❌ No	CLI interaction only
Build from Sources	✅ Yes	✅ Yes	Development, custom builds
Method 1: Install txd with Cosmovisor (Recommended for Node Operators)
Note: This option supports Linux OS only.

Why Cosmovisor? It automatically upgrades txd during chain upgrades, ensuring your node stays online.

Prerequisites
Verify network variables are set correctly:

bash
# Example for testnet
export TX_CHAIN_ID="txchain-testnet-1"
export TX_HOME="$HOME/.txd"
export TX_VERSION="v1.0.0"
export TX_BINARY_NAME="txd-linux-amd64"
export TX_COSMOVISOR_VERSION="v1.5.0"
export COSMOVISOR_TAR_NAME="cosmovisor-v1.5.0-linux-amd64.tar.gz"
Step 1: Create Folder Structure
bash
# Create necessary directories
mkdir -p $TX_HOME/bin
mkdir -p $TX_HOME/cosmovisor/genesis/bin
mkdir -p $TX_HOME/cosmovisor/upgrades
mkdir -p $TX_HOME/data

echo "✅ Directory structure created at $TX_HOME"
Step 2: Download txd Binary
For Mainnet and Testnet:

bash
# Download binary
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME

# If you get a 404 error, verify the URL:
echo "Checking URL: https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME"

# Make executable
chmod +x ./$TX_BINARY_NAME
For Devnet:

bash
curl -LOf https://storage.googleapis.com/dev-txd-binaries/txd-linux-amd64
chmod +x ./txd-linux-amd64
export TX_BINARY_NAME="txd-linux-amd64"
Step 3: Place Binary in Correct Location
bash
# Determine if this is a genesis or upgrade binary
if [ "$UPGRADE_NAME" == "genesis" ]; then
    export DESTINATION=$TX_HOME/cosmovisor/genesis/bin
else
    mkdir -p $TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin
    export DESTINATION=$TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME/bin
    # Create symlink for cosmovisor to use the current binary
    ln -s $TX_HOME/cosmovisor/upgrades/$UPGRADE_NAME $TX_HOME/cosmovisor/current
fi

# Move binary to destination
mv $TX_BINARY_NAME $DESTINATION/txd

echo "✅ Binary placed at: $DESTINATION/txd"
Step 4: Download and Install Cosmovisor
bash
# Download cosmovisor
curl -LO https://github.com/cosmos/cosmos-sdk/releases/download/cosmovisor%2F$TX_COSMOVISOR_VERSION/$COSMOVISOR_TAR_NAME

# Extract
mkdir cosmovisor-binaries
tar -xvf "$COSMOVISOR_TAR_NAME" -C cosmovisor-binaries

# Move to bin directory
mv "cosmovisor-binaries/cosmovisor" $TX_HOME/bin/cosmovisor

# Clean up
rm "$COSMOVISOR_TAR_NAME"
rm -r cosmovisor-binaries

echo "✅ Cosmovisor installed"
Step 5: Set Environment Variables
bash
# Add to PATH
export PATH=$PATH:$TX_HOME/bin
export PATH=$PATH:$DESTINATION

# Set cosmovisor environment variables
export DAEMON_HOME="$TX_HOME"
export DAEMON_NAME="txd"

# Make variables permanent (add to ~/.bashrc)
cat >> ~/.bashrc << EOF

# TX Blockchain Environment
export TX_HOME="\$HOME/.txd"
export PATH="\$PATH:\$TX_HOME/bin"
export DAEMON_HOME="\$TX_HOME"
export DAEMON_NAME="txd"
EOF

# Reload bashrc
source ~/.bashrc
Step 6: Verify Installation
bash
# Check txd version
txd version

# Check cosmovisor version
cosmovisor version

# Expected output example:
# txd: v1.0.0
# cosmovisor: v1.5.0
✅ Success! You have txd and cosmovisor installed. Return to the previous README to continue node setup.

Method 2: Install Prebuilt txd (For CLI Only)
Note: Linux OS only. Use this method if you only need CLI interaction without running a node.

Step 1: Create Directory Structure
bash
export TX_HOME="$HOME/.txd"
mkdir -p $TX_HOME/bin
Step 2: Download txd Binary
For Mainnet and Testnet:

bash
curl -LO https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME

# If 404 error, verify URL:
echo https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME
For Devnet:

bash
curl -LOf https://storage.googleapis.com/dev-txd-binaries/txd-linux-amd64
export TX_BINARY_NAME="txd-linux-amd64"
Step 3: Install Binary
bash
# Make executable
chmod +x ./$TX_BINARY_NAME

# Move to bin directory
mv $TX_BINARY_NAME $TX_HOME/bin/txd

# Add to PATH
export PATH=$PATH:$TX_HOME/bin

# Make permanent
echo 'export PATH="$PATH:$HOME/.txd/bin"' >> ~/.bashrc
source ~/.bashrc
Step 4: Verify Installation
bash
txd version
✅ Success! You have txd installed for CLI use.

Method 3: Build from Sources
Building from source gives you the most flexibility and is useful for development or custom builds.

Prerequisites
bash
# Install Go 1.21+
wget https://golang.org/dl/go1.21.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc

# Verify Go installation
go version
Step 1: Clone Repository
bash
git clone https://github.com/tokenize-x/tx-chain.git
cd tx-chain
Step 2: Checkout Desired Version
bash
# List available tags
git tag -l

# Checkout latest stable version
git checkout $(git describe --tags $(git rev-list --tags --max-count=1))

# Or checkout specific version
# git checkout v1.0.0
Step 3: Build Binary
bash
# Build
make build

# The binary will be at ./build/txd
ls -la ./build/txd
Step 4: Install to System
bash
# Install to /usr/local/bin
sudo make install

# Or manually copy
# cp ./build/txd /usr/local/bin/

# Verify
txd version
Step 5: Set Up Cosmovisor (Optional)
bash
# Install cosmovisor
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@latest

# Set up directory structure
export TX_HOME="$HOME/.txd"
mkdir -p $TX_HOME/cosmovisor/genesis/bin
cp $(which txd) $TX_HOME/cosmovisor/genesis/bin/

# Set environment variables
export DAEMON_HOME=$TX_HOME
export DAEMON_NAME=txd
✅ Success! You have built txd from source.

Common Configuration
Environment Variables Reference
Variable	Description	Example
TX_HOME	txd home directory	$HOME/.txd
DAEMON_HOME	Cosmovisor home	$HOME/.txd
DAEMON_NAME	Binary name	txd
TX_CHAIN_ID	Network chain ID	txchain-testnet-1
PATH Configuration
Add to ~/.bashrc or ~/.profile:

bash
# TX Blockchain paths
export TX_HOME="$HOME/.txd"
export PATH="$PATH:$TX_HOME/bin"

# Cosmovisor (if installed)
export DAEMON_HOME="$TX_HOME"
export DAEMON_NAME="txd"
export PATH="$PATH:$TX_HOME/cosmovisor/genesis/bin"
Troubleshooting
404 Error When Downloading
bash
# Verify the URL is correct
echo "https://github.com/tokenize-x/tx-chain/releases/download/$TX_VERSION/$TX_BINARY_NAME"

# Check available releases
curl -s https://api.github.com/repos/tokenize-x/tx-chain/releases | jq '.[].tag_name'
Permission Denied
bash
# Make binary executable
chmod +x ./txd-linux-amd64

# Or use sudo for system-wide install
sudo cp txd-linux-amd64 /usr/local/bin/txd
Command Not Found
bash
# Check if binary exists
ls -la $TX_HOME/bin/txd

# Verify PATH
echo $PATH

# Add to PATH temporarily
export PATH=$PATH:$TX_HOME/bin
Cosmovisor Not Found
bash
# Reinstall cosmovisor
go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@latest

# Verify installation path
which cosmovisor
Verification Checklist
After installation, run these checks:

bash
# 1. Check txd version
txd version

# 2. Check txd help
txd --help

# 3. Check cosmovisor (if installed)
cosmovisor version

# 4. Check directory structure
ls -la $TX_HOME/

# 5. Check PATH
which txd
Next Steps
After successful installation:

Configure Network Variables

Set Up Full Node

Run a Validator Node

Configure Sentry Nodes

Resources
Cosmovisor Documentation

TX Blockchain Releases

Build from Source Guide
