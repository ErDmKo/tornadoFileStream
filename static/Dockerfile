FROM nginx
RUN mkdir /app/ /app/html/ /app/upload/
VOLUME ["./html:/app/html/", "./upload:/app/upload/"]
ADD nginx.conf /etc/nginx/nginx.conf
