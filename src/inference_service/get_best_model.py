import mlflow
import dagshub
import os

def get_best_model(metric="f1_score"):
    dagshub.auth.add_app_token(os.environ['AIRFLOW_DAGSHUB_USER_TOKEN'], host=None)
    dagshub.init(url=os.environ['AIRFLOW_MLFLOW_TRACKING_URI'], mlflow=True)
    mlflow.set_tracking_uri(os.environ['AIRFLOW_MLFLOW_TRACKING_URI'])
    # get allruns data
    runs = mlflow.search_runs(experiment_ids=os.environ["EXPERIMENT_ID"])
    max_metric = runs["metrics."+metric].max()
    best_run = runs[runs["metrics."+metric] == max_metric]
    best_run = best_run.drop_duplicates(subset = "metrics."+metric)
    run_id = str(best_run["run_id"].values[0])
    model_uri = f"runs:/{run_id}/{os.environ["ARTIFACT_PATH"]}"
    loaded_model = mlflow.sklearn.load_model(model_uri)
    return loaded_model

