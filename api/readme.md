utiliisation en serveur seul ave uvicorn
---------> uvicorn main:app --host 0.0.0.0 --port 2222


pour le tester l'app voir la BDD dans main.py









construire l'image
--------> docker build -t api .

lancer le container
--------> docker run -p 2222:2222 api
