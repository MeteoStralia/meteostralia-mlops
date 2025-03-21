# meteostralia-mlops

## Virtual environment installation 
Run at root 

```
python3 -m venv env     
.\env\Scripts\activate
pip install -r requirements.txt
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

### Connexion to Dagshub

First connect Meteostralia github repo to dagshub (My repositories +New -> connect a repository -> Other -> set the adress to https://github.com/MeteoStralia/meteostralia-mlops -> identification needed with account name and password or token)

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
git add dvc.lock metrics/
git commit -m "testing a dvc versioning"
git tag -a versioning_test -m "testing a dvc versioning"
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
