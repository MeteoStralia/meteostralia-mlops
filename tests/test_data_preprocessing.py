# test_data_preprocessing.py

import unittest
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.data_preprocessing import load_data, preprocess_data, split_data

class TestDataPreprocessing(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = {
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50],
            'target': [0, 1, 0, 1, 0]
        }
        self.df = pd.DataFrame(self.data)
        self.file_path = "sample_data.csv"
        self.df.to_csv(self.file_path, index=False)

    def tearDown(self):
        # Cleanup
        import os
        os.remove(self.file_path)

    def test_load_data(self):
        # Test loading data from CSV
        df = load_data(self.file_path)
        pd.testing.assert_frame_equal(df, self.df)

    def test_preprocess_data(self):
        # Test data preprocessing
        preprocessed_df = preprocess_data(self.df.drop(columns=['target']))
        self.assertEqual(preprocessed_df.isnull().sum().sum(), 0)  # Pas de valeurs manquantes
        self.assertTrue(all(preprocessed_df.columns != 'target'))  # La colonne target doit être supprimée
        self.assertTrue(isinstance(preprocessed_df, pd.DataFrame))  # La sortie doit être un DataFrame
        
        # Test if the data is scaled
        scaler = StandardScaler()
        expected_df = pd.DataFrame(scaler.fit_transform(self.df.drop(columns=['target'])), columns=['feature1', 'feature2'])
        pd.testing.assert_frame_equal(preprocessed_df, expected_df)

    def test_split_data(self):
        # Test data splitting
        X_train, X_test, y_train, y_test = split_data(self.df, 'target')
        self.assertEqual(len(X_train), 4)
        self.assertEqual(len(X_test), 1)
        self.assertEqual(len(y_train), 4)
        self.assertEqual(len(y_test), 1)

if __name__ == "__main__":
    unittest.main()

