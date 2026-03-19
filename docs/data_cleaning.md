# Script Summary: `data_cleaning.py`

## Purpose
Cleans and narrows the raw market data by selecting only the configured companies, removing unneeded columns, and saving one cleaned parquet file per company for downstream processing.

## Inputs
- `src/config.toml`
- `BRONZE_DIR/parquet/companies.parquet`
- `BRONZE_DIR/parquet/share_prices.parquet`

## Outputs
- `SILVER_DIR/parquet/{company}_share_prices_cleaned.parquet` for each configured company

## Main Logic
1. Load directory paths and the target company list from `config.toml`.
2. Create the silver-layer parquet directory if it does not already exist.
3. Read the raw companies and share-price parquet files.
4. For each configured company:
   - Find its corresponding `SimFinId` from the companies dataset.
   - Filter share-price rows to that company only.
5. Drop the `Dividend` and `SimFinId` columns from each filtered dataset.
6. Save one cleaned parquet file per company.

## Key Dependencies
- `tomllib`
- `pathlib`
- `os`
- `polars`

## Important Notes
- Uses a `main()` entrypoint and runs as a standalone script.
- Depends on a `companies` list being defined in `config.toml`.
- Stores filtered company data in an in-memory dictionary keyed by company name.
- Uses company names to resolve `SimFinId` before filtering share prices.

## Pipeline Role
This is the cleaning and selection step after raw ingestion. It transforms the broad raw dataset into smaller company-specific parquet files that are easier to use in feature engineering and modeling.

## Caveats
- Assumes every configured company exists exactly once in the companies dataset.
- Assumes company names are spelled exactly as they appear in the source data.
- Performs only basic cleaning; it mainly filters and removes columns rather than handling nulls, outliers, or date issues.
- Writes separate files per company, which simplifies downstream access but may fragment the dataset.
