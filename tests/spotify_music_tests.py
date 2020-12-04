import sys
from os.path import dirname, join
import unittest
import unittest.mock as mock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import requests

sys.path.insert(1, join(dirname(__file__), "../"))
import spotify_music
import spotmusic_api

# TODO : if access token fails
class GetAccessToken(unittest.TestCase):
    ''' 
    tests for spotify_get_access_token
    '''
    
    def mock_access_token(self):
        return "123"
    
    def mock_request_post(self):
        return {'access_token':'123'}
        
    def test_access_token(self):
        with mock.patch("spotmusic_api.gettoken_call", self.mock_request_post):
            result = spotify_music.spotify_get_access_token()
        self.assertEqual(result, '123')


class Search(unittest.TestCase):
    
    '''
    tests for spotify_search
    '''

    def mock_request_get(self, url, headers, params):
        return "artist"

    def test_spotify_search(self):
        with mock.patch("spotify_music.spotify_get_access_token", GetAccessToken().mock_access_token),\
        mock.patch("spotify_music.spotmusic_api.spotsearch", self.mock_request_get):
            result = spotify_music.spotify_search("query", "artist")
        
        self.assertEqual(result, "artist")


class GetTrending(unittest.TestCase):
    
    '''
    tests for spotify_get_trending
    '''
    
    # mocks
    def mock_search_success(self, query, query_type):
        search_mock = mock.MagicMock()
        search_mock.status_code = 200
        search_mock.json.return_value = {'playlists' : 
            {'items' : [ 
                {'tracks': {'href': 'https://open.spotify.com/playlist/37i9dQZEVXbLRQDuF5jeBp?si=DevSoVAKT5WiU7YfwFFc7A'}}]
            }}
        return search_mock

    def mock_request_track_success(self, url, headers):
        return {'items' : ['Justin Beiber', 'Ariana Grande']}

    def mock_request_track_failure(self, url, headers):
        return None

    ## tests
    def test_trending_success(self):
        with mock.patch("spotify_music.spotify_search", self.mock_search_success),\
        mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.spotmusic_api.trendcall', self.mock_request_track_success):
            result = spotify_music.spotify_get_trending()
        
        self.assertEqual(result, ['Justin Beiber', 'Ariana Grande'])
    
    def test_trending_search_failure(self):
        with mock.patch("spotify_music.spotify_search", MockedSearch().failure),\
        mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.spotmusic_api.trendcall', self.mock_request_track_success):
            result = spotify_music.spotify_get_trending()
        
        self.assertEqual(result, None)
        
    def test_trending_tracks_failure(self):
        with mock.patch("spotify_music.spotify_search", self.mock_search_success),\
        mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.spotmusic_api.trendcall', self.mock_request_track_failure):
            result = spotify_music.spotify_get_trending()
        
        self.assertEqual(result, ["Trending","Machine","Broke"])


class GetRecommended(unittest.TestCase):
    
    '''
    tests for spotify_get_recommended
    '''
    
    def mock_request_rec_success(self, artists, token):
        return {'tracks': [{'name':'Self Control', 'artists': [{'name':'Frank Ocean'}]}]}
    
    def mock_request_rec_failure(self, artists, token):
        return None
    
    def test_recommended_success(self):
        with mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.spotmusic_api.getrecocall', self.mock_request_rec_success):
            results = spotify_music.spotify_get_recommended(['1anyVhU62p31KFi8MEzkbf', '2P5sC9cVZDToPxyomzF1UH'])
        self.assertEqual(results, [{'song':'Self Control', 'artist':'Frank Ocean'}])
  
    def test_recommended_failure(self):
        with mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
        mock.patch('spotify_music.spotmusic_api.getrecocall', self.mock_request_rec_failure):
            results = spotify_music.spotify_get_recommended([])
        self.assertEqual(results, [])


class SearchTrack(unittest.TestCase):
    
    '''
    tests for spotify_search_track
    '''
    
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


class SearchArtist(unittest.TestCase):
    
    '''
    tests for spotify_search_artist
    '''
    
    def test_artist_success(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().success):
            results = spotify_music.spotify_search_artist('Frank Ocean')
        
        self.assertDictEqual(results, {
            'artist_name':'Frank Ocean',
            'artist_icon':'httpicon',
            'external_link':'httpspotify',
        })
    
    def test_artist_search_failure(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().failure):
            results = spotify_music.spotify_search_artist('Frank Ocean')
        
        self.assertEqual(results, None)
    
    def test_artist_empty(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().empty):
            results = spotify_music.spotify_search_artist('Frank SeaLake')
        
        self.assertEqual(results, None)


