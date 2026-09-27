from datetime import datetime
from math import isfinite
from pathlib import Path
from typing import Any

import yaml


class ExperimentTracker:
    """Save each run and keep the best result for every model."""
    MODEL_ALIASES = {'LogisticRegression': 'LR'}

    def __init__(self, config, params: dict, result: float):
        self.config = config
        self.experiments_dir = Path(config.tracker.exp_dir)
        self.registry_file = self.experiments_dir / "registry.yaml"
        self.model_name = config.model.name
        self.model_alias = self._alias(self.model_name)
        self.exp_name = config.tracker.exp_name
        self.params = params
        self.result = float(result)
        if not isfinite(self.result):
            raise ValueError(f"Experiment metric must be finite, got {result!r}")

    @classmethod
    def _alias(cls, model_name: str) -> str:
        """Return the short alias for a model, falling back to the name itself."""
        return cls.MODEL_ALIASES.get(model_name, model_name)

    def save(self) -> dict[str, Any]:
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%m_%d_%H_%M_%S")

        # Load the registry to compare against the current best for this model.
        registry = {}
        if self.registry_file.exists():
            with self.registry_file.open("r", encoding="utf-8") as file:
                registry = yaml.safe_load(file) or {}

        previous = registry.get("models", {}).get(self.model_name)
        previous_best = previous["metric_value"] if previous else None
        is_best = previous_best is None or self.result > previous_best


        filename = f"{timestamp}_{self.model_alias}_{self.result:.4f}.yaml"
        record = {
            "exp_name": self.exp_name,
            "model_name": self.model_name,
            "timestamp": timestamp,
            "metric": self.config.cv.metric,
            "metric_value": self.result,
            "best_params": self.params,
            "config": self.config.to_dict(),
            "is_best": is_best,
        }
        with (self.experiments_dir / filename).open("w", encoding="utf-8") as file:
            yaml.safe_dump(record, file, allow_unicode=True, sort_keys=False)
        if is_best:

            registry.setdefault("models", {})[self.model_name] = {
                "metric": self.config.cv.metric,
                "metric_value": self.result,
                "timestamp": timestamp,
                "exp_file": filename,
                "best_params": self.params,
            }
            with self.registry_file.open("w", encoding="utf-8") as file:
                yaml.safe_dump(registry, file, allow_unicode=True, sort_keys=False)
        return record


