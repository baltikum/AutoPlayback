import urllib.parse as urlparse


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db_username = os.environ['DB_USER']
db_password = os.environ['DB_PASSW']
db_address = os.environ['DB_ADDRESS']
db_name = os.environ['DB_NAME']
#autoplayback_db

app = Flask(__name__)

#Databas
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@localhost/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




video_playback_entrys = [{'id':0,'name':'Vardagsrum', 'time':'20220422','file':'filnamn.mp4'}]


configured_cameras = []

from pack import routes
