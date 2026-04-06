# quick_test.py - Fast test for Ollama
import requests
import json

print("="*60)
print("🦙 QUICK OLLAMA TEST")
print("="*60)

# Test 1: Check if Ollama is running
try:
    response = requests.get("http://localhost:11434/api/tags")
    if response.status_code == 200:
        models = response.json().get('models', [])
        print(f"\n✅ Ollama is running!")
        print(f"📋 Models found: {len(models)}")
        for model in models[:3]:  # Show first 3 only
            print(f"   • {model['name']}")
        if len(models) > 3:
            print(f"   ... and {len(models)-3} more")
    else:
        print("❌ Ollama not responding")
except Exception as e:
    print(f"❌ Cannot connect to Ollama: {e}")
    exit()

# Test 2: Quick test with smallest model
print("\n🧪 Testing smallest model (gemma3:1b)...")
test_prompt = {
    "model": "gemma3:1b",
    "prompt": "Say 'Clawpack works!' in 3 words",
    "stream": False
}

try:
    response = requests.post("http://localhost:11434/api/generate", 
                            json=test_prompt, 
                            timeout=30)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Response: {result['response']}")
    else:
        print(f"⚠️ Model not loaded. Run: ollama pull gemma3:1b")
except Exception as e:
    print(f"⚠️ Error: {e}")

print("\n" + "="*60)
print("✅ Quick test complete!")
print("="*60)
print("\nTo test all models, run: python test_all_models.py")
print("(This will take 5-10 minutes for all 10 models)")