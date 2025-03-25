#!/bin/bash

cd ./api

# Télécharger la base de données depuis S3
echo "Téléchargement de la base de données depuis S3..."
python manage_db.py

cd ..
echo "constuction du docker-compose"
docker-compose up --build --force-recreate

echo "fermeture du docker-compose"
docker-compose down
