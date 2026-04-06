#!/usr/bin/env python3
"""
DATACLAW - Central Personal Library Manager

DESIGN PHILOSOPHY:
- Each agent has its OWN local library folder
- DataClaw provides a CENTRAL interface to manage ALL personal libraries
- Follows same hierarchical structure as Webclaw but for LOCAL content
- User-friendly: easy to add, search, organize personal materials

STRUCTURE:
  agents/{agent_name}/library/
    ├── e_books/        # Personal e-books and PDFs
    ├── research/       # Research papers
    ├── notes/          # Personal notes
    ├── citations/      # Saved citations
    ├── templates/      # Custom templates
    ├── references/     # Reference materials
    ├── imports/        # Import queue
    └── archive/        # Archived materials
"""

import sys
import os
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ============================================
# PATHS
# ============================================
AGENT_DIR = Path(__file__).parent
ROOT_DIR = AGENT_DIR.parent.parent
AGENTS_DIR = ROOT_DIR / "agents"

# Library categories
LIBRARY_CATEGORIES = ["e_books", "research", "notes", "citations", "templates", "references", "imports", "archive"]

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    "text": [".txt", ".md", ".json", ".csv"],
    "document": [".pdf", ".docx", ".odt"],
    "ebook": [".epub", ".mobi", ".azw"],
    "image": [".jpg", ".png", ".gif", ".svg"],
    "audio": [".mp3", ".wav", ".ogg"],
    "video": [".mp4", ".webm"]
}

# ============================================
# DATABASE (for indexing personal library)
# ============================================
DATACLAW_DB = AGENT_DIR / "library_index.db"

