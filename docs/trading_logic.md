# Script Summary: `trading_logic.py`

## Purpose
Loads the trained models and engineered datasets, generates trading signals on the holdout test period, simulates a simple trading strategy, and saves per-company backtest results and portfolio summaries.

## Inputs
- `src/config.toml`
- `GOLD_DIR/trained_models/{company}/classification_model.pkl`
- `GOLD_DIR/trained_models/{company}/regression_model.pkl`
- `GOLD_DIR/trained_models/{company}/metadata.json`
- `GOLD_DIR/parquet/{company}_share_prices_modeled.parquet`
- `SILVER_DIR/parquet/{company}_share_prices_cleaned.parquet`

## Outputs
For each company, a subdirectory under `GOLD_DIR/backtests/` containing:
- `holdout_backtest.csv`
- `holdout_backtest_summary.json`

Also produces:
- `GOLD_DIR/backtests/all_company_backtest_summary.csv`

## Main Logic
1. Load configuration values, directories, and company list from `config.toml`.
2. Create the backtest output directory if it does not already exist.
3. For each configured company:
   - Load the saved classification model, regression model, and metadata.
   - Load both the modeled dataset and the cleaned raw price dataset.
   - Build aligned holdout test data from the most recent portion of the series.
   - Generate classification probabilities, class predictions, and regression predictions.
   - Attach raw market prices needed for execution simulation.
   - Convert predictions into trading actions (`BUY`, `SELL`, `HOLD`) and position sizes.
   - Simulate sequential order execution with cash and inventory constraints.
   - Compute summary statistics for final portfolio performance.
   - Save the detailed trade log and summary metrics.
4. Aggregate all company summaries into a combined CSV report.

## Key Dependencies
- `os`
- `json`
- `pickle`
- `tomllib`
- `pathlib`
- `polars`
- `pandas`

## Strategy Logic
- Uses both model outputs:
  - Classification predicts direction
  - Regression predicts return magnitude
- Generates actions using probability thresholds:
  - Buy when predicted upside is sufficiently confident
  - Sell when predicted downside is sufficiently confident
  - Otherwise hold
- Sizes trades based on either:
  - Predicted return magnitude, when informative
  - Prediction confidence, as a fallback
- Caps trade size with configurable minimum / maximum rules.

## Backtest Mechanics
- Runs only on the holdout portion of the data.
- Starts with a fixed cash balance of `10000.0`.
- Tracks:
  - Executed action
  - Executed trade size
  - Trade value
  - Cash balance
  - Shares held
  - Portfolio value
- Prevents buying more shares than cash allows.
- Prevents selling more shares than are currently held.

## Saved Summary Metrics
- Initial portfolio value
- Final portfolio value
- Total return
- Number of executed buys, sells, and holds
- Total shares bought and sold

## Important Notes
- Aligns the raw and modeled datasets by trimming the raw data before selecting the holdout window.
- Uses the `Close` column as the execution price by default.
- Stores company backtests in folders named from the first word of the company name.
- Produces both detailed row-level outputs and compact summary files.

## Pipeline Role
This is the post-training strategy evaluation stage of the pipeline. It converts model predictions into executable trade decisions and estimates how those decisions would have performed on unseen holdout data.

## Caveats
- Backtests only the holdout split, not the full historical series or a rolling walk-forward evaluation.
- Ignores transaction costs, slippage, spreads, taxes, and market impact.
- Uses simple long-only inventory logic with discrete share counts.
- Dataset alignment depends on a hard-coded trim (`iloc[20:-1]`), which assumes a fixed feature-window loss from earlier preprocessing.
