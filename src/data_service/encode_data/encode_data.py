import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.base import BaseEstimator, TransformerMixin

# TODO régler les paths pour inclure les fonctions d'autres modules
import sys
sys.path.append('./src/')
sys.path.append('../../')
from data_service.ingest_data.ingest_new_data import load_data
class trigo_encoder(BaseEstimator, TransformerMixin):
    """
    Class to convert cyclical or categorical variable to sinus and cosinus

    Methods:
        fit
        transform
        get_feature_names_out
    """

    def __init__(self, col_select):
        self.col_select = col_select 
        self.mapping_cos_sin = {}

    def fit(self, X, y=None):
        angle_shift = 360/len(X[self.col_select].unique())
        mapping = {}
        i = 0
        for elt in X[self.col_select].unique():
            mapping[elt] = i*angle_shift
            i += 1

        for elt, angle in mapping.items():
            cos_a = np.round(np.cos(np.radians(angle)), 6)
            sin_a = np.round(np.sin(np.radians(angle)), 6)

            self.mapping_cos_sin[elt] = (cos_a, sin_a)

        return self


    def transform(self, X):
        X[self.col_select + '_cos'] = X[self.col_select].apply(lambda x : float(self.mapping_cos_sin[x][0]))
        X[self.col_select + '_sin'] = X[self.col_select].apply(lambda x : float(self.mapping_cos_sin[x][1]))
        X = X.drop(columns = self.col_select)
        self.X = X
        return X

    def get_feature_names_out(self):
        return [self.col_select + '_cos', self.col_select + '_sin']
    
    def get_mapping(self, X):
        angle_shift = 360/len(X[self.col_select].unique())
        mapping = {}
        i = 0
        for elt in X[self.col_select].unique():
            mapping[elt] = i*angle_shift
            i += 1

        for elt, angle in mapping.items():
            cos_a = np.round(np.cos(np.radians(angle)), 6)
            sin_a = np.round(np.sin(np.radians(angle)), 6)

            self.mapping_cos_sin[elt] = (cos_a, sin_a)
        return self.mapping_cos_sin
    
class trigo_encoder_len(BaseEstimator, TransformerMixin):
    """
    Class to convert cyclical or categorical variable to sinus and cosinus

    Methods:
        fit
        transform
        get_feature_names_out
    """

    def __init__(self, col_select, length):
        self.col_select = col_select
        self.length = length
        self.mapping_cos_sin = {}

    def fit(self, X, y=None):
        angle_shift = 360/self.length
        mapping = {}
        i = 0
        for elt in X[self.col_select].unique():
            mapping[elt] = i*angle_shift
            i += 1

        for elt, angle in mapping.items():
            cos_a = np.round(np.cos(np.radians(angle)), 6)
            sin_a = np.round(np.sin(np.radians(angle)), 6)

            self.mapping_cos_sin[elt] = (cos_a, sin_a)

        return self


    def transform(self, X):
        X[self.col_select + '_cos'] = X[self.col_select].apply(lambda x : float(self.mapping_cos_sin[x][0]))
        X[self.col_select + '_sin'] = X[self.col_select].apply(lambda x : float(self.mapping_cos_sin[x][1]))
        X = X.drop(columns = self.col_select)
        self.X = X
        return X
    
    def get_feature_names_out(self):
        return [self.col_select + '_cos', self.col_select + '_sin']

    def get_mapping(self):
        return self.self.mapping_cos_sin

