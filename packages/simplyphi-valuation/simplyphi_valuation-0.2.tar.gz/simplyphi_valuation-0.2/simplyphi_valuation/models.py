import joblib
import os
import pkg_resources
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin, clone
from sklearn.model_selection import KFold

class StackingAveragedModels(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self, base_models, meta_model, n_folds=5):
        self.base_models = base_models  # Fixed typo
        self.meta_model = meta_model
        self.n_folds = n_folds

    def fit(self, X, y):
        if hasattr(X, 'values'):
            X = X.values
        if hasattr(y, 'values'):
            y = y.values

        self.base_models_ = [list() for _ in self.base_models]
        self.meta_model_ = clone(self.meta_model)
        kfold = KFold(n_splits=self.n_folds, shuffle=True, random_state=156)

        out_of_fold_predictions = np.zeros((X.shape[0], len(self.base_models)))
        for i, model in enumerate(self.base_models):
            for train_index, holdout_index in kfold.split(X):
                instance = clone(model)
                self.base_models_[i].append(instance)
                instance.fit(X[train_index], y[train_index])
                y_pred = instance.predict(X[holdout_index])
                out_of_fold_predictions[holdout_index, i] = y_pred

        self.meta_model_.fit(out_of_fold_predictions, y)
        return self

    def predict(self, X):
        """Make predictions using the fitted meta-model."""
        if hasattr(X, 'values'):
            X = X.values

        meta_features = np.column_stack([
            np.mean([model.predict(X) for model in base_models], axis=0)
            for base_models in self.base_models_
        ])

        return self.meta_model_.predict(meta_features)

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
