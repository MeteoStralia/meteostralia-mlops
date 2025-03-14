# api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from data_preprocessing import preprocess_data

app = FastAPI()

class InferenceRequest(BaseModel):
    data: dict

class InferenceResponse(BaseModel):
    prediction: list

# Charger le modèle entraîné
model_path = "models/random_forest_model.pkl"
model = joblib.load(model_path)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MLOps API"}

@app.post("/predict", response_model=InferenceResponse)
def predict(request: InferenceRequest):
    try:
        # Convert input data to DataFrame
        input_data = pd.DataFrame([request.data])

        # Preprocess the data
        preprocessed_data = preprocess_data(input_data)

        # Make predictions
        predictions = model.predict(preprocessed_data)

        return InferenceResponse(prediction=predictions.tolist())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

