#!/usr/bin/env python3
"""TX Documentation Trainer - Load TX.org knowledge into clawpack"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
import hashlib

class TXTrainer:
    def __init__(self):
        self.db_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.knowledge_dir = Path(__file__).parent / "knowledge"
        self.knowledge_dir.mkdir(exist_ok=True)
        
    def create_knowledge_base(self):
        """Create knowledge base entries for TX ecosystem"""
        
        knowledge_entries = [
            # TX Platform Overview
            {
                "topic": "tx_platform_overview",
                "content": """
TX is a Layer-1 blockchain for Real-World Asset (RWA) tokenization.
Key features:
- Smart Tokens with built-in compliance (KYC/AML, whitelisting, clawbacks)
- WASM smart contracts
- IBC interoperability
- XRPL bridge for cross-chain transfers
- Built-in decentralized exchange (DEX)
""",
                "source": "https://tx.org",
                "category": "platform"
            },
            
            # Smart Tokens
            {
                "topic": "smart_tokens",
                "content": """
Smart Tokens on TX are native tokens with embedded compliance features:
- Freezing: Ability to freeze token transfers
- Whitelisting: Restrict transfers to approved addresses
- Clawbacks: Ability to recover tokens if needed
- Supply management: Mint/burn capabilities
- Permissioned transfers: Role-based access control
""",
                "source": "https://tx.org",
                "category": "technology"
            },
            
            # Asset Types
            {
                "topic": "asset_types",
                "content": """
TX supports tokenization of multiple asset types:
- Equities & ETFs (public, private, pre-IPO)
- Real Estate (commercial, residential, REITs)
- Funds (VC, private equity, hedge funds)
- Commodities (gold, oil, carbon credits)
- Intellectual Property & Royalties (music, patents, media)
- Structured Products & Debt Instruments
""",
                "source": "https://tx.org/issuers",
                "category": "assets"
            },
            
            # Network Details
            {
                "topic": "tx_networks",
                "content": """
TX Blockchain Networks:
- Mainnet: tx-mainnet-1, RPC: https://full-node.tx.org:26657
- Testnet: coreum-testnet-1, RPC: https://full-node.testnet-1.tx.dev:26657
- Devnet: tx-devnet-1, RPC: https://full-node.devnet-1.tx.dev:26657

Chain ID format: {network}-{version}
Denom: utestcore for testnet
Explorer: https://explorer.tx.org
""",
                "source": "https://docs.tx.org",
                "category": "network"
            },
            
            # XRPL Bridge
            {
                "topic": "xrpl_bridge",
                "content": """
TX-XRPL Bridge enables cross-chain asset transfers:
- Move assets between XRPL and TX blockchain
- Asset flow: Lock on source chain, mint on destination
- Fees: Transaction fees apply for bridge operations
- NFT Migration: Support for migrating NFTs between chains
- Relayer setup: Run a relayer for bridge operations
""",
                "source": "https://docs.tx.org/docs-bridge/overview",
                "category": "bridge"
            },
            
            # Developer Resources
            {
                "topic": "developer_resources",
                "content": """
TX Developer Resources:
- Developer Hub: https://tx.org/developers-hub
- Documentation: https://docs.tx.org
- GitHub: https://github.com/tokenize-x/tx-chain
- Bug Bounties: Find vulnerabilities, get rewards
- Dev Playground: Test WASM smart contracts
- Workshops: IBC, Coreum DEX, Smart Tokens
- Discord: Join developer community
""",
                "source": "https://tx.org/developers-hub",
                "category": "development"
            },
            
            # Compliance Features
            {
                "topic": "compliance",
                "content": """
TX Compliance Features:
- KYC/AML integration at protocol level
- Whitelisting for regulated assets
- Jurisdiction-based access control
- Audit trails for all transactions
- Regulatory reporting capabilities
- Freeze and clawback for compliance
""",
                "source": "https://tx.org",
                "category": "compliance"
            },
            
            # Issuer Features
            {
                "topic": "issuer_features",
                "content": """
TX Issuer Dashboard Features:
- Assisted onboarding process
- Issuer Admin Panel for asset management
- Compliance rule configuration
- Documentation management
- Investor segmentation by jurisdiction
- Accreditation verification
- Real-time distribution tracking
""",
                "source": "https://tx.org/issuers",
                "category": "issuers"
            },
            
            # TX Chain Technical
            {
                "topic": "tx_chain_technical",
                "content": """
