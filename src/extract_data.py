import requests
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, 
format='%(asctime)s - %(levelname)s - %(message)s')



def extract_data(url:str, params:dict) -> list[dict]:
    
    response = requests.get(url,params)
    data = response.json()

    if response.status_code != 200:
        logging.error("\n Error on the request")
        return []
    
    if not data:
        logging.warning("No data")
        return []


    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info(f'File saved at: {output_path}')
    return data
