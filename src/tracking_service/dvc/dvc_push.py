import subprocess


subprocess.run('git add DVC.lock')
subprocess.run('git push')
subprocess.run('dvc push')