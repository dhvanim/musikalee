"""
Python Code to parse spotify requests
"""
import spotlogin_api
import json

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



def get_top_artists(flaskid):
    """
    Aquire the name of favorite artists
    """
    uris = []
    try:
        response = spotlogin_api.get_top_call(flaskid)
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
        try:
            return response["item"]["name"]
        except KeyError:
            return "nothing is playing"
    except Exception:
        return "nothing is playing"

def get_top_tracks(flaskid):
    """
    Getting Artist's top tracks
    """
    try:
        response = spotlogin_api.get_artist_top_tracks_call(flaskid)
        topTracks = []
        
        for i in range(3):
            topTracks.append(json.dumps(response.json()['tracks'][i]['name'], indent=2))
        
        return topTracks
        
    except KeyError:
        return ["no tracks","no tracks","no tracks"]
        
def get_num_listeners(flaskid):
    try:
        response = spotlogin_api.get_artist_num_listeners(flaskid)
        return  json.dumps(response.json()['artists']['items'][0]['name'], indent=2)
    
    except Exception:
        return 0