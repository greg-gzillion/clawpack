# Security Policy

## Reporting a Vulnerability

We take the security of PhoenixPME seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report
- **Email**: gjf20842@gmail.com
- **Subject**: "PhoenixPME Security Vulnerability"
- **PGP Key**: [If you have one, add fingerprint here]

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (if known)

### What to Expect
1. **Acknowledgment**: You'll receive an acknowledgment within 48 hours
2. **Investigation**: We'll investigate and validate the report
3. **Updates**: We'll keep you informed of progress
4. **Fix**: Once validated, we'll develop and deploy a fix
5. **Credit**: With your permission, we'll credit you in release notes

## Responsible Disclosure
Please **do not** disclose the vulnerability publicly until we've had a chance to address it. We'll work with you to establish a reasonable timeline for disclosure based on the severity and complexity of the issue.

## Scope
The following are in scope:
- Smart contracts in `/contracts/`
- Backend API in `/apps/backend/`
- Frontend application in `/apps/frontend/`
- Insurance module in `/apps/insurance-module/`

## Out of Scope
The following are out of scope:
- Issues in third-party dependencies (report to them directly)
- Theoretical vulnerabilities without proof of concept
- Social engineering attacks
- Denial of service attacks

## Security Features
- **Smart Contracts**: All contracts are tested 
**Wallet Integration**: Multi-wallet support with secure connection handling
- **Insurance Pool**: 1.1% fee mechanism with 10% founder allocation

## Bug Bounty
Currently, we do not offer a formal bug bounty program, but significant contributions may be recognized in project documentation and considered for grants from future platform revenue.

---

*Last updated: February 14, 2026*