#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/greg/dev/claw-coder')

from market_data_integration import MarketDataIntegration
from phoenix_accurate_engine import PhoenixAccurateEngine
import json

print("\n" + "="*70)
print("🏛️ PHOENIXPME COMPLETE AUCTION SYSTEM")
print("="*70)

# Load market data
print("\n📊 Loading live precious metals prices...")
market = MarketDataIntegration()
auction_items = market.generate_auction_items()

print(f"   Gold: ${market.live_prices['gold']['ask']:,.2f}")
print(f"   Silver: ${market.live_prices['silver']['ask']:,.2f}")
print(f"   Platinum: ${market.live_prices['platinum']['ask']:,.2f}")

# Initialize engine
print("\n⚙️ Initializing auction engine...")
engine = PhoenixAccurateEngine()
engine.create_users(10)

# Create auctions
print("\n🏺 Creating auctions with real-time pricing...")
for i, item in enumerate(auction_items[:8]):
    seller = engine.users[i % len(engine.users)]
    auction = engine.create_auction(seller, item['description'], item['market_value'])
    print(f"   {item['description'][:40]}... - ${item['market_value']:,.2f}")

# Save configuration
config = {
    'market_prices': market.live_prices,
    'rules': engine.rules,
    'users': len(engine.users),
    'auctions': len(engine.auctions)
}

with open('/home/greg/dev/TX/phoenix_config.json', 'w') as f:
    json.dump(config, f, indent=2)

print("\n" + "="*50)
print("✅ SYSTEM READY")
print("="*50)
print(f"   Users: {len(engine.users)}")
print(f"   Auctions: {len(engine.auctions)}")
print(f"   Collateral: {engine.rules['collateral_percent']}% both parties")
print(f"   Fee: {engine.rules['fee_percent']}%")
print(f"\n📁 Config saved to: /home/greg/dev/TX/phoenix_config.json")
