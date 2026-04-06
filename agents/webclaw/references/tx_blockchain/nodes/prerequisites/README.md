Node Prerequisites - Common Setup
This document contains common information and system configuration required for any type of node (full, validator, or sentry).

Critical System Configuration
File Descriptor Limit (ulimit -n)
⚠️ CRITICAL: This setting is essential for the node to function properly. Without it, the node will crash as soon as it reaches the limit.

Check Current Limit
bash
ulimit -n
If the limit is less than 2048, you must increase it.

Recommended Setting: 65536

#### Increase the Limit

**Temporary (current session only):**
```bash
ulimit -n 65536
Permanent (system-wide):
bash
# Add to /etc/security/limits.conf
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "root soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "root hard nofile 65536" | sudo tee -a /etc/security/limits.conf
For systemd services:
bash
# In service file, add:
[Service]
LimitNOFILE=65536
Verify the change:
bash
# Log out and log back in, then check:
ulimit -n
# Should show 65536
Network Requirements
Public IP Address
Your node must have a public IP address to be discoverable by other nodes.

Check your IP:

bash
curl -s ifconfig.me
Configure external address in config:

bash
# Set in config.toml
external_address = "tcp://<your-public-ip>:26656"
Ports
Ensure these ports are open:

Port	Protocol	Purpose	Required
26656	TCP	P2P (peer-to-peer)	Yes
26657	TCP	RPC (optional)	Optional
1317	TCP	REST API	Optional
26660	TCP	Prometheus	Optional
Firewall Configuration
bash
# Allow P2P port
sudo ufw allow 26656/tcp

# If enabling RPC:
sudo ufw allow 26657/tcp

# Enable firewall
sudo ufw enable
Required Utilities
Install these essential utilities before proceeding:

crudini
Used for configuration file management.

bash
sudo apt update
sudo apt install -y crudini
Verify:

bash
crudini --version
curl
Used for API requests and network testing.

bash
sudo apt install -y curl
Verify:

bash
curl --version
jq
Used for JSON parsing and formatting.

bash
sudo apt install -y jq
Verify:

bash
jq --version
tar
Used for archive extraction.

bash
sudo apt install -y tar
Verify:

bash
tar --version
One-Line Installation
Install all required utilities at once:

bash
sudo apt update && sudo apt install -y curl jq tar crudini
System Configuration
Time Synchronization
Ensure your system time is synchronized:

bash
# Install chrony if not present
sudo apt install -y chrony

# Check status
timedelta
Swap Configuration
For nodes with limited RAM, configure swap:

bash
# Check if swap exists
sudo swapon --show

# Create swap file (8GB example)
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
Kernel Parameters
Optimize network performance:

bash
# Add to /etc/sysctl.conf
echo "net.core.rmem_max = 134217728" | sudo tee -a /etc/sysctl.conf
echo "net.core.wmem_max = 134217728" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_rmem = 4096 87380 134217728" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_wmem = 4096 65536 134217728" | sudo tee -a /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 5000" | sudo tee -a /etc/sysctl.conf

# Apply
sudo sysctl -p
Verification Checklist
Before proceeding with node setup, verify:
System Checks
bash
# Check file descriptor limit
ulimit -n
# Should be >= 2048 (preferably 65536)

# Check disk space
df -h

# Check memory
free -h

# Check CPU
nproc

# Check time sync
timedatectl status
Network Checks
bash
# Check public IP
curl -s ifconfig.me

# Check connectivity
ping -c 4 google.com

# Check ports
sudo netstat -tulpn | grep -E '26656|26657|1317'
Utility Checks
bash
# Verify all utilities installed
which crudini curl jq tar
# All should return paths
Troubleshooting
File Descriptor Limit Not Persisting
Check limits.conf syntax

Ensure no other limits override

For systemd services, add LimitNOFILE to service file

Network Not Reachable
Check firewall rules: sudo ufw status

Check cloud provider security groups

Verify external_address in config.toml

Utilities Not Found
Update package list: sudo apt update

Check if installed: dpkg -l | grep <package>

Try reinstalling: sudo apt install --reinstall <package>

Next Steps
After verifying prerequisites, choose your node type:

Run a Full Node

Run a Validator Node

Run a Sentry Node

Resources
System Requirements

Network Variables

Install txd

Troubleshooting Guide
