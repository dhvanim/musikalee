"""
All of the unittests that require mocking
"""
import sys
from os.path import dirname, join
import unittest
import unittest.mock as mock
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

sys.path.insert(1, join(dirname(__file__), "../"))
import app

INPUT = ""
EXPECTED = ""


class UserType:
    """
    Mocks UserType
    """

    def __init__(self):
        self.user_type = "user"


class MockFlask:
    """
    Mocks Flask
    """

    def __init__(self):
        """
        Get Sid
        """
        self.sid = "12345"


class MockedUser:
    """
    mocks query_user reponse
    """

    def __init__(self, username):
        self.username = username
        self.top_artists = []
        self.user_type = "user"


class MockedArtist:
    """
    mocks query_user reponse
    """

    def __init__(self, username):
        self.username = username
        self.top_artists = []
        self.user_type = "artist"


class GetFollowerData(unittest.TestCase):
    """
    Tests the send_user_profile function:

    """

    def setUp(self):
        self.user = {
            "followers": ["Cat", "Dhvani", "Justin"],
            "is_following": True,
            EXPECTED: {"followers": ["Cat", "Dhvani", "Justin"], "isFollowing": True},
        }

    def mock_get_username(self, user):
        """
        mocks results of get_username
        """
        return "aUsername"

    def mock_follower_update_db(self, user):
        """
        mocks results of follower_update_db
        """
        return [["Cat", "Dhvani", "Justin"], True]

    @mock.patch("app.SOCKETIO.emit")
    def test_recieve_follower_data(self, mocked_socket):
        """
        tests send_user_profile
        """
        fflask = MockFlask()
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.flask.request", fflask):
            with mock.patch("app.DB.session", session):
                with mock.patch("app.get_username", self.mock_get_username):
                    with mock.patch(
                            "app.follower_update_db", self.mock_follower_update_db
                    ):
                        app.update_follower_info()
        mocked_socket.assert_called_once_with("emit follower data", self.user[EXPECTED])


class GetUserProfile(unittest.TestCase):
    """
    Tests the send_user_profile function:

    """

    def setUp(self):
        self.user = {
            INPUT: True,
            EXPECTED: {
                "username": "aUsername",
                "profileType": "user",
                "topArtists": ["Singer 1", "Singer 2", "Singer 3"],
                "artistPics": [],
                "following": ["Cat", "Dhvani", "Justin"],
                "currentSong": "A song",
            },
        }

    def mock_get_top_art(self, user):
        """
        mocks results of get_top_artists
        """
        return [["Singer 1", "Singer 2", "Singer 3"], ["1,2,3"]]

    def mock_get_curr_song(self, user):
        """
        mocks results of get_current_song
        """
        return "A song"

    def mock_get_foll(self, user):
        """
        mocks result of get followers
        """
        return ["Cat", "Dhvani", "Justin"]

    def mock_username(self, sid):
        """
        mocks the result of username
        """
        return "aUsername"

    def mock_get_top_tracks(self, user):
        """
        mocks results of get_top_tracks
        """
        return ["Track 1", "Track 2", "Track 3"]

    def mock_get_num_listeners(self, user):
        """
        mocks results of get_num_listeners
        """
        return 12345

    @mock.patch("app.SOCKETIO.emit")
    def test_send_user_data_as_user(self, mocked_socket):
        """
        tests send_user_profile as a user
        """
        fflask = MockFlask()
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.flask.request", fflask):
            with mock.patch("app.DB.session", session):
                with mock.patch("app.get_username", self.mock_username):
                    with mock.patch("app.get_top_artists", self.mock_get_top_art):
                        with mock.patch(
                                "app.get_current_song", self.mock_get_curr_song
                        ):
                            with mock.patch("app.query_user", MockedUser):
                                with mock.patch(
                                        "app.get_followers_db", self.mock_get_foll
                                ):
                                    app.send_user_profile(True)
        mocked_socket.assert_called_once_with("emit user data", self.user[EXPECTED])


class FollowerUpdate(unittest.TestCase):
    """
    Class for testing all things followers related
    """
    def test_get_followers_db(self):
        """
        Tests getting followers given a user
        """
        session = UnifiedAlchemyMagicMock()
        data = "username"
        session.add(
            app.models.Users(
                "username", "profilepic", "user", [], ["follow1", "follow2"], []
            )
        )
        session.scalar.return_value = ["follow1", "follow2"]
        session.commit()
        with mock.patch("app.DB.session", session):  #
            app_result = app.get_followers_db(data)
            followers_result = ["follow1", "follow2"]
            self.assertEqual(followers_result, app_result)

    def test_follower_update_db(self):
        """
        Tests updating followers
        """
        session = UnifiedAlchemyMagicMock()
        data = "follow3"
        session.add(
            app.models.Users(
                "username", "profilepic", "user", [], ["follow1", "follow2"], []
            )
        )
        session.scalar.return_value = ["follow1", "follow2"]
        session.commit()
        with mock.patch("app.DB.session", session):  #
            app_result = app.follower_update_db(data)
            followers_result = [["follow1", "follow2", "follow3"], True]
            self.assertEqual(followers_result, app_result)

    def test_follower_update_db2(self):
        """
        Tests updating followers
        """
        session = UnifiedAlchemyMagicMock()
        data = "follow3"
        session.add(
            app.models.Users(
                "username",
                "profilepic",
                "user",
                [],
                ["follow1", "follow2", "follow3"],
                [],
            )
        )
        session.scalar.return_value = ["follow1", "follow2", "follow3"]
        session.commit()
        with mock.patch("app.DB.session", session):  #
            app_result = app.follower_update_db(data)
            followers_result = [["follow1", "follow2"], False]
            self.assertEqual(followers_result, app_result)
