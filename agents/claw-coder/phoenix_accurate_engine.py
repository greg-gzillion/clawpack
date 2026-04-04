#!/usr/bin/env python3
"""
PhoenixPME Accurate Auction Engine - Based ONLY on your documentation
"""

import json
from datetime import datetime, timedelta

class PhoenixAccurateEngine:
    def __init__(self):
        self.rules = {
            'collateral_percent': 10,
            'fee_percent': 1.1,
            'inspection_hours': 48,
            'phnx_per_usd': 1,
            'trust_per_success': 1,
            'dont_trust_per_failure': 1
        }
        self.users = []
        self.auctions = []
    
    def create_users(self, count=10):
        """Create users with reputation tracking"""
        for i in range(1, count + 1):
            self.users.append({
                'id': i,
                'name': f"user_{i:02d}",
                'phnx_balance': 0,
                'trust_score': 0,
                'dont_trust_score': 0,
                'total_fees_paid': 0
            })
        return self.users
    
    def create_auction(self, seller, item_name, market_value):
        """Create auction using YOUR rules"""
        collateral_amount = int(market_value * 0.1)
        fee_amount = int(market_value * 0.011)
        
        auction = {
            'id': f"AUC{len(self.auctions)+1:03d}",
            'seller': seller['name'],
            'item': item_name,
            'market_value': market_value,
            'starting_bid': int(market_value * 0.7),
            'reserve_price': int(market_value * 0.85),
            'buy_it_now': int(market_value * 1.15),
            'collateral_amount': collateral_amount,
            'fee_amount': fee_amount,
            'status': 'active',
            'bids': []
        }
        self.auctions.append(auction)
        return auction

