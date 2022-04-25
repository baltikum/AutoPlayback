#from collections import UserDict
#from email.headerregistry import AddressHeader

from turtle import reset
from flask import Flask, render_template, request, Response#,send_file,current_app
from flask_sqlalchemy import SQLAlchemy
import cv2, os, re, time, json, logging, traceback, datetime
from time import strftime
from Camera import Camera

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(8)

app = Flask(__name__)
from datetime import datetime


HOST = 'localhost'
PORT = 5000
SYSTEM_HOST = '192.168.0.5'
SYSTEM_GW = '192.168.0.1'
SYSTEM_NTP = '192.168.0.5'




#Databas
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:Elwyn2021?!@localhost/autoplayback_db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

#Exempel url
#url = f"rtsp://{username}:{password}@{camera_address}/onvif-media/media.amp"
#capture = cv2.VideoCapture(url)

app = Flask(__name__)


configured_cameras = []
capturing_cameras = []


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
    global configured_cameras
    camera = configured_cameras.get(id)
    camera.record()
    camera.motion_activated_at(time.time())
    
    

#IMG yield jpeg ström 
'''
#Live image stream jpeg backend
def generate_frames(id):
    global capturing_cameras
    try:
        id = int(id)
    except:
        id= 0
        
    while True:
            
        success,frame = capturing_cameras[id].read()
        if not success:
            break
        else:
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            #yield frame ?
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n'
                    + frame +b'\r\n')
@app.route('/video/<id>')
def get_stream(id):
    return Response(generate_frames(id),mimetype='multipart/x-mixed-replace; boundary=frame')
'''


#Den nya inspelade mp4 streamern
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
def get_chunk(byte1=None, byte2=None):
    full_path = "20220425_211355Vardagsrum.mp4"
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



#Load the camera configurations and start captures
def load_cameras():
    global configured_cameras
    try:
        file = open('camera_configurations.ini')
        jsonData = file.read()
        json_cameras = json.loads(jsonData)
        list_of_cameras= json_cameras['cameras']
        print(f'Loaded Cameras: {list_of_cameras}')
        
        for entry in list_of_cameras:
            configured_cameras.append(Camera(int(entry.get('id')), entry.get('ip'), entry.get('name'), entry.get('username'),
                                          entry.get('password'),entry.get('settings'),SYSTEM_HOST,
                                          SYSTEM_GW,SYSTEM_NTP))
        res = True
    except:
        logging.exception('Camera configuration did not load.')
        res = False
        
    return res
def configure_cameras():
    global configured_cameras
    for entry in configured_cameras:
        entry.configure_camera()
    return True
def start_cameras():
    global configured_cameras,capturing_cameras
    for entry in configured_cameras:
        capture = cv2.VideoCapture(entry.url)
        capturing_cameras.append(capture)
        
    return True       
def record_camera(id):
    global configured_cameras, capturing_cameras
    camera = capturing_cameras[id]

    #camera = cv2.VideoCapture(configured_cameras[id].url)
    now = datetime.now()
    format = "%Y%m%d_%H%M%S"
    time = now.strftime(format)

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fileout = cv2.VideoWriter(f'{time}{configured_cameras[id].camera_name}.mp4', codec, 20.0, (1024,  768))
    record = 0
    motion = 0
    while(True):
        
        res, frame = camera.read()
        record += 1
        
        if configured_cameras[id].camera_motion :
            fileout.write(frame)
            motion += 1
            if motion > 300:
                configured_cameras[id].camera_motion = False
        else:
            motion = 0
        
        if not res or record > 200:
            break

        
    camera.release()
    fileout.release()
   
#Motion route and add to threadpool
def read_captures(id):
    executor.submit(record_camera(id)) 
    return True
@app.route('/motion/<id>', methods=['POST'])
def motion_detected(id):
    print(f'Motion notification received from {id}')
    global capturing_cameras
    
    try:
        id = int(id)
        if id < len(capturing_cameras) and id >= 0:
            res = read_captures(id)
        else:
            raise Exception('id is not in range')
    except:
        traceback.print_exc()
        res = False
    return res
    
    
    
if __name__ == '__main__':

    if load_cameras():
        if configure_cameras():
            if start_cameras():
                logging.info('Camera configuration loaded.')
                record_camera(0)
    
    
    
    app.run(host='localhost',debug=True,threaded=True)
    
