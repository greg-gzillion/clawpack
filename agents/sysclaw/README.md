# SysClaw - System Maintenance Agent

## Commands
- python3 sysclaw.py - Full maintenance
- python3 sysclaw.py status - Check status  
- python3 sysclaw.py update-tx - Update TX project
- python3 sysclaw.py clean - Clean caches
- python3 sysclaw.py update-system - Update packages

## Maintains
TX project, apt packages, Docker, caches, logs

## Safety
Auto-stash, backups, prompts before changes, sudo only when needed

## Logs
~/.claw_memory/sysclaw.log
