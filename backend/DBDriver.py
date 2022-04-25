from flask_sqlalchemy import SQLAlchemy

class DBDriver():
    def __init__(self, user):
        self.user = user
        
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
    
    def __init__(self,name,username,password,device):
        self.name = name
        self.username = username
        self.password = password
        self.device = device
        
       
#database table model for camera configurations
class CameraEntry(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,default='Camera')
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(20),nullable=False, unique=True)
    added_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    
    def __repr__(self):
        return f'Camera {self.id} {self.name} added at {self.created_at}'
    
    def __init__(self,name,username,password,address):
        self.name = name
        self.username = username
        self.password = password
        self.address = address       