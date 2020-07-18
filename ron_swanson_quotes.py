import requests

API_URL = "https://ron-swanson-quotes.herokuapp.com/v2/quotes"


def get_swanson_quote():
    resp = requests.get(API_URL)
    if resp.status_code == 200:
        # print(resp.json()[0])
        return resp.json()[0]