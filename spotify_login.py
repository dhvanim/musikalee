"""
Python Code to parse spotify requests
"""
import requests

def get_user(auth):
    """
    Aquire A user object from Spotify using Auth Token
    """
    url = 'https://api.spotify.com/v1/me'
    try:
        response=requests.get(url,headers={"Authorization": "Bearer "+auth})
    except TypeError:
        response=requests.get(url,headers='{"Authorization": "Bearer "+auth}')
        
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
    try:
        response = requests.get(
                            'https://api.spotify.com/v1/me/top/artists',
                            headers={
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer '+auth,
                            }
                            )
                            
    except TypeError:
        response = requests.get(
                            'https://api.spotify.com/v1/me/top/artists',
                            headers="")
    uris=[]
    for item in response.json()['items']:
        uris.append(item['uri'])
    return uris
