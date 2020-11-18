"""
Python Code to parse spotify requests
"""
import requests
import models


def get_user(auth):
    """
    Aquire A user object from Spotify using Auth Token
    """

    url = "https://api.spotify.com/v1/me"
    try:
        response = requests.get(url, headers={"Authorization": "Bearer " + auth})
    except TypeError:
        response = requests.get(url, headers='{"Authorization": "Bearer "+auth}')

    unam = response.json()["display_name"]

    try:
        pfp = response.json()["images"][0]["url"]
    except KeyError:
        pfp = "./static/defaultPfp.png"
    utype = response.json()["type"]
    return {"username": unam, "profile-picture": pfp, "user-type": utype}


def get_artists(auth):
    """
    Aquire the list of favorite artists
    """

    try:
        response = requests.get(
            "https://api.spotify.com/v1/me/top/artists",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + auth,
            },
        )

    except TypeError:
        response = requests.get("https://api.spotify.com/v1/me/top/artists", headers="")
    uris = []
    for item in response.json()["items"]:
        uris.append(item["uri"])
    return uris


def get_top_artists(flaskid):
    """
    Aquire the name of favorite artists
    """
    auth = models.ActiveUsers.query.filter_by(serverid=flaskid).first().authtoken
    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + auth,
        }
    except TypeError:
        headers = 'Accept": "application/json,Content-Type: application/json'\
                'Authorization: Bearer  + auth,'
    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists", headers=headers
    )
    # print(response.json())
    uris = []
    for item in response.json()["items"]:
        uris.append(item["name"])
    return uris


def get_current_song(flaskid):
    """
    Getting what's currently being played by user
    """
    auth = models.ActiveUsers.query.filter_by(serverid=flaskid).first().authtoken
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    try:
        header = {"Authorization": "Bearer " + auth}
    except TypeError:
        header = '{"Authorization": "Bearer " + auth}'
    response = requests.get(url, headers=header)

    if str(response) == "<Response [200]>":
        return response.json()["item"]["name"]
    return "nothing is playing"
