#!/bin/bash

echo -e "AIRFLOW_UID=$(id -u)" > .env
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/orchestration_service"
echo -e "AIRFLOW_PROJ_DIR="$PROJECT_DIR >> .env
PROJECTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "PROJECTPATH=${PROJECTPATH}" >> .env
echo -e "AIRFLOW_DAGSHUB_USER_TOKEN=7413ebc3fe3b73d01f5661be0887338842044001" >> .env
echo -e "AIRFLOW_MLFLOW_TRACKING_USERNAME=meteostraliamlops" >> .env 
echo -e "AIRFLOW_MLFLOW_TRACKING_URI=https://dagshub.com/meteostraliamlops/meteostralia-mlops.mlflow" >> .env
#echo -e "AIRFLOW_DOCKER_HOST=\"unix://var/run/docker.sock\"" >> .env #Pour linux
echo -e "AIRFLOW_DOCKER_HOST=tcp://host.docker.internal:2375" >> .env 

