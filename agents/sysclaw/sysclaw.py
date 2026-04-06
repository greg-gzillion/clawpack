#!/usr/bin/env python3
"""SysClaw - Local machine maintenance agent"""

import os
import subprocess
import psutil
import shutil
from datetime import datetime
# Shared memory integration for sysclaw
import sqlite3
from pathlib import Path

class SharedMemory:
    def __init__(self):
        self.db_path = Path.home() / ".claw_memory" / "shared_memory.db"
        self.db_path.parent.mkdir(exist_ok=True)
    
    def log_system_event(self, event_type, details):
        try:
            conn = sqlite3.connect(str(self.db_path))
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS system_events
                         (id INTEGER PRIMARY KEY, event_type TEXT, 
                          details TEXT, timestamp TEXT)''')
            c.execute('INSERT INTO system_events (event_type, details, timestamp) VALUES (?,?,?)',
                      (event_type, details, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return True
        except:
            return False

import json

class SysClaw:
    def __init__(self):
        self.name = "sysclaw"
        self.capabilities = [
            "disk_cleanup",
            "memory_monitor",
            "backup_manager",
            "log_rotator",
            "performance_audit",
            "process_manager"
        ]
    
    def get_disk_usage(self):
        """Get disk usage statistics"""
        usage = shutil.disk_usage("/")
        return {
            "total": usage.total // (2**30),
            "used": usage.used // (2**30),
            "free": usage.free // (2**30),
            "percent": (usage.used / usage.total) * 100
        }
    
    def cleanup_docker(self):
        """Clean up docker resources"""
        commands = [
            "docker system prune -f",
            "docker volume prune -f",
            "docker image prune -f"
        ]
        results = []
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            results.append({"cmd": cmd, "output": result.stdout})
        return results
    
    def cleanup_apt(self):
        """Clean up apt cache"""
        commands = [
            "sudo apt-get clean",
            "sudo apt-get autoremove -y",
            "sudo apt-get autoclean"
        ]
        results = []
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            results.append({"cmd": cmd, "output": result.stdout})
        return results
    
    def get_memory_status(self):
        """Get memory statistics"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "ram": {
                "total": mem.total // (2**30),
                "available": mem.available // (2**30),
                "percent": mem.percent
            },
            "swap": {
                "total": swap.total // (2**30),
                "used": swap.used // (2**30),
                "percent": swap.percent
            }
        }
    
    def get_cpu_status(self):
        """Get CPU statistics"""
        return {
            "percent": psutil.cpu_percent(interval=1),
            "cores": psutil.cpu_count(),
            "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None
        }
    
    def cleanup_logs(self, days=30):
        """Clean up old log files"""
        log_dirs = ["/var/log", "~/.cache", "~/.local/share"]
        cleaned = []
        for log_dir in log_dirs:
            expanded = os.path.expanduser(log_dir)
            if os.path.exists(expanded):
                for root, dirs, files in os.walk(expanded):
                    for file in files:
                        path = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(path)
                            age_days = (datetime.now().timestamp() - mtime) / 86400
                            if age_days > days:
                                os.remove(path)
                                cleaned.append(path)
                        except:
                            pass
        return {"cleaned": len(cleaned), "files": cleaned[:10]}
    
    def run_maintenance(self):
        """Run full maintenance routine"""
        print("🔧 Running system maintenance...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "disk_before": self.get_disk_usage(),
            "docker_cleanup": self.cleanup_docker(),
            "apt_cleanup": self.cleanup_apt(),
            "log_cleanup": self.cleanup_logs(30),
            "memory": self.get_memory_status(),
            "cpu": self.get_cpu_status()
        }
        
        results["disk_after"] = self.get_disk_usage()
        results["disk_freed"] = results["disk_before"]["used"] - results["disk_after"]["used"]
        
        return results
    
    def get_status(self):
        """Get system status summary"""
        return {
            "agent": self.name,
            "capabilities": self.capabilities,
            "disk": self.get_disk_usage(),
            "memory": self.get_memory_status(),
            "cpu": self.get_cpu_status()
        }

if __name__ == "__main__":
    agent = SysClaw()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print(json.dumps(agent.get_status(), indent=2))
        elif sys.argv[1] == "maintenance":
            results = agent.run_maintenance()
            print(json.dumps(results, indent=2))
        elif sys.argv[1] == "cleanup":
            print("Cleaning up...")
            agent.cleanup_logs()
            agent.cleanup_docker()
            agent.cleanup_apt()
            print("✅ Cleanup complete")
    else:
        print(json.dumps(agent.get_status(), indent=2))
