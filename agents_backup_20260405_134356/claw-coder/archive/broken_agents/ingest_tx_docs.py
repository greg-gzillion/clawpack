#!/usr/bin/env python3
"""
TX Documentation Ingestion Script for Claw-Coder Agent
Loads and processes all TXdocumentation files for AI training
"""

import os
import json
import glob
from pathlib import Path
from typing import Dict, List
import hashlib

class TXDocumentationLoader:
    def __init__(self, docs_path: str):
        self.docs_path = Path(docs_path)
        self.knowledge_base = []
        
    def load_all_markdown_files(self) -> List[Dict]:
        """Load all markdown files from TXdocumentation"""
        md_files = glob.glob(str(self.docs_path / "**/*.md"), recursive=True)
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                rel_path = Path(file_path).relative_to(self.docs_path)
                
                self.knowledge_base.append({
                    'file': str(rel_path),
                    'category': self._get_category(rel_path),
                    'content': content,
                    'size': len(content),
                    'hash': hashlib.md5(content.encode()).hexdigest()
                })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
        return self.knowledge_base
    
    def _get_category(self, file_path: Path) -> str:
        """Determine document category from path"""
        path_str = str(file_path)
        
        if 'security' in path_str:
            return 'security'
        elif 'regulatory' in path_str:
            return 'regulatory'
        elif 'help' in path_str:
            return 'user_guides'
        elif 'support' in path_str:
            return 'support'
        elif 'tutorials' in path_str:
            return 'tutorials'
        elif 'nodes' in path_str:
            return 'validator_ops'
        elif 'modules' in path_str:
            return 'modules'
        elif 'ecosystem' in path_str:
            return 'ecosystem'
        else:
            return 'general'
    
    def create_vector_database(self, output_path: str):
        """Create a simple vector database for semantic search"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        # Extract content for vectorization
        documents = [doc['content'][:5000] for doc in self.knowledge_base]  # Limit length
        file_names = [doc['file'] for doc in self.knowledge_base]
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        vectors = vectorizer.fit_transform(documents)
        
        # Save vectorizer and vectors
        import joblib
        joblib.dump(vectorizer, f"{output_path}/vectorizer.pkl")
        np.save(f"{output_path}/vectors.npy", vectors.toarray())
        
        # Save metadata
        with open(f"{output_path}/metadata.json", 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
        
        print(f"✅ Vector database created at {output_path}")
        print(f"   - {len(self.knowledge_base)} documents indexed")
        print(f"   - {vectors.shape[1]} features")
    
    def create_training_data(self, output_path: str):
        """Create training data for fine-tuning"""
        training_data = []
        
        for doc in self.knowledge_base:
            # Create question-answer pairs
            training_data.append({
                'instruction': f"What does the TX documentation say about {doc['category']}?",
                'input': f"File: {doc['file']}\nCategory: {doc['category']}",
                'output': doc['content'][:2000]  # Truncate for training
            })
            
            # Extract key topics
            lines = doc['content'].split('\n')
            for i, line in enumerate(lines):
                if line.startswith('#') or line.startswith('##'):
                    topic = line.strip('#').strip()
                    context = '\n'.join(lines[max(0,i-2):min(len(lines), i+5)])
                    training_data.append({
                        'instruction': f"Explain {topic} in TX blockchain",
                        'input': f"From {doc['file']}",
                        'output': context[:1000]
                    })
        
        # Save training data
        with open(f"{output_path}/training_data.json", 'w') as f:
            json.dump(training_data[:5000], f, indent=2)  # Limit size
        
        print(f"✅ Training data created: {len(training_data[:5000])} samples")
    
    def create_knowledge_graph(self, output_path: str):
        """Create a knowledge graph of TX concepts"""
        import re
        
        concepts = {}
        
        for doc in self.knowledge_base:
            content = doc['content']
            
            # Extract key concepts
            concepts_found = re.findall(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)*)\b', content)
            
            for concept in concepts_found:
                if len(concept) > 3 and concept not in concepts:
                    concepts[concept] = {
                        'mentions': 1,
                        'files': [doc['file']]
                    }
                elif concept in concepts:
                    concepts[concept]['mentions'] += 1
                    if doc['file'] not in concepts[concept]['files']:
                        concepts[concept]['files'].append(doc['file'])
        
        # Save knowledge graph
        with open(f"{output_path}/knowledge_graph.json", 'w') as f:
            json.dump(concepts, f, indent=2)
        
        print(f"✅ Knowledge graph created: {len(concepts)} concepts")

def main():
    # Path to TXdocumentation (adjust if needed)
    tx_docs_path = "/home/greg/dev/TXdocumentation"
    
    # Create output directory
    output_dir = "/home/greg/dev/claw-coder/knowledge_base/tx_docs"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🚀 Loading TX Documentation...")
    loader = TXDocumentationLoader(tx_docs_path)
    
    print("📚 Loading all markdown files...")
    docs = loader.load_all_markdown_files()
    print(f"   Loaded {len(docs)} documents")
    
    print("\n🔍 Creating vector database...")
    loader.create_vector_database(output_dir)
    
    print("\n📝 Creating training data...")
    loader.create_training_data(output_dir)
    
    print("\n🕸️ Creating knowledge graph...")
    loader.create_knowledge_graph(output_dir)
    
    print("\n✅ Documentation ingestion complete!")
    print(f"📁 Knowledge base saved to: {output_dir}")

if __name__ == "__main__":
    main()
