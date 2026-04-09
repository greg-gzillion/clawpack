#!/usr/bin/env python3
"""
WEBCLAW - Court Data Reporter (READ ONLY)
Scans all courts and reports potential issues without changing anything
"""

import re
from pathlib import Path

JURISDICTIONS = Path(r"C:\Users\greg\dev\clawpack\agents\webclaw\references\agentforlaw\jurisdictions")

class CourtReporter:
    def __init__(self):
        self.issues = []
        self.checked = 0
    
    def scan_all(self):
        print("\n" + "="*70)
        print("WEBCLAW - COURT DATA REPORTER (READ ONLY)")
        print("Scanning for potential issues - NO CHANGES WILL BE MADE")
        print("="*70)
        
        for state_dir in JURISDICTIONS.iterdir():
            if state_dir.is_dir() and state_dir.name not in ['federal', 'territorial', 'tribal']:
                self.scan_state(state_dir)
        
        self.print_report()
    
    def scan_state(self, state_dir):
        for county_dir in state_dir.iterdir():
            if county_dir.is_dir():
                self.scan_county(state_dir.name, county_dir.name)
    
    def scan_county(self, state, county):
        court_file = JURISDICTIONS / state / county / "district_court.md"
        if not court_file.exists():
            return
        
        content = court_file.read_text(encoding='utf-8', errors='ignore')
        self.checked += 1
        
        # Check for phone number
        phone_match = re.search(r'- \*\*Phone\*\*: (.+)', content)
        if phone_match:
            phone = phone_match.group(1).strip()
            digits = re.sub(r'\D', '', phone)
            
            # Flag potential issues (but don't fix)
            issues = []
            if len(digits) != 10:
                issues.append("wrong length")
            if '000' in digits:
                issues.append("contains 000")
            if 'None' in phone:
                issues.append("contains None")
            if phone.startswith('\\'):
                issues.append("escaped character")
            if len(phone) < 10:
                issues.append("too short")
            
            if issues:
                self.issues.append({
                    'state': state,
                    'county': county,
                    'phone': phone,
                    'issues': issues,
                    'file': str(court_file)
                })
    
    def print_report(self):
        print(f"\n{'='*70}")
        print(f"SCAN COMPLETE")
        print(f"Checked: {self.checked} courts")
        print(f"Potential issues found: {len(self.issues)}")
        print(f"{'='*70}")
        
        if self.issues:
            print("\n📋 COURTS WITH POTENTIAL ISSUES:")
            print("-"*70)
            for item in self.issues[:50]:  # Show first 50
                print(f"\n📍 {item['state']}/{item['county']}")
                print(f"   Phone: {item['phone']}")
                print(f"   Issues: {', '.join(item['issues'])}")
                print(f"   File: {item['file']}")
            
            if len(self.issues) > 50:
                print(f"\n... and {len(self.issues) - 50} more")
            
            # Save full report to file
            report_path = Path.home() / ".claw_memory" / "court_issues_report.txt"
            report_path.parent.mkdir(exist_ok=True)
            
            with open(report_path, 'w') as f:
                f.write("COURT DATA ISSUES REPORT\n")
                f.write("="*60 + "\n\n")
                for item in self.issues:
                    f.write(f"State: {item['state']}\n")
                    f.write(f"County: {item['county']}\n")
                    f.write(f"Phone: {item['phone']}\n")
                    f.write(f"Issues: {', '.join(item['issues'])}\n")
                    f.write(f"File: {item['file']}\n")
                    f.write("-"*40 + "\n\n")
            
            print(f"\n📄 Full report saved to: {report_path}")
        else:
            print("\n✅ No issues found!")

if __name__ == "__main__":
    reporter = CourtReporter()
    reporter.scan_all()
