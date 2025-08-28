#!/bin/bash

set -e

echo "[Certbot] Starting certificate process..."

# passed in entrypoint
# source /etc/certbot/certbot-env.sh

# Check required environment variables
: "${CERTBOT_EMAIL?Need to set CERTBOT_EMAIL}"
: "${CERTBOT_DOMAINS?Need to set CERTBOT_DOMAINS}"

# Convert comma-separated domain list into array
IFS=',' read -ra DOMAIN_ARRAY <<< "$CERTBOT_DOMAINS"

# Build the array of -d flags for certbot
DOMAIN_ARGS=()
for domain in "${DOMAIN_ARRAY[@]}"; do
  DOMAIN_ARGS+=("-d" "$domain")
done

# Obtain or renew certificates using the webroot plugin
certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  --email "$CERTBOT_EMAIL" \
  --agree-tos --no-eff-email \
  "${DOMAIN_ARGS[@]}"

echo "[Certbot] Certificate process completed successfully."