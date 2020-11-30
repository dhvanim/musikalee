"""
All the api parts of spotlogin_api
"""
import requests
import models
import json

def get_user_call(auth):
    """
    Calls to get the user object
    """
    url = "https://api.spotify.com/v1/me"
    response = requests.get(url, headers={"Authorization": "Bearer " + auth})
    return response.json()


def get_artists_call(auth):
    """
    Gets top Artists on Login
    """
    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + auth,
        },
    )
    return response.json()


def get_top_call(flaskid):
    """
    Gets the Names of the Top Artists
    """
    query = models.ActiveUsers.query
    auth = query.filter_by(serverid=flaskid).first().authtoken
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth,
    }
    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists", headers=headers
    )
    return response.json()


def get_current_call(flaskid):
    """
    Get Users Current Song from spotify
    """
    query = models.ActiveUsers.query
    auth = query.filter_by(serverid=flaskid).first().authtoken
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    header = {"Authorization": "Bearer " + auth}
    response = requests.get(url, headers=header)
    return response.json()

def get_artist_id(flaskid, name):
    query = models.ActiveUsers.query
    auth = query.filter_by(serverid=flaskid).first().authtoken
    url = "https://api.spotify.com/v1/search?q={}&type=artist&market=US".format(name)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth,
    }
    response = requests.get(url, headers=headers)
    return json.dumps(response.json()['artists']['items'][0]['name'], indent=2)

def get_artist_top_tracks_call(flaskid):
    """
    Get Artist's top tracks
    """
    query = models.ActiveUsers.query
    auth = query.filter_by(serverid=flaskid).first().authtoken
    name = query.filter_by(serverid=flaskid).first().user
    artistID = get_artist_id(flaskid, name)
    url = "https://api.spotify.com/v1/artists/{}/top-tracks?country=US".format(artistID)
    header = {"Authorization": "Bearer " + auth}
    response = requests.get(url, headers=header)
    return response.json()
    
def get_artist_num_listeners(flaskid):
    query = models.ActiveUsers.query
    auth = query.filter_by(serverid=flaskid).first().authtoken
    name = query.filter_by(serverid=flaskid).first().user
    artistID = get_artist_id(flaskid, name)
    url = "https://api.spotify.com/v1/artists/{}".format(artistID)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth,
    }
    response = requests.get(url, headers=headers)
    return response.json()
    
