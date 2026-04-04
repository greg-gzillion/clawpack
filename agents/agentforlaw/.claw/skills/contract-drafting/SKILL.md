# Contract Drafting Skill

## Trigger
/draft contract [type]

## Types
- service
- sale
- employment
- lease
- partnership
- loan

## Workflow
1. Identify contract type
2. Parse parties JSON
3. Parse provisions JSON
4. Apply governing law default (Delaware)
5. Output contract in plain English

## Template
============================================================
[CONTRACT TYPE] CONTRACT
============================================================

PARTIES: [party_a] and [party_b]

[SERVICES/GOODS]: [description]

[PAYMENT/PRICE]: [amount]

GOVERNING LAW: [state]

Date: [current date]
============================================================
