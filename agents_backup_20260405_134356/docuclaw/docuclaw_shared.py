import os
#!/usr/bin/env python3
# docuclaw_shared.py - Document Writing Assistant
# Part of Clawpack - Cross-Learning AI Agent Ecosystem

import requests
import sqlite3
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY")


class SharedMemory:
    def __init__(self):
        self.path = Path.home() / ".claw_memory" / "shared_memory.db"
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(str(self.path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE,
                content TEXT,
                doc_type TEXT,
                timestamp TEXT,
                source_agent TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def save_document(self, title: str, content: str, doc_type: str, agent: str = "Docuclaw"):
        conn = sqlite3.connect(str(self.path))
        conn.execute("INSERT OR REPLACE INTO documents (title, content, doc_type, timestamp, source_agent) VALUES (?, ?, ?, ?, ?)",
                     (title, content, doc_type, datetime.now().isoformat(), agent))
        conn.commit()
        conn.close()
        print("💡 [Document saved to shared memory]")
    
    def get_document(self, title: str) -> Optional[str]:
        conn = sqlite3.connect(str(self.path))
        cur = conn.execute("SELECT content FROM documents WHERE title = ?", (title,))
        row = cur.fetchone()
        conn.close()
        if row:
            return row[0]
        return None
    
    def list_documents(self) -> List[str]:
        conn = sqlite3.connect(str(self.path))
        cur = conn.execute("SELECT title, doc_type, timestamp FROM documents ORDER BY timestamp DESC")
        rows = cur.fetchall()
        conn.close()
        return rows


class Docuclaw:
    def __init__(self):
        self.name = "Docuclaw"
        self.memory = SharedMemory()
        self.docs_path = Path.home() / ".claw_memory" / "documents"
        self.docs_path.mkdir(parents=True, exist_ok=True)
        self._print_welcome()
    
    def _print_welcome(self):
        print("\n" + "="*70)
        print("📝 DOCUCLAW - Document Writing Assistant")
        print("="*70)
        print("\n📚 COMMANDS:")
        print("  /write [topic]       - Write a document on a topic")
        print("  /summarize [text]    - Summarize text")
        print("  /outline [topic]     - Create document outline")
        print("  /proof [text]        - Proofread and correct grammar")
        print("  /format [text]       - Format as markdown")
        print("  /save [title]        - Save current document")
        print("  /load [title]        - Load saved document")
        print("  /list                - List saved documents")
        print("  /export [title]      - Export to file")
        print("  /help, /quit")
        print("="*70)
    
    def _call_ai(self, prompt: str) -> str:
        """Call AI API"""
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def write_document(self, topic: str) -> str:
        """Generate a document on a topic"""
        prompt = f"""Write a well-structured document about: {topic}

Include:
1. Title
2. Introduction
3. Key points (3-5 sections)
4. Conclusion
5. References (if applicable)

Format with markdown for headings, bullet points, and emphasis."""
        
        print(f"📝 Writing document about '{topic}'...")
        return self._call_ai(prompt)
    
    def summarize(self, text: str) -> str:
        """Summarize text"""
        prompt = f"""Summarize the following text concisely:

{text[:3000]}

Provide:
- Main idea (1 sentence)
- Key points (3-5 bullet points)
- Conclusion (1 sentence)"""
        
        print("📋 Summarizing...")
        return self._call_ai(prompt)
    
    def create_outline(self, topic: str) -> str:
        """Create document outline"""
        prompt = f"""Create a detailed outline for a document about: {topic}

Include:
- Title suggestion
- Chapter/section headings (with Roman numerals I, II, III...)
- Subsection ideas (A, B, C...)
- Key points to cover under each section"""
        
        print("📑 Creating outline...")
        return self._call_ai(prompt)
    
    def proofread(self, text: str) -> str:
        """Proofread and correct text"""
        prompt = f"""Proofread and correct the following text:

{text[:3000]}

Correct:
- Grammar errors
- Spelling mistakes
- Punctuation issues
- Style improvements

Return the corrected version only, with changes explained in brackets."""
        
        print("🔍 Proofreading...")
        return self._call_ai(prompt)
    
    def format_markdown(self, text: str) -> str:
        """Format text as markdown"""
        prompt = f"""Convert the following text to proper markdown format:

{text[:3000]}

Add:
- Headings (# ## ###)
- Bullet points (- or *)
- Bold/italic (**text** or *text*)
- Code blocks (```) if code detected
- Links [text](url) if URLs present

Return only the markdown formatted version."""
        
        print("🎨 Formatting as markdown...")
        return self._call_ai(prompt)
    
    def save_document(self, title: str, content: str):
        """Save document to shared memory and file"""
        # Save to shared memory
        self.memory.save_document(title, content, "document", self.name)
        
        # Save to file
        filename = self.docs_path / f"{title.replace(' ', '_')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"*Generated by Docuclaw on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(content)
        
        print(f"✅ Document saved to: {filename}")
        return str(filename)
    
    def load_document(self, title: str) -> Optional[str]:
        """Load document from shared memory"""
        content = self.memory.get_document(title)
        if content:
            print(f"📖 Loaded document: {title}")
            return content
        print(f"❌ Document not found: {title}")
        return None
    
    def list_documents(self) -> List[tuple]:
        """List all saved documents"""
        return self.memory.list_documents()
    
    def export_document(self, title: str) -> str:
        """Export document to file"""
        content = self.memory.get_document(title)
        if content:
            filename = self.docs_path / f"{title.replace(' ', '_')}_export.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return str(filename)
        return None
    
    def run(self):
        current_doc = ""
        
        while True:
            cmd = input("\n📝 Docuclaw> ").strip()
            if not cmd:
                continue
            if cmd == '/quit':
                break
            if cmd == '/help':
                self._print_welcome()
                continue
            
            # /write
            if cmd.startswith('/write '):
                topic = cmd[7:]
                result = self.write_document(topic)
                print("\n" + "="*50)
                print(result)
                print("="*50)
                current_doc = result
                continue
            
            # /summarize
            if cmd.startswith('/summarize '):
                text = cmd[11:]
                result = self.summarize(text)
                print("\n" + "="*50)
                print(result)
                print("="*50)
                continue
            
            # /outline
            if cmd.startswith('/outline '):
                topic = cmd[9:]
                result = self.create_outline(topic)
                print("\n" + "="*50)
                print(result)
                print("="*50)
                continue
            
            # /proof
            if cmd.startswith('/proof '):
                text = cmd[7:]
                result = self.proofread(text)
                print("\n" + "="*50)
                print(result)
                print("="*50)
                continue
            
            # /format
            if cmd.startswith('/format '):
                text = cmd[8:]
                result = self.format_markdown(text)
                print("\n" + "="*50)
                print(result)
                print("="*50)
                continue
            
            # /save
            if cmd.startswith('/save '):
                title = cmd[6:]
                if current_doc:
                    filename = self.save_document(title, current_doc)
                    print(f"✅ Saved to {filename}")
                else:
                    print("❌ No document to save. Write one first with /write")
                continue
            
            # /load
            if cmd.startswith('/load '):
                title = cmd[6:]
                content = self.load_document(title)
                if content:
                    current_doc = content
                    print("\n" + "="*50)
                    print(content[:500] + ("..." if len(content) > 500 else ""))
                    print("="*50)
                continue
            
            # /list
            if cmd == '/list':
                docs = self.list_documents()
                if docs:
                    print("\n📚 SAVED DOCUMENTS:")
                    for title, doc_type, timestamp in docs:
                        print(f"  📄 {title} ({doc_type}) - {timestamp[:16]}")
                else:
                    print("No documents found.")
                continue
            
            # /export
            if cmd.startswith('/export '):
                title = cmd[8:]
                filename = self.export_document(title)
                if filename:
                    print(f"✅ Exported to: {filename}")
                else:
                    print(f"❌ Document not found: {title}")
                continue
            
            print("Unknown command. Type /help")


def main():
    agent = Docuclaw()
    agent.run()


if __name__ == "__main__":
    main()