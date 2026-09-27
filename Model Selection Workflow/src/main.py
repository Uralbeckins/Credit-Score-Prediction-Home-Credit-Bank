import argparse

from .config import TuningConfig
from .tuning import TuningPipeline


def main():
    parser = argparse.ArgumentParser(description="Run model hyperparameter tuning.")
    parser.add_argument("config", help="Path to the experiment YAML configuration.")
    args = parser.parse_args()

    config = TuningConfig.from_yaml(args.config)
    record = TuningPipeline(config).run_hpo()
    print(
        f"Saved {record['model_name']} experiment: "
        f"{record['metric']}={record['metric_value']:.4f} "
        f"(best={record['is_best']})"
    )


if __name__ == "__main__":
    main()
