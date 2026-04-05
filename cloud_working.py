import requests

# YOUR API KEY
API_KEY = "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"

print("☁️ Cloud Chat (Free Models)")
print("Models available:")
print("1. Google Gemini Flash (fast)")
print("2. Meta Llama 3.2 (good)")
print("3. Microsoft Phi-3 (small)")
print("Type 'quit' to exit\n")

# List of free models to try
free_models = [
    "google/gemini-flash-1.5-8b",
    "meta-llama/llama-3.2-3b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free"
]

current_model = 0

while True:
    print(f"\nCurrent model: {free_models[current_model]}")
    question = input("You: ")
    if question.lower() == 'quit':
        break
    elif question.lower() == 'next':
        current_model = (current_model + 1) % len(free_models)
        print(f"Switched to: {free_models[current_model]}")
        continue
    
    print("Thinking...")
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": free_models[current_model],
                "messages": [{"role": "user", "content": question}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data['choices'][0]['message']['content']
            print(f"\n🤖 {answer}\n")
        else:
            print(f"Error: {response.status_code}")
            print(f"Try typing 'next' to switch models\n")
            
    except Exception as e:
        print(f"Exception: {e}\n")