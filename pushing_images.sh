#!/bin/bash
# A DECLENCER A CHAQUE GIT PUSH ou FETCH
timestamp="28032025" # TODO à mettre en dynamique
docker login -u=meteostralia -p=meteostralia\*2410  # à sécuriser

echo "Pushing images with tag "$timestamp
echo "":

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
