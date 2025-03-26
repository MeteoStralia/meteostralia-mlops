#!/usr/bin/env bash

# PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# echo $PROJECT_DIR
# set -euo pipefail

# export COMPOSE_FILE="${PROJECT_DIR}/docker-compose-airflow.yml"
# if [ $# -gt 0 ]; then
#     exec docker-compose run --rm airflow-worker "${@}"
# else
#     exec docker-compose run --rm airflow-worker
# fi

chmod -R 777 orchestration_service/logs/
chmod -R 777 orchestration_service/dags/
chmod -R 777 orchestration_service/plugins/

echo -e "AIRFLOW_UID=$(id -u)" > .env

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/orchestration_service"
echo -e "AIRFLOW_PROJ_DIR="$PROJECT_DIR >> .env
PROJECTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "AIRFLOW_VAR_PROJECTPATH="$PROJECTPATH >> .env
echo -e "AIRFLOW_VAR_MLFLOW_TRACKING_USERNAME=fde7dcd7368ad7d679356e489a202cb0dbbd4464" >> .env
echo -e "MLFLOW_TRACKING_URI=https://dagshub.com/bruno.vermont/meteostralia-mlops.mlflow" >> .env


export AIRFLOW_VAR_PROJECTPATH=$PROJECTPATH
# export COMPOSE_FILE="${PROJECT_DIR}/docker-compose-airflow_new.yaml"
# if [ $# -gt 0 ]; then
#     exec docker-compose run --rm airflow-worker "${@}"
# else
#     exec docker-compose run --rm airflow-worker
# fi