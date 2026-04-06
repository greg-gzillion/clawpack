# CertiK Security Audit Guide for TX Blockchain

## Overview

CertiK provides comprehensive security auditing and monitoring for blockchain projects. This guide explains how to interpret CertiK audit reports and security scores for TX blockchain and its ecosystem projects.

## Understanding the CertiK Dashboard

### Key Components
┌─────────────────────────────────────────────────────────────────────────────┐
│ CertiK Security Dashboard │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Code Security│ │ Fundamental │ │ Operational │ │ Community │ │
│ │ 5% │ │ Health │ │ Resilience │ │ Trust │ │
│ │ │ │ 5% │ │ 5% │ │ 35% │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │
│ ┌──────────────┐ ┌──────────────┐ │
│ │ Governance │ │ Market │ │
│ │ Strength │ │ Stability │ │
│ │ 10% │ │ 10% │ │
│ └──────────────┘ └──────────────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

## Code Security Analysis

### Audit Findings Severity Levels

| Severity | Description | Example Issues | Action Required |
|----------|-------------|----------------|-----------------|
| **Critical** | Direct threat to funds or consensus | Logical issues, reentrancy, access control | Must fix immediately |
| **Major** | Significant risk under specific conditions | Integer overflow, front-running | Fix asap |
| **Medium** | Moderate risk, limited impact | Gas inefficiencies, event emissions | Fix in next update |
| **Minor** | Low risk, best practice violations | Code style, naming conventions | Consider fixing |
| **Informational** | Suggestions for improvement | Documentation, optimizations | Optional |

### Audit Findings Distribution Example
Total Findings: 23
├── Critical: 1 (Resolved)
├── Major: 1 (Resolved)
├── Medium: 5 (Resolved)
├── Minor: 6 (Resolved)
└── Informational: 10 (5 Acknowledged, 5 Resolved)

text

### Audit Methods

| Method | Description | Purpose |
|--------|-------------|---------|
| **Manual Review** | Expert auditors manually review code | Catch logic flaws, business logic errors |
| **Static Analysis** | Automated tools scan code | Find common vulnerabilities, code smells |
| **Testnet Deployment** | Deploy and test on testnet | Verify functionality in real conditions |

## Audit Timeline

### Standard Audit Process
Day 0: Request Submitted
│
▼
Day 1-7: Initial Review
│
▼
Day 8-14: First Findings Report
│
▼
Day 15-21: Team Fixes Issues
│
▼
Day 22-28: Re-audit
│
▼
Day 29-35: Final Report
│
▼
Day 36-45: Public Disclosure

text

### Example Timeline
Requested: February 24, 2025
Revised: April 17, 2025
Duration: ~52 days

text

## Security Score Components

### 1. Code Security (Weight: 25%)

Evaluates:
- Audit history and quality
- Number and severity of findings
- Fix completion rate
- Code maturity

**Scoring:**
- 90-100%: Multiple clean audits
- 70-89%: Minor issues found and fixed
- 50-69%: Medium severity issues
- <50%: Critical issues or no audit

### 2. Fundamental Health (Weight: 20%)

Evaluates:
- Team verification status
- KYC completion
- Project age and maturity
- Documentation quality

### 3. Operational Resilience (Weight: 15%)

Evaluates:
- Bug bounty program existence and size
- Network security posture
- Application security
- DNS health

### 4. Community Trust (Weight: 15%)

Evaluates:
- Social media presence and engagement
- Community size and activity
- Developer community
- User ratings

### 5. Governance Strength (Weight: 15%)

Evaluates:
- On-chain governance setup
- Voting participation
- Proposal history
- Decentralization level

### 6. Market Stability (Weight: 10%)

Evaluates:
- Token price stability
- Liquidity depth
- Exchange listings
- Trading volume patterns

## Bug Bounty Program

### Program Structure

| Severity | Maximum Reward |
|----------|----------------|
| Critical | Up to $25,000 |
| Major | Up to $3,000 |
| Medium | Up to $1,000 |
| Low | Up to $500 |

### Assets in Scope

Typical assets covered:
1. Core blockchain node (`txd`)
2. Smart contracts (WASM)
3. IBC modules
4. Bridge contracts
5. DEX contracts
6. API endpoints

