from src import train_optuna_cv
from src import get_stats
from sklearn.model_selection import train_test_split
from src import Config
from src import save_experiment


def run_experiment(exp_name, model_class, param_space_func, df, n_trials=1, cv_num=5):
    
    if Config.TARGET_COL not in df.columns:
        raise ValueError(f"Целевая переменная '{Config.TARGET_COL}' отсутствует в DataFrame.")  
   
    X = df.drop(columns=[Config.TARGET_COL])
    y = df[Config.TARGET_COL]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=Config.TEST_SIZE, random_state=Config.SEED, stratify=y)
    
    best_pipeline, best_params = train_optuna_cv(model_class, param_space_func, X_train, y_train, n_trials=n_trials, cv_num=cv_num)
    eval_results = get_stats(best_pipeline, X_val, y_val)
    
    save_experiment(
        exp_name,
        model_class.__name__,
        best_params,
        eval_results
    )

    return eval_results