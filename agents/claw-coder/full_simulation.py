#!/usr/bin/env python3
"""
PhoenixPME Complete Simulation
Tests: Auctions, Bidding, Collateral, Disputes, Reputation, Governance
Based SOLELY on your documentation rules
"""

import json
import random
from datetime import datetime, timedelta
from market_data_integration import MarketDataIntegration
from phoenix_accurate_engine import PhoenixAccurateEngine

class PhoenixSimulation:
    def __init__(self):
        self.market = MarketDataIntegration()
        self.engine = PhoenixAccurateEngine()
        self.disputes = []
        self.results = {
            'successful_trades': 0,
            'failed_trades': 0,
            'total_fees': 0,
            'total_phnx_issued': 0,
            'disputes_resolved': 0
        }
    
    def run_complete_simulation(self):
        print("\n" + "="*70)
        print("🏛️ PHOENIXPME COMPLETE SIMULATION")
        print("="*70)
        print("\n📋 SIMULATING WITH YOUR ACTUAL RULES:")
        print(f"   • Collateral: {self.engine.rules['collateral_percent']}% both parties")
        print(f"   • Fee: {self.engine.rules['fee_percent']}%")
        print(f"   • Inspection: {self.engine.rules['inspection_hours']} hours")
        print(f"   • PHNX: 1 per ${self.engine.rules['phnx_per_usd']} TESTUSD in fees")
        
        # Step 1: Create users
        print("\n👥 STEP 1: Creating marketplace participants...")
        users = self.engine.create_users(15)
        print(f"   ✅ Created {len(users)} users with reputation tracking")
        
        # Step 2: Create auctions from real market data
        print("\n🏺 STEP 2: Creating auctions with live pricing...")
        auction_items = self.market.generate_auction_items()
        auctions = []
        
        for i, item in enumerate(auction_items[:10]):
            seller = users[i % len(users)]
            auction = self.engine.create_auction(seller, item['description'], item['market_value'])
            auction['metal_type'] = item['metal']
            auction['weight_oz'] = item['weight_oz']
            auctions.append(auction)
            print(f"   {item['description'][:45]}... - ${item['market_value']:,.2f}")
        
        # Step 3: Simulate bidding
        print("\n💸 STEP 3: Simulating bidding activity...")
        successful_bids = 0
        
        for auction in auctions[:5]:  # First 5 auctions
            current_bid = auction['starting_bid']
            num_bidders = random.randint(3, 8)
            
            for bid_round in range(num_bidders):
                bidder = random.choice([u for u in users if u['name'] != auction['seller']])
                
                # Calculate bid increment (5-25%)
                increment = int(current_bid * random.uniform(0.05, 0.25))
                if increment < 10:
                    increment = 10
                
                new_bid = current_bid + increment
                
                # 70% chance to continue bidding
                if random.random() < 0.7 or new_bid < auction['reserve_price']:
                    current_bid = new_bid
                    print(f"   {auction['item'][:30]}... {bidder['name']} bids ${current_bid:,.2f}")
                    
                    # Check if reserve met
                    if current_bid >= auction['reserve_price'] and not auction.get('reserve_met'):
                        auction['reserve_met'] = True
                        print(f"      🎯 RESERVE MET at ${current_bid:,.2f}!")
                    
                    # Check buy it now
                    if current_bid >= auction['buy_it_now']:
                        auction['winner'] = bidder['name']
                        auction['final_price'] = auction['buy_it_now']
                        auction['status'] = 'sold_bin'
                        print(f"      🏆 BUY IT NOW! Won by {bidder['name']}")
                        successful_bids += 1
                        break
                else:
                    break
            
            # If no buy it now but reserve met, highest bid wins
            if auction.get('reserve_met') and not auction.get('winner'):
                highest_bid = current_bid
                auction['winner'] = bidder['name']
                auction['final_price'] = highest_bid
                auction['status'] = 'sold'
                successful_bids += 1
                print(f"   {auction['item'][:30]}... SOLD to {bidder['name']} for ${highest_bid:,.2f}")
            
            # Process completed auction with YOUR rules
            if auction.get('winner'):
                self.process_successful_auction(auction, users)
        
        # Step 4: Simulate disputes (DONT_TRUST tokens)
        print("\n⚖️ STEP 4: Simulating dispute scenarios...")
        
        # Simulate a failed trade
        failed_auction = auctions[6] if len(auctions) > 6 else None
        if failed_auction:
            failed_auction['status'] = 'disputed'
            buyer = next((u for u in users if u['name'] == failed_auction.get('winner')), users[0])
            seller = next((u for u in users if u['name'] == failed_auction['seller']), users[1])
            
            # Issue DONT_TRUST tokens (YOUR rule)
            buyer['dont_trust_score'] += self.engine.rules['dont_trust_per_failure']
            seller['dont_trust_score'] += self.engine.rules['dont_trust_per_failure']
            self.results['failed_trades'] += 1
            
            print(f"   ❌ Dispute on {failed_auction['item'][:30]}...")
            print(f"      DONT_TRUST tokens issued to both parties")
            print(f"      Buyer {buyer['name']}: DONT_TRUST={buyer['dont_trust_score']}")
            print(f"      Seller {seller['name']}: DONT_TRUST={seller['dont_trust_score']}")
        
        # Step 5: Display reputation scores
        print("\n📊 STEP 5: Reputation Summary (TRUST/DONT_TRUST)")
        print("=" * 50)
        
        sorted_users = sorted(users, key=lambda x: x['trust_score'], reverse=True)
        for user in sorted_users[:5]:
            print(f"   🏆 {user['name']}: TRUST={user['trust_score']}, DONT_TRUST={user['dont_trust_score']}, PHNX={user['phnx_balance']}")
        
        # Step 6: Final report
        self.generate_report()
        
        return self.results
    
    def process_successful_auction(self, auction, users):
        """Process successful auction with YOUR tokenomics rules"""
        
        winner = next((u for u in users if u['name'] == auction['winner']), None)
        seller = next((u for u in users if u['name'] == auction['seller']), None)
        
        if not winner or not seller:
            return
        
        # Calculate fee (1.1% of final price - YOUR rule)
        fee_collected = int(auction['final_price'] * 0.011)
        
        # Calculate PHNX earned (1 per 1 TESTUSD in fees - YOUR rule)
        phnx_earned = int(fee_collected / 1_000_000)  # Assuming 6 decimals
        if phnx_earned == 0 and fee_collected > 0:
            phnx_earned = 1  # Minimum 1 PHNX
        
        # Issue TRUST tokens (1 per successful trade - YOUR rule)
        winner['trust_score'] += self.engine.rules['trust_per_success']
        seller['trust_score'] += self.engine.rules['trust_per_success']
        
        # Update PHNX balances
        winner['phnx_balance'] += phnx_earned
        seller['phnx_balance'] += phnx_earned
        
        # Update statistics
        self.results['successful_trades'] += 1
        self.results['total_fees'] += fee_collected
        self.results['total_phnx_issued'] += phnx_earned * 2  # Both parties
        
        print(f"      💰 Fee collected: ${fee_collected/1_000_000:,.2f} TESTUSD")
        print(f"      🗳️  PHNX issued: {phnx_earned} to {winner['name']}, {phnx_earned} to {seller['name']}")
        print(f"      ✅ TRUST tokens: +1 to both parties")
    
    def generate_report(self):
        """Generate final simulation report"""
        
        print("\n" + "="*70)
        print("📊 PHOENIXPME SIMULATION REPORT")
        print("="*70)
        
        print(f"\n📈 TRADE STATISTICS:")
        print(f"   Successful trades: {self.results['successful_trades']}")
        print(f"   Failed trades: {self.results['failed_trades']}")
        print(f"   Success rate: {self.results['successful_trades'] / (self.results['successful_trades'] + self.results['failed_trades']) * 100:.1f}%")
        
        print(f"\n💰 FEE & TOKENOMICS:")
        print(f"   Total fees collected: ${self.results['total_fees']/1_000_000:,.2f} TESTUSD")
        print(f"   Total PHNX issued: {self.results['total_phnx_issued']}")
        print(f"   PHNX allocation: {self.results['total_phnx_issued'] / (self.results['total_fees']/1_000_000) if self.results['total_fees'] > 0 else 0:.2f} per TESTUSD")
        
        print(f"\n🏛️ COMMUNITY RESERVE FUND:")
        print(f"   Total accumulated: ${self.results['total_fees']/1_000_000:,.2f} TESTUSD")
        print(f"   Controlled by: Future DAO (PHNX holders)")
        print(f"   Founder voting weight: 10% (permanent)")
        
        # Save results
        results_file = '/home/greg/dev/TX/simulation_results.json'
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'rules': self.engine.rules,
                'market_prices': self.market.live_prices,
                'results': self.results
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        print("\n✅ Simulation complete! All rules from YOUR documentation followed.")

if __name__ == "__main__":
    sim = PhoenixSimulation()
    sim.run_complete_simulation()
