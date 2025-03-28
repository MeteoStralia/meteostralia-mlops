#!/bin/bash
timestamp=$DOCKER_CURRENT_TAG
timestamp="28032025"
docker login -u=meteostralia -p=meteostralia\*2410 # à sécuriser

echo "Pulling images with tag "$timestamp
echo "":

docker pull meteostralia/meteorepo:reset_data$timestamp
docker pull meteostralia/meteorepo:ingest_data$timestamp
docker pull meteostralia/meteorepo:complete_nas$timestamp
docker pull meteostralia/meteorepo:encode_data$timestamp
docker pull meteostralia/meteorepo:features$timestamp
docker pull meteostralia/meteorepo:scale_data$timestamp
docker pull meteostralia/meteorepo:split_data$timestamp
docker pull meteostralia/meteorepo:training$timestamp
docker pull meteostralia/meteorepo:evaluate$timestamp
docker pull meteostralia/meteorepo:inference$timestamp
docker pull meteostralia/meteorepo:meteostralia-mlops-api$timestamp
docker pull meteostralia/meteorepo:meteostralia-mlops-streamlit$timestamp

docker pull redis:7.2-bookworm
docker pull apache/airflow:2.10.5
docker pull postgres:13