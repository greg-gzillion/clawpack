#!/usr/bin/env python3
"""
Historical Database for PhoenixPME Metrics
- Stores all metrics in SQLite
- Provides trend analysis
- Generates reports
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

class PhoenixPMEDatabase:
    def __init__(self, db_path="phoenixpme.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                crf_balance REAL,
                phnx_supply INTEGER,
                fee_collected REAL,
                collateral_ratio REAL,
                active_escrows INTEGER,
                total_volume REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS violations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                violation_type TEXT,
                severity TEXT,
                description TEXT,
                resolved BOOLEAN DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fixes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                file TEXT,
                bug_description TEXT,
                fix_applied TEXT,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def record_metrics(self, metrics):
        """Record current metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metrics (timestamp, crf_balance, phnx_supply, 
                               fee_collected, collateral_ratio, active_escrows, total_volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            metrics.get('crf_balance', 0),
            metrics.get('phnx_supply', 0),
            metrics.get('fee_collected', 0),
            metrics.get('collateral_ratio', 10),
            metrics.get('active_escrows', 0),
            metrics.get('total_volume', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def record_violation(self, violation_type, description, severity="HIGH"):
        """Record a compliance violation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO violations (timestamp, violation_type, severity, description)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), violation_type, severity, description))
        
        conn.commit()
        conn.close()
    
    def get_trends(self, days=30):
        """Get trend data for last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT timestamp, crf_balance, phnx_supply, total_volume
            FROM metrics
            WHERE timestamp > ?
            ORDER BY timestamp
        ''', (since_date,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def generate_report(self):
        """Generate a comprehensive report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get summary statistics
        cursor.execute('''
            SELECT 
                COUNT(*) as total_records,
                AVG(crf_balance) as avg_crf,
                MAX(crf_balance) as max_crf,
                AVG(collateral_ratio) as avg_collateral
            FROM metrics
        ''')
        summary = cursor.fetchone()
        
        # Get recent violations
        cursor.execute('''
            SELECT * FROM violations 
            WHERE timestamp > datetime('now', '-7 days')
            ORDER BY timestamp DESC
        ''')
        recent_violations = cursor.fetchall()
        
        conn.close()
        
        report = {
            'generated': datetime.now().isoformat(),
            'summary': {
                'total_records': summary[0],
                'avg_crf_balance': summary[1],
                'max_crf_balance': summary[2],
                'avg_collateral_ratio': summary[3]
            },
            'recent_violations': len(recent_violations),
            'violations': recent_violations[:10]
        }
        
        return report

if __name__ == "__main__":
    db = PhoenixPMEDatabase()
    print("📊 Database ready for PhoenixPME metrics")
    
    # Example: Generate report
    report = db.generate_report()
    print(json.dumps(report, indent=2))
