# PSE (Proof of Support Emission) Module

## Overview
The PSE (Proof of Support Emission) module is TX Blockchain's staking rewards distribution mechanism. It rewards delegators for supporting the network by delegating their tokens to validators. Unlike traditional inflation rewards, PSE is designed to be more flexible and efficient.

## Key Features
- **Multi-block distribution** - Large distributions split across multiple blocks
- **Sequential processing** - Distributions processed in order
- **State tracking** - Tracks processed distributions via LastProcessedDistributionID
- **Score-based rewards** - Rewards proportional to delegation time and amount
- **Clearing accounts** - Fee distribution to multiple destinations

## Architecture
┌─────────────────────────────────────────────────────────┐
│ PSE Module │
├─────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────────┐ ┌──────────────────────────┐ │
│ │ Allocation │ │ Distribution Schedule │ │
│ │ Schedule │◄───│ • Timestamp-based │ │
│ │ • Sequential IDs│ │ • Sequential IDs │ │
│ │ • Timestamps │ │ • Multi-block capable │ │
│ └─────────────────┘ └──────────────────────────┘ │
│ │
│ ┌─────────────────┐ ┌──────────────────────────┐ │
│ │ Score Tracking │ │ Distribution Processing │ │
│ │ • Account │ │ • Multi-block support │ │
│ │ • Delegation │ │ • Progress tracking │ │
│ │ • Snapshots │ │ • Cleanup │ │
│ └─────────────────┘ └──────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────┘

text

## Core Concepts

### Distribution Schedule
Scheduled distributions with:
- **ID**: Sequential identifier (1, 2, 3...)
- **Timestamp**: Unix timestamp when distribution occurs
- **Allocations**: List of clearing accounts and amounts

### Last Processed Distribution ID
Tracks the last completed distribution:
- `0`: No distribution processed yet
- `1+`: ID of last completed distribution
- Preserved in state for visibility

### Account Scores
Scores accumulate over time based on:
- Delegation amount
- Time delegated
- Validator performance

### Clearing Accounts
Recipients of PSE rewards:
- Investors
- Development fund
- Community reserve
- Staking rewards
- Validator commissions
- Ecosystem fund

## Distribution Flow

