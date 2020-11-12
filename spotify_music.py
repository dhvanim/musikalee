import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests

# set up spotify keys
dotenv_path = join(dirname(__file__), 'spotify.env')
load_dotenv(dotenv_path)

spotify_id = os.environ['SPOTIFY_CLIENT_ID']
spotify_secret = os.environ['SPOTIFY_CLIENT_SECRET']

# set up spotify auth and ges access token to make requests
def spotify_get_access_token():

    auth_url = 'https://accounts.spotify.com/api/token'
    auth_body_params = {
        'grant_type':'client_credentials',
        'client_id':spotify_id,
        'client_secret':spotify_secret,
    }
    auth_response = requests.post(auth_url, data=auth_body_params)
    auth_data = auth_response.json()

    access_token = auth_data['access_token']
    return access_token
    
# returns a dict of top 50 trending songs
def spotify_get_trending():
    
    playlist = "United States Top 50"
    
    access_token = spotify_get_access_token()
    
    header = { 'Authorization': 'Bearer {token}'.format(token=access_token) }

    # get tracks API endpoint URL
    search_url = "https://api.spotify.com/v1/search"
    search_body_params = { 'q':playlist, 'type':'playlist', 'limit':1 }
    search_response = requests.get(search_url, headers=header, params=search_body_params)

    # if api response error
    if search_response.status_code != 200:
        return None
        
    search_data = search_response.json()
    
    tracks_url = search_data['playlists']['items'][0]['tracks']['href']
    tracks_body_params = { 'fields':'items(track(name,artists(name)))'}
    tracks_response = requests.get(tracks_url, headers=header, params=tracks_body_params)
    
    # if api response error
    if tracks_response.status_code != 200:
        return None
        
    tracks_data = tracks_response.json()
    
    return tracks_data['items']
    
# returns recc songs
def spotify_get_recommended(artists):
    
    access_token = spotify_get_access_token()
    
    header = { 'Authorization': 'Bearer {token}'.format(token=access_token) }

    # get tracks API endpoint URL
    rec_url = "https://api.spotify.com/v1/recommendations"
    rec_body_params = { 'seed_artists': artists, 'limit':3 }
    rec_response = requests.get(rec_url, headers=header, params=rec_body_params)

    # if api response error
    if rec_response.status_code != 200:
        return None
        
    rec_data = rec_response.json()
    
    recs = []
    for tracks in rec_data["tracks"]:
        track = {}
        
        track["song"] = tracks["name"]
        
        artists_list = []
        for artists in tracks["artists"]:
            artists_list.append( artists["name"] )
        track["artist"] = ", ".join(artists_list)
        
        recs.append(track)
    
    return recs

def spotify_search_track(song, artist):
    
    query = "track:" + song + " artist:" + artist

    access_token = spotify_get_access_token()
    
    header = { 'Authorization': 'Bearer {token}'.format(token=access_token) }

    # get tracks API endpoint URL
    search_url = "https://api.spotify.com/v1/search"
    search_body_params = { 'q': query, 'type':'track', 'limit':1 }
    search_response = requests.get(search_url, headers=header, params=search_body_params)

    # if api response error
    if search_response.status_code != 200:
        return None
        
    search_data = search_response.json()

    track = search_data['tracks']['items'][0]['name']
    artists = []
    for a in search_data['tracks']['items'][0]['artists']:
        artists.append( a['name']) 
    album = search_data['tracks']['items'][0]['album']['name']
    preview_url = search_data['tracks']['items'][0]['preview_url']
    uri = search_data['tracks']['items'][0]['uri']
    
    return { 'song': track,
            'artist': artists,
            'album': album,
            'preview_url': preview_url,
            'uri': uri
            }