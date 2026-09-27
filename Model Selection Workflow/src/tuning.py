from pathlib import Path

import numpy as np
import optuna
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

from .exp_tracker import ExperimentTracker
from .models import build_model


class TuningPipeline:
    def __init__(self, config):
        self.preprocessor = None
        self.config = config

    def load_dataset(self):
        """Load features and target, excluding configured feature columns."""
        df = pd.read_csv(self.config.data.train_path)
        target_col = self.config.data.target_col
        if target_col not in df.columns:
            raise KeyError(f"Training data does not contain target column {target_col!r}")

        drop_cols = [target_col, *self.config.data.drop_cols]
        X = df.drop(columns=drop_cols)
        return X, df[target_col]

    def eval_model(self, params, X, y):
        """Evaluate hyperparameters with a reproducible stratified CV split."""
        cv = StratifiedKFold(
            n_splits=self.config.cv.n_splits,
            shuffle=True,
            random_state=self.config.seed,
        )
        scores = []
        for train_index, test_index in cv.split(X, y):
            model = build_model(self.config.model.name, **params)
            model.fit(X.iloc[train_index], y.iloc[train_index])
            y_true = y.iloc[test_index]
            y_pred = model.predict_proba(X.iloc[test_index])[:, 1]
            scores.append(roc_auc_score(y_true, y_pred))
        return float(np.mean(scores))

    def run_hpo(self):
        X, y = self.load_dataset()
        db_dir = Path(self.config.tracker.db_dir)
        db_dir.mkdir(parents=True, exist_ok=True)

        def objective(trial):
            params = self.config.suggest_params(trial)
            return self.eval_model(params, X, y)

        study = optuna.create_study(
            direction="maximize",
            storage=f"sqlite:///{db_dir / (self.config.model.name + '.db')}",
            study_name=f'{self.config.tracker.exp_name}-{self.config.model.name}',
            sampler=optuna.samplers.TPESampler(seed=self.config.seed),
            load_if_exists=True,
        )
        study.optimize(objective, n_trials=self.config.cv.n_trials)
        return self.record_run(self.config, study.best_params, study.best_value)

    def record_run(self, config, params, result):
        return ExperimentTracker(config, params, result).save()


def infer_column_types(df: pd.DataFrame):
    """Return numeric and categorical feature names."""
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(
        include=["object", "category", "bool", "string"]
    ).columns.tolist()
    return num_cols, cat_cols
