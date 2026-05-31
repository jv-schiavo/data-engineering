from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
#host = 'host.docker.internal'
host = 'localhost'

def get_engine():
    port = os.getenv("port","5433")

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(str(password))}@{host}:{port}/{database}")
    
    return engine

engine = get_engine()

def load_weather_data(table_name:str, df):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )

    logging.info('Data has been succesfully loaded')

    df_check = pd.read_sql(f'SELECT * FROM {table_name}', con=engine)
    logging.info(f'Total info from table: {len(df_check)}\n')

