"""
All the api parts of spotlogin_api
"""
import json
from sqlalchemy import desc
import requests
import models



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


def get_top_call(username):
    """
    Gets the Names of the Top Artists
    """
    query = models.ActiveUsers.query
    auth = (
        query.filter_by(user=username)
        .order_by(desc(models.ActiveUsers.id))
        .first()
        .authtoken
    )
    print(auth)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth,
    }
    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists", headers=headers
    )
    return response.json()


def get_current_call(username):
    """
    Get Users Current Song from spotify
    """
    query = models.ActiveUsers.query
    auth = (
        query.filter_by(user=username)
        .order_by(desc(models.ActiveUsers.id))
        .first()
        .authtoken
    )
    print(auth)
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    header = {"Authorization": "Bearer " + auth}
    response = requests.get(url, headers=header)
    return response.json()


def get_artist_id(flaskid, name):
    """
    Gets the ID of an Artist
    """
    query = models.ActiveUsers.query
    auth = query.filter_by(serverid=flaskid).first().authtoken
    url = "https://api.spotify.com/v1/search?q={}&type=artist&market=US".format(name)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth,
    }
    response = requests.get(url, headers=headers)
    return json.dumps(response.json()["artists"]["items"][0]["name"], indent=2)


def get_artist_top_tracks_call(flaskid):
    """
    Get Artist's top tracks
    """
    query = models.ActiveUsers.query
    auth = query.filter_by(serverid=flaskid).first().authtoken
    name = query.filter_by(serverid=flaskid).first().user
    artist_id = get_artist_id(flaskid, name)
    url = "https://api.spotify.com/v1/artists/{}/top-tracks?country=US".format(artist_id)
    header = {"Authorization": "Bearer " + auth}
    response = requests.get(url, headers=header)
    return response.json()


def get_artist_num_listeners(flaskid):
    """
    Get the number of listeners to a track
    """
    query = models.ActiveUsers.query
    auth = query.filter_by(serverid=flaskid).first().authtoken
    name = query.filter_by(serverid=flaskid).first().user
    artist_id = get_artist_id(flaskid, name)
    url = "https://api.spotify.com/v1/artists/{}".format(artist_id)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth,
    }
    response = requests.get(url, headers=headers)
    return response.json()
