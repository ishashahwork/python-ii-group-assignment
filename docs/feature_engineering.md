# Script Summary: `feature_engineering.py`

## Purpose
Builds model-ready datasets from the cleaned company share-price files by generating technical features, interaction terms, and prediction targets, then saving the transformed outputs as parquet files.

## Inputs
- `src/config.toml`
- `SILVER_DIR/parquet/{company}_share_prices_cleaned.parquet` for each configured company

## Outputs
- `GOLD_DIR/parquet/{company}_share_prices_modeled.parquet` for each configured company

## Main Logic
1. Load directory paths and target company names from `config.toml`.
2. Create the gold-layer parquet directory if it does not already exist.
3. For each configured company:
   - Load the cleaned parquet file lazily with Polars.
   - Generate return-based, volatility, moving-average, momentum, and volume-derived features over 5-, 10-, and 20-day windows.
   - Add single-period market structure features such as intraday return, trading range, close position, market cap, and dilution / issuance.
   - Create interaction features combining returns, volatility, momentum, and volume signals.
   - Create two prediction targets:
     - `Target Return Metric` for next-period return
     - `Target Return Class` for next-period direction
   - Drop raw columns and intermediate fields that are no longer needed.
   - Remove rows with null values caused by rolling windows and shifting.
   - Save the final modeled dataset to parquet.

## Key Dependencies
- `tomllib`
- `pathlib`
- `os`
- `polars`

## Engineered Features
- Log returns
- Rolling log returns
- Rolling volatility
- Moving-average ratios
- Momentum percentage changes
- Log volume ratios and volume change
- Intraday return and range-based features
- Log market cap
- Dilution / issuance change
- Return-volume, volatility-volume, and momentum-volatility interaction terms

## Important Notes
- Uses lazy Polars execution via `scan_parquet()` and materializes results only when writing output.
- Processes each company independently.
- Uses multiple rolling windows: 5, 10, and 20 days.
- Drops raw price, volume, and some intermediate columns before saving.
- Applies `drop_nulls()` after feature generation to remove incomplete early rows.

## Pipeline Role
This is the feature engineering and target construction stage of the pipeline. It converts cleaned market data into model-ready tabular datasets used later for training predictive models and evaluating trading decisions.

## Caveats
- Assumes all required input columns exist in the cleaned parquet files.
- Introduces data loss at the start and end of each series due to rolling calculations and forward target shifts.
- The moving-average calculation appears fixed at 5 days even inside the 10- and 20-day loop, which may be intentional or a bug.
- No explicit scaling, normalization, or feature selection is performed here beyond transformations and column dropping.
