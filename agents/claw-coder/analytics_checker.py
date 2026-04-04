#!/usr/bin/env python3
"""
Analytics Checker Module for Claw-Coder
Checks Google Analytics and Vercel stats for PhoenixPME
"""

import webbrowser
from datetime import datetime

class AnalyticsChecker:
    def __init__(self):
        self.project_name = "PhoenixPME"
        self.github_repo = "https://github.com/greg-gzillion/TX"
        self.vercel_project = "https://vercel.com/greg-gzillion/phoenix-frontend"
        self.ga_property = "https://analytics.google.com"
        
    def check_manually(self):
        """Open all analytics dashboards in browser"""
        print("\n📊 Opening Analytics Dashboards...")
        print("=" * 40)
        
        dashboards = [
            ("Vercel Analytics", self.vercel_project),
            ("Google Analytics", self.ga_property),
            ("GitHub Insights", f"{self.github_repo}/graphs/traffic")
        ]
        
        for name, url in dashboards:
            print(f"Opening {name}: {url}")
            webbrowser.open(url)
        
        print("\n✅ Dashboards opened in your browser")
        print("\n📋 Look for these metrics:")
        print("   • Referrers to your GitHub repo")
        print("   • Page views on Vercel frontend")
        print("   • Unique visitors vs returning")
        print("   • Traffic sources (Direct, Social, Referral)")
    
    def analyze_traffic_spike(self):
        """Analyze the April 1 traffic spike"""
        print("\n🔍 Analyzing April 1 Traffic Spike")
        print("=" * 40)
        
        print("""
Possible sources of the 39 unique cloners on 4/1/2026:

1. GitHub Search
   - People searching for 'claw' (due to Claude Code leak)
   - Your 'claw-coder' repo appeared in results
   - Visitors clicked through to your TX repo

2. Social Media
   - Did you post anything on Twitter/X on March 31/April 1?
   - Any Discord or Telegram mentions?

3. Direct Referral
   - Someone shared your link
   - Check GitHub Insights > Referring sites

4. Vercel Deployment
   - Your frontend at phoenix-frontend-seven.vercel.app
   - Any traffic spikes there?

To confirm the source:
1. Go to GitHub.com > TX repo > Insights > Traffic
2. Look at "Referring sites" section
3. See what sites sent visitors on April 1
""")
    
    def generate_report(self):
        """Generate analytics summary"""
        print("\n📈 Analytics Summary Report")
        print("=" * 40)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Project: {self.project_name}")
        print("")
        print("Known Metrics (from GitHub):")
        print("  • Total clones (14 days): 158")
        print("  • Unique cloners: 46")
        print("  • Peak day: April 1 (39 cloners)")
        print("  • Total views: 137")
        print("  • Unique visitors: 2")
        print("")
        print("Next Steps:")
        print("  1. Check Vercel for frontend traffic")
        print("  2. Check Google Analytics for referrers")
        print("  3. Add UTM tags to your links")
        print("  4. Set up custom dashboards")

def main():
    checker = AnalyticsChecker()
    
    print("\n🦞 Claw-Coder Analytics Module")
    print("=" * 40)
    print("\nOptions:")
    print("  1. Open all analytics dashboards")
    print("  2. Analyze April 1 traffic spike")
    print("  3. Generate analytics report")
    
    choice = input("\nSelect (1-3): ").strip()
    
    if choice == "1":
        checker.check_manually()
    elif choice == "2":
        checker.analyze_traffic_spike()
    elif choice == "3":
        checker.generate_report()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
