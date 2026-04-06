#!/usr/bin/env python3
"""
Optimized TX Agent - Prioritizes user-friendly documentation
"""

import json
import os
import glob
import re
from pathlib import Path

class OptimizedTXAgent:
    def __init__(self):
        self.docs = []
        self._load_documentation()
    
    def _should_prioritize(self, filepath):
        """Prioritize user-friendly docs over API/protobuf files"""
        priority_patterns = [
            'help/',
            'README.md',
            'introduction',
            'overview',
            'guide',
            'tutorial',
            'modules/',
            'security/',
            'regulatory/'
        ]
        
        low_priority_patterns = [
            'api.md',
            'protobuf',
            'tx-chain/docs/api',
            '.proto',
            'swagger'
        ]
        
        for pattern in low_priority_patterns:
            if pattern in filepath.lower():
                return False
        
        for pattern in priority_patterns:
            if pattern in filepath.lower():
                return True
        
        return True
    
    def _get_doc_type(self, filepath):
        """Determine document type for better formatting"""
        if 'help/' in filepath:
            return 'guide'
        elif 'tutorial' in filepath:
            return 'tutorial'
        elif 'modules/' in filepath:
            return 'module'
        elif 'security/' in filepath:
            return 'security'
        elif 'regulatory/' in filepath:
            return 'regulatory'
        elif 'nodes/' in filepath:
            return 'validator'
        elif 'api' in filepath or 'protobuf' in filepath:
            return 'api'
        else:
            return 'general'
    
    def _load_documentation(self):
        """Load and index documentation"""
        docs_path = "/home/greg/dev/TXdocumentation"
        
        # Skip these directories
        skip_dirs = ['phoenixpme', 'aed', 'alert', 'asset', 'comment', 'email-', 'feature-flag', 'file', 'holdings', 'kyc', 'minicms', 'notification', 'order', 'record', 'reference', 'trade', 'update', 'user', 'wallet']
        
        md_files = glob.glob(f"{docs_path}/**/*.md", recursive=True)
        
        print(f"📂 Scanning {len(md_files)} files...")
        
        for file_path in md_files:
            # Skip unwanted directories
            skip = False
            for skip_dir in skip_dirs:
                if f'/{skip_dir}' in file_path or f'\\{skip_dir}' in file_path:
                    skip = True
                    break
            
            if skip:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                rel_path = os.path.relpath(file_path, docs_path)
                
                # Skip if content is too short or seems like auto-generated API doc
                if len(content) < 100:
                    continue
                
                # Extract title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else Path(rel_path).stem.replace('-', ' ').title()
                
                # Extract description (first paragraph after title)
                desc_match = re.search(r'^#\s+.+?\n\n(.+?)(?=\n\n|\n#)', content, re.MULTILINE | re.DOTALL)
                description = desc_match.group(1).strip()[:300] if desc_match else ""
                
                self.docs.append({
                    'file': rel_path,
                    'title': title,
                    'description': description,
                    'content': content,
                    'content_lower': content.lower(),
                    'doc_type': self._get_doc_type(rel_path),
                    'priority': self._should_prioritize(rel_path),
                    'size': len(content)
                })
                
            except Exception as e:
                continue
        
        # Sort by priority (user-friendly docs first)
        self.docs.sort(key=lambda x: x['priority'], reverse=True)
        
        print(f"✅ Loaded {len(self.docs)} optimized documents")
        print(f"\n📚 Document types:")
        doc_types = {}
        for doc in self.docs:
            doc_types[doc['doc_type']] = doc_types.get(doc['doc_type'], 0) + 1
        for dt, count in sorted(doc_types.items()):
            print(f"   {dt}: {count}")
    
    def search(self, query, limit=3):
        """Smart search with contextual scoring"""
        query_lower = query.lower()
        results = []
        
        for doc in self.docs:
            score = 0
            
            # Title match (highest weight)
            if query_lower in doc['title'].lower():
                score += 20
                # Exact title match bonus
                if doc['title'].lower() == query_lower:
                    score += 30
            
            # Description match
            if query_lower in doc['description'].lower():
                score += 15
            
            # Content matches
            content_matches = doc['content_lower'].count(query_lower)
            score += min(content_matches * 2, 30)  # Cap at 30
            
            # File path match
            if query_lower in doc['file'].lower():
                score += 5
            
            # Boost for high-priority docs
            if doc['priority']:
                score += 10
            
            # Boost for specific doc types based on query
            if 'validator' in query_lower and doc['doc_type'] == 'validator':
                score += 15
            if 'security' in query_lower and doc['doc_type'] == 'security':
                score += 15
            if 'guide' in query_lower and doc['doc_type'] == 'guide':
                score += 10
            
            if score > 0:
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results][:limit]
    
    def _extract_relevant_section(self, content, query, max_length=800):
        """Extract the most relevant section from content"""
        query_lower = query.lower()
        lines = content.split('\n')
        
        # Find the best matching line
        best_idx = -1
        best_score = 0
        
        for i, line in enumerate(lines):
            if len(line.strip()) < 20:  # Skip short lines
                continue
            line_lower = line.lower()
            score = line_lower.count(query_lower)
            if score > best_score:
                best_score = score
                best_idx = i
        
        if best_idx >= 0:
            # Get context (2 lines before, 3 after)
            start = max(0, best_idx - 2)
            end = min(len(lines), best_idx + 4)
            section = '\n'.join(lines[start:end])
            
            # Clean up markdown
            section = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', section)  # Remove links
            section = re.sub(r'`([^`]+)`', r'\1', section)  # Remove inline code backticks
            
            if len(section) > max_length:
                section = section[:max_length] + "..."
            
            return section.strip()
        
        # Fallback: return first meaningful paragraph
        for line in lines:
            if len(line.strip()) > 40 and not line.startswith('#'):
                return line.strip()[:max_length]
        
        return content[:max_length]
    
    def answer(self, question):
        """Generate a clean, readable answer"""
        results = self.search(question, limit=2)
        
        if not results:
            return "I couldn't find information about that. Try asking about:\n• Smart contracts and tokens\n• Validators and staking\n• DEX trading\n• IBC bridges\n• Fee model\n• Governance\n• Security\n• MiCA compliance"
        
        # Use the best result
        doc = results[0]
        
        # Extract relevant section
        relevant_text = self._extract_relevant_section(doc['content'], question)
        
        # Format the response
        response = f"**{doc['title']}**\n"
        response += f"📄 `{doc['file']}`\n\n"
        response += relevant_text
        
        # Add reference to more results if available
        if len(results) > 1:
            response += f"\n\n📚 Also check: {results[1]['title']}"
        
        return response

