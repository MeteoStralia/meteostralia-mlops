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


echo "stopping all containers"
#docker stop $(docker ps -a -q)

echo "Téléchargement de la base de données depuis S3..."
echo ""
python ./api/manage_db.py

echo "lancement du docker-compose"
echo ""
docker compose -f docker-compose_airflow.yaml up #-d
