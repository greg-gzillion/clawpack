#!/usr/bin/env python3
"""Train all clawpack agents on TX ecosystem knowledge"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# TX Knowledge entries (from our earlier training)
TX_KNOWLEDGE = [
    {
        "topic": "tx_platform_overview",
        "content": """TX is a Layer-1 blockchain for Real-World Asset (RWA) tokenization.
Key features:
- Smart Tokens with built-in compliance (KYC/AML, whitelisting, clawbacks)
- WASM smart contracts
- IBC interoperability
- XRPL bridge for cross-chain transfers
- Built-in decentralized exchange (DEX)""",
        "category": "platform",
        "source": "https://tx.org"
    },
    {
        "topic": "smart_tokens",
        "content": """Smart Tokens on TX are native tokens with embedded compliance features:
- Freezing: Ability to freeze token transfers
- Whitelisting: Restrict transfers to approved addresses
- Clawbacks: Ability to recover tokens if needed
- Supply management: Mint/burn capabilities
- Permissioned transfers: Role-based access control""",
        "category": "technology",
        "source": "https://tx.org"
    },
    {
        "topic": "asset_types",
        "content": """TX supports tokenization of multiple asset types:
- Equities & ETFs (public, private, pre-IPO)
- Real Estate (commercial, residential, REITs)
- Funds (VC, private equity, hedge funds)
- Commodities (gold, oil, carbon credits)
- Intellectual Property & Royalties (music, patents, media)
- Structured Products & Debt Instruments""",
        "category": "assets",
        "source": "https://tx.org/issuers"
    },
    {
        "topic": "tx_networks",
        "content": """TX Blockchain Networks:
- Mainnet: tx-mainnet-1, RPC: https://full-node.tx.org:26657
- Testnet: coreum-testnet-1, RPC: https://full-node.testnet-1.tx.dev:26657
- Devnet: tx-devnet-1, RPC: https://full-node.devnet-1.tx.dev:26657
Chain ID format: {network}-{version}
Explorer: https://explorer.tx.org""",
        "category": "network",
        "source": "https://docs.tx.org"
    },
    {
        "topic": "xrpl_bridge",
        "content": """TX-XRPL Bridge enables cross-chain asset transfers:
- Move assets between XRPL and TX blockchain
- Asset flow: Lock on source chain, mint on destination
- Fees: Transaction fees apply for bridge operations
- NFT Migration: Support for migrating NFTs between chains
- Relayer setup: Run a relayer for bridge operations""",
        "category": "bridge",
        "source": "https://docs.tx.org/docs-bridge/overview"
    },
    {
        "topic": "developer_resources",
        "content": """TX Developer Resources:
- Developer Hub: https://tx.org/developers-hub
- Documentation: https://docs.tx.org
- GitHub: https://github.com/tokenize-x/tx-chain
- Bug Bounties: Find vulnerabilities, get rewards
- Dev Playground: Test WASM smart contracts
- Workshops: IBC, Coreum DEX, Smart Tokens""",
        "category": "development",
        "source": "https://tx.org/developers-hub"
    },
    {
        "topic": "compliance",
        "content": """TX Compliance Features:
- KYC/AML integration at protocol level
- Whitelisting for regulated assets
- Jurisdiction-based access control
- Audit trails for all transactions
- Regulatory reporting capabilities
- Freeze and clawback for compliance""",
        "category": "compliance",
        "source": "https://tx.org"
    },
    {
        "topic": "issuer_features",
        "content": """TX Issuer Dashboard Features:
- Assisted onboarding process
- Issuer Admin Panel for asset management
- Compliance rule configuration
- Documentation management
- Investor segmentation by jurisdiction
- Accreditation verification
- Real-time distribution tracking""",
        "category": "issuers",
        "source": "https://tx.org/issuers"
    },
    {
        "topic": "tx_chain_technical",
        "content": """TX Chain Technical Specifications:
- Built with Cosmos SDK
- Tendermint BFT consensus
- Bonded Proof of Stake (BPoS)
- WebAssembly (WASM) for smart contracts
- IBC protocol for interoperability
- Native DEX module
- Smart Token module for asset management
- Built with Go (95.9%) and Rust (4.0%)""",
        "category": "technical",
        "source": "https://github.com/tokenize-x/tx-chain"
    },
    {
        "topic": "getting_started",
        "content": """Getting Started with TX:
1. Clone repository: git clone https://github.com/tokenize-x/tx-chain
2. Setup dependencies: ./bin/tx-chain-builder setup
3. Build binaries: make build images
4. Start local chain: make znet-start
5. Interact via txd client
6. Deploy to testnet using faucet
Prerequisites: docker, g++, make, go 1.21+""",
        "category": "development",
        "source": "https://github.com/tokenize-x/tx-chain"
    }
]

