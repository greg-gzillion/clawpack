#!/usr/bin/env python3
"""
PhoenixPME Auction Simulator - Fully Automated Testing
Creates users, funds wallets, runs auctions, reports results
"""

import subprocess
import json
import time
import random
from pathlib import Path

class AuctionSimulator:
    def __init__(self):
        self.project_path = Path("/home/greg/dev/TX")
        self.users = []
        self.auctions = []
        self.results = []
        
    def create_users(self, count=10):
        """Create user wallets efficiently"""
        print(f"\n👥 Creating {count} user wallets...")
        
        for i in range(1, count + 1):
            name = f"user_{i:02d}"
            
            # Create wallet quietly
            result = subprocess.run(
                f'txd keys add {name} --keyring-backend test --chain-id coreum-testnet-1 2>/dev/null',
                shell=True, capture_output=True, text=True
            )
            
            # Extract address from output
            for line in result.stdout.split('\n'):
                if 'address:' in line:
                    addr = line.split('address:')[1].strip()
                    self.users.append({
                        'id': i,
                        'name': name,
                        'address': addr,
                        'balance': 0,
                        'escrow': None
                    })
                    print(f"  ✅ {name}: {addr[:20]}...")
                    break
        
        # Create escrow for each user
        for user in self.users:
            escrow_name = f"{user['name']}_escrow"
            result = subprocess.run(
                f'txd keys add {escrow_name} --keyring-backend test --chain-id coreum-testnet-1 2>/dev/null',
                shell=True, capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n'):
                if 'address:' in line:
                    user['escrow'] = line.split('address:')[1].strip()
                    break
        
        # Save to file
        with open(self.project_path / 'simulation_users.json', 'w') as f:
            json.dump(self.users, f, indent=2)
        
        print(f"\n✅ Created {len(self.users)} users with escrow accounts")
        return self.users
    
    def fund_wallets(self, amount="10000000utestcore"):
        """Fund all wallets from faucet"""
        print(f"\n💰 Funding wallets with {amount}...")
        
        for user in self.users:
            # Fund main wallet
            cmd = f'curl -s -X POST https://faucet.testnet-1.coreum.dev/claim -H "Content-Type: application/json" -d \'{{"address": "{user["address"]}"}}\''
            subprocess.run(cmd, shell=True, capture_output=True)
            
            # Fund escrow wallet
            cmd = f'curl -s -X POST https://faucet.testnet-1.coreum.dev/claim -H "Content-Type: application/json" -d \'{{"address": "{user["escrow"]}"}}\''
            subprocess.run(cmd, shell=True, capture_output=True)
            
            print(f"  ✅ {user['name']} funded")
            time.sleep(0.5)  # Avoid rate limiting
        
        print(f"\n✅ All wallets funded")
        return True
    
    def create_auction_items(self):
        """Create diverse auction items"""
        print(f"\n🏺 Creating auction items...")
        
        items = [
            {"name": "1oz Gold Eagle", "category": "gold", "min_bid": 2100, "reserve": 2150, "duration": 7},
            {"name": "10oz Silver Bar", "category": "silver", "min_bid": 280, "reserve": 290, "duration": 5},
            {"name": "1oz Platinum Maple", "category": "platinum", "min_bid": 950, "reserve": 980, "duration": 10},
            {"name": "Morgan Silver Dollar MS65", "category": "numismatic", "min_bid": 450, "reserve": 475, "duration": 14},
            {"name": "14k Diamond Ring 1.5ct", "category": "jewelry", "min_bid": 2800, "reserve": 2900, "duration": 7},
            {"name": "100oz Gold Bar", "category": "gold", "min_bid": 210000, "reserve": 215000, "duration": 30},
            {"name": "Rolex Daytona", "category": "luxury", "min_bid": 28000, "reserve": 29000, "duration": 7},
            {"name": "1/2oz Gold Kangaroo", "category": "gold", "min_bid": 1050, "reserve": 1080, "duration": 5},
            {"name": "Sterling Flatware Set", "category": "silver", "min_bid": 1200, "reserve": 1300, "duration": 10},
            {"name": "St Gaudens Double Eagle", "category": "numismatic", "min_bid": 2200, "reserve": 2350, "duration": 14},
        ]
        
        for i, item in enumerate(items, 1):
            seller = random.choice(self.users)
            self.auctions.append({
                'id': f"AUC{i:03d}",
                'seller': seller['name'],
                'seller_addr': seller['address'],
                'item': item['name'],
                'category': item['category'],
                'min_bid': item['min_bid'],
                'reserve': item['reserve'],
                'duration_days': item['duration'],
                'collateral': int(item['min_bid'] * 0.1),  # 10% collateral
                'status': 'pending',
                'bids': []
            })
            print(f"  ✅ {item['name']} - Seller: {seller['name']}")
        
        with open(self.project_path / 'simulation_auctions.json', 'w') as f:
            json.dump(self.auctions, f, indent=2)
        
        return self.auctions
    
    def simulate_bidding(self):
        """Run automated bidding simulation"""
        print(f"\n💸 Simulating bidding on all auctions...")
        
        for auction in self.auctions:
            print(f"\n  🏺 {auction['item']} (Starting: ${auction['min_bid']})")
            
            current_bid = auction['min_bid']
            winner = None
            bid_count = 0
            
            # Random number of bids (3-15)
            num_bids = random.randint(3, 15)
            
            for bid_round in range(num_bids):
                # Pick random bidder (not seller)
                bidders = [u for u in self.users if u['name'] != auction['seller']]
                if not bidders:
                    break
                    
                bidder = random.choice(bidders)
                
                # Calculate bid increment (5-25%)
                increment_pct = random.uniform(0.05, 0.25)
                increment = int(current_bid * increment_pct)
                if increment < 10:
                    increment = 10
                
                new_bid = current_bid + increment
                bid_count += 1
                
                # Chance to stop bidding decreases as price increases
                stop_chance = min(0.8, (new_bid / auction['reserve']) * 0.3)
                
                if random.random() > stop_chance or new_bid < auction['reserve']:
                    current_bid = new_bid
                    winner = bidder
                    print(f"     Round {bid_count}: {bidder['name']} bids ${current_bid:,}")
                    
                    # Record bid
                    auction['bids'].append({
                        'round': bid_count,
                        'bidder': bidder['name'],
                        'amount': current_bid,
                        'collateral': int(current_bid * 0.1)
                    })
                else:
                    print(f"     Round {bid_count}: No further bids")
                    break
                
                time.sleep(0.1)  # Simulate thinking time
            
            # Determine outcome
            if current_bid >= auction['reserve']:
                auction['status'] = 'sold'
                auction['final_price'] = current_bid
                auction['winner'] = winner['name'] if winner else 'none'
                print(f"     ✅ SOLD! Final: ${current_bid:,} to {winner['name'] if winner else 'none'}")
            else:
                auction['status'] = 'unsold'
                auction['final_price'] = current_bid
                print(f"     ❌ UNSOLD - Reserve not met (${auction['reserve']})")
        
        # Save results
        with open(self.project_path / 'simulation_results.json', 'w') as f:
            json.dump(self.auctions, f, indent=2)
        
        return self.auctions
    
    def generate_report(self):
        """Create comprehensive test report"""
        print(f"\n📊 SIMULATION REPORT")
        print("=" * 50)
        
        total_auctions = len(self.auctions)
        sold = len([a for a in self.auctions if a['status'] == 'sold'])
        unsold = len([a for a in self.auctions if a['status'] == 'unsold'])
        total_value = sum([a.get('final_price', 0) for a in self.auctions])
        total_collateral = sum([a.get('collateral', 0) for a in self.auctions])
        
        print(f"\n📈 Summary:")
        print(f"  Total Auctions: {total_auctions}")
        print(f"  Sold: {sold}")
        print(f"  Unsold: {unsold}")
        print(f"  Total Value: ${total_value:,}")
        print(f"  Total Collateral Locked: ${total_collateral:,}")
        
        print(f"\n🏆 Top Performers:")
        sorted_auctions = sorted(self.auctions, key=lambda x: x.get('final_price', 0), reverse=True)
        for a in sorted_auctions[:3]:
            if a['status'] == 'sold':
                print(f"  • {a['item']}: ${a['final_price']:,} (Winner: {a.get('winner', 'none')})")
        
        print(f"\n📁 Results saved to: simulation_results.json")
        
        # Generate test addresses file
        with open(self.project_path / 'test_addresses.json', 'w') as f:
            json.dump({
                'users': self.users,
                'auctions': self.auctions,
                'summary': {
                    'total_users': len(self.users),
                    'total_auctions': total_auctions,
                    'sold': sold,
                    'unsold': unsold,
                    'total_value': total_value
                }
            }, f, indent=2)
        
        return self.auctions
    
    def run_full_simulation(self):
        """Run complete simulation"""
        print("\n" + "="*60)
        print("🏛️ PHOENIXPME FULL AUCTION SIMULATION")
        print("="*60)
        
        self.create_users(10)
        self.fund_wallets()
        self.create_auction_items()
        self.simulate_bidding()
        self.generate_report()
        
        print("\n✅ Simulation complete!")
        print("\n📋 Next Steps:")
        print("  1. Review simulation_results.json")
        print("  2. Run: txd query bank balances testcore1... to check balances")
        print("  3. Deploy smart contracts to testnet")
        
        return True

if __name__ == "__main__":
    sim = AuctionSimulator()
    sim.run_full_simulation()
