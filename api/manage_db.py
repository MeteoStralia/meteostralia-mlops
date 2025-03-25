import boto3
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()
db_url = os.getenv('DB_PATH')
aws_access_key = os.getenv('ACCESS_KEY_AWS')
aws_access_secret = os.getenv('SECRET_KEY_AWS')


# Configuration de l'accès à S3
S3_BUCKET_NAME = 'meteostralia-mlops-database'
DB_FILE_NAME = 'meteostralia.db'


# Créez une session boto3 et une ressource S3
s3 = boto3.client('s3',
                  aws_access_key_id = aws_access_key,
                  aws_secret_access_key = aws_access_secret,
               )

def download_db_from_s3():
    try:
        # Télécharge le fichier depuis S3 vers le chemin local
        s3.download_file(S3_BUCKET_NAME, DB_FILE_NAME, db_url)
        print(f"Base de données {DB_FILE_NAME} téléchargée avec succès depuis S3.")
    except Exception as e:
        print(f"Erreur lors du téléchargement de la base de données : {e}")

def upload_db_to_s3():
    try:
        # Charge la base de données locale vers S3
        s3.upload_file(db_url, S3_BUCKET_NAME, DB_FILE_NAME)
        print(f"Base de données {DB_FILE_NAME} uploadée avec succès sur S3.")
    except Exception as e:
        print(f"Erreur lors du téléchargement de la base de données : {e}")

if __name__ == '__main__':
    download_db_from_s3()
    # upload_db_to_s3()
