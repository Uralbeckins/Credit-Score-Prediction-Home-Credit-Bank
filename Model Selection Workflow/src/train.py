import optuna
from optuna.trial import TrialState
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from src import MyPreprocessor, get_num_cat_ord_cols
from src import Config

def train_optuna_cv(model_class, param_space_func, X, y, n_trials=1, cv_num=5):
    
    num_cols, cat_cols, ord_cols = get_num_cat_ord_cols(X)
    
    preprocessor = MyPreprocessor(
        num_cols, cat_cols, ord_cols
    )

    def objective(trial):
            params = param_space_func(trial)
            
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('model', model_class(**params))
                ])
            
            cv = StratifiedKFold(n_splits=cv_num, shuffle=True, random_state=Config.SEED)

            score = cross_val_score(
                pipeline, X, y,
                cv=cv,
                scoring='roc_auc',
                n_jobs=-1,
                verbose=1
            ).mean()
            
            return score

    study = optuna.create_study(direction='maximize',
                                storage="sqlite:///optuna_logs.db",
                                study_name=model_class.__name__,
                                sampler=optuna.samplers.TPESampler(seed=Config.SEED),
                                load_if_exists=True)
    study.optimize(objective, n_trials=n_trials)

    # Fit the best model with the entire dataset for easy production use
    best_model = model_class(**study.best_params)

    best_pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('model', best_model)
                ])
    
    best_pipeline.fit(X, y)

    return best_pipeline, study.best_params