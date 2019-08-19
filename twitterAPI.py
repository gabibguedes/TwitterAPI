import requests
import json
from tokens import API_TOKEN, API_TOKEN_SECRET
import base64
import urllib.parse

TOKEN = ''

def create_barear_token():
    global TOKEN
    OAUTH2_TOKEN = 'https://api.twitter.com/oauth2/token'
    consumer_key = urllib.parse.quote(API_TOKEN)
    consumer_secret = urllib.parse.quote(API_TOKEN_SECRET)
    bearer_token = consumer_key + ':' + consumer_secret
    base64_encoded_bearer_token = base64.b64encode(bearer_token.encode('utf-8'))
    headers = {
        "Authorization": "Basic " + base64_encoded_bearer_token.decode('utf-8') + "",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Content-Length": "29"}

    response = requests.post(OAUTH2_TOKEN, headers=headers, data={'grant_type': 'client_credentials'})
    to_json = response.json()
    TOKEN = to_json['access_token']


def get_user_id(username):
    header = {'authorization': 'Bearer ' + TOKEN}
    url = 'https://api.twitter.com/1.1/users/show.json?screen_name=' + username
    r = requests.get(url, headers=header)
    user = json.loads(r.text)
    print(user['name'])
    print(user['id'])


create_barear_token()
username = input('Write your username: ')
get_user_id(username)
