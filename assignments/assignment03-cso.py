# Retrieves the dataset for the "exchequer account (historical series)" from the CSO, and stores it into a file called "cso.json"
# Author: Carmine Giardino
import json
import requests

url_beginning = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
url_end = "/JSON-stat/2.0/en"

def download_cso_dataset(dataset_id: str, filename: str):
    with open(filename, "wt") as f:
        print(json.dumps(get_cso_dataset(dataset_id)), file= f)
        
def get_cso_dataset(dataset_id: str):
    url = url_beginning + dataset_id + url_end
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve data from CSO. Status code: {response.status_code}")

if __name__ == "__main__":
    download_cso_dataset("FIQ02", "cso.json")