def encode_data(data_to_encode, 
                vars_binary=["RainTomorrow", "RainToday"], 
                vars_dummies=["Year", "Location", "Climate"], 
                vars_ordinal=['Cloud9am', 'Cloud3pm'],
                vars_trigo=["WindGustDir", "WindDir9am", "WindDir3pm", "Month", "Season"]
                ):
    """"
    Encode data with various methods

    Args:
        data_to_encode : DataFrame to encode
        vars_binary : list of columns to encode in binary (Yes -> 1, No -> 0)
        vars_dummies : list of columns to encode as dummies
        vars_ordinal: list of columns to as ordinal (variable with an order)
        vars_trigo : list of columns to encode as sinus and cosinus (cyclical...)
    Returns:
        pd.DataFrame : encoded DataFrame
    """
    # Check which variables are in data
    vars_binary = [x for x in vars_binary if x in data_to_encode.columns]
    vars_dummies = [x for x in vars_dummies if x in data_to_encode.columns]
    vars_ordinal = [x for x in vars_ordinal if x in data_to_encode.columns]
    vars_trigo = [x for x in vars_trigo if x in data_to_encode.columns]

    # Encode binary variables
    data_to_encode[vars_binary] = data_to_encode[vars_binary].apply(lambda x : (x == 'Yes').astype(int))

    # Encode dummies variables                                    
    data_to_encode = pd.get_dummies(data_to_encode, 
                                    columns=vars_dummies, dtype=int)
 
    # Encode sinus and cosinus variables
    for col in vars_trigo :
        data_to_encode = trigo_encoder(col_select=col).fit_transform(data_to_encode)
    
    # Encode ordinal variables
    data_to_encode[vars_ordinal] = OrdinalEncoder().fit_transform(data_to_encode[vars_ordinal])

    return data_to_encode

def encode_newdata(data_origin, new_data, 
                vars_binary=["RainTomorrow", "RainToday"], 
                vars_dummies=["Year", "Location", "Climate"], 
                vars_ordinal=['Cloud9am', 'Cloud3pm'],
                vars_trigo=["WindGustDir", "WindDir9am", "WindDir3pm", "Month", "Season"]
                ):
    """"
    Encode new_data with same enconding as source data

    Args:
        data_origin : DataFrame used to encode
        new_data : DataFrame to encode
        vars_binary : list of columns to encode in binary (Yes -> 1, No -> 0)
        vars_dummies : list of columns to encode as dummies
        vars_ordinal: list of columns to as ordinal (variable with an order)
        vars_trigo : list of columns to encode as sinus and cosinus (cyclical...)
    Returns:
        pd.DataFrame : encoded DataFrame
    """
    # Check which variables are in data
    vars_binary = [x for x in vars_binary if x in new_data.columns]
    vars_dummies = [x for x in vars_dummies if x in new_data.columns]
    vars_ordinal = [x for x in vars_ordinal if x in new_data.columns]
    vars_trigo = [x for x in vars_trigo if x in new_data.columns]

    # Encode binary variables
    data_origin[vars_binary] = data_origin[vars_binary].apply(lambda x : (x == 'Yes').astype(int))
    new_data[vars_binary] = data_origin[vars_binary].apply(lambda x : (x == 'Yes').astype(int))

    # Encode dummies variables                                    
    data_origin = pd.get_dummies(data_origin, 
                                 columns=vars_dummies, dtype=int)
    new_data = pd.get_dummies(new_data, 
                                 columns=vars_dummies, dtype=int)
    
    # Encode sinus and cosinus variables
    for col in vars_trigo:
        encoder = trigo_encoder(col_select=col)
        data_origin = encoder.fit_transform(data_origin)
        new_data = encoder.transform(new_data)
        
    # Encode ordinal variables
    encoder = OrdinalEncoder()
    data_origin[vars_ordinal] = encoder.fit_transform(data_origin[vars_ordinal])
    new_data[vars_ordinal] = encoder.transform(new_data[vars_ordinal])

    return new_data

if __name__ == '__main__':
    # Paths and parameters
    augmented_data_path = 'data/processed_data/augmented_data.csv'
    encoded_data_path = 'data/processed_data/encoded_data.csv'
    index_load = ["id_Location", "id_Date"]

    vars_binary = ["RainTomorrow", "RainToday"]
    vars_dummies = ["Year", "Location", "Climate"] 
    vars_ordinal = ['Cloud9am', 'Cloud3pm']
    vars_trigo = ["WindGustDir", "WindDir9am", "WindDir3pm", 
                  "Month", "Season"]
    
    # load data 
    df = load_data(augmented_data_path, index=index_load)
    df = encode_data(data_to_encode=df,
                     vars_binary=vars_binary,
                     vars_dummies=vars_dummies,
                     vars_ordinal=vars_ordinal,
                     vars_trigo=vars_trigo)
    
    # save all data to process data
    df.to_csv(encoded_data_path, index=True)
    print("Encoded data saved to ", encoded_data_path)
