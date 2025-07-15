#!/bin/bash
set -e

# === Load environment variables from .env.prod ===
if [ -f .env.prod ]; then
  export $(grep -v '^#' .env.prod | xargs)
else
  echo ".env.prod not found!"
  exit 1
fi

# === Determine system user ===
SYS_USER=${SUDO_USER:-$(logname 2>/dev/null || whoami)}

# === Install UFW and enable firewall ===
echo "🛡️  Configuring UFW..."
sudo apt update
sudo apt install -y ufw
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
echo "✅ UFW enabled with ports 22, 80, 443 allowed"

# === Install and configure logrotate ===
echo "🌀 Installing logrotate..."
sudo apt install -y logrotate

# === Logrotate config for restore-log.txt ===
RESTORE_LOGROTATE_CONF="/etc/logrotate.d/restore-log"
sudo tee "$RESTORE_LOGROTATE_CONF" > /dev/null <<EOF
/srv/backups/restore-log.txt {
    size 1M
    rotate 5
    compress
    missingok
    notifempty
    copytruncate
}
EOF
sudo logrotate -f "$RESTORE_LOGROTATE_CONF"
echo "✅ Log rotation configured for restore-log.txt"

# === Logrotate config for backup-log.txt ===
BACKUP_LOGROTATE_CONF="/etc/logrotate.d/backup-log"
sudo tee "$BACKUP_LOGROTATE_CONF" > /dev/null <<EOF
/srv/backups/backup-log.txt {
    size 1M
    rotate 5
    compress
    missingok
    notifempty
    copytruncate
}
EOF
sudo logrotate -f "$BACKUP_LOGROTATE_CONF"
echo "✅ Log rotation configured for backup-log.txt"

# === Add daily logrotate cron job if missing ===
if ! crontab -l 2>/dev/null | grep -q "logrotate"; then
  (crontab -l 2>/dev/null; echo "0 0 * * * /usr/sbin/logrotate /etc/logrotate.conf") | crontab -
  echo "🕒 Daily logrotate cron job added"
fi

# === Set up hourly PostgreSQL backups ===
echo "💾 Setting up hourly PostgreSQL backup..."
(crontab -l 2>/dev/null; echo "0 * * * * docker exec $DB_CONTAINER pg_dump -U $DB_USER -F c -d $DB_NAME > /srv/backups/\$(date +\%Y\%m\%d_\%H\%M)_bkp.dump 2>> /srv/backups/backup-log.txt && echo \"\$(date) - SUCCESS\" >> /srv/backups/backup-log.txt || echo \"\$(date) - FAIL\" >> /srv/backups/backup-log.txt") | crontab -

# === Set correct permissions for Traefik's acme.json ===
echo "🔐 Setting permissions for acme.json..."
mkdir -p traefik
touch traefik/acme.json
chmod 600 traefik/acme.json
echo "✅ Permissions for traefik/acme.json set"

# === Start Docker Compose stack ===
echo "🚀 Starting Docker services..."
docker-compose -f "$COMPOSE_PATH" run upload-static
docker-compose -f "$COMPOSE_PATH" up -d