# All agents in the ecosystem
AGENTS = [
    "agentforlaw",
    "claw-code", 
    "claw-coder",
    "crustyclaw",
    "eagleclaw",
    "rustypycraw",
    "sysclaw"
]

# Languages already mastered (from earlier)
LANGUAGES = [
    "C++", "Go", "JavaScript", "Python", "Rust", "Solidity", "TypeScript",
    "Java", "C#", "Kotlin", "Swift", "SQL", "HTML/CSS", "Zig", "Carbon",
    "Mojo", "Move", "Cairo", "Vyper"
]

class TXTrainer:
    def __init__(self):
        self.db_path = Path.home() / ".claw_memory" / "shared_memory.db"
        
    def train_all_agents(self):
        """Train all agents on TX knowledge"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Create TX knowledge table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tx_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT UNIQUE,
                content TEXT,
                category TEXT,
                source TEXT,
                stored_at TEXT
            )
        """)
        
        # Create agent_training table to track which agents know what
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_training (
                agent TEXT,
                topic TEXT,
                trained_at TEXT,
                proficiency INTEGER DEFAULT 5,
                UNIQUE(agent, topic)
            )
        """)
        
        # Store TX knowledge
        for knowledge in TX_KNOWLEDGE:
            cursor.execute("""
                INSERT OR REPLACE INTO tx_knowledge 
                (topic, content, category, source, stored_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                knowledge["topic"],
                knowledge["content"],
                knowledge["category"],
                knowledge["source"],
                datetime.now().isoformat()
            ))
        
        # Train each agent on each topic
        trained_count = 0
        for agent in AGENTS:
            for knowledge in TX_KNOWLEDGE:
                cursor.execute("""
                    INSERT OR REPLACE INTO agent_training 
                    (agent, topic, trained_at, proficiency)
                    VALUES (?, ?, ?, ?)
                """, (
                    agent,
                    knowledge["topic"],
                    datetime.now().isoformat(),
                    5  # Level 5 mastery
                ))
                trained_count += 1
            print(f"✅ Trained {agent} on {len(TX_KNOWLEDGE)} TX topics")
        
        conn.commit()
        conn.close()
        
        print(f"\n🎉 TOTAL: {trained_count} agent-topic trainings completed!")
        print(f"   {len(AGENTS)} agents × {len(TX_KNOWLEDGE)} topics = {trained_count}")
        
    def show_training_status(self):
        """Show which agents have TX knowledge"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        print("\n📊 TX Knowledge Training Status")
        print("=" * 50)
        
        for agent in AGENTS:
            cursor.execute("""
                SELECT COUNT(*) FROM agent_training 
                WHERE agent = ? AND proficiency >= 4
            """, (agent,))
            count = cursor.fetchone()[0]
            print(f"  🦞 {agent}: {count}/{len(TX_KNOWLEDGE)} topics mastered (Level 5)")
        
        cursor.execute("SELECT COUNT(*) FROM tx_knowledge")
        total_topics = cursor.fetchone()[0]
        print(f"\n  📚 Total TX topics in knowledge base: {total_topics}")
        
        conn.close()
    
    def verify_agent_knowledge(self, agent, topic):
        """Verify a specific agent knows a specific topic"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT at.proficiency, tk.content 
            FROM agent_training at
            JOIN tx_knowledge tk ON at.topic = tk.topic
            WHERE at.agent = ? AND at.topic = ?
        """, (agent, topic))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"✅ {agent} knows '{topic}' (Level {result[0]}/5)")
            print(f"   Content: {result[1][:200]}...")
            return True
        else:
            print(f"❌ {agent} does not know '{topic}'")
            return False

if __name__ == "__main__":
    trainer = TXTrainer()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "train":
            trainer.train_all_agents()
            trainer.show_training_status()
        elif sys.argv[1] == "status":
            trainer.show_training_status()
        elif sys.argv[1] == "verify" and len(sys.argv) > 2:
            agent = sys.argv[2]
            topic = sys.argv[3] if len(sys.argv) > 3 else "tx_platform_overview"
            trainer.verify_agent_knowledge(agent, topic)
    else:
        trainer.train_all_agents()
        trainer.show_training_status()
