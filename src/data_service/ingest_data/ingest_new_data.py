import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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
    df_new = reindex_data(df_new )
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
    current_data_path = 'data/current_data/current_data.csv'
    new_data_folder = 'data/new_data/'
    # load current data
    df_current = load_data(current_data_path)
    df_current = reindex_data(df_current)
    # list data files in new data folder
    new_data_files = os.listdir(new_data_folder)
    # add new data to current data
    for file in new_data_files:
        df_current = add_data(new_data_folder + file, df_current)
    # save all data to current data
    df_current.to_csv(current_data_path)

# # testing  
# raw_data_path = '../../../data/raw_data/weatherAUS.csv'
# current_data_path = '../../../data/current_data/current_data.csv'
# new_data_folder = '../../../data/new_data/'

# # récupère les données raw et les mets dans current
# raw_data = load_data(raw_data_path)
# raw_data.to_csv(current_data_path, index=False)

# # get current data
# df_current = load_data(current_data_path)
# df_current = reindex_data(df_current)
# new_data_files = os.listdir(new_data_folder)
# for file in new_data_files:
#     df_current = add_data(new_data_folder + file, df_current)

# df_current.to_csv(current_data_path, index=False)