
import pandas as pd
import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data

from sklearn.preprocessing import StandardScaler, MinMaxScaler

def scale_data(X_train, X_test, scaler = MinMaxScaler()):

    # Scale features
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_train_scaled = pd.DataFrame(X_train_scaled, index=X_train.index, columns = X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, index=X_test.index, columns = X_test.columns)
    return X_train_scaled, X_test_scaled

def scale_dataframe(data_to_scale, scaler = MinMaxScaler()):

    # Scale features
    data_scaled = scaler.fit_transform(data_to_scale)
    data_scaled = pd.DataFrame(data_scaled , index=data_to_scale.index, columns = data_to_scale.columns)
    return data_scaled


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
    print("Scaled training and test features saved to ", process_data_folder)