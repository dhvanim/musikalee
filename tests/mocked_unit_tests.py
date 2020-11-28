"""
All of the unittests that require mocking
"""
import sys
from os.path import dirname, join
import unittest
import unittest.mock as mock

sys.path.insert(1, join(dirname(__file__), "../"))
import app
import spotify_login

INPUT = ""
EXPECT = ""


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


if __name__ == "__main__":
    unittest.main()
