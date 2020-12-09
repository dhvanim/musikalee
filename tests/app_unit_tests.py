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
EXPECT = ""


class MockFlask:
    """
    Mocks Flask
    """
    def __init__(self):
        """
        Get Sid
        """
        self.sid = "12345"


class PostMusic(unittest.TestCase):
    """
    This is the test for the function
    """

    def setUp(self):
        """
        Initialize out Test Cases
        """
        self.post_song = {
            INPUT: {"song": "Hello", "artist": "Me"},
            EXPECT: {"song": "Hello", "artist": "Me"},
        }
        self.post_artist = {
            INPUT: {"artist": "Jim"},
            EXPECT: {"artist": "Jim"},
        }
        self.post_album = {
            INPUT: {"artist": "Jim", "album": "here they go again"},
            EXPECT: {"artist": "Jim", "album": "here they go again"},
        }
        self.post_playlist = {
            INPUT: {"playlist": "https://helloiambob"},
            EXPECT: {"playlist": "https://helloiambob"},
        }

    def mock_psong(self, song, artist):
        """
        mocks the test below
        """
        return {"song": "Hello", "artist": "Me"}

    def test_get_post_song(self):
        """
        Test Get_post_music data when Song
        """
        with mock.patch("app.spotify_search_track", self.mock_psong):
            result = app.get_post_music_data("song", self.post_song[INPUT])
        self.assertEqual(result, self.post_song[EXPECT])

    def mock_partist(self, artist):
        """
        mocks the test below
        """
        return {"artist": "Jim"}

    def test_get_post_artist(self):
        """
        Test Get_post_music data when Artist
        """
        with mock.patch("app.spotify_search_artist", self.mock_partist):
            result = app.get_post_music_data("artist", self.post_artist[INPUT])
        self.assertEqual(result, self.post_artist[EXPECT])

    def mock_palbum(self, album, artist):
        """
        mocks the test below
        """
        return {"album": "here they go again", "artist": "Jim"}

    def test_get_post_album(self):
        """
        Test Get_post_music data when Album
        """
        with mock.patch("app.spotify_search_album", self.mock_palbum):
            result = app.get_post_music_data("album", self.post_album[INPUT])
        self.assertEqual(result, self.post_album[EXPECT])

    def mock_playl(self, playlist):
        """
        mocks the test below
        """
        return {"playlist": "https://helloiambob"}

    def test_get_post_playlist(self):
        """
        Test Get_post_music data when Artist
        """
        with mock.patch("app.spotify_search_playlist", self.mock_playl):
            result = app.get_post_music_data("playlist",
                                             self.post_playlist[INPUT])
        self.assertEqual(result, self.post_playlist[EXPECT])


class RecievePosts(unittest.TestCase):
    """
    Tests the functions recieve_posts and emit_posts
    """
    def setUp(self):
        """
        The inputs/outputs for the tests
        """
        self.rec = {
            INPUT: {
                "user": {
                    "username": "Bob",
                    "pfp": "https://hello.com/hello.jpg",
                },
                "type": "song",
                "music": "playlist",
                "text": "Listening to my boi bob",
            }
        }

    def mock_mustype(self, music_type, music_data):
        """
        mocks the function get_post_music_data
        """
        return {"playlist": "https://music"}

    def test_post_recieve(self):
        """
        tests the on_post_recieve
        """
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.DB.session", session):
            with mock.patch("app.get_post_music_data", self.mock_mustype):
                app.on_post_receive(self.rec[INPUT])
        print(session.query(app.models.Posts).first())
        self.assertEqual(session.query(app.models.Posts).count(), 1)


class EmitUserOrArtistData(unittest.TestCase):
    """
    Tests the functions:
    emit_user_data
    emit_artist_data
    """

    def setUp(self):
        self.user = {
            "0": {"username": "Spl33nMq33n", "user_type": "user"},
            "1": [["1", "2", "3"], ["a","b","c"]],
            "2": "Musikalee",
            EXPECT: {
                "username": "Spl33nMq33n",
                "profileType": "user",
                "topArtists": ["1", "2", "3"],
                "artistPics": ["a","b","c"],
                "following": ["Cat", "Dhvani", "Justin"],
                "currentSong": "Musikalee",
            },
        }

    def mock_get_foll(self, user):
        """
        mocks result of get followers
        """
        return ["Cat", "Dhvani", "Justin"]

    def mock_username(self, sid):
        """
        mocks the result of username
        """
        return "Spl33nMq33n"

    @mock.patch("app.SOCKETIO.emit")
    def test_emituserdata(self, mocked_socket):
        """
        tests function emit user data
        """
        fflask = MockFlask()
        with mock.patch("app.flask.request", fflask):
            with mock.patch("app.get_followers_db", self.mock_get_foll):
                with mock.patch("app.get_username", self.mock_username):
                    app.emit_user_data(self.user["0"],
                                       self.user["1"],
                                       self.user["2"])
        mocked_socket.assert_called_once_with("emit user data",
                                              self.user[EXPECT])



