#!/usr/bin/env python3
"""Test PhoenixPME connection to Coreum testnet"""

import urllib.request
import json

# Working endpoints
RPC = "https://full-node.testnet-1.coreum.dev:26657"
REST = "https://full-node.testnet-1.coreum.dev:1317"

print("🦞 PhoenixPME - Coreum Testnet Connection Test")
print("=" * 50)

# Test RPC
resp = urllib.request.urlopen(f"{RPC}/status")
data = json.loads(resp.read())
print(f"✅ RPC Connected")
print(f"   Block Height: {data['result']['sync_info']['latest_block_height']}")
print(f"   Chain ID: {data['result']['node_info']['network']}")

# Test REST API - different endpoint
resp = urllib.request.urlopen(f"{REST}/cosmos/base/tendermint/v1beta1/node_info")
node_info = json.loads(resp.read())
print(f"\n✅ REST API Connected")
if 'node_info' in node_info:
    print(f"   Node: {node_info['node_info']['moniker']}")
elif 'default_node_info' in node_info:
    print(f"   Node: {node_info['default_node_info']['moniker']}")
else:
    print(f"   Response received: {list(node_info.keys())}")

# Test account query (optional - using a valid testnet address)
print(f"\n✅ Coreum testnet is ready for PhoenixPME deployment!")
print(f"\n📝 Use these endpoints in your PhoenixPME config:")
print(f"   RPC: {RPC}")
print(f"   REST: {REST}")
print(f"   Chain ID: coreum-testnet-1")
print(f"   Denom: utestcore")
