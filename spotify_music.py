import os
from os.path import join, dirname
from dotenv import load_dotenv
from urllib.parse import urlparse
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
    

def spotify_search(query, query_type):
    
    access_token = spotify_get_access_token()
    
    header = { 'Authorization': 'Bearer {token}'.format(token=access_token) }

    # get tracks API endpoint URL
    search_url = "https://api.spotify.com/v1/search"
    search_body_params = { 'q':query, 'type':query_type, 'limit':1 }
    search_response = requests.get(search_url, headers=header, params=search_body_params)

    return search_response

# returns a dict of top 50 trending songs
def spotify_get_trending():
    
    playlist = "United States Top 50"
    
    search_response = spotify_search(playlist, "playlist")
    
    # if api response error
    if search_response.status_code != 200:
        return None
        
    search_data = search_response.json()
    
    access_token = spotify_get_access_token()
    header = { 'Authorization': 'Bearer {token}'.format(token=access_token) }

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
    
    search_response = spotify_search(query, "track")

    # if api response error
    if search_response.status_code != 200:
        return None
        
    search_data = search_response.json()
    
    # if no results
    if search_data['tracks']['total'] == 0:
        return None
        
    track = search_data['tracks']['items'][0]['name']
    artists = []
    for a in search_data['tracks']['items'][0]['artists']:
        artists.append( a['name']) 
    album = search_data['tracks']['items'][0]['album']['name']
    album_art = search_data['tracks']['items'][0]['album']['images'][0]['url']
    external_link = search_data['tracks']['items'][0]['external_urls']['spotify']
    preview_url = search_data['tracks']['items'][0]['preview_url']
    
    return { 'song': track,
            'artist': artists,
            'album': album,
            'album_art': album_art,
            'external_link': external_link,
            'preview_url': preview_url,
            }

def spotify_search_artist(artist):
    
    query = "artist:" + artist
    
    search_response = spotify_search(query, "artist")

    # if api response error
    if search_response.status_code != 200:
        return None
        
    search_data = search_response.json()
    
    # if no results
    if search_data['artists']['total'] == 0:
        return None
    
    artist_name = search_data['artists']['items'][0]['name']
    artist_icon = search_data['artists']['items'][0]['images'][0]['url']
    external_link = search_data['artists']['items'][0]['external_urls']['spotify']
    
    return {
        'artist_name' : artist_name,
        'artist_icon' : artist_icon,
        'external_link' : external_link
    }

def spotify_search_album(album, artist):
    
    query = "album:" + album + " artist:" + artist
    
    search_response = spotify_search(query, "album")

    # if api response error
    if search_response.status_code != 200:
        return None
        
    search_data = search_response.json()
    
    # if no results
    if search_data['albums']['total'] == 0:
        return None
        
    artists = []
    for a in search_data['albums']['items'][0]['artists']:
        artists.append( a['name']) 
    album_name = search_data['albums']['items'][0]['name']
    album_art = search_data['albums']['items'][0]['images'][0]['url']
    release_date = search_data['albums']['items'][0]['release_date']
    total_tracks = search_data['albums']['items'][0]['total_tracks']
    external_link = search_data['albums']['items'][0]['external_urls']['spotify']
    
    return {
        "artists" : artists,
        "album_name" : album_name,
        "album_art" : album_art,
        "release_date" : release_date,
        "total_tracks" : total_tracks,
        "external_link" : external_link
    }

def spotify_search_playlist(url):
    try:
        parsed_url = urlparse(url)
        playlist_id = parsed_url.path.split('/')[2]
    except:
        return None
    
    access_token = spotify_get_access_token()
    header = { 'Authorization': 'Bearer {token}'.format(token=access_token) }

    # get tracks API endpoint URL
    search_url = "https://api.spotify.com/v1/playlists/" + playlist_id
    search_body_params = {'fields':"description,external_urls,followers,images,name,owner"}
    search_response = requests.get(search_url, headers=header, params=search_body_params)

    # if api response error
    if search_response.status_code != 200:
        return None
        
    search_data = search_response.json()
    
    playlist_desc = search_data['description']
    external_link = search_data['external_urls']['spotify']
    followers = search_data['followers']['total']
    playlist_art = search_data['images'][0]['url']
    playlist_name = search_data['name']
    playlist_owner = search_data['owner']['id']
    
    return {
        "playlist_name" : playlist_name,
        "playlist_desc" : playlist_desc,
        "playlist_art" : playlist_art,
        "playlist_owner" : playlist_owner,
        "followers" : followers,
        "external_link" : external_link
        }
