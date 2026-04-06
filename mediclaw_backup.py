import os
# mediclaw.py - Mediclaw: Medical Information & Wellness Agent
import requests

# Your working API key
CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

class Mediclaw:
    def __init__(self):
        self.name = "Mediclaw"
        self.role = "I provide medical information, first aid guidance, and wellness advice"
        
        self.categories = {
            "first_aid": "Emergency first aid procedures",
            "symptoms": "Symptom checking and guidance",
            "conditions": "Common medical conditions",
            "medications": "Medication information",
            "wellness": "Preventive health and wellness",
            "nutrition": "Dietary and nutrition advice",
            "mental_health": "Mental wellness resources"
        }
    
    def get_response(self, query, category="general"):
        """Get medical information response"""
        
        prompt = f"""You are Mediclaw, a helpful medical information assistant. 
Provide accurate, responsible medical information about: {query}

IMPORTANT RULES:
1. Always include a disclaimer that you are not a substitute for professional medical advice
2. Encourage seeking professional medical help for serious symptoms
3. Be clear about emergency warning signs
4. Provide practical, evidence-based information
5. Do NOT diagnose or prescribe

Please provide a helpful response about: {query}"""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def emergency_check(self, symptoms):
        """Check if symptoms require emergency attention"""
        
        emergency_keywords = [
            "chest pain", "difficulty breathing", "severe bleeding", "unconscious",
            "stroke", "seizure", "head injury", "poisoning", "suicidal", 
            "heart attack", "choking", "drowning", "burn", "fracture", "paralysis",
            "cannot speak", "blue lips", "severe allergic", "anaphylaxis"
        ]
        
        symptoms_lower = symptoms.lower()
        for keyword in emergency_keywords:
            if keyword in symptoms_lower:
                return True, keyword
        return False, None
    
    def chat(self):
        print("\n" + "="*70)
        print("ðŸ¦ž MEDICLAW - Medical Information & Wellness Agent")
        print("="*70)
        print("\nâš ï¸ IMPORTANT DISCLAIMER:")
        print("Mediclaw provides general medical information only.")
        print("This is NOT a substitute for professional medical advice.")
        print("For medical emergencies, call emergency services immediately.")
        print("="*70)
        
        print("\nCategories:")
        for code, desc in self.categories.items():
            print(f"  /{code:<15} - {desc}")
        
        print("\nCommands:")
        print("  /ask [question]    - Ask a medical question")
        print("  /emergency [symptoms] - Check if symptoms need immediate care")
        print("  /firstaid [situation] - Get first aid guidance")
        print("  /symptoms [description] - Symptom checker")
        print("  /wellness [topic]  - Wellness advice")
        print("  /disclaimer        - Show medical disclaimer")
        print("  /help              - Show this menu")
        print("  /quit              - Exit")
        
        print("\nExamples:")
        print("  /ask What are the signs of dehydration?")
        print("  /emergency severe chest pain")
        print("  /firstaid burn from hot water")
        print("  /symptoms persistent headache and fever")
        print("  /wellness tips for better sleep")
        print("="*70)
        
        while True:
            cmd = input("\nðŸ¥ Mediclaw> ").strip()
            
            if not cmd:
                continue
            if cmd == '/quit':
                break
            if cmd == '/help':
                print("\nCommands: /ask, /emergency, /firstaid, /symptoms, /wellness, /disclaimer, /help, /quit")
                continue
            if cmd == '/disclaimer':
                print("\nâš ï¸ MEDICAL DISCLAIMER:")
                print("Mediclaw is an AI assistant providing general medical information only.")
                print("Information provided is not a substitute for professional medical advice.")
                print("Always consult a qualified healthcare provider for medical concerns.")
                print("In emergencies, call your local emergency number immediately.")
                continue
            
            # Parse command
            if cmd.startswith('/ask '):
                question = cmd[5:]
                print(f"\nðŸ¦ž Mediclaw is analyzing your question...\n")
                result = self.get_response(question)
                print(f"\nðŸ“‹ RESPONSE:\n{result}\n")
                print("-"*50)
            
            elif cmd.startswith('/emergency '):
                symptoms = cmd[11:]
                is_emergency, keyword = self.emergency_check(symptoms)
                
                print(f"\nðŸš¨ EMERGENCY CHECK: {symptoms}")
                print("-"*50)
                
                if is_emergency:
                    print(f"\nâš ï¸ URGENT: '{keyword}' detected!")
                    print("This symptom requires IMMEDIATE medical attention.")
                    print("Call emergency services (911 in US, 112 in EU, 000 in Australia) NOW.")
                else:
                    print("\nâœ… No immediate emergency indicators detected.")
                    print("However, if symptoms worsen or concern you, consult a healthcare provider.")
                
                print("\n" + "-"*50)
            
            elif cmd.startswith('/firstaid '):
                situation = cmd[10:]
                print(f"\nðŸ©¹ FIRST AID FOR: {situation}\n")
                result = self.get_response(f"Provide first aid guidance for: {situation}. Include step-by-step instructions.")
                print(f"{result}\n")
                print("-"*50)
            
            elif cmd.startswith('/symptoms '):
                description = cmd[10:]
                print(f"\nðŸ” SYMPTOM CHECK: {description}\n")
                result = self.get_response(f"Based on these symptoms: {description}. Provide possible explanations and guidance. Emphasize when to see a doctor.")
                print(f"{result}\n")
                print("-"*50)
            
            elif cmd.startswith('/wellness '):
                topic = cmd[10:]
                print(f"\nðŸŒ¿ WELLNESS ADVICE: {topic}\n")
                result = self.get_response(f"Provide wellness and preventive health advice about: {topic}")
                print(f"{result}\n")
                print("-"*50)
            
            else:
                print("Unknown command. Use /ask, /emergency, /firstaid, /symptoms, /wellness, or /help")

def main():
    medic = Mediclaw()
    medic.chat()

if __name__ == "__main__":
    main()
