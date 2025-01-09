# pipeline.py

from .transformers import FillnaTransformer, NumTransformer, StrColTransformer, CatColTransformer, FeatureTransformer, PostProcessingTransformer, DropTransformer, InitializeDataTransformer
from .models import ModelPredictionTransformer
from sklearn.pipeline import Pipeline

def load_pipeline():
    pipeline = Pipeline([
        ('fillna', FillnaTransformer()),
        ('num_transform', NumTransformer()),
        ('str_col_transform', StrColTransformer()),
        ('cat_col_transform', CatColTransformer()),
        ('feature_transform', FeatureTransformer()),
        ('post_processing', PostProcessingTransformer()),
        ('drop_transform', DropTransformer()),
        ('initialize_data', InitializeDataTransformer()),
        ('model_predict', ModelPredictionTransformer())
    ])
    return pipeline
