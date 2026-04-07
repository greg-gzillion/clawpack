#!/usr/bin/env python3
"""
WEBCLAW - Central Reference Hub for Clawpack
"""

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

AGENT_DIR = Path(__file__).parent
ROOT_DIR = AGENT_DIR.parent.parent
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"
SHARED_DB.parent.mkdir(exist_ok=True)

class WebClaw:
    def __init__(self):
        self.name = "webclaw"
        self.init_shared_memory()
        self.print_welcome()
    
    def init_shared_memory(self):
        try:
            conn = sqlite3.connect(str(SHARED_DB))
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS webclaw_references
                         (id INTEGER PRIMARY KEY, category TEXT, 
                          file_path TEXT, title TEXT, access_count INTEGER DEFAULT 0)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Init error: {e}")
    
    def print_welcome(self):
        print("\n" + "="*60)
        print("🌐 WEBCLAW - Central Reference Hub")
        print("="*60)
        print("Running. Press Ctrl+C to stop.\n")
    
    def run(self):
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")

if __name__ == "__main__":
    agent = WebClaw()
    agent.run()