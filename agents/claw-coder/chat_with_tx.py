#!/usr/bin/env python3
"""
Interactive chat with TX documentation
"""

from tx_agent_knowledge import TXAgentKnowledge

def main():
    kb = TXAgentKnowledge()
    
    print("\n" + "="*60)
    print("🤖 Claw-Coder: TX Blockchain Assistant")
    print("="*60)
    print("Ask me anything about TX blockchain!")
    print("Commands: /search <term>, /category <name>, /help, /exit")
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
                print("  /search <term>    - Search documentation")
                print("  /category <name>  - Browse by category")
                print("  /categories       - List all categories")
                print("  /summary <topic>  - Get topic summary")
                print("  /exit             - Quit")
                print("\nOr just ask a question naturally!")
                continue
            
            if user_input.startswith("/search "):
                query = user_input[8:]
                results = kb.search(query, limit=5)
                print(f"\n📚 Found {len(results)} results:")
                for i, r in enumerate(results, 1):
                    print(f"\n{i}. [{r['category']}] {r['file']}")
                    print(f"   {r['content'][:200]}...")
                continue
            
            if user_input.startswith("/category "):
                cat = user_input[10:]
                docs = kb.get_category(cat)
                if docs:
                    print(f"\n📁 {cat} ({len(docs)} docs):")
                    for d in docs[:10]:
                        print(f"   - {d['file']}")
                else:
                    print(f"❌ Category '{cat}' not found")
                continue
            
            if user_input == "/categories":
                cats = kb.get_categories()
                print("\n📁 Categories:")
                for cat, count in sorted(cats.items()):
                    print(f"   {cat}: {count} docs")
                continue
            
            if user_input.startswith("/summary "):
                topic = user_input[9:]
                print(kb.summarize_topic(topic))
                continue
            
            # Natural language question
            answer = kb.answer(user_input)
            print(f"\n🤖 Claw-Coder: {answer}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
