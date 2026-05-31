import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, 
format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json'
# '../data/weather_data.json'

columns_to_drop = ['weather', 'weather_icon', 'sys.type']

columns_to_rename = {
    'base': 'base',
    'visibility' : 'visibility',
    'dt': 'datetime',
    'timezone': 'timezone',
    'id': 'city_id',
    'cod': 'code',
    'coord.lon': 'longitude',
    'coord.lat': 'lagitude',
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds", 
    "sys.type": "sys_type",                 
    "sys.id": "sys_id",                
    "sys.country": "country",                
    "sys.sunrise": "sunrise",                
    "sys.sunset": "sunset",
}

columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_data_frame(path_name:str) -> pd.DataFrame:

    logging.info('Creating DataFrame from json')
    path = path_name

    if not path.exists():
        raise FileNotFoundError(f'File not found: {path}')

    with open (path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f'\n DataFrame created: {len(df)} lines')
    return df

def normalize_weather_columns(df:pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)
    logging.info(f'\n Column "weather" normalized - {len(df.columns)} columns')

    return df

def drop_columns(df:pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:

    logging.info(f'\n Removing columns')
    df = df.drop(columns=columns_names)

    logging.info(f'Removed columns - {len(df.columns)} remaining columns')

    return df

def rename_columns(df:pd.DataFrame, columns_names:dict[str,str]) -> pd.DataFrame:
    
    logging.info(f'\n Renaming {len(columns_names)} colomuns')
    df = df.rename(columns=columns_names)

    logging.info(f'\n Renamed columns successfully')

    return df

def normalize_datetime_columns(df:pd.DataFrame, columns_name:list[str]) -> pd.DataFrame:

    logging.info(f'Converting columns to datetime')
    for name in columns_name:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('Europe/London')

    logging.info('Conversions completed')
    return df

def data_transformations():
    print("\n Initiating transformations")

    df = create_data_frame(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_to_drop)
    df = rename_columns(df, columns_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info("Transformations completed")

    return df

