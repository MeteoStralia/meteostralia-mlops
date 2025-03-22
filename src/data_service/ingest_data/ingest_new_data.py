import pandas as pd
import os
import sys
sys.path.append('./src/')

def load_data(file_path, index = None):
    """
    Charger les données depuis un fichier CSV.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    df = pd.read_csv(file_path, index_col=index)
    return df

def reindex_data(df):
    """
    # index by Location and Date.

    Args:
        pd.DataFrame

    Returns:
        pd.DataFrame
    """

    # set date to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    # index by Location and Date
    df = df.set_index(["Location", "Date"], drop=False)
    # changing index name
    df = df.reindex(df.index.rename({"Location" : "id_Location", "Date" : "id_Date"}))
    return df

def add_data(file_path, df_origin):
    """
    load new data from CSV file and concatenate them to current dataset.

    Args:
        file_path (str): Path to the CSV file.
        df_origin (pd.DataFrame) : current dataset

    Returns:
        pd.DataFrame: concat DataFrame
    """

    df_new = load_data(file_path)
    df_new = reindex_data(df_new)
    # verify if data does not already exist
    
    if set(df_new.index.values)  - set(df_origin.index.values) != set():
        index_tokeep = pd.MultiIndex.from_tuples(set(df_new.index.values)  - set(df_origin.index.values))
        df_new = df_new.loc[index_tokeep]
        # condat new data with df origin
        df_tuned = pd.concat([df_origin, df_new])
    else:
        print("no new data to add from", file_path)
        df_tuned = df_origin
    return df_tuned


if __name__ == '__main__':
    # Paths and parameters
    current_data_path = 'data/current_data/current_data.csv'
    uptodate_data_path = 'data/current_data/uptodate_data.csv'
    new_data_folder = 'data/new_data/'

    # load current data
    df_current = load_data(current_data_path)
    df_current = reindex_data(df_current)
    # list data files in new data folder
    new_data_files = os.listdir(new_data_folder)

    # add new data to current data
    for file in new_data_files:
        df_current = add_data(new_data_folder + file, df_current)
    
    # drop columns not needed
    if 'Unnamed: 0' in df_current.columns:
        df_current = df_current.drop(columns='Unnamed: 0')
    if ('id_Location' in df_current.columns) and ('id_Date' in df_current.columns):
        df_current = df_current.drop(columns=['id_Location', 'id_Date'])
    
    # save all data to current data and uptodate data
    df_current.reset_index().to_csv(current_data_path, index=False)
    print("new data saved to current")
    df_current.to_csv(uptodate_data_path, index=True)
    print("new data saved to uptodate")