from src.extract_data import extract_data
from src.transform_data import data_transformations
from src.load_data import load_weather_data

import os
from pathlib import Path
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, 
format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
print(API_KEY)

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": "London,GB",
    "units": "metric",
    "appid": API_KEY
}
table_name = 'london_weather'

def pipeline():
    try:
        logging.info('First step: Extract')
        extract_data(url, params)

        logging.info('Second Step: Tranform')
        df = data_transformations()

        logging.info('Third Step: Load')
        load_weather_data(table_name,df)

        print('\n'+'='*60)
        print('\n Pipeline succesfully completed')
        print('='*60)

    except Exception as e:
        logging.error(f'Pipeline error: {e}')
        import traceback
        traceback.print_exc()

pipeline()
