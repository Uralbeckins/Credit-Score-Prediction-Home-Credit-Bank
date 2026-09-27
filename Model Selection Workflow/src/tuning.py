from src import ExperimentTracker, build_model
import numpy as np
import pandas as pd
import optuna
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score, StratifiedKFold

# from sklearn.impute import SimpleImputer
# from sklearn.compose import ColumnTransformer
# from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PolynomialFeatures
# from optuna.trial import TrialState



class TuningPipeline:

    def __init__(self, config):
        self.preprocessor = None
        self.config = config

    def load_dataset(self):
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
        cv = StratifiedKFold(n_splits=self.config.cv.n_splits, shuffle = True, random_state=42)
        score_list = []

        for i, (train_index, test_index) in enumerate(cv.split(X_eval, y_eval)):
            model = build_model(self.config.model.name, **params)
            model.fit(X_eval.iloc[train_index], y_eval.iloc[train_index])
            y_pred = model.predict_proba(X_eval.iloc[test_index])[:, 1]
            y_true = y_eval[test_index]
            score_list.append(roc_auc_score(y_true, y_pred))
        return np.mean(score_list)

    
    def run_hpo(self):

        X, y = self.load_dataset()

        # num_cols, cat_cols = infer_column_types(X)
        # self.preprocessor = CustomPreprocessor(num_cols, cat_cols)
        # X_processed = self.preprocessor.fit_transform(X)
        X_processed = X

        def objective(trial):
            params = self.config.suggest_params(trial)
            return float(self.eval_model(params, X_processed, y))

        study = optuna.create_study(direction='maximize',
                            storage=f"sqlite:///{self.config.tracker.db_dir}/{self.config.model.name}.db",
                            study_name=self.config.model.name,
                            sampler=optuna.samplers.TPESampler(seed=42),
                            load_if_exists=True)
        study.optimize(objective, n_trials=self.config.cv.n_trials)
        best_params = study.best_params
        self.record_run(self.config, best_params, study.best_value)
        # Проверить, правильно ли брать study best_value
    

    def record_run(self, config, params, result):
        tracker = ExperimentTracker(config, params, result)
        tracker.save()


def infer_column_types(df: pd.DataFrame):
    """Gets numeric and categorical columns from df"""
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool", "string"]).columns.tolist()
    return num_cols, cat_cols