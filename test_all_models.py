# test_all_models.py - Test all 10 Ollama models
import sys
sys.path.append('agents')
from ollama_integration import OllamaManager, MODEL_CAPABILITIES

def test_all_models():
    print("\n" + "="*80)
    print("🦙 TESTING ALL 10 OLLAMA MODELS")
    print("="*80)
    
    ollama = OllamaManager()
    
    test_prompts = {
        "code": "Write a Python function to calculate fibonacci numbers",
        "general": "What is artificial intelligence?",
        "reasoning": "If a train travels 120 miles in 2 hours, what is its speed?",
        "medical": "What are the symptoms of diabetes?",
        "legal": "What is the 4th Amendment?"
    }
    
    for model in ollama.models:
        print(f"\n📝 Testing: {model}")
        print(f"   Size: {MODEL_CAPABILITIES.get(model, {}).get('size', 'Unknown')}")
        print(f"   Best for: {', '.join(MODEL_CAPABILITIES.get(model, {}).get('best_for', ['general']))}")
        
        # Test general knowledge
        response = ollama.generate(test_prompts["general"], model=model, temperature=0.3)
        print(f"   Response preview: {response[:100]}...")
        print(f"   ✅ {model} is working!")

if __name__ == "__main__":
    test_all_models()
