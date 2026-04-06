#!/usr/bin/env python3
import json
import os

class TXQuery:
    def __init__(self):
        kb_file = "/home/greg/dev/claw-coder/knowledge_base/tx_docs/knowledge_base.json"
        
        if not os.path.exists(kb_file):
            print("❌ Knowledge base not found. Run ingestion first")
            exit(1)
        
        with open(kb_file, 'r', encoding='utf-8') as f:
            self.knowledge = json.load(f)
        
        self.index = {doc['file']: doc for doc in self.knowledge}
        print(f"✅ Loaded {len(self.knowledge)} documents")
    
    def search(self, keyword):
        results = []
        keyword_lower = keyword.lower()
        
        for doc in self.knowledge:
            if (keyword_lower in doc['file'].lower() or 
                keyword_lower in doc['content'].lower()):
                score = doc['content'].lower().count(keyword_lower)
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results]
    
    def get_by_category(self, category):
        return [doc for doc in self.knowledge if doc['category'] == category]
    
    def show_categories(self):
        categories = {}
        for doc in self.knowledge:
            cat = doc['category']
            categories[cat] = categories.get(cat, 0) + 1
        return categories

def main():
    tx = TXQuery()
    
    print("\n" + "="*60)
    print("📚 TX Documentation Query Tool")
    print("="*60)
    print("\nCommands:")
    print("  search <term>     - Search for keyword")
    print("  category <name>   - List documents in category")
    print("  read <filename>   - Read full document")
    print("  categories        - Show all categories")
    print("  exit              - Quit")
    print("="*60)
    
    while True:
        try:
            cmd = input("\n🔍 TX> ").strip()
            if not cmd:
                continue
            
            if cmd == "exit":
                break
            
            if cmd == "categories":
                cats = tx.show_categories()
                print("\n📁 Categories:")
                for cat, count in sorted(cats.items()):
                    print(f"   {cat}: {count} docs")
                continue
            
            if cmd.startswith("category "):
                cat = cmd[9:]
                docs = tx.get_by_category(cat)
                if docs:
                    print(f"\n📁 {cat} ({len(docs)} docs):")
                    for doc in docs[:15]:
                        print(f"   - {doc['file']}")
                else:
                    print(f"❌ Category '{cat}' not found")
                continue
            
            if cmd.startswith("search "):
                keyword = cmd[7:]
                results = tx.search(keyword)
                if results:
                    print(f"\n📚 Found {len(results)} results:")
                    for i, doc in enumerate(results[:5], 1):
                        print(f"\n{i}. [{doc['category']}] {doc['file']}")
                        preview = doc['content'][:200].replace('\n', ' ')
                        print(f"   {preview}...")
                else:
                    print(f"❌ No results for '{keyword}'")
                continue
            
            if cmd.startswith("read "):
                fname = cmd[5:]
                if fname in tx.index:
                    doc = tx.index[fname]
                    print(f"\n📄 {doc['file']}\n")
                    print(doc['content'][:2000])
                    if len(doc['content']) > 2000:
                        print("\n... (truncated, use full_read for complete)")
                else:
                    print(f"❌ File '{fname}' not found")
                continue
            
            print("Unknown command. Try: search, category, read, categories, exit")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
