<h1 align="center" style="font-size: 50px;">
    PRÉVISIONS MÉTÉO EN AUSTRALIE - Projet MLOps avec interface utilisateur interactive : meteostralia-mlops
</h1>

Schéma Architecture à insérer

# Introduction
<hr style="border: 5px solid #555555;">

**Have you ever wondered** whether you should take an **umbrella** with you tomorrow?  
This **machine learning pipeline** trains a model that aims to predict the **probability of rain** the next day with the target variable `RainTomorrow` for **49 major cities** in **Australia**.

The main objective of this student project is to **translate the theoretical lessons into practice** by designing, building, and deploying a complete **MLOps architecture** based on the previous **Data Scientist project** - development of a machine learning solution.  
In this context, the **customer** is the **user** of our application. 

### Why is the **MLOps** approach relevant to this project?
**MLOps** is the best approach for a **weather prediction project**, because it guarantees **accuracy**, **speed**, **automation**, and **scalability**, while optimizing **costs**. It's a must for **reliable**, **real-time forecasts**.

The project will deal with two specific aspects:  
- How to **manage daily data collection**? 
- Produce a **turnkey solution** for users.

**NB**: Due to the **limited time** available for the development of this project, we opted for a **simple solution** in the form of a **Minimum Viable Product (MVP)**. To achieve this, we chose to use a **Random Forest** prediction model in order to quickly address the **essential goals** while ensuring **robust performance**.


### Project Organization
Arbre à insérer


### Requirements

**Tools**


# Installation
<hr style="border: 5px solid #555555;">

## Virtual environment installation 
Run at root 

```
python3 -m venv env     
.\env\Scripts\activate
pip install -r requirements.txt
```

## Environment variable to setup
create environment variable

```
bash en_var_create.sh
```

## Building and pushing images
Run at root (if images script are changed)
```
bash building_images.sh 
```
Then run (or directly run if build is already done)

```
bash pushing_images.sh 
```

## images cleanup
TO remove none none images run at root
```
bash cleanup_images.sh
```

## pulling latest images
Run at root 
```
bash pulling_images.sh 
```

## Initialization Airflow
To init the airflow services (only first time), run at root
```
docker compose -f docker-compose-airflow.yml up airflow-init -d
```

## Launch all the containers
Run at root 
```
bash launch_airflow.sh 
```

# Orchestration with Airflow

On windows, you have to enable on docker desktop the following option "Expose Daemon in tcp://localhost:2375 without TLS" cf(https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly#configure-docker-for-windows)

Check if all containers are healthy
```
docker container ls
```

then go to http://localhost:8080/
And test the dags : data_model_service and inference_service

## Connexion to Dagshub

First connect Meteostralia github repo to dagshub (My repositories +New -> connect a repository -> Other -> set the adress to https://github.com/MeteoStralia/meteostralia-mlops -> identification needed with account name and password or token)

## change MLFLOW setup and run parameters

Modify the scripts src\tracking_service\mlfow\params_create.py and \src\tracking_service\mlfow\experiment_setup.py
Then run at root
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


# Customer application: instructions for use
<hr style="border: 5px solid #555555;">

This section describes the methodology of how to use the interface for the two types of consumer : 
- The main one - who wants to know if it's going to rain tomorrow : user-client vision
- The one who wants to verifies predictions and API data : data technical vision

These two profiles will have different permissions and displays on the streamlit.

### Sign-in

### Log-in

# Creditors
<hr style="border: 5px solid #555555;">

### Students
**DataScientest oct24_bootcamp_mle**

Mathieu AMACHER

Viridiana BRENOT

Yassine TAZIT

Bruno VERMONT

### Mentor
Sébastien SIME