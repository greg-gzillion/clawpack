#!/usr/bin/env python3
"""
TX Blockchain Agent - Trained on TX documentation to help build PhoenixPME
"""

import os
import json
import glob
import re
from pathlib import Path

class TXBlockchainAgent:
    def __init__(self):
        self.docs = []
        self.knowledge_base = {}
        self._load_tx_documentation()
        self._build_knowledge_index()
    
    def _load_tx_documentation(self):
        """Load all TX blockchain documentation"""
        docs_path = "/home/greg/dev/TXdocumentation"
        
        # Focus on core TX blockchain directories
        tx_dirs = [
            'help/', 'modules/', 'security/', 'regulatory/',
            'tutorials/', 'nodes/', 'ecosystem/', 'technical/',
            'architecture/', 'development/', 'ibc/', 'dex/'
        ]
        
        # Core TX files
        tx_files = [
            '01-introduction.md', '02-smart-contracts.md', '03-smart-tokens.md',
            '04-smart-tokens.md', '05-fee-model.md', '06-dex.md', '07-bridges.md',
            '08-roadmap.md', '09-technical.md', 'README.md', 'TX-Blockchain.md'
        ]
        
        all_md_files = glob.glob(f"{docs_path}/**/*.md", recursive=True)
        
        print(f"📂 Scanning {len(all_md_files)} files in TXdocumentation...")
        
        for file_path in all_md_files:
            rel_path = os.path.relpath(file_path, docs_path)
            
            # Skip PhoenixPME specific files
            if 'phoenixpme' in rel_path:
                continue
            
            # Check if it's TX blockchain documentation
            is_tx_doc = False
            for tx_dir in tx_dirs:
                if tx_dir in rel_path:
                    is_tx_doc = True
                    break
            
            for tx_file in tx_files:
                if rel_path.endswith(tx_file):
                    is_tx_doc = True
                    break
            
            if not is_tx_doc:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Skip very short files
                if len(content) < 200:
                    continue
                
                # Extract title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else Path(rel_path).stem.replace('-', ' ').title()
                
                # Determine topic category
                category = self._categorize_doc(rel_path, content)
                
                # Extract key concepts
                concepts = self._extract_concepts(content)
                
                self.docs.append({
                    'file': rel_path,
                    'title': title,
                    'category': category,
                    'content': content,
                    'concepts': concepts,
                    'size': len(content)
                })
                
                print(f"   ✓ {category}: {title}")
                
            except Exception as e:
                print(f"   ⚠️ Error: {rel_path} - {e}")
        
        print(f"\n✅ Loaded {len(self.docs)} TX blockchain documentation files")
    
    def _categorize_doc(self, filepath, content):
        """Categorize document by topic"""
        file_lower = filepath.lower()
        content_lower = content.lower()
        
        if 'smart token' in content_lower or 'smarttoken' in content_lower:
            return 'Smart Tokens'
        if 'smart contract' in content_lower or 'cosmwasm' in content_lower:
            return 'Smart Contracts'
        if 'validator' in file_lower or 'node' in file_lower:
            return 'Validators & Nodes'
        if 'dex' in file_lower or 'decentralized exchange' in content_lower:
            return 'DEX & Trading'
        if 'ibc' in file_lower or 'bridge' in content_lower:
            return 'IBC & Bridges'
        if 'fee' in file_lower or 'gas' in content_lower:
            return 'Fee Model'
        if 'governance' in content_lower:
            return 'Governance'
        if 'security' in file_lower or 'audit' in content_lower:
            return 'Security'
        if 'mica' in content_lower or 'regulatory' in file_lower:
            return 'Regulatory'
        if 'tutorial' in file_lower or 'guide' in file_lower:
            return 'Guides'
        
        return 'Core Concepts'
    
    def _extract_concepts(self, content):
        """Extract key concepts from document"""
        concepts = []
        
        # Look for bolded terms, code blocks, or technical terms
        bold_pattern = r'\*\*([^*]+)\*\*'
        code_pattern = r'`([^`]+)`'
        
        bold_matches = re.findall(bold_pattern, content)
        code_matches = re.findall(code_pattern, content)
        
        concepts.extend(bold_matches[:10])
        concepts.extend(code_matches[:10])
        
        # Add unique concepts
        return list(set(concepts))[:20]
    
    def _build_knowledge_index(self):
        """Build search index"""
        self.index = {}
        for doc in self.docs:
            # Index by keywords in title and content
            words = set(re.findall(r'\b[a-z]{3,}\b', doc['title'].lower() + ' ' + doc['content'].lower()[:1000]))
            for word in words:
                if word not in self.index:
                    self.index[word] = []
                self.index[word].append(doc)
    
    def search(self, query, limit=3):
        """Search documentation"""
        query_lower = query.lower()
        query_words = set(re.findall(r'\b[a-z]{3,}\b', query_lower))
        
        scored_docs = []
        for doc in self.docs:
            score = 0
            
            # Title match
            if query_lower in doc['title'].lower():
                score += 30
            
            # Category match
            if query_lower in doc['category'].lower():
                score += 20
            
            # Word matches in content
            content_lower = doc['content'].lower()
            for word in query_words:
                score += content_lower.count(word) * 2
            
            # Exact phrase match
            if query_lower in content_lower:
                score += 50
            
            if score > 0:
                scored_docs.append((score, doc))
        
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:limit]]
    
    def find_relevant_section(self, content, query):
        """Find the most relevant section for a query"""
        query_lower = query.lower()
        lines = content.split('\n')
        
        best_section = ""
        best_score = 0
        
        for i, line in enumerate(lines):
            if len(line.strip()) < 30:
                continue
            
            line_lower = line.lower()
            score = line_lower.count(query_lower)
            
            # Check if this line is part of a section
            if score > best_score:
                best_score = score
                # Get surrounding context
                start = max(0, i-2)
                end = min(len(lines), i+3)
                best_section = '\n'.join(lines[start:end])
        
        if best_section:
            return best_section
        
        # Return first meaningful paragraph
        for line in lines:
            if len(line.strip()) > 50 and not line.startswith('#'):
                return line.strip()
        
        return content[:500]
    
    def answer(self, question, context="phoenixpme"):
        """Answer questions in context of building PhoenixPME on TX"""
        
        # Search for relevant docs
        results = self.search(question, limit=2)
        
        if not results:
            return self._suggest_alternatives(question)
        
        best = results[0]
        
        # Find relevant section
        relevant = self.find_relevant_section(best['content'], question)
        
        # Clean up markdown
        relevant = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', relevant)
        relevant = re.sub(r'`([^`]+)`', r'\1', relevant)
        
        # Add PhoenixPME context if applicable
        context_note = ""
        if context == "phoenixpme" and "smart token" in best['category'].lower():
            context_note = "\n\n💡 PhoenixPME Context: This applies to your token implementation."
        elif context == "phoenixpme" and "dex" in best['category'].lower():
            context_note = "\n\n💡 PhoenixPME Context: Use this for your trading features."
        
        response = f"**{best['title']}**\n"
        response += f"📁 Category: {best['category']}\n"
        response += f"📄 Source: `{best['file']}`\n\n"
        response += relevant[:600]
        response += context_note
        
        if len(results) > 1:
            response += f"\n\n📚 Also relevant: {results[1]['title']}"
        
        return response
    
    def _suggest_alternatives(self, question):
        """Suggest related topics"""
        suggestions = {
            'token': ['Smart Tokens', 'Token issuance', 'Token freezing', 'Clawback'],
            'contract': ['Smart Contracts', 'CosmWasm', 'Contract deployment'],
            'trade': ['DEX', 'Order book', 'Liquidity pools'],
            'validator': ['Staking', 'Validator setup', 'Delegation'],
            'fee': ['Fee model', 'Gas prices', 'Transaction fees'],
            'bridge': ['IBC', 'Cross-chain', 'Asset transfer']
        }
        
        question_lower = question.lower()
        for key, topics in suggestions.items():
            if key in question_lower:
                return f"I found specific TX blockchain info about {key}. Try asking:\n  • " + "\n  • ".join(topics)
        
        return "I can help with: Smart Tokens, Smart Contracts, DEX, Validators, IBC Bridges, Fee Model, Governance, or Security. What would you like to know?"

