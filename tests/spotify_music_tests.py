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
    
    # mocks
    def mock_search_success(self, query, query_type):
        search_mock = mock.MagicMock()
        search_mock.status_code = 200
        search_mock.json.return_value = {'playlists' : 
            {'items' : [ 
                {'tracks': {'href': 'https://open.spotify.com/playlist/37i9dQZEVXbLRQDuF5jeBp?si=DevSoVAKT5WiU7YfwFFc7A'}}]
            }}
        return search_mock

    def mock_request_track_success(self, url, headers, params):
        get_track_mock = mock.MagicMock()
        get_track_mock.status_code = 200
        get_track_mock.json.return_value = {'items' : ['Justin Beiber', 'Ariana Grande']}
        return get_track_mock

    def mock_request_track_failure(self, url, headers, params):
        get_track_mock = mock.MagicMock()
        get_track_mock.status_code = 201
        return get_track_mock

    ## tests
    def test_trending_success(self):
        with mock.patch("spotify_music.spotify_search", self.mock_search_success),\
        mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.requests.get', self.mock_request_track_success):
            result = spotify_music.spotify_get_trending()
        
        self.assertEqual(result, ['Justin Beiber', 'Ariana Grande'])
    
    def test_trending_search_failure(self):
        with mock.patch("spotify_music.spotify_search", MockedSearch().failure),\
        mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.requests.get', self.mock_request_track_success):
            result = spotify_music.spotify_get_trending()
        
        self.assertEqual(result, None)
        
    def test_trending_tracks_failure(self):
        with mock.patch("spotify_music.spotify_search", self.mock_search_success),\
        mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.requests.get', self.mock_request_track_failure):
            result = spotify_music.spotify_get_trending()
        
        self.assertEqual(result, None)

# tests spotify_get_recommended(artists):
class GetRecommended(unittest.TestCase):
    
    def mock_request_rec_success(self, url, headers, params):
        rec_mock = mock.MagicMock()
        rec_mock.status_code = 200
        rec_mock.json.return_value = {'tracks': [{'name':'Self Control', 'artists': [{'name':'Frank Ocean'}]}]}
        return rec_mock
    
    def mock_request_rec_failure(self, url, headers, params):
        rec_mock = mock.MagicMock()
        rec_mock.status_code = 202
        return rec_mock
    
    def test_recommended_success(self):
        with mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.requests.get', self.mock_request_rec_success):
            results = spotify_music.spotify_get_recommended(['1anyVhU62p31KFi8MEzkbf', '2P5sC9cVZDToPxyomzF1UH'])
        
        self.assertEqual(results, [{'song':'Self Control', 'artist':'Frank Ocean'}])
  
    def test_recommended_failure(self):
        with mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.requests.get', self.mock_request_rec_failure):
            results = spotify_music.spotify_get_recommended([])
        
        self.assertEqual(results, None)

class MockedSearch():
    def failure(self, query, query_type):
        search_mock = mock.MagicMock()
        search_mock.status_code = 201
        return search_mock
    
    def success(self, query, query_type):
        search_mock = mock.MagicMock()
        search_mock.status_code = 200
        
        if query_type == "track":
            search_mock.json.return_value = {
                'tracks': {
                    'total': 3,
                    'items': [ {
                        'name': 'Self Control',
                        'artists': [ {'name':'Frank Ocean'}],
                        'album': {
                            'name': 'Blonde',
                            'images': [{'url' : 'httpimg'}],
                        },
                        'external_urls': { 'spotify': 'httpspotify' },
                        'preview_url': 'httppreview'
                    }]
                }
            }

        return search_mock
    
    def empty(self, query, query_type):
        search_mock = mock.MagicMock()
        search_mock.status_code = 200
        title = query_type+'s'
        search_mock.json.return_value = {
            title: {
                'total': 0
            }
        }
        return search_mock


class SearchTrack(unittest.TestCase):
    
    def test_track_success(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().success):
            results = spotify_music.spotify_search_track('Self Control','Frank Ocean')
        
        self.assertDictEqual(results, {
            'song':'Self Control', 
            'artist':['Frank Ocean'],
            'album':'Blonde',
            'album_art':'httpimg',
            'external_link':'httpspotify',
            'preview_url':'httppreview'
        })
    
    def test_track_search_failure(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().failure):
            results = spotify_music.spotify_search_track('Self Control','Frank Ocean')
        
        self.assertEqual(results, None)
    
    def test_track_empty(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().empty):
            results = spotify_music.spotify_search_track('asdfghjkl','Frank Ocean')
        
        self.assertEqual(results, None)
        

    
    
if __name__ == "__main__":
    unittest.main()