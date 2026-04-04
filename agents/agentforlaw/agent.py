#!/usr/bin/env python3
import os
import sys
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask(question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"State the law directly. No conversation. Question: {question}"}],
        max_tokens=300,
        temperature=0.0
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print(ask(" ".join(sys.argv[1:])))
