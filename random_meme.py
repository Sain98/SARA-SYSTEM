from os import path
import requests

API_URL = "https://meme-api.herokuapp.com/gimme"
folder = "saved_memes"


def get_random_meme():
    resp = requests.get(API_URL)
    filename = None

    if resp.status_code == 200:
        print(resp.json()['url'])

        r = requests.get(resp.json()['url'])
        if r.status_code == 200:
            filename = resp.json()['url'].split('/')[-1]

            if not path.exists(filename):
                with open(folder + "/" + filename, 'wb') as f:
                    f.write(r.content)
                filename = folder + "/" + filename
            else:
                print("Already exists, not downloading")

    return filename
