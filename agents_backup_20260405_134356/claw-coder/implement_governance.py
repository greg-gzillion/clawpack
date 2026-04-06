#!/usr/bin/env python3
"""
PHNX Governance System Implementation
1 PHNX per $1 TESTUSD in fees - voting weight for Community Reserve Fund
"""

class PHNXGovernance:
    """
    Governance token system based on your documentation:
    - 1 PHNX per $1 TESTUSD in fees generated
    - Non-transferable, permanent on-chain record
    - Founder: 10% weight, Community: 90% weight
    """
    
    def __init__(self):
        self.phnx_balances = {}
        self.proposals = []
        self.founder_address = "testcore1m5adn3k68tk4zqmujpnstmp9r933jafzu44tnv"
        self.founder_weight = 10  # 10% permanent
        
    def mint_phnx(self, user, fees_paid_usd):
        """
        Mint PHNX tokens based on fees paid
        1 PHNX per $1 TESTUSD in fees
        """
        phnx_amount = int(fees_paid_usd)  # 1:1 ratio
        self.phnx_balances[user] = self.phnx_balances.get(user, 0) + phnx_amount
        print(f"Minted {phnx_amount} PHNX to {user} (${fees_paid_usd} in fees)")
        return phnx_amount
    
    def calculate_voting_power(self, user):
        """
        Calculate voting power including founder's 10% weight
        """
        user_phnx = self.phnx_balances.get(user, 0)
        total_phnx = sum(self.phnx_balances.values())
        
        if total_phnx == 0:
            return 0
        
        # Community portion (90% of voting weight)
        community_share = (user_phnx / total_phnx) * 90
        
        # Founder gets additional 10% weight
        if user == self.founder_address:
            return community_share + 10
        
        return community_share
    
    def create_proposal(self, title, description, cost_testusd):
        """
        Create governance proposal for CRF spending
        """
        proposal = {
            'id': len(self.proposals) + 1,
            'title': title,
            'description': description,
            'cost': cost_testusd,
            'votes_for': 0,
            'votes_against': 0,
            'status': 'active'
        }
        self.proposals.append(proposal)
        return proposal
    
    def vote(self, proposal_id, user, support):
        """
        Vote on proposal with PHNX-weighted voting
        """
        voting_power = self.calculate_voting_power(user)
        proposal = self.proposals[proposal_id - 1]
        
        if support:
            proposal['votes_for'] += voting_power
        else:
            proposal['votes_against'] += voting_power
        
        print(f"{user} voted {'FOR' if support else 'AGAINST'} with {voting_power:.1f}% power")
        
        # Check if proposal passed (66.7% threshold)
        total = proposal['votes_for'] + proposal['votes_against']
        if total >= 66.7:  # Your pass threshold
            proposal['status'] = 'passed' if proposal['votes_for'] >= 66.7 else 'failed'
            print(f"Proposal {proposal_id}: {proposal['status'].upper()}!")
        
        return proposal

# Integration code
def add_to_frontend():
    """
    Frontend components needed for governance
    """
    frontend_code = '''
    // Governance Dashboard Component
    // Shows:
    // - Your PHNX balance
    // - Voting power (including founder weight)
    // - Active proposals
    // - Community Reserve Fund balance
    // - Voting history
    
    function GovernanceDashboard() {
        const { phnxBalance, votingPower } = usePHNX();
        const { proposals, vote } = useGovernance();
        
        return (
            <div>
                <h2>PHNX Governance</h2>
                <p>Your PHNX: {phnxBalance}</p>
                <p>Voting Power: {votingPower}%</p>
                <ProposalList proposals={proposals} onVote={vote} />
                <CommunityReserveFund />
            </div>
        );
    }
    '''
    print(frontend_code)

if __name__ == "__main__":
    gov = PHNXGovernance()
    
    # Simulate fee collection
    gov.mint_phnx("user1", 65.70)  # $65.70 in fees = 65 PHNX
    gov.mint_phnx("user2", 25.25)   # $25.25 in fees = 25 PHNX
    
    # Calculate voting power
    print(f"\nUser1 voting power: {gov.calculate_voting_power('user1'):.1f}%")
    print(f"User2 voting power: {gov.calculate_voting_power('user2'):.1f}%")
    print(f"Founder voting power: {gov.calculate_voting_power(gov.founder_address):.1f}%")
    
    # Create and vote on proposal
    proposal = gov.create_proposal("Add Multi-Currency Support", "Integrate BTC/ETH/XRP", 5000)
    gov.vote(1, "user1", True)
    gov.vote(1, gov.founder_address, True)
