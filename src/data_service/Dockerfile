FROM ubuntu:latest
WORKDIR /app/
COPY --from=docker/compose-bin:v2.20.2 /docker-compose /usr/bin/compose
RUN ln -s /usr/bin/docker-compose /compose/docker-compose
#RUN compose version