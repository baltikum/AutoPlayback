from collections import UserDict
from email.headerregistry import Address
from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
import cv2
from Camera import Camera

from datetime import datetime


HOST = 'localhost'
PORT = 5000

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:Elwyn2021?!@localhost/autoplayback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
class Camera(db.Model):
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
    
    
    
id = "1"
name ="Livingroom Camera"
username = "onvif"
password = "onvif"
camera_address = "192.168.0.90"
width = "1024.0"
height = "768.0"
fps = "18.0"


url = f"rtsp://{username}:{password}@{camera_address}/onvif-media/media.amp"

capture = cv2.VideoCapture(url)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
            
        success,frame = capture.read()
        if not success:
            break
        else:
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            #yield frame ?
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'
                    + frame +b'\r\n')

@app.route('/video')
def get_stream():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/axis')
def motion():
    print("MOTION")        
    print("MOTION")  
    print("MOTION")  
    print("MOTION")  
    return {'motion':'motiooon'}




#create new user request
@app.route('/newuser', methods= ['POST'])
def create_new_user():
    #fetch data from fields
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    device = request.json['device']
    
    #create a user
    user = User(name,username,password,device)
    
    #submit to database
    db.session.add(user)
    db.session.commit()
    
    #returns data as json
    return format_userdata(user)

#Format json for succesfull login requests
def format_userdata(user):
    return {
        "id": user.id,
        "name": user.name,
        "username ": user.username ,
        "email": user.email,
        "privilege": user.privilege,
        "device": user.device,
        "created_at": user.created_at
    }



@app.route('/test')
def test():
    return {'cameras': 'camera1'}


#login page route
@app.route('/login', methods= ['GET'])
def login_page():
    return render_template(login.html)

#login submit request
@app.route('/login', methods= ['POST'])
def login_request():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username)
    
    if user:
        return format_userdata(user)
    else:
        return 'Username not found'

    

#get full list of camera configurations as json
@app.route('/cameras', methods = ['GET'])
def get_cameras():
    cameras = Camera.query.order_by(Camera.id.asc()).all()
    cameras_json = []
    for camera in cameras:
        cameras_json.append(format_camera(camera))
    return {'cameras': cameras_json }

#Format camera configurations to json
def format_camera(camera):
    return {
        "id": camera.id,
        "name": camera.name,
        "username": camera.username,
        "resolution": camera.resolution,
        "fps": camera.fps,
        "address": camera.address,
        "added_at": camera.added_at
    }

#Add new camera
@app.route('/cameras', methods = ['POST'])
def add_new_camera():
    #fetch data from fields
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    address = request.json['address']
    
    #create a new camera
    camera = Camera(name,username,password,address)
    
    #submit to database
    db.session.add(camera)
    db.session.commit()
    
    return 'Camera added.'


#delete camera by id
@app.route('/cameras/<id>', methods= ['DELETE'])
def delete_camera(id):
    camera = Camera.query.filter_by(id=id).one()
    db.session.delete(camera)
    db.session.commit()
    return 'Camera deleted.'


#update camera by id
@app.route('/cameras/<id>', methods= ['PUT'])
def update_camera(id):
    #Find camera
    camera = Camera.query.filter_by(id=id)
    
    #request new camera data
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    address = request.json['address']
    
    #update data on camera
    camera.update(dict(name = name,
                       username = username,
                       password = password,
                       address = address,
                       added_at = datetime.utcnow()))
    
    #commit to database
    db.session.commit()
    return f'Camera updated.'

if __name__ == '__main__':
    app.run(host='localhost',debug=True)
    
