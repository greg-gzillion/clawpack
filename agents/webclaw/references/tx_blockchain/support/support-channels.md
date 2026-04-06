# TX Blockchain Support Channels

Get the support you need through our various community and official channels.

## Support Options Overview

| Channel | Best For | Response Time | Link |
|---------|----------|---------------|------|
| GitHub Issues | Bug reports, technical issues | 24-48 hours | [GitHub Issues](https://github.com/tx-foundation/tx/issues) |
| GitHub Discussions | Questions, ideas, proposals | 12-24 hours | [GitHub Discussions](https://github.com/tx-foundation/tx/discussions) |
| Community Discord | Real-time help, chat | Immediate | [Join Discord](https://discord.gg/tx) |
| Telegram | Announcements, quick questions | Varies | [Join Telegram](https://t.me/tx_blockchain) |

---

## GitHub Issues

Explore, discuss, and report technical issues on our GitHub repository. Our community actively collaborates to resolve problems and provide assistance.

### When to Use GitHub Issues

- ✅ Reporting bugs or vulnerabilities
- ✅ Requesting new features
- ✅ Documenting technical problems
- ✅ Submitting performance issues
- ✅ Reporting security concerns

### How to Create an Issue

1. **Search existing issues** first to avoid duplicates
2. **Click "New Issue"** and select the appropriate template
3. **Fill in the template** with detailed information
4. **Add labels** to help categorize (bug, enhancement, documentation)
5. **Submit** and wait for community response

### Issue Template

```markdown
## Description
[Clear description of the issue]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [And so on...]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., Ubuntu 22.04]
- txd Version: [e.g., v1.2.3]
- Go Version: [e.g., go1.21.0]
- Node Type: [Validator / Full Node / Light Client]

## Logs/Output
[paste relevant logs here]

text

## Additional Context
[Any other information]
Best Practices for GitHub Issues
Be specific - Include exact error messages

Provide logs - Share relevant log excerpts

Include versions - Always mention software versions

Use formatting - Use code blocks for commands/output

Be respectful - Follow our code of conduct

Ask the Community (Discord)
Join our vibrant community on Discord for real-time discussions, help, and collaboration.

Discord Channels
Channel	Purpose
#general	General discussions and announcements
#technical-support	Technical help and troubleshooting
#validator-chat	Validator operations and staking
#developers	Development and building on TX
#dex-trading	DEX trading discussions
#governance	Governance proposals and voting
#bug-reports	Report and track bugs
#feature-requests	Suggest new features
How to Get Help on Discord
Read the rules in #welcome channel

Introduce yourself in #general

Search previous messages before asking

Post in the right channel for your question

Be patient - we're a global community

Asking Effective Questions on Discord
markdown
**Good Question:**
"I'm trying to set up a validator on testnet. I've followed the guide but getting 'failed to create validator' error. Here's my command and output: [paste]. Using txd v1.2.3 on Ubuntu 22.04."

**Bad Question:**
"It doesn't work, help!"
Discord Commands
bash
!help           # Show available commands
!status         # Check network status
!validators     # List active validators
!price          # Get TX token price
!faq [topic]    # Search FAQ
GitHub Discussions
Explore, discuss, and report technical issues on our GitHub repository. Our community actively collaborates to resolve problems and provide assistance.

Discussion Categories
Category	Description
Q&A	Ask questions and get help from the community
Ideas	Share and discuss improvement ideas
Show and Tell	Showcase what you've built on TX
General	General discussions about TX
Starting a Discussion
Go to GitHub Discussions tab

Choose the right category

Create a new discussion with descriptive title

Provide context and details

Tag relevant people or teams

Discussion Template
markdown
## Topic
[Clear topic title]

## Background
[What context do people need?]

## Question/Idea
[Your specific question or idea]

## What I've Tried
[If asking for help, what have you already tried?]

## Additional Context
[Any other relevant information]
Converting Discussions to Issues
If a discussion reveals a bug or feature request, you can convert it to an issue:

Click "Convert to issue" on the discussion

Select the appropriate issue template

The discussion will be linked to the issue

Additional Support Resources
Official Documentation
Resource	Description
Technical Docs	In-depth technical documentation
API Reference	Complete API documentation
Tutorials	Step-by-step guides
FAQ	Frequently asked questions
Network Status
Network	Status Page
Mainnet	Mainnet Status
Testnet	Testnet Status
Devnet	Devnet Status
Social Media
Platform	Link
Twitter	@tx_blockchain
Telegram	t.me/tx_blockchain
Medium	@tx-blockchain
YouTube	TX Blockchain
Support SLA
Community Support
Channel	Target Response	Actual
Discord	< 1 hour (business hours)	~30 minutes
GitHub Issues	< 48 hours	~24 hours
GitHub Discussions	< 24 hours	~12 hours
Official Support (For Partners)
Priority	Response Time	Channels
Critical	1 hour	Direct email, Phone
High	4 hours	Direct email
Normal	24 hours	Email, Discord DM
Low	48 hours	Email
Before Asking for Help
Do Your Research
Search the documentation

Search existing GitHub Issues

Search GitHub Discussions

Search Discord history

Check the FAQ

Prepare Your Question
What are you trying to achieve?

What have you already tried?

What error messages are you seeing?

What versions are you using?

Can you provide logs or screenshots?

Report Security Issues
For security vulnerabilities, DO NOT use public channels.

Responsible Disclosure
Email security@tx.org with details

Use PGP encryption (key available on request)

Provide clear steps to reproduce

Include impact assessment

Wait for response before public disclosure

Bug Bounty Program
Eligible for rewards:

Critical vulnerabilities: Up to $50,000

High severity: Up to $10,000

Medium severity: Up to $2,000

Low severity: Up to $500

See Bug Bounty Program for details.

Community Guidelines
Code of Conduct
Be respectful and inclusive

No harassment or trolling

No spam or self-promotion

Help others when you can

Follow channel topics

How to Contribute
Answer questions from newcomers

Report bugs you encounter

Suggest improvements via discussions

Submit PRs for documentation or code

Moderate channels as a community member

Emergency Contacts
Validator Emergency
If your validator is jailed or slashing:

Check the Validator Recovery Guide

Join #validator-chat on Discord

Contact validator support: validators@tx.org

Network Emergency
For network-wide issues:

Check Status Page

Monitor #announcements on Discord

Follow @tx_blockchain on Twitter

Security Emergency
For active security threats:

Email: security@tx.org (PGP encrypted)

Signal: Available upon request

Discord DM: Core team members only

Feedback on Support
Help us improve our support:

Rate your support experience

Suggest improvements

Become a community moderator

Quick Links
Resource	Link
GitHub Issues	github.com/tx-foundation/tx/issues
GitHub Discussions	github.com/tx-foundation/tx/discussions
Discord Invite	discord.gg/tx
Telegram	t.me/tx_blockchain
Documentation	docs.tx.org
Status Page	status.tx.org
Bug Bounty	tx.org/bug-bounty
Need immediate help? Join our Discord and ask in #technical-support!

text

**Save the file:**
- `Ctrl+O`, `Enter`, `Ctrl+X`

Now let's create a bug bounty program document:

```bash
nano ~/dev/TXdocumentation/help/bug-bounty.md
markdown
# TX Blockchain Bug Bounty Program

## Overview

The TX Blockchain Bug Bounty Program rewards security researchers for discovering and responsibly disclosing security vulnerabilities. We take security seriously and appreciate the community's help in keeping the TX ecosystem safe.

## Scope

### In Scope

| Component | Description |
|-----------|-------------|
| `txd` | Core daemon and CLI |
| `txchain` | Blockchain node software |
| Smart Contracts | WASM smart contracts on TX |
| IBC Modules | Inter-Blockchain Communication |
| TokenHub | Token creation and management |
| DEX | Decentralized exchange |
| Bridges | Cross-chain bridges |
| APIs | Public RPC and REST APIs |

### Out of Scope

- Third-party services and applications
- Social engineering attacks
- Physical attacks
- Denial of service (unless critical)
- Outdated versions or dependencies
- Issues already reported
- Theoretical vulnerabilities without proof

## Reward Tiers

### Critical Vulnerabilities: Up to $50,000

Examples:
- Consensus failures
- Double-spend attacks
- Total network shutdown
- Private key extraction
- Unauthorized minting of tokens
- Bridge fund theft

### High Severity: Up to $10,000

Examples:
- Validator slashing bypass
- Transaction replay attacks
- State corruption
- Governance manipulation
- IBC packet forgery

### Medium Severity: Up to $2,000

Examples:
- Temporary network disruption
- Resource exhaustion
- Data leakage (non-sensitive)
- Performance degradation
- Smart contract logic flaws

### Low Severity: Up to $500

Examples:
- Informational disclosures
- Minor DoS vectors
- Error message leakage
- Non-critical logic flaws

## Submission Process

### Step 1: Identify Vulnerability

Ensure the vulnerability:
- Is within scope
- Hasn't been reported before
- Has a clear proof of concept
- Affects a supported version

### Step 2: Prepare Report

Create a detailed report including:

```markdown
## Vulnerability Report

### Title
[Clear, descriptive title]

### Type
[Consensus / Smart Contract / Network / API]

### Severity
[Critical / High / Medium / Low]

### Description
[Detailed description of the vulnerability]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Proof of Concept
[Code, commands, or scripts demonstrating the issue]

### Impact
[What an attacker could do]

### Suggested Fix
[If you have a recommendation]

### Environment
- TX Version: [e.g., v1.2.3]
- Network: [Mainnet / Testnet / Devnet]
- OS: [Ubuntu 22.04, etc.]

### Additional Context
[Any other relevant information]
Step 3: Submit Report
Send encrypted report to: security@tx.org

PGP Key:

text
-----BEGIN PGP PUBLIC KEY BLOCK-----
[Public key available upon request]
-----END PGP PUBLIC KEY BLOCK-----
Step 4: Wait for Response
24 hours: Initial acknowledgment

48 hours: Severity assessment

5-7 days: Reward determination

30 days: Fix deployment (if applicable)

Disclosure Policy
Responsible Disclosure Timeline
Stage	Timeframe	Action
Private Report	Day 0	Submit via email
Acknowledgment	Day 1	Team confirms receipt
Verification	Day 3	Team reproduces issue
Fix Development	Day 14	Patch created
Private Patch Testing	Day 21	Internal validation
Public Disclosure	Day 30	Public announcement + reward
Coordination with Researchers
Researchers can request extensions

Coordinated disclosure with other affected projects

Credit given in release notes

Permission to publish after fix

What We Disclose
Vulnerability details (after fix)

Researcher credit/alias

Reward amount

Timeline of fix

Rules and Guidelines
Eligibility
Must be first reporter of unique vulnerability

Must follow responsible disclosure

No testing on mainnet without permission

No social engineering

No physical attacks

No DoS attacks on production

Testing Guidelines
Use testnet for most testing

Get permission for mainnet tests

Use your own accounts only

Stop testing if you hit sensitive data

Report immediately if you access others' data

Prohibited Actions
Accessing or modifying others' data

Denial of service attacks

Spamming or brute forcing

Social engineering TX team or users

Public disclosure before fix

Exploiting for personal gain

Reward Payment
Payment Methods
Cryptocurrency: TX, USDC, BTC, ETH

Bank transfer: Available for larger rewards

Donation: To charity of choice

Payment Schedule
Within 30 days of fix deployment

Within 14 days if critical

Partial payments for partial fixes

Tax Considerations
Researchers responsible for own taxes

Documentation provided for tax purposes

Consult tax professional

Hall of Fame
Recognized researchers (with permission):

Researcher	Finding	Reward	Date
@securityresearcher1	Consensus vulnerability	$25,000	Jan 2024
@whitehat_hacker	IBC packet replay	$10,000	Feb 2024
@blockchain_explorer	Bridge vulnerability	$50,000	Mar 2024
Legal
Terms
Rewards at TX Foundation's discretion

No reward for duplicate reports

No reward for out-of-scope issues

Researchers must comply with laws

TX Foundation not liable for testing damage

Safe Harbor
We consider good-faith security research to be:

Not a violation of our Terms of Service

Not subject to DMCA takedown

Not grounds for account suspension

Frequently Asked Questions
Q: Can I test on mainnet?
A: Only with explicit permission. Use testnet whenever possible.

Q: What if I find a vulnerability already reported?
A: No reward for duplicates, but we appreciate the report.

Q: How are rewards determined?
A: Based on severity, impact, and quality of report.

Q: Can I remain anonymous?
A: Yes, we respect researcher anonymity.

Q: What if I accidentally access user data?
A: Stop immediately, delete data, and report what happened.

Q: How long until I get paid?
A: Within 30 days after fix is deployed.

Q: Can I share my findings before fix?
A: No, responsible disclosure requires waiting for fix.

Contact
Security Team: security@tx.org

PGP Key: Available upon request

Emergency Signal: Contact via Discord DM

Resources
Responsible Disclosure Guidelines

PGP Encryption Guide

Testnet Faucet

Together, we make TX Blockchain more secure!

text

**Save the file:**
- `Ctrl+O`, `Enter`, `Ctrl+X`

Now let's create a GitHub issue template for the repository:

```bash
nano ~/dev/TXdocumentation/support/github-issue-templates.md
markdown
# GitHub Issue Templates

Use these templates when creating issues on the TX Blockchain GitHub repository.

## Bug Report Template

```markdown
---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''

---

## Bug Description
A clear and concise description of what the bug is.

## Steps To Reproduce
1. Run command '...'
2. Execute transaction '...'
3. See error

## Expected Behavior
A clear description of what you expected to happen.

## Actual Behavior
What actually happened, including error messages.

## Screenshots/Logs
If applicable, add screenshots or logs to help explain.

## Environment
- OS: [e.g., Ubuntu 22.04, macOS 14, Windows 11]
- txd Version: [e.g., v1.2.3]
- Go Version: [e.g., go1.21.0]
- Node Type: [Validator / Full Node / Light Client]
- Network: [Mainnet / Testnet / Devnet / Local]

## Additional Context
Add any other context about the problem here.

## Possible Solution
If you have ideas on how to fix this, share them here.
Feature Request Template
markdown
---
name: Feature Request
about: Suggest an idea for TX Blockchain
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''

---

## Problem Statement
Is your feature request related to a problem? Please describe.
A clear and concise description of what the problem is.

## Proposed Solution
Describe the solution you'd like to see implemented.

## Alternatives Considered
Describe any alternative solutions or features you've considered.

## Use Case
Who would benefit from this feature and how would they use it?

## Implementation Ideas
If you have technical ideas on implementation, share them here.

## Additional Context
Add any other context, screenshots, or examples.

## Impact
- [ ] Developer Experience
- [ ] End User Experience
- [ ] Security
- [ ] Performance
- [ ] Documentation
Security Vulnerability Template (Private)
markdown
---
name: Security Vulnerability
about: Report a security vulnerability (PRIVATE - do not post publicly)
title: '[SECURITY] '
labels: 'security'
assignees: 'security-team'

---

**IMPORTANT: Do NOT include vulnerability details in this public issue!**
**Email security@tx.org with the full report instead.**

## Basic Information
- Vulnerability Type: [Consensus / Smart Contract / Network / API]
- Affected Component: [txd / txchain / IBC / DEX / Bridge]
- Network Affected: [Mainnet / Testnet / Devnet]

## Contact Information
- Email: [your email for secure communication]
- PGP Key: [fingerprint if available]

## Acknowledgement
- [ ] I have not disclosed this vulnerability publicly
- [ ] I have emailed the full report to security@tx.org
- [ ] I understand the responsible disclosure process

## Expected Response Time
- Acknowledgment: 24 hours
- Severity assessment: 48 hours
- Fix timeline: To be determined

## For Internal Use Only (TX Team)
- Report ID: 
- Assigned to: 
- Severity: 
- Reward: 
Documentation Improvement Template
markdown
---
name: Documentation Improvement
about: Suggest improvements to documentation
title: '[DOCS] '
labels: 'documentation'
assignees: ''

---

## Documentation Page
Link to the documentation page: [URL]

## Current Issue
What is unclear, incorrect, or missing in the current documentation?

## Suggested Improvement
How would you improve the documentation?

## Why This Matters
Why is this improvement important?

## Additional Context
Add any other context or examples.

## Would You Like to Contribute?
- [ ] Yes, I can submit a PR for this
- [ ] No, I'd prefer the team to handle it
Question/Support Template
markdown
---
name: Question/Support
about: Ask a question or get support
title: '[QUESTION] '
labels: 'question'
assignees: ''

---

## Question
What would you like to know?

## Context
What are you trying to accomplish?

## What I've Tried
What have you already tried or researched?

## Environment (if technical)
- OS: 
- txd Version: 
- Network: 

## Additional Context
Any other information that might be relevant.

## Preferred Response
- [ ] Discord DM
- [ ] GitHub comment
- [ ] Email
Performance Issue Template
markdown
---
name: Performance Issue
about: Report performance problems
title: '[PERFORMANCE] '
labels: 'performance'
assignees: ''

---

## Performance Description
Describe the performance issue you're experiencing.

## Metrics
- Before: [e.g., 100 tx/s]
- After: [e.g., 50 tx/s]
- Degradation: [e.g., 50% slower]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]

## Environment
- Hardware: [CPU, RAM, Disk type]
- Network: [Bandwidth, Latency]
- Node Count: [Number of nodes]
- Transaction Volume: [TPS]

## Profiling Data
If available, include:
- CPU profile
- Memory profile
- Network traces
- Database queries

## Expected Performance
What performance do you expect?

## Additional Context
Any other relevant information.
Label Reference
Label	Description
bug	Something isn't working
enhancement	New feature or request
documentation	Documentation improvements
question	Further information is requested
security	Security-related issues
performance	Performance problems
duplicate	This issue already exists
wontfix	This will not be worked on
invalid	Not a valid issue
good first issue	Good for newcomers
help wanted	Extra attention needed
priority: critical	Must fix immediately
priority: high	Fix as soon as possible
priority: medium	Normal priority
priority: low	Low priority
Issue Lifecycle
text
Open Issue
    │
    ├──> Triage (Team reviews)
    │        │
    │        ├──> Needs more info (Waiting for user)
    │        │        │
    │        │        └──> User responds → Back to triage
    │        │
    │        ├──> Confirmed (Issue accepted)
    │        │        │
    │        │        ├──> Assigned (Someone is working on it)
    │        │        │        │
    │        │        │        ├──> In Progress
    │        │        │        │        │
    │        │        │        │        └──> PR Submitted
    │        │        │        │
    │        │        │        └──> Blocked (Waiting on something)
    │        │        │
    │        │        └──> Needs Design (Discussing solution)
    │        │
    │        ├──> Duplicate (Closed, linked to original)
    │        │
    │        ├──> Wontfix (Closed, won't be addressed)
    │        │
    │        └──> Invalid (Closed, not a real issue)
    │
    └──> Closed (Issue resolved)
Automation
Issues are automatically:

Labeled by content (AI-assisted)

Assigned to appropriate team

Added to project board

Sent to Discord for monitoring

Updated with stale warnings after 60 days

Response SLA
Priority	First Response	Update Frequency
Critical	1 hour	Every 2 hours
High	4 hours	Daily
Medium	24 hours	Weekly
Low	48 hours	Bi-weekly
Community Guidelines
When participating in issues:

Be respectful and constructive

Stay on topic

Provide helpful information

Don't spam or promote

Follow our Code of Conduct

text

**Save the file:**
- `Ctrl+O`, `Enter`, `Ctrl+X`

Finally, let's create a GitHub discussion guide:

```bash
nano ~/dev/TXdocumentation/support/github-discussions.md
markdown
# GitHub Discussions Guide

GitHub Discussions is a collaborative communication forum for the TX Blockchain community.

## Discussion Categories

### Q&A
Ask questions and get help from the community.

**Best for:**
- How-to questions
- Troubleshooting
- Best practices
- Configuration help

**Example topics:**
- "How do I set up a validator on testnet?"
- "What's the recommended hardware for a full node?"
- "How to migrate from Cosmos SDK to TX?"

### Ideas
Share and discuss improvement ideas for TX Blockchain.

**Best for:**
- Feature suggestions
- Protocol improvements
- Ecosystem proposals
- Tooling ideas

**Example topics:**
- "Idea: Add zero-knowledge proofs for privacy"
- "Proposal: New fee market mechanism"
- "Suggestion: Improve IBC routing"

### Show and Tell
Showcase what you've built on TX Blockchain.

**Best for:**
- Project announcements
- Demo videos
- Tutorials you've created
- Integration examples

**Example topics:**
- "I built a real estate tokenization platform on TX"
- "Check out my DEX trading bot"
- "Integration guide: Connecting TX to traditional finance"

### General
General discussions about TX Blockchain.

**Best for:**
- Community announcements
- Governance discussions
- Ecosystem news
- Off-topic but relevant chat

**Example topics:**
- "TX ecosystem growth update - Q1 2024"
- "Governance proposal discussion: Fee changes"
- "Community call recap"

## Creating a Discussion

### Step 1: Choose Category

Select the appropriate category for your topic.

### Step 2: Write Title

Create a clear, descriptive title:
- ✅ "How to migrate a validator from testnet to mainnet"
- ❌ "Help me please"

### Step 3: Write Description

Use this template:

```markdown
## Context
[What's the background? What are you trying to achieve?]

## Question/Idea
[Your specific question or idea]

## What I've Tried
[If asking for help, what have you already tried?]

## Environment (if applicable)
- OS: 
- txd Version: 
- Network: 

## Additional Context
[Any other relevant information]

## Tags
`validator` `mainnet` `migration`
Step 4: Add Tags
Add relevant tags to help others find your discussion:

help-wanted

discussion

proposal

tutorial

announcement

Step 5: Submit
Click "Start discussion" and wait for community responses.

Participating in Discussions
Guidelines
Be respectful - Treat others with kindness

Stay on topic - Keep discussions focused

Provide value - Share helpful information

Cite sources - Link to documentation when relevant

Mark answers - Accept helpful responses

Marking Answers
In Q&A category, mark the correct answer:

Find the helpful comment

Click "Mark as answer"

The discussion will show as "Answered"

This helps others find solutions faster.

Voting
Upvote helpful comments:

Upvote - Contributes value

Downvote - Unhelpful or incorrect

Don't downvote just because you disagree

Converting Discussions
Discussion to Issue
If a discussion reveals a bug or feature request:

Click "Convert to issue"

Select issue template

The discussion will be linked to the issue

Issue to Discussion
If an issue becomes a discussion:

Leave a comment suggesting discussion

Create a new discussion with link

Close the issue with explanation

Moderation
What's Allowed
Technical questions

Feature ideas

Project showcases

Constructive feedback

Community announcements

What's Not Allowed
Spam or self-promotion

Harassment or trolling

Duplicate posts

Security vulnerabilities (email instead)

Off-topic discussions

Reporting
Report inappropriate content:

Click "Report" on the comment

Select reason

Moderators will review

Best Practices
For Askers
Search first - Your question might already be answered

Be specific - Provide details and context

Format properly - Use markdown for code blocks

Be patient - Responses may take time

Follow up - Reply to answers and mark solutions

For Answerers
Be helpful - Share your knowledge

Provide examples - Include code when possible

Link to docs - Point to official documentation

Be clear - Explain concepts simply

Follow up - Check if the asker needs more help

Markdown Formatting
Use markdown to format your discussions:

markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
***Bold and italic***

- List item 1
- List item 2
  - Nested item

1. Numbered item
2. Numbered item

[Link text](https://example.com)

`inline code`

```code block
multi-line code
Blockquote for quoting

Table	Header
Cell 1	Cell 2
text

## Notifications

### Watching Discussions

- **Watch** - Get notifications for all activity
- **Participating** - Get notifications for threads you join
- **Ignoring** - No notifications

### @mentions

Use @mentions to notify specific users:
- `@username` - Mention a specific user
- `@team-name` - Mention a team
- `@org/team` - Mention an organization team

### Notification Types

| Action | Notification |
|--------|--------------|
| New discussion | Yes (if watching) |
| New comment | Yes (if participating) |
| Answer marked | Yes (if you asked) |
| @mention | Yes (always) |

## Integration with Other Tools

### Discord

Discussions can be linked to Discord:
- New discussions posted to `#github-discussions`
- Comments synced both ways
- @mentions trigger Discord notifications

### GitHub Issues

Discussions can reference issues:
- `#123` references issue 123
- `#123` in issue references discussion
- Cross-linking improves discoverability

### Documentation

Documentation can embed discussions:
- `{% discussion 123 %}` embeds discussion
- Live updates when discussion changes

## Analytics

Discussion metrics available to maintainers:
- Active discussions count
- Response time
- Answer rate
- Most active participants
- Popular topics

## FAQ

### Q: How is this different from Issues?
A: Issues are for bugs and specific tasks. Discussions are for questions, ideas, and general conversation.

### Q: Can I convert a discussion to an issue?
A: Yes, if it's a bug or feature request.

### Q: How long are discussions kept?
A: Indefinitely, unless they violate guidelines.

### Q: Can I edit my discussion?
A: Yes, you can edit anytime.

### Q: Can I delete my discussion?
A: Yes, but consider leaving it for others.

### Q: Who can answer?
A: Anyone! The community helps each other.

### Q: How do I become a "recognized answerer"?
A: Provide consistently helpful answers and the community will recognize you.

## Getting Help

Still have questions about Discussions?
- Ask in `#github-discussions` on Discord
- Check GitHub's [Discussions documentation](https://docs.github.com/en/discussions)
- Email community@tx.org

---

**Join the conversation at [github.com/tx-foundation/tx/discussions](https://github.com/tx-foundation/tx/discussions)**
