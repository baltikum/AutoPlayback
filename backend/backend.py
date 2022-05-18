

from pack import app

from datetime import datetime, timedelta
import traceback

from pack.sys_variables import Sys_variables
from pack.db_models import User,Recordings,CameraConfigs
from pack.presence import Presence
from pack.load_cameras import Load_Cameras

import time
from queue import Queue


from concurrent.futures import ThreadPoolExecutor





configured_cameras = []
capturing_cameras = []
presence_active = False

thread_pool = ThreadPoolExecutor()

video_playback_entrys = [{'id':0,'name':'Vardagsrum', 'time':'20220422','file':'filnamn.mp4'}]
archived_video_playback = [] #Should be written to database


camera_queues = []
controller_queue = Queue()


def message_controller(args):
    print('MESSAGECONTROLLER STARTED')
    print('MESSAGECONTROLLER STARTED')
    print('MESSAGECONTROLLER STARTED')

    #threadqueues
    camera_queues = args[0]
    in_queue = args[1]
    #local list of received motion alarms
    motion_list = []

    #initiate a list per camera
    for _ in queues:
        motion_list.append([])

    #message distributor loop
    while True:
        try:
            #Check for incoming messages
            if in_queue.empty():
                res = False
            else:
                res = in_queue.get_nowait()

            print(res)
            print(res)
            print(res)


            #Check content of received message
            if res:
                res_json = json.loads(res)

                #Individual camera commands
                if 'index' in res_json:
                    index = int(res['index'])
                    if 'motion' in res_json:
                        motion_list[index].append(datetime.now())
                    elif 'start_recording' in res_json:
                        res = camera_queues[index].put('_start')
                    elif 'stop_recording' in res_json:
                        res = camera_queues[index].put('_stop')

                #Presence commands
                if 'presence' in res_json:
                    status = res_json['presence']
                    status = int(status)
                    if status == 1 :
                        for i, _ in enumerate(motion_list):
                            res = camera_queues[i].put('_start')
                    else:
                        for i, _ in enumerate(motion_list):
                            res = camera_queues[i].put('_stop')


            #loop distributes motion alarms
            for i, list in enumerate(motion_list):
                if len(list) > 0:
                    res = camera_queues[i].put(list.pop(0))

        except:
            traceback.print_exc()


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
        camera.msg_queue = Queue()
        camera_queues.append(camera.msg_queue)
        thread_pool.submit(camera.start_recording, (camera.msg_queue, camera) )

    #add message controller thread
    thread_pool.submit(message_controller,(camera_queues,controller_queue))


    app.run(host='localhost', port=SYSTEM_SETTINGS.FLASK_PORT, debug=True, threaded=True)
