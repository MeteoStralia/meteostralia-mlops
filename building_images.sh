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

echo "Building traking service images"
echo "":
docker compose -f src/tracking_service/docker-compose.yml build

echo "Building api streamlit" 
echo "":
docker compose -f docker-compose.yml build # A mettre dans dossier api

echo "Building monitoring images"
echo "":
# docker compose -f dockprom/docker-compose.yml build # TODO à ajouter

# tagging images 
timestamp="28032025" # TODO à mettre en dynamique
docker login -u=meteostralia -p=meteostralia\*2410  # à sécuriser

docker tag  reset_data:latest meteostralia/meteorepo:reset_data$timestamp 
docker tag  ingest_data:latest meteostralia/meteorepo:ingest_data$timestamp 
docker tag  complete_nas:latest meteostralia/meteorepo:complete_nas$timestamp 
docker tag  encode_data:latest meteostralia/meteorepo:encode_data$timestamp 
docker tag  features:latest meteostralia/meteorepo:features$timestamp 
docker tag  scale_data:latest meteostralia/meteorepo:scale_data$timestamp 
docker tag  split_data:latest meteostralia/meteorepo:split_data$timestamp 
docker tag  training:latest meteostralia/meteorepo:training$timestamp 
docker tag  evaluate:latest meteostralia/meteorepo:evaluate$timestamp 
docker tag  inference:latest meteostralia/meteorepo:inference$timestamp 
docker tag  api:latest meteostralia/meteorepo:api$timestamp 
docker tag  streamlit:latest meteostralia/meteorepo:streamlit$timestamp 

