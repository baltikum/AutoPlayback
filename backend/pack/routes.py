
from datetime import datetime
from flask import render_template, request, Response
from pack.camera import Camera
from pack import app, video_playback_entrys,configured_cameras,db
from sqlalchemy import func 
from pack.db_models import SystemUsers,CameraConfigs,Recordings
import traceback,logging,json,os,re
from queue import Queue


"""

@app.route('/live/<url>', methods=['GET'])
def live(url):
    directory_path = os.getcwd()
    print("My current directory is : " + directory_path)
    filename = ('./public/video/' + url)
    with open(filename,'r') as file:
        temp = file.read()

    #resp = make_response(temp)
    #resp.headers['Access-Control-Allow-Origin'] = '*'
    return Response(temp,headers={ 'Access-Control-Allow-Origin': '*' })

"""




#Den nya inspelade mp4 streamern
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
def get_chunk(full_path, byte1=None, byte2=None):

    file_size = os.stat(full_path).st_size
    start = 0

    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(full_path, 'rb') as file:
        file.seek(start)
        chunk = file.read(length)
    return chunk, start, length, file_size
@app.route('/playback/<filename>')
def playback(filename):
    try:
        full_path = "../recordedvideo/" + str(filename)
    except:
        pass

    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])

    chunk, start, length, file_size = get_chunk(full_path, byte1, byte2)
    resp = Response(chunk, 206, mimetype='video/mp4',
                      content_type='video/mp4', direct_passthrough=True)
    resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return resp




@app.route('/playback/fetch', methods=['GET'])
def serve_playback():
    latest_recording = Recordings.query.filter(Recordings.id.desc()).first()

    # latest_recording = Recordings.query(func.max(Recordings.id)).first()
    print(latest_recording)
    print(latest_recording.content)
    return { 'recordings' : latest_recording.content }



#Store playback in database
@app.route('/playback/store', methods=['POST'])
def store_playback():
    recordings = request.json['recordings']

    recording = Recordings(recordings, datetime.datetime.now())

    db.session.add(recording)
    db.session.commit()
    
    return { 'status': True }



#Fetch live sources from frontend
@app.route('/live/sources', methods=['GET'])
def serve_livesources():
    live_list = []
    for entry in configured_cameras:
        live_list.append('http://192.168.0.5:666/'+str(entry.camera_id)+'.m3u8')
    return { 'live': live_list }







##USER ROUTES

#fetch configured userdata
@app.route('/get_users', methods= ['GET'])
def get_users():
    all_users = SystemUsers.query.all()
    json_users = []
    for user in all_users:
        json_users.append(format_userdata(user))
        
    return { 'users': json_users }
#create new user request
@app.route('/add_user', methods= ['POST'])
def create_new_user():
    #fetch data from fields
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    device = request.json['device']
    salt = request.json['salt']

  
    #create a user
    user = SystemUsers(name,username,password,email,0,device,salt)

    #submit to database
    db.session.add(user)
    db.session.commit()

    #returns data as json
    return format_userdata(user)
#Format json for succesfull login requests
def format_userdata(user):
    return {
        'id': user.id,
        'name': user.name,
        'username': user.username ,
        'email': user.email,
        'privilege': user.privilege,
        'device': user.device,
        'created_at': user.created_at
    }
#query db for user, fetch password salt
@app.route('/query_user_salt', methods= ['POST'])
def query_user():
    username = request.json['username']
    userQuery = SystemUsers.query.filter_by(username=username).first()
 
    
    if userQuery.username == username:
        return { 'status':True, 'salt':userQuery.salt }
    else:
        return { 'status':False } 
#login submit request
@app.route('/login', methods= ['POST'])
def login_request():
    username = request.json['username']
    password = request.json['password']

    userQuery = SystemUsers.query.filter_by(username=username).first()
    if userQuery.username == username:
        
        
        if password == userQuery.password:
            userData = format_userdata(userQuery)
            return userData
            
        return 'wrong password'

    else:
        return 'Username not found'
    





##CAMERA ROUTES

#get full list of camera configurations as json
@app.route('/get_cameras', methods = ['GET'])
def get_cameras():
    cameras = CameraConfigs.query.order_by(CameraConfigs.id.asc()).all()
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
        "password": camera.password,
        "address": camera.address,
        "settings": camera.settings,
        "added_at": camera.added_at
    }
#Add new camera
@app.route('/add_camera', methods = ['POST'])
def add_new_camera():
    #fetch data from fields
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    address = request.json['address']
    settings = request.json['settings']

    #create a new camera
    camera = CameraConfigs(name,username,password,address,settings)

    #submit to database
    db.session.add(camera)
    db.session.commit()

    return 'Camera added.'
#delete camera by id
@app.route('/delete_camera/<id>', methods= ['DELETE'])
def delete_camera(id):
    camera = CameraConfigs.query.filter_by(id=id).one()
    db.session.delete(camera)
    db.session.commit()
    return 'Camera deleted.'
#update camera by id
@app.route('/edit_camera/<id>', methods= ['PUT'])
def update_camera(id):
    #Find camera
    camera = CameraConfigs.query.filter_by(id=id)

    #request new camera data
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    address = request.json['address']
    settings = request.json['settings']

    #update data on camera
    camera.update(dict(name = name,
                       username = username,
                       password = password,
                       address = address,
                       added_at = datetime.utcnow()))

    #commit to database
    db.session.commit()
    return f'Camera updated.'
