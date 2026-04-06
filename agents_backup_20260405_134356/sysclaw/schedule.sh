#!/bin/bash
# Setup scheduled tasks for sysclaw

echo "🦞 Setting up SysClaw scheduled tasks"

# Create cron job for daily health check
CRON_CMD="cd $HOME/dev/sysclaw && python3 sysclaw_intelligent.py analyze >> $HOME/.claw_memory/sysclaw_cron.log 2>&1"

(crontab -l 2>/dev/null | grep -v "sysclaw") | crontab -
(crontab -l 2>/dev/null; echo "0 9 * * * $CRON_CMD") | crontab -

echo "✅ Daily health check scheduled at 9:00 AM"

echo ""
echo "Current crontab:"
crontab -l | grep sysclaw
