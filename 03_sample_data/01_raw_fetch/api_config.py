import requests
import json
from datetime import datetime
from pathlib import Path

BASE_URL  = 'https://dummyjson.com/'
end_point = "https://dummyjson.com/products"
HEADERS = {"Accept":"application/json"}
TIMEOUT = 20

def fetch_data(url):
    try:
        res = requests.get(
                        url,
                        headers=HEADERS,
                        timeout=TIMEOUT
                        
        )
        res.raise_for_status() 
        return res
    except requests.exceptions.HTTPError as err:
        print('HTTP Error Occured',err)
        return None
    except requests.exceptions.Timeout as err:
        print('Request timeout error ',err)
        return None
    except requests.RequestException as err:
        print('Exceptions returned',err)
        return None


def parse_data(obj):
    try:
        dict_data = obj.json()
        return dict_data    
        
    except json.JSONDecodeError as err:
        print('Parsing error',err)
        return None

def save_data(d,file_prefix):
    try:
        file_name = f"{file_prefix}_{datetime.today():%Y-%m-%d}.json"
        path = Path("03_sample_data") / "01_raw_fetch" / "raw_data"
        
        path.mkdir(parents=True, exist_ok=True)
        full_path = path / file_name
        
        with full_path.open(
                'w',
                encoding='utf-8'
        ) as pfile:
            json.dump(d,pfile,ensure_ascii=False,indent=4)
            return full_path
        
    except TypeError as err:
        print('Argument pass error occured',err)
        return None    
    except FileNotFoundError as err:
        print('File path not found',err)
        return None
    except PermissionError as err:
        print("Permission denied:", err)
        return None

    except OSError as err:
        print("File-writing error:", err)
        return None
    

data = fetch_data(end_point)

# now call the functions for successful API request
if data is not None:
    data_received = parse_data(data)
    if data_received is not None:
        json_data = save_data(data_received,'products')
        if json_data is not None:
            print(f'json file created successfully: {json_data}')



    



