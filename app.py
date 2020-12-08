"""
Our main file
"""
from os.path import join, dirname
import random
import os
from datetime import datetime
from dotenv import load_dotenv
import flask
import flask_socketio
import flask_sqlalchemy
from sqlalchemy import asc, desc
import timeago
from flask_socketio import join_room, leave_room

APP = flask.Flask(__name__)
SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

DOTENV_PATH = join(dirname(__file__), "sql.env")
load_dotenv(DOTENV_PATH)

DATABASE_URI = os.environ["DATABASE_URL"]
APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

DB = flask_sqlalchemy.SQLAlchemy(APP)

import models
from spotify_login import (
    get_user,
    get_artists,
    get_top_artists,
    get_current_song,
    get_num_listeners,
    get_top_tracks,
)
from spotify_music import (
    spotify_get_trending,
    spotify_get_recommended,
    spotify_search_track,
    spotify_search_artist,
    spotify_search_album,
    spotify_search_playlist,
)
from ticketmaster_api import search_events

DB.init_app(APP)
DB.app = APP

APP.static_folder = "static"


def get_username(flask_id):
    """
    Gets users username from flaskid
    """
    user = (
        DB.session.query(models.ActiveUsers).filter_by(
            serverid=flask_id).first().user
    )
    DB.session.commit()
    return user


def query_user(user):
    """
    Queries user object
    """
    user = models.Users.query.filter_by(username=user).first()
    DB.session.commit()
    return user


def get_post_music_data(music_type, music_data):
    """
    Gets a posts music metadata
    """
    data = {}

    if music_type == "song":
        song = music_data["song"].strip()
        artist = music_data["artist"].strip()
        data = spotify_search_track(song, artist)

    elif music_type == "artist":
        artist = music_data["artist"].strip()
        data = spotify_search_artist(artist)

    elif music_type == "album":
        artist = music_data["artist"].strip()
        album = music_data["album"].strip()
        data = spotify_search_album(album, artist)

    elif music_type == "playlist":
        playlist = music_data["playlist"].strip()
        data = spotify_search_playlist(playlist)

    return data


@SOCKETIO.on("user post channel")
def on_post_receive(data):
    """
    gets socket recieve post
    """
    username = data["user"]["username"]
    pfp = data["user"]["pfp"]

    music_type = data["type"]
    music_entry = get_post_music_data(music_type, data["music"])
    
    if music_entry == None:
        music_type = "default"
        music_entry = {}

    message = data["text"]
    num_likes = 0
    time = datetime.now()

    post = models.Posts(
        username, pfp, music_type, music_entry, message, num_likes, time
    )

    DB.session.add(post)
    DB.session.commit()

    post_dict = {
        "id": post.id,
        "username": post.username,
        "text": post.message,
        "num_likes": post.num_likes,
        "datetime": post.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
        "pfp": post.pfp,
        "comments": [],
        "is_liked": False,
        "isCommentsOpen": False,
        "music_type": post.music_type,
        "music": post.music,
    }

    SOCKETIO.emit("emit new post channel", post_dict)


def emit_posts():
    """
    Sends post to react
    """
    posts = []
    all_posts = (
        DB.session.query(models.Posts).order_by(
            desc(models.Posts.datetime)).all()
    )
    DB.session.commit()
    for post in all_posts:
        print(post.num_likes)
        entry = {
            "id": post.id,
            "username": post.username,
            "text": post.message,
            "num_likes": post.num_likes,
            "datetime": post.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            "pfp": post.pfp,
            "isCommentsOpen": False,
            "comments": [
                {
                    "text": comment.text,
                    "username": comment.username,
                    "datetime": timeago.format(comment.datetime,
                                               datetime.now()),
                }
                for comment in DB.session.query(models.Comments)
                .filter(models.Comments.post_id == post.id)
                .order_by(desc(models.Comments.datetime))
                .all()
            ],
            "is_liked": DB.session.query(models.Likes).filter(
                models.Likes.username == post.username,
                models.Likes.post_id == post.id).scalar() is not None,
            "music_type": post.music_type,
            "music": post.music,
        }

        posts.append(entry)
    SOCKETIO.emit("emit posts channel", posts)

