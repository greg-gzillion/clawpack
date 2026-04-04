#!/usr/bin/env python3
"""TX Agent - Monitor and interact with TX blockchain"""

import subprocess
import json
from pathlib import Path

class TXAgent:
    def __init__(self):
        self.testnet_rpc = "https://full-node.testnet-1.coreum.dev:26657"
        self.chain_id = "coreum-testnet-1"
        
    def get_status(self):
        """Get TX blockchain status"""
        try:
            import urllib.request
            response = urllib.request.urlopen(f"{self.testnet_rpc}/status", timeout=10)
            data = json.loads(response.read())
            return {
                "network": "TX Testnet",
                "chain_id": self.chain_id,
                "latest_block": data["result"]["sync_info"]["latest_block_height"],
                "catching_up": data["result"]["sync_info"]["catching_up"]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_validators(self):
        """Get validator set"""
        try:
            import urllib.request
            response = urllib.request.urlopen(f"{self.testnet_rpc}/validators?page=1&per_page=10", timeout=10)
            data = json.loads(response.read())
            return data["result"]["validators"]
        except Exception as e:
            return []
    
    def check_contract(self, contract_address):
        """Check smart contract status"""
        # This would use txd CLI to query contract
        cmd = f"txd query wasm contract {contract_address} --chain-id={self.chain_id} --node={self.testnet_rpc}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else None

if __name__ == "__main__":
    agent = TXAgent()
    print(json.dumps(agent.get_status(), indent=2))
