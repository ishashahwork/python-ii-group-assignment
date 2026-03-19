# Script Summary: `model_training.py`

## Purpose
Trains, tunes, evaluates, and saves both classification and regression XGBoost models for each configured company using the engineered feature datasets.

## Inputs
- `src/config.toml`
- `GOLD_DIR/parquet/{company}_share_prices_modeled.parquet` for each configured company

## Outputs
For each company, a subdirectory under `GOLD_DIR/trained_models/` containing:
- `classification_model.pkl`
- `regression_model.pkl`
- `metadata.json`

## Main Logic
1. Load configuration values and company list from `config.toml`.
2. Create the trained-model output directory if it does not already exist.
3. For each configured company:
   - Load the modeled parquet dataset.
   - Split columns into input features and two targets:
     - `Target Return Class`
     - `Target Return Metric`
   - Perform a chronological train / test split.
   - Build a time-series cross-validation scheme with `TimeSeriesSplit`.
   - Train and tune an `XGBClassifier` with randomized hyperparameter search using ROC AUC scoring.
   - Train and tune an `XGBRegressor` with randomized hyperparameter search using negative MSE scoring.
   - Evaluate both models on the holdout test set.
   - Save the trained models and metadata to disk.
4. Print per-company summary metrics to the console.

## Key Dependencies
- `os`
- `json`
- `pickle`
- `tomllib`
- `pathlib`
- `polars`
- `xgboost`
- `scikit-learn`

## Modeling Details
- Uses two separate supervised learning tasks:
  - Binary classification for next-period return direction
  - Regression for next-period return magnitude
- Uses a fixed chronological holdout split with a default 20% test fraction.
- Uses `TimeSeriesSplit` instead of random cross-validation to preserve temporal ordering.
- Runs `RandomizedSearchCV` with 40 sampled hyperparameter combinations for each model.
- Tunes parameters such as tree depth, learning rate, subsampling, regularization, and number of estimators.

## Saved Metadata
Each company’s `metadata.json` includes:
- Company name
- Feature column list
- Target names
- Classification metrics and best parameters
- Regression metrics and best parameters

## Important Notes
- Converts Polars data to pandas before model training.
- Casts the classification target to integer and the regression target to float.
- Creates one classifier and one regressor per company rather than one global model.
- Saves company outputs in folders named from the first word of the company name.

## Pipeline Role
This is the model training and evaluation stage of the pipeline. It consumes the engineered gold-layer datasets and produces the fitted models and performance metadata needed for later strategy logic or analysis.

## Caveats
- Assumes the modeled datasets are clean and contain all required feature and target columns.
- Uses only a single final holdout split, so performance may be sensitive to the most recent segment of the data.
- Saving outputs under the first word of the company name could cause naming collisions for similarly named companies.
- No explicit probability calibration, feature importance export, or model comparison beyond XGBoost is included.
