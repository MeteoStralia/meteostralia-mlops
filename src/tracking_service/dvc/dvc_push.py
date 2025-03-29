import subprocess
import datetime

timestamp = datetime.datetime.now().timestamp()
timestamp = str(int(round(timestamp)))
subprocess.run('dvc commit -q')
subprocess.run('git add DVC.lock')
subprocess.run("git commit -m 'new_data and model" + timestamp + "'")
subprocess.run("git tag -a " + timestamp + " -m 'new_data " + timestamp + "'")
subprocess.run('git push origin --tags')
subprocess.run('dvc push')