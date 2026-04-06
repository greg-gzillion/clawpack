# Validator Funding Requirements

## Overview
Becoming a validator on TX Blockchain requires staking a minimum amount of tokens. This guide explains the funding requirements and provides a clear breakdown of costs.

## Minimum Recommended: 20,300 TX Tokens

We recommend having at least **20,300 TX tokens** to become a validator. Here's the detailed breakdown:

| Component | Amount | Purpose |
|-----------|--------|---------|
| **Self-Delegation** | 20,000 TX | Minimum required to create validator |
| **Slashing Buffer** | 200 TX | Cover potential slashing (0.5% of 20,000) |
| **Transaction Fees** | 100 TX | Gas fees for operations |
| **Total** | **20,300 TX** | **Recommended minimum** |

## Understanding `min-self-delegation`

### What It Is
`min-self-delegation` is a parameter you set when creating your validator. It specifies the minimum amount of tokens you must stake with yourself for your validator to remain active.

### Minimum Value
- **Minimum**: 20,000 TX
- **Maximum**: No upper limit (can be higher)
- **Set at creation**: Cannot be changed later

### Why It Matters

```bash
# Example: Creating a validator with min-self-delegation = 20,000
txd tx staking create-validator \
  --amount=20000000utx \
  --min-self-delegation=20000000 \
  # ... other parameters
Key Points:

Your validator will only be active if your self-delegation ≥ min-self-delegation

If slashing reduces your self-delegation below this threshold, your validator becomes inactive

You must delegate more tokens to reactivate

Slashing Protection
Slashing Rates
Violation	Slash Rate	Example (20k stake)
Double Signing	5%	1,000 TX
Downtime	0.5%	100 TX
Recommended Buffer
text
Slashing Buffer = Self-Delegation × Max Expected Slash Rate
                 = 20,000 × 0.5% = 100 TX
For safety, we recommend 200 TX buffer (double the minimum) to cover:

One downtime slashing event (100 TX)

Some buffer for additional operations

Total Delegation Considerations
Active Set Requirement
⚠️ Important: Meeting min-self-delegation (20,000 TX) does NOT guarantee your validator will be in the active set.

Active Set Size: Top 64 validators by total stake

Getting into Active Set
Scenario	Total Stake Needed
Minimum	20,000+ TX (self-delegation)
Competitive	Depends on market
Top 64	Varies (check current threshold)
To join the active set, your validator's total delegation (self-delegation + delegations from others) must be in the top 64.

Delegation Strategy
bash
# Minimum approach
Self-delegation: 20,000 TX
External delegations: 0
Total stake: 20,000 TX
Status: May not be in active set

# Competitive approach
Self-delegation: 50,000 TX
External delegations: Variable
Total stake: 50,000+ TX
Status: Higher chance of active set
Cost Breakdown
Initial Costs
Item	Amount (TX)	Value (USD)*	Notes
Self-delegation	20,000	~$1,000-2,000	Minimum requirement
Slashing buffer	200	~$10-20	Safety reserve
Transaction fees	100	~$5-10	Gas for operations
Total Initial	20,300	~$1,015-2,030	
*USD values are estimates; actual prices vary

Ongoing Costs
Item	Monthly Cost (USD)	Notes
Server hosting	$50-200	Bare-metal or cloud
Bandwidth	$20-100	Network costs
Monitoring	$0-50	Tools and services
Maintenance	$0-500	Time/labor
Total Monthly	$70-850	
ROI Calculation
Rewards Structure
Parameter	Value
Annual inflation	~7%
Validator commission	5-20%
Block proposer bonus	1-5%
Example: Validator with 20,000 TX Self-Delegation
text
Total stake: 20,000 TX
Annual rewards: 20,000 × 7% = 1,400 TX
Validator commission: 10%
Net to validator: 1,400 × 10% = 140 TX
To delegators: 1,400 × 90% = 1,260 TX
Example: Validator with 50,000 TX Total Stake
text
Total stake: 50,000 TX
Annual rewards: 50,000 × 7% = 3,500 TX
Validator commission: 10%
Net to validator: 3,500 × 10% = 350 TX
Getting Tokens
Testnet
Faucet: https://faucet.testnet.tx.dev

Request tokens using your testcore address

Repeat until you have sufficient balance

bash
# Check balance
txd query bank balances $(txd keys show validator -a) \
  --node https://rpc.testnet.tx.dev:443
Mainnet
Pre-launch Sales: Participate in token sales

Exchanges: Purchase after launch

Community Grants: Apply for funding

Delegations: Attract delegators

Best Practices
1. Start with Testnet
bash
# Test your validator setup on testnet first
txd tx staking create-validator \
  --amount=20000000utestcore \
  --min-self-delegation=20000000 \
  # ... test with lower stakes
2. Monitor Your Stake
bash
# Check self-delegation
txd query staking validator $(txd keys show validator -a --bech=val) | \
  jq .tokens

# Check if in active set
txd query staking validators --limit=64 | \
  jq '.validators[] | select(.description.moniker=="your-validator")'
3. Maintain Buffer
Keep extra tokens in your wallet for:

Top-up if slashed

Transaction fees

Future delegation

4. Gradual Scaling
text
Phase 1: Start with minimum (20,000 TX)
Phase 2: Add buffer (200+ TX)
Phase 3: Increase self-delegation to attract delegators
Phase 4: Build reputation, gain external delegations
Common Questions
Q: Can I start with less than 20,000 TX?
A: No. The minimum min-self-delegation is 20,000 TX. Your validator creation will fail with less.

Q: What if my validator gets slashed below min-self-delegation?
A: Your validator becomes inactive. You must delegate more tokens to reach the minimum threshold again.

Q: Do I need 20,300 TX in my wallet or staked?
A:

20,000 TX will be staked (self-delegation)

300 TX should remain in wallet for fees and buffer

Q: How much do I need to be in top 64?
A: Check current active set threshold:

bash
txd query staking validators --limit=64 \
  --node https://rpc.testnet.tx.dev:443 | \
  jq '.validators[-1].tokens'
Q: Can I use IBC tokens?
A: No. Only native TX tokens can be used for staking.

Resources
System Requirements

Validator Setup

Network Variables

Faucet

