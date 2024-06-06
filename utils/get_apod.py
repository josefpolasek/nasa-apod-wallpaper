import requests


def get_apod(api_key):
    url = 'https://api.nasa.gov/planetary/apod'
    try:
        response = requests.get(url, params={'api_key': api_key})
        response.raise_for_status()
        data = response.json()
        return data.get("media_type"), data.get("url"), None
    except Exception as e:
        return None, None, e
