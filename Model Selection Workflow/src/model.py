import optuna
import pandas as pd
# from optuna.trial import TrialState
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from src import ExperimentTracker
# from catboost import Pool, cv
from sklearn.metrics import roc_auc_score
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PolynomialFeatures




class CustomModel:

    def __init__(self, config):
        self.model = config.get_model()
        self.preprocessor = None
        self.config = config

    def get_data(self):
        """Gets X, y from Config data_path"""
        data_path = self.config.data.train_path
        df = pd.read_csv(data_path)

        target_col = self.config.data.target_col
        if target_col in df.columns:
            y = df[target_col]
        else:
            raise KeyError("df doesn't have target column")
        
        X = df.drop(columns=target_col)
        return X, y


    def eval_model(self, params, X_eval, y_eval):
        """Evals model with StratifiedKFold and return mean score"""
        cv = StratifiedKFold(n_splits=self.config.cv.cv_num, shuffle = True, random_state=42)
        score_list = []

        for i, (train_index, test_index) in enumerate(cv.split(X_eval, y_eval)):
            model = self.model(**params)
            model.fit(X_eval.iloc[train_index], y_eval.iloc[train_index])
            y_pred = model.predict_proba(X_eval.iloc[test_index])[:, 1]
            y_true = y_eval[test_index]
            score_list.append(roc_auc_score(y_true, y_pred))
        return np.mean(score_list)

    
    def fit_optuna(self):

        X, y = self.get_data()

        # num_cols, cat_cols = self.get_col_types(X)
        # self.preprocessor = CustomPreprocessor(num_cols, cat_cols)
        # X_processed = self.preprocessor.fit_transform(X)
        X_processed = X

        def objective(trial):
            params = self.config.get_param_space(trial)
            return float(self.eval_model(params, X_processed, y))

        study = optuna.create_study(direction='maximize',
                            storage=f"sqlite:///{self.config.tracker.db_dir}/{self.config.model.name}.db",
                            study_name=self.config.model.name,
                            sampler=optuna.samplers.TPESampler(seed=42),
                            load_if_exists=True)
        study.optimize(objective, n_trials=self.config.cv.n_trials)
        best_params = study.best_params
        self.save_experiment(self.config, best_params, study.best_value)
        # Проверить, правильно ли брать study best_value
    

    @classmethod
    def get_col_types(cls, df: pd.DataFrame):
        """Gets numeric and categorical columns from df"""
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()
        return num_cols, cat_cols

    
    def save_experiment(self, config, params, result):
        tracker = ExperimentTracker(config, params, result)
        tracker.save()
        



# class CustomPreprocessor(BaseEstimator, TransformerMixin):
#     def __init__(self, num_cols, cat_cols):

#         num_branch = Pipeline([
#             ('scaler', StandardScaler()),
#             ('knn_imputer', SimpleImputer(strategy='median'))
#         ])
        
#         cat_branch = Pipeline([
#             ('mode_imputer', SimpleImputer(strategy='most_frequent')),
#             ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
#         ])
        
#         ord_branch = Pipeline([
#             ('mode_imputer', SimpleImputer(strategy='most_frequent')),
#             ('encoder', OrdinalEncoder(categories=ord_categories,
#                                        handle_unknown='use_encoded_value',
#                                        unknown_value=-1))
#         ])

#         # Combine all
#         self.preprocessor_first = ColumnTransformer([
#             ('numerical', num_branch, num_cols),
#             ('categorical', cat_branch, cat_cols),
#             ('ordinal', ord_branch, ord_cols)
#         ], remainder='drop')

#     def fit(self, X, y=None):
#         self.preprocessor.fit(X, y)
#         return self
    
#     def transform(self, X):
#         return self.preprocessor.transform(X)
    
#     def fit_transform(self, X, y=None):
#         return self.preprocessor.fit_transform(X, y)
# 
# 
# 