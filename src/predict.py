import mlflow.sklearn
import pandas as pd
import sys
from typing import Any

def get_latest_run_id(experiment_name: str) -> str:
    """
    Finds the most recent successful run ID for a given experiment.
    Useful so you don't have to manually paste the ID.
    """
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(f"Experiment '{experiment_name}' not found.")
    
    # Search for the latest finished run
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="status = 'FINISHED'",
        order_by=["start_time DESC"],
        max_results=1
    )
    
    if runs.empty:
        raise ValueError("No successful runs found.")
    
    return runs.iloc[0].run_id

def load_model(run_id: str) -> Any:
    """Loads the Scikit-Learn model artifact from MLflow."""
    # Matches the "model" artifact path used in train.py
    model_uri = f"runs:/{run_id}/model"
    print(f"Loading model from: {model_uri}")
    return mlflow.sklearn.load_model(model_uri)

def predict(model: Any, data: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the model to the data. 
    Returns the dataframe with a new 'Predicted_Salary' column.
    """
    # Select only the features the model expects (ignoring extra cols in test.csv)
    X = data[['YearsExperience']]
    predictions = model.predict(X)
    
    # Return new dataframe with results (immutable style)
    results = data.copy()
    results['Predicted_Salary'] = predictions
    return results

def main():
    # Configuration (could also come from your src.utils.load_config)
    EXPERIMENT_NAME = "salary_prediction" # Update to match your config
    
    # 1. Setup or Manual Set
    run_id = get_latest_run_id(EXPERIMENT_NAME)
    # run_id = #############
    
    # 2. Pipeline
    # Load Data -> Load Model -> Predict
    df_test = pd.read_csv("data/raw/salary_test.csv") 
    model = load_model(run_id)
    results = predict(model, df_test)
    
    # 3. Output
    print("\n=== Inference Results ===")
    print(results)
    
    # Optional: Save to file
    results.to_csv("predictions.csv", index=False)
    print("\nSaved predictions to 'predictions.csv'")

if __name__ == "__main__":
    main()