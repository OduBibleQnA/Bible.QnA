#!/bin/bash
set -e

# === Load environment variables from .env.prod ===
if [ -f .env.prod ]; then
  export $(grep -v '^#' .env.prod | xargs)
else
  echo ".env.prod not found!"
  exit 1
fi

# === Determine system user for file ownership ===
SYS_USER=${SUDO_USER:-$(logname 2>/dev/null || whoami)}

# === System update ===
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# === Set up backup directory ===
echo "📁 Creating /srv/backups..."
sudo mkdir -p /srv/backups
sudo chown "$SYS_USER:$SYS_USER" /srv/backups

# === Install Docker and Docker Compose ===
echo "🐳 Installing Docker & Docker Compose..."
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker "$SYS_USER"

echo "✅ Docker installed. Please reboot or run 'newgrp docker' before continuing with start-pt2.sh."

