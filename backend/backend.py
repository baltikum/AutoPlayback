

from cv2 import trace
from pack import app

from datetime import datetime, timedelta
import traceback

from pack.sys_variables import Sys_variables
from pack.db_models import User,Recordings,CameraConfigs
from pack.presence import Presence
from pack.load_cameras import Load_Cameras

from flask import request

import time, json,cv2,logging,sys
from queue import Queue


from concurrent.futures import ThreadPoolExecutor





configured_cameras = []
capturing_cameras = []
presence_active = False

thread_pool = ThreadPoolExecutor()

video_playback_entrys = [{'id':0,'name':'Vardagsrum', 'time':'20220422','file':'filnamn.mp4'}]
archived_video_playback = [] #Should be written to database


camera_out_queues = []
camera_in_queues = []
controller_queue = Queue()



def start_recording(args):

    in_queue = args[0]
    out_queue = args[1]
    camera = args[2]
    
    try:
        away_mode = False
        quit_thread = False
        motion_at = datetime.now() - timedelta(minutes=10)
        format = "%Y%m%d_%H%M%S"
    except:
        pass

    def query_msg_queue(in_queue, away_mode, motion_at, quit_thread):
        try:
            if in_queue.empty():
                res = False
            else:
                res = in_queue.get_nowait()
                #print(f'{res} was received at {in_queue}')

            if res:
                res_json = json.loads(res)
                if 'motion' in res_json:
                    motion_at = datetime.fromisoformat(res_json['motion'])
                elif 'presence' in res_json:
                    status = int(res_json['presence'])
                    if status != 1:
                        away_mode = True
                    else:
                        away_mode = False
                elif 'command' in res_json:
                    status = res_json['command']
                    if status == '_quit_thread':
                        quit_thread = True

            res = True
        except:
            res = False
            traceback.print_exc()

        return res, away_mode, motion_at, quit_thread

    def start_new_file(camera, motion_at):
        try:
            recording_started_at = motion_at.strftime(format)
            fileName = f'{recording_started_at}_{camera.camera_name}.mp4'
            codec = cv2.VideoWriter_fourcc(*'mp4v')
            fileout = cv2.VideoWriter(fileName, codec, camera.fps, (1024,  768))
            res = True
        except:
            traceback.print_exc()
            res = False
        return res,recording_started_at,fileName,fileout

    def record_video(in_queue, away_mode, motion_at, quit_thread):
        try:
            capture = cv2.VideoCapture(camera.url)
            buffer = []
            buffer_max_size = camera.fps * 3

            delay = (1.0/float(camera.fps))


            
            #Buffer awaiting motion
            while True:

                _ , frame = capture.read()
                buffer.append(frame)

                if len(buffer) > buffer_max_size :
                    buffer.pop(0)

                _, away_mode, motion_at, quit_thread = query_msg_queue(in_queue, away_mode, motion_at, quit_thread)

                if (((datetime.now() - motion_at).total_seconds() < 5)
                    or quit_thread ):
                        break
                time.sleep(delay)

        except:
            traceback.print_exc()

        res, rec_at, fileName, fileout = start_new_file(camera,motion_at)

        try:
            #Record to file loop
            while (datetime.now() - motion_at).total_seconds() < 15 :
                _ , frame = capture.read()
                buffer.append(frame)

                if len(buffer) > 0 :
                    fileout.write(buffer.pop(0))
                else:
                    fileout.write(frame)

                _, away_mode, motion_at, quit_thread = query_msg_queue(in_queue, away_mode, motion_at, quit_thread)

                time.sleep((1.0/float(camera.fps)))

            fileout.release()

            #Create recording entry
            ended_at = datetime.now()
            recording_ended_at = ended_at.strftime(format)
            video_playback_entry = ('{'
                    + f'"video_start_time": "{rec_at}",'
                    + f'"video_end_time": "{recording_ended_at}",'
                    + f'"video_camera_id": "{camera.id}",'
                    + f'"video_file": "{fileName}"'
                    + '}')
        except:
            traceback.print_exc()

        return video_playback_entry

    #Awaiting away mode
    while True:
        #Makes sure recording,queue and query is executed fully
        while True:
            _, away_mode, motion_at, quit_thread = query_msg_queue(in_queue, away_mode, motion_at, quit_thread)
            if not away_mode:
                break
            video_playback_entry = record_video(in_queue, away_mode, motion_at, quit_thread)
            out_queue.put(video_playback_entry)

        if quit_thread:
            exit(0)
        #Awaiting away mode delay
        time.sleep(5)




