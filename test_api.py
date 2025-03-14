# test_api.py

import unittest
from fastapi.testclient import TestClient
from src.api import app

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurer le TestClient pour l'application FastAPI
        cls.client = TestClient(app)

    def test_read_root(self):
        # Tester le root endpoint
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to the MLOps API"})

    def test_predict(self):
        # Tester l'endpoint de prédiction avec l'échantillon de donnée
        sample_data = {
            "data": {
                "feature1": 1,
                "feature2": 10
            }
        }
        response = self.client.post("/predict", json=sample_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("prediction", response.json())
        self.assertIsInstance(response.json()["prediction"], list)

    def test_predict_invalid_data(self):
        # Tester l'endpoint de prédiction avec une donnée invalide
        invalid_data = {
            "data": {
                "feature1": "invalid",
                "feature2": 10
            }
        }
        response = self.client.post("/predict", json=invalid_data)
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()

