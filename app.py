from os.path import join, dirname
import os
from dotenv import load_dotenv
from datetime import datetime
import flask
import flask_socketio
import flask_sqlalchemy
from flask_socketio import join_room, leave_room
import random
from spotify_login import get_user, get_artists
from spotify_trending import spotify_get_trending

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
    print("got post", data)
    query_username = models.ActiveUsers.query.filter_by(serverid = flask.request.sid).first()
    username = query_username.user
    
    query_pfp = models.Users.query.filter_by(username = username).first()
    pfp = query_pfp.profile_picture
    
    # TEMP MOCK
    music = "TEMP Misery Business by Paramore"
    title = "TEMP Post Title"
    
    message = data
    num_likes = 0
    time = datetime.now()
    
    post = models.Posts(username, pfp, music, message, title, num_likes, time)
    DB.session.add( post )
    DB.session.commit()
    print("added post", post)
    
    
    post_emitdata = {'username': post.username,
                    'pfp': post.pfp,
                    'music': post.music,
                    'text': post.message,
                    'title': post.title,
                    'num_likes': post.num_likes,
                    'time' : str( post.datetime )
                    }

    emit_posts(post_emitdata)

# temp mock
def emit_posts(data):
    socketio.emit('emit posts channel', data)
    print("emitted post: ", data)
    
    #data = [{'artist': 'Omar Apollo', 'song': 'Ugotme'}, {'artist': 'Ariana Grande', 'song': 'Positions'}, {'artist': 'Paramore', 'song': 'Misery Business'}]
    #socketio.emit('trending channel', data)

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
def emit_recommended():
    data = [{'artist': 'Clairo', 'song': 'Sofia'}, {'artist': 'Frank Ocean', 'song': 'Sweet Life'}, {'artist': 'Billie Eilish', 'song': 'bellyache'}]
    socketio.emit('recommended channel', data)

    
@app.route('/')
def hello():
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    join_room( flask.request.sid )
    
    print('Someone connected!')
    emit_user_data()
    socketio.emit('connected', {
        'test': 'Connected'
    })

    emit_trending()
    emit_recommended()
 
# temp mock
def emit_trending():
    
    trending = get_trending()
    socketio.emit('trending channel', trending, room=flask.request.sid)
    
def get_trending():
    
    # if DB empty, get trending
    # TODO later add timestamp and check daily
    if (models.Trending.query.all() == []):
        data = spotify_get_trending()
        for item in data:
            track = item['track']['name']
            artist = []
            for item_artist in item['track']['artists']:
                artist.append(item_artist['name'])
        
            DB.session.add(models.Trending(track, artist))
        
        DB.session.commit()
    
    
    # TODO fix same randint issue
    rand_ids = [random.randint(1,50), random.randint(1,50), random.randint(1,50)]
    trending = []
    
    for randid in rand_ids:
        track = {}
        query = models.Trending.query.filter_by(id = str(randid)).first()

        track['artist'] = ", ".join(query.artists)
        track['song'] = query.track
        
        trending.append( track )
    
    return trending

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
    
    # add to users if not already
    usersquery = models.Users.query.filter_by(username = user['username']).first()
    print ( usersquery )
    if (usersquery == [] or usersquery == None):
        db_user=models.Users(
                        user['username'],
                        user['profile-picture'],
                        user['user-type'],
                        artists,
                        [],
                        []
                    )
        DB.session.add(db_user)
        print( db_user )
    
    # add to active users table
    DB.session.add(models.ActiveUsers(user['username'], flask.request.sid))
    
    DB.session.commit()
    
    socketio.emit('login success', True, room=flask.request.sid)

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

