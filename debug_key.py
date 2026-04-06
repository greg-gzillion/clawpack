from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path("agents/docuclaw/docuclaw_shared.py").parent.parent / ".env"
print(f".env path: {env_path}")
print(f".env exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path)
key = os.environ.get("OPENROUTER_API_KEY")

if key:
    print(f"Key loaded: {key[:30]}...")
    print(f"Key length: {len(key)}")
else:
    print("Key NOT FOUND!")

# Also check the environment variable directly
env_key = os.environ.get("OPENROUTER_API_KEY")
print(f"Direct from env: {env_key[:30] if env_key else 'NOT SET'}...")
