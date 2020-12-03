"""
All of the unittests that require mocking
"""
import sys
from os.path import dirname, join
import unittest
import unittest.mock as mock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import requests

sys.path.insert(1, join(dirname(__file__), "../"))
import app
import models
import spotify_login
import spotify_music
import ticketmaster_api


INPUT = ""
EXPECT = ""


# for TicketmasterTest class
KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_ZIPCODE = ""
KEY_ARTIST = ""
KEY_PAGE = ""


class SpotifyLoginTest(unittest.TestCase):
    """
    This is the test for the 2 function in spotify_login.py
    """

    def setUp(self):
        """
        Initialize out Test Cases
        """
        self.user = {
            INPUT: "12345",
        }

    def mock_nuser(self, auth):
        """
        Mocks the response of a user with pfp
        """
        oput = {
            "display_name": "Bob",
            "images": [{"url": "http://hello"}],
            "type": "user",
        }
        return oput

    def test_user_normal(self):
        """
        Tests a User That has a pfp
        """
        expect = {
            "username": "Bob",
            "profile-picture": "http://hello",
            "user-type": "user",
        }
        with mock.patch("spotlogin_api.get_user_call", self.mock_nuser):
            result = spotify_login.get_user(self.user[INPUT])
        self.assertEqual(result, expect)

    def mock_nopfp(self, auth):
        """
        Mocks the response of a user with no pfp
        """
        oput = {
            "display_name": "Bob",
            "type": "user",
        }
        return oput

    def test_user_no_pfp(self):
        """
        Tests a User That has no pfp
        """
        expect = {
            "username": "Bob",
            "profile-picture": "./static/defaultPfp.png",
            "user-type": "user",
        }
        with mock.patch("spotlogin_api.get_user_call", self.mock_nopfp):
            result = spotify_login.get_user(self.user[INPUT])
        self.assertEqual(result, expect)

    def mock_artist(self, auth):
        """
        Mocks Artists Response
        """
        oput = {
            "items": [
                {"uri": "1", "name": "Bob"},
                {"uri": "2", "name": "Jack"},
                {"uri": "3", "name": "Jill"},
            ]
        }
        return oput

    def test_artist_uri(self):
        """
        Tests a working artist link
        """
        expect = ["1", "2", "3"]
        with mock.patch("spotlogin_api.get_artists_call", self.mock_artist):
            result = spotify_login.get_artists(self.user[INPUT])
        self.assertEqual(result, expect)

    def mock_key(self, auth):
        """
        Mocks KeyError
        """
        raise KeyError

    def test_artist_uri_exception(self):
        """
        Tests a working artist link
        """
        with mock.patch("spotlogin_api.get_artists_call", self.mock_key):
            result = spotify_login.get_artists(self.user[INPUT])
        self.assertEqual(result, [])

    def test_artist_name(self):
        """
        Tests a working artist link
        """
        expect = ["Bob", "Jack", "Jill"]
        with mock.patch("spotlogin_api.get_top_call", self.mock_artist):
            result = spotify_login.get_top_artists(self.user[INPUT])
        self.assertEqual(result, expect)

    def test_artist_name_exception(self):
        """
        Tests a working artist link
        """
        with mock.patch("spotlogin_api.get_top_call", self.mock_key):
            result = spotify_login.get_top_artists(self.user[INPUT])
        self.assertEqual(result, [])

    def mock_curr_song(self, flaskid):
        """
        Tests current song
        """
        oput = {"item": {"name": "Bob sings"}}
        return oput

    def test_curr_song(self):
        """
        Tests the returning of songs playing
        """
        expect = "Bob sings"
        with mock.patch("spotlogin_api.get_current_call", self.mock_curr_song):
            result = spotify_login.get_current_song(self.user[INPUT])
        self.assertEqual(result, expect)

    def mock_no_song(self, flaskid):
        """
        Returns no song playing
        """
        return {}

    def test_no_song(self):
        """
        Tests when no song is playing
        """
        expect = "nothing is playing"
        with mock.patch("spotlogin_api.get_current_call", self.mock_no_song):
            result = spotify_login.get_current_song(self.user[INPUT])
        self.assertEqual(result, expect)

    def test_curr_song_error(self):
        """
        Tests an exception occuring
        """
        expect = "nothing is playing"
        with mock.patch("spotlogin_api.get_current_call", self.mock_key):
            result = spotify_login.get_current_song(self.user[INPUT])
        self.assertEqual(result, expect)
        

