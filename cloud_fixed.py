import requests

API_KEY = "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"

# Confirmed working free models
models = [
    "deepseek/deepseek-chat",
    "mistralai/mistral-7b-instruct:free",
    "openchat/openchat-7b:free"
]

print("☁️ Cloud Chat (Testing Models)")
print("Type 'quit' to exit")
print("Type 'next' to change models\n")

current = 0

while True:
    print(f"\n📡 Model: {models[current]}")
    user_input = input("You: ")
    
    if user_input.lower() == 'quit':
        break
    elif user_input.lower() == 'next':
        current = (current + 1) % len(models)
        print(f"Switched to: {models[current]}")
        continue
    
    print("Thinking...")
    
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": models[current], "messages": [{"role": "user", "content": user_input}]},
            timeout=30
        )
        
        if r.status_code == 200:
            print(f"\n🤖 {r.json()['choices'][0]['message']['content']}\n")
        else:
            print(f"Error {r.status_code}: {r.text[:100]}\n")
            
    except Exception as e:
        print(f"Error: {e}\n")