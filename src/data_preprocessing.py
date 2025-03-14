# data_preprocessing.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    """
    Charger les données depuis un fichier CSV.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    return pd.read_csv(file_path)

def preprocess_data(df):
    """
    Effectuer le preprocess des données: gérer les valeurs manquantes, encoder les variables catégorielles, et scale features.

    Args:
        df (pd.DataFrame): Input data.

    Returns:
        pd.DataFrame: Preprocessed data.
    """
    # Gérer les valeurs manquantes
    df = df.dropna()
    
    # Encoder les variables catégorielles
    df = pd.get_dummies(df, drop_first=True)

    # Scale features
    scaler = StandardScaler()
    df[df.columns] = scaler.fit_transform(df[df.columns])

    return df

def split_data(df, target_column, test_size=0.2, random_state=42):
    """
    Diviser les données en training et testing sets.

    Args:
        df (pd.DataFrame): Input data.
        target_column (str): Name of the target column.
        test_size (float): Proportion of the data to include in the test split.
        random_state (int): Random seed.

    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

