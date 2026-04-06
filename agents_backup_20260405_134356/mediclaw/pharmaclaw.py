import os
# mediclaw.py - COMPLETE MEDICLAW: All Specialties + Homeopathy
import requests
import sqlite3
from pathlib import Path
from datetime import datetime

CLOUD_API_KEY = os.environ.get("OPENROUTER_API_KEY")

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
        prompt = f"""Provide helpful medical information about: {topic}

Category: {category}

Include practical, accurate information. Include disclaimer that this is not medical advice."""
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"},
                json={"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                return result
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {e}"
    
    def homeopathy_query(self, remedy):
        """Query homeopathic remedy information"""
        prompt = f"""Provide information about the homeopathic remedy {remedy}:

Include:
- Source/origin
- Key indications
- Modalities (better/worse)
- Typical potencies
- Clinical applications

Disclaimer: Educational only. Consult a qualified homeopath."""
        
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
        prompt = f"""Provide medication information for {med_name}:
- Drug class and mechanism
- Indications and dosage
- Contraindications and warnings
- Common side effects
- Major interactions"""
        
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
        prompt = f"""Provide first aid for: {situation}
Steps: scene safety, immediate actions, treatment, when to call emergency."""
        
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
    
    print("\n" + "="*70)
    print("COMMANDS:")
    print("="*70)
    
    print("\n🔬 CONVENTIONAL MEDICINE:")
    print("  /oncology [topic]     - Cancer, chemotherapy, immunotherapy")
    print("  /cardiology [topic]   - Heart disease, hypertension")
    print("  /neurology [topic]    - Stroke, epilepsy, Alzheimer's")
    print("  /pediatrics [topic]   - Children's health, vaccines")
    print("  /psychiatry [topic]   - Depression, anxiety, mental health")
    print("  /gynecology [topic]   - Women's health, pregnancy")
    print("  /dermatology [topic]  - Skin conditions, acne, melanoma")
    print("  /endocrinology [topic] - Diabetes, thyroid, hormones")
    print("  /gastro [topic]       - Digestive, IBD, GERD")
    print("  /pulmonology [topic]  - Lungs, asthma, COPD")
    print("  /infectious [topic]   - Bacterial, viral infections")
    print("  /orthopedics [topic]  - Bones, joints, fractures")
    print("  /urology [topic]      - Urinary tract, prostate")
    print("  /nutrition [topic]    - Diet, vitamins, supplements")
    print("  /sleep [topic]        - Insomnia, sleep apnea")
    
    print("\n🌿 HOMEOPATHY & INTEGRATIVE:")
    print("  /homeo [remedy]           - Homeopathic remedy information")
    print("  /homeo-symptom [symptoms] - Find remedies for symptoms")
    print("  /homeo-categories         - Show all remedy categories")
    print("  /homeo-sources            - Reputable homeopathy sources")
    print("  /integrative [condition]  - Integrative medicine approach")
    
    print("\n💊 MEDICATIONS:")
    print("  /med [name]           - Medication information")
    print("  /meds [category]      - List medications by category")
    print("  /categories           - Show all medication categories")
    
    print("\n🏥 FIRST AID & EMERGENCIES:")
    print("  /firstaid [situation] - First aid guidance")
    print("  /emergency [symptoms] - Emergency symptom checker")
    
    print("\n📖 GENERAL:")
    print("  /ask [question]       - General medical question")
    print("  /help                 - This menu")
    print("  /quit                 - Exit")
    
    print("\n" + "="*70)
    print("📚 EXAMPLES:")
    print("="*70)
    print("  /homeo Arnica")
    print("  /homeo-symptom anxiety insomnia")
    print("  /homeo-categories")
    print("  /homeo-sources")
    print("  /integrative anxiety")
    print("  /oncology breast cancer")
    print("  /med ibuprofen")
    print("  /emergency chest pain")
    print("="*70)
    
    while True:
        cmd = input("\n🏥 Mediclaw> ").strip()
        
        if not cmd:
            continue
        if cmd == '/quit':
            break
        if cmd == '/help':
            continue
        
        # Homeopathy commands
        if cmd == '/homeo-categories':
            print("\n🌿 HOMEOPATHIC REMEDY CATEGORIES:")
            for cat, remedies in m.homeopathic_remedies.items():
                print(f"\n{cat.upper()}:")
                print(f"  {', '.join(remedies)}")
            print("\n💡 Use /homeo [remedy] for detailed information")
            continue
        
        if cmd == '/homeo-sources':
            print("\n📚 REPUTABLE HOMEOPATHIC SOURCES:")
            for name, url in m.homeopathy_sources.items():
                print(f"\n{name}:")
                print(f"  {url}")
            continue
        
        if cmd.startswith('/homeo '):
            remedy = cmd[7:]
            print(f"\n🌿 HOMEOPATHIC REMEDY: {remedy}\n")
            print(m.homeopathy_query(remedy))
            print()
            continue
        
        if cmd.startswith('/homeo-symptom '):
            symptoms = cmd[15:]
            print(f"\n🌿 REMEDY FINDER for: {symptoms}\n")
            result = m.query(f"Suggest homeopathic remedies for: {symptoms}. List 3-5 remedies with key indications.", "homeopathy")
            print(result)
            print()
            continue
        
        if cmd.startswith('/integrative '):
            condition = cmd[13:]
            print(f"\n🔄 INTEGRATIVE APPROACH for: {condition}\n")
            result = m.query(f"Provide integrative medicine approach for {condition} including conventional treatment and complementary options like homeopathy, herbs, nutrition.", "integrative")
            print(result)
            print()
            continue
        
        # Emergency check
        if cmd.startswith('/emergency '):
            symptoms = cmd[11:]
            is_emerg, keyword, category = m.emergency_check(symptoms)
            print(f"\n🚨 EMERGENCY CHECK: {symptoms}")
            if is_emerg:
                print(f"\n⚠️ URGENT: '{keyword}' - Call emergency services NOW!")
            else:
                print("\n✅ No emergency signs detected. Consult doctor if concerned.")
            print()
            continue
        
        # First Aid
        if cmd.startswith('/firstaid '):
            situation = cmd[10:]
            print(f"\n🩹 FIRST AID: {situation}\n")
            print(m.first_aid(situation))
            print()
            continue
        
        # Medication
        if cmd.startswith('/med '):
            med = cmd[5:]
            print(f"\n💊 MEDICATION: {med}\n")
            print(m.get_medication(med))
            print()
            continue
        
        if cmd == '/categories':
            print("\n📂 MEDICATION CATEGORIES:")
            for cat, meds in m.med_categories.items():
                print(f"\n{cat.upper()}: {', '.join(meds)}")
            continue
        
        if cmd.startswith('/meds '):
            category = cmd[6:].lower()
            if category in m.med_categories:
                print(f"\n{category.upper()}: {', '.join(m.med_categories[category])}")
            else:
                print(f"Category not found. Use /categories to see all.")
            continue
        
        # Specialty queries
        specialties = {
            '/oncology': 'oncology', '/cardiology': 'cardiology', '/neurology': 'neurology',
            '/pediatrics': 'pediatrics', '/psychiatry': 'psychiatry', '/gynecology': 'gynecology',
            '/dermatology': 'dermatology', '/endocrinology': 'endocrinology', '/gastro': 'gastroenterology',
            '/pulmonology': 'pulmonology', '/nephrology': 'nephrology', '/rheumatology': 'rheumatology',
            '/infectious': 'infectious disease', '/ophthalmology': 'ophthalmology', '/orthopedics': 'orthopedics',
            '/urology': 'urology', '/geriatrics': 'geriatrics', '/genetics': 'genetics',
            '/immunology': 'immunology', '/nutrition': 'nutrition', '/sleep': 'sleep medicine',
            '/toxicology': 'toxicology', '/travel': 'travel medicine'
        }
        
        matched = False
        for prefix, specialty in specialties.items():
            if cmd.startswith(prefix + ' '):
                topic = cmd[len(prefix)+1:]
                print(f"\n🔬 {specialty.upper()}: {topic}\n")
                print(m.query(topic, specialty))
                print()
                matched = True
                break
        
        if matched:
            continue
        
        # General ask
        if cmd.startswith('/ask '):
            question = cmd[5:]
            print(f"\n🔍 QUESTION: {question}\n")
            print(m.query(question, 'general'))
            print()
            continue
        
        print("Unknown command. Type /help")

if __name__ == "__main__":
    main()