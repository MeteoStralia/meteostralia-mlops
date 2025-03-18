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

## Configuration data_service et modeling_service
Run at root (if first time)
```
docker compose build 
```
Then run (or directly run if build is already done)

```
docker compose up
```

## Configuration suivi DVC

### Initialisation DVC
Not needed if .dvc folder is already pulled
```
dvc init
```

### Connexion Dagshub

First connect Meteostralia github repo to dagshub (My repositories +New -> connect a repository -> Other -> set the adress to https://github.com/MeteoStralia/meteostralia-mlops -> identification needed with account name and password or token)

### Configurer le stockage distant sur Dagshub
installing S3 bucket
```
pip install "dvc[s3]"
dvc remote add origin s3://dvc
dvc remote modify origin endpointurl <REPODAGSHUBURL>
```
then verify if the .dvc/config is modified. It should look like

```
['remote "origin"']
    url = s3://dvc
    endpointurl = <REPODAGSHUBURL>
```
