# mediclaw.py - COMPLETE MEDICLAW: All Specialties + Homeopathy
import requests
import sqlite3
from pathlib import Path
from datetime import datetime

CLOUD_API_KEY = "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"

class CompleteMediclaw:
    def __init__(self):
        self.name = "Complete Mediclaw"
        self.cache_path = Path.home() / ".claw_memory" / "medical_cache.db"
        self.init_cache()
        
        # Homeopathic remedy categories
        self.homeopathic_remedies = {
            "first_aid": ["Arnica", "Calendula", "Hypericum", "Ledum", "Rhus tox", "Apis"],
            "acute_illness": ["Belladonna", "Aconite", "Ferrum phos", "Bryonia", "Gelsemium"],
            "digestive": ["Nux vomica", "Pulsatilla", "Lycopodium", "Carbo veg", "China"],
            "respiratory": ["Spongia", "Hepar sulph", "Kali bich", "Phosphorus", "Antimonium tart"],
            "mental_emotional": ["Ignatia", "Natrum mur", "Staphysagria", "Sepia", "Arsenicum album"],
            "skin": ["Sulphur", "Graphites", "Mezereum", "Rhus tox", "Urtica urens"],
            "women_health": ["Sepia", "Pulsatilla", "Lachesis", "Calcarea carb", "Lilium tig"],
            "children": ["Chamomilla", "Belladonna", "Pulsatilla", "Calc phos", "Silicea"]
        }
        
        # Homeopathic sources
        self.homeopathy_sources = {
            "HRI (Homeopathic Research Institute)": "https://www.hri-research.org",
            "LMHI (International Homeopathic League)": "https://www.lmhi.org",
            "NIH Homeopathy": "https://www.nccih.nih.gov/health/homeopathy",
            "British Homeopathic Association": "https://britishhomeopathic.org",
            "PubMed Homeopathy Studies": "https://pubmed.ncbi.nlm.nih.gov/?term=homeopathy"
        }
        
        # Emergency keywords
        self.emergency_keywords = {
            "cardiac": ["chest pain", "heart attack", "cardiac arrest", "palpitations"],
            "stroke": ["stroke", "facial droop", "arm weakness", "slurred speech"],
            "trauma": ["severe bleeding", "head injury", "gunshot", "stabbing"],
            "respiratory": ["choking", "difficulty breathing", "blue lips", "anaphylaxis"]
        }
        
        # Medication categories
        self.med_categories = {
            "antibiotics": ["amoxicillin", "azithromycin", "ciprofloxacin", "doxycycline"],
            "pain_relievers": ["ibuprofen", "acetaminophen", "aspirin", "naproxen"],
            "blood_pressure": ["lisinopril", "amlodipine", "metoprolol", "losartan"],
            "diabetes": ["metformin", "insulin", "glipizide", "sitagliptin"]
        }
    
    def init_cache(self):
        conn = sqlite3.connect(str(self.cache_path))
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT UNIQUE,
                response TEXT,
                category TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def query(self, topic, category="general"):
        """Query medical information"""
        prompt = f"Provide helpful medical information about: {topic}. Include disclaimer."
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def homeopathy_query(self, remedy):
        """Query homeopathic remedy information"""
        prompt = f"Provide information about homeopathic remedy {remedy}: source, indications, modalities, potencies."
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def emergency_check(self, symptoms):
        symptoms_lower = symptoms.lower()
        for category, keywords in self.emergency_keywords.items():
            for keyword in keywords:
                if keyword in symptoms_lower:
                    return True, keyword, category
        return False, None, None
    
    def get_medication(self, med_name):
        prompt = f"Provide medication information for {med_name}: uses, dosage, side effects, interactions."
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def first_aid(self, situation):
        prompt = f"Provide step-by-step first aid for: {situation}"
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"

