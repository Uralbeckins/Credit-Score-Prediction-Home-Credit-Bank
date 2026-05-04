from src import train_optuna_cv
from src import get_stats
from sklearn.model_selection import train_test_split
from src import Config
from src import save_experiment, prepare_data
import joblib


def run_experiment(exp_name, model_class, param_space_func, df, n_trials=1, cv_num=5, save_model=False):
    
    X, y = prepare_data(df)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=Config.TEST_SIZE, random_state=Config.SEED, stratify=y)
    
    best_pipeline, best_params = train_optuna_cv(model_class, param_space_func, X_train, y_train, n_trials=n_trials, cv_num=cv_num)
    eval_results = get_stats(best_pipeline, X_train, y_train, X_val, y_val)
    
    save_experiment(
        exp_name,
        model_class.__name__,
        best_params,
        eval_results
    )

    if save_model:
        joblib.dump(best_pipeline, f'models/{model_class.__name__}_model.joblib')
   
    # выход потом поменяю, пока колхозинг)
    return {
        'auc_mean_cv': f'{eval_results["auc_mean_cv"]:.4f}',
        'auc_std_cv': f'{eval_results["auc_std_cv"]:.4f}',
        'brier_score': f'{eval_results["brier_score"]:.4f}'
        }