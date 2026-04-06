# System Requirements for TX Nodes

## ⚠️ Critical Warning

> **Use only SSD or NVMe hard drives, directly attached to the motherboard.**
> 
> **Recommended**: Use a dedicated bare-metal server for production validators.
> 
> If you use a Cloud Computing Instance, ensure that your SSD disk is **directly attached to the motherboard**. Otherwise, you may experience I/O delay and risk being jailed for not signing blocks.

## Mainnet Requirements

### Validator Node

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **CPU** | 8 cores | High-performance CPU recommended |
| **RAM** | 16 GB | Minimum, 32 GB recommended |
| **Storage** | 500 GB - 2 TB | NVMe SSD, directly attached |
| **Network** | 100+ MBPS | Low latency, stable connection |
| **OS** | Ubuntu 20.04/22.04 LTS | Production tested |

### Full Node

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **CPU** | 4 cores | |
| **RAM** | 32 GB | Higher RAM for archive node |
| **Storage** | 2 TB | NVMe SSD, directly attached |
| **Network** | 100+ MBPS | |
| **OS** | Ubuntu 20.04/22.04 LTS | |

### Default Node

| Component | Requirement | Notes |
|-----------|-------------|-------|
| **CPU** | 4 cores | |
| **RAM** | 32 GB | |
| **Storage** | 1 TB | NVMe SSD, directly attached |
| **Network** | 100+ MBPS | |
| **OS** | Ubuntu 20.04/22.04 LTS | |

## Testnet Requirements

| Node Type | Cores | RAM | Storage | Network |
|-----------|-------|-----|---------|---------|
| **Validator** | 2 | 16 GB | 500 GB | 100+ MBPS |
| **Full Node** | 2 | 16 GB | 500 GB | 100+ MBPS |
| **Default** | 2 | 16 GB | 500 GB | 100+ MBPS |

## Devnet Requirements

> **Note**: To ease maintenance efforts, we support only `amd64` architecture for devnet.
> 
> **Recommendation**: Use testnet for more stable operations.

| Node Type | Cores | RAM | Storage | Network |
|-----------|-------|-----|---------|---------|
| **Validator** | 2 | 16 GB | 100 GB | 100+ MBPS |
| **Full Node** | 2 | 16 GB | 100 GB | 100+ MBPS |
| **Default** | 2 | 16 GB | 100 GB | 100+ MBPS |

## Storage Growth Estimates

| Network | Initial Size | Monthly Growth | Year 1 Total |
|---------|--------------|----------------|--------------|
| **Mainnet** | ~20 GB | 10-20 GB | 150-250 GB |
| **Testnet** | ~10 GB | 5-10 GB | 70-130 GB |
| **Devnet** | ~5 GB | Variable | Resets frequently |

## Network Requirements

### Required Ports

| Port | Protocol | Purpose | Firewall |
|------|----------|---------|----------|
| 26656 | TCP | P2P (peer-to-peer) | Open to peers |
| 26657 | TCP | RPC (query, tx broadcast) | Internal/optional |
| 1317 | TCP | REST API | Internal/optional |
| 26660 | TCP | Prometheus metrics | Internal/optional |

### Network Configuration

- **Minimum bandwidth**: 100 MBPS
- **Latency**: < 100ms to major peers
- **Stability**: 99.9% uptime target
- **IP**: Static IP recommended for validators

## Hardware Recommendations by Use Case

### Production Validator (Mainnet)
Hardware: Bare-metal server
CPU: AMD EPYC or Intel Xeon, 8+ cores
RAM: 32 GB ECC
Storage: 1 TB NVMe (enterprise grade)
Network: 1 Gbps dedicated
Redundancy: Dual power supply, RAID 1

text

### Cloud Validator (Mainnet)
Provider: AWS, GCP, Azure (dedicated instances)
Instance: Compute-optimized (c5/c6i series)
Storage: Provisioned IOPS SSD (io1/io2) with 5000+ IOPS
Network: Enhanced networking enabled
Region: Choose low-latency regions

text

### Testnet Validator
Provider: Any cloud or bare-metal
CPU: 2-4 cores
RAM: 16 GB
Storage: 500 GB SSD
Network: Standard (100 MBPS)

text

## Storage Performance Requirements

### Minimum IOPS
- **Sequential read**: 10,000+ IOPS
- **Sequential write**: 5,000+ IOPS
- **Random read**: 5,000+ IOPS
- **Random write**: 2,000+ IOPS

### Disk Types - DO NOT USE

| Disk Type | Status | Reason |
|-----------|--------|--------|
| HDD (5400 RPM) | ❌ Not Recommended | Too slow, will cause missed blocks |
| HDD (7200 RPM) | ❌ Not Recommended | Will cause sync delays |
| Network-attached storage | ❌ Not Recommended | I/O latency too high |
| USB Drives | ❌ Not Supported | Not reliable |

### Disk Types - RECOMMENDED

| Disk Type | Status | Use Case |
|-----------|--------|----------|
| NVMe SSD | ✅ Recommended | Best performance for validators |
| SATA SSD | ✅ Acceptable | Suitable for full nodes |
| RAID 0 SSDs | ✅ Acceptable | For higher throughput |
| Provisioned IOPS | ✅ Acceptable | Cloud deployments |

## Operating System

### Supported OS

| OS | Version | Architecture | Support Level |
|----|---------|--------------|---------------|
| **Ubuntu** | 20.04 LTS | amd64 | ✅ Full support |
| **Ubuntu** | 22.04 LTS | amd64 | ✅ Full support |
| **Debian** | 11+ | amd64 | ✅ Supported |
| **CentOS** | 7+ | amd64 | ⚠️ Community |
| **macOS** | Any | arm64/amd64 | ⚠️ Development only |
| **Windows** | Any | - | ❌ Not supported |

### System Configuration

```bash
# Recommended system limits
echo "fs.file-max = 65536" >> /etc/sysctl.conf
echo "net.core.somaxconn = 1024" >> /etc/sysctl.conf
echo "net.ipv4.tcp_tw_reuse = 1" >> /etc/sysctl.conf
sysctl -p

# File descriptors
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf
Monitoring Requirements
Basic Monitoring
CPU usage

Memory usage

Disk usage

Network I/O

Block height progress

Alerting
Node downtime

High missed blocks (for validators)

Disk space < 20%

Memory pressure

Scaling Recommendations
Small Scale (Testnet)
Single validator

2 sentry nodes

Basic monitoring

Medium Scale (Mainnet Entry)
1 validator

3 sentry nodes (different regions)

Redundant network

24/7 monitoring

Large Scale (Top Validator)
1 primary validator

2 backup validators (standby)

5+ sentry nodes globally distributed

Dedicated security team

Hardware security modules (HSM)

Disaster recovery plan

Resources
Network Variables

Install txd

Validator Setup

Troubleshooting Guide
