from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, List, Dict
import yaml
from dacite import from_dict
from sklearn.linear_model import LogisticRegression


@dataclass
class Data:
    train_path: str
    test_path: str
    target_col: str
    drop_cols: List[str] = field(default_factory=list)
    test_size: float = 0.2


@dataclass
class Param:
    """Описание одного гиперпараметра для Optuna."""
    type: str 
    low: Optional[float] = None
    high: Optional[float] = None
    choices: Optional[List[Any]] = None
    log: bool = False

@dataclass
class Model:
    name: str
    fixed_params: Dict[str, Any] = field(default_factory=dict)
    search_space: Dict[str, Param] = field(default_factory=dict)


@dataclass
class CrossVal:
    cv_num: int = 5
    n_trials: int = 50


@dataclass
class Config:
    data: Data
    model: Model
    cv: CrossVal

    @classmethod
    def load_cfg(cls, path: Path):
        path = Path(path)
        with path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
            print(raw)
        return from_dict(data_class=Config, data=raw)

    def get_model(self):
        if self.model.name == 'LogisticRegression':
            return LogisticRegression
        else:
            raise TypeError('Неизвестный тип модели')

    def get_param_space(self, trial):
        p = dict(self.model.fixed_params)
        for k, s in self.model.search_space.items():
            if s.type == "int":
                p[k] = trial.suggest_int(k, s.low, s.high)
            elif s.type == "float":
                p[k] = trial.suggest_float(k, s.low, s.high, log=s.log)
            elif s.type == "cat":
                p[k] = trial.suggest_categorical(k, s.choices)
            else:
                raise ValueError('Несуществующий тип fixed_param (int, float, cat)')
        return p

