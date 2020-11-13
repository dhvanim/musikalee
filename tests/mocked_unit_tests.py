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
import spotify_login

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
        self.userchk={
            INPUT: "12345",
            EXPECT: {
                        "username": "Bob",
                        "profile-picture": "test.test.test",
                        "user-type": "user"
                        
                    }
            }
            
        self.npfp={
            INPUT: "12345",
            EXPECT: {
                        "username": "Bob",
                        "profile-picture": "./static/defaultPfp.png",
                        "user-type": "user"
                        
                    }
        }
        self.artchk={
            INPUT: "12345",
            EXPECT: ["Hello", "World"]
        }
            
    def mock_user(self,url,headers):
        """
        Mocks the output of the spotify user response
        """
        oput={
            "display_name": "Bob",
            "images": [ {"url" : "test.test.test"}],
            "type": "user"
        }
        return SpotifyResult(oput)
    
    def test_user(self):
        """
        Tests a new User
        """
        with mock.patch("requests.get", self.mock_user):
                result = spotify_login.get_user(self.userchk[INPUT])
        self.assertEqual(result, self.userchk[EXPECT])
    
    def mock_pfp(self,url,headers):
        """
        Mocks the output of the spotify user response with no pfp
        """
        oput={
            "display_name": "Bob",
            "type": "user"
        }
        return SpotifyResult(oput)
        
    def test_nopfp(self):
        """
        Test default pfp
        """
        with mock.patch("requests.get", self.mock_pfp):
                result = spotify_login.get_user(self.npfp[INPUT])
        self.assertEqual(result, self.npfp[EXPECT])
    
    def mock_artist(self,url,headers):
        """
        Mocks an Artist Response
        """
        result={
                'items': [{"uri": "Hello"},{"uri": "World"}],
                }
        return SpotifyResult(result)
        
    def test_artists(self):
        """
        Gets the top artists of user
        """
        with mock.patch("requests.get", self.mock_artist):
            result = spotify_login.get_artists(self.artchk[INPUT])
        self.assertEqual(result, self.artchk[EXPECT])
    
if __name__ == "__main__":
    unittest.main()