def message_controller(args):
    #threadqueues
    camera_out_queues = args[0]
    camera_in_queues = args[1]
    in_queue = args[2]

    #local list of received motion alarms
    motion_list = []

    #initiate a list per camera
    for _ in camera_out_queues:
        motion_list.append([])

    #message distributor loop
    while True:
        try:
            #Check for incoming messages from application
            if in_queue.empty():
                res = False
            else:
                res = in_queue.get_nowait()


            #Check for incoming messages from cameras
            for q in camera_in_queues:
                if q.empty():
                    ret = False
                else:
                    ret = q.get_nowait()
                    break

            if ret:
                pass
                #print(ret)
                #Stoppa i databsen


            #Check content of received message
            if res:
                res_json = json.loads(res)

                #Individual camera commands
                if 'index' in res_json:
                    index = int(res['index'])
                    if 'motion' in res_json:
                        motion_list[index].append(datetime.now())
                    

                #Presence and quit commands distribution
                if 'presence' or 'command' in res_json:
                    for i, _ in enumerate(motion_list):
                        _ = camera_out_queues[i].put(res)
                       # print(f'{res} was put at {camera_out_queues[i]}')



            #loop distributes motion alarms
            for i, list in enumerate(motion_list):
                if len(list) > 0:
                    res = camera_out_queues[i].put(list.pop(0))

            time.sleep(0.1)
        except:
            traceback.print_exc()


#Receiving from presence module
@app.route('/presence', methods=['POST'])
def presence_detected():
    try:
        res = request.json
        status = str(res['presence'])
    except:
        logging.critical('Presence detection failed, incoming not recognized.')

    try:
        if status =='active': #Home
            presence_data = '{ "presence" : "1" }'
            _ = controller_queue.put(presence_data)
            res = True
        else : #Away
            presence_data = '{ "presence" : "0" }'
            controller_queue.put(presence_data)
            res = False
    except:
        logging.error('Presence failed to queue message to threads')

    return '{ "presence" : "' + str(res) + '" }'

@app.route('/motion', methods=['POST'])
def motion_id():
    try:
        data = request.json
        motion_data = '{"index":"' + str(data['index']) + '"}'
        res = controller_queue.put(motion_data)
    except:
        res = False
        traceback.print_exc()

    return '{ "response" : "' + res + '" }'

if __name__ == '__main__':


    SYSTEM_SETTINGS = Sys_variables()
    system_cameras = Load_Cameras(SYSTEM_SETTINGS)

    if not SYSTEM_SETTINGS.cameras_configured :
        try:
            for camera in system_cameras.loaded_cameras:
                camera.configure_camera()

            SYSTEM_SETTINGS.cameras_configured = True
        except:
            traceback.print_exc()



    #Presence controller thread
    #pre = Presence('72:85:fd:64:a4:87',10)
    #res, trace = pre.configure_presence()
    #thread_pool.submit(pre.run_presence)

    #add camera recording threads
    for camera in system_cameras.loaded_cameras:
        camera_out_queue = Queue()
        camera_in_queue = Queue()
        camera_out_queues.append(camera_out_queue)
        camera_in_queues.append(camera_in_queue)
        thread_pool.submit(start_recording, [camera_out_queue,camera_in_queue, camera] )

  
    #add message controller thread
    thread_pool.submit(message_controller,[camera_out_queues,camera_in_queues,controller_queue])

    
    presence_data = '{ "presence" : "0" }'
    controller_queue.put(presence_data)

    app.run(host='localhost', port=SYSTEM_SETTINGS.FLASK_PORT, debug=True, threaded=True, use_reloader=False)