class SearchAlbum(unittest.TestCase):
    
    '''
    tests for spotify_search_album
    '''
    
    def test_album_success(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().success):
            results = spotify_music.spotify_search_album('Blonde', 'Frank Ocean')
        
        self.assertDictEqual(results, {
            'artists':['Frank Ocean'],
            'album_name':'Blonde',
            'album_art':'httpimg',
            'release_date':'2016',
            'total_tracks':17,
            'external_link':'httpspotify',
        })
    
    def test_album_search_failure(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().failure):
            results = spotify_music.spotify_search_album('Blonde', 'Frank Ocean')
        
        self.assertEqual(results, None)
    
    def test_album_empty(self):
        with mock.patch('spotify_music.spotify_search', MockedSearch().empty):
            results = spotify_music.spotify_search_album('Brunette','Frank SeaLake')
        
        self.assertEqual(results, None)


class SearchPlaylist(unittest.TestCase):
    
    '''
    tests for spotify_search_playlist
    '''
    
    def mock_request_playlist_success(self, url, headers):
        return {
            'description': 'heyyyyyy :-)',
            'external_urls': { 'spotify': 'httpspotify' },
            'followers': {'total': 0},
            'images': [ {'url':'httpimg'} ],
            'name': 'Down to Earth',
            'owner': {'id':'dhvanii'},
        }
    
    def mock_request_playlist_failure(self, url, headers):
        return None
    
    def test_playlist_success(self):
        with mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
            mock.patch('spotify_music.spotmusic_api.search_playlist', self.mock_request_playlist_success):
                results = spotify_music.spotify_search_playlist('https://open.spotify.com/playlist/0Ix3TaQtxZb7cZNpFV1YKi?si=kUhWWU0lQ4SVUj8NYyYWxQ')
            
        self.assertEqual(results, {
            'playlist_name': 'Down to Earth',
            'playlist_desc': 'heyyyyyy :-)',
            'playlist_art': 'httpimg',
            'playlist_owner': 'dhvanii',
            'followers': 0,
            'external_link': 'httpspotify',
        })
    
    def test_playlist_url_failure1(self):
        with mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
            mock.patch('spotify_music.spotmusic_api.search_playlist', self.mock_request_playlist_success):
                results = spotify_music.spotify_search_playlist('https://open.spotify.com/playlist/')
                
        self.assertEqual(results, None)

    def test_playlist_url_failure2(self):
        with mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
            mock.patch('spotify_music.spotmusic_api.search_playlist', self.mock_request_playlist_success):
                results = spotify_music.spotify_search_playlist('http/')
                
        self.assertEqual(results, None)
    
    def test_playlist_search_failure(self):
        expect={
            "playlist_name": "",
            "playlist_desc": "",
            "playlist_art": "",
            "playlist_owner": "",
            "followers": "",
            "external_link": "",
        }
        with mock.patch('spotify_music.spotify_get_access_token', GetAccessToken().mock_access_token),\
            mock.patch('spotify_music.spotmusic_api.search_playlist', self.mock_request_playlist_failure):
                results = spotify_music.spotify_search_playlist('https://open.spotify.com/playlist/3544443543')
                
        self.assertEqual(results,expect)


class MockedSearch():
    
    '''
    mocks the function spotify_search
    '''
    
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
                    'total': 1,
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
        
        elif query_type == "artist":
            search_mock.json.return_value = {
                'artists': {
                    'total': 1,
                    'items': [ {
                        'name': 'Frank Ocean',
                        'images': [{'url':'httpicon'}],
                        'external_urls': {'spotify':'httpspotify'},
                    }]
                }
            }
            
        elif query_type == "album":
            search_mock.json.return_value = {
                'albums': {
                    'total': 1,
                    'items': [ {
                        'artists': [ {'name':'Frank Ocean'}],
                        'name': 'Blonde',
                        'images': [{'url':'httpimg'}],
                        'release_date': '2016',
                        'total_tracks': 17,
                        'external_urls': {'spotify':'httpspotify'},
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

    
    
if __name__ == "__main__":
    unittest.main()