#!/usr/bin/env python3
"""Simple web dashboard for sysclaw"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

def get_status():
    status = {
        "timestamp": datetime.now().isoformat(),
        "version": open(Path.home() / "dev/clawpack/VERSION").read().strip(),
        "tx": {},
        "system": {},
        "alerts": []
    }
    
    # Check TX status
    tx_dir = Path.home() / "dev/TX"
    if tx_dir.exists():
        import os
        os.chdir(tx_dir)
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        changes = len(result.stdout.strip().splitlines()) if result.stdout else 0
        status["tx"]["uncommitted"] = changes
        
        result = subprocess.run(["git", "rev-list", "HEAD..origin/HEAD", "--count"], 
                               capture_output=True, text=True)
        behind = int(result.stdout.strip() or 0)
        status["tx"]["behind"] = behind
    
    # Check disk
    import shutil
    disk = shutil.disk_usage("/")
    status["system"]["disk_percent"] = disk.used / disk.total * 100
    status["system"]["disk_free_gb"] = disk.free // (2**30)
    
    # Check alerts
    alert_log = Path.home() / ".claw_memory/alerts.log"
    if alert_log.exists():
        with open(alert_log) as f:
            lines = f.readlines()[-5:]
            status["alerts"] = [l.strip() for l in lines]
    
    return status

if __name__ == "__main__":
    # Simple HTML output
    status = get_status()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>SysClaw Dashboard</title>
    <style>
        body {{ font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }}
        .card {{ background: #161b22; padding: 20px; margin: 10px 0; border-radius: 8px; }}
        .good {{ color: #2ea043; }}
        .warning {{ color: #d29922; }}
        .critical {{ color: #f85149; }}
        pre {{ background: #0d1117; padding: 10px; overflow-x: auto; }}
    </style>
    </head>
    <body>
    <h1>🦞 SysClaw Dashboard</h1>
    <div class="card">
        <h2>Version: {status['version']}</h2>
        <p>Last updated: {status['timestamp']}</p>
    </div>
    <div class="card">
        <h2>TX Project</h2>
        <p>Uncommitted changes: {status['tx'].get('uncommitted', 0)}</p>
        <p>Commits behind: {status['tx'].get('behind', 0)}</p>
    </div>
    <div class="card">
        <h2>System</h2>
        <p>Disk usage: {status['system']['disk_percent']:.1f}%</p>
        <p>Free space: {status['system']['disk_free_gb']} GB</p>
    </div>
    <div class="card">
        <h2>Recent Alerts</h2>
        <pre>{chr(10).join(status['alerts'])}</pre>
    </div>
    </body>
    </html>
    """
    
    output_file = Path.home() / ".claw_memory/dashboard.html"
    output_file.write_text(html)
    print(f"✅ Dashboard generated: {output_file}")
    print(f"   Open in browser: file://{output_file}")
