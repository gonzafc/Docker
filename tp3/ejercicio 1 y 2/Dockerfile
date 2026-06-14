FROM nginx:alpine
LABEL autor="Gonzalo Romero"
LABEL descripcion="Imagen para el TP3"
ENV AMBIENTE=laboratorio
COPY ./index.html /usr/share/nginx/html/index.html
VOLUME /usr/share/nginx/html
EXPOSE 80
RUN addgroup -S myuser && adduser -S myuser -G myuser
USER myuser