def init_database():
    """Initialize the personal library index"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    # Master index of all personal library items
    c.execute('''CREATE TABLE IF NOT EXISTS library_index
                 (id INTEGER PRIMARY KEY,
                  agent TEXT,
                  category TEXT,
                  filename TEXT,
                  filepath TEXT,
                  file_hash TEXT,
                  file_size INTEGER,
                  title TEXT,
                  author TEXT,
                  tags TEXT,
                  notes TEXT,
                  added_date TEXT,
                  last_accessed TEXT,
                  access_count INTEGER DEFAULT 0)''')
    
    # Search history
    c.execute('''CREATE TABLE IF NOT EXISTS search_history
                 (id INTEGER PRIMARY KEY,
                  query TEXT,
                  results_count INTEGER,
                  timestamp TEXT)''')
    
    conn.commit()
    conn.close()

def get_agent_libraries():
    """Get list of all agents with library folders"""
    libraries = []
    for agent_dir in AGENTS_DIR.iterdir():
        if agent_dir.is_dir():
            library_dir = agent_dir / "library"
            if library_dir.exists():
                libraries.append({
                    "agent": agent_dir.name,
                    "path": library_dir,
                    "categories": [c for c in LIBRARY_CATEGORIES if (library_dir / c).exists()]
                })
    return libraries

def index_file(agent: str, category: str, filepath: Path) -> Dict:
    """Index a file in the personal library"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    # Calculate file hash for deduplication
    with open(filepath, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    
    file_size = filepath.stat().st_size
    
    # Try to extract title from filename
    title = filepath.stem.replace('_', ' ').replace('-', ' ')
    
    # Check if already indexed
    c.execute("SELECT id FROM library_index WHERE file_hash = ?", (file_hash,))
    existing = c.fetchone()
    
    if existing:
        conn.close()
        return {"status": "exists", "id": existing[0]}
    
    c.execute('''INSERT INTO library_index
                 (agent, category, filename, filepath, file_hash, file_size, title, added_date)
                 VALUES (?,?,?,?,?,?,?,?)''',
              (agent, category, filepath.name, str(filepath), file_hash, file_size, title, datetime.now().isoformat()))
    
    item_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {"status": "indexed", "id": item_id}

def search_library(query: str, agent: str = None, category: str = None) -> List[Dict]:
    """Search the personal library"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    sql = "SELECT agent, category, filename, title, tags, added_date FROM library_index WHERE filename LIKE ? OR title LIKE ?"
    params = [f'%{query}%', f'%{query}%']
    
    if agent:
        sql += " AND agent = ?"
        params.append(agent)
    
    if category:
        sql += " AND category = ?"
        params.append(category)
    
    sql += " ORDER BY added_date DESC LIMIT 50"
    
    c.execute(sql, params)
    results = [{"agent": r[0], "category": r[1], "filename": r[2], "title": r[3], "tags": r[4], "date": r[5]} for r in c.fetchall()]
    conn.close()
    
    # Save search history
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    c.execute("INSERT INTO search_history (query, results_count, timestamp) VALUES (?,?,?)",
              (query, len(results), datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    return results

# ============================================
# FILE MANAGEMENT FUNCTIONS
# ============================================

def add_file(source_path: str, agent: str, category: str) -> Dict:
    """Add a file to an agent's personal library"""
    source = Path(source_path)
    if not source.exists():
        return {"error": f"File not found: {source_path}"}
    
    if agent not in [l["agent"] for l in get_agent_libraries()]:
        return {"error": f"Agent '{agent}' not found or has no library"}
    
    if category not in LIBRARY_CATEGORIES:
        return {"error": f"Invalid category. Choose from: {', '.join(LIBRARY_CATEGORIES)}"}
    
    # Destination path
    dest_dir = AGENTS_DIR / agent / "library" / category
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Handle duplicate filenames
    dest_path = dest_dir / source.name
    counter = 1
    while dest_path.exists():
        stem = source.stem
        dest_path = dest_dir / f"{stem}_{counter}{source.suffix}"
        counter += 1
    
    # Copy file
    shutil.copy2(source, dest_path)
    
    # Index the file
    index_result = index_file(agent, category, dest_path)
    
    return {
        "status": "success",
        "source": str(source),
        "destination": str(dest_path),
        "agent": agent,
        "category": category,
        "indexed": index_result
    }

def list_agent_library(agent: str, category: str = None) -> List[Dict]:
    """List contents of an agent's personal library"""
    library_dir = AGENTS_DIR / agent / "library"
    if not library_dir.exists():
        return []
    
    items = []
    categories_to_scan = [category] if category else LIBRARY_CATEGORIES
    
    for cat in categories_to_scan:
        cat_dir = library_dir / cat
        if cat_dir.exists():
            for file in cat_dir.iterdir():
                if file.is_file():
                    items.append({
                        "agent": agent,
                        "category": cat,
                        "filename": file.name,
                        "size": file.stat().st_size,
                        "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                    })
    
    return items

def get_library_stats() -> Dict:
    """Get statistics for all personal libraries"""
    stats = {"agents": {}, "total_files": 0, "total_size_bytes": 0}
    
    for agent_info in get_agent_libraries():
        agent = agent_info["agent"]
        agent_stats = {"categories": {}, "total_files": 0, "total_size_bytes": 0}
        
        for category in agent_info["categories"]:
            cat_dir = agent_info["path"] / category
            if cat_dir.exists():
                files = list(cat_dir.iterdir())
                file_count = len([f for f in files if f.is_file()])
                total_size = sum(f.stat().st_size for f in files if f.is_file())
                
                agent_stats["categories"][category] = {
                    "files": file_count,
                    "size_bytes": total_size,
                    "size_mb": round(total_size / (1024 * 1024), 2)
                }
                agent_stats["total_files"] += file_count
                agent_stats["total_size_bytes"] += total_size
        
        stats["agents"][agent] = agent_stats
        stats["total_files"] += agent_stats["total_files"]
        stats["total_size_bytes"] += agent_stats["total_size_bytes"]
    
    stats["total_size_mb"] = round(stats["total_size_bytes"] / (1024 * 1024), 2)
    return stats

# ============================================
# MAIN AGENT CLASS
# ============================================

class DataClaw:
    def __init__(self):
        init_database()
        self.print_welcome()
    
    def print_welcome(self):
        print("\n" + "="*70)
        print("🗄️ DATACLAW - Personal Library Manager")
        print("="*70)
        print("MANAGE YOUR PERSONAL LIBRARY FOR EACH AGENT")
        print("="*70)
        print("\n📚 COMMANDS:")
        print("  /agents                    - List agents with libraries")
        print("  /list [agent] [category]   - List library contents")
        print("  /add [file] [agent] [cat]  - Add file to library")
        print("  /search [query] [agent]    - Search library")
        print("  /stats                     - Show library statistics")
        print("  /import [dir] [agent]      - Import entire directory")
        print("  /clean [agent] [category]  - Remove duplicates")
        print("  /help, /quit")
        print("="*70)
        print("📁 LIBRARY STRUCTURE:")
        print("   agents/{agent}/library/")
        for cat in LIBRARY_CATEGORIES:
            print(f"     ├── {cat}/")
        print("="*70)
    
    def handle_agents(self):
        libraries = get_agent_libraries()
        print("\n🤖 Agents with Personal Libraries:")
        for lib in libraries:
            categories_str = ", ".join(lib["categories"])
            print(f"  • {lib['agent']} - categories: {categories_str}")
    
    def handle_list(self, args):
        parts = args.split()
        agent = parts[0] if len(parts) > 0 else None
        category = parts[1] if len(parts) > 1 else None
        
        if not agent:
            print("Usage: /list [agent] [category]")
            return
        
        items = list_agent_library(agent, category)
        if items:
            print(f"\n📁 Library for {agent}:")
            for item in items:
                size_kb = round(item["size"] / 1024, 1)
                print(f"  📄 {item['category']}/{item['filename']} ({size_kb} KB)")
        else:
            print(f"No items found for {agent}")
    
    def handle_add(self, args):
        parts = args.split()
        if len(parts) < 3:
            print("Usage: /add [file_path] [agent] [category]")
            print(f"Categories: {', '.join(LIBRARY_CATEGORIES)}")
            return
        
        file_path = parts[0]
        agent = parts[1]
        category = parts[2]
        
        result = add_file(file_path, agent, category)
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ Added to {agent}/{category}: {result['destination']}")
    
    def handle_search(self, args):
        parts = args.split()
        if len(parts) < 1:
            print("Usage: /search [query] [agent]")
            return
        
        query = parts[0]
        agent = parts[1] if len(parts) > 1 else None
        
        results = search_library(query, agent)
        if results:
            print(f"\n🔍 Found {len(results)} results for '{query}':")
            for r in results:
                print(f"  📄 {r['agent']}/{r['category']}/{r['filename']}")
                print(f"     Title: {r['title']} - Added: {r['date'][:10]}")
        else:
            print(f"No results found for '{query}'")
    
    def handle_stats(self):
        stats = get_library_stats()
        print("\n📊 PERSONAL LIBRARY STATISTICS")
        print("=" * 50)
        for agent, agent_stats in stats["agents"].items():
            print(f"\n🤖 {agent}:")
            print(f"   Total files: {agent_stats['total_files']}")
            print(f"   Total size: {agent_stats['total_size_bytes'] / (1024*1024):.2f} MB")
            for cat, cat_stats in agent_stats["categories"].items():
                print(f"     📁 {cat}/: {cat_stats['files']} files ({cat_stats['size_mb']} MB)")
        
        print(f"\n📊 TOTAL: {stats['total_files']} files, {stats['total_size_mb']} MB")
    
    def handle_import(self, args):
        parts = args.split()
        if len(parts) < 2:
            print("Usage: /import [directory] [agent]")
            return
        
        dir_path = Path(parts[0])
        agent = parts[1]
        
        if not dir_path.exists():
            print(f"Directory not found: {dir_path}")
            return
        
        print(f"Importing files from {dir_path} to {agent}...")
        
        # Auto-detect file types and place in appropriate categories
        for file in dir_path.iterdir():
            if file.is_file():
                ext = file.suffix.lower()
                if ext in SUPPORTED_EXTENSIONS["ebook"]:
                    category = "e_books"
                elif ext in SUPPORTED_EXTENSIONS["document"]:
                    category = "research"
                elif ext in SUPPORTED_EXTENSIONS["text"]:
                    category = "notes"
                else:
                    category = "imports"
                
                result = add_file(str(file), agent, category)
                if "error" not in result:
                    print(f"  ✅ Imported: {file.name} → {category}/")
        
        print("Import complete!")
    
    def run(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("\n🗄️ DataClaw> ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/help":
                    self.print_welcome()
                elif cmd == "/agents":
                    self.handle_agents()
                elif cmd == "/stats":
                    self.handle_stats()
                elif cmd.startswith("/list "):
                    self.handle_list(cmd[6:])
                elif cmd.startswith("/add "):
                    self.handle_add(cmd[5:])
                elif cmd.startswith("/search "):
                    self.handle_search(cmd[8:])
                elif cmd.startswith("/import "):
                    self.handle_import(cmd[8:])
                elif cmd == "/clean":
                    print("Clean command - removes duplicates (coming soon)")
                else:
                    print("Unknown command. Try /help")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = DataClaw()
    agent.run()