def main():
    agent = OptimizedTXAgent()
    
    print("\n" + "="*60)
    print("🤖 Optimized TX Agent")
    print("="*60)
    print("\nI provide clean, readable answers about TX blockchain.")
    print("\nTry asking me about:")
    print("  • What is TX blockchain?")
    print("  • How do smart tokens work?")
    print("  • How do I become a validator?")
    print("  • What is the DEX?")
    print("  • How does IBC work?")
    print("  • What is the fee model?")
    print("  • How does governance work?")
    print("  • Is TX MiCA compliant?")
    print("\nCommands: /search <term>, /list, /help, /exit")
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
                print("  /search <term>   - Search documentation")
                print("  /list            - Show available topics")
                print("  /exit            - Quit")
                print("\nOr just ask a natural language question!")
                continue
            
            if user_input == "/list":
                topics = set()
                for doc in agent.docs[:30]:
                    if doc['priority']:
                        topics.add(doc['title'][:50])
                print("\n📚 Available topics:")
                for topic in sorted(list(topics))[:20]:
                    print(f"  • {topic}")
                continue
            
            if user_input.startswith("/search "):
                query = user_input[8:]
                results = agent.search(query, limit=5)
                if results:
                    print(f"\n📚 Found {len(results)} results:")
                    for i, doc in enumerate(results, 1):
                        print(f"\n{i}. **{doc['title']}**")
                        print(f"   📄 {doc['file']}")
                        print(f"   📝 {doc['description'][:100]}...")
                else:
                    print(f"\n❌ No results for '{query}'")
                continue
            
            # Natural language question
            print("\n" + "="*50)
            answer = agent.answer(user_input)
            print(answer)
            print("="*50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
