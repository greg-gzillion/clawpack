# Add ConsensusAnalyzer class to agentforlaw.py
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

CONSENSUS_CODE = '''
class ConsensusAnalyzer:
    @staticmethod
    def analyze_with_consensus(question, models=None):
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import time
        
        if not models:
            models = []
            import os
            if os.environ.get("GROQ_API_KEY"):
                models.append("groq/llama-3.3-70b-versatile")
            try:
                import requests
                r = requests.get("http://localhost:11434/api/tags", timeout=2)
                if r.status_code == 200:
            except:
                pass
        
        results = {}
        
        def query(model_spec):
            provider, model_name = model_spec.split('/', 1)
            try:
                start = time.time()
                from agentforlaw import LegalAnalyzer
                answer = LegalAnalyzer.analyze(question, model_name, provider)
                elapsed = time.time() - start
                return model_spec, {"answer": answer, "time": elapsed, "success": True}
            except Exception as e:
                return model_spec, {"answer": str(e), "time": 0, "success": False}
        
        print(f"Querying {len(models)} models...")
        with ThreadPoolExecutor(max_workers=len(models)) as executor:
            futures = {executor.submit(query, m): m for m in models}
            for future in as_completed(futures):
                model, result = future.result()
                results[model] = result
                status = "✓" if result["success"] else "✗"
                print(f"  {status} {model} ({result['time']:.1f}s)")
        
        best = max((r for r in results.values() if r["success"]), key=lambda x: len(x["answer"]), default=None)
        return best["answer"] if best else "No consensus reached"
'''

# Check if already added
if not grep -q "ConsensusAnalyzer" agentforlaw.py; then
    echo "Adding ConsensusAnalyzer..."
    # Insert before the main() function
    sed -i '/^def main():/i '"$CONSENSUS_CODE" agentforlaw.py
else
    echo "ConsensusAnalyzer already present"
fi
