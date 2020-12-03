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
from datetime import datetime
import spotify_login
import ticketmaster_api




INPUT = ""
EXPECT = ""


# for TicketmasterTest class
KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_ZIPCODE = ""
KEY_ARTIST = ""
KEY_PAGE = ""
DISPLAY_EVENTS_CHANNEL = "display_events"
EXPECTED_DATA = ""


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
        self.get_ticketmaster_event_success_params=[
            {
                KEY_INPUT: {
                        "zipcode": "07102",
                        "artist": "Justin", 
                        "page": 0
                },
                KEY_EXPECTED: {
                    DISPLAY_EVENTS_CHANNEL: "display events",
                    EXPECTED_DATA: [{
                        "name": "Justin Bieber", 
                        "url": "https://www.ticketmaster.com/justin-bieber-newark-new-jersey-07-09-2021/event/020058C5D7268823", 
                        "image": "https://s1.ticketm.net/dam/a/582/baac6105-02db-4ef3-a037-a6974d110582_1290581_TABLET_LANDSCAPE_3_2.jpg", 
                        "date": "July 09, 2021", 
                        "venue": "Prudential Center", 
                        "totalPages": 1, 
                        "currPage": 0
                    }]
                }
            }    
        ]
        
        
    # This method will be used by the mock to replace requests.get
    def mocked_search_event_response(self, url, headers={    
        "Accept": "application/json",
        "Content-Type": "application/json"}):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
    
            def json(self):
                return self.json_data
    
        
        return MockResponse({
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
        }, 200)
        

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
            
    @mock.patch('app.socketio.emit')
    def test_get_ticketmaster_events(self, mocked_socket):
        for test_case in self.get_ticketmaster_event_success_params:
            app.get_ticketmaster_events( 
                data = test_case[KEY_INPUT]
            )
            expected = test_case[KEY_EXPECTED]
            mocked_socket.assert_called_once_with( expected[DISPLAY_EVENTS_CHANNEL], expected[EXPECTED_DATA] )

class TestCommentsAndLikes(unittest.TestCase):
    
    def test_add_or_remove_like_from_db(self):
        session = UnifiedAlchemyMagicMock() 
        with mock.patch("app.DB.session", session): 
            app.add_or_remove_like_from_db("username", 0) 
            is_liked = session.query(app.models.Likes.id).filter_by(username="username", post_id=0).scalar() is not None
            session.commit()
            self.assertEqual(is_liked, True)
    
    def test_save_comment(self):
        session = UnifiedAlchemyMagicMock() 
        data = {"username":"user", "comment": "comment", "post_id": "0000"};
        with mock.patch("app.DB.session", session): #
            app.save_comment(data) 
            count = session.query(app.models.Comments).count()
            session.commit()
            self.assertEqual(count, 1)
            
    def test_update_likes_on_post(self):
        session = UnifiedAlchemyMagicMock() 
        data = {
                    "user" : {
                        "username" : "",
                        "pfp" : ""
                    },
                    "text" : "",
                    "type" : "",
                    "music" : {
                        "song" : "",
                        "artist" : "",
                        "album" : "",
                        "playlist" : ""
                    }
                }
        with mock.patch("app.DB.session", session):
            #add post to db
            app.on_post_receive(data)
            count = session.query(app.models.Posts).count()
            self.assertEqual(count, 1)
            
            #change id to be 0
            post = session.query(app.models.Posts).first() 
            post.id = 0
            session.commit()

            app.update_likes_on_post(0, 33) 
            session.commit()
            
            post = session.query(app.models.Posts).filter(app.models.Posts.id == 0)
            self.assertEqual(post.num_likes, 33)
            

class TestDatabase(unittest.TestCase):

    def test_get_username(self):
        session = UnifiedAlchemyMagicMock() 
        with mock.patch("app.DB.session", session):
            #add ActiveUser to get username of
            activeUser = app.models.ActiveUsers("user" , "flaskid", "authtoken")
            session.add(activeUser)
            session.commit()

            app.get_username("flaskid")
            user = session.query(app.models.ActiveUsers).first()
            self.assertEqual(user.user, "user")
            
    def test_query_user(self):
        session = UnifiedAlchemyMagicMock() 
        with mock.patch("app.DB.session", session):
            #add ActiveUser to get username of
            activeUser = app.models.ActiveUsers("user" , "flaskid", "authtoken")
            session.add(activeUser)
            session.commit()

            app.query_user("user")
            user = session.query(app.models.ActiveUsers).first()
            self.assertEqual(user.user, "user")

    # @mock.patch('app.socketio.emit')
    # def test_update_num_likes(self, mocked_socket):
    #     session = UnifiedAlchemyMagicMock() 
    #     with mock.patch("app.DB.session", session):
    #         app.update_num_likes({"num_likes": 13, "id": 0})
    #         expected = [{'id': 0, 'username': 'username', 'text': 'message', 'num_likes': 12, 'datetime': '06/01/2005, 00:00:00', 'pfp': 'pfp', 'isCommentsOpen': False, 'comments': [], 'is_liked': True, 'music_type': 'music_type', 'music': 'music'}]
    #         mocked_socket.assert_called_once_with( "like post channe", expected )
    
    @mock.patch('app.socketio.emit')
    def test_emit_posts(self, mocked_socket):
        session = UnifiedAlchemyMagicMock() 
        with mock.patch("app.DB.session", session):
            #add post to db
            session.add(app.models.Posts("username", "pfp", "music_type", "music", "message", 12, datetime.strptime('Jun 1 2005', '%b %d %Y')))
            session.commit()
            post = session.query(app.models.Posts).first() 
            post.id = 0
            session.commit()
            
            #add Like to db
            session.add(app.models.Likes("cat", 0))
            #add comment to db
            session.app(app.models.Comments("tom", "comment", 0, datetime.strptime('Jun 1 2005', '%b %d %Y')))
            session.commit()
            
            app.emit_posts()
            expected = [{'id': 0, 'username': 'username', 'text': 'message', 'num_likes': 12, 'datetime': '06/01/2005, 00:00:00', 'pfp': 'pfp', 'isCommentsOpen': False, 'comments': [], 'is_liked': True, 'music_type': 'music_type', 'music': 'music'}]
            mocked_socket.assert_called_once_with( "emit posts channel", expected )
if __name__ == "__main__":
    unittest.main()
