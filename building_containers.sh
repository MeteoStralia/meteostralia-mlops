#!/bin/bash
# A DECLENCER A CHAQUE GIT PUSH ou FETCH

echo "stopping all containers"
# docker stop $(docker ps -a -q)

echo "Building data service containers"
echo "":
docker compose -f src/data_service/docker-compose.yml build

echo "Building modeling service containers"
echo "":
docker compose -f src/modeling_service/docker-compose.yml build

echo "Building inference service containers"
echo "":
docker compose -f src/inference_service/docker-compose.yml build

echo "Building api streamlit and airflow containers"
echo "":
docker compose -f docker-compose_airflow.yaml build

#docker compose -f docker-compose_airflow.yaml up airflow-init

echo "stopping all containers"
docker stop $(docker ps -a -q)
