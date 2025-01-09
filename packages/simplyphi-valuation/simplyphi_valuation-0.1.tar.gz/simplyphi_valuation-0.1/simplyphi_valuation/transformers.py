# transformers.py

import pandas as pd
import numpy as np
import re
import joblib
from sklearn.base import BaseEstimator, TransformerMixin
import pkg_resources
import os


class NumTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.num_cols = ['stamp_duty', 'bathrooms', 'bedrooms', 'shared_lha', 'brma', 'habitable_rooms', 'floor_area', 'price']
        self.log_cols = ['price', 'floor_area', 'brma', 'shared_lha']
        self.location_cols = ['latitude', 'longitude']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        for col in self.num_cols:
            if col in X_copy.columns:
                X_copy[col] = X_copy[col].apply(self.clean_num_data)

        for col in self.log_cols:
            if col in X_copy.columns:
                X_copy[col] = X_copy[col].replace(0, np.nan)
                X_copy[col] = X_copy[col].apply(lambda x: np.log(x) if x > 0 else np.nan)

        X_copy[self.location_cols] = X_copy[self.location_cols].astype(np.float32)
        X_copy[X_copy.select_dtypes(include=['float64']).columns] = X_copy.select_dtypes(include=['float64']).astype(np.float32)

        return X_copy

    def clean_num_data(self, x):
        """Convert string with numeric values to float, or return the value unchanged."""
        if isinstance(x, str):
            match = re.search(r'\d+\.?\d*', x)
            if match:
                return np.float32(match.group())
            else:
                return np.nan
        elif isinstance(x, float):
            return np.float32(x)
        return np.nan


class FillnaTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.str_cols = ['display_address', 'summary', 'brma_text']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy[self.str_cols] = X_copy[self.str_cols].fillna('unknown').applymap(lambda x: x.strip() if isinstance(x, str) else x)
        X_copy['habitable_rooms'] = X_copy['habitable_rooms'].fillna(X_copy['bedrooms'])
        X = X.replace('None', np.nan)

        return X_copy


class DropTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.log_cols = ['price', 'floor_area', 'brma', 'shared_lha']
        self.str_cols = ['display_address', 'summary', 'brma_text']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.dropna(subset=self.log_cols)
        X_copy = X_copy.drop(columns=[col for col in self.str_cols if col in X_copy.columns])

        return X_copy


class FeatureTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.group_cols = ['region', 'laua', 'out_code', 'bedrooms']
        # self.ref_data_path = pkg_resources.resource_filename('simplyphi_valuation','data/training_grouped_data_for_meanandmedian.csv')
        self.ref_data_path = pkg_resources.resource_filename('simplyphi_valuation',os.path.join("data","training_grouped_data_for_meanandmedian.csv"))
        self.ref_data = pd.read_csv(self.ref_data_path)
        self.columns_to_transform = ['price', 'stamp_duty', 'brma', 'shared_lha', 'zscore']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        type_col_candidates = X_copy.columns[X_copy.columns.str.contains("type_")]
        if type_col_candidates.empty:
            raise ValueError("No column matching 'type_' found in the input data.")
        type_col = type_col_candidates.tolist()[0]
        group_cols = self.group_cols + [type_col]

        X_copy['total_rooms'] = X_copy['bedrooms'] + X_copy['bathrooms']
        X_copy['room_density'] = X_copy['floor_area'] / np.maximum(X_copy['total_rooms'], 1)
        X_copy['price_per_sqft'] = X_copy['price'] / np.maximum(X_copy['floor_area'], 1)

        X_copy = self.add_group_mean_median(X_copy, group_cols)

        return X_copy

    def add_group_mean_median(self, X_copy, group_cols):
        req_cols = [col for col in self.ref_data.columns if '_by_group_' in col]

        try:
            merged_data = pd.merge(
                X_copy, 
                self.ref_data[group_cols + req_cols], 
                on=group_cols, 
                how='left'
            )
            return merged_data
        except KeyError as e:
            raise KeyError(f"Missing required columns in reference data or input data: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while merging group statistics: {e}")


class StrColTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.keywords = ['pool', 'garden', 'garage', 'balcony', 'view']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        for keyword in self.keywords:
            column_name = f'has_{keyword}'
            X_copy[column_name] = X_copy['summary'].str.contains(keyword, case=False, na=False).astype(np.float32)

        return X_copy


class CatColTransformer(BaseEstimator, TransformerMixin):
    # def __init__(self, encoder_path="data/ordinal_encoder.pkl"):
    def __init__(self, encoder_path=os.path.join("data","ordinal_encoder.pkl")):
        self.one_hot_cols = ['type', 'epc_current_rating', 'epc_potential_rating']
        self.ordinal_cols = ['laua', 'region', 'out_code']
        self.encoder_path = pkg_resources.resource_filename("simplyphi_valuation",encoder_path)
        self.encoder = joblib.load(self.encoder_path)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        X_copy = pd.get_dummies(X_copy, columns=self.one_hot_cols, drop_first=False)
        try:
            X_copy[self.ordinal_cols] = self.encoder.transform(X_copy[self.ordinal_cols])
        except Exception:
            X_copy[self.ordinal_cols] = None
        
        return X_copy


class PostProcessingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_copy = X.copy()

        X_copy = X_copy.replace({False: 0, True: 1})
        X_copy.replace([np.inf, -np.inf], np.nan, inplace=True)
        numeric_cols = X_copy.select_dtypes(include=['float', 'int', 'bool']).columns
        X_copy[numeric_cols] = X_copy[numeric_cols].astype(np.float32)

        return X_copy


class InitializeDataTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.columns = [
            'bedrooms', 'bathrooms', 'price', 'latitude', 'longitude', 'laua',
            'out_code', 'region', 'habitable_rooms', 'floor_area', 'total_rooms',
            'room_density', 'price_per_sqft', 'mean_by_group_price',
            'mean_by_group_stamp_duty', 'mean_by_group_zscore',
            'mean_by_group_brma', 'mean_by_group_shared_lha',
            'median_by_group_price', 'median_by_group_stamp_duty',
            'median_by_group_zscore', 'median_by_group_brma',
            'median_by_group_shared_lha', 'has_parking', 'has_garden', 'has_pool',
            'has_garage', 'type_Apartment', 'type_Bungalow', 'type_Detached',
            'type_Detached Bungalow', 'type_Detached bungalow',
            'type_Detached house', 'type_Duplex', 'type_End of Terrace',
            'type_Flat', 'type_Ground Flat', 'type_Ground Maisonette', 'type_House',
            'type_Link Detached House', 'type_Maisonette', 'type_Semi-Detached',
            'type_Semi-Detached Bungalow', 'type_Semi-detached bungalow',
            'type_Semi-detached house', 'type_Studio', 'type_Terraced',
            'type_Terraced Bungalow', 'type_Terraced house', 'type_Town House',
            'type_Town house', 'type_bungalow', 'type_detached', 'type_end_terrace',
            'type_flat', 'type_maisonette', 'type_semi_detached',
            'type_semi_detached_bungalow', 'type_studio', 'type_terraced',
            'epc_current_rating_A', 'epc_current_rating_B', 'epc_current_rating_C',
            'epc_current_rating_D', 'epc_current_rating_E', 'epc_current_rating_F',
            'epc_current_rating_G', 'epc_current_rating_unknown',
            'epc_potential_rating_A', 'epc_potential_rating_B',
            'epc_potential_rating_C', 'epc_potential_rating_D',
            'epc_potential_rating_E', 'epc_potential_rating_F',
            'epc_potential_rating_G', 'epc_potential_rating_unknown'
        ]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if X.empty:
            raise ValueError("Input DataFrame is empty.")
        
        main_df = pd.DataFrame(0, index=[0], columns=self.columns, dtype='float32')
        
        for column in X.columns:
            if column in main_df.columns:
                main_df.at[0, column] = X.iloc[0][column]
        
        return main_df
