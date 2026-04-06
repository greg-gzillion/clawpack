import os
# clawpack_simple.py - Simplified Unified Controller
import requests
import sqlite3
from pathlib import Path

# YOUR WORKING API KEY (hardcoded for reliability)
CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY")
LOCAL_URL = "http://127.0.0.1:11434"
DB_PATH = Path.home() / ".claw_memory" / "shared_memory.db"

print("\n" + "="*60)
print("🦞 CLAWPACK UNIFIED (Working Version)")
print("="*60)
print("\nCommands:")
print("  /db [question]  - Database only (100% accurate)")
print("  /local [question] - Local GPU model (fast)")
print("  /cloud [question] - Cloud DeepSeek (powerful)")
print("  /compare [question] - See all three")
print("  /help - This menu")
print("  /quit - Exit")
print("="*60)

while True:
    cmd = input("\n> ").strip()
    
    if not cmd:
        continue
    
    if cmd == '/quit':
        break
    
    if cmd == '/help':
        print("\nCommands: /db, /local, /cloud, /compare, /help, /quit")
        continue
    
    # Parse command and question
    if cmd.startswith('/db '):
        question = cmd[4:]
        print("\n📚 DATABASE (100% accurate):")
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        c.execute("SELECT topic, content FROM tx_knowledge WHERE topic LIKE ? OR content LIKE ? LIMIT 3", 
                  (f"%{question}%", f"%{question}%"))
        results = c.fetchall()
        conn.close()
        if results:
            for topic, content in results:
                print(f"\n📖 {topic}:\n{content}\n")
        else:
            print("No exact match found.")
    
    elif cmd.startswith('/local '):
        question = cmd[7:]
        print("\n🖥️ LOCAL MODEL (thinking)...")
        try:
            r = requests.post(f"{LOCAL_URL}/api/generate", 
                            json={"model": "gemma3:4b", "prompt": question, "stream": False}, timeout=120)
            if r.status_code == 200:
                print(f"\n{r.json()['response']}\n")
            else:
                print(f"Error: {r.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    
    elif cmd.startswith('/cloud '):
        question = cmd[7:]
        print("\n☁️ CLOUD MODEL (thinking)...")
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                            headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                            json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": question}]},
                            timeout=60)
            if r.status_code == 200:
                print(f"\n{r.json()['choices'][0]['message']['content']}\n")
            else:
                print(f"Error: {r.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    
    elif cmd.startswith('/compare '):
        question = cmd[9:]
        print("\n" + "="*60)
        print(f"COMPARING: {question}")
        print("="*60)
        
        # Database
        print("\n📚 DATABASE:")
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        c.execute("SELECT content FROM tx_knowledge WHERE topic LIKE ? OR content LIKE ? LIMIT 1", 
                  (f"%{question}%", f"%{question}%"))
        result = c.fetchone()
        conn.close()
        if result:
            print(result[0][:500])
        else:
            print("No match in database")
        
        # Local
        print("\n🖥️ LOCAL (gemma3:4b):")
        try:
            r = requests.post(f"{LOCAL_URL}/api/generate", 
                            json={"model": "gemma3:4b", "prompt": question, "stream": False}, timeout=60)
            if r.status_code == 200:
                print(r.json()['response'][:500])
        except:
            print("Local model error")
        
        # Cloud
        print("\n☁️ CLOUD (DeepSeek):")
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                            headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                            json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": question}]},
                            timeout=60)
            if r.status_code == 200:
                print(r.json()['choices'][0]['message']['content'][:500])
        except:
            print("Cloud error")
        
        print("\n" + "="*60)
    
    else:
        print("Unknown command. Type /help for commands.")