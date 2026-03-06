from dotenv import load_dotenv
import os
import simfin as sf
import polars as pl

ETL_DIR = 'ETL'
RAW_DATA_DIR = os.path.join(ETL_DIR, 'data', 'raw')
PARQUET_DIR = os.path.join(RAW_DATA_DIR, 'parquet')

def main():
    print('\nStarting data ingestion...')

    print('\nLoading environment variables...')
    try:
        load_dotenv()
        sf.set_api_key(os.getenv('API_KEY'))
        sf.set_data_dir(RAW_DATA_DIR)
    except Exception as e:
        print('Failed to load environment variables. Raising exception.')
        raise e
    print('Environment variables loaded successfully.')

    print(f'\nLoading company data into {RAW_DATA_DIR}...')
    try:
        pd_companies = sf.load_companies(market='us')
        pl_companies = pl.DataFrame(pd_companies)
    except Exception as e:
        print('Failed to load company data. Raising exception.')
        raise e
    print('Successfully loaded company data.')

    print('\nLoading share prices...')
    try:
        pd_share_prices = sf.load_shareprices(market='us')
        pl_share_prices = pl.DataFrame(pd_share_prices)
    except Exception as e:
        print('Failed to load share prices. Raising exception.')
        raise e
    print('Successfully loaded share prices.')

    print(f'\nSaving to parquet at {PARQUET_DIR}...')
    try:
        share_prices_file_path = os.path.join(PARQUET_DIR, 'share_prices.parquet')
        pl_share_prices.write_parquet(share_prices_file_path)

        companies_file_path = os.path.join(PARQUET_DIR, 'companies.parquet')
        pl_companies.write_parquet(companies_file_path)
    except Exception as e:
        print('Failed to save to parquet. Raising exception.')
        raise e
    print('\nSuccessfully saved data to parquet.')
    print('\nData ingestion process finished.')

if __name__ == '__main__':
    main()