TX Chain Technical Specifications:
- Built with Cosmos SDK
- Tendermint BFT consensus
- Bonded Proof of Stake (BPoS)
- WebAssembly (WASM) for smart contracts
- IBC protocol for interoperability
- Native DEX module
- Smart Token module for asset management
- Built with Go (95.9%) and Rust (4.0%)
""",
                "source": "https://github.com/tokenize-x/tx-chain",
                "category": "technical"
            },
            
            # Getting Started
            {
                "topic": "getting_started",
                "content": """
Getting Started with TX:
1. Clone repository: git clone https://github.com/tokenize-x/tx-chain
2. Setup dependencies: ./bin/tx-chain-builder setup
3. Build binaries: make build images
4. Start local chain: make znet-start
5. Interact via txd client
6. Deploy to testnet using faucet
Prerequisites: docker, g++, make, go 1.21+
""",
                "source": "https://github.com/tokenize-x/tx-chain",
                "category": "development"
            }
        ]
        
        return knowledge_entries
    
    def store_in_memory(self):
        """Store all TX knowledge into shared memory"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Create knowledge table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tx_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                content TEXT,
                source TEXT,
                category TEXT,
                stored_at TEXT,
                hash TEXT
            )
        """)
        
        entries = self.create_knowledge_base()
        stored_count = 0
        
        for entry in entries:
            # Create hash for deduplication
            hash_input = f"{entry['topic']}{entry['content']}"
            content_hash = hashlib.md5(hash_input.encode()).hexdigest()
            
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO tx_knowledge 
                    (topic, content, source, category, stored_at, hash)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    entry['topic'],
                    entry['content'],
                    entry['source'],
                    entry['category'],
                    datetime.now().isoformat(),
                    content_hash
                ))
                stored_count += 1
                print(f"✅ Stored: {entry['topic']}")
            except Exception as e:
                print(f"❌ Failed {entry['topic']}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"\n📚 Total TX knowledge entries stored: {stored_count}")
        return stored_count
    
    def save_to_files(self):
        """Save knowledge as individual markdown files"""
        entries = self.create_knowledge_base()
        
        for entry in entries:
            filename = self.knowledge_dir / f"{entry['topic']}.md"
            with open(filename, 'w') as f:
                f.write(f"# {entry['topic'].replace('_', ' ').title()}\n\n")
                f.write(f"**Source:** {entry['source']}\n")
                f.write(f"**Category:** {entry['category']}\n")
                f.write(f"**Stored:** {datetime.now().isoformat()}\n\n")
                f.write(entry['content'].strip())
                f.write("\n")
            print(f"📄 Saved: {filename.name}")
        
        print(f"\n📁 Knowledge saved to: {self.knowledge_dir}")
    
    def query_knowledge(self, topic=None, category=None):
        """Query stored TX knowledge"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        query = "SELECT topic, content, source, category FROM tx_knowledge"
        params = []
        
        if topic:
            query += " WHERE topic LIKE ?"
            params.append(f"%{topic}%")
        elif category:
            query += " WHERE category = ?"
            params.append(category)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def show_summary(self):
        """Show summary of stored knowledge"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM tx_knowledge 
            GROUP BY category 
            ORDER BY count DESC
        """)
        
        print("\n📚 TX Knowledge Summary")
        print("=" * 40)
        for category, count in cursor.fetchall():
            print(f"  {category}: {count} entries")
        
        cursor.execute("SELECT COUNT(*) FROM tx_knowledge")
        total = cursor.fetchone()[0]
        print(f"\n  Total entries: {total}")
        conn.close()

if __name__ == "__main__":
    trainer = TXTrainer()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "store":
            trainer.store_in_memory()
            trainer.save_to_files()
        elif sys.argv[1] == "save":
            trainer.save_to_files()
        elif sys.argv[1] == "summary":
            trainer.show_summary()
        elif sys.argv[1] == "query" and len(sys.argv) > 2:
            results = trainer.query_knowledge(topic=sys.argv[2])
            for topic, content, source, category in results:
                print(f"\n📖 {topic}")
                print(f"   Source: {source}")
                print(f"   Content: {content[:200]}...")
    else:
        trainer.store_in_memory()
        trainer.save_to_files()
        trainer.show_summary()
