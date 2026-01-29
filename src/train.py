"""
This is slop right now. You need to modify it based on your dataset and model.
"""

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from src.utils import load_config

def train():
    config = load_config()
    
    # 1. Setup MLflow
    mlflow.set_experiment(config['train']['experiment_name'])
    
    with mlflow.start_run():
        # 2. Log Config Params
        print("Logging parameters to MLflow...")
        mlflow.log_params(config['train'])
        mlflow.log_param("data_source", config['data']['raw_path'])
        
        # 3. Load Data
        print("Loading processed data...")
        df = pd.read_csv(config['data']['processed_path'])
        
        # ASSUMPTION: The target column is named 'target'. Change this to your actual label.
        if 'target' not in df.columns:
            # Create a dummy target for the template to run if it doesn't exist
            import numpy as np
            df['target'] = np.random.rand(len(df))
            
        X = df.drop(columns=['target'])
        y = df['target']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=config['data']['test_size'],
            random_state=config['data']['random_state']
        )
        
        # 4. Train
        print(f"Training {config['train']['model_type']}...")
        model = RandomForestRegressor(
            n_estimators=config['train']['n_estimators'],
            max_depth=config['train']['max_depth']
        )
        model.fit(X_train, y_train)
        
        # 5. Evaluate
        predictions = model.predict(X_test)
        rmse = mean_squared_error(y_test, predictions, squared=False)
        print(f"Model RMSE: {rmse}")
        
        # 6. Log Metrics & Model
        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(model, "random_forest_model")
        
        print("Training Complete. Check 'mlruns' folder or run 'mlflow ui'")

if __name__ == "__main__":
    train()