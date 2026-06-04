import optuna
import pandas as pd
from optuna.trial import TrialState
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from src import MyPreprocessor, CatBoostPreprocessor, get_num_cat_ord_cols
from src import Config
from catboost import Pool, cv


def train_optuna_cv(model_class, param_space_func, X, y, n_trials=1, cv_num=5):
    
    num_cols, cat_cols, ord_cols, ord_cats = get_num_cat_ord_cols(X)

    if model_class.__name__ == 'CatBoostClassifier':
        preprocessor = CatBoostPreprocessor(
            num_cols, cat_cols, ord_cols, ord_cats
        )
        xx = preprocessor.fit_transform(X)
        cat_cols = xx.select_dtypes(include=['object', 'category']).columns.tolist()

    else:
        preprocessor = MyPreprocessor(
            num_cols, cat_cols, ord_cols, ord_cats
        )


    def objective(trial):
        params = param_space_func(trial)

        if model_class.__name__ == 'CatBoostClassifier':
            params['cat_features'] = cat_cols

        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model_class(**params))
            ])
        
        folds = StratifiedKFold(n_splits=cv_num, shuffle=True, random_state=Config.SEED)

        score = cross_val_score(
            pipeline, X, y,
            cv=folds,
            scoring='roc_auc',
            n_jobs=-1,
            verbose=1
        ).mean()
        
        return score

    study = optuna.create_study(direction='maximize',
                                storage=f"sqlite:///{model_class.__name__}_logs.db",
                                study_name=model_class.__name__,
                                sampler=optuna.samplers.TPESampler(seed=Config.SEED),
                                load_if_exists=True)
    study.optimize(objective, n_trials=n_trials)

    # Fit the best model with the entire dataset for easy production use
    if model_class.__name__ == 'CatBoostClassifier':
        best_params = study.best_params
        best_params['cat_features'] = cat_cols

    best_model = model_class(**best_params)

    best_pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('model', best_model)
                ])
    
    best_pipeline.fit(X, y)

    return best_pipeline, study.best_params