class GetReccomendedAndTrending(unittest.TestCase):
    """
    Tests the Function Get Reccomended and Get Trending
    """
    def setUp(self):
        """
        Initializes the variables
        """
        self.sample = {
            EXPECT: [{"artist": "a1, a2", "song": "s1"},
                     {"artist": "a3", "song": "s2"}]
        }
        self.rec = {
            EXPECT: ["cheese", "woohoo", "teehee"],
        }
        self.ten = {
            EXPECT: [
                {"song": "chungy", "artists": "bob"},
                {"song": "chun", "artists": "bob"},
                {"song": "Big", "artists": "Biff"},
            ]
        }

    def test_empty_recommended(self):
        """
        Tests empty account
        """
        result = app.get_recommended([])
        self.assertEqual(result, None)

    def mockrchoice(self, user_top_artists, test):
        """
        Mocks the random sample
        """
        return ["cheese", "woohoo", "teehee"]

    def mockrcall(self, user_top_artists):
        """
        Mocks the function call
        """
        return ["cheese", "woohoo", "teehee"]

    def test_recommended(self):
        """
        Tests an actual reccomended list
        """
        with mock.patch("app.random.sample", self.mockrchoice):
            with mock.patch("app.spotify_get_recommended", self.mockrcall):
                result = app.get_recommended(["::cheese",
                                              "::woohoo",
                                              "::teehee"])
        self.assertEqual(result, self.rec[EXPECT])

    def mocktcall(self):
        """
        Mocks call to spotify's trending
        """
        return [
            {"track": {"name": "chungy", "artists": [{"name": "bob"}]}},
            {"track": {"name": "chun", "artists": [{"name": "bob"}]}},
            {"track": {"name": "Big", "artists": [{"name": "Biff"}]}},
        ]

    def mockts(self, trending_query, test):
        """
        Mocks random sampling of trending
        """
        return [
            {"track": {"name": "chungy", "artists": [{"name": "bob"}]}},
            {"track": {"name": "chun", "artists": [{"name": "bob"}]}},
            {"track": {"name": "Big", "artists": [{"name": "Biff"}]}},
        ]

    def mock_parse(self, songs):
        """
        Mocks Parse
        """
        return [
            {"artists": "bob", "song": "chungy"},
            {"artists": "bob", "song": "chun"},
            {"artists": "Biff", "song": "Big"},
        ]

    def test_trending(self):
        """
        Tests trending
        """
        session = UnifiedAlchemyMagicMock()
        with mock.patch("app.DB.session", session):
            with mock.patch("app.spotify_get_trending", self.mocktcall):
                with mock.patch("app.random.sample", self.mockts):
                    with mock.patch("app.parse_tracks", self.mock_parse):
                        result = app.get_trending()
        self.assertEqual(result, self.ten[EXPECT])

    @mock.patch("app.SOCKETIO.emit")
    def test_emit_trending(self, mocked_socket):
        """
        Tests emit trending
        """
        session = UnifiedAlchemyMagicMock()
        fflask = MockFlask()
        with mock.patch("app.flask.request", fflask):
            with mock.patch("app.DB.session", session):
                with mock.patch("app.spotify_get_trending", self.mocktcall):
                    with mock.patch("app.random.sample", self.mockts):
                        with mock.patch("app.parse_tracks", self.mock_parse):
                            app.emit_trending()
                            mocked_socket.assert_called_once_with(
                                "trending channel",
                                self.ten[EXPECT],
                                room="12345"
                            )

    class Song:
        """
        mocks song object
        """
        def __init__(self, artists, track):
            """
            Initializer
            """
            self.artists = artists
            self.track = track

    def test_parse_tracks_success(self):
        """
        Tests parse tracks
        """
        songs = []
        song_one = self.Song(["a1", "a2"], "s1")
        song_two = self.Song(["a3"], "s2")
        songs.append(song_one)
        songs.append(song_two)
        response = app.parse_tracks(songs)
        expected = self.sample[EXPECT]
        self.assertEqual(response, expected)


class Lstorage(unittest.TestCase):
    """
    Tests get and emit local storage
    """
    @mock.patch("app.SOCKETIO.emit")
    def test_get_local_storage(self, mocked_socket):
        """
        Tests get local storage
        """
        app.get_local_storage()
        mocked_socket.assert_called_once_with("navigation change", True)

    @mock.patch("app.SOCKETIO.emit")
    def test_emit_local_storage(self, mocked_socket):
        """
        Tests emit local storage
        """
        app.emit_local_storage(1)
        mocked_socket.assert_called_once_with("get posts from local storage",
                                              True)


if __name__ == "__main__":
    unittest.main()
