#!/usr/bin/env python3
"""
PhoenixPME Multi-Currency Payment Gateway
- Accepts BTC, ETH, XRP on testnet
- INSTANTLY converts to TESTUSD
- All collateral and settlements in TESTUSD only
"""

import json
from datetime import datetime

class MultiCurrencyPayment:
    def __init__(self):
        # Testnet conversion rates (simulated - would use oracle in production)
        self.conversion_rates = {
            'BTC': 65000,      # 1 BTC = $65,000 USD
            'ETH': 3200,       # 1 ETH = $3,200 USD
            'XRP': 0.55,       # 1 XRP = $0.55 USD
            'SOL': 180,        # 1 SOL = $180 USD
        }
        
        # Settlement is ALWAYS in TESTUSD
        self.settlement_currency = 'TESTUSD'
        self.testusd_decimals = 1_000_000
        
        # Track all conversions
        self.conversions = []
        
    def convert_to_testusd(self, currency, amount):
        """Convert any currency to TESTUSD instantly"""
        
        if currency not in self.conversion_rates:
            return None, f"Unsupported currency: {currency}"
        
        # Step 1: Calculate USD value
        usd_value = amount * self.conversion_rates[currency]
        
        # Step 2: Convert to TESTUSD (1:1 with USD)
        testusd_amount = usd_value
        testusd_raw = int(testusd_amount * self.testusd_decimals)
        
        # Record conversion
        conversion = {
            'timestamp': datetime.now().isoformat(),
            'original_currency': currency,
            'original_amount': amount,
            'exchange_rate': self.conversion_rates[currency],
            'usd_value': usd_value,
            'settlement_currency': self.settlement_currency,
            'settlement_amount': testusd_amount,
            'settlement_raw': testusd_raw
        }
        self.conversions.append(conversion)
        
        return conversion, None
    
    def deposit_collateral(self, user, auction_id, currency, amount):
        """User deposits collateral in any currency"""
        
        print(f"\n💰 Collateral Deposit")
        print(f"   User: {user}")
        print(f"   Auction: {auction_id}")
        print(f"   Deposit: {amount} {currency}")
        
        # Convert to TESTUSD instantly
        conversion, error = self.convert_to_testusd(currency, amount)
        
        if error:
            print(f"   ❌ {error}")
            return None
        
        print(f"   ✅ Converted to: {conversion['settlement_amount']:,.2f} TESTUSD")
        print(f"   🔒 Collateral locked: {conversion['settlement_raw']:,} utestusd")
        print(f"   📊 Rate: 1 {currency} = ${conversion['exchange_rate']:,.2f}")
        
        return conversion
    
    def show_testnet_setup(self):
        """Show how to get testnet tokens"""
        
        print("\n" + "="*70)
        print("🔧 TESTNET SETUP - GET TEST TOKENS")
        print("="*70)
        
        faucets = {
            'BTC': 'https://bitcoin-testnet-faucet.mempool.co',
            'ETH': 'https://faucet.sepolia.dev',
            'XRP': 'https://xrpl.org/faucet.html',
            'TESTUSD': 'https://faucet.testnet.tx.dev'
        }
        
        for currency, faucet in faucets.items():
            print(f"\n{currency}:")
            print(f"   Faucet: {faucet}")
            if currency == 'TESTUSD':
                print(f"   Denom: utestusd (6 decimals)")
                print(f"   Address format: testcore1...")
            else:
                print(f"   Will be instantly converted to TESTUSD upon deposit")

def main():
    gateway = MultiCurrencyPayment()
    
    print("\n" + "="*70)
    print("💱 PHOENIXPME MULTI-CURRENCY PAYMENT GATEWAY")
    print("="*70)
    print("\n📋 HOW IT WORKS:")
    print("   1. User deposits BTC/ETH/XRP (testnet)")
    print("   2. Gateway instantly converts to TESTUSD")
    print("   3. All collateral and settlements in TESTUSD")
    print("   4. No price fluctuation risk")
    
    # Show testnet setup
    gateway.show_testnet_setup()
    
    # Simulate deposits
    print("\n" + "="*70)
    print("💸 SIMULATED DEPOSITS")
    print("="*70)
    
    deposits = [
        ("alice", "AUC001", "BTC", 0.01),
        ("bob", "AUC002", "ETH", 0.5),
        ("carol", "AUC003", "XRP", 1000),
    ]
    
    for user, auction, currency, amount in deposits:
        gateway.deposit_collateral(user, auction, currency, amount)
    
    # Save conversion record
    with open('/home/greg/dev/TX/multi_currency_conversions.json', 'w') as f:
        json.dump(gateway.conversions, f, indent=2)
    
    print("\n✅ Multi-currency gateway ready!")
    print("📁 Conversions saved to: /home/greg/dev/TX/multi_currency_conversions.json")

if __name__ == "__main__":
    main()
