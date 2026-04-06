#!/bin/bash
# Remove sysclaw scheduled tasks

crontab -l 2>/dev/null | grep -v "sysclaw" | crontab -
echo "✅ SysClaw scheduled tasks removed"
