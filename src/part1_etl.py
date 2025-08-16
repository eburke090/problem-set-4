'''
PART 1: ETL the dataset and save in `data/`

Here is the imbd_movie data:
https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true

It is in JSON format, so you'll need to handle accordingly and also figure out what's the best format for the two analysis parts. 
'''

import os
import pandas as pd
import json
import requests
def etl():
    """ETL imdb movies dataset and save to /data"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    # Load datasets and save to '/data'
    url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"

    #download and read the json file
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response

    movies = []
    for line in response.text.splitlines():
        try:
            movie = json.loads(line)
            movies.append(movie)
        except Exception:
            continue

    df = pd.DataFrame(movies)

    #save csv to /data
    csv_path = os.path.join(data_dir, 'imdb_movies.csv')
    df.to_csv(csv_path, index=False)

    print(f"Dataset saved to {csv_path}")
    return csv_path