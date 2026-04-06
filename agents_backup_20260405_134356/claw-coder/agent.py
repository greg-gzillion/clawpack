#!/usr/bin/env python3
"""
Claw-Coder Agent - Dual-repo awareness for PhoenixPME
"""

import os
import json
from pathlib import Path

class ClawAgent:
    def __init__(self):
        self.docs_path = Path("/home/greg/dev/TXdocumentation")
        self.project_path = Path("/home/greg/dev/TX")
        self.agent_path = Path("/home/greg/dev/claw-coder")
        
        # Load or create knowledge base
        self.kb_file = self.agent_path / "knowledge_base.json"
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self):
        if self.kb_file.exists():
            with open(self.kb_file, 'r') as f:
                return json.load(f)
        return {'docs_index': [], 'project_index': [], 'compliance_notes': []}
    
    def _save_knowledge(self):
        with open(self.kb_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def index_docs(self):
        """Index all TX documentation"""
        print("\n📖 Indexing TXdocumentation...")
        docs_index = []
        
        for md_file in self.docs_path.rglob("*.md"):
            if 'phoenixpme' in str(md_file).lower():
                try:
                    with open(md_file, 'r') as f:
                        content = f.read()
                    docs_index.append({
                        'path': str(md_file.relative_to(self.docs_path)),
                        'size': len(content),
                        'preview': content[:200]
                    })
                except:
                    pass
        
        self.knowledge['docs_index'] = docs_index
        self._save_knowledge()
        print(f"   Indexed {len(docs_index)} documentation files")
        return docs_index
    
    def scan_project(self):
        """Scan TX project for implementation"""
        print("\n💻 Scanning TX project...")
        project_index = []
        
        # Focus on auction-related files
        for rust_file in self.project_path.rglob("*.rs"):
            if 'auction' in str(rust_file).lower() or 'phoenix' in str(rust_file).lower():
                try:
                    with open(rust_file, 'r') as f:
                        content = f.read()
                    project_index.append({
                        'path': str(rust_file.relative_to(self.project_path)),
                        'type': 'contract',
                        'functions': self._extract_functions(content)
                    })
                except:
                    pass
        
        # Also scan scripts
        for sh_file in self.project_path.rglob("*.sh"):
            if 'test' in str(sh_file).lower() or 'deploy' in str(sh_file).lower():
                project_index.append({
                    'path': str(sh_file.relative_to(self.project_path)),
                    'type': 'script'
                })
        
        self.knowledge['project_index'] = project_index
        self._save_knowledge()
        print(f"   Found {len(project_index)} auction-related files")
        return project_index
    
    def _extract_functions(self, content):
        """Extract function names from Rust code"""
        import re
        functions = re.findall(r'fn\s+(\w+)\s*\(', content)
        return functions[:10]
    
    def check_compliance(self):
        """Check if project follows documentation"""
        print("\n🔍 Compliance Check")
        print("=" * 40)
        
        # Check for required components
        required = ['escrow', 'fee', 'reputation', 'collateral']
        found = []
        
        for item in self.knowledge.get('project_index', []):
            for req in required:
                if req in item['path'].lower():
                    found.append(req)
        
        print("\nRequired Components:")
        for req in required:
            status = "✅" if req in found else "❌"
            print(f"  {status} {req.upper()}")
        
        # Test addresses needed
        print("\n🏦 Test Addresses Required:")
        print("  • Buyer wallet")
        print("  • Seller wallet")
        print("  • Escrow wallet")
        print("  • Fee collector wallet")
        
        return found
    
    def interactive(self):
        """Main interactive loop"""
        print("\n" + "=" * 60)
        print("🦞 Claw-Coder Agent - PhoenixPME Assistant")
        print("=" * 60)
        print("\nI maintain awareness of TWO repos:")
        print("  📖 TXdocumentation - Rules & standards")
        print("  💻 TX Project - Your implementation")
        
        while True:
            print("\nCommands:")
            print("  • index     - Index documentation")
            print("  • scan      - Scan project files")
            print("  • check     - Check compliance")
            print("  • addresses - Show test addresses needed")
            print("  • status    - Show what I know")
            print("  • exit      - Quit")
            
            cmd = input("\n🦞 > ").strip().lower()
            
            if cmd == 'exit':
                print("\n👋 Keeping PhoenixPME compliant!")
                break
            elif cmd == 'index':
                self.index_docs()
            elif cmd == 'scan':
                self.scan_project()
            elif cmd == 'check':
                self.check_compliance()
            elif cmd == 'addresses':
                print("\n🏦 Test Addresses to Generate:")
                print("  txd keys add buyer_wallet")
                print("  txd keys add seller_wallet")
                print("  txd keys add escrow_wallet")
                print("  txd keys add fee_collector")
            elif cmd == 'status':
                print(f"\n📊 Status:")
                print(f"  Docs indexed: {len(self.knowledge.get('docs_index', []))}")
                print(f"  Project files: {len(self.knowledge.get('project_index', []))}")
            else:
                print("Unknown command")

if __name__ == "__main__":
    agent = ClawAgent()
    agent.interactive()
