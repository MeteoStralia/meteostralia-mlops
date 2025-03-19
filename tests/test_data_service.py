
import unittest
import pandas as pd
import sys
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler

#sys.path.append('.')
# import des fonctions à tester
from src.data_service.ingest_data.reset_data import reset_data
from src.data_service.ingest_data.ingest_new_data import load_data, add_data, reindex_data


class TestDataServiceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.raw_data_path="data/raw_data/weatherAUS.csv"
        self.current_data_path = 'data/current_data/current_data.csv'
        self.new_data_folder = 'data/new_data/'
        self.raw_data = pd.read_csv(self.raw_data_path)
        self.current_data = pd.read_csv(self.current_data_path )

    # Test if reset data equals raw_data
    def test_reset_data(self):
        reset_data()
        pd.testing.assert_frame_equal(self.current_data, 
                                      self.raw_data)
    
    # Test if add_data does not add duplicates
    def test_add_data(self):
        # load current data
        df_current = reindex_data(self.current_data)
        # list data files in new data folder
        new_data_files = os.listdir(self.new_data_folder)
        # add new data to current data
        for file in new_data_files:
            df_current = add_data(self.new_data_folder + file, df_current)

        assert not df_current[["Location", "Date"]].duplicated().any()    

    # no idea
    def test_reindex_data(self):
        pass

# Tests on processed data

class TestDataPreprocessing(unittest.TestCase):

    def setUp(self):
        self.current_data_path = 'data/current_data/current_data.csv'
        self.process_data_folder = 'data/processed_data/'
        self.target = "RainTomorrow"
        self.scaler = MinMaxScaler()
        self.X_train = load_data(self.process_data_folder + "X_train.csv")
        self.X_test = load_data(self.process_data_folder + "X_test.csv")
        self.X_train_scaled = load_data(self.process_data_folder + "X_train_scaled.csv")
        self.X_test_scaled  = load_data(self.process_data_folder + "X_test_scaled.csv")
        self.y_train = load_data(self.process_data_folder + "y_train.csv")
        self.y_test = load_data(self.process_data_folder + "y_test.csv")

    # Test on X_train processed data
    def train_preprocessed_data(self):
        self.assertEqual(self.X_train.isnull().sum().sum(), 0)  # Pas de valeurs manquantes
        self.assertTrue(all(self.X_train.columns !=  self.target))  # La colonne target doit être supprimée
        self.assertTrue(isinstance(self.X_train, pd.DataFrame))  # La sortie doit être un DataFrame
        
        # Test if the data is scaled
        scaler = MinMaxScaler()
        expected_df = pd.DataFrame(scaler.fit_transform(
            self.X_train),
            index=self.X_train.index, 
            columns = self.X_train.columns)
        pd.testing.assert_frame_equal(self.X_train_scaled, expected_df)

    # Tests on X_test processed data
    def test_preprocessed_data(self):
        self.assertEqual(self.X_test.isnull().sum().sum(), 0)  # Pas de valeurs manquantes
        self.assertTrue(all(self.X_test.columns !=  self.target))  # La colonne target doit être supprimée
        self.assertTrue(isinstance(self.X_test, pd.DataFrame))  # La sortie doit être un DataFrame
        
        # Test if the data is scaled
        scaler = MinMaxScaler()
        expected_df = pd.DataFrame(scaler.fit_transform(
            self.X_test),
            index=self.X_test.index, 
            columns = self.X_test.columns)
        pd.testing.assert_frame_equal(self.X_test_scaled, expected_df)

    # def test_split_data(self):
    #     # Test data splitting
    #     X_train, X_test, y_train, y_test = split_data(self.df, 'target')
    #     self.assertEqual(len(X_train), 4)
    #     self.assertEqual(len(X_test), 1)
    #     self.assertEqual(len(y_train), 4)
    #     self.assertEqual(len(y_test), 1)
if __name__ == "__main__":
   unittest.main()
