"""
Deals with api calls to psotify from spotify_music
"""
import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests

DOTENV_PATH = join(dirname(__file__), "spotify.env")
load_dotenv(DOTENV_PATH)

SPOTIFY_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]


def gettoken_call():
    """
    Request to spotify for auth data
    """
    auth_url = "https://accounts.spotify.com/api/token"
    auth_body_params = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_ID,
        "client_secret": SPOTIFY_SECRET,
    }
    auth_response = requests.post(auth_url, data=auth_body_params)
    auth_data = auth_response.json()
    return auth_data


def spotsearch(query, query_type, access_token):
    """
    request to search spotify
    """
    header = {"Authorization": "Bearer {token}".format(token=access_token)}

    # get tracks API endpoint URL
    search_url = "https://api.spotify.com/v1/search"
    search_body_params = {"q": query, "type": query_type, "limit": 1}
    search_response = requests.get(
        search_url, headers=header, params=search_body_params
    )
    return search_response


def trendcall(access_token, search_data):
    """
    Requst fot trending
    """
    header = {"Authorization": "Bearer {token}".format(token=access_token)}
    tracks_url = search_data["playlists"]["items"][0]["tracks"]["href"]
    tracks_body_params = {"fields": "items(track(name,artists(name)))"}
    tracks_response = requests.get(
        tracks_url, headers=header, params=tracks_body_params
    )
    # if api response error
    if tracks_response.status_code != 200:
        return None
    tracks_data = tracks_response.json()
    return tracks_data


def getrecocall(artists, access_token):
    """
    API call for get_reccomended
    """
    header = {"Authorization": "Bearer {token}".format(token=access_token)}
    # get tracks API endpoint URL
    rec_url = "https://api.spotify.com/v1/recommendations"
    rec_body_params = {"seed_artists": artists, "limit": 3}
    rec_response = requests.get(rec_url, headers=header,
                                params=rec_body_params)
    # if api response error
    if rec_response.status_code != 200:
        return None
    rec_data = rec_response.json()
    return rec_data


def search_playlist(access_token, playlist_id):
    """
    Special case searching for playlist
    """
    header = {"Authorization": "Bearer {token}".format(token=access_token)}
    # get tracks API endpoint URL
    search_url = "https://api.spotify.com/v1/playlists/" + playlist_id
    search_body_params = {
        "fields": "description,external_urls,followers,images,name,owner"
    }
    search_response = requests.get(
        search_url, headers=header, params=search_body_params
    )
    # if api response error
    if search_response.status_code != 200:
        return None
    search_data = search_response.json()
    return search_data
