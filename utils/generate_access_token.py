import requests


def generate_access_token(app_key, app_secret, refresh_token):
    token_url = 'https://api.dropbox.com/oauth2/token'
    response = requests.post(token_url, data={
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': app_key,
        'client_secret': app_secret
    })
    new_tokens = response.json()
    return new_tokens['access_token']
