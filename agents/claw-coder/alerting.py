#!/usr/bin/env python3
"""
Alerting System for PhoenixPME
- Slack webhooks
- Email alerts
- Discord notifications
"""

import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json
from pathlib import Path

class AlertSystem:
    def __init__(self, config_file='alert_config.json'):
        self.config = self.load_config(config_file)
    
    def load_config(self, config_file):
        default_config = {
            'slack_webhook': None,
            'discord_webhook': None,
            'email': {
                'enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'from_email': None,
                'to_email': None,
                'password': None
            }
        }
        
        if Path(config_file).exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return default_config
    
    def send_slack(self, message, severity="INFO"):
        """Send alert to Slack"""
        if not self.config.get('slack_webhook'):
            return
        
        color = {"INFO": "#36a64f", "WARNING": "#ffcc00", "CRITICAL": "#ff0000"}
        payload = {
            "attachments": [{
                "color": color.get(severity, "#36a64f"),
                "title": f"PhoenixPME Alert - {severity}",
                "text": message,
                "footer": "Claw-Coder Monitor",
                "ts": int(datetime.now().timestamp())
            }]
        }
        
        try:
            requests.post(self.config['slack_webhook'], json=payload)
            print("✅ Slack alert sent")
        except Exception as e:
            print(f"❌ Slack error: {e}")
    
    def send_email(self, subject, body):
        """Send email alert"""
        if not self.config.get('email', {}).get('enabled'):
            return
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.config['email']['from_email']
        msg['To'] = self.config['email']['to_email']
        
        try:
            server = smtplib.SMTP(self.config['email']['smtp_server'], 
                                  self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['from_email'], 
                        self.config['email']['password'])
            server.send_message(msg)
            server.quit()
            print("✅ Email alert sent")
        except Exception as e:
            print(f"❌ Email error: {e}")
    
    def alert_violation(self, violation):
        """Send violation alert to all channels"""
        message = f"""
🚨 PHOENIXPME VIOLATION
Time: {datetime.now()}
Violation: {violation}
Action: Immediate attention required
"""
        self.send_slack(message, "CRITICAL")
        self.send_email("PhoenixPME Violation Alert", message)

if __name__ == "__main__":
    alerts = AlertSystem()
    
    # Example usage
    alerts.alert_violation("Test violation - collateral ratio below 10%")