def get_followers_db(user):
    """
    Gets list of Followers
    """
    followers_list = DB.session.query(
        models.Users.following).filter_by(
            username=user).scalar()
    DB.session.commit()
    return followers_list

def follower_update_db(user):
    """
    Get List of followers
    """
    followers_list = DB.session.query(
        models.Users.following).filter_by(
            username=user).scalar()
    new_followers_list = followers_list
    DB.session.commit()
    if user not in followers_list:
        new_followers_list.append(user)
        is_followed = True
        DB.session.query(models.Users).filter(
            models.Users.username == user).update(
                {models.Users.following: new_followers_list},
                synchronize_session="fetch")
    else:
        new_followers_list.remove(user)
        is_followed = False
        DB.session.query(models.Users).filter(
            models.Users.username == user).update(
                {models.Users.following: new_followers_list},
                synchronize_session="fetch")
    DB.session.commit()
    return [new_followers_list, is_followed]

def add_or_remove_like_from_db(user, liked_post_id):
    """
    Adds the like functionality using stuff from react
    """
    is_liked = (
        DB.session.query(models.Likes.id)
        .filter_by(username=user, post_id=liked_post_id)
        .scalar()
        is not None
    )
    DB.session.commit()
    if is_liked:
        DB.session.query(models.Likes).filter_by(
            username=user, post_id=liked_post_id
        ).delete()
    else:
        DB.session.add(models.Likes(user, liked_post_id))
    DB.session.commit()
    
    return not is_liked


def update_likes_on_post(post_id, num_likes):
    """
    changes like number in query
    """
    post = DB.session.query(models.Posts).filter(models.Posts.id == post_id)
    post.first().num_likes = num_likes
    DB.session.commit()


@SOCKETIO.on("like post")
def update_num_likes(data):
    """
    When someone likes a post
    """
    num_likes = data["num_likes"]
    post_id = data["id"]

    update_likes_on_post(post_id, num_likes)

    username = get_username(flask.request.sid)
    is_liked = add_or_remove_like_from_db(username, post_id)


    SOCKETIO.emit(
        "like post channel",
        {"post_id": post_id, "num_likes": num_likes, "is_liked": is_liked},
    )


def emit_user_data(user_info, top_artists, curr_song):
    """
    Sends user profile
    """
    artist_list = []
    if len(top_artists) >= 3:
        artist_list.append(top_artists[0])
        artist_list.append(top_artists[1])
        artist_list.append(top_artists[2])
    followers_list = get_followers_db(get_username(flask.request.sid))
    print("here is userInfo: ", user_info)
    SOCKETIO.emit(
        "emit user data",
        {
            "username": user_info["username"],
            "profileType": user_info["user_type"],
            "topArtists": artist_list,
            "following": followers_list,
            "currentSong": curr_song,
        },
    )


@SOCKETIO.on("recieve follower data")
def update_follower_info():
    """
    Runs on recieving follower data
    """
    username = get_username(flask.request.sid)
    results = follower_update_db(username)
    followers = results[0]
    is_following = results[1]
    print("list of of followers", followers)
    SOCKETIO.emit('emit follower data',
                  {'followers': followers, 'isFollowing': is_following})

def emit_recommended():
    """
    Emits user's recommended
    """
    username = get_username(flask.request.sid)
    query_users = query_user(username)

    recommended = get_recommended(query_users.top_artists)

    if recommended is None:
        return

    SOCKETIO.emit("recommended channel", recommended, room=flask.request.sid)


def get_recommended(user_top_artists):
    """
    Gets user's reccomended
    """
    if len(user_top_artists) == 0:
        return None
    # keep only spotify ID
    for i in range(len(user_top_artists)):
        user_top_artists[i] = user_top_artists[i].split(":")[2]

    sample_artists = random.sample(user_top_artists, 3)

    recommended = spotify_get_recommended(sample_artists)
    return recommended


def emit_trending():
    """
    Sends trending to user timeline
    """
    trending = get_trending()
    SOCKETIO.emit("trending channel", trending, room=flask.request.sid)

        
