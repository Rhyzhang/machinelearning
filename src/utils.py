import yaml
import os

def load_config(config_path="configs/default_config.yaml"):
    """Safely loads the YAML config file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
        
    with open(config_path, "r") as f:
        return yaml.safe_load(f)