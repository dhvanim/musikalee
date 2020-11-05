from os.path import join, dirname
import os
from dotenv import load_dotenv
from datetime import datetime
import flask
import flask_socketio
import flask_sqlalchemy

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

DOTENV_PATH = join(dirname(__file__), "sql.env")
load_dotenv(DOTENV_PATH)

DATABASE_URI = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

DB = flask_sqlalchemy.SQLAlchemy(app)
DB.init_app(app)
DB.app = app

app.static_folder = 'static'


@socketio.on('user post channel')
def on_post_receive(data):
    
    # save to db first but other info isnt established yet
    
    # argument is temporary until it's in the database
    emit_posts(data)

def emit_posts(data):
    time = str( datetime.now() );
    post = {'username':'jan3apples', 'text':data, 'num_likes':'3', 'time':time}
    socketio.emit('emit posts channel', post)
    
@app.route('/')
def hello():
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )