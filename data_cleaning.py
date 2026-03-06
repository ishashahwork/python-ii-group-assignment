import tomllib
from pathlib import Path
import polars as pl

ETL_DIR = 'ETL'
RAW_DATA_DIR = os.path.join(ETL_DIR, 'data', 'raw')
PARQUET_DIR = os.path.join(RAW_DATA_DIR, 'parquet')

def main():
    print('\nStarting data cleaning...')

    print('\nLoading configuration...')
    try:
        config_file_path = Path("config.toml")

        with config_file_path.open("rb") as config_file:
            config = tomllib.load(config_file)

        COMPANIES = config['companies']
    except Exception as e:
        print('Failed to load configuration. Raising exception...')
        raise e
    print('Successfully loaded configuration.')

    print('\nReading parquet files...')
    try:
        companies = pl.read_parquet('ETL/data/raw/parquet/companies.parquet')
        share_prices = pl.read_parquet('ETL/data/raw/parquet/share_prices.parquet')
    except Exception as e:
        print('Failed to load parquet files. Raising exception...')
        raise e
    print('Successfully loaded parquet files.')

    print('\nFiltering down to selected companies...')
    try:
        print(f'Selected companies: {COMPANIES}')
        selected_companies = companies.filter(pl.col('Company Name').is_in(COMPANIES))
        SIMFIN_IDS = [id for id in selected_companies['SimFinId']]
        selected = share_prices.filter(pl.col('SimFinId').is_in(SIMFIN_IDS)
        print(f'Fetched {len(selected)} rows for {len(COMPANIES)} companies.')
    except Exception as e:
        print('Failed to filter dataframes. Raising exception...')
        raise e

if __name__ == '__main__':
    main()