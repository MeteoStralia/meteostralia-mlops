import pandas as pd
from sklearn.model_selection import train_test_split
import sys
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data, reindex_data

def split_data(df, target_column, test_size=0.2, random_state=42, sep_method = "classique"):
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
    # load data 
    process_data_path = 'data/processed_data/encoded_data.csv'
    df = load_data(process_data_path, index =["id_Location","id_Date"])
   
    # drop na (TODO : add a dropna function)
    missing_percentages = df.isna().mean()
    # Colonnes à conserver
    threshold = 0.25
    columns_to_keep = missing_percentages[missing_percentages <= threshold].index
    columns_dropped = missing_percentages[missing_percentages > threshold].index
    df = df[columns_to_keep]
    df = df.dropna()
    df = df.drop(columns = "Date")

    X_train, X_test, y_train, y_test = \
        split_data(df, target_column = "RainTomorrow", 
                   test_size=0.2, random_state=1234,
                   sep_method="classic")
                                                  
    # save all data to process data
    process_data_folder = 'data/processed_data/'

    X_train.to_csv(process_data_folder + "X_train.csv", index=False)
    X_test.to_csv(process_data_folder + "X_test.csv", index=False)
    y_train.to_csv(process_data_folder + "y_train.csv", index=False)
    y_test.to_csv(process_data_folder + "y_test.csv", index=False)