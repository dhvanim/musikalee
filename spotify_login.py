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
    pfp= response.json()['images'][0]['url']
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
    print(response.json())
    uris=[]
    for item in response.json()['items']:
        uris.append(item['uri'])
    return uris
