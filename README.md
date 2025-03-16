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

