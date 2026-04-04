#!/usr/bin/env python3
"""
Audit Log for AgentForLaw - Records all law lookups and document drafts
"""

import sqlite3
from datetime import datetime
from pathlib import Path

AUDIT_DIR = Path.home() / ".claw_audit"
AUDIT_DIR.mkdir(exist_ok=True)
AUDIT_DB = AUDIT_DIR / "audit.db"

def init_audit():
    conn = sqlite3.connect(str(AUDIT_DB))
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS law_queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        query_type TEXT,
        query TEXT,
        result TEXT,
        user TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS document_drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        doc_type TEXT,
        parties TEXT,
        provisions TEXT,
        output_file TEXT
    )''')
    conn.commit()
    conn.close()

def log_query(query_type, query, result, user=None):
    conn = sqlite3.connect(str(AUDIT_DB))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO law_queries (timestamp, query_type, query, result, user) VALUES (?, ?, ?, ?, ?)",
                   (datetime.now().isoformat(), query_type, query[:500], result[:500], user or "cli"))
    conn.commit()
    conn.close()

def log_draft(doc_type, parties, provisions, output_file):
    conn = sqlite3.connect(str(AUDIT_DB))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO document_drafts (timestamp, doc_type, parties, provisions, output_file) VALUES (?, ?, ?, ?, ?)",
                   (datetime.now().isoformat(), doc_type, str(parties)[:500], str(provisions)[:500], output_file))
    conn.commit()
    conn.close()

def get_history(limit=50):
    conn = sqlite3.connect(str(AUDIT_DB))
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, query_type, query FROM law_queries ORDER BY timestamp DESC LIMIT ?", (limit,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_drafts(limit=50):
    conn = sqlite3.connect(str(AUDIT_DB))
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, doc_type, output_file FROM document_drafts ORDER BY timestamp DESC LIMIT ?", (limit,))
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_audit()
    print("Audit log initialized at", AUDIT_DB)
