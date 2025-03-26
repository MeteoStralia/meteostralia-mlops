import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import sys
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import emoji

# TODO régler les paths pour inclure les fonctions d'autres modules
sys.path.append('./src/')
from data_service.ingest_data.ingest_new_data import load_data
from global_functions import create_folder_if_necessary, get_params_service

def complete_na_median_location_month(df, columns, verbose=False):
    """
    complete Na of columns with median by location and month.

    Args:
        df (pd.DataFrame) : dataset to complete
        columns (str) : columns to complete (quantitative variable)

    Returns:
        pd.DataFrame: modified DataFrame
    """
    
    median_values = df.groupby(["Month", "Location"])[columns].median()
    for col in columns:
        df[col] = df.set_index(["Month", "Location"])[col].fillna(median_values[col]).values
    
    if verbose == True:
        print("Remplacement de valeurs manquantes par la médiane par station et mois pour la variable ", columns, f"{emoji.emojize(':thumbs_up:')}")
    return df


def complete_na_mode_location_month(df, columns, verbose=False):
    """
    complete Na of columns with mode by location and month.

    Args:
        df (pd.DataFrame) : dataset to complete
        columns (str) : columns to complete (qualitative variable)

    Returns:
        pd.DataFrame: modified DataFrame
    """
    mode_values = df.groupby(["Month", "Location"])[columns].agg(lambda x: pd.Series.mode(x, dropna=False)[0])
    for col in columns:
        
        df[col] = df.set_index(["Month", "Location"])[col].fillna(mode_values[col]).values
    
    if verbose == True:
         print("Remplacement de valeurs manquantes par le mode par station et mois pour la variable ", columns, f"{emoji.emojize(':thumbs_up:')}")
    return df


def create_pipeline_nas(verbose=False):
    """
    Create a pipeline to complete Nas.
    Two different functions are applied to quantitative vars and qualitative vars
    Other functions could be added... (nearest neighours, rolling mean...)

    Args:
        verbose : to print pipeline information

    Returns:
        pipeline with steps (each step is a FunctionTransformer on one column)
    """

    quant_var = ['MinTemp', 'MaxTemp', 'Rainfall',
                'Evaporation','Sunshine',
                'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm',
                'Humidity9am', 'Humidity3pm',
                'Pressure9am', 'Pressure3pm',
                'Temp9am','Temp3pm']
    
    qual_var = ["WindGustDir", 'WindDir9am','WindDir3pm','Cloud9am', 'Cloud3pm']

    complete_nas_transformer = Pipeline(steps=[('init','')])

    for col_select in quant_var:
        complete_nas_transformer.steps.append(
            (('median_location_month_' + col_select), 
             FunctionTransformer(complete_na_median_location_month,
                                 kw_args={'columns':[col_select], 'verbose':verbose})))
        
    for col_select in qual_var:
        complete_nas_transformer.steps.append(
            (('mode_location_month_' + col_select), 
             FunctionTransformer(complete_na_mode_location_month,
                                 kw_args={'columns':[col_select], 'verbose':verbose})))
    
    # drop first step
    complete_nas_transformer.steps.pop(0)
    return complete_nas_transformer


if __name__ == '__main__':
    
    # paths and parameters
    load_dotenv(dotenv_path='src/docker.env'
    params_data = get_params_service(service="data_service")
    index_load = params_data["index_load"]
    uptodate_data_path = params_data["uptodate_data_path"]
    processed_data_folder = params_data["processed_data_folder"]
    processed_data_path = params_data["processed_data_path"]
    
    # load current data
    df_uptodate = load_data(uptodate_data_path, 
                            index=index_load)
    
    # add year and month (TODO add this in load data or before)
    df_uptodate["Year"] = pd.to_datetime(df_uptodate["Date"]).dt.year
    df_uptodate["Month"] = pd.to_datetime(df_uptodate["Date"]).dt.month

    # changing cloud to string (this variable is an index) (TODO add this in load data or before)
    df_uptodate["Cloud3pm"] = df_uptodate["Cloud3pm"].astype(str).replace('nan',np.nan)
    df_uptodate["Cloud9am"] = df_uptodate["Cloud9am"].astype(str).replace('nan',np.nan)
    
    # create Nas completion pipeline
    complete_nas_pipeline = create_pipeline_nas()
   
    # check Nas before 
    nas_before = pd.DataFrame(df_uptodate.isna().sum())

    # apply pipeline
    df_uptodate = complete_nas_pipeline.fit_transform(df_uptodate)
    
    # print Nas after
    nas_after = pd.DataFrame(df_uptodate.isna().sum())
    nas_after = pd.merge(nas_before, nas_after, left_index=True, right_index=True)
    nas_after.columns = ['Avant', 'Après']
    print(nas_after)
    
    # save all data to process data
    create_folder_if_necessary(processed_data_folder)
    df_uptodate.to_csv(processed_data_path, index=True)
    print("Completed data saved to ", processed_data_path)


