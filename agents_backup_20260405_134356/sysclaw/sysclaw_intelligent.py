#!/usr/bin/env python3
"""SysClaw Intelligent - Proactive system advisor"""

import os
import subprocess
import psutil
import json
from datetime import datetime
from pathlib import Path

class IntelligentSysClaw:
    def __init__(self):
        self.home = Path.home()
        self.tx_dir = self.home / "dev/TX"
        self.memory_dir = self.home / ".claw_memory"
        self.memory_dir.mkdir(exist_ok=True)
        
    def analyze_tx_project(self):
        """Deep analysis of TX project"""
        analysis = {
            "health": "unknown",
            "issues": [],
            "suggestions": [],
            "metrics": {}
        }
        
        if not self.tx_dir.exists():
            analysis["issues"].append("TX directory not found")
            return analysis
        
        os.chdir(self.tx_dir)
        
        # Check git health
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            analysis["issues"].append(f"Uncommitted changes: {len(result.stdout.splitlines())} files")
            analysis["suggestions"].append("Commit or stash changes: git add . && git commit -m 'message'")
        
        # Check branch health
        result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
        analysis["metrics"]["branch"] = result.stdout.strip()
        
        # Check behind/ahead
        subprocess.run(["git", "fetch"], capture_output=True)
        result = subprocess.run(["git", "rev-list", "HEAD..origin/HEAD", "--count"], capture_output=True, text=True)
        behind = int(result.stdout.strip() or 0)
        if behind > 0:
            analysis["issues"].append(f"Behind origin by {behind} commits")
            analysis["suggestions"].append(f"Pull updates: git pull")
        
        # Check for CI/CD files
        ci_files = [".github/workflows/", ".gitlab-ci.yml", "Jenkinsfile", "Dockerfile"]
        for ci in ci_files:
            if (self.tx_dir / ci).exists():
                analysis["metrics"]["ci"] = ci
                break
        
        # Check for tests
        test_dirs = ["tests/", "test/", "__tests__/", "spec/"]
        has_tests = any((self.tx_dir / td).exists() for td in test_dirs)
        if not has_tests:
            analysis["suggestions"].append("Add test suite for reliability")
        
        # Overall health
        if len(analysis["issues"]) == 0:
            analysis["health"] = "good"
        elif len(analysis["issues"]) <= 2:
            analysis["health"] = "fair"
        else:
            analysis["health"] = "needs_attention"
        
        return analysis
    
    def analyze_system(self):
        """Deep analysis of system health"""
        analysis = {
            "health": "unknown",
            "issues": [],
            "suggestions": [],
            "metrics": {}
        }
        
        # Disk space
        disk = psutil.disk_usage("/")
        analysis["metrics"]["disk_free_gb"] = disk.free // (2**30)
        analysis["metrics"]["disk_used_percent"] = disk.percent
        
        if disk.percent > 85:
            analysis["issues"].append(f"Disk at {disk.percent}% - low space")
            analysis["suggestions"].append("Clean Docker: docker system prune -a")
            analysis["suggestions"].append("Clean apt: sudo apt-get autoremove")
            analysis["suggestions"].append("Check large files: ncdu /")
        
        # Memory
        mem = psutil.virtual_memory()
        analysis["metrics"]["ram_used_percent"] = mem.percent
        if mem.percent > 90:
            analysis["issues"].append(f"RAM at {mem.percent}% - high usage")
            analysis["suggestions"].append("Check memory hogs: ps aux --sort=-%mem | head -10")
        
        # CPU
        cpu = psutil.cpu_percent(interval=1)
        analysis["metrics"]["cpu_percent"] = cpu
        if cpu > 80:
            analysis["issues"].append(f"CPU at {cpu}% - high load")
            analysis["suggestions"].append("Check CPU hogs: top -bn1 | head -20")
        
        # Package updates
        result = subprocess.run(["apt", "list", "--upgradable", "2>/dev/null"], 
                               shell=True, capture_output=True, text=True)
        upgradable = len([l for l in result.stdout.splitlines() if "upgradable" in l])
        analysis["metrics"]["upgradable_packages"] = upgradable
        if upgradable > 10:
            analysis["suggestions"].append(f"Run updates: sudo apt update && sudo apt upgrade -y")
        
        # Docker health
        result = subprocess.run(["docker", "ps", "-a", "--format", "table {{.Names}}\t{{.Status}}"], 
                               capture_output=True, text=True)
        containers = result.stdout.strip().splitlines()[1:] if result.stdout else []
        analysis["metrics"]["containers"] = len(containers)
        
        result = subprocess.run(["docker", "images", "-q"], capture_output=True, text=True)
        images = len([i for i in result.stdout.splitlines() if i])
        analysis["metrics"]["images"] = images
        
        if images > 10:
            analysis["suggestions"].append("Prune old Docker images: docker image prune -a")
        
        # Ollama health
        result = subprocess.run(["curl", "-s", "http://127.0.0.1:11434/api/tags"], 
                               capture_output=True, text=True)
        if result.stdout:
            import json as jsonlib
            try:
                models = jsonlib.loads(result.stdout).get("models", [])
                analysis["metrics"]["ollama_models"] = [m["name"] for m in models]
            except:
                pass
        
        # Overall health
        if len(analysis["issues"]) == 0:
            analysis["health"] = "good"
        elif len(analysis["issues"]) <= 2:
            analysis["health"] = "fair"
        else:
            analysis["health"] = "needs_attention"
        
        return analysis
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        print("\n" + "="*60)
        print("🦞 SysClaw Intelligent Analysis")
        print("="*60)
        
        print("\n📊 TX PROJECT ANALYSIS")
        tx = self.analyze_tx_project()
        print(f"   Health: {tx['health']}")
        print(f"   Branch: {tx['metrics'].get('branch', 'unknown')}")
        if tx['issues']:
            print(f"   Issues:")
            for issue in tx['issues']:
                print(f"     ⚠️ {issue}")
        if tx['suggestions']:
            print(f"   Suggestions:")
            for sug in tx['suggestions']:
                print(f"     💡 {sug}")
        
        print("\n🖥️ SYSTEM ANALYSIS")
        sys = self.analyze_system()
        print(f"   Health: {sys['health']}")
        print(f"   Disk: {sys['metrics'].get('disk_used_percent', 0)}% used ({sys['metrics'].get('disk_free_gb', 0)} GB free)")
        print(f"   RAM: {sys['metrics'].get('ram_used_percent', 0)}% used")
        print(f"   CPU: {sys['metrics'].get('cpu_percent', 0)}%")
        print(f"   Packages to update: {sys['metrics'].get('upgradable_packages', 0)}")
        
        if sys['issues']:
            print(f"   Issues:")
            for issue in sys['issues']:
                print(f"     ⚠️ {issue}")
        if sys['suggestions']:
            print(f"   Suggestions:")
            for sug in sys['suggestions']:
                print(f"     💡 {sug}")
        
        # Priority recommendations
        print("\n🎯 PRIORITY ACTIONS")
        priority_actions = []
        
        if sys['metrics'].get('disk_used_percent', 0) > 85:
            priority_actions.append("🔴 CRITICAL: Free disk space")
        if sys['metrics'].get('upgradable_packages', 0) > 20:
            priority_actions.append("🟡 MEDIUM: Run system updates")
        if tx['health'] == "needs_attention":
            priority_actions.append("🟡 MEDIUM: Fix TX project issues")
        
        if priority_actions:
            for action in priority_actions:
                print(f"   {action}")
        else:
            print("   ✅ System looks good! No urgent actions needed.")
        
        return {"tx": tx, "system": sys}
    
    def auto_fix_suggestions(self):
        """Offer to fix issues automatically"""
        recommendations = self.generate_recommendations()
        
        print("\n" + "="*60)
        print("🔧 Auto-Fix Options")
        print("="*60)
        
        actions = []
        
        # Check for disk cleanup opportunity
        disk = psutil.disk_usage("/")
        if disk.percent > 80:
            actions.append(("Clean Docker", "docker system prune -f"))
            actions.append(("Clean apt cache", "sudo apt-get clean"))
            actions.append(("Clean journal logs", "sudo journalctl --vacuum-time=7d"))
        
        # Check for updates
        result = subprocess.run(["apt", "list", "--upgradable", "2>/dev/null"], 
                               shell=True, capture_output=True, text=True)
        upgradable = len([l for l in result.stdout.splitlines() if "upgradable" in l])
        if upgradable > 5:
            actions.append(("Update system packages", "sudo apt update && sudo apt upgrade -y"))
        
        if actions:
            print("\nI can automatically fix these issues:")
            for i, (name, cmd) in enumerate(actions, 1):
                print(f"   {i}. {name}")
            
            choice = input("\nEnter number to fix, or 'all' for everything, or 'no': ").strip()
            
            if choice.lower() == 'all':
                for name, cmd in actions:
                    print(f"\n🔧 Running: {name}")
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"   ✅ {name} completed")
                    else:
                        print(f"   ❌ {name} failed: {result.stderr[:200]}")
            elif choice.isdigit() and 1 <= int(choice) <= len(actions):
                name, cmd = actions[int(choice)-1]
                print(f"\n🔧 Running: {name}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"   ✅ {name} completed")
                else:
                    print(f"   ❌ {name} failed: {result.stderr[:200]}")
            else:
                print("   No changes made")
        else:
            print("\n   No auto-fix actions needed. System looks good!")

if __name__ == "__main__":
    agent = IntelligentSysClaw()
    
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "analyze":
            agent.generate_recommendations()
        elif sys.argv[1] == "fix":
            agent.auto_fix_suggestions()
        else:
            print("Usage: python3 sysclaw_intelligent.py [analyze|fix]")
    else:
        agent.auto_fix_suggestions()
