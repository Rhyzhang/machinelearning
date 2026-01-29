"""
This is slop right now. You need to modify it based on your dataset and preprocessing needs.
"""


import pandas as pd
import os
from src.utils import load_config

def preprocess():
    # Load configuration
    config = load_config()

    # Paths from config 
    raw_path = config['data']['raw_path']
    processed_path = config['data']['processed_path']

    # Load raw data
    # NOTE: Ensure your data/raw/dataset.csv exists
    try:
        df = pd.read_csv(raw_path)
    except FileNotFoundError:
        print(f"ERROR: File not found at {raw_path}. Please add a CSV file there.")
        return

    ########################
    # Preprocessing Logic
    #     - Add feature engineering here
    ########################
    # example: dropna
    df = df.dropna()
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)

    # Save processed data
    df.to_csv(processed_path, index=False)
    print(f"Processed data saved to {processed_path}")

if __name__ == "__main__":
    preprocess()