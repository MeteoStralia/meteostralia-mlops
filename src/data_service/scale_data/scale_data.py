
import pandas as pd
import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data

from sklearn.preprocessing import StandardScaler, MinMaxScaler

def scale_data(X_train, X_test, scaler = StandardScaler()):

    # Scale features
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)
    X_train_scaled = pd.DataFrame(X_train_scaled, index=X_train.index, columns = X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, index=X_test.index, columns = X_test.columns)
    return X_train_scaled, X_test_scaled

if __name__ == '__main__':
    # load data 
    process_data_folder = 'data/processed_data/'
    X_train = load_data(process_data_folder + "X_train.csv")
    X_test = load_data(process_data_folder + "X_test.csv")
    
    X_train_scaled, X_test_scaled = scale_data(X_train, X_test, scaler=MinMaxScaler())
                                                  
    # save all data to process data
    process_data_folder = 'data/processed_data/'

    X_train_scaled.to_csv(process_data_folder + "X_train_scaled.csv", index=False)
    X_test_scaled.to_csv(process_data_folder + "X_test_scaled.csv", index=False)