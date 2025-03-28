#!/bin/bash

echo -e "AIRFLOW_UID=$(id -u)" > .env
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/orchestration_service"
echo -e "AIRFLOW_PROJ_DIR="$PROJECT_DIR >> .env
PROJECTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "PROJECTPATH=${PROJECTPATH}" >> .env
echo -e "DAGSHUB_USER_TOKEN=fde7dcd7368ad7d679356e489a202cb0dbbd4464" >> .env
echo -e "MLFLOW_TRACKING_USERNAME=fde7dcd7368ad7d679356e489a202cb0dbbd4464" >> .env
echo -e "AIRFLOW_DAGSHUB_USER_TOKEN=fde7dcd7368ad7d679356e489a202cb0dbbd4464" >> .env
echo -e "AIRFLOW_MLFLOW_TRACKING_USERNAME=fde7dcd7368ad7d679356e489a202cb0dbbd4464" >> .env 
echo -e "AIRFLOW_MLFLOW_TRACKING_URI=https://dagshub.com/bruno.vermont/meteostralia-mlops.mlflow" >> .env
#echo -e "AIRFLOW_DOCKER_HOST=\"unix://var/run/docker.sock\"" >> .env #Pour linux
echo -e "AIRFLOW_DOCKER_HOST=tcp://host.docker.internal:2375" >> .env 