### How to Participate

```bash
# 1. Review scope and rules
# 2. Find vulnerability
# 3. Document with proof of concept
# 4. Submit via CertiK SkyShield
# 5. Wait for triage (typically 48 hours)
# 6. Coordinate disclosure
CertiK Formal Verification
What is Formal Verification?
Mathematical proof that smart contract code behaves as intended for all possible inputs.

Verification Properties
Property	Description
Safety	Nothing bad happens
Liveness	Something good eventually happens
Invariants	Certain conditions always hold
Bounds	Values stay within limits
When to Use Formal Verification
High-value DeFi protocols

Bridge contracts

Governance systems

Token distribution mechanisms

Audit Impact on Token Price
Historical Pattern
text
Audit Announcement → Price Increment (Typical: +14%)
     │
     ├── Pre-audit: Speculation (volatile)
     │
     ├── Audit in progress: Stability
     │
     ├── Findings disclosed: Potential dip
     │
     └── Audit completion: Price appreciation
Price Movement Example
text
Pre-Audit Price: $0.0173
Post-Audit Price: $0.1454
Gain: +740%

Timeline: April 3 - May 12, 2025
Centralization Assessment
Risk Categories
Category	What It Means	Risk Level
Distribution	Token distribution across wallets	High if concentrated
Upgrade	Ability to upgrade contracts	Medium if not decentralized
Privilege	Special admin functions	Medium if not timelocked
Other	Other centralization vectors	Varies
Healthy Signs
✅ No single wallet holds >10% of supply

✅ Multi-sig with 5+ signers

✅ Timelock on upgrades (min 48 hours)

✅ No admin keys with unlimited power

Network Security Assessment
Categories Checked
Network Security (9 checks)
FTP service anonymous login

VNC service accessibility

RDP service accessibility

LDAP server accessibility

PPTP service accessibility

rsync service accessibility

SSH weak cipher support

SSH weak MAC support

CVE on related service

Application Security (11 checks)
Missing CSP headers

Missing X-Frame-Options

Missing HSTS

Missing X-Content-Type-Options

HTTP access allowed

Self-signed certificates

Wrong host certificate

Expired certificate

Weak SSL/TLS ciphers

SSL protocol support

TLS weak version

DNS Health (10 checks)
SPF record missing

DMARC record missing

DKIM record missing

Ineffective SPF record

SPF softfail without DMARC

Exposed name server versions

Recursive queries allowed

CNAME in NS records

Private MX record IPs

Invalid MX record characters

GitHub Monitoring
Metrics Tracked
Metric	Healthy Range
Account Age	>2 years
Followers	>100
Stars	>50
Commit Frequency	Daily/Weekly
Issue Response	<24 hours
PR Merge Time	<7 days
Activity Heatmap Interpretation
Dark colors = High activity (good)

Light colors = Low activity (warning)

Gaps = Development pauses (investigate)

Community Trust Metrics
Twitter Monitoring
Metric	Healthy	Warning
Followers	50,000+	<10,000
Growth Rate	>1% daily	Declining
Engagement	>2%	<0.5%
Tweet Frequency	5-10 daily	<1 daily
Telegram Monitoring
Metric	Healthy	Warning
Total Users	20,000+	<5,000
Daily Active	2,000+	<500
Daily Messages	1,000+	<200
Sentiment	Positive	Negative
How to Improve Your Security Score
Short-term Actions (1-2 weeks)
Fix audit findings - Prioritize critical and major issues

Implement bug bounty - Even a small program helps

Update documentation - Clear security policies

Enable HSTS and CSP - Web security headers

Medium-term Actions (1-3 months)
Complete KYC - Team verification

Run second audit - Different firm for perspective

Launch formal verification - For critical contracts

Improve social presence - Regular updates

Long-term Actions (3-12 months)
Decentralize governance - On-chain voting

Multi-sig all admin functions - No single signer

Timelock all upgrades - 48-hour minimum

Regular penetration testing - Quarterly

Reading Audit Reports
PDF Report Sections
Executive Summary - High-level findings

Scope - What was audited

Methodology - How audit was performed

Findings - Detailed issues

Recommendations - Fix suggestions

Conclusion - Overall assessment

Finding Format
markdown
## Finding #001: [Title]

**Severity:** Critical
**Status:** Resolved
**Type:** Logical Issue

**Description:**
[Detailed explanation]

**Location:**
`contracts/token.go:156`

**Impact:**
[What could go wrong]

**Recommendation:**
[How to fix]

**Resolution:**
[How it was fixed]
CertiK vs Other Auditors
Auditor	Strengths	Weaknesses
CertiK	Formal verification, continuous monitoring	Expensive
Trail of Bits	Deep manual review, high quality	Very expensive
ConsenSys Diligence	Good for DeFi	Long lead times
SlowMist	Good for Asian projects	Less formal verification
Quantstamp	Fast turnaround	Less comprehensive
Best Practices for Audit Preparation
Before Submitting for Audit
bash
# 1. Run static analyzers
txd lint
cargo audit
solc --strict-protection

# 2. Run tests with coverage
go test -cover ./...
cargo test -- --nocapture

# 3. Fuzz testing
go test -fuzz=. -fuzztime=30s

# 4. Document everything
# - Code comments
# - Architecture diagrams
# - Threat model
Documentation to Prepare
Architecture diagrams

Threat model

Test suite with >90% coverage

Deployment scripts

Upgrade procedures

Emergency response plan

Previous audit reports (if any)

Cost Estimates
Audit Pricing
Project Size	Complexity	Estimated Cost
Small (<5k LOC)	Low	$15,000 - $30,000
Medium (5-20k LOC)	Medium	$30,000 - $60,000
Large (20-50k LOC)	High	$60,000 - $120,000
Enterprise (>50k LOC)	Very High	$120,000 - $250,000+
Bug Bounty Costs
Program Type	Annual Cost
Basic (self-hosted)	$10,000 - $25,000
CertiK SkyShield	$25,000 - $100,000
Immunefi	$50,000 - $500,000+
Security Checklist for TX Projects
Pre-Launch Checklist
Smart contract audit (2 firms recommended)

Formal verification for critical contracts

Bug bounty program launched

Multi-sig for admin functions

Timelock for upgrades

Emergency pause mechanism

Incident response plan

Insurance coverage (if available)

Post-Launch Checklist
Continuous monitoring (CertiK Skynet)

Regular penetration testing (quarterly)

Community bug bounty ongoing

Regular audit re-reviews

Transparent incident disclosure

Security updates communicated

Resources
Security Tools
Tool	Purpose
Slither	Solidity static analysis
Mythril	EVM bytecode analysis
Echidna	Fuzzing for Ethereum
Foundry	Testing framework
GoSec	Go security linter
Learning Resources
CertiK Security Insights

Smart Contract Security Guidelines

Ethereum Smart Contract Best Practices

Note: Security scores should be used as one of many factors in evaluating a project. No audit can guarantee 100% security.

text

**Save the file:**
- `Ctrl+O`, `Enter`, `Ctrl+X`

Now let's create a guide specific to TX blockchain security:

```bash
nano ~/dev/TXdocumentation/security/tx-security-practices.md
markdown
# TX Blockchain Security Practices

