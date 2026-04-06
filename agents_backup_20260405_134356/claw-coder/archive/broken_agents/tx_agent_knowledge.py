"""
TX Blockchain Knowledge Base for Claw-Coder Agent
Provides semantic search and document retrieval for TX documentation
"""

import json
import os
from typing import List, Dict, Optional

class TXAgentKnowledge:
    """Knowledge base for TX blockchain documentation"""
    
    def __init__(self):
        self.kb_file = "/home/greg/dev/claw-coder/knowledge_base/tx_docs/knowledge_base.json"
        self.docs = []
        self.index = {}
        self._load()
    
    def _load(self):
        """Load the knowledge base"""
        if os.path.exists(self.kb_file):
            with open(self.kb_file, 'r', encoding='utf-8') as f:
                self.docs = json.load(f)
            self.index = {doc['file']: doc for doc in self.docs}
            print(f"✅ TX Knowledge: {len(self.docs)} documents loaded")
        else:
            print("⚠️ Run ingestion first: python3 simple_ingest.py")
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search documentation by keyword"""
        query_lower = query.lower()
        results = []
        
        for doc in self.docs:
            if (query_lower in doc['file'].lower() or 
                query_lower in doc['content'].lower()):
                score = doc['content'].lower().count(query_lower)
                results.append((score, doc))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results][:limit]
    
    def get_document(self, filepath: str) -> Optional[Dict]:
        """Get a specific document by filepath"""
        return self.index.get(filepath)
    
    def get_category(self, category: str) -> List[Dict]:
        """Get all documents in a category"""
        return [doc for doc in self.docs if doc['category'] == category]
    
    def get_categories(self) -> Dict:
        """Get all categories with counts"""
        cats = {}
        for doc in self.docs:
            cats[doc['category']] = cats.get(doc['category'], 0) + 1
        return cats
    
    def summarize_topic(self, topic: str) -> str:
        """Get a summary of a specific topic"""
        results = self.search(topic, limit=3)
        if not results:
            return f"No information found about '{topic}'"
        
        summary = f"📚 About {topic.upper()}:\n\n"
        for i, doc in enumerate(results, 1):
            summary += f"{i}. From {doc['file']}:\n"
            # Get first 500 chars
            content = doc['content'][:500].replace('\n', ' ')
            summary += f"   {content}...\n\n"
        return summary
    
    def answer(self, question: str) -> str:
        """Simple QA based on documentation"""
        keywords = question.lower().replace('?', '').split()
        
        # Find most relevant document
        best_match = None
        best_score = 0
        
        for doc in self.docs:
            score = sum(1 for kw in keywords if kw in doc['content'].lower())
            if score > best_score:
                best_score = score
                best_match = doc
        
        if best_match and best_score > 0:
            # Extract relevant paragraph
            lines = best_match['content'].split('\n')
            answer_lines = []
            for line in lines:
                if any(kw in line.lower() for kw in keywords[:3]):
                    answer_lines.append(line.strip())
            
            if answer_lines:
                return f"Based on {best_match['file']}:\n" + "\n".join(answer_lines[:3])
            else:
                return f"From {best_match['file']}:\n{best_match['content'][:500]}"
        
        return "I couldn't find an answer in the TX documentation."

# Example usage
if __name__ == "__main__":
    kb = TXAgentKnowledge()
    
    print("\n" + "="*60)
    print("🤖 Claw-Coder TX Knowledge Base")
    print("="*60)
    
    # Test queries
    print("\n🔍 Testing queries:\n")
    
    topics = ["smart contracts", "validator", "staking", "governance"]
    for topic in topics:
        print(f"\n📖 {topic.upper()}:")
        results = kb.search(topic, limit=2)
        for r in results:
            print(f"   - {r['file']}")
    
    print("\n" + "="*60)
    print("✅ Knowledge base ready for Claw-Coder agent!")
