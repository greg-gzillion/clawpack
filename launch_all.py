#!/usr/bin/env python3
"""
CLAWPACK MASTER LAUNCHER
Launches all agents and manages inter-agent communication
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

# Configuration
CLAWPACK_ROOT = Path(__file__).parent
AGENTS_DIR = CLAWPACK_ROOT / "agents"

# List of all agents to launch
AGENTS = {
    "unified": {
        "path": AGENTS_DIR / "unified" / "unified_shared.py",
        "port": 8001,
        "description": "Smart Router & Coordinator"
    },
    "webclaw": {
        "path": AGENTS_DIR / "webclaw" / "webclaw_shared.py",
        "port": 8002,
        "description": "Central Reference Hub"
    },
    "agentforlaw": {
        "path": AGENTS_DIR / "agentforlaw" / "agentforlaw.py",
        "port": 8003,
        "description": "Court Access"
    },
    "mediclaw": {
        "path": AGENTS_DIR / "mediclaw" / "mediclaw_shared.py",
        "port": 8004,
        "description": "Medical Information"
    },
    "polyclaw": {
        "path": AGENTS_DIR / "polyclaw" / "polyclaw_shared.py",
        "port": 8005,
        "description": "Translation"
    },
    "langclaw": {
        "path": AGENTS_DIR / "langclaw" / "langclaw.py",
        "port": 8006,
        "description": "Language Tutor"
    },
    "mathematicaclaw": {
        "path": AGENTS_DIR / "mathematicaclaw" / "mathematicaclaw.py",
        "port": 8007,
        "description": "Mathematics"
    },
    "docuclaw": {
        "path": AGENTS_DIR / "docuclaw" / "docuclaw.py",
        "port": 8008,
        "description": "Document Creation"
    },
    "dataclaw": {
        "path": AGENTS_DIR / "dataclaw" / "dataclaw.py",
        "port": 8009,
        "description": "Personal Library"
    }
}

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         🦞 CLAWPACK MASTER LAUNCHER                           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Launching all agents with cross-learning and shared memory...               ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """)

def launch_agent(agent_name, agent_info):
    """Launch a single agent"""
    if agent_info["path"].exists():
        print(f"  🚀 Launching {agent_name}: {agent_info['description']}")
        try:
            process = subprocess.Popen(
                [sys.executable, str(agent_info["path"])],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return process
        except Exception as e:
            print(f"  ❌ Failed to launch {agent_name}: {e}")
            return None
    else:
        print(f"  ⚠️ Agent not found: {agent_name} at {agent_info['path']}")
        return None

def main():
    print_banner()
    
    processes = {}
    
    print("\n📡 LAUNCHING AGENTS:")
    print("-" * 50)
    
    for agent_name, agent_info in AGENTS.items():
        process = launch_agent(agent_name, agent_info)
        if process:
            processes[agent_name] = process
        time.sleep(1)  # Stagger launches
    
    print(f"\n✅ LAUNCHED {len(processes)}/{len(AGENTS)} AGENTS")
    print("\n📊 RUNNING AGENTS:")
    print("-" * 50)
    for name, proc in processes.items():
        print(f"  ✅ {name} (PID: {proc.pid})")
    
    print("\n" + "="*70)
    print("💡 TIPS:")
    print("  • All agents share memory at ~/.claw_memory/")
    print("  • Webclaw provides central references")
    print("  • Cross-learning is ACTIVE")
    print("  • Press Ctrl+C to stop all agents")
    print("="*70)
    
    try:
        # Keep running
        while True:
            time.sleep(1)
            
            # Check if any process died
            for name, proc in list(processes.items()):
                if proc.poll() is not None:
                    print(f"⚠️ Agent {name} stopped (exit code: {proc.returncode})")
                    # Attempt restart
                    print(f"🔄 Restarting {name}...")
                    processes[name] = launch_agent(name, AGENTS[name])
                    
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down all agents...")
        for name, proc in processes.items():
            if proc and proc.poll() is None:
                proc.terminate()
                print(f"  ✅ Stopped {name}")
        print("\nGoodbye! 🦞")
        sys.exit(0)

if __name__ == "__main__":
    main()
