import yaml
from typing import Dict, Any, Union

class Config:

    data_path: str
    model_name: str
    search_space: Dict
    preprocessor: str
    num_studies: int

    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

        print(self.data)
