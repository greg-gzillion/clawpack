#!/usr/bin/env python3
"""
Index TXdocumentation for claw-coder
Includes all documentation files for TX blockchain
"""

import json
import os
from pathlib import Path
from datetime import datetime

INDEX_FILE = Path.home() / ".claw_index.json"
TX_DOCS_PATH = Path("/home/greg/dev/TXdocumentation")

def load_index():
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r') as f:
            return json.load(f)
    return {"files": {}, "docs": {}, "stats": {}}

def save_index(index):
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)

def index_tx_documentation():
    """Index all TXdocumentation files"""
    if not TX_DOCS_PATH.exists():
        print(f"❌ TXdocumentation not found at {TX_DOCS_PATH}")
        return
    
    index = load_index()
    
    # Clear existing TX docs to avoid duplicates
    docs_to_remove = []
    for doc_path, info in index.get("docs", {}).items():
        if "TXdocumentation" in doc_path:
            docs_to_remove.append(doc_path)
    
    for doc_path in docs_to_remove:
        del index["docs"][doc_path]
    
    print("📚 Indexing TXdocumentation...")
    print(f"   Path: {TX_DOCS_PATH}")
    
    file_count = 0
    doc_count = 0
    code_count = 0
    
    # File extensions to treat as documentation
    doc_extensions = {'.md', '.txt', '.rst', '.pdf', '.html', '.json', '.yaml', '.yml', '.toml'}
    code_extensions = {'.rs', '.go', '.py', '.js', '.ts', '.sh', '.mod', '.sum'}
    
    for filepath in TX_DOCS_PATH.rglob("*"):
        if filepath.is_file() and filepath.stat().st_size < 500000:  # 500KB max
            ext = filepath.suffix.lower()
            file_count += 1
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    
                    # Determine type
                    if ext in doc_extensions:
                        doc_type = "tx_documentation"
                        doc_count += 1
                    elif ext in code_extensions:
                        doc_type = "tx_code_example"
                        code_count += 1
                    else:
                        doc_type = "tx_other"
                    
                    # Store in index
                    index["docs"][str(filepath)] = {
                        "type": doc_type,
                        "name": filepath.name,
                        "ext": ext,
                        "lines": lines,
                        "size": len(content),
                        "path": str(filepath.relative_to(TX_DOCS_PATH)),
                        "modified": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
                    }
                    
                    if file_count % 100 == 0:
                        print(f"   Processed {file_count} files...")
                        
            except Exception as e:
                # Skip files that can't be read
                pass
    
    # Update stats
    index["stats"]["tx_documentation"] = {
        "total_files": file_count,
        "doc_files": doc_count,
        "code_examples": code_count,
        "path": str(TX_DOCS_PATH),
        "last_indexed": datetime.now().isoformat()
    }
    
    save_index(index)
    
    print(f"\n✅ TXdocumentation indexing complete!")
    print(f"   📁 Total files: {file_count}")
    print(f"   📖 Documentation: {doc_count}")
    print(f"   💻 Code examples: {code_count}")
    print(f"   📊 Index size: {len(index['docs'])} total docs")

def search_tx_docs(query, limit=20):
    """Search TXdocumentation for specific content"""
    index = load_index()
    results = []
    
    for doc_path, info in index.get("docs", {}).items():
        if "TXdocumentation" in doc_path and info.get("type") in ["tx_documentation", "tx_code_example"]:
            try:
                with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        # Find line numbers with matches
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if query.lower() in line.lower():
                                start = max(0, i-2)
                                end = min(len(lines), i+3)
                                context = '\n'.join(lines[start:end])
                                results.append({
                                    "file": str(doc_path),
                                    "path": info.get("path", doc_path),
                                    "line": i+1,
                                    "context": context[:300]
                                })
                                if len(results) >= limit:
                                    break
                    if len(results) >= limit:
                        break
            except:
                pass
    
    return results

if __name__ == "__main__":
    print("🦞 TXdocumentation Indexer")
    print("="*50)
    index_tx_documentation()
    
    # Test search
    print("\n🔍 Testing search capability...")
    results = search_tx_docs("collateral", 3)
    if results:
        print(f"   Found {len(results)} results for 'collateral'")
        for r in results[:2]:
            print(f"   📄 {r['path']} (line {r['line']})")
    else:
        print("   No results found (this is fine - just testing)")
