import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


EXPERIMENTS_DIR = Path("experiments")
REGISTRY_FILE = EXPERIMENTS_DIR / "registry.json"


def ensure_experiments_dir():
    """Создать директорию experiments если её нет."""
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)

def load_registry() -> dict:
    """Загрузить реестр экспериментов."""
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_registry(registry: dict):
    """Сохранить реестр экспериментов."""
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2, default=str)

def make_filename(exp_name: str, model_class: str, metric_str: str, now: datetime) -> str:
    
    model_names_dict = {
        "LogisticRegression": "LR",
        "RandomForestClassifier": "RF",
        "XGBClassifier": "XGB",
        "LGBMClassifier": "LGBM",
        "DecisionTreeClassifier": "DT",
        "CatBoostClassifier": "CatBoost"
    }

    if model_class in model_names_dict.keys():
        model_name = model_names_dict[model_class]
    else:
        ValueError(f"Модель '{model_class}' не распознана. Пожалуйста, добавьте её в словарь model_names_dict.")

    return f"{exp_name}_{model_name}_{metric_str}_{now.strftime('%H:%M')}.json"

def save_experiment(exp_name: str, model_class: str, params: dict, eval_results: dict):

    ensure_experiments_dir()
    
    # Определить метрику для имени файла
    metric_value = eval_results.get("auc_mean_cv", 0.0)
    now = datetime.now()
    
    # Сформировать имя файла
    
    filename = make_filename(exp_name, model_class, f'{metric_value:.4f}', now)
    file_path = EXPERIMENTS_DIR / filename
    
    # Проверить, является ли это лучшим результатом
    registry = load_registry()
    is_best = True
    
    if model_class in registry:
        existing_value = registry[model_class].get("metric_value", 0.0)
        is_best = metric_value > existing_value

    # Сохранить эксперимент
    experiment_record = {
        "exp_name": exp_name,
        "model_name": model_class,
        "params": params,
        "eval_results": eval_results,
        "timestamp": now.strftime("%Y-%m-%d %H:%M"),
        "is_best": is_best
    }
    
    with open(file_path, "w") as f:
        json.dump(experiment_record, f, indent=2, default=str)
    
    # Обновить реестр
    if is_best:
        registry[model_class] = experiment_record
        save_registry(registry)