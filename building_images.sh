#!/bin/bash
# A DECLENCER A CHAQUE GIT PUSH ou FETCH
echo "stopping all containers"
#docker stop $(docker ps -a -q)

echo "Building data service images"
echo "":
docker compose -f src/data_service/docker-compose.yml build

echo "Building modeling service images"
echo "":
docker compose -f src/modeling_service/docker-compose.yml build

echo "Building inference service images"
echo "":
docker compose -f src/inference_service/docker-compose.yml build

echo "Building api streamlit" 
echo "":
docker compose -f docker-compose.yml build # A mettre dans dossier api

echo "Building monitoring images"
echo "":
# docker compose -f dockprom/docker-compose.yml build # TODO à ajouter
