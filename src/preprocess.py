import pandas as pd
import os
from src.utils import load_config

def preprocess():
    # Load configuration
    config = load_config()

    # 1. Load raw data
    raw_path = config['data']['raw_path']
    df = pd.read_csv(raw_path)

`   # 2. Process data
    # Example processing for Salary Prediction dataset
    df = df[df['Salary'] > 0]
    
    # 3. Save processed data
    processed_path = config['data']['processed_path']
    df.to_csv(processed_path, index=False)
    print(f"Processed data saved to {processed_path}")

if __name__ == "__main__":
    preprocess()