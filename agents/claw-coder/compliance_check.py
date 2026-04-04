#!/usr/bin/env python3
"""Quick compliance check for PhoenixPME"""

import os
from pathlib import Path

docs_path = Path("/home/greg/dev/TXdocumentation")
project_path = Path("/home/greg/dev/TX")

print("\n" + "="*60)
print("🔍 PHOENIXPME COMPLIANCE CHECK")
print("="*60)

# Check what documentation exists
print("\n📖 TXdocumentation files:")
doc_count = 0
for md in docs_path.rglob("*.md"):
    if 'phoenixpme' not in str(md).lower():
        doc_count += 1
        if doc_count <= 5:
            print(f"   • {md.relative_to(docs_path)}")
if doc_count > 5:
    print(f"   ... and {doc_count - 5} more")
print(f"   Total: {doc_count} files")

# Check what project files exist
print("\n💻 TX Project auction files:")
auction_count = 0
for f in project_path.rglob("*"):
    if 'auction' in str(f).lower() and f.is_file():
        auction_count += 1
        if auction_count <= 10:
            print(f"   • {f.relative_to(project_path)}")
if auction_count > 10:
    print(f"   ... and {auction_count - 10} more")
print(f"   Total: {auction_count} files")

# Check for required components
print("\n📋 Required Components:")
components = {
    'escrow': False,
    'fee_accumulator': False,
    'reputation': False,
    'collateral': False,
    'test_addresses': False
}

# Scan for each component
for f in project_path.rglob("*"):
    if f.is_file():
        content_lower = open(f, 'r', errors='ignore').read().lower() if f.suffix in ['.rs', '.sh', '.js', '.ts'] else ''
        if 'escrow' in content_lower or 'escrow' in str(f).lower():
            components['escrow'] = True
        if 'fee' in content_lower and ('accumulator' in content_lower or 'collect' in content_lower):
            components['fee_accumulator'] = True
        if 'trust' in content_lower or 'reputation' in content_lower:
            components['reputation'] = True
        if 'collateral' in content_lower or 'percent' in content_lower:
            components['collateral'] = True
        if 'test_address' in str(f).lower() or 'generate' in str(f).lower():
            components['test_addresses'] = True

for comp, present in components.items():
    status = "✅" if present else "❌"
    print(f"   {status} {comp.replace('_', ' ').title()}")

# Summary
print("\n" + "="*60)
missing = [c for c, p in components.items() if not p]
if missing:
    print(f"\n⚠️ MISSING: {', '.join(missing)}")
else:
    print("\n✅ All components found!")

print("\n🏦 Test addresses needed:")
print("   txd keys add buyer_wallet --keyring-backend test")
print("   txd keys add seller_wallet --keyring-backend test")
print("   txd keys add escrow_wallet --keyring-backend test")
print("   txd keys add fee_collector --keyring-backend test")