## Overview

This document outlines security best practices for developers, validators, and users on the TX blockchain.

## For Smart Contract Developers

### Secure Development Lifecycle
┌─────────────────────────────────────────────────────────────────────────────┐
│ TX Smart Contract Security Lifecycle │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ Requirements Design Implementation Testing Audit Launch │
│ │ │ │ │ │ │ │
│ ▼ ▼ ▼ ▼ ▼ ▼ │
│ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ │
│ │Threat │ │Secure │ │Safe │ │Unit │ │CertiK │ │Bug │ │
│ │Model │───▶│Pattern│───▶│Libraries│────▶│Tests │─▶│Audit │─▶│Bounty │ │
│ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ │
│ │
└─────────────────────────────────────────────────────────────────────────────┘

text

### Common Vulnerabilities in Cosmos/TX

| Vulnerability | Description | Prevention |
|---------------|-------------|------------|
| **Reentrancy** | Repeated calls before state update | Use mutex locks, checks-effects-interactions |
| **Integer Overflow** | Numbers exceed max value | Use checked math (cosmos SDK has built-in) |
| **Access Control** | Unauthorized function calls | Use `onlyOwner` modifiers, capability-based |
| **Infinite Loops** | Gas exhaustion | Limit iterations, use pagination |
| **Message Validation** | Invalid inputs | Validate all external inputs |
| **Timestamp Dependence** | Miner manipulation | Use block height instead of timestamp |
| **Randomness** | Predictable values | Use commit-reveal or oracle |

