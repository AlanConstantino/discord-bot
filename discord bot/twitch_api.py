import json
import requests

# For Twitch API
BASE_URL = 'https://api.twitch.tv/helix/'
CLIENT_ID = 'YOUR CLIENT ID'
HEADERS = {'Client-ID': CLIENT_ID}


# Functions for my Twitch API
def query_twitch(query):
    url = BASE_URL + query
    response = requests.get(url, headers=HEADERS)
    return response.json() # returns response as json


def get_streamer_info(streamer_list):
    streamer_info = []
    for streamer in streamer_list:
        streamer_info.append(query_twitch('streams?user_login={}'.format(streamer)))

    return streamer_info # returns array of json

def get_game_title(game_id):
    json = query_twitch('games?id={}'.format(game_id))
    game_data = json['data']
    game_title = ''
    for data in game_data:
        game_title = data['name']

    return game_title # returns a string