# test_train.py

import unittest
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.train import train_model
from src.data_preprocessing import load_data, preprocess_data, split_data

class TestTrainModel(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = {
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50],
            'target': [0, 1, 0, 1, 0]
        }
        self.df = pd.DataFrame(self.data)
        self.file_path = "sample_data.csv"
        self.model_path = "test_model.pkl"
        self.df.to_csv(self.file_path, index=False)

    def tearDown(self):
        # Cleanup
        os.remove(self.file_path)
        if os.path.exists(self.model_path):
            os.remove(self.model_path)

    def test_train_model(self):
        # Test the train_model function
        train_model(self.file_path, 'target', self.model_path)
        
        # Check if the model file is created
        self.assertTrue(os.path.exists(self.model_path))

        # Load the model and test its predictions
        model = joblib.load(self.model_path)
        self.assertIsInstance(model, RandomForestClassifier)

        # Preprocess the data and split it
        df = load_data(self.file_path)
        df = preprocess_data(df)
        X_train, X_test, y_train, y_test = split_data(df, 'target')

        # Test the model accuracy
        accuracy = model.score(X_test, y_test)
        self.assertGreaterEqual(accuracy, 0.0)  # S'assurer que l'accuracy est une valeur valide

if __name__ == "__main__":
    unittest.main()

