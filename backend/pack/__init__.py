
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#Databas
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:Elwyn2021?!@localhost/autoplayback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from pack import routes