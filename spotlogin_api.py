"""
All the api parts of spotlogin_api
"""
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
