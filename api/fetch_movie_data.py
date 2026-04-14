import os
import requests
#from dotenv import load_dotenv

#load_dotenv()

DATA_URL = "http://www.omdbapi.com/"
API_KEY = os.getenv('API_KEY')


def fetch_movie_data(title):
    """"""
    params = {
        "apikey": API_KEY,
        "t": title
    }
    try:
        res = requests.get(DATA_URL, params=params)
        return res.json()
    except requests.exceptions.HTTPError:
        print('HTTP Error')
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        print('TIMEOUT Error')

