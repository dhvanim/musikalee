"""
Python Code to parse spotify requests
"""
import spotlogin_api


def get_user(auth):
    """
    Aquire A user object from Spotify using Auth Token
    """
    response = spotlogin_api.get_user_call(auth)
    unam = response["display_name"]
    try:
        pfp = response["images"][0]["url"]
    except IndexError:
        pfp = "./static/defaultPfp.png"
    except KeyError:
        pfp = "./static/defaultPfp.png"
    utype = response["type"]
    return {"username": unam, "profile-picture": pfp, "user-type": utype}


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
    except KeyError:
        return []


def get_top_artists(username):
    """
    Aquire the name of favorite artists
    """
    uris = []
    artist_pic = []
    try:
        response = spotlogin_api.get_top_call(username)
        for item in response["items"]:
            uris.append(item["name"])
            artist_pic.append(item["images"][0]["url"])
        return [uris, artist_pic]

    except KeyError:
        return uris


def get_current_song(username):
    """
    Getting what's currently being played by user
    """
    try:
        response = spotlogin_api.get_current_call(username)
        try:
            return [
                response["item"]["album"]["artists"][0]["name"],
                response["item"]["name"],
                response["item"]["preview_url"],
                response["item"]["album"]["images"][0]["url"],
            ]

        except KeyError:
            return [
                "nobody",
                "nothing",
                "no preview_url",
                "./static/defaultCoverArt.png",
            ]

    except Exception:
        return ["nobody", "nothing", "no preview_url", "./static/defaultCoverArt.png"]
