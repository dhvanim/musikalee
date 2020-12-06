"""
Music part of spotify parsing
"""
from urllib.parse import urlparse
import spotmusic_api


def spotify_get_access_token():
    """
    Gets the spotify access token
    """
    auth_data = spotmusic_api.gettoken_call()
    access_token = auth_data["access_token"]
    return access_token


def spotify_search(query, query_type):
    """
    Searches spotify using access token
    """
    access_token = spotify_get_access_token()
    return spotmusic_api.spotsearch(query, query_type, access_token)


# returns a dict of top 50 trending songs
def spotify_get_trending():
    """
    Gets the trending music
    """
    playlist = "United States Top 50"
    search_response = spotify_search(playlist, "playlist")
    # if api response error
    if search_response.status_code != 200:
        return None
    search_data = search_response.json()
    access_token = spotify_get_access_token()
    tracks_data = spotmusic_api.trendcall(access_token, search_data)
    if tracks_data is not None:
        return tracks_data["items"]
    return ["Trending", "Machine", "Broke"]


# returns recc songs
def spotify_get_recommended(artists):
    """
    Parses data from spotify api
    """
    access_token = spotify_get_access_token()
    rec_data = spotmusic_api.getrecocall(artists, access_token)
    recs = []
    if rec_data is None:
        return recs
    for tracks in rec_data["tracks"]:
        track = {}
        track["song"] = tracks["name"]
        artists_list = []
        for item in tracks["artists"]:
            artists_list.append(item["name"])
        track["artist"] = ", ".join(artists_list)
        recs.append(track)
    return recs


def spotify_search_track(song, artist):
    """
    Parses spotify search for a track
    """
    query = "track:" + song + " artist:" + artist
    search_response = spotify_search(query, "track")
    # if api response error
    if search_response.status_code != 200:
        return None
    search_data = search_response.json()
    # if no results
    if search_data["tracks"]["total"] == 0:
        return None
    track = search_data["tracks"]["items"][0]["name"]
    artists = []
    for item in search_data["tracks"]["items"][0]["artists"]:
        artists.append(item["name"])
    t_o = search_data["tracks"]["items"][0]
    album = t_o["album"]["name"]
    album_art = t_o["album"]["images"][0]["url"]
    external_link = t_o["external_urls"]["spotify"]
    preview_url = t_o["preview_url"]
    return {
        "song": track,
        "artist": artists,
        "album": album,
        "album_art": album_art,
        "external_link": external_link,
        "preview_url": preview_url,
    }


def spotify_search_artist(artist):
    """
    Searches for an artist spotify
    """
    query = "artist:" + artist
    search_response = spotify_search(query, "artist")
    # if api response error
    if search_response.status_code != 200:
        return None
    search_data = search_response.json()
    # if no results
    if search_data["artists"]["total"] == 0:
        return None
    ai_o = search_data["artists"]["items"][0]
    artist_name = ai_o["name"]
    artist_icon = ai_o["images"][0]["url"]
    external_link = ai_o["external_urls"]["spotify"]
    return {
        "artist_name": artist_name,
        "artist_icon": artist_icon,
        "external_link": external_link,
    }


def spotify_search_album(album, artist):
    """
    Parses a search for an album
    """
    query = "album:" + album + " artist:" + artist
    search_response = spotify_search(query, "album")
    # if api response error
    if search_response.status_code != 200:
        return None
    search_data = search_response.json()
    # if no results
    if search_data["albums"]["total"] == 0:
        return None
    artists = []
    al_o = search_data["albums"]["items"][0]
    for item in al_o["artists"]:
        artists.append(item["name"])
    album_name = al_o["name"]
    album_art = al_o["images"][0]["url"]
    release_date = al_o["release_date"]
    total_tracks = al_o["total_tracks"]
    external_link = al_o["external_urls"]["spotify"]
    return {
        "artists": artists,
        "album_name": album_name,
        "album_art": album_art,
        "release_date": release_date,
        "total_tracks": total_tracks,
        "external_link": external_link,
    }


def spotify_search_playlist(url):
    """
    Searches for a playlist
    """
    try:
        parsed_url = urlparse(url)
        playlist_id = parsed_url.path.split("/")[2]
        if len(playlist_id) == 0:
            return None
    except:
        return None
    access_token = spotify_get_access_token()
    search_data = spotmusic_api.search_playlist(access_token, playlist_id)
    if search_data is None:
        return {
            "playlist_name": "",
            "playlist_desc": "",
            "playlist_art": "",
            "playlist_owner": "",
            "followers": "",
            "external_link": "",
        }
    playlist_desc = search_data["description"]
    external_link = search_data["external_urls"]["spotify"]
    followers = search_data["followers"]["total"]
    playlist_art = search_data["images"][0]["url"]
    playlist_name = search_data["name"]
    playlist_owner = search_data["owner"]["id"]
    return {
        "playlist_name": playlist_name,
        "playlist_desc": playlist_desc,
        "playlist_art": playlist_art,
        "playlist_owner": playlist_owner,
        "followers": followers,
        "external_link": external_link,
    }
