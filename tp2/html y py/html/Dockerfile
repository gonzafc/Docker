FROM nginx:latest
EXPOSE 80
LABEL maintainer="Gonzalo Romero"
LABEL version="1.0"
LABEL description="Contenedor nginx para un tp"
ENV app="tp1"
RUN mkdir /mivolumen
VOLUME /mivolumen
COPY ./index.html /usr/share/nginx/html/index.html
