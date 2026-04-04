"""Configuration module for RustyPyCraw"""

import os
from pathlib import Path

CONFIG_DIR = os.path.expanduser("~/.rustypycraw")
os.makedirs(CONFIG_DIR, exist_ok=True)

MEMORY_DIR = os.path.join(CONFIG_DIR, "memory")
RULES_DIR = os.path.join(CONFIG_DIR, "rules")
AGENTS_DIR = os.path.join(CONFIG_DIR, "agents")

for d in [MEMORY_DIR, RULES_DIR, AGENTS_DIR]:
    os.makedirs(d, exist_ok=True)
