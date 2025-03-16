utiliisation en serveur seul ave uvicorn
---------> uvicorn main:app --host 0.0.0.0 --port 1111


pour le tester l'app voir la BDD dans main.py









construire l'image
--------> docker build -t api .

lancer le container
--------> docker run -p 1111:1111 api
