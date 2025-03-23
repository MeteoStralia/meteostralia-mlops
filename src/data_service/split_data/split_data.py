import pandas as pd
from sklearn.model_selection import train_test_split
import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data
from src.global_functions import get_params_service

def split_data(df, target_column=str, test_size=float, 
               random_state=int, sep_method="classic", **kwargs):
    """
    Diviser les données en training et testing sets.

    Args:
        df (pd.DataFrame): Input data.
        target_column (str): Name of the target column.
        test_size (float): Proportion of the data to include in the test split.
        random_state (int): Random seed.
        sep_method (str) : "classic" -> random, "temporal" -> split data on the temporal axis 
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    if sep_method == "classic":
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, 
            random_state=random_state, stratify = y)
    
    if sep_method == "temporal":
        train_size =1-test_size
        df["Date"] = df.index.get_level_values(1).values
        years = pd.to_datetime(df.Date).dt.year
        Part_data_year = years.value_counts().sort_index().cumsum()/len(years)
        year_split = Part_data_year.loc[Part_data_year > train_size].index[0]
        id_train = years[years < year_split].index
        id_test = years[years >= year_split].index
        X_train = X.loc[id_train]
        X_test =  X.loc[id_test]
        y_train = y.loc[id_train]
        y_test =  y.loc[id_test]
    
    return X_train, X_test, y_train, y_test

if __name__ == '__main__':

    # Paths and parameters
    params_data = get_params_service(service="data_service")
    encoded_data_path = params_data['encoded_data_path']
    processed_data_folder = params_data['processed_data_folder']
    index_load = params_data["index_load"]
    threshold = params_data["threshold"]
    # target_column = "RainTomorrow"
    # test_size = 0.2
    # random_state = 1234
    # sep_method = "classic"
   

    # load data 
    df = load_data(encoded_data_path, index=index_load)

    # drop columns with a lot a na (TODO : add a dropna function)
    missing_percentages = df.isna().mean()
    # Colonnes à conserver
    columns_to_keep = missing_percentages[missing_percentages <= threshold].index
    columns_dropped = missing_percentages[missing_percentages > threshold].index
    df = df[columns_to_keep]

    # drop remaining na
    df = df.dropna()

    if "Date" in df.columns:
        df = df.drop(columns="Date")

    X_train, X_test, y_train, y_test = \
        split_data(df, **params_data)
                                                  
    # save all data to process data
    X_train.to_csv(processed_data_folder + "X_train.csv", index=False)
    X_test.to_csv(processed_data_folder + "X_test.csv", index=False)
    y_train.to_csv(processed_data_folder + "y_train.csv", index=False)
    y_test.to_csv(processed_data_folder + "y_test.csv", index=False)
    print("Training and test data saved to ", processed_data_folder)