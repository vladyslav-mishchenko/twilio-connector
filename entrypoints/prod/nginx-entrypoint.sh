#!/bin/bash

set -e 

source /etc/nginx/nginx-env.sh

envsubst '${NGINX_HOSTNAME}' '${DOMAIN}' \
    < /etc/nginx/templates/default.conf.template \
    > /etc/nginx/conf.d/default.conf

exec "$@"
