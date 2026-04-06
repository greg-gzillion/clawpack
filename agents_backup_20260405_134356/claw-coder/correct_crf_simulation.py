#!/usr/bin/env python3
"""
PhoenixPME CORRECT Simulation
Community Reserve Fund is populated ONLY by 1.1% auction fees
"""

import json
from datetime import datetime

class CorrectPhoenixSimulation:
    def __init__(self):
        # YOUR actual rules from README.md
        self.auction_fee_percent = 1.1
        self.collateral_percent = 10
        self.inspection_hours = 48
        
        # Community Reserve Fund - ONLY from auction fees
        self.community_reserve_fund = {
            'total_testusd': 0,
            'source': '1.1% auction fees only',
            'address': 'testcore1m5adn3k68tk4zqmujpnstmp9r933jafzu44tnv',
            'withdrawal_allowed': False,
            'controlled_by': 'Future DAO (PHNX holders)'
        }
        
        # Track all auctions
        self.auctions = []
        self.total_fees_collected = 0
        
    def create_auction(self, auction_id, item_name, final_price_usd):
        """Create and complete an auction, adding fee to CRF"""
        
        # Calculate fee (1.1% of final price)
        fee_usd = final_price_usd * (self.auction_fee_percent / 100)
        fee_testusd = fee_usd * 1_000_000  # 6 decimals
        
        # Add to Community Reserve Fund
        self.community_reserve_fund['total_testusd'] += fee_testusd
        
        # Track fee
        self.total_fees_collected += fee_usd
        
        # Record auction
        auction = {
            'id': auction_id,
            'item': item_name,
            'final_price_usd': final_price_usd,
            'fee_usd': fee_usd,
            'fee_testusd': fee_testusd,
            'crf_after': self.community_reserve_fund['total_testusd']
        }
        self.auctions.append(auction)
        
        return auction
    
    def run_simulation(self):
        print("\n" + "="*70)
        print("🏛️ PHOENIXPME COMMUNITY RESERVE FUND SIMULATION")
        print("="*70)
        print("\n📋 RULES (from your README.md):")
        print(f"   • Fee: {self.auction_fee_percent}% per successful auction")
        print(f"   • Destination: Community Reserve Fund")
        print(f"   • CRF Address: {self.community_reserve_fund['address']}")
        print(f"   • Withdrawal: ❌ NO INDIVIDUAL can withdraw")
        print(f"   • Control: Future DAO (PHNX holders)")
        
        print("\n" + "="*70)
        print("💰 COMMUNITY RESERVE FUND GROWTH")
        print("="*70)
        
        # Run 10 auctions with your actual prices
        auctions_data = [
            ("1 oz Gold American Eagle MS70", 5973),
            ("1/2 oz Gold Maple Leaf", 2295),
            ("1 oz Silver Eagle MS70", 100),
            ("10 oz Silver Bar", 787),
            ("1 oz Platinum Eagle", 2734),
            ("1 oz Palladium Maple Leaf", 1610),
            ("14k Gold Diamond Ring", 2006),
            ("St Gaudens $20 Gold", 7240),
            ("Morgan Silver Dollar MS64", 84),
            ("1/4 oz Gold Coin", 1200)
        ]
        
        for i, (item, price) in enumerate(auctions_data, 1):
            auction = self.create_auction(f"AUC{i:03d}", item, price)
            
            print(f"\n📌 {item}")
            print(f"   Final Price: ${price:,.2f}")
            print(f"   Fee ({self.auction_fee_percent}%): ${auction['fee_usd']:.2f}")
            print(f"   CRF Balance: ${self.community_reserve_fund['total_testusd']/1_000_000:,.2f} TESTUSD")
        
        # Final report
        print("\n" + "="*70)
        print("📊 FINAL REPORT")
        print("="*70)
        
        print(f"\n🏦 COMMUNITY RESERVE FUND:")
        print(f"   Total auctions: {len(self.auctions)}")
        print(f"   Total fees collected: ${self.total_fees_collected:,.2f}")
        print(f"   CRF Balance: {self.community_reserve_fund['total_testusd']:,} utestusd")
        print(f"   CRF Balance: ${self.community_reserve_fund['total_testusd']/1_000_000:,.2f} TESTUSD")
        print(f"   Source: {self.community_reserve_fund['source']}")
        print(f"   Address: {self.community_reserve_fund['address']}")
        print(f"   Withdrawal: {self.community_reserve_fund['withdrawal_allowed']}")
        print(f"   Control: {self.community_reserve_fund['controlled_by']}")
        
        # PHNX calculation (1 PHNX per 1 TESTUSD in fees)
        phnx_issued = self.total_fees_collected  # 1:1 ratio
        print(f"\n🗳️ PHNX GOVERNANCE:")
        print(f"   PHNX issued: {phnx_issued:.0f} tokens")
        print(f"   Based on: 1 PHNX per $1 TESTUSD in fees")
        print(f"   Founder weight: 10% (permanent)")
        print(f"   Community weight: 90%")
        
        # Save results
        results = {
            'community_reserve_fund': {
                'address': self.community_reserve_fund['address'],
                'balance_testusd': self.community_reserve_fund['total_testusd'],
                'balance_usd': self.community_reserve_fund['total_testusd'] / 1_000_000,
                'source': self.community_reserve_fund['source'],
                'withdrawal_allowed': self.community_reserve_fund['withdrawal_allowed']
            },
            'auctions': self.auctions,
            'total_fees_usd': self.total_fees_collected,
            'phnx_issued': phnx_issued,
            'rules': {
                'fee_percent': self.auction_fee_percent,
                'collateral_percent': self.collateral_percent,
                'inspection_hours': self.inspection_hours
            }
        }
        
        with open('/home/greg/dev/TX/crf_simulation.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: /home/greg/dev/TX/crf_simulation.json")
        print("\n✅ Simulation complete! CRF populated ONLY by auction fees.")

if __name__ == "__main__":
    sim = CorrectPhoenixSimulation()
    sim.run_simulation()
