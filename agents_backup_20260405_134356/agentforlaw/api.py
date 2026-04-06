#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uvicorn
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import os

app = FastAPI(title="AgentForLaw API")

SHARED_MEMORY_DIR = Path.home() / ".claw_memory"
DB_PATH = SHARED_MEMORY_DIR / "shared_memory.db"

class LawRequest(BaseModel):
    question: str

class StatuteRequest(BaseModel):
    citation: str

class ContractRequest(BaseModel):
    contract_type: str
    parties: dict
    provisions: dict

class MemoryRequest(BaseModel):
    key: str
    value: str

@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = Path("web/templates/index.html")
    if html_path.exists():
        return html_path.read_text()
    return "<h1>AgentForLaw API</h1><p>Run: python api.py</p>"

@app.post("/analyze")
async def analyze(req: LawRequest):
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"State the law directly. No conversation. Question: {req.question}"}],
        max_tokens=500,
        temperature=0.0
    )
    return {"answer": response.choices[0].message.content}

@app.post("/statute")
async def statute(req: StatuteRequest):
    parts = req.citation.upper().replace('USC', '').strip().split()
    if len(parts) >= 2:
        return {"citation": req.citation, "url": f"https://www.law.cornell.edu/uscode/text/{parts[0]}/{parts[1]}"}
    raise HTTPException(status_code=400, detail="Invalid citation")

@app.get("/case/{case_name}")
async def case(case_name: str):
    return {"case": case_name, "url": f"https://www.courtlistener.com/?q={case_name.replace(' ', '+')}"}

@app.get("/constitution/amendment/{number}")
async def amendment(number: int):
    amendments = {1: "Free speech", 2: "Bear arms", 4: "Search and seizure", 5: "Due process", 14: "Equal protection"}
    return {"amendment": number, "summary": amendments.get(number, "Unknown"), "url": f"https://www.law.cornell.edu/constitution/amendment{number}"}

@app.post("/draft/contract")
async def draft_contract(req: ContractRequest):
    from agentforlaw import LawDocumentDrafting
    result = LawDocumentDrafting.draft_contract(req.contract_type, req.parties, req.provisions)
    return {"contract": result}

@app.post("/draft/will")
async def draft_will(parties: dict, provisions: dict):
    from agentforlaw import LawDocumentDrafting
    result = LawDocumentDrafting.draft_will(parties, provisions)
    return {"will": result}

@app.post("/memory/remember")
async def memory_remember(req: MemoryRequest):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, agent TEXT, key TEXT, value TEXT, timestamp TEXT)")
    cursor.execute("INSERT INTO memories (agent, key, value, timestamp) VALUES (?, ?, ?, ?)", 
                   ("agentforlaw", req.key, req.value, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return {"stored": req.key}

@app.get("/memory/recall/{key}")
async def memory_recall(key: str):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, agent TEXT, key TEXT, value TEXT, timestamp TEXT)")
    cursor.execute("SELECT agent, key, value FROM memories WHERE key LIKE ? ORDER BY timestamp DESC LIMIT 5", (f"%{key}%",))
    results = [{"agent": r[0], "key": r[1], "value": r[2]} for r in cursor.fetchall()]
    conn.close()
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Knowledge Base Endpoints
knowledge_base = {}

@app.post("/knowledge/learn")
async def learn(request: Request):
    data = await request.json()
    topic = data.get("topic")
    content = data.get("content")
    
    if not topic or not content:
        return {"error": "topic and content required"}
    
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = f".claw/knowledge/{timestamp}-{topic.replace(' ', '-')}.md"
    
    with open(filename, "w") as f:
        f.write(f"# {topic}\n\n{content}\n\n---\nLearned: {datetime.now()}")
    
    knowledge_base[topic] = content
    
    return {"stored": topic, "file": filename}

@app.get("/knowledge/recall/{topic}")
async def recall(topic: str):
    if topic in knowledge_base:
        return {"found": True, "content": knowledge_base[topic]}
    
    # Search files
    import glob
    for f in glob.glob(f".claw/knowledge/*{topic}*.md"):
        with open(f, "r") as file:
            return {"found": True, "source": f, "content": file.read()}
    
    return {"found": False, "message": f"No knowledge found for '{topic}'"}

@app.get("/knowledge/list")
async def list_knowledge():
    import glob
    files = glob.glob(".claw/knowledge/*.md")
    return {"entries": [f.replace(".claw/knowledge/", "") for f in files]}
