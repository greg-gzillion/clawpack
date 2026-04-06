#!/usr/bin/env python3
"""
Claw-Coder FINAL - Actually Finds and Shows Content
"""

import os
import glob

class ClawFinal:
    def __init__(self):
        self.docs = []
        self._load_all()
    
    def _load_all(self):
        """Load all TX documentation"""
        docs_path = "/home/greg/dev/TXdocumentation"
        
        # Keywords to identify TX docs (not PhoenixPME)
        tx_keywords = ['tx blockchain', 'smart token', 'smart contract', 'validator', 
                       'dex', 'ibc', 'fee model', 'coreum', 'txd', 'wasm', 'cosmwasm']
        
        for fp in glob.glob(f"{docs_path}/**/*.md", recursive=True):
            rel = os.path.relpath(fp, docs_path)
            
            # Skip PhoenixPME specific
            if 'phoenixpme' in rel.lower() or rel.startswith('phoenixpme'):
                continue
            
            # Skip generic files
            if rel in ['README.md', 'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md']:
                continue
            
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it's TX-related
                is_tx = False
                for kw in tx_keywords:
                    if kw in content.lower():
                        is_tx = True
                        break
                
                if not is_tx and len(content) > 500:
                    # Still include if it's a tutorial or guide
                    if 'tutorial' in rel or 'guide' in rel:
                        is_tx = True
                
                if is_tx and len(content) > 200:
                    self.docs.append({
                        'file': rel,
                        'content': content
                    })
            except:
                pass
        
        print(f"✅ Loaded {len(self.docs)} TX documents")
        
        # Show what we have
        print("\n📚 Available topics:")
        topics = set()
        for doc in self.docs[:20]:
            topic = doc['file'].split('/')[-1].replace('.md', '').replace('-', ' ')
            topics.add(topic[:40])
        for t in sorted(topics)[:15]:
            print(f"   • {t}")
    
    def find(self, query):
        """Find content matching query"""
        query_lower = query.lower()
        results = []
        
        for doc in self.docs:
            content_lower = doc['content'].lower()
            
            # Direct match in content
            if query_lower in content_lower:
                # Find the section containing the query
                lines = doc['content'].split('\n')
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        # Get surrounding lines
                        start = max(0, i-2)
                        end = min(len(lines), i+4)
                        section = '\n'.join(lines[start:end])
                        
                        results.append({
                            'file': doc['file'],
                            'section': section,
                            'line': line.strip()
                        })
                        break
        
        return results
    
    def answer(self, query):
        """Get answer for query"""
        results = self.find(query)
        
        if not results:
            # Try partial match
            words = query.lower().split()
            for doc in self.docs:
                for word in words:
                    if len(word) > 3 and word in doc['content'].lower():
                        lines = doc['content'].split('\n')
                        for line in lines:
                            if word in line.lower() and len(line.strip()) > 30:
                                results.append({
                                    'file': doc['file'],
                                    'section': line.strip(),
                                    'line': line.strip()
                                })
                                break
                if results:
                    break
        
        if not results:
            return None
        
        best = results[0]
        
        response = f"\n📄 **{best['file']}**\n"
        response += "=" * 50 + "\n"
        response += best['section'][:800]
        response += "\n" + "=" * 50
        
        return response

def main():
    agent = ClawFinal()
    
    print("\n" + "=" * 60)
    print("🦞 Claw-Coder FINAL - TX Blockchain Assistant")
    print("=" * 60)
    print("\nAsk me anything about TX blockchain for PhoenixPME development.")
    print("\nExamples:")
    print("  • How do I create a smart token?")
    print("  • How do I become a validator?")
    print("  • How does the DEX work?")
    print("  • What are the gas fees?")
    print("\nType 'exit' to quit, 'topics' to see available docs")
    print("=" * 60)
    
    while True:
        try:
            query = input("\n🦞 You: ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'exit':
                print("\n👋 Happy coding on TX!")
                break
            
            if query.lower() == 'topics':
                print("\n📚 Available documentation:")
                for doc in agent.docs[:25]:
                    print(f"   • {doc['file']}")
                continue
            
            answer = agent.answer(query)
            
            if answer:
                print(answer)
            else:
                print(f"\n❌ Couldn't find '{query}'")
                print("\n💡 Try searching for specific terms like:")
                print("   • 'smart token'")
                print("   • 'create fungible token'")
                print("   • 'validator setup'")
                print("   • 'dex order'")
                print("   • 'fee model'")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
