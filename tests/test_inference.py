# test_inference.py

import unittest
import pandas as pd
import joblib
import os
from src.inference import load_model, run_inference
from src.data_preprocessing import preprocess_data

class TestInference(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = {
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50]
        }
        self.df = pd.DataFrame(self.data)
        
        # Sample model for testing
        self.model_path = "test_model.pkl"
        self.model = joblib.load(self.model_path)
        
    def test_load_model(self):
        # Test loading the model
        model = load_model(self.model_path)
        self.assertIsNotNone(model)
        self.assertEqual(type(model).__name__, "RandomForestClassifier")
        
    def test_run_inference(self):
        # Test running inference
        preprocessed_data = preprocess_data(self.df)
        predictions = run_inference(self.model, preprocessed_data)
        self.assertEqual(len(predictions), len(self.df))
        self.assertIsInstance(predictions, pd.Series)
        
if __name__ == "__main__":
    unittest.main()

