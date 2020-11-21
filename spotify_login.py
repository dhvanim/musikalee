"""
Python Code to parse spotify requests
"""
import spotlogin_api

def get_user(auth):
    """
    Aquire A user object from Spotify using Auth Token
    """
    try:
        response = spotlogin_api.get_user_call(auth)
        unam = response["display_name"]
        try:
            pfp = response["images"][0]["url"]
        except KeyError:
            pfp = "./static/defaultPfp.png"
        utype = response["type"]
        return {"username": unam, "profile-picture": pfp, "user-type": utype}

    except Exception:
        return {"username": "", "profile-picture": "", "user-type": ""}


def get_artists(auth):
    """
    Aquire the list of favorite artists
    """
    try:
        response = spotlogin_api.get_artists_call(auth)
        uris = []
        for item in response["items"]:
            uris.append(item["uri"])
        return uris
    except Exception:
        return []


def get_top_artists(flaskid):
    """
    Aquire the name of favorite artists
    """
    try:
        response = spotlogin_api.get_top_call(flaskid)
    except Exception:
        return []

    uris = []
    try:
        for item in response["items"]:
            uris.append(item["name"])
        return uris

    except KeyError:
        return uris


def get_current_song(flaskid):
    """
    Getting what's currently being played by user
    """
    try:
        response = spotlogin_api.get_current_call(flaskid)
        if str(response) == "<Response [200]>":
            return response.json()["item"]["name"]
        return "nothing is playing"
    except Exception:
        return "nothing is playing"
