from collections import UserDict
from email.headerregistry import Address
import traceback
from flask import Flask, render_template, request, Response,send_file,current_app
from flask_sqlalchemy import SQLAlchemy
import cv2, os , re,time
from Camera import Camera
import json,logging

from datetime import datetime


HOST = 'localhost'
PORT = 5000
SYSTEM_HOST = '192.168.0.5'
SYSTEM_GW = '192.168.0.1'
SYSTEM_NTP = '192.168.0.5'


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

running_cameras = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/motion/<id>')
def motion_id(id):
    try: 
        camera_id = int(id)
        motion_activated(camera_id)
        res = True
    except:
        trace = traceback.format_exc()
        res = False
        print(trace)

def motion_activated(id):
    global running_cameras
    camera = running_cameras.get(id)
    camera.record()
    camera.motion_activated_at(time.time())
    
    



#Live image stream jpeg backend
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



#Den nya inspelade mp4 streamern
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
def get_chunk(byte1=None, byte2=None):
    full_path = "test.mp4"
    file_size = os.stat(full_path).st_size
    start = 0
    
    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(full_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size
@app.route('/playback')
def playback():
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])
       
    chunk, start, length, file_size = get_chunk(byte1, byte2)
    resp = Response(chunk, 206, mimetype='video/mp4',
                      content_type='video/mp4', direct_passthrough=True)
    resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return resp







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




def load_cameras():
    global running_cameras
    try:
        file = open('camera_configurations.ini')
        jsonData = file.read()
        json_cameras = json.loads(jsonData)
        list_of_cameras= json_cameras['cameras']
        print(f'Loaded Cameras: {list_of_cameras}')
        
        for entry in list_of_cameras:
            running_cameras.append(Camera(entry.get('ip'),entry.get('name'),entry.get('username'),
                                          entry.get('password'),entry.get('settings'),SYSTEM_HOST,
                                          SYSTEM_GW,SYSTEM_NTP))
        res = True
    except:
        logging.exception('Camera configuration did not load.')
        res = False
        
    return res

def configure_cameras():
    global running_cameras
    for entry in running_cameras:
        entry.configure_camera()
        

if __name__ == '__main__':

    if load_cameras() :
        res = configure_cameras()
        
    
    
    
    
    app.run(host='localhost',debug=True,threaded=True)
    
