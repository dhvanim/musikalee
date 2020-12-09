"""
All of the unittests that require mocking
"""
import sys
from os.path import dirname, join
import unittest
import unittest.mock as mock
from datetime import datetime
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

sys.path.insert(1, join(dirname(__file__), "../"))
import app
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


class MockResponse:
    """
    Mocks a response for ticketmaster
    """

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """
        returns json
        """
        return self.json_data


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

    def mock_top_tracks(self, auth):
        """
        Mocks artist's top tracks
        """
        oput = {"artists": {"items": [{"name": "s1"}, {"name": "s2"}, {"name": "s3"}]}}

        # mock = MockResponse(oput, 200)
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

    def test_top_tracks(self):
        """
        Tests a User That has a pfp
        """
        expect = ["s1", "s2", "s3"]
        with mock.patch(
                "spotlogin_api.get_artist_top_tracks_call", self.mock_top_tracks
        ):
            result = spotify_login.get_top_tracks(self.user[INPUT])
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
        expect = ["Bob"]
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
        expect = ['nobody', 'nothing', 'no preview_url', './static/defaultCoverArt.png']
        with mock.patch("spotlogin_api.get_current_call", self.mock_no_song):
            result = spotify_login.get_current_song(self.user[INPUT])
        self.assertEqual(result, expect)

    def test_curr_song_error(self):
        """
        Tests an exception occuring
        """
        expect = ['nobody', 'nothing', 'no preview_url', './static/defaultCoverArt.png']
        with mock.patch("spotlogin_api.get_current_call", self.mock_key):
            result = spotify_login.get_current_song(self.user[INPUT])
        self.assertEqual(result, expect)


