# src/models.py
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

class BaseModelAdapter(BaseEstimator):
    """Контракт: fit/predict/predict_proba/get_params — одинаковы для всех."""
    def fit(self, X, y):
        pass
    def predict_proba(self, X):
        pass    # всегда возвращаетpositives в 1-м столбце

class LogisticRegressionAdapter(BaseModelAdapter):
    def __init__(self, **params):
        self._model = LogisticRegression(**params)
    def fit(self, X, y):
        self._model.fit(X, y)
        return self
    def predict_proba(self, X):
        return self._model.predict_proba(X)


MODEL_REGISTRY = {
    "LogisticRegression": LogisticRegressionAdapter,
    # "CatBoost":             CatBoostAdapter,
    # "LightGBM":             LGBMAdapter,
    # "XGBoost":              XGBAdapter,
}

def build_model(name: str, **params):
    try:
        return MODEL_REGISTRY[name](**params)
    except KeyError:
        raise ValueError(f"Модель '{name}' не зарегистрирована. Доступны: {list(MODEL_REGISTRY)}")