### 1. Schedule Creation
```bash
# Governance creates distribution schedule
txd tx pse update-distribution-schedule \
  --schedule '[
    {
      "id": 1,
      "timestamp": 1700000000,
      "allocations": [
        {"clearing_account": "core1investor...", "amount": "1000000"},
        {"clearing_account": "core1dev...", "amount": "500000"}
      ]
    }
  ]' \
  --from gov-module \
  --chain-id tx-mainnet-1 \
  -y
2. Score Accumulation
Delegators earn scores over time

Scores tracked per distribution ID

Snapshot taken before each distribution

3. Distribution Processing
At scheduled timestamp, distribution begins

If large, split across multiple blocks

Processed in order of ID

Progress tracked via LastProcessedDistributionID

4. Cleanup
After processing, ID marked as processed

Entry preserved in state for visibility

Scores cleaned up

Ongoing distribution removed

Score Calculation
Delegator Score Formula
text
Score = Σ (Delegation Amount × Time Delegated)
Total Score
text
TotalScore = Σ(All Delegator Scores)
Reward Distribution
text
Delegator Reward = (Delegator Score / Total Score) × Distribution Amount
State Management
Key Stores
Store	Key	Value	Description
AllocationSchedule	ID	ScheduledDistribution	All distributions (processed + unprocessed)
LastProcessedDistributionID	-	uint64	ID of last completed distribution
AccountScoreSnapshot	(ID, Address)	Int	Account score at distribution
DelegationTimeEntries	(ID, Acc, Val)	DelegationTimeEntry	Delegation records per distribution
TotalScore	ID	Int	Total score for distribution
OngoingDistribution	-	ScheduledDistribution	Currently processing distribution
DistributedAmount	ID	Int	Amount distributed so far
Genesis State
protobuf
message GenesisState {
  repeated ScheduledDistribution scheduled_distributions = 1;
  repeated AccountScore account_scores = 2;
  bool distributions_disabled = 3;
  repeated TotalScoreEntry total_scores = 4;
  uint64 last_processed_distribution_id = 5;
}
Multi-Block Distribution
Why Multi-Block?
Large distributions may exceed block gas limits

Splitting across blocks prevents failures

Maintains deterministic processing

Process
Initiate: Distribution begins at scheduled timestamp

Process: Partially distribute in current block

Save: Store progress in OngoingDistribution

Resume: Continue in next block

Complete: Clean up when fully distributed

Example
text
Block 1000: Start distribution of 10,000,000 UTX
Block 1001: Processed 5,000,000 UTX, remaining 5,000,000
Block 1002: Processed 3,000,000 UTX, remaining 2,000,000
Block 1003: Processed 2,000,000 UTX, complete
Block 1004: Clean up, set LastProcessedDistributionID = 1
Queries
Get Last Processed Distribution ID
bash
txd query pse last-processed-distribution-id \
  --node https://rpc.testnet-1.coreum.dev:443
Get Scheduled Distributions
bash
# All distributions (processed + unprocessed)
txd query pse scheduled-distributions \
  --node https://rpc.testnet-1.coreum.dev:443
Get Account Score
bash
# Get current score for address
txd query pse score core1... \
  --node https://rpc.testnet-1.coreum.dev:443
Get Distribution Parameters
bash
txd query pse params \
  --node https://rpc.testnet-1.coreum.dev:443
Get Clearing Account Balances
bash
txd query pse clearing-account-balances \
  --node https://rpc.testnet-1.coreum.dev:443
Parameters
Parameter	Description
MinDistributionGapSeconds	Minimum time between distributions
ExcludedAddresses	Addresses excluded from rewards
ClearingAccountMappings	Fee distribution destinations
Messages
Update Distribution Schedule
protobuf
message MsgUpdateDistributionSchedule {
  string authority = 1;
  repeated ScheduledDistribution schedule = 2;
}
Validation Rules:

Schedule IDs must be sequential

No gaps from LastProcessedDistributionID + 1

Minimum gap between distributions enforced

Update Min Distribution Gap
protobuf
message MsgUpdateMinDistributionGap {
  string authority = 1;
  uint64 min_distribution_gap_seconds = 2;
}
Update Excluded Addresses
protobuf
message MsgUpdateExcludedAddresses {
  string authority = 1;
  repeated string excluded_addresses = 2;
}
Events
Distribution Started
json
{
  "type": "pse_distribution_started",
  "attributes": {
    "distribution_id": "1",
    "timestamp": "1700000000"
  }
}
Distribution Progress
json
{
  "type": "pse_distribution_progress",
  "attributes": {
    "distribution_id": "1",
    "distributed_amount": "5000000",
    "remaining_amount": "5000000"
  }
}
Distribution Completed
json
{
  "type": "pse_distribution_completed",
  "attributes": {
    "distribution_id": "1",
    "total_amount": "10000000"
  }
}
PSE in PhoenixPME
Integration
PhoenixPME auction fees (1.1%) go to Community Reserve Fund

CRF receives PSE rewards

Stakers earn PSE rewards for securing network

Fee Flow
text
Auction Success
    ↓
1.1% Platform Fee
    ↓
Community Reserve Fund (Clearing Account)
    ↓
PSE Distribution
    ↓
Stakers (via delegation)
Migration (v6 → v7)
Changes
Multi-block support: Large distributions split across blocks

LastProcessedDistributionID: Tracks progress

Preserved entries: Processed distributions kept in state

Sequential IDs: Enforced with no gaps

Migration Steps
Clear old schedule entries

Load new schedule from embedded JSON

Set LastProcessedDistributionID = 1

Reinitialize delegation time entries

Migrate account score snapshots

Proto Definitions
For detailed structure, refer to:

genesis.proto

query.proto

tx.proto

params.proto
