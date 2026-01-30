import mlflow
import mlflow.sklearn
import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from src.utils import load_config

def train():
    config = load_config()
    mlflow.set_experiment(config['train']['experiment_name'])
    
    with mlflow.start_run():
        # 1. Log Params
        mlflow.log_params(config['train'])
        
        # 2. Load Data
        df = pd.read_csv(config['data']['processed_path'])
        X = df[['YearsExperience']]
        y = df['Salary']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=config['data']['test_size'], random_state=config['data']['random_state']
        )
        
        # 3. Train
        model = RandomForestRegressor(
            n_estimators=config['train']['n_estimators'],
            max_depth=config['train']['max_depth'],
            random_state=42
        )
        model.fit(X_train, y_train)

        # 4. Calculate Metrics 
        mse = mean_squared_error(y_test, model.predict(X_test))
        r2 = r2_score(y_test, model.predict(X_test))
        
        # 5. Log Metrics
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("r2", r2)
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Training Complete. MSE: {mse:.2f} | R2: {r2:.4f}")

        # 6. Save Metrics to JSON for DVC (THE FIX)
        metrics = {
            "mse": mse,
            "r2": r2
        }
        with open("metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    train()