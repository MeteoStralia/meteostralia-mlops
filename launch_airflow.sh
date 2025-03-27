#!/bin/bash
echo "
##   ## ###### ######  ###### ####### ###### ###### ######      #     ##     ##      #
####### ##       ##    ##     ##   ## ##       ##   ##   ##    ###    ##     ##     ###
## # ## ####     ##    ####   ##   ## ######   ##   ######    ## ##   ##     ##    ## ##
##   ## ##       ##    ##     ##   ##     ##   ##   ## ##     #####   ##     ##    #####
##   ## ##       ##    ##     ##   ##     ##   ##   ##  ##   ##   ##  ##     ##   ##   ##
##   ## ######   ##    ###### ####### ######   ##   ##   ## ##     ## ###### ##  ##     ##
"

echo "Powered by :

   ###                ###              ###                 ###
  #   # ######       #   # #####      #   # #######       #   # #####
 #     #      #     #     #     #    #     #       #     #     #     #
#              #   #             #   #              #   #             #
#    Bruno     #   #   Mathieu   #   #  Viridiana   #   #   Yassine   #
 #            #     #           #     #            #     #           #
  ############       ###########       ############       ###########
"
echo ""
echo ""

# chmod -R 777 orchestration_service/logs/
# chmod -R 777 orchestration_service/dags/
# chmod -R 777 orchestration_service/plugins/

echo -e "AIRFLOW_UID=$(id -u)" > .env
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/orchestration_service"
echo -e "AIRFLOW_PROJ_DIR="$PROJECT_DIR >> .env
PROJECTPATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "PROJECTPATH=${PROJECTPATH}" >> .env
echo -e "MLFLOW_TRACKING_USERNAME=7413ebc3fe3b73d01f5661be0887338842044001" >> .env
echo -e "MLFLOW_TRACKING_URI=https://dagshub.com/meteostraliamlops/meteostralia-mlops.mlflow" >> .env
#echo -e "AIRFLOW_DOCKER_HOST=unix://var/run/docker.sock" >> .env #Pour linux
echo -e "AIRFLOW_DOCKER_HOST=tcp://host.docker.internal:2375" >> .env 
echo "stopping all containers"
docker stop $(docker ps -a -q)

echo "Téléchargement de la base de données depuis S3..."
echo ""
python ./api/manage_db.py

echo "lancement du docker-compose"
echo ""
docker compose -f docker-compose_airflow.yaml up #-d
