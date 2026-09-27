from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class DataConfig:
    train_path: str
    test_path: str
    target_col: str
    drop_cols: List[str] = field(default_factory=list)
    test_size: float = 0.2


@dataclass
class ParamSpace:
    """Description of one Optuna hyperparameter."""

    type: str
    low: Optional[float] = None
    high: Optional[float] = None
    choices: Optional[List[Any]] = None
    log: bool = False


@dataclass
class ModelConfig:
    name: str
    fixed_params: Dict[str, Any] = field(default_factory=dict)
    search_space: Dict[str, ParamSpace] = field(default_factory=dict)


@dataclass
class CrossValConfig:
    n_splits: int = 2
    n_trials: int = 1
    metric: str = "ROC_AUC"


@dataclass
class TrackerConfig:
    exp_name: str = ""
    exp_dir: str = "./experiments"
    db_dir: str = "./db"


@dataclass
class TuningConfig:
    data: DataConfig
    model: ModelConfig
    cv: CrossValConfig = field(default_factory=CrossValConfig)
    tracker: TrackerConfig = field(default_factory=TrackerConfig)
    seed: int = 42
    source_config: str = ""

    @classmethod
    def from_yaml(cls, path: Path) -> "TuningConfig":
        config_path = Path(path).expanduser().resolve()
        with config_path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
        if not isinstance(raw, dict):
            raise ValueError(f"Config must be a YAML mapping: {config_path}")

        model_values = dict(raw["model"])
        model_values["search_space"] = {
            name: ParamSpace(**values)
            for name, values in model_values.get("search_space", {}).items()
        }
        config = cls(
            data=DataConfig(**raw["data"]),
            model=ModelConfig(**model_values),
            cv=CrossValConfig(**raw.get("cv", {})),
            tracker=TrackerConfig(**raw.get("tracker", {})),
            seed=raw.get("seed", 42),
            source_config=str(config_path),
        )
        return config

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable snapshot of every setting used for a run."""
        return asdict(self)

    def suggest_params(self, trial) -> dict[str, Any]:
        params = dict(self.model.fixed_params)
        for name, space in self.model.search_space.items():
            if space.type == "int":
                params[name] = trial.suggest_int(name, space.low, space.high)
            elif space.type == "float":
                params[name] = trial.suggest_float(
                    name, space.low, space.high, log=space.log
                )
            elif space.type == "cat":
                params[name] = trial.suggest_categorical(name, space.choices)
            else:
                raise ValueError(
                    f"Unsupported search-space type {space.type!r}; "
                    "expected int, float, or cat"
                )
        return params
