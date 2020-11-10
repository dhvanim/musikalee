from os.path import join, dirname
import os
from dotenv import load_dotenv
from datetime import datetime
import flask
import flask_socketio
import flask_sqlalchemy
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
    
    # save to db first but other info isnt established yet
    
    # argument is temporary until it's in the database
    emit_posts(data)

# temp mock
def emit_posts(data):
    time = str( datetime.now() );
    post = {'username':'jan3apples', 'text':data, 'num_likes':'3', 'time':time}
    socketio.emit('emit posts channel', post)
    

    
    #data = [{'artist': 'Omar Apollo', 'song': 'Ugotme'}, {'artist': 'Ariana Grande', 'song': 'Positions'}, {'artist': 'Paramore', 'song': 'Misery Business'}]
    #socketio.emit('trending channel', data)

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
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    # temp example add/commit DELETE
    DB.session.add(models.Comments("jan3apples", "yess", 423, datetime.now()))
    DB.session.commit()
    
    emit_trending()
    emit_recommended()
 
# temp mock
def emit_trending():
    
    trending = get_trending()
    print(trending)
    socketio.emit('trending channel', trending)
    
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
    try:
        db_user=models.Users(
                        username=user['username'],
                        profile_picture=user['profile-picture'],
                        user_type=user['user-type'],
                        top_artists=artists,
                        following=[]
                        )
        DB.session.add(db_user)
        DB.session.commit()
    except:
        print("TODO SKIP IF ALREADY HAS ACCT ALSO FIX DBCALLS IF ACTUALLY BROKEN")
        
    
    socketio.emit('login success', True)

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

