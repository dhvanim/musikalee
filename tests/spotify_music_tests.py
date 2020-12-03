import sys
from os.path import dirname, join
import unittest
import unittest.mock as mock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import requests

sys.path.insert(1, join(dirname(__file__), "../"))
import spotify_music

# TODO : if access token fails
# tests spotify_get_access_token()
class GetAccessToken(unittest.TestCase):
    ''' tests all functions in spotify_music.py '''
    
    def mock_access_token(self):
        return "123"
    
    def mock_request_post(self, url, data):
        post_mock = mock.MagicMock()
        post_mock.json.return_value = {'access_token':'123'}
        return post_mock
        
    def test_access_token(self):
        with mock.patch("spotify_music.requests.post", self.mock_request_post):
            result = spotify_music.spotify_get_access_token()
        
        self.assertEqual(result, '123')


# tests spotify_search(query, query_type)
class Search(unittest.TestCase):

    def mock_request_get(self, url, headers, params):
        get_mock = mock.MagicMock()
        get_mock = params['type']
        return get_mock

    def test_spotify_search(self):
        with mock.patch("spotify_music.spotify_get_access_token", GetAccessToken().mock_access_token),\
        mock.patch("spotify_music.requests.get", self.mock_request_get):
            result = spotify_music.spotify_search("query", "artist")
        
        self.assertEqual(result, "artist")

 # tests spotify_get_trending()
class GetTrending(unittest.TestCase):
        
    def mock_search(self, query, query_type):
        search_mock = mock.MagicMock()
        search_mock.status_code = 200
        search_mock.json.return_value = {'playlists' : 
            {'items' : [ 
                {'tracks': {'href': 'https://open.spotify.com/playlist/37i9dQZEVXbLRQDuF5jeBp?si=DevSoVAKT5WiU7YfwFFc7A'}}]
            }}
        return search_mock
    
    def mock_get_request_get_track(self, url, headers, params):
        get_track_mock = mock.MagicMock()
        get_track_mock.status_code = 200
        get_track_mock.json.return_value = {'items' : ['Justin Beiber', 'Ariana Grande']}
        return get_track_mock

    def test_spotify_trending(self):
        with mock.patch("spotify_music.spotify_search", self.mock_search),\
        mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.requests.get', self.mock_get_request_get_track):
            result = spotify_music.spotify_get_trending()
        
        self.assertEqual(result, ['Justin Beiber', 'Ariana Grande'])
 
    
if __name__ == "__main__":
    unittest.main()