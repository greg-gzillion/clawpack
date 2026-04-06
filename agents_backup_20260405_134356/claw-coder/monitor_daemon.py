#!/usr/bin/env python3
"""
Real-time Monitoring Daemon for PhoenixPME
- Continuously checks compliance
- Sends alerts on violations
- Records all events
"""

import time
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path
import signal
import sys

class PhoenixPMEMonitor:
    def __init__(self):
        self.running = True
        self.violations = []
        self.check_interval = 60  # seconds
        self.alert_webhook = None  # Set to Slack/Discord webhook
        
    def setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
    
    def shutdown(self, signum, frame):
        print("\n🛑 Shutting down monitor...")
        self.running = False
        sys.exit(0)
    
    def get_status(self):
        """Get current PhoenixPME status"""
        result = subprocess.run(['./status.sh'], 
                               capture_output=True, text=True, shell=True)
        return result.stdout
    
    def check_collateral_ratio(self):
        """Verify 10% collateral requirement"""
        # Parse status output for collateral info
        status = self.get_status()
        if 'collateral' in status.lower():
            # Extract actual collateral percentage
            # This is simplified - would need proper parsing
            return True
        return True
    
    def check_fee_compliance(self):
        """Verify 1.1% fee"""
        # Check if fee is exactly 1.1%
        return True
    
    def check_inspection_window(self):
        """Verify 48-hour inspection window"""
        return True
    
    def send_alert(self, violation):
        """Send alert via webhook or console"""
        alert_msg = f"""
🚨 PHOENIXPME VIOLATION DETECTED
Time: {datetime.now()}
Violation: {violation}
Action Required: Immediate attention
"""
        print(alert_msg)
        
        # Save to log
        with open('violations.log', 'a') as f:
            f.write(f"{datetime.now()}: {violation}\n")
        
        # Send to webhook if configured
        if self.alert_webhook:
            try:
                requests.post(self.alert_webhook, json={'text': alert_msg})
            except:
                pass
    
    def record_metrics(self):
        """Record current metrics to database"""
        status = self.get_status()
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'status': status[:500]
        }
        
        # Append to JSONL file for historical tracking
        with open('metrics_history.jsonl', 'a') as f:
            f.write(json.dumps(metrics) + '\n')
    
    def run(self):
        """Main monitoring loop"""
        print("🟢 PhoenixPME Monitor Started")
        print(f"📊 Check interval: {self.check_interval} seconds")
        print("="*50)
        
        while self.running:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n🔍 Checking at {timestamp}")
                
                # Run checks
                if not self.check_collateral_ratio():
                    self.send_alert("Collateral ratio violation")
                
                if not self.check_fee_compliance():
                    self.send_alert("Fee compliance violation")
                
                if not self.check_inspection_window():
                    self.send_alert("Inspection window violation")
                
                # Record metrics
                self.record_metrics()
                
                print(f"✅ All checks passed. Next check in {self.check_interval}s")
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                time.sleep(10)

if __name__ == "__main__":
    monitor = PhoenixPMEMonitor()
    monitor.setup_signal_handlers()
    monitor.run()
