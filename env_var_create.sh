#!/bin/bash

echo -e "AIRFLOW_UID=$(id -u)" > .env
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/orchestration_service"
echo -e "AIRFLOW_PROJ_DIR="$PROJECT_DIR >> .env
PROJECTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "PROJECTPATH=${PROJECTPATH}" >> .env
echo -e "DAGSHUB_USER_TOKEN=dagshubtoken" >> .env
echo -e "MLFLOW_TRACKING_USERNAME=dagshubtoken" >> .env
echo -e "AIRFLOW_DAGSHUB_USER_TOKEN=dagshubtoken" >> .env
echo -e "AIRFLOW_MLFLOW_TRACKING_USERNAME=dagshubtoken" >> .env 
echo -e "AIRFLOW_MLFLOW_TRACKING_URI=trackingurl" >> .env
#echo -e "AIRFLOW_DOCKER_HOST=\"unix://var/run/docker.sock\"" >> .env #Pour linux
echo -e "AIRFLOW_DOCKER_HOST=tcp://host.docker.internal:2375" >> .env 

# TODO add docker username and password
