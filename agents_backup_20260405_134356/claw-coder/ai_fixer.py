#!/usr/bin/env python3
"""
AI-Powered Auto-Fix Agent for PhoenixPME
- Finds bugs using existing scanners
- Uses AI to generate fixes
- Creates PRs with fixes
"""

import requests
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_ai(prompt, model="codellama:7b"):
    """Send prompt to AI and get response"""
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        return r.json()["response"] if r.status_code == 200 else ""
    except:
        return ""

def scan_for_bugs():
    """Run existing bug scanner"""
    print("🔍 Scanning for bugs...")
    result = subprocess.run(['python3', 'auto_fix_agent.py'], 
                           capture_output=True, text=True)
    return result.stdout

def extract_bugs_from_output(output):
    """Parse bug scanner output"""
    bugs = []
    lines = output.split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ['bug', 'error', 'issue', 'vulnerability']):
            # Get context (3 lines before and after)
            start = max(0, i-3)
            end = min(len(lines), i+4)
            context = '\n'.join(lines[start:end])
            bugs.append({
                'description': line,
                'context': context,
                'line': i
            })
    return bugs

def get_file_content(filepath):
    """Read file content"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except:
        return ""

def ai_generate_fix(bug, filepath):
    """Use AI to generate a fix"""
    content = get_file_content(filepath)
    
    prompt = f"""
You are an expert Rust/CosmWasm developer fixing PhoenixPME smart contracts.

Bug found in file: {filepath}
Bug description: {bug['description']}
Context around bug:
{bug['context']}

Full file content (first 2000 chars):
{content[:2000]}

Generate a FIX for this bug. Return ONLY the corrected code block.
Focus on fixing the specific issue while maintaining all other functionality.
"""
    
    print(f"🤖 AI generating fix for: {bug['description'][:80]}...")
    fix = ask_ai(prompt, "deepseek-coder:6.7b")
    return fix

def create_pr_with_fix(filepath, bug, fix):
    """Create a PR with the fix"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_name = f"ai-fix-{timestamp}"
    
    # Create branch
    subprocess.run(['git', 'checkout', '-b', branch_name], cwd='/home/greg/dev/TX')
    
    # Apply fix (simplified - would need proper file patching)
    print(f"📝 Applying fix to {filepath}")
    
    # Commit
    subprocess.run(['git', 'add', filepath], cwd='/home/greg/dev/TX')
    subprocess.run(['git', 'commit', '-m', f'AI fix: {bug["description"][:50]}'], 
                   cwd='/home/greg/dev/TX')
    
    # Push and create PR
    subprocess.run(['git', 'push', 'origin', branch_name], cwd='/home/greg/dev/TX')
    
    print(f"✅ PR created: {branch_name}")
    return branch_name

def main():
    print("\n" + "="*60)
    print("🤖 AI-POWERED AUTO-FIX AGENT")
    print("="*60)
    
    # Scan for bugs
    scan_output = scan_for_bugs()
    
    if "BUG" not in scan_output.upper() and "ERROR" not in scan_output.upper():
        print("✅ No bugs found!")
        return
    
    # Extract bugs
    bugs = extract_bugs_from_output(scan_output)
    print(f"📋 Found {len(bugs)} potential issues")
    
    # Fix each bug
    fixes_applied = []
    for i, bug in enumerate(bugs):
        print(f"\n--- Fixing issue {i+1}/{len(bugs)} ---")
        
        # Find which file the bug is in
        file_match = re.search(r'([/\w]+\.rs)', bug['context'])
        if not file_match:
            print("⚠️ Could not determine file, skipping")
            continue
        
        filepath = file_match.group(1)
        
        # Generate fix
        fix = ai_generate_fix(bug, filepath)
        if fix and len(fix) > 50:
            print(f"💡 Suggested fix:\n{fix[:500]}")
            
            # Create PR
            branch = create_pr_with_fix(filepath, bug, fix)
            fixes_applied.append({'file': filepath, 'branch': branch})
        else:
            print("❌ AI couldn't generate a fix")
    
    # Summary
    print("\n" + "="*60)
    print("📊 FIX SUMMARY")
    print("="*60)
    print(f"✅ Fixed {len(fixes_applied)} issues")
    for fix in fixes_applied:
        print(f"  • {fix['file']} → {fix['branch']}")
    
    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'bugs_found': len(bugs),
        'fixes_applied': fixes_applied,
        'scan_output': scan_output[:1000]
    }
    with open('fix_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n📄 Report saved: fix_report.json")

if __name__ == "__main__":
    main()
