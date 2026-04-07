#!/usr/bin/env python3
"""
AGENTFORLAW - Open Court Access Agent
Part of Clawpack Cross-Learning Ecosystem
"""

import sys
import sqlite3
import re
import urllib.request
import urllib.parse
import json
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser

# ============================================
# CLAWPACK PATHS
# ============================================
AGENT_DIR = Path(__file__).parent
ROOT_DIR = Path(r"C:\Users\greg\dev\clawpack")
WEBCLAW_REFS = Path(r"C:\Users\greg\dev\clawpack\agents\webclaw\references\agentforlaw")
SHARED_DB = Path.home() / ".claw_memory" / "shared_memory.db"

# ============================================
# SHARED MEMORY
# ============================================
SHARED_DB.parent.mkdir(exist_ok=True)

def init_shared_memory():
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agentforlaw_knowledge
                 (id INTEGER PRIMARY KEY, query TEXT UNIQUE, 
                  response TEXT, category TEXT, jurisdiction TEXT,
                  timestamp TEXT, source_agent TEXT, usage_count INTEGER DEFAULT 1)''')
    c.execute('''CREATE TABLE IF NOT EXISTS case_searches
                 (id INTEGER PRIMARY KEY, query TEXT, citation TEXT,
                  court TEXT, date TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_to_shared_memory(query, response, category="general", jurisdiction="federal"):
    try:
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO agentforlaw_knowledge 
                     (query, response, category, jurisdiction, timestamp, source_agent, usage_count) 
                     VALUES (?,?,?,?,?,?,1)''',
                  (query.lower(), response[:500], category, jurisdiction, 
                   datetime.now().isoformat(), "agentforlaw"))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

# ============================================
# SIMPLE HTML STRIPPER
# ============================================
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    def handle_data(self, d):
        self.text.append(d)
    def get_data(self):
        return ''.join(self.text)

def strip_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# ============================================
# WEB RETRIEVAL (NO BROWSER)
# ============================================
def fetch_url_content(url, timeout=10):
    """Fetch content from URL without opening browser"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode('utf-8', errors='ignore')
            # Strip HTML tags
            text = strip_html(content)
            # Clean up whitespace
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n'.join(lines[:100])  # First 100 lines
    except Exception as e:
        return f"Error fetching: {e}"

def search_case_law(query):
    """Search case law and return results (no browser opening)"""
    encoded = urllib.parse.quote(query)
    
    # Use CourtListener API (free, no API key needed for basic search)
    url = f"https://www.courtlistener.com/api/rest/v3/search/?q={encoded}&type=o"
    
    try:
        headers = {'User-Agent': 'AgentForLaw/1.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            results = []
            for result in data.get('results', [])[:5]:
                results.append({
                    'title': result.get('caseName', 'Unknown'),
                    'court': result.get('court', 'Unknown'),
                    'date': result.get('dateFiled', 'Unknown'),
                    'url': result.get('absolute_url', ''),
                    'snippet': result.get('snippet', '')[:300]
                })
            return results
    except Exception as e:
        return [{'error': f"API error: {e}. Try: https://scholar.google.com/scholar?q={encoded}"}]

# ============================================
# WEBCLAW QUERY FUNCTIONS
# ============================================

def query_webclaw_reference(topic):
    """Search Webclaw reference files for information"""
    if not WEBCLAW_REFS.exists():
        return None
    
    topic_lower = topic.lower()
    results = []
    
    for category_dir in WEBCLAW_REFS.iterdir():
        if category_dir.is_dir():
            for md_file in category_dir.glob("*.md"):
                try:
                    content = md_file.read_text(encoding='utf-8')
                    if topic_lower in content.lower():
                        results.append({
                            "category": category_dir.name,
                            "file": md_file.name,
                            "content": content[:1000]
                        })
                except:
                    pass
    
    return results[:5]

def get_specific_county_info(state, county):
    """Get information for a specific county"""
    county_path = WEBCLAW_REFS / "jurisdictions" / state.upper() / county
    
    if not county_path.exists():
        return f"County '{county}' not found in {state}. Use /court {state} to see all counties."
    
    output = [f"# {county} County, {state}\n"]
    
    for court_file in sorted(county_path.glob("*.md")):
        court_name = court_file.stem.replace('_', ' ').title()
        content = court_file.read_text(encoding='utf-8')
        output.append(f"\n## {court_name}\n{content}")
    
    return "\n".join(output)

def get_court_info(jurisdiction):
    """Get court information from Webclaw jurisdictions folder"""
    if '/' in jurisdiction:
        state, county = jurisdiction.split('/', 1)
        state = state.upper()
        county = county.title()
        return get_specific_county_info(state, county)
    
    juris_path = WEBCLAW_REFS / "jurisdictions" / jurisdiction.upper()
    
    if not juris_path.exists():
        return None
    
    output = []
    
    # Read state-level court information
    state_dir = juris_path / "state"
    if state_dir.exists():
        for filename in ['supreme_court.md', 'court_of_appeals.md', 'state_resources.md']:
            file_path = state_dir / filename
            if file_path.exists():
                output.append(file_path.read_text(encoding='utf-8'))
    
    # List all county directories
    counties = []
    for item in juris_path.iterdir():
        if item.is_dir() and item.name not in ['state', 'federal']:
            counties.append(item.name)
    
    if counties:
        output.append(f"\n## COUNTIES ({len(counties)})\n")
        output.append(f"\nTip: Use /court {jurisdiction.upper()}/[CountyName] to view a specific county\n")
        
        county_list = sorted(counties)
        output.append(f"**Counties:** {', '.join(county_list[:30])}")
        if len(county_list) > 30:
            output.append(f"\n... and {len(county_list) - 30} more counties")
        
        # Show first 2 counties as examples
        output.append(f"\n### Example County Courts (first 2 counties)\n")
        for county in county_list[:2]:
            output.append(f"\n#### {county} County")
            for court_file in sorted((juris_path / county).glob("*.md")):
                court_name = court_file.stem.replace('_', ' ').title()
                content = court_file.read_text(encoding='utf-8')
                if len(content) > 200:
                    content = content[:200] + "..."
                output.append(f"\n**{court_name}**\n{content}")
    
    return "\n".join(output) if output else None

def get_federal_court_info(circuit=None, district=None):
    """Get federal court information from Webclaw"""
    federal_path = WEBCLAW_REFS / "jurisdictions" / "federal"
    
    if not federal_path.exists():
        return None
    
    results = []
    for district_dir in federal_path.iterdir():
        if district_dir.is_dir():
            if circuit and circuit.lower() in district_dir.name.lower():
                court_file = district_dir / "district_court.md"
                if court_file.exists():
                    results.append(court_file.read_text(encoding='utf-8'))
            elif not circuit:
                # Show list of available circuits
                results.append(f"  • {district_dir.name}")
    
    if results:
        if circuit:
            return "\n".join(results)
        else:
            return f"Available federal circuits:\n" + "\n".join(results[:10])
    
    return None

# ============================================
# CITATION PARSING
# ============================================

CITATION_PATTERNS = {
    "supreme_court": r'(\d+)\s+U\.?S\.?\s+(\d+)',
    "federal_reporter": r'(\d+)\s+F\.\s*(\d+)[a-z]?\s+(\d+)',
    "federal_supplement": r'(\d+)\s+F\.\s*Supp\.\s*(\d+)[a-z]?\s+(\d+)',
}

def parse_citation(text):
    """Parse legal citation from text"""
    matches = []
    for cite_type, pattern in CITATION_PATTERNS.items():
        found = re.findall(pattern, text)
        for match in found:
            matches.append({"type": cite_type, "citation": text, "components": match})
    return matches

def get_case_by_citation(citation):
    """Look up case by citation using free API"""
    encoded = urllib.parse.quote(citation)
    url = f"https://www.courtlistener.com/api/rest/v3/search/?q={encoded}&type=o"
    try:
        headers = {'User-Agent': 'AgentForLaw/1.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('results'):
                result = data['results'][0]
                return {
                    'title': result.get('caseName', 'Unknown'),
                    'court': result.get('court', 'Unknown'),
                    'date': result.get('dateFiled', 'Unknown'),
                    'url': f"https://www.courtlistener.com{result.get('absolute_url', '')}",
                    'snippet': result.get('snippet', '')[:500]
                }
    except Exception as e:
        return {'error': str(e)}
    return None

# ============================================
# MAIN AGENT CLASS
# ============================================

class AgentForLaw:
    def __init__(self):
        self.name = "agentforlaw"
        init_shared_memory()
        self.print_welcome()
    
    def print_welcome(self):
        print("\n" + "="*70)
        print("AGENTFORLAW - Open Court Access")
        print("="*70)
        print("FREE ACCESS TO:")
        print("  * All US court systems (via Webclaw references)")
        print("  * 50 State Courts + Federal Courts")
        print("  * Case law search (no browser windows)")
        print("  * Legal citations and forms")
        print("="*70)
        print("\nCOMMANDS:")
        print("  /search [query]       - Search case law (returns results)")
        print("  /cite [citation]      - Look up specific citation")
        print("  /court [state]        - Get state court information")
        print("  /court [state]/[cty]  - Get specific county court")
        print("  /federal [circuit]    - Get federal court information")
        print("  /ref [topic]          - Search Webclaw references")
        print("  /stats                - Show shared memory stats")
        print("  /help, /quit")
        print("="*70)
        print("All references come from Webclaw - the central hub")
        print("="*70)
    
    def handle_search(self, query):
        """Search case law - NO BROWSER OPENING"""
        print(f"\nSearching for: {query}")
        print("-" * 50)
        
        # First check Webclaw references
        refs = query_webclaw_reference(query)
        if refs:
            print("Found in Webclaw references:")
            for ref in refs:
                print(f"  * {ref['category']}/{ref['file']}")
            print()
        
        # Search CourtListener API
        results = search_case_law(query)
        
        if results and not results[0].get('error'):
            print(f"Found {len(results)} cases:\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['title']}")
                print(f"   Court: {r['court']} | Date: {r['date']}")
                print(f"   Summary: {r['snippet'][:200]}...")
                print(f"   URL: https://www.courtlistener.com{r['url']}")
                print()
        else:
            error_msg = results[0].get('error', 'No results found') if results else 'No results found'
            print(f"API Note: {error_msg}")
            print("\nAlternative: Use Google Scholar manually at:")
            print(f"  https://scholar.google.com/scholar?q={urllib.parse.quote(query)}")
        
        save_to_shared_memory(query, f"Searched: {query}", "search")
    
    def handle_cite(self, citation_text):
        """Look up specific citation"""
        print(f"\nLooking up citation: {citation_text}")
        print("-" * 50)
        
        case = get_case_by_citation(citation_text)
        if case and not case.get('error'):
            print(f"Case: {case['title']}")
            print(f"Court: {case['court']}")
            print(f"Date: {case['date']}")
            print(f"\nSummary: {case['snippet']}")
            print(f"\nFull text: {case['url']}")
        else:
            print("Citation not found in free databases.")
            print("Try using Google Scholar:")
            print(f"  https://scholar.google.com/scholar?q={urllib.parse.quote(citation_text)}")
    
    def handle_court(self, jurisdiction):
        print(f"\nLooking up court information for: {jurisdiction}")
        print("-" * 50)
        
        info = get_court_info(jurisdiction)
        if info:
            print(info)
            save_to_shared_memory(f"court_{jurisdiction}", info[:500], "court_info", jurisdiction)
        else:
            federal_info = get_federal_court_info(jurisdiction)
            if federal_info:
                print(federal_info)
            else:
                print(f"No court information found for: {jurisdiction}")
    
    def handle_federal(self, circuit):
        print(f"\nLooking up federal court information for Circuit: {circuit}")
        print("-" * 50)
        
        info = get_federal_court_info(circuit)
        if info:
            print(info)
            save_to_shared_memory(f"federal_{circuit}", info[:500], "federal_court", circuit)
        else:
            print(f"No federal court information found for: {circuit}")
            get_federal_court_info()  # Show available circuits
    
    def handle_ref(self, topic):
        print(f"\nSearching Webclaw references for: {topic}")
        print("-" * 50)
        
        results = query_webclaw_reference(topic)
        if results:
            for r in results:
                print(f"\nCategory: {r['category']}")
                print(f"File: {r['file']}")
                print(f"Content:\n{r['content'][:500]}...")
        else:
            print(f"No references found for: {topic}")
    
    def show_stats(self):
        conn = sqlite3.connect(str(SHARED_DB))
        c = conn.cursor()
        
        try:
            c.execute('SELECT COUNT(*) FROM agentforlaw_knowledge')
            count = c.fetchone()[0]
            print(f"\nShared memory entries: {count}")
            
            print("\nRecent knowledge:")
            c.execute('SELECT query, category, timestamp FROM agentforlaw_knowledge ORDER BY id DESC LIMIT 5')
            for row in c.fetchall():
                print(f"  * {row[0][:40]}... ({row[1]}) - {row[2][:16]}")
        except:
            print("No knowledge in shared memory yet")
        
        conn.close()
    
    def run(self):
        self.print_welcome()
        
        while True:
            try:
                cmd = input("\nAgentForLaw> ").strip()
                if not cmd:
                    continue
                
                if cmd == "/quit":
                    print("Goodbye!")
                    break
                elif cmd == "/help":
                    self.print_welcome()
                elif cmd == "/stats":
                    self.show_stats()
                elif cmd.startswith("/search "):
                    self.handle_search(cmd[8:])
                elif cmd.startswith("/court "):
                    self.handle_court(cmd[7:])
                elif cmd.startswith("/federal "):
                    self.handle_federal(cmd[9:])
                elif cmd.startswith("/cite "):
                    self.handle_cite(cmd[6:])
                elif cmd.startswith("/ref "):
                    self.handle_ref(cmd[5:])
                else:
                    self.handle_search(cmd)
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    agent = AgentForLaw()
    agent.run()

# ============================================
# CROSS-AGENT COMMANDS ADDED
# ============================================

def search_all_agents(query_text):
    """Search ALL agent tables in shared memory"""
    import sqlite3
    results = []
    
    conn = sqlite3.connect(str(SHARED_DB))
    c = conn.cursor()
    query_lower = query_text.lower()
    
    tables_to_search = [
        ('agentforlaw_knowledge', 'query', 'response', '⚖️'),
        ('medical_knowledge', 'query', 'response', '🏥'),
        ('math_knowledge', 'query', 'response', '📐'),
        ('translations', 'source_text', 'translated_text', '🌐'),
        ('unified_knowledge', 'query', 'response', '🧠'),
        ('memories', 'memory_text', 'memory_text', '💾'),
        ('documents', 'title', 'content', '📄')
    ]
    
    for table, q_col, r_col, icon in tables_to_search:
        try:
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not c.fetchone():
                continue
            c.execute(f"SELECT {q_col}, {r_col} FROM {table} WHERE LOWER({q_col}) LIKE ? LIMIT 5", 
                      (f'%{query_lower}%',))
            for row in c.fetchall():
                agent_name = table.replace('_knowledge', '').replace('_', ' ').title()
                results.append({
                    'icon': icon,
                    'agent': agent_name,
                    'query': row[0][:100] if row[0] else "N/A",
                    'response': row[1][:300] if row[1] else "N/A"
                })
        except:
            pass
    conn.close()
    return results

# Add /cross command to AgentForLaw class (monkey patch)
original_handle = AgentForLaw.handle_cross_search if hasattr(AgentForLaw, 'handle_cross_search') else None

def handle_cross_search(self, query):
    """Search all agents' knowledge"""
    print(f"\n🔍 Searching ALL agents for: {query}")
    print("-" * 50)
    results = search_all_agents(query)
    if results:
        print(f"✅ Found {len(results)} results across agents:\n")
        for r in results:
            print(f"  {r['icon']} {r['agent']}:")
            print(f"     Q: {r['query']}")
            print(f"     A: {r['response'][:150]}...")
            print()
    else:
        print("❌ No results found. Try a different query.")

AgentForLaw.handle_cross_search = handle_cross_search

print("✅ /cross command added to AgentForLaw")
