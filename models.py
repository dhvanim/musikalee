"""
Our DB model for sqlalchemy
"""
# models.py
from sqlalchemy.dialects import postgresql
from app import DB


class Posts(DB.Model):
    """
    Our table for posts
    """
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256))
    pfp = DB.Column(DB.String(256))
    music_type = DB.Column(DB.String(120))
    music = DB.Column(DB.JSON)
    message = DB.Column(DB.String(256))
    num_likes = DB.Column(DB.Integer)
    datetime = DB.Column(DB.DateTime)

    def __init__(self, username, pfp, music_type, music, message, num_likes, datetime):
        """
        Initializes row in Posts
        """
        self.username = username
        self.pfp = pfp
        self.music_type = music_type
        self.music = music
        self.message = message
        self.num_likes = num_likes
        self.datetime = datetime

    def __repr__(self):
        """
        Display
        """
        return "<Posts: %s>" % self.message


class Comments(DB.Model):
    """
    Table for comments
    """
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256))
    text = DB.Column(DB.String(256))
    post_id = DB.Column(DB.Integer)
    datetime = DB.Column(DB.DateTime)

    def __init__(self, username, text, post_id, datetime):
        """
        Initialize row in Comments
        """
        self.username = username
        self.text = text
        self.post_id = post_id
        self.datetime = datetime

    def __repr__(self):
        """
        Prints comments
        """
        return "<Comment name: {}\ntext:{}\npost_id: {}".format(
            self.username, self.text, self.post_id)


class Users(DB.Model):
    """
    Users Table
    """
    username = DB.Column(DB.String(256), primary_key=True)
    profile_picture = DB.Column(DB.String(256))
    user_type = DB.Column(DB.String(256))
    top_artists = DB.Column(postgresql.ARRAY(DB.String))
    following = DB.Column(postgresql.ARRAY(DB.String))
    my_likes = DB.Column(postgresql.ARRAY(DB.Integer))

    def __init__(self, username, profile_picture, user_type,
                 top_artists, following, my_likes):
        """
        Row in Users
        """
        self.username = username
        self.profile_picture = profile_picture
        self.user_type = user_type
        self.top_artists = top_artists
        self.following = following
        self.my_likes = my_likes

    def __repr__(self):
        """
        Prints Users
        """
        return "<Users name: {}".format(self.username)


class Trending(DB.Model):
    """
    Trending Table
    """
    id = DB.Column(DB.Integer, primary_key=True)
    track = DB.Column(DB.String(500))
    artists = DB.Column(postgresql.ARRAY(DB.String))

    def __init__(self, track, artists):
        """
        Row in Trending
        """
        self.track = track
        self.artists = artists

    def __repr__(self):
        """
        Print Trending
        """
        return "<Trending track: {} artists: {}>".format(
            self.track, self.artists)


class ActiveUsers(DB.Model):
    """
    A table of Active Users
    """
    id = DB.Column(DB.Integer, primary_key=True)
    user = DB.Column(DB.String(500))
    serverid = DB.Column(DB.String(500))
    authtoken = DB.Column(DB.String(500))

    def __init__(self, user, serverid, authtoken):
        """
        Row in the table
        """
        self.user = user
        self.serverid = serverid
        self.authtoken = authtoken

    def __repr__(self):
        """
        Make it printable
        """
        return "<ActiveUsers user: {} id: {}>".format(self.user, self.serverid)


class Likes(DB.Model):
    """
    Table of likes on posts
    """
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256))
    post_id = DB.Column(DB.Integer())

    def __init__(self, username, post_id):
        """
        Row in likes
        """
        self.username = username
        self.post_id = post_id

    def __repr__(self):
        """
        print it
        """
        return "<Likes username: {} post_id: {}>".format(
            self.username, self.post_id)
