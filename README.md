# meteostralia-mlops

## Virtual environment installation 
Run at root 

```
python3 -m venv env     
.\env\Scripts\activate
pip install -r requirements.txt
```

## Environment variable to setup
TODO faire un script bash ou un ficher de config

```
PROJECTPATH = <project path> -> local project path 
```

## Orchestration with Airflow

On windows, you have to enable on docker desktop the following option "Expose Daemon in tcp://localhost:2375 without TLS" cf(https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly#configure-docker-for-windows)

At root
```
echo -e "AIRFLOW_UID=$(id -u)" > .env
echo -e "AIRFLOW_PROJ_DIR=./orchestration_service"

```

Init db

To launch the airflow services, run at root
```
docker compose -f docker-compose-airflow.yml up -d
```

Check if all containers are healthy
```
docker container ls
```

then go to http://localhost:8080/



## Connexion to Dagshub

First connect Meteostralia github repo to dagshub (My repositories +New -> connect a repository -> Other -> set the adress to https://github.com/MeteoStralia/meteostralia-mlops -> identification needed with account name and password or token)

## Setup MLFLOW and run parameters
run at root
```
docker compose -f .\src\tracking_service\docker-compose.yml build
```
Then
```
docker compose -f .\src\tracking_service\docker-compose.yml up
```
## Data service (src/data_service)

TODO

## Modeling service (src/modeling_service)

TODO

## Inference service (src/inference_service)

TODO

## Configuration data_service et modeling_service
Run at root (if first time)
```
docker compose -f .\src\data_service\docker-compose.yml build 
docker compose -f .\src\modeling_service\docker-compose.yml build 
docker compose -f .\src\inference_service\docker-compose.yml build 
```
Then run (or directly run if build is already done)

```
docker compose -f .\src\data_service\docker-compose.yml up 
docker compose -f .\src\modeling_service\docker-compose.yml up
docker compose -f .\src\inference_service\docker-compose.yml up
```

## Configuration suivi DVC

### Initialisation DVC
Not needed if .dvc folder is already pulled
```
dvc init
```

Create local remote storage folder (not needed if you use dagshub remote storage)
```
dvc remote add -d remote_storage ../remote_storage
```

### Configurer le stockage distant sur Dagshub
installing S3 bucket
```
pip install "dvc[s3]"
dvc remote add origin s3://dvc
dvc remote modify origin endpointurl <REPODAGSHUBURL>.s3
```
then verify if the .dvc/config is modified. It should look like

```
['remote "origin"']
    url = s3://dvc
    endpointurl = <REPODAGSHUBURL>
```

In the repo Dasghub, in Remote/Data/DVC tab, copy and run the two lines under Setup credentials

```
dvc remote modify origin --local access_key_id your_token
dvc remote modify origin --local secret_access_key your_token
```

This shoudld appear in .dvc/config.local file.
Then run 

```
dvc remote default origin
```

to ensure that the remote storage is origin (dagshub)

### Adding tracking folders

```
dvc add ./data/current_data
dvc add ./data/processed_data
dvc add ./models 
dvc add ./metrics
```

### Testing on current data and models

removing local files
```
rm -rf ./data/current_data/ ./data/processed_data/ ./models ./metrics .dvc/cache
```

fetching remote files
```
dvc fetch 
```

downloading remote files
```
dvc checkout
```

data, models and metrics should appear on your local drive

### pushing a new run on DVC
First run a data or model pipeline
For example
```
docker compose -f .\src\modeling_service\docker-compose.yml build 
```
OR
```
DVC repro
```

Commit changes in dvc metadata 
```
dvc commit
```

Commit changes in metadata to git
```
git add dvc.lock
git commit -m "testing a dvc versioning"
git tag -a new_tag -m "testing a dvc versioning"
git push origin --tags
```

Push changes to DVC and changes in metadata to git
```
dvc push
git push
```

### Going back to a previous version
Verifying log 
```
git log --since="2025-03-17" --all
```

Going back to a previous version with tag HASH_CODE 
```
git checkout <HASH_CODE>
dvc fetch
dvc checkout
```

## Setup sub-module "dockprom" for docker containers and docker host monitoring
run at root
```
git submodule add https://github.com/stefanprodan/dockprom
```
Then
```
git submodule init
git submodule update
```
go to folder
```
cd dockprom
```
Then build
```
docker-compose up -d
```
Finally, open Grafana session at http://127.0.0.1:3000/ with ADMIN_USER='admin' ADMIN_PASSWORD='admin'