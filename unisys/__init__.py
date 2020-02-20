from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
#from flask_session import Session
import os

IMAGE_FOLDER = os.path.join('static', 'images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

app.config['SECRET_KEY'] = '2176705b4162dfcb2ed72d1430cba3c8'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///wtf.db'
#app.config['SESSION_TYPE'] = 'filesystem'


db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
lm=LoginManager(app)
#Session(app)
socketio = SocketIO(app)

lm.login_view='login'
lm.login_message_category = 'info'

from unisys import routes