import re

# Read the file
with open('agentforlaw.py', 'r') as f:
    content = f.read()

# Fix Groq model names to match actual API
# The correct Groq model IDs are:
# "llama-3.3-70b-versatile" - This one is correct
# "llama-3.1-8b-instant" - This one is correct  
# "mixtral-8x7b-32768" - This one is correct
# "gemma2-9b-it" - This might be "gemma-9b-it" or similar

# Replace the model list in discover_all
content = re.sub(
    r'"gemma2-9b-it"',
    '"gemma-9b-it"',
    content
)

# Add better error handling in _groq_analyze
old_method = '''    @staticmethod
    def _groq_analyze(question: str, model: str) -> str:
        try:
            from groq import Groq
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are AgentForLaw, an expert in US law. Provide accurate, concise legal analysis based on statutes, regulations, and case law."},
                    {"role": "user", "content": question}
                ],
                max_tokens=800,
                temperature=0.3
            )
            return f"[Groq/{model}]\\n{response.choices[0].message.content}"
        except Exception as e:
            return f"Groq error: {e}"'''

new_method = '''    @staticmethod
    def _groq_analyze(question: str, model: str) -> str:
        # Map friendly names to actual Groq model IDs
        model_map = {
            "llama-3.3-70b-versatile": "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant": "llama-3.1-8b-instant", 
            "mixtral-8x7b-32768": "mixtral-8x7b-32768",
            "gemma2-9b-it": "gemma2-9b-it",
            "gemma-9b-it": "gemma2-9b-it",
            "llama3.2:3b": "llama-3.1-8b-instant",  # fallback
            "codellama:7b": "llama-3.1-8b-instant"  # fallback
        }
        
        actual_model = model_map.get(model, "llama-3.3-70b-versatile")
        
        try:
            from groq import Groq
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            
            print(f"   Using Groq model: {actual_model}")
            
            response = client.chat.completions.create(
                model=actual_model,
                messages=[
                    {"role": "system", "content": "You are AgentForLaw, an expert in US law. Provide accurate, concise legal analysis based on statutes, regulations, and case law."},
                    {"role": "user", "content": question}
                ],
                max_tokens=800,
                temperature=0.3
            )
            return f"[Groq/{actual_model}]\\n{response.choices[0].message.content}"
        except Exception as e:
            # Fallback to a different model if first fails
            try:
                fallback_model = "llama-3.1-8b-instant"
                print(f"   Retrying with fallback model: {fallback_model}")
                from groq import Groq
                client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
                response = client.chat.completions.create(
                    model=fallback_model,
                    messages=[
                        {"role": "system", "content": "You are AgentForLaw, a legal expert."},
                        {"role": "user", "content": question}
                    ],
                    max_tokens=800,
                    temperature=0.3
                )
                return f"[Groq/{fallback_model}]\\n{response.choices[0].message.content}"
            except Exception as e2:
                return f"Groq error: {e}\\nFallback also failed: {e2}"'''

content = content.replace(old_method, new_method)

# Write the fixed file
with open('agentforlaw.py', 'w') as f:
    f.write(content)

print("✅ Fixed Groq model names and added fallback")
