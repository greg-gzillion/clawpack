#!/usr/bin/env python3
"""
RustyPyCraw CLI - Hybrid code crawler with shared memory and polyglot support
"""

import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="RustyPyCraw - Hybrid Code Crawler")
    
    # Basic commands
    parser.add_argument("path", nargs="?", default=".", help="Path to crawl")
    parser.add_argument("--stats", action="store_true", help="Show codebase statistics")
    parser.add_argument("--search", "-s", help="Search for pattern in files")
    parser.add_argument("--ask", "-a", help="Ask AI about the codebase")
    parser.add_argument("--groq", action="store_true", help="Use Groq API (fast)")
    parser.add_argument("--ollama", action="store_true", help="Use Ollama (local)")
    
    # Knowledge base commands
    parser.add_argument("--docs", "-d", help="Show documentation references for a language")
    parser.add_argument("--list-langs", action="store_true", help="List all languages with references")
    parser.add_argument("--all-docs", action="store_true", help="Show all documentation references")
    
    # Shared memory commands
    parser.add_argument("--shared-stats", action="store_true", help="Show shared memory statistics")
    parser.add_argument("--remember", nargs=2, metavar=('KEY', 'VALUE'), help="Store a memory")
    parser.add_argument("--recall", help="Recall memories by key")
    
    # Polyglot code generation
    parser.add_argument("--polyglot", "-pg", nargs=2, metavar=('LANG', 'NAME'), help="Generate code in any language")
    parser.add_argument("--list-langs-code", action="store_true", help="List all languages for code generation")
    
    args = parser.parse_args()
    
    # Handle knowledge base commands
    if args.all_docs:
        from .knowledge import KNOWLEDGE_BASE
        print("\n📚 ALL DOCUMENTATION REFERENCES")
        print("=" * 50)
        for category, refs in KNOWLEDGE_BASE.items():
            print(f"\n🔹 {category.upper()}:")
            for name, url in refs.items():
                print(f"   • {name}: {url}")
        return
    
    if args.list_langs:
        from .knowledge import list_languages
        print("\n📚 Available Languages with References:")
        print("-" * 40)
        for lang in list_languages():
            if lang != "general":
                print(f"  - {lang.upper()}")
        return
    
    if args.docs:
        from .knowledge import get_references
        refs = get_references(args.docs)
        print(f"\n📚 References for {args.docs.upper()}:")
        print("-" * 40)
        for name, url in refs.items():
            print(f"  {name}: {url}")
        return
    
    # Handle shared memory commands
    if args.shared_stats:
        from .shared_memory import SharedMemory
        memory = SharedMemory()
        stats = memory.get_stats()
        print("\n📚 SHARED MEMORY STATISTICS")
        print("=" * 50)
        print(f"  Total memories: {stats['memories']}")
        print(f"  Total conversations: {stats['conversations']}")
        print(f"  Registered agents: {stats['agents']}")
        memory.close()
        return
    
    if args.remember:
        from .shared_memory import SharedMemory
        memory = SharedMemory()
        memory.remember("rustypycraw", args.remember[0], args.remember[1])
        print(f"✅ Memory stored: {args.remember[0]} = {args.remember[1]}")
        memory.close()
        return
    
    if args.recall:
        from .shared_memory import SharedMemory
        memory = SharedMemory()
        results = memory.recall(args.recall)
        if results:
            print(f"\n📖 Memories matching '{args.recall}':")
            print("=" * 50)
            for agent, key, value, tags in results:
                print(f"\n🦞 {agent}: {key}")
                print(f"   {value[:200]}...")
        else:
            print(f"No memories found for '{args.recall}'")
        memory.close()
        return
    
    # Handle polyglot commands
    if args.list_langs_code:
        from .polyglot import PolyglotGenerator
        print("\n🌍 Supported Languages for Code Generation:")
        print("=" * 50)
        for lang in PolyglotGenerator.list_languages():
            print(f"  • {lang.upper()}")
        return
    
    if args.polyglot:
        from .polyglot import PolyglotGenerator
        language, name = args.polyglot
        code = PolyglotGenerator.generate(language, name)
        ext = PolyglotGenerator.LANGUAGES.get(language.lower(), {}).get("ext", ".txt")
        filename = f"{name.replace(' ', '_')}{ext}"
        with open(filename, 'w') as f:
            f.write(code)
        print(f"✅ Generated {language} code: {filename}")
        print(f"\n{code[:500]}...\n")
        return
    
    # Handle stats
    if args.stats:
        from .crawler import RustyPyCraw
        crawler = RustyPyCraw(args.path)
        stats = crawler.stats()
        print("\n📊 RustyPyCraw Statistics")
        print(f"  Path: {stats.get('root_path', 'Unknown')}")
        print(f"  Total lines: {stats.get('total_lines', 0):,}")
        print(f"  Languages:")
        for lang, count in stats.get('languages', {}).items():
            print(f"    {lang}: {count}")
        return
    
    # Handle search
    if args.search:
        from .crawler import RustyPyCraw
        crawler = RustyPyCraw(args.path)
        results = crawler.search(args.search)
        print(f"\n🔍 Found {len(results)} files containing '{args.search}':")
        for r in results[:20]:
            print(f"  {r}")
        return
    
    # Handle ask
    if args.ask:
        from .crawler import RustyPyCraw
        crawler = RustyPyCraw(args.path, use_ollama=args.ollama)
        answer = crawler.ask(args.ask)
        print(f"\n🤖 {answer}\n")
        return
    
    # Default: show help
    parser.print_help()

if __name__ == "__main__":
    main()