### Secure Code Patterns for TX

#### 1. Proper Message Validation

```go
// Good: Validate all inputs
func (k Keeper) Transfer(ctx sdk.Context, msg *types.MsgTransfer) error {
    // Validate addresses
    if err := sdk.VerifyAddressFormat(msg.Sender); err != nil {
        return err
    }
    
    // Validate amount
    if msg.Amount.IsZero() || msg.Amount.IsNegative() {
        return sdkerrors.Wrap(sdkerrors.ErrInvalidCoins, "amount must be positive")
    }
    
    // Validate asset exists
    if !k.HasAsset(ctx, msg.AssetId) {
        return sdkerrors.Wrap(types.ErrAssetNotFound, msg.AssetId)
    }
    
    // Continue with transfer...
}
2. Safe Balance Operations
go
// Good: Check balance before transfer
func (k Keeper) SendTokens(ctx sdk.Context, from, to sdk.AccAddress, amount sdk.Coin) error {
    // Get balance
    balance := k.bankKeeper.GetBalance(ctx, from, amount.Denom)
    
    // Check sufficient balance
    if balance.IsLT(amount) {
        return sdkerrors.Wrapf(sdkerrors.ErrInsufficientFunds, 
            "insufficient balance: %s < %s", balance, amount)
    }
    
    // Send coins (bank module handles atomic operation)
    return k.bankKeeper.SendCoins(ctx, from, to, sdk.NewCoins(amount))
}
3. Capability-Based Security
go
// Good: Use capabilities for authorization
func (k Keeper) CreateNewAccount(ctx sdk.Context, authority string) error {
    // Check capability
    if !k.HasCapability(ctx, authority, "create_account") {
        return sdkerrors.Wrap(types.ErrUnauthorized, authority)
    }
    
    // Create account...
    return nil
}
Testing Requirements
bash
# Minimum test coverage requirements
Unit Tests: 90% coverage
Integration Tests: 80% coverage
E2E Tests: Critical paths only

# Run tests with coverage
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Fuzz testing for numeric operations
go test -fuzz=FuzzTransfer -fuzztime=30s
For Validators
Validator Security Checklist
Infrastructure Security
Dedicated hardware - No shared hosting

Firewall configuration - Only necessary ports open

SSH key only - No password authentication

Fail2ban installed - Brute force protection

Regular updates - Security patches within 7 days

Monitoring - Prometheus + Grafana setup

Backups - Daily backups of consensus key (encrypted)

Key Management
bash
# Generate new consensus key
txd tendermint gen-validator

# Backup key (encrypted)
gpg --symmetric --cipher-algo AES256 priv_validator_key.json
# Store backup offline

# Hardware security module (HSM) for production
# Use YubiHSM or similar
Sentry Node Architecture
text
                    ┌─────────────────┐
                    │   Firewall/      │
                    │   Load Balancer  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Sentry 1 │  │ Sentry 2 │  │ Sentry 3 │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             │             │             │
             └──────────────┼──────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Validator   │
                    │  (Private)    │
                    └───────────────┘
Monitoring Alerts
yaml
# Prometheus alert rules
groups:
- name: tx-validator
  rules:
  - alert: ValidatorDown
    expr: up{job="validator"} == 0
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Validator is down"
      
  - alert: HighMissedBlocks
    expr: missed_blocks_rate > 0.10
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "Missed blocks >10%"
      
  - alert: ConsensusFailure
    expr: consensus_height{job="validator"} == 0
    for: 1m
    labels:
      severity: critical
For Users
Wallet Security
Hot Wallet vs Cold Wallet
Feature	Hot Wallet	Cold Wallet
Convenience	High	Low
Security	Low	High
Best for	Trading, small amounts	Long-term holding, large amounts
Examples	Leap, Cosmostation	Ledger, Trezor
Seed Phrase Security
text
DO:
✓ Write on paper (no digital photos)
✓ Store in multiple secure locations
✓ Use metal backup for fire protection
✓ Split into multiple parts (Shamir)
✓ Test recovery before sending funds

DON'T:
✗ Store in password manager
✗ Take screenshots
✗ Share with anyone
✗ Enter on any website
✗ Store in cloud
Transaction Verification
bash
# Always verify transaction details before signing
txd tx bank send <to> <amount> \
  --generate-only \
  --chain-id tx-mainnet-1 \
  --output json > tx.json

# Review the JSON
cat tx.json | jq '.body.messages[0]'

# Sign only after verification
txd tx sign tx.json --from <key>
Incident Response
Security Incident Severity Levels
Level	Description	Response Time
P0 (Critical)	Funds at risk, network halt	Immediate (15 min)
P1 (High)	Potential funds loss, contract exploit	1 hour
P2 (Medium)	Non-critical vulnerability	24 hours
P3 (Low)	Best practice violation	7 days
Incident Response Plan
bash
# 1. Detect incident
# - Monitoring alerts
# - User reports
# - Internal discovery

# 2. Assess severity (15 minutes)
# - Impact analysis
# - Affected systems
# - Potential losses

# 3. Contain (30 minutes)
# - Emergency pause (if available)
# - Block malicious addresses
# - Notify validators

# 4. Eradicate (2-4 hours)
# - Deploy emergency patch
# - Rotate compromised keys
# - Remove malicious code

# 5. Recover (24-48 hours)
# - Restore from backup
# - Replay transactions if needed
# - User compensation plan

# 6. Post-mortem (7 days)
# - Root cause analysis
# - Lessons learned
# - Security improvements
Emergency Contacts
Contact	Purpose	Method
TX Security Team	Security incidents	security@tx.org
Validators Emergency	Network issues	validators@tx.org
Bug Bounty	Vulnerability reports	bounty@tx.org
Regular Security Tasks
Daily
bash
# Check validator status
txd status

# Review logs for errors
journalctl -u txd -f --lines=50

# Check disk space
df -h

# Monitor network connections
netstat -tuna | grep 26656
Weekly
bash
# Update system
apt update && apt upgrade -y

# Review failed login attempts
grep "Failed password" /var/log/auth.log

# Check for software updates
txd version --long

# Verify peers
txd query tendermint-validator-set
Monthly
bash
# Security audit of configuration
# Review access logs
# Test backup restoration
# Rotate API keys (if any)
# Review and update documentation
Quarterly
Full security assessment

Penetration testing

Review and update incident response plan

Security training for team

Audit of third-party dependencies

Security Tools for TX
Recommended Tool Stack
Tool	Purpose	Installation
Fail2ban	Brute force protection	apt install fail2ban
Crowdsec	Advanced IPS	curl -s https://crowdsec.net | bash
Lynis	Security auditing	apt install lynis
ClamAV	Malware scanning	apt install clamav
RKHunter	Rootkit detection	apt install rkhunter
Auditd	System call auditing	apt install auditd
Monitoring Stack
yaml
# docker-compose for monitoring
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=secure_password
      
  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
Security Resources
Documentation
TX Security White Paper

CertiK Audit Reports

Bug Bounty Program

Contact
Security Team: security@tx.org

Emergency (PGP): Available upon request

Discord: #security channel

Remember: Security is a process, not a product. Regular reviews and updates are essential.

text

**Save the file:**
- `Ctrl+O`, `Enter`, `Ctrl+X`

Now let's create a quick reference card for security:

```bash
nano ~/dev/TXdocumentation/security/security-quick-reference.md
markdown
# TX Blockchain Security Quick Reference

