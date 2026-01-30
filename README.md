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

# [Optional] Clean up :D
mamba clean --all

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







# How do I revert to a previous state?

### Step 1: Find the "Time Travel" Coordinates (Commit Hash)

You likely want to go back to a specific experiment you saw in MLflow.

1. Open **MLflow UI** (`http://127.0.0.1:5000`).
2. Click on the run you want to restore (e.g., the one with the best accuracy).
3. Look for the **Git Commit** field in the Tags section.
4. Copy the first 6-7 characters of that hash (e.g., `a1b2c3d`).

---

### Step 2: The Revert Process

Open your terminal in the project root.

#### 1. Revert the Code & Pointers (Git)

Switch your code, config files, and DVC pointers (`.dvc` files) back to that specific moment.

```bash
git checkout a1b2c3d

```

* **What just happened:**
* Your `src/train.py` reverted to the old version.
* Your `configs/default_config.yaml` reverted to the old parameters (e.g., `n_estimators: 10`).
* Your `dvc.lock` reverted to point to the **old** version of the dataset hash.
* *Critically:* Your `data/` folder **has not changed yet**. It still holds the new data.



#### 2. Revert the Data (DVC)

Now, tell DVC to match the physical data to the pointers you just restored.

```bash
dvc checkout

```

* **What just happened:**
* DVC read the old `dvc.lock` file.
* It looked in your local cache (`.dvc/cache`) for the old data files.
* It instantly swapped the files in `data/raw/` and `data/processed/` with the old versions.



**You are now exactly where you were when you ran that experiment.** You can run `dvc repro` and it will reproduce the *exact same results*.

---

### Advanced Scenarios

#### Scenario A: "I deleted my cache! `dvc checkout` failed!"

If you ran `git checkout` but `dvc checkout` complains that files are missing (maybe you switched computers or cleared your cache), you simply pull them from the remote storage (GDrive).

```bash
dvc pull

```

#### Scenario B: "I want the Old Data, but I want to keep my New Code"

Sometimes you don't want to revert the whole project. You just want to test your **newest algorithm** on the **oldest dataset**.

1. **Stay on your current branch** (don't `git checkout` the whole project).
2. **Checkout only the data pointer:**
```bash
# Get the .dvc file from the old commit
git checkout a1b2c3d -- data/raw.dvc

```


3. **Sync the data:**
```bash
dvc checkout data/raw.dvc

```


4. **Update the lockfile (Important):**
Since you have "New Code" + "Old Data", this is a *new state*. You must record it.
```bash
dvc repro

```






