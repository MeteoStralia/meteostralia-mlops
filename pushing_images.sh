#!/bin/bash
# A DECLENCER A CHAQUE GIT PUSH ou FETCH
timestamp="28032025" # TODO à mettre en dynamique
docker login -u=meteostralia -p=meteostralia\*2410  # à sécuriser

echo "Pushing images with tag "$timestamp
echo "":

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

docker push meteostralia/meteorepo:reset_data$timestamp
docker push meteostralia/meteorepo:ingest_data$timestamp
docker push meteostralia/meteorepo:complete_nas$timestamp
docker push meteostralia/meteorepo:encode_data$timestamp
docker push meteostralia/meteorepo:features$timestamp
docker push meteostralia/meteorepo:scale_data$timestamp
docker push meteostralia/meteorepo:split_data$timestamp
docker push meteostralia/meteorepo:training$timestamp
docker push meteostralia/meteorepo:evaluate$timestamp
docker push meteostralia/meteorepo:inference$timestamp
docker push meteostralia/meteorepo:api$timestamp
docker push meteostralia/meteorepo:streamlit$timestamp

# TODO airflow images and monitoring images

# Add tag to environment var
echo -e "DOCKER_CURRENT_TAG="$timestamp >> .env 
