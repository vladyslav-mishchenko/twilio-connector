FROM nginx

WORKDIR /etc/nginx

# config
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# entrypoint
COPY entrypoints/prod/nginx-entrypoint.sh /usr/local/bin/entrypoints/nginx-entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoints/nginx-entrypoint.sh

# env
COPY env/prod/nginx-env.sh /etc/nginx/nginx-env.sh
RUN chmod +x /etc/nginx/nginx-env.sh

ENTRYPOINT ["/usr/local/bin/entrypoints/nginx-entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]