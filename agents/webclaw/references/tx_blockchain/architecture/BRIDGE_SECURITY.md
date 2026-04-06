# Bridge Security Architecture

**Document Status:** Living Document  
**Last Updated:** February 15, 2026  
**Owner:** Greg (@greg-gzillion)  
**Review Cycle:** Monthly

## Executive Summary

PhoenixPME requires a secure bridge between Coreum (where auctions occur) and XRPL (where RLUSD payments are processed). This document outlines our current testnet implementation, known limitations, security measures, and roadmap to production-ready security.

**Current Status:** ⚠️ Testnet Only - Not Production Ready

---

## Table of Contents

1. [Current Implementation (Testnet)](#current-implementation-testnet)
2. [Security Measures](#security-measures)
3. [Known Limitations](#known-limitations)
4. [Threat Model](#threat-model)
5. [Production Roadmap](#production-roadmap)
6. [Emergency Procedures](#emergency-procedures)

---

## Current Implementation (Testnet)

### Architecture Overview

```
User → Coreum Smart Contract → Bridge Oracle → XRPL Ledger
                                      ↓
                              Verification Service
                                      ↓
                              Community Reserve Fund (Escrow)
```

### How It Works Today

1. **User initiates transaction** on PhoenixPME frontend
2. **Coreum contract** creates auction and calculates fees (1.1%)
3. **Oracle service** monitors XRPL for RLUSD payments
4. **Verification** confirms payment received on XRPL
5. **Funds released** to seller, fees to Community Reserve Fund

### Current Components

- **Oracle:** Single centralized service monitoring XRPL
- **Verification:** XRPL transaction hash confirmation
- **Key Management:** Single private key (testnet only)
- **Escrow:** Coreum smart contract holds funds

---

## Security Measures

### Current (Testnet)

#### 1. Transaction Verification
- ✅ XRPL transaction hash verification
- ✅ Amount confirmation (matches auction price)
- ✅ Destination address validation
- ✅ Timeout protection (24-hour window)

#### 2. Smart Contract Security
- ✅ Reentrancy guards on all state-changing functions
- ✅ Checks-effects-interactions pattern
- ✅ Access control (only authorized oracle can confirm)
- ✅ Pause mechanism for emergencies

#### 3. Monitoring
- ✅ Transaction logging
- ✅ Failed transaction alerts
- ✅ Balance reconciliation (daily)

### Planned (Production)

#### 1. Multi-Signature Wallet
- **Threshold:** 3-of-5 or 5-of-7 multisig
- **Key Holders:** Geographically distributed, independent parties
- **Rotation:** Keys rotated quarterly
- **Backup:** Secure key recovery process

#### 2. Multi-Oracle Consensus
- **Oracles:** 5+ independent node operators
- **Consensus:** 4/5 threshold required
- **Slashing:** Oracle stake burned for dishonest behavior
- **Diversity:** Different implementations, geographic distribution

#### 3. Time-Locked Withdrawals
- **Small amounts (<$1,000):** Immediate
- **Medium amounts ($1,000-$10,000):** 24-hour delay
- **Large amounts (>$10,000):** 72-hour delay + manual review

---

## Known Limitations

### Critical Risks (Testnet)

| Risk | Impact | Mitigation (Testnet) | Production Solution |
|------|--------|---------------------|---------------------|
| Single oracle failure | Bridge stops working | Manual intervention | Multi-oracle consensus |
| Oracle compromise | Fake transactions accepted | Limited funds at risk (testnet) | Slashing + multi-sig |
| Key theft | Funds stolen | Testnet funds only | Hardware wallets + multi-sig |
| XRPL downtime | Transactions delayed | Wait for recovery | Multiple oracle sources |
| Smart contract bug | Funds locked/lost | Pause + upgrade | Professional audit + formal verification |

### Trust Assumptions (Current)

⚠️ **Users must trust:**
1. Oracle operator (me) is honest
2. Private key is secure
3. XRPL API is accurate
4. Smart contract code is correct

**These assumptions are acceptable for testnet, but NOT for production.**

---

## Threat Model

### Attack Vectors

#### 1. Oracle Manipulation
**Attack:** Malicious oracle reports fake XRPL payment  
**Impact:** Buyer gets item without paying  
**Likelihood:** Low (testnet), High (production without mitigation)  
**Mitigation:** 
- Testnet: Audit logs, limited funds
- Production: Multi-oracle consensus, slashing

#### 2. Replay Attacks
**Attack:** Same XRPL transaction used multiple times  
**Impact:** Multiple payouts for single payment  
**Likelihood:** Medium  
**Mitigation:** 
- ✅ Transaction hash tracking (prevents reuse)
- ✅ Nonce validation
- ✅ Expiration timestamps

#### 3. Front-Running
**Attack:** Attacker observes pending transaction and submits higher gas  
**Impact:** Transaction ordering manipulation  
**Likelihood:** Low (Coreum uses fair ordering)  
**Mitigation:** 
- ✅ Commit-reveal scheme for bids
- ✅ Batch processing
- ✅ Fair transaction ordering (Coreum native)

#### 4. Bridge Draining
**Attack:** Exploit in bridge logic drains Community Reserve Fund  
**Impact:** Complete loss of funds  
**Likelihood:** Low (simple logic), Medium (complex bridge)  
**Mitigation:**
- Testnet: Limited funds, monitoring
- Production: Formal verification, bug bounty, insurance

#### 5. Key Compromise
**Attack:** Private key stolen or leaked  
**Impact:** Attacker controls bridge  
**Likelihood:** Medium (single key), Low (multi-sig)  
**Mitigation:**
- Testnet: Hardware wallet, limited exposure
- Production: Multi-sig, hardware security modules (HSM)

---

## Production Roadmap

### Phase 1: Multi-Sig Implementation (Q1 2026)

**Goal:** Remove single-point-of-failure in key management

**Tasks:**
- [ ] Design 3-of-5 multi-sig scheme
- [ ] Recruit 4 additional key holders (trusted community members)
- [ ] Implement multi-sig contract on Coreum
- [ ] Test with small amounts ($100-$1000)
- [ ] Document key holder responsibilities
- [ ] Create key rotation procedure

**Success Criteria:**
- All transactions require 3/5 signatures
- No single key holder can move funds alone
- Key rotation process tested and documented

### Phase 2: Multi-Oracle Consensus (Q2 2026)

**Goal:** Decentralize oracle verification

**Tasks:**
- [ ] Design oracle consensus protocol
- [ ] Recruit 5+ independent oracle operators
- [ ] Implement slashing mechanism (stake requirement)
- [ ] Build oracle monitoring dashboard
- [ ] Test with 4/5 threshold
- [ ] Document oracle selection criteria

**Success Criteria:**
- 5+ oracles running independently
- 4/5 consensus required for transaction confirmation
- Slashing works (tested with malicious oracle simulation)
- No single oracle can halt the bridge

### Phase 3: Professional Audit (Q3 2026)

**Goal:** Third-party security validation

**Tasks:**
- [ ] Select audit firm (Trail of Bits, OpenZeppelin, or similar)
- [ ] Prepare audit materials (code, docs, threat model)
- [ ] Complete audit (4-6 weeks)
- [ ] Fix all critical and high-severity findings
- [ ] Publish audit report publicly
- [ ] Implement continuous security monitoring

**Success Criteria:**
- Zero critical findings
- All high findings resolved
- Public audit report available
- Bug bounty program launched

### Phase 4: Mainnet Launch (Q4 2026)

**Goal:** Production deployment with full security measures

**Prerequisites:**
- ✅ Multi-sig implemented and tested
- ✅ Multi-oracle consensus operational
- ✅ Professional audit completed
- ✅ Insurance coverage obtained
- ✅ Legal review completed
- ✅ Emergency procedures tested

---

## Emergency Procedures

### Contract Pause

**When to Use:**
- Oracle compromise suspected
- Smart contract bug discovered
- Unusual transaction patterns
- Key holder compromise

**How to Execute:**
```solidity
// Testnet: Single admin can pause
contract.pause()

// Production: 2-of-5 multisig required
multisig.execute(contract.pause, signatures[2])
```

**Impact:**
- All new auctions halted
- Existing auctions complete normally
- Withdrawals frozen
- Bridge operations stopped

**Recovery:**
1. Investigate incident (2-4 hours)
2. Fix vulnerability or rotate keys (4-24 hours)
3. Test fix on testnet (2-4 hours)
4. Deploy fix and unpause (2 hours)
5. Post-mortem report (within 48 hours)

### Oracle Replacement

**When to Use:**
- Oracle downtime >4 hours
- Oracle producing incorrect results
- Oracle compromised

**How to Execute:**
```bash
# Remove compromised oracle
bridge.removeOracle(oracle_address)

# Add replacement oracle
bridge.addOracle(new_oracle_address)

# Verify new oracle
bridge.verifyOracle(new_oracle_address)
```

**Timeline:**
- Detection: <1 hour (monitoring)
- Replacement: <4 hours (on-call oracle ready)
- Verification: <1 hour (test transactions)

### Key Rotation

**When to Use:**
- Quarterly (scheduled)
- Key holder compromise suspected
- Key holder unavailable >72 hours

**Process:**
1. Generate new keypair (offline, hardware wallet)
2. Collect 3/5 signatures for key update
3. Update contract with new public key
4. Test new key with small transaction
5. Securely destroy old key
6. Document rotation in audit log

---

## Security Principles

### Defense in Depth

We implement multiple layers of security:

1. **Smart Contract Layer:** Reentrancy guards, access control, pause mechanism
2. **Oracle Layer:** Multi-oracle consensus, slashing, monitoring
3. **Key Management Layer:** Multi-sig, hardware wallets, rotation
4. **Network Layer:** Rate limiting, DDoS protection
5. **Monitoring Layer:** Real-time alerts, anomaly detection

### Principle of Least Privilege

- Oracle can only **confirm** transactions, not create them
- Admin can **pause** contract, but cannot withdraw funds
- Multi-sig requires **3/5** agreement, preventing unilateral action

### Transparency

- All transactions logged on-chain (immutable audit trail)
- Oracle source code public (open source)
- Audit reports published
- Incident reports available within 48 hours

---

## Metrics and Monitoring

### Key Performance Indicators

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Bridge uptime | >99.5% | <98% |
| Oracle consensus time | <60 seconds | >300 seconds |
| Failed transactions | <1% | >5% |
| Key rotation frequency | Quarterly | Overdue >14 days |

### Monitoring Dashboard

Real-time visibility into:
- Bridge health status
- Oracle consensus rate
- Transaction success rate
- Pending transactions queue
- Community Reserve Fund balance
- Failed transaction logs

---

## Questions and Answers

### Why not use an existing bridge?

**Considered:** Wormhole, LayerZero, Axelar

**Decision:** Build our own for testnet, partner for production

**Reasoning:**
- Learning: Understand bridge mechanics deeply
- Customization: Specific needs for physical goods + insurance
- Cost: Existing bridges charge 0.1-0.5% (reduces our 1.1% margin)
- Timeline: Faster to deploy simple bridge for testnet

**Future:** May partner with established bridge for production to leverage their security infrastructure.

### What's the attack surface size?

**Lines of Code:**
- Bridge oracle: ~500 lines (JavaScript)
- Smart contract: ~800 lines (Rust/CosmWasm)
- Verification service: ~300 lines (JavaScript)

**Total:** ~1,600 lines of custom bridge code

**External Dependencies:**
- XRPL library (ripple-lib)
- Coreum SDK
- Web3 libraries

**Risk:** Every line of code is potential attack surface. Production requires professional audit.

### How much is at risk?

**Testnet:** ~$0 (test tokens only)

**Production (phased launch):**
- Phase 1 (Month 1): Max $10,000 TVL
- Phase 2 (Month 2-3): Max $50,000 TVL
- Phase 3 (Month 4-6): Max $200,000 TVL
- Phase 4 (Month 7+): Community Reserve Fund threshold ($50,000+)

**Risk Mitigation:** Gradual TVL increase allows time to identify issues before significant funds at risk.

---

## Conclusion

Our bridge security strategy balances **rapid testnet iteration** with a **conservative production roadmap**. We acknowledge current limitations (single oracle, single key) are acceptable for testnet but require significant enhancement for production.

The roadmap to production prioritizes:
1. **Multi-sig** (removes single point of failure in keys)
2. **Multi-oracle** (removes single point of failure in verification)
3. **Professional audit** (validates security assumptions)
4. **Gradual scale** (limits blast radius of undiscovered bugs)

**Timeline:** 9-12 months from testnet launch to production-ready bridge.

---

## Related Documentation

- [Oracle Design](./ORACLE_DESIGN.md) - Multi-oracle consensus architecture
- [Security Patterns](./SECURITY_PATTERNS.md) - Smart contract security best practices
- [Economic Model](../business/ECONOMIC_MODEL.md) - Community Reserve Fund economics
- [Emergency Runbook](../operations/EMERGENCY_RUNBOOK.md) - Incident response procedures

---

## Changelog

- **2026-02-15:** Initial version (testnet implementation documented)
- **TBD:** Multi-sig implementation update
- **TBD:** Multi-oracle implementation update
- **TBD:** Audit findings integration

---

## Feedback

This is a living document. If you identify security concerns or have suggestions, please:
- Open an issue: https://github.com/greg-gzillion/TX/issues
- Email: gjf20842@gmail.com
- Security vulnerabilities: security@phoenixpme.com (private disclosure)

**Bug Bounty:** Coming in Q3 2026 after professional audit.
