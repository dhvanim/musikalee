"""
All of the unittests that require mocking
"""
import sys
from os.path import dirname, join
import unittest
import unittest.mock as mock
import flask_socketio
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

sys.path.insert(1, join(dirname(__file__), "../"))
import app
import spotify_login
import spotlogin_api

INPUT=""
EXPECT=""

class SpotifyLoginTest(unittest.TestCase):
    """
    This is the test for the 2 function in spotify_login.py
    """
    def setUp(self):
        """
        Initialize out Test Cases
        """
        self.user={
            INPUT: "12345",
        }
    
    def mock_nuser(self, auth):
        """
        Mocks the response of a user with pfp
        """
        oput={
                'display_name': 'Bob',
                'images': [{'url': 'http://hello'}],
                'type': 'user'
            }
        return oput

    def test_user_normal(self):
        """
        Tests a User That has a pfp
        """
        expect={
                'username': 'Bob', 
                'profile-picture': 'http://hello', 
                "user-type": 'user',
            }
        with mock.patch("spotlogin_api.get_user_call", self.mock_nuser):
            result=spotify_login.get_user(self.user[INPUT])
        self.assertEqual(result,expect)
    
    def mock_nopfp(self,auth):
        """
        Mocks the response of a user with no pfp
        """
        oput={
                'display_name': 'Bob',
                'type': 'user',
            }
        return oput
    
    def test_user_no_pfp(self):
        """
        Tests a User That has no pfp
        """
        expect={
                'username': 'Bob', 
                'profile-picture': './static/defaultPfp.png', 
                "user-type": 'user',
            }
        with mock.patch("spotlogin_api.get_user_call", self.mock_nopfp):
            result=spotify_login.get_user(self.user[INPUT])
        self.assertEqual(result,expect)
    
    def mock_artist(self,auth):
        """
        Mocks Artists Response
        """
        oput={'items':[{'uri':"1"},{'uri':"2"},{'uri':"3"}]}
        return oput
        
    def test_artist(self):
        """
        Tests a working artist link
        """
        expect=["1","2","3"]
        with mock.patch("spotlogin_api.get_artists_call", self.mock_artist):
            result=spotify_login.get_artists(self.user[INPUT])
        self.assertEqual(result,expect)
        
    def mock_key(self,auth):
        """
        Mocks KeyError
        """
        raise KeyError
        
        
    def test_artist_exception(self):
        """
        Tests a working artist link
        """
        with mock.patch("spotlogin_api.get_artists_call", self.mock_key):
            result=spotify_login.get_artists(self.user[INPUT])
        self.assertEqual(result,[])
    
    
    
if __name__ == "__main__":
    unittest.main()