def main():
    agent = TXBlockchainAgent()
    
    print("\n" + "="*70)
    print("🤖 Claw-Coder: TX Blockchain Agent")
    print("="*70)
    print("\nI'm trained on TX blockchain documentation to help you build PhoenixPME.")
    print("\n💡 What I can help with:")
    print("   • Smart Tokens (for your PME token implementation)")
    print("   • Smart Contracts (CosmWasm on TX)")
    print("   • DEX & Trading (for your exchange features)")
    print("   • Validators & Staking")
    print("   • IBC Bridges (cross-chain functionality)")
    print("   • Fee Model & Gas Optimization")
    print("   • Governance & Security")
    print("   • MiCA Compliance (for regulatory needs)")
    
    print("\n" + "="*70)
    print("Ask me anything about TX blockchain for your PhoenixPME project!")
    print("Type 'exit' to quit, 'topics' for suggestions")
    print("="*70)
    
    # Show some key docs
    print("\n📚 Key TX documentation loaded:")
    categories = {}
    for doc in agent.docs:
        categories[doc['category']] = categories.get(doc['category'], 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"   • {cat}: {count} documents")
    
    while True:
        try:
            question = input("\n💬 PhoenixPME dev > ").strip()
            
            if not question:
                continue
            
            if question.lower() == 'exit':
                print("\n👋 Ready to build on TX! Goodbye!")
                break
            
            if question.lower() == 'topics':
                print("\n📖 Try asking about:")
                print("   • How do I implement Smart Tokens for PhoenixPME?")
                print("   • What are the token freezing/clawback features?")
                print("   • How does the DEX work for trading PME tokens?")
                print("   • What are the validator requirements?")
                print("   • How do I integrate IBC for cross-chain?")
                print("   • What are the gas fees like?")
                print("   • Is TX MiCA compliant?")
                continue
            
            print("\n" + "="*60)
            answer = agent.answer(question, context="phoenixpme")
            print(answer)
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
