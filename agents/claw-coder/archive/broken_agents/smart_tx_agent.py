#!/usr/bin/env python3
"""
Smart TX Agent - Knows TX blockchain vs PhoenixPME
"""

import json
import os
import glob

class SmartTXAgent:
    def __init__(self):
        self.tx_docs = []
        self.phoenix_docs = []
        self._load_documentation()
    
    def _load_documentation(self):
        """Load documentation, separating TX from PhoenixPME"""
        docs_path = "/home/greg/dev/TXdocumentation"
        
        # Find all markdown files
        md_files = glob.glob(f"{docs_path}/**/*.md", recursive=True)
        
        for file_path in md_files:
            rel_path = os.path.relpath(file_path, docs_path)
            
            # Check if it's PhoenixPME
            if 'phoenixpme' in rel_path or rel_path.startswith('phoenixpme'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.phoenix_docs.append({
                        'file': rel_path,
                        'content': f.read()
                    })
            else:
                # It's TX blockchain documentation
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.tx_docs.append({
                        'file': rel_path,
                        'content': f.read()
                    })
        
        print(f"✅ Loaded {len(self.tx_docs)} TX blockchain documents")
        print(f"📁 Loaded {len(self.phoenix_docs)} PhoenixPME documents")
    
    def search_tx(self, query, limit=5):
        """Search only TX blockchain docs"""
        query_lower = query.lower()
        results = []
        
        for doc in self.tx_docs:
            if query_lower in doc['content'].lower():
                score = doc['content'].lower().count(query_lower)
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results][:limit]
    
    def search_phoenix(self, query, limit=5):
        """Search only PhoenixPME docs"""
        query_lower = query.lower()
        results = []
        
        for doc in self.phoenix_docs:
            if query_lower in doc['content'].lower():
                score = doc['content'].lower().count(query_lower)
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results][:limit]
    
    def answer(self, question):
        """Answer based on context (prioritizes TX unless PhoenixPME mentioned)"""
        question_lower = question.lower()
        
        # Check if asking about PhoenixPME
        if 'phoenix' in question_lower or 'pme' in question_lower:
            results = self.search_phoenix(question, limit=1)
            if results:
                return f"📖 [PhoenixPME] {results[0]['file']}\n{results[0]['content'][:400]}"
        
        # Default to TX blockchain
        results = self.search_tx(question, limit=1)
        if results:
            return f"📖 [TX Blockchain] {results[0]['file']}\n{results[0]['content'][:400]}"
        
        return "I couldn't find that in either documentation set."

def main():
    agent = SmartTXAgent()
    
    print("\n" + "="*60)
    print("🤖 Smart TX Agent (TX Blockchain + PhoenixPME)")
    print("="*60)
    print("I know the difference between TX blockchain and PhoenixPME!")
    print("\nCommands:")
    print("  /tx <query>      - Search only TX blockchain docs")
    print("  /phoenix <query> - Search only PhoenixPME docs")
    print("  /help            - Show this help")
    print("  /exit            - Quit")
    print("\nOr just ask naturally - I'll figure out which docs to use!")
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
                print("  /tx <query>      - Search TX blockchain")
                print("  /phoenix <query> - Search PhoenixPME")
                print("  /exit            - Quit")
                continue
            
            if user_input.startswith("/tx "):
                query = user_input[4:]
                results = agent.search_tx(query)
                print(f"\n📚 TX Blockchain ({len(results)} results):")
                for i, r in enumerate(results, 1):
                    print(f"\n{i}. {r['file']}")
                    print(f"   {r['content'][:200]}...")
                continue
            
            if user_input.startswith("/phoenix "):
                query = user_input[9:]
                results = agent.search_phoenix(query)
                print(f"\n📚 PhoenixPME ({len(results)} results):")
                for i, r in enumerate(results, 1):
                    print(f"\n{i}. {r['file']}")
                    print(f"   {r['content'][:200]}...")
                continue
            
            # Natural language
            print(f"\n🤖 Agent: {agent.answer(user_input)}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
