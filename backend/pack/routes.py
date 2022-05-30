
from datetime import datetime
from flask import render_template, request, Response
from pack.camera import Camera
from pack import app, video_playback_entrys
import traceback,logging,json,os,re
from queue import Queue





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






#Den nya inspelade mp4 streamern
@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response
def get_chunk(byte1=None, byte2=None):
    full_path = "~/Documents/AutoPlayback/backend/public/video/0.mp4"
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




@app.route('/playback/fetch', methods=['GET'])
def serve_playback():
    global video_playback_entrys
    return json.dumps(video_playback_entrys)









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
