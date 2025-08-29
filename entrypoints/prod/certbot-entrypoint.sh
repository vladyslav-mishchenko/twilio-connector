#!/bin/bash

set -e

echo "CERTBOT ENTRYPOINT"
# source /etc/certbot/certbot-env.sh

exec "$@"