# TODO : if access token fails
class SpotifyMusicTest(unittest.TestCase):
    ''' tests all functions in spotify_music.py '''
    
    def mock_access_token(self):
        return "123"
    
    def mock_request_post(self, url, data):
        post_mock = mock.MagicMock()
        post_mock.json.return_value = {'access_token':'123'}
        return post_mock

    def mock_request_get(self, url, headers, params):
        get_mock = mock.MagicMock()
        get_mock = params['type']
        return get_mock
    
    # tests spotify_get_access_token()
    def test_access_token(self):
        with mock.patch("spotify_music.requests.post", self.mock_request_post):
            result = spotify_music.spotify_get_access_token()
        
        self.assertEqual(result, '123')
    
    # tests spotify_search(query, query_type)
    def test_spotify_search(self):
        with mock.patch("spotify_music.spotify_get_access_token", self.mock_access_token),\
        mock.patch("spotify_music.requests.get", self.mock_request_get):
            result = spotify_music.spotify_search("query", "artist")
        
        self.assertEqual(result, "artist")
    
        
        
    
    


class TicketmasterTest(unittest.TestCase):

    def setUp(self):
        self.request_ticketmaster_success_params=[
            {
                KEY_INPUT: {
                        KEY_ZIPCODE: "07201",
                        KEY_ARTIST: "Justin", 
                        KEY_PAGE: "0"
                    },
                KEY_EXPECTED: [
                    {
                        "name": "Justin Bieber", 
                        "url": "https://www.ticketmaster.com/justin-bieber-newark-new-jersey-07-09-2021/event/020058C5D7268823", 
                        "image": "https://s1.ticketm.net/dam/a/582/baac6105-02db-4ef3-a037-a6974d110582_1290581_TABLET_LANDSCAPE_3_2.jpg", 
                        "date": "July 09, 2021", 
                        "venue": "Prudential Center", 
                        "totalPages": 1, 
                        "currPage": 0
                    }
                ]
            }    
        ]
        
    def mocked_search_event_response(self, url, headers):
        r = requests.Response()
        r.status_code = 200;
        r.json = {
            "_embedded": {
                "events": [{
                    "name": "Justin Bieber",
                    "type": "event",
                    "url": "https://www.ticketmaster.com/justin-bieber-newark-new-jersey-07-09-2021/event/020058C5D7268823",
                    "images": [
                        {
                            "url": "https://s1.ticketm.net/dam/a/582/baac6105-02db-4ef3-a037-a6974d110582_1290581_TABLET_LANDSCAPE_3_2.jpg",
                        }
                    ],
                    "dates": {
                        "start": {
                            "dateTime": "2021-07-09T23:30:00Z"
                        }
                    },
                    "_embedded": {
                        "venues": [
                            {
                                "name": "Prudential Center"
                            }
                        ]
                    }
                }],
            },
            "page": {
                "size": 20,
                "totalElements": 1,
                "totalPages": 1,
                "number": 0
            }
        }
        return r
    
    def test_search_events_success(self):
        for test_case in self.request_ticketmaster_success_params:
            with mock.patch('requests.get', self.mocked_search_event_response):
                events = ticketmaster_api.search_events(
                    zipcode = test_case[KEY_INPUT][KEY_ZIPCODE],
                    artist = test_case[KEY_INPUT][KEY_ARTIST],
                    page = test_case[KEY_INPUT][KEY_PAGE]
                    )
                
                
            expected = test_case[KEY_EXPECTED]
            
            self.assertEqual(events, expected)


if __name__ == "__main__":
    unittest.main()