def get_trending():
    """
    Gets trending from spotify
    """
    if DB.session.query(models.Trending).count() == 0:
        data = spotify_get_trending()
        for item in data:
            track = item["track"]["name"]
            artist = []
            for item_artist in item["track"]["artists"]:
                artist.append(item_artist["name"])

            DB.session.add(models.Trending(track, artist))
            DB.session.commit()

        DB.session.commit()

    trending_query = models.Trending.query.all()
    DB.session.commit()
    sample = random.sample(trending_query, 3)

    return parse_tracks(sample)

def parse_tracks(sample):
    
    trending = []
    for song in sample:
        track = {}
        track["artist"] = ", ".join(song.artists)
        track["song"] = song.track
        trending.append(track)
    return trending

@SOCKETIO.on("get local storage")
def get_local_storage():
    """
    Says that navigation had changed
    """
    SOCKETIO.emit("navigation change", True)


@SOCKETIO.on("new spotify user")
def on_spotlogin(data):
    """
    Runs the code in spotify_login and adds it to the db
    """
    user = get_user(data["token"])
    artists = get_artists(data["token"])

    # add to users if not already, update top artists
    usersquery = query_user(user["username"])
    if usersquery == [] or usersquery is None:
        db_user = models.Users(
            username=user["username"],
            profile_picture=user["profile-picture"],
            user_type=user["user-type"],
            top_artists=artists,
            following=[],
            my_likes=[],
        )
        DB.session.add(db_user)
        DB.session.commit()
    else:
        usersquery.top_artists = artists

    # emit success to user, so they can access timeline
    SOCKETIO.emit(
        "login success",
        {
            "status": True,
            "userinfo": {"username": user["username"],
                         "pfp": user["profile-picture"]},
        },
        room=flask.request.sid,
    )

    # add to active users table
    DB.session.add(
        models.ActiveUsers(user["username"], flask.request.sid, data["token"])
    )

    # commit all db changes
    DB.session.commit()


# tell view to get local storage on navigation change
@SOCKETIO.on("get local storage")
def emit_local_storage(data):
    """
    Tells person to get from local storage
    """
    if data:
        # emit success to user, so they can access timeline
        SOCKETIO.emit("get posts from local storage", True)


# emit trending and recommended and posts
@SOCKETIO.on("user logged in")
def user_logged_in(data):
    """
    on login to spotify
    """
    if data:
        emit_posts()
        emit_recommended()
        emit_trending()


@SOCKETIO.on("get profile")
def send_user_profile(data):
    """
    sends the profile
    """
    if (data == True):
         username = get_username(flask.request.sid)
    else:
         username = data
    
    top_artists = get_top_artists(username)
    curr_song = get_current_song(username)

    usertype = query_user(username)
    userinfo = {"username": username, "user_type": usertype.user_type}
    emit_user_data(userinfo, top_artists, curr_song)


@SOCKETIO.on("post comment")
def save_comment(data):
    """
    Recieves the socket post for comments
    """
    username = data["username"]
    time = datetime.now()
    comment = models.Comments(username, data["comment"], data["postId"], time)
    DB.session.add(comment)
    DB.session.commit()

    comment = {
        "text": data["comment"],
        "username": username,
        "datetime": timeago.format(time, datetime.now()),
    }
    SOCKETIO.emit(
        "NEW COMMENT ON POST", {"post_id": data["postId"], "comment": comment}
    )


@SOCKETIO.on("search ticketmaster")
def get_ticketmaster_events(data):
    """
    Gets query from client for ticketmaster
    """
    zipcode = data["zipcode"]
    artist = data["artist"]
    page = str(data["page"])
    events = search_events(zipcode, artist, page)
    if zipcode == "" and artist == "":
        events = []
    if events is None:
        events = []
    SOCKETIO.emit("display events", events)


@APP.route("/")
def hello():
    """
    What actually renders the page
    """
    return flask.render_template("index.html")


@SOCKETIO.on("connect")
def on_connect():
    """
    Connect
    """
    join_room(flask.request.sid)
    
    print("Someone connected!")
    SOCKETIO.emit("connected", {"test": "Connected"})


@SOCKETIO.on("disconnect")
def on_disconnect():
    """
    Disconect
    """
    print("Someone disconnected!")


if __name__ == "__main__":
    SOCKETIO.run(
        APP,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "8080")),
        debug=True,
    )
