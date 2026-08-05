FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY .htpasswd /tmp/.htpasswd
RUN cp /tmp/.htpasswd /etc/nginx/.htpasswd && chmod 644 /etc/nginx/.htpasswd
COPY . /usr/share/nginx/html
RUN chmod -R +r /usr/share/nginx/html/data
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD wget -q -O - http://127.0.0.1/ >/dev/null || exit 1
