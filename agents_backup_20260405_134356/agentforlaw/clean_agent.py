#!/usr/bin/env python3
"""
AgentForLaw - Pure Agent of LAW (no legal, no garbage)
Studies and applies LAW: statutes, codes, regulations, constitutions, case law
"""

import os
import json
import re
from datetime import datetime

class LawAnalyzer:
    @staticmethod
    def analyze(question):
        """Pure law analysis using Groq only"""
        try:
            from groq import Groq
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are AgentForLaw. Answer only about LAW (statutes, codes, regulations, constitutions, case law). Do not give legal advice. Do not practice law. Only state what the law says."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Law analysis error: {e}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        print(LawAnalyzer.analyze(q))
