import joblib
import os
import pkg_resources
from sklearn.base import BaseEstimator, TransformerMixin

class ModelPredictionTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        # self.model_path = "/windows/parth/PhilCapital/new2/simplyphi_valuation/simplyphi_valuation/data/updated_model_jan3.pkl"
        self.model_path = pkg_resources.resource_filename(
            "simplyphi_valuation", os.path.join("data","updated_model_jan3.pkl")
        )
        self.model = joblib.load(self.model_path)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if "price" in X.columns:
            X = X.drop(["price"],axis=1)
        prediction = self.model.predict(X)
        return prediction
