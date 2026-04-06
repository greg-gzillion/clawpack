"""Neural memory network for pattern recognition across agents"""
import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

class NeuralMemory:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self._init_neural_tables()
    
    def _init_neural_tables(self):
        # Pattern recognition table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS neural_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_hash TEXT UNIQUE,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence REAL DEFAULT 0.5,
                occurrences INTEGER DEFAULT 1,
                last_seen TEXT,
                detected_by TEXT
            )
        """)
        
        # Agent embeddings (vector representations)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_embeddings (
                agent TEXT PRIMARY KEY,
                embedding_vector TEXT,
                expertise_domain TEXT,
                learning_rate REAL DEFAULT 0.01,
                last_update TEXT
            )
        """)
        
        # Knowledge graph edges
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_edges (
                source TEXT,
                target TEXT,
                relationship TEXT,
                weight REAL DEFAULT 1.0,
                timestamp TEXT,
                UNIQUE(source, target, relationship)
            )
        """)
        self.conn.commit()
    
    def detect_pattern(self, data, data_type="code"):
        """Detect patterns in new data"""
        pattern_hash = hashlib.md5(str(data).encode()).hexdigest()
        
        # Check if pattern exists
        self.cursor.execute("SELECT id, confidence, occurrences FROM neural_patterns WHERE pattern_hash = ?", (pattern_hash,))
        existing = self.cursor.fetchone()
        
        if existing:
            # Update existing pattern
            new_confidence = min(1.0, existing[1] + 0.05)
            self.cursor.execute("""
                UPDATE neural_patterns 
                SET confidence = ?, occurrences = occurrences + 1, last_seen = ?
                WHERE pattern_hash = ?
            """, (new_confidence, datetime.now().isoformat(), pattern_hash))
            return {"pattern_id": existing[0], "new": False, "confidence": new_confidence}
        else:
            # Create new pattern
            self.cursor.execute("""
                INSERT INTO neural_patterns (pattern_hash, pattern_type, pattern_data, last_seen, detected_by)
                VALUES (?, ?, ?, ?, ?)
            """, (pattern_hash, data_type, str(data)[:500], datetime.now().isoformat(), "system"))
            self.conn.commit()
            return {"pattern_id": self.cursor.lastrowid, "new": True, "confidence": 0.5}
    
    def create_embedding(self, agent, expertise, embedding=None):
        """Create vector embedding for agent"""
        if embedding is None:
            # Create simple embedding from expertise keywords
            keywords = expertise.lower().split()
            embedding = [hash(k) % 100 / 100 for k in keywords[:10]]  # Simple vector
            embedding = embedding + [0] * (10 - len(embedding))
        
        self.cursor.execute("""
            INSERT OR REPLACE INTO agent_embeddings (agent, embedding_vector, expertise_domain, last_update)
            VALUES (?, ?, ?, ?)
        """, (agent, json.dumps(embedding), expertise, datetime.now().isoformat()))
        self.conn.commit()
    
    def find_similar_agents(self, agent, top_k=3):
        """Find agents with similar expertise"""
        self.cursor.execute("SELECT embedding_vector FROM agent_embeddings WHERE agent = ?", (agent,))
        source_vec = json.loads(self.cursor.fetchone()[0]) if self.cursor.fetchone() else None
        
        if not source_vec:
            return []
        
        self.cursor.execute("SELECT agent, embedding_vector FROM agent_embeddings WHERE agent != ?", (agent,))
        similarities = []
        for other_agent, vec_json in self.cursor.fetchall():
            other_vec = json.loads(vec_json)
            # Cosine similarity
            dot = sum(a*b for a,b in zip(source_vec, other_vec))
            similarities.append((other_agent, dot))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def add_knowledge_edge(self, source, target, relationship):
        """Add relationship between knowledge items"""
        self.cursor.execute("""
            INSERT INTO knowledge_edges (source, target, relationship, timestamp)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(source, target, relationship) DO UPDATE SET
                weight = weight + 0.1,
                timestamp = ?
        """, (source, target, relationship, datetime.now().isoformat(), datetime.now().isoformat()))
        self.conn.commit()
    
    def get_knowledge_graph(self, node, depth=2):
        """Retrieve connected knowledge"""
        results = []
        for d in range(depth):
            self.cursor.execute("""
                SELECT source, target, relationship FROM knowledge_edges 
                WHERE source = ? OR target = ?
            """, (node, node))
            results.extend(self.cursor.fetchall())
        return results

print("✅ Neural memory system initialized")
