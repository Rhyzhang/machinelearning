# Machine Learning Project Template

This project uses **MLflow** for experiment tracking, **DVC** for data versioning, **Mamba** for environment management, and **Git** for code versioning.

## Structure Overview

```text
├── configs/               # Central YAML configuration (params, paths)
├── data/                  # Local data storage (Ignored by Git)
│   ├── raw/               # Original immutable data (Tracked by DVC)
│   └── processed/         # Cleaned data ready for training
├── notebooks/             # EDA and experimental notebooks
├── src/                   # Source code
│   ├── train.py           # Training script (logs to MLflow)
│   ├── preprocess.py      # Data cleaning script
│   └── utils.py           # Helper functions
├── dvc.yaml               # DVC Pipeline definition
├── environment.yml        # Mamba/Conda dependencies
└── setup.py               # Makes 'src' importable as a module

```

## Setup Guide

### 1. Environment Installation

Install [Mamba](https://github.com/mamba-org/mamba) first, then run:

```bash
# Create the environment
mamba env create -f environment.yml

# Activate the environment
mamba activate MLproject

# Install the local src package (Editable mode)
pip install -e .

```

### 2. DVC Initialization (Data Version Control)

Initialize DVC and set up your remote storage (Google Drive or Local).

**Option A: Google Drive**

```bash
dvc init
# Create a folder in Drive, get the ID from the URL
dvc remote add -d storage gdrive://YOUR_FOLDER_ID_HERE
git add .dvc/config
git commit -m "Setup DVC GDrive remote"

```

**Option B: Local Storage (e.g., External Hard Drive)**

```bash
dvc init
dvc remote add -d storage /path/to/external/drive/dvc_cache
git add .dvc/config
git commit -m "Setup DVC local remote"

```

---

## How to Run the Pipeline

### Step 1: Add Raw Data

1. Place your CSV file in `data/raw/dataset.csv`.
2. Track it with DVC:
```bash
dvc add data/raw/dataset.csv
git add data/raw/dataset.csv.dvc .gitignore
git commit -m "Add raw data"
dvc push  # Uploads data to configured remote

```



### Step 2: Run the Pipeline (Reproduction)

Instead of running python scripts manually, use DVC to run the pipeline defined in `dvc.yaml`. This ensures steps are only re-run if inputs change.

```bash
dvc repro

```

*This command will:*

1. Check if `configs/default_config.yaml` or `data/raw` has changed.
2. Run `src/preprocess.py`.
3. Run `src/train.py`.

### Step 3: View Results (MLflow)

To see your experiment results, metrics, and models:

```bash
mlflow ui

```

Open your browser to `http://127.0.0.1:5000`.

---

## Workflow for Changing Parameters

1. Open `configs/default_config.yaml`.
2. Change a parameter (e.g., `n_estimators: 200`).
3. Run `dvc repro`.
* *Note: DVC will realize the data hasn't changed, so it skips preprocessing and jumps straight to training.*


4. Check `mlflow ui` to compare the new run vs the old run.

## Maintenance

* **Sync Code:** `git push`
* **Sync Data:** `dvc push`
* **Clean Cache:** `dvc gc -w` (removes unused data versions from local cache)

