#!/usr/bin/env python3
"""
DATACLAW - Local/Personal Citation & Reference Manager

PURPOSE: Manages YOUR personal references, e-books, and research notes
RELATIONSHIP TO WEBCLAW: 
   - Webclaw = GLOBAL standard citations (Bluebook, APA, MLA, Chicago)
   - DataClaw = LOCAL personal references (your books, your notes, your citations)

This agent is OPTIONAL and does NOT interfere with Webclaw's global citation system.
All standard citations should come from Webclaw. DataClaw is for your personal library.
"""

import sys
import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ============================================
# PATHS
# ============================================
AGENT_DIR = Path(__file__).parent
ROOT_DIR = AGENT_DIR.parent.parent
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
DATACLAW_DB = AGENT_DIR / "personal_library.db"
LIBRARY_DIR = AGENT_DIR / "my_library"
NOTES_DIR = AGENT_DIR / "my_notes"

# Create directories
LIBRARY_DIR.mkdir(exist_ok=True)
NOTES_DIR.mkdir(exist_ok=True)

# ============================================
# DATABASE SCHEMA (Personal only)
# ============================================

def init_dataclaw_db():
    """Initialize personal reference database"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    # My personal book collection
    c.execute('''CREATE TABLE IF NOT EXISTS my_books
                 (id INTEGER PRIMARY KEY,
                  title TEXT UNIQUE,
                  author TEXT,
                  isbn TEXT,
                  publisher TEXT,
                  year TEXT,
                  category TEXT,
                  file_path TEXT,
                  notes TEXT,
                  tags TEXT,
                  added_date TEXT)''')
    
    # My saved citations (personal use)
    c.execute('''CREATE TABLE IF NOT EXISTS my_citations
                 (id INTEGER PRIMARY KEY,
                  title TEXT,
                  citation_text TEXT,
                  citation_style TEXT,
                  source TEXT,
                  notes TEXT,
                  saved_date TEXT)''')
    
    # My research notes
    c.execute('''CREATE TABLE IF NOT EXISTS my_notes
                 (id INTEGER PRIMARY KEY,
                  title TEXT UNIQUE,
                  content TEXT,
                  tags TEXT,
                  created_date TEXT,
                  modified_date TEXT)''')
    
    # My reading list
    c.execute('''CREATE TABLE IF NOT EXISTS my_reading_list
                 (id INTEGER PRIMARY KEY,
                  title TEXT UNIQUE,
                  author TEXT,
                  priority INTEGER DEFAULT 1,
                  status TEXT DEFAULT 'pending',
                  notes TEXT,
                  added_date TEXT)''')
    
    conn.commit()
    conn.close()

# ============================================
# PERSONAL REFERENCE FUNCTIONS
# ============================================

def add_personal_book(title, author, **kwargs):
    """Add a book to my personal library"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    try:
        c.execute('''INSERT OR REPLACE INTO my_books
                     (title, author, isbn, publisher, year, category, file_path, notes, tags, added_date)
                     VALUES (?,?,?,?,?,?,?,?,?,?)''',
                  (title, author, kwargs.get('isbn', ''), kwargs.get('publisher', ''),
                   kwargs.get('year', ''), kwargs.get('category', 'general'),
                   kwargs.get('file_path', ''), kwargs.get('notes', ''), kwargs.get('tags', ''),
                   datetime.now().isoformat()))
        conn.commit()
        print(f"📚 Added to personal library: {title}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def list_my_books(category=None):
    """List books in my personal library"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    if category:
        c.execute("SELECT title, author, year FROM my_books WHERE category = ? ORDER BY title", (category,))
    else:
        c.execute("SELECT title, author, year FROM my_books ORDER BY title")
    
    results = c.fetchall()
    conn.close()
    
    if results:
        print(f"\n📚 My Personal Library ({len(results)} books):")
        for title, author, year in results:
            print(f"  • {title} - {author} ({year})")
    else:
        print("\n📚 No books in personal library yet")
    return results

def save_personal_citation(title, citation_text, citation_style, notes=""):
    """Save a citation to my personal collection"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    try:
        c.execute('''INSERT INTO my_citations
                     (title, citation_text, citation_style, notes, saved_date)
                     VALUES (?,?,?,?,?)''',
                  (title, citation_text, citation_style, notes, datetime.now().isoformat()))
        conn.commit()
        print(f"📝 Saved personal citation: {title}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def list_my_citations():
    """List my saved personal citations"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    c.execute("SELECT title, citation_style, saved_date FROM my_citations ORDER BY saved_date DESC LIMIT 20")
    results = c.fetchall()
    conn.close()
    
    if results:
        print(f"\n📝 My Saved Citations ({len(results)}):")
        for title, style, date in results:
            print(f"  • {title} ({style}) - {date[:10]}")
    else:
        print("\n📝 No saved citations yet")
    return results

def add_note(title, content, tags=""):
    """Add a personal research note"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    try:
        c.execute('''INSERT OR REPLACE INTO my_notes
                     (title, content, tags, created_date, modified_date)
                     VALUES (?,?,?,?,?)''',
                  (title, content, tags, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        
        # Also save as markdown file
        note_file = NOTES_DIR / f"{title.replace(' ', '_')}.md"
        note_file.write_text(f"# {title}\n\nCreated: {datetime.now()}\nTags: {tags}\n\n{content}")
        
        print(f"📝 Saved personal note: {title}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def show_stats():
    """Show personal library statistics"""
    conn = sqlite3.connect(str(DATACLAW_DB))
    c = conn.cursor()
    
    print("\n📊 DATACLAW - Personal Library Statistics")
    print("-" * 40)
    
    tables = ['my_books', 'my_citations', 'my_notes', 'my_reading_list']
    for table in tables:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"  • {table}: {count} items")
    
    conn.close()

# ============================================
# MAIN AGENT CLASS
# ============================================

class DataClaw:
    def __init__(self):
        init_dataclaw_db()
        self.print_welcome()
    
    def print_welcome(self):
        print("\n" + "="*70)
        print("🗄️ DATACLAW - Personal Citation & Reference Manager")
        print("="*70)
        print("PURPOSE: Manage YOUR personal references and research")
        print("="*70)
        print("\n📚 COMMANDS (Personal Library Only):")
        print("  /book add \"Title\" \"Author\"     - Add book to my library")
        print("  /book list [category]           - List my books")
        print("  /cite save \"Title\" \"Citation\"  - Save personal citation")
        print("  /cite list                      - List my citations")
        print("  /note add \"Title\"              - Add research note")
        print("  /note list                      - List my notes")
        print("  /reading add \"Title\" \"Author\"  - Add to reading list")
        print("  /reading list                   - Show reading list")
        print("  /stats                          - Show library stats")
        print("  /help, /quit")
        print("="*70)
        print("💡 NOTE: For STANDARD citations (Bluebook, APA, MLA, Chicago)")
        print("   use Webclaw references or ask Unified Controller")
        print(f"📁 My Library: {LIBRARY_DIR}")
        print(f"📁 My Notes: {NOTES_DIR}")
        print("="*70)
    
    def handle_book_add(self, args):
        """Add a book: /book add \"Title\" \"Author\" category=law isbn=123"""
        import re
        # Parse quoted strings
        parts = re.findall(r'"([^"]*)"', args)
        if len(parts) < 2:
            print("Usage: /book add \"Title\" \"Author\" [category=value] [isbn=value]")
            return
        
        title = parts[0]
        author = parts[1]
        
        # Parse optional key=value parameters
        kwargs = {}
        remaining = args
        for part in parts:
            remaining = remaining.replace(f'"{part}"', '')
        
        for pair in remaining.split():
            if '=' in pair:
                key, value = pair.split('=', 1)
                kwargs[key.lower()] = value
        
        add_personal_book(title, author, **kwargs)
    
    def handle_book_list(self, category=None):
        list_my_books(category)
    
    def handle_cite_save(self, args):
        """Save citation: /cite save \"Title\" \"Citation\" style=bluebook notes=\"my notes\" """
        import re
        parts = re.findall(r'"([^"]*)"', args)
        if len(parts) < 2:
            print("Usage: /cite save \"Title\" \"Citation\" [style=bluebook] [notes=...]")
            return
        
        title = parts[0]
        citation = parts[1]
        
        # Parse options
        style = "bluebook"
        notes = ""
        remaining = args
        for part in parts:
            remaining = remaining.replace(f'"{part}"', '')
        
        for pair in remaining.split():
            if '=' in pair:
                key, value = pair.split('=', 1)
                if key == 'style':
                    style = value
                elif key == 'notes':
                    notes = value
        
        save_personal_citation(title, citation, style, notes)
    
    def handle_cite_list(self):
        list_my_citations()
    
    def handle_note_add(self, args):
        """Add note: /note add \"Title\" tags=research"""
        import re
        parts = re.findall(r'"([^"]*)"', args)
        if len(parts) < 1:
            print("Usage: /note add \"Title\" [tags=value]")
            return
        
        title = parts[0]
        
        # Parse tags
        tags = ""
        remaining = args
        for part in parts:
            remaining = remaining.replace(f'"{part}"', '')
        
        for pair in remaining.split():
            if '=' in pair:
                key, value = pair.split('=', 1)
                if key == 'tags':
                    tags = value
        
        print(f"Enter note content (end with Ctrl+Z on new line):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        content = '\n'.join(lines)
        add_note(title, content, tags)
    
    def handle_note_list(self):
        conn = sqlite3.connect(str(DATACLAW_DB))
        c = conn.cursor()
        c.execute("SELECT title, created_date FROM my_notes ORDER BY created_date DESC")
        results = c.fetchall()
        conn.close()
        
        if results:
            print(f"\n📝 My Notes ({len(results)}):")
            for title, date in results:
                print(f"  • {title} - {date[:10]}")
        else:
            print("\n📝 No notes yet")
    
    def handle_reading_add(self, args):
        """Add to reading list: /reading add \"Title\" \"Author\" priority=1"""
        import re
        parts = re.findall(r'"([^"]*)"', args)
        if len(parts) < 2:
            print("Usage: /reading add \"Title\" \"Author\" [priority=1-5]")
            return
        
        title = parts[0]
        author = parts[1]
        
        priority = 1
        remaining = args
        for part in parts:
            remaining = remaining.replace(f'"{part}"', '')
        
        for pair in remaining.split():
            if '=' in pair:
                key, value = pair.split('=', 1)
                if key == 'priority':
                    priority = int(value)
        
        conn = sqlite3.connect(str(DATACLAW_DB))
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO my_reading_list
                     (title, author, priority, added_date)
                     VALUES (?,?,?,?)''',
                  (title, author, priority, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        print(f"📖 Added to reading list: {title}")
    
    def handle_reading_list(self):
        conn = sqlite3.connect(str(DATACLAW_DB))
        c = conn.cursor()
        c.execute("SELECT title, author, priority, status FROM my_reading_list ORDER BY priority")
        results = c.fetchall()
        conn.close()
        
        if results:
            print(f"\n📖 My Reading List:")
            for title, author, priority, status in results:
                stars = "⭐" * priority
                print(f"  • {stars} {title} - {author} ({status})")
        else:
            print("\n📖 Reading list empty")
    
    def run(self):
        self.print_welcome()
        while True:
            try:
                cmd = input("\n🗄️ DataClaw> ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye! Happy researching!")
                    break
                elif cmd == "/help":
                    self.print_welcome()
                elif cmd == "/stats":
                    show_stats()
                elif cmd.startswith("/book add "):
                    self.handle_book_add(cmd[9:])
                elif cmd.startswith("/book list"):
                    parts = cmd.split()
                    category = parts[2] if len(parts) > 2 else None
                    self.handle_book_list(category)
                elif cmd.startswith("/cite save "):
                    self.handle_cite_save(cmd[10:])
                elif cmd == "/cite list":
                    self.handle_cite_list()
                elif cmd.startswith("/note add "):
                    self.handle_note_add(cmd[9:])
                elif cmd == "/note list":
                    self.handle_note_list()
                elif cmd.startswith("/reading add "):
                    self.handle_reading_add(cmd[12:])
                elif cmd == "/reading list":
                    self.handle_reading_list()
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