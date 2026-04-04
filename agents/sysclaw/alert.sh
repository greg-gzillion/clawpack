#!/bin/bash
# Send alerts for critical issues

ALERT_TYPE="$1"
MESSAGE="$2"
ALERT_LOG="$HOME/.claw_memory/alerts.log"

# Log alert
echo "$(date): [$ALERT_TYPE] $MESSAGE" >> "$ALERT_LOG"

# Terminal alert (always)
echo "🔔 ALERT: $MESSAGE"

# Desktop notification (if available)
if command -v notify-send &> /dev/null; then
    notify-send "SysClaw Alert" "$MESSAGE"
fi

# Email alert (configure if needed)
# echo "$MESSAGE" | mail -s "SysClaw: $ALERT_TYPE" your-email@example.com

# Slack webhook (configure if needed)
# WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
# curl -X POST -H 'Content-type: application/json' \
#   --data "{\"text\":\"[$ALERT_TYPE] $MESSAGE\"}" \
#   "$WEBHOOK_URL"