def main():
    m = CompleteMediclaw()
    
    print("\n" + "="*70)
    print("🦞 COMPLETE MEDICLAW - All Specialties + Homeopathy")
    print("="*70)
    print("\n⚠️ DISCLAIMER: For medical education only. Not a substitute for professional care.")
    print("="*70)
    
    print("\n🌿 HOMEOPATHY COMMANDS:")
    print("  /homeo [remedy]           - Remedy information")
    print("  /homeo-symptom [symptoms] - Find remedies")
    print("  /homeo-categories         - All remedy categories")
    print("  /homeo-sources            - Reputable sources")
    print("  /integrative [condition]  - Integrative approach")
    
    print("\n🔬 OTHER COMMANDS:")
    print("  /oncology, /cardiology, /neurology, /pediatrics, /psychiatry")
    print("  /med [name], /firstaid [situation], /emergency [symptoms]")
    print("  /ask [question], /quit")
    
    print("\n" + "="*70)
    print("EXAMPLES:")
    print("  /homeo Arnica")
    print("  /homeo-symptom anxiety")
    print("  /homeo-categories")
    print("  /integrative insomnia")
    print("="*70)
    
    while True:
        cmd = input("\n🏥 Mediclaw> ").strip()
        
        if not cmd:
            continue
        if cmd == '/quit':
            break
        
        # Homeopathy commands
        if cmd == '/homeo-categories':
            print("\n🌿 HOMEOPATHIC CATEGORIES:")
            for cat, remedies in m.homeopathic_remedies.items():
                print(f"\n{cat.upper()}: {', '.join(remedies)}")
            continue
        
        if cmd == '/homeo-sources':
            print("\n📚 HOMEOPATHIC SOURCES:")
            for name, url in m.homeopathy_sources.items():
                print(f"\n{name}: {url}")
            continue
        
        if cmd.startswith('/homeo '):
            remedy = cmd[7:]
            print(f"\n🌿 REMEDY: {remedy}\n")
            print(m.homeopathy_query(remedy))
            continue
        
        if cmd.startswith('/homeo-symptom '):
            symptoms = cmd[15:]
            print(f"\n🌿 REMEDIES FOR: {symptoms}\n")
            result = m.query(f"Suggest homeopathic remedies for {symptoms}. List 3-5 remedies.", "homeopathy")
            print(result)
            continue
        
        if cmd.startswith('/integrative '):
            condition = cmd[13:]
            print(f"\n🔄 INTEGRATIVE APPROACH: {condition}\n")
            result = m.query(f"Integrative medicine approach for {condition} including conventional and homeopathic options.", "integrative")
            print(result)
            continue
        
        # Emergency
        if cmd.startswith('/emergency '):
            symptoms = cmd[11:]
            is_emerg, keyword, category = m.emergency_check(symptoms)
            if is_emerg:
                print(f"\n⚠️ URGENT: '{keyword}' - Call emergency services NOW!")
            else:
                print("\n✅ No emergency signs detected.")
            continue
        
        # First aid
        if cmd.startswith('/firstaid '):
            print(f"\n🩹 {m.first_aid(cmd[10:])}\n")
            continue
        
        # Medication
        if cmd.startswith('/med '):
            print(f"\n💊 {m.get_medication(cmd[5:])}\n")
            continue
        
        # Specialty queries
        if cmd.startswith('/oncology '):
            print(f"\n🔬 {m.query(cmd[10:], 'oncology')}\n")
            continue
        if cmd.startswith('/cardiology '):
            print(f"\n🔬 {m.query(cmd[12:], 'cardiology')}\n")
            continue
        if cmd.startswith('/neurology '):
            print(f"\n🔬 {m.query(cmd[11:], 'neurology')}\n")
            continue
        if cmd.startswith('/pediatrics '):
            print(f"\n🔬 {m.query(cmd[12:], 'pediatrics')}\n")
            continue
        if cmd.startswith('/psychiatry '):
            print(f"\n🔬 {m.query(cmd[12:], 'psychiatry')}\n")
            continue
        
        # General ask
        if cmd.startswith('/ask '):
            print(f"\n📖 {m.query(cmd[5:], 'general')}\n")
            continue
        
        print("Unknown command. Try /homeo Arnica or /help")

if __name__ == "__main__":
    main()
