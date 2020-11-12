"""
Python Code to parse spotify requests
"""
import requests

def get_user(auth):
    """
    Aquire A user object from Spotify using Auth Token
    """
    url = 'https://api.spotify.com/v1/me'
    header = {"Authorization": "Bearer "+auth}
    response=requests.get(url,headers=header)
    unam=response.json()['display_name']
    try:
        pfp= response.json()['images'][0]['url']
    except:
        pfp = "./static/defaultPfp.png"
    utype=response.json()['type']
    return{
        'username': unam,
        'profile-picture': pfp,
        'user-type': utype
    }

def get_artists(auth):
    """
    Aquire the list of favorite artists
    """
    headers = {
   'Accept': 'application/json',
   'Content-Type': 'application/json',
    'Authorization': 'Bearer '+auth,
    }
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
    # print(response.json())
    uris=[]
    for item in response.json()['items']:
        uris.append(item['uri'])
    return uris

def get_top_artists(auth):
    """
    Aquire the name of favorite artists
    """
    headers = {
   'Accept': 'application/json',
   'Content-Type': 'application/json',
    'Authorization': 'Bearer '+auth,
    }
    response = requests.get('https://api.spotify.com/v1/me/top/artists', headers=headers)
    # print(response.json())
    uris=[]
    for item in response.json()['items']:
        uris.append(item['name'])
    return uris


def get_current_song(auth):
    """
    Getting what's currently being played by user
    """
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    header = {"Authorization": "Bearer "+auth}
    response=requests.get(url,headers=header)
    
    #if str(response) == "<Response [200]>":
    return response.json()
        
    #else:
        #return "nothing is playing"
    