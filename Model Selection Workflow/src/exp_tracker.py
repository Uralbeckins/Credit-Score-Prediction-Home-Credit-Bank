import json
from pathlib import Path
from datetime import datetime


class ExperimentTracker:
    """Трекер экспериментов: сохраняет результаты и ведёт реестр лучших моделей."""

    MODEL_ALIASES = {
        "LogisticRegression": "LR",
        "RandomForestClassifier": "RF",
        "XGBClassifier": "XGB",
        "LGBMClassifier": "LGBM",
        "DecisionTreeClassifier": "DT",
        "CatBoostClassifier": "CatBoost",
    }

    def __init__(self,
                 config,
                 params: dict = {},
                 result: float = 0
                 ):
        self.experiments_dir = config.tracker.exp_dir
        self.model_name = config.model.name
        self.exp_name = config.tracker.exp_name
        self.params = params
        self.result = result

        self.exp_file = Path(self.experiments_dir + '/' + "registry.json")
        

    def load_previous_exp(self) -> dict:
        """Check if last experiment file exists"""
        if not self.exp_file.exists():
            return {}
        with open(self.exp_file, "r") as f:
            return json.load(f)

    def save_exp(self, registry: dict) -> None:
        with open(self.exp_file, "w") as f:
            json.dump(registry, f, indent=2, default=str)

    # ---------- имя файла ----------

    def make_filename(self, metric: float, now: datetime) -> str:
        alias = self.MODEL_ALIASES.get(self.model_name)
        if alias is None:
            raise ValueError(
                f"Модель '{self.model_name}' не распознана. "
                f"Добавьте её в MODEL_ALIASES."
            )
        return f"{self.exp_name}_{alias}_{metric:.4f}_{now:%H:%M}.json"

    # ---------- сохранение эксперимента ----------

    def save(self):
        now = datetime.now()
        metric_value = self.result

        # проверить, лучший ли это результат для данной модели
        prev_exp_registry = self.load_previous_exp()
        previous_best = prev_exp_registry.get('metric', 0)
        is_best = metric_value > previous_best

        record = {
            "exp_name": self.exp_name,
            "model_name": self.model_name,
            "timestamp": now.strftime("%Y-%m-%d %H:%M"),
            "params": self.params,
            "eval_result": self.result,
            "is_best": is_best,
        }

        file_path = self.experiments_dir + '/' + self.make_filename(metric_value, now)
        with open(file_path, "w") as f:
            json.dump(record, f, indent=2, default=str)