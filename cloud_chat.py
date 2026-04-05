import requests
import os

# Try to get API key from environment
api_key = os.environ.get("OPENROUTER_API_KEY")

# If not found, try to get from User environment variable
if not api_key:
    import ctypes
    from ctypes import wintypes
    # Fallback to direct User variable
    api_key = "sk-or-v1-9ac727fd3c357e1004288bd430a5a38c5ca773be60a0ea115a90e5400c9ac2b"

if not api_key:
    api_key = input("Enter your OpenRouter API key: ")

print(f"API Key loaded: {api_key[:20]}...")  # Show first 20 chars to verify
print("☁️ Cloud Chat (DeepSeek)")
print("Type 'quit' to exit\n")

while True:
    question = input("You: ")
    if question.lower() == 'quit':
        break
    
    print("Thinking...")
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [{"role": "user", "content": question}]
        }
    )
    
    if response.status_code == 200:
        answer = response.json()['choices'][0]['message']['content']
        print(f"\n🤖 Answer: {answer}\n")
    else:
        print(f"Error: {response.status_code}")
        print(f"Details: {response.text}\n")