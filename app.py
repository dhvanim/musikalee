from os.path import join, dirname
import os
from dotenv import load_dotenv
from datetime import datetime
import flask
import flask_socketio
import flask_sqlalchemy
from sqlalchemy import desc
import models
import random
from spotify_login import get_user, get_artists

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

DOTENV_PATH = join(dirname(__file__), "sql.env")
load_dotenv(DOTENV_PATH)

DATABASE_URI = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

DB = flask_sqlalchemy.SQLAlchemy(app)

import models

DB.init_app(app)
DB.app = app

app.static_folder = 'static'

@socketio.on('user post channel')
def on_post_receive(data):
    
    # save to db first but other info isnt established yet
    time = str( datetime.now() );
    DB.session.add(models.Posts("catdematos98", [], data, "New Post", 0, time));
    DB.session.commit()
    # argument is temporary until it's in the database
    emit_posts()

def emit_posts():
    posts = [
        {
            "id": post.id,
            "username": post.username,
            "music": post.music,
            "text": post.message,
            "title": post.title,
            "num_likes": post.num_likes,
            "time": post.datetime.strftime("%m/%d/%Y, %H:%M:%S"),
            "comments": [
                            { 
                                "text": comment.text
                            }
                        for comment in DB.session.query(models.Comments).filter(models.Comments.post_id == post.id).order_by(desc(models.Comments.datetime)).all()
                        ]
        }
        for post in DB.session.query(models.Posts).order_by(desc(models.Posts.datetime)).all()
    ]
    socketio.emit('emit posts channel', posts)
    print(posts)
    

@socketio.on('like post')    
def update_num_likes(data):
    num_likes = data["num_likes"]
    post_id = data["id"]
    print("Post_id: {}".format(post_id))
    DB.session.query(models.Posts).filter(models.Posts.id == post_id).update({models.Posts.num_likes: num_likes}, synchronize_session = False) 
    DB.session.commit()
    
    #TODO 
    #get my username
    #add post_id to Users table where username is mine
    #myUsername = getMyUsername() 
    #DB.session.query(models.Users).filter(models.Users.username == myUsername).update({models.Users.my_likes: models.Users.my_likes.append(post_id)}, synchronize_session = False) 
    
    emit_posts()
    
@socketio.on('user data')    
def on_user_data_recieve():
    print("going to user")
    #database stuff happens here
    
    
def emit_user_data():
    print("giving user data")
    #userdata = {'username':'jan3apples','profileYype':'Listener', 'topArtists':['Drake', 'Shawn Mendes', 'Ariana Grande'], 'following':['Cat', 'Dhvani','Justin']}
    socketio.emit('emit user data', {'username':'jan3apples','profileType':'Listener', 'topArtists':['Drake', 'Shawn Mendes', 'Ariana Grande'], 'following':['Cat', 'Dhvani','Justin']})
    print("emiting user data")



# temp mock
def emit_trending():
    data = [{'artist': 'Omar Apollo', 'song': 'Ugotme'}, {'artist': 'Ariana Grande', 'song': 'Positions'}, {'artist': 'Paramore', 'song': 'Misery Business'}]
    socketio.emit('trending channel', data)

# temp mock
def emit_recommended():
    data = [{'artist': 'Clairo', 'song': 'Sofia'}, {'artist': 'Frank Ocean', 'song': 'Sweet Life'}, {'artist': 'Billie Eilish', 'song': 'bellyache'}]
    socketio.emit('recommended channel', data)

    
@app.route('/')
def hello():
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    emit_user_data()
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    # temp example add/commit DELETE
    DB.session.add(models.Comments("jan3apples", "yess", 423, datetime.now()))
    DB.session.commit()
    
    emit_posts()
    emit_trending()
    emit_recommended()
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new spotify user')
def on_spotlogin(data):
    """
    Runs the code in spotify_login and adds it to the db
    """
    user=get_user(data['token'])
    artists=get_artists(data['token'])
    try:
        db_user=models.Users(
                        username=user['username'],
                        profile_picture=user['profile-picture'],
                        user_type=user['user-type'],
                        top_artists=artists,
                        following=[],
                        my_likes=[]
                        )
        DB.session.add(db_user)
        DB.session.commit()
    except:
        print("TODO SKIP IF ALREADY HAS ACCT ALSO FIX DBCALLS IF ACTUALLY BROKEN")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

