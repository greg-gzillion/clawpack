#!/bin/bash
# Auto-backup TX project and clawpack

BACKUP_DIR="$HOME/backups/clawpack-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "🦞 Creating backup at $BACKUP_DIR"

# Backup TX project
if [ -d "$HOME/dev/TX" ]; then
    echo "📦 Backing up TX project..."
    cp -r "$HOME/dev/TX" "$BACKUP_DIR/"
    # Remove heavy folders
    rm -rf "$BACKUP_DIR/TX/node_modules" 2>/dev/null
    rm -rf "$BACKUP_DIR/TX/target" 2>/dev/null
fi

# Backup clawpack
echo "📦 Backing up clawpack..."
cp -r "$HOME/dev/clawpack" "$BACKUP_DIR/"

# Backup memory database
echo "🧠 Backing up memory database..."
cp "$HOME/.claw_memory/shared_memory.db" "$BACKUP_DIR/"

# Create manifest
echo "📋 Creating manifest..."
cat > "$BACKUP_DIR/manifest.txt" << MANIFEST
Backup created: $(date)
Clawpack version: $(cat ~/dev/clawpack/VERSION 2>/dev/null || echo "unknown")
TX project: $(cd ~/dev/TX 2>/dev/null && git rev-parse HEAD 2>/dev/null || echo "N/A")
MANIFEST

# Compress
cd "$HOME/backups"
tar -czf "clawpack-backup-$(date +%Y%m%d-%H%M%S).tar.gz" "clawpack-$(date +%Y%m%d-%H%M%S)"
rm -rf "$BACKUP_DIR"

echo "✅ Backup complete: $HOME/backups/clawpack-backup-$(date +%Y%m%d-%H%M%S).tar.gz"

# Keep only last 10 backups
ls -t clawpack-backup-*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f 2>/dev/null
echo "🧹 Kept last 10 backups"