class TicketmasterTest(unittest.TestCase):
    """
    TestCases for Ticketmaster
    """

    def setUp(self):
        """
        Setup
        """
        self.request_ticketmaster_success_params = [
            {
                KEY_INPUT: {KEY_ZIPCODE: "07201", KEY_ARTIST: "Justin", KEY_PAGE: "0"},
                KEY_EXPECTED: [
                    {
                        "name": "Justin Bieber",
                        "url": "https://www.ticketmaster.com/justin-bieber-newark"
                               + "-new-jersey-07-09-2021/event/020058C5D7268823",
                        "image": "https://s1.ticketm.net/dam/a/582/baac6105-02db-4ef3-a037"
                                 + "-a6974d110582_1290581_TABLET_LANDSCAPE_3_2.jpg",
                        "date": "July 09, 2021",
                        "venue": "Prudential Center",
                        "totalPages": 1,
                        "currPage": 0,
                    }
                ],
            }
        ]
        self.get_ticketmaster_event_success_params = [
            {
                KEY_INPUT: {"zipcode": "07102", "artist": "Justin", "page": 0},
                KEY_EXPECTED: {
                    DISPLAY_EVENTS_CHANNEL: "display events",
                    EXPECTED_DATA: [
                        {
                            "name": "Justin Bieber",
                            "url": "https://www.ticketmaster.com/justin-bieber-newark"
                                   + "-new-jersey-07-09-2021/event/020058C5D7268823",
                            "image": "https://s1.ticketm.net/dam/a/582/baac6105-02db-4ef3-"
                                     + "a037-a6974d110582_1290581_TABLET_LANDSCAPE_3_2.jpg",
                            "date": "July 09, 2021",
                            "venue": "Prudential Center",
                            "totalPages": 1,
                            "currPage": 0,
                        }
                    ],
                },
            }
        ]

    # This method will be used by the mock to replace requests.get
    def mocked_search_event_response(
            self,
            url,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
    ):
        """
        mock search_event
        """

        return MockResponse(
            {
                "_embedded": {
                    "events": [
                        {
                            "name": "Justin Bieber",
                            "type": "event",
                            "url": "https://www.ticketmaster.com/justin-bieber-newark-"
                                   + "new-jersey-07-09-2021/event/020058C5D7268823",
                            "images": [
                                {
                                    "url": "https://s1.ticketm.net/dam/a/582/baac6105-02db-4ef"
                                           + "3-a037-a6974d110582_1290581_TABLET_LANDSCAPE_3_2.jpg",
                                }
                            ],
                            "dates": {"start": {"dateTime": "2021-07-09T23:30:00Z"}},
                            "_embedded": {"venues": [{"name": "Prudential Center"}]},
                        }
                    ],
                },
                "page": {"size": 20, "totalElements": 1, "totalPages": 1, "number": 0},
            },
            200,
        )

    def test_search_events_success(self):
        """
        test search_events()
        """
        for test_case in self.request_ticketmaster_success_params:
            with mock.patch("requests.get", self.mocked_search_event_response):
                events = ticketmaster_api.search_events(
                    zipcode=test_case[KEY_INPUT][KEY_ZIPCODE],
                    artist=test_case[KEY_INPUT][KEY_ARTIST],
                    page=test_case[KEY_INPUT][KEY_PAGE],
                )

            expected = test_case[KEY_EXPECTED]

            self.assertEqual(events, expected)

    @mock.patch("app.SOCKETIO.emit")
    def test_get_ticketmaster_events(self, mocked_socket):
        """
        test get_ticketmaster_events
        """
        for test_case in self.get_ticketmaster_event_success_params:
            app.get_ticketmaster_events(data=test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            mocked_socket.assert_called_once_with(
                expected[DISPLAY_EVENTS_CHANNEL], expected[EXPECTED_DATA]
            )


class TestCommentsAndLikes(unittest.TestCase):
    """
    Tests all things related to Comments and Likes
    """

    def test_add_or_remove_like_from_db(self):
        """
        tests adding or removing a like from Likes model
        """
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.DB.session", session):
            app.add_or_remove_like_from_db("username", 0)
            is_liked = (
                session.query(app.models.Likes.id)
                .filter_by(username="username", post_id=0)
                .scalar()
                is not None
            )
            session.commit()
            self.assertEqual(is_liked, True)

    def test_save_comment(self):
        """
        Tests saving comment to Comment model
        """
        session = UnifiedAlchemyMagicMock()
        data = {"username": "user", "comment": "comment", "postId": "0000"}
        with mock.patch("app.DB.session", session):  #
            app.save_comment(data)
            count = session.query(app.models.Comments).count()
            session.commit()
            self.assertEqual(count, 1)

    def test_update_likes_on_post(self):
        """
        test updaing likes on Post model
        """
        session = UnifiedAlchemyMagicMock()
        session.add(
            app.models.Posts(
                username="username", 
                pfp="profilepic", 
                music_type = "music_type", 
                music = {}, 
                message ="message", 
                num_likes =12, 
                datetime =datetime.now()
            )
        )
        session.commit()
         # change id to be 0
        post = session.query(app.models.Posts).first()
        post.id = 0
        session.commit()     

        post = mock.MagicMock()
        post.id = 0
        post.num_likes = 33
        session.query.return_value.filter.return_value.first.return_value  = post
        print(session.query.first)
        
        with mock.patch("app.DB.session", session):
            app.update_likes_on_post(0, 33)
            session.commit()

            expected = session.query(app.models.Posts).filter(app.models.Posts.id == 0).first()
            print(expected)
            self.assertEqual(post.num_likes, 33)


class TestDatabase(unittest.TestCase):
    """
    Tests some common Database calls
    """

    def test_get_username(self):
        """
        test get_username
        """
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.DB.session", session):
            # add ActiveUser to get username of
            active_user = app.models.ActiveUsers("user", "flaskid", "authtoken")
            session.add(active_user)
            session.commit()

            app.get_username("flaskid")
            user = session.query(app.models.ActiveUsers).first()
            self.assertEqual(user.user, "user")

    def test_query_user(self):
        """
        test query_user
        """
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.DB.session", session):
            # add ActiveUser to get username of
            active_user = app.models.ActiveUsers("user", "flaskid", "authtoken")
            session.add(active_user)
            session.commit()

            app.query_user("user")
            user = session.query(app.models.ActiveUsers).first()
            self.assertEqual(user.user, "user")

    class MockFlask:
        """
        mocks flask sid
        """

        def __init__(self):
            self.sid = "12345"

    def mock_unam(self, sid):
        """
        mocks get_user response
        """
        return "username"

    def mock_update_likes(self, post_id, num_likes):
        return 
    @mock.patch("app.SOCKETIO.emit")
    def test_update_num_likes(self, mocked_socket):
        """
        test update_num_likes emit
        """
        session = UnifiedAlchemyMagicMock()
        fflask = self.MockFlask()
        with mock.patch("app.DB.session", session):
            with mock.patch("app.flask.request", fflask):
                with mock.patch("app.get_username", self.mock_unam):
                    with mock.patch("app.update_likes_on_post", self.mock_update_likes):
                        app.update_num_likes({"num_likes": 13, "id": 0})
        expected = {"post_id": 0, "num_likes": 13, "is_liked": False}
        mocked_socket.assert_called_once_with("like post channel", expected)

    @mock.patch("app.SOCKETIO.emit")
    def test_emit_posts(self, mocked_socket):
        """
        tests emit_posts
        """
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.DB.session", session):
            # add post to db
            session.add(
                app.models.Posts(
                    "username",
                    "pfp",
                    "music_type",
                    "music",
                    "message",
                    12,
                    datetime.strptime("Jun 1 2005", "%b %d %Y"),
                )
            )
            session.commit()
            post = session.query(app.models.Posts).first()
            post.id = 0
            session.commit()

            # add Like to db
            session.add(app.models.Likes("cat", 0))
            # add comment to db
            session.app(
                app.models.Comments(
                    "tom", "comment", 0, datetime.strptime("Jun 1 2005", "%b %d %Y")
                )
            )
            session.commit()

            app.emit_posts()
            expected = [
                {
                    "id": 0,
                    "username": "username",
                    "text": "message",
                    "num_likes": 12,
                    "datetime": "06/01/2005, 00:00:00",
                    "pfp": "pfp",
                    "isCommentsOpen": False,
                    "comments": [],
                    "is_liked": True,
                    "music_type": "music_type",
                    "music": "music",
                }
            ]
            mocked_socket.assert_called_once_with("emit posts channel", expected)

    def test_emit_posts_null(self):
        """
        tests emit posts with null
        """
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.DB.session", session):
            result = app.emit_posts()
        self.assertEqual(result, None)

    class MockedUser:
        """
        mocks query_user reponse
        """

        def __init__(self, username):
            self.username = username
            self.top_artists = []

    def mock_rec(self, artists):
        """
        mocks get_recommended response
        """
        return []

    @mock.patch("app.SOCKETIO.emit")
    def test_emit_recommended(self, mocked_socket):
        """
        test emit_recommended
        """
        session = UnifiedAlchemyMagicMock()
        fflask = self.MockFlask()
        user = self.MockedUser("username")
        with mock.patch("app.flask.request", fflask):
            with mock.patch("app.get_username", self.mock_unam):
                with mock.patch("app.query_user", self.MockedUser):
                    with mock.patch("app.get_recommended", self.mock_rec):
                        app.emit_recommended()
        expected = []
        mocked_socket.assert_called_once_with(
            "recommended channel", expected, room="12345"
        )

    def spot_user(self, token):
        """
        mocks spotify_login.get_user
        """

        return {
            "username": "Bob",
            "profile-picture": "./static/defaultPfp.png",
            "user-type": "user",
        }

    def spot_artists(self, token):
        """
        mocks spotify_login.get_artists
        """
        return ["1", "2", "3"]

    def mock_nuser(self, auth):
        """
        Mocks the response of a user with pfp
        """
        oput = {
            "display_name": "Bob",
            "images": [{"url": "./static/defaultPfp.png"}],
            "type": "user",
        }
        return oput

    @mock.patch("app.SOCKETIO.emit")
    def test_on_spotlogin(self, mocked_socket):
        """
        test on_spotlogin
        """
        session = UnifiedAlchemyMagicMock()
        fflask = self.MockFlask()
        with mock.patch("app.flask.request", fflask):
            with mock.patch("app.DB.session", session):
                with mock.patch("spotlogin_api.get_user_call", self.mock_nuser):
                    with mock.patch("spotify_login.get_user", self.spot_user):
                        with mock.patch("spotify_login.get_artists", self.spot_artists):
                            with mock.patch("app.query_user", self.MockedUser):
                                app.on_spotlogin({"token": "123"})
                                expect = {
                                    "status": True,
                                    "userinfo": {
                                        "username": "Bob",
                                        "pfp": "./static/defaultPfp.png",
                                    },
                                }
                                mocked_socket.assert_called_once_with(
                                    "login success", expect, room="12345"
                                )


if __name__ == "__main__":
    unittest.main()
