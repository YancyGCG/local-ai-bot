#!/bin/bash
# Backup script for Local AI Bot working version
# Created: $(date)

BACKUP_DIR="backups/working-react-frontend-$(date +%Y%m%d_%H%M%S)"
echo "Creating backup in $BACKUP_DIR..."

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup critical files
cp -r frontend "$BACKUP_DIR/"
cp -r src "$BACKUP_DIR/"
cp -r templates "$BACKUP_DIR/"
cp -r data "$BACKUP_DIR/"

# Backup configuration files
cp package.json "$BACKUP_DIR/" 2>/dev/null || true
cp requirements.txt "$BACKUP_DIR/" 2>/dev/null || true
cp README.md "$BACKUP_DIR/" 2>/dev/null || true

echo "Backup completed successfully in $BACKUP_DIR"
echo "To restore: cp -r $BACKUP_DIR/* ./"