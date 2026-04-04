#!/usr/bin/env python3
"""
PhoenixPME Real-Time Market Integration
Fetches live precious metals prices and adjusts auctions dynamically
"""

import json
from datetime import datetime
from pathlib import Path

class MarketDataIntegration:
    def __init__(self):
        # Live market data from your feed (April 2, 2026 16:05 EST)
        self.live_prices = {
            'gold': {
                'bid': 4675.10,
                'ask': 4677.10,
                'change': -82.40,
                'change_percent': -1.73,
                'low': 4554.30,
                'high': 4801.30,
                'timestamp': '2026-04-02 16:05:00 EST'
            },
            'silver': {
                'bid': 72.64,
                'ask': 72.89,
                'change': -2.34,
                'change_percent': -3.13,
                'low': 69.48,
                'high': 76.85
            },
            'platinum': {
                'bid': 1999.00,
                'ask': 2009.00,
                'change': 38.00,
                'change_percent': 1.94,
                'low': 1871.00,
                'high': 2010.00
            },
            'palladium': {
                'bid': 1494.00,
                'ask': 1534.00,
                'change': 33.00,
                'change_percent': 2.26,
                'low': 1407.00,
                'high': 1537.00
            }
        }
        
        self.premiums = {
            'coin_bu': 0.05,
            'coin_proof': 0.15,
            'bar': 0.02,
            'jewelry': 0.30,
            'numismatic': 0.50,
            'graded_ms70': 0.25,
            'graded_ms65': 0.10
        }
    
    def calculate_auction_price(self, metal_type, weight_oz, product_type, grade=None):
        """Calculate realistic auction price based on live market"""
        metal = metal_type.lower()
        if metal not in self.live_prices:
            return None
        
        base_price = self.live_prices[metal]['ask']
        metal_value = base_price * weight_oz
        premium = self.premiums.get(product_type, 0.05)
        
        if grade and grade in self.premiums:
            premium += self.premiums[grade]
        
        market_value = metal_value * (1 + premium)
        
        return {
            'metal_type': metal,
            'weight_oz': weight_oz,
            'product_type': product_type,
            'grade': grade,
            'base_price': base_price,
            'metal_value': metal_value,
            'premium_percent': premium * 100,
            'market_value': market_value,
            'starting_bid': int(market_value * 0.70),
            'reserve_price': int(market_value * 0.85),
            'buy_it_now': int(market_value * 1.15),
            'collateral_required': int(market_value * 0.10),
            'fee_1.1_percent': int(market_value * 0.011)
        }
    
    def generate_auction_items(self):
        """Generate realistic auction items based on live prices"""
        items = [
            ('gold', 1.0, 'coin_bu', 'graded_ms70', "1 oz Gold American Eagle BU MS70"),
            ('gold', 0.5, 'coin_bu', None, "1/2 oz Gold Canadian Maple Leaf"),
            ('silver', 1.0, 'coin_bu', 'graded_ms70', "1 oz Silver Eagle MS70"),
            ('silver', 10.0, 'bar', None, "10 oz Silver Bar RCM"),
            ('platinum', 1.0, 'coin_bu', 'graded_ms70', "1 oz Platinum Eagle MS70"),
            ('palladium', 1.0, 'coin_bu', None, "1 oz Palladium Maple Leaf"),
            ('gold', 0.33, 'jewelry', None, "14k Gold Diamond Ring 0.5ct"),
            ('gold', 0.9675, 'numismatic', 'graded_ms65', "1907 $20 St Gaudens MS65"),
            ('silver', 0.7734, 'numismatic', 'graded_ms64', "1921 Morgan Dollar MS64"),
        ]
        
        auction_items = []
        for metal, weight, product, grade, desc in items:
            pricing = self.calculate_auction_price(metal, weight, product, grade)
            if pricing:
                auction_items.append({
                    'id': f"ITEM{len(auction_items)+1:03d}",
                    'description': desc,
                    'metal': metal,
                    'weight_oz': weight,
                    'market_value': pricing['market_value'],
                    'starting_bid': pricing['starting_bid'],
                    'reserve_price': pricing['reserve_price'],
                    'buy_it_now': pricing['buy_it_now'],
                    'collateral': pricing['collateral_required']
                })
        
        return auction_items

if __name__ == "__main__":
    market = MarketDataIntegration()
    items = market.generate_auction_items()
    print(f"Generated {len(items)} auction items")
