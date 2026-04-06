#!/usr/bin/env python3
"""
TX Focused Agent - Only uses high-quality TX documentation
Excludes generic files and prioritizes technical accuracy
"""

import json
import os
import glob
import re

class TXFocusedAgent:
    def __init__(self):
        self.docs = []
        self._load_tx_documentation()
    
    def _is_valid_tx_doc(self, filepath, content):
        """Only include genuine TX blockchain documentation"""
        
        # Must-have TX indicators in content
        tx_indicators = [
            'tx blockchain', 'tx token', '$tx', 'txd',
            'coreum', 'sologenic', 'smart token', 'smart contract',
            'bonded proof of stake', 'bpos', 'ibc', 'dex',
            'fee model', 'validator', 'delegation', 'governance',
            'wasm', 'cosmwasm', 'miCA', 'kraken'
        ]
        
        # Check content for TX indicators
        content_lower = content.lower()
        has_tx_content = any(indicator in content_lower for indicator in tx_indicators)
        
        # Exclude obviously non-TX files
        exclude_patterns = [
            'privacy_policy', 'terms_of_service', 'code_of_conduct',
            'contributing', 'security.md', 'depoy_log', 'contract-readme',
            'phoenixpme', 'aed/', 'alert/', 'kyc/', 'wallet/',
            'email-', 'notification/', 'order/', 'trade/'
        ]
        
        filepath_lower = filepath.lower()
        for pattern in exclude_patterns:
            if pattern in filepath_lower:
                return False
        
        # Only include from these directories or specific files
        include_dirs = [
            'help/', 'modules/', 'security/', 'regulatory/',
            'tutorials/', 'nodes/', 'ecosystem/', 'technical/',
            'architecture/', 'development/'
        ]
        
        include_files = [
            '01-introduction.md', '02-smart-contracts.md', '03-smart-tokens.md',
            '04-smart-tokens.md', '05-fee-model.md', '06-dex.md', '07-bridges.md',
            'README.md', 'TX-Blockchain.md'
        ]
        
        is_included = False
        for include_dir in include_dirs:
            if include_dir in filepath:
                is_included = True
                break
        
        for include_file in include_files:
            if filepath.endswith(include_file):
                is_included = True
                break
        
        return is_included and has_tx_content
    
    def _load_tx_documentation(self):
        """Load only genuine TX documentation"""
        docs_path = "/home/greg/dev/TXdocumentation"
        
        md_files = glob.glob(f"{docs_path}/**/*.md", recursive=True)
        
        print(f"📂 Scanning {len(md_files)} files...")
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                rel_path = os.path.relpath(file_path, docs_path)
                
                if not self._is_valid_tx_doc(rel_path, content):
                    continue
                
                # Extract title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else os.path.basename(rel_path).replace('.md', '').replace('-', ' ').title()
                
                # Extract a good summary (first non-title paragraph)
                lines = content.split('\n')
                summary = ""
                for line in lines:
                    if line.strip() and not line.startswith('#') and len(line.strip()) > 30:
                        summary = line.strip()[:200]
                        break
                
                # Determine category
                if 'smart' in rel_path and ('token' in rel_path or 'contract' in rel_path):
                    category = 'Smart Contracts & Tokens'
                elif 'validator' in rel_path or 'node' in rel_path:
                    category = 'Validators & Nodes'
                elif 'dex' in rel_path:
                    category = 'DEX & Trading'
                elif 'ibc' in rel_path or 'bridge' in rel_path:
                    category = 'IBC & Bridges'
                elif 'fee' in rel_path:
                    category = 'Fee Model'
                elif 'governance' in rel_path:
                    category = 'Governance'
                elif 'security' in rel_path or 'audit' in rel_path:
                    category = 'Security'
                elif 'regulatory' in rel_path or 'mica' in rel_path:
                    category = 'Regulatory'
                else:
                    category = 'Core Concepts'
                
                self.docs.append({
                    'file': rel_path,
                    'title': title,
                    'summary': summary,
                    'content': content,
                    'category': category,
                    'priority': 1 if 'help' in rel_path or 'modules' in rel_path else 2
                })
                
                print(f"✓ {category}: {title}")
                
            except Exception as e:
                continue
        
        # Sort by priority
        self.docs.sort(key=lambda x: x['priority'])
        
        print(f"\n✅ Loaded {len(self.docs)} high-quality TX documents")
        
        # Show categories
        categories = {}
        for doc in self.docs:
            categories[doc['category']] = categories.get(doc['category'], 0) + 1
        print("\n📚 Documentation categories:")
        for cat, count in sorted(categories.items()):
            print(f"   {cat}: {count} docs")
    
    def search(self, query, limit=3):
        """Search for relevant documentation"""
        query_lower = query.lower()
        results = []
        
        for doc in self.docs:
            score = 0
            
            # Title match (highest)
            if query_lower in doc['title'].lower():
                score += 30
            
            # Category match
            if query_lower in doc['category'].lower():
                score += 20
            
            # Summary match
            if query_lower in doc['summary'].lower():
                score += 15
            
            # Content match
            score += min(doc['content'].lower().count(query_lower) * 2, 25)
            
            if score > 0:
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results][:limit]
    
    def get_answer(self, question):
        """Get a focused answer"""
        question_lower = question.lower()
        results = self.search(question, limit=2)
        
        if not results:
            return "I couldn't find specific information about that. Try asking about: smart contracts, smart tokens, validators, DEX, IBC, fee model, governance, or security."
        
        best = results[0]
        
        # Find the most relevant paragraph
        lines = best['content'].split('\n')
        relevant_paragraph = ""
        
        for i, line in enumerate(lines):
            if question_lower in line.lower() and len(line.strip()) > 40:
                relevant_paragraph = line.strip()
                # Get surrounding context
                if i > 0 and lines[i-1].strip() and not lines[i-1].startswith('#'):
                    relevant_paragraph = lines[i-1].strip() + " " + relevant_paragraph
                break
        
        if not relevant_paragraph:
            # Use summary or first good paragraph
            relevant_paragraph = best['summary'] or lines[1] if len(lines) > 1 else best['content'][:300]
        
        # Clean up markdown
        relevant_paragraph = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', relevant_paragraph)
        relevant_paragraph = re.sub(r'`([^`]+)`', r'\1', relevant_paragraph)
        
        answer = f"**{best['title']}**\n"
        answer += f"📁 Category: {best['category']}\n"
        answer += f"📄 Source: `{best['file']}`\n\n"
        answer += relevant_paragraph[:600]
        
        if len(results) > 1:
            answer += f"\n\n📚 Related: {results[1]['title']}"
        
        return answer

def main():
    agent = TXFocusedAgent()
    
    print("\n" + "="*60)
    print("🤖 TX Focused Agent")
    print("="*60)
    print("\nI only answer based on genuine TX blockchain documentation.")
    
    # Show available topics
    topics = set()
    for doc in agent.docs[:10]:
        topics.add(doc['category'])
    
    print("\n💡 I can help with:")
    for topic in sorted(topics):
        print(f"   • {topic}")
    
    print("\n" + "="*60)
    
    while True:
        try:
            question = input("\n💬 Ask about TX blockchain: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
            
            if question.lower() == 'help':
                print("\nTry asking questions like:")
                print("  • What are smart tokens?")
                print("  • How do I stake TX tokens?")
                print("  • What is the DEX?")
                print("  • How does IBC work?")
                print("  • What is the fee model?")
                print("  • How do I become a validator?")
                print("  • Is TX MiCA compliant?")
                continue
            
            print("\n" + "="*50)
            answer = agent.get_answer(question)
            print(answer)
            print("="*50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
