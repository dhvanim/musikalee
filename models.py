# models.py
from app import DB
from sqlalchemy.dialects import postgresql


class Posts(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256))
    pfp = DB.Column(DB.String(256))
    music = DB.Column(DB.String(120))
    message = DB.Column(DB.String(256))
    title = DB.Column(DB.String(120))
    num_likes = DB.Column(DB.Integer)
    datetime = DB.Column(DB.DateTime)
    

    def __init__(self, username, pfp, music, message, title, num_likes, datetime):
        self.username = username
        self.pfp = pfp
        self.music = music
        self.message = message
        self.title = title
        self.num_likes = num_likes
        self.datetime = datetime

    def __repr__(self):
        return "<Posts: %s>" % self.message


class Comments(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256))
    text = DB.Column(DB.String(256))
    post_id = DB.Column(DB.Integer)
    datetime = DB.Column(DB.DateTime)

    def __init__(self, username, text, post_id, datetime):
        self.username = username
        self.text = text
        self.post_id = post_id
        self.datetime = datetime

    def __repr__(self):
        return "<Comment name: {}\ntext:{}\post_id: {}".format(
            self.username, self.text, self.post_id
        )


class Users(DB.Model):
    username = DB.Column(DB.String(256), primary_key=True)
    profile_picture = DB.Column(DB.String(256))
    user_type = DB.Column(DB.String(256))
    top_artists = DB.Column(postgresql.ARRAY(DB.String))
    following = DB.Column(postgresql.ARRAY(DB.String))
    my_likes = DB.Column(postgresql.ARRAY(DB.Integer))

    def __init__(self, username, profile_picture, user_type, top_artists, following, my_likes):
        self.username = username
        self.profile_picture = profile_picture
        self.user_type = user_type
        self.top_artists = top_artists
        self.following = following
        self.my_likes = my_likes

    def __repr__(self):
        return "<Users name: {}".format(self.username)

class Trending(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    track = DB.Column(DB.String(500))
    artists = DB.Column(postgresql.ARRAY(DB.String))
    
    def __init__(self, track, artists):
        self.track = track
        self.artists = artists
        
    def __repr__(self):
        return "<Trending track: {} artists: {}>".format(self.track, self.artists)
        
 
class ActiveUsers(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    user = DB.Column(DB.String(500))
    serverid = DB.Column(DB.String(500))
    
    def __init__(self, user, serverid):
        self.user = user
        self.serverid = serverid
        
    def __repr__(self):
        return "<ActiveUsers user: {} id: {}>".format(self.user, self.serverid)

class Likes(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(256))
    post_id = DB.Column(DB.Integer())
    
    def __init__(self, username, post_id):
        self.username = username
        self.post_id = post_id
        
    def __repr__(self):
        return "<Likes username: {} post_id: {}>".format(self.username, self.post_id)        

class Music(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    song = DB.Column(DB.String(500))
    artist = DB.Column(postgresql.ARRAY(DB.String))
    album = DB.Column(DB.String(500))
    preview_url = DB.Column(DB.String(500))
    uri = DB.Column(DB.String(500))
    
    def __init__(self, song, artist, album, preview_url, uri):
        self.song = song
        self.artist = artist
        self.album = album
        self.preview_url = preview_url
        self.uri = uri
        
    def __repr__(self):
        return "<Music song: {} artist: {}>".format(self.song, self.artist)  
        
DB.create_all()
DB.session.commit()
