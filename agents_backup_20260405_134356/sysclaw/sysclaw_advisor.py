#!/usr/bin/env python3
"""SysClaw Advisor - Understands TX project structure"""

import os
import subprocess
from pathlib import Path

tx_dir = Path.home() / "dev/TX"

print("🦞 SysClaw TX Project Advisor")
print("="*50)

os.chdir(tx_dir)

result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
changes = result.stdout.strip().splitlines()

print(f"\n📁 Found {len(changes)} changed files:")

for change in changes:
    status = change[:2]
    file = change[3:]
    if status == " M":
        print(f"   📝 Modified: {file}")
    elif status == "??":
        print(f"   ✨ New file: {file}")
    elif "modified content" in change:
        print(f"   📦 Submodule: {file}")

print("\n💡 Recommendations:")
if any("backend" in c for c in changes):
    print("   • Test backend: cd ~/dev/TX && npm test")
if any("contracts" in c for c in changes):
    print("   • Build contracts: cd ~/dev/TX/contracts && cargo build")
if any("frontend" in c for c in changes):
    print("   • Lint frontend: cd ~/dev/TX/apps/frontend && npm run lint")
if any(".rustypycraw" in c for c in changes):
    print("   • Add to gitignore: echo .rustypycraw/ >> .gitignore")
if any("docs" in c for c in changes):
    print("   • Commit docs: git add docs/ && git commit -m docs: update")

print("\n🔧 Quick: git add . && git commit -m WIP")

