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

cd ./api

echo "Téléchargement de la base de données depuis S3..."
echo ""
python manage_db.py

cd ..
echo ""
echo "constuction du docker-compose"
echo ""
docker-compose up --build --force-recreate

echo ""
echo "fermeture du docker-compose"
echo ""
docker-compose down
