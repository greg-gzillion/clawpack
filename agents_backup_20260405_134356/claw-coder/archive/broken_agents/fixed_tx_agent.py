#!/usr/bin/env python3
"""
Fixed TX Agent - Properly indexes and searches documentation
"""

import json
import os
import glob
import re

class FixedTXAgent:
    def __init__(self):
        self.tx_docs = []
        self.phoenix_docs = []
        self._load_documentation()
    
    def _load_documentation(self):
        """Load and index documentation"""
        docs_path = "/home/greg/dev/TXdocumentation"
        
        # Find all markdown files
        md_files = glob.glob(f"{docs_path}/**/*.md", recursive=True)
        
        print(f"📂 Found {len(md_files)} total markdown files")
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                rel_path = os.path.relpath(file_path, docs_path)
                
                # Extract title from content
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else os.path.basename(rel_path)
                
                doc_info = {
                    'file': rel_path,
                    'title': title,
                    'content': content,
                    'content_lower': content.lower(),
                    'size': len(content)
                }
                
                # Check if it's PhoenixPME
                if 'phoenixpme' in rel_path:
                    self.phoenix_docs.append(doc_info)
                else:
                    self.tx_docs.append(doc_info)
                    
            except Exception as e:
                print(f"⚠️ Error loading {file_path}: {e}")
        
        print(f"✅ Loaded {len(self.tx_docs)} TX blockchain documents")
        print(f"📁 Loaded {len(self.phoenix_docs)} PhoenixPME documents")
        
        # Show some sample files to verify
        if self.tx_docs:
            print(f"\n📄 Sample TX files:")
            for doc in self.tx_docs[:3]:
                print(f"   - {doc['file']} ({doc['size']} chars)")
    
    def search_tx(self, query, limit=5):
        """Search only TX blockchain docs with scoring"""
        query_lower = query.lower()
        results = []
        
        for doc in self.tx_docs:
            score = 0
            # Count occurrences in content
            score += doc['content_lower'].count(query_lower) * 2
            # Count in title (higher weight)
            if query_lower in doc['title'].lower():
                score += 10
            # Count in filename
            if query_lower in doc['file'].lower():
                score += 5
            
            if score > 0:
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results][:limit]
    
    def search_phoenix(self, query, limit=5):
        """Search only PhoenixPME docs"""
        query_lower = query.lower()
        results = []
        
        for doc in self.phoenix_docs:
            score = doc['content_lower'].count(query_lower)
            if score > 0:
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results][:limit]
    
    def answer(self, question):
        """Answer based on context"""
        question_lower = question.lower()
        
        # Check if asking about PhoenixPME
        if 'phoenix' in question_lower or 'pme' in question_lower:
            results = self.search_phoenix(question, limit=1)
            if results:
                doc = results[0]
                # Extract relevant paragraph
                lines = doc['content'].split('\n')
                relevant_lines = []
                for i, line in enumerate(lines):
                    if question_lower in line.lower():
                        # Get context (2 lines before and after)
                        start = max(0, i-2)
                        end = min(len(lines), i+3)
                        relevant_lines = lines[start:end]
                        break
                
                if relevant_lines:
                    response = '\n'.join(relevant_lines)
                else:
                    response = doc['content'][:500]
                
                return f"📖 [PhoenixPME] {doc['file']}\n\n{response}"
        
        # Search TX blockchain
        results = self.search_tx(question, limit=1)
        if results:
            doc = results[0]
            # Find relevant section
            lines = doc['content'].split('\n')
            relevant_lines = []
            for i, line in enumerate(lines):
                if question_lower in line.lower():
                    start = max(0, i-2)
                    end = min(len(lines), i+3)
                    relevant_lines = lines[start:end]
                    break
            
            if relevant_lines:
                response = '\n'.join(relevant_lines)
            else:
                # Return first 500 chars if no direct match found
                response = doc['content'][:500]
            
            return f"📖 [TX Blockchain] {doc['title']}\n📄 {doc['file']}\n\n{response}"
        
        return "I couldn't find that in the documentation. Try asking about: smart contracts, tokens, validators, DEX, IBC, governance, or fees."

def main():
    agent = FixedTXAgent()
    
    print("\n" + "="*60)
    print("🤖 Fixed TX Agent (Properly Indexed)")
    print("="*60)
    print("\nTry asking me about:")
    print("  • TX blockchain overview")
    print("  • Smart contracts and smart tokens")
    print("  • Validator operations and staking")
    print("  • DEX and trading")
    print("  • IBC bridges")
    print("  • Fee model and gas")
    print("  • Governance")
    print("  • Security audits")
    print("  • MiCA compliance")
    print("\nCommands:")
    print("  /tx <query>      - Search TX docs")
    print("  /phoenix <query> - Search PhoenixPME")
    print("  /help            - Show commands")
    print("  /exit            - Quit")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "/exit":
                print("👋 Goodbye!")
                break
            
            if user_input == "/help":
                print("\nCommands:")
                print("  /tx <query>      - Search TX blockchain docs")
                print("  /phoenix <query> - Search PhoenixPME docs")
                print("  /help            - Show this help")
                print("  /exit            - Quit")
                print("\nOr just ask a natural language question!")
                continue
            
            if user_input.startswith("/tx "):
                query = user_input[4:]
                results = agent.search_tx(query)
                if results:
                    print(f"\n📚 Found {len(results)} results:")
                    for i, doc in enumerate(results, 1):
                        print(f"\n{i}. {doc['title']}")
                        print(f"   📄 {doc['file']}")
                        print(f"   📏 {doc['size']} chars")
                else:
                    print(f"\n❌ No results found for '{query}'")
                continue
            
            if user_input.startswith("/phoenix "):
                query = user_input[9:]
                results = agent.search_phoenix(query)
                if results:
                    print(f"\n📚 Found {len(results)} results:")
                    for i, doc in enumerate(results, 1):
                        print(f"\n{i}. {doc['file']}")
                        print(f"   📏 {doc['size']} chars")
                else:
                    print(f"\n❌ No PhoenixPME results found")
                continue
            
            # Natural language question
            print(f"\n🤖 Agent: {agent.answer(user_input)}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
