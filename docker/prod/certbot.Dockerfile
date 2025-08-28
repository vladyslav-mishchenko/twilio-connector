FROM python:3.10

# Install certbot and certbot-nginx plugin
RUN pip install --no-cache-dir certbot certbot-nginx

# Optional: install any dependencies you want (e.g., curl)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# entrypoint
COPY entrypoints/prod/certbot-entrypoint.sh /usr/local/bin/entrypoints/certbot-entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoints/certbot-entrypoint.sh

# env
COPY env/prod/certbot-env.sh /etc/certbot/certbot-env.sh
RUN chmod +x /etc/certbot/certbot-env.sh

# script for obtaining certificate
COPY certbot/obtain-certs.sh /usr/local/bin/obtain-certs.sh
RUN chmod +x /usr/local/bin/obtain-certs.sh

ENTRYPOINT ["/usr/local/bin/entrypoints/certbot-entrypoint.sh"]

CMD ["python"]
