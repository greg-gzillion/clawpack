"""EagleClaw configuration - extended from rustypycraw"""

import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".eagleclaw"
CONFIG_DIR.mkdir(exist_ok=True)

MEMORY_DIR = CONFIG_DIR / "memory"
RULES_DIR = CONFIG_DIR / "rules"
AGENTS_DIR = CONFIG_DIR / "agents"

for d in [MEMORY_DIR, RULES_DIR, AGENTS_DIR]:
    d.mkdir(exist_ok=True)

class EagleConfig:
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.permission_mode = os.environ.get("EAGLE_PERMISSION", "read-only")
        self.default_model = os.environ.get("EAGLE_MODEL", "codellama:7b")
