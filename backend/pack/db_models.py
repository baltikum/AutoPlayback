#from flask_sqlalchemy import SQLAlchemy
#from flask import Flask
from datetime import datetime
from pack import db


#database table model for users
class User(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,default='User')
    username = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    privilege = db.Column(db.String(10),nullable=False,default='user')
    device = db.Column(db.String(20),nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f'User {self.name} joined the system {self.created_at}'

    def __init__(self,name,username,password,email,privilege,device):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.privilege = privilege
        self.device = device


#database table model for camera configurations
class CameraConfigs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,default='Camera')
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(20),nullable=False, unique=True)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'Camera {self.id} {self.name} added at {self.created_at}'

    def __init__(self,name,username,password,address):
        self.name = name
        self.username = username
        self.password = password
        self.address = address


class Recordings(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(400),nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f'Playback scenario for {self.recorded_at} archived at {self.created_at}'

    def __init__(self,id,content,recorded_at):
        self.id = id
        self.content = content
        self.recorded_at = recorded_at