## Audit Severity Guide
CRITICAL ─────────► MUST FIX IMMEDIATELY
│
├─ Fund loss possible
├─ Consensus failure
└─ Unauthorized access

MAJOR ────────────► FIX ASAP (1-2 weeks)
│
├─ Limited fund risk
├─ Denial of service
└─ Privilege escalation

MEDIUM ───────────► FIX IN NEXT UPDATE
│
├─ Best practice violation
├─ Information disclosure
└─ Inefficient code

MINOR ────────────► CONSIDER FIXING
│
├─ Code style issues
├─ Missing events
└─ Naming conventions

INFORMATIONAL ────► OPTIONAL IMPROVEMENTS
│
├─ Documentation gaps
├─ Optimization suggestions
└─ Future considerations

text

## Security Score Interpretation

| Score | Meaning | Risk Level |
|-------|---------|------------|
| 90-100 | Excellent - Multiple clean audits | Low |
| 70-89 | Good - Minor issues fixed | Low-Medium |
| 50-69 | Fair - Medium issues present | Medium |
| 30-49 | Poor - Major issues present | High |
| 0-29 | Critical - Severe vulnerabilities | Critical |

## Quick Security Commands

### Validator Security

```bash
# Check validator status
txd query staking validator $(txd keys show <owner> --bech=val --address)

# Check slashing info
txd query slashing signing-info $(txd tendermint show-validator)

# Check missed blocks
txd query slashing signing-info $(txd tendermint show-validator) | grep missed_blocks_counter

# Unjail if needed
txd tx slashing unjail --from <owner>
Smart Contract Security
bash
# Run static analysis (CosmWasm)
cargo check
cargo clippy -- -D warnings

# Run tests with coverage
cargo tarpaulin --ignore-tests

# Check for known vulnerabilities
cargo audit
Node Security
bash
# Check open ports
ss -tuln

# Check firewall status
ufw status verbose

# Check failed login attempts
lastb | head -20

# Check disk encryption
lsblk
Security Checklist
Pre-Launch (14 items)
Smart contract audit completed

Critical findings resolved

Major findings resolved

Formal verification for core contracts

Bug bounty program launched

Multi-sig for admin (min 3/5)

Timelock for upgrades (min 48h)

Emergency pause mechanism

Incident response plan

Insurance coverage (if available)

Team KYC completed

Documentation complete

Test coverage >90%

Penetration testing completed

Monthly (6 items)
Review audit findings

Update dependencies

Check for new vulnerabilities

Review access logs

Test backup restoration

Update security documentation

Quarterly (5 items)
Full security assessment

Penetration testing

Review incident response plan

Security training for team

Audit third-party dependencies

Common Vulnerability Patterns
In TX/Cosmos SDK
go
// ❌ BAD: No validation
func (k Keeper) Transfer(ctx sdk.Context, msg *MsgTransfer) error {
    return k.bankKeeper.SendCoins(ctx, msg.Sender, msg.Receiver, msg.Amount)
}

// ✅ GOOD: Validation
func (k Keeper) Transfer(ctx sdk.Context, msg *MsgTransfer) error {
    if msg.Amount.IsZero() {
        return sdkerrors.Wrap(sdkerrors.ErrInvalidCoins, "amount cannot be zero")
    }
    if k.bankKeeper.GetBalance(ctx, msg.Sender, msg.Amount.Denom).IsLT(msg.Amount) {
        return sdkerrors.Wrap(sdkerrors.ErrInsufficientFunds, "insufficient balance")
    }
    return k.bankKeeper.SendCoins(ctx, msg.Sender, msg.Receiver, msg.Amount)
}
Access Control
go
// ❌ BAD: No access check
func (k Keeper) SetAdmin(ctx sdk.Context, newAdmin string) error {
    k.admin = newAdmin
    return nil
}

// ✅ GOOD: Access control
func (k Keeper) SetAdmin(ctx sdk.Context, caller string, newAdmin string) error {
    if caller != k.admin {
        return sdkerrors.Wrap(types.ErrUnauthorized, "only admin can set admin")
    }
    k.admin = newAdmin
    return nil
}
Emergency Contacts
Issue	Contact	Response Time
Smart Contract Exploit	security@tx.org	15 min
Validator Emergency	validators@tx.org	1 hour
Bug Bounty Submission	bounty@tx.org	24 hours
Security Question	community@tx.org	48 hours
Useful Links
CertiK Dashboard

Bug Bounty Program

Security Advisories

Audit Reports

