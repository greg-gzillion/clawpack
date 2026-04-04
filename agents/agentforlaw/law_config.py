"""
AgentForLaw Configuration - NO LEGAL JARGON
We apply law. We are not lawyers.
"""

# Prohibited phrases - these will be filtered from ALL output
PROHIBITED_PHRASES = [
    "legal advice", "attorney", "lawyer", "law firm",
    "retain counsel", "seek legal representation", "consult an attorney",
    "party of the first part", "party of the second part", "witnesseth",
    "heretofore", "wherein", "whereas", "aforesaid", "hereinafter",
    "notwithstanding", "in witness whereof", "know all men by these presents"
]

# Plain language replacements
REPLACEMENTS = {
    "party of the first part": "first party",
    "party of the second part": "second party",
    "witnesseth": "this document shows",
    "hereinafter": "from now on",
    "notwithstanding": "even if",
    "pursuant to": "under",
    "in accordance with": "following",
}

# System prompt for ALL AI models
LAW_ONLY_SYSTEM_PROMPT = """You are AgentForLaw. You apply LAW. You are not a lawyer.
Rules:
1. Never use legal jargon like "whereas", "heretofore", "party of the first part"
2. Never say "legal advice" or "consult an attorney"
3. Use plain English
4. State only what the law says (statutes, codes, regulations, constitutions)
5. Be direct. No greetings. No questions. No "how can I assist"
6. If asked about something outside law, say "I only apply law"
"""

# Test the config
if __name__ == "__main__":
    print("AgentForLaw - NO LEGAL JARGON")
    print("=" * 40)
    print(f"Blocking {len(PROHIBITED_PHRASES)} legal phrases")
    print(f"Replacing {len(REPLACEMENTS)} jargon terms")
    print("\nExample output will be plain English, not lawyer speak.")
