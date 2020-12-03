"""
All of the unittests that require mocking
"""
import sys
from os.path import dirname, join
import unittest
import unittest.mock as mock
from unittest.mock import patch
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
import requests

sys.path.insert(1, join(dirname(__file__), "../"))
import app

INPUT = ""
EXPECT = ""

class Post_music(unittest.TestCase):
    """
    This is the test for the function
    """
    def setUp(self):
        """
        Initialize out Test Cases
        """
        self.post_song={
            INPUT: {"song": 'Hello',"artist":"Me" },
            EXPECT: {"song": 'Hello',"artist":"Me" },
        }
        self.post_artist={
            INPUT: {"artist": 'Jim'},
            EXPECT: {"artist": 'Jim'},
        }
        self.post_album={
            INPUT: {"artist": 'Jim','album': "here they go again"},
            EXPECT: {"artist": 'Jim','album': "here they go again"},    
        }
        self.post_playlist={
            INPUT: {"playlist": 'https://helloiambob'},
            EXPECT: {"playlist": 'https://helloiambob'},
        }
    
    def mock_psong(self,song,artist):
        """
        mocks the test below
        """
        return {"song": 'Hello',"artist":"Me" }
    def test_get_post_song(self):
        """
        Test Get_post_music data when Song
        """
        with mock.patch('app.spotify_search_track',self.mock_psong):
            result = app.get_post_music_data("song",self.post_song[INPUT])
        self.assertEqual(result,self.post_song[EXPECT])
        
    def mock_partist(self,artist):
        """
        mocks the test below
        """
        return {'artist': 'Jim'}
    def test_get_post_artist(self):
        """
        Test Get_post_music data when Artist
        """
        with mock.patch('app.spotify_search_artist',self.mock_partist):
            result = app.get_post_music_data("artist",self.post_artist[INPUT])
        self.assertEqual(result,self.post_artist[EXPECT])
        
    def mock_palbum(self,album,artist):
        """
        mocks the test below
        """
        return {'album': 'here they go again', 'artist': 'Jim'}
    def test_get_post_album(self):
        """
        Test Get_post_music data when Album
        """
        with mock.patch('app.spotify_search_album',self.mock_palbum):
            result = app.get_post_music_data("album",self.post_album[INPUT])
        self.assertEqual(result,self.post_album[EXPECT])
    
    def mock_playl(self,playlist):
        """
        mocks the test below
        """
        return {'playlist': 'https://helloiambob'}
    def test_get_post_playlist(self):
        """
        Test Get_post_music data when Artist
        """
        with mock.patch('app.spotify_search_playlist',self.mock_playl):
            result = app.get_post_music_data("playlist",self.post_playlist[INPUT])
        self.assertEqual(result,self.post_playlist[EXPECT])
    
if __name__ == "__main__":
    unittest.main()
