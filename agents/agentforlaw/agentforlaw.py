#!/usr/bin/env python3
"""
AgentForLaw - Applies LAW. Groq only. No garbage.
"""

import os
import json
import sqlite3
import re
from datetime import datetime
from pathlib import Path
from groq import Groq

# ============================================================
# SHARED MEMORY
# ============================================================
SHARED_MEMORY_DIR = Path.home() / ".claw_memory"
SHARED_MEMORY_DIR.mkdir(exist_ok=True)
DB_PATH = SHARED_MEMORY_DIR / "shared_memory.db"

class SharedMemory:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()
        self._init_tables()
    
    def _init_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, agent TEXT, key TEXT, value TEXT, timestamp TEXT, tags TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS agent_registry (agent_id TEXT PRIMARY KEY, name TEXT, repo TEXT, capabilities TEXT, last_seen TEXT)''')
        self.conn.commit()
    
    def remember(self, key, value, tags=""):
        self.cursor.execute("INSERT INTO memories (agent, key, value, timestamp, tags) VALUES (?, ?, ?, ?, ?)", 
                          ("agentforlaw", key, value, datetime.now().isoformat(), tags))
        self.conn.commit()
    
    def recall(self, key):
        self.cursor.execute("SELECT agent, key, value, tags FROM memories WHERE key LIKE ? ORDER BY timestamp DESC LIMIT 10", (f"%{key}%",))
        return self.cursor.fetchall()
    
    def register(self):
        self.cursor.execute("INSERT OR REPLACE INTO agent_registry VALUES (?, ?, ?, ?, ?)", 
                          ("agentforlaw", "AgentForLaw", "https://github.com/greg-gzillion/agentforlaw", 
                           "law, statutes, constitution, case law, contracts, wills, trusts", datetime.now().isoformat()))
        self.conn.commit()
    
    def get_other_agents(self):
        self.cursor.execute("SELECT name, capabilities FROM agent_registry WHERE agent_id != 'agentforlaw'")
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()

# ============================================================
# LAW ANALYSIS (Groq only)
# ============================================================
class LawAnalyzer:
    @staticmethod
    def analyze(question):
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"State the law directly. No conversation. No suggestions. Question: {question}"}],
            max_tokens=500,
            temperature=0.0
        )
        return response.choices[0].message.content

# ============================================================
# LAW DOCUMENT DRAFTING
# ============================================================
class LawDocumentDrafting:
    @staticmethod
    def draft_contract(contract_type, parties, terms):
        defaults = {'governing_law': 'Delaware', 'services': 'services', 'payment': '$0', 'goods': 'goods', 'price': '$0', 
                   'position': 'position', 'salary': '$0', 'premises': 'premises', 'rent': '$0', 'term': 'one year', 
                   'purpose': 'business', 'sharing': 'equal', 'principal': '$0', 'interest': '0', 'repayment': 'on demand'}
        for key, default in defaults.items():
            if key not in terms:
                terms[key] = default
        
        templates = {
            "service": {"title": "SERVICE CONTRACT", "clauses": ["PARTIES: {party_a} and {party_b}", "SERVICES: {services}", "PAYMENT: {payment}", "GOVERNING LAW: {governing_law}"]},
            "sale": {"title": "SALES CONTRACT", "clauses": ["SELLER: {seller} BUYER: {buyer}", "GOODS: {goods}", "PRICE: {price}", "GOVERNING LAW: {governing_law}"]},
            "employment": {"title": "EMPLOYMENT CONTRACT", "clauses": ["EMPLOYER: {employer} EMPLOYEE: {employee}", "POSITION: {position}", "SALARY: {salary}", "GOVERNING LAW: {governing_law}"]},
            "lease": {"title": "LEASE CONTRACT", "clauses": ["LANDLORD: {landlord} TENANT: {tenant}", "PREMISES: {premises}", "RENT: {rent}", "TERM: {term}", "GOVERNING LAW: {governing_law}"]},
            "partnership": {"title": "PARTNERSHIP AGREEMENT", "clauses": ["PARTNERS: {partner_a} and {partner_b}", "PURPOSE: {purpose}", "PROFIT SHARING: {sharing}", "GOVERNING LAW: {governing_law}"]},
            "loan": {"title": "LOAN AGREEMENT", "clauses": ["LENDER: {lender} BORROWER: {borrower}", "PRINCIPAL: {principal}", "INTEREST: {interest}%", "REPAYMENT: {repayment}", "GOVERNING LAW: {governing_law}"]}
        }
        
        t = templates.get(contract_type, templates["service"])
        result = f"\n{'='*60}\n{t['title']}\n{'='*60}\n\n"
        format_dict = {**parties, **terms}
        for clause in t['clauses']:
            try:
                result += f"{clause.format(**format_dict)}\n\n"
            except KeyError:
                result += f"{clause}\n\n"
        result += f"\nDate: {datetime.now().strftime('%B %d, %Y')}\n{'='*60}\n"
        return result
    
    @staticmethod
    def draft_will(parties, provisions):
        date = datetime.now().strftime("%B %d, %Y")
        return f"\n{'='*60}\nLAST WILL AND TESTAMENT OF {parties.get('name', '_________')}\n{'='*60}\n\nI, {parties.get('name', '_________')}, declare this to be my Will.\n\nARTICLE I: EXECUTOR\nI appoint {provisions.get('executor', '_________')} as Executor.\n\nARTICLE II: DISPOSITION\nI give my estate to {provisions.get('beneficiary', '_________')}.\n\nARTICLE III: GOVERNING LAW\nThis Will is governed by {provisions.get('governing_state', '_________')}.\n\nIN WITNESS WHEREOF on {date}.\n\n{parties.get('name', '_________')} (Testator)\nWitness 1: _________    Witness 2: _________\n{'='*60}"
    
    @staticmethod
    def draft_trust(parties, provisions):
        date = datetime.now().strftime("%B %d, %Y")
        return f"\n{'='*60}\nREVOCABLE LIVING TRUST OF {parties.get('name', '_________')}\n{'='*60}\n\nSettlor: {parties.get('name', '_________')}\nTrustee: {provisions.get('trustee', '_________')}\nBeneficiaries: {provisions.get('beneficiaries', '_________')}\n\nGoverning Law: {provisions.get('governing_state', '_________')}\n\nExecuted on {date}.\n\n{parties.get('name', '_________')} (Settlor)\n{provisions.get('trustee', '_________')} (Trustee)\n{'='*60}"
    
    @staticmethod
    def draft_estate_document(doc_type, parties, provisions):
        date = datetime.now().strftime("%B %d, %Y")
        templates = {
            "power_of_attorney": f"\n{'='*60}\nDURABLE POWER OF ATTORNEY\n{'='*60}\n\nI, {parties.get('principal', '_________')}, appoint {provisions.get('agent', '_________')} as my Attorney-in-Fact.\n\nExecuted on {date}.\n\n{parties.get('principal', '_________')} (Principal)\n{'='*60}",
            "healthcare_directive": f"\n{'='*60}\nADVANCE HEALTH CARE DIRECTIVE\n{'='*60}\n\nI, {parties.get('principal', '_________')}, appoint {provisions.get('agent', '_________')} as my Health Care Agent.\n\nExecuted on {date}.\n\n{parties.get('principal', '_________')} (Principal)\n{'='*60}",
            "living_will": f"\n{'='*60}\nLIVING WILL\n{'='*60}\n\nI, {parties.get('declarant', '_________')}, direct that life-sustaining treatment be withheld if I have a terminal condition.\n\nExecuted on {date}.\n\n{parties.get('declarant', '_________')} (Declarant)\n{'='*60}"
        }
        return templates.get(doc_type, "Unknown document type")

# ============================================================
# CONSTITUTION & STATUTES
# ============================================================
class ConstitutionAccess:
    @staticmethod
    def get_article(article, section=None):
        articles = {1: "Legislative Branch", 2: "Executive Branch", 3: "Judicial Branch", 4: "States' Powers", 5: "Amendment Process", 6: "Federal Supremacy", 7: "Ratification"}
        result = {"article": article, "title": articles.get(article, "Unknown")}
        if section:
            result["section"] = section
            result["url"] = f"https://www.law.cornell.edu/constitution/article{article}#section{section}"
        else:
            result["url"] = f"https://www.law.cornell.edu/constitution/article{article}"
        return result
    
    @staticmethod
    def get_amendment(number):
        amendments = {1: "Free speech, religion, press, assembly", 2: "Right to bear arms", 4: "Search and seizure", 5: "Due process", 6: "Speedy trial", 8: "No cruel punishment", 10: "States' powers", 13: "Abolish slavery", 14: "Equal protection", 19: "Women's suffrage"}
        return {"amendment": number, "summary": amendments.get(number, "Not in library"), "url": f"https://www.law.cornell.edu/constitution/amendment{number}"}

class LawRetriever:
    @staticmethod
    def get_statute(citation):
        parts = citation.upper().replace('USC', '').strip().split()
        if len(parts) >= 2:
            return {"citation": citation, "url": f"https://www.law.cornell.edu/uscode/text/{parts[0]}/{parts[1]}"}
        return {"error": "Invalid format. Example: 15 USC 78a"}
    
    @staticmethod
    def get_case(case_name):
        return {"case": case_name, "url": f"https://www.courtlistener.com/?q={case_name.replace(' ', '+')}"}
    
    @staticmethod
    def get_cfr(citation):
        match = re.search(r'(\d+)\s+CFR\s+([\d\.]+)', citation, re.IGNORECASE)
        if match:
            return {"citation": citation, "url": f"https://www.ecfr.gov/current/title-{match.group(1)}/section-{match.group(2)}"}
        return {"error": "Invalid format. Example: 17 CFR 240.10b-5"}

class ClauseLibrary:
    CLAUSES = {
        "indemnification": "The indemnifying party shall defend, indemnify, and hold harmless the indemnified party from any and all claims arising out of this Agreement.",
        "confidentiality": "The receiving party shall not disclose confidential information to any third party without written consent.",
        "termination": "Either party may terminate this Agreement upon 30 days written notice.",
        "governing_law": "This Agreement shall be governed by the laws of the State of Delaware.",
        "arbitration": "Any dispute shall be resolved by binding arbitration."
    }
    
    @staticmethod
    def get_clause(name):
        return ClauseLibrary.CLAUSES.get(name, f"Clause '{name}' not found")
    
    @staticmethod
    def list_clauses():
        return list(ClauseLibrary.CLAUSES.keys())

class LegalDefinitions:
    DEFINITIONS = {
        "consideration": "Something of value given in exchange for a promise in a contract.",
        "due_process": "Constitutional requirement that government respect all legal rights. Fifth and Fourteenth Amendments.",
        "tort": "A civil wrong causing harm, giving the right to sue for damages.",
        "contract": "A legally enforceable agreement between two or more parties."
    }
    
    @staticmethod
    def define(term):
        return {"term": term, "definition": LegalDefinitions.DEFINITIONS.get(term.lower(), "Definition not found")}
    
    @staticmethod
    def list_terms():
        return list(LegalDefinitions.DEFINITIONS.keys())

# ============================================================
# MAIN
# ============================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="AgentForLaw - Applies LAW")
    
    parser.add_argument("--analyze", help="Analyze a law question")
    parser.add_argument("--statute", help="Look up US Code")
    parser.add_argument("--case", help="Search case law")
    parser.add_argument("--cfr", help="Look up regulation")
    parser.add_argument("--constitution", action="store_true")
    parser.add_argument("--article", type=int)
    parser.add_argument("--section", type=int)
    parser.add_argument("--amendment", type=int)
    parser.add_argument("--draft-contract", choices=["service", "sale", "employment", "lease", "partnership", "loan"])
    parser.add_argument("--draft-will", action="store_true")
    parser.add_argument("--draft-trust", action="store_true")
    parser.add_argument("--draft-estate", choices=["power_of_attorney", "healthcare_directive", "living_will"])
    parser.add_argument("--parties")
    parser.add_argument("--provisions")
    parser.add_argument("--list-clauses", action="store_true")
    parser.add_argument("--clause")
    parser.add_argument("--define")
    parser.add_argument("--list-terms", action="store_true")
    parser.add_argument("--remember", nargs=2, metavar=('KEY', 'VALUE'))
    parser.add_argument("--recall")
    parser.add_argument("--agents", action="store_true")
    parser.add_argument("--agencies", action="store_true")
    parser.add_argument("--domains", action="store_true")
    
    args = parser.parse_args()
    shared = SharedMemory()
    shared.register()
    
    if args.analyze:
        print(LawAnalyzer.analyze(args.analyze))
    elif args.statute:
        print(json.dumps(LawRetriever.get_statute(args.statute), indent=2))
    elif args.case:
        print(json.dumps(LawRetriever.get_case(args.case), indent=2))
    elif args.cfr:
        print(json.dumps(LawRetriever.get_cfr(args.cfr), indent=2))
    elif args.constitution:
        if args.amendment:
            print(json.dumps(ConstitutionAccess.get_amendment(args.amendment), indent=2))
        elif args.article:
            print(json.dumps(ConstitutionAccess.get_article(args.article, args.section), indent=2))
    elif args.draft_contract:
        parties = json.loads(args.parties) if args.parties else {}
        provisions = json.loads(args.provisions) if args.provisions else {}
        print(LawDocumentDrafting.draft_contract(args.draft_contract, parties, provisions))
    elif args.draft_will:
        parties = json.loads(args.parties) if args.parties else {}
        provisions = json.loads(args.provisions) if args.provisions else {}
        print(LawDocumentDrafting.draft_will(parties, provisions))
    elif args.draft_trust:
        parties = json.loads(args.parties) if args.parties else {}
        provisions = json.loads(args.provisions) if args.provisions else {}
        print(LawDocumentDrafting.draft_trust(parties, provisions))
    elif args.draft_estate:
        parties = json.loads(args.parties) if args.parties else {}
        provisions = json.loads(args.provisions) if args.provisions else {}
        print(LawDocumentDrafting.draft_estate_document(args.draft_estate, parties, provisions))
    elif args.list_clauses:
        for c in ClauseLibrary.list_clauses():
            print(f"  • {c}")
    elif args.clause:
        print(ClauseLibrary.get_clause(args.clause))
    elif args.define:
        print(json.dumps(LegalDefinitions.define(args.define), indent=2))
    elif args.list_terms:
        for t in LegalDefinitions.list_terms():
            print(f"  • {t}")
    elif args.remember:
        shared.remember(args.remember[0], args.remember[1])
        print(f"✅ Stored: {args.remember[0]}")
    elif args.recall:
        results = shared.recall(args.recall)
        for r in results:
            print(f"\n🦞 {r[0]}: {r[1]}\n   {r[2][:200]}")
    elif args.agents:
        for name, caps in shared.get_other_agents():
            print(f"  {name}: {caps[:60]}...")
    elif args.agencies:
        print("\nAgencies: SEC, CFTC, FINRA")
    elif args.domains:
        print("\nLaw Domains: constitutional, statutory, regulatory, case_law, contract, tort")
    else:
        parser.print_help()
    
    shared.close()

if __name__ == "__main__":
    main()

# Add to argument parser (after other arguments)
parser.add_argument("--remember", nargs=2, metavar=('KEY', 'VALUE'), help="Store in shared memory")
parser.add_argument("--recall", metavar='KEY', help="Retrieve from shared memory")
parser.add_argument("--agents", action="store_true", help="List all registered agents")
