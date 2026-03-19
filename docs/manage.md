# Script Summary: `manage.py`

## Purpose
Acts as the command-line entrypoint for the project by orchestrating the full pipeline or running an individual stage on demand.

## Inputs
- Command-line argument: `--stage`
- Internal module imports:
  - `src.data_ingestion`
  - `src.data_cleaning`
  - `src.feature_engineering`
  - `src.model_training`
  - `src.trading_logic`

## Outputs
- No direct data artifacts of its own
- Indirectly triggers the outputs of whichever pipeline stage is executed

## Main Logic
1. Import each pipeline module.
2. Define a `main()` function that runs the entire workflow in order:
   - data ingestion
   - data cleaning
   - feature engineering
   - model training
   - trading logic
3. Define a CLI argument `--stage` with selectable pipeline stages.
4. Execute either:
   - a single requested stage, or
   - the full pipeline when `--stage all` is used.

## Key Dependencies
- `argparse`
- Internal project modules under `src/`

## Important Notes
- Serves as the operational control script for the codebase.
- Supports both full end-to-end execution and stage-specific runs.
- Enforces valid stage names through `argparse` choices.
- Centralizes the intended execution order of the pipeline.

## Pipeline Role
This is the orchestration layer of the project. It is the main script a user would run to operate the workflow and ties together the ingestion, preprocessing, feature engineering, training, and trading / backtesting stages.

## Caveats
- Contains no dependency checks between stages, so running a later stage assumes required prior outputs already exist.
- Uses direct function calls rather than a workflow framework or task scheduler.
- The imported final stage is named `trading_logic`, so the README should stay consistent with that module name even if its behavior is primarily backtesting.
- Provides only one stage argument; no support for company-level filtering, custom config paths, or partial reruns within a stage.
