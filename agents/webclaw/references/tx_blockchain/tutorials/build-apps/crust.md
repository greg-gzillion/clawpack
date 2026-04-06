# Crust - TX Blockchain Development Environment

Crust helps you build and run all applications needed for TX Blockchain development and testing.

## Overview

Crust provides:
- Local development environment with multiple node configurations
- Integration testing framework
- Faucet and explorer integration
- Monitoring stack (Prometheus + Grafana)
- Multi-validator setups for testing
- IBC testing capabilities

## Prerequisites

```bash
# Install required dependencies
go version  # 1.18 or newer
gcc --version
docker --version
docker buildx version  # For Docker >23

# Verify installations
echo "Go: $(go version)"
echo "GCC: $(gcc --version | head -1)"
echo "Docker: $(docker --version)"
Installation
Clone Repositories
bash
# Set your workspace path
export TX_PATH=~/dev/tx-workspace
mkdir -p $TX_PATH
cd $TX_PATH

# Clone crust
git clone https://github.com/tokenize-x/tx-crust

# Clone core chain
git clone https://github.com/tokenize-x/tx-chain

# Optional: Clone faucet and explorer
git clone https://github.com/tokenize-x/tx-faucet
git clone https://github.com/tokenize-x/tx-callisto
Add to PATH (Optional)
bash
# Add bin directories to PATH
export PATH="$TX_PATH/tx-crust/bin:$TX_PATH/tx-chain/bin:$PATH"

# Add to ~/.bashrc for persistence
echo 'export PATH="$HOME/dev/tx-workspace/tx-crust/bin:$HOME/dev/tx-workspace/tx-chain/bin:$PATH"' >> ~/.bashrc
Build Components
Build Core Images
bash
# Build txd binaries and docker images
$TX_PATH/tx-chain/bin/txd-builder build images

# After build completes, create symlinks
ln -s $TX_PATH/tx-chain/bin/.cache/txd $TX_PATH/tx-crust/bin/.cache/
ln -s $TX_PATH/tx-chain/bin/txd $TX_PATH/tx-crust/bin/txd
Build Optional Components
bash
# Build faucet images
$TX_PATH/tx-faucet/bin/faucet-builder build images

# Build explorer images
$TX_PATH/tx-callisto/bin/callisto-builder build images
Note: Run respective builder commands after modifying any project.

ZNet - Local Development Environment
ZNet is the tool that spins up a development environment running the same components used in production.

Start ZNet
Method 1: Direct Commands
bash
# Start with default profile (1 validator)
crust znet start

# Start with multiple profiles
crust znet start --profiles=3txd,faucet,explorer,monitoring

# Start with specific txd version
crust znet start --txd-version=v1.0.0 --profiles=3txd,faucet
Method 2: Interactive Shell
bash
# Enter znet environment
crust znet

# Now you're in the environment
(znet) [znet] $ start --profiles=3txd,faucet

# Run commands without prefixing 'crust znet'
(znet) [znet] $ spec
(znet) [znet] $ logs txd-00-val
(znet) [znet] $ stop

# Exit environment
(znet) [znet] $ exit
ZNet Flags
Flag	Description	Default
--env	Environment name	"znet"
--profiles	Application profiles to run	"1txd"
--txd-version	Specific txd version to use	Latest
Available Profiles
Profile	Description
1txd	Single validator node
3txd	Three validator nodes
5txd	Five validator nodes
devnet	3 validators, 1 sentry, 1 seed, 2 full nodes
faucet	Testnet faucet
explorer	Block explorer
monitoring	Prometheus + Grafana stack
integration-tests-ibc	IBC integration test setup
integration-tests-modules	Modules integration test setup
Note: 1txd, 3txd, 5txd, and devnet are mutually exclusive.

Example: Full Development Environment
bash
# Start complete development environment
crust znet start --profiles=3txd,faucet,explorer,monitoring

# Access services:
# - Blockchain: RPC on port 26657
# - Faucet: http://localhost:8000
# - Explorer: http://localhost:3000
# - Grafana: http://localhost:3001 (admin/admin)
# - Prometheus: http://localhost:9092
ZNet Commands
Command	Description
start	Start all applications
stop	Stop all applications
remove	Stop and remove all resources
spec	Print environment specification
tests	Run integration tests
console	Start tmux session with logs
logs <app>	Tail logs from specific app
Interactive Examples
bash
# Enter environment
crust znet

# Start applications
(znet) [znet] $ start

# View specification
(znet) [znet] $ spec

# Tail logs
(znet) [znet] $ logs txd-00-val
(znet) [znet] $ logs faucet

# Stop applications
(znet) [znet] $ stop

# Start again
(znet) [znet] $ start

# Clean everything
(znet) [znet] $ remove
Manual Blockchain Interaction
Default Keys
Each txd instance comes with three standard keys:

alice

bob

charlie

Send Transactions
bash
# Start environment
crust znet start --profiles=1txd

# Enter znet shell
crust znet

# Generate a new wallet
(znet) [znet] $ txd-00-val keys add mywallet

# Get address
MY_ADDRESS=$(txd-00-val keys show mywallet -a)
echo "My address: $MY_ADDRESS"

# Check balance (initially 0)
(znet) [znet] $ txd-00-val query bank balances $MY_ADDRESS

# Send funds from bob (pre-funded)
(znet) [znet] $ txd-00-val tx bank send bob $MY_ADDRESS 10udevcore --from bob -y

# Check balance again
(znet) [znet] $ txd-00-val query bank balances $MY_ADDRESS

# Clean up
(znet) [znet] $ remove
Working with Multiple Validators
bash
# Start 3 validators
crust znet start --profiles=3txd

# Enter environment
crust znet

# Use different validator clients
(znet) [znet] $ txd-00-val status
(znet) [znet] $ txd-01-val status
(znet) [znet] $ txd-02-val status

# Check validator set
(znet) [znet] $ txd-00-val query staking validators

# Clean up
(znet) [znet] $ remove
Integration Testing
Run All Tests
bash
# Direct execution
crust znet test

# With specific txd version
crust znet test --txd-version=v1.0.0

# Test specific group
crust znet test --test-groups=coreum-upgrade
Interactive Testing
bash
# Enter environment
crust znet

# Start with integration test profile
(znet) [znet] $ start --profiles=integration-tests

# Run tests
(znet) [znet] $ tests

# Inspect if something went wrong
(znet) [znet] $ logs txd-00-val

# Clean up
(znet) [znet] $ remove
Test Groups
Test Group	Description
coreum-upgrade	Chain upgrade tests
coreum-modules	Module integration tests
ibc-transfer	IBC transfer tests
wasm	Smart contract tests
Monitoring Stack
Access Monitoring Tools
bash
# Start with monitoring profile
crust znet start --profiles=3txd,monitoring

# Access services:
echo "Grafana: http://localhost:3001 (admin/admin)"
echo "Prometheus: http://localhost:9092"
Grafana Dashboards
Default dashboards include:

Blockchain metrics (block height, tx volume)

Validator performance

Node health

Consensus statistics

Hard Reset
If you need to completely clean all ZNet data:

bash
# Stop and remove all containers
docker ps -a | grep znet | awk '{print $1}' | xargs docker stop 2>/dev/null
docker ps -a | grep znet | awk '{print $1}' | xargs docker rm 2>/dev/null

# Remove cache directory
rm -rf ~/.cache/crust/znet

# Or use znet remove command
crust znet remove
Complete Workflow Example
bash
#!/bin/bash
# Complete Crust development workflow

# 1. Setup
export TX_PATH=~/dev/tx-workspace
mkdir -p $TX_PATH
cd $TX_PATH

# 2. Clone repositories
git clone https://github.com/tokenize-x/tx-crust
git clone https://github.com/tokenize-x/tx-chain

# 3. Build
cd tx-chain
./bin/txd-builder build images
cd ..

# 4. Setup symlinks
ln -s $TX_PATH/tx-chain/bin/.cache/txd $TX_PATH/tx-crust/bin/.cache/
ln -s $TX_PATH/tx-chain/bin/txd $TX_PATH/tx-crust/bin/txd

# 5. Add to PATH
export PATH="$TX_PATH/tx-crust/bin:$TX_PATH/tx-chain/bin:$PATH"

# 6. Start development environment
crust znet start --profiles=3txd,faucet,explorer,monitoring

# 7. Enter interactive shell
crust znet

# Inside shell:
(znet) [znet] $ spec
(znet) [znet] $ logs txd-00-val

# Test transaction
(znet) [znet] $ txd-00-val keys add testwallet
(znet) [znet] $ txd-00-val tx bank send bob $(txd-00-val keys show testwallet -a) 100udevcore --from bob -y

# Run integration tests
(znet) [znet] $ tests

# Clean up when done
(znet) [znet] $ remove
Troubleshooting
Docker Buildx Issues
bash
# Install buildx separately
docker buildx install
docker buildx create --use

# Verify
docker buildx ls
Permission Issues
bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
Port Conflicts
bash
# Check if ports are in use
netstat -tulpn | grep -E '26657|8000|3000|3001|9092'

# Stop conflicting services or change ZNet configuration
Cache Issues
bash
# Clear cache and rebuild
rm -rf ~/.cache/crust
cd $TX_PATH/tx-chain
./bin/txd-builder build images --no-cache
Next Steps
Read TX Modules Specification

Check Web App Development

Explore Integration Testing Guide

Review Node Setup Guide
