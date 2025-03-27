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
echo -e "MLFLOW_TRACKING_USERNAME=fde7dcd7368ad7d679356e489a202cb0dbbd4464" >> .env
echo -e "MLFLOW_TRACKING_URI=https://dagshub.com/bruno.vermont/meteostralia-mlops.mlflow" >> .env

echo "stopping all containers"
docker stop $(docker ps -a -q)

echo "Téléchargement de la base de données depuis S3..."
echo ""
python ./api/manage_db.py

echo "lancement du docker-compose"
echo ""
docker compose -f docker-compose_airflow.yaml up #-d
