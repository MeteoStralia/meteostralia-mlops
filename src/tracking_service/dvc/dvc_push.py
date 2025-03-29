import subprocess
import datetime
import json
import os

with open("metrics/RainTomorrow/lastmetrics.json", "r") as file:
    metrics = json.load(file)


tag = list(metrics.keys())[0]
subprocess.run('dvc commit -q')
subprocess.run('git add dvc.lock')
subprocess.run(f"git commit -m 'datamodel'")
subprocess.run(f"git tag -a {tag} -m 'datamodel'")
subprocess.run('git push origin --tags')
subprocess.run('dvc push')