"""TX Knowledge Base module for Claw-Coder agent"""

import json
import os

class TXKnowledge:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        kb_file = "/home/greg/dev/claw-coder/knowledge_base/tx_docs/knowledge_base.json"
        if os.path.exists(kb_file):
            with open(kb_file, 'r') as f:
                self.docs = json.load(f)
            print(f"✅ TX Knowledge loaded: {len(self.docs)} documents")
        else:
            self.docs = []
            print("⚠️ Run ingestion first")
    
    def ask(self, query):
        """Simple QA interface"""
        results = []
        for doc in self.docs:
            if query.lower() in doc['content'].lower():
                results.append(doc)
        return results[:3] if results else None

# For use in other scripts
if __name__ == "__main__":
    kb = TXKnowledge()
    print(f"Ready with {len(kb.docs)} documents")
