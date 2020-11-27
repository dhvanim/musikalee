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

class SpotifyResult:
    def __init__(self,ret):
        self.ret=ret
        
    def json(self): 
        return self.ret

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
        oput={
                'display_name': 'Bob',
                'images': [{'url': 'http://hello'}],
                'type': 'user'
            }
        return SpotifyResult(oput).json()
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
    
if __name__ == "__main__":
    unittest.main()
